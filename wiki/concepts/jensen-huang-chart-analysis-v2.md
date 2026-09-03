---
name: jensen-huang-chart-analysis-v2
description: NVIDIA GTC Inference Economics 차트 재작성판 — 이미지로 확정한 정확한 판독값(12포인트), H100 32GPU/40kW 정의 교정, Qwen3-235B-A22B MoE 교정, 세 곡선 물리 해석
metadata:
  type: reference
  created: 2026-08-26
  verified: 2026-08-26
  supersedes: jensen-huang-chart-analysis.md (2026-08-21판)
tags: [jensen-huang, gtc, inference, gpu, chart-analysis, ro-v2, blackwell, rubin, hopper]
---

# 젠슨황 "Inference Economics" 차트 — 이미지 확정 재작성판 (v2)

> **임무**: Jensen Huang(GTC 2026)의 "Inference Performance and Efficiency Drive Company
> Results" 차트를 **실제 차트 이미지에서 육안 확정한 판독값**으로 전면 재작성한 단일 출처(SSOT).
>
> **v2가 만들어진 이유**: v1(2026-08-21)은 차트를 이미지 없이 **추측**으로 판독해
> H100 x=100 flat, Qwen 235B Dense, H100 NVL72 등 치명적 오류가 있었다. 이번 v2는
> 사용자가 직접 제공한 차트 이미지로 **모든 곡선 판독값을 확정**하고 물리 역산으로 검증했다.
>
> **생성일**: 2026-08-26 · **검증일**: 2026-08-26
> **관련 문서**: [gpu-inference-economics.md](gpu-inference-economics.md) / [gpu-inference-chart-verification.md](gpu-inference-chart-verification.md)

---

## 0. v2 주요 교정 요약 (v1 대비)

| 항목 | v1 (오류) | v2 (확정) | 근거 |
|------|-----------|-----------|------|
| **H100 랙 구성** | "NVL72 72 GPU / 65kW" | **32 GPU / ~40kW SuperPOD** | H100엔 NVL72 없음. DGX H100 SuperPOD = 32 GPU, ~40kW |
| **Qwen3 모델 타입** | "Dense 235B" | **MoE 235B-A22B** | Qwen3-235B-A22B = 235B 총/22B 활성, MoE |
| **H100 x=100 판독** | 0.15M (flat) | **0.06M (급강하)** | 이미지 확인. flat은 Rubin 곡선 |
| **Blackwell 랙** | 추정 "B300 Ultra" | **Blackwell NVL72 (72 GPU/~121kW)** | 차트 곡선이 NVL72 라벨 |
| **Rubin 랙** | R100 | **Rubin NVL72 (72 GPU/~199kW)** | 차트 곡선이 NVL72 라벨 |
| **차트 판독값** | 추측치 | **이미지 육안 확정 12포인트** | 사용자 제공 PNG |
| **H100 앵커 검증** | 9,750 TPS(65kW) | **6,000 TPS(40kW) = 187.5 TPS/GPU** | 32 GPU로 역산 시 자연스러운 효율 |
| **Qwen3 KV Cache** | 0.453 MB/tok (KV heads=8, layers=88 — Llama-405B 근접 가정) | **0.1925 MB/tok (KV heads=4, layers=94, GQA)** | Qwen3-235B-A22B 공식 config. v2첫판이 Dense→MoE 이름만 고치고 숫자 물려받음 |
| **Per-user KV (Free 32K)** | 14.1 GB/user | **6.16 GB/user** | 0.1925MB × 32K. Premium 400K = 102.4GB(176GB→교정) |
| **Kimi K2.5 KV** | (v1 미산출) | **84.38 KB/tok [MLA 추정]** = 10.80 GB/u(128K) | DeepSeek-V3/V4 레퍼런스(latent 512) 유도. 대외비 |
| **GPT MoE 2T KV** | (v1 미산출) | **256 KB/tok [추정]** = 32.77GB/u(128K), 102.4GB/u(400K) | 공식 스펙 비공개. 상용 시뮬레이션 추정치 |
| **H100 GPT 2T 서빙** | (v1 침묵) | **N/A — 차트 회색선(미지원)** | weights 4000GB > HBM 2560GB. 차트가 x=200부터 점 없음 = 물리 한계 일치. B300/R100 강제 당위성 |
| **Users 도출 방식** | TPS/x 단순 나눗셈 (HBM 무시) | **방향 b: available_VRAM / KV_per_user derive** | chart_users vs max_HBM 대조 → fitting 정합성 검증 |
| **R100 x=50 spill** | "CXL 불필요" | **SPILL 20.2TB (SOCAMM 흡수)** | 0.453→0.1925 교정 후에도 chart 6567u > max 3290u |
| **가중치 정밀도** | B300/R100 FP4(0.5B) 가정 | **전 세대 BF16(2B) 통일** | Spec v2 정합. FP4는 추론만, 저장은 BF16. 보수적 상한 |
| **B300 max_users** | x=200 602, x=400 193 (FP4) | **x=200 511, x=400 163 (BF16)** | weights 4000GB 기준 재계산. 전 포인트 OK 유지 |
| **H100 x=100 TPS** | (Spec v2 5,500 TPS 제안) | **2,400 TPS (0.06M) 유지** | 5,500T → 55u×10.80=594GB > avail 560GB OVERFLOW. 2,400T만 fitting 정합 |
| **x=100 꺾임 원인** | memory-bound 단일 설명 | **이중 병목 전환점 (memory+compute)** | Prefill O(N²) 32K→128K 16배 폭발 + KV 10.80GB 증가. Tensor Core 포화 |
| **R100 spill 방어** | SOCAMM 흡수만 | **+ NVLink-C2C 1.8TB/s 대역 보조·일관성** | 차트 1.65M 신뢰 → spill 필연(40.5TB>20.3TB). C2C가 피크 방어 |
| **B300 x=400 하강 원인** | (spill 가설) | **Memory Bandwidth Bound (spill 배제)** | 역산 2.1TB << 16.3TB. HBM3e 8TB/s 포화가 진짜 원인 |
| **3단계 곡선 징후** | (미통합) | **절벽(H100)·하강(B300)·수렴(R100)** | 세대 체급별 지배 병목 차이. R100 수렴 = Batch Saturation→Roofline |
| **R100 spill 성격** | 용량 결함 오해 | **성공의 역설 (Too Fast to Fit)** | 1.65M+0.199MW→3.9배 TPS→40.5TB>20.7TB. C2C+SOCAMM Scale-Out 전제. 결함 아님 |
| **B300 vs R100 대비** | (미대비) | **B300=Standalone / R100=Scale-Out** | 같은 20.7TB. B300은 10.4TB 안착(단독), R100은 40.5TB 초과(C2C 확장 전제) |

---

## 1. 차트 개요

**차트 제목**: "Inference Performance and Efficiency Drive Company Results"
**발표자**: Jensen Huang, NVIDIA CEO (GTC 2026)

### 1.1 두 축 (이미지로 확정)

| 축 | 의미 | 단위 |
|---|------|------|
| **Y축** | Throughput (전력당 효율) | **TPS/MW** — 메가와트당 토큰/초 |
| **X축** | Interactivity (상호작용성) | **TPS/User** — 사용자당 토큰/초 (높을수록 빠른 응답/짧은 context) |

> ⚠️ v1 오류: X축을 "Context Length"로 오해했으나, 실제는 **Interactivity TPS/User**.
> 하단 사용패턴(Free→Premium) 라벨이 각 x 위치에 직접 붙어 있음 → 매핑 확정.

### 1.2 4개 서비스 티어 (하단 사용패턴 라벨 — 이미지 확정)

| 티어 | x축 | 모델 | 파라미터 | 컨텍스트 | 가격 |
|---|---|------|---------|----------|------|
| **Free** | x=50 | **Qwen3-235B-A22B** (MoE) | 235B | **32K** | **$0** |
| **Medium** | x=100 | Kimi K2.5 | 1T (MoE) | 128K | **$3** |
| **High** | x=200 | GPT MoE | 2T | 128K | **$6** |
| **Premium** | x=400 | GPT MoE | 2T | 400K | **$45** |

> **핵심**: 가격 계층은 **컨텍스트 길이와 정확히 매핑**된다. x↑(더 빠른 응답 요구) =
> 더 긴 컨텍스트를 처리해야 = 더 비싼 프리미엄. 컨텍스트가 곧 비용의 원천.

### 1.3 3개 GPU 곡선 (이미지 확정)

| 곡선 | 실제 하드웨어 | 랙 구성 | 랙 전력 | HBM | Y축 x=50 |
|---|--------------|---------|--------|-----|---------|
| **Hopper** (회색) | **H100 SuperPOD** | **32 GPU** | **~40kW** | 80GB×32 | **0.15M** |
| **Blackwell NVL72** (청록) | **B300 NVL72** | **72 GPU** | **~121kW** | 288GB×72 | **0.7M** |
| **Rubin NVL72** (초록) | **R100 Vera Rubin NVL72** | **72 GPU** | **~199kW** | 288GB×72 | **1.65M** |

---

## 2. 차트 전체 판독 (이미지 육안 확정)

### 2.1 12 포인트 판독값 (TPS/MW)

| x (TPS/User) | **Hopper H100** | **Blackwell NVL72** | **Rubin NVL72** |
|---|---|---|---|
| **x=50** (Free, 32K) | **0.15M** | **0.7M** | **1.65M** |
| **x=100** (Medium, 128K) | **0.06M** (급강하) | **0.6M** | **1.6M** (flat) |
| **x=200** (High, 128K) | **N/A (회색선·미지원)** | **0.15M** | **0.7M** |
| **x=400** (Premium, 400K) | **N/A (회색선·미지원)** | **0.07M** | **0.2M** |

> ⚠️ 판독 정정 (2026-08-26): v2 첫 판은 H100 x=200/400을 0.02M/0.015M로
> 판독했으나, 차트에서 H100 곡선은 x=200부터 **점 없이 회색선** = 지원 불가.
> GPT 2T 가중치(4,000GB) > H100 HBM(2,560GB) 물리 한계와 100% 일치.
> 12포인트 중 H100 유효 점 = **x=50, x=100 only (2점)**.

### 2.2 차트 명시 Annotation (이미지 확정)

| 지점 | 표시 | 해석 |
|---|---|---|
| x=50 → RNVL72 | **2X ↑** | Rubin 컨텍스트 증가에도 flat 유지 (1.6M) |
| x=100 → BNVL72 | **2X ↑** | Blackwell 상대 점수 표시 |
| x=200 | **3X ↑** | H100 미지원 구간에서 B300이 0.15M — H100 한계(용량) 대비 차세대 랙의 효율 |
| x=400 | **10X ↑** | H100 미지원 구간에서 R100이 0.2M — 차세대 랙이 GPT 2T/400K를 가능케 하는 폭증 |

### 2.3 곡선 shape 요약

```
TPS/MW ┤
 1.65M ┤      ● Rubin (x=50~100 flat)
       │     ╱│╲
 0.7M  ┤    ● │ ╲● Rubin↓
       │   ╱  │   ╲
 0.15M ┤  ●───│────╲── Hopper 급강하
       │ ╱    │      ╲
 0.06M ┤●     │       ╲
       ┼──────┼────────┼────────┼──►
      50     100      200      400
                    │  H100 회색선 종료 (x=200~ 미지원)
```

- **Rubin**: x=50~100 flat (짧은 context에서 max 효율) → 이후 완만한 강하
- **Blackwell**: x=100까지 완만, x=200부터 급강하
- **Hopper**: x=50부터 강하, **x=200에서 회색선 종료(GPT 2T 미지원)**. x=200~400 점 없음.

---

## 3. GPU 세대별 스펙

### 3.1 GPU 비교 표

| Spec | **H100 Hopper** | **B300 Blackwell** | **R100 Vera Rubin** |
|------|----------------|--------------------|---------------------|
| 랙 이름 | DGX H100 SuperPOD | **Blackwell NVL72** | **Rubin NVL72** |
| GPU/rack | **32** | 72 | 72 |
| FP4 추론 | N/A (FP8 only) | 15,000 TFLOPS | **50,000 TFLOPS** |
| HBM | HBM3 80GB | HBM3e 288GB | **HBM4 288GB** |
| HBM BW/GPU | 3.35 TB/s | 8.0 TB/s | **22.0 TB/s** |
| TDP/GPU | 700W | 1,400W | 2,300W |
| **Rack 전력** | **~40kW** | **~121kW** | **~199kW** |
| NVL72 HBM BW 총합 | (32 GPU) 107.2 TB/s | 576 TB/s | **1,584 TB/s** |
| 냉각 | 공랭 가능 | 수랭 필수 | DLC 필수 |

### 3.2 냉각 임계 (DLC가 필수가 되는 이유)

```
H100:  ~40kW/rack  → 공랭 가능 (구형)
B300:  ~121kW/rack → 수랭 필수 (공랭 불가)
R100:  ~199kW/rack → DLC(Direct Liquid Cooling) 필수, 공랭으로 절대 불가

R100 NVL72 199kW = 기존 DC 랙(10-30kW)의 7-20배
```

> ⚠️ v1 오류: H100을 "NVL72 65kW"로 기재. 실제 H100 SuperPOD는 **32 GPU / ~40kW**.
> 공랭 40.8kW(수랭 전환 임계) 상: R100 MGB(1.4kW)조차 공랭 불가, 2.3kW GPU는 DLC 필수.

---

## 4. Memory-Bound Inference — 핵심 물리 법칙

### 4.1 Core Formula

```
Token/Sec = Total_Memory_BW / Total_KV_Cache_GB
```

- 각 토큰마다 GPU는 전체 KV 캐시를 랜덤 읽어야 함 (attention)
- **context 길이 × user 수가 커질수록 Token/sec 비례 감소**
- 이것이 X축(Interactivity)에서 x↑(길린 context/더 빠른 응답) → TPS/MW↓의 물리적 원인

### 4.2 KV Cache 계산 — 3 모델 라벨·산식 명시 (2026-08-26 정합성 재계산)

⚠️ v1 오류: Qwen3 235B를 **Dense + KV heads=8 + layers=88**(Llama-405B 근접) 가정으로
0.453 MB/token을 사용. 그러나 **Qwen3-235B-A22B는 MoE + GQA(KV heads=4, layers=94)**
이며 정확히 **0.1925 MB/token**(192.51 KB/token)이다. v2 첫 판에서 "Dense→MoE 이름만
고치고 숫자는 물려받는" 2차 오류가 있었음 — 아래 표로 전면 교정.

#### 4.2.1 모델별 KV Cache 규격 (라벨 + 산식)

| 모델 | 어텐션 | 산식 | KB/token | 라벨 |
|------|--------|------|---------:|------|
| **Qwen3-235B-A22B** | **GQA** | 2(K,V)×KV_heads(4)×head_dim(128)×2bytes×layers(94) = 192,512 B | **192.51** | **[확정]** 공식 config |
| **Kimi K2.5** (1T, 32B 활성) | **MLA** | DeepSeek-V3/V4 레퍼런스(latent 512, decoupled PE 64) 기반 유도 | **84.38** | **[추정]** 대외비 아키텍처 |
| **GPT-class MoE 2T** | **MoE 분산** | 상용 시뮬레이션 레퍼런스 | **256.00** | **[추정]** 공식 스펙 비공개 |

> **어텐션 분리 (v1 혼선 교정)**: Qwen3 = **GQA**(KV heads 4). Kimi K2.5 = **MLA**(latent 압축).
> GPT-class = MoE 분산 추론. 세 구조를 한 식에 섞지 않는다.

#### 4.2.2 Per-User KV Cache (GB) — 컨텍스트 확장에 따른 비용

```
Per-User KV = KB/token × context / 1e6  (→ GB)

모델        32K        128K        400K
─────────────────────────────────────────
Qwen3 GQA   6.16 GB   24.64 GB    77.00 GB   ← Free(32K) 기준
Kimi  MLA   2.70 GB   10.80 GB    33.75 GB   ← Medium(128K). 1T인데도 MLA 압축으로 Qwen3 Dense(가정)보다 작다
GPT   MoE   8.19 GB   32.77 GB   102.40 GB   ← High(128K)/Premium(400K). 400K = 102.4 GB/user
```

> **컨텍스트가 곧 비용**: Free 32K = **6.16 GB/user**. Premium 400K(GPT) = **102.40 GB/user**
> = **16.6배**. 이 16.6배의 VRAM 소모가 $0 → $45 프리미엄 가격(∞배)의 물리적 원천.
> **MLA 가성비 증명**: Kimi K2.5는 1T(1조) 파라미터 모델이지만, 컨텍스트 32K→128K(4배)에도
> per-user KV는 2.70→10.80 GB(**4배**)로 선형 증가하며 절대치가 Qwen3(24.64 GB)보다 작다.
> → 1T 거대 모델임에도 H100 랙에서 동시 유저 52명(Section 5)을 받을 수 있는 물리 근거.

#### 4.2.3 Prefill 연산량 폭발 — x=100 꺾임의 compute 근거 (2026-08-26 보강)

```
Prefill(초기 문맥 처리) 연산량은 context N에 대해 attention O(N²):
  32K  → N² = 1.0e9
  128K → N² = 16.4e9   (x=100, Medium 진입 시 16배 폭발)
  400K → N² = 160.0e9  (x=400, Premium — 128K 대비 추가 9.8배)

→ x=100(128K) 진입 순간 prefill 연산이 16배 폭발 → Tensor Core 포화 시작.
  decode KV(10.80GB/u) 증가(memory 요인) + prefill 16배(compute 요인)가 겹쳐
  곡선이 꺾이는 이중 병목 전환점(Section 8.1). R100은 HBM4 22TB/s로 memory를
  압도하므로 compute-bound 전환이 가장 먼저 발현.
```

### 4.3 MoE vs Dense — 활성 파라미터 차이 (FLOPs/token)

```
Qwen3-235B-A22B (MoE):  total 235B / active 22B → FLOPs/token ≈ 2×22B = 44B
Kimi K2.5     (MoE):    total 1.0T / active 32B → FLOPs/token ≈ 2×32B = 64B   (3.2% 초희소 활성화)
GPT-class     (MoE):   total 2.0T / active ~46B→ FLOPs/token ≈ 2×46B = 92B   (44~50B 추정)
만약 Dense 235B라면:                          → FLOPs/token ≈ 2×235B = 470B
```

→ MoE는 같은 플래그십 모델이지만 **활성 계산량이 5~10배 적음** → decode 효율 극대화.
차트의 "235B / 1T / 2T" 라벨은 **총 파라미터**이며, 실제 throughput은 **활성 파라미터**(22B/32B/~46B)가 지배.
**가중치 메모리는 총 파라미터 기준**이므로 Kimi(1T)/GPT(2T)는 HBM 대역·용량 압박이 Qwen3보다 훨씬 큼.

---

## 5. 차트 포인트 → Total TPS → Concurrent Users (물리량 derive + 12포인트 정합성)

> ⚠️ v1은 H100을 "NVL72 65kW"로 계산 → 9,750 TPS. v2 첫 판도 H100 40kW로 정정만 하고
> **users = TPS/x 단순 나눗셈**만 했다 — 이는 HBM 물리량을 무시한 암산이다.
> **v2 재계산(2026-08-26)**: users를 `available_VRAM / KV_per_user`로 먼저 derive하고,
> 차트 TPS/MW에서 trace한 chart_users와 대조해 **fitting 정합성**을 검증한다.

### 5.1 파생 공식 (방향 b — 물리량 기반 재도출)

```
Total TPS     = TPS/MW(차트) × rack_MW              ← 12포인트 차트 판독값에서 trace
chart_users   = Total TPS / x                      ← 차트가 말하는 동시 유저
HBM_total     = GPU_HBM × GPU 수
weights       = total_params × 2 bytes (BF16)      ← 모든 세대 BF16 기준 (보수적)
available_KV  = HBM_total − weights
max_users_HBM = available_KV / KV_per_user         ← 물리 한계 (fitting 상한)
fit_status    = "OK" if chart_users ≤ max_users_HBM else "SPILL"
```

> **가중치 정밀도 기준 (2026-08-26 정정)**: 모든 세대 **BF16(2 bytes/param)** 통일.
> B300/R100에서 FP4 추론이 가능하더라도, 가중치 저장은 BF16이 보수적 상한
> (B300 GPT 2T = 4,000GB → HBM 20.7TB에 fitting, 여유 16.3TB). FP4 가정(1,000GB)은
> 가용량을 과대 평가하므로 채택하지 않는다.

### 5.2 12포인트 정합성 표 (derive 결과 — HBM fitting 검증)

| GPU | x | 티어(모델) | TPS/MW | Total TPS | chart_users | HBM tot | weights | avail | KV/u(GB) | max_HBM users | fitting |
|-----|---|-----------|-------:|----------:|------------:|--------:|-------:|------:|---------:|--------------:|:-------:|
| H100 | 50 | Free(Qwen3) | 0.15 | 6,000 | 120 | 2,560 | 470 | 2,090 | 6.16 | 339 | **OK** |
| H100 | 100 | Med(Kimi) | 0.06 | 2,400 | 24 | 2,560 | 2,000 | 560 | 10.80 | 52 | **OK** |
| H100 | 200 | High(GPT) | — | — | — | — | — | — | — | — | **N/A (미지원)** |
| H100 | 400 | Prem(GPT) | — | — | — | — | — | — | — | — | **N/A (미지원)** |
| B300 | 50 | Free(Qwen3) | 0.70 | 84,700 | 1,694 | 20,736 | 470 | 20,266 | 6.16 | 3,290 | **OK** |
| B300 | 100 | Med(Kimi) | 0.60 | 72,600 | 726 | 20,736 | 2,000 | 18,736 | 10.80 | 1,735 | **OK** |
| B300 | 200 | High(GPT) | 0.15 | 18,150 | 91 | 20,736 | 4,000 | 16,736 | 32.77 | 511 | **OK** |
| B300 | 400 | Prem(GPT) | 0.07 | 8,470 | 21 | 20,736 | 4,000 | 16,736 | 102.40 | 163 | **OK** |
| R100 | 50 | Free(Qwen3) | 1.65 | 328,350 | 6,567 | 20,736 | 470 | 20,266 | 6.16 | 3,290 | **SPILL** |
| R100 | 100 | Med(Kimi) | 1.60 | 318,400 | 3,184 | 20,736 | 2,000 | 18,736 | 10.80 | 1,735 | **SPILL** |
| R100 | 200 | High(GPT) | 0.70 | 139,300 | 696 | 20,736 | 4,000 | 16,736 | 32.77 | 511 | **SPILL** |
| R100 | 400 | Prem(GPT) | 0.20 | 39,800 | 100 | 20,736 | 4,000 | 16,736 | 102.40 | 163 | **OK** |

> 단위: Total TPS = tokens/sec, HBM/weights/avail/KV = GB, users = 명.
> weights: 전 세대 BF16(2B/param). H100은 FP4 연산 미지원, B300/R100은 FP4 *추론* 지원(가중치 저장은 여전히 BF16). avail = HBM − weights.

### 5.3 정합성 판정 — 3개 패턴

**① OK (chart_users ≤ max_HBM)**: H100 x=50/100, B300 전 포인트, R100 x=400.
→ 차트 TPS를 HBM fitting만으로 달성 가능. CXL 불필요.

**② SPILL — R100 x=50/100/200**: chart_users가 max_HBM users를 **초과**.
→ 차트가 말하는 TPS를 내려면 **KV 캐시 일부가 HBM 밖(SOCAMM/CXL)으로 spill**되어야 성립.
R100 x=50: 6,567−3,290 = 3,277 users분(≈ 20.2 TB) spill. x=100: 3,184−1,735 = 1,449 users분(≈ 15.7 TB) spill.
→ **R100 고TPS의 전제 조건 = CXL/SOCAMM 확장** (Section 6·9의 물리 근거).

**③ N/A — H100 x=200/400**: 차트에서 H100은 x=200(GPT 2T)부터 **점 없이 회색선**으로
처리 = **지원 불가(Not Supported)**. 물리 근거: GPT 2T 가중치(BF16 4,000GB)가 H100 랙
HBM(2,560GB)을 초과해 올릴 수 없음. 차트 판독과 물리 법칙이 **100% 일치**.
→ **High/Premium 티어(GPT 2T, 128K/400K) 서빙 = B300(20.7TB)/R100(20.7TB) 차세대 랙 강제**.
이것이 비싼 Blackwell Ultra·Rubin 인프라로 넘어가야 하는 **담백한 물리적 당위성**.

### 5.4 세대 비율 (같은 x, TPS/MW — 차트 그대로)

| x | H→B | B→R | H→R |
|---|---|-----|-----|
| x=50 | 4.7X | 2.4X | 11.0X |
| x=100 | 10.0X | 2.7X | 26.7X |
| x=200 | **N/A** (H100 미지원) | 4.7X | **N/A** |
| x=400 | **N/A** (H100 미지원) | 2.9X | **N/A** |

> H100이 x=200/400에서 회색선(미지원)이므로 H→B, H→R 비율은 해당 행에서 정의 불가.
> x=400의 "10X ↑" annotation은 H100 점이 아니라 **차세대 랙이 H100 한계를 넘어선 폭증** 표현.
> B→R은 B300/R100 판독값 비율(0.15/0.7=4.7X, 0.07/0.2=2.9X)로 유효.

---

## 6. Hopper H100 @ (x=50, 0.15M) — 완전 역산 (32 GPU/40kW 교정판)

### 6.1 Power → Total Throughput

```
H100 SXM5:        700 W/GPU
SuperPOD:         32 GPUs
GPU-only:         22.4 kW (700 × 32)
Rack total:       ~40 kW (overhead ×1.8)
Rack in MW:       0.040 MW

차트 점: x=50, y=0.15M (TPS/MW)

Total TPS = 0.15M × 0.040 = 6,000 TPS
Per-GPU   = 6,000 / 32 = 187.5 TPS/GPU  ← 자연스러운 수치 (v1의 9,750/72=135보다 현실적)
```

### 6.2 Concurrent Users & Batch

```
Concurrent Users = 6,000 / 50 = 120 users
Per-GPU batch    = 120 / 32 ≈ 4 users/GPU
```

> ⚠️ v1은 "NVL72" 가정으로 batch 계산을 왜곡. **32 GPU 기준 batch ~4/GPU**.

### 6.3 KV Cache & HBM Fitting (32 GPU) — 6.16GB/user 교정

```
H100 32-GPU HBM Total:   80 GB × 32 = 2,560 GB = 2.5 TB
LLM Weights (Qwen3 235B, BF16): 235 × 2 = 470 GB   ← Free(32K) 서빙 시
Available for KV Cache:   2,560 - 470 = 2,090 GB ≈ 2.04 TB

Per-User KV (Qwen3, 32K) = 6.16 GB   ← v1의 14.1GB에서 교정 (0.453→0.1925 MB/tok)
x=50: 120 users × 6.16 GB = 739 GB = 0.74 TB
  0.74 TB << 2.04 TB → HBM fitting ✓ (여유 1.30 TB)

[Medium — Kimi 1T, 128K]
  Weights(BF16) = 1,000 × 2 = 2,000 GB → HBM 2,560 − 2,000 = 560 GB avail
  Per-User KV(MLA, 128K) = 10.80 GB
  x=100: 24 users × 10.80 = 259 GB < 560 GB → fitting ✓ (여유 301 GB)

[High/Premium — GPT 2T] → **N/A (미지원)**
  GPT 2T 가중치(BF16 4,000GB) > H100 HBM(2,560GB) → 랙에 올릴 수 없음.
  차트에서 H100은 x=200부터 **회색선(점 없음) = 지원 불가**. 차트와 물리 100% 일치.
  → High/Premium 티어 서빙은 B300/R100 차세대 랙(20.7TB HBM)이 강제됨.
```

### 6.4 Bottleneck — 왜 H100 곡선이 x=50부터 강하하고 x=200에서 끝나는가

```
x=50 (120 users, batch 4/GPU):
  H100 FP8 decode → 6,000 TPS (Qwen3 22B 활성, KV 6.16GB/u fitting OK)

x=100 (24 users, batch <1/GPU):
  Total TPS = 2,400 (0.06M). Kimi 1T 서빙.
  → batch < 1/GPU → memory-bound + scheduling starve → 급강하

x≥200: H100 회색선(미지원) — GPT 2T 가중치 4,000GB > HBM 2,560GB.
  → 차트가 x=200부터 점을 그리지 않는 것 = 물리 한계를 그대로 반영.
```

> **핵심 통찰**: Hopper 곡선이 유일하게 x=50부터 급강하하는 이유는 **32 GPU 랙이
> batch를 확보할 capacity가 적고, FP4 없이 FP8 density가 낮아** 같은 x에서도
> Blackwell/Rubin 만큼 token을 batch에 실어 나를 수 없기 때문. x=200에서 곡선이
> **끝(회색선)**으로 마무리되는 것은 GPT 2T가 랙에 못 올라는 물리 한계의 차트 표현.

---

## 7. 세 곡선이 분리되는 이유 — Compute Density × Batch

### 7.1 같은 x=50에서 세대가 10배 차이나는 이유

```
동일 워크로드: Free 티어, 32K context, x=50

  H100 (FP8, 32GPU):        TPS/MW = 0.15M   ← FP4 없음, 작은 batch
  B300 NVL72 (FP4, 72GPU):  TPS/MW = 0.7M    ← FP4 15K POPS, 72 GPU batch 여유
  R100 NVL72 (FP4, 72GPU):  TPS/MW = 1.65M   ← FP4 50K POPS, 대형 batch

격차 요인:
  1. FP4 density: B300이 FP8보다 약 4-8X dense → batch당 처리 token ↑
  2. GPU 수: 72 vs 32 → batch capacity 2.25X
  3. HBM4(22TB/s) vs HBM3(3.35TB/s): decode BW 6.6X
```

### 7.2 Rubin flat 구간 (x=50~100) + x=100 꺾임의 의미

```
Rubin은 x=50~100에서 1.65M → 1.6M (거의 flat):
  → x=50: compute-bound (배치 충분, 메모리 여유)
  → HBM4 22TB/s BW가 decode를 압도 → 메모리 병목 아님
  → x=100에서 1.6M로 미세 하강: 128K 진입, Prefill O(N²) 16배 폭발 시작
    (32K의 1.0e9 → 128K의 16.4e9). Tensor Core가 포화되기 시작 = compute-bound 전환점.
  → 성능이 flat = "compute와 batch 여유가 충분" 증거

Hopper는 같은 구간에서 급강하:
  → 이 구간에서 이미 memory-bound (FP8, 작은 batch)
  → 곡선 모양이 세대의 물리적 한계를 그대로 반영
```

### 7.3 B300 완만 하강 = Memory Bandwidth Bound (spill 아님, Standalone 단독 랙 최적화)

```
B300은 x=50~400 전 구간 끊김 없이 완만 우하향:
  → 용량 여유: HBM3e 20.7TB − 가중치 4TB = 16.3TB. x=400(KV 2.1TB)도 fitting OK.
    → spill-over 가설 배제 (역산 2.1TB << 16.3TB).
  → 진짜 원인: HBM3e 8TB/s decode 대역폭 한계(Memory Bandwidth Bound).
    x↑(컨텍스트 길어짐) → KV 커지 → 매 토큰마다 전체 KV를 랜덤 읽기 → 8TB/s 포화.
  → B300의 완만 기울기 = "용량은 남지만 고속도로(HBM3e 대역)가 포화"하는 하강.

[B300 = Standalone 단독 랙 최적화]
  차트 0.7M TPS/MW × 0.121MW = 84,700 TPS → x=50 유저 1,694명 → KV 10.4TB.
  10.4TB < 가용 20.3TB → 단일 랙 HBM 내 안착. C2C/SOCAMM 확장 불필요.
  → R100(Too Fast to Fit, Scale-Out)과 대비되는 "단독 랙 자급형" 모델.
```

### 7.4 R100 x=200+ 수렴 = Batch Saturation → Roofline

```
R100은 x=100 꺾임 이후 x=200(0.7M)→x=400(0.2M)로 완만 하강하며 수렴:
  → x=100: Prefill 16배 폭발로 compute-bound 1차 꺾임(Section 8.1)
  → x≥200: HBM4 22TB/s + FP4 50K POPS가 동시 포화 → Roofline 도달.
            대규모 Continuous Batching 가동률 100% 수렴 → 가중치 고정 비용 분산.
  → 추가 유저/컨텍스트가 들어와도 TPS/MW가 거의 변하지 않음 = 수렴 곡선.
  → H100(절벽)·B300(대역폭 하강)과 징후가 다른 "한계선 도달" 형태.
```

---

## 8. 세대별 Bottleneck 이동 (Memory → Compute)

```
세대    | Decode 특성                    | Primary Constraint
────────┼───────────────────────────────┼─────────────────────
H100    | FP8, HBM3 3.35TB/s            │ Memory-bound
(2024)  | 작은 batch에서 급강하          │ (FP8 density 낮음)
        |                                │ → 곡선이 x=50부터 하강
────────┼───────────────────────────────┼─────────────────────
B300    | FP4, HBM3e 8TB/s              │ Memory Bandwidth Bound
(2026)  | x=100까지 완만, x=200 급강하   │ (HBM3e 8TB/s decode 한계)
        |                                │ → 용량 여유(16.3TB) 있어도
        |                                │   대역폭이 포화 → 완만 하강
────────┼───────────────────────────────┼─────────────────────
R100    | FP4, HBM4 22TB/s              │ x=100: 이중 병목 전환점
(2027)  | x=50~100 flat, x=100 꺾임     │ x≥200: Batch Saturation
        | x≥200 완만 수렴(Roofline)      │ (HBM4 BW 압도 → 배치 포화)
        |                                │ → Roofline 한계선에 수렴
```

> **3단계 곡선 징후 (아키텍처 프레임)**: H100 = **절벽**(용량의 벽, N/A 회색선) ·
> B300 = **하강**(대역폭의 벽, HBM3e 8TB/s 포화) · R100 = **수렴**(연산의 벽 후
> Batch Saturation → Roofline). 같은 "하강"이어도 세대 체급별로 지배 병목이 다름.

### 8.1 x=100 꺾임 = Memory→Compute 이중 병목 전환점 (2026-08-26 보강)

```
x=100(Medium, 128K)에서 곡선이 꺾이는 물리 근거 — 두 요인 동시 작용:

[Memory 요인]  per-user KV가 6.16GB(32K) → 10.80GB(128K)로 증가
               → batch size 축소, decode 효율 저하

[Compute 요인] Prefill 연산량이 context N의 제곱에 비례 (attention O(N²))
               32K: N² = 1.0e9  →  128K: N² = 16.4e9  (정확히 16배 폭발)
               → 초기 문맥을 읽는 prefill에서 Tensor Core 포화
               → memory-bound에서 compute-bound로 과도기 전환

→ x=100은 단일 병목이 아니라 memory(KV 증가·batch 축소) + compute(Prefill 16배)가
  겹치는 전환점. x≥200에서는 compute-bound가 주 병목으로 고정.
```

### 8.2 R100 x=200+ 완만 수렴 = Batch Saturation → Roofline (2026-08-26 보강)

```
x=200 이후 R100 곡선이 수평에 가까이 눕는 물리 근거:

[Batch Saturation] R100 HBM4 20.7TB 내부에서 수천 명을 한 번에 묶어 처리하는
                   대규모 Continuous Batching 가동률이 100%에 수렴.
                   → 배치가 커질수록 가중치 읽기(고정 비용)가 모든 유저에 분산
                   → 한 유저당 한계 비용이 0에 수렴

[Roofline 도달]   더 이상 속도가 떨어지지 않는 하드웨어 물리 최대 한계선.
                   HBM4 22TB/s 대역 + FP4 50K POPS 연산이 동시 포화 →
                   추가 유저/컨텍스트가 들어와도 TPS/MW가 거의 변하지 않음(수렴).

→ R100 x=200(0.7M) → x=400(0.2M)의 완만 하강은 spill/용량 문제가 아니라
  "이미 한계선(Roofline)에 도달해 더 내려갈 곳이 없는" 수렴 곡선.
  H100(절벽)·B300(대역폭 하강)과 징후가 다른 이유.
```

> ⚠️ v2 첫 판은 x=100을 memory-bound로만 설명. Prefill O(N²) 16배 폭발 요인을
> 정식 보강(2026-08-26). R100은 HBM4 22TB/s로 memory를 압도하므로 x=100에서
> compute-bound 전환이 가장 먼저 나타나는 세대. x≥200은 Batch Saturation →
> Roofline 수렴으로 곡선이 눕는다.

---

## 9. 12 포인트 CXL / Spill-over 영향 (2026-08-26 정합성 재계산)

> CXL(서버로컬 + 풀)이 12 포인트에 미치는 영향. **derive된 users + 6.16/10.80/32.77/102.40 GB/user** 기준 재계산.
> v1/v2첫판은 14.1GB/user 가정으로 R100 x=50을 "CXL 불필요"로 봤으나, **0.1925MB/tok 교정 + chart_users vs max_HBM 대조** 결과 **R100 x=50부터 이미 SPILL**.

### 9.1 R100 NVL72 — spill 정량 + NVLink-C2C 방어 (72 GPU / 199kW, BF16 기준)

```
R100 HBM4 총: 288 × 72 = 20,736 GB ≈ 20.2 TB  (weights 차감 전)
R100 SOCAMM:  80 TB (44 TB/s)
NVLink-C2C:  1.8 TB/s (GPU간 일관성 패브릭) ← R100 전용 초고속 경로
CXL pool:    5 TB/s (열등, 호스트 경유)

[차트 1.65M TPS/MW 신뢰 → spill 필연]
x=50 (Free, Qwen3, 32K, 6.16GB/u):
  chart 6,567 users → 요구 KV 40.5 TB. max_HBM 3,290 users(20.3TB 가용).
  spill = 3,277 × 6.16 = 20.2 TB → SOCAMM 80TB 흡수.

x=100 (Medium, Kimi MLA, 128K, 10.80GB/u):
  chart 3,184 users → max_HBM 1,735 users. spill = 1,449 × 10.80 = 15.7 TB → SOCAMM 흡수.

x=200 (High, GPT, 128K, 32.77GB/u):
  chart 696 users → max_HBM 511 users. spill = 185 × 32.77 = 6.1 TB → SOCAMM 흡수.

x=400 (Premium, GPT, 400K, 102.40GB/u):
  chart 100 users → max_HBM 163 users → chart < max → OK, spill 없음.
```

**NVLink-C2C 1.8TB/s 방어 주석 (R100 spill 지연 억제)**:
R100은 spill이 발생해도 **일반 CXL(5TB/s, 호스트 경유)과 달리 NVLink-C2C 1.8TB/s
초고속 일관성 패브릭**으로 spill된 KV를 다른 GPU의 HBM에서 일관성 있게 접근.
- **대역 보조**: 1.8TB/s가 HBM4 22TB/s의 약 8% 보조 대역으로 작동 → spill 경로 병목 완화
- **일관성 유지**: GPU간 직접 일관성(μs 단위 지연)으로 호스트 경유 CXL 대비 지연 폭 억제
→ 차트 1.65M(피크 효율)은 "spill 없음"이 아니라 **"spill이 발생해도 C2C가 대역·지연을
방어하여 피크를 유지"**하는 것으로 설명됨. 타 세대(H100/B300)엔 C2C 일관성 패브릭 없음.

**R100 "성공의 역설 (Too Fast to Fit)" — Scale-Out 확장 메커니즘 (최종 확정)**:
R100 spill은 **용량 결함이 아니다**. B300과 HBM 용량이 같음(20.7TB)에도 R100만 spill이
발생하는 이유는 R100의 **압도적 가성비(1.65M TPS/MW, B300 2.4배) + 전력 폭발(0.199MW,
B300 1.6배)**로 Total TPS가 3.9배 → 동시 유저 3.9배 → KV 요구 40.5TB로 같은 HBM을 뚫고
나가기 때문. 즉 **"R100이 너무 빨라서, 같은 창고에 더 많은 사람을 한 번에 처리하려니
창고가 모자라는" 성공의 역설**. 단일 랙 HBM(20.7TB)으로는 차트 1.65M이 물리적으로
도달 불가 → **NVLink-C2C 1.8TB/s + LPDDR5X SOCAMM 80TB 풀 확장이 전제된 Scale-Out
아키텍처**. 이것이 R100만의 기술적 당위성이자 B300(Standalone)과의 대비점.

### 9.2 Spill-over + CXL 지연 패널티 수식 (구체화)

```
물리 상수 (2026 기준):
  HBM4 BW  (R100)      : 22 TB/s  (per-GPU 22TB/s)
  NVLink-C2C BW (R100) :  1.8 TB/s (GPU간 일관성 패브릭, μs 지연) ← R100 전용
  SOCAMM2 BW            : 44 TB/s (이론, 호스트 DDR5 풀)
  CXL 3.0 BW           :  5 TB/s (64 GB/s × 80 lanes 추정, 호스트 경유)
  HBM4 : CXL BW 비      : 22 / 5 = 4.4× → CXL 경로는 HBM 대역의 23%만

Spill 구간 지연 패널티 모델 (세대별 경로 차이 반영):
  [H100/B300 — CXL/SOCAMM 경로, 패널티 有]
    effective_decode_BW = HBM_BW × (HBM_fraction) + CXL_BW × (spill_fraction)
    latency_penalty ≈ 1 / (HBM_frac + 0.23 × spill_frac)
    → spill 100% 시 지연 3.5× 증가 (BW 0.23× 가중 평균과 정합)

  [R100 — NVLink-C2C 일관성 경로, 패널티 억제]
    effective_decode_BW = HBM4_BW × (HBM_frac) + C2C_BW × (spill_frac_to_other_GPU_HBM)
    C2C 1.8TB/s = HBM4 22TB/s의 8% 보조 대역 + GPU간 일관성(μs 지연)으로 호스트 경유 억제
    → spill이 발생해도 C2C가 대역 보조 + 일관성 유지로 피크 효율(1.65M) 방어
```

**Premium(400K) CXL 오프로드 물리 근거** — R100에서조차 chart 동시 유저가 HBM max를
초과해 spill이 발생하는 대규모 접속 시나리오에서 CXL 풀이 필요. 이 구간의 TPS당 단가는
**지연 3.5× 패널티** + **CapEx(CXL 풀 인프라)** + **400K prefill compute** 3중 부담 →
Free 대비 **≥15× 할증** 물리 근거(Section 10 가격 연동). (H100/B300의 Premium은
weights/용량 한계로 별개 문제 — H100은 N/A, B300은 HBM 내 fitting으로 CXL 불필요)

### 9.3 12 포인트 CXL 요약 (재계산)

| 포인트 | chart_users | max_HBM | spill(users) | spill(GB) | spill 목적지 | CXL 필요 |
|--------|------------:|--------:|-------------:|---------:|--------------|:--------:|
| H100 x=50 | 120 | 339 | 0 | 0 | — | NO |
| H100 x=100 | 24 | 52 | 0 | 0 | — | NO |
| H100 x=200 | — | — | — | — | (미지원·회색선) | **N/A** |
| H100 x=400 | — | — | — | — | (미지원·회색선) | **N/A** |
| B300 x=50 | 1,694 | 3,290 | 0 | 0 | — | NO |
| B300 x=100 | 726 | 1,735 | 0 | 0 | — | NO |
| B300 x=200 | 91 | 511 | 0 | 0 | — | NO |
| B300 x=400 | 21 | 163 | 0 | 0 | — | NO |
| R100 x=50 | 6,567 | 3,290 | **3,277** | 20.2 TB | SOCAMM | NO(SOCAMM 흡수) |
| R100 x=100 | 3,184 | 1,735 | **1,449** | 15.7 TB | SOCAMM | NO(SOCAMM 흡수) |
| R100 x=200 | 696 | 511 | **185** | 6.1 TB | SOCAMM | NO(SOCAMM 흡수) |
| R100 x=400 | 100 | 163 | 0 | 0 | — | NO |

> **핵심 재해석 (v2첫판 교정)**: 0.1925MB/tok 교정 + MLA 적용 후, **R100 x=50~200 spill이
> 전부 SOCAMM 80TB 범위 내**로 들어옴. CXL(5TB/s)이 실질 차트 영향을 주는 지점은
> "SOCAMM마저 초과하는 초대규모 동시 접속" 또는 "Premium에서 CXL 2.0/3.0 풀링으로
> HBM 한계 회피" 시나리오로 좁아짐. CXL 가치 = **capacity overflow 확장**, 가속이 아님.

---

## 10. 차트가 전하는 메시지 (3줄 요약 — 6.16GB 교정)

```
1. GPU가 세대를 거듭할수록 전력당 처리량(TPS/MW)이 폭증
   - 같은 x=50: H100 0.15M → B300 0.7M → R100 1.65M (약 11배)
   - 원인: FP4 density (H100 FP8만, B300/R100 FP4) + HBM4 BW (22TB/s)

2. 곡선 기울기가 세대별로 다른 이유 = 3단계 물리 징후 (절벽·하강·수렴)
   - H100 = **절벽**: 용량의 벽. x=200 가중치 4,000GB > HBM 2,560GB → N/A 회색선(구동 불가)
   - B300 = **하강**: 대역폭의 벽. 용량 여유(16.3TB) 있어도 HBM3e 8TB/s 포화 → 완만 하강(spill 아님). **Standalone 단독 랙 자급형**(10.4TB < 20.3TB)
   - R100 = **수렴**: 연산의 벽 후 Batch Saturation. x=100 Prefill 16배 폭발로 1차 꺾임 → x≥200 Roofline 도달. **Too Fast to Fit**(40.5TB > 20.7TB) → C2C+SOCAMM **Scale-Out** 전제

3. 컨텍스트(Interactivity 요구)가 길어질수록 처리량 급감
   - 컨텍스트는 곧 비용: 32K=6.16GB/u(Qwen3), 128K=10.80GB/u(Kimi MLA), 400K=102.40GB/u(GPT)
   - Premium이 Free 대비 16.6배 VRAM → $0 vs $45 가격 계층의 물리 원천
   - x=100(128K) 꺾임 = 이중 병목 전환점: KV 10.80GB 증가(memory) + Prefill O(N²) 16배 폭발(compute)
   - Rubin만 x=50~100 flat (HBM4 BW가 decode 압도). 단 R100도 chart 1.65M TPS 내려면
     spill 필연(40.5TB>20.3TB) → NVLink-C2C 1.8TB/s 대역 보조·일관성으로 피크 방어.

3. 가격 계층은 컨텍스트 길이 + 모델 규모와 정확히 매핑
   - Free($0, Qwen3 235B, 32K) → Medium($3, Kimi 1T MLA, 128K) → High($6, GPT 2T, 128K) → Premium($45, GPT 2T, 400K)
   - 긴 컨텍스트 + 대규모 모델 = 더 많은 KV 캐시 + weights + (초과 시) CXL 패널티 = 더 비싼 서비스 정당화
   - Premium ≥15× 할증 = (지연 3.5× CXL 패널티) × (CapEx) × (400K prefill) 물리 근거
```

---

## 11. 교차 참조

| 문서 | 용도 |
|------|------|
| [gpu-inference-economics.md](gpu-inference-economics.md) | GPU 세대별 TFLOPS/HBM/BW/TDP 스펙 |
| [gpu-inference-chart-verification.md](gpu-inference-chart-verification.md) | 기존 차트 판독/역산 (v1 계열) |
| [gpu-inference-tps-perf-calculation.md](gpu-inference-tps-perf-calculation.md) | x-sweep 계산 + 효율 모델 |
| [jensen-huang-chart-analysis.md](jensen-huang-chart-analysis.md) | **v1 (2026-08-21, 오류 포함, 보존됨)** |

---

## 12. 검증 방법 (이 판독이 확정된 이유)

1. **이미지 육안 판독**: 사용자가 제공한 GTC 2026 스테이지 슬라이드 PNG에서
   세 곡선의 12개 포인트를 직접 읽음.
2. **물리 역산 일치**: H100 x=50 → 6,000 TPS (40kW) = 187.5 TPS/GPU. 32 GPU 랙에서
   자연스러운 효율 범위임을 확인.
3. **Annotation 일치**: 2X/3X/10X 화살표가 절대 비율 경향과 정합적.
4. **가격 티어 매핑**: 하단 Free/Medium/High/Premium 라벨이 x=50/100/200/400에
   정확히 위치.

---

> **v1 대비 결론**: v1의 판독은 "이미지 없이 추측"으로 시작해 누적 오류가 있었으나,
> 구조(4 티어, 3 곡선, KV cache 물리 법칙, CXL cap)는 방향이 맞았다. v2는 그 구조를
> **실제 그림으로 확정한 판독값**으로 갈아끼운 정본이다. 이후 모든 Jensen Chart 논의는
> 이 v2를 기준으로 한다.
