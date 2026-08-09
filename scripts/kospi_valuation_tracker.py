#!/usr/bin/env python3
"""KOSPI forward P/E 근사치 daily tracker.

배경: 2026-08-09 사용자 제보 차트(Goldman Sachs Global Investment Research,
데이터 Quantiwise)가 2026-07-02 기준 KOSPI 12개월 선행(forward) PER을
6.65배(-2.7 표준편차, GFC 이후 최저)로 표시. 이 forward PER은 애널리스트
컨센서스 EPS 추정치가 필요해 무료 API로 직접 구할 수 없다
(sources/kospi-forward-per-band-chart-2026-08-09.md 참고).

이 스크립트는 그 한계를 인정한 채로, "forward EPS(분모)가 앵커 시점 이후
크게 변하지 않았다"는 가정 하에 KOSPI 지수 변화율(분자)만으로 근사
forward PE를 역산한다:

    approx_forward_pe(t) = ANCHOR_PE * KOSPI(t) / ANCHOR_KOSPI

⚠️ 이건 정밀치가 아니라 방향성 참고용 근사치다. 앵커 자체도 2026-07-02
09:51 KST 장중 스냅샷(뉴스 보도, 종가 아님)이라 오차가 있고, 어닝시즌
(예: SK하이닉스 7/29 실적발표) 이후 실제 컨센서스 EPS가 리비전됐다면
이 근사치는 실제 Quantiwise 값과 갈수록 벌어질 수 있다. 상세 근거·출처는
wiki/concepts/rally-justification-analysis.md "코스피 지수 전체 밸류에이션
맥락" 섹션 참고.

Usage:
    python3 scripts/kospi_valuation_tracker.py update
        sources/kr-index-quote.csv를 읽어 근사치를 계산하고
        sources/kospi-forward-pe-approx.csv에 upsert.

    python3 scripts/kospi_valuation_tracker.py update --raw
        계산 결과만 표준출력에 출력(파일 저장 안 함).
"""
import argparse
import csv
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_QUOTE_CSV = os.path.join(BASE_DIR, "sources", "kr-index-quote.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "sources", "kospi-forward-pe-approx.csv")

# --- 앵커 (2026-08-09 인제스트, sources/kospi-forward-per-band-chart-2026-08-09.md) ---
ANCHOR_DATE = "2026-07-02"
ANCHOR_NOTE = "09:51 KST 장중 스냅샷(뉴스 보도), 정확한 종가 아님"
ANCHOR_KOSPI = 7769.16
ANCHOR_FORWARD_PE = 6.65
ANCHOR_SD = -2.7
MEAN_PE_20Y = 10.0
SD1_UPPER = 11.2
SD1_LOWER = 8.8

OUTPUT_FIELDS = [
    "date", "kospi_level", "approx_forward_pe", "pct_of_anchor_pe",
    "vs_20y_mean", "band_position", "method", "anchor_date", "caveat",
]


def _read_index_quote_rows():
    """sources/kr-index-quote.csv에서 KOSPI(index_code=0001) 행만 읽는다."""
    rows = []
    if not os.path.exists(INDEX_QUOTE_CSV):
        raise SystemExit(f"입력 파일 없음: {INDEX_QUOTE_CSV}")
    with open(INDEX_QUOTE_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("index_code") == "0001":
                rows.append(row)
    return rows


def _band_position(pe):
    if pe > SD1_UPPER:
        return "+1SD 초과"
    if pe < SD1_LOWER:
        return "-1SD 미만"
    return "정상 밴드(±1SD)"


def compute_approx(rows):
    out = []
    for row in rows:
        date = row["date"]
        try:
            kospi = float(row["price"])
        except (TypeError, ValueError):
            continue
        approx_pe = ANCHOR_FORWARD_PE * kospi / ANCHOR_KOSPI
        pct_of_anchor = (approx_pe / ANCHOR_FORWARD_PE - 1) * 100
        vs_mean = (approx_pe / MEAN_PE_20Y - 1) * 100
        out.append({
            "date": date,
            "kospi_level": f"{kospi:.2f}",
            "approx_forward_pe": f"{approx_pe:.2f}",
            "pct_of_anchor_pe": f"{pct_of_anchor:+.2f}%",
            "vs_20y_mean": f"{vs_mean:+.2f}%",
            "band_position": _band_position(approx_pe),
            "method": "EPS불변가정 근사(지수변화율 역산)",
            "anchor_date": f"{ANCHOR_DATE}({ANCHOR_NOTE})",
            "caveat": "정밀치 아님, 어닝시즌 이후 실제 컨센서스 EPS 리비전 미반영",
        })
    return out


def _upsert(csv_path, fields, key_fields, new_rows):
    existing = {}
    if os.path.exists(csv_path):
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                key = tuple(row[k] for k in key_fields)
                existing[key] = row
    for row in new_rows:
        key = tuple(row[k] for k in key_fields)
        existing[key] = row
    ordered = sorted(existing.values(), key=lambda r: tuple(r[k] for k in key_fields))
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in ordered:
            writer.writerow(row)


def cmd_update(args):
    rows = _read_index_quote_rows()
    computed = compute_approx(rows)
    if args.raw:
        for row in computed:
            print(f"{row['date']}  KOSPI {row['kospi_level']}  "
                  f"근사PE {row['approx_forward_pe']}배  "
                  f"({row['band_position']}, 20년평균대비 {row['vs_20y_mean']})")
        return
    _upsert(OUTPUT_CSV, OUTPUT_FIELDS, ("date",), computed)
    latest = computed[-1] if computed else None
    if latest:
        print(f"최신({latest['date']}): KOSPI {latest['kospi_level']} → "
              f"근사 forward PE {latest['approx_forward_pe']}배 "
              f"({latest['band_position']}) → {OUTPUT_CSV}에 기록 ({len(computed)}행)")
    else:
        print("계산된 행 없음 (입력 CSV가 비어있거나 index_code=0001 데이터 없음)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_update = sub.add_parser("update", help="근사 forward PE 계산 및 CSV 갱신")
    p_update.add_argument("--raw", action="store_true", help="파일 저장 없이 표준출력만")
    p_update.set_defaults(func=cmd_update)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
