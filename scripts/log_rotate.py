#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
log_rotate.py — wiki/log.md deterministic rotation (GitHub Actions runner용).

LLM 없음. 순수 Python stdlib. CLAUDE.md "코드 작성 품질 프로토콜" 준수.

3인 하이브리드 중 GitHub Actions 층 담당:
  - 매일 00:20 KST(15:20 UTC) 실행
  - 어제(KST) 날짜 로그 항목을 log.md에서 잘라 log-archive/YYYY-MM/YYYY-MM-DD.md로 이관
  - 월말(1일) 분기: 전월 일일 아카이브 폴더 → 전월 월 아카이브 1파일로 병합 + 일일 파일 삭제
  - idempotent: 어제 아카이브가 이미 존재하면 cut skip (안전 재실행)
  - runner가 GitHub 인프라에 있어 git push 한계 없음 (회사망 73KB 제약 해당 없음)

요약(LLM 서술)은 Windows 측(claude -p → GLM 게이트웨이)이 담당.
이 스크립트는 요약 섹션("## 당월 요약", "## 직전월 요약")은 건드리지 않고
로그 항목(## 당일 log / 날짜로 시작하는 줄)만 분리해서 처리한다.

로직:
  log.md 구조 = [헤더/요약 프로즈] + [로그 항목들]
  - 헤더/요약: 첫 `^YYYY-MM-DD` 줄 이전의 모든 줄 (보존, 손대지 않음)
  - 로그 항목: `^YYYY-MM-DD`로 시작하는 줄 + 그 뒤 `^YYYY-MM-DD` 아닌 연속 줄들
    (항목이 여러 줄일 수 있으므로 다음 날짜 줄까지 한 항목으로 묶음)

월말 분기(오늘 KST = 1일):
  - 어제 = 전월 마지막 날 → 어제 cut 후,
    전월 일일 아카이브 폴더(log-archive/YYYY-MM/)의 모든 *.md를
    전월 월 아카이브(log-archive/YYYY-MM.md)로 병합(이미 있으면 skip/갱신),
    일일 파일 삭제. 병합은 idempotent(월 아카이브 존재 시 재실행해도 안전).

Usage:
  python log_rotate.py                 # 자동: 실행 시점 KST 기준 어제 처리
  python log_rotate.py --date 2026-08-06   # 명시적 대상 날짜 (테스트/수동)
  python log_rotate.py --dry-run       # 실제 파일 변경 없이 무엇을 할지 출력
  python log_rotate.py --repo-root /path   # 기본: cwd
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta, timezone

# Windows 콘솔 cp949가 em-dash/특수문자 인코딩 못 함 → stdout UTF-8 강제
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

KST = timezone(timedelta(hours=9))
LOG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")  # 줄 시작 날짜


def kst_yesterday() -> str:
    """실행 시점 KST 기준 어제 날짜 (YYYY-MM-DD)."""
    now_kst = datetime.now(KST)
    return (now_kst - timedelta(days=1)).strftime("%Y-%m-%d")


def parse_log_entries(content):
    """log.md 내용을 (header, entries)로 분리.

    header: 첫 ^YYYY-MM-DD 줄 이전의 모든 줄(문자열, 후행 newline 유지).
    entries: list of (date_str, body_text). body는 항목 전체 텍스트(개행 포함).
    여러 줄 항목 지원: ^YYYY-MM-DD 아닌 연속 줄은 이전 항목에 귀속.
    """
    lines = content.splitlines(keepends=True)
    header_lines = []
    idx = 0
    # 헤더: 첫 날짜 줄 전까지
    while idx < len(lines):
        if LOG_RE.match(lines[idx]):
            break
        header_lines.append(lines[idx])
        idx += 1

    entries = []
    cur_date = None
    cur_body = []
    while idx < len(lines):
        line = lines[idx]
        m = LOG_RE.match(line)
        if m:
            # 이전 항목 flush
            if cur_date is not None:
                entries.append((cur_date, "".join(cur_body)))
            cur_date = m.group(1)
            cur_body = [line]
        else:
            if cur_date is not None:
                cur_body.append(line)
            # cur_date None + 날짜 아닌 줄 = 헤더 연속 (이론상 위에서 잡힘)
        idx += 1
    if cur_date is not None:
        entries.append((cur_date, "".join(cur_body)))

    return "".join(header_lines), entries


ARCHIVE_FM = """---
title: Log Archive {date}
created: {date}
updated: {date}
tags: [log, archive]
---

# Log Archive — {date}

아카이브: `wiki/log.md`에서 로테이션(3인 하이브리드, GitHub Actions 층)이
이관한 {date} 로그 항목. 원본은 append-only 그대로 보존.

## 당일 log

{body}"""


def archive_path(repo_root, date_str):
    ym = date_str[:7]  # YYYY-MM
    return os.path.join(repo_root, "wiki", "log-archive", ym, f"{date_str}.md")


def monthly_archive_path(repo_root, ym):
    return os.path.join(repo_root, "wiki", "log-archive", f"{ym}.md")


MONTHLY_FM_HEADER = """---
title: Log Archive {ym}
created: {created}
updated: {updated}
tags: [log, archive, monthly]
---

# Log Archive — {ym}

월 아카이브: {ym} 일일 아카이브({ym}/YYYY-MM-DD.md)를 병합한 cold storage.
로테이션(3인 하이브리드) 월말 정산 시 자동 생성. 일일 파일은 병합 후 삭제.

"""


def do_cut(repo_root, target_date, dry_run):
    """어제(또는 지정) 날짜 항목을 log.md에서 잘라 아카이브로 이관."""
    log_path = os.path.join(repo_root, "wiki", "log.md")
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    header, entries = parse_log_entries(content)

    # idempotent: 아카이브 이미 존재하면 cut skip (재실행 안전)
    a_path = archive_path(repo_root, target_date)
    if os.path.exists(a_path):
        print(f"[skip] archive already exists: wiki/log-archive/{target_date[:7]}/{target_date}.md — cut idempotent, nothing to do")
        return False  # 변경 없음

    target_entries = [e for e in entries if e[0] == target_date]
    if not target_entries:
        print(f"[noop] no log entries for {target_date} in log.md — nothing to cut")
        return False

    remaining = [e for e in entries if e[0] != target_date]

    # 아카이브 파일 생성
    body = "".join(b for _, b in target_entries)
    archive_content = ARCHIVE_FM.format(date=target_date, body=body)

    # 남은 log.md 재조립: 헤더 + 남은 항목
    new_log = header + "".join(b for _, b in remaining)
    # 헤더가 빈 항목 사이에 끼어있던 빈 줄 정리: 끝에 개행 보장
    if new_log and not new_log.endswith("\n"):
        new_log += "\n"

    if dry_run:
        print(f"[dry-run] would create: {os.path.relpath(a_path, repo_root)} ({len(target_entries)} entries, {len(body)} bytes)")
        print(f"[dry-run] would rewrite: wiki/log.md ({len(remaining)} entries remain, was {len(entries)})")
        return False

    os.makedirs(os.path.dirname(a_path), exist_ok=True)
    with open(a_path, "w", encoding="utf-8") as f:
        f.write(archive_content)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(new_log)

    print(f"[cut] {len(target_entries)} entries ({len(body)} bytes) → {os.path.relpath(a_path, repo_root)}")
    print(f"[cut] log.md: {len(entries)} → {len(remaining)} entries")
    return True


def do_monthly_consolidate(repo_root, prev_ym, dry_run):
    """전월 일일 아카이브 폴더를 전월 월 아카이브로 병합.

    prev_ym: 전월 "YYYY-MM". 일일 파일(log-archive/YYYY-MM/*.md) 읽어
    월 아카이브(log-archive/YYYY-MM.md)에 날짜순 병합. 이미 월 아카이브가
    있으면 idempotent 재생성(전체 다시 조립, 안전). 일일 파일 삭제.
    """
    daily_dir = os.path.join(repo_root, "wiki", "log-archive", prev_ym)
    if not os.path.isdir(daily_dir):
        print(f"[skip] no daily archive dir for {prev_ym} — nothing to consolidate")
        return False

    daily_files = sorted(
        f for f in os.listdir(daily_dir) if f.endswith(".md")
    )
    if not daily_files:
        print(f"[skip] daily dir empty for {prev_ym}")
        return False

    # 각 일일 파일에서 로그 항목(날짜로 시작하는 줄)만 추출해 월 아카이브에 날짜 헤더로 붙임.
    # frontmatter, "# Log Archive" 타이틀, 안내문, "## 당일 log" 헤더는 모두 제외 —
    # 월 아카이브에는 날짜 항목만 깔끔히 들어가야 함.
    sections = []
    for fn in daily_files:
        d = os.path.join(daily_dir, fn)
        with open(d, "r", encoding="utf-8") as f:
            txt = f.read()
        date_str = fn[:-3]  # strip .md
        _, entries = parse_log_entries(txt)
        if not entries:
            continue
        body = "".join(b for _, b in entries)
        sections.append(f"## {date_str}\n{body.strip()}\n")

    created = f"{prev_ym}-01"
    today = datetime.now(KST).strftime("%Y-%m-%d")
    monthly = MONTHLY_FM_HEADER.format(ym=prev_ym, created=created, updated=today) + "\n".join(sections)

    m_path = monthly_archive_path(repo_root, prev_ym)
    if dry_run:
        print(f"[dry-run] would write monthly archive: {os.path.relpath(m_path, repo_root)} ({len(daily_files)} daily files merged)")
        print(f"[dry-run] would delete {len(daily_files)} daily files in {os.path.relpath(daily_dir, repo_root)}")
        return False

    with open(m_path, "w", encoding="utf-8") as f:
        f.write(monthly)
    for fn in daily_files:
        os.remove(os.path.join(daily_dir, fn))
    os.rmdir(daily_dir)  # 빈 폴더면 제거

    print(f"[consolidate] {len(daily_files)} daily files → {os.path.relpath(m_path, repo_root)}")
    print(f"[consolidate] deleted {len(daily_files)} daily files + empty dir")
    return True


def main():
    ap = argparse.ArgumentParser(description="wiki/log.md rotation (deterministic, LLM-free)")
    ap.add_argument("--date", help="대상 날짜 YYYY-MM-DD (기본: KST 어제)")
    ap.add_argument("--dry-run", action="store_true", help="변경 없이 무엇을 할지 출력")
    ap.add_argument("--repo-root", default=os.getcwd(), help="repo 루트 (기본: cwd)")
    args = ap.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    target = args.date or kst_yesterday()

    print(f"=== log_rotate: target={target}, repo={repo_root}, dry_run={args.dry_run} ===")

    changed = do_cut(repo_root, target, args.dry_run)

    # 월말 분기: 오늘 KST = 1일 → 어제는 전월 마지막 날 → 전월 병합
    today_kst = datetime.now(KST)
    if today_kst.day == 1:
        prev = (today_kst.replace(day=1) - timedelta(days=1))
        prev_ym = prev.strftime("%Y-%m")
        print(f"=== month-start detected: consolidating previous month {prev_ym} ===")
        consolidated = do_monthly_consolidate(repo_root, prev_ym, args.dry_run)
        changed = changed or consolidated

    print(f"=== done (changed={changed}) ===")
    # workflow가 commit 여부 판단: changed=True면 커밋, False면 skip
    sys.exit(0)


if __name__ == "__main__":
    main()
