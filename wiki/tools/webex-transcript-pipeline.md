# WebEx Transcript Processing Pipeline

> WebEx 미팅 녹음 → Whisper 전사 → 정제 → 오류 교정 → LLM 분류/번역 파이프라인

---

## 전체 흐름 (5단계)

```
[1] 녹음              python webex_recorder.py --auto 60
[2] 전사(Whisper)     (자동 실행, medium 모델 기준 1시간 ≈ 30분)
[3] 문장 분리         format_transcript.py (자동 실행)
[4] 오류 교정         correct_transcript.py (자동 실행, JSON LUT)
[5] LLM 분류/번역     transcribe_to_llm.py (수동 또는 API 설정 시 자동)
```

각 단계는 **새로운 파일 생성** (원본 보존, 롤백 가능)

---

## 빠른 시작

### AUTO 모드 (권장 ⭐)

```bash
python webex_recorder.py --auto 60
```

| 파라미터 | 설명 |
|---|---|
| `--auto 60` | 60초 녹음 후 전사·정제·교정 자동 실행 |
| `--auto 30` | 30초 테스트용 |
| `--auto 120` | 2분 녹음 |

`--auto N`을 지정하면:
1. 60초 단위로 N초 동안 WebEx 녹음
2. **Whisper 전사** (CPU multithread, SSL 패치 적용)
3. **문장 분리** (`. ! ?` 기준 줄바꿈)
4. **오류 교정** (JSON LUT v2, priority 기반 매칭)
5. 파일명 컨벤션: `webex-transcript-{time}.txt` → `*-formatted.txt` → `*-corrected.txt`

### 수동 모드

```bash
# 메뉴에서 옵션 선택
python webex_recorder.py
# 1: AUTO | 2: MENU (수동 설정)
```

---

## 단계별 명령어 (수동 실행)

### Step 1: 녹음

```bash
python webex_recorder.py --record 120     # 120초 녹음
python webex_recorder.py --record 3600   # 1시간 녹음
```

출력: `webex-audio/webex-transcript-{timestamp}.wav`

### Step 2: 전사 (Whisper)

```bash
python webex_transcribe.py webex-audio/webex-transcript-{timestamp}.wav
```

| 옵션 | 설명 |
|---|---|
| 모델 (default: medium) | `tiny` (빠름·정확도↓) / `base` / `small` / `medium` (기본) / `large` (느림·정확도↑) |
| CPU multithread | 자동 감지 (CPU 코어 × 2 스레드, 최소 8) |
| 진행률 | 실시간 출력 (subprocess PIPELINE + PYTHONUNBUFFERED) |

출력: `webex-audio/webex-transcript-{timestamp}.txt`

### Step 3: 문장 분리

```bash
python format_transcript.py "webex-audio/webex-transcript-{timestamp}.txt"
```

- `. ! ?` 기준 문장 분리
- 약어 인식 (mr, mrs, dr 등) — false split 방지
- 장문 자동 분할 (>400자)
- `*-formatted.txt` 생성 (중복 파일 건너뜀)

### Step 4: 오류 교정 (JSON LUT v2)

```bash
python correct_transcript.py "webex-audio/webex-transcript-{timestamp}-formatted.txt"
python correct_transcript.py "webex-audio/webex-transcript-{timestamp}-formatted.txt" --learn  # 자동 학습
```

- **JSON LUT v2** 기반 교정 (56개 패턴, 4 priority 레벨)
- priority 1: 고정 구문 (18개) — "in hardships" → "in partnerships"
- priority 2: 중간 패턴 (28개) — "kv cash" → "KV cache"
- priority 3: 단일 단어 (5개) — "marvel" → "Marvell"
- priority 4: 문맥 기반 (5개) — "cash" 주변에 "kv" 있으면 → "cache"

**`--learn` 옵션** — 교정 전/후를 비교하여 LUT 가 처리하지 못한 신규 교정쌍을 자동 감지하여 LUT JSON 에 병합
- `--auto` 모드에서는 자동으로 `--learn` 실행
- manual: `python correct_transcript.py file.txt --learn`

출력: `webex-transcript-{timestamp}-corrected.txt`
통계 출력: 각 priority별 교체 횟수 + 자동 학습 결과

### Step 5: LLM 분류/번역

```bash
python transcribe_to_llm.py "webex-audio/webex-transcript-{timestamp}-corrected.txt"
```

- LLM_API_ENDPOINT 환경변수 필요
- 카테고리 분류 + 한줄 영문/한줄 한국어 번역
- Q&A BOX 포함
- `*-final.md` 생성

---

## LUT 업데이트 (2 가지 방법)

### 방법 1: 자동 학습 (`--learn`) — 권장 ⭐

`correct_transcript.py --learn` 이 교정 전/후를 비교하여 미처리 교정쌍을 자동 감지, LUT 에 병합

```bash
python correct_transcript.py file.txt --learn
python webex_recorder.py --auto 30  # --auto 모드에서는 자동으로 --learn 실행
```

**동작 방식**:
1. 교정 전 (`*-formatted.txt`) / 교정 후 (`*-corrected.txt`) 행 단위 비교
2. `SequenceMatcher` 로 word-level 매칭 → 기술 관련 교정쌍 추출
3. LUT 가 처리한 것 외의 신규 교정쌍만 필터
4. LUT JSON 에 자동 병합 (`reason: "auto-learner"`)

### 방법 2: 수동 txt 추가 (`upgrade_lut.py`)

txt 파일 (`Error_correction_word_LUT.txt`) 에 새로운 오류 쌍을 추가:

```
wrong term | correct term
```

예시:
```
# 주석은 무시됨
in hardships | in partnerships
one hyperskiller | one hyperscaler
```

```bash
python upgrade_lut.py webex-audio/Error_correction_word_LUT.txt
```

- `|` 구분자 = 교정 규칙
- 구분자 없는 줄 = 용어집 (vocabulary)
- `#` 시작 줄 = 주석
- 기존 JSON 중복 규칙 자동 skip

---

## 파일 컨벤션

```
webex-audio/
├── webex-transcript-{timestamp}.wav        # 원본 녹음
├── webex-transcript-{timestamp}.txt        # 전사 원문
├── webex-transcript-{timestamp}-formatted.txt    # 문장 분리
├── webex-transcript-{timestamp}-corrected.txt    # 오류 교정
└── webex-transcript-{timestamp}-final.md         # LLM 분류/번역
```

**각 단계가 새 파일을 생성** — 원본은 절대 변경되지 않음

---

## 환경 설정

### Whisper 모델 다운로드 (사내 네트워크)

처음 실행 시 모델 다운로드 필요. 사내 MITM 프록시 문제 있음 —
`webex_transcribe.py`가 자동 패치 (`ssl.CERT_NONE`) 적용.

### LLM API

```bash
set LLM_API_ENDPOINT=http://your-api-endpoint/v1/chat/completions
```

---

## 비교 표

| 방법 | 속도 | 자동성 | 추천도 |
|---|---|---|---|
| `--auto N` | ⚡ 자동 | ⭐ 최고 | ⭐⭐⭐ |
| 단계별 수동 | ⚠️ 수동 | ⚠️ 낮음 | ⭐⭐ |
| `fix_all_transcripts.py` | batch | ⚡ 자동 | ⭐⭐ (기존 파일 일괄 처리) |

---

**생성일**: 2026-08-25
**검증**: JSON LUT v2 56개 패턴 테스트 완료 (48교정, 48개 파일 성공)

---

## RAG-LUT: Attention 기반 교정 (2026-08-25 신규 ⭐)

### 개념

"Attention is all you need" Transformer 원리를 LUT 교정에 적용.
기존 순차 적용 (56개 규칙 전부 필터 없이) 대신,
**각 텍스트 청크의 semantic context(Q) ↔ LUT 규칙 semantic(K)** 의
cosine similarity 로 관련 규칙만 retrieval 하여 적용.

### Transformer 매핑

| Transformer | RAG-LUT |
|---|---|
| **Query** | 현재 텍스트 청크의 TF-IDF embedding |
| **Key** | 각 LUT 규칙 (`match + reason + condition`) embedding |
| **Score** | cosine similarity (Q·K) |
| **Value** | 규칙의 replace 값 (실제 교정 적용) |

### 동작 방식

1. 텍스트를 ~200자 청크로 분할
2. 각 청크 ↔ LUT 규칙 cosine similarity 계산
3. 상위 K 개 관련 규칙만 해당 청크에 적용
4. 청크 결과 다시 조립

**안전 이중 계층**:
- **p1/p2 (정확한 구문, 결정적 오류)** → 항상 적용 (회귀 안전)
- **p3(단어)/p4(context)** → RAG retrieval 후 선택 적용
  - 예: "cash→cache" 를 돈 관련 청크엔 적용하지 않음

### 사용법

```bash
# 수동
python correct_transcript.py file.txt --rag
python correct_transcript.py file.txt --rag --topk 10

# AUTO 모드 (webex_recorder.py --auto 에서 자동 전달)
python webex_recorder.py --auto 30
```

**`--topk N`**: 각 청크에서 가져올 규칙 수 (기본 5)
- 더 많은 규칙: recall ↑, 속도를 위한 trade-off

### 성능

- **TF-IDF 임베딩**: numpy 기반, 설치 불요 (pure-python, 178-dim vocab)
- **지연 시간**: 100KB 전사 ≈ 0.2s (로컬 CPU)
- **추천도**: 기술 용어 교정 품질 ↑ (문맥 오적용 ↓)

### 비교: Classic vs RAG

| | Classic LUT | RAG-LUT |
|---|---|---|
| 적용 방식 | 전역 순차 | 청크별 retrieval |
| p1/p2 | always-on | always-on (동일) |
| p3/p4 | 전역 적용 | 문맥 기반 선택 |
| 오적용 가능성 | 높음 | 낮음 |
| 속도 | 빠름 | 약간 느림 (~2x) |
| 의존성 | 없음 | numpy |

**`--rag` 모드에서는 `--learn` 과 동시에 동작** (webex_recorder.py --auto)

---
