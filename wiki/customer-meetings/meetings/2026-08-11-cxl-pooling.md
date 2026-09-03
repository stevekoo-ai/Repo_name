---
title: "CXL 메모리 풀링 미팅 — 2026-08-11 (Customer Meeting Full Text)"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, partner, competitor, primary-source, full-text]
source: "sources/cxl-pooling-meeting-summary-2026-08-11.md"
author: "구병호"
date: "2026-08-11"
type: "meeting-full-text"
---

# CXL 메모리 풀링 미팅 — 2026-08-11 (Customer Meeting 전문)

> **Customer Meeting 전문 분류** — 구병호 작성 1차 현장 인텔리전스.
> 외부 웹 스위프(Daily Update/Newsroom)와 다른 **1차 관찰 자료** — 에이전시 보고서가 아닌 실제 미팅 발언·채널 센싱.
> 원문(raw): [sources/cxl-pooling-meeting-summary-2026-08-11.md](../../../sources/cxl-pooling-meeting-summary-2026-08-11.md)
> 분류 위치: `wiki/customer-meetings/meetings/` — log.md가 아닌 고객 미팅 전용 영역. by-customer/ 누적 페이지와 쌍.
> by-customer 교차: 이 미팅에 등장하는 상대방별 누적 이력은 `../by-customer/` 참조 (NVIDIA·Oracle·MSFT·Marvell·Liqid·Intel·AMD·Qualcomm·ScaleFlux·Micron·Samsung·Kioxia·Panmnesia).

---

## 핵심 정리 (빠른 탐색용)

**주요 정정 (2026-08-11)**: M사 = **Micron 확정** (추정 해소). FAMS → **famfs** 정정 (Micron famfs 파일시스템).

| 구분 | 항목 | 영향도 | DRAFT 반영 |
|---|---|---|---|
| Key 1 | NVIDIA KV cache off-loading CXL 관심 전환 + Dynamo tiering SW + Vera CXL IP 검증 샘플 | ★★★ | 6장/9장 |
| Key 2 | 주요 풀링 고객 = Neo-Cloud (CSP/OEM 아님), KV cache off-loading 최대 목적 | ★★ | 5장/11장 |
| Key 3 | Abaco 3.0 PNNL — Liqid+Primemas+Micron 3자, Micron 총괄 리드, famfs SW | ★★ | 4장/11장 |
| Key 4 | 삼성 in-house CXL3 controller PoC — Expansion+Processing Logic+SW Solution | ★ | 3장 |
| Key 5 | Marvell Photonics 기반 Pooled Controller 연말 ES, Pod-scale, RDMA 대비 저지연, Memory as a Service 필수, Penguin 협업 | ★★ | 2장/4장 |
| 파트너 | Marvell(3D stacked+TSMC, Density AI ASIC Partner)/Liqid(CXL3 내년Q3, Turn-key)/Intel(GPU Server KV Cache)/AMD(White Paper Supercomputing, Dynamo)/Qualcomm(Server SOC 정기콸)/ScaleFlux(①LPD 중단 ②POR Controller+Compression IP ③Pooled Switchless) | ★~★★ | 3·4·5·7·9장 |
| 경쟁사 | Micron Abaco 3.0 구성 확정 / Samsung CXL3 Processing / Kioxia CXL 2.0 CXL-SSD | ★ | 4장/11장 |

**교차검증 필요**: Dynamo = NVIDIA(tiering 운영 SW)·AMD(Inference SW Framework) 양쪽 언급 → 동일 SW인지 확인 (DRAFT 9장 후속).

---

## Key Takeaways

1) 첫번째로, Liqid와의 미팅에서 동사가 Nvidia와 KV cache Off-loading 목적으로 긴밀히 협력 중임을 언급하였는데 이는 자사가 그동안 CXL에 관심이 없다고 인지하고 있었던 것과는 상반된 내용이었습니다. 또한, NVidia가 KV cache off-loading을 목적으로 CXL 메모리 풀링에 관심을 가지고 있으며 이를 위해 Tiering 운영 SW인 Dynamo에 반영 중이라는 사실을 별도로 센싱 하였는데 이 또한 Liqid의 발언을 supporting 하는 내용이었습니다. 한편, 이번에 NV와 CXL 관련 F2F 미팅이 처음으로 셋업 되어 많은 기대를 했었는데 막상 미팅에는 Barry 포함 CXL consortium/spec 관련 등 디바이스 레벨의 인원들만 나와 미팅 자체는 큰 도움이 되지 못했습니다. 하지만 자사가 준비해 간 KV cache에서의 Pooling 가치 관련 시뮬레이션 한 자료를 NV 사내 관련 AI 전문가들에게 공유하여 피드백을 받아 주기로 하였습니다.

2) 두번째로, 자사 입장에서 메모리 Pooling의 주요 고객 상대는 CSP/OEM 업체 보다는 Neo-Cloud 고객이므로 이들 업체와의 협력이 필수적임을 Primemas 박일 대표 및 Pamnensia 정명수 대표와의 대화를 통해 인지하게 되었습니다. Liqid 또한 동일한 언급을 했었으며 이 업체들은 전통적인 IMDB 시장도 여전히 고려하고는 있으나 KV cache off-loading 목적이 가장 크다고 하였습니다. 자사는 지금까지 Pooling 관련하여 Neo-Cloud 와는 engage가 거의 없었는데 CXL 관련 잠재적인 고객이 될 수 있음으로 해당 업체들과의 논의를 시작하도록 하겠습니다.

3) 세번째로, 경쟁사 관련 "Liqid+Primemas+M사"가 3자로 미국 국립 연구소인 PNNL 프로젝트에 공동으로 engage 중이고 긴밀히 협력 중임은 기 인지하고 있었으나 M사가 이를 총체적으로 리드하고 있다는 점을 알게 되었습니다 (일명 Abaco3.0 프로젝트). 이는 M사가 DIMM 및 FAMS라는 SW를 제공하고 있고 M사가 PNNL과의 협력을 주도하고 있기 때문에 가능한 것으로 설명을 들었습니다. 자사 또한 현재 Step2를 통해 유사한 방향성을 목표로 하고 있는 만큼 빠른 시일 내에 catch-up할 수 있는 세부 계획들을 잘 수립 하도록 하겠습니다. 한편 삼성 경우 in-house controller 개발은 제품화를 떠나 PoC 수준에서 계속 진행 중인데 chip 내 단순 Expansion 기능뿐만 아니라 Processing 기능까지 보유하고 있으며 관련 SW Solution도 함께 개발 중인 것으로 파악하였습니다.

4) 마지막 네번째로, 메모리 Pooling과 연계하여 Optical I/F에 대한 관심 및 중요도가 커지고 있음을 실감할 수 있었습니다. 이를테면 Marvell사와의 별도 미팅을 통해 파악한 바에 따르면 동사가 Pod-scale 기반 Pooled Memory를 목적으로 Photonics 기반 Pooled Controller를 연말 ES로 출시할 예정임을 공유했습니다. 이는 장거리·고대역폭·저지연 구현 가능하다는 장점을 가지고 있고 실용화 단계에 근접해 있어 관련 기술 동향 센싱 및 협력을 추가적으로 더 강화하도록 하겠습니다.

---

## 고객

### 1) MSFT (Phyllis – Sr. Director, Roadmap & Strategy / Samir, Terry, Adam 등)

- Local CXL 디바이스는 TCO를 최우선으로 고려하며 MDS와 같은 저비용 미디어를 선호하지만, Pooled는 Local 디바이스와는 상황이 다르다는 의견을 확인했습니다.
- MSFT는 Pooled에 대해 현재 pathfinding 단계이며, AI 응용 관련 데이터가 아직 부족한 초기 단계이므로 자사와 협업을 이어가기로 했습니다. (Pooled Appliance 제공 시 자사와 협력 가능)
- Samir(System Architect)는 Rack 간 인터커넥트로서 Optic과 CXL SSD 활용의 중요성을 강조했습니다.

### 2) Oracle (Jay – Sr. HW PE)

- 기존에는 서버 형상 때문에 E3 폼팩터를 선호했으나, 메모리 평가를 총괄하던 Sang Park이 AWS에서 Oracle로 이직하면서 AIC 폼팩터도 검토 대상에 포함되었고, CXL 평가 프로젝트가 다시 시작되었습니다.
- 자사의 POC 제품인 AIC 기반 PNM이 Marvell 칩 및 폼팩터 크기 요건을 충족하여, 확보되는 대로 샘플을 전달하기로 했습니다. Oracle은 SW 업체이기도 하여 PNM의 Acceleration 기능을 잘 활용할 수 있을 것으로 자신하고 있으며, 이에 대한 후속 미팅을 차주에 이어가기로 했고 Marvell GM도 Top-down으로 지원하기로 했습니다.
- Pooled에도 여전히 관심이 있으나, NVIDIA/AMD GPU Rack과의 Reference Design 협업을 우선 진행하는 것이 핵심이라는 데 공감했습니다.

### 3) NVIDIA (Barry – Director, Derek – CXL Boards, Ameet – CXL Validation)

- AI Application을 CXL Pooled와 어떻게 연결할 지에 대해서는 많은 논의들이 제대로 이루어 지지 못했었는데 이는 이번 미팅에 참여한 인원들이 메모리 디바이스 담당자 중심이라 그랬었던 것으로 판단됨. AI 전문가들에게 자사 자료 공유하여 피드백 받아 주기로 협의함.
- 자사가 제공한 CXL 샘플은 Vera의 CXL IP를 검증하기 위한 것이었으며, 자사 GPU Rack과 CXL Pooled의 효과성에 대해서는 내부 논의 후 피드백을 주기로 했습니다.

---

## 파트너

### 1) Marvell CXL & 3D stacked (Will Chu – GM, Khurram – VP 등)

- FMS를 앞두고 자사와 공동 발간한 CXL-PNM 백서에 대해 서로 감사 인사를 나누었으며, Oracle이 PNM에 관심을 보임에 따라 이를 Top Level에서 적극 지원하기로 했습니다.
- 자사의 Pooled 계획을 공유하고, 이에 필요한 요소 기술(CXL Switch, Photonics 등)에 대한 협력을 이어가기로 했습니다.
- 특히 GPU Rack 공간 부족으로 Pooled 시스템을 별도 Rack으로 구성할 경우 Rack 간 인터커넥트가 Pain Point가 되는데, Marvell의 Photonics 기반 Pooled Silicon이 연내 이용 가능해짐에 따라 이에 대한 후속 미팅을 진행할 예정입니다.
- 3D Stack과 관련해서는 자사 전략을 소개했고 TSMC와의 협력 모델에 대해 긍정적인 피드백을 받았습니다. 현재 Density AI와 Marvell의 관계는 Marvell이 ASIC Partner임을 확인했으며, 자사 Spec에 대한 후속 미팅을 진행할 예정입니다.

### 2) Marvell Photonics 기반 Pooled (Ravi – PM, Steve – Sales)

- Pod-scale 기반 Pooled Memory를 가능하게 할 Photonics 기반 Pooled Controller를 연말 ES로 출시할 예정임을 공유했습니다. (RDMA 대비 저지연이며, PCIe 기반 Copper 케이블 대비 장거리·고대역폭·저지연 구현 가능)
- 이는 Memory as a Service(메모리 랙)를 가능하게 할 필수 요소 기술로 판단되어, 후속 미팅을 셋업하기로 했습니다.
- 현재 Appliance Maker로 펭귄(Penguin)과 협업 중임을 공유했습니다.

### 3) Liqid (CEO 및 CTO 등)

- 자사 외에도 Micron 및 미국 국책 연구소와 협력하여 Appliance 사업을 순조롭게 진행 중임을 공유했습니다. CXL3 기반 시스템은 내년 3분기에 이용 가능할 것으로 예상되며, Sharing 기능은 현재도 이용 가능하므로 CXL3까지 기다릴 필요가 없다는 점을 강조했습니다.
- 자사가 Turn-key로 Box 개발 및 사업을 제안할 경우 가능한지 문의한 데 대해, 가능하다는 피드백을 받았습니다.
- OCP에서도 자사와의 협력을 계속 이어가기로 했습니다. (자사는 OCP에도 Liqid에 시스템 대여를 요청한 상태)

### 4) Intel (Richelle – Sr. Director, Jenni – Manager / CXL Eco-system Enabling Team)

- 자사의 Pooled 메모리 시스템 전략 방향을 공유했으며, Intel은 자신 및 고객도 Pooled에 많은 관심을 보이고 있다면서 이를 어떻게 Validation할지 내부 논의가 필요하다는 입장을 밝혔습니다.
- 자사는 Intel DMR의 POC 기능인 Sharing에 대해 Co-enabling 및 Validation을, 그리고 Intel GPU Server–CXL Pooled 시스템 기반 KV Cache 협력 및 성능 향상 평가를 제안했으며, Intel은 내부 검토 후 피드백을 주기로 했습니다.
- US Testbed 협력에 대해서는 CXL Eco-system Enabling Team 내부적으로 아직 입장이 정리되지 않아, 확인 후 피드백을 주기로 했습니다.

### 5) AMD (Rita – CXL Arch, Fellow / Ketan – SK hynix Account Manager 등)

- 자사의 Pooled 메모리 시스템 전략 방향을 공유했으며, AMD와는 White Paper 작성이 발표보다 효과적이라는 데 공감하여, 공동 평가 결과를 Supercomputing 학회를 목표로 작성하기로 했습니다.
- Dynamo Inference SW Framework 외에도 AMD가 보유한 SW로 자사 SW를 마이그레이션하는 방안을 검토하기로 했습니다.

### 6) Qualcomm (Hui Lu, Benjamin Lee, IO Team)

- 주로 Qualcomm Server SOC를 위한 Validation 및 자사 제품 Spec에 대해 논의했으며, 정기 콜을 셋업하여 후속 진행하기로 했습니다.

### 7) ScaleFlux (Hao – CEO, Saeed – VP 등)

- 자사의 LPDDR 기반 CXL Controller 계획(분기 단위 모니터링, 현재는 Hold 상태)을 공유하고, 향후에는 System 기반으로 집중할 계획임을 밝혔습니다. 다만 Scaleflux는 LPD 콘셉트 자체는 여전히 Value가 있다는 피드백을 주었습니다.
- 자사가 System 기반에 집중하더라도 결국 Module이 필요하기 때문에 CXL Controller 협업은 계속 이어가기로 했으며, DRAM+NAND Hybrid를 지원하는 Controller에 대해서는 Scaleflux 내부적으로 개발이 Hold 상태이나 필요 시 재개 가능하다는 피드백을 받았습니다.
- 이는 기존에 MSR이 자사 관여 없이 프로그램을 진행하다가 연락이 끊기면서 Scaleflux 측에서 프로그램이 취소된 것으로 판단했기 때문이며, 앞으로는 SK hynix 상품기획 조직에서 이를 관리해 달라는 요청을 받았습니다.
- 협업 방향은 다음과 같이 정리했습니다: ① LPD 개발 중단 ② 현재 POR인 CXL Controller에 집중하고 Compression IP를 추가 반영 ③ Pooled(Switchless) 관련 협업 지속.

---

## 경쟁사

### 1) Micron

- Eco-partner들과 협업하여 Memory Rack Appliance 프로젝트 및 사업화(일명 Abaco 3.0)를 발표했습니다. Rack 단위 및 시스템 단위로 판매가 가능합니다.
- 시스템은 Liqid, AIC는 프라임마스(Primemas), 메모리(RDIMM)는 Micron, SW는 Micron의 famfs를 사용하며, 현재 미국 국립연구소(PNNL) 프로젝트에 도입되었음을 발표했습니다.

### 2) Samsung

- 내재화 CXL3 Controller는 개발이 진행 중이며, 단순 Expansion 기능뿐 아니라 Processing Logic까지 보유하고 있음을 확인했습니다. (관련 SW Solution도 개발 중)

### 3) Kioxia

- CXL 2.0 기반의 CXL-SSD를 부스에 전시하였으나 담당자가 자세한 사항은 알지 못하였습니다.
