# CXL Ecosystem Newsroom Landscape

> 30개 CXL 생태계 기업의 공식 newsroom/press release 채널 전수 조사 (2026-08-10).
> CXL Newsroom Collector 구축의 1차 소스 맵. 모든 URL은 WebFetch로 실제 검증.

---

## TL;DR

- **WebFetch 직접 수집 가능: 18/30** (영문 글로벌 newsroom)
- **대체 채널 필요: 12/30** (한국 공시 DART/KIND, 헤드리스 브라우저, PR 배포플랫폼, Marvell 흡수)
- **CXL 직접 신호 밀집: 9개사** — 컨트롤러·IP·메모리·검사장비 벤더에 집중
- **Host/Hyperscaler 9개사는 CXL 직접 언급 0건** — 간접(데이터센터/인프라) 신호만
- **뉴스룸은 매일 올라오지 않음** → 일일 발행은 빈 날이 대부분 → 주간 롤업이 자연스러움

---

## 1. 수집 방법별 분류 (설계의 핵심)

### Tier 1 — WebFetch 직접 연동 (정적 HTML, 자동화 가장 쉬움)

| 기업 | 카테고리 | newsroom URL | 형태 | CXL 신호 |
|------|----------|--------------|------|----------|
| Intel | Host | https://newsroom.intel.com/ | (a) PR 목록 | 없음 |
| AMD | Host | https://newsroom.amd.com/ | (a) PR 목록 | 없음 (HBM4 언급) |
| NVIDIA | Host | https://blogs.nvidia.com/ (실질) | (b) 블로그 | 간접 (메모리) |
| Qualcomm | Host | https://www.qualcomm.com/news/releases | (a) PR 목록 | 없음 |
| Microsoft | Host | https://blogs.microsoft.com/ | (b) 블로그 | 간접 (Azure HPC) |
| Google | Host | https://blog.google/ | (b) 블로그 | 없음 (날짜 미표시) |
| Meta | Host | https://about.fb.com/news/ | (a) PR 피드 | 간접 (data center) |
| AWS | Host | https://aws.amazon.com/blogs/aws/ | (b) 블로그 | 없음 |
| Alibaba | Host | https://www.alizila.com/ | (b/d) 에디토리얼 | 간접 (Alibaba Cloud, 날짜 sparse) |
| Astera Labs | Controller | https://www.asteralabs.com/newsroom/ | (a) PR 목록 | 있음 (Leo CXL 라인 별도; 최근은 PCIe/Scorpio) |
| Marvell | Controller | https://www.marvell.com/company/newsroom.html | (a) newsroom 통합 | 있음 (XConn 인수→CXL, AI Memory Portfolio) |
| Montage | Controller | https://www.montage-tech.com/Press_Releases | (a) PR 아카이브 | 있음 (CXL 3.2 MXC, CXL 3.x AEC) |
| Panmnesia | Controller | https://panmnesia.com/news/ | (a) PR 아카이브 | **있음 (가장 CXL 특화 — Fusion Switch, CXL 3.2 ASIC)** |
| Primemas | Controller | https://primemas.com/company/press.php | (a) PR 리스트 (한국어, 언론링크) | 있음 (CXL 메모리 컴퓨팅, 삼성/ETRI 협력) |
| Rambus | IP/EDA | https://www.rambus.com/news/ | (a) PR 목록 | 있음 (DDR5/HBM4E/SOCAMM2) |
| Synopsys | IP/EDA | https://www.synopsys.com/company/newsroom.html | (a) PR 목록 | 없음 (상위 6개) |
| Samsung | Memory | http://news.samsungsemiconductor.com/global/ | (a) PR 목록 | 있음 (FMS 2026 zHBM/zNAND-O) |
| SK hynix | Memory | https://news.skhynix.co.kr/ | (a)+(b) 혼합 | 있음 (FMS 2026, PIM, HBF) |
| Micron | Memory | https://www.micron.com/news | (a) PR 목록 | 간접 (Memory Supply) |
| Penguin Solutions (구 SMART Modular) | Memory | https://www.penguinsolutions.com/en-us | (a) PR 목록 | 있음 (CXL KV Cache Server, HBM/CXL Playbook) |
| H3 Platform | SW | https://www.h3platform.com/ | (a) PR (루트 임베드) | 있음 (CXL Pooling 5TB, FMS 2025) |
| 네오셈 | PCB/Test | https://www.neosem.com/ | (c) IR+제품news | 있음 (CXL 2.0 검사장비 세계 최초 양산 2024-07-30) |
| 엑시콘 | PCB/Test | https://www.exicon.co.kr/ | (c) IR 공시 | 없음 (공시 2개만) |

### Tier 2 — 대체 채널 필수 (WebFetch 불가)

| 기업 | 카테고리 | 사유 | 대체 채널 |
|------|----------|------|-----------|
| Microchip | Controller | 403 (봇 차단) | globenewswire/businesswire, SEC 8-K |
| XConn | Controller | 403 + Marvell 인수 흡수 (2026-02-10) | Marvell newsroom에서 XConn 키워드 추적 |
| FADU | Controller | 공식 도메인 미확실 (fadu.com placeholder) | KIND/DART, 한국 언론 (전자신문/디지털데일리) |
| EEUM | Controller | 공식 도메인 미확실 (eeum.com은 동명이인 커뮤니티) | KAIST spin-off 디렉토리, 한국 언론 |
| Cadence | IP/EDA | 403 (Akamai WAF) | 헤드리스 브라우저(Playwright), RSS, Google News site:쿼리 |
| OpenEdge | IP/EDA | 공식 사이트 미출시 (openedge-ai.com "Launching Soon") | SK hynix CXL 컨소시엄 발표 자료 간접 |
| Qualitas | IP/EDA | 503 | DART/KIND 공시 |
| MemVerge | SW | JS SPA (정적 fetch 빈 콘텐츠) | Playwright 헤드리스, PR Newswire, medium/Substack 블로그 |
| 티엘비 | PCB/Test | 자체 newsroom 미운영 (루트만 접근) | DART 공시 |

---

## 2. CXL 신호 밀도별 분류 (보고서 가중치 설계용)

### 🔴 CXL 직접 신호 (9개사 — 보고서 핵심 섹션)
제품 발표/양산/컨소시엄에서 "CXL" 명시. 이들이 보고서의 본질적 콘텐츠.

1. **Panmnesia** — CXL 3.2 Fusion Switch ASIC, ISCA/ISPASS 발표 (가장 밀도 높음)
2. **Montage** — CXL 3.2 MXC 칩 시료 생산, CXL 3.x AEC
3. **Marvell** — XConn 인수로 CXL 역량 확장, Structera CXL portfolio
4. **Primemas** — 삼성/ETRI와 CXL 기반 메모리 컴퓨팅, JBOM 양산
5. **Penguin Solutions** — CXL KV Cache Server 양산 (최초 production-ready)
6. **H3 Platform** — CXL Memory Sharing/Pooling 5TB
7. **Neosem** — CXL 2.0 검사장비 세계 최초 양산 출하
8. **SK hynix** — FMS 2026 차세대 메모리 아키텍처 (CXL/메모리 방향성)
9. **Samsung** — FMS 2026 zHBM/zNAND-O, 3D-Memory Vision

### 🟡 간접 신호 (메모리/반도체/데이터센터, CXL 미명시)
- Rambus (메모리 IP 전체), Astera (Leo CXL 라인 존재하나 최근은 PCIe), Micron (Memory Supply)
- NVIDIA, Microsoft, Meta, Alibaba (데이터센터/인프라)

### ⚪ 신호 없음 / 확인 불가
- Intel, AMD, Qualcomm, Google, AWS, Synopsys (상위 게시물에 CXL/메모리 없음)
- Cadence, Microchip, FADU, EEUM, OpenEdge, Qualitas, MemVerge, TLB (접근 불가로 미확인)

---

## 3. 페이지 형태 분류

- **(a) press release 목록**: Intel, AMD, Qualcomm, Meta, Astera, Marvell, Montage, Panmnesia, Primemas, Rambus, Synopsys, Samsung, Micron, Penguin, H3, 네오셈 — **가장 많음 (16)**. 제목+날짜 리스트 → 자동 파싱 용이.
- **(b) 블로그 게시물 목록**: NVIDIA, Microsoft, Google, AWS, Alibaba, MemVerge(예상) — 6. 본문 중심.
- **(c) IR 공시**: 네오셈, 엑시콘, 퀄리타스(예상) — 한국 기업. DART 보완 필수.
- **(d) 마케팅 페이지뿐(뉴스 없음)**: TLB, FADU, OpenEdge, Alibaba(일부) — 자체 newsroom 미운영.

---

## 4. 날짜 노출 이슈 (자동화 장애물)

- **목록에 날짜 미표시**: Google (blog.google), Alibaba (alizila.com) → 개별 기사 URL 크롤링 필요
- **최신 갱신 지연**: 네오셈 (최신 2024-12), 엑시콘 (공시 2개만) → DART 공시로 최신 보완
- **search 쿼리 URL 차단**: Intel (403), AMD (JS 렌더링) → 본문은 되나 검색 API 불가 → 전체 피드 순회 후 로컬 필터링 필요

---

## 5. 자동화 설계 시사점

1. **2-tier 파이프라인**: Tier 1(WebFetch 직접) + Tier 2(공시/헤드리스/PR배포플랫폼) 분리 구축
2. **한국 비상장/팹리스 5개사** (네오셈/엑시콘/TLB/퀄리타스/오픈엣지) → DART OpenAPI + KIND RSS 별도 파이프라인
3. **Cadence/MemVerge** → Playwright 헤드리스 브라우저 또는 PR Newswire/Business Wire 서드파티 피드
4. **XConn** → Marvell newsroom에서 XConn 키워드 추적만 실질적 (독립 수집 무의미)
5. **CXL 직접 신호 9개사** → 보고서 핵심 섹션, 발표 즉시 이벤트 트리거 알림 후보
6. **Host 9개사** → CXL 직접 신호 없음, 데이터센터/인프라 맥락 부록 처리 (또는 제외 후보)
7. **주간 롤업이 자연스러움** — 일일 발행은 빈 날이 대부분

---

## 6. 조사 방법론 비고

- WebSearch 도구가 현재 환경에서 tool_choice 스키마 에러로 완전 장애 → WebFetch만으로 조사
- 각 기업당 1차 URL 실패 시 폴백 URL 1-2개 시도
- 30개 전수 조사를 3개 병렬 에이전트로 분할 (Host 9 / Controller 9 / Memory·IP·SW·PCB 14)
- 실패 4개사(Microchip/XConn/FADU/EEUM) + 5개사(Cadence/OpenEdge/Qualitas/MemVerge/TLB)는 WebSearch 복구 시 도메인/접근 재확인 권장

---

## Sources

- 3개 병렬 조사 에이전트 WebFetch 결과 (2026-08-10)
- wiki/concepts/cxl-controller-vendor-landscape.md (vendor URL 기준점)
- 사용자 제공 30개 기업 6카테고리 리스트

---

## 구축 완료 (2026-08-11)

본 landscape를 기반으로 **CXL Newsroom Collector** 자동화 파이프라인 구축:

- `scripts/cxl_newsroom_collector.py` — 결정론적 Python 수집 (Tier 1 WebFetch
  + Tier 2 DART 공시/PR 배포플랫폼 RSS/XConn 키워드 필터)
- `.claude/prompts/cxl-newsroom-update.md` — 시스템 프롬프트 (절차+보고서구조)
- `prompts/cxl-newsroom-update-headless.txt` — 헤드리스 실행본문
- `scripts/run_cxl_newsroom_bounded.ps1` — hang-fix PS 래퍼 (CR1-CR11 복제)
- `scripts/cxl_newsroom_routine.bat` — 오케스트레이션 (git sync → 수집 → 해석, 로컬 산출물 생성)
- `scripts/register_cxl_newsroom_task.py` — schtasks 등록 (06:45 KST 매일)

**수집 실측 (2026-08-11)**: Tier 1 21개사 중 19개사 게시물 추출 성공
(BeautifulSoup 기반). Qualcomm(8842바이트, JS 렌더링 본문 부재), Panmnesia(날짜
포맷 특수)는 원시 데이터에 "0 posts (err)"로 한계 공개 — headless claude가
보고서 작성 시 WebFetch로 보완.

**운영**: schtasks `Steve_CXL_Newsroom_Update` 매일 06:45 KST (CXL Daily Update
06:30 직후). 다음 실행 2026-08-12 06:45.

**미해결**:
- DART_API_KEY 미설정 → 한국 5개사(네오셈/엑시콘/TLB/퀄리타스/오픈엣지) 공시
  수집 graceful skip (한계 공개). 키 등록 시 자동 활성화.
- DART corp_code 5개사 미확정 → DART_API_KEY 등록 후 corp_code 조회 필요.
- Qualcomm/Panmnesia 사이트별 파싱 개선 (현재 한계 공개 상태).
