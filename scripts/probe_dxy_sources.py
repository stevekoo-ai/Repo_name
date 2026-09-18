#!/usr/bin/env python3
"""DXY(ICE 달러지수) 대체 소스 프로브 — **일회성 조사 도구**.

## 왜 이게 필요한가 (2026-09-18)

FRED `DTWEXBGS`(달러지수 광의)는 연준 H.10 원천 자체가 며칠 늦게 나온다
— 2026-09-18 실측으로 `fetched_at=9/18`인데 `date=9/11`(7일 지연)을
확인했다(수집 실패 아님, GitHub Actions job 로그로 대조 완료).

매일 나오는 대안은 **ICE US Dollar Index(DXY)** 인데, 이건 6개 통화만
가중평균하는 **다른 바스켓**이라 DTWEXBGS의 대체가 아니라 **참고용
병기 지표**로만 쓴다(같은 값인 척 바꿔치기하면 이 저장소가 반복해서
겪은 "다른 정의를 같은 값으로 쓴 사고"를 되풀이한다).

## 왜 프로브가 따로 필요한가

개발 샌드박스의 egress 프록시가 stooq.com·finance.yahoo.com을 둘 다
`connect_rejected`로 막는다(kosis.kr·api.bls.gov·imf.org와 같은 상황).
**로컬에서 되는지 안 되는지 자체를 알 수 없으므로**, 실제 운영 환경인
GitHub Actions에서 이 스크립트를 돌려 어떤 소스/심볼이 살아있는지
실측한 뒤에 수집기를 확정한다 — 추측으로 코드를 쓰지 않는다.

## 확정 후

소스가 정해지면 이 스크립트는 삭제하고 `scripts/macro_data.py`의
프리셋/프로바이더로 흡수한다. 이 파일이 저장소에 남아 있다면 아직
확정 전이라는 뜻이다.

    python3 scripts/probe_dxy_sources.py
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

TIMEOUT = 20
UA = {"User-Agent": "Mozilla/5.0 (compatible; peos-agent/1.0; +https://github.com)"}

# stooq: 무인증 CSV. 심볼 표기가 문서화돼 있지 않아 후보를 전부 던져본다.
STOOQ_CANDIDATES = ["dx.f", "^dxy", "dxy", "dx_f", "usdidx"]

# yahoo chart API: 무인증 JSON. DX-Y.NYB(ICE DXY 현물), DX=F(선물).
YAHOO_CANDIDATES = ["DX-Y.NYB", "DX=F"]


def _get(url: str) -> tuple[int, bytes, str]:
    """(status, body, error). 예외를 삼키고 구조화해서 돌려준다 —
    프로브의 목적은 '실패했다'가 아니라 '어떻게 실패했다'를 남기는 것."""
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read(), ""
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:500], f"HTTPError {e.code}"
    except Exception as e:  # noqa: BLE001 — 프로브라 모든 실패를 기록해야 한다
        return 0, b"", f"{type(e).__name__}: {e}"


def probe_stooq(symbol: str) -> dict:
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
    status, body, err = _get(url)
    text = body.decode("utf-8", errors="replace")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    out = {
        "source": "stooq", "symbol": symbol, "url": url,
        "status": status, "error": err, "rows": len(lines),
        "header": lines[0] if lines else "",
        "last_lines": lines[-3:] if len(lines) > 1 else [],
    }
    # stooq는 없는 심볼에도 200 + "No data" 한 줄을 돌려주므로 본문으로 판정한다
    out["usable"] = bool(status == 200 and len(lines) > 5 and "," in (lines[0] if lines else ""))
    return out


def probe_yahoo(symbol: str) -> dict:
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
           f"?range=10d&interval=1d")
    status, body, err = _get(url)
    out = {"source": "yahoo", "symbol": symbol, "url": url,
           "status": status, "error": err, "rows": 0, "last_lines": []}
    if status == 200:
        try:
            data = json.loads(body)
            result = (data.get("chart") or {}).get("result") or []
            if result:
                ts = result[0].get("timestamp") or []
                quote = (result[0].get("indicators") or {}).get("quote") or [{}]
                closes = quote[0].get("close") or []
                out["rows"] = len(ts)
                out["last_lines"] = [
                    f"{t} close={c}" for t, c in list(zip(ts, closes))[-3:]
                ]
        except Exception as e:  # noqa: BLE001
            out["error"] = f"parse: {type(e).__name__}: {e}"
    out["usable"] = out["rows"] > 5
    return out


def main() -> int:
    results = []
    for s in STOOQ_CANDIDATES:
        results.append(probe_stooq(s))
    for s in YAHOO_CANDIDATES:
        results.append(probe_yahoo(s))

    print("=" * 72)
    print("DXY 대체 소스 프로브 결과")
    print("=" * 72)
    for r in results:
        mark = "✅ 사용가능" if r["usable"] else "❌"
        print(f"\n{mark} [{r['source']}] {r['symbol']}")
        print(f"   url    : {r['url']}")
        print(f"   status : {r['status']}  rows={r['rows']}  err={r['error'] or '-'}")
        if r.get("header"):
            print(f"   header : {r['header']}")
        for ln in r["last_lines"]:
            print(f"   last   : {ln}")

    usable = [r for r in results if r["usable"]]
    print("\n" + "=" * 72)
    if usable:
        print(f"사용 가능한 소스 {len(usable)}개: "
              + ", ".join(f"{r['source']}:{r['symbol']}" for r in usable))
    else:
        print("사용 가능한 소스 없음 — 이 환경에서도 전부 막혔다. "
              "다른 경로(예: 기존 KIS API의 해외지수 TR)를 검토해야 한다.")
    print("=" * 72)
    # 프로브는 '조사'라 소스가 없어도 실패로 보지 않는다(로그만 남긴다).
    return 0


if __name__ == "__main__":
    sys.exit(main())
