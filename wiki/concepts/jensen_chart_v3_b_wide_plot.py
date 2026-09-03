# -*- coding: utf-8 -*-
"""
Jensen v3 — Frame (b) wide: x=50 부터 x=2000 까지.
x=50~400: v2 확정 실선 (12포인트 판독값) + 기존 점선(CXL 전력 오버헤드) 참고용
x=400~2000: Frame (b) — users=x 증가, KV=x*102.40GB → OOM 사망(단절)
조건: x=400 기준 고정 (GPT 2T, 400K, 102.40 GB/user)을 x=400 이후에도 유지.
Low-res PNG. Korean labels.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

KV400 = 102.40  # GB/user @ x=400 (GPT 2T, 400K) — x=400 이후 고정 조건

# ============ v2 solid: x=50~400 (확정 판독) ============
xs_v2 = [50, 100, 200, 400]
h100_v2 = [0.15, 0.06, np.nan, np.nan]
b300_v2 = [0.70, 0.60, 0.15, 0.07]
r100_v2 = [1.65, 1.60, 0.70, 0.20]

# ============ Frame (b): x=400~2000, users=x → KV=x*KV400 → OOM ============
Xb = np.array([400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300,
               1400, 1500, 1600, 1700, 1800, 1900, 2000])
# 가용 KV(GB)와 사망 x
# H100: 가중치 4TB > HBM 2.56TB → 전 구간 사망(0)
# B300 HBM-only 16.3TB → 사망 x=159 (x=400부터 이미 사망)
# B300+CXL 100TB → 116.3TB → 사망 x=1136
# R100+SOCAMM 80TB → 96.3TB → 사망 x=940
# R100+CXL 100TB → 196.3TB → 사망 x=1917
die = {'b300_cxl': 116300/KV400, 'r100_socamm': 96300/KV400, 'r100_cxl': 196300/KV400}
# decay: x↑ 시 완만 하강 (compute-bound, 0.07/0.20M 기준)
def decay(base, x): return base * (400.0/x) ** 0.3

b300_cxl  = np.where(Xb <= die['b300_cxl'],  decay(0.07, Xb), np.nan)
r100_soc  = np.where(Xb <= die['r100_socamm'], decay(0.20, Xb), np.nan)
r100_cxl  = np.where(Xb <= die['r100_cxl'],   decay(0.20, Xb), np.nan)
h100_b    = np.zeros_like(Xb, dtype=float)        # 전 구간 사망
b300_hbm  = np.zeros_like(Xb, dtype=float)        # x=400부터 사망

# ============ Plot ============
fig, ax = plt.subplots(figsize=(13, 7.5), dpi=100)

# v2 solid (x=50~400) — 확정
ax.plot(xs_v2, [0.15,0.06,np.nan,np.nan], 'o-', color='#888888', lw=2.2, ms=8, label='H100 (v2 확정, x≥200 N/A)')
ax.plot(xs_v2, b300_v2, 's-', color='#17a2b8', lw=2.2, ms=8, label='B300 (v2 확정)')
ax.plot(xs_v2, r100_v2, 'D-', color='#28a745', lw=2.2, ms=8, label='R100 (v2 확정)')

# Frame (b) dashed (x=400~2000)
ax.plot(Xb, h100_b, 'o--', color='#888888', lw=1.6, ms=6, alpha=0.6, label='H100 (Frame b, 전 구간 사망)')
ax.plot(Xb, b300_hbm, 'x--', color='#17a2b8', lw=1.3, ms=7, alpha=0.4, label='B300 HBM-only (x=159 사망)')
ax.plot(Xb, b300_cxl, 's--', color='#17a2b8', lw=2.0, ms=7, alpha=0.85, label='B300+CXL 100TB (사망 x=1136)')
ax.plot(Xb, r100_soc, 'D--', color='#28a745', lw=2.0, ms=7, alpha=0.9, label='R100+SOCAMM 80TB (사망 x=940)')
ax.plot(Xb, r100_cxl, 'D--', color='#1a6b2e', lw=1.7, ms=6, alpha=0.75, label='R100+CXL 100TB (사망 x=1917)')

# ============ v2 point annotations (x=50~400) ============
ctx = {50:'32K',100:'128K',200:'128K',400:'400K'}
mw = {'H100':0.040,'B300':0.121,'R100':0.199}
v2pts = {'H100':{50:0.15,100:0.06},'B300':{50:0.70,100:0.60,200:0.15,400:0.07},'R100':{50:1.65,100:1.60,200:0.70,400:0.20}}
for gpu,pts in v2pts.items():
    for xi,ypm in pts.items():
        tps=ypm*1e6*mw[gpu]; u=tps/xi
        dy = 12 if gpu=='R100' else -30
        col = {'H100':'#555','B300':'#17a2b8','R100':'#28a745'}[gpu]
        ax.annotate(f'{ctx[xi]}\nu={u:,.0f}\n{tps/1000:.0f}k', xy=(xi,ypm),
                    xytext=(0,dy), textcoords='offset points', fontsize=5.5, color=col,
                    ha='center', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.15', fc='white', ec=col, alpha=0.85))

# ============ Frame (b) 사망 마킹 + 주석 ============
for d, base, color, name in [(1136, 0.07, '#17a2b8', 'B300+CXL'),
                              (940, 0.20, '#28a745', 'R100+SOCAMM'),
                              (1917, 0.20, '#1a6b2e', 'R100+CXL')]:
    y = decay(base, d)
    ax.plot(d, y, 'X', color=color, markersize=14, markeredgewidth=2.5, zorder=5)
    ax.annotate(f'{name}\n사망 x={d}\nKV={d*KV400/1000:.0f}TB\nu={d}',
                xy=(d, y), xytext=(15, -30 if 'R100' in name else 25),
                textcoords='offset points', fontsize=7, color=color, fontweight='bold',
                ha='left', arrowprops=dict(arrowstyle='->', color=color, lw=1.2),
                bbox=dict(fc='white', ec=color, alpha=0.9))

# Frame (b) user/KV annotations on R100+SOCAMM (x=400~800)
for xi in [500, 600, 700, 800]:
    y = decay(0.20, xi)
    ax.annotate(f'u={xi}\nKV={xi*KV400/1000:.0f}T', xy=(xi, y),
                xytext=(0, 10), textcoords='offset points', fontsize=5.3, color='#28a745',
                ha='center', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='#28a745', alpha=0.85))

# x=400 transition divider
ax.axvline(x=400, color='#999', linestyle=':', lw=1.2, alpha=0.7)
ax.text(410, 1.55, 'x=400 이후\nFrame (b)\nusers=x 증가', fontsize=8, color='#555',
        va='top', style='italic')

# ============ Axes ============
ax.set_xlabel('X: TPS/User  (← 짧은 ctx   긴 ctx →)', fontsize=11)
ax.set_ylabel('Y: TPS/MW (전력당 효율)', fontsize=11)
ax.set_title('젠슨황 v3 — Frame (b): x=50~2000 확장 (users=x → OOM 사망)',
             fontsize=13, fontweight='bold')
ax.set_xticks([50,100,200,400,600,800,1000,1200,1400,1600,1800,2000])
ax.set_xlim(20, 2050)
ax.set_ylim(-0.05, 1.85)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper right', fontsize=7.8, framealpha=0.92, ncol=2)

fig.text(0.5, 0.01,
         '실선 = v2 확정 (x=50~400) · 점선 = Frame (b) users=x 증가 → KV=x×102.4GB 폭증 → OOM 단절 · '
         '사망: B300+CXL x=1136, R100+SOCAMM x=940, R100+CXL x=1917',
         ha='center', fontsize=8.5, color='#555', style='italic')

plt.tight_layout(rect=[0, 0.03, 1, 1])
out = r'c:\Users\2053437\wiki\reference\jensen-huang-chart-v3-b-wide.png'
plt.savefig(out, dpi=110, bbox_inches='tight', facecolor='white')
print('SAVED:', out)
