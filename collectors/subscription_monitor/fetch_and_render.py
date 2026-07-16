"""
Fetches currently-open 국민주택 (public housing, savings-total ranking) subscription
listings in 서울/경기 from the 청약Home Open API (data.go.kr / api.odcloud.kr),
and renders docs/subscription-monitor.html.

Requires env var DATA_GO_KR_KEY (활용신청 인증키, "일반 인증키(Encoding)").
"""

import html
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

from alerts import run_alerts

KST = timezone(timedelta(hours=9))
BASE_URL = "https://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/getAPTLttotPblancDetail"
TARGET_REGIONS = {"서울", "경기"}
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "subscription-monitor.html")

MY_SAVINGS_TOTAL = 28_050_000
MY_SAVINGS_ROUNDS = 249
MY_JOIN_DATE = "2005-11-03"


def fetch_page(service_key: str, today: str, page: int, per_page: int = 200) -> dict:
    params = {
        "page": page,
        "perPage": per_page,
        "cond[HOUSE_DTL_SECD_NM::EQ]": "국민",
        "cond[RCEPT_ENDDE::GTE]": today,
    }
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Infuser {service_key}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def fetch_all(service_key: str, today: str) -> list[dict]:
    rows: list[dict] = []
    page = 1
    while True:
        data = fetch_page(service_key, today, page)
        rows.extend(data.get("data", []))
        match_count = data.get("matchCount", 0)
        per_page = data.get("perPage", 200)
        if page * per_page >= match_count or page > 10:
            break
        page += 1
    return rows


def fmt_money(n) -> str:
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return "-"


def row_html(r: dict) -> str:
    name = html.escape(r.get("HOUSE_NM") or "-")
    is_newlywed = "신혼희망타운" in (r.get("HOUSE_NM") or "")
    region = html.escape(r.get("SUBSCRPT_AREA_CODE_NM") or "-")
    addr = html.escape(r.get("HSSPLY_ADRES") or "-")
    rcept_b = r.get("RCEPT_BGNDE") or "-"
    rcept_e = r.get("RCEPT_ENDDE") or "-"
    announce = r.get("PRZWNER_PRESNATN_DE") or "-"
    households = fmt_money(r.get("TOT_SUPLY_HSHLDCO"))
    url = html.escape(r.get("PBLANC_URL") or "#")
    tag = '<span class="tag warn">신혼희망타운(별도기준 가능)</span>' if is_newlywed else '<span class="tag ok">일반 순차제</span>'
    return f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener">{name}</a></td>
          <td class="num">{region}</td>
          <td>{addr}</td>
          <td class="num">{rcept_b} ~ {rcept_e}</td>
          <td class="num">{announce}</td>
          <td class="num">{households}</td>
          <td>{tag}</td>
        </tr>"""


def render(rows: list[dict], now_kst: datetime) -> str:
    rows_sorted = sorted(rows, key=lambda r: (r.get("RCEPT_ENDDE") or "9999-99-99"))
    body_rows = "\n".join(row_html(r) for r in rows_sorted) or (
        '<tr><td colspan="7" style="text-align:center;color:var(--muted);padding:28px;">'
        "현재 접수 마감 전인 서울·경기 국민주택 일반공급 건이 없습니다.</td></tr>"
    )
    next_run = now_kst + timedelta(hours=4)
    updated_str = now_kst.strftime("%Y-%m-%d %H:%M KST")
    next_str = next_run.strftime("%m-%d %H:%M KST")

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>국민주택 일반공급 모니터</title>
<style>
  :root{{
    --bg:#f5f6f8; --surface:#ffffff; --surface-2:#eceff3; --ink:#161a20; --muted:#5c6470;
    --line:#dde1e7; --accent:#0b5fb0; --accent-ink:#0a4a8a; --accent-soft:#e3edf9;
    --live:#0e9a6c; --live-soft:#e1f5ec;
    --warn:#b5551a; --warn-soft:#fbe9db; --warn-line:#eec7a0;
  }}
  @media (prefers-color-scheme: dark){{
    :root{{
      --bg:#0d1116; --surface:#151a21; --surface-2:#1b212a; --ink:#e7ebf1; --muted:#8b93a1;
      --line:#2a323d; --accent:#5aa9ef; --accent-ink:#8ec4f5; --accent-soft:#122a41;
      --live:#3fd39a; --live-soft:#0f2c22;
      --warn:#ffab6b; --warn-soft:#3a2415; --warn-line:#5a381f;
    }}
  }}
  *{{box-sizing:border-box;}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font-family:"Pretendard Variable","Apple SD Gothic Neo","Malgun Gothic",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    line-height:1.6;}}
  .page{{max-width:980px;margin:0 auto;padding:44px 22px 90px;}}
  .topbar{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;
    padding-bottom:22px;border-bottom:1px solid var(--line);margin-bottom:28px;}}
  .brand .eyebrow{{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:700;
    letter-spacing:.07em;text-transform:uppercase;color:var(--accent-ink);}}
  .brand .eyebrow .dot{{width:7px;height:7px;border-radius:50%;background:var(--live);box-shadow:0 0 0 3px var(--live-soft);}}
  .brand h1{{font-size:clamp(22px,3.4vw,28px);font-weight:800;letter-spacing:-0.02em;margin:8px 0 4px;}}
  .brand p{{margin:0;color:var(--muted);font-size:14px;max-width:56ch;}}
  .clock{{text-align:right;font-size:12.5px;color:var(--muted);font-variant-numeric:tabular-nums;
    display:flex;flex-direction:column;gap:4px;min-width:190px;}}
  .clock b{{color:var(--ink);font-size:13.5px;}}
  .clock .next{{color:var(--accent-ink);font-weight:700;}}
  section{{margin-top:36px;}}
  h2{{font-size:18px;font-weight:800;margin:0 0 4px;display:flex;align-items:center;gap:9px;}}
  .lead{{color:var(--muted);font-size:14px;margin:0 0 16px;max-width:70ch;}}
  .bench{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 22px;font-size:14.5px;}}
  .bench b{{color:var(--accent-ink);font-variant-numeric:tabular-nums;}}
  .tablewrap{{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--surface);}}
  table{{border-collapse:collapse;width:100%;min-width:820px;font-size:13.6px;}}
  th,td{{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top;}}
  th{{background:var(--surface-2);font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;
    color:var(--muted);font-weight:700;white-space:nowrap;}}
  tr:last-child td{{border-bottom:none;}}
  td.num{{font-variant-numeric:tabular-nums;white-space:nowrap;}}
  a{{color:var(--accent-ink);text-decoration:none;border-bottom:1px solid currentColor;}}
  .tag{{display:inline-block;font-size:11px;font-weight:700;padding:2px 9px;border-radius:100px;white-space:nowrap;}}
  .tag.ok{{background:var(--live-soft);color:var(--live);}}
  .tag.warn{{background:var(--warn-soft);color:var(--warn);}}
  .checklist{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px;}}
  .checklist li{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 15px;font-size:13.8px;}}
  footer{{margin-top:48px;padding-top:20px;border-top:1px solid var(--line);font-size:12px;color:var(--muted);}}
</style>
</head>
<body>
<div class="page">
  <div class="topbar">
    <div class="brand">
      <span class="eyebrow"><span class="dot"></span>자동 모니터링 · LIVE</span>
      <h1>서울·경기 국민주택 일반공급 모니터</h1>
      <p>청약Home 공식 Open API 기반. 접수 마감이 지나지 않은 서울·경기 국민주택(공공분양/뉴홈) 건만 표시합니다.</p>
    </div>
    <div class="clock">
      <div>마지막 갱신<br><b>{updated_str}</b></div>
      <div class="next">다음 갱신 예정 {next_str}</div>
    </div>
  </div>

  <section>
    <h2>내 청약통장</h2>
    <div class="bench">
      저축총액 <b>{fmt_money(MY_SAVINGS_TOTAL)}원</b> · {MY_SAVINGS_ROUNDS}회 납입 · 가입일 {MY_JOIN_DATE}
    </div>
  </section>

  <section>
    <h2>현재 접수중 / 접수예정 공고 ({len(rows_sorted)}건)</h2>
    <p class="lead">국민주택 순차제(저축총액순) 대상만 표시합니다. 신혼희망타운은 &ldquo;국민&rdquo;으로 분류되지만 별도 자체 기준이 있을 수 있어 태그로 구분했습니다.</p>
    <div class="tablewrap">
      <table>
        <thead>
          <tr><th>단지명</th><th>지역</th><th>주소</th><th>일반공급 접수기간</th><th>당첨자 발표</th><th>총 세대수</th><th>구분</th></tr>
        </thead>
        <tbody>{body_rows}
        </tbody>
      </table>
    </div>
  </section>

  <section>
    <h2>직접 확인 채널</h2>
    <ul class="checklist">
      <li><a href="https://www.applyhome.co.kr/ai/aib/selectSubscrptCalenderView.do" target="_blank" rel="noopener">청약홈 청약캘린더</a> — 관심지역 알림(이메일/문자) 신청 가능</li>
      <li><a href="https://apply.lh.or.kr/" target="_blank" rel="noopener">LH청약플러스</a></li>
      <li><a href="https://apply.gh.or.kr/" target="_blank" rel="noopener">GH 경기주택도시공사 청약센터</a></li>
    </ul>
  </section>

  <footer>
    데이터 출처: 한국부동산원 청약Home 분양정보 조회 서비스(공공데이터포털 Open API). 하루 3회(10/14/18시 KST) 자동 갱신됩니다.
    계약·청약 신청 전 반드시 청약홈 원문 공고를 확인하세요.
  </footer>
</div>
</body>
</html>
"""


def main() -> None:
    service_key = os.environ["DATA_GO_KR_KEY"]
    now_kst = datetime.now(KST)
    today = now_kst.strftime("%Y-%m-%d")

    all_rows = fetch_all(service_key, today)
    rows = [r for r in all_rows if r.get("SUBSCRPT_AREA_CODE_NM") in TARGET_REGIONS]

    fired = run_alerts(all_rows)
    if fired:
        print(f"fired {fired} new 플랫폼시티 alert(s)")

    html_out = render(rows, now_kst)
    out_path = os.path.normpath(OUTPUT_PATH)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"wrote {out_path} with {len(rows)} matching listings (of {len(all_rows)} nationwide 국민주택 open)")


if __name__ == "__main__":
    main()
