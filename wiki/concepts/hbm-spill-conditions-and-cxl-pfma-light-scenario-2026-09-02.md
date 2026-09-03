# HBM Spill 조건 MECE 분류 + PFMA×Light 시나리오 (X<50 역방향)

> 2026-09-02 추가 검토. 상위: [[cxl-pooled-rack-feasibility-multi-rack-2026-09-01]] (3관점 검토), [[jensen-huang-chart-session-handoff-20260828]].
> 사용자 2가지 질문:
> 1. HBM spill 발생 조건을 MECE하게 분류하고, CXL Pooled Rack이 positive인 case 조사
> 2. CXL BW/RDMA 한계를 PFMA로 극복한다 치고, Light(LLM/concurrency/context)에서 X<50 역할 가능?
> 모든 수치는 [[jensen_chart_calc]] 엔진 기반. PFMA 정의는 [[english-meeting-script-style]] Example 1 (2026-08-24 Marvell 미팅) + [[pfma-email-interpretation-2026-09-01]] (CXL3.x CMM 샘플 요청).

---

## 0. 전제: 현재 그래프 12점은 모두 spill=0

R100=101kW 기준, 12점 전부 HBM 99% 이내 안착 (spill=0). 따라서 **spill은 그래프 범위 밖(x>400, x<50, 또는 Y 예측 초과 burst)에서 발생**.

---

## 1. Part 1 — HBM Spill 조건 MECE 분류

spill = max(0, LLM + KV_total − HBM)
KV_total = users × per-user KV = users × (context × KV_per_token ÷ 1024)

∴ **spill > 0의 3가지 원인 (MECE)**:

| 케이스 | 원인 | 변수 | 임계값 (R100, 101kW) |
|---|---|---|---|
| **A. LLM 대형화** | weight 자체가 HBM 초과 | LLM_GB ↑ | Free(50): LLM 634GB 초과 시 spill (현재 470GB, 여유 164GB) |
| **B. Context 증가** | per-user KV 증대 (x>400) | context ↑ | context 4배(x=1600) 시 Free~High 전 티어 spill |
| **C. 사용자 폭증** | burst traffic (Y 예측 초과) | users ↑ | Free(50): 1.01배만 초과해도 spill; Premium(400): 3.2배까지 여유 |
| (D. HBM 감소) | 설계 변경 | HBM ↓ | 그래프 범위 밖 (설계 파라미터) |

### Case별 상세 임계표

**Case A — LLM 대형화 (101kW, 사용자 수 그래프값 유지)**

| x | users | KV(GB) | spill 임계 LLM(GB) | 현재 LLM | 여유 |
|---|---|---|---|---|---|
| 50 | 3,333 | 20,102 | **634** | 470 | 164GB (1.35×) |
| 100 | 1,616 | 14,544 | 6,192 | 2,000 | 4,192GB (3.1×) |
| 200 | 354 | 10,870 | 9,866 | 4,000 | 5,866GB (2.5×) |
| 400 | 50 | 4,853 | 15,883 | 4,000 | 11,883GB (4×) |

→ Free(50)만 LLM 634GB 이상에서 spill. 10T+ MoE 모델이 Free 티어에서 spill 유발.

**Case B — Context 증대 (per-user KV 2배/4배)**

| context 배수 | x=50 spill | x=100 spill | x=200 spill | x=400 spill |
|---|---|---|---|---|
| 2× (x≈800) | 19,938GB | 10,352GB | 5,004GB | **0GB** |
| 4× (x≈1600) | 60,143GB | 39,440GB | 26,744GB | 2,675GB |

→ Premium(400)이 context 증대에 가장 강함 (사용자 50명이라 KV 총량 작음).
→ Free(50)가 context 증대에 가장 취약 (사용자 3,333명이라 KV 총량 큼).

**Case C — 사용자 폭증 (burst traffic)**

| x | 그래프 users | per-user KV | spill 임계 users | 여유 배수 |
|---|---|---|---|---|
| 50 | 3,333 | 6.03GB | 3,360 | **1.0× (거의 한계)** |
| 100 | 1,616 | 9.00GB | 2,082 | 1.3× |
| 200 | 354 | 30.75GB | 544 | 1.5× |
| 400 | 50 | 96.09GB | 174 | 3.2× |

→ Free(50)는 이미 99%라 burst traffic에 극히 취약. Premium(400)은 3.2배까지 버팀.

### CXL Pooled Rack이 positive인 case (Part 1 결론)

| 케이스 | CXL positive? | 이유 |
|---|---|---|
| **A. LLM 10T+ (Free 티어)** | **✓ positive** | LLM 자체가 HBM 초과 → CXL에 weight 일부 offload. 단 weight는 hot(매 토큰 read) → CXL BW 한계 → **소수 huge MoE에서만** |
| **B. x>400 (context 증대)** | **✓ positive (대표적)** | per-user KV 증대 → 총 KV가 HBM 초과 → cold KV를 CXL로. **이게 CXL 본래 용도** |
| **C. 사용자 폭증 (Free)** | **✓ positive** | burst 시 총 KV 초과 → CXL이 overflow 흡수. 단 Free는 여유 1.0×라 자주 발생 |
| **C. 사용자 폭증 (Premium)** | △ 약positive | 3.2배 여유라 CXL 필요성 낮음 |
| **D. HBM 감소** | ✓ positive | CXL이 용량 보충 (설계 차원) |

**→ CXL이 가장 positive인 case: B(context 증대, x>400) + C-burst(Free 사용자 폭증)**
**→ A(LLM 10T+)는 CXL BW 한계로 제한적 (weight는 hot path)**

---

## 2. Part 2 — PFMA × Light(L/M/C) 시나리오: X<50 역방향

### 2.1 PFMA 기술 정의 (회의록 기반)

**출처**: [[english-meeting-script-style]] Example 1 (2026-08-24 Marvell Ravi 미팅) + [[pfma-email-interpretation-2026-09-01]]

회의록 핵심 문장:
> "SK hynix is currently evaluating not only CXL memory modules but also **CXL pooled memory appliances**. When we deploy them **out-rack**, we need to overcome the **RDMA bottleneck**, and we're hoping **Marvell's PFMA** can help address this."

+ 9/1 이메일: CXL3.x CMM 샘플 16개 요청 (US 8 + Taiwan 8), 10월 ES → 27년 2월 CS → 양산

**PFMA = Pooled [Memory] Fabric Appliance / Architecture (Marvell)** — CXL pooled memory를 out-rack(랙 외부)에 배포할 때 cross-rack RDMA bottleneck을 극복하는 Marvell의 풀드 메모리 패브릭 솔루션. (정확한 expansion은 Marvell 파트너 용어라 비공개; 회의록 맥락상 이 범위)

### 2.2 핵심 가설 검증: Light 조건이면 CXL BW/RDMA로 감당 가능?

**인터페이스 위계 (per-GPU 환산)**:

| 인터페이스 | per-GPU BW | HBM 대비 |
|---|---|---|
| HBM4 (in-GPU) | 22,000 GB/s | 100% |
| PFMA (DPU 8포트 6.4 TB/s ÷ 72) | 89 GB/s | 0.4% |
| CXL disagg (5 TB/s ÷ 72) | 69 GB/s | 0.3% |
| RDMA 단일포트 (0.8 TB/s ÷ 72) | 11 GB/s | 0.05% |

→ PFMA는 RDMA 단일포트 대비 **8× 향상** (11 → 89 GB/s), 하지만 HBM 대비 0.4%.

**Light 시나리오 1사용자 decode TPS** (TPS = BW ÷ per-user KV):

| 시나리오 | per-user KV | HBM TPS | CXL TPS | RDMA TPS | **PFMA TPS** |
|---|---|---|---|---|---|
| Ultra-Light (8B, 4K ctx) | 0.20 GB | 112,640 | 356 | 57 | **455** |
| Light-Light-Light (30B, 4K) | 0.28 GB | 78,222 | 247 | 40 | **316** |
| Light-Light-Mid (30B, 8K) | 0.56 GB | 39,111 | 123 | 20 | **158** |
| Mid-Light-Light (235B, 4K) | 0.75 GB | 29,181 | 92 | 15 | **118** |
| 현재 Free x=50 (235B, 32K) | 6.03 GB | 3,648 | 12 | 2 | **15** |

**→ Ultra-Light는 PFMA로 455 TPS/GPU** — HBM의 0.4%지만, **Light 서비스는 TPS 자체가 낮아도 충분** → 실용 가능
**→ 현재 Free(x=50) per-user KV 6.03GB는 PFMA로 15 TPS** → 실용 불가 (Light 아님)

### 2.3 X<50 영역 = "HBM over-spec" 영역

Light 시나리오의 HBM 점유율 (사용자 50명 기준):

| 시나리오 | LLM+KV (GB) | HBM 점유율 | 의미 |
|---|---|---|---|
| Ultra-Light (8B, 4K) | 25.8 | **0.13%** | HBM 99.87% 낭비 |
| Light-Light-Light (30B, 4K) | 74.1 | 0.36% | HBM 99.6% 낭비 |
| Light-Light-Mid (30B, 8K) | 88.1 | 0.42% | HBM 99.6% 낭비 |
| Mid-Light-Light (235B, 4K) | 272.7 | 1.32% | HBM 98.7% 낭비 |
| 현재 Free x=50 (235B, 32K) | 771.6 | 3.72% | (이미 Light 아님) |

**→ X<50 영역은 HBM이 극단적 over-spec** (0.1~1.3%만 사용)
**→ GPU 72대 HBM 20TB는 Light 서비스에 심각한 과잉 투자**

### 2.4 Part 2 결론: X<50에서 CXL Pooled Rack + PFMA 역할

**사용자 가설 검증 결과**: **X<50에서 역할 가능 — 그리고 오히려 X>400보다 더 자연스러운 적용**

이유:
1. **용량 관점**: Light는 HBM 0.1~1.3%만 사용 → CXL pooled(100TB)가 LLM+KV 충분히 수용. HBM 전혀 불필요.
2. **BW 관점**: per-user KV 0.2~0.75GB → PFMA(89 GB/s per GPU)로 118~455 TPS 확보. Light 서비스 TPS 요구량(수십~수백 TPS) 충족.
3. **RDMA 관점**: PFMA가 cross-rack RDMA bottleneck을 DPU 8포트 bundling으로 극복 (RDMA 단일 11 → PFMA 89 GB/s, 8×).
4. **경제 관점**: HBM over-spec 영역 → GPU 랙 대신 CXL pooled rack으로 serving → HBM 투자 0, GPU 소수 + CXL 메모리로 비용 절감.

### 2.5 X>400 vs X<50: CXL 역할 비교

| 구분 | X>400 (1차 검토) | X<50 (본 검토, Part 2) |
|---|---|---|
| 용량 압박 | spill 발생 (KV 초과) | **여유 과잉** (HBM over-spec) |
| CXL 역할 | cold KV offload (HBM 보조) | **LLM+KV 전체 수용 (HBM 대체)** |
| per-user KV | 96~384GB (巨大) | 0.2~0.75GB (微小) |
| CXL BW 충분? | 부족 (BW 한계) | **충분 (PFMA 8×로 가속)** |
| GPU 필요 | O (HBM serving) | **최소 (CXL 메모리가 주체)** |
| 경제성 | spill 흡수 (방어적) | **HBM 투자 회피 (공세적)** |

**→ X>400은 CXL이 "HBM의 overflow 방패"라면, X<50은 CXL이 "HBM의 대체재". 후자가 훨씬 공세적·경제적 가치 큼.**

---

## 3. 종합 결론

### 3.1 Part 1 — Spill 조건 & CXL positive case

- **spill 3원인 MECE**: A(LLM 대형화) / B(context 증대) / C(사용자 폭증)
- 현재 그래프 12점은 전부 spill=0 → spill은 그래프 **범위 밖** 현상
- **CXL이 가장 positive**: **B(x>400 context 증대)** + **C-Free(사용자 폭증)**
- A(LLM 10T+)는 weight가 hot path라 CXL BW 한계 → 제한적

### 3.2 Part 2 — PFMA × Light, X<50 역방향

- **X<50은 "HBM over-spec" 영역** (HBM 0.1~1.3%만 사용)
- **PFMA(RDMA bottleneck 극복) + Light(LLM/concurrency/context) 조합에서 CXL이 HBM 대체 가능**
- per-user KV 0.2~0.75GB → PFMA 89 GB/s로 118~455 TPS/GPU → Light 서비스 충분
- **X>400(overflow 방패)보다 X<50(HBM 대체)이 CXL 더 공세적·경제적 가치 큼**
- 단, **PFMA가 RDMA bottleneck 실제로 극복한다는 전제** (회의록 기대, 실증은 2027년 CS 이후)

### 3.3 젠슨황 그래프 양쪽 끝에서의 CXL

```
X<50 (Light)         X=50~400 (그래프)        X>400 (Premium+)
   ↓                     ↓                       ↓
CXL = HBM 대체        CXL = standby           CXL = overflow 방패
(PFMA × Light)       (spill=0, 불필요)       (cold KV offload)
공세적·경제적            —                    방어적·필수
```

**젠슨황 그래프는 X=50~400(HBM 경제학)만 그렸지만, 양쪽 끝(X<50, X>400)에서 CXL이 각각 다른 역할**:
- X<50: HBM 대체 (비용 우위, PFMA 전제)
- X>400: HBM 보조 (용량 방어)

### 3.4 ⚠️ 정정 — Tiering은 BW 부족을 보완하지 못한다 (2026-09-02 사용자 지적)

> 앞서 "Hot/Cold Tiering으로 TPS 유지"라고 기술했으나 **과장**. 사용자 질문 "Tiering이 BW 부족을 보완할 수 있어?"에 대한 정답은 **"없다"**.

**오류의 원인**: "attention locality (최근 25%가 가중치 80%)"를 "cold KV는 안 읽어도 된다"로 잘못 번역. 실제로는:
- 토큰 N+1 생성 시 토큰 1~N **전체 KV**를 읽어 attention 점수를 계산해야 함
- cold KV의 가중치가 작아도, **그 가중치를 계산하려면 cold KV를 읽어야 함**
- ∴ 읽어야 할 총량은 hot + cold = 전체 context (tiering이 줄여주는 건 없음)

**수치 검증** (R100 x=400 Premium, per-user KV 96.09 GB):

| 구분 | TPS/GPU | 결과 |
|---|---|---|
| 전부 HBM (기준) | 228,952 | — |
| Tiering (hot 25% HBM + cold 75% CXL 직접 read) | 963 | **237× 하락** |
| Prefetch (cold를 미리 HBM으로) | — | prefetch 사이클(1.04s)이 단일 decode(4.4ms)의 238배 → 적체 누적 |

**정확한 역할 구분**:
- **Tiering은 "용량" 문제를 풀 뿐 "BW" 문제는 풀지 못함** — 용량과 BW는 다른 차원
- Tiering이 할 수 있는 것: spill 처리 (HBM에 안 들어가는 KV를 CXL에 보관 → TPS 하락을 감수하고 서비스 자체를 유지)

**X>400에서 TPS를 진정 유지하려면** (tiering이 아닌):
1. **PFMA로 CXL BW 자체를 HBM 수준까지 끌어올리는 것** (PF-Chiplet >16 Tbps ≈ HBM 22 Tbps의 73%) — "어디에 저장하느냐"가 아니라 "얼마나 빨리 읽느냐"를 해결
2. **KV Cache Reuse** — 동일 prefix를 1회만 저장·공유 → 실제 읽는 KV 총량 자체를 감소 (읽어야 할 총량 자체를 줄임)
3. **KV를 다수 GPU에 분산 저장** — 각 GPU가 자기 부분만 read → 병렬로 BW 합산

→ **Tiering은 이 중 어느 것도 직접 해결하지 못함**. "어디에 저장하느냐"지, "얼마나 빨리 읽느냐"가 아님.

**∴ 앞선 보고서 초안에서 "KV Cache Hot/Cold Tiering 및 Pre-fetch로 TPS 유지"는 오류. 정정: Tiering은 용량 offload일 뿐 TPS 유지 수단이 아님. TPS 유지는 (1) PFMA BW 확장, (2) KV Reuse 총량 감소, (3) KV 분산 저장으로 달성.**

---

## 4. 계산 근거

| 수치 | 출처 |
|---|---|
| R100 101kW, HBM 20,736GB, per-user KV (6.03/9.00/30.75/96.09) | `jensen_chart_calc.py` |
| HBM4 22 TB/s, CXL disagg 5 TB/s, RDMA 단일 0.8 TB/s, DPU 8포트 6.4 TB/s | [[cxl-pooled-rack-feasibility-multi-rack-2026-09-01]] §3.1 |
| PFMA 정의 (out-rack RDMA bottleneck 극복) | [[english-meeting-script-style]] Example 1 (Marvell 2026-08-24 미팅) |
| CXL3.x CMM 샘플 일정 (10월 ES → 27년 2월 CS) | [[pfma-email-interpretation-2026-09-01]] |
| Light LLM 시나리오 (Qwen3-30B/8B, 4K/8K ctx) | 합리적 가정 — KV/token 0.072/0.050 MB는 MLA/소형 모델 수준 |
| TPS = BW ÷ per-user KV (decode 단계) | [[jensen-huang-chart-session-handoff-20260828]] §2.3 |

---

## 5. 후속 검토 후보

- [ ] X<50 정식 역산 (Light 시나리오의 Y=TPS/MW, 사용자 수)
- [ ] PFMA 실제 BW 실측 (Marvell 2027년 CS 이후 검증, 현재는 회의록 기대치)
- [ ] Light 시나리오 비용 모델 (CXL pooled rack vs NVL72 GPU 랝크 $/M-token)
- [ ] Qwen3-30B-A3B / Qwen3-8B 실제 KV/token 확인 (현재 가정값 0.072/0.050)
- [ ] PFMA × Light의 "HBM 대체" 경제성 임계점 (어느 X 값에서 CXL이 HBM보다 저렴)
