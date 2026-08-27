# wiki_digest — 위키 판단형 지식 → daily 리포트 브리지

daily 리포트 개편 계획(Phase 4, 2026-08-27) — HBM Cycle Score 정성축, SK
Hynix 9체크포인트, 찐반등 4대 신호, 트럼프 중간선거 트래커 같은 **판단형
지식**은 WebSearch·애널리스트 리포트 해석·뉴스 종합처럼 사람(또는 Claude)의
판단이 필요해서, LLM을 쓰지 않는 결정론적 cron 파이프라인(`engine/report/`)
이 스스로 재현할 수 없다. 위키(`wiki/monitoring/*-status.md`)가 유일한
원천이고, 이 디렉토리는 그 "Latest Status"의 압축 요약을 daily 리포트가
안전하게(자유문 파싱 없이) 읽을 수 있는 작은 구조화 파일로만 미러링한다.

## 규칙

- **이 디렉토리의 파일은 절대 첫 원천이 아니다.** 항상 대응하는
  `wiki/monitoring/*-status.md`의 Latest Status를 요약한 것 — 새 판단을
  여기서 만들지 않는다.
- **위키 페이지를 갱신하는 바로 그 작업(Claude 트리거·`/ingest`·수동 편집)
  이 같은 커밋에서 이 파일도 같이 갱신한다.** 별도 파이프라인이 아니라
  기존 절차에 한 스텝 추가하는 것.
- `as_of`는 그 요약이 근거한 위키 Latest Status의 날짜. 대응하는
  `wiki/monitoring/*.md`의 frontmatter `updated:`보다 오래되면 드리프트—
  `tests/test_exposure_reconciliation.py::test_wiki_digest_is_not_stale...`
  가 이걸 감지한다.
- `status_label`은 한 줄 배지(이모지+짧은 판정), `one_line_summary`는
  리포트에 그대로 노출될 한두 문장 — 위키 원문을 다시 풀어쓰지 말고
  위키의 최신 판정을 그대로 인용한다.

## 스키마

```yaml
concept_page: "wiki/concepts/<slug>.md"        # framework 정의
monitoring_page: "wiki/monitoring/<slug>-status.md"  # 일일 상태(원천)
as_of: "YYYY-MM-DD"                             # 위 페이지 Latest Status 날짜
status_label: "..."                             # 배지 한 줄
one_line_summary: "..."                         # 리포트에 노출될 요약
```
