"""청약 리포트 — daily, PEOS와 분리된 가벼운 리포트 (Master Instruction 16, 17, 25).

사용자 요청 원문: "PEOS가 아니라 하루 한번 보내는 청약 리포트에 내용을 추가해줘"
+ "부동산 관련 가격 매매 전세 동향등도 청약 리포트로 분리해서 가져와. PEOS는
너무 무거워서 좀 나눠야해."

PEOS(engine/report/run.py)는 거시(ECOS/KOSIS/FRED) + CCI + SK하이닉스 실측
데이터까지 전부 모으는 무거운 파이프라인이다. 이 리포트는 그 반대 극단을
의도적으로 겨냥한다 — 청약 의사결정에 실제로 쓰이는 것만:

  1. 청약 우려사항 daily 추적 (engine/exporters/subscription_concern_tracker.py)
  2. 부동산 실거래가 동향 — 아파트/연립다세대/오피스텔 매매 + 아파트 전월세
     (국토교통부 실거래가 공개시스템, engine/real_estate/*)

거시 엔진(engine/macro)도, CCI 위기지수도, SK하이닉스 실측 데이터도 이 파이프
라인은 아예 import하지 않는다 — ECOS/KOSIS/FRED 호출이 전혀 없다는 뜻. 유일한
네트워크 의존은 국토교통부 MOLIT API(DATA_GO_KR_KEY)뿐이고, exposure 모델은
config/portfolio.yaml만 읽는 무네트워크 모듈이다.

이 5개 섹션(청약 우려사항 + 매매 3종 + 전세)은 원래 PEOS(markdown.py)에
있었다 — 2026-09-02에 이 리포트로 이관하면서 PEOS main_sections에서는
제거했다. PEOS의 real_estate_decision(WAIT/ENTER 판단)은 거시 신호와 결합돼
있어 그대로 PEOS에 남아있다 — 이 리포트는 "시세가 지금 어떤가"를 다루고,
PEOS는 "지금 진입할 때인가"를 다룬다.

    python -m engine.report.subscription_report
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from core.logger import log_event
from engine.exporters.subscription_concern_tracker import compute_subscription_concerns
from engine.real_estate import market_trend as real_estate_trend
from engine.real_estate import officetel_trend, rent_trend, villa_trend
from .markdown import _fmt

KST = timezone(timedelta(hours=9))
REPO_ROOT = Path(__file__).resolve().parents[2]


def _tier_label(tier: str) -> str:
    return {"seoul": "서울", "capital_area": "수도권", "nationwide": "전국(대표표본)"}.get(tier, tier)


def _sale_trend_section(re_data: dict | None, title: str, highlight_label: str = "청약 타겟 지역") -> str:
    """국토교통부 실거래가 기반 서울/수도권/전국 가격 추세 + 하이라이트 지역 — 아파트/연립다세대
    /오피스텔 매매 세 종류가 데이터 소스(collector)만 다르고 형식은 동일해서 공용으로 뺐다."""
    if not re_data:
        return ""

    lines = [f"## {title} 실거래가 동향 (국토교통부 실거래가 공개시스템)", ""]

    is_pending = re_data["fetch_status"] == "pending"
    is_dead_source_error = re_data["fetch_status"] == "source_error" and not any(
        t.get("data_status") == "ok" for t in re_data.get("tiers", {}).values()
    )
    if is_pending or is_dead_source_error:
        if is_pending:
            lines.append(f"- [사실] 데이터 상태: Pending — {re_data.get('fetch_note') or 'DATA_GO_KR_KEY 미설정'}")
        else:
            lines.append(f"- [사실] 데이터 상태: Source Error — {re_data.get('fetch_note') or '국토교통부 API 응답 없음'}")
        lines.append("")
        lines.append("**데이터 준비 중:** 다음 리포트에서 재시도됩니다. 아래는 채워질 정보의 형식입니다.")
        lines.append("")
        lines.append("| 지역군 | 기준월 | 평당가(만원) | MoM | 3개월 추세 | 거래량 | 시장 온도 |")
        lines.append("|---|---|---|---|---|---|---|")
        lines.append("| 서울 | - | - | - | - | - | - |")
        lines.append("| 수도권 | - | - | - | - | - | - |")
        lines.append("| 전국(대표표본) | - | - | - | - | - | - |")
        lines.append("")
        lines.append(f"### {highlight_label} 하이라이트 — 용인 기흥구")
        lines.append("- [사실] 플랫폼시티 인근 지역의 월간 실거래가 추세")
        lines.append("- 기준: 평당가(만원), 전월비 변화율, 월간 거래량, 시장 온도(과열/보합/냉각)")
        lines.append("")
        lines.append("### 서울 구별 순위")
        lines.append("- [분석] 25개 자치구를 실거래가 상승률로 순위화")
        lines.append("- 상승 TOP 3 (Gainers)")
        lines.append("- 하락 TOP 3 (Decliners)")
        return "\n".join(lines)

    coverage = re_data.get("regions_covered")
    total = re_data.get("regions_total")
    if coverage is not None and total:
        lines.append(f"- [사실] 조회 지역 커버리지: {coverage}/{total}개 지역")
        lines.append("")

    lines += ["| 지역군 | 기준월 | 평당가(만원) | MoM | 3개월 추세 | 거래량 | 시장 온도 |",
              "|---|---|---|---|---|---|---|"]
    for tier in ("seoul", "capital_area", "nationwide"):
        t = re_data["tiers"][tier]
        if t.get("data_status") != "ok":
            lines.append(f"| {_tier_label(tier)} | - | Pending | - | - | - | - |")
            continue
        lines.append(
            f"| {t['label']} | {t['reference_month']} | {_fmt(t['price_per_pyeong_manwon'])} | "
            f"{_fmt(t['mom_change_pct'], '%')} | {_fmt(t['trend_3m_pct'], '%')} | "
            f"{_fmt(t['transaction_count'])}건 | {t['market_heat']} |"
        )
    lines.append("")
    lines.append("- [해석] '전국'은 250여개 시군구 전수조사가 아니라 8개 특·광역시 + 주요 도청소재지 대표 도시 표본 기준 추정치.")
    lines.append("")

    hl = re_data["highlight"]
    lines.append(f"### {highlight_label} 하이라이트 — {hl['region_name']}")
    if hl.get("note"):
        lines.append(f"- [사실] {hl['note']}")
    if hl.get("data_status") == "ok":
        lines.append(
            f"- [사실] {hl['reference_month']} 기준 평당가 {_fmt(hl['price_per_pyeong_manwon'])}만원 "
            f"(MoM {_fmt(hl.get('mom_change_pct'), '%')}), 거래 {_fmt(hl.get('transaction_count'))}건, "
            f"시장 온도 {hl.get('market_heat', 'N/A')}"
        )
    else:
        lines.append("- [사실] 데이터 상태: Pending — 최근 조회 기간 내 확인된 실거래 없음")
    lines.append("")

    movers = re_data.get("seoul_district_movers", {})
    if movers.get("data_status") == "ok":
        lines.append("### 서울 자치구 MoM 상승/하락 TOP")
        gainers = ", ".join(f"{g['name']} ({_fmt(g['mom_change_pct'], '%')})" for g in movers["gainers"])
        decliners = ", ".join(f"{d['name']} ({_fmt(d['mom_change_pct'], '%')})" for d in movers["decliners"])
        lines.append(f"- 상승 TOP: {gainers or '데이터 부족'}")
        lines.append(f"- 하락 TOP: {decliners or '데이터 부족'}")

    return "\n".join(lines)


def _real_estate_trend(payload: dict) -> str:
    return _sale_trend_section(payload.get("real_estate"), "아파트 매매")


def _villa_trend(payload: dict) -> str:
    return _sale_trend_section(payload.get("real_estate_villa"), "연립다세대(빌라) 매매")


def _officetel_trend(payload: dict) -> str:
    return _sale_trend_section(payload.get("real_estate_officetel"), "오피스텔 매매")


def _rent_trend(payload: dict) -> str:
    """아파트 전월세 실거래가 — 전세(평당 보증금)와 월세(평당 보증금+평당 월세)를 함께 표시.
    현재 전월세로 거주 중인 사용자의 갱신·이사 판단에 바로 쓰이는 섹션이라 청약 타겟 지역
    하이라이트를 매매 섹션들과 동일한 비중으로 유지한다."""
    re_data = payload.get("real_estate_rent")
    if not re_data:
        return ""

    lines = ["## 아파트 전월세 실거래가 동향 (국토교통부 실거래가 공개시스템)", ""]

    is_pending = re_data["fetch_status"] == "pending"
    is_dead_source_error = re_data["fetch_status"] == "source_error" and not any(
        t.get("data_status") == "ok" for t in re_data.get("jeonse_tiers", {}).values()
    )
    if is_pending or is_dead_source_error:
        if is_pending:
            lines.append(f"- [사실] 데이터 상태: Pending — {re_data.get('fetch_note') or 'DATA_GO_KR_KEY 미설정'}")
        else:
            lines.append(f"- [사실] 데이터 상태: Source Error — {re_data.get('fetch_note') or '국토교통부 API 응답 없음'}")
        lines.append("")
        lines.append("**데이터 준비 중:** 다음 리포트에서 재시도됩니다.")
        return "\n".join(lines)

    coverage = re_data.get("regions_covered")
    total = re_data.get("regions_total")
    if coverage is not None and total:
        lines.append(f"- [사실] 조회 지역 커버리지: {coverage}/{total}개 지역")
        lines.append("")

    lines.append("### 전세 (평당 보증금)")
    lines += ["| 지역군 | 기준월 | 평당 보증금(만원) | MoM | 3개월 추세 | 거래량 | 시장 온도 |",
              "|---|---|---|---|---|---|---|"]
    for tier in ("seoul", "capital_area", "nationwide"):
        t = re_data["jeonse_tiers"][tier]
        if t.get("data_status") != "ok":
            lines.append(f"| {_tier_label(tier)} | - | Pending | - | - | - | - |")
            continue
        lines.append(
            f"| {t['label']} | {t['reference_month']} | {_fmt(t['price_per_pyeong_manwon'])} | "
            f"{_fmt(t['mom_change_pct'], '%')} | {_fmt(t['trend_3m_pct'], '%')} | "
            f"{_fmt(t['transaction_count'])}건 | {t['market_heat']} |"
        )
    lines.append("")

    lines.append("### 월세 (평당 보증금 + 평당 월세)")
    lines += ["| 지역군 | 기준월 | 평당 보증금(만원) | 보증금 MoM | 평당 월세(만원) | 월세 MoM | 거래량 |",
              "|---|---|---|---|---|---|---|"]
    for tier in ("seoul", "capital_area", "nationwide"):
        t = re_data["wolse_tiers"][tier]
        if t.get("data_status") != "ok":
            lines.append(f"| {_tier_label(tier)} | - | Pending | - | - | - | - |")
            continue
        lines.append(
            f"| {t['label']} | {t['reference_month']} | {_fmt(t['deposit_per_pyeong_manwon'])} | "
            f"{_fmt(t.get('deposit_mom_change_pct'), '%')} | {_fmt(t.get('rent_per_pyeong_manwon'))} | "
            f"{_fmt(t.get('rent_mom_change_pct'), '%')} | {_fmt(t.get('transaction_count'))}건 |"
        )
    lines.append("")
    lines.append("- [해석] '전국'은 250여개 시군구 전수조사가 아니라 8개 특·광역시 + 주요 도청소재지 대표 도시 표본 기준 추정치.")
    lines.append("")

    hl = re_data["jeonse_highlight"]
    lines.append(f"### 청약 타겟 지역(현 거주 지역군) 전세 하이라이트 — {hl['region_name']}")
    if hl.get("note"):
        lines.append(f"- [사실] {hl['note']}")
    if hl.get("data_status") == "ok":
        lines.append(
            f"- [사실] {hl['reference_month']} 기준 평당 보증금 {_fmt(hl['price_per_pyeong_manwon'])}만원 "
            f"(MoM {_fmt(hl.get('mom_change_pct'), '%')}), 거래 {_fmt(hl.get('transaction_count'))}건, "
            f"시장 온도 {hl.get('market_heat', 'N/A')}"
        )
    else:
        lines.append("- [사실] 데이터 상태: Pending — 최근 조회 기간 내 확인된 실거래 없음")
    lines.append("")

    movers = re_data.get("seoul_jeonse_district_movers", {})
    if movers.get("data_status") == "ok":
        lines.append("### 서울 자치구 전세 MoM 상승/하락 TOP")
        gainers = ", ".join(f"{g['name']} ({_fmt(g['mom_change_pct'], '%')})" for g in movers["gainers"])
        decliners = ", ".join(f"{d['name']} ({_fmt(d['mom_change_pct'], '%')})" for d in movers["decliners"])
        lines.append(f"- 상승 TOP: {gainers or '데이터 부족'}")
        lines.append(f"- 하락 TOP: {decliners or '데이터 부족'}")

    return "\n".join(lines)


def _subscription_concerns_section(payload: dict) -> str:
    """청약 우려사항 daily 추적.

    사용자 요청 원문: "정보를 취득하면 항상 나를 바라봐야해. 내가 현재 우려하는
    것들에 대해서 그 정보들이 진행되고 있는 방향을 분석해서 긴급하게 처리해야
    하는지 전략을 수정해야하는지를 알려주는 daily보고서가 되어야하는거야."

    5개 우려사항(소득제한/플랫폼시티 민영분류/전세만료/통학거리/자금갭)을 매일
    재평가해 🔴긴급 / 🟡전략재검토 / 🟢관망 3단계로 판정한다. 새 정보가 들어와도
    urgency가 바뀌지 않으면 조용히 관망 — 매일 똑같은 경보를 반복하지 않는다.

    payload["subscription_concerns"]를 읽기만 한다(재계산하지 않음) —
    build_subscription_report_payload()가 이미 try/except로 감싸 계산해뒀으므로
    여기서 다시 부르면 같은 실패를 여기서도 반복해 렌더링 전체를 죽일 수 있다.
    """
    report = payload.get("subscription_concerns")
    if report is None:
        return "# 1. 청약 우려사항 daily 추적\n\n- [사실] 데이터 상태: Pending — 계산 실패 또는 미실행 (로그 확인 필요)"

    urgency_emoji_line = {
        "🔴 긴급": "🔴",
        "🟡 전략재검토": "🟡",
        "🟢 관망": "🟢",
    }

    lines = [
        "# 1. 청약 우려사항 daily 추적",
        "",
        f"**{report.headline}**",
        "",
    ]

    for c in report.concerns:
        emoji = urgency_emoji_line.get(c.urgency, "❔")
        lines.append(f"## {emoji} {c.name} — {c.urgency}")
        lines.append(f"- 현황: {c.status}")
        lines.append(f"- 권고: {c.recommendation}")
        for d in c.detail:
            lines.append(f"  - {d}")
        lines.append("")

    return "\n".join(lines)


def build_subscription_report_payload() -> dict:
    """PEOS 없이 독립적으로 도는, 청약 리포트 전용의 가벼운 payload.

    거시 엔진(engine.macro)도 CCI도 SK하이닉스 실측 수집도 import하지 않는다.
    네트워크 의존은 MOLIT(부동산 4종) 하나뿐 — exposure 모델은 무네트워크.
    각 단계는 다른 것에 영향을 주지 않도록 독립적으로 실패 허용(try/except).
    """
    payload: dict = {}

    try:
        from engine.exposure.model import build_exposure_model
        payload["exposure"] = build_exposure_model()
        log_event("exposure_model.computed", semi_pct=round(payload["exposure"].semi_pct, 1))
    except Exception as exc:
        log_event("exposure_model.failed", error=str(exc), level="warning")
        payload["exposure"] = None

    try:
        payload["real_estate"] = real_estate_trend.compute_real_estate_trend()
    except Exception as exc:
        log_event("real_estate_trend.failed", error=str(exc), level="warning")
        payload["real_estate"] = None

    try:
        payload["real_estate_rent"] = rent_trend.compute_rent_trend()
    except Exception as exc:
        log_event("rent_trend.failed", error=str(exc), level="warning")
        payload["real_estate_rent"] = None

    try:
        payload["real_estate_villa"] = villa_trend.compute_villa_trend()
    except Exception as exc:
        log_event("villa_trend.failed", error=str(exc), level="warning")
        payload["real_estate_villa"] = None

    try:
        payload["real_estate_officetel"] = officetel_trend.compute_officetel_trend()
    except Exception as exc:
        log_event("officetel_trend.failed", error=str(exc), level="warning")
        payload["real_estate_officetel"] = None

    # subscription_concerns는 exposure가 payload에 이미 있어야 자금조달 갭
    # 체크가 동작하므로 반드시 그 다음 자리.
    try:
        payload["subscription_concerns"] = compute_subscription_concerns(payload)
        log_event("subscription_concerns.computed",
                  overall_urgency=payload["subscription_concerns"].overall_urgency)
    except Exception as exc:
        log_event("subscription_concerns.failed", error=str(exc), level="warning")
        payload["subscription_concerns"] = None

    return payload


def render_subscription_report(payload: dict, report_date: str) -> str:
    """블록 단위로 조립 — 각 블록은 이미 완결된 여러 줄 문자열(또는 데이터가
    없으면 빈 문자열)이고, 빈 블록은 건너뛴다. 리스트를 통째로 '\\n'.join하며
    빈 줄만 걸러내면(과거 버전의 버그) 헤더/블록쿼트 사이 빈 줄까지 사라져
    마크다운 블록 구분이 깨진다 — 그래서 블록째로 '\\n\\n'.join한다."""
    intro = (
        f"# 청약 리포트 — {report_date}\n\n"
        "> 이 리포트는 PEOS(거시/SK하이닉스 판단)와 분리된 청약 전용 리포트입니다. "
        "거시경제 데이터를 전혀 쓰지 않아 매매/전세 실거래가(국토교통부)와 "
        "청약 우려사항 추적만 담아 가볍게 유지합니다."
    )
    blocks = [
        intro,
        _subscription_concerns_section(payload),
        "# 2. 부동산 실거래가 동향",
        _real_estate_trend(payload),
        _rent_trend(payload),
        _villa_trend(payload),
        _officetel_trend(payload),
    ]
    return "\n\n".join(b for b in blocks if b)


def email_subject(payload: dict, report_date: str) -> str:
    """scripts/send_subscription_report_email.py가 그대로 재사용하는 제목 형식."""
    concerns = payload.get("subscription_concerns")
    headline = concerns.headline if concerns else "청약 우려사항 데이터 없음"
    return f"[청약 리포트] {report_date} — {headline}"


def run(archive_date: str | None = None) -> dict[str, Path]:
    """생성만 한다 — 발송은 하지 않는다.

    daily-peos-report.yml에서 이미 얻은 교훈(2026-08-08~10, 리포트 3일 연속
    생성 성공 → 발송/push 실패가 조용히 묻힘) 그대로: 생성은 최선을 다하고
    예외를 삼켜도 되지만(개별 섹션 try/except), 발송은 별도 단계
    (scripts/send_subscription_report_email.py)에서 실패 시 시끄럽게 죽어야
    한다. 그래서 이 함수는 notify를 호출하지 않는다.
    """
    payload = build_subscription_report_payload()
    today_kst = archive_date or datetime.now(KST).date().isoformat()

    out_dir = REPO_ROOT / "report"
    out_dir.mkdir(parents=True, exist_ok=True)

    content = render_subscription_report(payload, today_kst)
    md_path = out_dir / f"subscription-report-{today_kst}.md"
    md_path.write_text(content, encoding="utf-8")

    log_event("subscription_report.generated", date=today_kst, path=str(md_path))

    return {"markdown": md_path}


def main() -> None:
    paths = run()
    print(f"Markdown: {paths['markdown']}")


if __name__ == "__main__":
    main()
