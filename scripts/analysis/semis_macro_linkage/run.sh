#!/usr/bin/env bash
# 반도체 3종목(삼성전자·하이닉스·마이크론) × 거시 지표 연동성 — 재현
# 필요: sources/macro-series.csv, sources/sk-hynix-investor-flow.csv, sources/sk-hynix-credit-balance.csv, Yahoo 접근, numpy
# 사용: run.sh            → 6개월(기본, 1~6단계 전체)
#       run.sh long       → 6개월 + 12개월·24개월 + 롤링 6개월(2-c 재검정)
set -euo pipefail
cd "$(dirname "$0")"
END="${LINKAGE_END:-2026-10-23}"

run_one () {   # $1=태그 $2=시작일
  export LINKAGE_TAG="$1" LINKAGE_START="$2" LINKAGE_END="$END"
  python3 prep.py     # 1~2단계: 종목 종가 + 지표 정리·시차 정렬(out/<태그>/ 에 저장)
  python3 corr.py     # 3~4단계: 일간·주간 상관, 구간별, 폭락 4일(6개월 기본 기준)
  python3 factor.py   # 5~6단계: 다변수 R², 공통 요인, 하이닉스 고유 몫, 순열검정·반분 일관성
}
# 기본 6개월은 2026-04-23~10-23(분석 당시 기간)으로 고정 — 최신 기간으로 보려면 LINKAGE_START/END를 지정
run_one 6m "${LINKAGE_START:-2026-04-23}"
if [ "${1:-}" = "long" ]; then
  run_one 12m "2025-10-24"
  run_one 24m "2024-10-24"
  LINKAGE_TAG=24m python3 rolling.py
fi
