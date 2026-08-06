import React, { useState, useMemo, useCallback } from "react";
import {
  ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, Brush,
} from "recharts";

/**
 * SK하이닉스(또는 다른 종목) 주가 + 외국인보유율 5년 차트.
 *
 * scripts/hynix_5y_history.py의 `merge` 서브커맨드가 생성하는
 * sources/hynix_price_foreign_5y.csv를 업로드하면 바로 그려진다.
 * 기대 컬럼: date,ticker,open,high,low,close,volume,foreign_hold_pct,foreign_hold_qty
 * (foreign_hold_pct/qty는 KRX 백필이 없는 날짜엔 빈 문자열일 수 있음 —
 * 이 컴포넌트는 그런 구간을 이어서 그리지 않고 끊어서 보여준다, 지어내서
 * 채우지 않는다는 이 프로젝트의 원칙과 동일.)
 *
 * ⚠ 이 파일은 kis_hynix_foreign_ownership.py / merge 커맨드의 실제 CSV
 * 출력을 대상으로 작성됐다 — 컬럼명이 다르면 COLUMN_MAP만 고치면 된다.
 */

const COLUMN_MAP = {
  date: "date",
  close: "close",
  foreignPct: "foreign_hold_pct",
};

/** 아주 단순한 CSV 파서 — 이 프로젝트가 생성하는 CSV는 값에 콤마·따옴표가
 * 섞이지 않는 순수 숫자/날짜/영문 위주라 정규 CSV 파서(quoted field 처리
 * 등) 없이 split(",")만으로 충분하다. 다른 소스의 CSV(값에 콤마 포함
 * 가능성 있는)를 올릴 계획이면 papaparse 등으로 교체할 것. */
function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  if (lines.length < 2) return [];
  const headers = lines[0].split(",").map((h) => h.trim());
  return lines.slice(1).map((line) => {
    const cells = line.split(",");
    const row = {};
    headers.forEach((h, i) => {
      row[h] = cells[i] !== undefined ? cells[i].trim() : "";
    });
    return row;
  });
}

function toChartRows(rawRows) {
  return rawRows
    .map((r) => {
      const close = Number(r[COLUMN_MAP.close]);
      const pctRaw = r[COLUMN_MAP.foreignPct];
      return {
        date: r[COLUMN_MAP.date],
        close: Number.isFinite(close) ? close : null,
        foreignPct: pctRaw === "" || pctRaw === undefined ? null : Number(pctRaw),
      };
    })
    .filter((r) => r.date && r.close !== null)
    .sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0));
}

function formatKrw(v) {
  if (v === null || v === undefined) return "-";
  return `${Math.round(v).toLocaleString("ko-KR")}원`;
}

function formatPct(v) {
  if (v === null || v === undefined) return "미확인";
  return `${v.toFixed(2)}%`;
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || payload.length === 0) return null;
  const close = payload.find((p) => p.dataKey === "close");
  const pct = payload.find((p) => p.dataKey === "foreignPct");
  return (
    <div
      style={{
        background: "var(--tooltip-bg, #1b232e)",
        color: "var(--tooltip-fg, #e7edf3)",
        border: "1px solid #2c3644",
        borderRadius: 8,
        padding: "8px 12px",
        fontSize: 13,
      }}
    >
      <div style={{ fontWeight: 700, marginBottom: 4 }}>{label}</div>
      <div>주가: {close ? formatKrw(close.value) : "-"}</div>
      <div>외국인 보유율: {pct ? formatPct(pct.value) : "미확인(백필 공백 구간)"}</div>
    </div>
  );
}

export default function HynixForeignOwnershipChart() {
  const [rows, setRows] = useState([]);
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState("");

  const handleFile = useCallback((e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    setError("");
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (evt) => {
      try {
        const parsed = parseCsv(String(evt.target.result));
        const chartRows = toChartRows(parsed);
        if (chartRows.length === 0) {
          setError(
            "CSV를 읽었지만 유효한 행이 없습니다 — 컬럼명이 date/close/foreign_hold_pct와 " +
              "다르면 이 파일 상단 COLUMN_MAP을 실제 CSV 헤더에 맞게 고치세요."
          );
          setRows([]);
          return;
        }
        setRows(chartRows);
      } catch (err) {
        setError(`CSV 파싱 실패: ${err.message}`);
        setRows([]);
      }
    };
    reader.onerror = () => setError("파일을 읽는 중 오류가 발생했습니다.");
    reader.readAsText(file);
  }, []);

  const coveragePct = useMemo(() => {
    if (rows.length === 0) return null;
    const withPct = rows.filter((r) => r.foreignPct !== null).length;
    return (withPct / rows.length) * 100;
  }, [rows]);

  return (
    <div style={{ fontFamily: "-apple-system, BlinkMacSystemFont, sans-serif", padding: 16 }}>
      <h2 style={{ marginBottom: 4 }}>주가 + 외국인보유율 5년 추이</h2>
      <p style={{ color: "#8a96a3", fontSize: 13, marginTop: 0 }}>
        scripts/hynix_5y_history.py의 merge 결과 CSV(hynix_price_foreign_5y.csv)를
        업로드하세요. 좌축=주가(원), 우축=외국인 보유율(%). 하단 브러시로 구간을
        확대할 수 있습니다.
      </p>

      <input type="file" accept=".csv,text/csv" onChange={handleFile} />
      {fileName && (
        <span style={{ marginLeft: 8, fontSize: 13, color: "#8a96a3" }}>{fileName}</span>
      )}

      {error && (
        <div style={{ color: "#ff6b6b", marginTop: 12, fontSize: 13 }}>{error}</div>
      )}

      {rows.length > 0 && (
        <>
          <div style={{ fontSize: 13, color: "#8a96a3", margin: "8px 0" }}>
            {rows.length}거래일 로드됨 · 외국인보유율 매칭{" "}
            {coveragePct !== null ? `${coveragePct.toFixed(0)}%` : "-"}
            {coveragePct !== null && coveragePct < 90 && (
              <span style={{ color: "#ffb454" }}>
                {" "}
                (매칭률이 낮습니다 — foreign-ownership 백필이 부분적일 수 있습니다)
              </span>
            )}
          </div>

          <ResponsiveContainer width="100%" height={480}>
            <ComposedChart data={rows} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2c3644" />
              <XAxis
                dataKey="date"
                minTickGap={40}
                tick={{ fontSize: 11 }}
              />
              <YAxis
                yAxisId="price"
                orientation="left"
                tickFormatter={(v) => `${(v / 10000).toFixed(0)}만`}
                width={60}
              />
              <YAxis
                yAxisId="foreign"
                orientation="right"
                domain={["auto", "auto"]}
                tickFormatter={(v) => `${v}%`}
                width={50}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Line
                yAxisId="price"
                type="monotone"
                dataKey="close"
                name="주가(원)"
                stroke="#5ab0ff"
                dot={false}
                strokeWidth={1.5}
                connectNulls
              />
              <Line
                yAxisId="foreign"
                type="monotone"
                dataKey="foreignPct"
                name="외국인 보유율(%)"
                stroke="#ffb454"
                dot={false}
                strokeWidth={1.5}
                connectNulls={false}
              />
              <Brush dataKey="date" height={24} stroke="#5ab0ff" travellerWidth={8} />
            </ComposedChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
}
