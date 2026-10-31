import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L

F="Arial"
BLUE=Font(name=F,color="0000FF"); BLK=Font(name=F); BOLD=Font(name=F,bold=True)
GRN=Font(name=F,color="008000"); HDR=Font(name=F,bold=True,color="FFFFFF")
YEL=PatternFill("solid",fgColor="FFFF00"); HFILL=PatternFill("solid",fgColor="1F4E78")
SUB=PatternFill("solid",fgColor="DDEBF7")
WON='#,##0;(#,##0);"-"'; EOK='#,##0.00"억";(#,##0.00"억");"-"'
thin=Side(style="thin",color="BFBFBF"); BOX=Border(top=thin,bottom=thin,left=thin,right=thin)

wb=Workbook()
# ---------------- 안내 ----------------
g=wb.active; g.title="안내"
lines=[("주거·청약 월별 자금 계획 (2026-11 ~ 2031-12)",BOLD),
("작성 2026-10-31, Steve's Wiki. 숫자는 추정이며 매매 지시가 아니다(R4). 공식 매매 신호는 판단 엔진.",BLK),
("",BLK),
("사용법",BOLD),
("1) '가정' 시트의 노란 칸 3개(임시 거주 선택, 청약 시나리오, 주가 시나리오)를 바꾸면 전체가 다시 계산된다.",BLK),
("2) 파란 글씨 = 입력값(바꿔도 됨). 검은 글씨 = 수식(건드리지 말 것). 초록 = 다른 시트 참조.",BLK),
("3) '월별' 시트: 매달 들어오고 나가는 돈, 하이닉스 자동 매도 주수, 현금 잔액, 순자산.",BLK),
("4) '요약' 시트: 현재 선택한 조합의 결과(최저 현금, 부족 월, 매도 주수, 2031-12 순자산).",BLK),
("5) '시나리오비교' 시트: 모든 조합(임시 거주 7 × 청약 3 × 주가 3 = 63)을 미리 계산해 둔 값(작성 시점 스냅샷, 가정을 바꾸면 갱신 안 됨).",BLK),
("6) '전략' 시트: 하이닉스 매도·PS·청약 대응 규칙(Claude 의견, 결정은 사용자).",BLK),
("",BLK),
("하이닉스 자동 매도 규칙(월별 시트 W~Y열)",BOLD),
("매달 '앞으로 N개월 확정 지출'을 현금으로 확보하도록 부족분만큼 판다. N = 주가 ≥ 200만 원이면 12, 그 외 1(그 달 필요한 만큼만 — 사용자 10/31 '200만 원 회복 후 매도'). 가정 시트에서 변경.",BLK),
("주식은 '자유 보유분'만 쓴다 — IRP·DC 제외. 하나증권 마크업 67주는 2027-02 해제 후 매도 가능분에 더함(사용자 2026-10-31).",BLK),
("",BLK),
("주요 출처",BOLD),
("광교 A17BL 공고문(sources/gwanggyo-naturen-centreville-a17bl-public-housing-notice-2026-10-30.pdf) 84B 10층 이상 납부표",BLK),
("주변 전월세: sources/suji-jinsan-prugio-nearby-rent-survey-2026-10-30.md(사용자 조사 10/30), KB부동산(힐스테이트 수지구청역)",BLK),
("자산: KIS 자동 수집(sources/portfolio-cash.csv·portfolio-holdings.csv 10/30), config/user.yaml, 사용자 제공(10/31)",BLK),
("PS: 2026 임단협 최종안(머니투데이 2026-09-16), 2025분 지급률 2964%(ZDNet 2026-02-04), DC 적립 근속별 비율(파이낸셜뉴스 2025-12-23)",BLK),
("플랫폼시티: 공고 없음 — 일정·분양가는 전부 가정(위키 concepts/yongin-platform-city-project-facts.md)",BLK)]
for i,(t,f) in enumerate(lines,1):
    c=g.cell(row=i,column=1,value=t); c.font=f
g.column_dimensions["A"].width=140

# ---------------- 가정 ----------------
a=wb.create_sheet("가정")
a.column_dimensions["A"].width=34; a.column_dimensions["B"].width=18; a.column_dimensions["C"].width=16
for col in "DEFGH": a.column_dimensions[col].width=16
a.column_dimensions["I"].width=60
R={}
def hdr(r,text):
    c=a.cell(row=r,column=1,value=text); c.font=HDR; c.fill=HFILL
    for col in range(2,10): a.cell(row=r,column=col).fill=HFILL
def inp(r,key,label,val,fmt=None,note="",yellow=False):
    a.cell(row=r,column=1,value=label).font=BLK
    c=a.cell(row=r,column=2,value=val); c.font=BLUE
    if fmt: c.number_format=fmt
    if yellow: c.fill=YEL
    if note: a.cell(row=r,column=9,value=note).font=Font(name=F,italic=True,color="595959")
    R[key]=f"가정!$B${r}"
r=1
a.cell(row=r,column=1,value="가정 — 파란 글씨는 입력, 노란 칸은 시나리오 선택").font=BOLD; r+=2
hdr(r,"① 시나리오 선택 (노란 칸)"); r+=1
inp(r,"sel_house","임시 거주 선택 (1~7, 아래 표)",1,None,"아래 ③ 표 번호",True); r+=1
inp(r,"sel_sub","청약·매매 시나리오 (1~4)",1,None,"1=광교 당첨, 2=광교 낙첨→플랫폼시티 당첨, 3=둘 다 낙첨, 4=매매(2027-02, 청약 포기)",True); r+=1
inp(r,"sel_px","하이닉스 주가 시나리오 (1~3)",2,None,"1=비관, 2=기준, 3=낙관 (④ 표)",True); r+=2

hdr(r,"② 현재 자산 (2026-10-30 기준)"); r+=1
inp(r,"cash0","시작 현금 (CMA)",42233169,WON,"KIS 수집 portfolio-cash.csv 2026-10-30"); r+=1
inp(r,"other0","기타 투자자산 (ISA 내 채권·ETF·삼성전자 등 + 일반계좌 기타)",59760000,WON,"ISA 82.49백만 − ISA 하이닉스 28.36 + 일반 해외 등 약 5.6 (KIS 10/30). ISA 채권 포함(사용자 정정 10/31)"); r+=1
inp(r,"other_month","기타 투자자산 현금화 월",dt.date(2027,2,1),"yyyy-mm","ISA 채권 만기 2027-01-18 이후 정리 가정"); r+=1
inp(r,"shares0","하이닉스 자유 보유 주수",183,"#,##0","일반 120 + ISA 20 + 하나 자유분 43. IRP·DC 제외(사용자 지시)"); r+=1
inp(r,"lock_qty","하나증권 마크업 주수 (해제 후 매도 가능)",67,"#,##0","마크업 8,791,650원, 2027-02-11 해제 — 이후 매도 가능(사용자 10/31)"); r+=1
inp(r,"lock_month","마크업 해제 월",dt.date(2027,2,1),"yyyy-mm","2027-02-11"); r+=1
inp(r,"px0","하이닉스 시작 주가 (원)",1418000,WON,"2026-10-30 정규장 종가(한국경제·서울신문)"); r+=1
inp(r,"deposit_now","현재 전세 보증금 (반환)",462000000,WON,"config/user.yaml, 반환 2027-02-20"); r+=1
inp(r,"move_month","현재 집 반환·임시 거주 시작 월",dt.date(2027,2,1),"yyyy-mm","실제 이사일 2027-02-20(config/user.yaml)"); r+=1
inp(r,"sub_acct","청약통장 잔액 (당첨 후 해지)",28800000,WON,"2026-07 2,830만 + 월 25만 납입 추정"); r+=1
inp(r,"loan_old","기존 회사 주택대출 잔액",50000000,WON,"사용자 제공 10/31 — 순자산에서 차감"); r+=1
inp(r,"loan_rate","회사 주택대출 금리",0.015,"0.0%","사용자 제공 10/31"); r+=1
inp(r,"loan_new","회사 주택대출 추가 실행액",150000000,WON,"한도 2억 중 잔여(사용자 제공 10/31)"); r+=1
inp(r,"loan_month","추가 대출 실행 월",dt.date(2027,2,1),"yyyy-mm","임시 거주 계약 시점 가정"); r+=1
inp(r,"save_m","월 순저축 (급여 − 생활비, 월세 제외)",0,WON,"사용자 확인 2026-10-31: 거의 없음 → 0"); r+=1
inp(r,"min_cash","최소 현금 보유",30000000,WON,"비상금 가정"); r+=2

hdr(r,"③ 임시 거주 선택지 (2027-02 입주, 2년 단위 갱신)"); r+=1
for j,h in enumerate(["번호","보증금","월세","선택지","근거"],1):
    c=a.cell(row=r,column=j if j<4 else (4 if j==4 else 9),value=h); c.font=BOLD; c.fill=SUB
r+=1
houses=[(1,520000000,0,"진산마을성원상떼빌 84㎡ 전세","10/30 조사 105동 18층 5.2억(223m, 같은 학군)"),
(2,700000000,0,"힐스테이트 수지구청역 오피스텔 전세","사용자 예상 7억(10/31). KB 6.3억·최근 실거래 6.9억(7/11)"),
(3,800000000,0,"하이브엘 84㎡ 전세 (전대차)","10/30 조사 101동 8억 — HUG 불가·전대 구조"),
(4,200000000,3000000,"하이브엘 84㎡ 월세 2억/300만","사용자 예상 수준(10/31), 10/30 조사 101동 22층과 동일"),
(5,350000000,2000000,"하이브엘 84㎡ 월세 3.5억/200만","10/30 조사 103동 15층"),
(6,200000000,2100000,"진산마을푸르지오 월세 2억/210만","10/30 조사 101동 6층"),
(7,750000000,0,"진산마을푸르지오 전세 7.5억","10/30 조사 102동 호가")]
house_top=r
for n,d,m,name,src in houses:
    a.cell(row=r,column=1,value=n).font=BLUE
    c=a.cell(row=r,column=2,value=d); c.font=BLUE; c.number_format=WON
    c=a.cell(row=r,column=3,value=m); c.font=BLUE; c.number_format=WON
    a.cell(row=r,column=4,value=name).font=BLUE
    a.cell(row=r,column=9,value=src).font=Font(name=F,italic=True,color="595959")
    r+=1
house_bot=r-1
R["h_dep"]=f"INDEX(가정!$B${house_top}:$B${house_bot},{R['sel_house']})"
R["h_rent"]=f"INDEX(가정!$C${house_top}:$C${house_bot},{R['sel_house']})"
R["h_name"]=f"INDEX(가정!$D${house_top}:$D${house_bot},{R['sel_house']})"
inp(r,"renew_up","갱신 시 인상률 (전세 보증금·월세)",0.05,"0.0%","주택임대차보호법 갱신 상한 5%, 24개월마다"); r+=2

hdr(r,"④ 하이닉스 주가 시나리오 (연 변화율, 월 복리)"); r+=1
px_top=r
for n,gname,gr in [(1,"비관",-0.20),(2,"기준",0.0),(3,"낙관",0.20)]:
    a.cell(row=r,column=1,value=n).font=BLUE; a.cell(row=r,column=4,value=gname).font=BLUE
    c=a.cell(row=r,column=2,value=gr); c.font=BLUE; c.number_format="0.0%"; r+=1
R["g"]=f"INDEX(가정!$B${px_top}:$B${px_top+2},{R['sel_px']})"
inp(r,"px_accel","가속 가격 (이상이면 12개월분 선확보)",2000000,WON,"기존 T2 accelerate_if 2,000,000원(execution_plan.yaml)"); r+=1
inp(r,"px_stop","손절 가격 (미만이면 18개월분 선확보)",1341000,WON,"⑫ 시나리오 S3 바닥선 1,341,000원"); r+=1
inp(r,"n_base","기본 선확보 개월 수",1,None,"사용자 10/31: 200만 회복 전에는 필요한 만큼만 매도 → 1(다음 달분)"); r+=1
inp(r,"n_accel","가속 시 선확보 개월 수",12,None,""); r+=1
inp(r,"n_stop","손절 시 선확보 개월 수",1,None,"사용자 선호에 맞춰 1. ⑫ S3 플레이북은 18개월 선확보를 권함 — 비관 시나리오에서 재검토"); r+=1
inp(r,"t1_month","T1 매도 월",dt.date(2026,11,1),"yyyy-mm","T1 13주(선거 전) + 연기분 12주(11/13까지) 합산"); r+=1
inp(r,"t1_qty","T1 매도 주수",25,"#,##0","2026-10-29 사용자 확정안"); r+=2

hdr(r,"⑤ PS (사용자: 연봉 1.4억·근속 18년·DC 적립 가입·매도 제한 없음)"); r+=1
inp(r,"salary","연봉 (PS 산정 기준)",140000000,WON,"사용자 제공 10/31"); r+=1
inp(r,"ps26","2026년분 PS 배수 (연봉 대비)",7.6,"0.0x","2026 OP 264.8조(4Q=3Q 가정)/2025 47.2조 × 2025분 1.482배, 임금·인원 증가 보정 7.6~8.3 하단"); r+=1
inp(r,"ps27","2027년분 PS 배수 (2028-02 지급)",3.0,"0.0x","보수적(사용자 10/31): 3배 ≈ 2027 영업이익 약 105조(2026 추정 265조의 40%) 수준"); r+=1
inp(r,"ps28","2028년분 PS 배수 (2029-02 지급)",0.0,"0.0x","⚠️ 가정 — 보수적으로 0"); r+=1
inp(r,"ps_now","당해 지급 비율",0.8,"0%","임단협 최종안: 당해 80%(현금 50%+자사주 30%), 이연 20%(1·2년 후 각 10% 자사주)"); r+=1
inp(r,"ps_cash","그 중 현금 비율 (PS 대비)",0.5,"0%","기본 현금 50%"); r+=1
inp(r,"ps_dc","DC 적립 비율 (당해 지급분 대비)",0.2,"0%","근속 11~20년 20%(파이낸셜뉴스 2025-12-23), DC는 퇴직 시까지 잠김"); r+=1
inp(r,"tax","PS 실효 세율 (소득세·지방세·4대보험)",0.49,"0%","연봉 1.4억 합산 시 한계세율 42~45%+지방세+보험 약 4.9% — 추정"); r+=2

hdr(r,"⑥ 광교 A17BL 84B 10층 이상 (공고문 확정값)"); r+=1
inp(r,"gg_price","공급금액",948900000,WON,"공고문 p.6 납부표"); r+=1
inp(r,"gg_bal","발코니 확장비",4006000,WON,"20% 계약 시, 80% 잔금"); r+=1
inp(r,"gg_fund","주택도시기금 융자 (잔금 중)",75000000,WON,"공고문 — 현금 대신 융자"); r+=1
inp(r,"fund_rate","기금 융자 금리",0.025,"0.0%","⚠️ 가정"); r+=1
inp(r,"acq","취득세율 (지방교육세 포함)",0.033,"0.0%","9억 초과 1주택 3%+교육세 0.3% — 추정"); r+=1
inp(r,"gg_jan","광교 잔금 월",dt.date(2029,10,1),"yyyy-mm","입주 2029-10 예정(공고문)"); r+=1
inp(r,"gg_move","광교 실입주 월",dt.date(2031,2,1),"yyyy-mm","첫째 2031-02 고교 졸업, 둘째 2031-03 고1 — 거주의무 3년 유예 기한 2032-10 안"); r+=1
inp(r,"rent_out","광교 잔금~실입주 사이 전세 놓기 (1=예, 0=아니오)",1,None,"세입자 2년 보장 → 2031-10까지 거주 주장 가능 위험"); r+=1
inp(r,"tenant_dep","광교 세입자 전세 보증금",600000000,WON,"⚠️ 가정 — 광교 신축 84㎡ 전세 시세 미조사"); r+=2
gg_top=r
for j,h in enumerate(["회차","월","금액","","","","","","비고"],1):
    if h: c=a.cell(row=r,column=j,value=h); c.font=BOLD; c.fill=SUB
r+=1
gg_sched=[("계약금+발코니 20%",dt.date(2026,12,1),"=B{p}*0.1+B{b}*0.2"),
("중도금 1",dt.date(2027,5,1),"=B{p}*0.1"),("중도금 2",dt.date(2027,10,1),"=B{p}*0.1"),
("중도금 3",dt.date(2028,3,1),"=B{p}*0.1"),("중도금 4",dt.date(2028,8,1),"=B{p}*0.1"),
("중도금 5",dt.date(2028,12,1),"=B{p}*0.1"),("중도금 6",dt.date(2029,5,1),"=B{p}*0.1"),
("잔금(기금 제외)+발코니 80%+취득세",None,"=B{p}*0.3-B{f}+B{b}*0.8+B{p}*B{t}")]
pr=int(R["gg_price"].split("$")[-1]); br=int(R["gg_bal"].split("$")[-1]); fr=int(R["gg_fund"].split("$")[-1]); tr=int(R["acq"].split("$")[-1]); jr=int(R["gg_jan"].split("$")[-1])
gs=r
for name,d,f in gg_sched:
    a.cell(row=r,column=1,value=name).font=BLK
    c=a.cell(row=r,column=2,value=d if d else f"=B{jr}"); c.number_format="yyyy-mm"; c.font=BLUE if d else BLK
    c=a.cell(row=r,column=3,value=f.format(p=pr,b=br,f=fr,t=tr)); c.number_format=WON
    r+=1
ge=r-1
a.cell(row=r,column=1,value="광교 합계(현금)").font=BOLD
c=a.cell(row=r,column=3,value=f"=SUM(C{gs}:C{ge})"); c.number_format=WON; c.font=BOLD; r+=2
R["gg_dates"]=f"가정!$B${gs}:$B${ge}"; R["gg_amts"]=f"가정!$C${gs}:$C${ge}"

hdr(r,"⑦ 플랫폼시티 공공분양 (⚠️ 전부 가정 — 공고 없음)"); r+=1
inp(r,"pf_price","분양가 84㎡",870000000,WON,"분상제, 광교 9.49억·인근 민간 평당 2,250만 비교 추정 7.8~9.5억 중간"); r+=1
inp(r,"pf_contract","계약 월",dt.date(2028,3,1),"yyyy-mm","'2027 하반기 이후 분양 본격화'(뉴스웍스) → 공고 2027-12 가정"); r+=1
inp(r,"pf_gap","중도금 간격 (개월)",6,None,"6회 10%씩"); r+=1
inp(r,"pf_move","입주·잔금 월",dt.date(2031,9,1),"yyyy-mm","부지 준공 2030-12 목표 → 가정"); r+=2
pr2=int(R["pf_price"].split("$")[-1]); cr=int(R["pf_contract"].split("$")[-1]); gr_=int(R["pf_gap"].split("$")[-1]); mr=int(R["pf_move"].split("$")[-1])
for j,h in enumerate(["회차","월","금액"],1):
    c=a.cell(row=r,column=j,value=h); c.font=BOLD; c.fill=SUB
r+=1; ps_=r
a.cell(row=r,column=1,value="계약금 10%"); c=a.cell(row=r,column=2,value=f"=B{cr}"); c.number_format="yyyy-mm"
c=a.cell(row=r,column=3,value=f"=B{pr2}*0.1"); c.number_format=WON; r+=1
for k in range(1,7):
    a.cell(row=r,column=1,value=f"중도금 {k}")
    c=a.cell(row=r,column=2,value=f"=EDATE(B{cr},B{gr_}*{k})"); c.number_format="yyyy-mm"
    c=a.cell(row=r,column=3,value=f"=B{pr2}*0.1"); c.number_format=WON; r+=1
a.cell(row=r,column=1,value="잔금 30%+취득세"); c=a.cell(row=r,column=2,value=f"=B{mr}"); c.number_format="yyyy-mm"
c=a.cell(row=r,column=3,value=f"=B{pr2}*0.3+B{pr2}*B{tr}"); c.number_format=WON; pe=r; r+=2
R["pf_dates"]=f"가정!$B${ps_}:$B${pe}"; R["pf_amts"]=f"가정!$C${ps_}:$C${pe}"

hdr(r,"⑧ 중도금 대출 (선택)"); r+=1
inp(r,"mid_loan","중도금을 대출로 낼지 (1=예, 0=아니오)",0,None,"공고문: 대출 알선은 의무 아님 — GH 확인 필요"); r+=1
inp(r,"mid_rate","중도금 대출 금리 (이자 후불, 잔금 때 일괄 상환)",0.045,"0.0%","⚠️ 가정"); r+=1
r+=1
hdr(r,"⑨ 매매안 (청약 시나리오 4) · 청약 당첨 시 시세"); r+=1
inp(r,"buy_price","매수 가격 (84㎡)",1300000000,WON,"⚠️ 가정 — 진산푸르지오 호가 13.8~14.3억, 리치고 모델 12.6억(10/29) 사이"); r+=1
inp(r,"buy_month","매수·입주 월",dt.date(2027,2,1),"yyyy-mm","현 전세 만기와 동시"); r+=1
inp(r,"ltv","주담대 LTV",0.4,"0%","투기과열지구 무주택 40%(수지 2025-10·기흥 2026-07 지정)"); r+=1
inp(r,"loan_cap","주담대 한도",600000000,WON,"수도권 주담대 6억 상한(2025-06 대책) — 현행 확인 필요"); r+=1
inp(r,"mort_rate","주담대 금리",0.045,"0.0%","⚠️ 가정"); r+=1
inp(r,"mort_years","상환 기간 (년)",30,None,"원리금 균등"); r+=1
inp(r,"buy_cost","취득 부대비용 (취득세+중개 등)",0.038,"0.0%","취득세 약 3.3% + 중개·등기 약 0.5% — 추정"); r+=1
inp(r,"house_g","매수 주택 연 상승률",0.02,"0.0%","⚠️ 가정 — 보수적"); r+=1
inp(r,"gg_market","광교 84㎡ 시세 (잔금 이후 평가)",1500000000,WON,"⚠️ 가정 — 주변 84㎡ 14.8~19.3억 하단"); r+=1
inp(r,"pf_market","플랫폼시티 84㎡ 시세 (잔금 이후 평가)",1200000000,WON,"⚠️ 가정 — e편한세상 용인역 플랫폼시티 분양 12억(2023)"); r+=1

# ---------------- 월별 ----------------
m=wb.create_sheet("월별")
cols=["월","경과월","하이닉스 주가","급여 순저축","PS 현금(세후)","PS 자사주(주)","현재 보증금 반환","기타자산 현금화","청약통장 해지",
"회사대출 실행","임시거주 보증금 지급/반환","월세","회사대출 이자","청약 납입","중도금 대출 상환·이자","광교 세입자 보증금(+수령/−반환)",
"기금 이자","순 확정 지출(같은 달 확정 수입 차감)","향후 N개월 지출","현금(매도 전)","선확보 개월 N","T1 매도(주)","자동 매도(주)","매도 대금","현금(월말)",
"자유 보유 주수(월말)","주식 평가액","DC 누적","임시거주 보증금 보유","청약 납입 누계","대출 잔액(회사+중도금+기금+세입자)","순자산(DC 제외, 주택 시세 반영)","경고","매매 지출(구입·원리금)","매수 주택 평가액","주담대 잔액","청약 주택 시세 차익(잔금 후)"]
for j,h in enumerate(cols,1):
    c=m.cell(row=1,column=j,value=h); c.font=HDR; c.fill=HFILL; c.alignment=Alignment(wrap_text=True,vertical="center")
    m.column_dimensions[L(j)].width=14
m.column_dimensions["A"].width=10; m.column_dimensions["AG"].width=18; m.row_dimensions[1].height=48
m.freeze_panes="C2"
start=dt.date(2026,11,1); N=62; first=2; last=first+N-1
def mo(i):
    y=start.year+(start.month-1+i)//12; mm=(start.month-1+i)%12+1; return dt.date(y,mm,1)
A=R
for i in range(N):
    r=first+i; p=r-1
    D=f"$A{r}"
    m.cell(row=r,column=1,value=mo(i)).number_format="yyyy-mm"
    m[f"B{r}"]=i
    m[f"C{r}"]=f"={A['px0']}*(1+{A['g']})^(B{r}/12)"
    m[f"D{r}"]=f"={A['save_m']}"
    # PS: 지급 연도 Y+1 2월. 2026분(2027-02), 2027분(2028-02), 2028분(2029-02) + 이연 2회
    def ps_cash(key,yr):
        Gs=f"{A['salary']}*{A[key]}"
        now=f"(MONTH({D})=2)*(YEAR({D})={yr+1})*({Gs}*{A['ps_cash']}-{Gs}*{A['ps_now']}*{A['ps_dc']}-({Gs}*{A['ps_now']}-{Gs}*{A['ps_now']}*{A['ps_dc']})*{A['tax']})"
        d1=f"(MONTH({D})=2)*(YEAR({D})={yr+2})*(-{Gs}*0.1*{A['tax']})"
        d2=f"(MONTH({D})=2)*(YEAR({D})={yr+3})*(-{Gs}*0.1*{A['tax']})"
        return f"{now}+{d1}+{d2}"
    def ps_stock(key,yr):
        Gs=f"{A['salary']}*{A[key]}"
        stockpart=f"({A['ps_now']}-{A['ps_cash']})"
        return (f"(MONTH({D})=2)*(YEAR({D})={yr+1})*{Gs}*{stockpart}/C{r}"
                f"+(MONTH({D})=2)*(YEAR({D})={yr+2})*{Gs}*0.1/C{r}+(MONTH({D})=2)*(YEAR({D})={yr+3})*{Gs}*0.1/C{r}")
    m[f"E{r}"]="="+"+".join(ps_cash(k,y) for k,y in (("ps26",2026),("ps27",2027),("ps28",2028)))
    m[f"F{r}"]="=ROUNDDOWN("+"+".join(ps_stock(k,y) for k,y in (("ps26",2026),("ps27",2027),("ps28",2028)))+",0)"
    m[f"G{r}"]=f"=IF({D}={A['move_month']},{A['deposit_now']},0)"
    m[f"H{r}"]=f"=IF({D}={A['other_month']},{A['other0']},0)"
    # 청약통장: 당첨 시 계약 월에 해지
    m[f"I{r}"]=(f"=IF(AND({A['sel_sub']}=1,{D}=INDEX({A['gg_dates']},1)),{A['sub_acct']},0)"
                f"+IF(AND({A['sel_sub']}=2,{D}={A['pf_contract']}),{A['sub_acct']},0)")
    m[f"J{r}"]=f"=IF({D}={A['loan_month']},{A['loan_new']},0)-IF(AND({D}=AE${first},{D}>{A['loan_month']}),{A['loan_new']},0)"
    # 임시거주 종료 월: 광교=실입주, 플랫폼=입주, 낙첨=없음
    endm=f"IF({A['sel_sub']}=1,{A['gg_move']},IF({A['sel_sub']}=2,{A['pf_move']},DATE(2099,1,1)))"
    k_since=f"(YEAR({D})*12+MONTH({D})-YEAR({A['move_month']})*12-MONTH({A['move_month']}))"
    dep_t=f"{A['h_dep']}*(1+{A['renew_up']})^INT({k_since}/24)"
    m[f"K{r}"]=(f"=({A['sel_sub']}<>4)*(IF({D}={A['move_month']},-{A['h_dep']},0)"
                f"+IF(AND({D}>{A['move_month']},{D}<{endm},MOD({k_since},24)=0),-({dep_t}-{A['h_dep']}*(1+{A['renew_up']})^(INT({k_since}/24)-1)),0)"
                f"+IF({D}={endm},{A['h_dep']}*(1+{A['renew_up']})^INT(({k_since}-1)/24),0))")
    m[f"L{r}"]=f"=({A['sel_sub']}<>4)*IF(AND({D}>={A['move_month']},{D}<{endm}),-{A['h_rent']}*(1+{A['renew_up']})^INT({k_since}/24),0)"
    m[f"M{r}"]=f"=-({A['loan_old']}+IF(AND({D}>{A['loan_month']},{D}<={endm}),{A['loan_new']},0))*{A['loan_rate']}/12"
    sub_pay=(f"(IF({A['sel_sub']}=1,SUMIFS({A['gg_amts']},{A['gg_dates']},{D}),0)"
             f"+IF({A['sel_sub']}=2,SUMIFS({A['pf_amts']},{A['pf_dates']},{D}),0))")
    # 중도금(2~7번째 회차)만 대출로 대체 가능
    mid_gg=f"IF({A['sel_sub']}=1,SUMIFS({A['gg_amts']},{A['gg_dates']},{D})*({D}>INDEX({A['gg_dates']},1))*({D}<INDEX({A['gg_dates']},8)),0)"
    mid_pf=f"IF({A['sel_sub']}=2,SUMIFS({A['pf_amts']},{A['pf_dates']},{D})*({D}>INDEX({A['pf_dates']},1))*({D}<INDEX({A['pf_dates']},8)),0)"
    m[f"N{r}"]=f"=-({sub_pay}-{A['mid_loan']}*({mid_gg}+{mid_pf}))"
    # 중도금 대출 상환: 잔금 월에 원금+단리 이자
    jan=f"IF({A['sel_sub']}=1,INDEX({A['gg_dates']},8),IF({A['sel_sub']}=2,INDEX({A['pf_dates']},8),DATE(2099,1,1)))"
    dates_rng=f"IF({A['sel_sub']}=1,1,0)"
    m[f"O{r}"]=(f"=IF(AND({A['mid_loan']}=1,{D}={jan}),-("
                f"IF({A['sel_sub']}=1,SUMPRODUCT(({A['gg_dates']}>INDEX({A['gg_dates']},1))*({A['gg_dates']}<INDEX({A['gg_dates']},8))*{A['gg_amts']}*(1+{A['mid_rate']}*((YEAR({D})*12+MONTH({D}))-(YEAR({A['gg_dates']})*12+MONTH({A['gg_dates']})))/12)),0)"
                f"+IF({A['sel_sub']}=2,SUMPRODUCT(({A['pf_dates']}>INDEX({A['pf_dates']},1))*({A['pf_dates']}<INDEX({A['pf_dates']},8))*{A['pf_amts']}*(1+{A['mid_rate']}*((YEAR({D})*12+MONTH({D}))-(YEAR({A['pf_dates']})*12+MONTH({A['pf_dates']})))/12)),0)),0)")
    # 광교 세입자: 잔금 월 수령, 실입주 월 반환 (광교 당첨 + 전세 놓기)
    m[f"P{r}"]=(f"=IF(AND({A['sel_sub']}=1,{A['rent_out']}=1,{A['gg_move']}>{A['gg_jan']}),"
                f"IF({D}={A['gg_jan']},{A['tenant_dep']},0)-IF({D}={A['gg_move']},{A['tenant_dep']},0),0)")
    m[f"Q{r}"]=f"=IF(AND({A['sel_sub']}=1,{D}>{A['gg_jan']}),-{A['gg_fund']}*{A['fund_rate']}/12,0)"
    # 확정 지출(음수 항목 합, 양수는 제외) — 선확보 대상
    m[f"R{r}"]=f"=MAX(0,-(E{r}+G{r}+H{r}+I{r}+J{r}+K{r}+L{r}+M{r}+N{r}+O{r}+P{r}+Q{r}+AH{r}))"
    m[f"S{r}"]=f"=SUM(R{r+1}:R{min(r+18,last)})" if r<last else "=0"
    prev_cash=f"{A['cash0']}" if r==first else f"Y{p}"
    LN=f"MIN({A['buy_price']}*{A['ltv']},{A['loan_cap']})"
    PM=f"PMT({A['mort_rate']}/12,{A['mort_years']}*12,-{LN})"
    KB=f"(YEAR({D})*12+MONTH({D})-YEAR({A['buy_month']})*12-MONTH({A['buy_month']}))"
    m[f"AH{r}"]=(f"=IF({A['sel_sub']}=4,IF({D}={A['buy_month']},-({A['buy_price']}-{LN}+{A['buy_price']}*{A['buy_cost']}),0)"
                 f"-IF({D}>{A['buy_month']},{PM},0),0)")
    m[f"AI{r}"]=f"=IF(AND({A['sel_sub']}=4,{D}>={A['buy_month']}),{A['buy_price']}*(1+{A['house_g']})^({KB}/12),0)"
    m[f"AJ{r}"]=(f"=IF(AND({A['sel_sub']}=4,{D}>={A['buy_month']}),"
                 f"{LN}*(1+{A['mort_rate']}/12)^{KB}-{PM}*((1+{A['mort_rate']}/12)^{KB}-1)/({A['mort_rate']}/12),0)")
    m[f"AK{r}"]=(f"=IF(AND({A['sel_sub']}=1,{D}>={A['gg_jan']}),{A['gg_market']}-{A['gg_price']},0)"
                 f"+IF(AND({A['sel_sub']}=2,{D}>={A['pf_move']}),{A['pf_market']}-{A['pf_price']},0)")
    m[f"T{r}"]=f"={prev_cash}+D{r}+E{r}+G{r}+H{r}+I{r}+J{r}+K{r}+L{r}+M{r}+N{r}+O{r}+P{r}+Q{r}+AH{r}"
    m[f"U{r}"]=f"=IF(C{r}>={A['px_accel']},{A['n_accel']},IF(C{r}<{A['px_stop']},{A['n_stop']},{A['n_base']}))"
    prev_sh=f"{A['shares0']}" if r==first else f"Z{p}"
    m[f"V{r}"]=f"=IF({D}={A['t1_month']},MIN({A['t1_qty']},{prev_sh}),0)"
    # 향후 U개월 지출: S열은 18개월 고정 합이라 U개월로 다시 계산
    fwd=f"SUM(R{r+1}:INDEX(R:R,MIN(ROW()+U{r},{last})))" if r<last else "0"
    m[f"S{r}"]=f"={fwd}"
    rel=f"IF({D}={A['lock_month']},{A['lock_qty']},0)"
    avail=f"({prev_sh}+F{r}+{rel}-V{r})"
    need=f"MAX(0,MAX({A['min_cash']},S{r})-(T{r}+V{r}*C{r}))"
    m[f"W{r}"]=f"=MIN({avail},ROUNDUP({need}/C{r},0))"
    m[f"X{r}"]=f"=(V{r}+W{r})*C{r}"
    m[f"Y{r}"]=f"=T{r}+X{r}"
    m[f"Z{r}"]=f"={prev_sh}+F{r}+{rel}-V{r}-W{r}"
    m[f"AA{r}"]=f"=Z{r}*C{r}"
    prev_dc="0" if r==first else f"AB{p}"
    m[f"AB{r}"]=(f"={prev_dc}+(MONTH({D})=2)*(YEAR({D})=2027)*{A['salary']}*{A['ps26']}*{A['ps_now']}*{A['ps_dc']}"
                 f"+(MONTH({D})=2)*(YEAR({D})=2028)*{A['salary']}*{A['ps27']}*{A['ps_now']}*{A['ps_dc']}"
                 f"+(MONTH({D})=2)*(YEAR({D})=2029)*{A['salary']}*{A['ps28']}*{A['ps_now']}*{A['ps_dc']}")
    prev_hd=f"{A['deposit_now']}" if r==first else f"AC{p}"
    m[f"AC{r}"]=f"={prev_hd}-G{r}-K{r}"
    prev_paid="0" if r==first else f"AD{p}"
    paid_add=(f"IF({A['sel_sub']}=1,SUMIFS({A['gg_amts']},{A['gg_dates']},{D}),0)+IF({A['sel_sub']}=2,SUMIFS({A['pf_amts']},{A['pf_dates']},{D}),0)"
              f"+IF(AND({A['sel_sub']}=1,{D}={A['gg_jan']}),{A['gg_fund']},0)")
    m[f"AD{r}"]=f"={prev_paid}+{paid_add}"
    prev_mid="0" if r==first else f"AH{p}"
    # 대출 잔액: 회사(기존+추가) + 중도금 대출 원금 누계 + 기금 + 세입자 보증금
    m[f"AE{r}"]=(f"={A['loan_old']}+IF(AND({D}>={A['loan_month']},{D}<{endm}),{A['loan_new']},0)"
                 f"+{A['mid_loan']}*(IF({A['sel_sub']}=1,SUMPRODUCT(({A['gg_dates']}>INDEX({A['gg_dates']},1))*({A['gg_dates']}<INDEX({A['gg_dates']},8))*({A['gg_dates']}<={D})*{A['gg_amts']}),0)"
                 f"+IF({A['sel_sub']}=2,SUMPRODUCT(({A['pf_dates']}>INDEX({A['pf_dates']},1))*({A['pf_dates']}<INDEX({A['pf_dates']},8))*({A['pf_dates']}<={D})*{A['pf_amts']}),0))*({D}<{jan})"
                 f"+IF(AND({A['sel_sub']}=1,{D}>={A['gg_jan']}),{A['gg_fund']},0)"
                 f"+IF(AND({A['sel_sub']}=1,{A['rent_out']}=1,{D}>={A['gg_jan']},{D}<{A['gg_move']}),{A['tenant_dep']},0)")
    m[f"AF{r}"]=f"=Y{r}+AA{r}+AC{r}+AD{r}-AE{r}+IF({D}<{A['other_month']},{A['other0']},0)+IF({D}<{A['lock_month']},{A['lock_qty']}*C{r},0)+AI{r}-AJ{r}+AK{r}"
    m[f"AG{r}"]=f'=IF(Y{r}<0,"현금 부족",IF(Y{r}<{A["min_cash"]},"최소현금 미달",""))'
    for col in list(range(3,33))+[34,35,36,37]:
        cell=m.cell(row=r,column=col)
        if col in (6,21,22,23,26): cell.number_format="#,##0"
        else: cell.number_format=WON
        cell.font=BLK
    m.cell(row=r,column=2).number_format="0"
# 회사대출 상환: J열 수식에 반영(임시거주 종료 월) — 재작성
for i in range(N):
    r=first+i; D=f"$A{r}"
    endm=f"IF({A['sel_sub']}=1,{A['gg_move']},IF({A['sel_sub']}=2,{A['pf_move']},DATE(2099,1,1)))"
    m[f"J{r}"]=f"=IF({D}={A['loan_month']},{A['loan_new']},0)-IF({D}={endm},{A['loan_new']},0)"

# ---------------- 요약 ----------------
s=wb.create_sheet("요약",1)
s.column_dimensions["A"].width=40; s.column_dimensions["B"].width=22; s.column_dimensions["C"].width=50
rng=lambda c: f"월별!${c}${first}:${c}${last}"
rows=[("선택: 임시 거주",f"={A['h_name']}",""),
("선택: 청약",f'=CHOOSE({A["sel_sub"]},"광교 당첨","광교 낙첨→플랫폼시티 당첨","둘 다 낙첨","매매(2027-02)")',""),
("선택: 주가",f"=INDEX(가정!$D${px_top}:$D${px_top+2},{A['sel_px']})",""),
("최저 월말 현금",f"=MIN({rng('Y')})","0 미만이면 계획이 깨진다"),
("최저 현금 월",f"=INDEX({rng('A')},MATCH(MIN({rng('Y')}),{rng('Y')},0))",""),
("현금 부족 개월 수",f'=COUNTIF({rng("Y")},"<0")',""),
("T1 매도 주수 합계",f"=SUM({rng('V')})",""),
("자동 매도 주수 합계",f"=SUM({rng('W')})",""),
("PS 자사주 수령 주수 합계",f"=SUM({rng('F')})",""),
("2031-12 자유 보유 주수",f"=INDEX({rng('Z')},{N})",""),
("2031-12 하이닉스 주가",f"=INDEX({rng('C')},{N})",""),
("2031-12 현금",f"=INDEX({rng('Y')},{N})",""),
("2031-12 순자산 (DC 제외, 주택 시세 반영)",f"=INDEX({rng('AF')},{N})",""),
("2031-12 DC 누적 (PS 적립분)",f"=INDEX({rng('AB')},{N})",""),
("월세 총지출",f"=-SUM({rng('L')})",""),
("판정",f'=IF(MIN({rng("Y")})<0,"❌ 자금 부족 — 대출·매도·거주 선택 조정 필요","✅ 계획대로 가능")',"")]
s.cell(row=1,column=1,value="요약 — 현재 '가정' 선택 기준").font=BOLD
for i,(k,f,n) in enumerate(rows,3):
    s.cell(row=i,column=1,value=k).font=BLK
    c=s.cell(row=i,column=2,value=f); c.font=GRN
    if "주수" in k or "개월" in k: c.number_format="#,##0"
    elif "월" == k[-1] : c.number_format="yyyy-mm"
    elif "판정" in k or "선택" in k: pass
    else: c.number_format=WON
    if k=="최저 현금 월": c.number_format="yyyy-mm"
    s.cell(row=i,column=3,value=n).font=Font(name=F,italic=True,color="595959")
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if c.font and c.font.name!=F: c.font=Font(name=F,bold=c.font.bold,color=c.font.color,italic=c.font.italic)
wb.save("/home/user/Repo_name/report/housing/housing-cashflow-plan-2026-10-31.xlsx")
import json; json.dump({"first":first,"last":last,"R":R},open("/tmp/claude-0/plan_meta.json","w"),ensure_ascii=False)
print("ok", first, last)

# ---------------- 전략 ----------------
wb=load_workbook_reopen=None
from openpyxl import load_workbook
wb=load_workbook("/home/user/Repo_name/report/housing/housing-cashflow-plan-2026-10-31.xlsx")
t=wb.create_sheet("전략")
t.column_dimensions["A"].width=26; t.column_dimensions["B"].width=110
rows=[("전략 — 하이닉스 매도·PS·청약 대응 (Claude 의견, 공식 신호는 판단 엔진, 결정은 사용자 · 2026-10-31)",None),
("",""),
("원칙","날짜가 있는 돈은 미리 확보한다. 하이닉스는 '언제 팔까'가 아니라 '다음 N개월 지출을 현금으로 들고 있는가'로 판다(월별 시트 W열 자동 매도)."),
("주가 구간별 행동","① 주가 ≥ 2,000,000원: 다음 12개월 지출 선확보 + 남는 몫 분산(비만치료제·리츠·인도·금) — 사용자 10/31 선호"),
("","② 2,000,000원 미만: 그 달 필요한 만큼만 매도(선확보 1개월). 단점: 주가가 계속 빠지면 더 싼 값에 더 많이 판다 — 비관 시나리오 비교 참고"),
("","③ 1,341,000원 미만(⑫ S3): 플레이북은 18개월 선확보를 권함 — 현재 엑셀은 사용자 선호대로 1개월, 이 구간에 들어가면 재검토"),
("T1 (기존 계획)","13주는 늦어도 11/3 장 마감(선거 전), 연기분 12주는 11/13까지 — 정규장 종가 1,403,920원 미만 또는 1,341,000원 미만이면 다음 거래일 매도. 모델은 2026-11에 25주로 반영."),
("광교 접수(11/10) 전","GH에 중도금 대출 알선 여부·이자 방식 확인. 모델상 대출 없이도 기준 시나리오는 가능하나, 비관(주가 연 −20%)에서는 여유가 얇다 — '시나리오비교' 시트 확인."),
("계약금(2026-12)","CMA + 청약통장 해지 + T1 매도 대금으로 충당. 이를 위해 T1 대금은 CMA에 그대로 둔다."),
("PS 자사주(2027-02)","받는 즉시 다음 6개월 중도금분(2027-05, 2027-10)에 해당하는 만큼 매도 — 세금은 이미 현금 몫에서 빠졌으므로 주식은 순수 재원. 나머지는 주가 구간 규칙에 따름."),
("2027년분 PS(2028-02)","가정 시트 ps27(기본 3.0배)을 실적에 맞춰 갱신. 커지면 중도금 대출 필요성이 사라지고 분산 재원이 생긴다."),
("임시 거주","보증금이 낮을수록(성원상떼빌 5.2억) 하이닉스를 덜 판다. 하이브엘 전세 8억은 전대차·HUG 불가·하루 전출(청약 거주기간 단절 위험)로 비권장, 하이브엘 월세는 월 200~300만이 2031년까지 누적 — 비교 시트의 '월세 총지출' 참고."),
("광교 2029-10~2031-02","전세를 놓으면 잔금을 세입자 보증금으로 내고, 2031-02 임시 거주 보증금을 돌려받아 세입자에게 돌려준다. 세입자 2년 보장(→2031-10) 충돌 위험 — 계약 시 전문가 확인."),
("집중도 목표(의견)","2031년까지 하이닉스 비중을 금융자산의 50% 이하로. PS 자사주가 계속 들어오므로 '받는 만큼 일부는 판다'가 기본값."),
("점검 주기","매월 1일: 월별 시트 실제 현금·주수 확인. 분기마다: 주가 시나리오·PS 배수·플랫폼시티 공고 여부 갱신. 공고가 뜨면 ⑦ 표를 실제 값으로 교체.")]
for i,(k,v) in enumerate(rows,1):
    c=t.cell(row=i,column=1,value=k); c.font=Font(name=F,bold=True)
    if v is not None:
        c2=t.cell(row=i,column=2,value=v); c2.font=Font(name=F); c2.alignment=Alignment(wrap_text=True,vertical="top")
wb.save("/home/user/Repo_name/report/housing/housing-cashflow-plan-2026-10-31.xlsx")
print("strategy ok")
