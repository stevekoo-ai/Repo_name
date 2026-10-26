import os, json, math, random, csv, bisect, statistics as st
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
exec(open(os.path.join(HERE, 'corr.py'), encoding='utf-8').read().split('# ---------- 3a.')[0])   # P, STK, IND, mode_for, corr, pairs 재사용

def build(stock, inds, lo='0000', hi='9999'):
    r = P[(stock, '_ret')]; c = {i: P[(stock, i, mode_for(stock, i))] for i in inds}
    ds = sorted(d for d in r if lo <= d <= hi and all(d in c[i] and not c[i][d][1] for i in inds))
    X = np.array([[c[i][d][0] for i in inds] for d in ds]); y = np.array([r[d] for d in ds])
    return ds, X, y

def ols(X, y):
    A = np.column_stack([np.ones(len(y)), X]); b, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ b; r2 = 1 - res.var()/y.var(); n, k = len(y), X.shape[1]
    return b, r2, 1 - (1-r2)*(n-1)/(n-k-1)

# ---------- 5a. 지표 4개 선택(서로 겹치지 않게) + 설명력 + 표본외 ----------
print('=== 5a. 다변수 설명력 (서로 상관 |ρ|<0.7인 상위 4개 지표) ===')
full = {s: {i: corr(*pairs(s, i, mode_for(s, i))[1:]) for i in IND} for s in STK}
sel = {}
for s in STK:
    chosen = []
    for i in sorted(IND, key=lambda i: -abs(full[s][i] or 0)):
        ok = True
        for j in chosen:
            ds, xi, xj = pairs(s, i, mode_for(s, i))[0], pairs(s, i, mode_for(s, i))[1], pairs(s, j, mode_for(s, j))[1]
            m = {d: v for d, v in zip(*pairs(s, j, mode_for(s, j))[:2])}
            a = [(v, m[d]) for d, v in zip(pairs(s, i, mode_for(s, i))[0], xi) if d in m]
            if abs(corr([p for p, _ in a], [q for _, q in a]) or 0) >= 0.7: ok = False; break
        if ok: chosen.append(i)
        if len(chosen) == 4: break
    sel[s] = chosen
    ds, X, y = build(s, chosen)
    b, r2, ar2 = ols(X, y)
    half = len(ds)//2
    b1, *_ = ols(X[:half], y[:half])
    pred = np.column_stack([np.ones(len(y)-half), X[half:]]) @ b1
    oos = 1 - ((y[half:]-pred)**2).sum()/((y[half:]-y[:half].mean())**2).sum()
    print(f'{s}: {chosen}  N={len(ds)}  R²={r2:.2f}  조정R²={ar2:.2f}  표본외R²(앞반으로 적합→뒷반 예측)={oos:+.2f}')

# ---------- 5b. 세 종목 공통 요인 ----------
print('\n=== 5b. 세 종목 공통 요인 (한국 거래일 기준, 마이크론은 직전 미국 세션) ===')
ks = sorted(set(P[('삼성전자', '_ret')]) & set(P[('하이닉스', '_ret')]))
mu = P[('마이크론', '_ret')]; mud = sorted(mu)
def prev_us(d):
    i = bisect.bisect_left(mud, d) - 1
    return mud[i] if i >= 0 else None
rows = [(d, P[('삼성전자', '_ret')][d], P[('하이닉스', '_ret')][d], mu[prev_us(d)]) for d in ks if prev_us(d)]
D = np.array([[r[1], r[2], r[3]] for r in rows]); Z = (D - D.mean(0))/D.std(0)
w, v = np.linalg.eigh(np.corrcoef(Z.T)); o = w.argsort()[::-1]; w, v = w[o], v[:, o]
if v[:, 0].sum() < 0: v[:, 0] *= -1
print(f'N={len(rows)}일  PC1 설명 비중 {w[0]/w.sum():.0%}  적재(삼성/하이닉스/마이크론) = ' + ' / '.join(f'{x:+.2f}' for x in v[:, 0]))
print('종목쌍 상관: 삼성-하이닉스 %.2f, 삼성-MU(전일) %.2f, 하이닉스-MU(전일) %.2f' % (np.corrcoef(D.T)[0,1], np.corrcoef(D.T)[0,2], np.corrcoef(D.T)[1,2]))
pc1 = Z @ v[:, 0]; dates = [r[0] for r in rows]
print('PC1과 연동 상위 지표(한국 종목 시차 규칙, 이월일 제외):')
rr = {}
for i in IND:
    c = P[('하이닉스', i, mode_for('하이닉스', i))]
    a = [(c[d][0], p) for d, p in zip(dates, pc1) if d in c and not c[d][1]]
    rr[i] = (corr([x for x, _ in a], [y for _, y in a]), len(a))
for i in sorted(rr, key=lambda i: -abs(rr[i][0] or 0))[:5]: print(f'  {i:11} r={rr[i][0]:+.2f} (N={rr[i][1]})')

# ---------- 5c. 하이닉스 고유 몫 ----------
print('\n=== 5c. 하이닉스 고유 몫 = 하이닉스 − β×삼성전자 (같은 한국 업종 요인 제거) ===')
sam = np.array([r[1] for r in rows]); hyn = np.array([r[2] for r in rows])
beta = np.polyfit(sam, hyn, 1)[0]; resid = hyn - beta*sam
print(f'β={beta:.2f}  하이닉스 변동 중 삼성전자로 설명되는 몫 R²={np.corrcoef(sam,hyn)[0,1]**2:.2f}')
lo, hi = '2026-06-23', '2026-10-23'
cum = lambda ds: sum(x for d, x in zip(dates, resid) if d in ds)
sub = [d for d in dates if lo <= d <= hi]
print(f'6/23~10/23 고유 몫 누적(로그) {sum(x for d,x in zip(dates,resid) if lo<=d<=hi):+.2f} (약 {(math.exp(sum(x for d,x in zip(dates,resid) if lo<=d<=hi))-1)*100:+.0f}%)')
fl = {r['date']: int(r['foreign_net_krw'])/1e12 for r in csv.DictReader(open(os.path.join(REPO, 'sources', 'sk-hynix-investor-flow.csv')))}
inst = {r['date']: int(r['inst_net_krw'])/1e12 for r in csv.DictReader(open(os.path.join(REPO, 'sources', 'sk-hynix-investor-flow.csv')))}
ret = {r['date']: int(r['retail_net_krw'])/1e12 for r in csv.DictReader(open(os.path.join(REPO, 'sources', 'sk-hynix-investor-flow.csv')))}
cb = {r['date']: float(r['loan_balance_qty']) for r in csv.DictReader(open(os.path.join(REPO, 'sources', 'sk-hynix-credit-balance.csv')))}
for nm, f in [('외국인 순매수(조원)', fl), ('기관', inst), ('개인', ret)]:
    a = [(f[d], x) for d, x in zip(dates, resid) if d in f and lo <= d <= hi]
    print(f'  고유 몫 vs {nm:12} r={corr([p for p,_ in a],[q for _,q in a]):+.2f} (N={len(a)})')
cbk = sorted(cb); a = []
for d, x in zip(dates, resid):
    if lo <= d <= hi and d in cb:
        i = cbk.index(d)
        if i > 0: a.append(((cb[d]/cb[cbk[i-1]]-1)*100, x))
print(f'  고유 몫 vs 신용융자 잔고 일간 변화율        r={corr([p for p,_ in a],[q for _,q in a]):+.2f} (N={len(a)})')
# 비교: 삼성전자 쪽엔 투자자 자료 없음. 하이닉스 원자료 수익률과의 상관도 함께
a2 = [(fl[d], h) for d, h in zip(dates, hyn) if d in fl and lo <= d <= hi]
print(f'  (참고) 하이닉스 원수익률 vs 외국인 순매수 r={corr([p for p,_ in a2],[q for _,q in a2]):+.2f}')

# ---------- 6. 우연 여부: 블록 순열검정 + 반분 일관성 ----------
print('\n=== 6a. 우연 검정: 수익률을 5일 블록으로 섞어 20개 지표 중 최대 |r|이 우연히 이만큼 나올 확률 ===')
random.seed(7)
for s in STK:
    r = P[(s, '_ret')]
    obs = max(abs(full[s][i] or 0) for i in IND)
    ds_all = sorted(r); vals = [r[d] for d in ds_all]; B = 5
    blocks = [vals[k:k+B] for k in range(0, len(vals), B)]
    cnt = 0; T = 600
    for _ in range(T):
        random.shuffle(blocks); sh = [x for b in blocks for x in b]; rs = dict(zip(ds_all, sh)); mx = 0
        for i in IND:
            c = P[(s, i, mode_for(s, i))]
            a = [(c[d][0], rs[d]) for d in ds_all if d in c and not c[d][1]]
            rv = corr([p for p,_ in a],[q for _,q in a]) or 0; mx = max(mx, abs(rv))
        cnt += mx >= obs
    print(f'  {s}: 관측 최대|r|={obs:.2f}  우연 확률 p≈{cnt/T:.3f}')
print('\n=== 6b. 반분 일관성: 앞 절반/뒤 절반 모두 같은 부호인 상위 지표 ===')
for s in STK:
    ds = sorted(P[(s, '_ret')]); mid = ds[len(ds)//2]
    top = sorted(IND, key=lambda i: -abs(full[s][i] or 0))[:6]; out = []
    for i in top:
        m = mode_for(s, i)
        a = corr(*pairs(s, i, m, '0000', mid)[1:]); b = corr(*pairs(s, i, m, mid, '9999')[1:])
        out.append(f'{i}({a:+.2f}/{b:+.2f}){"✔" if a*b > 0 and min(abs(a),abs(b)) > 0.1 else "✘"}')
    print(f'  {s} [앞/뒤 | 분기일 {mid}]: ' + ' '.join(out))
