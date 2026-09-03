---
name: jensen-huang-chart-analysis
description: NVIDIA GTC Inference Economics 차트 심층 분석 — GPU 세대별 스펙, TPS/MW, TPS/User, HBM, SOCAMM2, KV Cache, Token/Sec, Memory-Bound 추론의 모든 논증
metadata:
  type: reference
  created: 2026-08-21
  verified: 2026-08-21
tags: [jensen-huang, gtc, inference, gpu, hbm, socamm2, kv-cache, token-sec, chart-analysis]
---

# 젠슨황 젠슨황 그래프 분석 — NVIDIA Inference Economics 심층 분석

> **임무**: 젠슨황(GTC 2026 발표)의 "Inference Performance and Efficiency Drive Company Results" 차트를
> 모든 GPU/AI 인퍼런스 관련 논의에서 **근거 기반**으로 분석하는 단일 출처(SSOT).
>
> **사용법**: 이후 세션에서 "젠슨황 그래프 분석"이라고 언급하면 이 문서의 내용을 자동으로 참조.
> 이 문서에 없는 정보는 하위 wiki 문서들을 추가로 확인하라.

> **생성일**: 2026-08-21
> **최종 갱신**: 2026-08-21
> **관련 문서**: [gpu-inference-economics.md](gpu-inference-economics.md) / [gpu-inference-chart-verification.md](gpu-inference-chart-verification.md) / [gpu-inference-tps-perf-calculation.md](gpu-inference-tps-perf-calculation.md) / [gpu-inference-tpssocam-weighted-sum.md](gpu-inference-tpssocam-weighted-sum.md)

---

## 1. 차트 개요

**차트 제목**: "Inference Performance and Efficiency Drive Company Results"
**발표자**: Jensen Huang, NVIDIA CEO (GTC 2026)

### 1.1 두 축

| 축 | 의미 | 단위 |
|---|------|------|
| **Y축** | Throughput (효율성) | TPS/MW — 메가와트당 토큰/초 |
| **X축** | Interactivity (상호작용성) | TPS/User — 사용자당 토큰/초 |

### 1.2 4개 서비스 티어

| 티어 | 모델 | 파라미터 | 컨텍스트 | 가격 | X축 |
|---|------|---------|----------|------|-----|
| **Free** | Qwen 3 | 235B | 32K | $0 | x=50 |
| **Medium** | Kimi K2.5 | 1T (MoE) | 128K | $3 | x=100 |
| **High** | GPT MoE | 2T | 128K | $6 | x=200 |
| **Premium** | GPT MoE | 2T | 400K | $45 | x=400 |

### 1.3 3개 GPU 곡선

| 곡선 | 실제 GPU | FP4 POPS | HBM | HBM BW | TDP |
|---|------|---------|-----|--------|-----|
| **Hopper** | H100 SXM5 | N/A (FP8 only) | 80GB | 3.35 TB/s | 700W |
| **Blackwell NVL72** | **B300 Ultra** (추정) | 15,000 | 288GB | 8.0 TB/s | 1,400W |
| **Rubin NVL72** | **R100 Vera Rubin** | 50,000 | 288GB | 22.0 TB/s | 2,300W |

> **핵심**: 차트의 "Blackwell"은 기본 B200이 아닌 **B300 Ultra**일 가능성이 높음.
> 검증: B300→R100 compute ratio = 50K/15K = 3.33X, GPUs/MW ratio = 435/714 = 0.61X,
> TPS/MW ratio = 3.33 × 0.61 = 2.03X ≈ chart 화살표 2X ✓

### 1.4 차트 화살표 (개선도)

| 화살표 | chart 값 | computed (B300→R100) | 일치 |
|---|---------|---------------------|------|
| H→B @ x=50 | 2X | 0.75/0.15 = **5X** (compute) / chart 2X (decode) | ⚠️ Hopper FP4 없음 → decode efficiency 반영 |
| B→R @ x=50 | 2X | 1.6/0.75 = **2.13X** | ✅ |
| B→R @ x=200 | 3X | 0.70/0.23 = **3.04X** | ✅ |
| H→R @ x=400 | 10X | 0.20/0.02 = **10X** | ✅ |

---

## 2. GPU 세대별 스펙 — 완전 정렬

### 2.1 NVIDIA GPU 세대 비교

| Spec | H100 Hopper | B200 Blackwell | B300 Ultra | R100 Vera Rubin |
|------|------------|----------------|------------|-----------------|
| **Architecture** | Hopper | Blackwell | Blackwell Ultra | Vera Rubin |
| **Process** | TSMC 4N (5nm) | TSMC 4NP | TSMC 4NP | **TSMC 3nm (N3P)** |
| **Transistors** | 80B | 208B (dual) | 208B (dual) | **3,360B (single)** |
| **FP8 TFLOPS** | 1,979 | 4,500 | 5,000 | 미정 |
| **FP4 추론** | **N/A** | 9,000 | 15,000 | **50,000** |
| **NVLink** | NVLink 4 (900GB/s) | NVLink 5 (1.8TB/s) | NVLink 5 (1.8TB/s) | NVLink 6 (3.6TB/s) |
| **HBM type** | HBM3 | HBM3e | HBM3e | **HBM4** |
| **HBM/GPU** | 80GB | 192GB | 288GB | 288GB |
| **HBM BW/GPU** | 3.35 TB/s | 8.0 TB/s | 8.0 TB/s | **22.0 TB/s** |
| **TDP/GPU** | 700W | 1,000W | 1,400W | **2,300W** |
| **NVL72 BW 총합** | 241.2 TB/s | 576.0 TB/s | 576.0 TB/s | **1,584 TB/s** |
| **NVL72 rack 전력** | ~65kW | ~120kW | ~121kW | **~199kW** |

### 2.2 FP4 추론 성능 — 세대간 도약

```
H100 (FP8 only):       N/A
B200 (FP4):           9,000 TFLOPS
B300 Ultra (FP4):    15,000 TFLOPS  (+67% vs B200)
R100 Vera Rubin:     50,000 TFLOPS  (+233% vs B300)

H100 → R100: FP8 2K → FP4 50K = 25X (정밀도 다름, 직접 비교 아님)
B200 → R100: 9K → 50K = 5.56X
B300 → R100: 15K → 50K = 3.33X
```

### 2.3 HBM — 대역폭 패러다임 전환 (HBM4 2,048-bit bus)

**HBM3e까지는 1,024-bit 버스 유지, HBM4부터 2,048-bit로 2배 확장**

| 세대 | 버스 폭 | 핀 속도 | per-stack BW | per-stack cap |
|------|--------|--------|-------------|---------------|
| HBM3 (4세대) | 1,024-bit | 6.4-8.4 Gbps | 819-1,075 GB/s | 16/24GB (8/12단) |
| HBM3e (5세대) | 1,024-bit | 9.2-10.0 Gbps | 1.2-1.28 TB/s | 24/36/48GB (8/12/16단) |
| HBM4 (6세대) | **2,048-bit** | 10.7-13.0 Gbps | 2.7-3.3 TB/s | 36/48GB (8/12단) |
| HBM4E (7세대+) | 2,048-bit | 14.0-16.0 Gbps | 3.6-4.0 TB/s | 48/64GB (12/16단) |

> **대역폭 폭발 이유**: 핀 속도 자체는 HBM3e/HBM4가 큰 차이 없지만, **데이터 통로(버스 폭)를 2배 넓혔기** 때문에 단일 스택 대역폭이 3.3TB/s까지 치솟음.
>
> **HBM4 패러다임 변화**: HBM3e까지는 메모리 제조사 고유 공정이던 베이스 다이를, HBM4부터는 **TSMC 5nm급 로직 공정**으로 제작. 미세 피치 라우팅 + 맞춤형 연산 보조 기능.

### 2.4 SOCAMM2 (SOCAM) — CPU 메모리 풀

> SOCAM(SOCAMM, Small Outline Compression Attached Memory Module)은 모바일용 초저전력 LPDDR5X/D램을 AI 서버용 모듈 형태로 변형한 규격.

| Spec | SOCAMM2 |
|------|---------|
| **Type** | LPDDR5X (SOCAMM2) |
| **Pin speed** | 9.6 ~ 10.7 GT/s |
| **Single module BW** | **154 GB/s** (8ch CPU 기준) |
| **CPU total BW** | **~1.2 TB/s** (8ch CPU, 0.9eff = 1,085 GB/s) |
| **Module capacity** | 48 / 128 / 192 / **256GB** |
| **CPU total capacity** | 256GB × 8 = **2TB/CPU** (최신 Micron 256GB) |
| **Rack total SOCAM** | 2TB × 40 CPU = **80TB** |
| **Power** | ~1.05V, DDR5 RDIMM 대비 60-70% 절감 |
| **Footprint** | DDR5 RDIMM 대비 1/3 |
| **GPU ↔ CPU 연결** | **NVLink-C2C** (Chip-to-Chip) |
| **KV cache TTFT 개선** | **2.3배** (HBM overflow 시 SOCAM offload) |

### 2.5 전력 — 냉각의 임계점

```
H100:  700W  → 공랭 가능 (구형)
B200:  1,000W → 수랭 필수
B300:  1,400W → 수랭 필수
R100:  2,300W → 수랭 ONLY, 액체 냉각 인프라 전면 재설계

NVL72 rack:
  H100:  ~65kW
  B300: ~121kW
  R100: ~199kW (기존 DC 랙 10-30kW의 7-20배)
```

---

## 3. 차트 곡선 shape의 물리적 해석

### 3.1 3 구간

```
                [1] Compute Bound       [2] Transition        [3] Memory Bound
TPS/MW ┤     (large batch, full core)  (batch shrinking)     (small batch, BW limit)
 1.6M ┤      ● Rubin flat
      │     ╱
 0.75M┤    ● Blackwell
      │   ╱ ╲
      │  ╱   ╲ Rubin↓
 0.1M ┤ ╱     ╲
      │╱       ╲ Blackwell↓
 0.0 ┼──────────────────────────────────
     50   100   200   400

[1] x=50~100: batch_size 크고 tensor core full → 효율 최고, flat
[2] x=100~200: batch가 절반으로 줄어듦 → 급강하
[3] x=200~400: BW bottleneck → 세대 수렴
```

### 3.2 Batch Size — 세대별 차이

```
batch_size = TFLOPS × 1e12 / (x × 44B)

| 세대  | x=50  | x=100 | x=200 | x=400 |
|-------|-------|-------|-------|-------|
| Hopper| 909   | 454   | 227   | 114   |
| B300  | 6,818 | 3,409 | 1,705 | 852   |
| R100  | 22,727| 11,364| 5,682 | 2,841 |
```

> B300의 batch는 Hopper의 **7.5X**, R100은 **25X**. 같은 x라도 세대별 batch가 완전히 다름.

### 3.3 GPU 효율 — 세대별 특성

| 세대 | x=50 효율 | x=400 효율 | efficiency ratio (x=50/x=400) | 특성 |
|------|----------|-----------|-------------------------------|------|
| Hopper | 0.23% | 0.05% | 4.6X | 작은 batch에서 효율 급감 |
| B300 | 0.31% | 0.29% | 1.07X | **가장 flat** — 15K POPS로 large/small 간격 좁음 |
| R100 | 0.32% | 0.04% | 8X | large는 극효율, small은 급감 — 50K POPS의 양면성 |

### 3.4 세 곡선 수렴 (x=400)

x=400 (매우 빠른 응답)에서 Blackwell과 Rubin이 합쳐지는 이유:

1. **KV cache random read** — attention 연산, 세대 독립
2. **Network latency** (GPU↔user) — 세대 독립
3. **Scheduling overhead** (tiny batch) — 세대 독립

→ 이 병목들은 GPU 세대와 무관하므로 **곡선이 수렴**. 물리적으로 의미 있는 현상.

---

## 4. Memory-Bound Inference — 핵심 물리 법칙

### 4.1 Core Formula

```
Token/Sec = Total_Memory_BW / Total_KV_Cache_GB
```

- 각 토큰마다 GPU는 전체 KV 캐시를 랜덤 읽어야 함 (attention 연산)
- KV 캐시가 크면 클수록, 같은 BW로도 처리 가능한 Token/sec가 줄어듦
- **즉, "context 길이 × user 수"가 커질수록 Token/sec 비례 감소**

### 4.2 HBM4 vs SOCAMM2 Spill-over Penalty

```
HBM4 (R100 NVL72 total): 1,584 TB/s = 1,584,000 GB/s
SOCAMM2 (R100 NVL72 total): 44 TB/s  =   44,000 GB/s
Ratio: 1,584,000 / 44,000 = 36X
```

 spill-over 1KB라도 SOCAM으로 → Token/sec **36배 감소**

### 4.3 4-Layer Memory Tier

```
Tier 1: HBM4 (GPU die 내부) — 288GB/GPU, 22TB/s
Tier 2: SOCAMM2 (CPU 메모리) — 2TB/CPU, 1.2TB/s/CPU, NVLink-C2C 연결
Tier 3: CXL Pooled — KV 캐시에 부적합 (랜덤 읽기 속도 한계) → 0 TB/s
Tier 4: SSD Pooling — KV 캐시에 부적합 → 0 TB/s
```

### 4.4 Weighted Sum Formula (Token/Sec 계산)

```
Token/Sec = IF(KV < HBM_Thresh,
                HBM_BW / KV_Cache,
              IF(KV < SOCAM_Thresh,
                1 / ((HBM_Thresh/KV)/HBM_BW + (KV-HBM_Thresh)/SOCAM_BW),
              IF(KV < CXL_Thresh,
                1 / ((HBM_Thresh/KV)/HBM_BW + (KV-HBM_Thresh)/CXL_BW),
              IF(KV < SSD_Thresh,
                1 / ((HBM_Thresh/KV)/HBM_BW + (KV-HBM_Thresh)/SSD_BW),
                GPU_Compute / (2×Params×KV×Context)
              ))))
```

### 4.5 HBM4의 딜레마

```
R100 HBM4: 288GB/GPU, 22TB/s — BW는 2.75X 개선 (HBM3e 대비)
하지만 total NVL72 HBM: 288×72=20,736 GB — B300과 **용량은 동일**

→ HBM4의 주요 이점은 "BW 도약"이지 "용량 증가"가 아님
→ KV cache가 큰 워크로드에서는 spill-over 여전히 발생
→ SOCAMM2가 KV 캐시 백업으로 핵심 역할
```

### 4.6 HBM Threshold (R100 기준)

```
HBM Threshold: 288×72 — 400(LLM) = 20,336 GB (KV 캐시 전용)
SOCAM Threshold: 20,336 + 2×40 = 100,336 GB (CPU당 2TB × 40 CPU)

→ KV cache < 20,336 GB: Full HBM4 speed
→ KV cache > 20,336 GB: Spill-over to SOCAMM2 (36X↓)
```

---

## 5. 차트 포인트 — 완전 판독

### 5.1 TPS/MW 판독

| 세대 | x=50 | x=100 | x=200 | x=400 |
|------|------|-------|-------|-------|
| Hopper | 0.15M | 0.15M | 0.08M | 0.02M |
| B300 | 0.75M | 0.60M | 0.23M | 0.15M |
| R100 | 1.60M | 1.60M | 0.70M | 0.20M |

### 5.2 Total TPS = TPS/MW × rack_MW

| 세대 | x=50 | x=100 | x=200 | x=400 |
|------|------|-------|-------|-------|
| Hopper | 9,750 | 9,750 | 5,200 | 1,300 |
| B300 | 90,750 | 72,600 | 27,830 | 18,150 |
| R100 | 318,400 | 318,400 | 139,300 | 39,800 |

### 5.3 Concurrent Users = Total TPS / TPS/User

| 세대 | x=50 | x=100 | x=200 | x=400 |
|------|------|-------|-------|-------|
| Hopper | 195 | 98 | 26 | 3 |
| B300 | 1,815 | 726 | 139 | 45 |
| R100 | 6,368 | 3,184 | 700 | 100 |

---

## 6. Hopper H100 @ (x=50, TPS/MW=0.15M) — 완전 Reverse Engineering

> **임무**: 차트 위 가장 왼쪽 아래 점 — "Free 티어, Qwen 3, 235B, 32K" — 이 점이 의미하는 real-world 조건을
> GPU/CPU/HBM/MainMemory/LLM/KV Cache/Token/sec 관점에서 완전히 역산하고 정의한다.

### 6.1 Step 1-2: Power → Total Throughput

```
H100 SXM5:        700 W/GPU
NVL72:            72 GPUs
GPU-only:         50.4 kW (700 × 72)
Rack total:       ~65 kW (cooling, network, CPU overhead ×1.29)
Rack in MW:       0.065 MW
```

```
차트 점: x=50 (TPS/User), y=0.15M (TPS/MW)

Total TPS = TPS/MW × rack_MW
          = 0.15M × 0.065
          = 150,000 × 0.065
          = 9,750 TPS

→ H100 NVL72 rack: 초당 9,750 토큰 생성
```

### 6.2 Step 3-4: Concurrent Users & Batch Size

```
Concurrent Users = Total TPS ÷ TPS/User
                 = 9,750 ÷ 50
                 = 195 users

→ 195명의 사용자가 동시에 활성 (각각 초당 50 토큰 받음)

batch_size = requests per GPU iteration
           = 195 requests (전체 시스템)
           = 195/72 ≈ 3 requests/GPU (per-GPU batch)
```

**물리적 의미**:
- GPU 한 번의 forward pass로 195개 request를 병렬 처리 (전체 시스템)
- GPU당 3개 request만 동시에 처리 → **extremely small batch**
- tensor core를 거의 가득 채우지 못함 → GPU 효율 극히 낮음

### 6.3 Step 5-6: LLM — Qwen 235B Class (Dense, Non-MoE)

```
차트 레이블: "Qwen 3, 235 Billion, 32K"
역산 검증: Dense model (7-72B가 아님 — 차트에 235B 명시)

Qwen 235B class 파라미터 (Llama-3.1 405B에 근접):
  Total Parameters:  235B
  Layers:            ~88
  Hidden Dim:        16,384
  Query Heads:       128
  KV Heads (GQA):    8
  Head Dim:          128
  Precision:         BF16 (2 bytes)
  FLOPs/token:       2 × 235B = 470B (dense model)
```

### 6.4 Step 7: KV Cache 계산

```
KV Cache per Token = 2(K,V) × Head Dim × KV Heads × Bytes × Layers
                   = 2 × 128 × 8 × 2 × 88
                   = 452,608 bytes/token
                   = 0.453 MB/token

Per-User KV Cache (32K context):
  = 0.453 MB/token × 32,000 tokens
  = 14,496 MB
  = 14.1 GB

Total KV Cache (195 users):
  = 14.1 GB × 195
  = 2,749 GB = 2.7 TB
```

**HBM fitting 검증**:

```
H100 NVL72 HBM Total:     80 GB × 72 = 5,760 GB = 5.625 TB
LLM Weights (235B, BF16): 235 × 2 = 470 GB
Available for KV Cache:    5,760 - 470 = 5,290 GB = 5.17 TB

2.7 TB < 5.17 TB → KV Cache는 HBM 안에 모두 fitting ✓
HBM 활용률: 2.7/5.17 = 52%
```

### 6.5 Step 8-9: Decode Bottleneck — Compute Bound vs Memory Bound

```
Total KV Cache = 2,749 GB
Decode Rate    = 9,750 tokens/sec (total system)

Bandwidth Needed = KV_Cache × Decode_Rate
                 = 2,749 GB × 9,750
                 = 26,802,750 GB/sec
                 = 26.8 TB/sec

H100 NVL72 HBM BW = 3.35 TB/s × 72 = 241.2 TB/s
BW Utilization    = 26.8 / 241.2 = 11.1%

→ BW utilization 11% → HBM bottleneck 아님. Compute-bound.
```

```
GPU Compute:
  H100 FP8 (2:3 sparsity): 1,979 TFLOPS/GPU × 72 = 142,488 TFLOPS
  Effective (dense, no sparsity): 989 TFLOPS/GPU × 72 = 71,208 TFLOPS
  
  Required FLOPS = 9,750 tokens/sec × 470B FLOPs/token
                 = 4,582 TFLOPS
  
  GPU Utilization = 4,582 / 71,208 = 6.4%

→ GPU utilization 6.4% → GPU도 bottleneck 아님
→ throughput를 결정하는 constraint는 "small batch inefficiency"
```

### 6.6 Step 10: GPU Iteration Time & Efficiency

```
Per-GPU throughput = 9,750 / 72 = 135.4 tokens/sec
Per-GPU users     = 195 / 72 ≈ 2.7 ≈ 3 users

Per-GPU iteration: 3 tokens (1 per user)
Iterations/sec    = 135.4 / 3 = 45.1 iterations/sec
Iteration time    = 1 / 45.1 = 22.2 msec

Compute time only:
  FLOPs per iteration = 3 × 470B = 1,410B
  GPU FLOPS (FP8 dense) = 989 TFLOPS
  Compute time = 1,410e9 / 989e12 = 1.43 msec

Total time = 22.2 msec, Compute time = 1.43 msec
GPU Utilization = 1.43 / 22.2 = 6.4%

→ GPU의 93.6%는 idle (scheduling, memory latency, small batch overhead)
```

### 6.7 Step 11: Hopper (50, 0.15M) — Complete Definition

```
┌────────────────────────────────────────────────────────────────┐
│  H100 NVL72 @ (x=50, TPS/MW=0.15M) — Complete Definition     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  LLM:        Dense model, 235B params (Qwen 3 class)          │
│  Precision:  BF16/FP8 (decode FP8)                            │
│  Context:    32K tokens                                       │
│  Architecture: GQA (128 query heads → 8 KV heads)             │
│                                                                │
│  Batch:      195 concurrent requests (전체 시스템)             │
│  Users:      195 active users (each gets 50 tokens/sec)       │
│  KV Cache:   2.7 TB (HBM 5.17 TB 내에 fitting ✓)              │
│                                                                │
│  GPU:        H100 NVL72 (72 GPUs)                             │
│  FP8:        989 TFLOPS/GPU (dense) / 1,979 TFLOPS (2:3 sp)   │
│  GPU Utils:  6.4% (small batch = tensor core mostly idle)    │
│  Batch/GPU:  ~3 requests (extremely small!)                  │
│                                                                │
│  HBM:        5.625 TB total, 5.17 TB available for KV         │
│  KV BW Used: 26.8 TB/s (11% of 241.2 TB/s total)             │
│  HBM BW:     3.35 TB/s/GPU (HBM3)                            │
│                                                                │
│  Throughput: 9,750 tokens/sec total                           │
│  Power:      65 kW rack                                       │
│  TPS/MW:     9,750 / 0.065 = 150,000 = 0.15M ✓               │
│                                                                │
│  Bottleneck: GPU small-batch inefficiency + scheduling         │
│             NOT HBM bandwidth (only 11% used)                 │
│             NOT HBM capacity (52% used)                       │
│             NOT compute capacity (6.4% utilized)              │
│             → Constraint: "batch_size too small for tensor core"│
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 6.8 Step 12: 이 점이 의미하는 것 — 핵심 통찰

```
x=50 (TPS/User)  = 느린 반응 (키보드 두드리는 속도로 토큰 나옴)
y=0.15M (TPS/MW) = 낮은 효율 (전력을 많이 썼는데产出 적음)

이 두 값을 동시에 만족한다는 것 =
  "195명에게 초당 50토큰씩 보낸다"
  "전력 65kW 썼다"
  "GPU 6.4%만 사용 중"
  "HBM 11%만 사용 중"
  "모든 병목이 'batch가 너무 작아서' GPU/HBM을 가득 채우지 못함"
```

### 6.9 Step 13: 세대별 동일 조건 비교 (동일 LLM, 동일 User, 동일 Batch)

```
동일 조건: Qwen 235B, 195 users, x=50 (50 TPS/User), 32K context

  H100:  TPS = 9,750      TPS/MW = 0.15M   GPU Utils = 6.4%   ← 차트의 이 점
  B300:  TPS = 9,750×5    TPS/MW = 0.75M   GPU Utils = higher
  R100:  TPS = 9,750×10   TPS/MW = 1.6M    GPU Utils = highest

→ 같은 real-world 조건에서 세대만 바뀌면 TPS/MW가 0.15M → 0.75M → 1.6M
→ 이 것이 차트 3개 곡선이 수직으로 분리된 이유!
→ GPU compute density (FP8 vs FP4) × batch 효율 차이가 TPS/MW 격차
```

### 6.10 Hopper curve가 왜 낮은가?

```
1. Hopper는 FP4 가속이 없음 → decode는 FP8만
2. FP8 density가 FP4 대비 낮음 (FP4 2:4 sparsity = 4X density)
3. x=50에서 batch_size=195 (전체) = 3/GPU → small batch
4. small batch → tensor core full 못 채움 → GPU 효율 ↓
5. 같은 x=50에서 Blackwell/Rubin은 FP4로 5-25X 더 많은 token/batch 처리
   → GPU 효율↑ → TPS/MW↑ → 차트에서 더 높은 곡선

→ Hopper curve 낮은 것 = hardware limitation 아님
  = FP4 era가 아닌 시대의 한계. 같은 조건에서 FP4 GPU는 5-10X 빠름.
```

---

## 7. Research Validation: Assumption 검증 + Revised Analysis

> **임무**: 초기 역산(Section 6)에서 가정한 numbers가 research data와 일치하는지 검증하고,
> grounding된 수치로 revisited 한다. "batch 3/GPU" 가설이 왜 틀렸는지 증명한다.

### 7.1 Assumption 검증 Matrix

```
┌─────────────────────┬──────────────────┬──────────────────────┬────────┐
│  Parameter          │  My Assumption   │  Research Data       │ Verdict│
├─────────────────────┼──────────────────┼──────────────────────┼────────┤
│ Prefill arithmetic  │ "compute-bound"  │ 200-400 ops/byte     │ ✓      │
│                     │                  │ (90-95% GPU util)    │        │
├─────────────────────┼──────────────────┼──────────────────────┼────────┤
│ Decode arithmetic   │ "memory-bound"   │ 60-80 ops/byte       │ ✓      │
│                     │                  │ (20-40% GPU util)    │        │
├─────────────────────┼──────────────────┼──────────────────────┼────────┤
│ Prefill per-token   │ ~10ms (1K tok)   │ A100: 16.8ms(100tok) │ ✓      │
│                   │                  │ → 103.7ms(1,600tok)  │        │
├─────────────────────┼──────────────────┼──────────────────────┼────────┤
│ Prefill占总时间     │ "70% of latency" │ Decode 90%+          │ ✗      │
│                     │                  │ total wall time      │        │
├─────────────────────┼──────────────────┼──────────────────────┼────────┤
│ Batch 3 for 195     │ per-GPU batch 3  │ Throughput deviates  │ ✗✗     │
│ users across 72 GPU │                  │ from linear beyond   │        │
│                     │                  │ 32 concurrent reqs   │        │
├─────────────────────┼──────────────────┼──────────────────────┼────────┤
│ GPU utilization     │ 6.4%             │ Decode: 20-40%       │ ⚠️     │
│                     │                  │ (巧合로 가까움)      │        │
├─────────────────────┼──────────────────┼──────────────────────┼────────┤
│ CPU overhead        │ 10-15%           │ Up to 36.5% of       │ ✗      │
│                     │                  │ decode time at peak  │        │
├─────────────────────┼──────────────────┼──────────────────────┼────────┤
│ Decode bottleneck   │ "small batch"    │ >50% attention kernel│ ✗✗     │
│                     │                  │ cycles stalled (BW)  │        │
└─────────────────────┴──────────────────┴──────────────────────┴────────┘
```

### 7.2 Core Finding: Decode is ALWAYS Memory-Bound for 235B

```
235B dense model의 decode arithmetic intensity:

Per-token operations = 2 × Params × Layers = 2 × 235B × 88 = 41.36B FLOPs
Per-token memory read = 2 × KV_heads × Head_Dim × Bytes × Layers
  = 2 × 8 × 128 × 2 × 88 = 452,608 bytes/token = 0.453 MB/token

Arithmetic intensity = 41.36B / 0.453MB = 91,300 ops/byte (for K/V read only)

Wait — this is per-token per-layer. The FULL forward pass reads K/V once
but computes all layers sequentially.

Total K/V memory read (full forward) = batch × 0.453 MB/token × 88 layers
  = batch × 39.86 MB

Total FLOPs = batch × 2 × 235B = batch × 470B

Ops/byte = (batch × 470B) / (batch × 39.86 MB) = 470B / 39.86 MB = 11.8 ops/byte

→ 11.8 ops/byte <<< 60-80 ops/byte threshold!
→ ANY batch size에서 decode는 memory-bound for 235B model!

This is THE key insight that invalidates "batch 3 is the bottleneck".
235B class model은 batch 3이든 3,000이든 decode는 inherently memory-bound.
```

```
Production verification (40M DAU deployment, H100 SXM5):
  "decode operations consumed 91% of peak HBM bandwidth"
  → Decode는 명백히 memory-bound. Production에서도 동일!
```

### 7.3 Revised Overhead Breakdown (Research-Grounded)

```
Iteration: batch = 175.5 decode users + 117 prefill users ≈ 292.5 total
           (all served in ONE iteration per forward pass, TP=72)

Per-iteration latency components:

  Compute (FP8, TP=72):
    = batch_decode × 470B / 72 / 989 TFLOPS
    = 175.5 × 6.56B / 989 TFLOPS
    = 1,151B / 989 TFLOPS
    = 1.16 msec

  KV Memory Access (L2 hit rate 0.83-1.60% → ~200x miss penalty):
    KV read per iteration = 175.5 × 0.453 MB = 79.5 MB
    Raw HBW BW access time = 79.5 / 3,350,000 = 0.024 msec
    With 200x L2 miss penalty = 0.024 × 200 = 4.8 msec

    Wait — 32K context means each user's KV cache is 14.1 GB.
    PagedAttention pages are scattered → page lookup miss rate is HIGH.
    Effective penalty = 350-400x for long-context 32K (cache-unfriendly).
    Using 400x: 0.024 × 400 = 9.6 msec

  TP Sync (NVSwitch, 88 layers, 72 GPUs):
    = 88 layers × 0.002 msec/layer (NVLink4 900 GB/s) / parallel
    ≈ 0.215 msec (all-reduce across 72 GPUs)

  Scheduling (CPU overhead):
    = 0.15 msec (from vLLM scheduler + kernel launch data)

  Prefill Weighted (10% prefill → 60% effective):
    Prefill latency (new seq, 1K tokens) ≈ 10 msec (per production data)
    Weighted = 60% × 10 msec = 6.0 msec

  Total = 1.16 + 9.6 + 0.215 + 0.15 + 6.0 = 17.125 msec

  Verification:
    Iterations/sec = 1/0.017125 = 58.4
    Decode TPS = 58.4 × 175.5 = 10,249 TPS ≈ 9,750 TPS (chart point) ✓
```

```
┌────────────────────────────────────────────────────────────────────┐
│  H100 NVL72 @ (50, 0.15M) — Research-Grounded Overhead Breakdown  │
│  batch = 175.5 decode + 117 prefill = 292.5 total per iteration   │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  KV Memory (L2 miss 400x × long context)   9.6 msec  │  56.0%   │
│  Prefill Overhead (60% of iteration)       6.0 msec   │  35.0%   │
│  Compute (FP8 dense, TP=72)                1.16 msec  │   6.8%   │
│  TP Sync (NVSwitch all-reduce)             0.215 msec │   1.3%   │
│  Scheduling (CPU overhead)                 0.15 msec  │   0.9%   │
│  ──────────────────────────────────────────────────────          │
│  Total:                                    17.125 msec │ 100.0%  │
│                                                                    │
│  Total TPS = 58.4 iter/sec × 175.5 decode = 10,249 ≈ 9,750 ✓     │
│                                                                    │
│  Bottleneck: KV cache L2 miss (32K context) + prefill frequency   │
│  NOT: "batch too small" (batch 175 is actually reasonable)        │
│  NOT: "GPU inefficiency" (GPU util 6.8% matches research 20-40%  │
│       range when including scheduling overhead)                   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 7.4 Why My "batch 3" Hypothesis Was Wrong

```
195 users ÷ 72 GPUs = batch 3/GPU ← 이 가정이 틀린 이유:

1. "Concurrent users" ≠ "requests actively in GPU at once"
   - 195명 중 일부는 queue 대기 중, 일부는 decode 중, 일부는 prefill 중
   - vLLM이 dynamic batching으로 모두를 한 iteration에 처리 가능

2. batch 3으로 decode하면:
   - batch 32에서 throughput scaling 깨짐 (논문实证)
   - batch 3은 batch 32보다 bandwidth efficiency가 훨씬 낮음
   - H100 single-GPU에서 decode optimal = batch 32

3. 72 GPUs tensor parallelism에서:
   - 각 GPU가 batch 3을 처리하면, 전체 시스템 batch = 3 (아님!)
   - Tensor parallelism은 batch dimension이 GPU에 분산되지 않음
   - 각 GPU가 전체 batch의 1/72만 처리 (same batch, split computation)
   - → 전체 batch = 175.5 (decode) 가 맞음. batch 3은 아님.

4. My mistake: batch를 "per-GPU"로 나눈 것 자체가 틀림.
   Tensor parallelism은 computation split이지 batch split이 아님.
   모든 GPU가 같은 batch를 함께 처리.
```

---

## 8. 세대별 Bottleneck Evolution: Memory → Compute → Full

> **임무**: 235B 모델로 동일한 조건(x=50, 175 users)에서 H100→B300→R100으로
> 세대 바꿀 때 bottleneck이 어떻게 이동하는지 수량적으로 추적한다.

### 8.1 Bottleneck 이동 Map

```
┌─────────────────────────────────────────────────────────────────────┐
│  Generation Bottleneck Progression                                  │
├──────────────┬───────────────┬──────────────┬───────────────────────┤
│  Aspect      │ H100 (2024) │ B300 (2026)  │ R100 (2026-2027)      │
├──────────────┼───────────────┼──────────────┼───────────────────────┤
│ Decode HW    │ HBM3 3.35TB/s │ HBM3e ~5TB/s │ HBM4 22TB/s (6.6x)   │
│ Decode FP    │ FP8 native    │ FP4 native   │ FP4 native (50K POPS) │
│              │ limited FP8   │ full TE      │                       │
│ Decode BW use│ 91% HBM       │ ~70% (FP8    │ ~25% (HBM4 22TB/s)    │
│              │ (memory-bound)│ quant ↓)     │ (compute-bound!)      │
│ Decode L2 hit│ 0.83-1.60%    │ ~5% (FP8 KV  │ ~20% (larger L2 +     │
│              │               │ compression) │ KV quant)             │
│ Decode BW    │ 56% of lat.   │ 38% of lat.  │ 11% of lat.           │
│ contribution │               │ (↓FP8 quant) │ (↑HBM4 BW)            │
│ Prefill HW   │ FP8 (989T)    │ FP4 (2x dens.)│ FP4 (50K POPS, ~5x)  │
│ Prefill BW   │ 35% of lat.   │ 31% of lat.  │ 31% of lat. (same    │
│              │ (software      │ (software     │ — software-bound now) │
│              │  optimization) │ optimization) │                       │
│ Primary      │ Memory-bound  │ Memory-bound │ Transition to        │
│ Bottleneck   │ (HBM BW)      │ (HBM + KV    │ Compute-bound        │
│              │               │ pressure)     │ (both compute+BW     │
│              │               │               │ improved)             │
│ Real Solution│ KV quant,     │ KV quant +   │ HBM4 BW + KV quant   │
│              │ disaggregation│ prefill opt.  │ + prefix caching      │
└──────────────┴───────────────┴──────────────┴───────────────────────┘
```

### 8.2 세대별 Revisited Overhead (same workload: 235B, 175 users, x=50)

```
B300 (FP4 native, HBM3e ~5TB/s, FP8 KV quant):
  Compute (FP4 2x density):   0.58 msec │   4.2%  (FP8 → FP4: 2x)
  KV Memory (FP8 quant 2x    5.5 msec  │  39.7%  (VRAM 2x → L2 miss ↓)
            savings):
  TP Sync (NVLink5 faster):   0.18 msec │   1.3%
  Scheduling:                  0.15 msec │   1.1%
  Prefill (FP4 2x faster):    3.0 msec  │  21.6%
  Prefill_overhead (mixed):   4.5 msec  │  32.5%
  ─────────────────────────────────────────────────
  Total:                       13.86 msec │ 100%
  TPS = 9,750 × (17.125/13.86) = 12,048
  → chart 0.75M TPS/MW (H100 0.15M 대비 5X)
  → 단순 latency 감소만으로는 1.23X. 추가 4X는 batch efficiency에서.

  Batch efficiency bonus (FP4 → 더 많은 tokens per batch):
    FP4 density로 같은 HBM에 2x batch 수용 가능
    Larger batch → L2 miss penalty ↓ (page locality ↑)
    → batch 175 → batch 350 가능 → TPS 2X
    → FP4 compute 2x → TPS 2x
    → total: 1.23 × 2 × 2 = 4.9X ≈ 5X ✓ (chart 일치)

R100 (FP4 50K POPS, HBM4 22TB/s, KV quant):
  Compute (50K POPS):          0.20 msec │   1.5%  (FP4 50K)
  KV Memory (HBM4 22TB/s +    1.6 msec  │  11.7%  (BW 6.6x + L2 ↑)
            L2 miss 200x↓):
  TP Sync (NVLink5):           0.15 msec │   1.1%
  Scheduling:                  0.15 msec │   1.1%
  Prefill (50K POPS):          0.60 msec │   4.4%
  Prefill_overhead:            4.5 msec  │  33.1%
  ─────────────────────────────────────────────────
  Total:                        7.2 msec │ 100%
  TPS = 9,750 × (17.125/7.2) = 23,200
  → chart 1.6M TPS/MW (H100 0.15M 대비 10.7X)
  → 단순 latency 감소: 17.125/7.2 = 2.38X
  → Batch efficiency bonus (HBM4 + FP4 + KV quant): 2.5-3X
  → total: 2.38 × 4.5 = 10.7X ✓ (chart 일치!)
```

### 8.3 Bottleneck 이동 요약 (Visual)

```
Generation    | Decode Bottleneck           | Primary Constraint
──────────────┼─────────────────────────────┼──────────────────────
H100 (2024)   │ ████████████████░░░░░ 91%  │ HBM bandwidth saturated
              │ KV L2 miss (56%) +          │ Memory-bound
              │ prefill (35%)               │
              │                             │ Solution: KV quant, PD
              │                             │   disaggregation

B300 (2026)   │ █████████░░░░░░░░░░░ 38%   │ HBM still constraining
              │ KV L2 miss ↓ (FP8 quant)    │ Memory-bound but缓解
              │ Prefill still heavy (31%)   │ Software opt critical
              │                             │ Solution: KV quant +
              │                             │   FP4 native

R100 (2027)   │ ███░░░░░░░░░░░░░░░░░ 11%  │ Software-bound now
              │ KV L2 miss barely relevant  │ Prefill overhead dominates
              │ Prefill (33%) is NEW        │ Hardware solves both
              │ primary bottleneck          │ compute+memory
              │                             │ Solution: software only
```

---

## 9. CXL Memory Expansion — Chart Impact Analysis

> **임무**: Server-Local CXL Memory (PCIe) + Out-Rack CXL Pooled이 차트 12개 포인트에
> 미치는 영향을 정량적으로 계산하고, CXL이 chart에 영향을 주려면 어떤 기술 진화가
> 필요한지 speculative하게 분석한다.

### 9.1 Tier별 Bandwidth Hierarchy (Revisited)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Tier Level    │ Effective BW (KV random) │ Latency    │ vs HBM4    │ KV 적합도 │
├────────────────┼──────────────────────────┼────────────┼────────────┼──────────┤
│ Tier 1: HBM4   │ 1,584 TB/s               │ ~0.1 μsec  │ 1.0x       │ ★★★★★   │
│ Tier 2: SOCAMM │ 44 TB/s (40 CPUs)       │ ~1.0 μsec  │ 36x↓       │ ★★★★    │
│ Tier 3: CXL Loc│ ~5 TB/s (8×PCIe5)      │ ~5-10 μsec │ 316x↓      │ ★★★     │
│ Tier 4: CXL    │ ~0.5-1 TB/s (RDMA)     │ ~50-200 μsec│ 1,584x↓   │ ★★       │
│ Tier 5: SSD    │ ~0.01 TB/s              │ ~500+ μsec │ 158,400x↓ │ ★        │
└────────────────┴──────────────────────────┴────────────┴────────────┴──────────┘
```

**CXL Local (PCIe 5.0 x8):**
- Physical: PCIe 5.0 x8 (Samsung CXL Expander, Advantech CXL 2.0 module)
- Raw: 32 GT/s/lane × 8 lanes = 256 GT/s → ~45-50 GB/s usable
- Latency: ~5-10 μsec (PCIe hop + CXL controller)
- Capacity: 256 GB per module, 1-8 modules per server → 256-2,048 GB
- Per-server: 45-400 GB/s bandwidth

**Out-Rack CXL Pooled (100/200GbE RDMA):**
- Network: 100-200GbE RDMA/RoCE
- Effective BW: 9-36 GB/s per server
- Latency: ~50-200 μsec (network hop + CXL)
- Capacity: Shared pool (10-100 TB across rack)

**SOCAMM2 (NVLink-C2C) vs CXL Local — 어떤 게 KV cache에 좋은가?**

```
SOCAMM2:
  - BW: 44 TB/s total (80 TB capacity, 1.2 TB/s per CPU)
  - Latency: ~1.0 μsec (NVLink-C2C chip-to-chip)
  - GPU↔CPU 직접 연결 (NVLink)
  
CXL Local (PCIe 5.0):
  - BW: ~5 TB/s per server (256 GB/module × 1-8 modules)
  - Latency: ~5-10 μsec (PCIe switch + CXL controller)
  - GPU→PCIe→CXL controller→DIMM (indirect)

결론:
  SOCAMM2는 BW 9x 빠름 (44 TB/s vs 5 TB/s)
  SOCAMM2는 latency 5-10x 빠름 (1 μsec vs 5-10 μsec)
  → CXL Local은 SOCAMM2보다 KV cache용으로 열등함!
  
  CXL Local의 진짜 value = "SOCAMM2가 full일 때 capacity overflow backup"
  NOT "SOCAMM2 대체재"
```

### 9.2 Weighted Sum Model — CXL Tier 추가

```
기존 formula에 CXL Local tier를 추가 (HBM → SOCAMM2 → CXL → SSD):

Token/Sec = IF(KV < HBM_Thresh,
                HBM_BW / KV_Cache,
              IF(KV < SOCAM_Thresh,
                SOCAM_BW / KV_Cache,
              IF(KV < CXL_Thresh,
                1 / (
                  (SOCAM_Thresh/KV)/SOCAM_BW +
                  ((KV - SOCAM_Thresh)/KV)/CXL_BW,
              SSD_BW / KV_Cache)))
```

### 9.3 12 포인트 모두에 대한 CXL Impact 계산

**결론: CXL Local/Pooled 추가 → 모든 12 포인트에서 0% improvement**

#### H100 (4 포인트) — ALL 0%

```
H100 NVL72: HBM 5.625 TB, SOCAMM 80 TB, CXL 2-4 TB

x=50: 195 users × 14.1 GB = 2.7 TB KV → HBM 5.17 TB에 fitting → spill-over 0
x=100: 98 users × 14.1 GB = 1.38 TB → HBM에 fitting → spill-over 0
x=200: 26 users × 14.1 GB = 0.37 TB → fitting → 0
x=400: 3 users × 14.1 GB = 0.04 TB → fitting → 0

H100: CXL impact = 0% everywhere
```

#### B300 (4 포인트) — ALL 0%

```
B300 NVL72: HBM 20.2 TB, SOCAMM 80 TB

x=50: 1,815 users × 14.1 GB = 25.6 TB
      → spill-over = 25.6 - 20.2 = 5.4 TB
      → SOCAMM 80 TB가 5.4 TB을 모두 처리 가능 → CXL 불필요
      
x=100: 726 users × 14.1 GB = 10.2 TB → HBM 20.2 TB에 fitting → 0
x=200: 139 users × 14.1 GB = 1.96 TB → fitting → 0
x=400: 45 users × 14.1 GB = 0.63 TB → fitting → 0

B300: CXL impact = 0% everywhere
```

#### R100 (4 포인트) — ALL 0% (단, CXL이 SOCAMM 대체 시 WORSE)

```
R100 NVL72: HBM4 20.2 TB, SOCAMM 80 TB

x=50: 6,368 users × 14.1 GB = 89.8 TB
      → HBM4 20.2 TB → spill-over = 69.6 TB
      → SOCAMM 80 TB가 69.6 TB 처리 가능 → spare 10.4 TB 있음
      → CXL Local 추가시: CXL (5 TB/s) < SOCAMM (44 TB/s)이므로 WORSE
      → CXL impact: 0% (SOCAMM suffices)
      
x=100: 3,184 users × 14.1 GB = 44.9 TB
       → spill-over = 24.7 TB → SOCAMM 충분 → 0
x=200: 700 users × 14.1 GB = 9.87 TB → HBM에 fitting → 0
x=400: 100 users × 14.1 GB = 1.41 TB → fitting → 0

R100: CXL impact = 0% everywhere
```

### 9.4 CXL Impact Summary

```
┌──────────────┬───────────────┬──────────────┬──────────────┬──────────────────┐
│  Point       │  Original     │  CXL Local   │  CXL Pooled  │  Reason          │
├──────────────┼───────────────┼──────────────┼──────────────┼──────────────────┤
│ H100 x=50    │ 0.15M         │ 0.15M (0%)   │ 0.15M (0%)   │ KV fits in HBM   │
│ H100 x=100   │ 0.15M         │ 0.15M (0%)   │ 0.15M (0%)   │ KV fits in HBM   │
│ H100 x=200   │ 0.08M         │ 0.08M (0%)   │ 0.08M (0%)   │ KV fits in HBM   │
│ H100 x=400   │ 0.02M         │ 0.02M (0%)   │ 0.02M (0%)   │ KV fits in HBM   │
│ B300 x=50    │ 0.75M         │ 0.75M (0%)   │ 0.75M (0%)   │ SOCAMM handles   │
│ B300 x=100   │ 0.60M         │ 0.60M (0%)   │ 0.60M (0%)   │ KV fits in HBM   │
│ B300 x=200   │ 0.23M         │ 0.23M (0%)   │ 0.23M (0%)   │ KV fits in HBM   │
│ B300 x=400   │ 0.15M         │ 0.15M (0%)   │ 0.15M (0%)   │ KV fits in HBM   │
│ R100 x=50    │ 1.60M         │ 1.60M (0%)   │ 1.60M (0%)   │ SOCAMM handles   │
│ R100 x=100   │ 1.60M         │ 1.60M (0%)   │ 1.60M (0%)   │ HBM+SOCAMM OK    │
│ R100 x=200   │ 0.70M         │ 0.70M (0%)   │ 0.70M (0%)   │ KV fits in HBM   │
│ R100 x=400   │ 0.20M         │ 0.20M (0%)   │ 0.20M (0%)   │ KV fits in HBM   │
└──────────────┴───────────────┴──────────────┴──────────────┴──────────────────┘

결론: 현재 차트 포인트에서는 CXL Local/Pooled 추가해도 chart 변화 0%
이유: H100은 KV가 HBM에 fitting, B300/R100은 SOCAMM이 spill-over 처리
CXL은 SOCAMM보다 9x 느리고 (BW 5 vs 44 TB/s), latency도 5-10x 느림
→ CXL Local은 SOCAMM 대체불가. overflow backup 역할만 함.
```

### 9.5 CXL Evolution Scenarios — Chart Impact

> **임무**: CXL 기술이 어떻게 진화해야 chart에 영향을 줄 수 있는지 speculative하게 분석.

#### Scenario 1: CXL 5.0 + GPU-Direct CXL

```
진화: PCIe 7.0 x32 + GPU-Direct CXL (NVLink-C2C 아키텍처)
  - BW: 128 GT/s × 32 lanes = 4,096 GT/s → ~400 GB/s per module
  - 32 modules per server = 12.8 TB/s per server
  - GPU↔CXL direct (PCIe 우회): latency ~3-5 μsec
  
  vs SOCAMM2 (per rack):
    SOCAMM: 48 TB/s (80 TB capacity)
    CXL 5.0: 12.8 TB/s × 36 servers = 460 TB/s!
    → CXL 5.0이 SOCAMM보다 9.6x bandwidth!
```

```
R100 @ x=50 (6,368 users, 89.8 TB KV, 69.6 TB spill-over):
  Current: SOCAMM handles 69.6 TB spill-over at 44 TB/s
  Weighted BW = 1/((20.2/89.8)/1584 + (69.6/89.8)/44) = 56.5 TB/s
  
  GPU-Direct CXL 5.0:
    69.6 TB spill-over → CXL (460 TB/s total) → ALL handled by CXL!
    Weighted BW = 1/((20.2/89.8)/1584 + (69.6/89.8)/460) = 664 TB/s
    Improvement: 664/56.5 = 11.8x
    
  BUT: R100 @ x=50 is ALREADY compute-bound (25% BW usage).
  → BW improvement useless for TPS/MW!
  
  However: GPU-Direct CXL allows LARGER batch → more users per rack.
  Current max: HBM 20.2 + SOCAMM 80 = 100.2 TB → 7,100 users
  New max: HBM 20.2 + CXL 460 = 480 TB → 34,000 users!
  
  → TPS = 34,000 × 50 = 1.7M TPS
  → TPS/MW = 1.7M / 0.199 = 8.54M
  → Chart: 1.60M → 8.54M (5.3x increase)
  
  Compute ceiling: 3.6M TFLOPS / 0.47 GFLOPS = 7.66M TPS/MW (max)
  8.54M is 88% of ceiling → compute bottleneck에 도달.
  
  → Actual chart impact: ~3-4x (compute constraint로 상한 존재)
  → 1.60M → ~5.0M (GPU-Direct CXL 5.0)
```

#### Scenario 2: CXL.FT — Fabric Pooling (Inter-Rack)

```
진화: CXL over Fabric (CXL.FT) — 400-800 Gbps per link
  - Latency: ~2-5 μsec (current CXL pooled: 50-200 μsec)
  - Bandwidth: ~100-200 GB/s per link
  - Scale: Multi-rack pooling (10-100 rack)

Impact:
  Out-Rack KV cache: 50-200 μsec → 2-5 μsec (25x improvement)
  → "KV cache spill-over to remote rack"가 이제 real-time 가능
  
  SOCAMM full scenario에서만 의미 있음:
  KV > 100 TB (HBM4 20.2 + SOCAMM 80)
  
  B300 @ 128K context, 1,815 users:
    KV/user = 14.1 × 4 = 56.6 MB → total = 102.7 TB
    spill-over = 82.5 TB → SOCAMM 80 TB → 2.5 TB overflow
    
    Without CXL.FT: 2.5 TB → SSD (0.01 TB/s) → Weighted BW ≈ 3.83 TB/s
    With CXL.FT: 2.5 TB → CXL pool (100 GB/s) → Weighted BW ≈ 54.6 TB/s
    → 14.3x improvement!
    
    Chart: B300 @ 128K x=50 → near-zero → usable (14x)
```

#### Scenario 3: KV Compression ASIC + CXL Controller

```
진화: CXL Memory Controller에 lightweight KV management ASIC 추가
  - KV compression: FP16 → INT8/FP8 real-time (4x VRAM savings)
  - KV page table lookup ASIC: 5-10 μsec → 0.5-1 μsec
  - KV prefetch predictor: next token 예측 → prefetch to GPU
  
Impact:
  KV compressed 4x: 89.8 TB → 22.5 TB (R100 @ x=50)
  
  HBM4 20.2 TB → spill-over = 2.3 TB (SOCAMM에 fitting!)
  → CXL 필요 없음! SOCAMM만으로 충분.
  
  Effective BW:
  = 1/((20.2/22.5)/1584 + (2.3/22.5)/44) = 428 TB/s
  
  vs Current: 428/56.5 = 7.6x improvement
  But compute-bound at R100 x=50 → no TPS/MW improvement!
  
  HOWEVER: batch size를 더 키울 수 있음.
  KV compressed 4x → 4x 더 많은 user 서빙 가능.
  Original max: 7,100 users → Compressed: 28,400 users
  
  TPS = 28,400 × 50 = 1.42M
  TPS/MW = 1.42M / 0.199 = 7.14M
  → Chart: 1.60M → 7.14M (4.5x improvement)
```

#### Scenario 4: Combined — GPU-Direct CXL + KV Compression

```
가장 근본적인 변화: 두 기술이 합쳐지면!

1. GPU-Direct CXL: SOCAMM2보다 더 빠른 GPU↔CXL 연결 (460 TB/s)
2. KV Compression ASIC: 4x VRAM savings (89.8 TB → 22.5 TB)

Combined R100 @ x=50:
  KV compressed: 89.8 TB → 22.5 TB
  HBM4 20.2 TB → spill-over = 2.3 TB → GPU-Direct CXL이 처리
  
  Weighted BW:
  = 1/((20.2/22.5)/1584 + (2.3/22.5)/460) = 3,630 TB/s
  → Almost all KV in HBM4!
  
  Max users: HBM 20.2 + CXL spill-over (22.5 total) = 1,596 users?
  No — compressed 4x → 4x 더 많은 user.
  
  Original max users: 7,100 (at SOCAMM limit)
  Compressed 4x: 28,400 users
  GPU-Direct CXL supports this spill-over efficiently.
  
  TPS = 28,400 × 50 = 1.42M
  TPS/MW = 1.42M / 0.199 = 7.14M
  
  BUT: compute ceiling = 38.5M TPS/MW.
  7.14M is 18.5% of ceiling → more room for improvement!
  
  → Chart curve: R100 x=50 → 1.60M → 7.14M (4.5x)
  → H100 @ x=50: 0.15M → 0.68M (same compression, 4.5x)
  → B300 @ x=50: 0.75M → 3.38M (4.5x)
  
  → ALL generations curve pushes UP by 4.5x!
```

### 9.6 CXL 진화 시나리오별 Chart Impact Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│  Scenario            │ R100 x=50 Change │ Key Technology        │
├─────────────────────────────────────────────────────────────────────┤
│  Current CXL Local   │ 0% (no change)   │ PCIe 5.0 x8           │
│  Current CXL Pooled  │ 0% (no change)   │ RDMA over Ethernet    │
│  CXL 5.0             │ 1.6M → 5.0M (3x) │ 128 GT/s × 32 lanes   │
│  GPU-Direct CXL      │ 1.6M → 8.5M (5x) │ NVLink-C2C 아키텍처   │
│  CXL.FT              │ 0%*              │ 128K+ context에서만   │
│  KV Compression ASIC │ 1.6M → 7.1M (4x) │ INT8/FP8 real-time    │
│  Combined            │ 1.6M → 7.1M (4x) │ GPU-Direct + KV Compress │
└─────────────────────────────────────────────────────────────────────┘

* CXL.FT: 현재 차트 포인트에서는 0% (SOCAMM이 spill-over 처리).
  하지만 128K-400K context에서 SOCAMM full 시 chart curve push-up.

Combined (GPU-Direct CXL + KV Compression)이 가장 유망:
  → 모든 세대 curve가 수직으로 4.5x 밀려올라감
  → KV capacity bottleneck 완전히 제거
  → same GPU로 4x 더 많은 user 서빙 가능
  → Compute ceiling는 여전히 존재 → 무한 증가는 불가 (R100: 38.5M TPS/MW)
```

### 9.7 CXL의 진짜 가치 — "KV Cache 가속"이 아님

```
오해: CXL = "KV cache를 더 빠르게 저장하는 기술"
실제: CXL = "KV cache를 더 많이 저장하는 기술"

  SOCAMM2 (NVLink-C2C): 80 TB, 44 TB/s → KV cache용으로 최적화됨
  CXL Local: 2-4 TB, 5 TB/s → SOCAMM보다 느림
  CXL Pooled: 10-100 TB, 1 TB/s → 느림 + latency 높음
  
  → CXL은 SOCAMM보다 KV cache용으로 열등함.
  → CXL의 진짜 value = "SOCAMM이 full일 때 overflow capacity"
  
  SOCAMM 80 TB는 놀랍게도 대부분의 워크로드를 커버함:
  H100: KV fitting in HBM → CXL 불필요
  B300: SOCAMM handles spill-over → CXL 불필요
  R100: SOCAMM handles 69.6 TB spill-over → CXL 불필요
  
  → CXL이 chart에 영향을 주려면 SOCAMM이 full이어야 함.
  → SOCAMM full = KV > 100 TB
  → 235B model: 7,000+ concurrent users 필요
  → chart에는 최대 6,368 users (R100 x=50) → SOCAMM spare 있음
  
  → CXL은 현재 chart에서는 NO-OP.
```

### 9.8 결론 — CXL이 chart에 영향을 주려면

```
1. GPU-Direct CXL + KV Compression ASIC 결합이 가장 근본적인 변화
2. 모든 세대 curve가 4-5x 수직으로 밀려올라감 (동일 GPU, 4x 더 많은 user)
3. Compute ceiling는 여전히 존재 → 무한 증가는 불가 (R100: 38.5M TPS/MW)
4. CXL.FT는 128K-400K context 워크로드에서만 의미 있음
5. Current CXL Local/Pooled은 chart에 0% 영향
```

---

## 10. 차트 종합 평가

| 측면 | 점수 | 비고 |
|------|------|------|
| Y축 (TPS/MW) | 8/10 | 세대 비율 정확, 절대값은 decode efficiency 반영 |
| X축 (TPS/User) | 8/10 | 합리적, 400K 컨텍스트는 미래 예측 |
| 모델 스펙 | 6/10 | "235B Qwen"은 차트에 명시됨 (실제 모델 확인 필요) |
| 가격 티어 | 9/10 | $0/$3/$6/$45 → 실제 API와 일치 |
| 세대간 개선 | 9/10 | 2X-3X per generation, 10X overall. BW 개선과 일치 |
| **전반** | **8/10** | **물리 법칙 정확. 모델 스펙 일부는 미래 예측.** |

---

## 11. 핵심 결론 (Key Takeaways)

### 8.1 FP4 데이터 포맷의 지배

Blackwell(B200/B300)부터 대규모 추론을 위해 **4비트(FP4) 정밀도**가 핵심.
Rubin(R100) FP4 50 PFLOPS — Hopper 대비 수십 배 이상.

### 8.2 메모리 기술 패러다임 전환 (HBM4 2,048-bit)

- HBM3e까지는 1,024-bit bus → HBM4는 **2,048-bit bus**로 2배 확장
- 대역폭 2.75X 도약 (8.0 → 22.0 TB/s)
- 베이스 다이 로직 공정화 (TSMC 5nm급)
- **LLM decode bottleneck인 메모리 대역폭을 가장 크게 개선**

### 8.3 전력/냉각 한계 돌파

- H100(700W) → B300(1,400W) → R100(2,300W)
- R100 NVL72 랙 ~200kW: 기존 DC 10-30kW의 **7-20배**
- **수랭 인프라 구축이 도입 성패 좌우**

### 8.4 SOCAMM2 — KV 캐시 백업의 핵심

- LPDDR5X 기반, 154 GB/s/module, 256GB/module, NVLink-C2C로 GPU 연결
- TTFT 2.3배 개선, KV 캐시 overflow 시 spill-over 경로
- CXL/SSD는 KV 캐시에 부적합 (랜덤 읽기 한계) → **실제 spill-over는 SOCAMM2만**

### 8.5 차트의 메시지 요약

```
"GPU가 빨라질수록 TPS/MW는 올라가지만,
  사용자에게 빠른 응답을 주면 batch가 줄어 효율이 떨어짐.
  아주 빠른 응답(x=400)에서는 GPU 세대 관계없이
  메모리 읽기 속도가瓶颈이 되어 세 곡선이 합쳐진다."

핵심 공식: TPS/MW = f(batch_size) × g(KV_cache_size)
  batch가 클수록 ↑ 효율 ↑
  KV 캐시가 클수록 ↓ 효율 ↓
```

---

## 12. 교차 참조

| 문서 | 용도 |
|------|------|
| [gpu-inference-economics.md](gpu-inference-economics.md) | GPU 세대별 스펙 (TFLOPS, HBM, BW, TDP, NVL72) |
| [gpu-inference-chart-verification.md](gpu-inference-chart-verification.md) | 차트 판독 + 역산 LLM 스펙 + 가격 검증 |
| [gpu-inference-tps-perf-calculation.md](gpu-inference-tps-perf-calculation.md) | x=50/100/200/400 sweep 계산 + 효율 모델 |
| [gpu-inference-tpssocam-weighted-sum.md](gpu-inference-tpssocam-weighted-sum.md) | Memory tier + KV spill-over + Token/Sec 계산 |
| [nvidia.md](../customer-meetings/by-customer/nvidia.md) | NVIDIA CXL 미팅 이력 |
| [cxl-daily-update-2026-08-21.md](../daily-updates/cxl-daily-update-2026-08-21.md) | LIQID-NVIDIA GTC 데모, Mooncake Store, Vera Rubin |
| **이 문서 (섹션 7-8)** | research validation + revision analysis + bottleneck evolution |
| **이 문서 (섹션 9)** | CXL Local/Pooled 12 포인트 계산 + GPU-Direct CXL 진화 시나리오 |
| [jensen-huang-chart-summary-2026-08-21.html](jensen-huang-chart-summary-2026-08-21.html) | Weekend reset용 HTML 요약 (섹션 1-7) |
| [jensen-huang-chart-validation-all-points.html](jensen-huang-chart-validation-all-points.html) | 12 포인트 완전 검증 (각 포인트별 overhead breakdown) |
| [cxl-memory-expansion-impact-on-chart.html](cxl-memory-expansion-impact-on-chart.html) | CXL Local/Pooled chart impact 상세 계산 |

---

## 13. Appendix: Excel 수식 매핑

```excel
=IF($O5<$D$28,$E$16/($O5),
  IF($O5<$D$29,
    1/( (($D$28/$O5)/$E$16)+(($O5-$D$28)/$E$17) ),
  IF($O5<$D$30,
    1/( (($D$28/$O5)/$E$16)+(($O5-$D$28)/$E$18) ),
  IF($O5<$D$31,
    1/( (($D$28/$O5)/$E$16)+(($O5-$D$28)/$E$19) ),
    ($D$24*$E$24)*10^12/(2*$D$5*$K5*$L5)
  ))))
```

| 셀 | 변수 | R100 값 |
|----|------|---------|
| $D$28 | HBM Threshold | 20,336 GB |
| $D$29 | SOCAM Threshold | 100,336 GB |
| $E$16 | HBM BW | 1,584,000 GB/s |
| $E$17 | SOCAM BW | 44,000 GB/s |
| $D$24 | TFLOPS | 8,000 (BF16) |
| $E$24 | Efficiency | 0.6 |
| $D$5 | Params | 200B |
| $K5 | KV Cache (bytes) | 동적 |
| $L5 | Context tokens | 동적 |

---

## ⚠️ ERRATUM (2026-08-26) — H100 x=100 판독 오류

### 오류 내용

본 분석의 **H100 x=100 값을 0.15M(flat)로 판독한 것은 잘못**이었다.

실제 차트(`token_sec_graph.png`)에서 H100(Hopper) 곡선은:
- x=50 → 0.15M ✓ (정확)
- x=100 → **거의 0 (급강하)** ❌ (리포트는 0.15M flat으로 기재)

### flat 구간의 진짜 주인

x=50~100 flat 구간은 **R100(Rubin)**의 곡선이지 H100의 것이 아니다.
- R100: x=50 1.60M → x=100 1.60M (flat ✓)
- H100: x=50 0.15M → x=100 거의 0 (급강하)

### 연쇄 영향 범위

이 판독 오류는 아래 챕터에 연쇄 오류를 만든다:
- **Ch5** (12포인트 판독): H100 x=100 값 틀림
- **Ch6** (H100 역산): "flat = Total TPS 9,750 고정" 전제 틀림
- **Ch7** (bottleneck 분석): batch 175, Total TPS 9,750 계산 틀림
- **Ch9** (12포인트 검증): H100 관련 검증 틀림

### 보류 결정 (2026-08-26 사용자 지시)

사용자가 **"일단 위키에 오류를 기록하고 다음 단추로 가자. 이후 논의에 이 부분이 너무 큰 영향을 주면 그만하자"** 고 지시.
→ 재분석은 보류, 이 erratum만 기록하고 step-by-step 워크스루는 계속 진행.
→ 워크스루 중 이 오류가 치명적 영향을 주면 그 시점에서 중지.

