# WebEx Transcript Processing — Architecture & Design

> WebEx 미팅 녹음 → Whisper 전사 → 정제 → 오류 교정 → LLM 분류 파이프라인의 설계 철학, 아키텍처, 구현 디테일

**최신 업데이트**: 2026-08-25 — RAG-LUT (Transformer Attention 원리) + MP4 자동 파이프라인 + Anthropic SDK 기반 번역 개편

---

## Overview

### 문제 정의

WebEx 미팅 전사는 여러 복잡한 단계를 거치며 각 단계에서 오류가 발생:
1. **녹음**: ffmpeg dshow → WAV
2. **전사**: Whisper CPU → phonetic error (예: "cash" ↔ "cache")
3. **정제**: 줄바꿈 없음, 장문 연속 텍스트
4. **교정**: Whisper의 동음이의 오인식, 고유명사 철자 오류
5. **분류/번역**: LLM이 전체 텍스트를 읽고 맥락 기반 분류

### 설계 원칙

1. **파일 분리 (분리된 산출물)** — 각 단계가 **새로운 파일** 생성, 원본 보존
2. **롤백 가능** — 각 단계의 출력이 독립 파일이므로 중간 단계로 복귀 가능
3. **JSON LUT v2** — 단순 텍스트가 아닌 **우선순위 + 조건** 기반 교정
4. **LLM 활용** — 정규식으로 해결 못 하는 문맥 판단은 LLM에 위임

---

## 아키텍처

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  녹음       │───▶│  전사(Whisper)│───▶│  문장 분리   │
│ ffmpeg      │    │ CPU multithread│   │ format_*.py  │
└─────────────┘    └──────────────┘    └──────────────┘
                                                │
                                                ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  LLM 분류   │◀───│  오류 교정   │◀───│  전사 원문   │
│ transcribe  │    │ JSON LUT v2  │    │  *.txt       │
│ _to_llm.py  │    │ correct_*.py │    └──────────────┘
└─────────────┘    └──────────────┘
```

### 파일 흐름

```
webex-transcript-2026-08-25_075532.txt          (전사 원문 — 2,400줄)
    │
    ▼ format_transcript.py
webex-transcript-2026-08-25_075532-formatted.txt (문장 분리 — 618줄)
    │
    ▼ correct_transcript.py + JSON LUT
webex-transcript-2026-08-25_075532-corrected.txt (오류 교정 — 618줄, 48교정)
    │
    ▼ transcribe_to_llm.py
webex-transcript-2026-08-25_075532-final.md      (LLM 분류/번역 — MD 포맷)
```

---

## JSON LUT v2 — 교정 엔진

### 구조

```json
{
  "version": "2.0",
  "rules": [
    {
      "priority": 1,
      "type": "phrase",
      "patterns": [
        { "match": "in hardships", "replace": "in partnerships" }
      ]
    },
    {
      "priority": 4,
      "type": "context_word",
      "patterns": [
        {
          "match": "cash",
          "replace": "cache",
          "condition": { "type": "near", "words": ["kv", "cache"], "distance": 10 }
        }
      ]
    }
  ]
}
```

### 4 Priority 레이어

| Priority | 타입 | 기준 | 예제 |
|----------|------|------|------|
| p1 | phrase | 3+ 단어 또는 철자만 다른 구문 | "in hardships" → "in partnerships" |
| p2 | phrase | 2 단어 또는 기술 용어 | "kv cash" → "KV cache" |
| p3 | word | 단일 단어 (boundary match) | "marvel" → "Marvell" |
| p4 | context_word | 주변 단어 확인 후 교체 | "cash" → (주변에 "kv" 있으면 "cache") |

### `correct_transcript.py` 동작 원리

1. JSON LUT 읽기 → 패턴 컴파일 (정규식)
2. priority 낮은 순서대로 적용 (p1 → p2 → p3 → p4)
3. 동일 original은 가장 긴 match 유지 (중복 제거)
4. 문맥 조건 (`near:`) — 매칭 위치 ±30자 조회, 키워드 존재 시 교체
5. 통계 추적 — 각 priority별 교체 횟수 출력

### 교정 성공률 (테스트 결과)

```
LUT: 56 patterns loaded
48 corrections applied
  p1 (exact):    16
  p2 (medium):   26
  p4 (context):   8
```

주요 교정 건:
- **KV cache** 관련 11회 (p2: 8회 + p4: 3회)
- **CXL** 관련 6회 ("cx" → "CXL", "six cell" → "CXL protocol")
- **Company names**: "SK heinrich" → "SK hynix"
- **Technical terms**: "hyperskiller" → "hyperscaler"

---

## Whisper 전사 — CPU 최적화

### PyTorch multithreading

```python
num_cpu = os.cpu_count() or 4
torch.set_num_threads(max(num_cpu * 2, 8))
```

현재 환경: 20 cores × 2 = **40 threads** (이미 최대)

### GPU 가속 불가능

Intel Iris Xe — CUDA 없음 → CPU 전용. 유일한 속도 개선:
- `medium` → `small` 모델 변경 (약 3~4배 빠름, 정확도 약간↓)

### SSL 패치 (사내 네트워크)

```python
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE
whisper._download = _patched_download  # 맥락 패치
```

### Subprocess 실시간 진행률

```python
Popen(cmd, env=env, stdout=PIPE, stderr=PIPE, stdin=PIPE, text=True)
# PYTHONUNBUFFERED=1 환경변수로 stdout 즉시 출력
```

---

## 오류 교정 — 왜 LLM인가

### Regex의 한계

`transcribe_to_report.py`에서 regex 기반 분류를 여러 차례 시도했으나 실패:

- `is_host()` 패턴이 main speaker 라인도 host로 분류
- `QUESTION_RE`가 main speaker 문장도 질문으로 오인식
- 문맥 없는 규칙 → false positive/low recall

### LLM 기반 해결 (Anthropic SDK 기반, 2026-08-25 개편)

`transcribe_to_llm.py`가 RAG 교정된 트랜스크립트를 읽고 영한병기 Markdown을 생성합니다.

**Anthropic Python SDK 기반** (2026-08-25):
```python
from anthropic import Anthropic
client = Anthropic()  # ANTHROPIC_BASE_URL + ANTHROPIC_AUTH_TOKEN 자동 로드
```

**스트리밍 + 청크 분할** (사내 LLM 호환):
- 616라인 → 200라인 단위 청크 (4개)
- `client.messages.stream()` 사용 (10분 이상 응답 필수)
- `temperature` 미지원 사내 LLM 대비 `try/except TypeError`

**환경변수** (`.claude/settings.json`에서 자동 로드):
- `ANTHROPIC_BASE_URL` — 사내 LLM 게이트웨이
- `ANTHROPIC_AUTH_TOKEN` — 인증 토큰
- `ANTHROPIC_DEFAULT_SONNET_MODEL` — 모델명

**발견/해결한 에러** (2026-08-25):
1. `urllib.request` 수동 HTTP → 403 Forbidden → SDK 변경으로 해결
2. `client.messages.create()` → `temperature` 파라미터 미지원 → stream + 온도 제거
3. 10분 이상 응답 → 스트리밍 필수 (`Streaming is required...`)
4. 환경변수 미설정 → LLM 번역 스킵 → SDK가 env 자동 로드

**출력**: `webex-transcript-*-rag-corrected-llm-output.md` (영한병기 Markdown)

---

## LUT 유지보수

### txt → JSON 마이그레이션

```bash
# 1. Error_correction_word_LUT.txt 에 추가
echo "wrong term | correct term" >> webex-audio/Error_correction_word_LUT.txt

# 2. JSON v2로 병합
python upgrade_lut.py webex-audio/Error_correction_word_LUT.txt
```

- `|` 구분자 = 교정 규칙
- 구분자 없는 줄 = 용어집 (vocabulary)
- `#` 시작 줄 = 주석
- 기존 JSON 중복 규칙 자동 skip

### upgrade_lut.py 동작

```
txt 파싱 → original/correction 추출 → JSON 기존 규칙과 비교 → 신규만 병합
```

우선순위 자동 할당:
- 3+ 단어 → p1
- 2 단어 → p2
- 1 단어 → p3

---

## RAG-LUT (2026-08-25 신규 — Transformer Attention 원리)

### 개념

TF-IDF vectorization + cosine similarity로 LUT 교정 규칙을 "임베딩"하고, 교정 대상 텍스트와 유사한 규칙을 문맥에 맞게 검색해 적용합니다.

**Attention 메커니즘 매핑**:
- Query = 교정 대상 chunk embedding
- Key = LUT 규칙 embedding
- Score = cosine similarity (유사도)
- Value = rule replacement

**두 레이어 안전망**:
| 레이어 | 동작 | 조건 |
|--------|------|------|
| p1/p2 | 항상 적용 (always-on) | 정확구문 + 회귀안전 |
| p3/p4 | RAG 검색 후 적용 | cosine similarity ≥ 0.01 일 때만 |

### 구현

`rag_lut.py` — 순수 파이썬 TF-IDF (numpy 의존성만, sklearn 불필요):
```python
# IDF: log((N+1)/(df+1))+1 (sklearn 호환)
# embedding: 토큰 평균 벡터 (on-the-fly, init 시 계산)
```

### 라인브레이크 보존 (2026-08-25 버그픽스)

**발견**: RAG 교정 후 formatted.txt의 줄바꿈이 모두 사라짐 (문제가 1줄로 붙음).

**원인**: `split_chunks()`가 `\n`을 구문 경계로 사용해 newlines을 소모.

**수정**: `splitlines(True)` → 라인 단위 처리 → 각 라인의 trailing whitespace(`\n`, `\r\n`) 보존.
```python
# before (buggy):
chunks = split_chunks(text, max_tokens=CHUNK_SIZE)

# after (fixed):
lines = text.splitlines(True)  # keepends=True
for line in lines:
    line_stripped = line.strip()
    if not line_stripped:
        corrected_lines.append(line)  # blank lines preserved
        continue
    corrected_line, applied = _correct_chunk(line_stripped, tokenize(line_stripped))
    corrected_lines.append(corrected_line + line[len(line_stripped):])  # restore trailing \n
```

**테스트 결과** (1시간 Marvell 미팅, 39,557바이트):
- 입력: 616줄 → 출력: 616줄 (100% 보존)
- RAG 규칙 적용: 22개 (cosine similarity 기반 검색)
- Always-on (p1/p2): 41개 교정
- 라인 변경: 53/616 (약 8.6%)

### 교정 결과 파일

`webex-transcript-formatted-YYYY-MM-DD_HHMMSS-rag-corrected.txt` — RAG 교정 완료본.
`correct_transcript.py --rag`로도 수동 실행 가능.

---

## 파일 위치

| 파일 | 역할 |
|---|---|
| `repo/webex_recorder.py` | 엔트리 — 녹음 + `--auto` 파이프라인 orchestration |
| `repo/webex_transcribe.py` | Whisper 전사 (SSL 패치, multithread) |
| `repo/format_transcript.py` | 문장 분리 (`. ! ?`) |
| `repo/correct_transcript.py` | 오류 교정 (JSON LUT v2) |
| `repo/rag_lut.py` | RAG-LUT 교정 엔진 (TF-IDF + cosine similarity, 2026-08-25 신규) |
| `repo/transcribe_to_llm.py` | LLM 분류/번역 (Anthropic SDK 기반) |
| `repo/upgrade_lut.py` | txt → JSON 병합 (LUT 유지보수) |
| `repo/fix_all_transcripts.py` | batch 처리 (기존 파일 일괄) |
| `repo/webex-audio/Error_correction_word_LUT.json` | 교정 규칙 (56개 패턴) |
| `repo/webex-audio/Error_correction_word_LUT.txt` | 원본 LUT + 용어집 |

---

## 테스트

### 단축 테스트 (30초)

```bash
python webex_recorder.py --auto 30
```

녹음 30초 → 전사 → 포맷 → 교정 → 결과 파일 확인

### 교정만 재실행

```bash
python correct_transcript.py "webex-audio/webex-transcript-*.txt"
```

---

**생성일**: 2026-08-25
**검증**: 전체 파이프라인 `--auto 30` 테스트 완료, JSON LUT 56개 패턴 48교정 확인
