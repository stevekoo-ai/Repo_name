"""
Tracks cumulative progress toward the "앞으로 확인되는 모든 공공분양에 대해
15건까지, 모집공고를 직접 열어서 60㎡ 초과 일반공급 소득 무관 여부를 확인"
goal (사용자 요청, 2026-09-13).

Design: every listing judge_listings() produces (국민주택, 서울/경기, currently
open) is a review candidate — not just the personal-interest keyword matches
(플랫폼시티/광교/원천동) that income_analysis.py originally targeted. The first
REVIEW_CAP distinct listings we encounter (by id, first-seen order across
cron runs) each get their 모집공고문 opened once via
income_analysis.analyze_listing() and recorded here, whether that attempt
succeeds or fails — a failed attempt (PDF not found, parser mismatch, etc.)
still consumed one look at the notice and is reported as such, matching
income_analysis.py's own graceful-degradation philosophy (a human looks at
the failures instead of an endless silent retry loop). Once REVIEW_CAP is
reached, no further listings are opened — the pipeline reports the final
tally and stops.

State persists in income_review_state.json (tracked by git, same append/
persist pattern as alerted_state.json) so progress survives across the
30-min cron runs and across workflow re-runs.

📚 Classification rules: wiki/concepts/public-housing-income-requirement-framework.md
   (this tracker only decides *whether/when* to look; income_analysis.py
   decides *what the notice says*).
"""

from __future__ import annotations

import json
import os
from datetime import datetime

REVIEW_CAP = 15

STATE_PATH = os.path.join(os.path.dirname(__file__), "income_review_state.json")


def load_state() -> dict:
    if not os.path.exists(STATE_PATH):
        return {"count": 0, "reviews": []}
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"count": data.get("count", 0), "reviews": data.get("reviews", [])}


def save_state(state: dict) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def is_complete(state: dict) -> bool:
    return state["count"] >= REVIEW_CAP


def already_reviewed(state: dict, listing_id: str) -> bool:
    return any(r["id"] == listing_id for r in state["reviews"])


def record(
    state: dict,
    listing_id: str,
    name: str,
    region: str,
    keyword: str | None,
    now_kst: datetime,
    analysis: dict,
) -> dict:
    """Append one review result and bump the counter in place. Returns the
    entry just recorded (for immediate use composing a notification)."""
    entry = {
        "id": listing_id,
        "name": name,
        "region": region,
        "keyword": keyword,
        "reviewed_at": now_kst.strftime("%Y-%m-%d %H:%M KST"),
        "status": analysis.get("status"),
        "business_type": analysis.get("business_type"),
        "income_scope": analysis.get("income_scope"),
        "exceptions": analysis.get("exceptions") or [],
        "reason": analysis.get("reason"),
        "pdf_url": analysis.get("pdf_url"),
    }
    state["reviews"].append(entry)
    state["count"] = len(state["reviews"])
    return entry


def progress_label(state: dict) -> str:
    return f"{min(state['count'], REVIEW_CAP)}회/{REVIEW_CAP}회"


def exception_count(state: dict) -> int:
    return sum(1 for r in state["reviews"] if r.get("exceptions"))
