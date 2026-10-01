#!/usr/bin/env bash
# push + rebase 재시도. 재생성 가능한 파일 충돌은 다시 만들어 해결한다.
#
# 2026-10-01 신설 — daily-peos-report가 9/30·10/1 이틀 연속 실패했다. 리포트는
# 만들어졌는데 push 직전 rebase에서 docs/reports-index.html이 충돌했다. 이 파일은
# 4개 워크플로(PEOS·청약·하이닉스·부동산)가 매번 저장소 내용으로 통째로 다시
# 만드는 링크 목록이라, 어느 쪽 내용을 고를 문제가 아니라 **rebase 후 다시
# 만들면 되는** 파일이다. 기존 루프는 rebase가 충돌하면 그대로 죽었다.
#
# 재생성 가능 목록(REGEN) 밖의 파일이 충돌하면 rebase를 취소하고 실패한다 —
# 데이터 파일을 임의로 한쪽으로 덮으면 안 되기 때문이다.
#
#   bash scripts/push_with_retry.sh [branch]
set -u
BRANCH="${1:-${GITHUB_REF_NAME:-main}}"
REGEN="docs/reports-index.html"

for i in 1 2 3 4 5; do
  if git push origin "HEAD:$BRANCH"; then
    exit 0
  fi
  echo "push rejected, rebasing onto latest $BRANCH (attempt $i)"
  git fetch origin "$BRANCH"
  if ! git rebase --autostash "origin/$BRANCH"; then
    while true; do
      conflicted=$(git diff --name-only --diff-filter=U)
      [ -z "$conflicted" ] && break
      for f in $conflicted; do
        case " $REGEN " in
          *" $f "*) ;;
          *) echo "::error::재생성할 수 없는 파일 충돌: $f — rebase 취소"; git rebase --abort; exit 1 ;;
        esac
      done
      echo "재생성 가능한 파일 충돌 → 다시 생성: $conflicted"
      python3 scripts/build_reports_index.py || { git rebase --abort; exit 1; }
      git add $REGEN
      if ! GIT_EDITOR=true git rebase --continue; then
        # 다음 커밋에서 또 충돌하면 while이 다시 처리한다
        continue
      fi
    done
  fi
  sleep $((i * 3))
done
echo "::error::push 5회 실패"
exit 1
