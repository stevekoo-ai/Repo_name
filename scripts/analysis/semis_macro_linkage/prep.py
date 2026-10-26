"""1단계: 종목 종가 + 거시 지표를 같은 기준(일간 변화)으로 정리한다."""
import os, sys, csv, json, math, bisect, collections
from datetime import date, timedelta
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "scripts")); sys.path.insert(0, REPO)
import macro_data

OUT = os.path.join(HERE, "out") + os.sep   # 생성물(커밋 제외, .gitignore)
os.makedirs(OUT, exist_ok=True)
START, END = '2026-04-23', '2026-10-23'

# --- 종목 ---
STOCKS = {'삼성전자': '005930.KS', '하이닉스': '000660.KS', '마이크론': 'MU'}
px = {}
for n, t in STOCKS.items():
    bars, _ = macro_data.yahoo_chart(t, start='2026-04-01')
    px[n] = {b[0]: float(b[1]) for b in bars if b[0] <= END}
json.dump(px, open(OUT + 'px.json', 'w'))

# --- 지표: (이름, 소스series, 변환, 군, 비고) ---
# 변환: bp=수준 차이×100(%p→bp), pt=수준 차이, lr=로그수익률
IND = [
 ('us_2y',        'us_2y',               'bp', '금리', 'FRED'),
 ('us_10y',       'us_10y_yf',           'bp', '금리', 'Yahoo(FRED us_10y는 10/22까지라 최신 쪽 사용)'),
 ('us_30y',       'us_30y',              'bp', '금리', 'FRED'),
 ('us_3m',        'us_3m',               'bp', '금리', 'FRED'),
 ('kr_10y',       'kr_treasury_10y',     'bp', '금리', 'ECOS 국고10년'),
 ('us_5y5y_infl', 'us_5y5y_infl',        'bp', '금리', 'FRED 5y5y 기대인플레'),
 ('usdkrw',       'kr_usdkrw',           'lr', '달러·환율', ''),
 ('dxy',          'us_dollar_index_dxy', 'lr', '달러·환율', 'Yahoo DXY(FRED 달러지수는 10/16까지)'),
 ('usdjpy',       'usd_jpy',             'lr', '달러·환율', 'FRED(10/16까지)'),
 ('usdcny',       'usd_cny',             'lr', '달러·환율', 'FRED(10/16까지)'),
 ('brent_fut',    'us_brent_futures',    'lr', '유가', 'ICE 근월물'),
 ('brent_spot',   'us_brent',            'lr', '유가', 'FRED 현물(10/20까지)'),
 ('wti',          'us_wti',              'lr', '유가', 'FRED(10/20까지)'),
 ('vix',          'us_vix_yf',           'lr', '위험선호·신용', 'Yahoo'),
 ('fear_greed',   'us_fear_greed',       'pt', '위험선호·신용', 'CNN 0~100'),
 ('hy_oas',       'us_hy_oas',           'bp', '위험선호·신용', 'FRED 하이일드 스프레드'),
 ('hy_tr',        'us_hy_tr',            'lr', '위험선호·신용', 'FRED 하이일드 총수익지수'),
 ('ig_tr',        'us_ig_tr',            'lr', '위험선호·신용', 'FRED 투자등급 총수익지수'),
 ('nasdaq',       'us_nasdaq_yf',        'lr', '주식시장', 'Yahoo'),
 ('sp500',        'us_sp500_yf',         'lr', '주식시장', 'Yahoo'),
]
ser = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(REPO, 'sources', 'macro-series.csv'))):
    ser[r['series']][r['date']] = float(r['value'])

def asof(d, dates, vals, ds):
    """ds(문자열 날짜) 이하 마지막 관측값과 그 날짜."""
    i = bisect.bisect_right(dates, ds) - 1
    return (vals[i], dates[i]) if i >= 0 else (None, None)

def change(kind, a, b):
    if a is None or b is None: return None
    if kind == 'bp': return (b - a) * 100
    if kind == 'pt': return b - a
    return math.log(b / a) if a > 0 and b > 0 else None

def minus1(ds): return (date.fromisoformat(ds) - timedelta(days=1)).isoformat()

panel = {}   # (stock, ind, mode) -> {date: change}
cov = []
for sn in STOCKS:
    days = sorted(d for d in px[sn] if d >= '2026-04-01')
    pairs = [(days[i-1], days[i]) for i in range(1, len(days)) if START <= days[i] <= END]
    rets = {b: math.log(px[sn][b] / px[sn][a]) for a, b in pairs}
    panel[(sn, '_ret')] = rets
    for name, src, kind, grp, note in IND:
        s = ser[src]; dates = sorted(s); vals = [s[d] for d in dates]
        for mode in ('same', 'lead1'):
            ch, stale, miss = {}, 0, 0
            for a, b in pairs:
                aa, bb = (a, b) if mode == 'same' else (minus1(a), minus1(b))
                va, da = asof(aa, dates, vals, aa); vb, db = asof(bb, dates, vals, bb)
                if da is None or db is None or db > END: miss += 1; continue
                if da == db: stale += 1          # 구간 안에 새 관측이 없다(휴장·미갱신) → 변화 0으로 이월
                c = change(kind, va, vb)
                if c is None: miss += 1; continue
                ch[b] = (c, da == db)
            panel[(sn, name, mode)] = ch
            cov.append((sn, name, mode, len(pairs), len(ch), stale, miss))
json.dump({'|'.join(k): v for k, v in panel.items()}, open(OUT + 'panel.json', 'w'))

# --- 보고 ---
print('기간', START, '~', END)
for sn in STOCKS:
    print(f'{sn}: 거래일(수익률) {len(panel[(sn,"_ret")])}개, 첫 {min(panel[(sn,"_ret")])}, 끝 {max(panel[(sn,"_ret")])}')
print()
print(f'{"지표":14}{"군":10}{"마지막 관측":12}{"6개월 관측수":>10}  비고')
for name, src, kind, grp, note in IND:
    s = ser[src]; ds = sorted(d for d in s if START <= d <= END)
    print(f'{name:14}{grp:10}{ds[-1]:12}{len(ds):>10}  {note}')
print()
print('종목별·지표별 결측/이월 (same 모드) — 표본 N 대비 이월(stale) 비율')
agg = collections.defaultdict(dict)
for sn, name, mode, n, got, stale, miss in cov:
    if mode == 'same': agg[name][sn] = (n, got, stale, miss)
for name, *_ in IND:
    row = agg[name]
    print(f'{name:14}', ' | '.join(f'{sn} N={v[1]}/{v[0]} 이월{v[2]} 결측{v[3]}' for sn, v in row.items()))
