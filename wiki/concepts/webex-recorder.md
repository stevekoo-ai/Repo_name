---
title: "WebEx Meeting Recorder + Transcriber"
created: 2026-08-24
updated: 2026-08-27
tags: [webex, audio-recording, speech-to-text, whisper, ffmpeg, bluetooth-headset, transcription, batch, meeting-minutes]
---

# WebEx Meeting Recorder + Transcriber

> WebEx 미팅 오디오를 자동 녹음하고 Whisper로 전사(Transcription)하는 시스템.
> Bluetooth 헤드셋 연결 시에도 시스템 음성을 포착 가능한 VB-Cable 기반 아키텍처.

---

## 핵심 문제

Windows에서 Bluetooth 헤드셋을 사용할 때:

- **Stereo Mix 가 숨겨진다**: Zone Wireless 등 Bluetooth 헤드셋 연결 시 Windows가 Realtek Stereo Mix를 dshow 장치 목록에서 숨김
- **sounddevice WASAPI loopback 실패**: PortAudio 호환성 문제로 loopback 스트림 오픈 불가
- **PyTorch Segfault**: Python 3.14 + PyTorch 2.13 + Whisper 연동 시 메모리 할당 실패 + segmentation fault
- **cp949 인코딩 오류**: 한국어 장치명(Realtek(R) Audio 등)이 ffmpeg stderr에 포함되면 Windows 터미널에서 decode 실패
- **전사 후 번역 부재**: RAG 교정까지는 자동으로 되지만 LLM 영한병기 번역이 환경변수 미설정·SDK 파라미터 불일치 등으로 스킵될 수 있음 (아래 "LLM 번역 파이프라인" 참조)

---

## 2026-08-27 업데이트 (MP4 파이프라인 디버그 + 배치 + 회의록)

### 3개 결함 수정 (MP4→WAV→전사→post-process end-to-end 복구)

MP4 비디오 자동 전사(`--source`)가 3개 독립 결함으로 끊기던 것을 모두 복구. Marvell mp4(52분)로 end-to-end 검증 완료.

| # | 결함 | 원인 | 수정 | 검증 |
|---|---|---|---|---|
| **#1** | 13:00 세션 35분→6단어 환각 | 추출 WAV 평균 볼륨 **-52.1 dB** (너무 낮음) → Whisper hallucination | `extract_audio_from_video`에 `loudnorm=I=-16:TP=-1.5:LRA=11` 볼륨 정규화 + `_measure_volume` 측정/경고 + `_warn_if_hallucination`(<50자 감지) | Marvell: -35.5→**-17.6 dB**, 37896 chars 정상 전사 ✅ |
| **#2** | post-process LLM 단계 skip | `run_postprocess`는 `-corrected` 기대 but `correct_transcript.py --rag`는 `-rag-corrected` 생성 → 파일명 불일치 | `run_postprocess` 전면 재작성: `-rag-corrected` 예측 정확화, glob 폴백 정리 | formatted→rag-corrected→llm-output 전체 완료 ✅ |
| **#3** | `check_channels_wav` 항상 fallback | `Downloads/ffprobe.exe` 미존재 (실제는 `bin/ffprobe.exe`) | `FFMPEG_BIN`/`FFPROBE_BIN` 자동 탐지 (bin/ 우선→Downloads→PATH) + `-t 300`(5분 잘림) 제거 | `bin/ffprobe.exe` 정상 탐지 ✅ |

**수정 파일**:
- [webex_recorder.py](../../repo/webex_recorder.py) — `extract_audio_from_video`(볼륨 정규화+측정), `transcribe` wrapper(hallucination 감지), `run_postprocess`(파일명 체인 재작성)
- [webex_transcribe.py](../../repo/webex_transcribe.py) — `FFMPEG_BIN`/`FFPROBE_BIN` 자동 탐지, `convert_stereo_to_mono` 잘라내기 제거

### 4시간 녹음 상한 + graceful 조기 종료 (2026-08-26)

- `MAX_RECORDING_SECONDS = 14400` (4시간) 상한
- `q + Enter` (stdin 데몬 스레드) 또는 `Ctrl+C`로 ffmpeg graceful 종료 → WAV 헤더 보존
- `subprocess.Popen(stdin=PIPE)` + `_q_listener` 스레드 + `_send_q` 헬퍼
- 표준 시나리오: 미팅 끝나면 q+Enter로 조기 종료, 최대 4시간 상한

### 언어별 BAT 파일 (더블클릭 실행)

`C:\Users\2053437\repo\` 에 3개 BAT (구조 동일, `--lang`만 다름):
- `record-webex-en.bat` — English (`--lang en`)
- `record-webex-ko.bat` — 한국어 (`--lang ko`)
- `record-webex-zh.bat` — 중국어 (`--lang zh`)

모두 `--auto --noask` + 4시간 상한 + `q+Enter`/`Ctrl+C` 종료 + `webex-audio\schedule.log` 누적.

### 배치 루프 스크립트 (PicPick 폴더 일괄 처리)

[batch_transcribe.py](../../repo/batch_transcribe.py) — `C:\PicPick\` 의 정형화된 mp4 파일명을 순회하며 end-to-end 파이프라인 실행.

**파일명 규칙** (사용자가 수작업으로 정형화):
```
YYYY-MM-DD HH MM SS_LANG_제목.mp4
LANG = EN | KR | CN  (대문자 고정)
```
날짜/시간/언어/제목 구분자는 **공백**, 언어-제목은 `_` (PicPick 기본 녹화명 형식에 맞춤).
예: `2026-08-25 08 00 59_EN_Marvell-PFMA.mp4`
파싱 정규식: `^(?P<date>\d{4}-\d{2}-\d{2})\ (?P<hh>\d{2})\ (?P<mm>\d{2})\ (?P<ss>\d{2})_(?P<lang>EN|KR|CN)_(?P<title>.+?)\.mp4$`
LANG→Whisper 매핑: `EN→en`, `KR→ko`, `CN→zh`

**안전장치**:
- 최종 회의록 md가 있으면 skip (재시작 안전 — 며칠 걸리는 작업)
- `batch-failures.log`에 실패 파일 기록 → `--force`로 재실행
- 미정형화 파일명 자동 skip (규칙 미매칭 분류만)
- `--min-size`로 소형 파일 skip (기본 1MB)

**실행 모드**:
```bash
python batch_transcribe.py --dry-run              # 파싱만 확인 (파일명 정형화 검증)
python batch_transcribe.py --limit 3              # 처음 3개만 (테스트)
python batch_transcribe.py                        # 전체 순차 실행
python batch_transcribe.py --force                # 완료된 것도 재실행
python batch_transcribe.py --model small           # 모델 지정 (기본 small)
python batch_transcribe.py --source D:\\Other      # 폴더 지정
```

**산출물** (`webex-audio/`):
```
<제목>-extracted.wav                    # 정규화된 오디오
<제목>-extracted.txt                    # Whisper 전사
<제목>-extracted-formatted.txt          # 문장 분리
<제목>-extracted-rag-corrected.txt      # LUT+RAG 교정
<제목>-extracted-rag-corrected-llm-output.md  # LLM 한영 번역
YYYY-MM-DD_제목-회의록.md               # 최종 회의록 (batch_transcribe 생성)
```

**주의**: 219개 파일 전체는 CPU 기준 수일 소요. `--limit`로 소수 테스트 후 전체 적용 권장.

### 회의록 자동 생성 (정식 포맷 — Marvell 형식)

`batch_transcribe.py`의 `generate_meeting_minutes()`가 교정본(`-rag-corrected.txt`)을 LLM에 재투입하여 Marvell 정식 회의록 포맷으로 요약·재구성. 임시 복사 구현에서 LLM 재호출 기반으로 2026-08-27 업그레이드.

**포맷 구조** (모든 회의록에 공통 적용):
1. **헤더** — `# <제목> 회의록` + 일시/언어/소스 메타데이터
2. **회의 개요 표** — 일시 · 장소 · 주체 · 주제 (4행 표)
3. **참석자** — 전사에서 추론한 발언자/조직 정리 (미확정 표기)
4. **Summary (개요)** — 핵심 내용 3문장 요약
5. **주요 논의 내용** — 3~5개 번호 섹션 (각 섹션: 타이틀 + 2 꼭지, 꼽지당 1문장)
6. **Action Items** — 체크박스 + 담당자/조직 + 액션 한 문장
7. **꼬리말** — "Whisper 전사 + RAG 교정 + LLM 요약 기반"

**LLM 모델**: 사내 vLLM 허용 모델 사용 (기본 `GLM-5.2`, `MINUTES_MODEL` 환경변수로 오버라이드). `claude-*` 모델은 team access 거부(403)되므로 사용 불가.

**폴백**: LLM 호출 실패 시 `llm_output` 또는 교정본을 본문으로 사용(경고 헤더 추가). 전사 단계까지 날아가는 일은 없음.

**재생성 전용 스크립트** (전사는 이미 된 상태에서 회의록만 다시 만들 때):
```bash
python regenerate_minutes.py              # 13개 전체 재생성 (완료된 것은 skip)
python regenerate_minutes.py --force      # 이미 있어도 강제 재생성
python regenerate_minutes.py --limit 2    # 처음 2개만 (테스트)
```

**검증 결과** (2026-08-27): PicPick mp4 13개 전체 정식 회의록으로 재생성 완료. 한국어 원본(미래포럼)도 정상 처리. 파일당 5~8KB, LLM 호출 1회/파일.

**수동 작성 예시** (참고용, Marvell 2026-08-25): [Marvell-PFMA-회의록-2026-08-25.md](../../repo/webex-audio/Marvell-PFMA-회의록-2026-08-25.md) — 자동 생성 포맷의 기준이 된 원본.

---

## 해결 아키텍처

```
WebEx 미팅 오디오
  ↓
WebEx Speaker: CABLE Input(VB-Audio Virtual Cable)
  ↓ (WebEx 오디오 → 가상 케이블로 라우팅)
CABLE Output(VB-Audio Virtual Cable)
  ↓ (ffmpeg dshow로 포착)
ffmpeg 녹음 → webex-audio-YYYY-MM-DD_HHMMSS.wav
  ↓ (별도 프로세스)
PyTorch/Whisper 전사 → webex-transcript-YYYY-MM-DD_HHMMSS.txt
```

### 설계 결정

| 요소 | 선택 | 이유 |
|------|------|------|
| 녹음 | ffmpeg dshow | sounddevice WASAPI 실패, PortAudio 호환성 문제 |
| 가상 케이블 | VB-Audio Cable (무료) | Stereo Mix 대체, Bluetooth 헤드셋과 병행 가능 |
| 음성인식 | PyTorch/Whisper medium | 한국어+영어 다국어 지원 |
| 프로세스 분리 | ffmpeg + subprocess | Segfault 격리 (Recording 프로세스에 PyTorch 없음) |
| 샘플레이트 | 16kHz | Whisper 최적화 |
| 채널 | Mono(1ch) 기본 | 파일 작음, 전사 정확도 차이 미미 |
| 인코딩 | encoding='utf-8', errors='replace' | cp949 decode 오류 방지 |

---

## 시스템 파일

### `repo/webex_recorder.py` (메인 에ント리 포인트 — ~415줄)

**CLI 인터페이스** (2026-08-27 배치+4시간 상한+결함 수정 반영):
```bash
# 녹음 + 자동 전사 (4시간 상한, q+Enter/Ctrl+C로 조기 종료)
python webex_recorder.py --auto                  # 4시간 상한 (대화형 메뉴)
python webex_recorder.py --auto --noask          # 설정 없이 자동 실행
python webex_recorder.py --auto 3600             # 1시간 지정
python webex_recorder.py --record 3600           # 녹음만
python webex_recorder.py --transcribe 파일.wav   # 기존 wav 전사
python webex_recorder.py --auto --model small    # 빠른 전사

# MP4 비디오 → 오디오 추출(볼륨 정규화) → 전사 → RAG 교정 → LLM 번역
python webex_recorder.py --source "C:\PicPick\meeting.mp4" --lang en
python webex_recorder.py --source "meeting.mp4" --model small  # 모델 지정

# 배치 (PicPick 폴더 순회 — 파일명 규칙 필요)
python batch_transcribe.py --dry-run             # 파싱만 확인
python batch_transcribe.py --limit 3             # 테스트
python batch_transcribe.py                       # 전체 실행
```

**구성 요소**:
- `get_audio_devices()`: ffmpeg dshow로 사용 가능한 audio 장치 목록 조회
- `show_menu(config)`: 대화형 메뉴 (장치/언어/모델/채널)
- `record(duration, config)`: ffmpeg dshow로 WAV 녹음 (4시간 상한, q+Enter/Ctrl+C graceful 종료, `_q_listener` 데몬 스레드)
- `transcribe(audio_path, model, language)`: 별도 프로세스에서 Whisper 전사 + `_warn_if_hallucination` 감지
- `auto(duration, config)`: 녹음 → 전사 → 결과 출력 파이프라인
- `extract_audio_from_video(video_path, output_dir, language)`: MP4/MKV/AVI/MOV/WEBM → WAV(16kHz mono) 추출, `loudnorm` 볼륨 정규화 + `_measure_volume` 측정
- `run_postprocess(transcript_path, audio_dir)`: format → RAG 교정(`-rag-corrected`) → LLM 번역 파이프라인 (2026-08-27 파일명 체인 재작성)

**언어 설정 — 4옵션으로 단순화 (2026-08-25)**:
```python
WHISPER_LANGUAGES = {
    None: '[0] 자동 감지',
    'en': '[1] English',
    'zh': '[2] Chinese',
    'ko': '[3] Korean',
}
```
이전 80개 언어 메뉴를 제거하고 자주 쓰는 4옵션만 남김. `--lang en/ko/zh` 플래그로 명시 강제 가능.

**기본 설정**:
```python
DEFAULT_CONFIG = {
    'audio_device': 'CABLE Output(VB-Audio Virtual Cable)',
    'channels': 1,        # mono
    'sample_rate': 16000, # whisper optimal
    'language': None,     # None = auto-detect
    'model': 'medium',
}
```

### `repo/webex_transcribe.py` (전사 전용 스크립트 — ~61줄)

별도 프로세스에서 실행되어 Segfault 격리.

```bash
python webex_transcribe.py audio.wav                    # 자동 감지
python webex_transcribe.py audio.wav medium              # 모델 지정
python webex_transcribe.py audio.wav --language en       # 언어 강제
```

**핵심 동작**:
1. `gc.collect()` — 메모리 정리
2. `whisper.load_model(model_name, device='cpu')` — CPU 전용 (GPU 없음)
3. `model.transcribe(audio_path, language=language, verbose=False)` — 전사
4. 결과 저장: `webex-transcript-{timestamp}.txt`
5. `OUTPUT:{path}` 마커로 부모 프로세스에 결과 경로 반환

---

## WebEx 오디오 설정 (필수)

WebEx 미팅 내에서:

| 설정 | 값 | 설명 |
|------|------|------|
| Speaker (스피커) | `CABLE Input(VB-Audio Virtual Cable)` | 미팅 오디오 → 가상 케이블로 라우팅 |
| Mic (마이크) | `Zone Wireless` (또는 Bluetooth 헤드셋) | 사용자 음성 녹음 |

이 설정으로 WebEx 오디오가 CABLE Input → CABLE Output 경로로 흐르고, ffmpeg가 CABLE Output에서 포착.

---

## 작동 순서

### 1. 자동 모드 (`--auto`)

### 2. MP4 비디오 자동 전사 (`--source`)

```
--source "meeting.mp4"
  ↓ ffmpeg 추출 (-af loudnorm=I=-16:TP=-1.5:LRA=11 -acodec pcm_s16le -ar 16000 -ac 1)
  ↓              ↑ 볼륨 정규화(2026-08-27 추가) + _measure_volume 측정/경고
wav (C:/Users/2053437/repo/webex-audio/meeting-extracted.wav)
  ↓ Whisper 전사 + _warn_if_hallucination (비정상 짧은 결과 감지)
transcript.txt
  ↓ format_transcript.py
transcript-formatted.txt (문장 분리)
  ↓ correct_transcript.py --learn --rag (TF-IDF + cosine similarity)
transcript-rag-corrected.txt (2026-08-27 파일명 체인 정확화)
  ↓ transcribe_to_llm.py (Anthropic SDK 스트리밍)
transcript-rag-corrected-llm-output.md (영한병기 Markdown)
```

**설계 결정** — 원본 위치에서 직접 처리. MP4 파일을 복사하지 않고 `ffmpeg`로 audio만 추출해 `webex-audio/`에 저장. 볼륨 정규화(`loudnorm`)는 저볼륨 mp4(예: -52dB)에서 Whisper hallucination을 방지하기 위해 2026-08-27에 추가.

### 3. LLM 번역 파이프라인 (`--source` 자동 포함)

RAG 교정된 트랜스크립트를 Anthropic SDK로 LLM에 넘겨 영한병기 Markdown을 생성합니다.

```python
# transcribe_to_llm.py — Anthropic SDK 기반 (2026-08-25 개편)
from anthropic import Anthropic  # env에서 base_url/token 자동 읽음
client = Anthropic()  # ANTHROPIC_BASE_URL + ANTHROPIC_AUTH_TOKEN
```

**환경변수** (`.claude/settings.json`에서 자동 로드):
- `ANTHROPIC_BASE_URL` — 사내 LLM 게이트웨이 (예: `http://common.llm.skhynix.com`)
- `ANTHROPIC_AUTH_TOKEN` — 인증 토큰
- `ANTHROPIC_DEFAULT_SONNET_MODEL` — 모델명 (예: `gemma-4-31B-it`, `sonnet`)

**클라우드 모드**: Anthropic SDK가 `ANTHROPIC_BASE_URL`이 없으면 기본 Anthropic API를 사용합니다.

**스트리밍 + 청크 분할** (2026-08-25): 616라인 → 200라인 단위 4 청크, `client.messages.stream()` 사용. 사내 LLM이 `temperature` 파라미터를 받지 않으면 `try/except TypeError`로 폴백.

**실패 사례** (2026-08-25 디버깅 기록):
- `urllib.request` 기반 수동 HTTP → 403 Forbidden (SDK 방식이 사내 인증을 더 잘 처리)
- `client.messages.create()` → `temperature` 미지원 400 에러 → `try/except TypeError`로 `stream()` + 온도 제거
- 10분 이상 장기 응답 → 스트리밍 필수 (`Streaming is required for operations that may take longer than 10 minutes`)

```
$ python webex_recorder.py --auto 600

==================================================
  WebEx Meeting Recorder - 설정
==================================================

--- [1] 녹음 소스 ---
    1. CABLE Output(VB-Audio Virtual Cable)   ← 현재 설정
    2. 헤드셋 마이크(Zone Wireless)
    0. 현재 설정 유지

녹음 소스 선택 (번호) > 0     (변경 없으면 0)

--- [2] 언어 ---
    1. 자동 감지 (모든 언어)   ← 현재 설정
    2. 영어 (English)
    ... 80개 언어 옵션
    0. 현재 설정 유지

언어 선택 (번호) > 0

--- [3] Whisper 모델 ---
    4. medium - 느림, 좋은 정확도 (권장) ← 현재 설정
    0. 현재 설정 유지

모델 선택 (번호) > 0

--- [4] 오디오 채널 ---
    1. Mono (1ch) - 파일 작음
    2. Stereo (2ch) - 현재 설정

채널 선택 (번호) > 1         (mono로 변경)

==================================================
  최종 설정
==================================================
  녹음 소스: CABLE Output(VB-Audio Virtual Cable)
  언어: 자동 감지 (모든 언어)
  모델: medium
  채널: 1ch
==================================================
진행하시겠습니까? (y/n) > y

[REC] 녹음 시작... (600초, CABLE Output(VB-Audio Virtual Cable))
[REC] 언어: 자동 감지 (모든 언어)
[REC] 출력: C:/Users/2053437/repo/webex-audio/webex-audio-2026-08-21_062038.wav
[REC] 저장 완료: 4832KB
[REC] 전사 시작... (CPU, 몇 분 걸림)
[WHISPER] Loading model: medium...
[WHISPER] Transcribing: .../webex-audio-2026-08-21_062038.wav
[WHISPER] 언어 자동 감지 중...
[WHISPER] (CPU라서 몇 분 걸릴 수 있음)
[WHISPER] Language: en
[WHISPER] Duration: 60.0s
[WHISPER] Text: 304 chars
[WHISPER] Transcript saved: .../webex-transcript-2026-08-21_062038.txt
[WHISPER] OUTPUT:.../webex-transcript-2026-08-21_062038.txt

==================================================
전사 결과:
==================================================
you to get fast and reliable response...
==================================================

✅ 파일:
   오디오: C:/.../webex-audio-2026-08-21_062038.wav
   전사:   C:/.../webex-transcript-2026-08-21_062038.txt
```

### 2. 녹음만 (`--record`)

```bash
python webex_recorder.py --record 3600   # 1시간 녹음만
python webex_recorder.py --transcribe webex-audio/webex-audio-2026-08-21_062038.wav   # 나중에 전사
```

---

## 출력 파일

| 패턴 | 설명 | 예시 |
|------|------|------|
| `webex-audio-{timestamp}.wav` | 녹음된 WAV 오디오 | `webex-audio-2026-08-21_062038.wav` |
| `webex-transcript-{timestamp}.txt` | 전사된 텍스트 | `webex-transcript-2026-08-21_062038.txt` |

- **매번 새 파일 생성** (append 아님) — 타임스탬프 포함
- 디렉토리: `repo/webex-audio/`
- 인코딩: WAV = PCM s16le, TXT = UTF-8

---

## 성능 참고

| 항목 | 값 |
|------|-----|
| 녹음 크기 | 16kHz mono: ~288KB/min |
| 전사 시간 | medium 모델, 1분 오디오 → 수 분 (CPU) |
| 모델 크기 | medium: ~1.5GB 메모리 |
| 전사 정확도 | medium 권장, tiny는 빠르지만 낮음 |

---

## 학습된 교훈 (Lessons Learned)

### 시도하고 실패한 접근

1. **sounddevice WASAPI loopback** → PortAudio stream info struct 호환성 실패
2. **PyAudio** → wheel 빌드 실패 (Microsoft Visual C++ 필요)
3. **same-process recording + transcription** → PyTorch Segfault
4. **Stereo Mix (Realtek)** → Bluetooth 헤드셋 연결 시 숨겨짐

### 성공한 접근

1. **ffmpeg dshow** → Windows DirectShow API, 모든 장치 지원
2. **VB-Audio Cable** → 무료 가상 오디오 케이블, Bluetooth 병행 가능
3. **subprocess 분리** → Segfault 완전 격리
4. **encoding='utf-8', errors='replace'** → 한국어 장치명 대응

### 음성 없는 녹음 문제

- RMS = 0.53 또는 1: 오디오 소스가 제대로 라우팅되지 않음
- WebEx Speaker가 CABLE Input이 맞는지 반드시 확인
- WebEx 미팅 중 다른 사람이 말하고 있을 때만 오디오 유입

---

## 알려진 제한사항

1. **CPU 전사**: GPU 없으므로 전사에 수 분 소요 (medium 기준)
2. **PyTorch 모델 메모리**: medium 모델 로드에 ~1.5GB RAM 필요
3. **Whisper language code**: `su` (Sundanese) 라벨이 "수난어"로 표기됨 (본래 Sundanese)
4. **VB-Cable 설치 필수**: 설치 전에는 사용 불가 (무료)

---

## 관련 파일

- [webex_recorder.py](../../repo/webex_recorder.py) — 메인 엔트리 포인트 (녹음/전사/post-process)
- [webex_transcribe.py](../../repo/webex_transcribe.py) — 전사 전용 스크립트 (별도 프로세스)
- [batch_transcribe.py](../../repo/batch_transcribe.py) — 배치 루프 (PicPick 폴더 순회, 2026-08-27 추가)
- [regenerate_minutes.py](../../repo/regenerate_minutes.py) — 회의록만 재생성 (전사 건너뜀, 정식 포맷 업그레이드 후 재적용 시 사용, 2026-08-27 추가)
- [record-webex-en.bat](../../repo/record-webex-en.bat) / [record-webex-ko.bat](../../repo/record-webex-ko.bat) / [record-webex-zh.bat](../../repo/record-webex-zh.bat) — 언어별 더블클릭 실행 BAT
- [webex-audio/](../../repo/webex-audio/) — 녹음/전사/회의록 결과 디렉토리
- [webex-audio/Marvell-PFMA-회의록-2026-08-25.md](../../repo/webex-audio/Marvell-PFMA-회의록-2026-08-25.md) — 회의록 작성 예시 (수동)

## 관련 개념

- [[customer-meetings-intelligence]] — 고객 미팅 인텔리전스 운영 패턴
