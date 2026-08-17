"""2026-08-17 임시 프로브 — customs-preliminary-probe.yml 전용, 확인되면
customs-preliminary-probe.yml과 함께 삭제. 관세청 보도자료 목록/상세
페이지가 GitHub Actions 러너에서 실제로 접근되는지, HTML 구조가 어떤지
확인한다(이 세션 WebFetch는 customs.go.kr이 egress 차단이라 직접 못 봄)."""
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}


def probe(label, url):
    print(f"=== {label}: {url} ===")
    try:
        r = requests.get(url, timeout=15, headers=HEADERS)
        print("status:", r.status_code)
        print("length:", len(r.text))
        print("--- first 4000 chars ---")
        print(r.text[:4000])
    except Exception as e:
        print("ERROR:", type(e).__name__, e)
    print()


probe("목록 페이지", "https://www.customs.go.kr/kcs/na/ntt/selectNttList.do?bbsId=1362&mi=2891")
probe("상세 페이지(8월 1~10일 잠정치)",
      "https://www.customs.go.kr/kcs/na/ntt/selectNttInfo.do?mi=2891&bbsId=1362&nttSn=10172763")
