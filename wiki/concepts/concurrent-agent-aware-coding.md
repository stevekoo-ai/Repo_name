---
title: 동시 실행 중인 다른 Agent를 고려한 코딩 규칙 (Concurrent-Agent-Aware Coding)
created: 2026-08-07
updated: 2026-08-07
tags: [coding, ops, safety, process-management, priority, headless, multi-agent]
---

> 🔴 **우선순위: 최상. 코드를 작성·수정할 때마다 반드시 먼저 적용한다.**
> 이 규칙은 [CLAUDE.md "코드 작성 품질"](../../CLAUDE.md) 섹션의 **최상위
> 상위 규칙**으로 등록되어 있다 — API/파라미터 검증보다 *먼저* 검토한다.
> 이유: API 오류는 치명적이지 않지만(스크립트가 실패하는 데 그침), 이 규칙을
> 어기면 **사용자의 live interactive Claude Code 세션과 다른 Agent의
> 진행 중 작업이 통째로 강제 종료**된다 — 되돌릴 수 없고, 사용자가 대화
> 컨텍스트를 잃는다.

## 핵심 원칙

코드가 **동시에 실행 중일 수 있는 다른 프로세스를 죽이거나 방해하지
않도록** 작성한다. 특히 headless 자동화 스크립트(`claude -p` 래퍼,
스케줄러, bat/ps1 루틴)에서 프로세스를 정리(cleanup/sweep/kill)할 때,
매칭 조건이 **좁아야** 한다 — 넓은 매칭은 의도치 않게 다른 Agent 세션을
잡아 죽인다.

이 규칙은 git 동시 편집 충돌([multi-client-conflict-prevention.md](multi-client-conflict-prevention.md))과는
**다른 레이어**의 안전 규칙이다:
- git 충돌 규칙 = 두 클라이언트가 **같은 파일**을 편집할 때 데이터 손상 방지.
- 이 규칙 = 여러 프로세스가 **같은 머신**에서 동시에 실행될 때 프로세스 강제 종료 방지.
두 규칙 모두 "동시 사용자를 고려한다"는 같은 철학에서 나왔으나 적용 영역이 다르다 — 둘 다 지킨다.

## 발단 — 실제 사건 (2026-08-07, FATAL)

`scripts/run_cxl_claude_bounded.ps1` / `run_claude_bounded.ps1` 두
headless `claude -p` 래퍼의 타임아웃 분기에 이런 process sweep이 있었다:

```powershell
$procs = Get-CimInstance Win32_Process | Where-Object {
    ($_.Name -eq 'claude.exe' -or $_.Name -eq 'node.exe') -and
    $_.CommandLine -and ($_.CommandLine -match 'claude')
}
foreach ($np in $procs) { & taskkill /F /PID $np.ProcessId 2>&1 | Out-Null }
```

의도는 타임아웃 시 고아 headless 자식 `claude.exe`/`node.exe`를 정리하는
것이었다. 그러나 매칭 조건이 **"commandline에 'claude'가 들어간 모든
claude.exe/node.exe"** 였고, 이 조건은 **사용자가 대화하고 있는 live
interactive Claude Code 세션도 만족**한다.

결과: 좁은 타임아웃(90초 테스트)으로 claude가 첫 응답조차 하기 전에
강제 컷 → sweep이 전역 `claude.exe`/`node.exe`를 뒤져 → headless 자식
**뿐 아니라 이 interactive 세션까지 `taskkill /F`로 통째로 강제 종료** →
대화 창이 빠져나가버림. 사용자가 "이 내용을 실행하면서 claude 실행 창을
빠져나가 버린다. 이거 하지마!"라고 보고한 문제의 정체.

다른 Agent(모바일/데스크톱 병렬 세션, 스케줄러가 띄운 다른 headless
작업)도 같은 머신에서 `node.exe`/`claude.exe`를 쓰면 동일하게 죽는다 —
진행 중인 작업이 통째로 사라진다.

## 규칙 (코드 작성 시 반드시 적용)

### R1. 프로세스 kill 매칭은 좁혀라 — 넓히지 마라
`taskkill`/`Stop-Process`/`Get-CimInstance Win32_Process`로 프로세스를
잡을 때, **commandline 부분 문자열 매칭만으로는 절대 부족하다.**
`'claude'` 같은 generic 키워드는 interactive 세션·다른 Agent·다른
headless 작업 전부 매칭한다. 최소 두 가지 안전장치를 겹쳐라:

1. **PID 직접 추적**: 내가 spawn한 프로세스의 PID(`Start-Process -PassThro`
   또는 job의 child PID)만 kill. 가장 안전. 추적이 어려우면 아래로.
2. **CreationDate 시간 창**: 내 job 시작 시각 **이후**에 생성된
   프로세스만 타겟. interactive 세션은 래퍼 시작 **전부터** 존재하므로
   매칭에서 자동 제외된다 — commandline 매칭과 무관한 2차 안전장치.
   ```powershell
   $launchTime = $t0.AddSeconds(-2)   # job 시작 직전, 여유 2초
   $procs = Get-CimInstance Win32_Process | Where-Object {
       ($_.Name -eq 'claude.exe' -or $_.Name -eq 'node.exe') -and
       $_.CommandLine -and ($_.CommandLine -match 'claude') -and
       $_.CreationDate -and ([datetime]$_.CreationDate) -ge $launchTime
   }
   ```
3. **commandline 시그니처 한정**: headless 작업만의 고유 문자열
   (system-prompt 파일 경로, headless 전용 플래그 조합)로 추가 좁힘.
   2중·3중 안전장치.

### R2. sweep보다 "고아를 남기는 쪽"이 안전하면 그렇게 하라
프로세스 정리(sweep)가 다른 작업을 죽일 위험이 있으면, **sweep 자체를
빼라.** 고아 headless 자식 프로세스가 남을 수 있지만, 그건 "다른
Agent의 작업이 멈추는 것"보다 훨씬 안전하다. 고아 프로세스는 시스템
자원을 조금 쓰다 종료되거나 다음 부팅에 정리되지만, 강제 종료된
interactive 세션의 **대화 컨텍스트는 되돌릴 수 없다.**

사용자가 명시적으로 "sweep을 하면 창이 죽으니 다른 Agent 작업도 멈추게
되, 이 명령은 적용하지 않는 게 좋겠다"고 판단한 경우, sweep 블록 전체를
제거하고 `Stop-Job`만 남긴다 (본 사건의 실제 조치 — CR11).

### R3. 코드를 짜기 전에 "이 머신에 지금 뭐가 돌고 있는가"를 묻는다
스케줄러·bat 루틴·래퍼가 돌아가는 머신에는:
- 사용자의 interactive Claude Code 세션 (이 창)
- 모바일/데스크톱 병렬 Claude Code 세션 (가능)
- 다른 headless `claude -p` 작업 (스케줄러)
- GitHub Actions runner, 동기화 데몬, 기타 `node.exe` 프로세스

가 동시에 존재할 수 있다. 프로세스 kill·파일 잠금·포트 점유·글로벌
상태 변경 같은 **"환경 전체에 영향"을 주는 코드**를 짤 때는, "이 코드가
저 무리 중 하나를 실수로 건드리지 않는가"를 먼저 점검한다.

### R4. 좁은 타임아웃으로 테스트하지 마라
좁은 타임아웃(예: 90초)으로 무거운 headless 작업을 테스트하면, 첫 응답
전에 강제 컷 → 타임아웃 분기(sweep 포함)가 발생 → 위 사건 재현. 정상
타임아웃(CXL 25분 / SK 10분)에서만 검증한다. 좁은 타임아웃 테스트 자체가
R1/R2 위반 코드를 자주 발동시켜 위험을 키운다.

### R5. 공유 자원(global state) 변경도 같은 원칙
프로세스 kill뿐 아니라 — 전역 환경변수/레지스트리/공유
파일(`.claude/settings.json`, `.wiki/active-session.json` 등)을
코드가 건드릴 때도 "다른 동시 세션이 이 상태에 의존하고 있지 않은가"
점검. 변경이 필요하면 [messagebox](../messagebox.md)로 먼저 알리고
(운영 규칙 2), 겹치지 않게 순서를 잡는다.

## 적용 체크리스트 (코드 작성 전/중)

- [ ] 이 코드가 `taskkill`/`Stop-Process`/프로세스 매칭을 하는가? → R1
- [ ] 매칭 조건이 generic keyword(`'claude'`, `'node'`) 부분 문자열만인가? → R1 (좁혀라)
- [ ] PID 직접 추적 또는 CreationDate 시간 창을 쓰는가? → R1
- [ ] sweep이 위험하면 빼는 게 낫다면 뺐는가? → R2
- [ ] 좁은 타임아웃으로 테스트하고 있는가? → R4 (중단)
- [ ] 공유 자원·전역 상태를 변경하는가? → R5
- [ ] 이 머신의 다른 동시 세션에 영향이 가는가? → R3

## 다른 규칙과의 관계

- **[multi-client-conflict-prevention.md](multi-client-conflict-prevention.md)**:
  git 동시 편집 충돌 방지. 본 페이지는 프로세스 레이어. 둘 다 "동시
  사용자 고려" 철학. 큰 변화 시 [messagebox](../messagebox.md) 게시는
  양쪽 공통 전제.
- **[claude-code-internal-routing.md](claude-code-internal-routing.md)**:
  사내 LLM 라우팅·재부팅 후 접속 복구. headless 자동화가 라우팅 환경
  위에서 돈다는 점에서 연관.
- **[CLAUDE.md "코드 작성 품질"](../../CLAUDE.md)**: 본 규칙은 그 섹션의
  최상위 상위 규칙으로 등록됨. API/파라미터 검증(Double/triple check)보다
  *우선* 적용 — 치명도가 더 높기 때문.

## Sources

- 2026-08-07 사용자 보고: "이 내용을 실행하면서 claude 실행 창을
  빠져나가 버린다. 이거 하지마!" + "다른 동시 사용되고 있는 Agent를
  고려해서 코딩을 해야 한다는 내용을 wiki에 작성해줘. 우선순위를 높혀서
  coding에 꼭 참조할 수 있도록."
- 실제 사건: `scripts/run_cxl_claude_bounded.ps1`·`run_claude_bounded.ps1`
  타임아웃 분기 process sweep이 interactive Claude Code 세션을
  `taskkill /F`로 강제 종료 (CR11 수정으로 sweep 제거).
- [다중 클라이언트 충돌 방지 운영](multi-client-conflict-prevention.md)
- [CLAUDE.md 코드 작성 품질 / 중간 단계 작업 프로토콜](../../CLAUDE.md)
