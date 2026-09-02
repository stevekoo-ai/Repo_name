---
name: gpu-inference-chart-verification
description: NVIDIA inference economics chart verification — reverse-engineered LLM specs, TPS/MW and TPS/User axis validation
metadata:
  type: reference
  created: 2026-08-20
  verified: 2026-08-20
---

# GPU Inference Economics Chart — Verification & Reverse-Engineered Specs

NVIDIA inference economics slide analysis — chart's X/Y axes validated, assumed LLM specs reverse-engineered.

> **Source**: NVIDIA keynote slide (GTC-style)
> **Date**: 2026-08-20
> **Analysis method**: Chart points read from image → total TPS inverse-calculation → model spec reconstruction → cross-check with known GPU specs and real-world model data

---

## 1. Chart Overview

**Chart structure:**
- **Y-axis**: TPS/MW — tokens per second per megawatt (GPU decode throughput efficiency)
- **X-axis**: TPS/User — tokens per second per concurrent user (interactivity target / SLA)
- **Three GPU curves**: Hopper (H100 SXM5), Blackwell (B200), Rubin (B300)
- **Four service tiers**: FREE ($0), MEDIUM ($3), HIGH ($6), PREMIUM ($45)

**Chart annotations:**
- Hopper → Blackwell: 2X improvement at x=50, 2X at x=100, 3X at x=200
- Hopper → Blackwell → Rubin: 10X overall at x=400

---

## 2. Chart Points Read from Image

| Tier | GPU | TPS/User | TPS/MW | Implied Total TPS | Implied Users |
|------|-----|----------|--------|-------------------|---------------|
| **FREE** | Hopper | 50 | 150,000 | 9,750 | 195 |
| **MEDIUM** | Blackwell | 100 | ~1,000,000 | ~120,000 | ~1,200 |
| **HIGH** | Blackwell | 200 | 700,000 | 84,000 | 420 |
| **PREMIUM** | Blackwell | 400 | 200,000 | 24,000 | 60 |
| Rubin @ 200 | Rubin | 200 | 1,600,000 | 230,400 | 1,152 |
| Rubin @ 400 | Rubin | 400 | 200,000 | 28,800 | 72 |

**Calculation method**: `Total TPS = TPS/MW × rack_MW`
- Hopper rack: 65kW = 0.065 MW
- Blackwell rack: 120kW = 0.120 MW
- Rubin rack: 144kW = 0.144 MW

---

## 3. Reverse-Engineered LLM Specs (What the Chart Assumes)

The chart's TPS/MW numbers imply specific model specifications. Here's what the chart MUST assume to produce the curves shown.

### 3.1 Derivation Method

```
Formula: TPS = HBM_BW / (Active_Params × 2 bytes)
→ Active_Params = HBM_BW / (TPS × 2)

Where:
  HBM_BW = total rack bandwidth (TB/s converted to bytes/s)
  TPS = total system throughput (from chart's TPS/MW × rack_MW)
  2 = bytes per parameter (FP16 weights)
```

**Key insight**: The chart measures SYNTHETIC throughput (max batching, no KV cache constraint) for TPS/MW, then shows the PER-USER interactivity as a separate axis. The curve shape represents the THROUGHPUT-LATENCY FRONTIER (standard systems theory).

### 3.2 FREE Tier — Hopper Curve at x=50

```
Chart data:
  TPS/User: 50
  TPS/MW: 150,000
  GPU: Hopper H100 SXM5 NVL72

Reverse-calculated:
  Total throughput: 9,750 TPS (0.065 MW × 150,000)
  Concurrent users: 195 (9,750 / 50)
  Total HBM BW available: 241.2 TB/s (3.35 × 72)

KV Cache constraint:
  Usable HBM: ~4.5 TB (80% of 5.625 TB)
  Users: 195
  Max KV cache/user: ~23.2 GB (4,500 GB / 195)
```

**ASSUMED MODEL SPEC:**

| Spec | Value | Status |
|------|-------|--------|
| Architecture | Dense (non-MoE) | Required by TPS/MW |
| Total Parameters | **7-72B** | Chart says "235B" → WRONG |
| Active Parameters | 7-72B (same as total, dense) | |
| Context Window | 32K tokens | Matches chart label |
| Hidden Dim | 4,096-8,192 | Llama-70B class |
| Layers | 32-80 | |
| KV Cache/User | 0.5-3 GB | Fits in Hopper HBM |
| Max Concurrent | 100-200 users | Reasonable |
| HBM BW Util | ~40-60% | Realistic decode efficiency |

**REAL-WORLD EQUIVALENT**: Llama-3.1-70B class, Qwen-2.5-32B class

**VERDICT**: `"235B"` on chart is WRONG. Qwen family has 7B, 14B, 32B, 72B, 110B — no 235B model exists. The chart's TPS/MW requires 7-72B dense model.

---

### 3.3 MEDIUM Tier — Blackwell Curve at x~100

```
Chart data:
  TPS/User: 100
  TPS/MW: ~1,000,000 (interpolated from Blackwell curve)
  GPU: Blackwell B200 NVL72

Reverse-calculated:
  Total throughput: ~120,000 TPS (0.12 MW × 1M TPS/MW)
  Concurrent users: ~1,200 (120,000 / 100)
  Total HBM BW available: 576 TB/s (8 × 72)
```

**ASSUMED MODEL SPEC:**

| Spec | Value | Status |
|------|-------|--------|
| Architecture | MoE (Mixture of Experts) | |
| Total Parameters | **1-3T** (all experts) | Chart says "1T" → plausible as total |
| Active Parameters | **1-3B per token** | Chart requires this for TPS/MW |
| Context Window | 128K tokens | Matches chart label |
| Hidden Dim | 4,096-8,192 (per expert) | |
| Layers | 48-80 | |
| Experts | 64-128 | Many small experts |
| KV Cache/User | ~4.6 MB max | Very constrained |

**REAL-WORLD EQUIVALENT**: Mixtral 8x7B class (46.7B total, 12.9B active)

**VERDICT**: `"1T"` likely refers to TOTAL params (MoE). But active params of 1-3B is UNUSUALLY LOW for MoE. Typical MoE (Kimi K1) has 100-500B active. The chart assumes a more efficient MoE with many small experts than what currently exists.

---

### 3.4 HIGH Tier — Blackwell Curve at x=200

```
Chart data:
  TPS/User: 200
  TPS/MW: 700,000
  GPU: Blackwell B200 NVL72

Reverse-calculated:
  Total throughput: 84,000 TPS (0.12 MW × 700K)
  Concurrent users: 420 (84,000 / 200)
  Total HBM BW available: 576 TB/s
```

**ASSUMED MODEL SPEC:**

| Spec | Value | Status |
|------|-------|--------|
| Architecture | MoE | |
| Total Parameters | **2-5T** (estimated) | Chart says "2T" → plausible |
| Active Parameters | **2-5B per token** | Chart requires this |
| Context Window | 128K tokens | Matches chart label |

**REAL-WORLD EQUIVALENT**: GPT-4o class (2T total, ~100B active)

**VERDICT**: `"2T"` total params is plausible for GPT-4o class. But the chart's TPS/MW implies only 2-5B active params, NOT the ~100B active that GPT-4o actually uses. This is a ~100X difference. Either:
1. Chart assumes more efficient MoE than currently exists, OR
2. TPS/MW measurement excludes prefill overhead, OR
3. TPS/MW is synthetic (batch=1, no real context)

---

### 3.5 PREMIUM Tier — Blackwell/Rubin at x=400

```
Chart data:
  TPS/User: 400
  TPS/MW: 200,000
  Both Blackwell and Rubin curves converge at 200K

Reverse-calculated:
  Total throughput: 24,000 TPS (0.12 MW × 200K)
  Concurrent users: 60 (24,000 / 400)
```

**ASSUMED MODEL SPEC:**

| Spec | Value | Status |
|------|-------|--------|
| Architecture | MoE | |
| Total Parameters | 2-5T | Same as High tier |
| Active Parameters | 100-200B | Like GPT-4o (at 400K context, bottleneck shifts) |
| Context Window | **400K tokens** | **DOES NOT EXIST** |

**REAL-WORLD EQUIVALENT**: No current model offers 400K context. Closest: Gemini 1.5 Pro (1M+ context), Claude Opus (200K context).

**VERDICT**: `400K context` DOES NOT EXIST. No current public model supports this. This is a FUTURE PROJECTION.

**Why Blackwell and Rubin CONVERGE at x=400:**
At very high interactivity targets, the bottleneck shifts from GPU compute/BW to:
1. KV cache memory (per-user storage dominates)
2. Network latency between GPU and user
3. Scheduling overhead (tiny batches = less efficiency)

These bottlenecks are GENERATION-INDEPENDENT, so curves converge. This is PHYSICALLY MEANINGFUL.

---

## 4. Generational Improvement Verification

### Chart Claims vs Memory Bandwidth Improvements

| Transition | Chart Improvement | Memory BW Improvement | Status |
|------------|-------------------|----------------------|--------|
| Hopper → Blackwell (x=50) | 2X | 2.4X (3.35 → 8.00 TB/s) | CONSISTENT |
| Hopper → Blackwell (x=200) | 3X | 2.4X | PLAUSIBLE (prefill overhead reduces ratio) |
| Hopper → Blackwell (x=400) | ~200K / ~150K ≈ 1.3X | 2.4X | Converged at high interactivity |
| Overall Hopper → Rubin (x=400) | 10X | ~4.8X (3.35 → 16 TB/s) | PLAUSIBLE |

**Why chart shows 2X-3X not 4.8X:**
1. Decoding is not 100% bandwidth-bound (compute overhead)
2. Pre-fill is compute-bound (not bandwidth-bound)
3. Real-world utilization < 100% (40-60% typical for decode)

**Verdict**: 2X-3X per generation is CONSISTENT with real-world decode throughput improvements.

---

## 5. Price Tier Verification

| Tier | Chart Price | Real API Equivalent | Status |
|------|-------------|-------------------|--------|
| FREE | $0 | Qwen free tier, Claude free tier, GPT-4o-mini free | ✓ PLASUABLE |
| MEDIUM | $3 | Kimi API, Gemini Pro (~$3/M input) | ✓ PLASUABLE |
| HIGH | $6 | GPT-4o ($5/M input), mid-tier Claude | ✓ PLASUABLE |
| PREMIUM | $45 | GPT-4 Turbo ($10/M input + $30/M output), Claude Opus ($15/M input + $75/M output) | ✓ PLASUABLE |

---

## 6. Final Verdict

### Overall Accuracy Scores

| Aspect | Score | Notes |
|--------|-------|-------|
| **Y-AXIS (TPS/MW)** | 6/10 | Ratios between generations correct, but absolute values assume more efficient MoE than currently exists |
| **X-AXIS (TPS/User)** | 8/10 | Reasonable interactivity targets, but 400K context model doesn't exist |
| **MODEL SPECS** | 4/10 | "235B Qwen" is wrong, "400K context" doesn't exist, MoE efficiency assumed is unrealistically high |
| **PRICING** | 9/10 | $0/$3/$6/$45 maps well to real API tiers |
| **GENERATIONAL** | 9/10 | 2X-3X per generation, 10X overall. Consistent with memory bandwidth improvements |
| **OVERALL** | **7/10** | Chart's PHYSICS are correct. Model SPECS are inaccurate or forward-looking |

### Key Findings Summary

1. **"235B" for Free tier is WRONG** — Qwen doesn't have a 235B model. Likely 7-72B dense model.
2. **"1T" for Medium is TOTAL params (MoE)** — Active params per token are 1-3B based on chart's TPS/MW, much smaller than real Kimi K1 (100-500B active).
3. **"2T" for High/Premium is TOTAL params (MoE)** — Chart's TPS/MW implies active params of 1-5B, NOT ~100B that GPT-4o uses. Chart assumes more efficient MoE than currently exists.
4. **400K context for Premium tier DOES NOT EXIST** — No current public model supports this. Future projection.
5. **Generational improvement factors (2X-3X) are CONSISTENT** with real memory bandwidth improvements.
6. **Curve convergence at x=400 is PHYSICALLY MEANINGFUL** — At very high interactivity, bottlenecks are generation-independent.

---

## 7. Sources & References

| Source | Type | Relevance |
|--------|------|-----------|
| [GPU Inference Economics Specs](gpu-inference-economics.md) | wiki reference | Hopper/Blackwell/Rubin TFLOPS, HBM, bandwidth, power specs |
| NVIDIA GTC 2024 keynote | primary source | B200 specs, GB200 NVL72 benchmark (1.4M TPS) |
| NVIDIA GTC 2025 announcement | primary source | Rubin architecture "2X" claims |
| Llama, Qwen, Kimi, GPT-4o public docs | primary sources | Model architecture, parameter counts, context windows |
| Real-world API pricing | public data | Price tier validation |
