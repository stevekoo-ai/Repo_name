---
title: "customer-meetings/ 인덱스 — 미팅 목록 + 상대방별 교차표"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, index]
---

# customer-meetings/ 인덱스

> 2뷰 마스터 인덱스: 미팅별 목록 + 상대방×미팅 교차표.
> 규칙·네이밍은 [README.md](README.md).

---

## 1) 미팅별 목록 (날짜순, 최신→과거)

| 날짜 | 미팅 | 전문 | 등장 상대방 |
|---|---|---|---|
| 2026-08-11 | CXL 메모리 풀링 미팅 | [meetings/2026-08-11-cxl-pooling.md](meetings/2026-08-11-cxl-pooling.md) | MSFT·Oracle·NVIDIA / Marvell·Liqid·Intel·AMD·Qualcomm·ScaleFlux / Micron·Samsung·Kioxia / Panmnesia·Primemas·Penguin |
| 2026-05-27 | DELL TDF CXL Next Gen 스펙 미팅 | [meetings/2026-05-27-dell-tdf-cxl-nextgen.md](meetings/2026-05-27-dell-tdf-cxl-nextgen.md) | Dell / Marvell·Xcena (간접) |
| 2026-05-07 | HPE CXL Gen2 미팅 | [meetings/2026-05-07-hpe-cxl-gen2.md](meetings/2026-05-07-hpe-cxl-gen2.md) | HPE / Montage (간접) |
| 2026-04-30 | MSFT CXL KV Cache 미팅 | [meetings/2026-04-30-msft-cxl-kv-cache.md](meetings/2026-04-30-msft-cxl-kv-cache.md) | MSFT (Phyllis Ng) |
| 2026-03-12 | FMTA CXL 미팅 | [meetings/2026-03-12-fmta-cxl.md](meetings/2026-03-12-fmta-cxl.md) | NVIDIA (법인 F2F) |
| 2026-03-11 | Oracle OCI CXL Pooling 미팅 | [meetings/2026-03-11-oracle-oci-cxl.md](meetings/2026-03-11-oracle-oci-cxl.md) | Oracle / Marvell·Xconn·Montage·Broadcom·AMD (간접) |
| 2026-02-12 | HPE CXL EVB / Gen13 Venice 미팅 | [meetings/2026-02-12-hpe-cxl-evb.md](meetings/2026-02-12-hpe-cxl-evb.md) | HPE (Pope Eric 외) |
| 2026-02-10 | AWS CXL KV Cache 중간 Tier 미팅 | [meetings/2026-02-10-aws-cxl-kv-cache.md](meetings/2026-02-10-aws-cxl-kv-cache.md) | AWS (Ashiq Reza 외 6명) |
| 2026-02-06 | IBM Power Future CXL 미팅 | [meetings/2026-02-06-ibm-power-future.md](meetings/2026-02-06-ibm-power-future.md) | IBM (Patrick Breen·David Cadigan·Gary) |
| 2026-02-05 | Google DRAM/MRDIMM 미팅 (첫 비-CXL) | [meetings/2026-02-05-google-dram-mrdimm.md](meetings/2026-02-05-google-dram-mrdimm.md) | Google (Brian Morris 외 5명) / AMD·Intel (간접) |
| 2026-01-15 | Lenovo CXL CMM 미팅 | [meetings/2026-01-15-lenovo-cxl-cmm.md](meetings/2026-01-15-lenovo-cxl-cmm.md) | Lenovo (Sumanta·SJ Park·Fred·Joymoon) |

---

## 2) 상대방×미팅 교차표 (상대방별 누적 보기 입구)

| 상대방 | relation | by-customer | 미팅 이력 | 현재 상태 |
|---|---|---|---|---|
| Dell | customer | [dell.md](by-customer/dell.md) | 2026-05-27 | PowerEdge AIC align / AI 풀링 전용 재설계 의향 / Tech. meeting 후속 예정 |
| HPE | customer | [hpe.md](by-customer/hpe.md) | 2026-05-07, 2026-02-12 | Gen2 샘플 align(05-07) / 2027-06 Venice Launch / 유럽 PQC FU 미해결 — 단 02-12가 HPE 기원(EVB 8pcs CXL 2.0, Venice Post-Launch, MRDIMM+CXL, CMM x4) |
| NVIDIA | customer | [nvidia.md](by-customer/nvidia.md) | 2026-08-11, 2026-03-12 | KV cache CXL 관심 전환(08-11) — 단 03-12 FMTA에서 질의(**NVIDIA 발의 축 기원**) / 피드백 대기. **KV Cache thread = 두 평행 축**: 자사 발의(AWS 02-10→MSFT 04-30) + NVIDIA 발의(03-12→08-11) |
| Oracle | customer | [oracle.md](by-customer/oracle.md) | 2026-08-11, 2026-03-11 | POC(08-11) / AIC PNM 샘플 대기 — 단 03-11에선 AIC 너무 큼·SPOF 감당 불가 → HA 필수(Montage MHD 경로). Sang Park 이직으로 AIC 재검토 반전 |
| MSFT | customer | [msft.md](by-customer/msft.md) | 2026-08-11, 2026-04-30 | pathfinding / KV Cache 오프로딩 제안(04-30, 자사 발의) → Pooled Appliance 협력(08-11) / TCO·Multi-sourcing 우려 |
| AWS | customer | [aws.md](by-customer/aws.md) | 2026-02-10 | PoC 검증 / **자사 발의 KV Cache 중간 Tier 제안(02-10) = 자사 발의 축 기원** / Killer Use case 안 보임 + 1DPC 선호 / KV Cache 심화 시 중장기 재부상 |
| IBM | customer | [ibm.md](by-customer/ibm.md) | 2026-02-06 | Power Future(@2028) 최초 Native-CXL 2.0 / SAP HANA IMDB $/GB 절감 / 2028 AIC only → 2029 AIC+E3.S 2T / HHHL 256GB 갭 → LPD5/FHHL 검토 / Latency 300→200~250ns / **KV-Cache "다른 기회" 독립 인지(02-06, 가장 이른 KV Cache 언급)** / HMSDK 관심 / **말뭉치 최초 CXL 미팅** |
| Google | customer | [google.md](by-customer/google.md) | 2026-02-05 | **말뭉치 최초 미팅 + 첫 비-CXL(DRAM)** / Intel DMR 48→64GB(GA 27년 1~2월) / 1cnm 96GB NPI Intercept / **DDR5 PRAC 미지원 Google 수용**(DDR6서 논의) / **AMD Venice MRD 필수**·ARM4 RDIMM 백업 / **MRD Gen3 = Default**(Florence Gen4 Q2~3 느림) / LP MRDIMM = AMD 지원 좌우 / DDR6 64Gb·x6 반대(JEDEC) |
| Lenovo | customer | [lenovo.md](by-customer/lenovo.md) | 2026-01-15 | **말뭉치 최초 미팅** / 2세대 CMM ES 26-09말·CS 27-02말(공유 컨트롤러 납기 지연으로 delay) / SIT부터 CS 필수 / Early-ES BBFV 투입 제안 / **CMM 가격이 RDIMM보다 비싸 → sales 부진** → 저등급(Graded memory) DRAM 저가 CMM 개발 요구 / 2nd Gen 512GB 취소 여부 + 3rd Gen FF 문의 |
| Marvell | partner | [marvell.md](by-customer/marvell.md) | 2026-08-11, 2026-05-27, 2026-03-11 | 백서 완료 / Photonics Pooled 연말 ES / CMM AX 공동개발 / **CXL switch 인수(Broadcom 경쟁, Xconn)** |
| Liqid | partner | [liqid.md](by-customer/liqid.md) | 2026-08-11 | CXL3 내년Q3 / Turn-key Box 가능 / OCP |
| Intel | partner | [intel.md](by-customer/intel.md) | 2026-08-11 | Pooled Validation 내부 논의 / GPU Server KV Cache 제안 |
| AMD | partner | [amd.md](by-customer/amd.md) | 2026-08-11, 2026-03-11 | White Paper 공동 작성(Supercomputing) / Dynamo / **DIMM 12→16ch 확장 = Local CXL 가치 훼손**(03-11 간접) |
| Qualcomm | partner | [qualcomm.md](by-customer/qualcomm.md) | 2026-08-11 | 정기 콜 셋업 / Server SOC Validation |
| ScaleFlux | partner | [scaleflux.md](by-customer/scaleflux.md) | 2026-08-11 | 협업 재정렬 3원칙 / 상품기획 이관 |
| Panmnesia | partner | [panmnesia.md](by-customer/panmnesia.md) | 2026-08-11 | Neo-Cloud 타겟 확인 / 논의 시작 필요 |
| Primemas | partner | [primemas.md](by-customer/primemas.md) | 2026-08-11 | Neo-Cloud 타겟 / Abaco 3.0 AIC 담당 |
| Penguin | partner | [penguin.md](by-customer/penguin.md) | 2026-08-11 | Marvell Photonics Appliance Maker (간접) |
| Xcena | partner | [xcena.md](by-customer/xcena.md) | 2026-05-27 | CMM AX 컨트롤러 공동개발 (Structure A Eval Card) / 간접 등장 |
| Xconn | partner | [xconn.md](by-customer/xconn.md) | 2026-03-11 | CXL switch 벤더 / Marvell 인수 대상 / Oracle pooling bottleneck / 4월 Oracle-Xconn/Marvell 재논의 |
| Micron | competitor | [micron.md](by-customer/micron.md) | 2026-08-11 | Abaco 3.0 총괄 리드 / PNNL / famfs |
| Samsung | competitor | [samsung.md](by-customer/samsung.md) | 2026-08-11 | in-house CXL3 controller PoC / Expansion+Processing |
| Kioxia | competitor | [kioxia.md](by-customer/kioxia.md) | 2026-08-11 | CXL 2.0 CXL-SSD 전시 (정보 얕음) |
| Montage | competitor | [montage.md](by-customer/montage.md) | 2026-08-11, 2026-05-07, 2026-03-11 | CXL 3.2 MXC 업계 최초 시료생산 / Gen2 third party (HPE 간접) / **MHD 2포트=HA 경로(Oracle 간접, 8CH/2CH 미해결)** |
| Broadcom | competitor | [broadcom.md](by-customer/broadcom.md) | 2026-03-11 | CXL switch 시장 부정("시장 없다") / Marvell 경쟁 상대 (Xconn 인수 배경) |

---

## 3) 교차검증 대기 (양쪽 언급 등)

- **Dynamo**: NVIDIA(tiering 운영 SW) + AMD(Inference SW Framework) 양쪽 언급 → 동일 SW인지 확인 → [nvidia.md](by-customer/nvidia.md)·[amd.md](by-customer/amd.md)
- **Montage MXC vs CMM AX**: Montage CXL 3.2 MXC 업계 최초 시료생산(2026-08-11 Newsroom) vs 자사 CMM AX(Structure A, Marvell+Xcena, Eval Card 단계, 2026-05-27 Dell) — 컨트롤러 IP 타이밍 격차. HPE Gen2에서는 Montage가 third party(2026-05-07) → HPE Gen3(CXL 3.x) 전환 시 Montage MXC vs 자사 CMM AX 경쟁 → [montage.md](by-customer/montage.md)·[marvell.md](by-customer/marvell.md)·[xcena.md](by-customer/xcena.md)
- **E3.S 주 전망 일관성**: HPE 김의현 TL "E3.S가 주"(2026-05-07) ↔ Dell Stuart Berke "모듈 수 2배 E3 RAS 우세"(2026-05-27) — E3.S/E3 열세권(Serviceability/RAS) 일관. AIC는 초기 Acceptance(05-07) → 고용량 TCO(05-27) → AI 풀링 전용 재설계(05-27)로 진화 → [hpe.md](by-customer/hpe.md)·[dell.md](by-customer/dell.md)
- **★★★ KV Cache CXL thread — 두 평행 축 + IBM 독립 인지 (재정립)**: **(A) 자사 발의 축**: AWS 02-10(자사 중간 Tier 제안) → MSFT 04-30(자사 CXL DM Pooling 제안, Phyllis 동의) → MSFT 08-11 pathfinding. **(B) NVIDIA 발의 축**: NVIDIA 03-12(FMTA 질의) → NVIDIA 08-11(관심 전환 ★★★). **(C) IBM 독립 인지**: **IBM 02-06(가장 이른 KV Cache 언급 기록 — "Gen6 케이스에서 KV-Cache 다른 기회, NVMe 대비 워크로드 성능 향상" 고객 측 독립 인식)**. 두 축은 08-11에서 수렴, IBM 02-06은 자사/NVIDIA 양 축과 별개 고객 측 인지. 공통 배경 = "AI 확산→KV Cache 폭증, Storage spillover 시 성능 급락"(AWS 02-10 명시, IBM 02-06이 "KV-Cache 다른 기회"로 4일 앞선 최초 언급). **정정 이력**: 04-30=기원 → 03-12 NVIDIA=기원 → 02-10 AWS(자사 발의)+03-12 NVIDIA(NVIDIA 발의) 두 축 → **02-06 IBM 독립 인지(3번째 출처) 추가**. → [aws.md](by-customer/aws.md)·[nvidia.md](by-customer/nvidia.md)·[msft.md](by-customer/msft.md)·[ibm.md](by-customer/ibm.md)·[../meetings/2026-02-10-aws-cxl-kv-cache.md](meetings/2026-02-10-aws-cxl-kv-cache.md)·[../meetings/2026-03-12-fmta-cxl.md](meetings/2026-03-12-fmta-cxl.md)·[../meetings/2026-02-06-ibm-power-future.md](meetings/2026-02-06-ibm-power-future.md)
- **폼팩터 + Cooling thread (7-way)**: **AWS 02-10 "1DPC 선호 + 용량만 확장"** ↔ **HPE 02-12 "E3.S slot 수 + PCIe lane 수 제약 → CMM 고용량 + x4 모드(NVMe backplane 호환)"** ↔ FMTA 03-12 "Liquid Cooling엔 E1.S 적합, E3.S는 크다" ↔ **Oracle 03-11 "AIC 너무 큼 + Liquid 사용 불가"** ↔ HPE 05-07 "E3.S 주(main)" ↔ Dell 05-27 "AIC vs E3.L/S 트레이드오프" ↔ **IBM 02-06 "2028 AIC only → 2029 AIC+E3.S 2T 분리 로드맵, HHHL 256GB 갭 → LPD5/FHHL cover"**. E1.S(liquid cooling, FMTA) / E3.S(air/serviceability, HPE 주, 단 02-12 slot/PCIe lane 제약 / IBM 2029 추가) / E3.L(고용량 512GB+, Dell) / AIC=CMM(표준FF 유연성 + E3.S 제약 우회, 단 Oracle엔 너무 큼 / IBM 2028 출발) / **1DPC 선호(AWS, 단일 구성)**. **Oracle = 폼팩터 제약 가장 강한** (AIC 큼+liquid 불가), **AWS = 구성 단순성 최우선** (1DPC), **IBM = 시계열 분리(2028 AIC→2029 AIC+E3.S 2T) + HHHL 고용량 갭 인지**. → [aws.md](by-customer/aws.md)·[hpe.md](by-customer/hpe.md)·[nvidia.md](by-customer/nvidia.md)·[oracle.md](by-customer/oracle.md)·[dell.md](by-customer/dell.md)·[ibm.md](by-customer/ibm.md)
- **TCO 검증 thread**: **AWS 02-10 "명확한 TCO 개선 필요(고객 체감)"** ↔ **Oracle 03-11 "TCO 최우선, DIMM 수준 Cost 요구"** ↔ MSFT 04-30 "Competitive TCO 상세 분석 필요" ↔ Dell 05-27 "AIC TCO 우세 / E3.S TCO 열세(용량 한계)" ↔ HPE 05-07 "AIC Acceptance → E3.S 주" ↔ IBM 02-06 "$/GB 절감 핵심 제안 + 속도 낮춰 TCO 개선 검토(2nd Tier 용량·비용 균형)" ↔ **Lenovo 01-15 "CMM 가격이 RDIMM보다 비싸 → sales 부진, 저등급(Graded memory) DRAM 저가 CMM 개발 필요(가장 이른 TCO/가격 언급 + 가장 직접적 cost 장벽)"**. TCO = **7개 고객 공통** 우려/검증 과제. **Oracle이 가장 엄격**(DIMM 수준 명시), **AWS는 "Killer Use case + 성능/비용/응용 동시 만족"** 전제, **IBM = $/GB 절감 그 자체가 제안 명목**(SAP HANA IMDB), **Lenovo = 가격 자체가 sales 장애(RDIMM 대비 프리미엄) → 저가 CMM(Graded memory) 요구(가장 이르고 가장 직접)**. → [aws.md](by-customer/aws.md)·[oracle.md](by-customer/oracle.md)·[msft.md](by-customer/msft.md)·[dell.md](by-customer/dell.md)·[hpe.md](by-customer/hpe.md)·[ibm.md](by-customer/ibm.md)·[lenovo.md](by-customer/lenovo.md)
- **★★ CXL switch 경쟁 구도 (2026-03-11 Oracle)**: Marvell(Broadcom 경쟁 위해 Xconn switch 인수) vs Broadcom("CXL switch 시장 없다" 주장) vs Xconn(인수 대상, Oracle pooling bottleneck). Oracle pooling 일정 = switch 공급망 좌우. Switch 기반(switch) vs Switchless(Montage MHD 2포트/자사 CMM 2포트) — Oracle이 최종 선택할 아키텍처 = 자사 CMM 경쟁력 직결. 6월 Oracle sync-up에서 확인. → [xconn.md](by-customer/xconn.md)·[broadcom.md](by-customer/broadcom.md)·[marvell.md](by-customer/marvell.md)·[montage.md](by-customer/montage.md)·[oracle.md](by-customer/oracle.md)
- **★ Local CXL 가치 훼손 thread (AMD + Oracle DB)**: Oracle 03-11 "DB 팀 tiered memory → TCO 무의미 + DIMM ch 확장이 나음 → 계획 중단" + "AMD 12→16ch → CXL 추가 가치 없어짐". CPU DIMM 채널 확장 트렌드 = Local CXL 사업성 악화. 단, Pooled(Oracle OCI VM, MSFT pathfinding, NVIDIA KV cache)는 별개 — Local 부정 ≠ Pooled 부정. → [amd.md](by-customer/amd.md)·[oracle.md](by-customer/oracle.md)
- **★ Oracle HA 요구 vs 아키텍처 선택 (2026-03-11)**: Oracle SPOF 감당 불가 → HA 필수. 단일 CXL switch = SPOF. 해결 경로: (a) Switchless + Montage MHD 2포트(2호스트, SPOF 제거) (b) 자사 2세대 CMM 2포트(동일 원리). Oracle "최소 4대 서버" 풀. 미해결: Montage MHD = 8CH or 2CH? "true solution" 의미? (Jay 모름 → Montage 직접 문의). → [oracle.md](by-customer/oracle.md)·[montage.md](by-customer/montage.md)
- **★ Oracle AIC 시계열 반전 (03-11 → 08-11)**: 03-11 "AIC 너무 큼" → 08-11 "Sang Park AWS→Oracle 이직 → AIC PNM 검토 재개". Jay(JEBA SUNDRARAJ) 양쪽 공통 참석. AIC 거부가 인재 이동으로 5개월 만에 반전 — 담당자 변경이 폼팩터 입장 좌우. → [oracle.md](by-customer/oracle.md)
- **★ HPE Venice 시계열 (02-12 → 05-07)**: 02-12 "EVB 8pcs(2025-12 제공) CXL 2.0 평가(문제 없음) → CXL 3.0 계획 + Gen13 Venice **Post-Launch**(샘플 RDIMM과 불일치 가능)" → 05-07 "Gen2 컨트롤러=Montage, 2027-06 Venice(SP7/SP8) Launch, 자사 2월 sample acceptable". 02-12 "CXL Post-Launch(지연)" ↔ 05-07 "2027-06 Launch" 교차. 자사 2월 sample = 02-12 미팅 직후 제공 추정. HPE CXL 접촉의 기원 = 02-12. → [hpe.md](by-customer/hpe.md)
- **★ IMDB / Memory sharing use case thread (02-12 HPE)**: HPE 02-12 "IMDB 응용 NVMe 대비 CXL 성능+용량 우수, AI 응용 NVMe→CXL 대체 가능, **Memory sharing = 특정 workload 강점**, IMDB 고객 Main:CXL=1:1". ↔ MSFT 04-30 "SW path-finding(메모리 쉐어링/동적·정적 할당)" ↔ Oracle 03-11 "OCI VM 온디맨드 메모리 할당" ↔ **IBM 02-06 "SAP HANA IMDB = 2nd tier memory, $/GB 절감(Memory sharing 명시 없으나 IMDB use case 가장 명시적)"**. IMDB/Memory use case = HPE(02-12)·MSFT(04-30)·Oracle(03-11)·**IBM(02-06, 가장 이른 IMDB 명시)** 4개 고객 공통. **IBM = SAP HANA IMDB로 가장 구체적 applied use case** (나머지는 generic/VM/pathfinding). → [hpe.md](by-customer/hpe.md)·[msft.md](by-customer/msft.md)·[oracle.md](by-customer/oracle.md)·[ibm.md](by-customer/ibm.md)
- **★★ AMD Venice 플랫폼 교차 (Google 02-05 DRAM ↔ HPE 02-12 CXL)**: **동일 AMD Venice 플랫폼**이 두 관점에서 교차 등장. **Google 02-05(DRAM, 비-CXL)**: Venice = High Performance, **MRDIMM 필수/POR**(BW/Core, RDIMM 전환 시 System balance 붕괴), EVT 빌드 진행 중, DVT CS샘플 PO 임박. **HPE 02-12(CXL)**: "Gen13 Venice" CXL = **Post-Launch**(샘플 RDIMM 불일치, 지연). → Venice의 DRAM(MRDIMM) 페이즈는 Google이 진행 중(EVT), CXL 페이즈는 HPE가 Post-Launch 대기. 두 CSP가 동일 플랫폼의 다른 메모리 페이즈를 각자 평가. ARM4(Value Prop, RDIMM 8800 백업)·Florence(Gen4, Gen3 대비 Q2~3 느림)는 Google 02-05에서만. → [google.md](by-customer/google.md)·[hpe.md](by-customer/hpe.md)·[amd.md](by-customer/amd.md)
- **★ MRDIMM thread (Google 02-05 비-CXL + HPE 02-12 CXL)**: **Google 02-05**: MRDIMM Gen2 라인업 자사 축소 중 → Google은 Venice서 MRD 여전히 POR(필수). **MRD Gen3 = Google Default 요구**(타 CSP Gen3 선택 시 경쟁력). **LP MRDIMM** = AMD 지원 여부 좌우(자사, Google에 AMD 설득 요청). 경쟁사 "Gen2 없이 Gen3/Gen4 고려 안 함". **HPE 02-12**: **MRDIMM+CXL 조합**(IMDB NVMe 대비 성능+용량, "두 마리 토끼" 제안). → MRDIMM이 DRAM 단독(Google) 관점과 CXL 결합(HPE) 관점 양쪽에서 등장. 자사 Gen2 축소 전략이 Google Venice POR과 긴장. → [google.md](by-customer/google.md)·[hpe.md](by-customer/hpe.md)
- **★ Intel DMR 플랫폼 교차 (Google 02-05 DRAM ↔ Intel 08-11 CXL)**: **Google 02-05(DRAM, 비-CXL)**: Intel DMR POR **48→64GB 변경 검토**(EVT 검증 후 최종), **(Confidential) GA @27년 1~2월**. 자사 1cnm 96GB 4개월 당겨 DMR NPI Intercept + ARM3 Sustain Qual 제안. EMR/Ghostfish 64GB 7200Mbps 샘플 필요(현재 5600Mbps 운용). **Intel 08-11(CXL)**: Intel DMR Sharing **Co-enabling/Validation** + Intel GPU Server–CXL Pooled KV Cache 협력 제안. → 동일 Intel DMR 플랫폼이 DRAM(Google, 27년 1~2월 GA) 관점과 CXL(Intel 직접, Co-enabling) 관점 양쪽 교차. 02-05 DRAM 선행 → 08-11 CXL 협력으로 확장. → [google.md](by-customer/google.md)·[intel.md](by-customer/intel.md)
- **★ 첫 비-CXL(DRAM) 미팅 — 분류 범위 확장 (Google 02-05)**: 본 미팅은 customer-meetings/ 2-tier 구조의 **첫 비-CXL 미팅**. README "고객·파트너 미팅 인텔리전스" 범위가 CXL뿐 아니라 DRAM DIMM 로드맵(RDIMM/MRDIMM/DDR5 PRAC/DDR6)까지 커버함 확인. DRAM 로드맵 미팅이 CXL 미팅과 동일 2-tier 구조(meetings/ + by-customer/)로 분류됨. CXL thread(7장/9장) 외 **DRAM thread(7장 Main Memory: DDR5/DDR6/MRDIMM Gen2/Gen3/Gen4/PRAC)**가 별도 추축. → [google.md](by-customer/google.md)
- **★ CMM 컨트롤러 납기 지연 thread (Lenovo 01-15, 가장 이른 샘플 일정 이슈)**: **Lenovo 01-15 "공유 컨트롤러(=CMM 컨트롤러) 납기 지연 → 2세대 제품 일정 영향 → ES 26-09말/CS 27-02말 delay"**. 컨트롤러 공급망이 CMM 2세대 일정 좌우. ↔ Marvell CMM AX(Marvell+Xcena 공동개발, Structure A, Eval Card 단계, 2026-05-27 Dell) ↔ Montage MXC(CXL 3.2 업계 최초 시료생산, 2026-08-11 Newsroom). Lenovo 01-15가 컨트롤러 일정 이슈의 **가장 이른 기록** — 컨트롤러 IP 타이밍(Montage MXC 시료 vs 자사 CMM AX Eval Card)이 고객 샘플 일정에 직접 영향. → [lenovo.md](by-customer/lenovo.md)·[marvell.md](by-customer/marvell.md)·[montage.md](by-customer/montage.md)·[xcena.md](by-customer/xcena.md)
- **★ 3rd Gen 폼팩터 전환기 thread (Lenovo 01-15 + Dell 05-27 + IBM 02-06)**: **Lenovo 01-15 "2nd Gen 512GB 계획 취소 여부 + 3rd Gen 기타 FF 고려 문의(SJ Park)"** — 2nd Gen 고용량 계획 불확실성 + 3rd Gen FF 전환 논의 최초 언급. ↔ Dell 05-27 "AIC vs E3.L/S 트레이드오프(3세대 CXL 둘 중 택일)" ↔ IBM 02-06 "2028 AIC only → 2029 AIC+E3.S 2T 분리 로드맵". 3rd Gen FF = 세 고객(Lenovo·Dell·IBM) 공통 전환기 논의. **Lenovo가 가장 이른 3rd Gen FF 언급(01-15) + 2nd Gen 512GB 취소 가능성**. → [lenovo.md](by-customer/lenovo.md)·[dell.md](by-customer/dell.md)·[ibm.md](by-customer/ibm.md)
