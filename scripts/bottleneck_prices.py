#!/usr/bin/env python3
"""병목 이동 추적용 주가 수집 → sources/bottleneck-prices.csv.

수집 대상 티커는 data/manual_inputs/bottleneck_rotation.yaml 한 곳에서만
정한다(바스켓·수단·비교기준 전부의 합집합) — 목록이 두 벌이면 갈라진다.

macro-series.csv에 섞지 않는 이유: 그 파일은 거시지표 소비처(환율 엔진,
주간 분석, 브리핑 원장 등)가 여럿이라 개별 종목 20개를 끼워 넣으면 그쪽
집계·스테일 판정이 오염된다.

Yahoo 접근은 macro_data.yahoo_chart()를 재사용한다(2026-09-18 Actions
프로브로 러너에서 동작 검증된 경로). 한 종목 실패로 전체가 죽지 않고,
전부 실패했을 때만 exit 1 한다 — 워크플로 재시도 루프가 그걸 보고 돈다.
"""
from __future__ import annotations

import csv
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro_data  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "data" / "manual_inputs" / "bottleneck_rotation.yaml"
OUT = REPO / "sources" / "bottleneck-prices.csv"
FIELDS = ["ticker", "date", "close", "name", "currency", "fetched_at"]
LOOKBACK_DAYS = 420  # 120일선 + 3개월 수익률 + 1주 지속 확인에 충분


def tickers_from_config(cfg: dict) -> list[str]:
    out: set[str] = set()

    def add_signal_tickers(sig: dict) -> None:
        if sig.get("type") in ("rel_return", "ma_position"):
            out.update(sig.get("basket") or [])
            if sig.get("vs"):
                out.add(sig["vs"])

    inc = cfg.get("incumbent") or {}
    if inc.get("leader"):
        out.add(inc["leader"]["ticker"])
    for s in inc.get("signals") or []:
        add_signal_tickers(s)
    for c in cfg.get("candidates") or []:
        out.update(c.get("basket") or [])
        for group in ("etf", "leaders"):
            for ins in (c.get("instruments") or {}).get(group) or []:
                out.add(ins["ticker"])
        for s in c.get("signals") or []:
            add_signal_tickers(s)
    return sorted(out)


def _read() -> dict[tuple[str, str], dict]:
    if not OUT.exists():
        return {}
    with OUT.open(encoding="utf-8") as fh:
        return {(r["ticker"], r["date"]): r for r in csv.DictReader(fh)}


def _write(rows: dict[tuple[str, str], dict]) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for k in sorted(rows):
            w.writerow(rows[k])


def main() -> int:
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    tickers = tickers_from_config(cfg)
    start = (date.today() - timedelta(days=LOOKBACK_DAYS)).isoformat()
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    rows = _read()
    ok, failed = [], []
    for t in tickers:
        try:
            bars, meta = macro_data.yahoo_chart(t, start=start)
        except RuntimeError as e:
            failed.append(t)
            print(f"✗ {t}: {e}", file=sys.stderr)
            continue
        name = meta.get("longName") or meta.get("shortName") or ""
        cur = meta.get("currency") or ""
        for d, close in bars:
            rows[(t, d)] = {"ticker": t, "date": d, "close": close, "name": name,
                            "currency": cur, "fetched_at": fetched_at}
        ok.append(t)
        # 이름을 로그에 남긴다 — 설정의 verify: true 티커(한국 ETF·도쿄 상장)가
        # 의도한 종목인지 이 한 줄로 실측 확인한다.
        print(f"✓ {t}: {name} ({cur}) {len(bars)}일, 최신 {bars[-1][0]} = {bars[-1][1]}")

    if ok:
        _write(rows)
    print(f"\n성공 {len(ok)}/{len(tickers)}" + (f", 실패: {', '.join(failed)}" if failed else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
