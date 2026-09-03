# 실행 레이어 통합 — BAT/PS1 → Execute/ (2026-08-26)

> **🆕 2026-08-26**, BAT/PS1 파일을 `bin/`과 `scripts/` 양쪽에 흩어진 것에서 `Execute/` 단일 폴더로 통합.

## 문제 정의

리팩토링 전 실행 파일이 세 곳에 흩어져 있음:

| 위치 | BAT | PS1 | 문제 |
|------|-----|-----|------|
| 루트 `C:\Users\2053437\` | `run_cxl_daily.bat`, `run_daily.bat` | `cxl_diag.ps1`, `cxl_repro_test.bat` | 루트 분산 |
| `scripts\` | `cxl_daily_routine.bat`, `cxl_daily_v2_routine.bat`, `cxl_newsroom_routine.bat`, `log_summarize_routine.bat` | `run_cxl_claude_bounded.ps1`, `run_cxl_newsroom_bounded.ps1`, `run_log_summarize_bounded.ps1`, `run_poet_claude_bounded.ps1`, `run_poet_regenerate.ps1` | BAT가 Python 스크립트 폴더와 혼재 |
| `bin\` | (없음) | (없음) | `ffmpeg.exe`, `ffprobe.exe`만 존재 |

BAT ←→ PS1 간에 `scripts\run_xxx_bounded.ps1`으로 서로 참조하고 있어, 폴더 위치가 꼬여 있음.

## 해법: `Execute/` 단일 폴더

모든 BAT + PS1 파일을 `Execute/` 폴더로 통합. Python은 `scripts/`에 그대로 유지.

```
C:\Users\2053437\
├── Execute/              ← 모든 BAT + PS1 (16개 파일)
│   ├── run_cxl_daily.bat              # CXL Daily 메인 (Task Scheduler: Steve_CXL_Daily_Update, 06:30)
│   ├── run_daily.bat                  # POET Daily 메인 (Task Scheduler: Daily Brief Headless, DISABLED)
│   ├── cxl_daily_v2_routine.bat       # CXL Newsroom v2 파이프라인 (Task Scheduler: CXL Newsroom v2, 07:00)
│   ├── cxl_newsroom_routine.bat       # CXL Newsroom Update (Task Scheduler: Steve_CXL_Newsroom_Update, 06:45)
│   ├── log_summarize_routine.bat      # log.md 요약 (Task Scheduler: Steve_Log_Manager, 00:40)
│   ├── cxl_daily_routine.bat          # 고스트 레퍼런스 (실제 실행 안 함)
│   ├── run_cxl_claude_bounded.ps1     # claude 래퍼 (CXL Daily)
│   ├── run_cxl_newsroom_bounded.ps1   # claude 래퍼 (CXL Newsroom)
│   ├── run_log_summarize_bounded.ps1  # claude 래퍼 (log 요약)
│   ├── run_poet_claude_bounded.ps1    # claude 래퍼 (POET)
│   ├── run_poet_regenerate.ps1        # POET 재생성 (수동)
│   ├── cxl_diag.ps1                   # 진단용
│   ├── cxl_repro_test.bat             # 테스트용
│   ├── setup_and_run.bat              # 헬퍼
│   ├── setup_tasks.bat                # 헬퍼
│   └── temp_create_tasks.bat          # 헬퍼 (임시)
├── scripts/              ← Python만 (BAT 0개)
└── bin/                  ← ffmpeg.exe, ffprobe.exe (media tools)
```

## 변경 사항 상세

### 1. 파일 이동

| 이동 전 | 이동 후 |
|---------|---------|
| `run_cxl_daily.bat` | `Execute\run_cxl_daily.bat` |
| `run_daily.bat` | `Execute\run_daily.bat` |
| `cxl_diag.ps1` | `Execute\cxl_diag.ps1` |
| `cxl_repro_test.bat` | `Execute\cxl_repro_test.bat` |
| `setup_and_run.bat` | `Execute\setup_and_run.bat` |
| `setup_tasks.bat` | `Execute\setup_tasks.bat` |
| `temp_create_tasks.bat` | `Execute\temp_create_tasks.bat` |
| `scripts/cxl_daily_routine.bat` | `Execute\cxl_daily_routine.bat` |
| `scripts/cxl_daily_v2_routine.bat` | `Execute\cxl_daily_v2_routine.bat` |
| `scripts/cxl_newsroom_routine.bat` | `Execute\cxl_newsroom_routine.bat` |
| `scripts/log_summarize_routine.bat` | `Execute\log_summarize_routine.bat` |
| `scripts/run_cxl_claude_bounded.ps1` | `Execute\run_cxl_claude_bounded.ps1` |
| `scripts/run_cxl_newsroom_bounded.ps1` | `Execute\run_cxl_newsroom_bounded.ps1` |
| `scripts/run_log_summarize_bounded.ps1` | `Execute\run_log_summarize_bounded.ps1` |
| `scripts/run_poet_claude_bounded.ps1` | `Execute\run_poet_claude_bounded.ps1` |
| `scripts/run_poet_regenerate.ps1` | `Execute\run_poet_regenerate.ps1` |

### 2. BAT 파일 내부 참조 경로 수정

BAT에서 BAT/PS1 호출 경로를 `scripts\` → `Execute\`로 변경:

| 파일 (라인) | 변경 전 | 변경 후 |
|-------------|---------|---------|
| `run_cxl_daily.bat:72` | `scripts\run_cxl_claude_bounded.ps1` | `Execute\run_cxl_claude_bounded.ps1` |
| `run_daily.bat:91` | `scripts\run_poet_claude_bounded.ps1` | `Execute\run_poet_claude_bounded.ps1` |
| `cxl_newsroom_routine.bat:68` | `scripts\run_cxl_newsroom_bounded.ps1` | `Execute\run_cxl_newsroom_bounded.ps1` |
| `log_summarize_routine.bat:64` | `scripts\run_log_summarize_bounded.ps1` | `Execute\run_log_summarize_bounded.ps1` |
| `cxl_daily_routine.bat:67` | `scripts\run_cxl_claude_bounded.ps1` | `Execute\run_cxl_claude_bounded.ps1` |

BAT 상단 `cd /d "C:\Users\2053437"`로 작업 디렉토리는 루트 고정 → 상대 경로로 `Execute\*.bat` 접근.

### 3. Python 파일 BAT 경로 수정

Python에서 BAT 절대 경로를 참조하는 스크립트 업데이트:

| 파일 | 변경 전 | 변경 후 |
|------|---------|---------|
| `scripts/register_cxl_newsroom_task.py:41` | `r"C:\Users\2053437\scripts\cxl_newsroom_routine.bat"` | `r"C:\Users\2053437\Execute\cxl_newsroom_routine.bat"` |
| `scripts/register_log_summarize_task.py:35` | `r"C:\Users\2053437\scripts\log_summarize_routine.bat"` | `r"C:\Users\2053437\Execute\log_summarize_routine.bat"` |

**Python 호출은 그대로 유지**: BAT에서 `python scripts\upload_log_summary.py` 등 Python 스크립트는 `scripts/`에 그대로 두므로 BAT 내부 참조 변경 안 함.

### 4. PS1 주석 수정

| 파일 | 변경 전 | 변경 후 |
|------|---------|---------|
| `run_poet_regenerate.ps1:3` | `Run from PS: .\scripts\run_poet_regenerate.ps1` | `Run from PS: .\Execute\run_poet_regenerate.ps1` |

### 5. 고스트 파일

- `Execute\cxl_daily_routine.bat`: Task Scheduler에서 등록되지 않은 레퍼런스용 파일. 내용 상동 but `cd /d "C:\Users\2053437"` + `scripts\run_cxl_claude_bounded.ps1`(수정 후 `Execute\`). 실제 실행은 `run_cxl_daily.bat`이 담당.

## 백업 위치

모든 파일은 실행 전 `.claude/backups/Execute-backup-20260826/`에 백업됨.

## Task Scheduler 작업 (수동 업데이트 필요)

Task Scheduler에서 BAT 경로를 새 위치로 업데이트해야 함:

| 작업명 | 새 BAT 경로 | 예정 시간 |
|--------|------------|----------|
| `Steve_CXL_Daily_Update` | `C:\Users\2053437\Execute\run_cxl_daily.bat` | 06:30 KST |
| `CXL Newsroom v2` | `C:\Users\2053437\Execute\cxl_daily_v2_routine.bat` | 07:00 KST |
| `Steve_CXL_Newsroom_Update` | `C:\Users\2053437\Execute\cxl_newsroom_routine.bat` | 06:45 KST |
| `Steve_Log_Manager` | `C:\Users\2053437\Execute\log_summarize_routine.bat` | 00:40 KST |
| `Daily Brief Headless` (Disabled) | `C:\Users\2053437\Execute\run_daily.bat` | 수동 |

> schtasks 자동 등록은 안전 분류기 차단으로 불가 — 수동 CMD 실행 필요.

## 설계 원칙

1. **BAT + PS1 = 실행 레이어** → `Execute/`
2. **Python = 데이터 처리 레이어** → `scripts/`
3. **media tools** → `bin/` (ffmpeg/ffprobe)
4. BAT 상단 `cd /d`로 작업 디렉토리 고정, 상대 경로로 다른 레이어 참조
5. 절대 경로(PS1 `WorkDir`)는 `C:\Users\2053437`로 고정 — BAT의 cd /d가 작업 디렉토리 설정

## 관련 문서

- [헤드리스 Claude 자율 사이클](headless-claude-autonomous-cycle.md) — 배치 파일 아키텍처 개요
- [보고서 생성 — Lessons Learned](report-generation-lessons-learned-2026-08-20.md) — BAT 실행 환경 체크리스트
- [실행 레이어 통합](execution-layers-consolidation.md) — 이 문서
