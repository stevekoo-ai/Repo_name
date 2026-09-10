"""Enhanced HTML renderer for PEOS report with CCI + Rate Analysis integrated display."""
from __future__ import annotations

import html as _html
from datetime import datetime


def _esc(value) -> str:
    """HTML 이스케이프.

    FX 섹션의 근거 문자열은 수동 입력(fx_risk_events.yaml)에서 오는 값이
    섞여 있어 그대로 넣으면 안 된다 — 이 저장소는 개인용이지만, 수집
    데이터가 리포트 HTML로 그대로 흘러드는 경로는 막아두는 게 맞다."""
    return _html.escape(str(value), quote=True)


def _hex_to_rgb(hex_color: str) -> str:
    """Convert hex color to RGB tuple string."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{r}, {g}, {b}"


def _state_label(state: str) -> str:
    """Get human-readable state label."""
    labels = {
        "GREEN": "🟢 정상 (확장 모드)",
        "YELLOW": "🟡 경고 (둔화 모드)",
        "RED": "🔴 위기 (퇴출 모드)",
    }
    return labels.get(state, "? Unknown")


def _cci_quality_label(dq: dict, module: str) -> str:
    """PRIMARY/FALLBACK/NO_DATA + 며칠 전 데이터인지 한 줄로 — markdown.py의
    _quality_cell()과 같은 정보를 HTML용으로 렌더. 2026-09-01 신설(사용자
    지적: "데이터 신선도가 표시가 없네!")."""
    q = (dq or {}).get(module)
    if not q:
        return "—"
    quality = q.get("quality")
    if quality == "NO_DATA":
        return "⛔ 없음"
    days = q.get("days_stale")
    days_note = f" · {days}일 전" if days is not None else ""
    badge = "🟢실측" if quality == "PRIMARY" else "🟡대체"
    return f"{badge}{days_note}"


def _cci_module_rows(cci: dict) -> str:
    """CCI 9개 모듈 전부를 표 행으로 렌더 — 2026-09-01 이전엔 4개(Copper-Gold/
    Buffett/Rule of 20/K-Sahm)가 "기타 지표"라는 합산 숫자 하나로 뭉개져
    있었다(사용자 질문 "기타항목에 5는 뭐야?"의 원인 — 그 5는 Rule of 20 혼자
    늘 5/5를 찍던, 실제로는 PER 데이터가 없어 구조적으로 항상 만점이던 버그
    였다). 이제 9개 모두 각자 점수 + 신선도를 보여준다."""
    sc = cci.get("score_components", {})
    dq = cci.get("data_quality", {})
    rows = [
        ("Sahm Rule (고용)", "sahm", 20),
        ("Yield Curve", "yield_curve", 15),
        ("Harvey Filter", "harvey", 15),
        ("Copper-Gold Ratio", "copper_gold", 10),
        ("Credit OAS", "credit_oas", 15),
        ("Buffett Indicator*", "buffett", 5),
        ("Rule of 20*", "rule_of_20", 5),
        ("K-Sahm Rule (한국 고용)", "k_sahm", 5),
        ("Semiconductor Cycle", "semiconductor", 10),
    ]
    lines = []
    for label, key, max_score in rows:
        lines.append(
            f"<tr><td>{label}</td>"
            f"<td><strong>{sc.get(key, 0)}/{max_score}</strong></td>"
            f"<td>{_cci_quality_label(dq, key)}</td></tr>"
        )
    lines.append(
        '<tr><td colspan="3" style="font-size:0.85em;color:#94A3B8;">'
        "*2026-09-01부로 영구 비활성화 — 필요한 실데이터(시가총액, PER)가 "
        "이 저장소에 없어 값을 지어내지 않고 0점 고정</td></tr>"
    )
    return "\n                    ".join(lines)


def _rate_state_label(score: int) -> str:
    """Get rate analysis state label."""
    if score >= 85:
        return "극도의 완화"
    elif score >= 70:
        return "완화 국면"
    elif score >= 55:
        return "중립~완화"
    elif score >= 40:
        return "긴축 국면"
    else:
        return "극도의 긴축"


def _render_sk_hynix_action(action: dict) -> str:
    """Render SK Hynix action box."""
    if not action:
        return ""

    state = action.get("state", "UNKNOWN")
    action_type = action.get("action", "")
    max_weight = action.get("max_weight", 0)
    description = action.get("description", "")
    signal = action.get("signal", "")

    state_class = {"GREEN": "green", "YELLOW": "yellow", "RED": ""}.get(state, "")

    return f"""
    <div class="action-box {state_class}">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px;">
            <div>
                <strong style="color: #CBD5E1;">조치</strong>
                <div style="font-size: 1.2em; color: #F1F5F9; margin-top: 5px;">{action_type}</div>
            </div>
            <div>
                <strong style="color: #CBD5E1;">최대 비중</strong>
                <div style="font-size: 1.2em; color: #F1F5F9; margin-top: 5px;">{max_weight}%</div>
            </div>
        </div>
        <div style="margin-bottom: 15px;">
            <strong style="color: #CBD5E1;">상황:</strong>
            <p style="margin-top: 8px;">{description}</p>
        </div>
        <div>
            <strong style="color: #CBD5E1;">신호:</strong>
            <p style="margin-top: 8px;">{signal}</p>
        </div>
    </div>"""


_HEAT_COLOR = {"과열": "#F97316", "냉각": "#3B82F6", "보합": "#94A3B8", "데이터 부족": "#64748B"}


def _fmt_pct(value) -> str:
    if value is None:
        return "N/A"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"


def _render_tier_card(tier: dict) -> str:
    """One 서울/수도권/전국 mini-card inside the real-estate section."""
    if tier.get("data_status") != "ok":
        return f"""
        <div style="background: rgba(51, 65, 85, 0.3); padding: 20px; border-radius: 8px;">
            <div style="font-size: 1.1em; color: #F1F5F9; font-weight: 600; margin-bottom: 10px;">{tier['label']}</div>
            <div style="color: #94A3B8;">Pending — 데이터 확보 전</div>
        </div>"""

    heat = tier["market_heat"]
    heat_color = _HEAT_COLOR.get(heat, "#94A3B8")
    mom = tier.get("mom_change_pct")
    mom_color = "#F87171" if (mom or 0) > 0 else "#60A5FA" if (mom or 0) < 0 else "#94A3B8"

    return f"""
        <div style="background: rgba(51, 65, 85, 0.3); padding: 20px; border-radius: 8px; border-left: 4px solid {heat_color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="font-size: 1.1em; color: #F1F5F9; font-weight: 600;">{tier['label']}</div>
                <span style="background: {heat_color}33; color: {heat_color}; padding: 3px 10px; border-radius: 12px; font-size: 0.85em; font-weight: 600;">{heat}</span>
            </div>
            <div style="font-size: 1.6em; font-weight: bold; color: #F1F5F9;">{_fmt(tier['price_per_pyeong_manwon'])}만원<span style="font-size: 0.5em; color: #94A3B8;">/평</span></div>
            <div style="margin-top: 8px; color: {mom_color}; font-weight: 600;">MoM {_fmt_pct(mom)}</div>
            <div style="margin-top: 4px; color: #94A3B8; font-size: 0.9em;">3개월 추세 {_fmt_pct(tier.get('trend_3m_pct'))} · 거래 {_fmt(tier.get('transaction_count'))}건 ({tier.get('reference_month', '')})</div>
        </div>"""


def _fmt(value) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:,.0f}"
    return str(value)


def _render_district_movers(movers: dict) -> str:
    if movers.get("data_status") != "ok":
        return '<p style="color: #94A3B8;">아직 MoM을 계산할 만큼 이력이 쌓이지 않았습니다 (다음 리포트부터 표시).</p>'

    def _row(items: list[dict], color: str) -> str:
        if not items:
            return '<span style="color: #64748B;">데이터 부족</span>'
        return " · ".join(f"<span style=\"color: {color};\">{i['name']} ({_fmt_pct(i['mom_change_pct'])})</span>" for i in items)

    return f"""
        <div class="metric"><span class="metric-label">상승 TOP</span><span>{_row(movers['gainers'], '#F87171')}</span></div>
        <div class="metric"><span class="metric-label">하락 TOP</span><span>{_row(movers['decliners'], '#60A5FA')}</span></div>"""


def _render_real_estate_placeholder(status_label: str, note: str, title: str = "부동산", icon: str = "🏘️") -> str:
    return f"""
        <div class="card" style="margin-bottom: 30px;">
            <h2>{icon} {title} 실거래가 동향 (국토교통부 실거래가 공개시스템)</h2>
            <p style="color: #94A3B8;">{status_label} — {note}</p>
            <p style="color: #64748B; font-size: 0.9em; margin-top: 8px;">데이터 준비 중: 다음 리포트에서 재시도됩니다. 아래는 채워질 정보의 형식입니다.</p>
            <table>
                <tr><th>지역군</th><th>기준월</th><th>평당가(만원)</th><th>MoM</th><th>3개월 추세</th><th>거래량</th><th>시장 온도</th></tr>
                <tr><td>서울</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr>
                <tr><td>수도권</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr>
                <tr><td>전국(대표표본)</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr>
            </table>
            <div class="portfolio-section" style="border-left-color: #A855F7; margin-top: 15px;">
                <strong style="color: #D8B4FE;">📍 청약 타겟 지역 — 용인 기흥구</strong>
                <div style="color: #94A3B8; font-size: 0.9em; margin-top: 4px;">플랫폼시티 인근 지역의 월간 실거래가 추세 (평당가/MoM/거래량/시장 온도)를 다음 리포트부터 표시합니다.</div>
            </div>
        </div>"""


def _render_sale_trend_section(re_data: dict, title: str, icon: str = "🏘️") -> str:
    """국토교통부 실거래가 매매 섹션 — 아파트/연립다세대/오피스텔이 데이터 소스만 다르고
    형식은 동일해서 공용으로 뺐다."""
    if not re_data:
        return ""

    if re_data.get("fetch_status") == "pending":
        return _render_real_estate_placeholder("Pending", re_data.get('fetch_note') or 'DATA_GO_KR_KEY 미설정', title, icon)

    tiers = re_data.get("tiers", {})
    any_ok = any(t.get("data_status") == "ok" for t in tiers.values())
    if not any_ok:
        return _render_real_estate_placeholder("Source Error", re_data.get('fetch_note') or '국토교통부 API 응답 없음', title, icon)

    coverage = re_data.get("regions_covered")
    total = re_data.get("regions_total")
    coverage_note = f"조회 지역 {coverage}/{total}개" if coverage is not None and total else ""

    hl = re_data.get("highlight", {})
    hl_body = ""
    if hl.get("data_status") == "ok":
        hl_body = (
            f"{hl['reference_month']} 기준 평당가 <strong style=\"color:#F1F5F9;\">{_fmt(hl['price_per_pyeong_manwon'])}만원</strong>"
            f" (MoM {_fmt_pct(hl.get('mom_change_pct'))}), 거래 {_fmt(hl.get('transaction_count'))}건, "
            f"시장 온도 <span style=\"color:{_HEAT_COLOR.get(hl.get('market_heat'), '#94A3B8')};\">{hl.get('market_heat', 'N/A')}</span>"
        )
    else:
        hl_body = "최근 조회 기간 내 확인된 실거래가 없습니다."

    return f"""
        <div class="card" style="margin-bottom: 30px;">
            <h2>{icon} {title} 실거래가 동향 (국토교통부 실거래가 공개시스템)</h2>
            <p style="color: #94A3B8; margin-bottom: 15px;">{coverage_note} · '전국'은 전수조사가 아닌 8개 특·광역시+주요 도청소재지 대표 표본 기준 추정치</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 25px;">
                {_render_tier_card(tiers.get('seoul', {}))}
                {_render_tier_card(tiers.get('capital_area', {}))}
                {_render_tier_card(tiers.get('nationwide', {}))}
            </div>

            <div class="portfolio-section" style="border-left-color: #A855F7;">
                <strong style="color: #D8B4FE;">📍 청약 타겟 지역 — {hl.get('region_name', '')}</strong>
                {f'<div style="color: #94A3B8; font-size: 0.9em; margin-top: 4px;">{hl["note"]}</div>' if hl.get('note') else ''}
                <div style="margin-top: 10px;">{hl_body}</div>
            </div>

            <h3 style="margin-top: 25px; margin-bottom: 10px; color: #CBD5E1;">서울 자치구 MoM 상승/하락 TOP</h3>
            {_render_district_movers(re_data.get('seoul_district_movers', {}))}
        </div>"""


def _render_real_estate_section(re_data: dict) -> str:
    return _render_sale_trend_section(re_data, "아파트 매매")


def _render_villa_section(re_data: dict) -> str:
    return _render_sale_trend_section(re_data, "연립다세대(빌라) 매매", icon="🏚️")


def _render_officetel_section(re_data: dict) -> str:
    return _render_sale_trend_section(re_data, "오피스텔 매매", icon="🏢")


def _render_wolse_tier_card(tier: dict) -> str:
    """전월세 월세 지역군 카드 — 매매용 _render_tier_card와 달리 시장 온도가 없고
    보증금/월세 두 숫자를 같이 보여준다."""
    if tier.get("data_status") != "ok":
        return f"""
        <div style="background: rgba(51, 65, 85, 0.3); padding: 20px; border-radius: 8px;">
            <div style="font-size: 1.1em; color: #F1F5F9; font-weight: 600; margin-bottom: 10px;">{tier['label']}</div>
            <div style="color: #94A3B8;">Pending — 데이터 확보 전</div>
        </div>"""

    deposit_mom = tier.get("deposit_mom_change_pct")
    deposit_mom_color = "#F87171" if (deposit_mom or 0) > 0 else "#60A5FA" if (deposit_mom or 0) < 0 else "#94A3B8"

    return f"""
        <div style="background: rgba(51, 65, 85, 0.3); padding: 20px; border-radius: 8px;">
            <div style="font-size: 1.1em; color: #F1F5F9; font-weight: 600; margin-bottom: 12px;">{tier['label']}</div>
            <div style="font-size: 1.4em; font-weight: bold; color: #F1F5F9;">보증금 {_fmt(tier['deposit_per_pyeong_manwon'])}만원<span style="font-size: 0.5em; color: #94A3B8;">/평</span></div>
            <div style="margin-top: 4px; color: {deposit_mom_color}; font-weight: 600;">MoM {_fmt_pct(deposit_mom)}</div>
            <div style="margin-top: 10px; font-size: 1.1em; color: #F1F5F9;">월세 {_fmt(tier.get('rent_per_pyeong_manwon'))}만원<span style="font-size: 0.6em; color: #94A3B8;">/평</span></div>
            <div style="margin-top: 4px; color: #94A3B8; font-size: 0.9em;">거래 {_fmt(tier.get('transaction_count'))}건 ({tier.get('reference_month', '')})</div>
        </div>"""


def _render_rent_section(re_data: dict) -> str:
    if not re_data:
        return ""

    if re_data.get("fetch_status") == "pending":
        return _render_real_estate_placeholder("Pending", re_data.get('fetch_note') or 'DATA_GO_KR_KEY 미설정', "아파트 전월세", icon="🏠")

    jeonse_tiers = re_data.get("jeonse_tiers", {})
    any_ok = any(t.get("data_status") == "ok" for t in jeonse_tiers.values())
    if not any_ok:
        return _render_real_estate_placeholder("Source Error", re_data.get('fetch_note') or '국토교통부 API 응답 없음', "아파트 전월세", icon="🏠")

    coverage = re_data.get("regions_covered")
    total = re_data.get("regions_total")
    coverage_note = f"조회 지역 {coverage}/{total}개" if coverage is not None and total else ""

    wolse_tiers = re_data.get("wolse_tiers", {})
    hl = re_data.get("jeonse_highlight", {})
    hl_body = ""
    if hl.get("data_status") == "ok":
        hl_body = (
            f"{hl['reference_month']} 기준 평당 보증금 <strong style=\"color:#F1F5F9;\">{_fmt(hl['price_per_pyeong_manwon'])}만원</strong>"
            f" (MoM {_fmt_pct(hl.get('mom_change_pct'))}), 거래 {_fmt(hl.get('transaction_count'))}건, "
            f"시장 온도 <span style=\"color:{_HEAT_COLOR.get(hl.get('market_heat'), '#94A3B8')};\">{hl.get('market_heat', 'N/A')}</span>"
        )
    else:
        hl_body = "최근 조회 기간 내 확인된 전세 실거래가 없습니다."

    return f"""
        <div class="card" style="margin-bottom: 30px;">
            <h2>🏠 아파트 전월세 실거래가 동향 (국토교통부 실거래가 공개시스템)</h2>
            <p style="color: #94A3B8; margin-bottom: 15px;">{coverage_note} · '전국'은 전수조사가 아닌 8개 특·광역시+주요 도청소재지 대표 표본 기준 추정치</p>

            <h3 style="margin-bottom: 10px; color: #CBD5E1;">전세 (평당 보증금)</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 25px;">
                {_render_tier_card(jeonse_tiers.get('seoul', {}))}
                {_render_tier_card(jeonse_tiers.get('capital_area', {}))}
                {_render_tier_card(jeonse_tiers.get('nationwide', {}))}
            </div>

            <h3 style="margin-bottom: 10px; color: #CBD5E1;">월세 (평당 보증금 + 평당 월세)</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 25px;">
                {_render_wolse_tier_card(wolse_tiers.get('seoul', {}))}
                {_render_wolse_tier_card(wolse_tiers.get('capital_area', {}))}
                {_render_wolse_tier_card(wolse_tiers.get('nationwide', {}))}
            </div>

            <div class="portfolio-section" style="border-left-color: #A855F7;">
                <strong style="color: #D8B4FE;">📍 현 거주 지역군(청약 타겟 인근) 전세 — {hl.get('region_name', '')}</strong>
                {f'<div style="color: #94A3B8; font-size: 0.9em; margin-top: 4px;">{hl["note"]}</div>' if hl.get('note') else ''}
                <div style="margin-top: 10px;">{hl_body}</div>
            </div>

            <h3 style="margin-top: 25px; margin-bottom: 10px; color: #CBD5E1;">서울 자치구 전세 MoM 상승/하락 TOP</h3>
            {_render_district_movers(re_data.get('seoul_jeonse_district_movers', {}))}
        </div>"""


def _rate_or_missing(rates: dict, key: str, suffix: str = "%") -> str:
    """Render a rate, or say it is uncollected.

    `.get(key, "N/A")` does not help here: the key exists with a None value once
    the staleness guard drops an old series, so the page rendered "None%".
    """
    v = (rates or {}).get(key)
    if v is None:
        return '<span style="color:#94A3B8;font-size:0.85em">미수집</span>'
    return f"{v}{suffix}"


def _stale_series_note(rate: dict) -> str:
    """Explain dropped series inline. Mirrors markdown.py — this renderer feeds
    docs/report.html and the emailed report, so a fix applied only there would
    never reach the page the user actually opens."""
    stale = (rate or {}).get("stale_series") or []
    if not stale:
        return ""
    rows = "".join(
        f"<li><code>{d['series']}</code> — 최종 관측 {d['as_of']} ({d['age_days']:,}일 경과)</li>"
        for d in stale
    )
    return f"""
            <div style="margin-top:16px;padding:12px 14px;border-radius:8px;
                        background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.35)">
                <div style="color:#FBBF24;font-weight:700;margin-bottom:6px">⚠️ 너무 낡아 제외된 시리즈</div>
                <ul style="color:#94A3B8;margin:0;padding-left:18px">{rows}</ul>
                <div style="color:#64748B;font-size:0.85em;margin-top:8px">
                    2026-08-13까지 현재값처럼 표시되어 실재하지 않는 한-KR 금리차를 만들어냈습니다.
                    신선도 기준(45일) 초과 시 값을 버리고 사유를 남깁니다.
                </div>
            </div>"""


def _render_exposure_and_reconciliation(payload: dict) -> str:
    """Sections 0 and 0.5 for the HTML renderer.

    render_html() is a SEPARATE code path from markdown.py — anything wired only
    into the markdown renderer never reaches docs/report.html (the public
    dashboard) or the emailed report. Section 0/0.5 were added to markdown first
    and this renderer kept publishing the old, unreconciled view, including the
    CCI "적극 매수" instruction that reconciliation demotes under R4.
    Keep the two renderers in step.
    """
    m = payload.get("exposure")
    rec = payload.get("reconciliation")
    out = []

    if m is not None:
        def eok(v):
            return f"{v/100_000_000:.2f}억"
        emp = next((h for h in m.holdings if h.ticker == "000660.KS"), None)
        sellable = f"{emp.sellable_qty:,}주" if emp else "—"
        locked = f"{emp.locked_qty:,}주 ({emp.lock_until})" if emp and emp.locked_qty else "없음"
        out.append(f"""
        <div class="card" style="margin-bottom: 30px; border-left: 4px solid #38BDF8;">
            <h2>🧭 0. 포지션 &amp; 익스포저</h2>
            <p style="color:#94A3B8; margin: 8px 0 18px;">
                외부 API를 쓰지 않는 섹션 — 지표가 전부 이월된 날에도 이 숫자는 유효하다.
            </p>
            <div class="grid-2">
                <div>
                    <h3 style="color:#CBD5E1;">집중도</h3>
                    <p style="font-size: 2rem; font-weight: 800; color:#F87171; margin:6px 0;">
                        반도체 {m.semi_pct:.1f}%</p>
                    <p style="color:#94A3B8;">주식+ETF {eok(m.total_valued)} 중 {eok(m.semi_valued)}<br>
                    SK하이닉스 단독 {eok(m.employer_valued)} ({m.employer_pct:.1f}%)<br>
                    급여·PS·퇴직연금이 같은 회사 → 실질 집중도는 이보다 높음</p>
                </div>
                <div>
                    <h3 style="color:#CBD5E1;">동원 가능 자금</h3>
                    <p style="font-size: 2rem; font-weight: 800; color:#38BDF8; margin:6px 0;">
                        {eok(m.deployable_cash)}</p>
                    <p style="color:#94A3B8;">현금 {eok(m.cash_krw)} + 매각가능 {eok(m.liquid_valued)}<br>
                    즉시 조정 가능: <strong style="color:#E2E8F0;">{sellable}</strong><br>
                    락업: {locked}</p>
                </div>
            </div>
            <p style="color:#64748B; font-size:0.85rem; margin-top:14px;">
                시세 검증 커버리지 {m.priced_coverage_pct:.0f}% — 나머지는 매수원가 기준 근사.
            </p>
        </div>""")

    if rec is not None:
        ok = rec.tradeable
        color = "#10B981" if ok else "#EF4444"
        badge = "실행 가능" if ok else "오늘 실행 보류"
        blockers = "".join(f"<li>{b}</li>" for b in rec.blockers) or "<li>없음</li>"
        conflicts = "".join(
            f"""<div style="margin:14px 0; padding:12px; background:rgba(148,163,184,0.08); border-radius:8px;">
                <div style="font-weight:700; color:#E2E8F0;">{i}. {c.topic}</div>
                <div style="color:#94A3B8; margin-top:6px;">
                    <div>격하: {c.claim_a}</div>
                    <div>채택: {c.claim_b}</div>
                    <div style="color:#64748B; margin-top:4px;">{c.rule} — {c.resolution}</div>
                </div>
            </div>"""
            for i, c in enumerate(rec.conflicts, 1)
        )
        out.append(f"""
        <div class="card" style="margin-bottom: 30px; border-left: 4px solid {color};">
            <h2>⚖️ 0.5 엔진 정합성 점검</h2>
            <p style="font-size:1.4rem; font-weight:800; color:{color}; margin:10px 0;">{badge}</p>
            <p style="color:#94A3B8;">{rec.verdict}</p>
            <h3 style="margin-top:18px; color:#CBD5E1;">보류 사유</h3>
            <ul style="color:#94A3B8; padding-left:18px;">{blockers}</ul>
            <h3 style="margin-top:18px; color:#CBD5E1;">검출된 충돌 {len(rec.conflicts)}건</h3>
            {conflicts or '<p style="color:#94A3B8;">없음</p>'}
        </div>""")

    return "".join(out)


def _render_fx_regime(payload: dict) -> str:
    """§1.7 환율 국면 (FRS) — HTML 카드.

    ⚠ 2026-09-10에 발견한 구멍을 막는 함수다. FRS §1.7을 markdown.py에만
    연결해두고 "완료"라고 했는데, **사용자가 실제로 받아보는 건 HTML이다**
    — daily-peos-report.yml이 report/<날짜>.html을 이메일로 보내고
    docs/report.html로 게시한다. 마크다운은 저장소 안에만 있다.
    렌더러가 둘인 구조에선 새 섹션을 양쪽에 다 붙여야 전달된다.

    markdown 쪽(engine/report/fx_regime_section.py)과 **같은 payload**를
    읽는다 — 두 렌더러가 서로 다른 계산을 하면 같은 날 리포트가 두 얘기를
    하게 된다. 계산은 payload.py가 한 번만 하고 여기선 표기만 한다.

    R4 준수: 국면·경고·사실만 낸다. 헤지/매매 지시, 종목·비중 추천,
    목표 환율은 markdown 쪽과 동일하게 만들지 않는다.
    """
    fx = payload.get("fx_regime")
    if not fx or fx.get("score") is None:
        return ""

    score = fx["score"]
    # (+)=원화 강세. 부호에 색을 매핑하되 CCI의 GREEN/RED와 의미가 다르므로
    # (여긴 좋고 나쁨이 아니라 방향이다) 파랑/주황을 쓴다.
    color = "#38BDF8" if score > 0 else ("#FB923C" if score < 0 else "#94A3B8")
    gap = fx.get("gap") or {}
    months = fx.get("episode_months")

    factor_rows = "".join(
        f"<tr><td>{_esc(f['label'])}</td><td style='text-align:right'>{f['weight']}</td>"
        f"<td style='text-align:right'>"
        f"{('%+.2f' % f['normalized']) if f['available'] else '—'}</td>"
        f"<td style='color:#94A3B8;font-size:0.9em'>{_esc(f['detail'])}</td></tr>"
        for f in fx.get("factors", [])
    )

    warn_rows = "".join(
        f"<tr><td>{_esc(w['label'])}</td>"
        f"<td style='text-align:center'>{'🔥' if w['fired'] else '·'}</td>"
        f"<td style='color:#94A3B8;font-size:0.9em'>{_esc(w['detail'])}</td>"
        f"<td style='color:#94A3B8;font-size:0.85em'>"
        f"{_esc((w.get('evidence') or {}).get('verdict', '미측정'))}</td></tr>"
        for w in fx.get("warnings", [])
    )

    ctx = fx.get("dollar_context") or {}
    facts = []
    if ctx.get("cash_yield") is not None:
        facts.append(
            f"<li><b>달러 현금 기준선</b>: 미 3개월물 <b>{ctx['cash_yield']:.2f}%</b>. "
            "과거 5개 국면 중 4개는 미국이 제로금리라 '환전 후 대기'가 무수익이었다.</li>")
    if gap:
        facts.append(
            f"<li><b>환차익 구조</b>: 국면 전체를 보유하면 환차익은 구조적으로 0에 가깝다"
            f"(양끝이 모두 36개월선 교차점). 현재 이격 {gap['pct']:+.1f}%. "
            "<b>목표 환율은 제시하지 않는다.</b></li>")
    if fx.get("warning_count"):
        kind = fx.get("trigger_kind")
        if kind == "US_TIGHTENING":
            facts.append(
                "<li><b>⚠ 장기채 함의</b>: 종료 경고 원인이 <b>미국 긴축 전환</b>이다. "
                "과거 국면 종료 직후 10년물 12개월 수익 중앙값 −0.3%로 "
                "무조건 진입(+3.9%) 대비 4.2%p 열위였다.</li>")
        elif kind == "NON_US_SHOCK":
            facts.append(
                "<li><b>장기채 함의</b>: 원인이 <b>미국 외 충격</b>이다. 2018-10형처럼 "
                "연준이 완화로 돌아서면 장기채가 최고 성적(+16.2%)을 낸 전례가 있다.</li>")
        else:
            facts.append(
                "<li><b>장기채 함의</b>: 경고는 켜졌으나 원인이 특정되지 않아 판단을 보류한다.</li>")
    bits = []
    if ctx.get("hy_oas") is not None:
        bits.append(f"하이일드 스프레드 {ctx['hy_oas']:.2f}%p")
    if ctx.get("vix") is not None:
        bits.append(f"VIX {ctx['vix']:.1f}")
    if bits:
        facts.append(f"<li><b>위험 보상 맥락</b>: {', '.join(bits)}. "
                     "스프레드가 좁을수록 위험 대비 보상이 얇다.</li>")

    dur = f" · {months}개월째" if months else ""
    gap_line = (f"현물 {gap['spot']:,.1f}원 vs 36개월선 {gap['ma36']:,.1f}원 "
                f"({gap['pct']:+.1f}%){dur}") if gap else ""

    return f"""
        <div class="card" style="margin-bottom:40px;">
            <h2>💱 1.7 환율 국면 (FRS)
                <span style="font-size:0.8rem; color:#94A3B8;">(근거 제공 · 포지션 지시 아님)</span></h2>
            <div class="score-display">
                <div class="score-number" style="color:{color}">{score:+.0f}</div>
                <div class="score-text">{_esc(fx.get('label', ''))}</div>
                <div style="color:#94A3B8; margin-top:8px; font-size:0.9em">
                    −100~+100 · (+)=원화 강세 압력 · 커버리지 {fx.get('coverage', 0) * 100:.0f}%
                </div>
                <div style="color:#CBD5E1; margin-top:10px;">{gap_line}</div>
            </div>

            <table>
                <tr><th>요인</th><th style="text-align:right">가중</th>
                    <th style="text-align:right">점수</th><th>근거</th></tr>
                {factor_rows}
            </table>

            <h3 style="margin-top:25px; color:#CBD5E1;">
                국면 전환 경고 — {_esc(fx.get('warning_level', ''))} ({fx.get('warning_count', 0)}/4)</h3>
            <table>
                <tr><th>감지기</th><th style="text-align:center">상태</th>
                    <th>근거</th><th>실측 예측력</th></tr>
                {warn_rows}
            </table>
            <p style="color:#94A3B8; font-size:0.85em; margin-top:10px;">
                예측력은 2008~2026 하회 국면 83개월 백테스트 리프트(1.0 = 정보 없음).
                켜진 경고를 전부 같은 무게로 읽으면 안 된다.</p>

            <h3 style="margin-top:25px; color:#CBD5E1;">달러 자산 맥락 (판단 재료 — 추천 아님)</h3>
            <ul style="color:#CBD5E1; padding-left:20px; line-height:1.8;">{''.join(facts)}</ul>
        </div>
"""


# ─────────────────────────────────────────────────────────────
# 2026-09-10 이식 — 마크다운엔 있는데 HTML엔 없던 섹션들
#
# 이 저장소는 리포트 렌더러가 둘인데(markdown.py / html_new.py) 사용자가
# 매일 이메일로 받고 docs/report.html로 보는 건 **HTML 쪽**이다. 그런데
# 실측해보니 HTML에 Executive Summary·Action Plan·시나리오·논의사항·
# 경제캘린더가 통째로 빠져 있었다(마크다운엔 Action Plan만 11군데).
#
# 구현 자체는 engine/report/html.py에 있었지만 그 파일의 render_html은
# 아무 데서도 호출되지 않는 죽은 코드였다 — "구현은 있는데 전달은 안 되는"
# 상태로 방치돼 있었다. 여기로 옮기고 html.py는 삭제한다.
#
# ⚠ 마크업을 그대로 복사하지 않았다. html.py는 밝은 테마(--surface 등)에
# <section class="card">를 쓰고 이 파일은 어두운 그라데이션에 자체 인라인
# CSS를 쓴다 — 클래스가 서로 없다. 내용만 가져오고 표현은 이 파일 양식
# (.card / <h2> / <table>)으로 다시 썼다.

_TIER_LABEL = {
    5: "★★★★★ 반드시 확인/실행", 4: "★★★★☆ 검토", 3: "★★★☆☆ 관찰",
    2: "★★☆☆☆ 참고", 1: "보류",
}
_TIER_COLOR = {5: "#EF4444", 4: "#F59E0B", 3: "#38BDF8", 2: "#94A3B8", 1: "#64748B"}


def _kv_rows(rows) -> str:
    return "".join(
        f'<div class="metric"><span class="metric-label">{k}</span>'
        f'<span style="text-align:right;max-width:70%">{v}</span></div>'
        for k, v in rows)


_STATUS_KR = {
    "ok": "정상", "stale": "이월", "pending": "미수집",
    "not_released": "미발표", "source_error": "수집실패",
}


def _fmt_num(value, suffix: str = "") -> str:
    if value is None:
        return '<span style="color:#64748B">Pending</span>'
    if isinstance(value, (int, float)):
        return f"{value:,.2f}{suffix}"
    return _esc(value)


def _sparkline_svg(history, years: int, width: int = 176, height: int = 44) -> str:
    """표 칸 안에 들어가는 자립형 SVG 추세선.

    2026-09-10 이식 — 단일 색상(판단이 아니라 크기·추세 표현), 2px 선,
    점마다 숫자를 찍지 않고 양끝만 직접 라벨링, 호버는 네이티브 <title>로
    처리해 차트 라이브러리를 안 쓴다. 색만 이 파일의 어두운 테마에 맞게
    var(--accent) → 고정 색으로 바꿨다(이 파일엔 CSS 변수가 없다)."""
    history = history or []
    if len(history) < 2:
        return f'<span style="color:#64748B; font-size:0.8em">{years}년 이력 부족</span>'
    values = [h["value"] for h in history]
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0
    pad = 4
    n = len(values)

    def x(i):
        return pad + (width - 2 * pad) * i / (n - 1)

    def y(v):
        return height - pad - (height - 2 * pad) * (v - lo) / span

    points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))
    start_date, end_date = history[0]["date"][:7], history[-1]["date"][:7]
    start_val, end_val = values[0], values[-1]
    tooltip = _esc(f"{start_date} {start_val:.2f} → {end_date} {end_val:.2f}")
    return (
        f'<svg class="spark" viewBox="0 0 {width} {height}" width="{width}" height="{height}"'
        f' role="img" aria-label="{tooltip}"><title>{tooltip}</title>'
        f'<polyline points="{points}" fill="none" stroke="#38BDF8" stroke-width="2"'
        ' stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{x(n - 1):.1f}" cy="{y(end_val):.1f}" r="2.5" fill="#38BDF8"/></svg>'
        f'<div style="display:flex;justify-content:space-between;color:#64748B;font-size:0.7em">'
        f'<span>{_esc(start_date)}·{start_val:.1f}</span>'
        f'<span>{_esc(end_date)}·{end_val:.1f}</span></div>')


def _render_macro_dashboard(payload: dict, dashboard_key: str = "macro_dashboard",
                            title: str = "Macro Dashboard") -> str:
    """10개 거시 지표 표 + 10년 추세 스파크라인.

    ⚠ 2026-09-10 발견 — 이 섹션이 production HTML에 **통째로 없었다**.
    마크다운 §1은 "거시 경제 대시보드"로 10개 지표를 싣는데, 매일 이메일로
    나가는 HTML엔 실질 GDP도 실업률도 한 줄이 없었다. 구현은 죽은
    html.py에만 있었다.

    † ‡ 각주는 그대로 옮겼다 — "이월"과 "전월 스냅샷 없어 원자료 이력 사용"을
    구분해 표기하는 게 R2·R3의 실무적 표현이라, 표기가 사라지면 이월값이
    실시간값처럼 보인다."""
    rows_data = payload.get(dashboard_key) or []
    if not rows_data:
        return ""
    has_fallback = any(r.get("previous_source") == "series_history" for r in rows_data)
    has_stale = any(r.get("status") == "stale" for r in rows_data)

    rows = ""
    for r in rows_data:
        stale_mark = ('<sup style="color:#F59E0B" title="오늘 실시간 조회 실패 — 마지막으로 확인된 값 유지 중">‡</sup>'
                      if r.get("status") == "stale" else "")
        fallback_mark = ('<sup style="color:#94A3B8" title="전월 리포트 스냅샷이 아직 없어 원자료 이력의 직전 값을 사용">†</sup>'
                         if r.get("previous_source") == "series_history" else "")
        source = r.get("source") or _STATUS_KR.get(r.get("status"), r.get("status"))
        rows += (
            f'<tr><td>{_esc(r.get("indicator"))}</td>'
            f'<td>{_fmt_num(r.get("current"))}{stale_mark}</td>'
            f'<td>{_fmt_num(r.get("previous"))}{fallback_mark}</td>'
            f'<td>{_esc(r.get("trend"))}</td><td>{_fmt_num(r.get("score"))}</td>'
            f'<td>{_sparkline_svg(r.get("history"), r.get("history_years", 10))}</td>'
            f'<td style="color:#94A3B8; font-size:0.85em">{_esc(source)}</td></tr>')

    notes = []
    if has_stale:
        notes.append("‡ 오늘 실시간 조회에 실패한 지표입니다 — 마지막으로 확인된 값을 "
                     "그대로 유지해 표시했습니다(추측·대체 데이터 아님).")
    if has_fallback:
        notes.append("† 전월 PEOS 리포트가 아직 쌓이지 않아, 해당 지표는 원자료(공식 통계) "
                     "이력의 직전 발표값으로 대체 표시했습니다.")
    footnote = (f'<p style="color:#94A3B8; font-size:0.82em; margin-top:12px;">{" ".join(notes)}</p>'
                if notes else "")

    return (
        '\n        <div class="card" style="margin-bottom:40px;">\n'
        f'            <h2>📊 {_esc(title)}</h2>\n'
        '            <table><tr><th>지표</th><th>현재</th><th>이전</th><th>추세</th>'
        '<th>점수</th><th>10년 추세</th><th>출처</th></tr>'
        f'{rows}</table>\n'
        f'            {footnote}\n'
        '        </div>\n'
    )


def _render_us_macro_dashboard(payload: dict) -> str:
    if not payload.get("us_macro_dashboard"):
        return ""
    return _render_macro_dashboard(payload, "us_macro_dashboard", "US Macro Dashboard")


def _render_executive_summary(payload: dict) -> str:
    macro = payload.get("macro")
    brief = payload.get("personal_executive_brief")
    if not macro or not brief:
        return ""
    actions = payload.get("actions") or []
    changes = "; ".join(c["message"] for c in macro.get("changes", [])[:3]) or "데이터 부족"
    readiness = payload.get("report_readiness", "")
    rc = {"final": "#10B981", "draft": "#94A3B8"}.get(readiness, "#F59E0B")
    transition = (f"({_esc(macro.get('transition'))})" if macro.get("transition")
                  else "(변동 없음)")
    rows = [
        ("현재 경기 국면",
         f"{_esc(macro.get('regime'))} ({_esc(macro.get('score_band_label'))}, 총점 {macro.get('score')})"),
        ("지난달 대비 변화",
         f"{_esc(macro.get('previous_regime'))} → {_esc(macro.get('regime'))} {transition}"),
        ("핵심 원인", _esc(changes)),
        ("사용자에게 중요한 의미", _esc(brief.get("one_line_diagnosis"))),
        ("이번 달 핵심 행동",
         _esc(actions[0]["title"]) if actions else "핵심 지표 확보 후 재평가 필요"),
        ("리포트 충족도",
         f'<span style="color:{rc};font-weight:600">{_esc(readiness)}</span>'),
    ]
    return (
        '\n        <div class="card" style="margin-bottom:40px;">\n'
        '            <h2>📋 Executive Summary</h2>\n'
        f'            {_kv_rows(rows)}\n'
        '        </div>\n'
    )


def _render_action_plan(payload: dict) -> str:
    actions = payload.get("actions") or []
    if not actions:
        return ""
    by_tier: dict[int, list] = {}
    for a in actions:
        by_tier.setdefault(a.get("priority", 3), []).append(a)

    groups = []
    for tier in (5, 4, 3, 2, 1):
        items = by_tier.get(tier)
        if not items:
            continue
        color = _TIER_COLOR[tier]
        cards = ""
        for a in items:
            conflict = (f'<div><b style="color:#F59E0B">조정</b> {_esc(a["conflict_note"])}</div>'
                        if a.get("conflict_note") else "")
            cards += (
                f'<div style="border-left:3px solid {color}; padding:12px 16px; margin:12px 0;'
                ' background:rgba(0,0,0,0.25); border-radius:6px;">'
                f'<div style="font-weight:600; color:#F1F5F9; margin-bottom:8px;">{_esc(a.get("title"))}</div>'
                '<div style="color:#CBD5E1; font-size:0.92em; line-height:1.7;">'
                f'<div><b style="color:#94A3B8">이유</b> {_esc(a.get("reason"))}</div>'
                f'<div><b style="color:#94A3B8">보류 조건</b> {_esc(a.get("invalid_condition"))}</div>'
                f'<div><b style="color:#94A3B8">재점검</b> {_esc(a.get("recheck"))}</div>'
                f'{conflict}</div></div>')
        groups.append(
            f'<h3 style="margin-top:20px; color:{color};">{_esc(_TIER_LABEL[tier])}</h3>{cards}')

    return (
        '\n        <div class="card" style="margin-bottom:40px;">\n'
        '            <h2>✅ 이번 달 Action Plan</h2>\n'
        f'            {"".join(groups)}\n'
        '        </div>\n'
    )


def _render_scenarios(payload: dict) -> str:
    s = payload.get("scenarios")
    if not s:
        return ""
    colors = {"base": "#38BDF8", "bull": "#10B981", "bear": "#EF4444"}
    cards = ""
    for name, label in (("base", "Base"), ("bull", "Bull"), ("bear", "Bear")):
        item = s.get(name)
        if not isinstance(item, dict):
            continue
        cards += (
            f'<div class="card" style="border-top:3px solid {colors[name]};">'
            f'<h3 style="color:{colors[name]}; margin-bottom:12px;">{label}'
            f'<span style="float:right; color:#CBD5E1;">{item.get("probability")}%</span></h3>'
            f'<p style="color:#CBD5E1; margin:8px 0;"><b>전제</b> {_esc(item.get("premise"))}</p>'
            f'<p style="color:#CBD5E1; margin:8px 0;"><b>기대되는 변화</b> {_esc(item.get("expected_change"))}</p>'
            f'<p style="color:#CBD5E1; margin:8px 0;"><b>사용자 영향</b> {_esc(item.get("user_impact"))}</p>'
            '</div>')
    conditions = "".join(f"<li>{_esc(c)}</li>" for c in s.get("invalid_conditions", []))
    return (
        '\n        <div class="card" style="margin-bottom:40px;">\n'
        '            <h2>🔀 시나리오 분석</h2>\n'
        f'            <div class="grid-2" style="margin:20px 0;">{cards}</div>\n'
        '            <h3 style="color:#CBD5E1;">깨지는 조건</h3>\n'
        f'            <ul style="color:#CBD5E1; padding-left:20px; line-height:1.8;">{conditions}</ul>\n'
        '        </div>\n'
    )


def _render_calendar(payload: dict) -> str:
    events = payload.get("calendar") or []
    if not events:
        # 없는 걸 "확정된 일정 없음"으로 매일 찍으면 그것도 신호처럼 읽힌다 —
        # 이벤트가 없으면 섹션 자체를 생략한다(R3).
        return ""
    rows = "".join(
        f'<tr><td>{_esc(e.get("date"))}</td><td>{_esc(e.get("name"))}</td>'
        f'<td>{_esc(e.get("importance_label"))}</td><td>{e.get("priority_score")}점</td></tr>'
        for e in events)
    return (
        '\n        <div class="card" style="margin-bottom:40px;">\n'
        '            <h2>🗓️ 경제 캘린더</h2>\n'
        '            <table><tr><th>날짜</th><th>이벤트</th><th>중요도</th><th>영향도</th></tr>'
        f'{rows}</table>\n'
        '        </div>\n'
    )


def _render_discussion(payload: dict) -> str:
    """논의가 필요한 결정 사항 — 답변을 적어 복사·이슈 제출할 수 있는 섹션.

    ⚠ 이메일 본문에서는 JS가 동작하지 않는다. 그래도 넣는 이유는 이 리포트가
    docs/report.html로도 게시되고 거기서는 버튼이 실제로 동작하기 때문이다.
    이메일에서는 질문과 입력칸이 정적으로 보일 뿐 손해가 없다."""
    points = payload.get("discussion_points") or []
    if not points:
        return ""
    cards = ""
    for p in points:
        cards += (
            f'<div class="discuss-card" data-id="{_esc(p.get("id"))}"'
            f' data-topic="{_esc(p.get("topic"))}" data-question="{_esc(p.get("question"))}"'
            ' style="background:rgba(0,0,0,0.25); border-radius:8px; padding:16px; margin:12px 0;">'
            f'<div style="font-weight:600; color:#F1F5F9;">💬 {_esc(p.get("topic"))}</div>'
            f'<p style="color:#94A3B8; font-size:0.92em; margin:8px 0;">{_esc(p.get("context"))}</p>'
            f'<p style="color:#CBD5E1; margin:8px 0;">{_esc(p.get("question"))}</p>'
            '<textarea class="discuss-input" rows="3" style="width:100%;'
            ' background:rgba(15,23,42,0.8); color:#E2E8F0; border:1px solid #334155;'
            ' border-radius:6px; padding:8px;"'
            ' placeholder="생각을 적어보세요 (비워두면 복사·제출에서 빠집니다)"></textarea>'
            '<div style="margin-top:8px;">'
            '<button type="button" class="btn-fb" onclick="peosCopyOne(this)">📋 이 답변 복사</button>'
            '<button type="button" class="btn-fb" onclick="peosIssueOne(this)">🔗 GitHub Issue로 제출</button>'
            '</div></div>')
    return (
        '\n        <div class="card" style="margin-bottom:40px;">\n'
        '            <h2>🗣️ 논의가 필요한 결정 사항</h2>\n'
        f'            {cards}\n'
        '            <div style="margin-top:16px;">'
        '<button type="button" class="btn-fb" onclick="peosCopyAll(this)">📋 작성한 답변 전체 복사</button>'
        '<span style="color:#94A3B8; font-size:0.85em;">비워둔 항목은 자동 제외됩니다.'
        ' "GitHub Issue로 제출"은 공개 저장소에 남으니 공개돼도 괜찮은 항목에만 사용하세요.</span>'
        '</div>\n        </div>\n'
    )


def _render_personal_brief(payload: dict) -> str:
    b = payload.get("personal_executive_brief")
    if not b:
        return ""
    summary = ", ".join(f"{k}={v}" for k, v in (b.get("asset_summary") or {}).items() if v)
    events = "; ".join(b.get("top_events") or []) or "없음"
    rows = [("한 줄 진단", _esc(b.get("one_line_diagnosis"))),
            ("자산 요약", _esc(summary) if summary else "—"),
            ("주요 이벤트", _esc(events))]
    return (
        '\n        <div class="card" style="margin-bottom:40px;">\n'
        '            <h2>🧾 Personal Executive Brief</h2>\n'
        f'            {_kv_rows(rows)}\n'
        '        </div>\n'
    )


_FEEDBACK_JS = """
function peosFindCard(el) { return el.closest('.discuss-card'); }

function peosBuildEntry(card) {
  var ta = card.querySelector('textarea');
  var val = (ta.value || '').trim();
  if (!val) return null;
  return { topic: card.dataset.topic, question: card.dataset.question, answer: val };
}

function peosEntryText(entry) {
  return '### ' + entry.topic + '\\n질문: ' + entry.question + '\\n답변: ' + entry.answer;
}

// Some viewers (e.g. a preview rendered inside a sandboxed iframe) block
// navigator.clipboard, document.execCommand('copy'), window.alert, and
// window.open outright — silently, with no error thrown, and even
// programmatic focus()/select() can land the browser's actual selection
// somewhere else entirely (that's what copied the whole page once already).
// So: no modal, no scripted select() the user has to trust blindly. One
// always-visible, always-in-place output box; the user clicks into it
// themselves and selects with their own Ctrl+A, which is native browser
// behavior no page script can misdirect.
function peosShowOutput(message, text, linkUrl) {
  var box = document.getElementById('peos-copy-output');
  var msgEl = document.getElementById('peos-copy-output-msg');
  var taEl = document.getElementById('peos-copy-output-text');
  var linkEl = document.getElementById('peos-copy-output-link');
  msgEl.textContent = message;
  taEl.value = text || '';
  if (linkUrl) {
    linkEl.style.display = 'inline-block';
    linkEl.href = linkUrl;
  } else {
    linkEl.style.display = 'none';
    linkEl.removeAttribute('href');
  }
  if (box.scrollIntoView) box.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function peosCopyText(text, btn) {
  // Best-effort only — never trusted as the source of truth for whether the
  // copy actually landed on the system clipboard, since these can silently
  // no-op or misfire depending on the viewer.
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text);
  } catch (e) { /* ignore */ }
  peosShowOutput(
    '아래 박스에 복사할 내용을 넣어뒀습니다. 자동 복사를 시도했지만 확실하지 않으니, ' +
    '박스를 직접 클릭한 뒤 Ctrl+A(Mac: Cmd+A) → Ctrl+C(Mac: Cmd+C)로 복사해주세요.',
    text, null
  );
}

function peosCopyOne(btn) {
  var entry = peosBuildEntry(peosFindCard(btn));
  if (!entry) { peosShowOutput('먼저 답변을 입력해주세요.', '', null); return; }
  peosCopyText(peosEntryText(entry), btn);
}

function peosCopyAll(btn) {
  var section = document.getElementById('discussion-section');
  var month = section.dataset.month;
  var cards = section.querySelectorAll('.discuss-card');
  var parts = [];
  cards.forEach(function (card) {
    var entry = peosBuildEntry(card);
    if (entry) parts.push(peosEntryText(entry));
  });
  if (!parts.length) { peosShowOutput('입력한 답변이 없습니다.', '', null); return; }
  peosCopyText('PEOS ' + month + ' 리포트 피드백\\n\\n' + parts.join('\\n\\n'), btn);
}

function peosIssueOne(btn) {
  var card = peosFindCard(btn);
  var entry = peosBuildEntry(card);
  if (!entry) { peosShowOutput('먼저 답변을 입력해주세요.', '', null); return; }
  var section = document.getElementById('discussion-section');
  var repo = section.dataset.repo;
  var month = section.dataset.month;
  if (!repo) { peosShowOutput('연결된 GitHub 저장소 정보가 없습니다.', '', null); return; }
  var title = encodeURIComponent('[피드백] ' + month + ' - ' + entry.topic);
  var body = encodeURIComponent('**질문**\\n' + entry.question + '\\n\\n**답변**\\n' + entry.answer);
  var url = 'https://github.com/' + repo + '/issues/new?title=' + title + '&body=' + body;
  var opened = null;
  try { opened = window.open(url, '_blank', 'noopener'); } catch (e) { /* blocked — fall through */ }
  if (!opened) {
    peosShowOutput('이 화면에서는 새 창 열기가 막혀 있습니다. 아래 링크를 눌러 GitHub 이슈 작성 페이지로 이동해주세요.', '', url);
  }
}
"""


def render_html(payload: dict) -> str:
    """Render comprehensive PEOS report as beautiful, responsive HTML."""
    month = payload["report_month"]
    cci = payload.get("cci_analysis", {})
    rate = payload.get("rate_analysis", {})

    state_color = {"GREEN": "#10B981", "YELLOW": "#F59E0B", "RED": "#EF4444"}
    cci_state = cci.get("state", "UNKNOWN")
    cci_color = state_color.get(cci_state, "#6B7280")
    cci_rgb = _hex_to_rgb(cci_color)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PEOS 일일 리포트 - {month}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            color: #E2E8F0;
            line-height: 1.6;
            min-height: 100vh;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .header {{
            text-align: center;
            padding: 40px 20px;
            background: rgba(15, 23, 42, 0.5);
            border-bottom: 2px solid #334155;
            margin-bottom: 40px;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; color: #F1F5F9; }}
        .header p {{ color: #CBD5E1; font-size: 1.1em; }}
        .header .date {{ color: #94A3B8; margin-top: 10px; }}

        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 40px; }}
        .card {{
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 30px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}
        .card:hover {{ border-color: #475569; transform: translateY(-2px); }}
        .card h2 {{ font-size: 1.5em; margin-bottom: 20px; color: #F1F5F9; border-bottom: 2px solid #334155; padding-bottom: 15px; }}

        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #334155;
        }}
        .metric:last-child {{ border-bottom: none; }}

        /* 2026-09-10 이식 — 논의 섹션 버튼. html.py에서 옮겨온 섹션이
           쓰는 유일한 클래스라 여기 한 벌만 둔다. */
        .btn-fb {{
            background: rgba(56, 130, 229, 0.15);
            color: #93C5FD;
            border: 1px solid #3987e5;
            border-radius: 6px;
            padding: 6px 12px;
            margin-right: 8px;
            font-size: 0.85em;
            cursor: pointer;
        }}
        .btn-fb:hover {{ background: rgba(56, 130, 229, 0.3); }}
        .metric-label {{ color: #CBD5E1; }}
        .metric-value {{ font-size: 1.3em; font-weight: 600; }}

        .score-display {{
            text-align: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            margin: 20px 0;
        }}
        .score-number {{
            font-size: 3em;
            font-weight: bold;
            color: {cci_color};
            text-shadow: 0 0 20px rgba({cci_rgb}, 0.5);
        }}
        .score-text {{ font-size: 1.2em; color: #CBD5E1; margin-top: 10px; }}

        .state-badge {{
            display: inline-block;
            padding: 8px 16px;
            background-color: {cci_color};
            color: white;
            border-radius: 20px;
            font-weight: 600;
            margin-top: 10px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background: rgba(51, 65, 85, 0.5);
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #475569;
            color: #F1F5F9;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #334155;
        }}
        tr:hover {{ background-color: rgba(51, 65, 85, 0.3); }}

        .portfolio-section {{
            background: rgba(51, 65, 85, 0.2);
            border-left: 4px solid #3B82F6;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
        }}

        .action-box {{
            background: rgba(239, 68, 68, 0.1);
            border: 2px solid #EF4444;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
        }}

        .action-box.green {{
            background: rgba(16, 185, 129, 0.1);
            border-color: #10B981;
        }}

        .action-box.yellow {{
            background: rgba(245, 158, 11, 0.1);
            border-color: #F59E0B;
        }}

        .tag {{
            display: inline-block;
            padding: 4px 12px;
            background: rgba(59, 130, 246, 0.2);
            border: 1px solid #3B82F6;
            border-radius: 4px;
            font-size: 0.9em;
            margin: 4px 4px 4px 0;
            color: #93C5FD;
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #64748B;
            border-top: 1px solid #334155;
            margin-top: 40px;
        }}

        @media (max-width: 900px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 PEOS 일일 리포트</h1>
            <p>매일 자동 생성 · 기준월 {month}</p>
            <div class="date">{datetime.now().strftime('%Y년 %m월 %d일')} 생성</div>
        </div>

        {_render_executive_summary(payload)}

        {_render_exposure_and_reconciliation(payload)}

        {_render_fx_regime(payload)}

        {_render_macro_dashboard(payload)}

        {_render_us_macro_dashboard(payload)}

        <div class="grid-2">
            <!-- CCI 카드 -->
            <div class="card">
                <h2>🚨 위기지수 분석 (CCI)</h2>
                <div class="score-display">
                    <div class="score-number">{cci.get('total_score', '--')}/100</div>
                    <div class="score-text">{cci_state}</div>
                    <div class="state-badge">{_state_label(cci_state)}</div>
                </div>

                <h3 style="margin-top: 25px; color: #CBD5E1;">모듈별 점수</h3>
                <table>
                    <tr>
                        <th>지표</th>
                        <th>점수</th>
                        <th>신선도</th>
                    </tr>
                    {_cci_module_rows(cci)}
                </table>
            </div>

            <!-- Rate Analysis 카드 -->
            <div class="card">
                <h2>💰 금리 분석 (Rate Analysis)</h2>
                <div class="score-display">
                    <div class="score-number">{rate.get('total_score', '--')}/100</div>
                    <div class="score-text">{_rate_state_label(rate.get('total_score', 0))}</div>
                </div>

                <h3 style="margin-top: 25px; color: #CBD5E1;">현재 금리</h3>
                <div class="metric">
                    <span class="metric-label">US 10Y Treasury</span>
                    <span class="metric-value">{rate.get('current_rates', {}).get('us_10y', 'N/A')}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">KR 10Y Bond</span>
                    <span class="metric-value">{_rate_or_missing(rate.get('current_rates', {}), 'kr_10y')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Spread</span>
                    <span class="metric-value">{_rate_or_missing(rate.get('current_rates', {}), 'spread_bp', ' bp')}</span>
                </div>

                {_stale_series_note(rate)}

                <h3 style="margin-top: 25px; color: #CBD5E1;">금리 컴포넌트</h3>
                <table>
                    <tr>
                        <th>항목</th>
                        <th>점수</th>
                    </tr>
                    <tr>
                        <td>절대 금리 수준</td>
                        <td>{rate.get('score_components', {}).get('absolute_rates', 0)}/30</td>
                    </tr>
                    <tr>
                        <td>추세 분석</td>
                        <td>{rate.get('score_components', {}).get('trend_analysis', 0)}/30</td>
                    </tr>
                    <tr>
                        <td>금리차 (Spread)</td>
                        <td>{rate.get('score_components', {}).get('spread', 0)}/25</td>
                    </tr>
                    <tr>
                        <td>시장 신호</td>
                        <td>{rate.get('score_components', {}).get('market_signals', 0)}/15</td>
                    </tr>
                </table>
            </div>
        </div>

        <!-- SK하이닉스 액션 플랜 -->
        <div class="card" style="margin-bottom: 30px;">
            <h2>🎯 위기지수 기반 위험환경 정보 <span style="font-size:0.8rem; color:#94A3B8;">(포지션 지시 아님)</span></h2>
            <p style="color:#FBBF24; background:rgba(251,191,36,0.1); padding:10px 12px; border-radius:8px; margin-bottom:14px;">
                R4 — 종목 매수/매도 지시는 SK하이닉스 의사결정 엔진만 낼 수 있습니다.
                아래 문구는 위기 국면 서술이며, 0.5절의 판정을 우선하십시오.
            </p>
            {_render_sk_hynix_action(cci.get('sk_hynix_action', {}))}
        </div>

        <!-- 2026-09-02: 부동산 실거래가 동향(매매 3종 + 전세) + 청약 우려사항은
             engine/report/subscription_report.py(별도 daily "청약 리포트")로
             이관 — 사용자 요청 "PEOS는 너무 무거워서 좀 나눠야해". -->

        <!-- 포트폴리오 추천 -->
        <div class="card" style="margin-bottom: 30px;">
            <h2>📈 포트폴리오 추천 (금리 기반)</h2>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0;">
                <div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #3B82F6;">
                    <div style="font-size: 2em; font-weight: bold; color: #93C5FD;">{rate.get('portfolio_recommendation', {}).get('stocks', '--')}%</div>
                    <div style="color: #CBD5E1; margin-top: 10px;">주식 (Stocks)</div>
                </div>
                <div style="background: rgba(34, 197, 94, 0.1); padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #22C55E;">
                    <div style="font-size: 2em; font-weight: bold; color: #86EFAC;">{rate.get('portfolio_recommendation', {}).get('bonds', '--')}%</div>
                    <div style="color: #CBD5E1; margin-top: 10px;">채권 (Bonds)</div>
                </div>
                <div style="background: rgba(168, 85, 247, 0.1); padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #A855F7;">
                    <div style="font-size: 2em; font-weight: bold; color: #D8B4FE;">{rate.get('portfolio_recommendation', {}).get('cash', '--')}%</div>
                    <div style="color: #CBD5E1; margin-top: 10px;">현금 (Cash)</div>
                </div>
            </div>
            <div class="portfolio-section">
                <strong>상태:</strong> {rate.get('portfolio_recommendation', {}).get('condition', 'N/A')}
                <br><br>
                <strong>리밸런싱 트리거:</strong> {rate.get('portfolio_recommendation', {}).get('rebalance_trigger', '--')} 점
            </div>
        </div>

        <!-- SK하이닉스 아웃룩 -->
        <div class="card" style="margin-bottom: 30px;">
            <h2>🔮 SK하이닉스 전망 (3개월/6개월/12개월)</h2>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0;">
                <div style="background: rgba(34, 197, 94, 0.1); padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.8em; font-weight: bold; color: #86EFAC;">{rate.get('sk_hynix_outlook', {}).get('3m_upside_probability', '--')}%</div>
                    <div style="color: #CBD5E1; margin-top: 10px;">3개월 상승확률</div>
                </div>
                <div style="background: rgba(34, 197, 94, 0.1); padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.8em; font-weight: bold; color: #86EFAC;">{rate.get('sk_hynix_outlook', {}).get('6m_upside_probability', '--')}%</div>
                    <div style="color: #CBD5E1; margin-top: 10px;">6개월 상승확률</div>
                </div>
                <div style="background: rgba(34, 197, 94, 0.1); padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.8em; font-weight: bold; color: #86EFAC;">{rate.get('sk_hynix_outlook', {}).get('12m_upside_probability', '--')}%</div>
                    <div style="color: #CBD5E1; margin-top: 10px;">12개월 상승확률</div>
                </div>
            </div>
            <div class="portfolio-section">
                <strong>근거:</strong> {rate.get('sk_hynix_outlook', {}).get('rationale', 'N/A')}
            </div>
        </div>

        {_render_action_plan(payload)}

        {_render_scenarios(payload)}

        {_render_calendar(payload)}

        {_render_discussion(payload)}

        {_render_personal_brief(payload)}

        <div class="footer">
            <p>PEOS Monthly Report © 2026 | 생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} KST</p>
        </div>
    </div>
    <script>{_FEEDBACK_JS}</script>
</body>
</html>"""
    return html
