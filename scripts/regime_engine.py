#!/usr/bin/env python3
"""
HBM Cycle Score의 매크로 국면(G/I/L) 엔진.

sources/macro-database-1954-2026.md에 박제된 CPI/실업률/연방기금금리
원자료(1954~2026, 사용자가 다른 대화에서 만든 시드 데이터)를 파싱해
매달 G(성장)/I(물가)/L(유동성) 국면 점수를 계산하고, z-score 유클리드
거리로 가장 닮은 과거 시기를 찾는다.

이 스크립트는 웹검색이 아니라 정적 시드 데이터 기반이라, 시드 데이터의
마지막 달(현재 2026-05) 이후 신규 월간 지표(UNRATE/CPI/FEDFUNDS 신규
발표분)는 반영하지 못한다. 신규 발표분은:
  (a) 사용자가 이미 구축한 별도 FRED API 파이프라인 산출값을 이 파일의
      CSV 블록 끝에 새 행으로 append하거나,
      (권장) --append-month로 값을 넘기면 이 스크립트가 직접 append,
  (b) 또는 라우틴이 웹검색으로 최신 발표치를 확인해 같은 방식으로 append
하는 두 경로 모두 지원한다 — 값을 넣는 방식(API vs 웹검색)은 무엇이든
상관없고, 이 스크립트 입장에서는 "새 CSV 행이 추가됐는가"만 중요하다.

사용법:
  python3 scripts/regime_engine.py                  # 최신월 국면 + 유사 시기 출력(JSON)
  python3 scripts/regime_engine.py --date 2026-05    # 특정월 기준 조회
  python3 scripts/regime_engine.py --append-month 2026-06 --cpi 330.5 --unrate 4.3 --fedfunds 4.33
      # 신규 월 데이터를 세 CSV 블록에 각각 append(중복 월이면 덮어씀)
"""
import re
import sys
import json
import argparse
import math
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "sources" / "macro-database-1954-2026.md"


def _extract_csv_block(text: str, header_line: str) -> str:
    """헤더 라인(`## N. \`xxx.csv\``) 뒤의 ```csv ... ``` 블록 원문을 추출."""
    idx = text.index(header_line)
    start = text.index("```csv", idx) + len("```csv")
    end = text.index("```", start)
    return text[start:end].strip("\n")


def load_series(path: Path = SOURCE):
    text = path.read_text(encoding="utf-8")

    cpi_block = _extract_csv_block(text, "## 3. `cpi_monthly.csv`")
    unrate_block = _extract_csv_block(text, "## 4. `unemployment_rate_monthly.csv`")
    fedfunds_block = _extract_csv_block(text, "## 5. `fedfunds_monthly.csv`")

    def parse(block, value_col):
        rows = {}
        lines = block.splitlines()
        header = lines[0].split(",")
        vi = header.index(value_col)
        for line in lines[1:]:
            if not line.strip():
                continue
            parts = line.split(",")
            y, m = int(parts[0]), int(parts[1])
            v = parts[vi].strip()
            if v in ("", "."):
                continue
            rows[(y, m)] = float(v)
        return rows

    cpi = parse(cpi_block, "cpi_index")
    unrate = parse(unrate_block, "unemployment_rate_pct")
    fedfunds = parse(fedfunds_block, "effective_fed_funds_rate_pct")
    return cpi, unrate, fedfunds


def _shift(y, m, n):
    idx = y * 12 + (m - 1) - n
    return idx // 12, idx % 12 + 1


def compute_regime_series(cpi, unrate, fedfunds):
    """월별 G/I/L + quadrant. cpi/unrate 12개월전, cpi 6개월전 값이 모두 있는 달만."""
    out = {}
    for (y, m) in sorted(cpi.keys()):
        if (y, m) not in unrate or (y, m) not in fedfunds:
            continue
        y12, m12 = _shift(y, m, 12)
        y6, m6 = _shift(y, m, 6)
        if (y12, m12) not in cpi or (y12, m12) not in unrate:
            continue
        if (y6, m6) not in cpi:
            continue

        unrate_t = unrate[(y, m)]
        unrate_t12 = unrate[(y12, m12)]
        G = -(unrate_t - unrate_t12)

        cpi_t = cpi[(y, m)]
        cpi_t12 = cpi[(y12, m12)]
        cpi_t6 = cpi[(y6, m6)]
        cpi_yoy_t = cpi_t / cpi_t12 - 1
        cpi_yoy_t6 = cpi_t6 / cpi[_shift(y6, m6, 12)] - 1 if _shift(y6, m6, 12) in cpi else None
        if cpi_yoy_t6 is None:
            continue
        I = cpi_yoy_t - cpi_yoy_t6

        fedfunds_t = fedfunds[(y, m)]
        L = fedfunds_t - cpi_yoy_t * 100

        if G > 0 and I < 0:
            quadrant = "recovery"
        elif G > 0 and I >= 0:
            quadrant = "overheat"
        elif G <= 0 and I > 0:
            quadrant = "stagflation"
        else:
            quadrant = "reflation"

        out[(y, m)] = {"G": G, "I": I, "L": L, "quadrant": quadrant, "cpi_yoy": cpi_yoy_t}
    return out


def zscore_all(regime):
    keys = list(regime.keys())
    def stats(vals):
        n = len(vals)
        mean = sum(vals) / n
        var = sum((v - mean) ** 2 for v in vals) / n
        return mean, math.sqrt(var)

    Gm, Gs = stats([regime[k]["G"] for k in keys])
    Im, Is = stats([regime[k]["I"] for k in keys])
    Lm, Ls = stats([regime[k]["L"] for k in keys])

    z = {}
    for k in keys:
        r = regime[k]
        z[k] = (
            (r["G"] - Gm) / Gs,
            (r["I"] - Im) / Is,
            (r["L"] - Ls) / Ls if Ls else 0.0,
        )
    return z, (Gm, Gs, Im, Is, Lm, Ls)


def find_analogues(regime, target_key, top_n=5, exclude_recent_months=24, min_gap_months=12):
    z, _ = zscore_all(regime)
    if target_key not in z:
        raise SystemExit(f"target {target_key} not in regime series (데이터 부족한 달일 수 있음)")
    tz = z[target_key]

    ty, tm = target_key
    target_idx = ty * 12 + tm

    dists = []
    for k, zz in z.items():
        ky, km = k
        idx = ky * 12 + km
        if abs(target_idx - idx) < exclude_recent_months:
            continue
        d = math.sqrt(sum((a - b) ** 2 for a, b in zip(tz, zz)))
        dists.append((d, k))
    dists.sort()

    picked = []
    for d, k in dists:
        if all(abs((k[0] * 12 + k[1]) - (pk[0] * 12 + pk[1])) >= min_gap_months for _, pk in picked):
            picked.append((d, k))
        if len(picked) >= top_n:
            break
    return picked


def append_month(path: Path, date_str: str, cpi=None, unrate=None, fedfunds=None):
    y, m = date_str.split("-")
    y, m = int(y), f"{int(m):02d}"
    text = path.read_text(encoding="utf-8")

    def upsert(header_line, value_col, value):
        if value is None:
            return text
        nonlocal_text = text
        idx = nonlocal_text.index(header_line)
        start = nonlocal_text.index("```csv", idx) + len("```csv\n")
        end = nonlocal_text.index("```", start)
        block = nonlocal_text[start:end]
        lines = [l for l in block.splitlines() if l.strip()]
        new_row = f"{y},{m},{value}"
        prefix = f"{y},{m},"
        lines = [l for l in lines if not l.startswith(prefix)]
        lines.append(new_row)
        # keep header first, sort data rows chronologically
        header, *data = lines
        data.sort(key=lambda l: (int(l.split(',')[0]), int(l.split(',')[1])))
        new_block = "\n".join([header] + data) + "\n"
        return nonlocal_text[:start] + new_block + nonlocal_text[end:]

    text = upsert("## 3. `cpi_monthly.csv`", "cpi_index", cpi)
    text = upsert("## 4. `unemployment_rate_monthly.csv`", "unemployment_rate_pct", unrate)
    text = upsert("## 5. `fedfunds_monthly.csv`", "effective_fed_funds_rate_pct", fedfunds)
    path.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM, 기본은 시드 데이터의 마지막 달")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--append-month", help="YYYY-MM — 새 월 데이터 append 후 종료")
    ap.add_argument("--cpi", type=float)
    ap.add_argument("--unrate", type=float)
    ap.add_argument("--fedfunds", type=float)
    args = ap.parse_args()

    if args.append_month:
        append_month(SOURCE, args.append_month, args.cpi, args.unrate, args.fedfunds)
        print(f"appended {args.append_month} to {SOURCE}")
        return

    cpi, unrate, fedfunds = load_series()
    regime = compute_regime_series(cpi, unrate, fedfunds)

    if args.date:
        y, m = map(int, args.date.split("-"))
        target = (y, m)
    else:
        target = max(regime.keys())

    r = regime[target]
    matches = find_analogues(regime, target, top_n=args.top)

    result = {
        "target": f"{target[0]}-{target[1]:02d}",
        "G": round(r["G"], 3),
        "I": round(r["I"], 4),
        "L": round(r["L"], 3),
        "quadrant": r["quadrant"],
        "cpi_yoy_pct": round(r["cpi_yoy"] * 100, 2),
        "top_analogues": [
            {
                "period": f"{k[0]}-{k[1]:02d}",
                "distance": round(d, 3),
                "G": round(regime[k]["G"], 3),
                "I": round(regime[k]["I"], 4),
                "L": round(regime[k]["L"], 3),
                "quadrant": regime[k]["quadrant"],
            }
            for d, k in matches
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
