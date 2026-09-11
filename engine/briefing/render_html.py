"""브리핑 마크다운 → HTML. **LLM을 쓰지 않는다 — 순수 변환이라 0 토큰이다.**

## 왜 라이브러리를 안 쓰나

`markdown`·`mistune`이 이 저장소에 없고, 이 변환의 입력은 **우리가 형식을
정한 브리핑 마크다운 하나뿐**이다(Routine 프롬프트가 섹션 구조를 못박는다).
범용 파서를 의존성으로 들이는 것보다, 그 구조만 정확히 다루는 변환기를
두고 테스트로 고정하는 편이 낫다.

## 보안 — 이스케이프 순서가 중요하다

브리핑 본문엔 **뉴스에서 온 텍스트**가 섞인다. 그래서 **HTML 이스케이프를
먼저** 하고 그 위에 마크다운 인라인 규칙을 적용한다. 마크다운 문법
문자(`*` `[` `]` `(` `)` `|` 백틱)는 이스케이프 대상이 아니라서 순서를
이렇게 잡아도 문법이 깨지지 않는다. 반대로 하면 `<script>`가 그대로 남는다.

## 스타일

`engine/report/html_shared.py`의 `_CSS`를 재사용한다 — 월간 PEOS 리포트·
데일리 대시보드와 같은 제품으로 보이게 하는 게 목적이고, 새 스타일을 여기서
만들지 않는다.
"""
from __future__ import annotations

import html as _html
import re

from engine.report.html_shared import _CSS

_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_CODE = re.compile(r"`([^`]+)`")


def _inline(text: str) -> str:
    """인라인 마크다운. **이스케이프가 먼저다**(모듈 docstring 참조)."""
    out = _html.escape(text, quote=False)
    out = _CODE.sub(r"<code>\1</code>", out)
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    # 링크는 http(s)와 상대경로만 허용한다 — javascript: 같은 스킴을 막는다
    def _link(m):
        label, href = m.group(1), m.group(2)
        if not re.match(r"^(https?://|\.{0,2}/|[A-Za-z0-9_.-]+/)", href):
            return label
        return f'<a href="{_html.escape(href, quote=True)}">{label}</a>'
    return _LINK.sub(_link, out)


def _strip_frontmatter(md: str) -> tuple[dict, str]:
    if not md.startswith("---"):
        return {}, md
    end = md.find("\n---", 3)
    if end == -1:
        return {}, md
    meta = {}
    for line in md[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, md[end + 4:]


def _table(rows: list[str]) -> str:
    """| a | b | 형식. 두 번째 줄이 |---|---:| 정렬행이다."""
    def cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]

    header = cells(rows[0])
    aligns = []
    for spec in cells(rows[1]):
        if spec.endswith(":") and spec.startswith(":"):
            aligns.append("center")
        elif spec.endswith(":"):
            aligns.append("right")
        else:
            aligns.append("left")
    out = ["<div class='table-wrap'><table><thead><tr>"]
    for i, h in enumerate(header):
        a = aligns[i] if i < len(aligns) else "left"
        out.append(f"<th style='text-align:{a}'>{_inline(h)}</th>")
    out.append("</tr></thead><tbody>")
    for line in rows[2:]:
        out.append("<tr>")
        for i, c in enumerate(cells(line)):
            a = aligns[i] if i < len(aligns) else "left"
            out.append(f"<td style='text-align:{a}'>{_inline(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def markdown_to_body(md: str) -> str:
    """브리핑 마크다운의 본문만 HTML로. <html> 골격은 render_briefing_html이 씌운다."""
    _, md = _strip_frontmatter(md)
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # 표 — 다음 줄이 정렬행이어야 표로 인정한다
        if (stripped.startswith("|") and i + 1 < len(lines)
                and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip())):
            block = [lines[i], lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            out.append(_table(block))
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            out.append(f"<h{min(level, 4)}>{_inline(stripped[level:].strip())}</h{min(level, 4)}>")
            i += 1
            continue

        if re.match(r"^-{3,}$", stripped):
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote>{_inline(' '.join(block))}</blockquote>")
            continue

        if stripped.startswith("- "):
            block = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                block.append(f"<li>{_inline(lines[i].strip()[2:])}</li>")
                i += 1
            out.append(f"<ul>{''.join(block)}</ul>")
            continue

        if re.match(r"^\d+\.\s", stripped):
            block = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                # f-string 안에 백슬래시를 못 넣는 파이썬 버전이 있어 분리한다
                item = re.sub(r"^\d+\.\s", "", lines[i].strip())
                block.append("<li>" + _inline(item) + "</li>")
                i += 1
            out.append(f"<ol>{''.join(block)}</ol>")
            continue

        # 문단 — 빈 줄까지 이어붙인다(마크다운의 소프트 줄바꿈)
        block = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#|>|-\s|\||\d+\.\s|-{3,}$)", lines[i].strip()):
            block.append(lines[i].strip())
            i += 1
        if block:
            out.append(f"<p>{_inline(' '.join(block))}</p>")
    return "\n".join(out)


def render_briefing_html(md: str, title: str | None = None) -> str:
    meta, _ = _strip_frontmatter(md)
    title = title or meta.get("title", "PEOS 브리핑")
    body = markdown_to_body(md)
    generated = meta.get("generated_at", "")
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_html.escape(title)}</title>
<style>{_CSS}
/* 브리핑 전용 최소 보강 — 나머지는 월간 리포트·대시보드와 같은 _CSS를 쓴다 */
body {{ max-width: 860px; margin: 0 auto; padding: 24px 16px 48px; }}
h2 {{ margin-top: 32px; padding-top: 16px; border-top: 1px solid var(--border); }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ padding: 6px 10px; border-bottom: 1px solid var(--border); }}
blockquote {{ margin: 12px 0; padding: 10px 14px; background: var(--surface-2);
  border-left: 3px solid var(--accent); border-radius: 4px; }}
.table-wrap {{ overflow-x: auto; }}
</style>
</head>
<body>
{body}
<footer>PEOS 브리핑 · 코드 생성 HTML{f" · {_html.escape(generated)}" if generated else ""}</footer>
</body>
</html>"""
