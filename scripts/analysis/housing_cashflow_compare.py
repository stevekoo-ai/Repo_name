import json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
F="Arial"; d=json.load(open("/tmp/claude-0/scen.json"))
P="report/housing/housing-cashflow-plan-2026-10-31.xlsx"
wb=load_workbook(P)
if "시나리오비교" in wb.sheetnames: del wb["시나리오비교"]
s=wb.create_sheet("시나리오비교",2)
s["A1"]="시나리오 비교 — 66개 조합(임시 거주 7×청약 3×주가 3 + 매매 3) 스냅샷 (2026-10-31 가정 기준, 값 고정: 가정을 바꾸면 이 표는 갱신되지 않음. 현재 선택 조합은 '요약' 시트가 실시간)"; s["A1"].font=Font(name=F,bold=True)
s["A2"]="가정: 월 순저축 0, 2027분 PS 3.0배, 2028분 0, 광교 전세 놓기 6억, 중도금 대출 안 함, 하나 67주 2027-02 해제, 매도 규칙 200만 미만 1개월·이상 12개월, 매매 13억·LTV 40%·4.5%·집값 연 2%, 광교 시세 15억·플랫폼 12억, 주가 비관 연−20%·기준 0%·낙관 +20%. 매도 주수 = T1 25주 + 자동 매도(PS 자사주 포함)."; s["A2"].font=Font(name=F,italic=True,color="595959")
hd=["임시 거주","청약","주가","최저 월말 현금(원)","최저 현금 월","하이닉스 매도 주수(T1+자동)","PS 자사주 수령 주수","2031-12 자유 보유 주수","2031-12 순자산(원, DC 제외)","2031-12 DC 누적(원)","월세 총지출(원)","판정"]
for j,h in enumerate(hd,1):
    c=s.cell(row=4,column=j,value=h); c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=PatternFill("solid",fgColor="1F4E78"); c.alignment=Alignment(wrap_text=True)
for i,r in enumerate(d,5):
    v=r[3:]; row=[v[0],v[1],v[2],v[3],str(v[4])[:7],v[6]+v[7],v[8],v[9],v[12],v[13],v[14],v[15]]
    for j,x in enumerate(row,1):
        c=s.cell(row=i,column=j,value=x); c.font=Font(name=F)
        if j in (4,9,10,11): c.number_format='#,##0;(#,##0);"-"'
        if j in (6,7,8): c.number_format="#,##0"
for j,w in enumerate([34,26,8,18,12,16,14,16,20,16,16,26],1): s.column_dimensions[chr(64+j)].width=w
s.freeze_panes="A5"; s.auto_filter.ref=f"A4:L{4+len(d)}"; # 확률 가중 시트
if "확률가중" in wb.sheetnames: del wb["확률가중"]
q=wb.create_sheet("확률가중",3)
q["A1"]="확률 가중 비교 — 2031-12 순자산 기댓값(DC 제외, 주택 시세 반영). 파란 칸 확률을 바꾸면 다시 계산된다."; q["A1"].font=Font(name=F,bold=True)
q["A3"]="광교 당첨 확률"; q["B3"]=0.22; q["C3"]="경기 풀 15~20% + 기타 약 5% (커트라인 표본 2026-10-31)"
q["A4"]="플랫폼시티 당첨 확률"; q["B4"]=0.45; q["C4"]="용인 당해 풀 표본 추정 약 45%(30~60%)"
for c in ("B3","B4"): q[c].font=Font(name=F,color="0000FF"); q[c].number_format="0%"; q[c].fill=PatternFill("solid",fgColor="FFFF00")
hd2=["임시 거주","주가","A. 광교 넣음 (광교→플랫폼→낙첨)","B. 광교 안 넣음 (플랫폼→낙첨)","C. 매매 (2027-02)","A 최악(둘 다 낙첨)","최고 기댓값"]
for j,h in enumerate(hd2,1):
    c=q.cell(row=6,column=j,value=h); c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=PatternFill("solid",fgColor="1F4E78"); c.alignment=Alignment(wrap_text=True)
names=[]; [names.append(r[3]) for r in d if r[4]=="광교 당첨" and r[3] not in names]
rng=lambda col: f"시나리오비교!${col}$5:${col}${4+len(d)}"
NW=lambda h,sub,px: f'SUMIFS({rng("I")},{rng("A")},{h},{rng("B")},"{sub}",{rng("C")},{px})'
rr=7
for nm in names:
    for px in ("비관","기준","낙관"):
        q.cell(row=rr,column=1,value=nm).font=Font(name=F); q.cell(row=rr,column=2,value=px).font=Font(name=F)
        hc=f"$A{rr}"; pc=f"$B{rr}"
        g1=NW(hc,"광교 당첨",pc); g2=NW(hc,"광교 낙첨→플랫폼시티 당첨",pc); g3=NW(hc,"둘 다 낙첨",pc)
        q.cell(row=rr,column=3,value=f"=$B$3*{g1}+(1-$B$3)*($B$4*{g2}+(1-$B$4)*{g3})")
        q.cell(row=rr,column=4,value=f"=$B$4*{g2}+(1-$B$4)*{g3}")
        q.cell(row=rr,column=5,value=f'=SUMIFS({rng("I")},{rng("B")},"매매(2027-02)",{rng("C")},{pc})')
        q.cell(row=rr,column=6,value=f"={g3}")
        q.cell(row=rr,column=7,value=f'=INDEX($C$6:$E$6,MATCH(MAX(C{rr}:E{rr}),C{rr}:E{rr},0))')
        for col in (3,4,5,6): q.cell(row=rr,column=col).number_format='#,##0;(#,##0);"-"'; q.cell(row=rr,column=col).font=Font(name=F)
        rr+=1
for j,w in enumerate([34,8,22,22,20,20,30],1): q.column_dimensions[chr(64+j)].width=w
q.cell(row=rr+1,column=1,value="주의: 기댓값은 평균이다. A·B는 낙첨 시 2031년까지 무주택(최악 열). 매매는 청약 기회를 포기하는 대신 결과가 확정적이다. 시나리오비교 시트 값은 작성 시점 스냅샷.").font=Font(name=F,italic=True,color="595959")
wb.save(P)
