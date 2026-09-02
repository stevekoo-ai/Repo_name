---
title: CXL GPU Direct Memory — Dynamo · NIXL · CUDA Direct CXL 아키텍처
created: 2026-08-21
updated: 2026-08-21
tags: [cxl, gpu-direct, cuda-direct-cxl, dynamo, nixl, kv-cache, offload, directed-tlp]
---

GPU 가 CXL 메모리를 직접 접근하는 기술의 전체 스택.

**핵심 질문**: "Dynamo 의 offloading 으로 GPU ↔ CXL 메모리 direct 연결이 가능한가?"

---

## 요약 (TL;DR)

> **Dynamo 가 CXL 을 직접 타겟팅하는 것은 아님.** Dynamo 는 "CPU RAM + SSD"만 표기.
>
> 그러나 CXL 메모리가 OS 에 투명하게 DRAM 스페이스에 맵핑되면, 우연히 offload 대상에 포함될 수 있음. 이는 Dynamo 가 CXL 을 의도적으로 연결한 게 아니라 OS 투명성의 부수 효과.
>
> **물리적 direct 연결은 CUDA Direct CXL + CXL 3.0 Directed TLP + GPU 의 CXL 네이티브 지원이 모두 필요.** 현재 상용 GPU(NVIDIA) 는 CXL 프로토콜을 네이티브로 지원하지 않으므로, CPU DMA 경유가 불가피.
>
> **SW stack (CXL Shared Memory Library) 은 "물리적 직접 접근을 여러 GPU 가 안전하게 같이 쓸 수 있도록 관리"하는 역할.** Overhead 는 있지만 "VRAM 부족 → 실패" 보다는 낫음.

---

## 1. Dynamo — 오케스트레이터 (Two Brain)

### 1.1 정의

**NVIDIA Dynamo** — 데이터센터 규모의 분산 LLM 서빙 오케스트레이터.
vLLM, SGLang, TensorRT-LLM 위에 쌓여서 다수 GPU 클러스터를 하나의 엔진처럼 돌림.

### 1.2 세 가지 핵심 기능

#### Prefill / Decode 분리

```
GPU A (Prefill 전담): "대한민국 수도는?" 20자 읽고 컨텍스트 파악
         │ KV cache 생성
         ▼
GPU B (Decode 전담): "서울입니다." → "한국에서" → "가장 큰" → "도시는?"
```

서로 다른 GPU 가 역할 나누므로 각각 효율적. Prompt 처리가 GPU 부하가 높고,
Token generation 이 낮으니 분리하면 전체 처리량↑.

#### KV Cache Offloading (질문의 핵심)

```
GPU VRAM 이 꽉 차면?
  │
  ▼
Dynamo 가 자동으로 KV cache 를 CPU RAM 으로 밀어낸다
  │
  │ (NIXL — low-latency transfer library 로 전송)
  │
  ▼
GPU RAM 은 비어있으니까 다른 요청 받을 수 있음
```

- **L0 (GPU VRAM)** — Fast, 직접 접근
- **L1 (CPU RAM)** — Offload target, cudaMemcpy 경유
- **L2 (Local SSD)** — Colder cache

**핵심**: Dynamo 가 offload 할 때 CUDA Direct CXL 로 전송하려 해도,
현재 상용 GPU 의 경우 CPU DMA 경유가 불가피.

#### Dynamic Scheduling (SLO Planner)

실시간 workload 보고 GPU 리소스 동적 조절. 지체 시간 SLO 유지.

### 1.3 Dynamo 와 CXL 메모리의 관계

| 질문 | 답 |
|---|---|
| Dynamo 가 CXL 을 명시적으로 지원하나? | ❌ 아님. 문서상 "CPU RAM + SSD"만 표기 |
| CXL 메모리가 offload 에 우연히 포함될 수 있나? | ⚠️ 이론상 가능 (OS 투명성) — 하지만 보장 X, 최적화 X |
| GPU → CXL Direct 연결을 공식 지원하나? | ❌ 아님 |

> **Dynamo 는 "주소만 보냄"**: "CPU RAM 이라는 주소 공간에 KV cache 밀어넣어"
> OS 가 CXL 메모리를 DRAM 스페이스에 투명하게 합쳐뒀으면 CXL 에도 갈 수 있음.
> 하지만 Dynamo 가 CXL 을 의도적으로 타겟팅하는 건 아님.

---

## 2. NIXL — 데이터 전송 레이어 (Nerve)

### 2.1 정의

**NVIDIA Inference Xfer Library (NIXL)** — AI 추론 간 GPU ↔ 메모리 계층 간
초고속 비동기 전송 라이브러리.

### 2.2 왜 필요한가?

| | 일반 cudaMemcpy() | NIXL |
|---|---|---|
| 방법 | CPU 가 복사해줌 | DMA 직접 전송 |
| CPU 부하 | 높음 | 낮음 |
| 속도 | 느림 | 빠름 |
| 서버 간 전송 | ❌ | ⚠️ 지원 (RDMA) |

### 2.3 비유

> 일반 cudaMemcpy: A 가 책을 B 에게 주고 싶을 때 → A 가 책 들고 직접 걸어다님 (느림)
> NIXL: A 가 "이 책 B 로 보내" → 택배 시스템이 자동으로 운반 (빠름, 개입 안 함)

### 2.4 Dynamo 와 NIXL 의 관계

```
[Dynamo = 두뇌]          [NIXL = 신경]
     │                        │
     │ "이거 지금 밀어야겠다"  │
     ├──────────────────────► │
     │                        │ 데이터 NIXL 로 빠르고 직접 전송
     │                        │
     ▼                        ▼
GPU VRAM ←───────────── CPU RAM (확장 디스크 역할)
```

- **Dynamo**: "어디로 얼마나 밀어야 한다"고 판단하는 두뇌
- **NIXL**: 실제로 데이터를 빠르고 직접 전송하는 신경

---

## 3. CXL 토폴로지 — 물리적 연결 구조

### 3.1 표준 토폴로지 (CXL 1.x/2.0)

```
GPU ── PCIe ──► CPU (IOH) ── CXL Switch ──► CXL Memory Expander
                │
            CPU Memory Controller
                │
          Local DRAM
```

**CPU 가 매개체.** GPU 가 CXL 메모리에 직접 접근하려면 CPU 의 IOMMU 매핑
+ DMA 라우팅이 필수.

### 3.2 CXL 3.0 — Directed TLP

**Directed TLP** = CXL 3.0 에서 새로 추가된 기능.

**TLP (Transaction Layer Packet)** = PCIe/CXL 에서 데이터가 움직일 때 붙는
"주소 라벨".

| | CXL 2.0 | CXL 3.0 Directed TLP |
|---|---|---|
| 라우팅 | CPU 가 라우팅 | GPU 가 CXL 디바이스에 직접 라우팅 가능 |
| CPU 개입 | 필수 | 선택 |
| Direct 가능 | ❌ | ⚠️ GPU 가 CXL 네이티브여야 함 |

### 3.3 caveat — GPU 가 CXL 네이티브가 아님

```
GPU = PCIe End Point (CXL 프로토콜 미지원)
CXL Memory = CXL Memory Expander

→ GPU 가 Directed TLP 를 붙일 수 없음
→ 결국 GPU → CPU → CXL Switch → CXL Memory
```

**비유:**
> CXL 2.0 = "우편물 우체국 경유 필수"
> CXL 3.0 Directed TLP = "직송 우편 시스템"
>
> 근데 GPU 가 직송 우체국 가입 안 함 → 결국 우체국 경유

---

## 4. CUDA Direct CXL — 물리적 Direct 접근

### 4.1 정의

NVIDIA 의 **CUDA Direct CXL** — GPU 가 CXL 메모리를 직접 읽고 쓸 수 있게
하는 드라이버/OS 레벨 기능.

### 4.2 지원 조건

- CUDA Direct CXL 지원 드라이버 + CUDA toolkit 필요
- 특정 GPU 모델만 지원
- 특정 CXL 메모리 익스팬더만 호환
- Linux OS 필요

### 4.3 한계

```
CUDA Direct CXL 지원이라도:
GPU ── cudaMemcpy ──► CPU DMA ──► CXL 메모리

cudaMemcpy 은 여전히 CPU DMA 경유입니다.
```

**CUDA Direct CXL 은 "물리적 직접 접근"은 해줘도 "논리적 관리"는 안 함.**
Lock/Allocator/Directory 같은 건 SW stack 이 해야 함.

---

## 5. SW Stack — 소프트웨어 관리 레이어

### 5.1 전체 구조 (그림 기반)

```
Scheduler
  │ lookup
  ▼
KV Connector Interface
  │
  ├── GPU Worker (read/write KV → GPU Memory)
  │
  ├── KV Transfer Handler
  │     ├── publish ──► Prefix Cache Index
  │     ├── alloc/free ──► CXL Shared Memory Library
  │     └── submit ──► GPU-CXL copy workers
  │            └── cudaMemcpy ──► GPU Memory ↔ CXL Shared Memory
  │
  └── GPU Memory ↔ CXL Shared Memory
        │
        └── CXL Shared Memory Library
              ├── Inter-Node Lock
              ├── Memory Allocator
              └── Object Directory
```

### 5.2 각 레이어의 역할

| 레이어 | 역할 |
|---|---|
| **CUDA Direct CXL** (하드웨어/드라이버) | GPU ↔ CXL 물리적 direct 접근 가능하게 함 |
| **CXL Shared Memory Library** (SW stack) | CXL 메모리를 "공유 RAM 풀"로 추상화 |
| **Inter-Node Lock** | 여러 GPU 동시 접근 충돌 방지 |
| **Memory Allocator** | CXL 메모리 공간 할당/해제 |
| **Object Directory** | KV cache 위치 추적 |

### 5.3 SW Stack 이 하는 일

```
GPU: "CXL 메모리 0x8000 에 써"
  │
  ▼
CXL Shared Memory Library 가 "CXL 메모리를 공유 RAM 처럼 보이게 함"
  │
  ├── Inter-Node Lock — 다른 GPU 가 동시에 쓰지 못하게 잠금
  ├── Memory Allocator — 비어있는 주소 찾아서 할당
  ├── Object Directory — "이 KV cache 는 CXL 0x8000 에 있음"
  └── cudaMemcpy — 실제 데이터 전송 (GPU ↔ CXL)
```

---

## 6. Overhead 분석

### 6.1 Overhead 유형

| Overhead 유형 | 크기 | 설명 |
|---|---|---|
| **cudaMemcpy (CPU DMA 경유)** | ⚠️ 높음 | CPU 가 매개체, PCIe 대역폭 일부만 사용 |
| **Inter-Node Lock** | ⚠️ 높음 | 다른 GPU 대기 (컨테이션 시) |
| **Memory Allocator** | ⚠️ 중간 | 공간 할당 탐색 (O(N)) |
| **Object Directory** | ⚠️ 낮음 | 주소 찾기 (빠름) |
| **함수 호출 체인** | ⚠️ 낮음 | 5 층 중첩 (~5ms) |
| **CXL 메모리 물리적 latency** | ⚠️ 중간 | CPU 소켓 연결 (150~200ns) |

### 6.2 함수 호출 체인

```python
kv_connector.submit()                    # 1
  └─ kv_transfer_handler.alloc()         # 2
      └─ cxl_shared_mem.alloc()          # 3
          └─ inter_node_lock.lock()      # 4
              └─ cudaMemcpy()             # 5 (실제 전송)
```

### 6.3 Latency 비교

| 메모리 | Latency |
|---|---|
| GPU VRAM | ~100ns |
| CPU RAM | ~100ns |
| CXL 메모리 | ~150~200ns (CPU 경유) |

### 6.4 Trade-off

```
VRAM 가득 차서 swap 하면?
  └─ 추론 멈춤 = 실패

Offload 하면?
  ├─ Overhead 있음 (~50~100ns 추가)
  └─ 하지만 실행 가능 = 성공
```

> **Overhead 는 있지만, "VRAM 부족 → 실행 불가" 보다는 낫습니다.**

---

## 7. 최종 판단 Matrix

| 조건 | GPU ↔ CXL Direct 가능? |
|---|---|
| CXL 2.0 + CUDA Direct CXL 지원 | ⚠️ 가능 (드라이버/컨트롤러 호환 필수) |
| CXL 2.0 + CUDA Direct CXL 미지원 | ❌ CPU DMA 경유만 |
| CXL 3.0 + Directed TLP + CUDA Direct CXL | ✅ 가능 (가장 이상적) |
| CXL 3.0 만 지원 (CUDA Direct CXL 미지원) | ❌ GPU 가 CXL 네이티브 아님 |
| SW stack 만 있고 하드웨어/드라이버 없음 | ❌ SW stack 만으로는 부족 |

### 3 층 모두 필요

```
CXL 3.0 Directed TLP + CUDA Direct CXL + SW Stack
```

세 가지가 모두 충족되어야 GPU ↔ CXL direct 메모리 액세스 가능.
SW stack 만으로는 하드웨어/드라이버 한계를 넘을 수 없음.

---

## 8. 비유 정리

> **고급 GPS 네비게이션 (SW Stack) + 오프로드 가능 차량 (CUDA Direct CXL) + 직행 고속도로 (CXL 3.0 Directed TLP)**
>
> 네비게이션만 있다고 오프로드 갈 수 있는 건 아님.
> 차량과 도로가 모두 필요하죠.

---

## 9. 관련 페이지

- [CXL & 차세대 메모리 트랙](cxl-next-gen-memory.md) — CXL 기본 개념 + SK하이닉스 밸류에이션 관점
- [CXL 메모리 상품기획 DRAFT](cxl-memory-product-planning-draft.md) — 상품기획 종합 DRAFT
- [GPU Inference Economics — NVIDIA世代별 사양 검증](../reference/gpu-inference-economics.md) — H100/B200/B300 스펙 검증
- [웹 검색 우회 가이드](../tools/web-search-workaround.md) — 사내 vLLM web_search 오류 대응

---

**생성일**: 2026-08-21
**최종 검토**: 2026-08-21
**소스**: 논의 기록 — Dynamo/NIXL/CXL Direct Memory 아키텍처 종합
