#!/usr/bin/env python3
"""
엔비디아 과거 급등 사례 vs 현재 SK하이닉스/반도체 섹터 비교.

가설: "이번 반도체 반등이 과거 엔비디아 급등 시작과 같은가?"

분석 메트릭: 거래량배수 / 종가위치(%) / 10일내 고점돌파여부
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

KST = timezone(timedelta(hours=9))
ANALYSIS_DIR = Path(__file__).resolve().parent.parent / "sources"


def fetch_nvidia_history(start_date="2016-01-01", end_date=None):
    """엔비디아 전체 이력 데이터 가져오기."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    nvda = yf.download("NVDA", start=start_date, end=end_date, progress=False)
    return nvda


def identify_bullish_regimes(df, sma_window=50, vol_threshold_pct=1.5):
    """
    엔비디아에서 급등 시작 구간 식별.

    조건: SMA를 넘는 종가 + 거래량 평균 대비 50% 이상 증가
    """
    df = df.copy()
    df['SMA'] = df['Close'].rolling(window=sma_window).mean()
    df['Avg_Vol'] = df['Volume'].rolling(window=sma_window).mean()
    df['Vol_Ratio'] = df['Volume'] / df['Avg_Vol']

    # 급등 시작: SMA 돌파 + 거래량 >= 평균의 1.5배
    df['Bullish_Start'] = (df['Close'] > df['SMA']) & (df['Vol_Ratio'] >= vol_threshold_pct)

    # 연속적인 급등 구간 그룹화
    df['Regime_Group'] = (df['Bullish_Start'] != df['Bullish_Start'].shift()).cumsum()

    return df


def extract_regime_metrics(df, regime_group_id):
    """
    특정 급등 구간의 메트릭 추출.

    - 거래량배수: 시작일 거래량 / 이전 50일 평균
    - 종가위치: (close - 52week_low) / (52week_high - 52week_low) * 100
    - 10일내 고점돌파: 다음 10일 중 이전 고점 돌파 여부
    """
    regime = df[df['Regime_Group'] == regime_group_id]
    if len(regime) < 2:
        return None

    start_idx = regime.index[0]
    start_price = regime.iloc[0]['Close']
    vol_ratio = regime.iloc[0]['Vol_Ratio']

    # 종가 위치 (52주 기준)
    lookback_52w = start_idx - timedelta(days=365)
    history_52w = df[df.index >= lookback_52w][:start_idx]
    if len(history_52w) > 0:
        high_52w = history_52w['High'].max()
        low_52w = history_52w['Low'].min()
        price_position = ((start_price - low_52w) / (high_52w - low_52w) * 100) if (high_52w - low_52w) > 0 else 50
    else:
        price_position = None

    # 이전 고점
    prev_high = history_52w['High'].max() if len(history_52w) > 0 else start_price

    # 10일내 고점돌파 확인
    next_10d = regime.iloc[1:11] if len(regime) > 10 else regime.iloc[1:]
    broke_high = next_10d['High'].max() > prev_high if len(next_10d) > 0 else False

    return {
        'date': start_idx.strftime('%Y-%m-%d'),
        'start_price': round(start_price, 2),
        'vol_ratio': round(vol_ratio, 2),
        'price_position_pct': round(price_position, 1) if price_position else None,
        'broke_high_10d': broke_high,
        'regime_len': len(regime)
    }


def analyze_nvidia_cases(nvda_df, min_regime_len=5):
    """엔비디아 주요 급등 사례 분석."""
    regimes = []

    # 급등 구간별 메트릭 추출
    for regime_id in nvda_df['Regime_Group'].unique():
        if pd.isna(regime_id):
            continue

        regime_data = nvda_df[nvda_df['Regime_Group'] == regime_id]
        if len(regime_data) >= min_regime_len:
            metrics = extract_regime_metrics(nvda_df, regime_id)
            if metrics:
                regimes.append(metrics)

    # 최근순 정렬, 상위 10개 선택
    regimes_sorted = sorted(regimes, key=lambda x: x['date'], reverse=True)[:10]

    return regimes_sorted


def format_case_summary(case):
    """한 줄 요약 포맷: 거래량배수 / 종가위치 / 10일내고점돌파여부"""
    vol = f"{case['vol_ratio']:.1f}배"
    price_pos = f"{case['price_position_pct']:.0f}%" if case['price_position_pct'] else "불명"
    broke = "✓" if case['broke_high_10d'] else "✗"

    return f"{case['date']} | {vol} | {price_pos} | {broke}"


def main():
    print("엔비디아 역사 데이터 다운로드 중...")
    nvda_df = fetch_nvidia_history("2015-01-01")

    print("급등 구간 식별 중...")
    nvda_df = identify_bullish_regimes(nvda_df)

    print("\n엔비디아 주요 급등 사례 (최근 10개):")
    print("=" * 70)
    print("날짜       | 거래량배수 | 종가위치 | 10일내고점돌파")
    print("-" * 70)

    cases = analyze_nvidia_cases(nvda_df)
    for case in cases:
        print(format_case_summary(case))

    # 패턴 분석
    print("\n" + "=" * 70)
    print("패턴 분석:")
    vol_ratios = [c['vol_ratio'] for c in cases]
    prices_pos = [c['price_position_pct'] for c in cases if c['price_position_pct']]
    broke_count = sum(1 for c in cases if c['broke_high_10d'])

    print(f"- 거래량배수 평균: {np.mean(vol_ratios):.2f}배 (min: {min(vol_ratios):.2f}, max: {max(vol_ratios):.2f})")
    print(f"- 거래량배수 >= 2배 사례: {sum(1 for v in vol_ratios if v >= 2.0)}/{len(cases)}")
    print(f"- 종가위치 평균: {np.mean(prices_pos):.1f}% (고가근처 = 80~100%)")
    print(f"- 종가 80% 이상(고가근처) 사례: {sum(1 for p in prices_pos if p >= 80)}/{len(cases)}")
    print(f"- 10일내 고점돌파 달성: {broke_count}/{len(cases)}")

    # 패턴 기준
    print("\n성공 패턴 (기준): 2배 이상 + 고가근처 + 10일내 고점돌파")
    success = sum(1 for c in cases if c['vol_ratio'] >= 2.0 and
                  (c['price_position_pct'] and c['price_position_pct'] >= 80) and
                  c['broke_high_10d'])
    print(f"패턴 충족 사례: {success}/{len(cases)} ({100*success/len(cases):.0f}%)")

    # 결과 저장
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = ANALYSIS_DIR / "nvidia-bullish-cases.json"
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now(KST).isoformat(),
            'cases': cases,
            'summary': {
                'vol_ratio_mean': float(np.mean(vol_ratios)),
                'vol_ratio_ge2x_count': int(sum(1 for v in vol_ratios if v >= 2.0)),
                'price_pos_mean': float(np.mean(prices_pos)),
                'price_pos_high_count': int(sum(1 for p in prices_pos if p >= 80)),
                'broke_high_10d_count': int(broke_count),
                'success_pattern_count': int(success)
            }
        }, f, indent=2)

    print(f"\n(저장됨: {output_file})")


if __name__ == "__main__":
    main()
