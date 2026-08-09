---
title: KOSPI 12개월 선행(Forward) PER 밴드 차트 — GFC 이후 최저 수준
ingested: 2026-08-09
source_type: user-provided screenshot — Goldman Sachs Global Investment Research (data source: Quantiwise)
tags: [kospi, valuation, per, macro, goldman-sachs]
---

## 원본 내용

**차트 제목**: "Exhibit 1: KOSPI 12m forward P/E hit the lowest level since the
G.F.C amid the recent market volatility"

**출처**: Goldman Sachs Global Investment Research 리포트, 데이터 소스는
Quantiwise (사용자가 차트 하단 attribution을 추가 스크린샷으로 제보,
2026-08-09). 리포트 제목·발행일자는 미확인이나 발행사·데이터벤더는
확정.

**차트 구성**: KOSPI 12개월 선행 PER 밴드, 2006년 7월 ~ 2026년 7월 (20년
히스토리)
- 검은 실선: KOSPI 12개월 선행 PER 실제 추이
- 하늘색 굵은 선: 20년 평균 PER 약 10.0배
- 점선 밴드: +1 표준편차 약 11.2배 / -1 표준편차 약 8.8배
- 최신값(빨간 다이아몬드 마커): **6.65배, -2.7 표준편차** (2026-07-02 기준,
  차트 내 각주 인용)

**핵심 메시지**: KOSPI 선행 PER이 2008년 글로벌 금융위기(GFC) 이후
최저 수준까지 하락. 20년 평균 대비 -2.7 표준편차라는 극단적 저평가
구간에 진입 — 밸류에이션만 놓고 보면 20년 역사에서 가장 싼 축에 속함.

## 데이터 출처 조사 (2026-08-09, Claude 웹검색)

사용자가 "이 지표를 API로 구할 수 있나?"라고 질의해 조사한 결과:

- **이 정확한 "12개월 선행 PER" 시계열은 무료 공개 API로 구할 수 없음** —
  forward PER은 애널리스트 컨센서스 EPS 추정치가 필요하기 때문에
  Bloomberg/Refinitiv/FnGuide DataGuide/**Quantiwise**/Yonhap Infomax
  같은 유료 컨센서스 집계 업체 전용 데이터. (이 차트 자체가 Goldman
  Sachs Global Investment Research가 Quantiwise 데이터를 인용한
  사례 — 국내 기관 리서치에서 Quantiwise가 실제로 이런 용도로
  쓰인다는 실증)
- [KRX 정보데이터시스템](https://data.krx.co.kr/contents/MDC/ISIF/isif/MDCISIF002.cmd)은
  코스피 지수 전체의 **trailing PER**(직전 실적 기준, forward 아님)만
  제공. 공식 API는 openapi.krx.co.kr에서 유료 신청, 또는 비공식
  `pykrx` 파이썬 라이브러리(`get_index_fundamental()`)로 스크래핑 가능.
- 이미 구축된 KIS Open API(`FHKST01010100` 현재가 TR, [kis-api-reference.md](../wiki/concepts/kis-api-reference.md))는
  개별종목(SK하이닉스 등) 단위 trailing PER/PBR은 자동 수집 경로가
  있으나, **지수 전체 forward PER은 자동화 경로 없음**.
- 결론: 사실상 이런 IB/증권사 리서치 노트 이미지를 사용자가 직접
  제보하는 방식이 이 지표를 확보하는 유일한 경로 — 자동화 후보에서
  제외하고 수동 인제스트 대상으로 유지.

## 웹상 공개 교차검증 (2026-08-09, Claude 웹검색)

Goldman Sachs 원본 차트(기관 전용 리서치)는 공개 웹에 게재되지 않으나,
**동일 수치를 인용한 공개 뉴스 기사가 다수 확인됨**:

- [Investing.com — "Korea's KOSPI P/E valuation falls to lowest since
  global financial crisis"](https://www.investing.com/news/stock-market-news/koreas-kospi-pe-valuation-falls-to-lowest-since-global-financial-crisis-4775362) —
  7/8 기준 12개월 선행 PER 6.25배로 2008 GFC 당시(6.27배)보다도 낮은
  2005년 이후 최저치 보도. Goldman Sachs 스트레스테스트 시나리오도
  함께 인용(컨센서스 NTM EPS -33% 하향 가정 시 KOSPI 8,750 예상).
- [BigGo Finance — "KOSPI's Forward P/E Hits 'All-Time Low' in the 7x
  Range... Is the 6000-Level Market 'Undervalued' or a 'Danger
  Signal'?"](https://finance.biggo.com/news/YMHulZ0BJouf4oEhrYB1)
- 검색 스니펫에서 6.65배·-2.7표준편차(2009 금융위기 이후 최저)라는
  이 차트와 정확히 일치하는 수치도 별도로 확인 — 시점에 따라
  6.25~7.5배 사이 변동 언급(4월 반등 이후는 7.5배·-2.1SD로 다소
  회복된 값 보도).

**주의**: 이 환경 네트워크 프록시가 investing.com·CNBC·BigGo Finance
등 다수 도메인을 차단해 WebFetch로 원문 전체를 열람하지는 못함 —
검색 스니펫만으로 교차검증. 원문 전체 확인이 필요하면 사용자가 직접
접속해 확인 권장.

## 연결 지점

- [SK하이닉스 주가 상승의 정당성 분석](../wiki/concepts/rally-justification-analysis.md) —
  SK하이닉스 개별 선행 PER 6.8~6.9배 저평가 근거와 같은 방향(시장 전체가
  저평가 국면이라는 교차검증)
- [미국 거시국면(G/I/L)과 역사적 유사 시기 매칭](../wiki/concepts/macro-regime-history.md) —
  stagflation 국면 판정과 밸류에이션 극단치 시기가 겹침
