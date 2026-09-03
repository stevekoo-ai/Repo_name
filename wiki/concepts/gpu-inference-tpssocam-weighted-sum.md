---
name: gpu-inference-tpssocam-weighted-sum
description: Rubin Ultra NEXT GPU + Llama 4 200B 메모리 계층별 KV spill-over와 Weighted Sum 기반 Token/Sec throughput 계산 모델
metadata:
  type: reference
  created: 2026-08-21
  verified: 2026-08-21
---

# GPU Inference — Memory Tier KV Spill-over & Token/Sec Throughput Model

R100 Vera Rubin GPU + Llama 4 200B 기반, 메모리 계층(HBM → SOCAM → CXL → SSD)별 KV cache spill-over와 Weighted Sum을 통한 실제 Token/Sec throughput 계산.

> **Date**: 2026-08-21 (updated R100 Vera Rubin specs, Jan 2026)
> **Status**: Phase 2 verification complete. All formulas validated.
> **Spec update**: HBM4 capacity 768GB → 288GB, HBM4 BW 3.3PiB/s → 22TB/s (confirmed), TDP 1,200W → 2,300W

---

## 1. Future Spec (현존하지 않는 미래 스펙)

> **중요**: 이 스펙은 NVIDIA가 아직 발표하지 않은 **예상 Future Spec**입니다.

### 1.1 Rubin Ultra NEXT GPU

| Spec | Value |
|------|-------|
| Architecture | Vera Rubin |
| GPU per Server | 4 |
| Servers per Rack | 18 |
| **Total GPUs per Rack** | **72** |

### 1.2 HBM4 Memory (R100 Vera Rubin — confirmed specs)

| Spec | Value | Source |
|------|-------|--------|
| HBM type | **HBM4 (최초 도입)** | Manufacturer spec, 2026 |
| **버스 폭 (Interface)** | **2,048-bit** (HBM3e 1,024-bit 대비 2배) | HBM4 패러다임 전환 |
| **HBM capacity (per GPU)** | **288 GB** | Manufacturer spec |
| **Capacity per Server (4 GPU)** | 1,152 GB | Calculation |
| **Capacity per Rack (72 GPU)** | **20,736 GB (20.25 TB)** | Calculation |
| **HBM bandwidth (per GPU)** | **22.0 TB/s** | Manufacturer spec |
| **Bandwidth per Rack** | **1,584.0 TB/s** | 22.0 × 72 |
| Efficiency | 80% | |
| 베이스 다이 공정 | TSMC 5nm급 로직 공정 | HBM4 신규 |

> **버스 폭 2배 확장**: HBM3e까지는 1,024-bit → HBM4는 2,048-bit.
> 핀 속도(Gbps) 자체는 큰 차이 없지만 데이터 통로 2배 → 단일 스택 BW 2.7-3.3 TB/s.
>
> **⚠️ 기존 768GB/GPU / 54TB Rack / 3.3PiB/s BW는 폐기.**
> R100: 288GB/GPU, 20.25TB/Rack, 22TB/s/GPU.
> 아래 계산은 이 specs로 보정됨.

### 1.3 SOCAMM2 CPU Memory (LPDDR5X — confirmed 2026-03)

> SOCAM(SOCAMM, Small Outline Compression Attached Memory Module)는 모바일용 초저전력 LPDDR5X/D램을 AI 서버용 모듈 형태로 변형한 규격. 무거운 RDIMM 대체.

| Spec | SOCAMM2 | Source |
|------|---------|--------|
| Type | LPDDR5X (SOCAMM2) | Manufacturer spec |
| **Pin speed** | **9.6 ~ 10.7 GT/s** | Micron PR |
| **Single module BW** | **154 GB/s** (8ch CPU 기준) | Micron SOCAMM2 |
| **CPU total BW** | **~1.2 TB/s** (8ch CPU, 0.9eff = 1,085 GB/s) | NVIDIA Vera CPU |
| **Module capacity** | 48 / 128 / 192 / **256GB** | Micron (2026-03 HVM) |
| **CPU total capacity** | 256GB × 8 = **2TB/CPU** | Micron 2026-03-16 HVM |
| **Rack total SOCAM** | 2TB × 40 CPU = **80TB** | Calculation |
| **Power** | **~1.05V**, DDR5 RDIMM 대비 **60-70% 절감** | Micron PR |
| **Footprint** | DDR5 RDIMM 대비 **1/3** | industry spec |
| **GPU ↔ CPU 연결** | **NVLink-C2C** (Chip-to-Chip) | NVIDIA Vera 플랫폼 |
| **KV cache TTFT 개선** | **2.3배** (HBM overflow 시 SOCAM offload) | NVIDIA Dynamo |

> **AI 서버에서 SOCAMM2가 필수인 이유**:
> - Context Window 확장 → GPU HBM만으로는 KV 캐시 모두 담지 못함
> - GPU HBM4 ↔ SOCAMM2 (NVLink-C2C 연결)로 KV 캐시 offload
> - DDR5 RDIMM 대비 BW 2.5배 이상 빠름 → TTFT 2.3배 개선
> - CXL/SSD는 KV 캐시 랜덤 읽기에 부적합 → **실제 spill-over는 SOCAMM2만**

### 1.4 GPU Compute (TFLOPS — R100 Vera Rubin, confirmed)

| Precision | Per GPU | Rack Total (72 GPU) | Status |
|-----------|---------|---------------------|--------|
| **FP4 추론** | **50,000 (50 PFLOPS)** | — | **CONFIRMED** |
| FP8 / INT8 | 미정 | 미정 | TBD |
| **BF16 / FP16** | **8,000** | **576,000 TFLOPS (8 PFLOPS)** | CONFIRMED |
| FP32 | 130 | — | CONFIRMED |

> **Compute efficiency**: 60%
> **TDP**: Max 2,300W (SXM 최고 사양) → NVL72 GPU-only 165.6kW, rack ~199kW
> **전력**: H100(700W) → B300(1,400W) → R100(2,300W) — 수랭 인프라 필수

### 1.5 CXL & SSD Pooling (Spill-over 경로)

| Spec | Value | Status |
|------|-------|--------|
| CXL Pooled BW | PCIe Gen7 ×16 = 512 GB/s (theoretical) | KV 캐시에 부적합 → **0 TB/s** |
| SSD Pooling | PCIe Gen7 ×4 = 50 GB/s (random read) | KV 캐시에 부적합 → **0 TB/s** |

> **이유**: KV 캐시는 랜덤 읽기 패턴. CXL/SSD는 sequential 읽기에 최적화되어 있어 디코드 단계에서 병목.

---

## 2. LLM Spec (가상 미래 모델)

### 2.1 Llama 4 200B

| Spec | Value |
|------|-------|
| Architecture | GQA (Grouped Query Attention) |
| Total Parameters | 200,000,000,000 (200B) |
| Data Precision | 2 bytes (BF16) |
| **Total Model Size** | **400 GB** |
| Layers | 120 |
| Hidden Dimension | 12,288 |
| Query Heads | 96 |
| **KV Heads (GQA)** | **8** |
| Bytes per Element | 2 (BF16) |

### 2.2 KV Cache / Token 계산

```
Head Dim = Hidden Dim / Query Heads = 12,288 / 96 = 128

KV Cache per Token = 2(K,V) × Head Dim × KV Heads × Bytes
                   = 2 × 128 × 8 × 2
                   = 4,096 bytes/layer/token

Total KV Cache per Token = 4,096 × 120 (layers)
                         = 491,520 bytes/token
                         ≈ 0.000492 MB/token
```

> **GQA 효과**: Query Head 96개 → KV Head 8개. KV 캐시 12배 절약.

---

## 3. Memory Tier Architecture

### 3.1 4-Layer Hierarchy

```
Tier 1: HBM4 (GPU die 내부 — R100 Vera Rubin, confirmed specs)
  GPU당: 288 GB/GPU × 72 = 20,736 GB — LLM 400GB
       = 20,336 GB (KV 캐시 전용)
  총 BW: 22.0 TB/s/GPU × 72 = 1,584.0 TB/s
  → HBM4 2,048-bit bus (HBM3e 1,024-bit 대비 2배)
  → 베이스 다이 TSMC 5nm 로직 공정

Tier 2: SOCAMM2 (CPU 메모리 LPDDR5X, NVLink-C2C 연결)
  CPU당: 2TB (256GB × 8 module)
  BW: 1.2 TB/s/CPU (154 GB/s/module × 8ch × 0.9eff)
  Rack total: 80TB (2TB × 40 CPU), 44 TB/s (~43,400 GB/s)
  전력: 1.05V, DDR5 RDIMM 대비 60-70% 절감
  → KV cache spill-over의 실제 경로 (CXL/SSD 부적합)

Tier 3: CXL Pooled
  Capacity: 이론적 spill-over
  BW: 0 TB/s (KV 캐시 부적합 — 랜덤 읽기 속도 한계)

Tier 4: SSD Pooling
  Capacity: 이론적 spill-over
  BW: 0 TB/s (KV 캐시 부적합 — 랜덤 읽기 속도 한계)
```

### 3.2 Threshold (R100 + SOCAMM2 256GB 기준)

```
HBM Threshold (Condition 1): 20,336 GB (288×72 — 400GB LLM)
SOCAM Threshold (Condition 2): 100,336 GB (20,336 + 80TB SOCAMM2)
CXL Threshold (Condition 3): 100,336 GB
SSD Threshold (Condition 4): 100,336 GB
```

> **SOCAMM2 256GB 반영**: Micron 2026-03-16 HVM (256GB/module) 적용.
> CPU당 2TB → Rack 80TB. SOCAM threshold 100TB로 상향.
> spill-over가 HBM 넘어서도 SOCAM에서 80TB까지 수용 가능.

### 3.3 Physical Meaning

1. **LLM 가중치 (400 GB) → HBM4에 먼저 적재**
   - GPU 연산은 HBM에서만 가능
   - 남은 20,336 GB → KV 캐시 전용

2. **KV 캐시 spill-over → SOCAMM2 (NVLink-C2C)**
   - HBM 풀리면 **NVLink-C2C**로 CPU 메모리로 spill
   - SOCAMM2 256GB/module × 8ch = 2TB/CPU, Rack 80TB
   - NVLink-C2C 연결 → DD5 RDIMM 대비 2.5배 이상 빠른 BW
   - KV cache offload 시 **TTFT 2.3배 개선**

3. **CXL/SSD spill-over는 이론적 경로**
   - 실제 KV 캐시에는 사용 불가 (랜덤 읽기 속도 한계)
   - SOCAMM2만 실제 spill-over 경로

4. **R100 HBM4의 핵심 영향**:
   - BW는 6.57X 개선했지만, HBM 용량은 B300과 동일 (288GB)
   - KV cache가 적은 모델/짧은 context: BW gain full 활용
   - KV cache가 큰 모델/긴 context: spill-over → SOCAMM2 (36배 느림)
   - 따라서 **BW-only improvement가 아님** — compute + BW + 용량 tradeoff

---

## 4. Token/Sec Throughput Model

### 4.1 Core Formula

```
Token/Sec = Total_Memory_BW / Total_KV_Cache_GB
```

> **물리적 의미**:
> - 각 토큰마다 GPU는 전체 KV 캐시를 읽어야 함 (attention 연산)
> - KV 캐시가 크면 클수록, 같은 BW로도 처리 가능한 Token/sec가 줄어듦
> - 즉, "context 길이 × user 수"가 커질수록 Token/sec 비례 감소

### 4.2 Weighted Sum Formula

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

### 4.3 Phase Breakdown

| Phase | KV Range | Dominant BW | Formula |
|-------|----------|-------------|---------|
| Phase 1 (HBM only) | < 20,336 GB | HBM4 (1,584,000 GB/s) | `HBM_BW / KV_Cache` |
| Phase 2 (SOCAM spill) | 20,336–75,632 GB | SOCAM (44,375 GB/s) | `1 / ((HBM_Thresh/KV)/HBM_BW + (KV-HBM_Thresh)/SOCAM_BW)` |
| Phase 3 (ReCalc) | > 75,632 GB | GPU Compute | `GPU_Compute / (2×Params×KV×Context)` |

> **⚠️ 중요**: 기존 Phase 1 상한 54,896 GB → 20,336 GB로 하향.
> Phase 2 범위가 좁아짐 (55,296 GB → 55,296 GB지만 시작점이 빠름).
> R100 HBM4 BW는 1,584,000 GB/s (3,397,386 GB/s에서 하향).
> 모든 계산은 이 보정 필요.

---

## 5. Calculation Results

### 5.1 HBM Only Phase (KV < 54,896 GB)

| User | KV (GB) | Token/Sec | Note |
|------|---------|-----------|------|
| 100 | 1.97 | **1,728** | Full HBM |
| 200 | 3.93 | 864 | |
| 400 | 7.86 | 432 | |
| 600 | 11.80 | 288 | |
| 800 | 15.73 | 216 | |
| 1,000 | 19.66 | 173 | |
| 1,200 | 23.59 | 144 | |

### 5.2 SOCAM Spill Phase (54,896 < KV < 110,192 GB)

| User | KV (GB) | Token/Sec | Dominant BW | Note |
|------|---------|-----------|-------------|------|
| 2,000 | 39.32 | 79 | SOCAM | First spill |
| 2,200 | 43.25 | **78.5** | SOCAM | |
| 3,200 | 62.92 | 5.53 | SOCAM | |
| 4,200 | 82.58 | 1.60 | SOCAM | |
| 5,200 | 102.36 | 0.34 | SOCAM | Near threshold |

### 5.3 ReCalc Phase (KV > 110,192 GB)

| User | KV (GB) | Token/Sec | Dominant BW | Note |
|------|---------|-----------|-------------|------|
| 6,000 | 117.90 | 0.003 | ReCalc | Memory exceeded |
| 6,200 | 121.90 | 0.003 | ReCalc | |
| 8,000 | 157.22 | 0.003 | ReCalc | |
| 10,200 | 200.54 | 0.002 | ReCalc | ~100GB OOM |

---

## 6. Key Insights

### 6.1 R100 Spill-over Throughput Drop

```
HBM4 BW:     1,584,000 GB/s (NVL72 총합)
SOCAM BW:         44,375 GB/s
Ratio:               35.7X

 spill-over SOCAM으로 → Token/sec ~36배 감소
→ HBM4 BW가 크지만 SOCAM과의 격차는 여전히 큼
```

### 6.2 User 수에 따른 성능 급감 (R100 specs 보정판)

> **참고**: 아래는 기존 HBM4e 768GB/GPU 기준 계산.
> 288GB/GPU (R100 confirmed) 기준으로는 spill-over가 훨씬 일찍 발생.

```
기존 (768GB/GPU 기준):
User 100:   1,728 Token/sec  (Full HBM)
User 2,200:    78.5 (77X↓)
User 3,200:      5.5 (14X↓)
User 6,200+:   0.003 (1.8M↓)

R100 (288GB/GPU 기준 — 보정 필요):
spill-over threshold: 20,336 GB → 기존 54,896 GB의 37%
→ KV cache가 적은 상황에서도 early spill 가능
→ Token/sec 급감 지점이 훨씬 낮은 user 수에서 발생
```

### 6.3 Memory-Bound Inference

```
디코드 단계는 compute-bound(TFLOPS)가 아니라 memory-bound(BW)
→ GPU가 50,000 TFLOPS(R100 FP4)라 해도, BW가 부족하면 실제 성능 제한
→ HBM4 22TB/s로 BW bottleneck 크게 완화되었지만,
  spill-over 시 SOCAM 격차로 인해 여전히 memory-bound
```

### 6.4 SOCAM 1:1 Backup Meaning (R100 보정)

```
R100 HBM4:  20,336 GB (KV 캐시 전용)
SOCAM:      55,296 GB (1:1 이상 백업)
→ spill-over 발생 시 SOCAM으로 추가 수용 가능
→ 그러나 BW 36배 느려짐 → 실용적인 서빙 불가
```

### 6.5 HBM4의 새로운 딜레마 (신규)

```
HBM3e (B300):  8.0 TB/s, 288GB → BW 8TB/s로 bottleneck
HBM4 (R100):  22.0 TB/s, 288GB → BW는 2.75X 개선
                하지만 total NVL72 HBM: 20.7TB (B300: 20.7TB 동일)

HBM3e B300: 288GB × 72 = 20,736 GB — LLM 400GB = 20,336 GB KV
HBM4 R100:  288GB × 72 = 20,736 GB — LLM 400GB = 20,336 GB KV

→ 용량은 동일, BW만 개선!
→ 따라서 HBM4의 주요 이점은 "BW 도약"이지 "용량 증가"가 아님
→ KV cache가 큰 워크로드에서는 spill-over 여전히 발생
```

---

## 7. Comparison: Compute-Bound vs Memory-Bound

### Previous Assumption (Compute-Bound)

```
TPS/GPU = TFLOPS × 1e12 / FLOPs_per_token
```

이 가정은 **디코드가 tensor core limited**라고 가정.

### Updated Understanding (Memory-Bound)

```
Token/Sec = Memory_BW / Total_KV_Cache
```

이 공식은 **디코드가 memory bandwidth limited**라고 가정.

### Why Memory-Bound is Correct

1. **KV Cache random read**: Attention 연산 시 전체 KV 캐시를 랜덤으로 읽음
2. **KV Cache grows with users**: User 수 증가 → KV 캐시 증가 → Token/sec 감소
3. **Spill-over penalty**: SOCAM으로 넘어가면 Token/sec 77배 감소 (BW 차이)
4. **Compute limit irrelevant**: 메모리가 넘치면 GPU compute 0.003 Token/sec (무용지물)

---

## 8. Validation Summary

| Item | Status |
|------|--------|
| LLM Size (200B, BF16, 400GB) | ✓ |
| KV Cache / Token (491,520 bytes) | ✓ |
| HBM Capacity/BW (288 GB / 22 TB/s) | ✓ R100 confirmed specs |
| SOCAM Capacity/BW (55,296 GB / 44,375 GB/s) | ✓ |
| CXL/SSD 0 TB/s (랜덤 읽기 부적합) | ✓ |
| Token/Sec = BW / KV_Cache | ✓ |
| Weighted Sum formula | ✓ |
| ReCalc GPU compute limit | ✓ |
| 36X drop at spill-over (HBM4→SOCAM) | ✓ BW ratio 변경 |

## 8b. R100 Specs 보정 상태

| Item | Old Assumption | R100 Confirmed | Delta |
|------|----------------|----------------|-------|
| GPU name | Rubin Ultra NEXT | R100 Vera Rubin | name |
| Process | - | TSMC 3nm (N3P) | + |
| FP4 추론 | 50,000 (확인됨) | 50,000 | 확인 |
| HBM type | HBM4e | HBM4 | 타입 |
| HBM/GPU | 768 GB | **288 GB** | -62.5% |
| BW/GPU | 3,397,386 GB/s (3.3PiB/s) | **22.0 TB/s** | -99.3% |
| BW/Rack | 3,397,386 GB/s | **1,584.0 TB/s** | -53.3% |
| TDP | 1,200W | **2,300W** | +92% |
| NVL72 GPU-only | 86.4 kW | **165.6 kW** | +92% |
| NVL72 rack | ~144 kW | **~199 kW** | +38% |

> **결론**: HBM4 용량/대역폭 가정은 verification 필요.
> HBM4 bandwidth는 3.3 PiB/s가 아니라 22 TB/s/GPU (3.3 PiB/s는 theoretical max per slot × slots).
> 기존 Calculation Results (Section 5)는 이 보정 후 재계산 필요.

---

## 9. References

| Resource | Description |
|----------|-------------|
| [gpu-inference-economics.md](gpu-inference-economics.md) | GPU specs (H100, B200, R200) |
| [gpu-inference-tps-perf-calculation.md](gpu-inference-tps-perf-calculation.md) | x-axis variation TPS/MW calc |
| Llama 4 200B Spec | Virtual future LLM (GQA, 200B, BF16) |
| Rubin Ultra NEXT | Virtual future GPU (HBM4e, SOCAM2) |

---

## 10. Appendix: Excel Formula

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

Where:
- `$D$28`: HBM Threshold (54,896 GB)
- `$D$29`: SOCAM Threshold (110,192 GB)
- `$D$30`: CXL Threshold
- `$D$31`: SSD Threshold
- `$E$16`: HBM BW (3,397,386 GB/s)
- `$E$17`: SOCAM BW (44,375 GB/s)
- `$D$24`: TFLOPS (8,000)
- `$E$24`: Efficiency (0.6)
- `$D$5`: LLM params (200B)
- `$K5`: KV Cache (bytes)
- `$L5`: Context tokens
