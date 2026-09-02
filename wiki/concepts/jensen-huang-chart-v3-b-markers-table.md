# Jensen v3 — Frame (b) 마커 상세 테이블

> 그래프(`jensen-huang-chart-v3-b-wide-v2.png`)에는 약속된 공통 마커(●×▲◆)만
> 포인트로 표시하고, 모든 텍스트 설명은 이 테이블로 분리했다.

## 마커 규칙 (공통 표시)

| 마커 | 색 | 의미 |
|---|---|---|
| ● | 빨강 | 1차 사망 — 가중치 > HBM, 모델 로드 불가 (0 TPS) |
| × | 검정 | 2차 사망 — OOM: KV > HBM + Main Memory + CXL 전체 |
| ▲ | 주황 | HBM → Main Memory(SOCAMM) / CXL 전환 (KV가 HBM 한계 초과) |
| ◆ | 보라 | Main Memory(SOCAMM) → CXL 전환 (SOCAMM 한계 도달) |

---

## GPU 세대별 마커 위치

### H100 (HBM3 80GB×32 = 2.56TB, 3.35 TB/s, ~40kW)
> x=100 조건 고정 (Kimi 1T 가중치 2TB, 10.80 GB/user)

| 마커 | x 위치 | 메모리 총량 | 내용 |
|---|---|---|---|
| ▲ | 52 | 2TB (HBM 2.56TB 한계 도달) | HBM → CXL 전환. KV가 HBM 한계 초과해 CXL 100TB 풀로 넘침 |
| ● | 200 | — | 1차 사망. 가중치 4TB > HBM 2.56TB → 모델 로드 불가, 0 TPS (v2 지점) |
| ● | 400 | — | 1차 사망. 동일 원인, 더 긴 ctx (v2 끝점) |
| × | 9311 (범위밖) | 100TB (CXL) | 2차 사망. CXL 100TB로도 KV 수용 불가 → OOM (그래프 범위 밖) |

### B300 NVL72 (HBM3e 288GB×72 = 20.7TB, 8.0 TB/s, ~121kW)
> SOCAMM 없음 — HBM 한계 도달 시 곧장 CXL 100TB 풀로 전환

| 마커 | x 위치 | 메모리 총량 | 내용 |
|---|---|---|---|
| ▲ | 159 | 16TB | HBM → CXL 전환. SOCAMM 단계 없이 HBM 한계 초과 시 직접 CXL |
| × | 1917 | 196TB (HBM 20.7TB + CXL ~175TB) | 2차 사망. CXL 100TB 풀 + HBM으로도 KV 수용 불가 → OOM |

### R100 Vera Rubin NVL72 (HBM4 288GB×72 = 20.7TB, 22.0 TB/s, ~199kW)
> 3단계 메모리: HBM → SOCAMM 80TB → CXL 100TB

| 마커 | x 위치 | 메모리 총량 | 내용 |
|---|---|---|---|
| ▲ | 178 | 18TB | HBM → SOCAMM 전환. KV가 HBM 20.7TB 한계 초과 → SOCAMM 80TB 풀로 넘침 |
| ◆ | 940 | 96TB (HBM + SOCAMM 80TB 한계 도달) | SOCAMM → CXL 전환. SOCAMM 80TB 한계 도달 → CXL 100TB 풀로 넘침 |
| × | 940 | 96TB | 2차 사망 (R100+SOCAMM). SOCAMM 한계 도달 시점 = 전환점과 동일. CXL 연장 전 사망 |
| × | 1936 | 198TB (HBM + SOCAMM 80TB + CXL 100TB) | 2차 사망 (R100+CXL). CXL 100TB까지 합쳐도 KV 수용 불가 → 최종 OOM |

---

## 메모리 넘침 흐름 한눈에 보기

```
H100:   HBM 2.56TB ──▲(x=52)──> CXL 100TB ──×(x=9311, 범위밖)
B300:   HBM 20.7TB ──▲(x=159)─> CXL 100TB ──×(x=1917)
R100:   HBM 20.7TB ──▲(x=178)─> SOCAMM 80TB ──◆(x=940)─> CXL 100TB ──×(x=1936)
```

> R100만 3단계(SOCAMM 포함). H100·B300은 SOCAMM 없이 HBM→CXL 직접 전환.
> 1차 사망 ●은 H100 전용(B300·R100은 가중치가 HBM 안에 들어옴).
