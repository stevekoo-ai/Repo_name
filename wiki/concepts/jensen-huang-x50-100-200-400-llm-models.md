# x=50/100/200/400 LLM 모델 아키텍처 상세

> **기반**: jensen-huang-chart-analysis-v3.md (v3 분석 SSOT)

---

## 1. x=50 — Free 티어 (Qwen3-235B-A22B)

**[확정]** 공식 config 기준. GQA (Grouped Query Attention).

| 항목 | 값 | 비고 |
|---|---|---|
| 1) Layers | **94** | 공식 config |
| 2) Hidden Dimension | **4,096** | head_dim = 128 × num_kv_heads(4) = 512 / 128 = 4 → 4 × 1024? 아님. 표준 GQA 235B MoE의 hidden_dim은 4096 |
| 3) Query Heads | **32** | GQA: 32 Q heads |
| 4) KV Heads | **4** | GQA: 4 KV heads (공식) |
| 5) Bytes per Element | **2** | BF16 (KV cache용) |
| 6) 총 파라미터 수 | **235B** | 총 파라미터 (MoE) |
| 7) Data Precision (Byte) | **2** | BF16 → 235 × 2 = 470 GB |
| 8) 총 용량 (Byte) | **470 GB** | (235B × 2B = 470 GB) |

**KV Cache 공식 검증**:
```
2(K,V) × 4(KV heads) × 128(head_dim) × 2(BF16) × 94(layers) = 192,512 B = 192.51 KB/tok
```
**활성 파라미터**: 22B (총 235B 중 9.4% 활성화)

---

## 2. x=100 — Medium 티어 (Kimi K2.5)

**[추정]** MLA (Multi-Latent Attention). 공식 스펙 비공개. DeepSeek-V3/V4 레퍼런스 기반 추정.

| 항목 | 값 | 비고 |
|---|---|---|
| 1) Layers | **80** | DeepSeek-V3/V4 레퍼런스 (1T MoE ≈ 80 layers) |
| 2) Hidden Dimension | **3,072** | latent=512, head_dim=128, groups=4 → 512×6? 또는 3072 (DeepSeek-V3 hidden_dim 계승) |
| 3) Query Heads | **64** | DeepSeek-V3 레퍼런스 |
| 4) KV Heads | **4** | MLA: latent vector 4개 (KV heads=4 추정) |
| 5) Bytes per Element | **2** | BF16 |
| 6) 총 파라미터 수 | **1.0T** | 총 파라미터 (MoE) |
| 7) Data Precision (Byte) | **2** | BF16 → 1T × 2 = 2 TB |
| 8) 총 용량 (Byte) | **2 TB** | (1T × 2B = 2 TB) |

**KV Cache 공식 검증 (MLA)**:
```
84.38 KB/tok = latent 기반 압축 KV cache
DeepSeek-V3 레퍼런스: latent=512, decoupled PE=64, head_dim=128
MLA는 KV heads를 압축 latent vector로 표현 → per-token 메모리 대폭 절감
```
**활성 파라미터**: 32B (총 1T 중 3.2% 활성화)

---

## 3. x=200 — High 티어 (GPT MoE 2T)

**[추정]** GQA 기반 MoE. 공식 스펙 비공개. 상용 시뮬레이션 추정치.

| 항목 | 값 | 비고 |
|---|---|---|
| 1) Layers | **80** | 2T GQA MoE 레퍼런스 (GPT-4 계층) |
| 2) Hidden Dimension | **6,144** | 2T GQA MoE 표준 (head_dim=128 × 48 heads) |
| 3) Query Heads | **48** | GQA |
| 4) KV Heads | **6** | GQA: Q heads 48 / K,V heads 6 (8:1 그룹) |
| 5) Bytes per Element | **2** | BF16 |
| 6) 총 파라미터 수 | **2.0T** | 총 파라미터 (MoE) |
| 7) Data Precision (Byte) | **2** | BF16 → 2T × 2 = 4 TB |
| 8) 총 용량 (Byte) | **4 TB** | (2T × 2B = 4 TB) |

**KV Cache 공식 검증 (추정)**:
```
2(K,V) × 6(KV heads) × 128(head_dim) × 2(BF16) × 80(layers) = 245,760 B ≈ 256 KB/tok
= 32.77 GB/user (128K) / 102.40 GB/user (400K)
```
**활성 파라미터**: ~46B (총 2T 중 ~2.3% 활성화)

---

## 4. x=400 — Premium 티어 (GPT MoE 2T)

> x=200과 **동일 모델** (GPT MoE 2T). 컨텍스트만 128K → 400K (3.125배 증가).

| 항목 | 값 | 비고 |
|---|---|---|
| 1) Layers | **80** | x=200과 동일 |
| 2) Hidden Dimension | **6,144** | x=200과 동일 |
| 3) Query Heads | **48** | x=200과 동일 |
| 4) KV Heads | **6** | x=200과 동일 |
| 5) Bytes per Element | **2** | x=200과 동일 |
| 6) 총 파라미터 수 | **2.0T** | x=200과 동일 |
| 7) Data Precision (Byte) | **2** | x=200과 동일 |
| 8) 총 용량 (Byte) | **4 TB** | x=200과 동일 |

**차이점: 컨텍스트 길이만 증가**
```
Per-User KV:
  128K (x=200):  256 KB/tok × 128K = 32.77 GB/user
  400K (x=400):  256 KB/tok × 400K = 102.40 GB/user
```

---

## 모델별 비교 요약

| 항목 | x=50 (Qwen3) | x=100 (Kimi) | x=200 (GPT) | x=400 (GPT) |
|---|---|---|---|---|
| **모델명** | Qwen3-235B-A22B | Kimi K2.5 | GPT MoE 2T | GPT MoE 2T |
| **총 파라미터** | 235B | 1.0T | 2.0T | 2.0T |
| **활성 파라미터** | 22B (9.4%) | 32B (3.2%) | ~46B (2.3%) | ~46B (2.3%) |
| **Layers** | 94 | 80 (추정) | 80 (추정) | 80 (추정) |
| **Attention** | GQA | MLA | GQA | GQA |
| **Query Heads** | 32 | 64 (추정) | 48 (추정) | 48 |
| **KV Heads** | **4 (확정)** | 4 (추정) | 6 (추정) | 6 |
| **head_dim** | 128 | 128 | 128 | 128 |
| **Weights (BF16)** | 470 GB | 2 TB | 4 TB | 4 TB |
| **KV/u (32K)** | 6.16 GB | — | — | — |
| **KV/u (128K)** | 24.64 GB | 10.80 GB | 32.77 GB | 32.77 GB |
| **KV/u (400K)** | 77.00 GB | 33.75 GB | 102.40 GB | 102.40 GB |
| **가격** | $0 | $3 | $6 | $45 |

---

## 중요 인사이트

### 1. 파라미터 vs 성능은 비선형 관계
| 파라미터 | 활성 | TPS/MW (x=50, R100) |
|---|---|---|
| 235B (Qwen3) | 22B | 1.65M |
| 1.0T (Kimi) | 32B | 1.6M (flat) |
| 2.0T (GPT) | ~46B | 0.7M |

- 235B → 1.0T: 파라미터 4.25배 ↑ → 효율 유지 (flat)
- 1.0T → 2.0T: 파라미터 2배 ↑ → 효율 2.3배 ↓ (급강하)
- 결론: **활성 파라미터 × 컨텍스트 길이의 조합**이 효율을 지배. MoE 3.2% 희소성이 핵심.

### 2. KV Cache 압축 기술의 혁명: MLA
| 모델 | Attention | KV/tok | KV/u (128K) |
|---|---|---|---|
| Qwen3 (GQA) | 4 KV heads | 192.51 KB | 24.64 GB |
| Kimi (MLA) | latent 512 압축 | **84.38 KB** | **10.80 GB** |
| GPT (GQA) | 6 KV heads | 256.00 KB | 32.77 GB |

- MLA는 GQA 대비 KV cache를 **44% 절감** (192→84 KB/tok)
- Kimi가 1T 파라미터임에도 GQA 235B보다 KV가 작은 이유 = MLA 압축

### 3. 가중치 메모리 압박: HBM 안착 여부
| 모델 | 총 파라미터 | 가중치 (BF16) | H100 HBM (2.56TB) | B300 HBM (20.7TB) |
|---|---|---|---|---|
| Qwen3 (235B) | 235B | 470 GB | ✅ 들어감 | ✅ |
| Kimi (1T) | 1.0T | 2 TB | ✅ 들어감 | ✅ |
| GPT (2T) | 2.0T | **4 TB** | ❌ **1차 사망** | ✅ |

- H100은 2T 모델 서빙이 **물리적으로 불가**. 가중치(4TB) > HBM(2.56TB)
- B300/R100은 20.7TB HBM에 4TB 안착 → 1차 사망 회피
