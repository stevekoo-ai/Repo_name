"""Rendering: the investment clock face image and history trend charts."""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

from .model import PHASES, ClockReading

QUADRANT_ORDER = [12, 3, 6, 9]  # clockwise starting at top


def _hour_to_angle_deg(hour: int) -> float:
    """Convert a clock hour (12/3/6/9) to a math angle in degrees, 0=east, CCW+."""
    # 12 o'clock -> 90 (up), 3 -> 0 (right), 6 -> -90 (down), 9 -> 180 (left)
    return {12: 90, 3: 0, 6: -90, 9: 180}[hour]


def draw_clock(reading: ClockReading, out_path: str | Path, size: int = 900) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 6), dpi=size // 6)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")

    phase_by_hour = {p["hour"]: p for p in PHASES.values()}
    active_hour = reading.phase["hour"]

    # Quadrant wedges
    for hour in QUADRANT_ORDER:
        p = phase_by_hour[hour]
        center_deg = _hour_to_angle_deg(hour)
        theta1, theta2 = center_deg - 45, center_deg + 45
        is_active = hour == active_hour
        wedge = mpatches.Wedge(
            (0, 0), 1.05, theta1, theta2,
            facecolor=p["color"], alpha=0.85 if is_active else 0.25,
            edgecolor="white", linewidth=2,
        )
        ax.add_patch(wedge)
        label_r = 0.65
        rad = math.radians(center_deg)
        lx, ly = label_r * math.cos(rad), label_r * math.sin(rad)
        ax.text(
            lx, ly, f"{p['name']}\n({p['asset']})",
            ha="center", va="center", fontsize=11,
            fontweight="bold" if is_active else "normal",
            color="white" if is_active else "#333333",
        )

    # Outer ring + hour ticks at 12/3/6/9
    circle = plt.Circle((0, 0), 1.05, fill=False, edgecolor="#222222", linewidth=2)
    ax.add_patch(circle)
    for hour in QUADRANT_ORDER:
        rad = math.radians(_hour_to_angle_deg(hour))
        x1, y1 = 1.0 * math.cos(rad), 1.0 * math.sin(rad)
        x2, y2 = 1.1 * math.cos(rad), 1.1 * math.sin(rad)
        ax.plot([x1, x2], [y1, y2], color="#222222", linewidth=2)

    # Hour hand pointing at the active phase
    rad = math.radians(_hour_to_angle_deg(active_hour))
    hx, hy = 0.75 * math.cos(rad), 0.75 * math.sin(rad)
    ax.annotate(
        "", xy=(hx, hy), xytext=(0, 0),
        arrowprops=dict(arrowstyle="-|>", color="#111111", lw=4, mutation_scale=25),
    )
    ax.add_patch(plt.Circle((0, 0), 0.04, color="#111111", zorder=5))

    ax.set_title(
        f"Investment Clock — {reading.phase['name']} phase\n"
        f"Best asset: {reading.phase['asset']}",
        fontsize=13, fontweight="bold", pad=10,
    )

    fig.tight_layout()
    fig.savefig(out_path, facecolor="white")
    plt.close(fig)
    return out_path


def draw_trend_charts(history: pd.DataFrame, out_dir: str | Path) -> dict[str, Path]:
    """Draw growth and inflation trend line charts from the accumulated history table."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    if history.empty:
        return paths

    plot_df = history.drop_duplicates(subset=["data_asof"], keep="last").sort_values("data_asof")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(plot_df["data_asof"], plot_df["growth_value"], color="#4C72B0", marker="o", markersize=3)
    ax.axhline(0, color="#999999", linewidth=1, linestyle="--")
    ax.set_title("Growth proxy (OECD CLI / Industrial Production)")
    ax.set_ylabel("Index level")
    fig.autofmt_xdate()
    fig.tight_layout()
    growth_path = out_dir / "trend_growth.png"
    fig.savefig(growth_path)
    plt.close(fig)
    paths["growth"] = growth_path

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(plot_df["data_asof"], plot_df["inflation_yoy"], color="#C44E52", marker="o", markersize=3)
    ax.axhline(2.0, color="#999999", linewidth=1, linestyle="--", label="2% target")
    ax.set_title("CPI YoY (%)")
    ax.set_ylabel("% YoY")
    ax.legend(loc="upper left", fontsize=8)
    fig.autofmt_xdate()
    fig.tight_layout()
    inflation_path = out_dir / "trend_inflation.png"
    fig.savefig(inflation_path)
    plt.close(fig)
    paths["inflation"] = inflation_path

    return paths
