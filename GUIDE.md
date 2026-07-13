# 사용 설명서 (간단 버전)

## 이게 뭔가요?

미국 거시경제 지표를 매일 자동으로 확인해서 지금이 경기 사이클의 어느 국면인지
판단하고, 그 국면에서 유리한 자산군을 알려주는 자동 리포트입니다.
"Merrill Lynch Investment Clock"이라는 오래된 프레임워크를 그대로 구현한 것입니다.

## 동작 순서 (매일 08:00 KST에 자동 실행)

```
① 데이터 수집 → ② 국면 판정 → ③ 시각화 → ④ 누적 저장 → ⑤ 자동 커밋
```

1. **데이터 수집** (`src/clock/data_sources.py`)
   FRED(미국 연준 경제데이터)에서 API 키 없이 두 지표를 가져옵니다.
   - 성장: OECD 경기선행지수(CLI) — 안 되면 산업생산지수로 대체
   - 물가: CPI(소비자물가) 전년동월비

2. **국면 판정** (`src/clock/model.py`)
   두 지표가 각각 **"3개월 전보다 올랐는가, 내렸는가"** 만 봅니다.

   | 성장 | 물가 | 국면 | 유리 자산 |
   |---|---|---|---|
   | ↑ | ↓ | 회복 (Recovery) | 주식 |
   | ↑ | ↑ | 과열 (Overheat) | 원자재 |
   | ↓ | ↑ | 스태그플레이션 | 현금 |
   | ↓ | ↓ | 침체/리플레이션 | 채권 |

3. **시각화** (`src/clock/render.py`, `report.py`)
   시계 그림 위에 시침이 현재 국면(12/3/6/9시 방향)을 가리키도록 그리고,
   성장·물가 추이 그래프와 최근 기록 표를 붙여 `docs/index.html` 대시보드로 만듭니다.

4. **누적 저장** (`src/clock/storage.py`)
   판정 결과를 `data/history.csv`에 한 줄씩 쌓습니다. 지표가 월간이라 실제 국면은
   보통 한 달에 한 번 정도만 바뀌고, 그 사이엔 같은 국면이 반복 기록되는 게 정상입니다.

5. **자동 커밋** (`.github/workflows/daily-clock-report.yml`)
   위 결과를 GitHub Actions가 저장소에 자동으로 커밋·푸시합니다. 사람이 손댈 필요 없음.

## 결과는 어디서 보나요?

- **대시보드**: `https://<github아이디>.github.io/<저장소명>/`
  (Settings → Pages에서 `main` 브랜치 `/docs` 폴더를 소스로 지정해야 열람 가능)
- **원본 데이터**: 저장소의 `data/history.csv` (표 형태, 엑셀로 열어도 됨)
- **수동 실행**: GitHub 저장소 → Actions 탭 → `Daily Investment Clock Report` → `Run workflow`

## 알림을 더 받고 싶다면

기본은 대시보드만 갱신되고 별도 알림은 없습니다. Slack이나 이메일로 매일 요약을 받고
싶으면 저장소 Settings → Secrets에 다음을 등록하면 코드 수정 없이 자동으로 켜집니다.

- Slack: `SLACK_WEBHOOK_URL`
- 이메일: `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`, `NOTIFY_EMAIL_TO`

## 주의사항

- 투자 자문이 아니라 참고용 프레임워크 시각화입니다.
- 자세한 기술 설명(지표 목록, 계산식 등)은 `README.md`를 참고하세요.
