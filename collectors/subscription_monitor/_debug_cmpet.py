"""throwaway: 청약홈 광교 A17BL 공공분양(2026000528) 1순위 경쟁률 공식 조회."""
import re, urllib.request
from playwright.sync_api import sync_playwright
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
for u in ["https://www.applyhome.co.kr/ai/aia/selectAPTCompetitionPopup.do?houseManageNo=2026000528&pblancNo=2026000528",
          "https://www.applyhome.co.kr/ai/aia/selectAPTCompetitionPopup.do?houseManageNo=2026000528&pblancNo=2026000528&houseSecd=01"]:
    try:
        b=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=25).read().decode("utf-8","replace")
        t=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",b))
        print("### URL",u,"len",len(b)); i=t.find("084"); print(t[max(0,i-300):i+3000] if i>=0 else t[:1500])
    except Exception as e: print("### URL ERR",u,e)
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(user_agent=UA,locale="ko-KR")
    pg.goto("https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancListView.do",wait_until="networkidle",timeout=60000)
    row=pg.locator('tr[data-hmno="2026000528"]').first
    print("### row:",row.inner_text()[:300].replace("\n"," "))
    btn=row.locator("text=경쟁률").first
    try:
        with pg.context.expect_page(timeout=8000) as np_: btn.click()
        q=np_.value; q.wait_for_load_state("networkidle"); txt=q.inner_text("body"); print("### popup page url",q.url)
    except Exception as e:
        print("### no new page:",type(e).__name__); pg.wait_for_timeout(4000); txt=pg.inner_text("body")
    i=txt.find("084"); print("### TEXT"); print(txt[max(0,i-500):i+4000] if i>=0 else txt[-3000:])
    br.close()
