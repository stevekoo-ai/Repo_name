"""2-c 롤링 6개월: 24개월 패널에서 6개월 창을 3개월씩 밀며 종목별 연동 상위 지표를 본다.
"연동 1위 지표가 계속 바뀌는가"를 기간을 늘려 재검정한다. 사용: LINKAGE_TAG=24m python3 rolling.py"""
import os
from datetime import date, timedelta
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corr.py'), encoding='utf-8').read().split('# ---------- 3a.')[0])

allds = sorted(P[('하이닉스', '_ret')])
first, last = date.fromisoformat(allds[0]), date.fromisoformat(allds[-1])
print(f'=== 롤링 6개월 창 (3개월 간격) [{TAG}] {first}~{last} ===')
wins = []
end = last
while end - timedelta(days=182) >= first:
    wins.append(((end - timedelta(days=182)).isoformat(), end.isoformat())); end -= timedelta(days=91)
wins.reverse()
stab = {s: [] for s in STK}
for lo, hi in wins:
    print(f'--- {lo} ~ {hi}')
    for s in STK:
        rr = {}
        for i in IND:
            ds, x, y = pairs(s, i, mode_for(s, i), lo, hi); r = corr(x, y)
            if r is not None and len(ds) >= 60: rr[i] = (r, len(ds))
        if not rr: print(f'  {s}: 표본 부족'); continue
        top = sorted(rr, key=lambda i: -abs(rr[i][0]))[:3]
        stab[s].append(top[0])
        print(f'  {s:6} N≈{max(v[1] for v in rr.values()):>3} ' + ', '.join(f'{i}({rr[i][0]:+.2f})' for i in top))
print('\n=== 창별 1위 지표 일치도 ===')
for s in STK:
    from collections import Counter
    c = Counter(stab[s])
    print(f'  {s}: 1위 지표 {dict(c)} → 가장 자주 1위 {c.most_common(1)[0][0] if c else "-"} ({c.most_common(1)[0][1] if c else 0}/{len(stab[s])}개 창)')
