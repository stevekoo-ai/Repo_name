# NVIDIA R100 Vera Rubin NVL72 — Rack 인프라 명세 (예상)

> **출처**: v3 분석 (GTC 2026 Jensen Huang 발표 차트 육안 판독) + GB300 NVL72 구조 확장<br>
> **상태**: NVIDIA 공식 datasheet 미출시 → 예측 명세. GB300 구조와 동일 아키텍처 가정.

---

## 1. R100 Vera Rubin NVL72 100% 수랭식 랙 구성 (18대 서버 조합 예상)

* **냉각방식:** 100% 직접 수랭식 (Direct-to-Chip Liquid Cooling) DLC 인프라
* **폼팩터:** 1U 두께의 초고밀도 트레이 구조 및 전면 I/O, 후면 백플레인 직결 (GB300과 동일 예상)
* **아키텍처 설계:** Grace CPU당 **독립 32채널 온보드 직결 구조** — 3단계 메모리 (HBM → SOCAMM → CXL)

---

## Table 1. R100 Vera Rubin NVL72 랙 세부 인프라 명세

| 분류 | 하드웨어 세부 구성 명세 (랙 1대 총합) | 물리적 탑재 용량 (Capacity) | 실무 기준 유효 대역폭 (Bandwidth) | 유효 효율 설정 |
| :--- | :--- | :--- | :--- | :--- |
| **GPU 메모리<br>(HBM4)** | • 총 72개 R100 GPU (서버당 4개 × 18대)<br>• GPU 1대당 288GB VRAM (36GB 스택 × 8개 활성화 ※)<br>• **올바른 수식:** 22,000 GB/s × 72개 GPU × 0.8 | **20,736 GB**<br>(정확히 20.25 TiB) | **1,584,000 GB/s**<br>(약 1,584 TB/s) | **80%**<br>(보수적 접근) |
| **인터커넥트<br>(NVLink ?)** | • 총 ?대 NVLink 스위치 트레이 (GB300과 동일 9대 예상 ※)<br>• 72개 GPU를 단일 거대 메모리 도메인으로 후면 백플레인 직결 | **-** | **260,000 GB/s**<br>(약 260 TB/s ※ NVLink 6 추정) | **100%**<br>(이론 패브릭) |
| **시스템 메모리<br>(SOCAMM)** | • 총 ?개 SOCAMM 패키지 (Grace CPU 32ch 독립 버스 라인 ※)<br>• LPDDR5X 기반, Grace CPU당 32채널 독점 가동<br>• **올바른 수식:** 1,024 GB/s × 2CPU × 18대 × 0.9 | **81,920 GB**<br>(실효 약 80 TB ※) | **16,588.8 GB/s**<br>(약 16.6 TB/s ※) | **90%**<br>(합리적 접근) |
| **풀드 메모리<br>(CXL 3.2)** | • CXL 3.2 Pooled Memory 100TB 확장<br>• SOCAMM 한계 도달 시 2차 확장 단계<br>• PCIe Gen6 기반 | **102,400 GB**<br>(100 TB) | **~3,200 GB/s**<br>(약 3.2 TB/s ※) | **80%**<br>(CXL 3.2 PCIe Gen6 추정) |

---

## 2. R100 3단계 메모리 아키텍처

```
HBM4 (20.7TB)  →  SOCAMM 80TB  →  CXL 3.2 100TB
  ▲x=178        ◆x=940           ×x=1936
  (HBM 초과)    (SOCAMM 초과)    (2차 사망)
```

> **특징**: R100만 **3단계 메모리** (HBM → SOCAMM → CXL) 거침.
> H100/B300은 SOCAMM 없이 HBM → CXL 직접 전환.

---

## 3. 연산 스펙 (TFLOPS)

| 포맷 | TFLOPS (NVL72당) | Rack 합산 (72 GPU) | 비고 |
|---|---|---|---|
| **NVFP4 (초경량 추론)** | **50,000** | 50,000 | Vera Rubin 공식 — 50 PFLOPS |
| FP8 / INT8 (표준 양자화) | ~17,500 | ~17,500 | 추정 — NVFP4 대비 0.35x |
| BF16 / FP16 (지능 보존) | ~17,500 | ~17,500 | 추정 |
| FP32 (전통 일반) | ~950 | ~950 | FP16 대비 ~0.054x |

---

## 4. GB300 대비 R100 핵심 변화 요약

| 항목 | GB300 (Blackwell) | R100 (Vera Rubin) | 변화율 |
|---|---|---|---|
| HBM 타입 | HBM3e | **HBM4** | ↑ |
| HBM 대역폭/GPU | 8.0 TB/s | **22.0 TB/s** | **2.75×** |
| Rack HBM 대역폭 | 460.8 TB/s | **1,584 TB/s** | **3.44×** |
| FP4 추론 | 15,000 TFLOPS | **50,000 TFLOPS** | **3.33×** |
| 시스템 메모리 | LPDDR5X 18TB | **SOCAMM 80TB + CXL 100TB** | 3단계 확장 |
| x=50 TPS/MW | 0.7M | **1.65M** | **2.36×** |
| x=100 TPS/MW | 0.6M | **1.6M (flat)** | **2.67×** (유지력) |
| 랙 전력 | ~121kW | **~199kW** | 1.65× |

---

## 5. 추정치 명시

| 항목 | 근거 | 신뢰도 |
|---|---|---|
| GPU/server (4개), server 수 (18대) | GB300 NVL72와 동일 아키텍처 가정 | 낮음 ※ |
| HBM4 구성 (36GB × 8) | HBM3e (36GB × 8) 계승 가정 | 낮음 ※ |
| HBM4 대역폭 22.0 TB/s | GTC 2026 Jensen Huang 발표 차트 | 높음 ✅ |
| NVLink 6 대역폭 260 TB/s | GB300 NVLink 5 (130 TB/s) 대비 예상 | 낮음 ※ |
| SOCAMM 80TB | v3 분석 사망 지점 역산 기반 | 중간 △ |
| CXL 3.2 대역폭 3.2 TB/s | 산업 벤치마크 기반 | 낮음 ※ |

> ⚠️ R100은 GTC 2026 발표 단계로, NVIDIA 공식 datasheet 미출시. 모든 미인증 값은 ※ 표시.
