# Macro Investment Clock Agent

미국 거시경제 지표를 매일 자동으로 수집해 **Merrill Lynch Investment Clock**(성장 x 물가 2축 4국면) 모델로
현재 경기 국면을 판정하고, 시계 이미지 + 트렌드 차트 + 히스토리 테이블을 담은 대시보드를 생성하는 에이전트입니다.

참고 자료:
- [Macro Ops — The Investment Clock](https://macro-ops.com/the-investment-clock/)
- 美林投资时钟 관련 중국어 리서치 자료 (사용자 제공 링크, 접근 제한으로 원문 대신 공개된 동일 프레임워크 설명을 참고)

## 모델 로직

- **성장(Growth) 축**: OECD Composite Leading Indicator (미국, amplitude-adjusted, `USALOLITOAASTSAM`).
  구할 수 없으면 산업생산지수(`INDPRO`) YoY로 대체.
- **물가(Inflation) 축**: CPI YoY (`CPIAUCSL` 기준 계산). Core CPI(`CPILFESL`)는 참고용 보조 지표.
- **모멘텀 판정**: 각 지표의 "3개월 전 대비 변화"가 양수면 `rising`, 음수면 `falling`.
- **4 국면** (시계방향, 12→3→6→9):

  | 시계 위치 | 국면 | 성장 | 물가 | 유리 자산 |
  |---|---|---|---|---|
  | 12시 | Reflation (침체/저물가) | falling | falling | 채권 |
  | 3시 | Recovery (회복) | rising | falling | 주식 |
  | 6시 | Overheat (과열) | rising | rising | 원자재 |
  | 9시 | Stagflation (스태그플레이션) | falling | rising | 현금 |

- 참고용 컨텍스트 지표: 10Y-2Y 국채 스프레드(`T10Y2Y`), 실업률(`UNRATE`) — 국면 판정에는 쓰이지 않고 대시보드에만 표시.

## 데이터 소스 / Input 목록

전부 [FRED](https://fred.stlouisfed.org)의 공개 CSV 엔드포인트(`/graph/fredgraph.csv?id=...`)에서 **API 키 없이** 수집합니다.

| 이름 | FRED 시리즈 | 용도 |
|---|---|---|
| 성장(주) | `USALOLITOAASTSAM` | OECD CLI, 성장 축 |
| 성장(보조/fallback) | `INDPRO` | 산업생산, CLI 불가 시 대체 |
| 물가(주) | `CPIAUCSL` | CPI, 물가 축 |
| 물가(보조) | `CPILFESL` | Core CPI, 참고 |
| 컨텍스트 | `T10Y2Y`, `UNRATE` | 장단기 금리차, 실업률 (참고 표시용) |

FRED CSV는 키 없이도 동작하지만, 요청 제한/차단이 걸릴 경우를 대비해 `FRED_API_KEY` 환경변수(GitHub Secret)를 설정하면
공식 REST API로 자동 폴백하도록 만들어 두었습니다 (`src/clock/data_sources.py`).

> **참고**: 이 개발 샌드박스는 아웃바운드 네트워크가 정책상 제한되어 있어 FRED 접속을 직접 테스트하지 못했습니다
> (합성 데이터로 파이프라인 전체를 검증함). GitHub Actions 러너는 일반 인터넷 환경이라 정상 동작해야 하며,
> 첫 병합 후 반드시 **Actions 탭에서 수동 실행(workflow_dispatch)** 으로 한 번 확인해 주세요.

## 자동화 구조 (하루 1회, 08:00 KST)

`.github/workflows/daily-clock-report.yml`이 매일 08:00 KST(23:00 UTC)에 실행되어:
1. `python -m src.clock.main` 실행 → 데이터 수집 → 국면 판정 → `data/history.csv`에 누적 →
   `docs/clock.png`, `docs/trend_growth.png`, `docs/trend_inflation.png`, `docs/index.html` 생성
2. 변경분을 저장소에 자동 커밋/푸시

리포트는 **정적 대시보드(GitHub Pages)** 로 제공됩니다. 알림(이메일/Slack)은 기본 비활성화(no-op)이며,
`src/clock/notify.py`가 환경변수만으로 채널을 스위칭할 수 있게 되어 있습니다:

- `SLACK_WEBHOOK_URL` 설정 → Slack으로 매일 요약 전송
- `SMTP_HOST` + `SMTP_USER` + `SMTP_PASSWORD` + `NOTIFY_EMAIL_TO` 설정 → 이메일 전송

다른 자동화 방식(예: 별도 서버 cron, Claude 세션 Routine 등)으로 바꾸고 싶다면 `src/clock/main.py`의
`run()` 함수만 그대로 호출하면 되므로 워크플로우 교체가 쉽습니다.

## 사용자가 직접 해야 할 일 (Manual steps)

1. **이 브랜치의 PR을 `main`으로 merge** — GitHub Actions의 `schedule` 트리거는 기본 브랜치에서만 동작합니다.
2. **GitHub Pages 활성화**: 저장소 Settings → Pages → Source를 `main` 브랜치의 `/docs` 폴더로 설정
   (그러면 `https://<user>.github.io/<repo>/` 에서 매일 갱신되는 대시보드를 볼 수 있습니다).
3. **(선택) Slack/이메일 알림을 원하면** 위에 나온 환경변수들을 저장소 Settings → Secrets and variables → Actions에 등록.
4. **(선택) FRED API 키**: [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html)에서 무료 발급 후
   `FRED_API_KEY` secret으로 등록하면 CSV 크롤링이 막힐 때 자동 폴백됩니다.
5. Merge 직후 **Actions 탭 → Daily Investment Clock Report → Run workflow**로 한 번 수동 실행해 정상 동작 확인 권장.

## 로컬 실행

```bash
pip install -r requirements.txt
python -m src.clock.main
```

`data/history.csv`와 `docs/`가 갱신됩니다.

## 테스트

```bash
pip install pytest
python -m pytest tests/
```

4개 국면 매핑 로직에 대한 스모크 테스트가 포함되어 있습니다 (`tests/test_model.py`).

## 한계 및 주의사항

- 원문 자료(`macro-ops.com`, ksyun 첨부 PDF)는 이 환경에서 접근 시 403으로 차단되어 원문 전체를 직접 인용하지는
  못했고, 공개적으로 알려진 동일 Merrill Lynch Investment Clock 프레임워크 설명(검색 결과 및 일반 지식)을 기반으로 구현했습니다.
- 이 모델은 월간 지표(CPI, 산업생산 등) 기반이라 실제 국면은 한 달에 한 번 정도만 바뀝니다. 매일 리포트를 생성하지만
  `data_asof`(실제 데이터 기준월)가 같으면 국면도 동일하게 반복 표시되는 것이 정상입니다.
- 투자 자문이 아니며, 참고용 프레임워크 시각화입니다.
