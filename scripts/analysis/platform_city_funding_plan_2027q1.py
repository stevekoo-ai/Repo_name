import math,sys
P=float(sys.argv[1]) if len(sys.argv)>1 else 1113000   # 하이닉스 주가 가정(고정)
price=870_000_000                                         # 플랫폼시티 84㎡ 분양가 가정
M=lambda y,m:(y,m)
def months(a,b):
    y,m=a;out=[]
    while (y,m)<=b: out.append((y,m)); m+=1; y,m=(y+1,1) if m>12 else (y,m)
    return out
ev={}  # (y,m) -> list of (label, amount) +유입 -유출 ; ('SH',n) 주식 유입
def add(k,l,a): ev.setdefault(k,[]).append((l,a))
add(M(2027,2),"현 전세 보증금 반환",462_000_000)
add(M(2027,2),"임시거주 전세 보증금(성원상떼빌 5.2억 가정)",-520_000_000)
add(M(2027,2),"회사 주택대출 추가 실행",150_000_000)
add(M(2027,2),"기타 투자자산 현금화(ISA 채권·ETF 등)",52_700_000)
add(M(2027,2),"2026분 PS 현금(세후, DC20% 적립 후)",30_000_000)
add(M(2027,2),"SH:2026분 PS 자사주 약 3.2억",320_000_000)
add(M(2027,3),"청약통장 해지(당첨 후)",29_800_000)
add(M(2027,3),"플랫폼시티 계약금 10%",-0.10*price)
for k in [M(2027,8),M(2028,1),M(2028,6),M(2028,11),M(2029,4),M(2029,9)]:
    add(k,"중도금 10%",-0.10*price)
add(M(2028,2),"SH:2027분 PS(3배 가정)+2026분 이연 10% 세후",192_000_000)
add(M(2029,2),"SH:이연 자사주(2026분·2027분) 세후",75_000_000)
add(M(2029,2),"임시거주 갱신 +5%",-26_000_000)
add(M(2030,1),"잔금 30% − 기금융자 7,500만",-(0.30*price-75_000_000))
add(M(2030,1),"취득세 약 3.08%",-0.0308*price)
add(M(2030,1),"임시거주 보증금 반환",546_000_000)
add(M(2030,2),"SH:2027분 이연 10% 세후",21_000_000)
cash=40_039_813; sh=183; lock=67; MIN=30_000_000; interest=200_000_000*0.015/12
rows=[];totsell=0;minc=(1e18,None)
for k in months(M(2026,12),M(2030,2)):
    flows=ev.get(k,[]); labels=[]
    if k==M(2027,2): sh+=lock; labels.append("하나 마크업 67주 해제")
    io=0
    for l,a in flows:
        if l.startswith("SH:"): n=round(a/P); sh+=n; labels.append(l[3:]+f" (+{n}주)")
        else: io+=a; labels.append(l)
    loan_int = -(50_000_000*0.015/12) if k<M(2027,2) else -interest
    io+=loan_int
    cash+=io; sell=0
    if cash<MIN:
        sell=math.ceil((MIN+6*interest-cash)/P); sell=min(sell,sh); cash+=sell*P; sh-=sell; totsell+=sell
    if cash<minc[0]: minc=(cash,k)
    rows.append((f"{k[0]}-{k[1]:02d}"," · ".join(labels) or "—",io,sell,cash,sh))
print(f"| 월 | 이벤트 | 현금 순흐름(만원) | 하이닉스 매도 | 월말 현금(만원) | 하이닉스 보유(주) |")
print("|---|---|---:|---:|---:|---:|")
for r in rows: print(f"| {r[0]} | {r[1]} | {r[2]/1e4:+,.0f} | {r[3] or ''} | {r[4]/1e4:,.0f} | {r[5]} |")
print(f"\n주가 {P:,.0f}: 총 매도 {totsell}주, 2030-02 보유 {sh}주(평가 {sh*P/1e8:.2f}억), 최저 현금 {minc[0]/1e4:,.0f}만 {minc[1]}")
