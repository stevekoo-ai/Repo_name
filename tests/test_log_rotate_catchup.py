"""log_rotate — 늦게 추가된 항목·회전이 빠진 날도 따라잡는다(2026-09-25)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import log_rotate as R  # noqa: E402


def _repo(tmp_path, log_body):
    (tmp_path / "wiki" / "log-archive" / "2026-09").mkdir(parents=True)
    (tmp_path / "wiki" / "log.md").write_text("# Log\n\n## 당일 log (append-only)\n\n" + log_body, encoding="utf-8")
    return tmp_path


def test_late_append_to_already_archived_day_is_moved_without_duplication(tmp_path):
    repo = _repo(tmp_path, "2026-09-20 — A old\n2026-09-20 — B late\n2026-09-23 — C missed\n2026-09-25 — D today\n")
    arc = repo / "wiki" / "log-archive" / "2026-09" / "2026-09-20.md"
    arc.write_text("# archive\n\n2026-09-20 — A old\n", encoding="utf-8")
    assert R.do_cut(str(repo), "2026-09-24", False) is True
    log = (repo / "wiki" / "log.md").read_text(encoding="utf-8")
    assert "D today" in log and "A old" not in log and "C missed" not in log
    a = arc.read_text(encoding="utf-8")
    assert a.count("A old") == 1 and "B late" in a
    assert (repo / "wiki" / "log-archive" / "2026-09" / "2026-09-23.md").exists()
    assert R.do_cut(str(repo), "2026-09-24", False) is False  # 재실행 안전
