"""Enhanced HTML renderer for PEOS report with CCI + Rate Analysis integrated display."""
from __future__ import annotations
from datetime import datetime


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


def render_html(payload: dict) -> str:
    """Render comprehensive PEOS report as beautiful, responsive HTML."""
    month = payload["report_month"]
    cci = payload.get("cci_analysis", {})
    rate = payload.get("rate_analysis", {})
    real_estate = payload.get("real_estate", {})
    real_estate_rent = payload.get("real_estate_rent", {})
    real_estate_villa = payload.get("real_estate_villa", {})
    real_estate_officetel = payload.get("real_estate_officetel", {})

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

        {_render_exposure_and_reconciliation(payload)}

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

        <!-- 부동산 실거래가 동향 -->
        {_render_real_estate_section(real_estate)}
        {_render_rent_section(real_estate_rent)}
        {_render_villa_section(real_estate_villa)}
        {_render_officetel_section(real_estate_officetel)}

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

        <div class="footer">
            <p>PEOS Monthly Report © 2026 | 생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} KST</p>
        </div>
    </div>
</body>
</html>"""
    return html
