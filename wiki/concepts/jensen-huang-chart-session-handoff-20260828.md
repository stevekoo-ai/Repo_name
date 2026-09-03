# Jensen Huang Inference Economics Chart — 논의 핸드오프 (2026-08-28)

> **용도**: 이 파일은 젠슨황 그래프 논의의 **단일 핸드오프 문서(SSOT)** 다.
> 후속 세션에서 이 논의를 재개할 때 **반드시 이 파일을 먼저 읽고 시작한다.**
> 기존 대화에서 잊어버리는 내용 없이 후속 논의를 하기 위한 수준으로 기록했다.

---

## 0. 최종 확정값 (SSOT — 계산은 전부 python 엔진으로)

### 0.1 계산 엔진 (필수 도구)

- **파일**: `wiki/concepts/jensen_chart_calc.py`
- **규칙**: 논리에서 계산으로 전개되는 **모든 숫자는 python으로 구현**해서 검증한다 (사용자 지시, 2026-08-28).
- 실행: `cd wiki/reference && python jensen_chart_calc.py`
- 구성: GPU 상수 / 12점 좌표 / LLM 스펙 / 사용자 역산 / KV·HBM·MainMem 계산 / 전력 시나리오 비교 / 99% HBM 전력 역산
- **환산 규약**: KV cache GB 환산은 **÷1024** (이전 ÷1000 표기는 오류였음)
- 콘솔 cp949 인코딩 문제 때문에 파일 상단에서 stdout을 UTF-8로 강제하고 있음 (수정 금지)

### 0.2 GPU Rack 상수 (확정)

| 항목 | H100 | B300 NVL72 | R100 NVL72 |
|---|---|---|---|
| **운영 전력 (★확정)** | **0.040 MW** (40kW, NVIDIA 공식) | **0.121 MW** (121kW) | **0.101 MW (101 kW)** |
| HBM | 2,560 GB (80×32) | 20,736 GB (288×72) | 20,736 GB (288×72) |
| HBM BW (GPU당) | 3.35 TB/s | 8.0 TB/s | 22.0 TB/s |
| HBM BW (랙 합계) | ~85.8 TB/s | ~576 TB/s | ~1,584 TB/s |
| Main Memory | 8,192 GB (2TB×4) | 18,432 GB (LPDDR5X 256GB×72) | 18,432 GB |
| R100 전용 | — | — | SOCAMM 80TB + CXL 100TB (2·3단) |
| GPU TDP | 700W | 1,400W | 2,300W (Max 상한) |
| GPU수/서버 | 8×4 servers=32 | 4×18 servers=72 | 4×18 servers=72 |

### 0.3 LLM 스펙 (x=50/100/200/400)

| x | 등급 | 모델 | Attention | KV/token (MB) | LLM 가중치 (GB) | Context | per-user KV (GB) |
|---|---|---|---|---|---|---|---|
| 50 | Free | Qwen3-235B-A22B | GQA (KV heads=4, 94 layers) | 0.193 | 470 | 32,000 | 6.03 |
| 100 | Medium | Kimi K2.5 | MLA (latent=512) | 0.072 | 2,000 | 128,000 | 9.00 |
| 200 | High | GPT MoE 2T | GQA (KV heads=6, 80 layers) | 0.246 | 4,000 | 128,000 | 30.75 |
| 400 | Premium | GPT MoE 2T | GQA | 0.246 | 4,000 | 400,000 | 96.09 |

- per-user KV = Context × KV/token ÷ 1024 → **GPU 세대와 무관, 동일 모델+컨텍스트면 동일**
- MLA가 GQA 대비 KV/token ~44% 절감 (중국계 LLM: MLA+INT4 / 미국계: GQA+BF16)

### 0.4 12개 점 좌표 + 역산 사용자 수 (R100=101kW 최종본)

공식: **사용자 수 = (TPS/MW × 1e6 × Rack Power[MW]) ÷ x**

| 세대 | 등급 | 모델 | 사용자(명) | Context | 총 KV(GB) | LLM(GB) | HBM(GB) | 총필요(GB) | HBM 사용률 |
|---|---|---|---|---|---|---|---|---|---|
| H100 | Free | Qwen3 23B | 120 | 32,000 | 724 | 470 | 2,560 | 1,194 | 47% |
| H100 | Medium | KIMI K2.5 | 24 | 128,000 | 216 | 2,000 | 2,560 | 2,216 | 87% |
| H100 | High | GPT MoE 2T | **1차사망●** | 128,000 | — | 4,000 | 2,560 | — | — |
| H100 | Premium | GPT MoE 2T | **1차사망●** | 400,000 | — | 4,000 | 2,560 | — | — |
| B300 | Free | Qwen3 23B | 1,694 | 32,000 | 10,217 | 470 | 20,736 | 10,687 | 52% |
| B300 | Medium | KIMI K2.5 | 726 | 128,000 | 6,534 | 2,000 | 20,736 | 8,534 | 41% |
| B300 | High | GPT MoE 2T | 91 | 128,000 | 2,791 | 4,000 | 20,736 | 6,791 | 33% |
| B300 | Premium | GPT MoE 2T | 21 | 400,000 | 2,035 | 4,000 | 20,736 | 6,035 | 29% |
| R100 | Free | Qwen3 23B | 3,333 | 32,000 | 20,102 | 470 | 20,736 | 20,572 | **99%** |
| R100 | Medium | KIMI K2.5 | 1,616 | 128,000 | 14,544 | 2,000 | 20,736 | 16,544 | 80% |
| R100 | High | GPT MoE 2T | 354 | 128,000 | 10,870 | 4,000 | 20,736 | 14,870 | 72% |
| R100 | Premium | GPT MoE 2T | 50 | 400,000 | 4,853 | 4,000 | 20,736 | 8,853 | 43% |

12점 좌표 (X=x, Y=TPS/MW):
- H100: (50,0.15M) (100,0.06M) — x=200/400은 1차사망(가중치 4TB > HBM 2.56TB)
- B300: (50,0.70M) (100,0.60M) (200,0.15M) (400,0.07M)
- R100: (50,1.65M) (100,1.60M) (200,0.70M) (400,0.20M)

---

## 1. R100 전력 결정 과정 (핵심 논쟁 기록 — 다시 반복하지 말 것)

### 결론: **R100 운영 전력 = 101 kW (0.101 MW)** — 사용자 확정 (2026-08-28)

**결정 논리**: "R100 전력 = 동시 사용자 수가 **LLM+KV 총필요가 HBM 용량의 99%**가 되는 값으로 역산"

```
목표: LLM + KV = 0.99 × 20,736 = 20,528.64 GB
KV 목표 = 20,528.64 − 470 = 20,058.64 GB
사용자 = 20,058.64 ÷ 6.03125 (per-user KV) = 3,326명
전력 P = 3,326 × 50 ÷ 1,650,000 = 0.1008 MW ≈ 101 kW
```

python 검증: **0.1008 MW** (Free 티어가 결정 제약 — 나머지 티어는 더 여유)

### 전력 후보 비교 (엔진 출력, Free x=50 기준)

| 시나리오 | P_MW | Free 사용자 | 총필요GB | vs HBM+MainMem 39,168 | 판정 |
|---|---|---|---|---|---|
| **101 kW (MaxLPS)** | **0.101** | **3,333** | **20,572** | **53%** | **✓ 채택** |
| 120 kW (공급망 하한) | 0.120 | 3,960 | 24,354 | 62% | ✓ |
| 144 kW (Nominal) | 0.144 | 4,752 | 29,130 | 74% | ✓ (대안) |
| 165.6 kW (GPU-only Max-P) | 0.166 | 5,465 | 33,430 | 85% | ✓ |
| 199 kW (구 위키 정격) | 0.199 | 6,567 | 40,077 | 102% | **✗ Free에서 초과 → 폐기** |

### 전력값 출처/모드 정리 (R100 NVL72)

- ~101 kW: NVIDIA MaxLPS 소프트웨어 전력 최적화 (절대 최소) ← **★ 채택**
- 120~166 kW: 대만 공급망 BOM 실측 범위 (144 kW가 이 구간 = Nominal 대표)
- 190 kW: Dynamic Max-Q (효율 곡선 최적점)
- 199 kW: 구 위키 표준 정격 (TDP 2,300W 기반) — **Free에서 40,077GB로 HBM+MainMem 102% 초과 → TPS 나락 → 폐기**
- 230~240 kW: Static Max-P 설계 상한

### ⚠️ 위키 내 불일치 (미해결 정리 작업)

- 위키 v3 분석·rack-specs 등 다수 문서는 **199kW**로 기록됨 → 101kW로 갱신 필요
- 144kW는 "구버전 TDP 1,200W 시절 값"이 아니라 **공급망 Nominal 실측값**으로, 물리적으로 유효
- 계산 엔진(`jensen_chart_calc.py`)은 0.101로 이미 갱신 완료
- 199kW 시절 계산들(v3 분석의 사용자 6,567/3,184/700/100)은 모두 구식 — 사용자 수는 101kW 기준 3,333/1,616/354/50

---

## 2. 그래프의 물리 — 확정된 해석 (이것이 이 논의의 핵심 결론)

### 2.0 두 축을 왜 이렇게 잡았는가 — 젠슨황의 의도 (2026-08-31 보강)

> 이 절은 2026-08-31에 보강된 해석이다. 사용자 질문 "X축을 왜 TPS/User로?
> X축 증가에 왜 LLM size+Context를 묶었나? Y축은 왜 TPS/MW? 두 축으로 뭘 말하려 했나?"
> 에 대한 답변을 정리한 것으로, §2.1~2.4의 물리와 정확히 일관된다.

**X축 = TPS/User — "상호작용성 1인당 부하" (= 서비스 등급의 대리 변수)**

- `x = 사용자 1명이 초당 소모하는 TPS 부하` (§2.4 확정) → 개별 사용자에게 돌려주는 체감 속도(interactivity)의 척도
- x=50 → 가볍고 다수 동시 / x=400 → 무겁고 소수 집중
- **핵심**: x를 올리는 것은 "더 빨리"가 아니라 **서비스 등급(Free→Medium→High→Premium)을 올리는 것**.
  x=50/100/200/400은 LLM 가중치(470→2,000→4,000GB)와 컨텍스트(32K→128K→400K)가 같이 커지는 점
  (A-2 표). → X축은 "속도 축"인 척하면서, 실제로는 **"등급이 올라갈수록 부풀어오르는 1인당 부하"**를 압축.
  - 모델↑ → per-token 가중치 읽기↑ / 컨텍스트↑ → per-user KV↑ (6.03→9.00→30.75→96.09 GB)
  - 합쳐져 x=400의 1인당 부하 = x=50의 ~8배
- 젠슨황의 의도: "사용자 수를 늘리는 게 아니라, **더 지능적인 서비스로 올라갈 때 1인당 부하가 비선형적으로 커지는 경제 구조**"를 한 축에 담음.

**Y축 = TPS/MW — "에너지 효율(와트당 처리량)"**

- `TPS/MW = HBM_BW ÷ (KV_per_token × Context × MW)` (§2 핵심 공식) → 전력 1W로 1초당 처리하는 토큰 수 = 에너지 단가(economics)의 축
- 인퍼런스 비용의 최대 항목은 칩 원가가 아니라 **전력** (데이터센터 TCO에서 전력 지배적) → TPS(절대량)가 아니라 TPS/MW(전력당 효율)로 잡아야 세대간 "전력을 얼마나 잘 쓰는가"가 직접 비교됨
- Y축은 TFLOPS가 아니라 **HBM 대역폭(3.35→8.0→22.0 TB/s)**이 결정 (§2.2) → Y축 = "메모리 대역폭을 전력으로 나눈 효율"

**두 축이 말하는 메시지 (한 문장)**

> "서비스 등급(X)이 올라갈수록 전력 효율(Y)은 떨어지고 — 새 GPU 세대는 그 하락 곡선 전체를 위로 들어올린다."

- 같은 세대 곡선 내: x↑ → per-user KV↑ → Y↓ ("더 지능적인 서비스는 전력 효율이 나빠진다" = 경제적 trade-off)
- 세대 전환: 같은 x에서 Y가 위로 점프 (HBM BW 6.6× → 같은 등급·전력으로 더 많은 사용자·높은 효율)
- H100 x=200/400 사망(●): "구세대는 Premium 서비스 자체가 불가능" (가중치 4TB > HBM 2.56TB)

**최종**: X축 = "지능의 단가(1인당 부하)", Y축 = "에너지의 단가(와트당 효율)". 두 단가의 교차점을
GPU 세대가 어떻게 밀어올리는지를 한 장에 그린 것 → "HBM 대역폭 전쟁이 곧 인퍼런스 경제학의 승부"
(§5 결론, §4 C-Level 시사점과 일관).

### 2.1 TPS/MW (Y축)의 정체

```
TPS = GPU Memory BW ÷ Total KV Cache        (decode phase 기준)
TPS/MW = HBM_BW ÷ (KV_per_token × Context × Rack MW)
```

- **사용자 수는 TPS/MW에서 역산된 결과값이지, TPS/MW의 원인이 아님** (인과 방향 주의)
- Total KV cache가 Premium에서 오히려 줄어드는 것: 컨텍스트 3.1×↑보다 사용자 7.1×↓가 압도하기 때문 (45.3M 토큰 → 20.0M 토큰)
- 그러나 **per-user KV는 컨텍스트 3.125배 증가로 30.75→96.09 GB로 커지고**, 이것이 분모를 키워 TPS/MW를 낮춤

### 2.2 세대간 차이의 근원

- LLM 인퍼런스 decode는 **연산(TFLOPS)이 아니라 메모리 읽기(HBM BW) 병목**
- HBM BW: H100 3.35 → B300 8.0 (2.4×) → R100 22.0 TB/s (2.75×) — **H100→R100 6.6×**
- 같은 Premium 티어: B300 21명 vs R100 50명 — per-user KV는 동일(96.09GB), 차이는 순수히 TPS/MW×MW 차이
- 사용자 비유 확정: **"그냥 BW가 10배 차이 난다"** (H100 대비 R100 랙급 15×)

### 2.3 KV Cache 역설 (Premium vs High)

- 총 KV cache: Premium < High (사용자 7× 감소 효과)
- per-user KV: Premium > High (컨텍스트 3.125×)
- TPS/MW: Premium < High (컨텍스트가 분모 → 효율 하락)
- **세 값은 서로 다른 축** — 총량(부하), 개인(컨텍스트), 효율(BW)

### 2.4 사용자 역산의 직관

```
x = 사용자 1명이 초당 소모하는 TPS 부하
동시 사용자 수 = 랙 총 TPS ÷ x

R100 예: x=50 → 166,650÷50=3,333명 / x=100 → 161,600÷100=1,616명
        x=200 → 70,700÷200=354명  / x=400 → 20,200÷400=50명
```

### 2.5 축 설계의 의도 — 젠슨황은 왜 X=TPS/User, Y=TPS/MW로 그렸는가 (2026-08-31 확정)

**X축 (TPS/User) = "수요 측" 축 — 서비스 등급의 대리 변수**
- x = 사용자 1명이 체감하는 응답 속도(interactivity) = "1명을 얼마나 빠르게/풍부하게 서빙하는가"
- x는 단일 변수가 아니라 **등급 묶음**: x↑ = 컨텍스트↑ + 모델 크기↑ + 빠른 응답 요구가 한 세트
  (에이전트·코딩 어시스턴트 같은 프리미엄 워크로드가 이 조합을 요구 — 시장이 실제로 그렇게 이동)
- **부하 계수 정정**: x 자체는 8배(400÷50)지만, 1인당 메모리 부하(per-user KV)는
  6.03→96.09 GB = **15.9배** (KV/token 1.27× × 컨텍스트 12.5×). 즉 "속도 축인 척하면서
  실제로는 부하 축" — 등급이 오르면 TPS 부하는 선형(8×), 메모리 부하는 그 이상(15.9×)

**가중치 vs KV의 비용 성격 구분 (decode 기준)**
- 가중치: **배치 전체가 공유하는 비용** (토큰당 1회 읽음, 사용자 수로 amortize)
  → "큰 모델은 사용자를 많이 받아야 상쇄됨" — Premium이 소수 정예일 수밖에 없는 구조적 이유 중 하나
- KV: **1인당 전용 비용** (사용자 수로 amortize 불가, 컨텍스트에 정비례)
  → "왜 Premium 티어는 사용자 수가 소수인가"의 메커니즘 (KV가 1인당 전용이기 때문)

**Y축 (TPS/MW) = "공급 측" 축 — 에너지 단가의 역수**
- MW ÷ TPS = 토큰 1개당 에너지 = 전기요금의 본질 → TPS/MW = tokens per megajoule
- AI 시대의 희소 자원은 GPU가 아니라 **전력** → 데이터센터 사업자의 질문
  "내 100MW로 몇 토큰을 팔 수 있는가"에 대한 직답. 전기요금→마진으로 직결되는 C-level 언어
- 물리적 실체: HBM_BW ÷ (KV/token × Context × MW) — 세대 격차는 HBM BW(3.35→8.0→22.0 TB/s)

**두 축의 조합 — 차트의 정체: "서비스 등급별 공급 프론티어 지도"**

| 축 | 정규화 대상 | 답하는 질문 |
|---|---|---|
| X (TPS/User) | 수요 측 — 서비스 품질 | "어떤 등급의 서비스를 파는가?" |
| Y (TPS/MW) | 공급 측 — 전력 효율 | "그 서비스를 전력 1단위당 얼마나 효율적으로 파나?" |

- **Y÷X에 역산 공식이 내장**: users = Y × MW ÷ X — 축 설계만으로 "각 등급에서 랙이 버는 고객 수"가 자동 도출
- 같은 세대 내: x↑ → per-user KV↑ → Y↓ (더 지능적 서비스는 전력 효율이 나빠지는 물리적 trade-off)
- 세대 교체: 곡선 전체가 위로 점프 (HBM BW 진보)
- 구세대(H100): 오른쪽 끝(x≥200)에서 가중치 4TB > HBM 2.56TB 절벽 (1차 사망)

**한 문장 결론**: 젠슨황은 X축으로 "지능의 단가(1인당 부하)"를, Y축으로 "에너지의 단가(와트당 효율)"를 재고,
두 단가의 교차점을 GPU 세대가 어떻게 밀어올리는지를 한 장에 그렸다.
기술적으로는 정확한 물리(HBM BW 결정론)를, 비즈니스적으로는 신세대 전환을 정당화하는 로드맵 서사로 포장한 차트.

---

## 3. 사용자 확정 결론 3가지 (2026-08-28 사용자 정립, 모두 검증 완료)

1. **그래프 12점은 모두 "HBM 용량 안에서 가용한" User 수와 Context를 보여준다.**
   R100=101kW 기준 Free(x=50)가 HBM 99%로 최대 제약, 나머지 티어는 모두 여유. SOCAMM/CXL 미사용.
2. **Y축(TPS/MW)의 실질 결정 요인은 세대별 GPU의 TFLOPS가 아니라 HBM Bandwidth.**
   LLM decode는 메모리 병목 → BW 3.35→8.0→22.0 TB/s가 세대 곡선을 분리.
3. **CXL Pooled memory를 추가해도 이 그래프(X=400 이내)에서 변화 포인트가 없다.**
   CXL은 용량은 주지만 BW가 HBM의 1/10 이하 → TPS/MW(그래프 Y)를 움직이지 못함. spill이 없으므로 standby 상태.

---

## 4. 확장 논의 — CXL/SOCAMM의 진짜 역할

### 4.1 그래프가 성립하는 경계 조건

- X=400 범위 내: **CXL standby, SOCAMM offload 거의 없음** (R100 101kW 기준 spill 0)
- X축 확장 (더 큰 LLM + 더 긴 Context + 더 많은 User): KV가 HBM→SOCAMM→CXL로 offloading 되는 조건이 생김
- **단, X축 확장 시 CXL BW 한계**: CXL BW로는 heavy context 서비스 수준의 TPS 보장 불가.
  GPU가 KV를 **re-computation** 하는 것이 CXL 전송보다 나은 상황 발생.
  = re-computation은 막을 수 있으나 BW가 낮아 heavy context 전송이 안 됨

### 4.2 CXL 활성화 시나리오 (사용자 제시 + 검증 의견)

#### 4.2.0 PFMA (Photonic Fabric Memory Appliance) — Marvell, 2026-08-21 Hot Interconnects

> 정식 명칭 확인 (2026-09-02 웹 검증): Marvell 공식 블로그 + ConvergeDigest + arxiv 2607.27187 일치.
> [[english-meeting-script-style]] Example 1 (2026-08-24 Marvell Ravi 미팅) + [[pfma-email-interpretation-2026-09-01]] (CXL3.x CMM 샘플 요청)

- **정의**: 랙 장착형 공유 메모리 appliance. HBM3e 1TB + DDR5 16-32TB를 단일 공유 주소 공간으로 풀링, 최대 16 서버/XPU가 **여러 랙에 걸쳐** 같은 메모리 풀 접근. 16개 Photonic Fabric Memory Module(각 HBM3e 72GB + DIMM 8개 + Photonic Fabric ASIC + 광 I/O 7.2 Tbps)을 passive all-to-all fiber shuffle로 연결. HBM은 DDR의 write-through cache, 하드웨어 세마포어로 coherency. 2026-02 Marvell Celestial AI 인수에서 비롯.
- **핵심 가치**: "cross-node KV cache" — prefill 노드→decode 노드로 KV를 패킷 네트워크(RDMA)로 복사할 필요 없이 **공유 광 메모리에서 직접 read**. 스케줄러가 prefill/decode 워크로드를 임의 가속기에 배치 가능 (모두 같은 cache 접근).
- **BW/지연**: PF-NIC(PCIe Gen6 x16 / CXL 3.1) 2 Tbps / ~300 ns; PF-Chiplet(XPU 패키지 통합) >16 Tbps / ~230 ns. HBM은 여전히 최속(용량 제한), PFMA는 수백 ns 접근의 중간 tier (storage class보다 훨씬 �름).
- **cross-rack 극복 메커니즘**: 광 도달 ~50 m (실용 25-30 m, 랙 간 충분), passive all-to-all shuffle + 32 외부 laser. **"RDMA 한계 극복" = RDMA 전송 자체를 skip** (공유 메모리에서 직접 read).
- **실증 상태**: Llama-405B trace(8×H200) 시뮬레이션 — 동시 대화 ~300 vs 50, KV cache hit ~82%. **pre-silicon 시뮬레이션, 양산 실측 아님** (2027년 CS 이후 검증 필요).

- **A. CXL pooled Rack mix** → Total MW 절감 + 사용자 증가: **조건부 가능**.
  KV Cache hit rate와 pooled capacity sharing 효율에 좌우.
  Prefetch(CXL→HBM)가 잘 되면 CXL이 HBM 여유분 역할 → 서버당 HBM 탑재량 감소
- **B. Mid-grade LLM + Mid-Context 서비스**: Kimi K2.5(Medium, 128K)가 GPT 2T(Premium, 400K) 대비
  per-user KV 10배 적음 → 같은 HBM으로 10배 사용자 수용. **Cost-Performance 최적점** ✓
- **C. KV Cache Reuse** 🎯: 동일 prefix(시스템 프롬프트, RAG 공통 문서)를 1회만 계산/저장하고 공유.
  **HBM Ceiling를 소프트웨어로 확장** → 그래프 Y축↑(같은 x에서 사용자↑) + X축→(더 긴 컨텍스트) 모두 가능.

### 4.3 CXL Sharing으로 HBM 절감 (사용자 예시 확정)

> GPU server 18대가 각각 공통 KV cache "A"를 복제 보유 → CXL sharing 공간에 1벌만 두고 공유
> **절감 = A × (18−1) = A × 17**

- 개념: "중복 KV deduplication" — KV Cache Reuse(2.2-C)의 하드웨어 구현
- 조건: 공유 A가 hot하면 CXL BW 병목 → hot KV는 HBM, cold KV만 CXL
- 정정 기록: 절감분은 "(공유할당량×서버수)"가 아니라 **"서버별 (peak−평균)의 합"** — 풀 1개가 N서버의 spike를 흡수하는 peak-shaving 구조

### 4.4 CXL BW 검증 (PCIe Gen7 관점)

| 링크 | BW 단방향 | HBM4(22TB/s) 대비 |
|---|---|---|
| PCIe Gen5 x16 | ~64 GB/s | 1/344 |
| PCIe Gen6 x16 | ~128 GB/s | 1/172 |
| PCIe Gen7 x16 | ~256 GB/s | 1/86 |

- **단일 링크**: HBM 대비 1/300 수준 → decode hot path 불가
- **Disaggregated(10대 풀링)**: 10배 병렬 → 2.5~5 TB/s → **SOCAMM 단일(약 1.2 TB/s)의 2~4배, HBM 대비 1/4~1/9**
- **결론: "CXL은 생각할 수 없을 만큼 느리다"는 과장. 정확히는:**
  - 단일 링크 → hot path 불가
  - Disaggregated 병렬화 → 선형 BW 확장 가능 → **cold KV 저장 + prefetch 소스로 실용적**
  - 단독 serving → TPS 붕괴 (1/300) → 불가

---

## 5. 검증 도중 교정된 오류들 (재발 방지)

| 오류 | 정정 |
|---|---|
| KV GB 환산을 ÷1000으로 | **÷1024 규약** (per-user: 6.03/9.00/30.75/96.09 GB) |
| 제공 외부 계산 "R100 Free KV 19,803GB" | 수식 그대로면 **39,607GB** — 2배 축소 오류였고 정확 계산으로 199kW 폐기 근거 확립 |
| "144kW는 물리 불가" (내 단정) | 오류. TDP 2,300W(Max-P 상한) ≠ 평균 소비전력. 144kW는 공급망 Nominal 실측 범위 내 유효값 |
| "0.101MW는 물리 트렌드와 모순" | 논쟁 후 사용자 결정: **메모리 안착(HBM 99%) 기준 역산을 채택** → 101 kW 확정 |
| Prefill 때문에 TPS/MW 감소 (설명 오류) | **decode phase 기준**. TPS = BW ÷ KV_cache. Prefill 병목 설명은 부적절했음 |
| B300 High=150/Premium=70 | 엔진 재계산: **91/21** (0.15M×0.121÷200, 0.07M×0.121÷400) |
| R100 Premium users 100 vs 200 | 정확값 0.2M×0.199÷400=100 → 101kW 기준 **50** |

---

## 6. 후속 논의 시 읽을 파일

1. **이 문서** — 전체 핸드오프
2. `jensen_chart_calc.py` — 계산 실행/검증 (수정 시 전 숫자 재검증)
3. `jensen-huang-chart-analysis-v3.md` — v3 전체 분석 (R100 전력 199kW 표기 → 갱신 필요)
4. `jensen-huang-chart-kv-cache-capacity-matrix.md` — 12점 capacity 매트릭스 (R100 전력 갱신 필요)
5. `jensen-huang-r100-rack-specs.md` — R100 표준 테이블 (199kW 표기 → 갱신 필요)
6. `jensen_chart_v3_plot.py` — 그래프 시각화 (0.199 MW 하드코딩 → 갱신 필요)
7. `gpu-inference-tpssocam-weighted-sum.md` — TDP 1,200→2,300W 이력, SOCAMM 배경

## 7. 외부 검증 — 업계 3소스 교차 검증 (2026-08-31 추가)

> 사용자 요청: "웹에서 믿을 만한 젠슨황 그래프 분석/해석을 최소 3개 찾아보고, 내가 보지 못한 view가 있는지 확인"
> (검색은 search.py 사용 — 회사망 web_search 도구 400 오류 우회)

### 7.1 소스 요약

| 소스 | 날짜 | 핵심 수치 | 축/방법론 |
|---|---|---|---|
| **CoreWeave** (coreweave.com/blog/nvidia-vera-rubin-nvl72-on-coreweave-10x-more-tokens-per-megawatt-than-blackwell) | 2026-07-21 | DeepSeek R1, 동일 interactivity에서 **VR NVL72 = GB200 대비 10× TPS/MW** | **"TPS/user × TPS/MW" 축으로 실측** — 저희 그래프 축 해석과 동일 |
| **NVIDIA 공식 블로그** (blogs.nvidia.com/blog/vera-rubin-nvl72-efficiency-ai-agents) | 2026-08-24 | agentic coding 실측 **30× throughput/MW, 35× token cost** (vs GB300) | OpenRouter: agentic은 채팅 대비 **15× 토큰** 소모 |
| **SemiAnalysis** (inferencex.semianalysis.com/blog/vera-rubin-nvl72-vs-gb200-nvl72-inference) | 2026-07-23 | DeepSeek R1 기준 **5.4× perf/MW, 5× perf/$** (vs GB200) | TCO 모델: Rubin GPU당 $3.57/GPU-hr — **$/M-token 뷰** |

### 7.2 저희가 보지 못한 새로운 View (5개)

1. **Disaggregated prefill/decode 분리** (CoreWeave·NVIDIA) — 프로덕션 스택은 prefill과 decode를
   **물리적으로 다른 GPU 풀**로 분리 (Dynamo + TensorRT-LLM). 젠슨황 그래프의 Y축은
   이 소프트웨어 스택(Expert Parallelism + NVFP4 + MTP + disaggregated serving)이 켜진 상태의 값.
   저희 "decode-only" 공식은 물리 하한이고, 실측 10×는 소프트웨어 co-design이 얹힌 값.
2. **KV offloading + KV-aware routing (NVIDIA 공식 구현)** — "Distributed KV-caching extends memory
   across the scale-up GPU domain, while KV-cache offloading tiers less-active context to host and storage,
   keeping previously processed context accessible **without recomputation**"
   + **KV-aware routing**: 관련 KV를 이미 가진 GPU로 요청 라우팅.
   → **저희 §4.3 "KV Cache Reuse" 논리가 이미 Dynamo에 제품화됨.** 저희는 "미래"라 했지만 NVIDIA는 "현재 제품".
   저희 결론("CXL standby"는 X=400 이내에서 유효)은 유지되나, 소프트웨어 계층이 한 세대 앞서 있음.
3. **가중치 압축 변수 (NVFP4 + LUT Tensor Core)** — SemiAnalysis: DeepSeek R1 가중치 NVFP4 ~1.09TB,
   Rubin의 LUT 기반 압축 형식으로 패키지 수 6→4개. 저희는 가중치 고정(4TB BF16) 가정 →
   **압축이 1차 사망선(가중치>HBM) 자체를 이동시키는 변수**. H100도 NVFP4면 4TB→2TB로 사망선 회피 가능성.
4. **TCO 뷰 ($/M-token)** — SemiAnalysis: "Per-MW만으론 부족. Cost per million tokens는 TCO 반영.
   Rubin은 GPU당 TCO가 더 높다($3.57/GPU-hr)". 즉 **MW 효율 1위 ≠ 비용 1위** —
   C-level 판단에는 $/M-token(자본+전력+데이터센터)이 필요.
5. **Rubin = "kicker" 아키텍처** — SM107은 SM100 대비 microarchitecture 점프가 작음.
   **세대 격차는 마이크로아키텍처가 아니라 메모리(HBM4 2.8× BW)와 시스템 co-design에서 나옴** —
   저희 "HBM BW 전쟁" 결론을 외부 분석가도 동일하게 확인.

### 7.3 종합 평가

- **일관 확인**: 저희 핵심 3결론(HBM BW 결정론 / 12점 HBM 안착 / CXL standby)은 외부 분석과 정면 일치.
  CoreWeave가 정확히 "TPS/user × TPS/MW" 축으로 실측 → **축 해석의 정확성 검증됨**.
- **보완 방향**: 저희는 "하드웨어 물리" 집중, 업계는 ①소프트웨어 co-design(Dynamo, disaggregated serving)
  ②압축(NVFP4/LUT) ③TCO($/토큰)를 동시에 봄.
- **시간축 관점 (SemiAnalysis)**: "Rubin 5.4×는 소프트웨어 미성숙 상태에서 나온 값 — 성숙하면 격차는 더 벌어진다"
  (Blackwell 때와 동일 패턴). 저희 분석에 없던 **시간축 관점**.
- **정책적 시사점**: 젠슨황 그래프의 곡선은 "하드웨어 물리 + 소프트웨어 co-design"의 합성값.
  같은 하드웨어에서 Dynamo/압축 튜닝으로 Y축이 수 배 움직일 수 있음 →
  **Y축을 "하드웨어 상한"으로 읽을지 "소프트웨어 성숙도 함수"로 읽을지 구분 필요.**
  저희 물리 분석(101kW, HBM 99%)은 상한 프레임으로 유효하나, 실측(CoreWeave 10×)은 소프트웨어가 켜진 값.

### 7.4 후속 검토 후보 (새 관점 기반)

- [ ] NVFP4/압축 시나리오를 12점 계산에 반영 (가중치 4TB→1~2TB 시 H100 1차 사망선 이동 확인)
- [ ] disaggregated prefill/decode 를 반영한 Y축 재해석 (graph Y = SW-on 값인지 HW 상한인지)
- [ ] $/M-token TCO 관점 부록 (SemiAnalysis $3.57/GPU-hr 인용)
- [ ] KV-aware routing을 KV Reuse §4.3에 제품 사례로 추가

---

## 8. 미해결 / 다음 논의 후보

- [ ] 위키 전반의 R100 전력 199→101kW 일괄 갱신 (v3 분석, matrix, rack-specs, plot 스크립트)
- [ ] R100 트렌드 역설 기록: 물리 트렌드(R100≥B300 전력 증가)와 101kW 채택의 긴장 — "MaxLPS 소프트웨어 전력 최적화"라는 근거로 정리했으나, "B300(121kW) > R100(101kW)"는 물리 트렌드와 반대 → 이 부분은 **그래프가 그려진 조건(전력 다이어트 운영 모드)** 으로 명시할 필요 있음
- [ ] KV Cache Reuse의 그래프 변화 정량화 (Y축 상승 폭 계산)
- [ ] CXL 10대 Disaggregated 풀링 시 BW 상세 계산 (SOCAMM 대비)
- [ ] x=800 초가혹 시나리오를 101kW 기준으로 재계산 (v3는 199kW 기준)
