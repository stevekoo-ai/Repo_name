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

# 상태 이모지 → 색상 등급. 브리핑 본문이 이미 이 이모지들로 심각도를
# 표시해왔는데(🔴 위험/✅ 적중 등), 지금까지는 렌더러가 이걸 그냥 평문으로
# 찍어서 md와 html이 시각적으로 구분이 안 됐다 — 이모지 자체는 색이
# 있어 보이지만 주변 텍스트·배경은 다른 문단과 완전히 동일했다.
_SEVERITY_EMOJI = {
    "🔴": "bad", "❌": "bad",
    "🟠": "warn", "🟡": "warn", "⚠️": "warn",
    "🟢": "good", "✅": "good",
    "🔵": "neutral",
}


def _leading_severity(text: str) -> str | None:
    t = text.lstrip()
    t = re.sub(r"^\d+\.\s*", "", t)  # "1. 🟢 원화..." 처럼 번호 접두어가 붙는 경우
    for emo, sev in _SEVERITY_EMOJI.items():
        if t.startswith(emo):
            return sev
    return None


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


def _wrap_sections(fragments: list[str]) -> str:
    """`##` 경계로 카드를 나눈다. 지금까지는 h2/p/table이 전부 같은 높이의
    평문으로 흘러나와 "제목과 내용의 구분이 안 된다"는 지적을 받았다 —
    `_CSS`엔 `.card`가 이미 있었는데 이 변환기가 한 번도 안 썼다."""
    sections: list[list[str]] = [[]]
    titles: list[str | None] = [None]
    for frag in fragments:
        m = re.match(r"^<h2>(.*)</h2>$", frag)
        if m:
            sections.append([frag])
            titles.append(re.sub(r"<[^>]+>", "", m.group(1)).strip())
        else:
            sections[-1].append(frag)
    out = []
    for idx, sec in enumerate(sections):
        if not sec:
            continue
        content = "\n".join(sec)
        if idx == 0:
            out.append(f"<header class='masthead'>{content}</header>")
        else:
            cls = "card highlight" if titles[idx] == "결론" else "card"
            out.append(f"<section class='{cls}'>{content}</section>")
    return "\n".join(out)


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
            text = stripped[level:].strip()
            sev = _leading_severity(text) if level == 3 else None
            cls = f" class='hx-{sev}'" if sev else ""
            tag = min(level, 4)
            out.append(f"<h{tag}{cls}>{_inline(text)}</h{tag}>")
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
            text = " ".join(block)
            sev = _leading_severity(text)
            cls = f" class='bq-{sev}'" if sev else ""
            out.append(f"<blockquote{cls}>{_inline(text)}</blockquote>")
            continue

        # 순서/비순서 목록 — 마크다운 소프트 줄바꿈으로 한 항목이 여러
        # 줄에 걸치는 경우가 실제 브리핑에 항상 있다(들여쓴 계속줄).
        # 예전 구현은 계속줄을 못 알아채고 별도 <p>로 떼어내 문장이
        # <ol>과 <p> 사이에서 잘렸다 — "줄이 안 맞는다"는 지적의 실체.
        if stripped.startswith("- ") or re.match(r"^\d+\.\s", stripped):
            ordered = bool(re.match(r"^\d+\.\s", stripped))
            items: list[str] = []
            current: list[str] | None = None
            while i < len(lines):
                raw = lines[i]
                s = raw.strip()
                if not s:
                    # 항목 사이 빈 줄(loose list)이다 — 그다음 첫 비어있지
                    # 않은 줄이 새 항목이면 목록을 계속 잇는다. 안 그러면
                    # 여기서 끝. 실제 브리핑은 항목마다 빈 줄로 나뉘어 있어,
                    # 이 처리가 없으면 항목마다 별도 <ol>이 생겨 브라우저가
                    # 번호를 매번 1로 재시작한다("1. 1. 1."로 보이던 원인).
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    nxt = lines[j].strip() if j < len(lines) else ""
                    nxt_is_new = bool(re.match(r"^\d+\.\s", nxt)) if ordered else nxt.startswith("- ")
                    if nxt_is_new:
                        i = j
                        continue
                    break
                starts_new = bool(re.match(r"^\d+\.\s", s)) if ordered else s.startswith("- ")
                if starts_new:
                    if current is not None:
                        items.append(" ".join(current))
                    current = [re.sub(r"^\d+\.\s", "", s) if ordered else s[2:]]
                    i += 1
                elif (current is not None and raw[:1].isspace()
                        and not re.match(r"^(#|>|\||-{3,}$)", s)):
                    current.append(s)
                    i += 1
                else:
                    break
            if current is not None:
                items.append(" ".join(current))
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + f"</{tag}>")
            continue

        # 문단 — 빈 줄까지 이어붙인다(마크다운의 소프트 줄바꿈)
        block = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#|>|-\s|\||\d+\.\s|-{3,}$)", lines[i].strip()):
            block.append(lines[i].strip())
            i += 1
        if block:
            out.append(f"<p>{_inline(' '.join(block))}</p>")
    return _wrap_sections(out)


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
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ padding: 6px 10px; border-bottom: 1px solid var(--border); }}
blockquote {{ margin: 12px 0; padding: 10px 14px; background: var(--surface-2);
  border-left: 3px solid var(--accent); border-radius: 4px; }}
.table-wrap {{ overflow-x: auto; }}
header.masthead {{ padding-top: 0; }}
/* 심각도 이모지(🔴🟠🟡✅❌ 등)로 시작하는 인용/소제목은 그 등급 색으로
   강조한다 — "뭘 강조해야 할지 모르겠다"는 지적에 대한 답: 지금까지
   이모지는 색이 있는데 주변은 다른 문단과 똑같았다. */
blockquote.bq-bad {{ background: var(--bad-bg); border-left-color: var(--bad); }}
blockquote.bq-warn {{ background: var(--warn-bg); border-left-color: var(--warn); }}
blockquote.bq-good {{ background: var(--good-bg); border-left-color: var(--good); }}
blockquote.bq-neutral {{ background: var(--neutral-bg); border-left-color: var(--neutral); }}
h3.hx-bad, h3.hx-warn, h3.hx-good, h3.hx-neutral {{
  padding-left: 10px; border-left: 4px solid; margin-left: -12px; }}
h3.hx-bad {{ border-color: var(--bad); }}
h3.hx-warn {{ border-color: var(--warn); }}
h3.hx-good {{ border-color: var(--good); }}
h3.hx-neutral {{ border-color: var(--neutral); }}
</style>
</head>
<body>
{body}
<footer>PEOS 브리핑 · 코드 생성 HTML{f" · {_html.escape(generated)}" if generated else ""}</footer>
</body>
</html>"""
