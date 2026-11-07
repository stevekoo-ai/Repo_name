---
name: steves-wiki-navigator
description: Steve's Wiki(stevekoo-ai/Repo_name) 저장소 온보딩과 길찾기. 이 저장소에서 처음 작업을 시작할 때, 무엇이 어디에 있는지·무엇이 자동으로 도는지·어떤 규칙을 지켜야 하는지·사용자가 지금 무엇을 진행 중인지 알아야 할 때 사용한다. "위키 구조", "어디에 저장돼 있어", "자동화 뭐 돌아", "새 터미널", "온보딩", "저장소 지도" 같은 요청이나, SK하이닉스·거시·주거·청약 관련 위키 질문을 받았는데 저장소 맥락이 없을 때 먼저 불러온다.
---

# Steve's Wiki 길잡이

이 스킬은 저장소 전체 지도를 대신하지 않는다. **단일 출처는 저장소 안의 `wiki/architecture/repository-map.md`다.** 이 스킬은 그 문서를 찾아 읽고, 핵심 규칙을 놓치지 않게 하는 순서를 정한다.

## 1. 저장소 확보

1. 작업 폴더에 `CLAUDE.md`와 `wiki/`가 있는지 확인한다.
   - **클라우드 세션:** 보통 `/home/user/Repo_name`
   - **PC:** 사용자가 clone한 폴더
2. 없으면 GitHub `stevekoo-ai/Repo_name`을 clone한다.
3. **항상 main에서 작업한다.**
   ```bash
   git checkout main && git pull --rebase origin main
   ```
   다른 세션과 자동 수집이 수시로 커밋하므로, 작업 전 pull은 필수다.

## 2. 읽는 순서 (5분)

1. `CLAUDE.md`(루트)
   - 최우선 정책: 트랙 A(경제판단, 개인 자산)는 업로드·메일 허용, 트랙 B(회사 업무)는 금지. 애매하면 B로 본다.
   - 작업 프로토콜: 계획 → 진행 표시 → 완료 보고
2. `wiki/architecture/repository-map.md` **← 핵심.** 담긴 내용:
   - 폴더 지도
   - 자동화 시간표(KST)
   - 진행 중 과제
   - 알려진 버그
3. `wiki/CLAUDE.md`: 위키 스키마, Ingest/Query/Lint 방법
4. `wiki/log.md` 마지막 30줄, `MessageBox.md`, `wiki/messagebox.md`
5. 질문 주제에 맞는 `wiki/monitoring/*-status.md`의 **Latest Status**

## 3. 질문 유형별 바로가기

| 질문 | 먼저 볼 곳 |
|---|---|
| 하이닉스 팔까 말까 | `wiki/concepts/scenario-action-playbook.md`(S1~S4, 판정 기록), `sources/sk-hynix-price-snapshot.csv` |
| 시세·수급 숫자 | `sources/sk-hynix-*.csv`(**웹검색보다 우선**). 정규장 종가는 `fetched_at`이 07:xx UTC인 행. 저녁 행은 NXT 시세로 덮인 버그가 있다 |
| 보유 종목·계좌 | `sources/portfolio-holdings.csv`, `wiki/entities/my-portfolio.md` |
| 거시·금리·선거 | `wiki/monitoring/rate-outlook-scenario-status.md`, `wiki/concepts/midterm-history-playbook.md`, `sources/macro-series.csv` |
| AI 투자·메모리 | `wiki/monitoring/ai-capex-slowdown-status.md`, `wiki/monitoring/memory-price-hynix-guidance-status.md` |
| 청약·주거 | `wiki/monitoring/gwanggyo-a17bl-application-status.md`, `housing-funding-execution-status.md`, `yongin-suji-rent-status.md`, `wiki/concepts/yongin-platform-city-project-facts.md` |
| 사용자 정보 | `wiki/entities/user-profile.md`, `config/user.yaml` |
| 자동화 상세 | `wiki/architecture/automation-pipeline-reference.md`(재시도·알림·저장 위치). 워크플로 목록은 repository-map 7장이 더 최신 |
| 브리핑 | `report/briefing/`, `wiki/concepts/briefing-compass.md`, `data/briefing/compass.yaml` |

## 4. 꼭 지킬 규칙

- **R1 실측 우선:** KIS CSV, 사용자 제공 데이터, 웹검색 순으로 믿는다.
- **R3 판단 불가:** 데이터가 없으면 "판단 불가"다. 안전하다는 뜻이 아니다.
- **R4 결정은 사용자:** 엔진 신호가 공식 판단이다. Claude는 의견임을 표시해서 말하고, 결정은 사용자가 한다.
- **단정 금지:** 확인하지 않은 사실을 단정하지 않는다. 출처와 신뢰도를 붙인다.
- **sources/는 불변:** 새 원자료는 `sources/주제-화자-YYYY-MM-DD.md`로 새 파일만 추가한다.
- **위키 페이지:** 새로 만들기보다 기존 페이지 갱신을 우선한다. 새 페이지를 만들면 `wiki/index.md`에 한 줄을 추가한다.
- **log.md:**
  - `## 당일 log` 맨 아래에만 한 줄 append한다. 형식: `YYYY-MM-DD HH:MM UTC — 종류 ... → updated ...`
  - 충돌이 나면 두 줄을 모두 보존한다.
  - 회전(00:20 KST)은 자동이니 건드리지 않는다.
- **push:** `bash scripts/push_with_retry.sh main`으로만 한다. 거절되면 fetch, rebase 후 재시도한다.
- **HTML 보고서:** 덮어쓰지 않는다. 파일명에 날짜와 시간을 넣어 새로 만든다.
- **수정 금지 영역:**
  - `engine/valuation/hynix_band.py`
  - `engine/report/signal_recorder.py`
  - `engine/report/weekly_analysis.py`
  - PEOS 섹션 순서
- **답변 스타일:**
  - 한국어로, 깊이 조사하되 간결하게 답한다.
  - "오드리"라고 부르면 `wiki/concepts/audrey-briefing-style.md`를 따른다. 기호와 단락 없이, 귀로 듣는 글로 쓴다.
- **트랙 B 자료 취급:** `wiki/customer-meetings/`와 CXL 관련은 읽기만 한다. 새로 올리거나 메일로 보내지 않는다.
- **IRP·DC는 건드리지 않는다.** 하나증권 마크업 67주는 2027-02까지 보유한다.

## 5. 작업을 마칠 때

1. 바꾼 위키 페이지의 `updated:` 날짜를 갱신하고, 관련 페이지와 서로 링크한다.
2. `wiki/log.md`에 한 줄을 추가한다.
3. 커밋 메시지는 `docs:`, `feat:`, `fix:` 중 하나로 시작한다.
4. `bash scripts/push_with_retry.sh main`으로 push한다.
5. 저장소 구조가 바뀌었으면(새 폴더, 새 워크플로, 새 루틴) **`wiki/architecture/repository-map.md`도 같은 커밋에서 갱신**한다. 이 스킬은 그 문서를 가리키기만 하므로 따로 고칠 필요가 없다.
