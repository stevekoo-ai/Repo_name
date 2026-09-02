---
title: CXL 컨트롤러/커넥티비티 칩셋 벤더 동향
created: 2026-08-03
updated: 2026-08-03
tags: [cxl, vendors, controller, switch, retimer, memory-buffer, AI, LLM]
---

CXL(Compute Express Link) 커넥티비티 칩셋 벤더들의 제품 포지션,
해결하는 use case / pain point, 2024~2026 발표 제품과 파트너십을
정리한 벤더 풍경도. 상위 개념 페이지 [cxl-next-gen-memory](cxl-next-gen-memory.md)와
중복되는 부분은 이 페이지에서는 **칩셋/IP 벤더 관점**으로 한정.

> 작성일 2026-08-03 기준, 공식 사이트 및 업계 보도 웹 조사 결과
> (WebSearch 백엔드 장애로 인해 WebFetch 직접 호출 + DuckDuckGo HTML
> 검색 페이지 경유로 수집). URL은 각 섹션에 명시.

---

## 벤더 포지션 매트릭스 (요약)

| 벤더 | 칩셋 유형 | CXL 버전 | AI/LLM 강조 | 대표 제품 |
|---|---|---|---|---|
| Panmnesia | Switch / Retimer / Endpoint / IP | 3.2 (PCIe 6.4) | 매우 강함 | PanSwitch, PanRetimer |
| Marvell | Memory controller / Switch / Near-mem accel | 2.0~3.x | 강함 | Structera A/X/S 시리즈 |
| Astera Labs | Switch / Retimer / Memory controller | 2.0~3.x | 매우 강함 | Scorpio X-Series, Leo, Aries |
| Montage (澜起科技) | Memory eXpander Controller / DDR5 RCD/DB | 3.1 | 강함 | MXC M88MX6852, Jintide |
| Microchip | Memory controller / Retimer | 1.1~3.1 | 강함 | SMC 2000/2100, XpressConnect Retimer |
| ScaleFlux | Computational storage + Memory controller | 3.1~3.2 | 매우 강함 (KV cache) | MC500, MC600, FC6116 |
| Rambus | Controller IP / PHY IP / Retimer | 1.1~3.1 | 강함 | CXL Controller IP (64 GT/s) |
| Synopsys | Controller IP / Verification IP / PHY | 1.0~3.0 | 강함 | CXL Controller IP, VIP |
| Cadence | Controller IP / Verification IP | 1.1~4.0 | 강함 | CXL Controller IP, CXL VIP |
| XConn | Hybrid Switch | 3.1 | 강함 | Apollo 2 (XC60064) |
| Axiado | 보안 TCU (CXL 직접 제품 아님) | - | 약함 | AX3080 TCU |
| **Axaina / Axia** | (확인 불가 — 실제 CXL 벤더 아님) | - | - | - |

> **비고 (Axaina/Axia)**: 사용자가 "Axaina CXL 또는 Axia CXL controller"로
> 지목한 벤더를 웹 검색(DuckDuckGo)으로 확인한 결과, **Axaina/Axia라는
> 이름의 CXL 칩셋 벤더는 발견되지 않음**. 검색 결과는 소셜 미디어
> 프로필 또는 AXA XL(보험사)에 국한. 비슷한 이름의 실제 관련 벤더는
> **Axiado(보안 TCU, AX3080)** 정도이나 이는 CXL 칩셋이 아닌
> 하드웨어 루티드 보안 컨트롤러. **원래 지칭이 무엇이었는지 사용자
> 재확인 필요** — 후보로는 Axiado, XConn, Panmnesia, 또는 다른 이름의
> 오타 가능성.

---

## 1. Panmnesia (파네시아) — CXL 3.2 스위치/레티머 퓨전

한국 기반 CXL 전문 팹리스. **CXL 3.2 + Port-Based Routing(PBR)**를
선도하는 포지션.

### 제품군
- **PanSwitch** — PCIe 6.4-CXL 3.2 퓨전 스위치. **세계 최초 CXL 3.2
  PBR 완전 구현**을 표방. **sub-100ns** 레이턴시.
- **PanRetimer** — PCIe 6.4 / CXL 3.2 링크 리타이머. 자체
  Link Controller IP 기반, **two-digit nanosecond** 왕복 레이턴시.
- **PanEndpoint** — CXL 엔드포인트 장치.
- **Link Controller IP / LAU IP / Controller IP** — 실리콘 IP 라인업.
- **PanFabric** — PBR 기반 패브릭 아키텍처.

### Use case / Pain point 해결
- **메모리 디스어그리게이션**: PBR로 컴퓨즈블(composable) 아키텍처
  구현 — 자원을 동적으로 풀링해 AI 데이터센터 자원 낭비 축소
- **대역폭 병목 / 레이턴시**: "Higher Scalability, Same Latency
  Class" — 스케일을 키워도 레이턴시 클래스 유지
- **AI/HPC/클라우드**: 단일 패브릭로 컴퓨트-메모리 연결

### 2024~2026 발표/파트너십
- **2025-11**: PCIe 6.0/CXL 3.2 스위치 샘플 출하 발표
- **CES 2026**: PCIe 6.4-CXL 3.2 퓨전 스위치 전시, 2026년 내 양산
  목표
- **2026-03**: OpenChip과 전략 파트너십
- **ISCA 2026**: 차세대 CXL 컨트롤러 및 PBR 스위치 연구 발표
- **SKTelecom** — CXL 기반 AI 랙 검증 협력
- 멤버십: CXL Consortium, RISC-V International, PCI-SIG, OCP, **UALink**

출처: https://panmnesia.com/ 및 DuckDuckGo 검색 결과

---

## 2. Marvell — Structera 시리즈 (controller/switch/near-mem accel)

### 제품군 (Structera 패밀리)
- **Structera A 2504** (근메모리 가속기): Arm Neoverse V2 코어
  16개 @3.2GHz, CXL 2.0 + PCIe 5.0 x16, DDR5-6400 4채널 (DIMM
  채널당 최대 2개), 최대 200 GB/s 대역폭
- **Structera X 2504** (메모리 확장 컨트롤러): DDR5 6TB+ 용량,
  최대 200 GB/s, 1x16 또는 2x8 포트
- **Structera X 2404** (DDR4 마이그레이션용): DDR4 4TB+, 채널당
  3 DIMM
- **Structera S 20256** (CXL 스위치): 최대 2 TB/s 스위칭 용량,
  16x16 또는 32x8 구성 가능 포트 — 메모리 풀링

### 공통 기능
- 인라인 LZ4 압축 + XTS-AES 256비트 암호화 (전 제품)
- **"mission-critical applications like AI"** 강조

### Use case / Pain point
- **메모리 용량 한계 / TCO**: DDR5 6TB+ 확장, 압축으로 유효 용량
  확대
- **메모리 풀링**: Structera S로 disaggregated memory 자원
  할당 → AI 스케일러빌리티
- **Memory Wall** 돌파 — 메모리 풀링 스위치 출시로 AI 메모리 병목
  해소 명시

### 파트너십 / 상호운용성
- AMD EPYC CPU, 5th Gen Intel Xeon Scalable 상호운용성 검증 완료
- **NVIDIA NVLink Fusion** 생태계 참여

출처: https://www.marvell.com/products/cxl.html

---

## 3. Astera Labs — Scorpio / Leo / Aries (스위치+레티머+컨트롤러 풀스택)

### 제품군
- **Scorpio Smart Fabric Switches**
  - **X-Series**: 320 PCIe lane, "Largest open, memory-semantic
    fabric switch". 백엔드 GPU 클러스터링용 — all-gather /
    all-scatter / all-to-all / all-reduce / reduce-scatter 가속.
    최대 80개 가속기를 PCIe로 직접 라우팅, 멀티랙 수천 GPU 확장.
    **2024-05-05 실리콘 최초 공개**. Scorpio X-Series 320 Lane
    모델은 현재 하이퍼스케일러에 **출하 중**(2026-06).
  - **P-Series**: 32~320 lane 패밀리 — CXL 메모리 풀링/패브릭.
- **Leo CXL Smart Memory Controllers**
  - A1000-1254AB: CXL 1.1/2.0, 16x32G, DDR5-5600 RDIMM 4슬롯,
    2TB, 확장+풀링+공유
  - CM5082E: 8x32G, DDR5-5600 2채널, 2TB, 확장 전용
  - CM5162E: 16x32G, DDR5-5600 2채널, 2TB, 확장 전용
  - CM5162P: 16x32G, DDR5-5600 2채널, 2TB, 확장+풀링+공유
- **Aries PCIe/CXL Smart DSP Retimers** — 멀티랙 GPU 클러스터링용.
  PAM4 DSP 기반. PCIe 5.0/6.0 지원.
- **Aries PCIe/CXL Smart Cable Modules** — 케이블 연동 모듈

### Use case / Pain point
- **토큰 성능 극대화**: single-hop, line-rate peer-to-peer GPU
  연결로 GPU 유휴 시간 최소화
- **LLM 추론 가속**: "40% faster time to insights with LLM"
  (챗봇 서비스 배포 사례)
- 추천 엔진, 엔지니어링 시뮬레이션, DB 처리

### 파트너십 / 2024~2026
- **NVIDIA NVLink Fusion** 생태계 정렬
- **AMD, Intel, SMART Modular, NVIDIA** 협력 (Leo 컨트롤러)
- **Micron** — CXL 통합 솔루션 검증 (클라우드/하이퍼스케일러 가속)
- Computex 2026 (6/2-5) — PCIe 6.0 광학 컴포넌트 및 풀랙 데모
- 2026-06-03 대만 오퍼레이션 확장 발표

출처: https://www.asteralabs.com/products/, https://www.asteralabs.com/products/leo-cxl-smart-memory-controllers/

---

## 4. Montage Technology (澜起科技) — CXL MXC + DDR5 인터페이스 칩

중국 기반 메모리 인터페이스 칩 전문. **DDR5 RCD/DB + CXL MXC**를
결합한 포지션.

### 제품군
- **MXC (Memory eXpander Controller) M88MX6852**
  - CXL 3.1 Type 3 표준 (CXL 3.2 호환)
  - PCIe 6.2 PHY — 최대 64 GT/s, x8 링크 (x4 bifurcation 가능)
  - 통합 듀얼채널 DDR5 컨트롤러 — DDR5-8000 MT/s 지원
  - CXL.mem + CXL.io 처리
  - 데모 구성: 512GB native DDR5 + 512GB CXL (RDIMM 4개)
- **Jintide CXL Memory Expander** — MXC 기반 모듈
- **DDR5 RCD (Registering Clock Driver) / DB (Data Buffer)**
  - 2024-01-04 발표 — **DDR5 RCD04**, 최대 7200 MT/s
- **M88MX5891/5851** — 이전 세대 MXC 칩 (CXL 2.0)

### Use case / Pain point
- **AI 트레이닝 메모리 병목**: "overcome memory bottlenecks, scale
  AI training efficiently"
- **메모리 어그리게이션**: 데이터센터 대규모 메모리 집적
- HPC 워크로드

### 파트너십 / 2024~2026
- **SK hynix** — MXC를 SK하이닉스 최초 DDR5 DRAM 기반 CXL 메모리
  모듈에 채택
- **AMD, Intel** — 샘플 평가 진행 중
- CXL Integrators List 등재 (상호운용성 인증)
- **2025-08/09**: M88MX6852 전략 고객 샘플링 시작
- **DevCon 2025 / FMS 2025** 공개 검증/기술 쇼케이스 예정

출처: DuckDuckgo 검색 (Montage Technology M88MX6852, Jintide CXL
memory expander)

---

## 5. Microchip — SMC 컨트롤러 + XpressConnect 리타이머

### 제품군
- **SMC 2000 시리즈** (1세대 CXL 메모리 컨트롤러)
  - SMC 2000 16x32G, SMC 2000 8x32G — CXL 1.1/2.0, PCIe 5.0,
    DDR4/DDR5 지원
- **SMC 2100 시리즈** (2세대) — CXL Type 3, DDR5 + enhanced ECC
- **XpressConnect PCIe 6.0 / CXL 3.1 Retimers**
  - **64 GT/s**, pin-to-pin 레이턴시 **<12 ns**
  - PCIe Gen 3~6 하위 호환
  - **3-nm Switchtec PCIe Gen 6 스위치**와 사전 검증된
    상호운용 패브릭 구성
- **Switchtec PCIe 스위치** (PAX/PXH 계열) — CXL 패브릭에
  적용

### Use case / Pain point
- **메모리 확장 / 자원 디스어그리게이션** — 베이스보드/라이저/
  케이블 인터커넥트 전 영역
- **AI 인프라** — 대규모 AI 메모리 확장 시나리오
- "CXL Memory pool for AI workloads", "low-latency DRAM memory
  bandwidth per CPU/GPU core"

### 2024~2026
- 2025년 XpressConnect CXL 3.1 리타이머 출시
- Switchtec Gen 6 스위치와 사전 검증된 패브릭 강조

출처: https://www.microchip.com (일부 403), DuckDuckGo 검색

---

## 6. ScaleFlux — 컴퓨테이셔널 스토리지 + CXL 메모리 컨트롤러 (KV cache 강조)

### 제품군
- **MC500** — CXL 3.1 Type 3 메모리 컨트롤러. advanced ECC.
  2025년 양산 샘플링.
- **MC600** — PCIe Gen6, CXL 3.2 Type 3. 양산 준비 펌웨어 +
  표준화 레퍼런스 디자인
- **FC6116** — PCIe Gen6 NVMe SSD 컨트롤러 (컴퓨테이셔널 스토리지)
- **컨텍스트 텔레메트리 기반 데이터 플레이스먼트** — Flexible
  Data Placement (FDP) write stream 200+개 / 드라이브

### Use case / Pain point (AI/LLM 특화)
- **KV cache 고속 접근**: high-endurance SSD를 "shared,
  pod-level context tier for high-speed KV-cache access"로
  배치 — GPU 스톨 최소화, 추론 처리량 유지
- **롱컨텍스트 추론 / 에이전틱 AI** 워크로드 타겟
- **7~10+ DWPD 내구성** — 쓰기 집중적 KV cache 워크로드 대응
- **TCO**: 기존 시스템 개조 없이 AI 메모리 확장 — "without
  costly server overhauls"

### 파트너십 / 2024~2026
- **XConn** — CXL 3.1 상호운용성 테스트 (FMS 2025)
- **AMD** — 프로세서 상호운용
- **NVIDIA, AIC, FarmGPU, Lightbits Labs** — 생태계 협력
- NVIDIA GTC, FMS 2025 데모, FMS 2026 차세대 Gen6 포트폴리오
  데뷔

출처: DuckDuckGo 검색 (ScaleFlux MC500/MC600/FC6116, FMS 2025)

---

## 7. Rambus — CXL Controller IP / PHY IP / Retimer IP

### 제품군 (IP 중심)
- **CXL Controller IP**
  - CXL 3.1: **64 GT/s**, CXL 2.0/1.1: 32 GT/s
  - CXL.io / CXL.mem / CXL.cache 프로토콜
  - x1~x16 lane, PIPE 6.x/5.x
  - Host / Device / Switch Port / Dual-Mode-Shared 모드
  - SoC / ASIC / FPGA 최적화
- **CCIX Controller IP** (CCIX 1.1)
- **PCIe 7.0 Switch IP** + **HBM4/HBM4E Controller** — 2026
  카탈로그 확장
- **Memory Interface Chips** / **Retimer** — 포트폴리오 일부

### Use case / Pain point
- AI/ML, 데이터센터, 엣지 — 고대역폭 캐시 일관 인터커넥트
- IP 라이선스 모델 — 팹리스/시스템 업체가 자체 실리콘에 통합

### 파트너십 / 2024~2026
- **Samtec** (광 케이블), **Viavi** (익서사이저) 협력 데모
- **Tenstorrent** — 유연/전력효율 솔루션 공동 개발
- 2026 copyright 페이지 — CXL Memory Initiative 강조

출처: https://www.rambus.com/cxl/

---

## 8. Synopsys — CXL Controller IP / PHY / Verification IP

### 제품군
- **CXL Controller IP** — CXL 1.0, 1.1, 2.0, 3.0 지원 (**3.1은
  명시되지 않음**)
- **PHY IP**: PCIe 6.0/CXL 3.0, PCIe 5.0/CXL 2.0/1.0
- **IDE Security Modules** — CXL 2.0/3.0
- **CXL Verification IP** 서브시스템
- 데이터패스 폭: 1024/512/256/128비트 — x2~x16 링크

### Use case / Pain point
- "secure, low-latency and high-bandwidth interconnect for AI,
  ML, cloud computing"
- IP 통합 — 칩셋 업체가 검증된 컨트롤러를 빠르게 설계
- 2025-11 블로그: 차세대 대역폭 수요 전망

출처: https://www.synopsys.com/cxl

---

## 9. Cadence — CXL Controller IP + Verification IP (4.0 대응)

### 제품군
- **CXL Controller IP** — CXL 3.1 및 이전 리비전
- **CXL Verification IP** — CXL 1.1~3.1 커버, **향후 CXL 4.0
  검증 툴(128 GT/s)** 준비
- Type 1/2/3 장치 검증 지원
- 리타이머 컴플라이언스 — "truncated normal compliance
  pattern" 락 정확도

### Use case / Pain point
- HPC, ML, 클라우드 인프라 — 스마트 I/O, 메모리 익스팬더, GPU
  가속기
- 파트너 통합 데모: **SMART Modular Leo 컨트롤러** + 확장 카드
  → 처리량 향상, GPU 점유율 개선

### 2024~2026
- **FMS 2025 / CXL DevCon 25** 실리콘 쇼케이스
- **Astera Labs Aries** 스마트 DSP 리타이머와 연계 데모

출처: DuckDuckGo 검색 (Cadence CXL Controller IP, Verification IP)

---

## 10. XConn — Apollo 2 하이브리드 스위치 (CXL 3.1 + PCIe Gen6)

### 제품군
- **Apollo 2 (XC60064)** — 2세대 하이브리드 스위치
  - CXL 3.1 + PCIe Gen 6.2
  - 64 포트 / 64~260 lane 구성
  - **Synopsys 실리콘 검증 IP** 탑재

### Use case / Pain point
- AI/ML/HPC — **"GPU direct access to a CXL memory pool"**
- 메모리 풀링을 통한 AI 워크로드 가속

### 파트너십 / 2024~2026
- **2025-03-17**: Apollo 2 공개
- **ScaleFlux** — FMS 2025 상호운용성 데모 (MC500과 연동)
- **Synopsys** — IP 공급

출처: DuckDuckGo 검색 (XConn Apollo 2 CXL switch)

---

## 11. Axiado (보안 TCU) — Axaina/Axia 관련 후보

Axiado는 CXL 칩셋 벤더는 아니지만, 이름이 가장 비슷하여 기록.
- **AX3080 TCU (Trusted Control/Compute Unit)** — 하드웨어 루티드
  보안 + 내장 AI. 네트워크/물리 위협 인터셉트. CXL 패브릭 보안
  부문에 적용 가능성은 있으나 CXL 컨트롤러/스위치 제품은 아님.

---

## 공통적으로 해결되는 Pain Point 요약

| Pain Point | 주요 해결 벤더 / 제품 |
|---|---|
| **메모리 용량 한계** (Memory Wall) | Marvell Structera X (6TB+), Montage MXC, Microchip SMC, ScaleFlux MC500/600 |
| **대역폭 병목** | Panmnesia PanSwitch (sub-100ns, CXL 3.2), Astera Scorpio X (320 lane), Montage DDR5-8000 |
| **레이턴시** | Panmnesia PanRetimer (two-digit ns), Microchip XpressConnect (<12 ns) |
| **TCO / 자원 활용** | Marvell Structera S (풀링 2 TB/s), Astera Leo CM5162P (풀링+공유), Panmnesia PBR (컴포즈블) |
| **AI 추론 효율 / KV cache** | ScaleFlux (KV-cache pod tier), Penguin (KV-cache 서버, 별도), Astera (40% faster insights), Marvell (압축) |
| **GPU 클러스터링** | Astera Scorpio X (멀티랙 수천 GPU), Aries cable module |
| **상호운용성 / 검증** | Cadence/Synopsys VIP, Rambus IP, Montage CXL Integrators List |

---

## AI/LLM 워크로드 관련 핵심 인사이트

1. **KV-cache는 CXL의 첫 번째 실질적 AI 유스케이스** — ScaleFlux가
   pod-레벨 KV-cache 컨텍스트 티어를 명시적으로 제품화한 점이
   가장 구체적. 삼성 1TB CXL 메모리 풀(8-GPU 92% 추론 성능
   유지, [cxl-next-gen-memory](cxl-next-gen-memory.md) 참조)과
   방향 일치.
2. **하이퍼스케일러 출하 시작** — Astera Scorpio X-Series 320 Lane
   이미 하이퍼스케일러 출하 중 (2026-06). Microsoft Azure
   상용 CXL 메모리 배포는 Astera Labs Leo 기반 (상위 페이지
   ⓐ 항목 참조).
3. **CXL 3.2 + PBR이 차세대 분기점** — Panmnesia가 가장 공격적
   포지션. UALink 컨소시엄과의 연계도 주목 — NVIDIA 대항 카트라
   측면.
4. **3사(D램 벤더) 자체 컨트롤러 상용화 중단** (상위 페이지 ⓒ 참조)
   → Marvell / Montage / Microchip / ScaleFlux 같은 독립
   컨트롤러 벤더가 반사이익. 특히 **Montage는 SK하이닉스 CXL
   모듈에 MXC를 공급**하는 형태로 이미 수혜.
5. **IP 벤더(Rambus/Synopsys/Cadence)는 CXL 3.1~4.0 스펙을
   선제 지원** — 실리콘 제품보다 한 세대 앞서는 경향. Cadence는
   이미 128 GT/s CXL 4.0 검증 툴 준비 중.

---

## 한계 / 향후 체크 포인트

- **WebSearch 백엔드 장애**로 WebFetch 직접 호출 + DuckDuckGo
  HTML 검색만 사용 — 일부 벤더(Microchip 공식 사이트 403, Marvell
  세부 스펙 PDF 404)는 검색 결과에 의존. 공식 스펙시트 직접
  확인 필요시 재조사.
- **Axaina/Axia 벤더 정체 미확인** — 사용자 재확인 필요.
- 파트너십 날짜, 정확한 출시일, 가격 정보는 대부분의 경우
  명시되지 않아 누락 — 차차 보강 필요.
- 벤더별 매출/출하량/점유율 등 시장 지표는 이 조사 범위外.

---

## 고객 미팅 1차 자료 연결 (2026-08-11 추가)

> 작성일 2026-08-03 웹 조사에 2026-01-15~08-11 고객 미팅 1차 자료를
> 교차검증 보강. 미팅 전문은 [customer-meetings/meetings/](../customer-meetings/meetings/),
> 교차 thread는 [customer-meetings/index.md §3](../customer-meetings/index.md),
> 운영 패턴은 [customer-meetings-intelligence.md](customer-meetings-intelligence.md).

### Lenovo 01-15 — "공유 컨트롤러 납기 지연" (고객측 1차 증거)
- **가장 직접적 cost 장벽**: Lenovo가 CXL CMM 도입 시 공유 컨트롤러
  납기 지연을 비용·일정 장벽으로 명시. (TCO thread 7고객 중 가장 직접)
- **CMM 컨트롤러 크로스**: Marvell CMM AX(Structera A 계열) ↔ Montage MXC
  — 위 매트릭스의 Marvell·Montage 두 행이 실제 고객 RFP에서 경합 중임이
  1차 자료로 확인.
- **3rd Gen 폼팩터 전환 thread 기원**: Lenovo 01-15 + IBM 02-06 + Dell 05-27
  3개 미팅이 3rd Gen FF 전환을 언급 → 컨트롤러 벤더 입장에선
  E3.S 2T 대응 타이밍이 폼팩터 전환과 동기화됨.

### 교차검증 결과 (웹 조사 ↔ 미팅)
- **Marvell Structera**: 웹 조사 제품군(CMM 컨트롤러)이 Lenovo 미팅
  "공유 컨트롤러" 범주와 일치 — 미팅에선 벤더명 미기재, 웹 조사가 보강.
- **Montage MXC**: 웹 조사 "SK하이닉스 CXL 모듈에 MXC 공급"이
  미팅 언급과 정합 — 본 페이지 ⓒ 항목(자사 모듈에 타 컨트롤러) 지지.
- **미해결**: Lenovo 미팅에서 언급된 구체 컨트롤러 벤더명은 미확정.
  Marvell vs Montage 경합 가설은 추가 미팅/공식 발표로 확정 필요.

### 데이터 한계
- 미팅 발언은 단일 출처. 웹 조사와 충돌 시 명시적 표기.
- 컨트롤러 벤더 특정은 미팅에선 대부분 익명("공유 컨트롤러") —
  웹 조사 제품명 매핑은 (추정) 명시.

---

## Sources

- https://panmnesia.com/
- https://www.marvell.com/products/cxl.html
- https://www.asteralabs.com/products/
- https://www.asteralabs.com/products/leo-cxl-smart-memory-controllers/
- https://www.rambus.com/cxl/
- https://www.synopsys.com/cxl
- DuckDuckGo HTML 검색 결과: Montage Technology M88MX6852,
  Microchip Switchtec / XpressConnect, ScaleFlux MC500/MC600,
  Cadence CXL Controller IP, XConn Apollo 2, Axiado AX3080
- [cxl-next-gen-memory](cxl-next-gen-memory.md) (상위 개념 페이지)
- [customer-meetings-intelligence.md](customer-meetings-intelligence.md) (운영 패턴, 2026-08-11 추가)
