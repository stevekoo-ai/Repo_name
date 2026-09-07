"""Shared collector plumbing: retry, raw-tier storage, normalized-tier storage.

Storage layout (Master Instruction 7.4, 7.5):
  data/raw/<source>/<series_id>__<fetched_at>.json   -- immutable, one file per fetch
  data/normalized/<series_id>.csv                     -- tidy (date, value) rows, deduped by date

Raw files are never edited or overwritten — each fetch writes a new
timestamped file, so initial/revised/final releases are all preserved
(7.5's revision requirement).
"""
from __future__ import annotations

import json
import re
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, TypeVar

import pandas as pd
import requests

from core.logger import log_event

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"
NORMALIZED_DIR = REPO_ROOT / "data" / "normalized"

T = TypeVar("T")

_SECRET_QUERY_PARAM = re.compile(r"(?i)([?&](?:service[_-]?key|api[_-]?key|key|token|secret)=)[^&\s]+")


def redact_url(url: str) -> str:
    """Mask API-key/token-shaped query params in a URL.

    requests.exceptions.HTTPError embeds the full request URL — including query
    string — in its message (`"... for url: {resp.url}"`). Every collector that
    authenticates via a `?serviceKey=`/`?apiKey=`-style query param (MOLIT, FRED,
    KOSIS) would otherwise leak the raw key into anything that logs or surfaces
    str(exc) — which for MOLIT specifically means the committed, public
    report/<month>.md `fetch_note` text, not just an ephemeral log line. See
    raise_for_status() below, the actual call site for this.
    """
    return _SECRET_QUERY_PARAM.sub(r"\1***", url)


def raise_for_status(resp: requests.Response) -> None:
    """Like resp.raise_for_status(), but with API keys/tokens stripped from the
    exception message via redact_url() — safe to log or embed in report text."""
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        raise requests.exceptions.HTTPError(redact_url(str(exc)), response=resp) from None


def retry(fn: Callable[[], T], attempts: int = 3, backoff_seconds: float = 1.5, label: str = "") -> T | None:
    """Retry `fn` with linear backoff. Returns None (does not raise) after exhausting attempts.

    Every attempt and the final outcome are logged per 19.1 (API Retry).
    """
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            result = fn()
            if attempt > 1:
                log_event("collector.retry_succeeded", label=label, attempt=attempt)
            return result
        except Exception as exc:  # collectors must never crash the pipeline
            last_exc = exc
            log_event(
                "collector.fetch_failed",
                level="warning",
                label=label,
                attempt=attempt,
                error=str(exc),
            )
            if attempt < attempts:
                time.sleep(backoff_seconds * attempt)
    log_event("collector.fetch_exhausted", level="error", label=label, error=str(last_exc))
    return None


def write_raw(source: str, series_id: str, payload: Any) -> Path:
    """Persist an immutable raw snapshot. Returns the path written."""
    source_dir = RAW_DIR / source
    source_dir.mkdir(parents=True, exist_ok=True)
    fetched_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = source_dir / f"{series_id}__{fetched_at}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, default=str, indent=2), encoding="utf-8")
    log_event("collector.raw_saved", source=source, series_id=series_id, path=str(path))
    return path


def latest_raw(source: str, series_id: str) -> Any | None:
    """Read back the most recent raw snapshot for a series, if any."""
    source_dir = RAW_DIR / source
    if not source_dir.exists():
        return None
    candidates = sorted(source_dir.glob(f"{series_id}__*.json"))
    if not candidates:
        return None
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


def append_normalized(series_id: str, rows: list[dict]) -> pd.DataFrame:
    """Append (date, value) rows to the normalized-tier CSV for a series, deduped by date.

    `rows` items must have at least {"date": iso-date-str, "value": float}.
    """
    NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)
    path = NORMALIZED_DIR / f"{series_id}.csv"
    new_df = pd.DataFrame(rows)
    if new_df.empty:
        return new_df
    new_df["date"] = pd.to_datetime(new_df["date"]).dt.date.astype(str)

    if path.exists() and path.stat().st_size > 0:
        existing = pd.read_csv(path)
        existing["date"] = existing["date"].astype(str)
        combined = pd.concat([existing, new_df], ignore_index=True)
    else:
        combined = new_df

    combined = combined.drop_duplicates(subset=["date"], keep="last").sort_values("date").reset_index(drop=True)
    combined.to_csv(path, index=False)
    log_event("collector.normalized_saved", series_id=series_id, rows=len(combined))
    return combined


def read_normalized(series_id: str) -> pd.DataFrame:
    path = NORMALIZED_DIR / f"{series_id}.csv"
    if not path.exists():
        return pd.DataFrame(columns=["date", "value"])
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def as_date_value_tuples(df: pd.DataFrame) -> list[tuple[date, float]]:
    return [(row.date, float(row.value)) for row in df.itertuples() if pd.notna(row.value)]


def series_change_over_rows(series_id: str, offset_rows: int) -> tuple[float, float] | tuple[None, None]:
    """(latest, value `offset_rows` rows earlier) for a normalized series.

    Used for daily/irregular-cadence series (FX, yields) where a fixed row
    offset approximates a calendar window better than the monthly-cadence
    assumption in core.utils.compute_trend.
    """
    df = read_normalized(series_id)
    if df.empty or len(df) <= offset_rows:
        return None, None
    s = df.sort_values("date")["value"]
    return float(s.iloc[-1]), float(s.iloc[-1 - offset_rows])


# --------------------------------------------------------------------------
# data.go.kr(공공데이터포털) 응답 파서 — JSON/XML 양쪽 모두 처리
# --------------------------------------------------------------------------
#
# 2026-09-07 API 전수 프로브(scripts/api_probe.py, Actions run 34126443827)로
# 드러난 장애를 고치며 신설. 증상: MOLIT 4종(아파트매매·전월세·빌라·오피스텔)이
# 전부 실패하고 있었는데, 각 모듈의 에러 메시지는 "likely a service/auth error"
# 라고 오진하고 있었다. 실제 응답은 resultCode 000 / OK 에 진짜 거래 데이터가
# 들어 있는 **정상 응답**이었고, 유일한 문제는 `type=json`을 요청했는데도
# 서버가 XML로 돌려준다는 것이었다 — resp.json()이 ValueError를 내고 그게
# 인증 오류로 둔갑했다.
#
# 피해가 조용했던 이유: 각 모듈의 서킷브레이커가 이 예외를 잡아
# {"status": "source_error"}를 *리턴*만 하고 프로세스는 0으로 끝나서,
# real-estate-sync.yml이 234회 연속 "success"로 초록불을 켰다. 그동안
# data/normalized/molit_* 는 2026-08-11 이후 한 줄도 안 늘었다.
#
# 그래서 이 파서는 **형식을 신뢰하지 않는다**. Content-Type도 믿지 않고
# (data.go.kr은 XML을 주면서 application/json을 붙이는 경우가 있다) 본문을
# 실제로 파싱해본다. JSON이면 JSON으로, 아니면 XML로 — 어느 쪽이든 같은
# list[dict]가 나온다. 앞으로 data.go.kr이 형식을 또 바꿔도 조용히 죽지 않는다.

_DATA_GO_KR_OK_CODES = (None, "00", "000", "0")


def _xml_item_to_dict(item) -> dict[str, Any]:
    """<item> 엘리먼트의 자식들을 {태그: 텍스트} dict로. 값은 전부 문자열이지만,
    호출부(_price_per_pyeong 등)가 이미 float(str(...).replace(",","")) 패턴이라
    JSON 경로와 동작이 같다. 빈 엘리먼트(<aptDong> </aptDong>)는 ""로 정규화."""
    return {child.tag: (child.text or "").strip() for child in item}


def parse_data_go_kr_items(resp: requests.Response, label: str) -> list[dict[str, Any]]:
    """data.go.kr OpenAPI 응답에서 item 리스트를 뽑는다 (JSON/XML 무관).

    resultCode가 성공 코드가 아니면 RuntimeError를 던진다 — 이건 진짜 오류이고,
    형식 문제와 구분돼야 한다(과거엔 둘이 뒤섞여 원인을 못 찾았다).
    거래가 0건이면 빈 리스트를 돌려준다 — 오류가 아니다.
    """
    import xml.etree.ElementTree as ET

    text = resp.text
    payload = None
    try:
        payload = resp.json()
    except ValueError:
        payload = None

    if isinstance(payload, dict):
        # JSON 경로. 이 API군의 JSON은 {"header":..., "body":...} 평면 구조지만
        # 일부 상품은 "response"로 한 겹 감싼다 — 둘 다 지원.
        envelope = payload.get("response", payload)
        header = envelope.get("header", {})
        code = header.get("resultCode")
        if code is None and "body" not in envelope:
            # 이 API군의 봉투가 아니다. 여기서 조용히 []를 돌려주면 "거래 0건"으로
            # 둔갑해 또 한 번의 조용한 실패가 된다 — 알 수 없는 응답은 알 수 없다고 말한다.
            raise RuntimeError(
                f"{label}: data.go.kr 응답 형식이 아님(header/body 없음): {redact_url(text[:300])}"
            )
        if code not in _DATA_GO_KR_OK_CODES:
            raise RuntimeError(f"{label} 오류 응답 resultCode={code}: {header.get('resultMsg')}")
        items = (envelope.get("body") or {}).get("items")
        if not items:
            return []
        rows = items.get("item", []) if isinstance(items, dict) else items
        if isinstance(rows, dict):
            return [rows]
        return rows if isinstance(rows, list) else []

    # XML 경로.
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        # JSON도 XML도 아니면 그때는 진짜로 알 수 없는 응답이다 — 본문을 보여주되
        # 키가 echo될 수 있으니 방어적으로 마스킹.
        raise RuntimeError(
            f"{label}: JSON도 XML도 아닌 응답 ({exc}): {redact_url(text[:300])}"
        ) from None

    # data.go.kr 게이트웨이는 서비스에 도달하기 *전에* 요청을 거절할 때 본 응답과
    # 전혀 다른 봉투를 쓴다: <OpenAPI_ServiceResponse><cmmMsgHeader><errMsg>...
    # 이건 인증키가 유효하지만 **이 상품에 활용신청 승인이 안 된** 경우의 대표
    # 시그니처다(data.go.kr 승인은 키 단위가 아니라 상품 단위). 아래 일반
    # "형식이 아님" 오류로 뭉뚱그리면 원인 진단이 다시 어려워지므로 따로 잡는다.
    gateway_err = root.findtext(".//cmmMsgHeader/errMsg")
    if gateway_err:
        detail = root.findtext(".//cmmMsgHeader/returnAuthMsg") or ""
        raise RuntimeError(
            f"{label}: data.go.kr 게이트웨이 거절 — {gateway_err} {detail}".strip()
            + " (인증키가 이 상품에 활용신청 승인됐는지 확인할 것 — 승인은 상품 단위)"
        )

    code = root.findtext("header/resultCode")
    if code is None and not root.findall(".//items"):
        # XML로 "파싱은 되지만" data.go.kr 봉투가 아닌 경우 — 대표적으로 게이트웨이가
        # 끼워넣는 HTML 오류 페이지(<html>502 Bad Gateway</html>)가 그렇다. 이건
        # ElementTree 기준으론 멀쩡한 XML이라, 형식만 보고 넘어가면 resultCode도
        # items도 없는 채로 빈 리스트가 나가 "거래 0건"으로 오독된다.
        raise RuntimeError(
            f"{label}: data.go.kr 응답 형식이 아님(resultCode/items 없음): {redact_url(text[:300])}"
        )
    if code not in _DATA_GO_KR_OK_CODES:
        msg = root.findtext("header/resultMsg", default="(메시지 없음)")
        raise RuntimeError(f"{label} 오류 응답 resultCode={code}: {msg}")

    return [_xml_item_to_dict(item) for item in root.findall(".//items/item")]
