# -*- coding: utf-8 -*-
"""
Jensen v3 — x=400 조건 고정(GPT 2T, 400K, KV 102.40 GB/user) 후 x를 100 단위로 증가.
Frame (a): users 고정(=100) + x 증가 → 하드웨어 한계 도달 → 효율 붕괴(0 수렴)
Frame (b): users = x 증가 → KV = x*102.40GB 폭증 → OOM 사망(단절)
Low-res PNG. Korean labels. 두 패널 나란히 비교.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

X = np.array([400, 500, 600, 700, 800, 900, 1000])
KV_PER_U = 102.40  # GB/user (GPT 2T, 400K)

# ============ FRAME (a): users=100 고정, 효율 = 한계x / 요청x ============
# R100 x=400 chart: 39,800 TPS / 100 users -> 한계 x=398
# B300 x=400 chart: 8,470 / 21 -> 한계 x=403 (but users=21 고정 시)
# 효율(달성율) = min(1, 한계x / x). TPS/MW = 기준 TPS/MW × 달성율
# 기준: x=400 TPS/MW (B300=0.07, R100=0.20), users 고정
limit_r100 = 398.0   # R100 한계 x (39800/100)
limit_b300 = 403.3   # B300 한계 x (8470/21)

def eff_a(limit, x):
    return np.minimum(1.0, limit / x)

b300_a = 0.07 * eff_a(limit_b300, X)      # B300 기준 0.07M
r100_a = 0.20 * eff_a(limit_r100, X)     # R100 기준 0.20M
# H100: x=400부터 N/A (가중치 4TB > HBM 2.56TB) — 전 구간 0
h100_a = np.zeros_like(X, dtype=float)

# ============ FRAME (b): users = x, KV = x*102.40 → OOM ============
# 사망 x: B300+CXL=1136, R100+SOCAMM=940, R100+CXL=1917
# H100: 가중치 불가 → 전 구간 사망(0)
# B300 HBM-only: 사망 x=159 → x=400부터 이미 사망(0)
# B300+CXL: 사망 x=1136 → x=400~800 OK, x=900~1000 사망
# R100 SOCAMM: 사망 x=940 → x=400~800 OK, x=900+ 사망
# R100+CXL: 사망 x=1917 → x=400~1000 전부 OK
die_b300_cxl = 1136
die_r100_socamm = 940
die_r100_cxl = 1917

# TPS/MW: 용량 여부와 무관하게 x 증가 시 완만 하강(차트 추세 유지 가정)
# 기준 0.07/0.20M @ x=400, x↑ 시 약간 하강 (compute-bound 완만)
def decay(base, x):
    return base * (400.0 / x) ** 0.3   # 완만 하강

b300_cxl_b = np.where(X <= die_b300_cxl, decay(0.07, X), np.nan)
r100_socamm_b = np.where(X <= die_r100_socamm, decay(0.20, X), np.nan)
r100_cxl_b = np.where(X <= die_r100_cxl, decay(0.20, X), np.nan)
h100_b = np.zeros_like(X, dtype=float)         # 전 구간 사망
b300_hbm_b = np.zeros_like(X, dtype=float)      # x=400부터 사망

# ============ Plot: 2 panels ============
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), dpi=100)

# ---------- Panel (a) ----------
ax1.set_title('Frame (a): 사용자 수 고정(=100) + x 증가\n→ 효율 붕괴 (사망 지점 없음, 0 수렴)',
              fontsize=11, fontweight='bold')
ax1.plot(X, h100_a, 'o--', color='#888888', linewidth=1.8, markersize=7,
         label='H100 (x=400 N/A, 전 구간 사망)')
ax1.plot(X, b300_a, 's-', color='#17a2b8', linewidth=2.2, markersize=8,
         label='B300 (한계 x=403)')
ax1.plot(X, r100_a, 'D-', color='#28a745', linewidth=2.2, markersize=8,
         label='R100 (한계 x=398)')
# annotations
for xi in X:
    ax1.annotate(f'u=100\nx={xi}', xy=(xi, 0.20*eff_a(limit_r100, xi)),
                 xytext=(0, 10), textcoords='offset points',
                 fontsize=5.8, color='#28a745', ha='center',
                 bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#28a745', alpha=0.8))
ax1.set_xlabel('X: TPS/User (1인당 속도 요구)', fontsize=10)
ax1.set_ylabel('Y: TPS/MW (달성 효율)', fontsize=10)
ax1.set_xticks(X)
ax1.set_ylim(-0.02, 0.25)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend(loc='upper right', fontsize=8)
ax1.text(700, 0.22, 'x=400 조건 고정\nGPT 2T / 400K / 102.4GB/u',
         fontsize=8, color='#555', ha='center', style='italic',
         bbox=dict(fc='lightyellow', ec='#cc9', alpha=0.9))

# ---------- Panel (b) ----------
ax2.set_title('Frame (b): 사용자 수 = x 증가 → KV=x×102.4GB 폭증\n→ OOM 사망 (단절 지점 존재)',
              fontsize=11, fontweight='bold')
ax2.plot(X, h100_b, 'o--', color='#888888', linewidth=1.8, markersize=7,
         label='H100 (가중치 불가, 전 구간 사망)')
ax2.plot(X, b300_hbm_b, 'x--', color='#17a2b8', linewidth=1.5, markersize=8,
         alpha=0.5, label='B300 HBM-only (x=159 사망)')
ax2.plot(X, b300_cxl_b, 's-', color='#17a2b8', linewidth=2.2, markersize=8,
         label='B300+CXL 100TB (사망 x=1136)')
ax2.plot(X, r100_socamm_b, 'D-', color='#28a745', linewidth=2.2, markersize=8,
         label='R100+SOCAMM 80TB (사망 x=940)')
ax2.plot(X, r100_cxl_b, 'D--', color='#1a6b2e', linewidth=1.8, markersize=7,
         alpha=0.8, label='R100+CXL 100TB (사망 x=1917, 그래프 내 생존)')
# 사망 단절 마킹
for die, base, color, name in [(1136, 0.07, '#17a2b8', 'B300+CXL'),
                                (940, 0.20, '#28a745', 'R100+SOCAMM')]:
    if die in X:
        ax2.plot(die, decay(base, die), 'x', color=color, markersize=14, markeredgewidth=3)
        ax2.annotate(f'{name}\n사망 x={die}\nKV={die*102.4/1000:.0f}TB',
                     xy=(die, decay(base, die)), xytext=(-40, 25),
                     textcoords='offset points', fontsize=7, color=color,
                     fontweight='bold', ha='center',
                     arrowprops=dict(arrowstyle='->', color=color, lw=1.2),
                     bbox=dict(fc='white', ec=color, alpha=0.9))
# user/KV annotations on R100+SOCAMM
for xi in [400, 500, 600, 700, 800]:
    y = decay(0.20, xi)
    ax2.annotate(f'u={xi}\nKV={xi*102.4/1000:.0f}TB', xy=(xi, y),
                 xytext=(0, 12), textcoords='offset points',
                 fontsize=5.8, color='#28a745', ha='center', fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#28a745', alpha=0.85))
ax2.set_xlabel('X: TPS/User (= 동시 사용자 수, users=x)', fontsize=10)
ax2.set_ylabel('Y: TPS/MW (단절 시 NaN)', fontsize=10)
ax2.set_xticks(X)
ax2.set_ylim(-0.02, 0.25)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.legend(loc='upper right', fontsize=7.5)
ax2.text(800, 0.22, 'x=400 조건 고정\nGPT 2T / 400K / 102.4GB/u',
         fontsize=8, color='#555', ha='center', style='italic',
         bbox=dict(fc='lightyellow', ec='#cc9', alpha=0.9))

fig.suptitle('젠슨황 v3 — x=400 조건 고정 후 x를 100 단위로 증가 (R100 사망 조건까지)',
             fontsize=13, fontweight='bold', y=0.98)
fig.text(0.5, 0.01,
         '(a) 사용자 고정 = 효율 붕괴(0 수렴, 사망 지점 無) · '
         '(b) 사용자=x 증가 = OOM 사망(단절 지점 確認: B300+CXL x=1136, R100+SOCAMM x=940)',
         ha='center', fontsize=8.5, color='#555', style='italic')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
out = r'c:\Users\2053437\wiki\reference\jensen-huang-chart-v3-xstep.png'
plt.savefig(out, dpi=110, bbox_inches='tight', facecolor='white')
print('SAVED:', out)
