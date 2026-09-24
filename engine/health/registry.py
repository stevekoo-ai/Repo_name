"""데이터 수집 블록 전수 인벤토리 — close-loop 데이터 헬스 시스템의 단일 출처.

## 왜 이 파일이 필요한가

사용자 요청: "데이터 수집 블럭 API 자동 수집 포함, 정상 작동 중인지 센싱하고,
신선도와 내용에 비정상이 확인되면 이것을 제어하는 기능을 추가해서 feedback이
있는 close-loop system을 만들자. 보고서가 항상 마음에 안들어!"

이 저장소는 지금까지 매번 "우연히 발견한" 사고를 하나씩 고쳐왔다 —
채권 누락(TR이 채권을 안 줌), 브리핑-거시수집 경쟁조건, 휴장갭 판정
버그, "해당 뉴스 없음"이 미검색과 안 구분됨... 전부 **누군가 우연히
알아챌 때까지 아무도 몰랐다.** 이 파일은 그 패턴 자체를 끊는다 —
"수집이 몇 개나 있고 각각 언제 살아있어야 하는지"를 코드가 알고 있어야
"조용히 죽었다"를 코드가 판정할 수 있다.

## 신선도 판정 방식 4가지 (실측 기반 — 추측 아님)

이 저장소의 실제 파일들을 조사한 결과 신선도를 알 수 있는 방법이
소스마다 다르다:

- `CSV_FETCHED_AT` — CSV에 `fetched_at` 컬럼이 있다(가장 정확, 가장 흔함).
- `CSV_LATEST_DATE` — `fetched_at`은 없고 `date` 컬럼만 있다(예:
  `data/normalized/customs_export_dlr.csv`). 이 경우 "며칠 전 데이터인가"는
  수집 시각이 아니라 **데이터 시차**를 재는 것이다 — 월간 지표라면 발표
  주기 자체가 몇 주씩이라 임계값을 그에 맞게 넉넉히 잡는다.
- `RUN_LOG` — 대상 파일 자체엔 시각 정보가 없지만
  `sources/automation-run-log.csv`(이미 6개 워크플로가 성공 시각을
  기록 중인 기존 인프라, 새로 안 만들고 재사용)에 (workflow, step) 쌍으로
  기록된다.
- `DATED_FILE_GLOB` — 파일명 자체에 날짜가 박힌다(`report/2026-09-15.md`
  같은 형태). 파일 존재 여부 자체가 신선도다 — mtime도 fetched_at도
  필요 없다.

## ⚠️ mtime을 안 쓰는 이유

GitHub Actions의 `actions/checkout`은 매 실행마다 새로 체크아웃하고,
그 순간 모든 파일의 mtime이 "체크아웃 시각"으로 재설정된다 — 즉
**os.path.getmtime()은 이 환경에서 "언제 실제로 수집됐는가"를 전혀
말해주지 않는다.** git 커밋 시각(`git log`)도 기본 체크아웃이 얕은
복제(depth=1)라 신뢰할 수 없다. 그래서 이 저장소가 이미 쓰고 있는
"콘텐츠 안에 시각을 남긴다"(fetched_at 컬럼, run-log) 방식만 쓴다.

## `data/normalized/*.csv`는 여기 등록하지 않는다

이 카테고리(ECOS/FRED/KOSIS/BLS/IMF/관세청/산업통상부가 (date,value)
형태로 떨어지는 시리즈, 232개)는 이미 `scripts/data_freshness_audit.py`가
**시리즈별로 발표 주기를 자동 추론**해 훨씬 정교한 신선도 판정을 하고
있었다(월간/분기 지표를 시간 단위 하드코딩 임계값으로 재는 것보다 낫다).
2026-09-15 실측 확인: **DEAD 22개·stale 18개가 이미 발견돼 있었는데
GitHub Actions 로그의 `::warning::` 한 줄로만 남고 그 다음(제어)이
없었다** — 이게 바로 이 close-loop 시스템이 메우려는 공백이다. 그래서
여기 개별 등록하는 대신 `check.py`가 `data_freshness_audit.audit()`을
직접 호출해 결과를 흡수한다(중복 판정 로직을 만들지 않는다).

## 거래일 예외

시장 데이터(하이닉스 가격, 지수, 포트폴리오)는 휴장일엔 새 데이터가
없는 게 정상이다. `market` 필드가 있으면 `engine.briefing.calendar`로
"마지막 거래일 데이터까지는 왔는가"만 확인하고, 오늘이 휴장이면 그
이상 요구하지 않는다 — 주말마다 우는 시스템은 곧 무시당한다.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class FreshnessMode(str, Enum):
    CSV_FETCHED_AT = "csv_fetched_at"
    CSV_LATEST_DATE = "csv_latest_date"
    RUN_LOG = "run_log"
    DATED_FILE_GLOB = "dated_file_glob"


@dataclass(frozen=True)
class SourceSpec:
    slug: str
    description: str
    workflow: str                       # 재발동 안내용 — 어느 .github/workflows/*.yml인지
    mode: FreshnessMode
    max_age_hours: float                # 이 이상 오래되면 STALE
    path: str | None = None             # CSV_FETCHED_AT / CSV_LATEST_DATE 용
    run_log_workflow: str | None = None  # RUN_LOG 용 (workflow 컬럼 값)
    run_log_step: str | None = None      # RUN_LOG 용 (step 컬럼 값)
    dated_glob_template: str | None = None  # DATED_FILE_GLOB 용, "report/{date}.md"
    dated_lookback_days: int = 3         # 오늘 파일이 없으면 며칠 전까지 인정할지
    market: str | None = None            # "KR" | "US" | None — 거래일 예외 적용 여부
    min_rows: int = 1                    # 콘텐츠 검증: 최소 행 수 (CSV만)
    required_columns: tuple[str, ...] = field(default_factory=tuple)  # 콘텐츠 검증
    severity: str = "warning"            # "critical" | "warning" — 알림 임계 다르게


# ── 인벤토리 (2026-09-15 전수 조사, .github/workflows/*.yml 실측) ──────────
#
# max_age_hours는 "cron 주기 + GitHub Actions 큐 지연 관측치(최대 약 2시간,
# wiki/log.md 2026-09-15 항목 참고) + 안전 마진"으로 잡는다 — cron 주기와
# 똑같이 잡으면 정상적인 지연에도 매번 오탐이 뜬다.

SOURCES: tuple[SourceSpec, ...] = (
    # ── 거시 지표 (FRED/ECOS) ──
    SourceSpec(
        slug="macro-series",
        description="거시 지표 (FRED·ECOS) — 금리·환율·유가·CPI 등",
        workflow="macro-data-sync.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/macro-series.csv",
        max_age_hours=30,  # cron 2회(20:15/22:10 UTC) 중 하나는 24시간 내 반드시 성공해야
        required_columns=("series", "date", "value", "provider", "fetched_at"),
        severity="critical",  # 브리핑 전체가 이 데이터로 돈다
    ),
    # ── SK하이닉스 시세·수급 (KIS API, 하루 3회) ──
    SourceSpec(
        slug="hynix-price-snapshot",
        description="SK하이닉스 시세 스냅샷",
        workflow="sk-hynix-daily-report.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/sk-hynix-price-snapshot.csv",
        max_age_hours=30,
        market="KR",
        required_columns=("date", "ticker", "price", "change_pct", "fetched_at"),
        severity="critical",
    ),
    SourceSpec(
        slug="hynix-investor-flow",
        description="SK하이닉스 투자자별 매매동향",
        workflow="sk-hynix-daily-report.yml",
        mode=FreshnessMode.RUN_LOG,
        run_log_workflow="sk-hynix-daily-report",
        run_log_step="investor_flow_fetch",
        max_age_hours=30,
        market="KR",
        min_rows=1,
        required_columns=("date", "ticker", "foreign_net_qty"),
        severity="warning",
    ),
    SourceSpec(
        slug="hynix-adr-quote",
        description="SK하이닉스 ADR 시세",
        workflow="sk-hynix-daily-report.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/sk-hynix-adr-quote.csv",
        max_age_hours=48,  # ADR은 미국 세션 종가라 하루 지연이 정상적일 수 있음
        market="US",
        required_columns=("date", "symbol", "price", "fetched_at"),
        severity="warning",
    ),
    SourceSpec(
        slug="hynix-credit-balance",
        description="SK하이닉스 신용융자 잔고",
        workflow="sk-hynix-daily-report.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/sk-hynix-credit-balance.csv",
        max_age_hours=30,
        market="KR",
        required_columns=("date", "ticker", "loan_balance_qty", "fetched_at"),
        severity="warning",
    ),
    SourceSpec(
        slug="hynix-short-sale",
        description="SK하이닉스 공매도 현황",
        workflow="sk-hynix-daily-report.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/sk-hynix-short-sale.csv",
        max_age_hours=30,
        market="KR",
        required_columns=("date", "ticker", "short_qty", "fetched_at"),
        severity="warning",
    ),
    SourceSpec(
        slug="kr-index-quote",
        description="코스피/코스닥 지수",
        workflow="sk-hynix-daily-report.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/kr-index-quote.csv",
        max_age_hours=30,
        market="KR",
        required_columns=("date", "index_code", "price", "fetched_at"),
        severity="warning",
    ),
    SourceSpec(
        slug="portfolio-etf-nav",
        description="ETF NAV·괴리율 (커버드콜 침식률 실측용)",
        workflow="sk-hynix-daily-report.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/portfolio-etf-nav.csv",
        max_age_hours=30,
        market="KR",
        required_columns=("date", "ticker", "nav", "fetched_at"),
        severity="warning",
    ),
    # ── 포트폴리오 보유 현황 (KIS API, 19:10 KST 1회) ──
    SourceSpec(
        slug="portfolio-holdings",
        description="증권 계좌 보유 종목",
        workflow="portfolio-holdings-sync.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/portfolio-holdings.csv",
        max_age_hours=30,
        market="KR",
        required_columns=("date", "account_label", "ticker", "quantity", "fetched_at"),
        severity="critical",  # 자금 조달 실행 계획(engine/execution/plan.py)이 이 위에서 돈다
    ),
    SourceSpec(
        slug="portfolio-bonds",
        description="장내채권 잔고 (2026-09-12 신규 — 과거 누락 사고 재발 방지 대상)",
        workflow="portfolio-holdings-sync.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/portfolio-bonds.csv",
        max_age_hours=30,
        market="KR",
        required_columns=("date", "account_label", "ticker", "maturity", "fetched_at"),
        severity="critical",
    ),
    # ── 하이퍼스케일러 CapEx (SEC EDGAR, 주 1회) ──
    SourceSpec(
        slug="hyperscaler-capex",
        description="빅테크 CapEx (SEC EDGAR XBRL)",
        workflow="sec-edgar-capex.yml",
        mode=FreshnessMode.RUN_LOG,
        run_log_workflow="sec-edgar-capex",
        run_log_step="capex_fetch",
        max_age_hours=24 * 9,  # 주 1회 cron, 실행 자체가 안 됐는지만 감시(분기 실측은 원래 몇달 지연)
        required_columns=("company", "ticker", "value_usd", "fetched_at"),
        severity="warning",
    ),
    SourceSpec(
        slug="ai-periphery-fundamentals",
        description="AI 밸류체인 변두리 펀더멘털 (SEC EDGAR)",
        workflow="sec-edgar-capex.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/ai-periphery-fundamentals.csv",
        max_age_hours=24 * 9,
        required_columns=("company", "ticker", "value_usd", "fetched_at"),
        severity="warning",
    ),
    # 2026-09-24 추가 — 병목 이동 추적(engine/bottleneck/rotation.py) 주가.
    # macro-data-sync.yml 안에서 매일 두 번 돌지만 실패해도 잡을 죽이지 않게
    # 설계했으므로, 조용한 실패는 여기 fetched_at 신선도로만 잡힌다.
    SourceSpec(
        slug="bottleneck-prices",
        description="병목 이동 추적 주가 (Yahoo — 전력·광통신·NAND·하이닉스)",
        workflow="macro-data-sync.yml",
        mode=FreshnessMode.CSV_FETCHED_AT,
        path="sources/bottleneck-prices.csv",
        max_age_hours=50,
        required_columns=("ticker", "date", "close", "fetched_at"),
        severity="warning",
    ),
    # ── 부동산 실거래가 (국토부, 매일 03:00 KST) ──
    SourceSpec(
        slug="real-estate-apartment-sale",
        description="아파트 매매 실거래가 (국토부)",
        workflow="real-estate-sync.yml",
        mode=FreshnessMode.RUN_LOG,
        run_log_workflow="real-estate-sync",
        run_log_step="apartment_sale",
        max_age_hours=30,
        severity="warning",
    ),
    SourceSpec(
        slug="real-estate-apartment-rent",
        description="아파트 전월세 실거래가 (국토부)",
        workflow="real-estate-sync.yml",
        mode=FreshnessMode.RUN_LOG,
        run_log_workflow="real-estate-sync",
        run_log_step="apartment_rent",
        max_age_hours=30,
        severity="warning",
    ),
    # ── 청약 모니터 (자체 close-loop 보유 — 여기선 심박만 표시) ──
    SourceSpec(
        slug="subscription-monitor",
        description="청약 모니터 (자체 health_state.json 보유 — 심박만 대조 표시)",
        workflow="subscription-monitor.yml",
        mode=FreshnessMode.RUN_LOG,
        run_log_workflow="subscription-monitor",
        run_log_step="heartbeat",  # 실제로는 자체 JSON을 별도 로직에서 읽음(check.py)
        max_age_hours=3,  # 30분 cron
        severity="warning",
    ),
    # ── 일일 리포트 산출물 (파일명에 날짜가 박힘) ──
    SourceSpec(
        slug="peos-daily-report",
        description="PEOS 일일 경제판단 리포트",
        workflow="daily-peos-report.yml",
        mode=FreshnessMode.DATED_FILE_GLOB,
        dated_glob_template="report/{date}.md",
        dated_lookback_days=2,
        max_age_hours=30,
        severity="critical",  # 이게 사용자가 매일 받는 그 보고서다
    ),
    SourceSpec(
        slug="subscription-daily-report",
        description="청약 일일 리포트",
        workflow="subscription-daily-report.yml",
        mode=FreshnessMode.DATED_FILE_GLOB,
        dated_glob_template="report/subscription-report-{date}.md",
        dated_lookback_days=2,
        max_age_hours=30,
        severity="warning",
    ),
)


def by_slug(slug: str) -> SourceSpec:
    for s in SOURCES:
        if s.slug == slug:
            return s
    raise KeyError(f"등록되지 않은 소스: {slug}")
