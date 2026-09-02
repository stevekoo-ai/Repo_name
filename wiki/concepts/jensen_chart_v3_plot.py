# -*- coding: utf-8 -*-
"""
Jensen Huang Inference Economics Chart v3
- Solid lines: v2 original 12 points (x=50,100,200,400)
- Extended x=800: v3 capacity-planning scenario
- Dashed lines: CXL 3.2 100TB Pooled DRAM effect (v3)
Labels in Korean. Low-resolution PNG to conserve context.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# Korean font (Windows Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ---------- Data ----------
x = [50, 100, 200, 400, 800]

# v2 solid (확정 판독값) — H100 x=200/400/800 = N/A
h100 = [0.15, 0.06, np.nan, np.nan, np.nan]
b300 = [0.70, 0.60, 0.15, 0.07, np.nan]   # x=800: OOM (단절)
r100 = [1.65, 1.60, 0.70, 0.20, np.nan]   # x=800: spill 무너짐 (단절)

# v3 CXL dashed (추정치 — 라벨 명시)
# H100+CXL: x=50/100 ~20% down(전력), x=200/400 저TPS 부활, x=800=0(사망)
h100_cxl = [0.12, 0.048, 0.025, 0.015, 0.0]
# B300+CXL: 전구간 ~7% down + x=800 부활(가파른 저TPS)
b300_cxl = [0.65, 0.56, 0.14, 0.065, 0.018]
# R100+CXL: x=50~400 미세 down + x=800 완만 하강 방어
r100_cxl = [1.60, 1.55, 0.68, 0.19, 0.06]

# ---------- Plot ----------
fig, ax = plt.subplots(figsize=(11, 7), dpi=100)

# Solid (v2 original)
ax.plot([50,100,200,400], [0.15,0.06,np.nan,np.nan], 'o-', color='#888888',
        linewidth=2.2, markersize=8, label='H100 Hopper (v2, 확정)')
ax.plot([50,100,200,400], [0.70,0.60,0.15,0.07], 's-', color='#17a2b8',
        linewidth=2.2, markersize=8, label='B300 Blackwell NVL72 (v2, 확정)')
ax.plot([50,100,200,400], [1.65,1.60,0.70,0.20], 'D-', color='#28a745',
        linewidth=2.2, markersize=8, label='R100 Vera Rubin NVL72 (v2, 확정)')

# Dashed (v3 CXL effect — 추정)
ax.plot(x, h100_cxl, '^--', color='#888888', linewidth=1.8, markersize=7,
        alpha=0.75, label='H100 + CXL 100TB (v3 추정)')
ax.plot(x, b300_cxl, 'v--', color='#17a2b8', linewidth=1.8, markersize=7,
        alpha=0.75, label='B300 + CXL 100TB (v3 추정)')
ax.plot(x, r100_cxl, 'p--', color='#28a745', linewidth=1.8, markersize=7,
        alpha=0.75, label='R100 + CXL 100TB (v3 추정)')

# ---------- v2 solid point annotations: ctx / users / TPS ----------
# Format: "ctx\nu=users\ntps=TPS"
def ann(gpu, pts, mw, color, dy):
    for xi, ypm in pts.items():
        if ypm is None:
            continue
        tps = ypm*1e6*mw
        u = tps/xi
        ctx = {50:'32K',100:'128K',200:'128K',400:'400K'}[xi]
        ax.annotate(f'{ctx}\nu={u:,.0f}\n{tps/1000:.0f}k TPS',
                    xy=(xi, ypm), xytext=(0, dy), textcoords='offset points',
                    fontsize=6.3, color=color, ha='center', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=color, alpha=0.85))

ann('H100', {50:0.15,100:0.06}, 0.040, '#555', -32)   # below
ann('B300', {50:0.70,100:0.60,200:0.15,400:0.07}, 0.121, '#17a2b8', -32)  # below
ann('R100', {50:1.65,100:1.60,200:0.70,400:0.20}, 0.199, '#28a745', 12)   # above (top curve)

# x=800 divider
ax.axvline(x=800, color='red', linestyle=':', linewidth=1.5, alpha=0.6)
ax.text(810, 1.55, 'x=800\n초가혹 확장\n(v3 신규)', color='red',
        fontsize=9, va='top', fontweight='bold')

# N/A annotation for H100 x=200/400
ax.annotate('H100 N/A\n(회색선·미지원)', xy=(300, 0.03), fontsize=8,
            color='#555555', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#888', alpha=0.85))

# B300/R100 x=800 OOM break marker
ax.plot(800, 0.07, 'x', color='#17a2b8', markersize=12, markeredgewidth=3)
ax.plot(800, 0.20, 'x', color='#28a745', markersize=12, markeredgewidth=3)
ax.text(780, 0.30, 'B300/R100\nx=800 OOM 단절\n(CXL 없으면)', fontsize=7.5,
        color='#444', ha='right', style='italic')

# CXL save annotation at x=800
ax.annotate('CXL 부활\nB300: 452명\nR100: 770명', xy=(800, 0.018),
            xytext=(720, 0.10), fontsize=8, color='#b8860b',
            arrowprops=dict(arrowstyle='->', color='#b8860b', lw=1.2),
            ha='center', fontweight='bold')

# ---------- v3 CXL dashed x=800 annotations (용량 계획: 500명 목표 기준) ----------
# x=800: ctx=1M, 목표 500명, KV 128TB → CXL 부활 지점
ax.annotate('1M\nu=500\n(CXL 부활)', xy=(800, 0.018),
            xytext=(0, -30), textcoords='offset points',
            fontsize=6.3, color='#17a2b8', ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#17a2b8', alpha=0.85))
ax.annotate('1M\nu=500\n(770명 방어)', xy=(800, 0.06),
            xytext=(0, 10), textcoords='offset points',
            fontsize=6.3, color='#28a745', ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#28a745', alpha=0.85))

# H100 death at x=800
ax.annotate('H100 사망\n(Gen5 64GB/s\n5TB 못 끌어옴)', xy=(800, 0.0),
            xytext=(800, -0.12), fontsize=7.5, color='#c0392b',
            ha='center', fontweight='bold')

# Axes
ax.set_xlabel('X: TPS/User (Interactivity)  ←  짧은 ctx    긴 ctx  →', fontsize=11)
ax.set_ylabel('Y: TPS/MW (전력당 효율)', fontsize=11)
ax.set_title('젠슨황 Inference Economics — v2 확정 + v3 CXL 100TB 확장 (x=800)',
             fontsize=13, fontweight='bold')
ax.set_xticks([50, 100, 200, 400, 800])
ax.set_xticklabels(['x=50\nFree\n32K', 'x=100\nMedium\n128K', 'x=200\nHigh\n128K',
                    'x=400\nPremium\n400K', 'x=800\n초가혹\n1M'])
ax.set_xlim(20, 880)
ax.set_ylim(-0.18, 1.85)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper right', fontsize=8.5, framealpha=0.92)

# Footnote
fig.text(0.5, 0.01,
         '실선 = v2 이미지 확정 판독값 · 점선 = v3 CXL 3.2 PCIe Gen6 100TB 효과 [추정] · '
         'x=800 = 용량 계획 시나리오(5T/1M-ctx, 256GB/user) · 핵심: "용량은 CXL, 효율은 R100"',
         ha='center', fontsize=8, color='#555', style='italic')

plt.tight_layout(rect=[0, 0.03, 1, 1])
out = r'c:\Users\2053437\wiki\reference\jensen-huang-chart-v3-graph.png'
plt.savefig(out, dpi=110, bbox_inches='tight', facecolor='white')
print('SAVED:', out)
