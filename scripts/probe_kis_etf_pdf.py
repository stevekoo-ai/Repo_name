#!/usr/bin/env python3
"""[일회성 조사 도구 — 확인 후 삭제] KIS로 병목 섹터 ETF PDF(구성종목·비중)를
받을 수 있는지 실측한다.

확인할 것 (2026-09-24 사용자 요청: "관련 ETF를 수집하고 그 ETF의 PDF 중 가장
포션이 큰 대장주가 다 같은 주식을 지목하는지, 어떤 리스트의 회사들이 대장주
후보인지, 순위 바뀜이 있는지 확인 가능한지 검토"):
  1. 종목 마스터(kospi_code.mst)에서 ETF를 가려내고 이름으로 섹터 ETF를 찾을 수 있나
  2. 테마 마스터(theme_code.mst)에 전력·광·메모리 테마와 편입 종목이 있나
  3. TR FHKST121600C0(ETF 구성종목시세) output2에 비중(etf_cnfg_issu_rlim)이
     실제로 의미대로 들어오나, 몇 종목까지 오나, 해외 구성종목은 어떻게 오나
"""
from __future__ import annotations

import io
import json
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import investor_flow as IF  # noqa: E402

MASTER = "https://new.real.download.dws.co.kr/common/master/{}.mst.zip"
ETF_KEYWORDS = ["전력", "그리드", "전기", "원자력", "원전", "변압", "인프라",
                "반도체", "메모리", "HBM", "데이터센터", "광통신", "통신"]
THEME_KEYWORDS = ["전력", "변압", "전선", "원전", "원자력", "광통신", "광케이블",
                  "메모리", "낸드", "NAND", "HBM", "반도체", "데이터센터", "SSD"]
PDF_TARGET_KEYWORDS = ["전력", "그리드", "메모리", "HBM", "광통신"]
MAX_PDF_CALLS = 14


def _download(name: str) -> list[str]:
    with urllib.request.urlopen(MASTER.format(name), timeout=60) as r:
        z = zipfile.ZipFile(io.BytesIO(r.read()))
    raw = z.read(z.namelist()[0])
    return raw.decode("cp949", errors="replace").splitlines()


def parse_equity_master(lines: list[str], tail: int) -> list[dict]:
    out = []
    for row in lines:
        if len(row) <= tail:
            continue
        head, part2 = row[:len(row) - tail], row[-tail:]
        out.append({"code": head[0:9].strip(), "name": head[21:].strip(), "group": part2[0:2]})
    return out


def kis_pdf(code: str) -> dict:
    token = IF.kis_get_token("real")
    host = IF.KIS_HOSTS["real"]
    req = urllib.request.Request(
        f"{host}/uapi/etfetn/v1/quotations/inquire-component-stock-price"
        f"?FID_COND_MRKT_DIV_CODE=J&FID_INPUT_ISCD={code}&FID_COND_SCR_DIV_CODE=11216",
        headers={"content-type": "application/json; charset=utf-8",
                 "authorization": f"Bearer {token}",
                 "appkey": IF._get_env_or_die("KIS_APP_KEY"),
                 "appsecret": IF._get_env_or_die("KIS_APP_SECRET"),
                 "tr_id": "FHKST121600C0", "custtype": "P"})
    with urllib.request.urlopen(req, timeout=IF.KIS_HTTP_TIMEOUT_S) as r:
        return json.loads(r.read())


def main() -> None:
    print("## 1. 종목 마스터 — ETF 식별·섹터 ETF 목록")
    kospi = parse_equity_master(_download("kospi_code"), 228)
    kosdaq = parse_equity_master(_download("kosdaq_code"), 222)
    names = {r["code"]: r["name"] for r in kospi + kosdaq}
    groups: dict[str, int] = {}
    for r in kospi:
        groups[r["group"]] = groups.get(r["group"], 0) + 1
    print(f"코스피 {len(kospi)}행 / 코스닥 {len(kosdaq)}행, 코스피 그룹코드 분포: {groups}")
    etfs = [r for r in kospi if r["group"] == "EF"]
    print(f"그룹코드 EF(ETF 추정) {len(etfs)}개 — 예시 5개: {[(r['code'], r['name']) for r in etfs[:5]]}")
    sector_etfs = [r for r in etfs if any(k in r["name"] for k in ETF_KEYWORDS)]
    print(f"\n섹터 키워드 ETF {len(sector_etfs)}개:")
    for r in sector_etfs:
        print(f"- {r['code']} {r['name']}")

    print("\n## 2. 테마 마스터 — 섹터 테마와 편입 종목")
    themes: dict[tuple[str, str], list[str]] = {}
    tlines = _download("theme_code")
    print(f"원본 예시 3줄: {[repr(l) for l in tlines[:3]]}")
    for row in tlines:
        tcode, tname, jcode = row[0:3], row[3:-10].strip(), row[-10:].strip()
        themes.setdefault((tcode, tname), []).append(jcode)
    print(f"테마 총 {len(themes)}개")
    for (tc, tn), members in sorted(themes.items()):
        if any(k in tn for k in THEME_KEYWORDS):
            shown = ", ".join(f"{names.get(m.lstrip('A'), names.get(m, '?'))}({m})" for m in members[:25])
            print(f"- [{tc}] {tn} — {len(members)}종목: {shown}")

    print("\n## 3. ETF PDF(구성종목·비중) 실호출 — TR FHKST121600C0")
    targets = [r for r in sector_etfs if any(k in r["name"] for k in PDF_TARGET_KEYWORDS)][:MAX_PDF_CALLS]
    for i, r in enumerate(targets):
        try:
            data = kis_pdf(r["code"])
        except Exception as e:  # noqa: BLE001 — 진단 도구: 실패도 결과다
            print(f"\n### {r['code']} {r['name']} — 호출 실패 {type(e).__name__}: {e}")
            continue
        o1, o2 = data.get("output1") or {}, data.get("output2") or []
        print(f"\n### {r['code']} {r['name']} — rt_cd={data.get('rt_cd')} msg={data.get('msg1')}")
        if i == 0:
            print(f"output1 키: {sorted(o1)}")
            print(f"output1 값: {json.dumps(o1, ensure_ascii=False)}")
            if o2:
                print(f"output2[0] 전체: {json.dumps(o2[0], ensure_ascii=False)}")
        print(f"output2 {len(o2)}행, 구성종목수(etf_cnfg_issu_cnt)={o1.get('etf_cnfg_issu_cnt')}")
        rows = sorted(o2, key=lambda x: float(x.get("etf_cnfg_issu_rlim") or 0), reverse=True)
        total = sum(float(x.get("etf_cnfg_issu_rlim") or 0) for x in o2)
        print(f"비중 합계 {total:.2f} — 상위 10:")
        for x in rows[:10]:
            print(f"  {x.get('stck_shrn_iscd')} {x.get('hts_kor_isnm')} 비중={x.get('etf_cnfg_issu_rlim')} "
                  f"평가금액={x.get('etf_vltn_amt')}")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
