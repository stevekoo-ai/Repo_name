---
title: "CXL Daily Update — 2026-08-04"
created: 2026-08-04
updated: 2026-08-04
tags: [cxl, daily-update, delta, insight, market-intel]
baseline: "DRAFT v0.3 + 0장(훑어보기, 2026-08-03)"
---

# CXL Daily Update Report — 2026-08-04

> 발행일: 2026-08-04 09:26 KST
> 기준선: 2026-08-03 DRAFT v0.3 + "0장 최신 업데이트(훑어보기)"
> 조사 방법: 9개 카테고리 전수 WebFetch 조사 (FMS 2026 컨퍼런스 8/4 산타클라라 시작에 맞춰 다수 발표)
> 형식: 각 delta별 [변경]/[영향]/[액션]

---

## 📰 헤드라인 (오늘의 핵심)

1. **FMS 2026 컨퍼런스 오늘(8/4) 산타클라라 개막** — Kioxia XL1, Marvell, ScaleFlux, CXL Consortium 다수 발표 예정
2. **UALink 2.0 (2026.04) 발표** — 기존 DRAFT는 1.0(2025.04)까지만 기재 → **진짜 delta**
3. **AI 패브릭 3-way rivalry로 확정** — UALink vs NVIDIA vs **Ultra Ethernet**(기존 2-way에서 3-way)
4. **JEDEC, DDR6/LPDDR6에서 CAMM2 표준화 확정, 기존 레이아웃 단계적 폐지 예고**
5. **Q3 DRAM 가격 13~18% 상승** (구체 수치) — 초기 DDR6/CAMM2 "천문학적 가격" 경고
6. **HBM 점유율 구체화**: SK Hynix 62% / Micron 21% / Samsung 17% → Samsung 내년 30%+ 목표
7. **Hyperscaler 2026 AI 인프라 지출 $600B~$770B** (전체 합산, 기존 Alphabet $195-205B만 기재)
8. **NVIDIA Vera Rubin 상세**: 88-core CPU + 336B 트랜지스터 GPU, "Blackwell 대비 5배 추론 성능"

---

## 📊 Delta 상세 (기준선 대비 변경)

### Delta-1: AI 패브릭 — UALink 2.0 + 3-way rivalry <span style="color:red">★중요</span>

**[변경]**
- 기존 DRAFT(6장)는 UALink 1.0(2025.04, 1,024 가속기)까지만 기재
- **UALink 2.0이 2026.04에 발표**된 사실 추가. 상용 HW는 **2026.12** 예정
- **3-way rivalry로 확정**: UALink vs NVIDIA(독점) vs **Ultra Ethernet** (기존 2-way에서 3-way)
- NVIDIA는 "licensing initiative"(=NVLink Fusion)로 제3자 개발자에게 호환성 개방
- UALink는 "최초의 신뢰할 수 있는 개방형 대안"

**[영향]**
- CXL의 진영 중립적 위치가 더 명확해짐 — 3-way 패브릭 경쟁 모두에 메모리 풀 레이어로 부착 가능
- Ultra Ethernet이 새로운 변수 — CXL 4.0 패브릭과 Ultra Ethernet의 관계 정리 필요
- 상품기획: 3개 진영 모두를 지원하는 "진영 중립적 메모리 풀" 포지셔닝(12.2 옵션4) 가치 상승

**[액션]**
- DRAFT 6장에 UALink 2.0(2026.04) + Ultra Ethernet 3-way rivalry 추가 보강
- Ultra Ethernet vs CXL 4.0 패브릭 관계 심층 조사 필요

---

### Delta-2: Main Memory — JEDEC CAMM2 표준화 + 가격 경고 <span style="color:red">★중요</span>

**[변경]**
- 기존 DRAFT(7장)는 CAMM2/LPCAMM2/SOCAMM2를 DDR6/LPDDR6 폼팩터로 언급
- **JEDEC가 표준 메모리 레이아웃을 단계적 폐지하고 DDR6/LPDDR6에서 CAMM2로 전환** 예고
- **Q3 DRAM 가격 13~18% 상승**(구체 수치, 기존은 "인상" 정성)
- 원인: 서버 수요 + wafer가 고수익 앱(HBM 등)으로 이동
- **초기 DDR6/CAMM2 HW는 "천문학적 가격" 경고**(공급 압박)

**[영향]**
- 메인메모리 폼팩터 전환이 CXL 메모리 모듈 설계에 직결 — CXL 컨트롤러가 DDR5/6 채널을 쓰므로 CAMM2 전환 일정이 CXL 모듈 로드맵에 영향
- 가격 상승 → CXL 메모리 풀링의 비용 절감 가치 상승(overprovisioning 회피)
- 단, 초기 DDR6/CAMM2 고가 → 단기 CXL 메모리 비용 프리미엄 확대 가능

**[액션]**
- DRAFT 7장에 JEDEC CAMM2 표준화 일정 + Q3 가격 13~18% 수치 추가
- CAMM2 전환 일정 vs CXL 모듈 로드맵 정합성 검토

---

### Delta-3: HBM 점유율 + 16-layer 로드맵 <span style="color:red">★중요</span>

**[변경]**
- 기존 0장(훑어보기)은 SK Hynix Q2 실적만 기재, 점유율 미기재
- **HBM 점유율 구체**: SK Hynix 62% / Micron 21% / Samsung 17%
- **Samsung 내년(2027) HBM 점유율 30%+ 목표** — 현재 17%에서 대폭 확대
- 3사 모두 **8-layer HBM3E 양산**, 12-layer/16-layer 진행
- **NVIDIA가 2026 말 16-layer HBM 요청**

**[영향]**
- Samsung의 HBM 역공이 본격화 — 17%→30%+ 목표는 SK Hynix 62% 지배에 대한 도전
- 16-layer HBM이 2026 말 NVIDIA 요청 → SK하이닉스/Samsung 양산 경쟁 격화
- HBM 3사 경쟁 심화 → 본문 10장 "2026 HBM 가격 하방 압력" 가설 강화

**[액션]**
- DRAFT 10장/11.3장에 HBM 점유율(62/21/17) + Samsung 30%+ 목표 + 16-layer 로드맵 추가
- SK하이닉스 관점: 점유율 방어 전략 vs CXL 차별화 가치 재검증

---

### Delta-4: Hyperscaler 2026 AI 인프라 지출 $600B~$770B

**[변경]**
- 기존 0장은 Alphabet(Google) $195-205B만 기재
- **Google/Microsoft/Meta/Amazon 합산 2026 AI 인프라 지출 $600B~$770B**
- CXL을 통한 메모리 disaggregation이 이 자본을 효율화하는 핵심 수단("stranded DRAM → shared pools, overprovisioning 제거")

**[영향]**
- $600-770B 규모 자본이 CXL 풀링 채택의 자본 여력 — 본문 11장 "CSP 채택 가속" 강화
- composable 아키텍처가 대규모 자본 효율화의 핵심 → CXL 풀링 상품 기획의 시장 타당성 강화

**[액션]**
- DRAFT 11.2장에 hyperscaler 합산 $600-770B 수치 추가 (Alphabet 단일에서 합산으로 확장)

---

### Delta-5: NVIDIA Vera Rubin 상세 + SK Hynix 정렬

**[변경]**
- 기존 0장은 "Vera Rubin 가속기용 HBM 장기 공급"만 언급
- **Vera Rubin 상세**: 88-core 커스텀 CPU + 336B 트랜지스터 GPU, **"Blackwell 대비 5배 추론 성능"**, 더 저렴한 토큰 생성 목표
- AMD MI350은 "고용량 GPU 메모리로 가격 비효율 주소" 강조

**[영향]**
- Vera Rubin 5배 추론 성능 → KV cache 메모리 요구 폭증 → CXL 풀링 수요 증폭
- SK하이닉스가 Vera Rubin HBM 공급자 → SK하이닉스 CXL 전략을 NVIDIA 생태와 정렬하는 근거 강화(0장 시사점 확인)

**[액션]**
- DRAFT 0장/9장에 Vera Rubin 5배 추론 성능 수치 추가 → KV cache 요구량 모델 업데이트 필요

---

### Delta-6: FMS 2026 컨퍼런스 개막 (8/4 산타클라라)

**[변경]**
- 기존 DRAFT는 개별 벤더 발표만 산재
- **FMS 2026(Future of Memory and Storage) 오늘(8/4) 산타클라라 개막** — Kioxia XL1, Marvell(Agentic AI Inference 포트폴리오), ScaleFlux(2개 Gen6 실리콘), CXL Consortium 모두 참가
- Marvell: "Agentic AI Inference" 프레임 신규 — 기존 "AI 인프라"에서 "Agentic AI"로 정제
- ScaleFlux: 2개 차세대 PCIe Gen6 실리콘 솔루션 소개(본문 MC600/FC6116과 정합)

**[영향]**
- FMS 2026이 CXL 3.2 양산/CXL 4.0 생태의 마케팅 가속점 — 본문 제품 동향의 발표 시점 기준
- "Agentic AI Inference" 프레임 — KV cache 오프로드 use case가 더 구체화(agentic 워크플로의 캐시 특성)

**[액션]**
- FMS 2026 발표를 본문 3장/4장에 반영 (이미 대부분 반영되었으나 Agentic AI 프레임 추가)

---

### Delta-7: Mooncake 메트릭 구체화

**[변경]**
- 기존 DRAFT(8.3)는 Mooncake 아키텍처만 기재
- **Mooncake+vLLM 결합 메트릭**: "latency 대폭 감소, agentic 워크플로 처리량 향상", CPU/Disk 오프로드로 더 큰 컨텍스트 윈도우

**[영향]**
- Mooncake의 KV cache 중심 disagg 아키텍처가 CXL 풀과 결합 시 정량적 이점 검증
- agentic 워크플로 — 토큰 생성보다 캐시 처리가 병목 → CXL 풀 가치 명확

**[액션]**
- DRAFT 8.3장에 Mooncake+vLLM 메트릭 추가

---

## 🔍 미변경 카테고리 (변동 없음)

| 카테고리 | 상태 | 비고 |
|---|---|---|
| CXL 스펙 버전 | 미변경 | CXL 4.0(2025.11.18), 3.2 양산 — 0장과 일치 |
| CXL 디바이스 타입 | 미변경 | Type 1/2/3 — 본문 2.2절 유지 |
| Intel/AMD CXL 지원 | 미변경 | Granite Rapids CXL 2.0, Turin CXL 2.0, Diamond Rapids mid-2027 — 본문 5장 유지 |
| GPU CXL | 미변경 | MI350 288GB/8TB/s, NVIDIA CXL 미사용 — 본문 5.2절 유지 |
| 풀링 아키텍처(Expansion/Pooling/Sharing) | 미변경 | 4.7절 유지 |
| XCENA | 미변경 | MX1/MX1P/MX1S — 본문 3장 유지 |

---

## 📈 기준선 대비 delta 요약 매트릭스

| # | 항목 | 기준선(8/3) | 오늘(8/4) | 영향도 |
|---|---|---|---|---|
| 1 | UALink | 1.0(2025.04) | **2.0(2026.04) + 3-way(Ultra Ethernet)** | ★★★ |
| 2 | AI 패브릭 경쟁 | 2-way | **3-way (UALink/NVIDIA/Ultra Ethernet)** | ★★★ |
| 3 | JEDEC CAMM2 | 폼팩터 언급 | **표준화 확정, 기존 레이아웃 폐지** | ★★★ |
| 4 | Q3 DRAM 가격 | "인상" | **13~18% 상승** | ★★ |
| 5 | DDR6/CAMM2 가격 | 미언급 | **"천문학적 가격" 경고** | ★★ |
| 6 | HBM 점유율 | 미기재 | **SK 62/Micron 21/Samsung 17** | ★★★ |
| 7 | Samsung HBM 목표 | 미기재 | **내년 30%+ (17%→30%)** | ★★★ |
| 8 | 16-layer HBM | 미기재 | **NVIDIA 2026 말 16-layer 요청** | ★★ |
| 9 | Hyperscaler CapEx | Alphabet $195-205B | **합산 $600-770B** | ★★★ |
| 10 | Vera Rubin | "HBM 공급" | **88-core+336B, 5배 추론 성능** | ★★ |
| 11 | FMS 2026 | 미언급 | **8/4 산타클라라 개막** | ★★ |
| 12 | Marvell 프레임 | "AI 인프라" | **"Agentic AI Inference"** | ★ |
| 13 | Mooncake 메트릭 | 아키텍처만 | **vLLM 결합 메트릭(latency↓/처리량↑)** | ★ |

---

## 🎯 종합 인사이트 (상품기획 시사점)

1. **AI 패브릭 3-way 경쟁 확정** → CXL "진영 중립적 메모리 풀" 포지셔닝(12.2 옵션4) 가치 상승. 3개 진영 모두에 부착 가능한 유일한 메모리 레이어
2. **CAMM2 표준화 + Q3 가격 13~18% 상승** → CXL 메모리 풀링의 overprovisioning 절감 가치 강화. 단, 초기 DDR6/CAMM2 고가 → CXL 비용 프리미엄 단기 확대 가능성
3. **Samsung HBM 역공(17%→30%+)** + NVIDIA 16-layer 요청 → HBM 경쟁 심화 → 가격 하방(본문 10장 가설 강화). SK하이닉스는 점유율 방어 + CXL 차별화 동시 추진 필요
4. **Hyperscaler $600-770B 자본** → CXL 풀링 채택 자본 여력 압도적. 상품 기획의 시장 타당성 강력
5. **Vera Rubin 5배 추론 성능** → KV cache 요구 폭증 → CXL KV cache 풀(cleanest win use case) 수요 확정적 증가
6. **Agentic AI Inference 프레임** → agentic 워크플로의 캐시 특성이 KV cache 오프로드 use case를 더 구체화

---

## 📋 후속 액션 (DRAFT 보강)

- [ ] DRAFT 6장: UALink 2.0(2026.04) + Ultra Ethernet 3-way rivalry 추가
- [ ] DRAFT 7장: JEDEC CAMM2 표준화 일정 + Q3 가격 13~18% 수치 + "천문학적 가격" 경고 추가
- [ ] DRAFT 10장/11.3장: HBM 점유율(62/21/17) + Samsung 30%+ 목표 + 16-layer 로드맵 추가
- [ ] DRAFT 11.2장: hyperscaler 합산 $600-770B 수치 추가
- [ ] DRAFT 0장/9장: Vera Rubin 5배 추론 성능 수치 추가
- [ ] DRAFT 3장/4장: FMS 2026 + Marvell "Agentic AI Inference" 프레임 추가
- [ ] DRAFT 8.3장: Mooncake+vLLM 메트릭 추가

---

## 📁 관련 파일

- 기준선 DRAFT: `wiki/concepts/cxl-memory-product-planning-draft.md` (v0.3 + 0장)
- HTML 보고서: `wiki/cxl-memory-product-planning-report-2026-08-04-0906.html`
- 본 Daily Update(HTML): `wiki/cxl-daily-report-2026-08-04-0926.html`
- 본 Daily Update(MD): `wiki/daily-updates/cxl-daily-update-2026-08-04.md`

---

## 데이터 한계 공개

- WebSearch API 백엔드 장애 지속 → WebFetch + DuckDuckGo HTML 경유
- FMS 2026(8/4 개막) 발표가 진행 중이라 일부 발표 내용은 일정 공개만 확인됨 — 추가 발표 시 보강 필요
- UALink 2.0 세부 스펙(1.0의 1,024 가속기 대비 확장 규모)은 미확인 — 후속 조사 필요
- Ultra Ethernet vs CXL 4.0 패브릭 관계는 본 조사에서 명확하지 않음 — 심층 조사 필요
- 중요 수치(HBM 점유율, CapEx)는 단일 출처 기반 가능 → 1차 출처 교차검증 권장
