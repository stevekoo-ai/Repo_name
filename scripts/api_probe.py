"""전체 데이터 소스 API 생존 프로브 — "다 찔러보기" 진단 도구.

2026-09-07 사용자 요청("fred든 뭐든 API를 다 찔러봐")으로 만든 단발성
진단 스크립트. 이 저장소가 키를 들고 있거나 config/api.yaml에 등록해둔
모든 외부 데이터 소스에 **최소 1회씩만** 호출을 날려, 지금 이 순간
무엇이 살아 있고 무엇이 죽어 있고 어떤 키가 놀고 있는지를 한 표로 만든다.

왜 필요한가: 이 저장소는 소스가 죽어도 파이프라인을 멈추지 않도록
설계돼 있다(7.9/19.2 — 키 없으면 PENDING, 실패해도 리포트는 나감).
그 설계 덕에 **소스 하나가 몇 달째 죽어 있어도 아무도 모른다**. 실제로
이 프로브를 만들면서 BLS_API_KEY가 두 워크플로에 주입되는데 이를 쓰는
코드가 저장소에 단 한 줄도 없다는 걸 발견했다. 이 스크립트는 그런
"조용한 공백"을 정기적으로 드러내기 위한 것이다.

원칙:
- **기존에 성공한 코드 경로를 재사용한다**(wiki/CLAUDE.md 최우선 원칙).
  ECOS/KOSIS/FRED는 collectors의 fetch_series를 그대로 부르고, MOLIT
  계열은 각 모듈의 _fetch_region_month를 부른다 — 프로브 전용으로 API
  호출을 다시 짜면 "프로브는 되는데 실제 수집은 안 되는"(또는 그 반대의)
  거짓 신호가 나온다.
- **최소 호출**: 소스당 1회. 지역 전수 조회나 10년 백필은 하지 않는다.
- **키가 없으면 실패가 아니라 skipped**: 키 미설정과 API 장애를 구분해
  보고한다(R3 — 미수집은 판정이 아니다).
- **KIS는 기본적으로 건너뛴다**: KIS는 같은 appkey로 단시간 내 토큰을
  재발급하면 403을 뱉고, 그 사고가 실제로 3일 연속 워크플로 실패를
  일으킨 적이 있다(wiki/CLAUDE.md 8-3). 프로브가 일일 수집을 망가뜨리면
  안 되므로 PROBE_KIS=1 을 명시적으로 줄 때만 찌른다.

로컬 실행은 대부분 실패한다(에이전트 프록시가 FRED 등 외부 도메인을
막는다) — GitHub Actions(.github/workflows/api-probe.yml)에서 돌리는 것이
정상 사용법이다.

사용:
    PYTHONPATH=. python3 scripts/api_probe.py            # 표 + JSON 출력
    PROBE_KIS=1 PYTHONPATH=. python3 scripts/api_probe.py  # KIS 토큰까지
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import requests  # noqa: E402

from core.config import api_config, get_api_key  # noqa: E402

TIMEOUT = 20

# 상태 코드 — 표와 JSON에서 같은 어휘를 쓴다.
ALIVE = "ALIVE"      # 호출 성공 + 실제 값 확인
EMPTY = "EMPTY"      # 호출은 성공했으나 데이터가 비어 있음(장애일 수도, 정상일 수도)
DEAD = "DEAD"        # 호출 실패(네트워크/인증/에러 응답)
SKIPPED = "SKIPPED"  # 키 미설정 등으로 시도 자체를 안 함 — 실패가 아님


def _last_month_yyyymm() -> str:
    today = datetime.now(timezone.utc)
    first = today.replace(day=1)
    return (first - timedelta(days=1)).strftime("%Y%m")


# --------------------------------------------------------------------------
# 개별 프로브 — 각각 (status, detail) 반환. 예외는 호출자가 잡아 DEAD로 기록.
# --------------------------------------------------------------------------

def probe_fred_csv() -> tuple[str, str]:
    """키 없이 도는 CSV 엔드포인트 — 이 저장소의 FRED 기본 경로."""
    from collectors import fred
    resp = requests.get(
        fred.FRED_CSV_URL, params={"id": "DGS10"},
        headers=fred._HEADERS, timeout=TIMEOUT,
    )
    resp.raise_for_status()
    lines = [ln for ln in resp.text.strip().splitlines() if ln]
    if len(lines) < 2:
        return EMPTY, "CSV 응답에 데이터 행 없음"
    return ALIVE, f"DGS10 마지막 행: {lines[-1]} (총 {len(lines) - 1}행)"


def probe_fred_api() -> tuple[str, str]:
    """FRED_API_KEY를 쓰는 공식 REST 경로 — CSV가 막혔을 때의 폴백."""
    key = get_api_key("fred")
    if not key:
        return SKIPPED, "FRED_API_KEY 미설정 (CSV 경로가 기본이라 정상)"
    from collectors import fred
    resp = requests.get(
        fred.FRED_API_URL,
        params={"series_id": "DGS10", "api_key": key, "file_type": "json",
                "sort_order": "desc", "limit": 1},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    obs = resp.json().get("observations", [])
    if not obs:
        return EMPTY, "observations 비어 있음"
    return ALIVE, f"DGS10 최신: {obs[0].get('date')} = {obs[0].get('value')}"


def probe_fred_fx() -> tuple[str, str]:
    """오늘 macro_data.py PRESETS에 추가한 3개 환율 시리즈가 실제로 응답하는지."""
    from collectors import fred
    out = []
    for sid in ("DEXKOUS", "DEXJPUS", "DEXCHUS"):
        resp = requests.get(fred.FRED_CSV_URL, params={"id": sid},
                            headers=fred._HEADERS, timeout=TIMEOUT)
        if resp.status_code != 200:
            out.append(f"{sid}=HTTP{resp.status_code}")
            continue
        lines = [ln for ln in resp.text.strip().splitlines() if ln]
        out.append(f"{sid}={lines[-1] if len(lines) > 1 else '빈응답'}")
    status = ALIVE if all("HTTP" not in o and "빈응답" not in o for o in out) else EMPTY
    return status, "; ".join(out)


def probe_ecos() -> tuple[str, str]:
    if not get_api_key("ecos"):
        return SKIPPED, "ECOS_API_KEY 미설정"
    from collectors import ecos
    dp = ecos.fetch_series("base_rate")
    if getattr(dp, "value", None) is None:
        return EMPTY, f"status={getattr(dp, 'status', '?')} — 값 없음"
    return ALIVE, f"기준금리 {dp.value} (as_of={getattr(dp, 'as_of', '?')})"


def probe_kosis() -> tuple[str, str]:
    if not get_api_key("kosis"):
        return SKIPPED, "KOSIS_API_KEY 미설정"
    from collectors import kosis
    dp = kosis.fetch_series("cpi_index")
    if getattr(dp, "value", None) is None:
        # 2026-09-07 프로브 실측으로 기존 진단이 뒤집혔다: collectors/kosis.py 상단
        # 주석은 "kosis.kr TCP connect timeout, 한국 IP 제한 의심"이라고 적고 있지만,
        # 실제 응답은 "해당 통계표가 존재하지 않습니다" — 서버는 살아 있고 인증도
        # 통과했으며 **통계표 ID(tblId/itmId)가 틀린 것**이다. 네트워크 문제가
        # 아니므로 KOSIS 콘솔에서 통계표 좌표만 다시 확인하면 살릴 수 있다.
        return EMPTY, f"status={getattr(dp, 'status', '?')} — 값 없음 (원인은 네트워크가 아니라 통계표 ID 오류)"
    return ALIVE, f"CPI지수 {dp.value} (as_of={getattr(dp, 'as_of', '?')})"


def _probe_molit_like(module_name: str, label: str) -> tuple[str, str]:
    """MOLIT 계열 4종 공통 — 강남구(11680) 지난달 1개월치만 최소 조회."""
    key = get_api_key("molit")
    if not key:
        return SKIPPED, "DATA_GO_KR_KEY 미설정"
    import importlib
    mod = importlib.import_module(f"collectors.{module_name}")
    rows = mod._fetch_region_month("11680", _last_month_yyyymm(), key)
    if not rows:
        return EMPTY, f"{label}: 강남구 {_last_month_yyyymm()} 거래 0건 (승인 문제 아닐 수 있음)"
    return ALIVE, f"{label}: 강남구 {_last_month_yyyymm()} {len(rows)}건, 샘플 키={sorted(rows[0])[:6]}"


def probe_molit_apt() -> tuple[str, str]:
    return _probe_molit_like("molit", "아파트매매")


def probe_molit_rent() -> tuple[str, str]:
    return _probe_molit_like("molit_rent", "아파트전월세")


def probe_molit_villa() -> tuple[str, str]:
    return _probe_molit_like("molit_villa", "연립다세대매매")


def probe_molit_officetel() -> tuple[str, str]:
    return _probe_molit_like("molit_officetel", "오피스텔매매")


def probe_customs_trade() -> tuple[str, str]:
    if not get_api_key("customs_trade"):
        return SKIPPED, "DATA_GO_KR_KEY 미설정"
    from collectors import customs_trade
    ym = _last_month_yyyymm()
    rows = customs_trade._fetch_year_window(ym, ym, get_api_key("customs_trade"))
    if not rows:
        return EMPTY, f"{ym} 수출입 실적 0건"
    # _fetch_year_window은 원시 XML 필드명(year/expDlr)이 아니라 정규화된 키
    # (date/exp_dlr/imp_dlr)로 dict를 만들어 돌려준다 — 첫 실행에서 원시 필드명을
    # 읽다가 전부 None이 나왔다. 프로브가 수집 코드의 실제 반환 형태를 따라가야 한다.
    r = rows[-1]
    return ALIVE, f"{r.get('date')} 수출 {r.get('exp_dlr'):,.0f} / 수입 {r.get('imp_dlr'):,.0f} 달러"


def probe_bls() -> tuple[str, str]:
    """BLS_API_KEY는 두 워크플로에 주입되지만 이를 쓰는 코드가 저장소에
    한 줄도 없다(2026-09-07 확인). 키가 실제로 유효한지, 무엇을 받을 수
    있는지를 여기서 처음으로 확인한다 — CUUR0000SA0 = US CPI-U 전체."""
    cfg = api_config()["sources"]["bls"]
    key = get_api_key("bls")
    body = {"seriesid": ["CUUR0000SA0"], "startyear": str(datetime.now().year - 1),
            "endyear": str(datetime.now().year)}
    if key:
        body["registrationkey"] = key
    resp = requests.post(cfg["base_url"], json=body, timeout=TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("status") != "REQUEST_SUCCEEDED":
        return DEAD, f"status={payload.get('status')} msg={payload.get('message')}"
    series = payload.get("Results", {}).get("series", [])
    data = series[0].get("data", []) if series else []
    if not data:
        return EMPTY, "series는 왔으나 data 비어 있음"
    d = data[0]
    tag = "키 사용" if key else "키 없이(v2 무료 한도)"
    return ALIVE, f"[{tag}] CPI-U {d.get('year')}-{d.get('period')} = {d.get('value')} (총 {len(data)}개월)"


def probe_imf() -> tuple[str, str]:
    """config/api.yaml에 등록돼 있으나 collectors에 구현이 없는 소스 — 살아 있는지만 확인."""
    base = api_config()["sources"]["imf"]["base_url"]
    resp = requests.get(f"{base}/NGDP_RPCH/KOR", timeout=TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()
    values = payload.get("values", {}).get("NGDP_RPCH", {}).get("KOR", {})
    if not values:
        return EMPTY, "응답은 왔으나 KOR 실질GDP성장률 값 없음"
    latest = sorted(values)[-1]
    return ALIVE, f"KOR 실질GDP성장률 {latest} = {values[latest]} (미구현 소스, 연도 {sorted(values)[0]}~{latest})"


def probe_oecd() -> tuple[str, str]:
    """OECD SDMX — config엔 있으나 collectors 미구현. FRED가 OECD 미러를 이미
    제공(kr_cpi_oecd 등)해서 굳이 안 쓰고 있었던 것으로 보인다."""
    base = api_config()["sources"]["oecd"]["base_url"]
    url = f"{base}/OECD.SDD.STES,DSD_STES@DF_CLI,/KOR.M.LI...AA...H"
    resp = requests.get(url, params={"format": "csvfile", "lastNObservations": 1},
                        headers={"Accept": "text/csv"}, timeout=TIMEOUT)
    if resp.status_code != 200:
        return DEAD, f"HTTP {resp.status_code}: {resp.text[:150]}"
    lines = [ln for ln in resp.text.strip().splitlines() if ln]
    if len(lines) < 2:
        return EMPTY, "CSV 헤더만 옴"
    return ALIVE, f"KOR CLI 최신행 있음 ({len(lines) - 1}행)"


def _probe_kis_account(appkey_env: str, secret_env: str, label: str) -> tuple[str, str]:
    """KIS 토큰 발급 — 재발급 제한(403) 사고 이력 때문에 기본 비활성."""
    if os.environ.get("PROBE_KIS") != "1":
        return SKIPPED, "PROBE_KIS=1 아님 — KIS 토큰 재발급 제한(403) 사고 방지로 기본 생략"
    appkey, secret = os.environ.get(appkey_env), os.environ.get(secret_env)
    if not appkey or not secret:
        return SKIPPED, f"{appkey_env}/{secret_env} 미설정"
    resp = requests.post(
        "https://openapi.koreainvestment.com:9443/oauth2/tokenP",
        json={"grant_type": "client_credentials", "appkey": appkey, "appsecret": secret},
        timeout=TIMEOUT,
    )
    if resp.status_code != 200:
        return DEAD, f"HTTP {resp.status_code}: {resp.text[:200]}"
    data = resp.json()
    if not data.get("access_token"):
        return DEAD, f"토큰 없음: {str(data)[:200]}"
    return ALIVE, f"{label} 토큰 발급 성공 (만료 {data.get('access_token_token_expired')})"


def probe_kis_gen() -> tuple[str, str]:
    return _probe_kis_account("KIS_APP_KEY", "KIS_APP_SECRET", "일반계좌")


def probe_kis_irp() -> tuple[str, str]:
    return _probe_kis_account("KIS_APP_KEY_IRP", "KIS_APP_SECRET_IRP", "IRP계좌")


def probe_kis_isp() -> tuple[str, str]:
    return _probe_kis_account("KIS_APP_KEY_ISP", "KIS_APP_SECRET_ISP", "ISA계좌")


PROBES: list[tuple[str, str, callable]] = [
    ("fred_csv", "FRED (키리스 CSV, 기본 경로)", probe_fred_csv),
    ("fred_api", "FRED (REST API, 폴백)", probe_fred_api),
    ("fred_fx", "FRED 환율 3종 (DEXKOUS/JPUS/CHUS)", probe_fred_fx),
    ("ecos", "한국은행 ECOS", probe_ecos),
    ("kosis", "통계청 KOSIS", probe_kosis),
    ("molit_apt", "국토부 아파트매매 실거래", probe_molit_apt),
    ("molit_rent", "국토부 아파트전월세 실거래", probe_molit_rent),
    ("molit_villa", "국토부 연립다세대 실거래", probe_molit_villa),
    ("molit_officetel", "국토부 오피스텔 실거래", probe_molit_officetel),
    ("customs_trade", "관세청 수출입총괄", probe_customs_trade),
    ("bls", "US BLS (미사용 키 검증)", probe_bls),
    ("imf", "IMF WEO (미구현 소스)", probe_imf),
    ("oecd", "OECD SDMX (미구현 소스)", probe_oecd),
    ("kis_gen", "KIS 일반계좌 토큰", probe_kis_gen),
    ("kis_irp", "KIS IRP계좌 토큰", probe_kis_irp),
    ("kis_isp", "KIS ISA계좌 토큰", probe_kis_isp),
]


def run_all() -> list[dict]:
    results = []
    for key, label, fn in PROBES:
        started = time.time()
        try:
            status, detail = fn()
        except Exception as exc:  # noqa: BLE001 — 프로브는 어떤 실패든 기록만 하고 계속 간다
            status = DEAD
            detail = f"{type(exc).__name__}: {str(exc)[:300]}"
            if os.environ.get("PROBE_TRACEBACK") == "1":
                traceback.print_exc()
        elapsed = time.time() - started
        results.append({
            "key": key, "label": label, "status": status,
            "latency_s": round(elapsed, 2), "detail": detail,
        })
        print(f"[{status:7s}] {elapsed:6.2f}s  {label}\n            {detail}", flush=True)
    return results


def main() -> int:
    print(f"=== API PROBE {datetime.now(timezone.utc).isoformat()} ===\n", flush=True)
    results = run_all()

    print("\n=== 요약 표 (마크다운) ===\n")
    print("| 소스 | 상태 | 응답(초) | 내용 |")
    print("|---|---|---|---|")
    for r in results:
        detail = r["detail"].replace("|", "\\|").replace("\n", " ")
        print(f"| {r['label']} | {r['status']} | {r['latency_s']} | {detail} |")

    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("\n집계: " + ", ".join(f"{k} {v}건" for k, v in sorted(counts.items())))

    print("\n=== JSON ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))

    # DEAD가 있어도 종료코드는 0 — 이건 진단 도구지 게이트가 아니다.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
