# customer-meetings/ — 고객·파트너 미팅 인텔리전스 분류

> **1차 현장 인텔리전스 보존 영역.** log.md(일일 작업 로그, 자동 회전 대상)가 아닌
> 미팅 전문·상대방별 누적 이력 전용 분류. Daily Update(웹 스위프 delta)와 다른
> 비공개 미팅 발언 기반 1차 자료.

## 구조 (2-tier)

```
customer-meetings/
├─ README.md          ← 본 파일 (규칙·네이밍)
├─ index.md           ← 2뷰 마스터 인덱스 (미팅 목록 + 상대방별 교차표)
├─ meetings/          ← 미팅별(날짜키, 변경 불가, 전문)
│  └─ YYYY-MM-DD-<slug>.md
└─ by-customer/       ← 상대방별 누적 (현재 상태 + 모든 미팅 이력, append)
   └─ <customer-slug>.md
```

### 두 접근 경로 (many-to-many)
- **미팅별 보기** = `meetings/` (한 미팅에 여러 상대방 동시 발언의 전체 맥락)
- **상대방별 보기** = `by-customer/` (한 상대방의 모든 미팅 누적 + 현재 관계 상태)
- 같은 사실이 양쪽에 나오되, **전문은 meetings/가 단일 출처**, by-customer/는 요약+상태.

## 상대방 범위 (relation)
- **customer**: 구매하는 고객 (MSFT·Oracle·NVIDIA 등)
- **partner**: 협력 파트너 (Marvell·Liqid·Intel·AMD·Qualcomm·ScaleFlux·Panmnesia·Primemas·Penguin 등)
- **competitor**: 추적 경쟁사 (Micron·Samsung·Kioxia 등)
- 한 미팅에 여러 relation이 섞여도 각각 by-customer 파일로 분리.

## 네이밍 규칙
- **meetings/**: `YYYY-MM-DD-<slug>.md` (slug = 미팅 주제 kebab-case. 예: `2026-08-11-cxl-pooling.md`)
- **by-customer/**: `<customer-slug>.md` (회사 소문자 kebab. 예: `nvidia.md`, `msft.md`)
  - 사내 약칭 우선(msft/nvidia), 정식명은 title 필드에.
  - 원문 표기 변형(Pamnesia/Pamnensia)은 title에 "(원문 표기)" 명시, 파일명은 정규 슬러그 `panmnesia`.

## Ingest 절차 (새 미팅 들어올 때)
1. 원문 → `sources/` (immutable, 새 파일만)
2. 전문 + 핵심 정리 → `meetings/YYYY-MM-DD-<slug>.md` (신규)
3. 등장하는 모든 상대방 → `by-customer/<customer>.md` 갱신:
   - "미팅 이력"에 1줄 append (날짜·참석·핵심·전문 링크·★·DRAFT 챕터)
   - "현재 관계 상태"·"핵심 팩트" 갱신 (최신 미팅 기준)
   - 신규 상대방이면 파일 생성 (frontmatter + 현재 상태 + 이력 1건)
4. `index.md` 갱신 (미팅 목록 1줄 + 교차표 행 추가)
5. `wiki/index.md` customer-meetings 섹션 갱신
6. `wiki/log.md` `## 당일 log` 맨 아래 1줄 INGEST (R1 준수)

## CXL DRAFT 연결
- by-customer 핵심 팩트는 DRAFT 챕터로 연결 (3장 컨트롤러·4장 풀링·5장 CPU/GPU·6장 AI 패브릭·7장 Main Memory·9장 KV offload·11장 시장 인텔리전스·12장 상품기획).
- ★★★/★★/★ 영향도 표기. DRAFT 본문 반영은 정규 .md 경로 복구 후 일괄 (3호 한계 #3 준수).

## 데이터 한계 공개 원칙
- 1차 미팅 발언 = 단일 출처. 외부 교차검증 미수행 명시.
- 추정(M사=Micron 등)은 확정 전 "(추정)" 명시, 확정 시 정정.
- 원문 표기 변형(Pamnesia/famfs 등)은 정정 시 "(FAMS→famfs 정정)" 식으로 추적 가능 명시.

## Local-only 정책 (2026-08-11 사용자 지시)
- github push 안 함. 모든 파일 local working tree에만. push 필요 시 사용자 확인 후.
