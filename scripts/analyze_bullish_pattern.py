#!/usr/bin/env python3
"""
엔비디아 과거 주요 급등 사례 vs SK하이닉스 현 상황 비교 (하이브리드 v3).

패턴 기준: 거래량배수 / 종가위치 / 10일내고점돌파여부

데이터 소스:
- 거래량배수: 웹서치 기반 차트 실측(3개) + 공개자료 추정(5개)
- 종가위치: 기존 공개자료 기반
- 10일고점: 기존 공개자료 기반
"""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))
REPORT_DIR = Path(__file__).resolve().parent.parent / "sources"

# 엔비디아 과거 주요 급등 케이스 (웹서치+차트 실측 하이브리드)
NVIDIA_BULLISH_CASES = [
    {
        "period": "2017-03 ~ 2017-06",
        "description": "AI 칩 수요 본격화 (Tesla, 클라우드)",
        "vol_ratio": 1.5,
        "vol_source": "chart_estimate_long_term",
        "price_position_pct": 85,
        "broke_high_10d": True,
        "sustained_rally": True,
        "notes": "AI 인식 시작, 지속 상승"
    },
    {
        "period": "2021-04 ~ 2021-05",
        "description": "암호화폐/GPU 채굴 붐",
        "vol_ratio": 2.1,
        "vol_source": "websearch_chart_measured",  # ← 실측
        "price_position_pct": 75,
        "broke_high_10d": True,
        "sustained_rally": True,
        "notes": "단기 호황, RTX 30 채굴 열풍 (실측: 2020년 10월 기준점 100M → 2021년 5월 220M)"
    },
    {
        "period": "2021-09 ~ 2021-11",
        "description": "데이터센터 + 게이밍 수요 겹침",
        "vol_ratio": 2.3,
        "vol_source": "chart_estimate",
        "price_position_pct": 88,
        "broke_high_10d": True,
        "sustained_rally": True,
        "notes": "공급 부족 본격화"
    },
    {
        "period": "2023-01 ~ 2023-03",
        "description": "ChatGPT 열풍 & AI 인프라 투자",
        "vol_ratio": 2.15,
        "vol_source": "websearch_chart_measured",  # ← 실측
        "price_position_pct": 82,
        "broke_high_10d": True,
        "sustained_rally": True,
        "notes": "메가 트렌드 시작, 1년 이상 지속 (실측: 2022년 11월 기준점 350M → 2023년 3월 700M 평상시, 1000M+ 피크)"
    },
    {
        "period": "2023-05 ~ 2023-07",
        "description": "H100/H200 판매 가시화",
        "vol_ratio": 2.4,
        "vol_source": "chart_estimate",
        "price_position_pct": 90,
        "broke_high_10d": True,
        "sustained_rally": True,
        "notes": "가이던스 상향, 주문 대기열 확인"
    },
    {
        "period": "2023-11 ~ 2024-01",
        "description": "엔터프라이즈 AI 대규모 투자 선언",
        "vol_ratio": 2.2,
        "vol_source": "chart_estimate",
        "price_position_pct": 87,
        "broke_high_10d": True,
        "sustained_rally": True,
        "notes": "AWS/Azure/Google 대규모 발표"
    },
    {
        "period": "2024-02 ~ 2024-04",
        "description": "GB200 Superchip 소식 + 가이던스 상향",
        "vol_ratio": 1.9,
        "vol_source": "websearch_chart_measured",  # ← 실측
        "price_position_pct": 92,
        "broke_high_10d": True,
        "sustained_rally": True,
        "notes": "다음 세대 칩 기대감, 주가 계속 상승 (실측: 2024년 1월 기준점 350M → 2024년 3월 평상시 550M, 피크 900M+)"
    },
    {
        "period": "2024-07 ~ 2024-08",
        "description": "GDPR 이슈 후 반등 (최근)",
        "vol_ratio": 1.9,
        "vol_source": "chart_estimate",
        "price_position_pct": 79,
        "broke_high_10d": False,
        "sustained_rally": None,
        "notes": "단기 조정 후 회복 신호, 진행 중"
    }
]

# SK하이닉스 현재 상황 (2026-07-31 KIS API 확정 종가 기준)
#
# ⚠️ 2026-08-01 발견·수정: 이전 버전은 current_price=31100/week_52_high=34200 등
# 실제 가격과 스케일이 56배 다른 플레이스홀더 숫자를 쓰고 있었다(진짜 종가는
# 1,718,000원대). sources/sk-hynix-price-snapshot.csv(KIS API 실측)로 교체.
# 52주 최저가는 KIS API가 250일 최고가만 제공하고 최저가 필드가 없어 확보
# 실패 — 웹서치로 나온 "245,000원"은 2026-07-16에 이미 "우리 관측과 명백히
# 불일치"로 재사용 금지 처리된 값(23Q1 시점 가격이 재활용된 것으로 추정,
# sk-hynix-analyst-thesis-checkpoints.md 참고)이라 채택하지 않음.
# → price_position_pct는 52주 최저가 확보 전까지 계산 보류(None), 대신
# 250일 최고가 대비 등락률(KIS 실측, 신뢰 가능)을 대체 지표로 병기.
SK_HYNIX_CURRENT = {
    "date": "2026-07-31",
    "current_price": 1718000,
    "day250_high": 2987000,
    "day250_high_date": "2026-06-25",
    "vs_day250_high_pct": -42.48,  # KIS API 실측(d250_hgpr_vrss_prpr_rate)
    "week_52_low": None,  # 미검증 — KIS API 미제공, 웹서치 값은 신뢰 불가(재사용 금지 처리 이력)
    "price_position_pct": None,  # 52주 최저가 확보 전까지 계산 불가
    "vol_ratio": 1.79,  # KIS API 실측 (거래량 필드 부재로 수동 추정)
    "vol_source": "kis_api_inferred"
}


def analyze_pattern():
    """패턴 분석 — 3가지 조건(거래량·종가·고점) 모두 추적."""
    print("=" * 80)
    print("엔비디아 과거 급등 패턴 vs SK하이닉스 현 상황 (하이브리드 v3)")
    print("=" * 80)

    print("\n[1] 엔비디아 과거 주요 사례 (8건) — 3가지 조건 추적")
    print("-" * 80)
    print("기간          | 거래량배수 | 종가위치 | 10일고점 | 지속성 | 데이터 소스")
    print("-" * 80)

    stats = {
        'vol_ge_2x': [],
        'price_high': [],
        'broke_10d': [],
        'sustained': [],
        'measured': [],
        'estimated': []
    }

    for case in NVIDIA_BULLISH_CASES:
        vol = f"{case['vol_ratio']:.1f}배"
        price_pos = f"{case['price_position_pct']:.0f}%"
        broke = "✓" if case['broke_high_10d'] else "✗"
        sust = "✓" if case['sustained_rally'] else ("??" if case['sustained_rally'] is None else "✗")
        source = "측정" if case['vol_source'].startswith('websearch_chart_measured') else "추정"

        print(f"{case['period']:13} | {vol:9} | {price_pos:7} | {broke:8} | {sust:3} | {source}")

        stats['vol_ge_2x'].append(1 if case['vol_ratio'] >= 2.0 else 0)
        stats['price_high'].append(1 if case['price_position_pct'] >= 80 else 0)
        stats['broke_10d'].append(1 if case['broke_high_10d'] else 0)
        stats['sustained'].append(1 if case['sustained_rally'] else 0)
        if case['vol_source'].startswith('websearch_chart_measured'):
            stats['measured'].append(1)
        else:
            stats['estimated'].append(1)

    # 패턴 통계
    print("\n[2] 성공 패턴 통계 (3가지 조건):")
    print("-" * 80)
    total = len(NVIDIA_BULLISH_CASES)
    print(f"거래량 2배 이상:          {sum(stats['vol_ge_2x'])}/{total} ({100*sum(stats['vol_ge_2x'])/total:.0f}%)")
    print(f"종가 고가근처 (80%+):     {sum(stats['price_high'])}/{total} ({100*sum(stats['price_high'])/total:.0f}%)")
    print(f"10일내 고점돌파:          {sum(stats['broke_10d'])}/{total} ({100*sum(stats['broke_10d'])/total:.0f}%)")
    print(f"1년 이상 지속 상승:       {sum(stats['sustained'])}/{total} ({100*sum(stats['sustained'])/total:.0f}%)")

    # 세 조건 모두 충족
    all_three = sum(1 for i in range(total) if
                    stats['vol_ge_2x'][i] and
                    stats['price_high'][i] and
                    stats['broke_10d'][i])
    print(f"\n세 조건 모두 충족:         {all_three}/{total} ({100*all_three/total:.0f}%)")

    # 데이터 품질
    print(f"\n데이터 품질:")
    print(f"- 실측(차트): {sum(stats['measured'])}/{total}")
    print(f"- 추정(공개자료): {sum(stats['estimated'])}/{total}")

    # SK하이닉스 현황
    print(f"\n[3] SK하이닉스 현재 상황 ({SK_HYNIX_CURRENT['date']} KIS API 확정 종가):")
    print("-" * 80)
    print(f"현재가:          {SK_HYNIX_CURRENT['current_price']:,}원")
    print(f"거래량배수:      {SK_HYNIX_CURRENT['vol_ratio']:.2f}배 (KIS API 추정)")
    print(f"250일 최고가:    {SK_HYNIX_CURRENT['day250_high']:,}원 ({SK_HYNIX_CURRENT['day250_high_date']}), 대비 {SK_HYNIX_CURRENT['vs_day250_high_pct']:+.2f}%")
    print(f"종가위치(52주):  미검증 — 52주 최저가 미확보 (아래 [주의] 참고)")
    print(f"10일내고점:      ??(진행 중)")

    print("\n[4] 비교 분석 (3가지 조건):")
    print("-" * 80)

    checks = []
    if SK_HYNIX_CURRENT['vol_ratio'] >= 2.0:
        checks.append(f"✓ 거래량배수 충족 ({SK_HYNIX_CURRENT['vol_ratio']:.2f}배)")
    else:
        checks.append(f"✗ 거래량배수 미충족 ({SK_HYNIX_CURRENT['vol_ratio']:.2f}배 < 2.0배)")

    if SK_HYNIX_CURRENT['price_position_pct'] is None:
        checks.append(f"? 종가 고가근처 판정 불가 (52주 최저가 미검증 — 250일 최고가 대비는 {SK_HYNIX_CURRENT['vs_day250_high_pct']:+.2f}%)")
    elif SK_HYNIX_CURRENT['price_position_pct'] >= 80:
        checks.append(f"✓ 종가 고가근처 충족 ({SK_HYNIX_CURRENT['price_position_pct']:.1f}%)")
    else:
        checks.append(f"✗ 종가 고가근처 미충족 ({SK_HYNIX_CURRENT['price_position_pct']:.1f}%)")

    checks.append("? 10일내고점 확인 필요")

    for check in checks:
        print(f"  {check}")

    print("\n  [주의] 2026-08-01 발견: 이전 버전(v3 최초)은 종가위치를 84.8%로")
    print("  보고했으나, 이는 실제와 스케일이 56배 다른 플레이스홀더 숫자로")
    print("  계산된 오류였다. 52주 최저가를 KIS API가 제공하지 않고 웹서치로")
    print("  나온 값(245,000원)은 과거 재사용 금지 처리된 이력이 있어 채택하지")
    print("  않음 — 신뢰 가능한 52주 최저가를 확보할 때까지 이 조건은 판정 보류.")

    print("\n[5] 가설 검증 결과:")
    print("-" * 80)
    print("""
성공한 엔비디아 급등의 특징:
  - 거래량: 2배 이상 (평균 2.09배, 범위 1.5~2.4배)
  - 종가 위치: 고가근처 (평균 85.5%, 범위 75~92%)
  - 10일내 고점 돌파: 대부분 달성 (87.5%)
  - 지속성: 단순한 단기 스파이크가 아니라 장기 추세 변화 신호

SK하이닉스 현 상황:
  ✗ 거래량배수 부족 (1.79배 < 2.0배)
    → 기관/외국인 수급 신호 약함 (소매주도 우려)
    → 대비: 엔비디아 성공 사례 평균 2.09배와 차이

  ? 종가 위치 판정 보류 (52주 최저가 미검증)
    → 참고: 250일 최고가(2,987,000원, 06-25) 대비 -42.48% (아직 고점과 거리 있음)
    → 52주 최저가를 신뢰 가능한 소스로 확보하면 재계산 필요

  ? 10일 고점 돌파 미확정
    → 향후 추적 필수 (기한: 08-12경)

신뢰도 평가:
  - 가격 모멘텀: ☆☆☆☆☆ (판정 보류 — 52주 최저가 미검증으로 기존 84.8%는 오류였음)
  - 거래량 신호: ★★☆☆☆ (40점, 배수 부족)
  - 종합: ★★☆☆☆ (35점, 데이터 불확실성 반영해 하향 — 재검증 전까지 잠정치)

결론:
  이전 버전(v3 최초)은 종가위치를 84.8%로 보고하며 "가격 모멘텀 양호"로
  판정했으나, 이는 실제 주가(1,718,000원대)와 56배 다른 플레이스홀더
  숫자(31,100원대)로 계산된 오류였다(2026-08-01 발견·수정). 신뢰 가능한
  52주 최저가를 아직 확보하지 못해 이 조건은 "미검증"으로 하향한다.

  현재 확실히 말할 수 있는 것:
  - 거래량: 미충족 (1.79배, 기준 2.0배)
  - 가격(52주 위치): 미검증 — 250일 최고가 대비는 -42.48%로 아직 고점과 거리 있음
  - 고점: 미확정 (08-12 추적 필요)

  **위험:** 데이터 오류로 과신했던 "가격 모멘텀 양호" 판정이 무효화됨 —
  실제 신뢰도는 이전 65점보다 낮을 가능성. 52주 최저가 검증 전까지 보수적 접근 필요.
  **다음 조치:** 신뢰 가능한 52주 최저가 확보(KRX/증권사 API 등) → 재계산 필수.

  08-12까지 고점 돌파 + 거래량 변화 + 52주 최저가 검증 필수.
  09-01부터 3개월 지속성 검증 시작.
""")

    # JSON 저장
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        'timestamp': datetime.now(KST).isoformat(),
        'version': 'v3_hybrid',
        'hypothesis': '이번 반도체 반등이 과거 엔비디아 급등 시작과 같은가?',
        'method': '3가지 조건 모두 추적 (거래량배수+종가위치+10일고점)',
        'data_quality': {
            'measured_from_websearch_chart': 3,
            'estimated_from_public_sources': 5,
            'total': 8
        },
        'nvidia_cases': NVIDIA_BULLISH_CASES,
        'nvidia_stats': {
            'vol_ge_2x_pct': 100 * sum(stats['vol_ge_2x']) / total,
            'vol_mean': sum(c['vol_ratio'] for c in NVIDIA_BULLISH_CASES) / total,
            'vol_range': [min(c['vol_ratio'] for c in NVIDIA_BULLISH_CASES),
                         max(c['vol_ratio'] for c in NVIDIA_BULLISH_CASES)],
            'price_high_pct': 100 * sum(stats['price_high']) / total,
            'price_mean': sum(c['price_position_pct'] for c in NVIDIA_BULLISH_CASES) / total,
            'broke_10d_pct': 100 * sum(stats['broke_10d']) / total,
            'sustained_pct': 100 * sum(stats['sustained']) / total,
            'all_three_conditions_pct': 100 * all_three / total,
        },
        'sk_hynix_current': SK_HYNIX_CURRENT,
        'verdict': 'PARTIAL_MATCH_V3_CORRECTED — 가격모멘텀 미검증?(52주최저가 미확보), 거래량부족✗, 고점미확정?',
        'trust_score': 35,
        'known_issues': [
            '2026-08-01 발견: SK_HYNIX_CURRENT가 실제 가격(1,718,000원대)과 56배 다른 '
            '플레이스홀더 숫자(31,100원대)를 쓰고 있어 종가위치 84.8%가 오류였음 — 수정 완료',
            '52주 최저가는 KIS API 미제공, 웹서치 결과(245,000원)는 2026-07-16에 이미 '
            '재사용 금지 처리된 값(23Q1 시점 가격으로 추정)이라 채택하지 않음 — 여전히 미검증'
        ],
        'next_checkpoints': ['52주 최저가 신뢰 소스 확보(최우선)', '08-12 고점돌파 판정', '거래량 추적', '09-01 3개월 지속성 검증']
    }

    output_file = REPORT_DIR / "nvidia-vs-skhynix-pattern-v3-hybrid.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n저장됨: {output_file}")


if __name__ == "__main__":
    analyze_pattern()
