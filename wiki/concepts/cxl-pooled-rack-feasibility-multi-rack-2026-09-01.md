# CXL Pooled Rack 타당성 검토 — Multi-Rack·Prefetch·RDMA 3관점

> 2026-09-01 추가 검토. 1차 결론("그래프 x≤400 범위에서 CXL은 standby") 위에서,
> 사용자가 제시한 3가지 추가 관점을 계산 엔진 기반으로 검증.
> 상위 문서: [[jensen-huang-chart-session-handoff-20260828]] §4 (CXL/SOCAMM 역할).
> 모든 수치는 [[jensen_chart_calc]] 엔진 및 본 검토에서 산출.

---

## 0. 검토 배경 (1차 결론 재확인)

- 그래프 12개 점은 **R100=101kW 기준 모두 HBM 99% 이내 안착** (spill=0)
- ∴ 그래프 범위(x≤400)에서 **CXL pooled memory를 적용해도 성능 향상 효과 없음** (용량 여유분만 증가)
- 본 검토는 이 1차 결론을 전제로, **multi-rack 확장 시나리오**에서 CXL이 의미를 가지는 조건을 3관점에서 탐색

---

## 1. Point 1 — CXL Pooled Rack 전력·TPS/MW (Multi-rack 관점)

### 명제
> "CXL pooled rack(10 CXL server, 100TB)이 NVL72보다 전력을 적게 쓰면, multi-rack 측면에서 MW를 낮출 수 있고 TPS를 더 가져올 수 있다"

### 수치 검증

| 항목 | NVL72 GPU 랙 | CXL Pooled 랙 (10 server, 100TB) |
|---|---|---|
| 전력 | **101 kW** (MaxLPS) | **10~20 kW** (메모리 appliance 추정, GPU 0) |
| 자체 TPS | O (72 GPU 연산) | **X (GPU 없음, 용량 저장소)** |
| 역할 | TPS 생성 | KV 용량 저장 + prefetch 소스 |

### 핵심 역설 — "CXL 랙은 TPS를 내지 않는다"

CXL pooled 랙은 GPU가 없는 **메모리 appliance**이므로 자체 TPS=0. 
GPU 랙이 CXL에서 KV를 끌어와야 처리 가능 → **TPS의 주체는 GPU 랙**.

따라서 Multi-rack TPS/MW 계산:
```
TPS/MW(multi) = (GPU 랙이 만든 TPS) / (GPU 랙 MW + CXL 랙 MW)
```

**그래프 범위(x≤400, spill=0)에서의 시뮬레이션** (CXL 랙 10kW 추가):

| x | 단일 랙 TPS/MW | 1 NVL72 + 1 CXL(10kW) | 변화 |
|---|---|---|---|
| 50 (Free) | 1.65M | 1.50M | **↓ 9%** |
| 100 (Medium) | 1.60M | 1.46M | **↓ 9%** |
| 200 (High) | 0.70M | 0.64M | **↓ 9%** |
| 400 (Premium) | 0.20M | 0.18M | **↓ 10%** |

### 결론 (Point 1)

**명제는 그래프 범위 내에서 성립하지 않는다.** 이유:
1. **spill=0** → CXL 용량이 필요 없음 (HBM이 이미 충분)
2. CXL 랙 전력(10~20kW)이 분모에 더해져 **TPS/MW가 오히려 하락** (9~10%)
3. CXL 랙은 GPU가 없어 **TPS 생성에 기여하지 않음** → 분자(TPS) 증가 없이 분모(MW)만 증가

**단, 예외 조건**: 
- 그래프 범위 밖(**x>400**, spill 발생)에서는 CXL이 용량을 제공 → 사용자 증가 가능 → TPS 분자 증가
- 이 경우에만 "CXL 랙 전력↓ → TPS/MW↑" 명제가 조건부 성립 (§3 참조)

---

## 2. Point 2 — NVL72→CXL 대체 시 TPS 감소 + Prefetch Hiding

### 명제
> "NVL72를 CXL pooled rack으로 대체했을 시 TPS 감소효과가 prefetch를 통해 hiding되어야 하는데, 이것이 가능할지? 적절한 혼합 비율은?"

### 2.1 BW 위계 (R100 기준)

| 인터페이스 | BW (TB/s) | HBM4(22 TB/s) 대비 | 용도 |
|---|---|---|---|
| HBM4 (in-GPU) | 22.0 | 1× | hot KV read (decode 병목) |
| DPU 8포트 (cross-rack bundling) | 6.4 | 1/3.4 | 다중 RDMA bundling |
| CXL disagg 10-way (in-rack fabric) | 2.5~5.0 | 1/9~1/4 | cold KV prefetch 소스 |
| NVLink5 풀 (in-rack, GPU↔GPU) | 1.8 | 1/12 | 랙 내 GPU간 KV migration |
| RDMA XDR 단일포트 (cross-rack) | 0.8 | 1/27 | 단일 랙간 링크 |
| CXL 단일 (PCIe Gen7 x16) | 0.256 | 1/86 | 단일 host↔CXL 링크 |

### 2.2 NVL72 KV를 CXL에서 읽을 때 TPS 감소율

```
TPS(decode) = BW ÷ per-user KV
```

per-GPU 기준 (CXL disagg 2.5~5.0 TB/s를 72 GPU로 분할):

| x | per-user KV | HBM TPS/GPU | CXL disagg TPS/GPU | 감소율 |
|---|---|---|---|---|
| 50 | 6.03 GB | 3,648 | 6~12 | **↓ 99.7%** |
| 100 | 9.00 GB | 2,444 | 4~8 | **↓ 99.7%** |
| 200 | 30.75 GB | 715 | 1~2 | **↓ 99.7%** |
| 400 | 96.09 GB | 229 | 0.4~0.7 | **↓ 99.7%** |

→ **NVL72 KV 전체를 CXL에서 읽으면 TPS가 0.3%로 붕괴** (1/300 수준)

### 2.3 Prefetch Hiding 가능 조건 — "지연은 hide, BW 부족은 hide 불가"

**핵심 구분**: 
- decode는 **"다음 토큰"**을 생성 (예측 불가) — 단, attention이 읽는 KV는 **"이미 생성된 과거 토큰"** (예측 가능)
- ∴ **이미 확정된 KV**는 CXL→HBM으로 **prefetch 가능**

**하지만 prefetch의 본질적 한계**:
- prefetch는 **latency(지연) hide**에는 유효
- **BW 부족**은 hide 불가 — CXL disagg(5 TB/s)가 HBM(22 TB/s)의 23%이면, 
  prefetch해도 단위시간당 가져올 수 있는 데이터 총량이 1/4

**∴ hot KV(활성 context, attention 가중치 높음)는 반드시 HBM, cold KV(과거, 가중치 낮음)만 CXL**

### 2.4 Hot/Cold Tiering 기반 혼합 비율

**가정**: attention locality (recency bias) → 최근 25% 토큰이 attention의 ~80%
- **hot KV = 25% context → HBM**
- **cold KV = 75% context → CXL**

**용량 기반 혼합 비율** (CXL 100TB당 처리 가능 NVL72 대수):

| x | 총 KV (GB) | cold 75% (GB) | CXL 100TB당 NVL72 대수 |
|---|---|---|---|
| 50 (Free) | 20,102 | 15,077 | 6.6 대 |
| 100 (Medium) | 14,544 | 10,908 | 9.2 대 |
| 200 (High) | 10,870 | 8,153 | 12.3 대 |
| 400 (Premium) | 4,853 | 3,640 | 27.5 대 |

**→ 그래프 범위(x≤400)에서는 spill=0이므로 이 혼합 비율은 "용량 의미"만 있고 TPS/MW 개선 없음**
**→ 단, x>400 확장 시나리오에서는 의미 부여** (§3)

### 2.5 결론 (Point 2)

1. **NVL72를 CXL pooled로 "대체"하면 TPS가 1/300로 붕괴** — 대체 불가
2. **Prefetch hiding은 "지연"에는 유효하나 "BW 부족"은 hide 불가** — CXL disagg(5 TB/s) = HBM 23%
3. **∴ CXL은 "대체"가 아니라 "cold KV tier"로 병존** — hot KV는 HBM, cold KV만 CXL prefetch
4. **적정 혼합**: NVL72 GPU 랙(연산+hot KV) : CXL pooled 랙(cold KV 저장) = 
   - 용량 관점 **1 : 7~27** (x별, cold KV 기준)
   - 단 그래프 범위 내에서는 **NVL72 100% + CXL standby**가 최적 (spill이 없으므로)

---

## 3. Point 3 — Rack-to-Rack Interface (RDMA) BW 제약

### 명제
> "어떤 interface(RDMA)를 Rack-to-Rack 연결에 사용하는지에 따라 Bandwidth가 제약이 있을 수 있다"

### 3.1 인터페이스 위계와 물리적 거리

```
[GPU 내부] HBM 22 TB/s
    ↓ 1/12
[랙 내 GPU간] NVLink5 1.8 TB/s        ← NVIDIA가 72 GPU를 한 랙에 묶은 이유
    ↓ 1/27 (단일포트) ~ 1/3.4 (DPU 8포트)
[랙 간] RDMA 0.8~6.4 TB/s              ← CXL pooled가 넘어야 할 경계
    ↓ 1/86
[host↔CXL 단일] PCIe Gen7 0.256 TB/s
```

### 3.2 RDMA가 미치는 영향

1. **CXL→GPU prefetch**: cross-rack RDMA 단일포트(0.8 TB/s) << HBM(22 TB/s) 1/27
   → **DPU 다중포트 bundling(8포트 6.4 TB/s) 또는 다중 링크 필수**
2. **Multi-rack 분산**: 모든 데이터가 cross-rack 경유 → RDMA BW가 시스템 TPS 상한
3. **Disaggregated prefill/decode** (CoreWeave/NVIDIA 모델):
   - prefill 랙 ↔ decode 랙 간 KV 전송 → **RDMA가 결정 병목**
   - NVIDIA가 NVL72 하나에 72 GPU를 묶은 이유: **NVLink(1.8 TB/s)로 in-rack 해결**, RDMA 의존 최소화

### 3.3 결론 (Point 3)

1. **CXL pooled rack은 NVL72와 "물리적으로 같은 랙 또는 인접 배치" 전제** — 
   RDMA 단일포트(0.8 TB/s)로는 HBM 1/27, cross-rack prefetch 사실상 불가
2. **DPU 8포트 bundling(6.4 TB/s) 또는 CXL disagg 10-way(5 TB/s) 병렬화 필수** — 
   단일 인터페이스로는 BW 부족
3. **RDMA 인터페이스 선택이 CXL 아키텍처의 실용성을 결정** — 
   InfiniBand XDR(0.8 TB/s) vs Ethernet Ultra(RoCE, 0.8 TB/s) vs 차세대 1.6 Tb/s
4. **"인터페이스 위계"가 CXL 도입 가능성의 물리적 상한** — 
   HBM > DPU8 ≈ CXL disagg > NVLink > RDMA 단일 > CXL 단일

---

## 4. 3관점 종합 결론

### 4.1 그래프 범위(x≤400) 내 — 1차 결론 유지

| 관점 | 결론 |
|---|---|
| Point 1 (전력·TPS/MW) | **CXL 랙 전력↓ 이점 없음** — spill=0이고 CXL은 TPS 생성 안 함 → TPS/MW 오히려 ↓9% |
| Point 2 (prefetch hiding) | **대체 불가, cold tier로 병존만 가능** — BW 1/300 붕괴, prefetch로 BW 부족 hide 불가 |
| Point 3 (RDMA 제약) | **cross-rack RDMA가 병목** — 단일포트 1/27, DPU bundling 전제 |

→ **그래프 범위 내에서 CXL pooled rack 도입은 3관점 모두에서 효과 없음 또는 역효과**

### 4.2 그래프 범위 밖(x>400, spill 발생) — 조건부 의미

x=800(2배 context) 시뮬레이션 (per-user KV 192 GB):

| 사용자 | 총 KV (GB) | HBM 점유 | spill (GB) | CXL 의미 |
|---|---|---|---|---|
| 50 | 9,609 | 66% | 0 | 불필요 |
| 100 | 19,219 | 112% | 2,483 | **cold KV offload** |
| 150 | 28,828 | 158% | 12,092 | **cold KV offload** |
| 200 | 38,438 | 205% | 21,702 | **cold KV offload** |

→ **spill 발생 시에만 CXL pooled rack이 의미**:
- Point 1: 사용자 증가 → TPS 분자 증가 → CXL 랙 전력 증가분 상쇄 가능
- Point 2: cold KV를 CXL로, hot KV는 HBM → TPS는 HBM BW 유지
- Point 3: DPU bundling + 인접 배치 전제 → RDMA 병목 회피

### 4.3 CXL Pooled Rack 도입 조건 (3관점 종합)

CXL pooled rack이 **실제 효과를 내기 위한 필요조건**:

1. **워크로드 조건**: x>400 (초장 context) 또는 사용자 폭증으로 **spill > 0** 발생
2. **Tiering 조건**: hot/cold KV 분리 — hot 25%는 HBM, cold 75%는 CXL
3. **인터페이스 조건**: 
   - CXL pooled rack은 NVL72와 **물리적으로 인접** (또는 같은 랙)
   - **DPU 8포트 bundling(6.4 TB/s) 또는 CXL disagg 10-way(5 TB/s)** 병렬화
   - 단일 RDMA 포트(0.8 TB/s)로는 prefetch 불가
4. **용량 조건**: CXL 100TB당 NVL72 **7~27대** 분산 (x별, cold KV 75% 기준)
5. **소프트웨어 조건**: KV-aware routing + prefetch scheduler (NVIDIA Dynamo 이미 제품화)

### 4.4 핵심 통찰

> **CXL pooled rack은 "그래프 안의 점을 움직이는" 역할이 아니라, 
> "그래프의 경계를 x>400으로 확장하는" 역할이다.**
>
> - 그래프 안(x≤400): HBM 99% 안착 → CXL standby, 도입 시 TPS/MW 역효과
> - 그래프 밖(x>400): spill 발생 → CXL이 cold KV를 흡수, HBM은 hot KV 전담
> - 단 이때도 "대체"가 아니라 "tier 병존" + "RDMA 병목 회피" 전제

---

## 5. 계산 근거 (엔진 검증)

| 수치 | 출처 |
|---|---|
| R100 101kW, HBM 20,736GB, per-user KV (6.03/9.00/30.75/96.09) | `jensen_chart_calc.py` GPU·LLM 상수 |
| HBM4 22 TB/s, SOCAMM 1.2 TB/s, CXL Gen7 0.256 TB/s, disagg 2.5~5 TB/s | 핸드오프 §4.4 |
| NVLink5 1.8 TB/s, IB NDR 0.4 / XDR 0.8 TB/s, DPU 8포트 6.4 TB/s | 본 검토 (NVIDIA 공식 스펙 기준) |
| Multi-rack TPS/MW, x=800 spill 시뮬레이션 | 본 검토 (엔진 함수 응용) |
| Hot/cold 25/75% tiering 가정 | attention locality (recency bias) 합리적 가정 — 실측 시 검증 필요 |

---

## 6. 후속 검토 후보

- [ ] Hot/cold 25/75% 분할 비율 실측 검증 (attention pattern profiling)
- [ ] x=800 정식 역산 (101kW 기준 사용자·KV·전력)
- [ ] NVFP4 weight compression 시나리오 (LLM 4TB → ?GB, HBM 점유 변화)
- [ ] Disaggregated prefill/decode 분리 시 RDMA KV 전송 병목 정량화
- [ ] $/M-token TCO 관점에서 CXL 랙 도입 임계점 (용량↑ vs 전력↑ trade-off)
