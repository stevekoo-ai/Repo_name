"""상황 보고 — 정규 브리핑을 쓰지 않는 날에도 사용자에게 반드시 가는 메일.

2026-09-24 사용자: "모든 보고서는 조용히 발행하지 않는 게 아니라!! 내게 상황을
알려야지! 어떤 문제인지, 그리고 그 문제 외에 보고할 수 있는 내용으로 메일을
쓰는 것으로 하라." (원칙: wiki/concepts/report-delivery-policy.md)

그 전까지 브리핑은 휴장일·"조용한 날"이면 아무것도 발행하지 않고 끝났다 —
2026-09-24(추석 연휴)에는 아침·저녁 브리핑이 둘 다 사라졌는데 사용자는 이유를
알 수 없었다. 이 모듈은 그런 날의 대체 보고서를 **코드로** 만든다(LLM 호출 없음,
토큰 0): ①왜 정규 브리핑이 없는지 ②그래도 보고할 수 있는 것(데이터 헬스,
하이닉스 실측, 자금계획 경보, 병목 추적, 다가오는 일정, 예측 원장).
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
BRIEF_DIR = REPO / "report" / "briefing"
KST = timezone(timedelta(hours=9))
SLOT_LABEL = {"AM": "아침 브리핑", "PM": "저녁 브리핑", "WEEKEND": "주간 전망"}
NEXT_SLOT = {"AM": "오늘 저녁 브리핑(19:40 KST)", "PM": "다음 거래일 아침 브리핑(08:00 KST)",
             "WEEKEND": "다음 주 월요일 아침 브리핑(08:00 KST)"}


def kr_holiday_name(d: date) -> str | None:
    """한국 증시 휴장이면 그 이름(주말이면 '주말'), 아니면 None."""
    from engine.briefing import calendar as C

    if C.is_trading_day("KR", d):
        return None
    if d.weekday() >= 5:
        return "주말"
    try:
        doc = yaml.safe_load(C._HOLIDAY_FILE.read_text(encoding="utf-8")) or {}
        for r in doc.get("KR", []):
            if r.get("date") == d.isoformat():
                return r.get("name") or "휴장일"
    except OSError:
        pass
    return "휴장일"


def skip_reason(slot: str, as_of: date, gate) -> str | None:
    """정규 브리핑을 쓰지 않을 이유. 없으면 None(= 정규 발행)."""
    if slot in ("AM", "PM"):
        hol = kr_holiday_name(as_of)
        if hol:
            what = "오늘 한국장 전망" if slot == "AM" else "오늘 한국장 정리"
            return (f"오늘({as_of.isoformat()})은 한국 증시 휴장({hol})이라 "
                    f"정규 브리핑의 '{what}'은 의미가 없습니다.")
    if gate is not None and not gate.publish:
        return ("오늘은 발행 기준에 해당하는 움직임이 없었습니다 — 나스닥·원/달러 1일 ±1% 이상, "
                "검증일이 도래한 예측, 자금계획 CDP·매도 기한, 데이터 헬스 critical 중 "
                "어느 것도 해당하지 않습니다(조용한 날).")
    return None


def _for_reader(body: str) -> str:
    """팩 블록에는 브리핑 작성 LLM에게 주는 지시문("~에 반드시 반영할 것")이 섞여 있다.
    사람에게 가는 상황 보고에선 그 줄을 뺀다."""
    keep = [ln for ln in body.splitlines()
            if not (ln.lstrip().startswith(">") and ("반영할 것" in ln or "옮기지 말고" in ln))]
    return "\n".join(keep)


def _safe(builder, *args) -> tuple[str, str]:
    try:
        b = builder(*args)
        return b.title, _for_reader(b.body)
    except Exception as exc:  # noqa: BLE001 — 한 블록 실패로 상황 보고 전체가 죽으면 안 된다
        return getattr(builder, "__name__", "블록"), f"(생성 실패: {type(exc).__name__}: {exc})"


def build_status_markdown(title: str, heading: str, problem_lines: list[str],
                          next_line: str | None, calendar_slot: str = "AM",
                          as_of: date | None = None, extra_front: dict | None = None) -> str:
    """상황 보고 공용 틀 — ①무엇이 문제인가 ②그 외 보고할 수 있는 내용.

    브리핑 대체(notice)와 워치독의 미도착 경보가 같은 틀을 쓴다."""
    from engine.briefing import context as X

    as_of = as_of or datetime.now(KST).date()
    now = datetime.now(KST)
    front = ["---", f"title: {title}", f"generated_at: {now:%Y-%m-%d %H:%M} KST"]
    for k, v in (extra_front or {}).items():
        front.append(f"{k}: {v}")
    front.append("---")
    lines = front + ["", f"# {title}", "", f"## {heading}"]
    lines += [f"- {ln}" for ln in problem_lines]
    if next_line:
        lines.append(f"- 다음 정규 보고: {next_line}")
    lines += ["", "## 그 외 보고할 수 있는 내용", ""]
    blocks = [
        (X.build_data_health_block,),
        (X.build_hynix_block, as_of),
        (X.build_execution_block, as_of),
        (X.build_bottleneck_block, as_of),
        (X.build_calendar_block, as_of, calendar_slot),
        (X.build_ledger_block, as_of),
    ]
    for spec in blocks:
        btitle, body = _safe(*spec)
        lines += [f"### {btitle}", "", body.strip(), ""]
    lines += [
        "## Sources",
        "- 코드 자동 생성(`engine/briefing/notice.py`, LLM 미사용) — 브리핑 팩과 같은 데이터",
        "- 원칙: `wiki/concepts/report-delivery-policy.md` (조용한 미발행 금지)",
        "",
    ]
    return "\n".join(lines)


def build_notice_markdown(slot: str, as_of: date, reason: str,
                          extra_problem: str | None = None) -> str:
    """정규 브리핑 대신 보내는 상황 보고. reason은 '왜 정규 브리핑이 없는가'.
    extra_problem은 워치독이 채운다(예: '루틴이 제시간에 발행하지 않음')."""
    label = SLOT_LABEL[slot]
    problems = [reason] + ([f"⚠️ {extra_problem}"] if extra_problem else [])
    return build_status_markdown(
        title=f"상황 보고 {as_of.isoformat()} ({label} 대체)",
        heading="오늘 정규 브리핑이 없는 이유",
        problem_lines=problems,
        next_line=NEXT_SLOT[slot],
        calendar_slot=slot if slot in ("AM", "PM") else "AM",
        as_of=as_of,
        extra_front={"slot": slot, "notice": "true"},
    )


def write_notice(slot: str, as_of: date, reason: str, extra_problem: str | None = None,
                 overwrite: bool = False) -> Path:
    """report/briefing/<date>-<slot>.md 로 저장. 이미 정규 브리핑이 있으면 덮지 않는다."""
    BRIEF_DIR.mkdir(parents=True, exist_ok=True)
    path = BRIEF_DIR / f"{as_of.isoformat()}-{slot}.md"
    if path.exists() and not overwrite:
        return path
    path.write_text(build_notice_markdown(slot, as_of, reason, extra_problem), encoding="utf-8")
    return path
