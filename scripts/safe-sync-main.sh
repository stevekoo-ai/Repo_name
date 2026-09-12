#!/usr/bin/env bash
# safe-sync-main.sh
#
# main 브랜치를 origin/main으로 안전하게 동기화한다.
#
# 왜 필요한가:
#   컨테이너/세션이 shallow clone으로 시작하는 경우, 로컬 main과
#   origin/main이 공통 조상을 계산할 수 없어(merge-base 실패) 실제로는
#   조상-후손 관계(순수 fast-forward)인데도 "divergent branches"로
#   오진단된다. 이 상태에서 `git pull`(merge)이나 `git rebase`를 그대로
#   실행하면 불필요한 병합 커밋이 생기거나, 최악의 경우 로컬에 없는
#   히스토리를 잘못 재작성할 위험이 있다.
#
# 이 스크립트가 하는 일:
#   1. shallow clone이면 --unshallow로 전체 히스토리를 먼저 확보한다.
#   2. origin/main을 fetch한다.
#   3. merge-base를 계산해 실제 관계를 확인한다.
#   4. 순수 fast-forward가 가능할 때만 --ff-only로 진행한다.
#   5. 진짜 divergence(로컬에만 있는 미푸시 커밋 존재)면 병합/리베이스를
#      자동으로 하지 않고 즉시 중단하며 상황을 보고한다 — 사용자 판단 필요.
#
# 사용법:
#   bash scripts/safe-sync-main.sh
#
# 종료 코드:
#   0 = 정상 동기화(이미 최신 포함) / 1 = 진짜 divergence로 중단 / 2 = 기타 오류

set -euo pipefail

BRANCH="main"
REMOTE="origin"

cd "$(git rev-parse --show-toplevel)"

current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$current_branch" != "$BRANCH" ]]; then
  echo "[safe-sync] 경고: 현재 브랜치가 '$current_branch'입니다. '$BRANCH'로 전환합니다." >&2
  git checkout "$BRANCH"
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "[safe-sync] 중단: 워킹트리에 커밋되지 않은 변경이 있습니다. 먼저 커밋/stash 하세요." >&2
  git status -sb
  exit 2
fi

if [[ -f .git/shallow ]]; then
  echo "[safe-sync] shallow clone 감지 — 전체 히스토리를 가져옵니다 (git fetch --unshallow)..."
  git fetch --unshallow "$REMOTE" "$BRANCH"
else
  echo "[safe-sync] fetch $REMOTE/$BRANCH..."
  git fetch "$REMOTE" "$BRANCH"
fi

local_head="$(git rev-parse "$BRANCH")"
remote_head="$(git rev-parse "$REMOTE/$BRANCH")"

if [[ "$local_head" == "$remote_head" ]]; then
  echo "[safe-sync] 이미 최신입니다 ($local_head). 변경 없음."
  exit 0
fi

merge_base="$(git merge-base "$BRANCH" "$REMOTE/$BRANCH")"

if [[ "$merge_base" == "$local_head" ]]; then
  # 로컬 main은 origin/main의 순수 조상 -> 안전한 fast-forward
  echo "[safe-sync] 순수 fast-forward 가능. 병합합니다..."
  git merge --ff-only "$REMOTE/$BRANCH"
  echo "[safe-sync] 완료. HEAD -> $(git rev-parse --short "$BRANCH")"
  exit 0
fi

if [[ "$merge_base" == "$remote_head" ]]; then
  echo "[safe-sync] 로컬 main이 origin/main보다 앞서 있습니다 (미푸시 커밋 존재)." >&2
  echo "[safe-sync] 자동으로 아무것도 하지 않습니다 — 필요 시 직접 push 하세요." >&2
  git log --oneline "$REMOTE/$BRANCH..$BRANCH"
  exit 1
fi

echo "[safe-sync] 중단: 진짜 divergence입니다 (로컬/원격 모두에 상대에 없는 커밋 존재)." >&2
echo "[safe-sync] 자동 merge/rebase를 하지 않습니다 — Prime Directive(Never destroy active work) 준수." >&2
echo "" >&2
echo "로컬에만 있는 커밋:" >&2
git log --oneline "$REMOTE/$BRANCH..$BRANCH" >&2
echo "" >&2
echo "원격에만 있는 커밋:" >&2
git log --oneline "$BRANCH..$REMOTE/$BRANCH" >&2
exit 1
