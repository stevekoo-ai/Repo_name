---
title: "AI 패브릭 3-way 경쟁과 CXL의 레이어 분담 (UALink / NVLink / Ultra Ethernet vs CXL 4.0)"
created: 2026-08-04
updated: 2026-08-04
tags: [cxl, ai-fabric, ualink, nvlink, ultra-ethernet, scale-up, scale-out, memory-pooling, product-planning]
---

# AI 패브릭 3-way 경쟁과 CXL의 레이어 분담

> 2026-08-04 심층 조사. DRAFT v0.4 6장(6.2b) 보강용. 핵심 질문: **Ultra Ethernet은 CXL 4.0과 경쟁하는가, 아니면 다른 레이어인가?** 결론: **다른 레이어다** — Ultra Ethernet/UALink/NVLink는 GPU/XPU **스케일업·스케일아웃 패브릭**이고, CXL 4.0은 **메모리 풀링/disaggregation 레이어**. 경쟁이 아니라 공존·보완.

---

## 1. 3-way 패브릭 경쟁의 실체 (GPU/XPU 연결 레이어)

AI 가속기를 어떻게 연결하느냐(= "GPU 스케일업/스케일아웃 패브릭")를 둘러싼 3개 진영. **모두 GPU/XPU 간 통신 패브릭** — 메모리 풀링과는 다른 계층.

| 진영 | 프로토콜 성격 | 스케일 | 핵심 사실 |
|---|---|---|---|
| **NVIDIA NVLink** | 독점/폐쇄 | 최대 576 GPU | NVLink Fusion("licensing initiative")으로 제3자 개발자에게 호환성 개방하며 진영 방어 |
| **UALink** | 개방형 컨소시엄, **신규 스케일업 프로토콜** | 단일 패브릭 1,024 가속기(1.0), 200 GT/s/라인 | 2025.04 UALink 1.0 → **2026.04 UALink 2.0**, 상용 HW 2026.12. "최초의 신뢰할 수 있는 개방형 대안" |
| **Ultra Ethernet (UEC)** | 개방형, **이더넷 기반 스케일아웃** | 데이터센터 전체 | "Ethernet remains the scale-out standard" 확장. tail latency 최적화. spec v1.0.3 |

### 핵심 인용 (1차 조사)
- **"UALink is a completely new scale-up protocol, while Ultra Ethernet builds on Ethernet for scale-out."** — UALink=스케일업, Ultra Ethernet=스케일아웃. **둘은 경쟁이 아니라 보완**.
- UALink v1은 단순성 우선 설계, UEC RC1은 565페이지 방대 명세(다중 벤더 상호운용성 중점).
- 일부 출처는 "UALink, Ultra Ethernet, Huawei UB-Mesh compete"로 묶어 스케일아웃/스케업 맥락의 3-way(+) 경쟁으로 서술 — GPU/XPU 패브릭 레이어 내 경쟁.

---

## 2. Ultra Ethernet Consortium (UEC) 상세

- **위상**: 리눅스 재단 JDF 산하 ISO 국제 표준 조직. 2026.07.17 갱신.
- **스티어링 멤버(10개사)**: AMD, Cisco, Intel, Meta, Microsoft, Oracle 등
- **일반 멤버**: Alibaba Cloud, ByteDance, Google Cloud, Huawei, **Nvidia**, Qualcomm 등 25개+
- **기여 멤버**: AsteraLabs, Credo, Lightmatter, Micron, Super Micro 등
- **목표**: 개방/상호운용/고성능 풀 통신 스택. 대역폭·지연·꼬리지연(tail latency) 최적화. "tail latency is the figure of merit"
- **제품**: 2024년부터 표준 기반 첫 제품. 관련 SDO 협력해 이더넷 공식 기술로 채택 목표
- **주의**: UEC 공식 사이트에는 **CXL 언급 없음** — UEC는 GPU/XPU 네트워크 패브릭에 집중, CXL(메모리 레이어)과는 명시적 연관 미설정

---

## 3. CXL 4.0의 위치 — 메모리 레이어 (패브릭 경쟁과 다른 계층)

CXL은 위 3-way 경쟁(GPU/XPU 패브릭)과 **경쟁하지 않는다**. CXL 4.0(2025.11.18 확정, 128 GT/s)은 **메모리 분해/disaggregation** 계층에 집중.

| 계층 | 기술 | 역할 |
|---|---|---|
| **GPU/XPU 패브릭** | NVLink / UALink / Ultra Ethernet | 가속기 간 통신(스케일업/스케일아웃) |
| **메모리 풀링 레이어** | **CXL 4.0** | terabyte-scale 공유 메모리, 멀티랙 메모리 풀링, "shared memory resources throughout the data center" |

### 핵심 인용 (1차 조사)
- **"Ultra Ethernet: Scale-out networking across data centers"** — Ultra Ethernet은 데이터센터급 네트워크 패브릭 레이어.
- **CXL 4.0은 할당 리소스 통합보다는 메모리 풀링에 집중** — Ultra Ethernet(네트워크) vs CXL(메모리) 기능 분담 명확.
- **"UALink works alongside PCIe and CXL, but only UALink has the effect of unifying the allocated resources."** — UALink·PCIe·CXL은 **함께 동작(보완)**. 리소스 통합은 UALink, 메모리 풀링은 CXL.

---

## 4. 레이어 분담 모델 (정리)

```
┌─────────────────────────────────────────────┐
│  GPU/XPU 패브릭 (스케일업/스케일아웃)         │  ← 3-way 경쟁
│  NVLink | UALink | Ultra Ethernet             │     (가속기 간 통신)
├─────────────────────────────────────────────┤
│  메모리 풀링 레이어 (disaggregation)          │  ← CXL 4.0
│  CXL 4.0 (128 GT/s, 멀티랙 공유 메모리)       │     (진영 중립적, 3-way 모두에 부착)
├─────────────────────────────────────────────┤
│  호스트 메인 메모리 (DDR5/6, CAMM2, MRDIMM)   │
└─────────────────────────────────────────────┘
```

- **CXL은 GPU/XPU 패브릭 3-way 경쟁의 "아래" 메모리 레이어**에 위치. 어느 패브릭이 이기든 그 위에서 동작하는 가속기는 CXL 메모리 풀에 접근 가능.
- 따라서 CXL = **진영 중립적 메모리 레이어**. 3-way 패브릭 경쟁이 격화될수록 CXL의 진영 리스크 헷지 가치 상승(DRAFT 12.2 옵션4).

---

## 5. 상품기획 시사점

1. **Ultra Ethernet은 CXL의 경쟁자가 아니다** — 레이어가 다름. CXL 메모리 풀 제품 기획 시 Ultra Ethernet을 "위협"으로 분류하는 것은 오류. 오히려 Ultra Ethernet 기반 데이터센터에도 CXL 메모리 풀이 부착되므로 시장 확장.
2. **3-way 경쟁 → CXL 진영 중립 가치 상승** — NVLink/UALink/Ultra Ethernet 중 어느 쪽이 승해도 CXL 메모리 계층은 부착. 진업 리스크에 헷지되는 유일한 메모리 레이어.
3. **UALink·PCIe·CXL은 함께 동작**(1차 인용) — CXL 메모리 풀 제품은 UALink/Ultra Ethernet 패브릭과 명시적 통합 설계 필요(인터페이스·토폴로지).
4. **UEC 멤버에 Nvidia/AsteraLabs/Micron 포함** — Ultra Ethernet 생태의 하드웨어 벤더가 CXL 생태와 겹침 → 벤더 입장에서 두 레이어 동시 지원은 자연스러운 전략.
5. **NVLink 최대 576 GPU vs UALink 1,024** — 규모 한계가 UALink 존재 이유. 단일 랙/포드 규모가 커질수록 메모리 풀링(CXL) 수요도 연쇄 확대.

---

## 6. 미해결 / 후속

- UEC 사이트에 CXL 언급 없음 → Ultra Ethernet ↔ CXL 4.0의 **명시적 통합 토폴로지**(CXL 메모리 풀이 Ultra Ethernet 패브릭 위에서 어떻게 노출되는지)는 1차 문서 미확보. 후속 조사.
- UALink 2.0 세부 스펙(1.0의 1,024 대비 확장 규모) 미확인.
- Huawei UB-Mesh가 3-way+ 경쟁에 포함되는지 별도 확인 필요(중국 진영).

---

## Sources

- [Ultra Ethernet Consortium 공식](https://ultraethernet.org/) (WebFetch, 2026-08-04)
- DuckDuckGo HTML 경유 검색: "Ultra Ethernet Consortium UALink scale up scale out difference CXL" / "Ultra Ethernet CXL 4.0 memory pooling fabric layer coexist" (2026-08-04)
- [CXL DRAFT v0.4 — 6장 AI 패브릭 진영 대치](cxl-memory-product-planning-draft.md)
- [CXL Daily Update 1호 (2026-08-04)](../daily-updates/cxl-daily-update-2026-08-04.md) — delta-1 (UALink 2.0 + 3-way rivalry)

## 데이터 한계 공개

- UEC 공식 사이트에 CXL 직접 언급 없어 레이어 분담은 주로 UALink/Ultra Ethernet 비교 출처 + CXL 스펙 출처 교차 추론. 1차 출처(UALink/CXL 양쪽이 관계를 공식 서술한 문서) 확보 권장.
- "UALink, Ultra Ethernet, Huawei UB-Mesh compete" 인용은 단일 출처 — 3-way(+중국) 경쟁 서술의 교차검증 필요.
- 2026-08-04 조사 기준. UALink 2.0(2026.04) 상용 HW(2026.12) 전후로 관계 재확정 필요.
