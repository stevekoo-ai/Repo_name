---
title: "CXL Daily Update — 2026-08-06"
created: 2026-08-06
updated: 2026-08-06
tags: [cxl, daily-update, delta, insight, market-intel]
baseline: "DRAFT v0.4 + Daily Update 1호(2026-08-04)"
---

# CXL Daily Update Report — 2026-08-06

> 발행일: 2026-08-06 02:40 KST
> 기준선: DRAFT v0.4 + Daily Update 1호(2026-08-04)
> 조사 방법: 12개 카테고리 전수 WebFetch 조사 (DuckDuckGo HTML 폴백 경유)
> 형식: 각 delta별 [변경]/[영향]/[액션]
> 원시 데이터: [sources/cxl-daily-raw-2026-08-06.md](../../sources/cxl-daily-raw-2026-08-06.md)

## 📰 헤드라인 (오늘의 핵심)

> **용어 주석 (처음 등장하는 줄임말·기술 용어 풀이)**
> - **CXL**(Compute Express Link): CPU와 메모리를 고속으로 연결하는 산업 표준 규격. 여러 서버가 메모리를 나눠 쓰게 해준다.
> - **MXC**(Memory eXpander Controller): CXL 메모리 확장을 담당하는 칩. 메모리와 CPU 사이에서 데이터 이동 관리.
> - **trial production**: 시제품 소량 생산 단계. 양산 전 마지막 검증을 거치는 중간 단계.
> - **HBM**(High Bandwidth Memory): 고대역폭 메모리. AI 연산용 고성능 메모리로 주로 GPU에 탑재.
> - **FMS**(Flash Memory Summit): 플래시/메모리 산업 대형 행사. 벤더 신제품이 집중 발표됨.
> - **ISCA**(International Symposium on Computer Architecture): 컴퓨터 아키텍처 분야 최고 학회.
> - **CapEx**(Capital Expenditure): 설비투자. 시설·장비에 쓰는 자본 지출.
> - **YoY**(Year-over-Year): 전년 동기 대비 증감률. **QoQ**(Quarter-over-Quarter): 전분기 대비.
> - **DRAM**: PC·서버에 쓰이는 주기억장치(일반적 RAM). **KV cache**: AI 추론 시 이전 계산 결과를 임시 저장·재사용하는 메모리 영역.
> - **메모리 풀링**: 여러 서버가 하나의 메모리 자원을 나눠 쓰는 기술. **hyperscaler**: 대규모 데이터센터를 운영하는 빅테크(Amazon/Google/Meta/Microsoft 등).

- **Montage, CXL 3.2 MXC 컨트롤러(M88MX6852) trial production 진입** (2026-07-30) — CXL 3.2 스펙 기준 최초 trial production (벤더 발표 기준) ★★★
- **FMS 2026 CXL 하드웨어 발표 집중**: Marvell 48TB 단일 CXL 스위치, Kioxia XL1, ScaleFlux MC600, XCENA 20TB 풀링 데모 공개
- **Panmnesia, ISCA 2026에서 next-stage CXL controller + fabric switch 발표** (2026-07-01) — 학회 발표 ★★
- **Liqid EX-5410C — CXL 2.0 40TB/chassis → 160TB+ 통합 풀**, PNNL Abaco AI-for-Science 적용 (2026-08-04)
- **HBM 3사 실적**: Micron Q3 $41.46B, Samsung 이익 +756%, SK Hynix 영업이익률 72% (3사 각기 다른 지표 공개, 단일 출처 일부) — 2026 HBM output +62% YoY
- **4대 US 클라우드 2026 CapEx $650-725B** (Amazon $200B / Google $185B / Meta $125B / Microsoft 잔여 추정), ~75% AI 인프라, "전력에 60%+ 지출" (단일 출처)
- **DRAM 가격 상승 둔화 신호**: 소비자 한계 도달, 단 AI 수요는 Q3까지 지탱
- **CXL Mini-DevCon 2026-08-03 Santa Clara** 개최 — 컨소시엄 자체 이벤트

## 🎯 종합 인사이트 (상품기획 시사점)

> 최고위층 보고용. 과장 표현 배제, 사실·수치 중심. 영향도 높은 내용(★★★/★★)은 원시 데이터 원문 대비 cross-check 수행. 각 항목 `[출처](URL)` 클릭 시 원문 확인. 기술 용어는 헤드라인 상단 용어 주석 참조.

1. **CXL 3.2 컨트롤러 실리콘이 trial production(시제품 소량 생산, 양산 전 검증) 단계 진입** — Montage가 CXL 3.2 표준용 메모리 연결 칩(MXC, M88MX6852)의 시제품 소량 생산 단계에 진입(2026-07-30). 벤더 발표는 "CXL 3.2 스펙 기준 최초"로 한정("업계 최초"는 벤더 자체 표현, 교차 검증 미완료). 시사점: CXL 칩을 만드는 7개 벤더 중 어느 세대(CXL 2.0 vs 3.2)를 먼저 확보하느냐가 제품 차별화 요소. [출처: PRNewswire](https://www.prnewswire.com/news-releases/montage-technology-announces-industry-first-trial-production-of-cxl-3-2-mxc-chip-302838936.html) / [Xenospectrum](https://xenospectrum.com/en/montage-cxl-3-2-trial-chip/)

2. **CXL 메모리 풀(여러 서버가 나눠 쓰는 메모리 자원) 단위 용량 20~160TB 확장 + 고객 적용 사례** — Marvell 단일 CXL 스위치 뒤 48TB 집계(FMS 2026 발표), Liqid EX-5410C 40TB/chassis → 160TB+ 풀(PNNL Abaco AI-for-Science 적용, 2026-08-04). 대규모 AI 추론용 임시 메모리(KV cache)를 CXL로 빼내는 것의 하드웨어 실현성에 대한 구체적 용량 근거 확보. 128GB/request × 동시 요청 수 = 필요 풀 용량 산정 정량 기준. [출처: Futurum Group(Marvell)](https://futurumgroup.com/insights/marvell-scales-ai-memory-to-48tb-behind-a-single-cxl-switch-at-fms-2026/) / [BusinessWire(Liqid)](https://www.businesswire.com/news/home/20260804535529/en/Liqid-Launches-the-Industrys-Most-Advanced-CXL-Memory-Pooling-Platform-for-AI-and-Scientific-Discovery)

3. **KV cache(AI 추론용 임시 메모리) 정량 수치 확보** — 700억 매개변수(70B) 모델 @ 32K context = ~128GB KV cache/request(context 길이에 비례해 증가), FP8(저정밀도 데이터 형식) 양자화 시 -50%, paged attention+prefix caching+GQA+FP8 조합 시 4~40x 비용 압축(기존 FP16 대비). 128GB/request는 단일 GPU 메모리 한계 초과 → CXL 외부 메모리 풀 필요성의 정량 근거. TCO(총소유비용) 모델 핵심 입력값. [출처: arxiv](https://arxiv.org/pdf/2603.20397) / [gpuaas](https://gpuaas.com/blog/kv-cache-inference-costs-optimization)

4. **HBM(AI용 고대역폭 메모리) 3사 실적 + 차세대(HBM4) 양산 시작** — Micron Q3 매출 $41.46B, Samsung 이익 +756% YoY(전년 동기 대비), SK Hynix 영업이익률 72% (3사가 각기 다른 지표만 공개, 비교 일관성 부족; Samsung +756%/Micron $41.46B는 gate.com 단일 출처). 2026 HBM 생산량 +62% YoY 확장 전망 vs 가격 +20-40% YoY 상승 → 수요가 공급 확대를 상회(HBM4 양산 초기). SK Hynix 점유율 방어 vs Samsung 추격 경쟁 지속. [출처: gate.com(3사 실적)](https://gate.com) / [koreainvestinsights(SK 72%)](https://koreainvestinsights.com) / [presenc.ai(HBM4 ramping)](https://presenc.ai)

5. **Hyperscaler(대규모 데이터센터 운영사) AI 인프라 비용 구조: 전력 60%+** — 4대 US 클라우드 2026 CapEx(설비투자) 합산 $650-725B(Amazon $200B/Google $185B/Meta $125B/Microsoft 잔여 추정/Oracle 일부), +70-77% YoY, ~75% AI 특화. "전력/인프라에 60%+ 지출, 칩이 아닌"(nextwavesinsight 단일 출처, 교차 검증 미완료) → CXL 메모리 풀링의 전력/랙 효율 가치가 hyperscaler 비용 구조에 기여 가능성. [출처: nextwavesinsight(전력 60%+)](https://nextwavesinsight.com/hyperscaler-ai-capex-microsoft-google-amazon-meta-2026/) / [valueaddvc(CapEx 분해)](https://valueaddvc.com)

6. **FMS 2026(메모리 산업 행사)에서 CXL 하드웨어 발표 집중** — 4개 벤더(Marvell/Kioxia/ScaleFlux/XCENA)가 구체 제품·데모로 발표. CXL이 표준 문서 단계에서 시제품/데모 단계로 전환 확인. [상세: 본 보고서 🎪 업계 이벤트 섹션]

7. **DRAM(주기억장치) 가격 세그먼트 분화** — 소비자 측 상승 둔화(가격 부담 한계 도달) + AI/서버 측은 Q3 2026까지 상승 지속. 단순 "상승"에서 용도별 분화로 정교화. 소비자 메모리 둔화 → 서버 DRAM 우선 전환 가능 → CXL 메모리 모듈 공급 간접 영향. [출처: Tom's Hardware](https://www.tomshardware.com/pc-components/ram/memory-price-surge-begins-to-cool-as-consumers-hit-affordability-limit-ai-demand-still-keeps-dram-and-nand-prices-climbing-through-q3-2026)

## 📊 Delta 상세 (기준선 대비 변경)

### Delta-1: Montage CXL 3.2 MXC — CXL 3.2 스펙 기준 최초 trial production <span style="color:red">★★★</span>

**[변경]**
- 기존 DRAFT(3장 컨트롤러 벤더)는 Montage를 7개 컨트롤러 벤더 중 하나로 기재, 구체 제품/일정 미상세
- **Montage가 CXL 3.2 Memory eXpander Controller(MXC) 칩 M88MX6852의 trial production에 진입** (2026-07-30~31) — 벤더 발표는 "CXL 3.2 스펙 매칭 칩 기준 최초"("industry's first trial production"). ("업계 최초"는 벤더 자체 표현, 독립 교차 검증 미완료)
- CXL 3.2 컨트롤러 실리콘이 양산 전 단계에 진입한 첫 사례

**[영향]**
- CXL 3.2 디바이스 생태의 실리콘 레벨 검증 시작 — DRAFT 3장 "CXL 3.x 컨트롤러 로드맵" 추상적 기재를 구체 제품/일정으로 보강 근거
- 컨트롤러 벤더 7개 중 Montage가 **CXL 3.2 기준 최초 진입** — 벤더별 세대 분화 가시화
- 상품기획: CXL 3.2 컨트롤러 확보 시점이 경쟁 벤더보다 선행하는 Montage의 차별화 포인트, 단 trial production→양산 전환 시점 추가 추적 필요

**[액션]**
- DRAFT 3장 Montage 행에 CXL 3.2 MXC M88MX6852 trial production(2026-07-30) 추가
- DRAFT 3장에 "벤더별 CXL 세대 분화" 관점 추가 (3.2 최초 진입 벤더 명시)

### Delta-2: FMS 2026 CXL 하드웨어 쇼케이스 — Marvell 48TB / Kioxia XL1 / ScaleFlux MC600 / XCENA 20TB <span style="color:red">★★</span>

**[변경]**
- 기존 DRAFT(3장/4장)는 FMS 2026 + Marvell "Agentic AI Inference" 프레임을 언급(Daily Update 1호 반영), 단 구체 제품/용량 미상세
- **FMS 2026에서 4개 벤더가 구체 CXL 하드웨어로 일제히 전시**:
  - **Marvell**: Bravera SC6 + Structera CXL switches — 단일 스위치 뒤 최대 **48TB AI memory** 집계 (agentic inference)
  - **Kioxia**: XL1 Series CXL memory expansion module — XL-FLASH + CXL 결합, 덜 빈번한 데이터 DRAM에서 이동
  - **ScaleFlux**: MC600 CXL Memory Controller + FC6116 PCIe Gen6 SSD Controller (2026-07-28 발표, 2026-07-31 FMS 상세)
  - **XCENA**: FMS 2026에서 **최대 20TB CXL memory pool** 풀링 시스템 + **KV cache sharing 데모**

**[영향]**
- DRAFT 4장(풀링 SW/어플라이언스)의 "48TB 단일 스위치" 용량 기준 신규 획득 — CXL 풀링 단위 용량 급격 확대 추세 구체화
- XL-FLASH 기반 CXL 모듈(비휘발성 + CXL)은 DRAFT 2장(CXL 디바이스/미디어) "미디어 다양화" 관점 보강
- XCENA의 KV cache sharing 데모는 DRAFT 8장(AI Rack/KV offload)와 9장 연결 — CXL 메모리 풀에서 KV cache 공유가 이미 하드웨어 데모 단계
- 상품기획: CXL 메모리 풀 단위 용량이 20~48TB로 확장 → 대규모 KV offload의 실현성 구체적 근거

**[액션]**
- DRAFT 4장에 Marvell 48TB single switch 수치 추가
- DRAFT 2장에 Kioxia XL1(XL-FLASH + CXL) 미디어 추가
- DRAFT 3장 ScaleFlux 행에 MC600 + FC6116 추가, XCENA 행에 20TB 풀링 데모 + KV cache sharing 추가
- DRAFT 8장에 XCENA KV cache sharing 데모(하드웨어 단계) 역링크

### Delta-3: Panmnesia ISCA 2026 — next-stage CXL controller + fabric switch <span style="color:red">★★</span>

**[변경]**
- 기존 DRAFT(3장)는 Panmnesia를 7개 컨트롤러 벤더 중 하나로 기재, 학회 발표 미반영
- **Panmnesia가 ISCA 2026(2026-07-01)에서 next-stage CXL controller + 그 위에 구축된 fabric switch 발표**
- 주요 컴퓨터 아키텍처 학회(ISCA) 레벨에서 next-stage 아키텍처 공개

**[영향]**
- Panmnesia의 fabric switch 접근은 DRAFT 4장(풀링) + 6장(AI 패브릭) 교차 — CXL 컨트롤러가 fabric switch로 확장되는 아키텍처 방향성
- "next-stage" 표현이 다음 CXL 세대(3.x→4.0) 컨트롤러 사전 검증 신호
- 상품기획: CXL 컨트롤러 + fabric switch 결합이 학회 레벨에서 이미 검증 단계 — DRAFT 12장 아키텍처 옵션 보강 근거

**[액션]**
- DRAFT 3장 Panmnesia 행에 ISCA 2026 next-stage controller + fabric switch(2026-07-01) 추가
- DRAFT 4장/6장에 Panmnesia fabric switch 방향성 역링크 검토

### Delta-4: Liqid EX-5410C — 160TB+ CXL 풀, PNNL 적용 <span style="color:red">★★</span>

**[변경]**
- 기존 DRAFT(4장 풀링 SW/어플라이언스)는 Liqid를 생태 벤더로 언급, 구체 제품/용량/고객 미상세
- **Liqid EX-5410C Memory Platform** (2026-08-04):
  - CXL 2.0 memory expansion system
  - chassis당 최대 **40TB DRAM**
  - **160TB+ unified memory pool**로 확장
  - **PNNL(Pacific Northwest National Lab) Abaco AI-for-Science 플랫폼**에 rack-scale CXL 2.0 memory pooling 인프라 공급
- 2026 CXL 생태 맵 확보: Astera Leo, Samsung CMM-D, Micron CZ120, SK Hynix Niagara, Kioxia, MemVerge Memory Machine, Liqid Matrix (overprovisioning 제거 목적)

**[영향]**
- DRAFT 4장의 CXL 풀링 용량 기준(160TB+) + 실제 고객(PNNL 국립연구소) 신규 획득 — CXL 풀링이 상용/연구 검증 단계
- PNNL AI-for-Science 적용은 DRAFT 11장(CSP/시장) "비 CSP 연구 시장" 세그먼트 보강
- 상품기획: CXL 풀링 단위 용량 160TB+ → 대규모 AI 메모리 풀의 상용 검증 사례

**[액션]**
- DRAFT 4장에 Liqid EX-5410C(40TB/chassis → 160TB+ pool, PNNL Abaco, 2026-08-04) 추가
- DRAFT 4장에 2026 CXL 생태 맵(Astera Leo/Samsung CMM-D/Micron CZ120/SK Hynix Niagara/Kioxia/MemVerge/Liqid Matrix) 정리

### Delta-5: HBM 3사 실적 + 2026 HBM output +62% <span style="color:red">★★</span>

**[변경]**
- 기존 DRAFT(10장/11.3장, Daily Update 1호 반영)는 HBM 점유율 62/21/17 + Samsung 30% 목표 + 16-layer 로드맵 기재
- **신규 실적 수치 획득**:
  - **Micron Q3 revenue: $41.46B**
  - **Samsung: 이익 +756%**
  - **SK Hynix: 72% 영업이익률**
  - **DRAM/HBM 가격 up 20-40% YoY**
  - **2026 HBM output: +62% YoY** (capacity additions + yield gains)
  - **HBM3E dominates shipments, HBM4 ramping** (HBM4 양산 램프 시작)
- HBM 점유율 출처별 분산 확인: 01.co(SK 60%/Micron 22%/Samsung 18%) vs presenc.ai(SK 50-62%/Micron 5-20%/Samsung 25-40%) — 단일 수치 아닌 **범위 표기 권장**

**[영향]**
- DRAFT 10장 "2026 HBM 가격 하방 압력" 가설 강화 근거 — 2026 HBM output +62% YoY는 공급 확대 → 가격 하방 요인
- 단, 가격은 여전히 20-40% YoY 상승 → 수요 증가가 공급 확대를 상회 (HBM4 램프 초기 수요)
- SK Hynix 72% 영업이익률 + Samsung 이익 +756% — HBM 사업 호황 지속, 점유율 경쟁 심화(Samsung 추격) 재료 (3사 지표 불일치·일부 단일 출처(gate.com) 주의)
- HBM4 ramping 시작은 DRAFT 0장(훑어보기) "차세대 HBM 일정" 보강

**[액션]**
- DRAFT 10장에 2026 HBM output +62% YoY, 가격 +20-40% YoY, 3사 실적(Micron $41.46B / Samsung +756% / SK Hynix 72%) 추가
- DRAFT 10장 HBM 점유율을 단일 수치(62/21/17)에서 범위 표기로 조정 (출처별 분산 공개)
- DRAFT 0장에 HBM3E dominates / HBM4 ramping 상태 추가

### Delta-6: Hyperscaler 2026 CapEx 상세 분해 + 전력 60%+ <span style="color:red">★★</span>

**[변경]**
- 기존 DRAFT(11장, Daily Update 1호 반영)는 hyperscaler 합산 $600-770B 기재
- **상세 분해 획득**:
  - 4대 US 클라우드 합산 **$650-725B** (기존 범위 내, 정밀화)
  - **+70-77% YoY surge**
  - **~75%가 AI 특화 인프라**
  - **상세 분해**: Amazon $200B / Google(Alphabet) $185B / Meta $125B / Microsoft 잔여 / Oracle 5개사 그룹 일부
  - **Q1 2026 합산 outlay $130B+** (2026-04-29 Q1 earnings, 물리 배치 가속)
  - **"spend 60%+ on power, not chips"** — 오퍼레이터가 전력 기반 인프라 우선

**[영향]**
- DRAFT 11장 CapEx를 범위($600-770B)에서 정밀 범위($650-725B) + 회사별 분해로 보강
- **"전력 60%+ 지출"**은 DRAFT 11장 비용 구조 신규 인사이트 — AI 인프라 비용이 칩이 아닌 전력/인프라에 집중 → CXL 메모리 풀링의 전력/랙 효율 가치 기여 가능성 (단일 출처 nextwavesinsight, 교차 검증 미완료)
- Q1 2026 $130B 집행은 연간 가이던스($650-725B) 대비 분기당 ~$162B 선상 — 가이던스 신뢰성 확인
- 상품기획: CXL 메모리 풀링이 "전력/랙 효율" 관점에서 호스팅스케일러 비용 구조에 기여한다는 포지셔닝 근거 강화

**[액션]**
- DRAFT 11장에 CapEx 상세 분해(Amazon $200B/Google $185B/Meta $125B/Microsoft 잔여) + +70-77% YoY + ~75% AI + Q1 $130B 집행 추가
- DRAFT 11장에 "전력 60%+ 지출" 비용 구조 인사이트 추가 — CXL 풀링의 전력/랙 효율 가치 역링크
- DRAFT 12장(상품기획)에 "전력/랙 효율" 포지셔닝 강화

### Delta-7: DRAM 가격 상승 둔화 신호 <span style="color:red">★</span>

**[변경]**
- 기존 DRAFT(7장/10장, Daily Update 1호 반영)는 Q3 DRAM +13~18% QoQ 상승 기재, 둔화 신호 미반영
- **신규 신호**: "Memory price surge begins to cool as consumers hit affordability limit" — 가격 상승이 소비자 한계 도달로 둔화 시작
- 단, AI 수요는 여전히 DRAM/NAND 가격을 Q3 2026까지 밀어올림 (소비자 측 둔화, AI/서버 측은 지속)

**[영향]**
- DRAFT 10장 가격 전망에 "소비자 측 둔화 vs AI/서버 측 지속" 이중 추세 추가 — 단순 "상승"에서 "세그먼트 분화"로 정교화
- 상품기획: 소비자 메모리 둔화가 공급 전환(서버 우선)에 영향 가능 → CXL 메모리 모듈 공급 간접 영향

**[액션]**
- DRAFT 10장에 DRAM 가격 "소비자 측 둔화 + AI/서버 측 지속" 이중 추세 추가

### Delta-8: KV cache 정량 수치 — 70B/32K = 128GB, FP8 -50%, 4~40x 비용 압축 <span style="color:red">★</span>

**[변경]**
- 기존 DRAFT(8장 AI Rack/KV offload, 12장 TCO)는 KV cache 정성 중심, 정량 모델링 수치 미상세
- **신규 정량 수치 획득**:
  - **70B 모델 @ 32K context = ~128GB KV cache per request** (context에 선형 스케일)
  - **FP8 KV cache 양자화: per-token cache memory -50%**
  - **paged attention + prefix caching + GQA + FP8 quantization = long-context inference cost 4~40x 압축** vs unoptimised FP16 baseline
  - "GPU hours are the dominant cost" → 직접 per-token cost 전환

**[영향]**
- DRAFT 8장 "KV offload 가치"를 정량 모델링으로 보강 — 128GB/request는 단일 GPU 메모리 초과 → CXL 메모리 풀의 실현성 정량 근거
- DRAFT 12장 TCO 모델에 FP8 -50% + 4~40x 압축 수치 추가 — KV cache 최적화가 비용 구조에 미치는 영향 정량화
- 상품기획: 128GB/request × 동시 요청 수 = CXL 메모리 풀 용량 산정의 정량 기준 획득 (예: 100 동시 요청 = 12.8TB → Marvell 48TB 스위치로 커버)

**[액션]**
- DRAFT 8장에 70B/32K = 128GB KV cache/request 정량 수치 추가
- DRAFT 12장 TCO 모델에 FP8 -50% + 4~40x 비용 압축 수치 추가
- DRAFT 12장에 "CXL 풀 용량 산정 정량 기준" (128GB × 동시 요청) 추가

## 🎪 업계 이벤트 / 학회 (별도 정리)

> 2호 조사 기간(2026-07~08) 중 3개 이벤트 포착. 각 이벤트별 발표/전시 요약 + 자료 링크.
> ⚠️ 이미지/블럭다이어그램/발표 슬라이드는 WebFetch가 직접 다운로드/호스팅하지 못함 → 원문 URL 제공으로 사용자가 직접 방문해 확보. 잡히는 image URL은 인라인 hotlink(원문 저작권).

### 이벤트 1: FMS 2026 (Future of Memory and Storage)

- **개요**: 2026-08-04 개막, 산타클라라 (Future of Memory and Storage). 메모리/스토리지 업계 최대 연례 행사. CXL 3.2 양산/CXL 4.0 생태 마케팅 가속점.
- **주요 발표/전시 요약** (벤더별):
  - **Marvell**: Bravera SC6 + Structera CXL switches — **단일 스위치 뒤 최대 48TB AI memory** 집계. "Agentic AI Inference" 프레임 신규 발표(1호 delta-6). agentic 워크플로 캐시 특성이 KV cache 오프로드 use case 구체화.
  - **Kioxia**: XL1 Series CXL memory expansion module — XL-FLASH(저지연 플래시) + CXL 결합, DRAM 사용량 최적화. DRAM-플래시 성능 갭 브리지.
  - **ScaleFlux**: MC600 CXL Memory Controller + FC6116 PCIe Gen6 SSD Controller (2026-07-28 사전 발표, FMS 상세). 차세대 PCIe Gen6 실리콘 2종.
  - **XCENA**: **최대 20TB CXL memory pool** 풀링 시스템 데모 + **KV cache sharing 데모**(하드웨어 단계). MX1 컴퓨테이셔널 메모리 컨트롤러(RISC-V) 기반.
  - **CXL Consortium**: 참가 — CXL 생태 홍보. (상세 세션 미확보)
- **자료 링크**:
  - Marvell 48TB 스위치: https://futurumgroup.com/insights/marvell-scales-ai-memory-to-48tb-behind-a-single-cxl-switch-at-fms-2026/
  - Kioxia XL1: https://www.businesswire.com/news/home/20260803920975/en/ (BusinessWire) / https://www.storagenewsletter.com/2026/08/04/fms-2026-kioxia-to-showcase-cxl-compatible-memory-expansion-module-kioxia-xl1-series-for-ai-workloads/
  - ScaleFlux MC600: https://www.storagenewsletter.com/2026/07/31/fms-2026-scaleflux-unveils-pcie-gen6-ssd-and-cxl-memory-controllers/
  - XCENA 20TB 풀링/KV 데모: https://blocksandfiles.com (FMS 2026 XCENA 데모 보도, 2026-08-04)
- **CXL 상품기획 연관점**: Delta-2(FMS 2026 하드웨어), Delta-1(Montage, FMS 맥락). CXL 메모리 풀 단위 용량 20~48TB 확장, KV cache sharing 하드웨어 데모 단계 → 대규모 KV offload 실현성 근거.

### 이벤트 2: ISCA 2026 (International Symposium on Computer Architecture)

- **개요**: 2026-07-01 (학회 발표). 컴퓨터 아키텍처 최상위 학회. CXL 컨트롤러/패브릭 스위치 next-stage 아키텍처 학회 레벨 공개.
- **주요 발표/전시 요약**:
  - **Panmnesia**: **"Silicon-Proven Unified Low-Latency CXL Controller"** + 그 위에 구축된 **fabric switch** 발표. CXL 컨트롤러 → fabric switch 확장 방향성. "next-stage" 표현이 다음 CXL 세대(3.x→4.0) 컨트롤러 사전 검증 신호.
- **자료 링크**:
  - Panmnesia ISCA 2026 발표: https://www.storagenewsletter.com/2026/07/01/panmnesia-unveils-next-stage-cxl-switch-and-controller/
  - (ISCA 2026 공식 프로그램/논문 PDF는 본 조사 미확보 — 학회 페이지 직접 확인 권장)
- **CXL 상품기획 연관점**: Delta-3(Panmnesia ISCA 2026). DRAFT 12장 아키텍처 옵션 보강 근거 — 컨트롤러+fabric switch 결합이 학회 검증 단계.

### 이벤트 3: CXL Mini-DevCon 2026

- **개요**: 2026-08-03, Santa Clara Marriott. CXL Consortium 자체 주최 mini devcon. FMS 직전 하루 전 개최.
- **주요 발표/전시 요약**:
  - 하드웨어 데모 2026-08-04 보도(blocksandfiles.com). 상세 세션/발표 내용은 본 조사 미확보.
- **자료 링크**:
  - CXL Mini-DevCon: https://www.computeexpresslink.org / https://10times.com (이벤트 리스트)
  - 데모 보도: https://blocksandfiles.com
- **CXL 상품기획 연관점**: 카테고리 1(CXL 스펙/표준) 보강. 컨소시엄 자체 이벤트로 CXL 생태 활동 지속 신호. (Delta 본문 반영 아닌 이벤트 메모)

> 후속 추적: FMS 2026 상세 세션/키노트 자료, ISCA 2026 논문 PDF, CXL Mini-DevCon 발표 슬라이드는 3호에서 재추적 권장(agenda 보강).

## 🗞️ 테크/서버 사이트 Top 헤드라인 (타이틀만 취합)

> 본 CXL/메모리 본조사 밖의 넓은 서버 생태 신호. 타이틀만, 본문 요약 없음.
> 각 사이트 홈 1회 WebFetch (캡처 시각: 2026-08-06 04:30 KST 전후, 일중 랭킹 변동 가능).

### The Register — Top Stories (명시적 Top 3)
1. Microsoft tells engineers to curb their token-burning enthusiasm (AI and ML)
2. London cops handed victim's new address and number to her stalker, watchdog says (Security)
3. Meta wants to get inside your terminal with its new coding agent (AI and ML)

### ServeTheHome — Featured (홈 상단)
- Gigantic DapuStor R6060 512TB E2 NVMe SSD Shown at FMS 2026 ★ (Storage)
- AMD Helios Architecture Deep Dive: The Power of AMD's Hardware Combined (Accelerators)
- Lenovo ThinkPad X1 Carbon Gen 14 Review (Mobile)
- ASUS Showcases NUC 16 Family Powered By Panther Lake (Workstation)

### Tom's Hardware — Trending / News Stream 상단
- AMD Advancing AI
- RAM Shortage
- AI Data Centers
- AMD Instinct MI455X
- CXMT's DRAM ambitions could have it capture 30% of the market by 2030 ★ (News Stream)
- Microsoft quietly purges 32GB of RAM recommendations from its website (News Stream)

### Phoronix — Most Popular News This Week
- The First Open-Source Firmware Released For Modern AMD Ryzen AM5 Platform
- Arch Linux AUR Under Another Wave Of Malicious Packages, Package Adoptions Halted
- Linux 7.3 Looks Like It Will Upstream FailFS
- AMD Begins Posting Display Core Next 6 "DCN6" Linux Patches For RDNA5 GPUs

### Data Center Dynamics — Latest News / Long Reads 상단
- AMD posts Q2 '26 revenue of $11.5bn, with data center revenue up 107% for the quarter ★ (Latest News)
- Duke Energy data center pipeline grows by 2.7GW since Q4 2025 (Latest News)
- NSF plans $100m AI Infrastructure Hubs program to boost science R&D (Latest News)
- Nvidia's LPU gamble (Long Reads)

> ★ 표시 = CXL/메모리/AI 인프라 직접 관련 → 본문 delta/인사이트와 교차 확인 대상.
> ServeTheHome(DapuStor 512TB E2 @ FMS 2026)·Tom's Hardware(CXMT 30%/RAM shortage/Microsoft RAM 추천 purge)·DCD(AMD data center +107%)·Phoronix(AMD firmware)는 본조사 카테고리 2/5/6/8/11과 간접~직접 연관.

## 🔍 미변경 카테고리 (변동 없음)

| 카테고리 | 상태 | 비고 |
|---|---|---|
| 1. CXL 스펙/표준 | 🟦 보강 | CXL Mini-DevCon 2026-08-03 개최 사실 추가(Delta 반영 아닌 이벤트 메모), CXL 4.0 스펙 live 상태 확인 |
| 5. 서버 OEM | ⚪ 미변경 | Dell/HPE/Lenovo/Supermicro CXL GA 서버 이미 시장(2026-06), 신규 발표 없음 |
| 6. CPU/GPU CXL | ⚪ 미변경 | Intel Xeon/AMD EPYC/ARM Neoverse/NVIDIA CXL 지원 mid-2026 GA, 신규 발표 없음 |
| 7. AI 패브릭 | ⚪ 미변경 | UALink 2.0(2026-04-07)/200G, NVLink 5.0 1.8TB/s, 3-way 경쟁 — 기준선 v0.4와 일치 |
| 9. AI Rack/KV offload | ⚪ 미변경 | Mooncake 75%/vLLM connector/LMCache(2026-05) — 기준선 v0.4와 일치, 최신 갱신 없음 |

> 카테고리 1(CXL 스펙)은 Mini-DevCon 이벤트로 미변경이나, 컨소시엄 활동 지속 확인. 카테고리 5/6/7/9는 기준선 v0.4에서 현시점까지 추가 변동 미확인.

## 📈 기준선 대비 delta 요약 매트릭스

| # | 항목 | 기준선(v0.4) | 오늘(2026-08-06) | 영향도 |
|---|---|---|---|---|
| 1 | Montage CXL 3.2 컨트롤러 | 7개 벤더 중 하나, 일정 미상세 | MXC M88MX6852 CXL 3.2 스펙 기준 최초 trial production(2026-07-30) | ★★★ |
| 2 | FMS 2026 CXL 하드웨어 | Marvell "Agentic AI" 프레임만 | Marvell 48TB switch / Kioxia XL1 / ScaleFlux MC600 / XCENA 20TB+KV 데모 | ★★ |
| 3 | Panmnesia | 7개 벤더 중 하나 | ISCA 2026 next-stage controller + fabric switch(2026-07-01) | ★★ |
| 4 | Liqid 풀링 | 생태 벤더 언급 | EX-5410C 40TB/chassis → 160TB+ pool, PNNL Abaco 적용 | ★★ |
| 5 | HBM 실적 | 점유율 62/21/17 + Samsung 30% 목표 | Micron $41.46B / Samsung +756% / SK 72% / HBM output +62% / HBM4 ramping | ★★ |
| 6 | Hyperscaler CapEx | 합산 $600-770B | $650-725B 상세 분해(Amazon 200/Google 185/Meta 125) + 전력 60%+ + Q1 $130B | ★★ |
| 7 | DRAM 가격 | Q3 +13~18% QoQ 상승 | + 소비자 측 둔화 신호 + AI/서버 측 지속 이중 추세 | ★ |
| 8 | KV cache 정량 | 정성 중심 | 70B/32K = 128GB/request, FP8 -50%, 4~40x 비용 압축 | ★ |

## 📋 후속 액션 (DRAFT 보강)

- [ ] DRAFT 3장 Montage 행: CXL 3.2 MXC M88MX6852 trial production(2026-07-30) 추가 — Delta-1
- [ ] DRAFT 3장: "벤더별 CXL 세대 분화" 관점 추가 — Delta-1
- [ ] DRAFT 4장: Marvell 48TB single switch 수치 추가 — Delta-2
- [ ] DRAFT 2장: Kioxia XL1(XL-FLASH + CXL) 미디어 추가 — Delta-2
- [ ] DRAFT 3장 ScaleFlux 행: MC600 + FC6116 추가 — Delta-2
- [ ] DRAFT 3장 XCENA 행: 20TB 풀링 데모 + KV cache sharing 추가 — Delta-2
- [ ] DRAFT 8장: XCENA KV cache sharing 데모 역링크 — Delta-2
- [ ] DRAFT 3장 Panmnesia 행: ISCA 2026 next-stage controller + fabric switch(2026-07-01) 추가 — Delta-3
- [ ] DRAFT 4장: Liqid EX-5410C(40TB/chassis → 160TB+ pool, PNNL Abaco, 2026-08-04) 추가 — Delta-4
- [ ] DRAFT 4장: 2026 CXL 생태 맵(Astera Leo/Samsung CMM-D/Micron CZ120/SK Hynix Niagara/Kioxia/MemVerge/Liqid Matrix) 정리 — Delta-4
- [ ] DRAFT 10장: 2026 HBM output +62% YoY, 가격 +20-40% YoY, 3사 실적(Micron $41.46B/Samsung +756%/SK 72%) 추가 — Delta-5
- [ ] DRAFT 10장: HBM 점유율 단일 수치 → 범위 표기 조정(출처별 분산 공개) — Delta-5
- [ ] DRAFT 0장: HBM3E dominates / HBM4 ramping 상태 추가 — Delta-5
- [ ] DRAFT 11장: CapEx 상세 분해 + +70-77% YoY + ~75% AI + Q1 $130B 집행 추가 — Delta-6
- [ ] DRAFT 11장: "전력 60%+ 지출" 비용 구조 인사이트 추가 — Delta-6
- [ ] DRAFT 12장: "전력/랙 효율" 포지셔닝 강화 — Delta-6
- [ ] DRAFT 10장: DRAM 가격 "소비자 측 둔화 + AI/서버 측 지속" 이중 추세 추가 — Delta-7
- [ ] DRAFT 8장: 70B/32K = 128GB KV cache/request 정량 수치 추가 — Delta-8
- [ ] DRAFT 12장 TCO: FP8 -50% + 4~40x 비용 압축 수치 추가 — Delta-8
- [ ] DRAFT 12장: "CXL 풀 용량 산정 정량 기준"(128GB × 동시 요청) 추가 — Delta-8

> ★★★ delta 1건(Montage CXL 3.2), ★★ delta 5건, ★ delta 2건. 총 delta 8건. DRAFT v0.4 → v0.5 보강 예정.

## 📁 관련 파일

- 원시 데이터: [sources/cxl-daily-raw-2026-08-06.md](../../sources/cxl-daily-raw-2026-08-06.md)
- 기준선 DRAFT: [wiki/concepts/cxl-memory-product-planning-draft.md](../concepts/cxl-memory-product-planning-draft.md)
- 직전 Daily Update: [wiki/daily-updates/cxl-daily-update-2026-08-04.md](cxl-daily-update-2026-08-04.md)
- 핸드오프: [wiki/concepts/cxl-product-planning-session-handoff.md](../concepts/cxl-product-planning-session-handoff.md)
- Daily Update 루틴 설계: [wiki/concepts/cxl-daily-update-auto-routine.md](../concepts/cxl-daily-update-auto-routine.md)

## 데이터 한계 공개

- **HBM 점유율 출처별 분산**: 01.co(SK 60%/Micron 22%/Samsung 18%) vs presenc.ai(SK 50-62%/Micron 5-20%/Samsung 25-40%) — 단일 수치 아닌 범위로 취급. 기준선 v0.4의 62/21/17은 SK 상단치 기준으로 추정.
- **WebFetch 백엔드**: Google Search 직접 WebFetch 차단 → DuckDuckGo HTML 폴백으로 12/12 카테고리 수집 완료. 일부 카테고리(5/6/7/9)는 2026-07~08 신규 발표 미확인 → 기준선 v0.4 기준 미변경 처리.
- **날짜 분포**: 대부분 2026-07~08(FMS 2026 집중), 카테고리 9(Mooncake/vLLM)은 2026-05 데이터로 최신 갱신 없음.
- **MRDIMM**: 구체 throughput 수치 미확보.
- **CXL 4.0 세부 일정**: "약 1-2년마다 업데이트" 추정치 외 구체 다음 버전 일정 미확인.
- **이 보고서는 WebFetch 공개 소스 기반** — 사내 비공개 정보/실물 데모 관찰 미포함. 수치는 발표 시점 기준.
