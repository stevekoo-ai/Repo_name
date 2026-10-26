import os, json, math, collections, statistics as st
from datetime import date
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = os.environ.get('LINKAGE_TAG', '6m')
P = {tuple(k.split('|')): v for k, v in json.load(open(os.path.join(HERE, 'out', TAG, 'panel.json'))).items()}
STK = ['삼성전자', '하이닉스', '마이크론']
IND = 'us_2y us_10y us_30y us_3m kr_10y us_5y5y_infl usdkrw dxy usdjpy usdcny usdjpy_yf usdcny_yf brent_fut brent_spot wti wti_fut vix fear_greed hy_oas hy_tr ig_tr nasdaq sp500'.split()
KRIND = {'kr_10y', 'usdkrw'}
def mode_for(stock, ind):   # 결과를 보기 전에 정한 시차 규칙
    if stock == '마이크론': return 'same'
    return 'same' if ind in KRIND else 'lead1'

def corr(x, y):
    n = len(x)
    if n < 8: return None
    mx, my = sum(x)/n, sum(y)/n
    sx = sum((a-mx)**2 for a in x); sy = sum((b-my)**2 for b in y)
    return sum((a-mx)*(b-my) for a, b in zip(x, y)) / math.sqrt(sx*sy) if sx > 0 and sy > 0 else None

def pairs(stock, ind, mode, lo='0000', hi='9999', drop_stale=True):
    r = P[(stock, '_ret')]; c = P[(stock, ind, mode)]
    ds = sorted(d for d in r if d in c and lo <= d <= hi and not (drop_stale and c[d][1]))
    return ds, [c[d][0] for d in ds], [r[d] for d in ds]

def tstat(r, n): return r*math.sqrt((n-2)/(1-r*r)) if r is not None and abs(r) < 1 else None

# ---------- 3a. 일간 상관 (전체 6개월, 규칙 시차) ----------
print(f'=== 3a. 일간 변화 상관 [{TAG}] (시차 규칙 적용, 이월일 제외) ===')
res = {}
for s in STK:
    res[s] = {}
    for i in IND:
        ds, x, y = pairs(s, i, mode_for(s, i)); r = corr(x, y); res[s][i] = (r, len(ds))
hdr = f'{"지표":13}' + ''.join(f'{s:>12}' for s in STK)
print(hdr)
for i in sorted(IND, key=lambda i: -max(abs(res[s][i][0] or 0) for s in STK)):
    print(f'{i:13}' + ''.join(f'{res[s][i][0]:>+9.2f}({res[s][i][1]:>3})' if res[s][i][0] is not None else f'{"n/a":>12}' for s in STK))
print('(괄호=사용 일수. |r|>0.18이면 N≈120에서 양측 5% 유의 수준)\n')
for s in STK:
    top = sorted(IND, key=lambda i: -abs(res[s][i][0] or 0))[:5]
    print(f'{s} 상위 5: ' + ', '.join(f'{i}({res[s][i][0]:+.2f})' for i in top))

# ---------- 3b. 시차 규칙 반대 모드 (견고성) ----------
print('\n=== 3b. 견고성: 반대 시차에서도 같은 부호·비슷한 크기인가 (|r| 상위 지표) ===')
for s in STK:
    top = sorted(IND, key=lambda i: -abs(res[s][i][0] or 0))[:5]
    row = []
    for i in top:
        m1 = mode_for(s, i); m2 = 'lead1' if m1 == 'same' else 'same'
        r2 = corr(*pairs(s, i, m2)[1:])
        row.append(f'{i} {m1}:{res[s][i][0]:+.2f}/{m2}:{r2:+.2f}')
    print(f'{s}: ' + ' | '.join(row))

# ---------- 3c. 주간 (달력 주 합산) ----------
print('\n=== 3c. 주간 변화 상관 (보조, 약 26주) ===')
def weekly(stock, ind, mode):
    r = P[(stock, '_ret')]; c = P[(stock, ind, mode)]
    W = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for d in r:
        if d in c and not c[d][1]:
            y, w, _ = date.fromisoformat(d).isocalendar(); k = (y, w)
            W[k][0] += c[d][0]; W[k][1] += r[d]; W[k][2] += 1
    ks = sorted(k for k in W if W[k][2] >= 3)
    return [W[k][0] for k in ks], [W[k][1] for k in ks]
wres = {}
for s in STK:
    wres[s] = {i: (corr(*weekly(s, i, mode_for(s, i))), len(weekly(s, i, mode_for(s, i))[0])) for i in IND}
    top = sorted(IND, key=lambda i: -abs(wres[s][i][0] or 0))[:5]
    print(f'{s} 상위 5(주간): ' + ', '.join(f'{i}({wres[s][i][0]:+.2f})' for i in top), f'[N={wres[s][top[0]][1]}주]')

# ---------- 4. 구간별 ----------
SEG = [('상승기 4/23~6/22', '2026-04-23', '2026-06-22'), ('하락기 6/23~10/23', '2026-06-23', '2026-10-23'),
       ('7월', '2026-07-01', '2026-07-31'), ('8~9월', '2026-08-01', '2026-09-30'), ('10월', '2026-10-01', '2026-10-23')]
print('\n=== 4. 구간별 일간 상관 — 구간마다 |r| 상위 3 지표 ===')
for s in STK:
    print(f'[{s}]')
    for name, lo, hi in SEG:
        rr = {}
        for i in IND:
            ds, x, y = pairs(s, i, mode_for(s, i), lo, hi); r = corr(x, y)
            if r is not None: rr[i] = (r, len(ds))
        if not rr: continue
        top = sorted(rr, key=lambda i: -abs(rr[i][0]))[:3]
        print(f'  {name:16} N≈{max(v[1] for v in rr.values()):>3}  ' + ', '.join(f'{i}({rr[i][0]:+.2f})' for i in top))
# 폭락 4일 (기술통계)
print('\n=== 4b. 10/12~10/15 폭락 4거래일 — 종목 수익률 vs 지표 변화 ===')
days = ['2026-10-12', '2026-10-13', '2026-10-14', '2026-10-15']
for s in STK:
    r = P[(s, '_ret')]
    print(f'[{s}] ' + ' '.join(f'{d[5:]}:{(math.exp(r[d])-1)*100:+.1f}%' for d in days if d in r))
for i in ['us_10y', 'vix', 'hy_oas', 'nasdaq', 'brent_fut', 'usdkrw', 'fear_greed']:
    c = P[('하이닉스', i, mode_for('하이닉스', i))]
    print(f'  {i:11}(하이닉스 정렬) ' + ' '.join(f'{d[5:]}:{c[d][0]:+.3f}{"*" if c[d][1] else ""}' for d in days if d in c))
