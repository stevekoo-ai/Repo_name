# Jensen v3 — Graph 12 Points: User Count × KV Cache vs HBM/MainMemory

> **데이터 출처**: v3 분석 (jensen-huang-chart-analysis-v3.md) + GPU Rack 스펙 + 제공 LLM 데이터

---

## GPU Hardware Specs (1 Rack 기준)

| 항목 | H100 | B300 NVL72 | R100 NVL72 |
|---|---|---|---|
| **HBM Capacity** | 2,560 GB (2.5 TB) | 20,736 GB (20.2 TB) | 20,736 GB (20.2 TB) |
| **HBM BW** | 85,760 GB/s (85.8 TB/s) | 552,960 GB/s (553 TB/s) | 1,105,920 GB/s (1,106 TB/s) |
| **Main Memory Capacity** | 8,192 GB (8 TB) | 18,432 GB (18 TB) | 18,432 GB (18 TB) |
| **Main Memory BW** | 2,212 GB/s (2.2 TB/s) | 22,188 GB/s (22.2 TB/s) | 29,860 GB/s (29.9 TB/s) |
| **Server 구성** | 8 GPU/server × 4 server = 32 GPU | 4 GPU/server × 18 server = 72 GPU | 4 GPU/server × 18 server = 72 GPU |

---

## LLM Specs (x=50/100/200/400 기준)

| 항목 | Free (x=50) | Medium (x=100) | High (x=200) | Premium (x=400) |
|---|---|---|---|---|
| LLM Version | Qwen3-235B-A22B | Kimi K2.5 | GPT MoE 2T | GPT MoE 2T |
| Attention | GQA (KV heads=4) | MLA (latent=512) | GQA (KV heads=6) | GQA (KV heads=6) |
| LLM 가중치 (weights) | 470 GB | 2,000 GB | 4,000 GB | 4,000 GB |
| KV Cache / Token | 0.193 MB/tok | 0.072 MB/tok | 0.246 MB/tok | 0.246 MB/tok |
| Context Length | 32,000 | 128,000 | 128,000 | 400,000 |
| **Per-User KV Cache** | **6.16 GB/u** | **9.22 GB/u** | **31.49 GB/u** | **98.56 GB/u** |

> Per-User KV = KV/tok (MB) × Context Length (tok) ÷ 1,024

---

## Chart Users 역산 공식

```
Chart Users = (Chart TPS/MW × 1e6 × Rack Power[MW]) / x
  - H100 MW: 0.04MW (40kW)
  - B300 MW: 0.121MW (121kW)
  - R100 MW: 0.199MW (199kW)
```

**계산 검증 (v3 분석과 일치):**

| Tier | x | Model | Chart TPS/MW | Rack MW | Chart Users | v3 분석 users | 일치? |
|---|---|---|---|---|---|---|---|
| Free | 50 | Qwen3 | H100 0.15M | 0.04 | **120** | 339 | ⚠️ 불일치 |
| | | | B300 0.7M | 0.121 | **1,694** | 1,694 | ✅ 일치 |
| | | | R100 1.65M | 0.199 | **6,567** | 6,567 | ✅ 일치 |
| Medium | 100 | Kimi K2.5 | H100 0.06M | 0.04 | **24** | 52 | ⚠️ 불일치 |
| | | | B300 0.6M | 0.121 | **726** | 726 | ✅ 일치 |
| | | | R100 1.6M | 0.199 | **3,184** | 3,184 | ✅ 일치 |
| High | 200 | GPT MoE 2T | B300 0.15M | 0.121 | **150** | 150 | ✅ 일치 |
| | | | R100 0.7M | 0.199 | **700** | 700 | ✅ 일치 |
| Premium | 400 | GPT MoE 2T | B300 0.07M | 0.121 | **70** | 70 | ✅ 일치 |
| | | | R100 0.2M | 0.199 | **200** | 100 | ⚠️ 불일치 |

> ⚠️ H100 Users: 차트 TPS/MW가 **per-GPU** 값일 가능성 있음. 실제 사용자는 v3 분석 값을 사용.
> ⚠️ R100 Premium x=400: v3은 100명, 계산은 200명. v3 분석과 비교 필요.

---

## 12개 Graph 포인트 — KV Cache vs HBM/MainMemory

### HBM 사용 가능량 (LLM 가중치 차감 후)

| GPU | HBM Total | 가중치 (High/Premium) | 가중치 (Free/Medium) | Available for KV |
|---|---|---|---|---|
| H100 | 2,560 GB | 4,000 GB | 470 GB | **1,447 GB** (Free/Medium) |
| B300 | 20,736 GB | 4,000 GB | 2,000 GB | **16,736 GB** (High/Premium) |
| R100 | 20,736 GB | 4,000 GB | 2,000 GB | **16,736 GB** (High/Premium) |

---

### Point 1: Free (x=50, Qwen3, 32K, 6.16 GB/u)

| GPU | Chart TPS/MW | Chart Users | KV Cache Required | HBM Available | HBM Over? | Main Memory | 점유율 |
|---|---|---|---|---|---|---|---|
| **H100** | 0.15M | **339** (v3) | 2,088 GB (339×6.16) | 2,090 GB (v3) | ✅ **아니오** (100%) | 2,088 GB / 8,192 GB | **25.5%** |
| **B300** | 0.7M | **1,694** | 10,432 GB (1,694×6.16) | 18,736 GB (v3) | ✅ 아니요 (56%) | 10,432 GB / 18,432 GB | **56.6%** |
| **R100** | 1.65M | **6,567** | 40,453 GB (6,567×6.16) | — | ❌ **넘어섬** (195%) | 40,453 GB / 18,432 GB | **219%** |

> ⚠️ R100 Free: KV cache 40,453 GB → HBM 20,736 GB **넘어섬** → spill 19,717 GB → SOCAMM 80TB 흡수
> R100 spill: 19,717 GB / SOCAMM 80TB = **24.6%** 수준

---

### Point 2: Medium (x=100, Kimi K2.5, 128K, 9.22 GB/u)

| GPU | Chart TPS/MW | Chart Users | KV Cache Required | HBM Available | HBM Over? | Main Memory | 점유율 |
|---|---|---|---|---|---|---|---|
| **H100** | 0.06M | **52** (v3) | 479 GB (52×9.22) | 2,090 GB (v3) | ✅ 아니요 (23%) | 479 GB / 8,192 GB | **5.8%** |
| **B300** | 0.6M | **726** | 6,693 GB (726×9.22) | 18,736 GB (v3) | ✅ 아니요 (36%) | 6,693 GB / 18,432 GB | **36.3%** |
| **R100** | 1.6M | **3,184** | 29,357 GB (3,184×9.22) | — | ❌ **넘어섬** (142%) | 29,357 GB / 18,432 GB | **159%** |

> ⚠️ R100 Medium: KV cache 29,357 GB → HBM 20,736 GB **넘어섬** → spill 8,621 GB → SOCAMM 80TB 흡수
> R100 spill: 8,621 GB / SOCAMM 80TB = **10.8%** 수준

---

### Point 3: High (x=200, GPT MoE 2T, 128K, 31.49 GB/u)

| GPU | Chart TPS/MW | Chart Users | KV Cache Required | HBM Available | HBM Over? | Main Memory | 점유율 |
|---|---|---|---|---|---|---|---|
| **H100** | N/A | — | — | — | ❌ **1차 사망 ●** | — | — |
| **B300** | 0.15M | **150** | 4,724 GB (150×31.49) | 16,736 GB | ✅ 아니요 (28%) | 4,724 GB / 18,432 GB | **25.6%** |
| **R100** | 0.7M | **700** | 22,043 GB (700×31.49) | 16,736 GB | ❌ **넘어섬** (132%) | 22,043 GB / 18,432 GB | **120%** |

> ⚠️ H100: 가중치 4TB > HBM 2.56TB → **1차 사망 ● (모델 로드 불가, 0 TPS)**
>
> ⚠️ R100: KV cache 22,043 GB → HBM 16,736 GB **넘어섬** → spill 5,307 GB → SOCAMM 흡수
> R100 spill: 5,307 GB / SOCAMM 80TB = **6.6%** 수준

---

### Point 4: Premium (x=400, GPT MoE 2T, 400K, 98.56 GB/u)

| GPU | Chart TPS/MW | Chart Users | KV Cache Required | HBM Available | HBM Over? | Main Memory | 점유율 |
|---|---|---|---|---|---|---|---|
| **H100** | N/A | — | — | — | ❌ **1차 사망 ●** | — | — |
| **B300** | 0.07M | **70** | 6,899 GB (70×98.56) | 16,736 GB | ✅ 아니요 (41%) | 6,899 GB / 18,432 GB | **37.4%** |
| **R100** | 0.2M | **100** (v3) | 9,856 GB (100×98.56) | 16,736 GB | ✅ 아니요 (59%) | 9,856 GB / 18,432 GB | **53.5%** |

> ⚠️ H100: 가중치 4TB > HBM 2.56TB → **1차 사망 ●**
>
> R100 Premium: KV cache 9,856 GB < HBM 16,736 GB → **HBM 안착** (59%)

---

## 통합 요약: Graph 12 Points Status

### 1차 사망 (가중치 > HBM) — H100 전용

| Tier | x | HBM | 가중치 | 1차 사망? |
|---|---|---|---|---|
| Free | 50 | 2.56TB | 470 GB | ✅ **OK** |
| Medium | 100 | 2.56TB | 2,000 GB | ✅ **OK** |
| High | 200 | 2.56TB | **4,000 GB** | ❌ **사망 ●** |
| Premium | 400 | 2.56TB | **4,000 GB** | ❌ **사망 ●** |

### KV Cache vs HBM (HBM Available 기준)

| GPU | Tier | x | KV Cache | HBM Avail | Status |
|---|---|---|---|---|---|
| H100 | Free | 50 | 2,088 GB | 2,090 GB | ✅ OK (100%) |
| H100 | Medium | 100 | 479 GB | 2,090 GB | ✅ OK (23%) |
| H100 | High/Premium | 200/400 | — | — | ❌ 1차 사망 ● |
| B300 | Free | 50 | 10,432 GB | 18,736 GB | ✅ OK (56%) |
| B300 | Medium | 100 | 6,693 GB | 18,736 GB | ✅ OK (36%) |
| B300 | High | 200 | 4,724 GB | 16,736 GB | ✅ OK (28%) |
| B300 | Premium | 400 | 6,899 GB | 16,736 GB | ✅ OK (41%) |
| R100 | Free | 50 | 40,453 GB | 16,736 GB | ❌ spill (242%) |
| R100 | Medium | 100 | 29,357 GB | 16,736 GB | ❌ spill (176%) |
| R100 | High | 200 | 22,043 GB | 16,736 GB | ❌ spill (132%) |
| R100 | Premium | 400 | 9,856 GB | 16,736 GB | ✅ OK (59%) |

### Main Memory 점유율 (KV Cache / Main Memory)

| GPU | Tier | x | KV Cache | Main Memory | 점유율 |
|---|---|---|---|---|---|
| H100 | Free | 50 | 2,088 GB | 8,192 GB | **25.5%** |
| H100 | Medium | 100 | 479 GB | 8,192 GB | **5.8%** |
| B300 | Free | 50 | 10,432 GB | 18,432 GB | **56.6%** |
| B300 | Medium | 100 | 6,693 GB | 18,432 GB | **36.3%** |
| B300 | High | 200 | 4,724 GB | 18,432 GB | **25.6%** |
| B300 | Premium | 400 | 6,899 GB | 18,432 GB | **37.4%** |
| R100 | Free | 50 | 40,453 GB | 18,432 GB | **219%** ⚠️ |
| R100 | Medium | 100 | 29,357 GB | 18,432 GB | **159%** ⚠️ |
| R100 | High | 200 | 22,043 GB | 18,432 GB | **120%** ⚠️ |
| R100 | Premium | 400 | 9,856 GB | 18,432 GB | **53.5%** |

---

## Graph 12 Points Visual Summary

```
              H100          B300          R100
Free:         OK(100%)      OK(56%)       spill(242%)
Medium:       OK(23%)       OK(36%)       spill(176%)
High:   X 사망 ●            OK(28%)       spill(132%)
Premium:X 사망 ●            OK(41%)       OK(59%)

■ HBM Available 점유율 (가중치 차감 후)
■ Main Memory 점유율 (KV Cache 기준)
■ R100: Free~High는 HBM을 넘어 SOCAMM/CXL로溢出
■ R100 Premium만 HBM 안착
```

---

## R100 spill → SOCAMM + CXL 흡수 경로

| Tier | x | spill (HBM 초과분) | SOCAMM 80TB | CXL 100TB | Total Fit? |
|---|---|---|---|---|---|
| Free | 50 | spill 23,717 GB | 23,717 / 80TB = **30%** | — | ✅ OK |
| Medium | 100 | spill 12,621 GB | 12,621 / 80TB = **15.8%** | — | ✅ OK |
| High | 200 | spill 5,307 GB | 5,307 / 80TB = **6.6%** | — | ✅ OK |
| Premium | 400 | HBM 안착 (0 spill) | — | — | ✅ OK |

> R100 spill = KV Cache - HBM Available
> R100 Free spill 23,717 GB / SOCAMM 80TB = 30% → SOCAMM로 충분
> SOCAMM 한계 도달 시 CXL 100TB 추가 → 총 180TB 확보

---

## 핵심 인사이트

### 1. H100: Free/Medium만 HBM에 fitting, High/Premium는 1차 사망 ●
- 가중치 4TB > HBM 2.56TB → 모델 로드 불가
- 차트에서 회색선 = 존재하지 않음

### 2. R100: Free~High는 HBM spill, Premium만 HBM 안착
- R100 spill은 SOCAMM 80TB로 흡수 가능 (가장 큰 spill 30%)
- SOCAMM 한계 넘어서면 CXL 100TB도 동원 (총 180TB)
- **R100 Premium x=400만 HBM에 fitting (59%)**

### 3. B300: 모든 포인트 HBM 안착
- B300은 spill 없이 모든 티어 HBM 안에 fitting
- SOCAMM 단계 없어 HBM 한계 도달 시 곧장 CXL로 전환

### 4. R100 Main Memory는 모든 점에서 overflowing (Free~High)
- R100 Free: Main Memory 219% → HBM + SOCAMM + CXL 필요
- R100 Medium: Main Memory 159% → SOCAMM + CXL 필요
- R100 High: Main Memory 120% → SOCAMM + CXL 필요

### 5. CXL 3.2 100TB가 R100의 "산소호흡기"
- R100 spill 발생 시 SOCAMM 80TB + CXL 100TB로 총 180TB 확보
- R100 Free spill (23.7TB) → SOCAMM만으로도 충분
- R100 Medium spill (12.6TB) → SOCAMM만으로도 충분
- R100 High spill (5.3GB) → SOCAMM만으로 충분
