#!/usr/bin/env bash
# 반도체 3종목(삼성전자·하이닉스·마이크론) × 거시 지표 연동성 — 1~6단계 재현
# 필요: sources/macro-series.csv, sources/sk-hynix-investor-flow.csv, sources/sk-hynix-credit-balance.csv, Yahoo 접근, numpy
set -euo pipefail
cd "$(dirname "$0")"
python3 prep.py     # 1~2단계: 종목 종가 + 지표 정리·시차 정렬(out/ 에 저장)
python3 corr.py     # 3~4단계: 일간·주간 상관, 구간별, 폭락 4일
python3 factor.py   # 5~6단계: 다변수 R², 공통 요인, 하이닉스 고유 몫, 순열검정·반분 일관성
