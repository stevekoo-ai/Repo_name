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
                <strong style="color: #CBD5E1;">Action</strong>
                <div style="font-size: 1.2em; color: #F1F5F9; margin-top: 5px;">{action_type}</div>
            </div>
            <div>
                <strong style="color: #CBD5E1;">Max Weight</strong>
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


def _render_real_estate_placeholder(status_label: str, note: str) -> str:
    return f"""
        <div class="card" style="margin-bottom: 30px;">
            <h2>🏘️ 부동산 실거래가 동향 (국토교통부 실거래가 공개시스템)</h2>
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


def _render_real_estate_section(re_data: dict) -> str:
    if not re_data:
        return ""

    if re_data.get("fetch_status") == "pending":
        return _render_real_estate_placeholder("Pending", re_data.get('fetch_note', 'MOLIT_API_KEY 미설정'))

    tiers = re_data.get("tiers", {})
    any_ok = any(t.get("data_status") == "ok" for t in tiers.values())
    if not any_ok:
        return _render_real_estate_placeholder("Source Error", re_data.get('fetch_note', '국토교통부 API 응답 없음'))

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
            <h2>🏘️ 부동산 실거래가 동향 (국토교통부 실거래가 공개시스템)</h2>
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


def render_html(payload: dict) -> str:
    """Render comprehensive PEOS report as beautiful, responsive HTML."""
    month = payload["report_month"]
    cci = payload.get("cci_analysis", {})
    rate = payload.get("rate_analysis", {})
    real_estate = payload.get("real_estate", {})

    state_color = {"GREEN": "#10B981", "YELLOW": "#F59E0B", "RED": "#EF4444"}
    cci_state = cci.get("state", "UNKNOWN")
    cci_color = state_color.get(cci_state, "#6B7280")
    cci_rgb = _hex_to_rgb(cci_color)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PEOS 월간 리포트 - {month}</title>
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
            <h1>📊 PEOS 월간 리포트</h1>
            <p>{month}</p>
            <div class="date">{datetime.now().strftime('%Y년 %m월 %d일')}</div>
        </div>

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
                    </tr>
                    <tr>
                        <td>Sahm Rule (고용)</td>
                        <td><strong>{cci.get('score_components', {}).get('sahm', 0)}/20</strong></td>
                    </tr>
                    <tr>
                        <td>Yield Curve</td>
                        <td><strong>{cci.get('score_components', {}).get('yield_curve', 0)}/15</strong></td>
                    </tr>
                    <tr>
                        <td>Harvey Filter</td>
                        <td><strong>{cci.get('score_components', {}).get('harvey', 0)}/15</strong></td>
                    </tr>
                    <tr>
                        <td>Credit OAS</td>
                        <td><strong>{cci.get('score_components', {}).get('credit_oas', 0)}/15</strong></td>
                    </tr>
                    <tr>
                        <td>Semiconductor Cycle</td>
                        <td><strong>{cci.get('score_components', {}).get('semiconductor', 0)}/10</strong></td>
                    </tr>
                    <tr>
                        <td>기타 지표</td>
                        <td><strong>{cci.get('score_components', {}).get('copper_gold', 0) + cci.get('score_components', {}).get('buffett', 0) + cci.get('score_components', {}).get('rule_of_20', 0) + cci.get('score_components', {}).get('k_sahm', 0)}</strong></td>
                    </tr>
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
                    <span class="metric-value">{rate.get('current_rates', {}).get('kr_10y', 'N/A')}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Spread</span>
                    <span class="metric-value">{rate.get('current_rates', {}).get('spread_bp', 'N/A')} bp</span>
                </div>

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

        <!-- SK Hynix 액션 플랜 -->
        <div class="card" style="margin-bottom: 30px;">
            <h2>🎯 SK Hynix 포지션 관리</h2>
            {_render_sk_hynix_action(cci.get('sk_hynix_action', {}))}
        </div>

        <!-- 부동산 실거래가 동향 -->
        {_render_real_estate_section(real_estate)}

        <!-- 포트폴리오 추천 -->
        <div class="card" style="margin-bottom: 30px;">
            <h2>📈 포트폴리오 추천 (Rate 기반)</h2>
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

        <!-- SK Hynix 아웃룩 -->
        <div class="card" style="margin-bottom: 30px;">
            <h2>🔮 SK Hynix 전망 (3M/6M/12M)</h2>
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
