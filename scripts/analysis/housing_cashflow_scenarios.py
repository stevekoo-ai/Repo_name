import json, shutil, subprocess, os
from openpyxl import load_workbook
SRC="report/housing/housing-cashflow-plan-2026-10-31.xlsx"
REC="/root/.claude/skills/synced/9fa28180-9b71-441c-a36e-3766c0c75677_580680f8-4590-415f-b1f5-65c0ef4692fc/xlsx/scripts/recalc.py"
meta=json.load(open("/tmp/claude-0/plan_meta.json")); R=meta["R"]
cell=lambda k:R[k].split("!")[1].replace("$","")
tmp="/tmp/claude-0/scen_tmp.xlsx"
out=[]
for h,sub,px in [(h,sub,px) for h in range(1,8) for sub in (1,2,3) for px in (1,2,3)]+[(1,4,px) for px in (1,2,3)]:
  if True:
    if True:
      wb=load_workbook(SRC); a=wb["가정"]
      a[cell("sel_house")]=h; a[cell("sel_sub")]=sub; a[cell("sel_px")]=px
      wb.save(tmp)
      subprocess.run(["python3",REC,tmp,"60"],capture_output=True)
      v=load_workbook(tmp,data_only=True)["요약"]
      vals=[r[1] for r in v.iter_rows(min_row=3,values_only=True)]
      out.append([h,sub,px]+vals)
json.dump(out,open("/tmp/claude-0/scen.json","w"),ensure_ascii=False,default=str)
print(len(out))
