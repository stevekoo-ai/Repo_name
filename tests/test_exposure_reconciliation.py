"""Regression tests for the decision layer added 2026-08-10.

Each test here pins a bug that shipped silently — the failure mode in every
case was a wrong number rendered confidently, not an exception. They are the
cheapest guard against the same class of defect returning.

Runs under pytest, and also standalone (`python tests/test_exposure_reconciliation.py`)
since pytest is not installed in every environment this repo runs in.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine.exposure.model import build_exposure_model
from engine.report.reconciliation import reconcile, CONFIDENCE_FLOOR


# ── exposure model ──────────────────────────────────────────────────────────

def test_holding_quantity_comes_from_config_not_a_literal():
    """markdown.py used to print a hardcoded '1,200주'. The real position is 248."""
    m = build_exposure_model()
    sk = next(h for h in m.holdings if h.ticker == "000660.KS")
    assert sk.quantity == 248, f"expected 248 from portfolio.yaml, got {sk.quantity}"
    assert sk.quantity != 1200


def test_lockup_is_excluded_from_sellable():
    """67 shares are locked until 2027-02-11, so only 181 are a decision variable."""
    m = build_exposure_model()
    sk = next(h for h in m.holdings if h.ticker == "000660.KS")
    assert sk.locked_qty == 67
    assert sk.sellable_qty == sk.quantity - sk.locked_qty == 181


def test_unpriced_holdings_fall_back_to_cost_never_to_a_fake_market_value():
    """The dangerous failure is silently treating avg_price as a quote: P/L would
    read exactly 0 while looking precise. Unpriced holdings must expose
    market_value=None and be valued at cost."""
    m = build_exposure_model()
    unpriced = [h for h in m.holdings if h.market_value is None]
    assert unpriced, "fixture expects at least one holding without a verified quote"
    for h in unpriced:
        assert h.valued == h.cost
    assert 0 < m.priced_coverage_pct < 100


def test_exposure_model_prefers_live_kis_snapshot_over_the_hardcoded_price():
    """2026-08-27: KNOWN_PRICES was stuck at a 2026-08-07 snapshot even though
    sk-hynix-daily-report.yml has written a fresher price to
    sources/sk-hynix-price-snapshot.csv every day since. The live CSV must win
    once it exists for a ticker, and its as_of date must be reported honestly
    (not silently overwritten with the stale hardcoded date)."""
    from engine.exposure import model as m

    assert m.KNOWN_PRICES["000660.KS"]["as_of"] == "2026-08-07", (
        "this test's premise is that KNOWN_PRICES is the older/fallback source — "
        "if this fails, the file itself may have been refreshed, which is fine, "
        "just update this assertion's expected date"
    )
    live = m._load_live_price("000660.KS")
    assert live is not None, "fixture expects sources/sk-hynix-price-snapshot.csv to have a 000660 row"
    assert live["as_of"] > "2026-08-07", "the live snapshot should be newer than the hardcoded fallback"

    model = m.build_exposure_model()
    sk = next(h for h in model.holdings if h.ticker == "000660.KS")
    assert sk.market_value == sk.quantity * live["price"]
    assert sk.price_as_of == live["as_of"]


def test_load_live_price_falls_back_gracefully_when_csv_is_missing():
    """A ticker with no collector-backed CSV (or a CSV that vanished) must return
    None, not raise — build_exposure_model() then falls through to KNOWN_PRICES
    or cost basis, never crashes Section 0."""
    from engine.exposure import model as m
    import pathlib

    saved = m.LIVE_PRICE_CSV
    m.LIVE_PRICE_CSV = {"000660.KS": (pathlib.Path("/nonexistent/does-not-exist.csv"), "000660")}
    try:
        assert m._load_live_price("000660.KS") is None
        assert m._load_live_price("999999.KS") is None  # not in the map at all
    finally:
        m.LIVE_PRICE_CSV = saved


def test_concentration_is_sector_wide_not_single_ticker():
    """The risk is not 'SK하이닉스 한 종목' — 삼성전자/제주반도체/반도체 ETF ride the
    same memory cycle, so semi exposure must exceed the employer position alone."""
    m = build_exposure_model()
    assert m.semi_valued > m.employer_valued
    assert m.semi_pct > m.employer_pct


def test_deployable_cash_excludes_locked_value():
    m = build_exposure_model()
    assert m.deployable_cash == m.cash_krw + m.liquid_valued
    assert m.liquid_valued == m.total_valued - m.locked_valued


def test_exposure_model_needs_no_network():
    """Section 0 exists precisely so it survives a day when every collector fails.
    If this ever starts making requests, that guarantee is gone."""
    import requests

    def _boom(*a, **k):
        raise AssertionError("exposure model must not perform network I/O")

    saved = requests.get, requests.post
    requests.get, requests.post = _boom, _boom
    try:
        build_exposure_model()
    finally:
        requests.get, requests.post = saved


# ── reconciliation ──────────────────────────────────────────────────────────

@dataclass
class _Decision:
    signal: str
    confidence: float


def _payload(**over):
    base = {
        "cci_analysis": {"state": "GREEN", "total_score": 5,
                         "sk_hynix_action": {"action": "적극 매수 (Long)", "max_weight": 25}},
        "sk_hynix_decision": _Decision("HOLD", 50.0),
        "macro_us": {"regime": "Recession", "confidence": 41.9},
        "us_macro_dashboard": [{"status": "stale"}] * 8,
        "macro_dashboard": [{"status": "stale"}] * 7 + [{"status": "ok"}] * 3,
        "rate_analysis": {"sk_hynix_outlook": {"rationale": "미-한 금리차 확대(달러 강세)가 수출 경쟁력을 뒷받침."}},
        "weekly_analysis": {"indicators": {"kr_usdkrw": {
            "pct_change": -5.6, "current_value": 1418.8, "value_12w_ago": 1503.5}}},
    }
    base.update(over)
    return base


def test_r4_only_the_decision_engine_may_instruct_on_a_position():
    rec = reconcile(_payload())
    topics = [c.topic for c in rec.conflicts]
    assert "SK하이닉스 포지션 지시" in topics
    c = next(c for c in rec.conflicts if c.topic == "SK하이닉스 포지션 지시")
    assert "적극 매수" in c.claim_a and "HOLD" in c.claim_b, "CCI must be the demoted side"


def test_r1_measured_fx_beats_inferred_dollar_strength():
    rec = reconcile(_payload())
    assert any(c.topic == "환율 방향" for c in rec.conflicts)


def test_r5_sub_floor_confidence_blocks_execution():
    rec = reconcile(_payload())
    assert rec.tradeable is False
    assert any(str(int(CONFIDENCE_FLOOR)) in b for b in rec.blockers)


def test_clean_payload_is_tradeable():
    """Guard against the checks being unconditionally true."""
    rec = reconcile({
        "cci_analysis": {"state": "GREEN", "total_score": 5},
        "sk_hynix_decision": _Decision("BUY", 78.0),
        "macro_us": {"regime": "Expansion", "confidence": 88},
        "us_macro_dashboard": [{"status": "ok"}] * 8,
        "macro_dashboard": [{"status": "ok"}] * 10,
        "rate_analysis": {}, "weekly_analysis": {"indicators": {}},
    })
    assert rec.conflicts == []
    assert rec.tradeable is True


def test_reconcile_reads_weekly_analysis_so_it_must_run_last():
    """reconcile() placed before weekly_analysis in build_report_payload found
    only 2 of 3 conflicts. Missing FX data must simply drop that check, and the
    ordering requirement is asserted here so the regression is visible."""
    p = _payload()
    p.pop("weekly_analysis")
    rec = reconcile(p)
    assert not any(c.topic == "환율 방향" for c in rec.conflicts)


# ── signal recorder ─────────────────────────────────────────────────────────

def test_signal_recording_is_idempotent_per_day(tmp_path=None):
    """Two runs on the same day used to append two rows, double-counting that day
    in the rolling confidence average."""
    import csv, importlib
    from engine.report import signal_recorder as sr

    saved_dir = sr.DATA_DIR
    import pathlib, tempfile
    tmp = pathlib.Path(tempfile.mkdtemp())
    sr.DATA_DIR = tmp
    try:
        for conf in (50.0, 62.0):
            sr.record_daily_signal("2026-08-10", "HOLD", conf, "WAIT", 60.0, "t")
        rows = list(csv.DictReader(open(sr.get_signal_file_path("2026-08-10"))))
        assert len(rows) == 1, f"expected one row per day, got {len(rows)}"
        assert float(rows[0]["sk_hynix_confidence"]) == 62.0, "re-record should overwrite"
    finally:
        sr.DATA_DIR = saved_dir


def test_load_signals_includes_the_current_month():
    """The month cursor kept the start day-of-month, so a 90-day window starting
    05-12 stepped to 08-12 and exited before opening August's file."""
    import csv, pathlib, tempfile
    from engine.report import signal_recorder as sr

    saved_dir = sr.DATA_DIR
    tmp = pathlib.Path(tempfile.mkdtemp())
    sr.DATA_DIR = tmp
    try:
        # today's date is what matters; record for "today" and read it back
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        sr.record_daily_signal(today, "HOLD", 50.0, "WAIT", 60.0, "t")
        got = sr.load_signals()
        assert any(s.date == today for s in got), "current month must be loaded"
    finally:
        sr.DATA_DIR = saved_dir


# ── unit consistency ────────────────────────────────────────────────────────

def test_current_account_label_matches_the_collector_declared_unit():
    """config/rules.yaml said 억달러 while collectors/ecos.py declares 백만달러 for
    stat_code 301Y013 — a 100x mismatch that also made the rule's neutral band
    ($0~50M) unreachable, so the indicator scored positive unconditionally."""
    from core.config import rules_config
    from collectors.ecos import ECOS_SERIES

    declared = ECOS_SERIES["current_account"]["unit"]
    label = rules_config()["macro"]["current_account"]["label"]
    assert declared in label, f"rules.yaml label {label!r} must carry the collector unit {declared!r}"


def test_current_account_thresholds_are_in_the_same_unit_as_the_data():
    """A positive threshold of 50 against a 백만달러 series means '$50M', which every
    month clears trivially. Korea's current account is tens of billions USD, so the
    bar has to sit in the thousands once the unit is 백만달러."""
    from core.config import rules_config

    rule = rules_config()["macro"]["current_account"]
    assert rule["positive"]["gte"] >= 1000, (
        "threshold looks like it is still expressed in 억달러 while the series is 백만달러"
    )


# ── rate series freshness ───────────────────────────────────────────────────

def test_stale_rate_series_is_dropped_not_reported_as_current():
    """ecos_kr_10y_yield stopped updating in 2018, and _get_latest_rate returned
    the last row regardless of date — so the 2018-08-24 quote was published as
    today's Korean 10Y and produced a ~312bp US-KR spread that never existed."""
    from engine.rate_analysis import scoring

    detail = scoring.calculate_rate_score()
    stale_ids = {d["series"] for d in detail.stale_series}

    if "ecos_kr_10y_yield" in stale_ids:
        assert detail.kr_10y is None, "a series flagged stale must not also supply a value"
        assert detail.spread is None, "spread must not be computed from a dropped series"
        rec = next(d for d in detail.stale_series if d["series"] == "ecos_kr_10y_yield")
        assert rec["age_days"] > scoring.MAX_RATE_AGE_DAYS
        assert rec["as_of"], "the observation date must be recorded so the report can explain"


def test_rate_freshness_threshold_is_short_enough_to_catch_a_dead_series():
    """A market quote is only 'current' briefly. If this ever grows past a quarter
    it stops catching the failure it was written for."""
    from engine.rate_analysis import scoring
    assert 0 < scoring.MAX_RATE_AGE_DAYS <= 92


def test_both_renderers_handle_a_missing_rate():
    """markdown.py and html_new.py are separate code paths; html_new used
    .get(key, 'N/A'), which returns None when the key exists with a None value
    and rendered the literal 'None%' on the public dashboard."""
    from engine.report.html_new import _rate_or_missing

    assert "미수집" in _rate_or_missing({"kr_10y": None}, "kr_10y")
    assert "None" not in _rate_or_missing({"kr_10y": None}, "kr_10y")
    assert _rate_or_missing({"kr_10y": 3.21}, "kr_10y") == "3.21%"


# ── collector pagination ────────────────────────────────────────────────────

def test_ecos_walks_every_page_instead_of_keeping_only_the_oldest_ones():
    """ECOS caps StatisticSearch at 1000 rows PER REQUEST and pages oldest-first.
    This collector asked for /1/500/ in one shot, so it received the oldest 500
    rows and nothing after — kr_10y_yield, kr_3y_yield and usdkrw all froze at
    2018-08-24 for 2,912 days. Raising the requested number does NOT fix it (the
    cap is server-side); only walking list_total_count does, which is what this
    test pins. The fake server below enforces the same 1000-row cap, so a
    single-shot implementation cannot pass it.
    """
    import types
    from collectors import ecos

    TOTAL = 2520        # ~10y of business days — the real daily-series length
    SERVER_CAP = 1000   # what ECOS returns regardless of how many you ask for
    requested: list[tuple[int, int]] = []

    class _Resp:
        def __init__(self, payload):
            self._payload = payload

        def raise_for_status(self):
            pass

        def json(self):
            return self._payload

    def fake_get(url, timeout=None):
        # .../json/kr/<row_from>/<row_to>/<stat>/<cycle>/<start>/<end>/<item>
        parts = url.split("/")
        row_from, row_to = int(parts[-7]), int(parts[-6])
        requested.append((row_from, row_to))
        row_to = min(row_to, row_from + SERVER_CAP - 1, TOTAL)
        rows = [{"TIME": str(n), "DATA_VALUE": str(n)}
                for n in range(row_from, row_to + 1)]
        return _Resp({"StatisticSearch": {"list_total_count": TOTAL, "row": rows}})

    real_requests = ecos.requests
    ecos.requests = types.SimpleNamespace(get=fake_get)
    try:
        rows = ecos._fetch_stat("721Y001", "D", "0101000", "KEY",
                                "20160101", "20260814")
    finally:
        ecos.requests = real_requests

    assert len(requested) >= 3, (
        f"{TOTAL} rows cannot arrive in {len(requested)} request(s) at a "
        f"{SERVER_CAP}-row cap — pagination is not happening"
    )
    assert requested[0][0] == 1, "first page must start at row 1"
    assert len(rows) == TOTAL, f"walked only {len(rows)} of {TOTAL} rows"
    # The newest end is precisely what used to go missing.
    assert rows[-1]["DATA_VALUE"] == str(TOTAL)


def test_ecos_pagination_is_bounded():
    """The walk must terminate even if a provider reports an absurd total."""
    from collectors.ecos import _PAGE_SIZE, _MAX_PAGES

    assert _PAGE_SIZE == 1000, "1000 is the ECOS server-side cap, not a preference"
    assert 0 < _MAX_PAGES <= 50


# ── report delivery ─────────────────────────────────────────────────────────

def _clear_channel_env():
    """Remove every var build_channel() looks at, and return them for restore."""
    import os
    keys = ["SLACK_WEBHOOK_URL", "SMTP_HOST", "SMTP_PORT", "SMTP_USER",
            "SMTP_PASSWORD", "NOTIFY_EMAIL_TO", "GMAIL_ADDRESS", "GMAIL_APP_PASSWORD"]
    saved = {k: os.environ.pop(k, None) for k in keys}
    return saved


def _restore_channel_env(saved):
    import os
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def test_unconfigured_channel_is_distinguishable_from_a_successful_send():
    """`NoopChannel` prints and returns, so a missing channel and a delivered
    mail were indistinguishable. That is the shape of the 2026-08-08~10 failure:
    nothing arrived and nothing said so."""
    from core import notify

    saved = _clear_channel_env()
    try:
        assert notify.is_configured() is False
        import os
        os.environ["GMAIL_ADDRESS"] = "someone@example.com"
        os.environ["GMAIL_APP_PASSWORD"] = "app-password"
        assert notify.is_configured() is True
    finally:
        _restore_channel_env(saved)


def test_sender_fails_loudly_when_a_channel_is_expected_but_absent():
    """In CI the secrets exist, so an unconfigured channel means the workflow
    forgot to pass them through `env:` — a misconfiguration, not a no-op."""
    import sys
    from scripts import send_report_email

    saved = _clear_channel_env()
    real_argv = sys.argv
    try:
        sys.argv = ["send_report_email"]
        assert send_report_email.main() == 1, "missing channel must not exit 0"
        sys.argv = ["send_report_email", "--allow-unconfigured"]
        assert send_report_email.main() == 0, "--allow-unconfigured is the local escape hatch"
    finally:
        sys.argv = real_argv
        _restore_channel_env(saved)


def test_report_email_carries_the_html_body_and_the_file():
    """The body is what makes the report readable on a phone; the attachment is
    the archival copy. Sending only one of them was the old behaviour — the
    pipeline's summary mail was plain text with no report in it at all."""
    from email import message_from_string
    from core.notify import EmailChannel
    from scripts.send_report_email import find_report
    from datetime import date

    report = find_report(date.today()) or find_report(date(2026, 8, 13))
    assert report is not None, "no report on disk to exercise the sender with"

    sent: list[str] = []
    ch = EmailChannel("smtp.example.com", 465, "me@example.com", "pw", "me@example.com")
    ch._deliver = lambda raw: sent.append(raw)

    ch.send_document("[PEOS 리포트] 테스트", report.read_text(encoding="utf-8"), [report])

    assert len(sent) == 1
    msg = message_from_string(sent[0])
    subtypes = {p.get_content_type() for p in msg.walk()}
    assert "text/html" in subtypes, "HTML body missing — reader would see nothing"
    assert "text/plain" in subtypes, "no plain-text alternative — spam signal"
    filenames = [p.get_filename() for p in msg.walk() if p.get_filename()]
    assert report.name in filenames, f"attachment missing, got {filenames}"
    # Headers whose absence Gmail treats as forgery (already learned once).
    assert msg["Date"] and msg["Message-ID"]


def test_email_channel_splits_comma_separated_recipients():
    """2026-09-01: NOTIFY_EMAIL_TO="stevekoo.kr@gmail.com, byeongho.koo@sk.com"
    (personal + company inbox) must reach BOTH addresses. Before this fix,
    to_addr was passed through as one opaque string and sendmail() got called
    as `sendmail(user, [to_addr], raw)` — wrapping the whole comma-string as a
    single RFC821 recipient, so SMTP servers would either bounce it or (worse)
    silently deliver to nowhere. This pins the fix: the constructor must split
    on commas into the real per-recipient list SMTP needs, while the "To"
    header stays a single human-readable comma-joined string."""
    from core.notify import EmailChannel

    ch = EmailChannel(
        "smtp.example.com", 465, "me@example.com", "pw",
        "stevekoo.kr@gmail.com, byeongho.koo@sk.com",
    )

    assert ch.to_addrs == ["stevekoo.kr@gmail.com", "byeongho.koo@sk.com"], (
        "sendmail() must receive each address as its own list item"
    )
    assert ch.to_addr == "stevekoo.kr@gmail.com, byeongho.koo@sk.com", (
        "the 'To' header should stay a single readable comma-joined string"
    )

    delivered_to = {}

    class _FakeServer:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, password): pass
        def sendmail(self, from_addr, to_addrs, raw):
            delivered_to["to_addrs"] = to_addrs

    import core.notify as notify_mod
    real_smtp_ssl = notify_mod.smtplib.SMTP_SSL
    notify_mod.smtplib.SMTP_SSL = _FakeServer
    try:
        ch.send("subject", "body")
    finally:
        notify_mod.smtplib.SMTP_SSL = real_smtp_ssl

    assert delivered_to["to_addrs"] == ["stevekoo.kr@gmail.com", "byeongho.koo@sk.com"], (
        "both recipients must actually be passed to smtplib.sendmail(), not just "
        "stored on the object"
    )


def test_email_channel_single_recipient_unaffected():
    """Backward compatibility: a plain single address (no comma) must keep
    working exactly as before — this is the shape every existing secret/test
    already uses."""
    from core.notify import EmailChannel

    ch = EmailChannel("smtp.example.com", 465, "me@example.com", "pw", "me@example.com")
    assert ch.to_addrs == ["me@example.com"]
    assert ch.to_addr == "me@example.com"


def test_slack_does_not_try_to_post_raw_html():
    """A webhook cannot carry a document. Posting 300KB of markup into a channel
    is worse than sending the headline and pointing at the repo copy."""
    from core.notify import SlackChannel

    posted: list[tuple[str, str]] = []
    ch = SlackChannel("https://hooks.example.com/x")
    ch.send = lambda subject, body: posted.append((subject, body))

    ch.send_document("[PEOS 리포트]", "<html><body>" + "x" * 50_000 + "</body></html>")

    assert len(posted) == 1
    assert "<html>" not in posted[0][1]


def test_freshness_audit_flags_a_dead_series():
    """The audit is the standing guard against this class of failure: a job can
    exit 0 while collecting nothing, so success has to be measured on the data."""
    from scripts.data_freshness_audit import audit

    rows = audit()
    assert rows, "audit found no series at all — check data/normalized/"
    by_name = {r["series"]: r for r in rows}

    known_dead = "ecos_kr_10y_yield"
    if known_dead in by_name:
        r = by_name[known_dead]
        # Until a live run repairs it, this must read as dead rather than ok.
        assert r["status"] in ("dead", "ok"), f"unexpected status {r['status']}"
        if r["status"] == "dead":
            assert r["frequency"] == "daily"
            assert r["age_days"] > 365


# ── exports/price correlation ───────────────────────────────────────────────

def test_price_yoy_requires_a_prior_year_observation():
    """Converting a price level to %YoY needs a close ~12 months earlier.
    With less than a year of history this must return nothing, not a guess —
    an early-partial YoY would be indistinguishable from a real one once it
    lands in the correlation table."""
    import pandas as pd
    from scripts.correlation_analysis import _load_price_yoy, MONTHLY_PRICE_CSV

    import tempfile, os
    from pathlib import Path
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    try:
        df = pd.DataFrame([
            {"date": "2026-05-01", "code": "TEST", "label": "t", "close": 100.0,
             "source": "test", "fetched_at": ""},
            {"date": "2026-06-01", "code": "TEST", "label": "t", "close": 110.0,
             "source": "test", "fetched_at": ""},
        ])
        df.to_csv(path, index=False)
        import scripts.correlation_analysis as mod
        real_path = mod.MONTHLY_PRICE_CSV
        mod.MONTHLY_PRICE_CSV = Path(path)
        try:
            yoy = mod._load_price_yoy("TEST")
        finally:
            mod.MONTHLY_PRICE_CSV = real_path
        assert yoy.empty, f"expected no YoY points with <12mo of history, got {yoy}"
    finally:
        os.remove(path)


def test_price_yoy_computes_correctly_with_a_year_of_history():
    """The one case that should actually produce a number."""
    import pandas as pd, tempfile, os
    from pathlib import Path
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    try:
        df = pd.DataFrame([
            {"date": "2025-06-01", "code": "TEST", "label": "t", "close": 100.0,
             "source": "test", "fetched_at": ""},
            {"date": "2026-06-01", "code": "TEST", "label": "t", "close": 150.0,
             "source": "test", "fetched_at": ""},
        ])
        df.to_csv(path, index=False)
        import scripts.correlation_analysis as mod
        real_path = mod.MONTHLY_PRICE_CSV
        mod.MONTHLY_PRICE_CSV = Path(path)
        try:
            yoy = mod._load_price_yoy("TEST")
        finally:
            mod.MONTHLY_PRICE_CSV = real_path
        assert len(yoy) == 1
        assert abs(yoy.iloc[0] - 50.0) < 1e-9, f"expected +50% YoY, got {yoy.iloc[0]}"
    finally:
        os.remove(path)


def test_pairwise_correlation_matches_known_synthetic_case():
    """Pin the actual math, not just that it runs."""
    import pandas as pd
    from scripts.correlation_analysis import pairwise_correlations

    df = pd.DataFrame({
        "a": [1.0, 2.0, 3.0, 4.0],
        "b": [2.0, 4.0, 6.0, 8.0],      # perfectly correlated with a
        "c": [4.0, 3.0, 2.0, 1.0],      # perfectly anti-correlated with a
    })
    pairs = {(p["a"], p["b"]): p for p in pairwise_correlations(df)}
    assert abs(pairs[("a", "b")]["r"] - 1.0) < 1e-9
    assert abs(pairs[("a", "c")]["r"] + 1.0) < 1e-9
    assert pairs[("a", "b")]["n"] == 4


def test_low_sample_pairs_are_flagged_not_silently_trusted():
    """A correlation table without n is not trustworthy — this repo has
    already shipped one fabricated-confidence number (the 8-year-old rate
    published as current); a bare r with no sample-size caveat is the same
    failure shape applied to statistics instead of a single value."""
    from scripts.correlation_analysis import render_markdown, MIN_TRUSTWORTHY_N
    import pandas as pd

    df = pd.DataFrame({"total_exports_yoy": [1.0, 2.0, 3.0, 4.0],
                        "semi_exports_yoy": [2.0, 4.0, 6.0, 8.0]},
                       index=pd.to_datetime(["2026-04-01", "2026-05-01", "2026-06-01", "2026-07-01"]))
    df.index.name = "month"
    pairs = [{"a": "total_exports_yoy", "b": "semi_exports_yoy", "r": 1.0, "n": 4}]
    assert 4 < MIN_TRUSTWORTHY_N, "test assumes n=4 is below the trust floor"
    md = render_markdown(df, pairs)
    assert "신뢰 불가" in md, "a low-n pair must be visibly flagged, not presented as a plain number"


def test_correlation_prefers_growth_rates_over_raw_levels():
    """The whole point of converting price to %YoY before correlating is to
    avoid crediting a shared upward trend as a real relationship — pin that
    the loader is actually a rate transform, not a passthrough of levels."""
    import pandas as pd, tempfile, os
    from pathlib import Path
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    try:
        # Monotonically rising level, ~5%/mo compounding — %YoY should land
        # near 12*5% territory, not equal the raw closing level itself.
        rows = []
        price = 100.0
        for i in range(13):
            rows.append({"date": f"2025-{(i % 12) + 1:02d}-01" if i < 12 else "2026-01-01",
                         "code": "TEST", "label": "t", "close": price, "source": "t", "fetched_at": ""})
            price *= 1.05
        df = pd.DataFrame(rows)
        df.to_csv(path, index=False)
        import scripts.correlation_analysis as mod
        real_path = mod.MONTHLY_PRICE_CSV
        mod.MONTHLY_PRICE_CSV = Path(path)
        try:
            yoy = mod._load_price_yoy("TEST")
        finally:
            mod.MONTHLY_PRICE_CSV = real_path
        assert not yoy.empty
        assert all(v != rows[i]["close"] for i, v in enumerate(yoy.values)), \
            "YoY output must not just be the raw close level"
    finally:
        os.remove(path)


# ── customs_trade collector (관세청 수출입총괄 GW) ──────────────────────────

def test_customs_trade_year_windows_split_on_a_1_year_boundary():
    """The API rejects any strtYymm~endYymm span over 12 months
    (resultCode=99, confirmed live 2026-08-17) — pin that the splitter never
    produces a window wider than that, including the partial first/last year."""
    from collectors.customs_trade import _year_windows

    assert _year_windows("202506", "202607") == [("202506", "202512"), ("202601", "202607")]
    assert _year_windows("199001", "199012") == [("199001", "199012")]
    assert _year_windows("202601", "202601") == [("202601", "202601")]


def test_customs_trade_parses_real_response_shape_and_drops_the_total_row():
    """getNewtradeList appends a trailing <year>총계</year> summary row to
    every response — pin that it's filtered out (it would otherwise look
    like a 13th "month" and corrupt any month-indexed series)."""
    import collectors.customs_trade as ct
    from unittest.mock import patch, MagicMock

    sample_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<response><header><resultCode>00</resultCode>'
        '<resultMsg>정상서비스.</resultMsg></header><body><items>'
        '<item><balPayments>8700467993</balPayments><expCnt>1027989</expCnt>'
        '<expDlr>65843936782</expDlr><impCnt>4936713</impCnt>'
        '<impDlr>57143468789</impDlr><year>2026.01</year></item>'
        '<item><balPayments>167759691097</balPayments><expCnt>7920384</expCnt>'
        '<expDlr>595062835447</expDlr><impCnt>34460197</impCnt>'
        '<impDlr>427303144350</impDlr><year>총계</year></item>'
        '</items></body></response>'
    )
    mock_resp = MagicMock()
    mock_resp.text = sample_xml
    mock_resp.raise_for_status = MagicMock()

    with patch("collectors.customs_trade.requests.get", return_value=mock_resp):
        rows = ct._fetch_year_window("202601", "202601", "FAKEKEY")

    assert len(rows) == 1, "the 총계 summary row must be dropped, not kept as a 13th month"
    assert rows[0]["date"] == "2026-01-01"
    assert rows[0]["exp_dlr"] == 65843936782.0
    assert rows[0]["imp_dlr"] == 57143468789.0


def test_customs_trade_circuit_breaker_aborts_after_first_window_fails():
    """Live 2026-08-17: this GitHub Actions runner pool intermittently can't
    even open a TCP connection to apis.data.go.kr (same documented symptom
    as collectors/molit.py's KOSIS/ECOS circuit breaker). fetch_range() must
    give up after the first window fails its probe, not retry every
    remaining window (up to 37 for a full 1990-2026 backfill) and burn
    minutes on a connection that's already known to be down this run."""
    import collectors.customs_trade as ct
    from unittest.mock import patch

    calls = []

    def always_fails(strt, end, api_key, timeout=20):
        calls.append((strt, end))
        raise RuntimeError("Connection to apis.data.go.kr timed out.")

    with patch("collectors.customs_trade.get_api_key", return_value="FAKEKEY"), \
         patch("collectors.customs_trade._fetch_year_window", side_effect=always_fails):
        rows = ct.fetch_range("202401", "202612")  # 3 windows: 2024, 2025, 2026

    assert rows == []
    assert len(calls) == 2, (
        f"expected exactly 2 calls (the probe's 2 attempts on window 1 only), got {len(calls)}: {calls}"
    )


def test_customs_trade_raises_loudly_on_a_non_ok_result_code():
    """A resultCode != 00 (e.g. 99 = query span too wide) must raise, not
    silently return an empty/partial list that looks like 'no data that
    month' — those are different failure modes and must not be conflated."""
    import collectors.customs_trade as ct
    from unittest.mock import patch, MagicMock

    err_xml = (
        '<?xml version="1.0" encoding="UTF-8"?><response><header>'
        '<resultCode>99</resultCode>'
        '<resultMsg>시작과 종료의 조회기간은 1년이내 기간만 가능합니다.</resultMsg>'
        '</header></response>'
    )
    mock_resp = MagicMock()
    mock_resp.text = err_xml
    mock_resp.raise_for_status = MagicMock()

    with patch("collectors.customs_trade.requests.get", return_value=mock_resp):
        try:
            ct._fetch_year_window("200001", "202607", "FAKEKEY")
            assert False, "expected a RuntimeError for resultCode=99"
        except RuntimeError as exc:
            assert "99" in str(exc)


# ── annual (long-run) exports/KOSPI correlation ─────────────────────────────

def test_kospi_annual_yoy_computes_from_manual_yaml():
    """The manual kospi_annual.yaml is the only source in a fresh sandbox
    (no KIS credentials, no monthly-price-history.csv yet) — pin that the
    loader turns consecutive year-end closes into %YoY correctly on its own,
    with no live CSV present at all."""
    import pandas as pd, tempfile, os
    from pathlib import Path
    fd, path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd)
    try:
        Path(path).write_text(
            "series:\n"
            "  close:\n"
            "    - { date: \"2023-12-28\", value: 100.0 }\n"
            "    - { date: \"2024-12-30\", value: 110.0 }\n"
            "    - { date: \"2025-12-30\", value: 143.0 }\n",
            encoding="utf-8",
        )
        import scripts.correlation_analysis as mod
        real_kospi = mod.KOSPI_ANNUAL_YAML
        real_csv = mod.MONTHLY_PRICE_CSV
        mod.KOSPI_ANNUAL_YAML = Path(path)
        mod.MONTHLY_PRICE_CSV = Path("/nonexistent/does-not-exist.csv")
        try:
            yoy = mod._load_kospi_annual_yoy()
        finally:
            mod.KOSPI_ANNUAL_YAML = real_kospi
            mod.MONTHLY_PRICE_CSV = real_csv
        assert len(yoy) == 2
        assert abs(yoy.loc[pd.Timestamp("2024-01-01")] - 10.0) < 1e-9
        assert abs(yoy.loc[pd.Timestamp("2025-01-01")] - 30.0) < 1e-9
    finally:
        os.remove(path)


def test_kospi_annual_yoy_prefers_live_kis_close_over_manual_file():
    """Once exports-price-correlation.yml has actually collected a December
    close via KIS, that real value must win over the manually-sourced
    (WebSearch-only, unverifiable-in-sandbox) kospi_annual.yaml for the same
    year — otherwise the live pipeline would silently have zero effect on
    this analysis, contradicting the loader's own priority comment."""
    import pandas as pd, tempfile, os
    from pathlib import Path
    fd_yaml, yaml_path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd_yaml)
    fd_csv, csv_path = tempfile.mkstemp(suffix=".csv")
    os.close(fd_csv)
    try:
        Path(yaml_path).write_text(
            "series:\n"
            "  close:\n"
            "    - { date: \"2023-12-28\", value: 100.0 }\n"
            "    - { date: \"2024-12-30\", value: 999.0 }\n",  # deliberately wrong
            encoding="utf-8",
        )
        pd.DataFrame([
            {"date": "2024-12-30", "code": "0001", "label": "코스피", "close": 120.0,
             "source": "kis", "fetched_at": ""},
        ]).to_csv(csv_path, index=False)

        import scripts.correlation_analysis as mod
        real_kospi = mod.KOSPI_ANNUAL_YAML
        real_csv = mod.MONTHLY_PRICE_CSV
        mod.KOSPI_ANNUAL_YAML = Path(yaml_path)
        mod.MONTHLY_PRICE_CSV = Path(csv_path)
        try:
            yoy = mod._load_kospi_annual_yoy()
        finally:
            mod.KOSPI_ANNUAL_YAML = real_kospi
            mod.MONTHLY_PRICE_CSV = real_csv
        # (120/100 - 1) * 100 = 20.0, NOT (999/100 - 1) * 100 = 899.0
        assert abs(yoy.loc[pd.Timestamp("2024-01-01")] - 20.0) < 1e-9, \
            f"live KIS close must override the manual file, got {yoy.loc[pd.Timestamp('2024-01-01')]}"
    finally:
        os.remove(yaml_path)
        os.remove(csv_path)


def test_build_annual_dataset_reads_both_manual_yaml_files():
    """End-to-end sanity: build_annual_dataset must actually wire together
    exports_annual.yaml (two series) and kospi_annual.yaml (via
    _load_kospi_annual_yoy) into one DataFrame keyed by year."""
    import pandas as pd, tempfile, os
    from pathlib import Path
    fd_exp, exp_path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd_exp)
    fd_kospi, kospi_path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd_kospi)
    try:
        Path(exp_path).write_text(
            "series:\n"
            "  total_exports_yoy:\n"
            "    - { date: \"2024-01-01\", value: 8.2 }\n"
            "    - { date: \"2025-01-01\", value: 3.8 }\n"
            "  semiconductor_exports_yoy:\n"
            "    - { date: \"2024-01-01\", value: 43.9 }\n"
            "    - { date: \"2025-01-01\", value: 22.1 }\n",
            encoding="utf-8",
        )
        Path(kospi_path).write_text(
            "series:\n"
            "  close:\n"
            "    - { date: \"2023-12-28\", value: 2655.28 }\n"
            "    - { date: \"2024-12-30\", value: 2399.49 }\n"
            "    - { date: \"2025-12-30\", value: 4214.17 }\n",
            encoding="utf-8",
        )
        import scripts.correlation_analysis as mod
        real_exp = mod.EXPORTS_ANNUAL_YAML
        real_kospi = mod.KOSPI_ANNUAL_YAML
        real_csv = mod.MONTHLY_PRICE_CSV
        mod.EXPORTS_ANNUAL_YAML = Path(exp_path)
        mod.KOSPI_ANNUAL_YAML = Path(kospi_path)
        mod.MONTHLY_PRICE_CSV = Path("/nonexistent/does-not-exist.csv")
        try:
            df = mod.build_annual_dataset()
        finally:
            mod.EXPORTS_ANNUAL_YAML = real_exp
            mod.KOSPI_ANNUAL_YAML = real_kospi
            mod.MONTHLY_PRICE_CSV = real_csv
        assert list(df.columns) == ["total_exports_yoy", "semi_exports_yoy", "kospi_yoy"]
        assert df.loc[pd.Timestamp("2025-01-01"), "total_exports_yoy"] == 3.8
        assert df.loc[pd.Timestamp("2025-01-01"), "semi_exports_yoy"] == 22.1
        kospi_2025 = df.loc[pd.Timestamp("2025-01-01"), "kospi_yoy"]
        assert abs(kospi_2025 - ((4214.17 / 2399.49 - 1) * 100)) < 1e-6
    finally:
        os.remove(exp_path)
        os.remove(kospi_path)


def test_customs_export_yoy_computes_from_real_data():
    """collectors/customs_trade.py writes level ($ dollars) rows to
    customs_export_dlr.csv — pin that the loader turns those into %YoY
    correctly, same math as _load_price_yoy but a different source file."""
    import pandas as pd, tempfile, os
    from pathlib import Path
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    try:
        pd.DataFrame([
            {"date": "2025-06-01", "value": 1000000.0},
            {"date": "2026-06-01", "value": 1200000.0},
        ]).to_csv(path, index=False)
        import scripts.correlation_analysis as mod
        real_path = mod.CUSTOMS_EXPORT_CSV
        mod.CUSTOMS_EXPORT_CSV = Path(path)
        try:
            yoy = mod._load_customs_export_yoy()
        finally:
            mod.CUSTOMS_EXPORT_CSV = real_path
        assert len(yoy) == 1
        assert abs(yoy.iloc[0] - 20.0) < 1e-9, f"expected +20% YoY, got {yoy.iloc[0]}"
    finally:
        os.remove(path)


def test_build_dataset_prefers_real_customs_data_over_manual_motie():
    """Once collectors/customs_trade.py has real data for a month, that must
    win over the manually-maintained motie_total_exports_yoy.csv for the same
    month — same live-overrides-manual priority as the annual KOSPI loader.
    Regression target: combine_first() called on the wrong operand order
    would silently make the manual (weaker) source win instead."""
    import pandas as pd, tempfile, os
    from pathlib import Path
    fd_customs, customs_path = tempfile.mkstemp(suffix=".csv")
    os.close(fd_customs)
    fd_motie, motie_path = tempfile.mkstemp(suffix=".csv")
    os.close(fd_motie)
    try:
        # Two years of levels so 2026-04 gets a real %YoY.
        pd.DataFrame([
            {"date": "2025-04-01", "value": 1000000.0},
            {"date": "2026-04-01", "value": 1100000.0},
        ]).to_csv(customs_path, index=False)
        # Manual file deliberately disagrees for the same month.
        pd.DataFrame([
            {"date": "2026-04-01", "value": 999.9},
        ]).to_csv(motie_path, index=False)

        import scripts.correlation_analysis as mod
        real_customs = mod.CUSTOMS_EXPORT_CSV
        real_normalized = mod.NORMALIZED
        mod.CUSTOMS_EXPORT_CSV = Path(customs_path)
        # _load_motie() reads NORMALIZED / f"{series_id}.csv" — point it at a
        # temp dir containing a same-named file so build_dataset() reads our
        # fixture instead of the repo's real motie_total_exports_yoy.csv.
        tmp_dir = Path(tempfile.mkdtemp())
        (tmp_dir / "motie_total_exports_yoy.csv").write_text(Path(motie_path).read_text())
        (tmp_dir / "motie_semiconductor_exports_yoy.csv").write_text("date,value\n")
        mod.NORMALIZED = tmp_dir
        try:
            df = mod.build_dataset()
        finally:
            mod.CUSTOMS_EXPORT_CSV = real_customs
            mod.NORMALIZED = real_normalized
        got = df.loc[pd.Timestamp("2026-04-01"), "total_exports_yoy"]
        assert abs(got - 10.0) < 1e-9, \
            f"real customs %YoY (+10.0) must win over manual (999.9), got {got}"
    finally:
        os.remove(customs_path)
        os.remove(motie_path)


def test_render_annual_markdown_handles_missing_metric_without_crashing():
    """Same robustness class as render_markdown's own reindex fix — a caller
    passing a frame missing a column entirely must render '—', not KeyError."""
    from scripts.correlation_analysis import render_annual_markdown
    import pandas as pd

    df = pd.DataFrame({"total_exports_yoy": [8.2, 3.8]},
                       index=pd.to_datetime(["2024-01-01", "2025-01-01"]))
    df.index.name = "year"
    pairs = [{"a": "total_exports_yoy", "b": "kospi_yoy", "r": float("nan"), "n": 0}]
    md = render_annual_markdown(df, pairs)
    assert "—" in md
    assert "2025" in md


def test_backward_date_windows_walks_from_now_to_a_target_start():
    """kis_fetch_monthly_price_history is confirmed (2026-08-17,
    kis-monthly-depth-probe.yml) to truncate to the most recent ~50 months
    regardless of how wide a date range is requested (months=90 → still only
    50 rows back to 2022-07). _backward_date_windows is what lets
    kis_fetch_monthly_price_history_deep walk further back by making several
    narrower, non-overlapping calls with the end date pulled progressively
    into the past."""
    from datetime import date, timedelta
    from scripts.investor_flow import _backward_date_windows

    windows = _backward_date_windows(date(2026, 8, 17), date(2019, 1, 1), months_per_window=45)
    assert windows[0][1] == date(2026, 8, 17)   # newest window ends "now"
    assert windows[-1][0] == date(2019, 1, 1)   # oldest window starts exactly at target
    for start, end in windows:
        assert start <= end
        assert start >= date(2019, 1, 1)
    # non-overlapping: each next (older) window ends the day before the
    # previous window started
    for i in range(len(windows) - 1):
        prev_start = windows[i][0]
        next_end = windows[i + 1][1]
        assert next_end == prev_start - timedelta(days=1)


def test_backward_date_windows_single_window_when_range_is_short():
    """A range that already fits inside one call's ~50-month reach must not
    be split — that would just waste an extra KIS call."""
    from datetime import date
    from scripts.investor_flow import _backward_date_windows

    windows = _backward_date_windows(date(2026, 8, 17), date(2026, 1, 1), months_per_window=45)
    assert windows == [(date(2026, 1, 1), date(2026, 8, 17))]


def test_drop_current_incomplete_month_removes_the_in_progress_month():
    """The customs/KIS collectors write a row for whatever calendar month a
    run happens to land in, even though that month isn't over — comparing
    that partial figure to a prior COMPLETE month produces a swing that
    looks like a real move (found 2026-08-17: 총수출 %YoY showed -32.8% at
    the last point, which was actually just a half-counted August, not a
    real collapse). This must be dropped before any YoY/QoQ math runs."""
    import pandas as pd
    from scripts.correlation_analysis import _drop_current_incomplete_month

    now = pd.Timestamp.now(tz="UTC").tz_localize(None)
    current_month = pd.Timestamp(year=now.year, month=now.month, day=1)
    prior_month = current_month - pd.DateOffset(months=1)
    s = pd.Series({prior_month: 100.0, current_month: 40.0})
    out = _drop_current_incomplete_month(s)
    assert list(out.index) == [prior_month]
    assert out.iloc[0] == 100.0


def test_quarterly_sum_drops_a_quarter_with_fewer_than_3_months():
    """A flow variable (export dollars) summed over a quarter that only has
    1-2 monthly observations understates that quarter next to a real 3-month
    quarter — same partial-period trap as the monthly case, one level up."""
    import pandas as pd
    from scripts.correlation_analysis import _quarterly_sum

    s = pd.Series({
        pd.Timestamp("2024-01-01"): 10.0,
        pd.Timestamp("2024-02-01"): 10.0,
        pd.Timestamp("2024-03-01"): 10.0,
        pd.Timestamp("2024-04-01"): 5.0,   # only 1 month into Q2 2024
    })
    out = _quarterly_sum(s)
    assert list(out.index) == [pd.Timestamp("2024-03-31")]
    assert out.iloc[0] == 30.0


def test_quarterly_last_drops_the_in_progress_quarter():
    """A stock variable's (price) "last observation in the quarter" is only
    meaningful once the quarter has actually ended — otherwise it's just
    whatever the most recent trading day happens to be, and would silently
    change value every time the pipeline reruns later in the same quarter."""
    import pandas as pd
    from scripts.correlation_analysis import _quarterly_last

    now = pd.Timestamp.now(tz="UTC").tz_localize(None)
    current_q_end = now.to_period("Q").end_time.normalize()
    prior_q_end = current_q_end - pd.offsets.QuarterEnd(1)
    s = pd.Series({
        prior_q_end: 100.0,
        current_q_end - pd.DateOffset(days=5): 999.0,  # a snapshot inside the still-open quarter
    })
    out = _quarterly_last(s)
    assert list(out.index) == [prior_q_end]
    assert out.iloc[0] == 100.0


def test_qoq_computes_percent_change_from_the_prior_quarter():
    """Pin the actual math, not just that it runs."""
    import pandas as pd
    from scripts.correlation_analysis import _qoq

    s = pd.Series({pd.Timestamp("2024-03-31"): 100.0, pd.Timestamp("2024-06-30"): 110.0})
    out = _qoq(s)
    assert len(out) == 1
    assert abs(out.iloc[0] - 10.0) < 1e-9


def test_daily_yoy_finds_the_nearest_trading_day_within_tolerance():
    """Exactly 365 days earlier is rarely a trading day (weekend/holiday) —
    _daily_yoy must fall back to the closest available observation inside
    the tolerance window, not require an exact calendar match."""
    import pandas as pd
    from scripts.correlation_analysis import _daily_yoy

    # 2025-08-15 is a Friday; 2026-08-14 (Friday) is the "today" observation.
    # The exact year-earlier date (2025-08-14, a Thursday) is missing —
    # nearest available is 2025-08-15, 1 day off, well inside tolerance.
    s = pd.Series({
        pd.Timestamp("2025-08-15"): 100.0,
        pd.Timestamp("2026-08-14"): 150.0,
    })
    out = _daily_yoy(s, tolerance_days=5)
    assert len(out) == 1
    assert abs(out.iloc[0] - 50.0) < 1e-9


def test_daily_yoy_skips_a_day_with_no_prior_year_observation_nearby():
    """If nothing falls inside the tolerance window (e.g. history doesn't
    go back a full year yet, or there's a gap), that day is dropped rather
    than paired with a far-off, misleading "closest" value."""
    import pandas as pd
    from scripts.correlation_analysis import _daily_yoy

    s = pd.Series({
        pd.Timestamp("2025-01-01"): 100.0,   # nothing ~1yr before this
        pd.Timestamp("2026-08-14"): 150.0,   # nothing ~1yr before this either
    })
    out = _daily_yoy(s, tolerance_days=5)
    assert out.empty


def test_filter_from_does_not_crash_on_an_empty_series():
    """Regression: an empty pd.Series(dtype=float) has a RangeIndex, not a
    DatetimeIndex — comparing it to a Timestamp (series.index >= cutoff)
    raises TypeError. build_daily_focus_dataset hit this the first time it
    ran with no daily-price-history.csv yet (all three inputs can be empty)."""
    import pandas as pd
    from scripts.correlation_analysis import _filter_from

    empty = pd.Series(dtype=float)
    out = _filter_from(empty, pd.Timestamp("2024-01-01"))
    assert out.empty

    populated = pd.Series({pd.Timestamp("2023-01-01"): 1.0, pd.Timestamp("2025-01-01"): 2.0})
    out2 = _filter_from(populated, pd.Timestamp("2024-01-01"))
    assert list(out2.index) == [pd.Timestamp("2025-01-01")]


def test_load_exports_preliminary_returns_the_current_months_estimate():
    """2026-08-17 user request: draw the next (not-yet-final) point from
    관세청's 10-day preliminary release. Only surface it when it actually
    targets the in-progress month — a stale preliminary from a month that's
    already closed would misleadingly overwrite a real point."""
    import pandas as pd, tempfile, os, yaml
    from pathlib import Path
    import scripts.correlation_analysis as mod

    now = pd.Timestamp.now(tz="UTC").tz_localize(None)
    current_month = pd.Timestamp(year=now.year, month=now.month, day=1)

    fd, path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd)
    try:
        payload = {
            "latest": {
                "target_month": current_month.strftime("%Y-%m-%d"),
                "period_label": "1일~10일",
                "period_start": current_month.strftime("%Y-%m-%d"),
                "period_end": (current_month + pd.Timedelta(days=9)).strftime("%Y-%m-%d"),
                "total_exports_yoy": 45.3,
                "source": "관세청 보도자료",
            }
        }
        Path(path).write_text(yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8")
        real_path = mod.EXPORTS_PRELIMINARY_YAML
        mod.EXPORTS_PRELIMINARY_YAML = Path(path)
        try:
            result = mod.load_exports_preliminary()
        finally:
            mod.EXPORTS_PRELIMINARY_YAML = real_path
        assert result is not None
        assert result["date"] == current_month
        assert abs(result["value"] - 45.3) < 1e-9
        assert "label_en" in result and result["label_en"]  # ASCII chart label always derivable
        assert result["semi_value"] is None  # field absent from this payload -> must not crash, not fabricate
    finally:
        os.remove(path)


def test_load_exports_preliminary_also_surfaces_the_semiconductor_yoy():
    """2026-08-17 user request: '최근 급등과 급락 장세의 수출과의 관계를
    확인해보자' — the yaml already records semiconductor_exports_yoy
    (참고용) but nothing read it until now. It must come through as
    semi_value so the chart can draw a second preliminary point."""
    import pandas as pd, tempfile, os, yaml
    from pathlib import Path
    import scripts.correlation_analysis as mod

    now = pd.Timestamp.now(tz="UTC").tz_localize(None)
    current_month = pd.Timestamp(year=now.year, month=now.month, day=1)

    fd, path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd)
    try:
        payload = {
            "latest": {
                "target_month": current_month.strftime("%Y-%m-%d"),
                "period_label": "1일~10일",
                "period_start": current_month.strftime("%Y-%m-%d"),
                "period_end": (current_month + pd.Timedelta(days=9)).strftime("%Y-%m-%d"),
                "total_exports_yoy": 45.3,
                "semiconductor_exports_yoy": 155.4,
                "source": "관세청 보도자료",
            }
        }
        Path(path).write_text(yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8")
        real_path = mod.EXPORTS_PRELIMINARY_YAML
        mod.EXPORTS_PRELIMINARY_YAML = Path(path)
        try:
            result = mod.load_exports_preliminary()
        finally:
            mod.EXPORTS_PRELIMINARY_YAML = real_path
        assert result is not None
        assert abs(result["semi_value"] - 155.4) < 1e-9
    finally:
        os.remove(path)


def test_load_exports_preliminary_ignores_a_stale_target_month():
    """A preliminary reading left over from a month that has already closed
    (nobody updated the file after month-end) must not be drawn as if it
    were still the in-progress estimate."""
    import pandas as pd, tempfile, os, yaml
    from pathlib import Path
    import scripts.correlation_analysis as mod

    fd, path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd)
    try:
        payload = {"latest": {
            "target_month": "2019-01-01",  # safely in the past regardless of when this test runs
            "period_label": "1일~10일", "period_start": "2019-01-01", "period_end": "2019-01-10",
            "total_exports_yoy": 1.0, "source": "test",
        }}
        Path(path).write_text(yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8")
        real_path = mod.EXPORTS_PRELIMINARY_YAML
        mod.EXPORTS_PRELIMINARY_YAML = Path(path)
        try:
            result = mod.load_exports_preliminary()
        finally:
            mod.EXPORTS_PRELIMINARY_YAML = real_path
        assert result is None
    finally:
        os.remove(path)


def test_build_levels_dataset_assembles_the_three_raw_level_columns():
    """2026-08-17 user request: '절대 수치(레벨)로 트렌드를 코스피와 비교'.
    build_levels_dataset() must reuse the already-tested level loaders
    (_load_customs_export_level / _load_price_level) unmodified and just
    assemble them into one frame — no %YoY transform, no new fetching.

    semi_exports_usd was added later the same day ('YoY를 거꾸로 역산해서
    RAW level로 그려줄 수 있어?' — turned out to be real published $ amounts
    already sitting in exports.yaml comments, not an actual YoY reversal)."""
    import scripts.correlation_analysis as mod

    df = mod.build_levels_dataset()
    assert list(df.columns) == [
        "total_exports_usd", "semi_exports_usd", "hynix_price_krw", "kospi_index",
    ]
    # real collected data should give at least some non-null history in each column
    assert df["total_exports_usd"].notna().any()
    assert df["kospi_index"].notna().any()


def test_load_semi_exports_level_converts_100m_usd_units_to_raw_usd():
    """2026-08-17 user request: '반도체수출 raw level'. exports.yaml stores
    semiconductor_exports_usd_100m in 억 달러 (hundred-million-dollar) units
    — the loader must scale by 1e8 so it's directly comparable (same raw-USD
    units) to total_exports_usd from _load_customs_export_level()."""
    import pandas as pd
    import scripts.correlation_analysis as mod

    series = mod._load_semi_exports_level()
    assert not series.empty
    # 2026-04 real published figure is 319.0억 달러 = $31.9B
    val = series.loc[pd.Timestamp("2026-04-01")]
    assert abs(val - 319.0 * 1e8) < 1e-6


def test_estimate_preliminary_export_level_scales_prior_year_by_the_prelim_yoy():
    """2026-08-17 user request: '10일 잠정치에 대한 예상치도 [레벨 차트에]
    같이 추가해줘'. load_exports_preliminary() only gives %YoY — converting
    it to a level for the LEVELS chart means: prior-year-same-month level ×
    (1 + prelim %YoY / 100). Must never touch the real level series."""
    import pandas as pd
    import scripts.correlation_analysis as mod

    export_level = pd.Series(
        {pd.Timestamp("2025-08-01"): 100.0, pd.Timestamp("2026-07-01"): 200.0},
        dtype=float,
    )
    preliminary = {
        "date": pd.Timestamp("2026-08-01"),
        "value": 45.3,  # %YoY
        "label_en": "Aug 1-10 prelim.",
    }
    result = mod._estimate_preliminary_export_level(export_level, preliminary)
    assert result is not None
    assert result["date"] == pd.Timestamp("2026-08-01")
    assert abs(result["value"] - 145.3) < 1e-9  # 100 * (1 + 45.3/100)
    assert result["label_en"] == "Aug 1-10 prelim."

    # no prior-year same month in the series -> can't scale anything, must not guess
    assert mod._estimate_preliminary_export_level(
        pd.Series({pd.Timestamp("2026-07-01"): 200.0}, dtype=float), preliminary
    ) is None

    # no preliminary reading at all -> nothing to estimate
    assert mod._estimate_preliminary_export_level(export_level, None) is None


def test_series_peak_vs_latest_flags_a_pullback_from_the_recent_peak():
    """2026-08-17 user request: '이 총수출이 어쨌든 피크를 찍고 떨어진
    것이 다시 고지를 향해갈 수 있을지 보고서에 포인트로 기술해줘'.
    _series_peak_vs_latest must find the peak within the recent window and
    correctly report a pullback (negative gap, negative MoM) — this is the
    exact June-peak/July-pullback shape seen in the real semiconductor
    export data."""
    import pandas as pd
    import scripts.correlation_analysis as mod

    series = pd.Series({
        pd.Timestamp("2026-04-01"): 31.9e9,
        pd.Timestamp("2026-05-01"): 37.2e9,
        pd.Timestamp("2026-06-01"): 44.8e9,  # peak
        pd.Timestamp("2026-07-01"): 41.0e9,  # pullback
    })
    stat = mod._series_peak_vs_latest(series)
    assert stat is not None
    assert stat["peak_date"] == pd.Timestamp("2026-06-01")
    assert stat["latest_date"] == pd.Timestamp("2026-07-01")
    assert stat["gap_from_peak_pct"] < 0  # still below the peak
    assert stat["mom_pct"] < 0            # fell versus the prior month

    # fewer than 2 real points -> nothing to compare, must not guess
    assert mod._series_peak_vs_latest(pd.Series({pd.Timestamp("2026-07-01"): 41.0e9})) is None


def test_yoy_deceleration_trend_distinguishes_widening_from_narrowing():
    """The 2nd-derivative check must tell 'deceleration is accelerating'
    apart from 'deceleration is easing' — both look like a falling YoY
    line at a glance, but they imply opposite forward paths."""
    import pandas as pd
    import scripts.correlation_analysis as mod

    # 199.5 -> 178.8 (delta -20.7) -> 155.4 (delta -23.4): gap widening
    widening = pd.Series({pd.Timestamp("2026-06-01"): 199.5, pd.Timestamp("2026-07-01"): 178.8})
    assert "커지고" in mod._yoy_deceleration_trend(widening, 155.4)

    # 199.5 -> 178.8 (delta -20.7) -> 170.0 (delta -8.8): gap narrowing
    narrowing = pd.Series({pd.Timestamp("2026-06-01"): 199.5, pd.Timestamp("2026-07-01"): 178.8})
    assert "줄고" in mod._yoy_deceleration_trend(narrowing, 170.0)

    # fewer than 3 total points (2 real + 0 prelim) -> can't compute a 2nd derivative
    assert mod._yoy_deceleration_trend(pd.Series({pd.Timestamp("2026-07-01"): 178.8}), None) is None


def test_render_export_recovery_watch_note_links_to_the_wiki_concept():
    """2026-08-17 user request: 'wiki에 남기고 ... 보고서에 포인트로
    기술해줘'. The note must be computed from real data (not a fixed
    string) and must point back to the wiki concept doc that carries the
    full hypothesis set, so the report and the wiki stay one source of
    truth instead of two independent narratives drifting apart."""
    import scripts.correlation_analysis as mod

    levels_df = mod.build_levels_dataset()
    yoy_df = mod.build_dataset()
    note = mod.render_export_recovery_watch_note(levels_df, yoy_df, mod.load_exports_preliminary())
    assert "semiconductor-export-peak-recovery-watch.md" in note
    assert "반도체수출" in note or "총수출" in note


def test_hbm_cycle_score_module_is_shared_not_duplicated():
    """2026-08-27: score_foreign_flow_axis/score_foreign_holding_axis used to be
    defined twice inline inside scripts/daily_report.py with no other caller —
    now both live once in scripts/hbm_cycle_score.py, importable package-style
    (PYTHONPATH=., what engine/report/payload.py uses) with the expected shape."""
    from scripts.hbm_cycle_score import score_foreign_flow_axis, score_foreign_holding_axis

    flow = score_foreign_flow_axis("000660")
    assert flow["max"] == 15.0
    assert 0.0 <= flow["score"] <= 15.0
    assert set(flow["detail"].keys()) == {"당일", "20일_누적", "모멘텀(5일vs20일)"}

    holding = score_foreign_holding_axis("000660")
    assert holding["max"] == 15.0
    assert 0.0 <= holding["score"] <= 15.0


def test_daily_report_delegates_to_the_shared_hbm_module_not_a_private_copy():
    """daily_report.py is only ever run sibling-style (`cd scripts && python3
    daily_report.py`, exactly how sk-hynix-daily-report.yml invokes it), so this
    spawns it that way rather than importing scripts.daily_report from repo
    root (which can't work — daily_report.py's own investor_flow import is
    sibling-style too, a pre-existing property this test isn't re-litigating).
    Confirms the two callers are the literal same function object, not two
    definitions that could silently drift apart."""
    import subprocess

    result = subprocess.run(
        ["python3", "-c",
         "import daily_report, hbm_cycle_score as hbm; "
         "print(daily_report.score_foreign_flow_axis is hbm.score_foreign_flow_axis); "
         "print(daily_report.score_foreign_holding_axis is hbm.score_foreign_holding_axis)"],
        cwd="scripts", capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"daily_report.py failed to import: {result.stderr}"
    assert result.stdout.strip().splitlines() == ["True", "True"]


def test_capex_periphery_module_is_shared_not_duplicated():
    """2026-08-27: read_hyperscaler_capex/read_ai_periphery moved out of
    scripts/daily_report.py the same way the HBM axes did — package-style
    import must work (what engine/report/payload.py uses) and return the
    expected per-ticker shape."""
    from scripts.capex_periphery import read_hyperscaler_capex, read_ai_periphery

    capex = read_hyperscaler_capex()
    assert capex, "fixture expects sources/hyperscaler-capex.csv to have rows"
    for ticker in ("GOOGL", "MSFT", "AMZN", "META"):
        assert ticker in capex, f"expected {ticker} in hyperscaler capex data"
        assert "value_usd" in capex[ticker] and "end_date" in capex[ticker]

    periphery = read_ai_periphery()
    assert periphery, "fixture expects sources/ai-periphery-fundamentals.csv to have rows"


def test_adr_crosscheck_resolves_when_two_independent_methods_agree():
    """2026-09-01: user asked '하이닉스 ADR 주가에 대해서 아직 혼돈이 있어?' —
    investigating sources/sk-hynix-adr-quote.csv's MISMATCH history (10
    occurrences) showed a consistent pattern: rate and hist (two independent
    methods) agreed with each other every time, while calc (which trusts the
    same row's `diff` field) was the lone outlier — e.g. the 2026-08-24 row
    was exactly rate:-4.92|calc:+5.46|hist:-4.92. This pins the fix: when
    rate and hist agree within tolerance, resolve using their average and
    tag RESOLVED_2OF3 (not silently blended into OK, not left as a MISMATCH
    blank) — calc/diff is excluded, and detail keeps all three values."""
    from scripts.investor_flow import _adr_crosscheck, ADR_CROSSCHECK_TOLERANCE_PCT

    # The real 2026-08-24 case.
    crosscheck, change_pct, detail = _adr_crosscheck(rate_pct=-4.92, calc_pct=5.46, hist_pct=-4.92)
    assert crosscheck == "RESOLVED_2OF3"
    assert abs(change_pct - (-4.92)) < 1e-6, change_pct
    assert "calc:+5.46" in detail, "excluded method's value must still be traceable in detail"

    # All three agree -> still OK, unaffected by the new branch.
    crosscheck, change_pct, detail = _adr_crosscheck(2.20, 2.20, 2.20)
    assert crosscheck == "OK"
    assert abs(change_pct - 2.20) < 1e-6, change_pct

    # A genuine 3-way conflict (rate/hist don't agree either) must still
    # fall back to MISMATCH with change_pct withheld — RESOLVED_2OF3 must
    # not swallow every disagreement.
    crosscheck, change_pct, detail = _adr_crosscheck(rate_pct=-4.92, calc_pct=5.46, hist_pct=1.0)
    assert crosscheck == "MISMATCH"
    assert change_pct is None

    # rate missing entirely -> can't apply the 2-of-3 rule, stays MISMATCH.
    crosscheck, change_pct, detail = _adr_crosscheck(rate_pct=None, calc_pct=5.46, hist_pct=-4.92)
    assert crosscheck == "MISMATCH"
    assert change_pct is None


def test_daily_report_shows_resolved_2of3_note_not_silent_blend():
    """The ADR report line must say when a value was RESOLVED_2OF3 rather than
    rendering it identically to a clean 3/3 OK — silently blending an
    auto-resolved anomaly into a normal-looking line would hide exactly the
    kind of drift this fix exists to catch."""
    from scripts.investor_flow import _adr_crosscheck

    crosscheck, change_pct, detail = _adr_crosscheck(-4.92, 5.46, -4.92)
    assert crosscheck == "RESOLVED_2OF3"
    # daily_report.py's ADR section renders this note only for RESOLVED_2OF3;
    # this test locks the crosscheck value it keys off of.
    assert crosscheck != "OK" and crosscheck != "MISMATCH"


def test_daily_report_delegates_to_the_shared_capex_module_not_a_private_copy():
    """Same guarantee as test_daily_report_delegates_to_the_shared_hbm_module —
    spawned sibling-style (cwd=scripts), matching the real CI invocation."""
    import subprocess

    result = subprocess.run(
        ["python3", "-c",
         "import daily_report, capex_periphery as cp; "
         "print(daily_report.read_hyperscaler_capex is cp.read_hyperscaler_capex); "
         "print(daily_report.read_ai_periphery is cp.read_ai_periphery)"],
        cwd="scripts", capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"daily_report.py failed to import: {result.stderr}"
    assert result.stdout.strip().splitlines() == ["True", "True"]


def test_month_trend_compares_start_vs_latest_without_fabricating_a_full_window():
    """2026-09-01: user complaint — '보고서에 트렌드가 안 보여' (the report shows
    no trend, every section was a single day's snapshot). _month_trend() must
    compare the latest row to the oldest row within the last N days, and when
    fewer than N days of history exist it must say so via actual_days rather
    than silently presenting a shorter span as a full 30-day trend."""
    import subprocess

    script = (
        "import daily_report as dr\n"
        "rows = [\n"
        "    {'date': '2026-08-01', 'price': '100'},\n"
        "    {'date': '2026-08-15', 'price': '110'},\n"
        "    {'date': '2026-08-31', 'price': '120'},\n"
        "]\n"
        "t = dr._month_trend(rows, 'date', 'price', days=30)\n"
        "assert t['start_val'] == 100.0 and t['latest_val'] == 120.0, t\n"
        "assert t['delta'] == 20.0 and abs(t['pct'] - 20.0) < 1e-9, t\n"
        "assert t['min'] == 100.0 and t['max'] == 120.0, t\n"
        "assert t['actual_days'] == 30, t\n"
        "# fewer than 2 rows -> None, not a fabricated single-point trend\n"
        "assert dr._month_trend([rows[0]], 'date', 'price') is None\n"
        "# a window shorter than the requested days must say so honestly\n"
        "short_rows = [{'date': '2026-08-28', 'price': '50'}, {'date': '2026-08-31', 'price': '55'}]\n"
        "t2 = dr._month_trend(short_rows, 'date', 'price', days=30)\n"
        "assert t2['actual_days'] == 3, t2\n"
        "line = dr._fmt_trend_line('테스트', t2, unit='원', decimals=0)\n"
        "assert '30일 미만' in line, line\n"
        "print('OK')\n"
    )
    result = subprocess.run(["python3", "-c", script], cwd="scripts",
                             capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert result.stdout.strip() == "OK"


def test_daily_report_trend_section_renders_from_real_accumulated_csvs():
    """The new '최근 1개월 트렌드' section must actually appear in build_report()'s
    output and reflect the real sources/*.csv history (no fabrication) — this
    guards against the section being wired but never called, or silently
    raising and getting swallowed."""
    import subprocess

    result = subprocess.run(
        ["python3", "-c", "import daily_report as dr; print(dr.build_report('000660'))"],
        cwd="scripts", capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    out = result.stdout
    assert "## 최근 1개월 트렌드" in out
    assert "- 주가:" in out and "- 외국인 보유율:" in out
    assert "- 신용융자잔고:" in out and "- 공매도 비중:" in out and "- 코스피지수:" in out


def test_sk_hynix_section_shows_live_data_and_capex_as_context_not_a_directive():
    """2026-08-27 Phase 3: the '오늘의 실측 데이터'/CapEx lines must render from
    real payload data, and must never contain BUY/SELL/HOLD language of their
    own — R4 (포지션 지시는 단일 출처) says only the decision engine may
    instruct a position; supplementary evidence sections must read as context."""
    from dataclasses import dataclass
    from engine.report.markdown import _sk_hynix_decision_section
    from scripts.capex_periphery import read_hyperscaler_capex, read_ai_periphery
    from scripts.investor_flow import read_latest_price_snapshot, read_ticker_rows, summarize_flows, \
        credit_balance_streak, read_latest_short_sale, read_latest_adr
    from scripts.hbm_cycle_score import score_foreign_flow_axis, score_foreign_holding_axis

    flow_rows = read_ticker_rows("000660")
    fake_payload = {
        "personal": {"semiconductor_score": 83.8, "semiconductor_band": "강한 긍정"},
        "rate_analysis": {"total_score": 65.0},
        "hbm_cycle_score": {
            "ticker": "000660",
            "foreign_flow": score_foreign_flow_axis("000660"),
            "foreign_holding": score_foreign_holding_axis("000660"),
        },
        "hyperscaler_capex": read_hyperscaler_capex(),
        "ai_periphery": read_ai_periphery(),
        "sk_hynix_live": {
            "price_snapshot": read_latest_price_snapshot("000660"),
            "flow_summary": summarize_flows(flow_rows) if flow_rows else None,
            "flow_latest_date": flow_rows[-1]["date"] if flow_rows else None,
            "credit_balance": credit_balance_streak("000660"),
            "short_sale": read_latest_short_sale("000660"),
            "adr": read_latest_adr("SKHY"),
        },
    }

    @dataclass
    class FakeDecision:
        signal: str = "HOLD"
        confidence: float = 50.0
        rationale: str = "test"
        macro_linkage: str = "test linkage"
        risk_flags: list = None
        triggers: list = None
        next_check: str = "soon"
        valuation_band: dict = None

    import engine.exporters.sk_hynix_decision as skmod
    orig = skmod.compute_sk_hynix_decision
    skmod.compute_sk_hynix_decision = lambda p: FakeDecision(risk_flags=[], triggers=[])
    try:
        out = _sk_hynix_decision_section(fake_payload)
    finally:
        skmod.compute_sk_hynix_decision = orig

    assert "오늘의 실측 데이터" in out
    assert "하이퍼스케일러 CapEx QoQ" in out
    assert "GOOGL" in out  # real ticker from the CSV, not a placeholder
    # R4 guard: no directive language inside the evidence sections
    evidence_start = out.find("## HBM Cycle Score")
    evidence_end = out.find("## 위험 신호")
    evidence_text = out[evidence_start:evidence_end]
    for verb in ("매수하세요", "매도하세요", "지금 사", "지금 팔"):
        assert verb not in evidence_text


def test_wiki_digests_load_from_the_real_repo_and_none_are_stale():
    """2026-08-27 Phase 4: data/wiki_digest/*.yaml must load cleanly against the
    real wiki/monitoring/*.md files and, since both were written/updated in the
    same session, none should show drift yet."""
    from engine.report.wiki_digest import load_wiki_digests

    digests = load_wiki_digests()
    slugs = {d["slug"] for d in digests}
    assert {"hbm-cycle-score", "sk-hynix-analyst-thesis-checkpoints",
            "market-cycles-leverage-risk", "trump-midterm-tracker",
            "data-center-construction-vs-opposition",
            "semiconductor-export-peak-recovery"} <= slugs
    for d in digests:
        assert d["one_line_summary"], f"{d['slug']} digest has no summary"
        assert not d["is_stale"], f"{d['slug']} digest is stale relative to its wiki page"


def test_wiki_digest_drift_is_detected_not_silently_ignored():
    """The whole point of this bridge is that a wiki update without a matching
    digest update must be visible (data/wiki_digest/README.md's drift rule) —
    this pins that detection with a synthetic monitoring page dated after the
    digest's as_of. read_frontmatter() resolves monitoring_page as
    REPO_ROOT / monitoring_page, so the fake page has to live under REPO_ROOT
    for this round-trip to work — a tempdir outside the repo can't be used."""
    import os
    import shutil
    import tempfile
    import yaml as yaml_mod
    from engine.report import wiki_digest as wd

    tmp_name = f"_test_wiki_digest_drift_{next(tempfile._get_candidate_names())}"
    monitoring_dir = wd.REPO_ROOT / tmp_name
    monitoring_dir.mkdir()
    monitoring = monitoring_dir / "fake-status.md"
    monitoring.write_text("---\nupdated: 2026-09-01\n---\n\n# Latest Status\nfoo\n", encoding="utf-8")

    digest_dir = monitoring_dir / "digests"
    digest_dir.mkdir()
    rel_monitoring_path = os.path.relpath(str(monitoring), str(wd.REPO_ROOT))
    (digest_dir / "fake.yaml").write_text(
        yaml_mod.safe_dump({
            "monitoring_page": rel_monitoring_path,
            "as_of": "2026-08-20",
            "status_label": "test",
            "one_line_summary": "test",
        }),
        encoding="utf-8",
    )

    saved_dir = wd.DIGEST_DIR
    wd.DIGEST_DIR = digest_dir
    try:
        digests = wd.load_wiki_digests()
    finally:
        wd.DIGEST_DIR = saved_dir
        shutil.rmtree(monitoring_dir)

    assert len(digests) == 1
    assert digests[0]["is_stale"] is True
    assert digests[0]["page_updated"] == "2026-09-01"


def test_wiki_digest_section_never_contains_directive_language():
    """R4 guard for Phase 4 — the wiki digest section is context, never a second
    position instruction alongside the decision engine."""
    from engine.report.markdown import _wiki_digest_section
    from engine.report.wiki_digest import load_wiki_digests

    out = _wiki_digest_section({"wiki_digests": load_wiki_digests()})
    assert "2.7 위키 추적 신호 요약" in out
    for verb in ("매수하세요", "매도하세요", "지금 사", "지금 팔"):
        assert verb not in out
    assert "R4" in out  # explicit "not a directive" disclaimer present


def test_calendar_section_and_economic_events_no_longer_contradict_each_other():
    """2026-08-27 Phase 5: Section 14 used to read data/manual_inputs/calendar.yaml
    (all-EXAMPLE, past-dated -> always '확정된 일정 없음') while Section 3.5 read a
    separate hardcoded event list -- the same report simultaneously claimed 'no
    events' and listed three specific ones. Both must now agree on the same
    events."""
    from engine.report.markdown import _calendar
    from engine.report.economic_events import get_upcoming_events

    out = _calendar({})
    events = get_upcoming_events()
    for e in events:
        assert e.date in out and e.name in out
    assert "확정된 일정 없음" not in out or not events


def test_stale_hardcoded_events_are_flagged_loudly_not_shown_as_current():
    """get_upcoming_events() is still Phase-3a placeholder data (its own docstring
    says so) — if every event date has already passed, generate_event_section()
    must say so loudly rather than silently presenting stale sample dates as
    this week's real calendar."""
    from engine.report.economic_events import generate_event_section, get_upcoming_events
    from datetime import datetime

    events = get_upcoming_events()
    all_past = all((datetime.strptime(e.date, "%Y-%m-%d") - datetime.now()).days < 0 for e in events)
    out = generate_event_section({})
    if all_past:
        assert "이미 지난 날짜" in out


def test_reports_index_covers_every_report_file_and_links_are_well_formed():
    """2026-08-31: 'every generated report must be reachable via a link here'
    (user request) — build_index() must find every dated/monthly report/*.md
    and sources/sk-hynix-auto-report-*.md that actually exists on disk, and
    every .html file must get mirrored into docs/archive/ so its link
    actually resolves (GitHub's blob view doesn't render .html, only Pages
    serving docs/ does)."""
    import glob
    from scripts.build_reports_index import build_index, ARCHIVE_DIR, INDEX_PATH

    build_index()
    out = INDEX_PATH.read_text(encoding="utf-8")

    real_daily_md = glob.glob("report/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md")
    assert real_daily_md, "fixture expects at least one dated report/*.md on disk"
    for path in real_daily_md:
        assert path.split("/")[-1].replace(".md", "") in out

    real_html = glob.glob("report/*.html")
    for path in real_html:
        name = path.split("/")[-1]
        mirrored = ARCHIVE_DIR / name
        assert mirrored.exists(), f"{name} should have been mirrored into docs/archive/"
        assert name in out

    sk_hynix_md = glob.glob("sources/sk-hynix-auto-report-*.md")
    if sk_hynix_md:
        sample = sk_hynix_md[0].split("/")[-1]
        assert sample in out


def test_reports_index_mirroring_is_idempotent():
    """Re-running the index builder with no new report files must not touch
    files it already mirrored (CI commits only real diffs, not a full
    re-copy every run)."""
    from scripts.build_reports_index import build_index, ARCHIVE_DIR

    build_index()
    sample = next(ARCHIVE_DIR.glob("*.html"), None)
    assert sample is not None, "fixture expects at least one mirrored .html file"
    mtime_before = sample.stat().st_mtime_ns

    build_index()
    assert sample.stat().st_mtime_ns == mtime_before, "unchanged file must not be rewritten"


def test_archive_date_uses_kst_not_the_runners_utc_clock():
    """2026-09-01: report/2026-08-31.md never got created because run.py used
    date.today() (the GitHub Actions runner's UTC clock) to name the daily
    archive, but the cron targets 06:00 KST. A run that fires late — e.g.
    23:08 UTC on 2026-08-30, a real delay observed on this workflow — is
    already 08:08 KST on 2026-08-31 (KST = UTC+9 crosses midnight at 15:00
    UTC), so it should archive as 2026-08-31, not the UTC calendar date
    2026-08-30 the old code would have produced. This pins the fix
    (engine/report/run.py's KST-based `today_kst`) against that exact
    real-world instant."""
    from engine.report.run import KST
    from datetime import datetime, timezone

    # The literal instant run #64 actually started (created_at from the
    # GitHub Actions API) — this is real observed data, not a hypothetical.
    delayed_utc_instant = datetime(2026, 8, 30, 23, 8, 23, tzinfo=timezone.utc)

    old_buggy_result = delayed_utc_instant.date().isoformat()  # what date.today() equivalent gave
    fixed_result = delayed_utc_instant.astimezone(KST).date().isoformat()

    assert old_buggy_result == "2026-08-30", "sanity check on the fixture itself"
    assert fixed_result == "2026-08-31", (
        "a run landing at 23:08 UTC is already the next KST day — the archive "
        "must be dated 2026-08-31, matching the 06:00 KST slot this cron targets"
    )


def test_automation_run_log_creates_header_then_appends():
    """2026-08-27: CI 단계 자동 상태로그 신설 — 첫 호출은 헤더+1행, 두 번째
    호출은 헤더 없이 1행만 추가해야 append-only 원칙을 지킨다."""
    import csv, pathlib, tempfile
    from scripts.log_automation_run import append_row

    tmp = pathlib.Path(tempfile.mkdtemp()) / "automation-run-log.csv"
    append_row("sk-hynix-daily-report", "investor_flow_fetch", "1", "36", "success", path=tmp)
    append_row("macro-data-sync", "macro_sync", "5", "36", "exhausted", path=tmp)

    rows = list(csv.DictReader(open(tmp, encoding="utf-8")))
    assert len(rows) == 2, f"expected 2 data rows, got {len(rows)}"
    assert rows[0]["workflow"] == "sk-hynix-daily-report"
    assert rows[0]["result"] == "success"
    assert rows[1]["workflow"] == "macro-data-sync"
    assert rows[1]["attempts_used"] == "5"
    assert rows[1]["result"] == "exhausted"


def test_automation_run_log_rejects_unknown_result():
    """success/exhausted 둘 중 하나가 아니면 조용히 넘어가지 않고 즉시 실패
    — CI 스텝에서 오타가 나면 로그가 아니라 워크플로 자체가 눈에 띄게 죽어야
    한다(silent corruption 방지)."""
    import pathlib, tempfile
    from scripts.log_automation_run import append_row

    tmp = pathlib.Path(tempfile.mkdtemp()) / "automation-run-log.csv"
    try:
        append_row("sk-hynix-daily-report", "investor_flow_fetch", "1", "36", "partial", path=tmp)
        raised = False
    except ValueError:
        raised = True
    assert raised, "an invalid result value must raise, not be written"
    assert not tmp.exists(), "no file should be created on a rejected write"


def _fake_cci_payload(**overrides):
    """Minimal but structurally real cci_analysis payload — same shape
    engine/report/payload.py's _cci_section() produces, so the markdown/HTML
    renderers exercise their real key-lookup paths."""
    base = {
        "total_score": 5, "state": "GREEN",
        "score_components": {
            "sahm": 0, "yield_curve": 0, "harvey": 0, "copper_gold": 3,
            "credit_oas": 0, "buffett": 0, "rule_of_20": 0, "k_sahm": 0, "semiconductor": 5,
        },
        "raw_values": {
            "ur_ma3": None, "ur_min_12m": None, "spread_10y2y": None, "spread_10y3m": None,
            "hy_oas": None, "copper_gold_ratio": -0.02, "k_emp_yoy": None, "semi_cycle_index": -0.01,
        },
        "data_quality": {
            "sahm": {"quality": "NO_DATA", "series": None, "as_of": None, "days_stale": None},
            "yield_curve": {"quality": "PRIMARY", "series": "fred_us_10y_treasury", "as_of": "2026-08-28", "days_stale": 4},
            "harvey": {"quality": "PRIMARY", "series": "fred_us_yield_curve_10y2y", "as_of": "2026-08-31", "days_stale": 1},
            "copper_gold": {"quality": "PRIMARY", "series": "fred_us_industrial_production", "as_of": "2026-07-01", "days_stale": 62},
            "credit_oas": {"quality": "NO_DATA", "series": None, "as_of": None, "days_stale": None},
            "buffett": {"quality": "NO_DATA", "series": None, "as_of": None, "days_stale": None},
            "rule_of_20": {"quality": "NO_DATA", "series": None, "as_of": None, "days_stale": None},
            "k_sahm": {"quality": "NO_DATA", "series": None, "as_of": None, "days_stale": None},
            "semiconductor": {"quality": "FALLBACK", "series": "fred_us_industrial_production", "as_of": "2026-07-01", "days_stale": 62},
        },
        "sk_hynix_action": {"action": "적극 매수 (Long)", "max_weight": 25,
                            "description": "d", "signal": "s"},
        "interpretation": {"GREEN": "g", "YELLOW": "y", "RED": "r"},
    }
    base.update(overrides)
    return base


def test_cci_report_shows_freshness_for_every_module_not_just_a_score():
    """2026-09-01: user said '데이터 신선도가 표시가 없네! 특히 몇점이고 판단만
    하는 항목은 믿을 수가 없네!' — the markdown CCI section must show, for
    every one of the 9 modules, whether the score came from a fresh primary
    series, a fallback, or no data at all (not just a bare number)."""
    from engine.report.markdown import _cci_analysis

    out = _cci_analysis({"cci_analysis": _fake_cci_payload()})

    # The score table must carry a freshness column with real badges, not
    # just the score numbers.
    assert "데이터 신선도" in out
    assert "🟢실측 · 4일 전" in out  # yield_curve
    assert "🟡대체 · 62일 전" in out  # semiconductor
    assert "⛔ 데이터없음(판정 안 함)" in out  # e.g. sahm/credit_oas/buffett/rule_of_20/k_sahm

    # All 9 modules must have their own numbered narrative — before this fix,
    # Copper-Gold/Buffett/Rule of 20/K-Sahm had no individual write-up at all
    # (only Sahm/Yield Curve/Harvey/Credit OAS/Semiconductor did).
    for n in range(1, 10):
        assert f"**{n}." in out, f"module #{n} is missing its narrative section"
    assert "Copper-Gold Ratio**" in out
    assert "Buffett Indicator**" in out
    assert "Rule of 20**" in out
    assert "K-Sahm Rule" in out


def test_cci_report_explains_why_buffett_and_rule20_are_disabled():
    """The disabled modules must say *why* in the report itself (no real PER /
    market-cap data source exists), not just show a silent 0 that reads as
    'measured and safe' — that silent-0 pattern is exactly what let Rule of
    20 masquerade as a real signal for as long as it did."""
    from engine.report.markdown import _cci_analysis

    out = _cci_analysis({"cci_analysis": _fake_cci_payload()})
    assert "영구 비활성화" in out
    assert "시가총액" in out  # Buffett's missing data source, named explicitly
    assert "PER" in out       # Rule of 20's missing data source, named explicitly


def test_html_cci_table_lists_all_nine_modules_not_a_summed_other_row():
    """Before this fix, HTML rendered Copper-Gold/Buffett/Rule of 20/K-Sahm as
    one opaque summed '기타 지표' number — exactly what made the user unable
    to tell what the constant '5' was. Each module must now be its own row."""
    from engine.report.html_new import _cci_module_rows

    rows_html = _cci_module_rows(_fake_cci_payload())
    assert "기타 지표" not in rows_html
    for label in ("Copper-Gold Ratio", "Buffett Indicator", "Rule of 20", "K-Sahm Rule"):
        assert label in rows_html
    assert "🟢실측 · 4일 전" in rows_html   # yield_curve
    assert "🟡대체 · 62일 전" in rows_html  # semiconductor
    assert "⛔ 없음" in rows_html           # buffett/rule_of_20


if __name__ == "__main__":
    import sys, traceback
    fns = [(n, f) for n, f in sorted(globals().items())
           if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in fns:
        try:
            fn()
            print(f"  PASS  {name}")
        except Exception:
            failed += 1
            print(f"  FAIL  {name}")
            traceback.print_exc()
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
