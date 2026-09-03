---
name: gpu-inference-economics
description: NVIDIA GPU generations (Hopper/Blackwell/Rubin) TFLOPS, HBM, bandwidth, power specs — verified sources only
metadata:
  type: reference
  created: 2026-08-20
  verified: 2026-08-20
---

# GPU Inference Economics — Verification Reference

NVIDIA GPU generations: Hopper (H100) → Blackwell (B200) → Rubin (B300)

> **Source**: NVIDIA GTC 2023, NVIDIA GTC 2024, NVIDIA GTC 2025
> **Date**: 2026-08-20
> **Verified by**: GPU inference economics chart analysis

---

## 1. Hopper — H100 SXM5

**Verification Status**: ALL CONFIRMED (NVIDIA official specs)

### Compute

| Spec | Value | Source |
|------|-------|--------|
| Process | TSMC 4N (custom 5nm class) | NVIDIA |
| Transistors | 80 billion | NVIDIA |
| Die size | 815 mm² | NVIDIA |
| FP64 TFLOPS (dense) | 67 TFLOPS | NVIDIA spec sheet |
| FP8 TFLOPS (dense) | 989 TFLOPS | NVIDIA spec sheet |
| FP8 TFLOPS (2:3 sparsity) | 1,979 TFLOPS | NVIDIA spec sheet |
| FP4 POPS (2:4 sparsity) | 3,958 POPS | NVIDIA spec sheet |

> **Note**: POPS includes sparsity acceleration (4X density for 2:4).
> NVIDIA uses POPS for FP4, TFLOPS for FP8/FP64 — not directly comparable.

### Memory

| Spec | Value | Source |
|------|-------|--------|
| HBM type | HBM3 | NVIDIA |
| HBM capacity (per GPU) | 80 GB | NVIDIA |
| HBM bandwidth (per GPU) | 3.35 TB/s | NVIDIA |

### Power & NVL72

| Spec | Value | Source |
|------|-------|--------|
| TDP (per GPU) | 700 W | NVIDIA (SXM5 form factor) |
| NVL72 GPU count | 72 | NVIDIA |
| NVL72 total HBM | 5.625 TB (80 × 72 / 1024) | Calculation |
| NVL72 total bandwidth | 241.2 TB/s (3.35 × 72) | Calculation |
| NVL72 GPU-only power | 50.4 kW (700 × 72) | Calculation |

---

## 2. Blackwell — B200

**Verification Status**: PARTIALLY VERIFIED (key specs confirmed)

### Compute

| Spec | Value | Source | Status |
|------|-------|--------|--------|
| Architecture | Blackwell | NVIDIA GTC 2024 | CONFIRMED |
| Process | TSMC 4NP | NVIDIA GTC 2024 | CONFIRMED |
| Transistors (GB200) | 208 billion | NVIDIA GTC 2024 | CONFIRMED |
| FP4 POPS (per B200) | 10,000 POPS (10 PFLOPS) | NVIDIA GTC 2024 | CONFIRMED |
| FP4 POPS (GB200 2-chip) | 20,000 POPS (20 PFLOPS) | NVIDIA GTC 2024 | CONFIRMED |

> **Source**: NVIDIA GTC 2024 keynote, Jensen Huang
> "20 petaflops of FP4 compute per GB200 superchip"

### Memory

| Spec | Value | Source | Status |
|------|-------|--------|--------|
| HBM type | HBM3e | NVIDIA GTC 2024 | CONFIRMED |
| HBM capacity (per GPU) | 192 GB | NVIDIA GTC 2024 | CONFIRMED |
| HBM bandwidth (per GPU) | 8 TB/s | NVIDIA GTC 2024 | CONFIRMED |

### Power

| Spec | Value | Source | Status |
|------|-------|--------|--------|
| TDP (per GPU) | 1,000 W | NVIDIA GTC 2024 | CONFIRMED (widely reported) |
| NVL72 GPU count | 72 | NVIDIA GTC 2024 | CONFIRMED |
| NVL72 boards | 36 (2 GPUs per board) | NVIDIA GTC 2024 | CONFIRMED |
| NVL72 Grace CPUs | 36 | NVIDIA GTC 2024 | CONFIRMED |
| NVL72 GPU-only power | 72 kW (1,000 × 72) | Calculation | DERIVED |
| NVL72 total rack power | ~120 kW | NVIDIA GTC 2024 | CONFIRMED |

### Memory Totals

| Spec | Value | Status |
|------|-------|--------|
| NVL72 total HBM | ~6.912 TB (192 × 72 / 1024) | DERIVED |
| NVL72 total bandwidth | 576.0 TB/s (8 × 72) | DERIVED |

### Inference Benchmark

| Spec | Value | Source | Status |
|------|-------|--------|--------|
| GB200 NVL72 throughput | 1.4M tokens/sec (200B, FP4, 128K) | NVIDIA GTC 2024 | CONFIRMED |

### UNVERIFIED

| Spec | Note |
|------|------|
| B200 FP8 TFLOPS | Never stated by NVIDIA — derived from FP4/FP8 ratio: ~2,500 TFLOPS |
| TDP 1,000W | Widely reported, but hard to find on NVIDIA official spec page |
| HBM bandwidth 8 TB/s | Stated in keynote, not on a spec sheet |

---

## 3. Rubin — B300

**Verification Status**: "2X" claims only — NO specific numbers confirmed

### What NVIDIA Confirmed (GTC 2025)

| Spec | Value | Source | Status |
|------|-------|--------|--------|
| Architecture announced | GTC 2025 | NVIDIA GTC 2025 | CONFIRMED |
| FP4 compute vs Blackwell | "2X" | NVIDIA GTC 2025 | CONFIRMED (claim only) |
| Memory bandwidth vs Blackwell | "2X" | NVIDIA GTC 2025 | CONFIRMED (claim only) |
| Rubin NVL72 | 72 GPUs, ships after Blackwell | NVIDIA GTC 2025 | CONFIRMED |

### Derived Estimates (from "2X" claims — NOT confirmed)

| Spec | Estimate | Note |
|------|----------|------|
| FP4 POPS (per GPU) | ~20,000 POPS | 2 × 10,000 (B200) |
| HBM bandwidth (per GPU) | ~16 TB/s | 2 × 8 (B200) |
| HBM type | HBM4? | Expected but not confirmed |
| HBM capacity (per GPU) | ~256 GB? | HBM4 generation — not stated |
| TDP (per GPU) | ~1,200W? | Estimated |
| NVL72 GPU-only power | ~86.4 kW? | 1,200 × 72 — estimated |
| NVL72 total rack power | ~144 kW? | × 1.2 overhead — estimated |

> **WARNING**: These are DERIVED from NVIDIA's "2X" marketing claims.
> No independently verified specifications exist for Rubin B300.

---

## 4. Cross-Generation Comparison

### Confirmed Data

| Spec | H100 SXM5 | B200 | B300 (Rubin) |
|------|-----------|------|--------------|
| **FP4 POPS (per chip)** | 3,958 POPS | 10,000 POPS | ~20,000 POPS (claim) |
| **HBM capacity (per GPU)** | 80 GB | 192 GB | ~256 GB? (claim) |
| **HBM bandwidth (per GPU)** | 3.35 TB/s | 8 TB/s | ~16 TB/s? (claim) |
| **TDP (per GPU)** | 700 W | 1,000 W | ~1,200W? (unverified) |

### Memory-Bandwidth Improvement

| Transition | Bandwidth/Chip Improvement |
|------------|--------------------------|
| Hopper → Blackwell | 2.4X (3.35 → 8.00 TB/s) |
| Blackwell → Rubin | 2.0X (8.00 → ~16.00 TB/s) — claim |
| Hopper → Blackwell (total) | 2.4X (241 → 576 TB/s) |

### Key Insight

> **POPS improvement (compute) >> Real-world TPS improvement (throughput)**
>
> - B200 FP4 POPS is 2.5X H100 (3,958 → 10,000)
> - B200 HBM bandwidth is 2.4X H100 (3.35 → 8.00 TB/s)
> - For large models, throughput is **memory-bandwidth limited**, not compute limited
> - Therefore actual TPS improvement is ~2-3X per generation
> - This matches NVIDIA's own GTC demo numbers and the inference economics chart

---

## 5. Important Notes

### TFLOPS vs POPS — NVIDIA's Unit Switching

NVIDIA uses different units across generations:

- **H100**: Reports in **TFLOPS** (e.g., "989 TFLOPS FP8")
- **B200**: Reports in **PFLOPS POPS** (e.g., "10 PFLOPS FP4")

POPS includes sparsity acceleration (2:4 sparsity = 4X density).
TFLOPS is usually reported without sparsity (dense).

**Direct TFLOPS comparison across generations is misleading** unless you normalize for sparsity assumptions.

### Sparsity Explained

- 2:2 sparsity = half of weights are zero → 2X throughput
- 2:4 sparsity = quarter of weights are zero → 4X throughput
- FP4 uses 2:4 sparsity → POPS = 4X TFLOPS-equivalent

### Memory Wall

The gap between peak POPS claims and real-world TPS is caused by the memory wall:

1. **POPS** = peak theoretical (with sparsity acceleration)
2. **Memory bandwidth** = the real bottleneck for large models
3. **KV cache** = the real bottleneck for concurrent users

For a 200B parameter model:
- Compute is NOT the bottleneck (HBM bandwidth limits throughput)
- KV cache per user is the hard constraint for concurrent sessions

---

## 6. Sources

| Source | URL/Event | Date |
|--------|-----------|------|
| H100 spec sheet | NVIDIA official | GTC 2023 |
| B200 keynote | NVIDIA GTC 2024 (Jensen Huang) | Mar 2024 |
| GB200 NVL72 benchmark | NVIDIA GTC 2024 | Mar 2024 |
| Rubin announcement | NVIDIA GTC 2025 | 2025 |
| B200 TDP | Multiple sources (widely reported) | 2024 |
| Process nodes | AnandTech (secondary source) | 2024 |
