# -*- coding: utf-8 -*-
"""
Jensen v3 — Frame (b) wide x=50~2000. 텍스트 없는 깔끔판:
- 그래프 위에는 텍스트/화살표/라벨 전혀 없음
- 오직 곡선 + 약속된 공통 마커(●×▲◆) 포인트만 표시
- 상단에 마커 규칙 범례 1개만 유지 (한눈에 HBM->Main->CXL 흐름)
- 각 마커의 상세 내용은 별도 markdown 테이블로 기술
  -> jensen-huang-chart-v3-b-markers-table.md
Low-res PNG. Korean labels.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ============ v2 solid: x=50~400 ============
xs_v2 = [50, 100, 200, 400]
b300_v2 = [0.70, 0.60, 0.15, 0.07]
r100_v2 = [1.65, 1.60, 0.70, 0.20]
h100_v2 = [0.15, 0.06, np.nan, np.nan]

# ============ Frame (b): x=400~2000, users=x ============
Xb = np.array([400,500,600,700,800,900,1000,1100,1200,1300,
               1400,1500,1600,1700,1800,1900,2000])
def decay(base, x): return base * (400.0/x) ** 0.3

# R100: HBM->SOCAMM x=178, SOCAMM->CXL x=940, 최종사망 x=1936
die_r100_soc = 940; die_r100_cxl = 1936
r100_soc = np.where(Xb <= die_r100_soc, decay(0.20, Xb), np.nan)
r100_cxl = np.where(Xb <= die_r100_cxl, decay(0.20, Xb), np.nan)

# B300: HBM->CXL x=159 (SOCAMM 없음), 최종사망 x=1917
die_b300_cxl = 1917
b300_cxl = np.where(Xb <= die_b300_cxl, decay(0.07, Xb), np.nan)
b300_hbm = np.zeros_like(Xb, dtype=float)

# H100 (x=100조건: Kimi 1T, 10.80GB/u) — HBM->CXL x=52, 사망 x=9311(범위밖)
def h100_decay(x): return 0.06 * (100.0/x) ** 0.3 * 0.9
h100_cxl = h100_decay(Xb)

# ============ Plot ============
fig, ax = plt.subplots(figsize=(16, 9), dpi=100)

# v2 solid
ax.plot(xs_v2, [0.15,0.06,np.nan,np.nan], 'o-', color='#888888', lw=2.2, ms=8,
        label='H100 (v2, x>=200 1차사망)')
ax.plot(xs_v2, b300_v2, 's-', color='#17a2b8', lw=2.2, ms=8, label='B300 (v2 확정)')
ax.plot(xs_v2, r100_v2, 'D-', color='#28a745', lw=2.2, ms=8, label='R100 (v2 확정)')

# Frame (b) dashed
ax.plot(Xb, b300_hbm, 'x--', color='#17a2b8', lw=1.2, ms=6, alpha=0.35,
        label='B300 HBM-only (2차사망 x=159)')
ax.plot(Xb, b300_cxl, 's--', color='#17a2b8', lw=2.0, ms=7, alpha=0.85,
        label='B300+CXL 100TB (2차사망 x=1917)')
ax.plot(Xb, r100_soc, 'D--', color='#28a745', lw=2.0, ms=7, alpha=0.9,
        label='R100+SOCAMM (2차사망 x=940)')
ax.plot(Xb, r100_cxl, 'D--', color='#1a6b2e', lw=1.7, ms=6, alpha=0.75,
        label='R100+CXL 100TB (2차사망 x=1936)')
ax.plot(Xb, h100_cxl, 'o--', color='#666666', lw=1.8, ms=6, alpha=0.8,
        label='H100+CXL (x=100조건, 사망 x=9311 범위밖)')

# ============ 마커: 약속된 공통 표시만 (텍스트 없음) ============
# 1차 사망 (가중치>HBM): 빨간 ●  [H100 x=200, 400]
ax.plot([200, 400], [0.0, 0.0], 'o', color='red', ms=13, markeredgecolor='darkred',
        markeredgewidth=2, zorder=6)
# 2차 사망 (OOM): 검정 ×  [B300 x=159, R100+SOCAMM x=940, B300+CXL x=1917, R100+CXL x=1936]
for d, base in [(159, 0.07), (940, 0.20), (1917, 0.07), (1936, 0.20)]:
    y = decay(base, d) if d >= 400 else 0.0
    ax.plot(d, y, 'X', color='black', markersize=13, markeredgecolor='black',
            markeredgewidth=2.8, zorder=5)
# HBM->SOCAMM/CXL 전환: 주황 ▲  [R100 x=178, B300 x=159, H100 x=52]
ax.plot(178, decay(0.20, 178), '^', color='orange', ms=12, markeredgecolor='darkorange',
        markeredgewidth=2, zorder=6)
ax.plot(159, 0.0, '^', color='orange', ms=12, markeredgecolor='darkorange',
        markeredgewidth=2, zorder=6)
ax.plot(52, 0.0, '^', color='orange', ms=11, markeredgecolor='darkorange',
        markeredgewidth=2, zorder=6)
# SOCAMM->CXL 전환: 보라 ◆  [R100 x=940]
ax.plot(940, decay(0.20, 940), 'D', color='purple', ms=11, markeredgecolor='indigo',
        markeredgewidth=2, zorder=6)

# ============ 표식 규칙 범례 (상단 중앙, 유일한 텍스트) ============
rule_text = (
    "표식 규칙 (메모리 넘침 흐름)\n"
    "● 빨강 = 1차 사망 (가중치 > HBM, 모델 로드 불가)\n"
    "× 검정 = 2차 사망 (OOM: KV > HBM+Main+CXL 전체)\n"
    "▲ 주황 = HBM -> Main Memory(SOCAMM)/CXL 전환\n"
    "◆ 보라 = Main Memory(SOCAMM) -> CXL 전환\n"
    "실선 = v2 확정   점선 = Frame(b) users=x"
)
ax.text(0.5, 0.97, rule_text, transform=ax.transAxes, fontsize=7.5, color='#222',
        ha='center', va='top', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', fc='#f7f7f7', ec='#444', alpha=0.95))

# x=400 divider
ax.axvline(x=400, color='#999', linestyle=':', lw=1.0, alpha=0.6)
ax.text(400, 1.80, 'x=400 (Frame b 시작)', fontsize=6, color='#888', ha='center', style='italic')

# ============ Axes ============
ax.set_xlabel('X: TPS/User  (← 짧은 ctx   긴 ctx →)', fontsize=11)
ax.set_ylabel('Y: TPS/MW (전력당 효율)', fontsize=11)
ax.set_title('젠슨황 v3 — Frame (b) x=50~2000 (단계별 사망 + 메모리 전환 + H100 x=100조건 CXL)',
             fontsize=12, fontweight='bold')
ax.set_xticks([50,100,200,400,600,800,1000,1200,1400,1600,1800,2000])
ax.set_xlim(20, 2080)
ax.set_ylim(-0.05, 1.90)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='center right', fontsize=7, framealpha=0.92, ncol=1)

plt.tight_layout(rect=[0, 0.01, 1, 1])
out = r'c:\Users\2053437\wiki\reference\jensen-huang-chart-v3-b-wide-v2.png'
plt.savefig(out, dpi=110, bbox_inches='tight', facecolor='white')
print('SAVED:', out)

# ============================================================
# 마커 상세 테이블 (markdown) 별도 파일로 출력
# ============================================================
table = r"""# Jensen v3 — Frame (b) 마커 상세 테이블

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
"""
tbl_path = r'c:\Users\2053437\wiki\reference\jensen-huang-chart-v3-b-markers-table.md'
with open(tbl_path, 'w', encoding='utf-8') as f:
    f.write(table)
print('TABLE SAVED:', tbl_path)
