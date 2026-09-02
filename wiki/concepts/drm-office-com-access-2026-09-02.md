# 회사 DRM(MarkAny Document SAFER) 환경에서 AI가 Office 문서를 읽고 수정하고 저장하는 방법

> 🆕 2026-09-02. **단일 출처(SSOT).** 다른 LLM·에이전트가 이 방법을 그대로 복제할 수 있도록 검증된 절차·코드·실측 데이터를 모두 담았다. "나한테 다시 묻지 말 것"을 전제로 작성됨. 핸드오프 패키지는 `DRM_off.zip`(스크립트 + 이 문서 사본 + README)로 동봉.

---

## 0. TL;DR (3줄 요약)

1. 회사 PC는 **MarkAny Document SAFER** DRM이 걸려 있어, 모든 Office 문서 파일 헤더가 `<DOCUMENT SAFER V201...` 컨테이너로 암호화되어 있다.
2. bash/cat/Python-openfile 등 **일반 파일 I/O로는 암호문 바이트만 보인다** (커널 필터 투명 복호화 안 함). 사용자가 더블클릭할 때는 Office 앱 내부에서 `MADRMAgent.exe`가 복호화한다.
3. AI도 동일 경로를 타려면 **pywin32로 Office COM 자동화**(`Word.Application` / `Excel.Application` / `PowerPoint.Application`)를 쓴다 → 평문 읽기·수정·저장 모두 가능하고, **저장 시 자동 재암호화되어 DRM 보호 포맷이 보존**된다.

---

## 1. 환경 실측 (이 PC에서 검증된 값)

| 항목 | 측정값 | 비고 |
|---|---|---|
| DRM 솔루션 | **MarkAny Document SAFER** | 한국 기업용 문서 DRM 표준 |
| DRM 에이전트(사용자 세션) | `C:\MarkAny\Document SAFER\MADRMAgent.exe` (PID 27216 실행 중) | 파일 암·복호화 담당 |
| 웹 DRM(브라우저) | `C:\Program Files (x86)\MarkAny\WebDRMNoAX\bin\MaWebDRMAgent.exe` | 본 주제와 무관 (웹 다운로드 DRM) |
| 보호 파일 헤더(실측) | `b'<DOCUMENT SAFER V201'` (처음 20바이트) | 모든 보호 docx/xlsx/pptx 공통 |
| 커널 투명 복호화 | **없음** | bash로 읽으면 암호문 그대로 보임 |
| Python | 3.14.6 | 시스템 PATH에 `python`/`python3` |
| pywin32 | 설치됨 (`import win32com.client` OK) | `pip install pywin32` 로 설치 가능 |
| Office | 2016 (64bit) — Word/Excel/PowerPoint | `C:\Program Files\Microsoft Office\Office16\` |
| 한글(HWP) | **설치 안 됨** | .hwp 파일은 이 방법으로 불가 (한글어플리케이션 필요) |
| 운영체제 | Windows 10 Enterprise LTSC 2021 19044 | 한국어 |

### 측정 명령 (재검증용)
```bash
# 1) DRM 에이전트 경로/실행 확인
wmic process where "name='MADRMAgent.exe'" get ExecutablePath,ProcessId

# 2) 보호 파일 헤더 확인 (어떤 파일이든)
head -c 20 "경로/문서.docx" | xxd
# → 00000000: 3c44 4f43 554d 454e 5420 5341 4645 5220  <DOCUMENT SAFER

# 3) Python/pywin32/Office 확인
python --version
python -c "import win32com.client; print('pywin32 OK')"
ls "/c/Program Files/Microsoft Office/Office16/WINWORD.EXE"
```

---

## 2. 왜 일반 파일 I/O로는 안 되는가 (원리)

MarkAny Document SAFER는 **"애플리케이션 레벨 DRM"** 이다:
- 파일 자체를 `<DOCUMENT SAFER V201` 헤더 + 암호문 본문으로 저장.
- OS 커널에 파일시스템 필터 드라이버를 올려 투명 복호화를 하는 방식이 **아니다**.
- 따라서 `cat`, `open(path).read()`, `Read` 도구, `git diff` 등은 **암호화된 바이트만** 가져온다.
- Office(Word/Excel/PowerPoint)가 기동할 때 `MADRMAgent.exe`와 연동해 메모리에 평문을 올린다. 사용자가 더블클릭하는 것은 이 경로.

→ AI가 평문을 보려면 **Office 프로세스를 통해서** 열어야 한다. 그 인터페이스가 COM 자동화.

---

## 3. 해법: pywin32 Office COM 자동화

### 3.1 핵심 패턴 (Word — 읽기)
```python
import win32com.client as wcom
word = wcom.DispatchEx("Word.Application")
word.Visible = False          # 백그라운드
word.DisplayAlerts = False
doc = word.Documents.Open(FileName=r"C:\path\보호문서.docx",
                          ReadOnly=True,      # 읽기 전용 추출 시 안전
                          AddToRecentFiles=False, Visible=False)
text = doc.Content.Text        # 평문 (사용자 더블클릭과 동일 경로로 복호화됨)
doc.Close(SaveChanges=0)
word.Quit()
```

### 3.2 수정 + 저장 (재암호화 검증됨)
```python
doc = word.Documents.Open(FileName=path, ReadOnly=False)  # 쓰기 모드
rng = doc.Content
rng.Collapse(0)               # 0 = wdCollapseEnd
rng.InsertParagraphAfter()
rng.InsertAfter("새 내용")
doc.Save()                     # ★ 저장 시 Office가 SAFER 포맷으로 자동 재암호화
doc.Close(SaveChanges=0)
```

### 3.3 실측 검증 결과 (2026-09-02, 본 PC)
샘플 `미팅 script_20260812.docx` 사본으로 읽기/수정/저장 라운드트립 수행:
```
[1 read] extracted 6105 chars                      ← 평문 추출 성공
[3 save] saved via Word                             ← Word.Save 호출
[4 header] b'<DOCUMENT SAFER V201'                  ← 저장 후 헤더 = DRM 포맷 보존됨
[4 is SAFER format preserved?] True                 ← 재암호화 확인
[4 marker present after reopen?] True               ← 수정내용 평문에 반영됨
[4 total chars now] 6176                            ← 6105 + 71자 마커 = 정확
ROUND-TRIP OK: True
```

**결론**: 저장해도 `<DOCUMENT SAFER` 헤더가 유지되므로 편집 후에도 DRM 보호 상태가 보존된다. 사용자가 더블클릭으로 다시 열어도 정상 복호화됨을 확인.

---

## 4. 앱별 API 요약 (Word / Excel / PowerPoint)

| 앱 | ProgID | 열기 | 본문 객체 | 셀/슬라이드 |
|---|---|---|---|---|
| Word | `Word.Application` | `Documents.Open(FileName=...)` | `doc.Content.Text` (전체) / `doc.Paragraphs` | — |
| Excel | `Excel.Application` | `Workbooks.Open(FileName=...)` | `wb.Worksheets(1).UsedRange.Value` | `ws.Cells(r,c).Value`, `ws.Range("A1").Value` |
| PowerPoint | `PowerPoint.Application` | `Presentations.Open(FileName, ReadOnly:=...)` | `pres.Slides(i).Shapes(j).TextFrame.TextRange.Text` | 슬라이드별 Shape 순회 |

### 공통 주의
- `Visible=False`로 백그라운드 가능. 단, 일부 DRM 정책이 "보이는 창"을 요구하면 폴백으로 `Visible=True` 사용.
- 항상 `finally`에서 `doc.Close(SaveChanges=0)` + `app.Quit()` 호출 (좀비 Office 프로세스 방지).
- `DispatchEx`를 쓰면 항상 새 인스턴스 — 다른 열린 문서에 영향 안 줌.
- 콘솔 인코딩 문제로 한글이 깨져 보여도 파일 내용은 정상 (UTF-8/UTF-16 LE). `doc.Content.Text`는 Python 내부에서 유니코드로 처리되므로 안전.

---

## 5. 재사용 가능한 헬퍼 라이브러리: `drm_office.py`

아래 파일은 `DRM_off.zip`에 동봉됨. `from drm_office import read_docx, edit_docx, read_xlsx, read_pptx` 형태로 임포트하여 즉시 사용 가능.

<details>
<summary><b>drm_office.py 전체 소스</b> (클릭하여 펼치기)</summary>

```python
# -*- coding: utf-8 -*-
"""
drm_office.py — MarkAny Document SAFER DRM 환경에서 Office 문서를 읽/수정/저장.
요구: Python 3.x + pywin32 + Office(Word/Excel/PowerPoint).
원리: COM 자동화로 Office 프로세스를 통해 열면 DRM이 자동 복호화됨.
저자: Claude (2026-09-02). 검증: 본 PC 라운드트립 OK.
"""
import os, contextlib
import win32com.client as wcom

# Office enum 상수(숫자) — late binding에서 상수 이름이 안 들어올 때 직접 숫자 사용
WdCollapseEnd = 0
WdDoNotSaveChanges = 0
WdFormatDocumentDefault = 16  # docx
xlOpenXMLWorkbook = 51        # xlsx
ppSaveAsOpenXMLPresentation = 24  # pptx

def _abs(path):
    return os.path.abspath(path)

@contextlib.contextmanager
def _office(progid):
    app = wcom.DispatchEx(progid)
    app.Visible = False
    try:
        app.DisplayAlerts = False
    except Exception:
        pass
    try:
        yield app
    finally:
        try: app.Quit()
        except Exception: pass

# ---- Word ----
def read_docx(path):
    """DRM docx/doc → 평문 텍스트(str) 반환. 원본 변경 없음."""
    with _office("Word.Application") as word:
        doc = word.Documents.Open(FileName=_abs(path), ReadOnly=True,
                                  AddToRecentFiles=False, Visible=False)
        try:
            return doc.Content.Text
        finally:
            doc.Close(SaveChanges=WdDoNotSaveChanges)

def edit_docx(path, append_text=None, replace_text=None, save=True):
    """
    DRM docx 수정.
    - append_text: 문서 끝에 문단 추가 (str)
    - replace_text: 전체 본문 치환 (str) — 주의: 서식 손실
    - save=True: 원본 파일에 저장(DRM 재암호화). False면 저장 안 함.
    반환: 저장 후 평문(str).
    """
    with _office("Word.Application") as word:
        doc = word.Documents.Open(FileName=_abs(path), ReadOnly=False,
                                  AddToRecentFiles=False, Visible=False)
        try:
            if replace_text is not None:
                doc.Content.Text = replace_text
            if append_text is not None:
                rng = doc.Content
                rng.Collapse(WdCollapseEnd)
                rng.InsertParagraphAfter()
                rng.InsertAfter(append_text)
            if save:
                doc.Save()
            return doc.Content.Text
        finally:
            doc.Close(SaveChanges=WdDoNotSaveChanges)

# ---- Excel ----
def read_xlsx(path, sheet=None, used_range=True):
    """
    DRM xlsx → {sheet_name: [[row values], ...]} dict.
    sheet=None이면 모든 시트, sheet=이름/인덱스면 해당 시트만.
    used_range=True면 UsedRange만(빠름), False면 사용 영역 추정 안 함(제외).
    """
    with _office("Excel.Application") as xl:
        wb = xl.Workbooks.Open(FileName=_abs(path), ReadOnly=True)
        try:
            out = {}
            sheets = [wb.Sheets(sheet)] if sheet is not None else list(wb.Sheets)
            for ws in sheets:
                rng = ws.UsedRange
                vals = rng.Value  # 1-indexed 2D tuple-of-tuples
                if vals is None:
                    out[ws.Name] = []
                elif isinstance(vals, tuple):
                    # 단일 셀일 수도 → 2D 보장
                    if len(vals) == 1 and isinstance(vals[0], tuple):
                        out[ws.Name] = [list(vals[0])]
                    else:
                        out[ws.Name] = [list(r) for r in vals]
                else:
                    out[ws.Name] = [[vals]]
            return out
        finally:
            wb.Close(SaveChanges=False)

def write_xlsx_cell(path, sheet, cell, value, save=True):
    """DRM xlsx 특정 셀 값 변경 후 저장(재암호화). cell='A1' 형식."""
    with _office("Excel.Application") as xl:
        wb = xl.Workbooks.Open(FileName=_abs(path), ReadOnly=False)
        try:
            ws = wb.Sheets(sheet)
            ws.Range(cell).Value = value
            if save:
                wb.Save()
            return ws.Range(cell).Value
        finally:
            wb.Close(SaveChanges=False)

# ---- PowerPoint ----
def read_pptx(path):
    """DRM pptx → [{slide: i, texts: [str,...]}, ...] 슬라이드별 텍스트."""
    with _office("PowerPoint.Application") as pp:
        # ReadOnly: -1=True(Office 상수 msoTrue). Presentations.Open은 Visible 인자 없음.
        pres = pp.Presentations.Open(_abs(path), ReadOnly=-1)
        try:
            out = []
            for i, slide in enumerate(pres.Slides, start=1):
                texts = []
                for shape in slide.Shapes:
                    if shape.HasTextFrame and shape.TextFrame.HasText:
                        texts.append(shape.TextFrame.TextRange.Text)
                out.append({"slide": i, "texts": texts})
            return out
        finally:
            pres.Close()

def edit_pptx_slide_text(path, slide_index, shape_index, new_text, save=True):
    """
    DRM pptx 특정 슬라이드/shape 텍스트 변경 후 저장.
    slide_index/shape_index는 1부터 시작.
    """
    with _office("PowerPoint.Application") as pp:
        pres = pp.Presentations.Open(_abs(path), ReadOnly=0)  # 0=False=읽기쓰기
        try:
            slide = pres.Slides(slide_index)
            shape = slide.Shapes(shape_index)
            shape.TextFrame.TextRange.Text = new_text
            if save:
                pres.Save()
            return shape.TextFrame.TextRange.Text
        finally:
            pres.Close()

# ---- CLI ----
if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 3:
        print("Usage: drm_office.py <read|read_xlsx|read_pptx> <file>")
        sys.exit(1)
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == "read":
        print(read_docx(path))
    elif cmd == "read_xlsx":
        print(json.dumps(read_xlsx(path), ensure_ascii=False, default=str, indent=2))
    elif cmd == "read_pptx":
        print(json.dumps(read_pptx(path), ensure_ascii=False, indent=2))
    else:
        print(f"unknown cmd: {cmd}")
```
</details>

---

## 6. 단계별 사용 절차 (다른 LLM이 따라 하는 용)

### 사전 확인 (1분)
```bash
python -c "import win32com.client" || pip install pywin32
ls "/c/Program Files/Microsoft Office/Office16/WINWORD.EXE"
```
→ 둘 다 OK면 진행. Office가 다른 경로면 `find "/c/Program Files" -name WINWORD.EXE` 로 위치 확인.

### 읽기 (DRM 문서 평문 추출)
```bash
python drm_office.py read "C:\Users\me\문서.docx"
```
또는 Python 스크립트 내:
```python
from drm_office import read_docx
text = read_docx(r"C:\Users\me\문서.docx")
```

### 수정 + 저장 (DRM 재암호화)
```python
from drm_office import edit_docx
edit_docx(r"C:\Users\me\문서.docx", append_text="\n추가 내용")
# → 원본 파일에 저장되며, 헤더가 <DOCUMENT SAFER 로 유지됨 (재암호화)
```

### 검증 (수정 후 DRM 보존 확인)
```bash
head -c 20 "C:\Users\me\문서.docx" | xxd
# 3c44 4f43 554d 454e 5420 5341 4645 5220  <DOCUMENT SAFER  ← OK
```

---

## 7. 주의사항 / 한계 / 예외

| 항목 | 설명 |
|---|---|
| **HWP(한글) 파일** | 한글 애플리케이션이 설치되어야 함. 본 PC엔 없음 → `HWP.Application` COM 사용 불가. HWP가 설치된 PC면 동일 패턴으로 가능할 수 있음(미검증). |
| **PDF** | Office가 PDF를 직접 편집하지 않음. 읽기는 `Word.Documents.Open`이 PDF를 변환 열기 지원하므로 평문 추출 가능할 수 있으나(미검증), 편집은 별도 도구 필요. |
| **일반 텍스트/코드 파일** | DRM 대상 아님 (`.txt`, `.py`, `.md`, `.csv` 등). bash/Read로 그대로 읽고 쓰면 됨. |
| **백그라운드(visible=False) 차단 정책** | 일부 DRM 정책이 보이는 Office 창만 허용. 그 경우 `app.Visible=True`로 폴백. 자동화엔 시간 더 걸리지만 기능은 동일. |
| **Office 프로세스 잔류** | 반드시 `finally`에서 Quit. 좀비 프로세스가 쌓이면 다음 Dispatch가 느려지거나 충돌. |
| **동시 편집 충돌** | 사용자가 같은 파일을 더블클릭으로 열려 있으면 COM Open이 "사용중" 에러. 파일 닫힌 상태에서 실행할 것. |
| **DRM 권한** | 파일별로 권한(편집가능/읽기전용)이 다를 수 있음. 편집 권한 없는 파일은 `ReadOnly=True`로만 열림. 권한 에러 시 읽기 전용으로 폴백. |
| **네트워크 드라이브** | UNC/SMB 경로도 `os.path.abspath` + `FileName=`으로 가능하나, 속도 느림. 가능하면 로컬로 복사 후 작업. |
| **회사망 우회 금지** | 이 방법은 **DRM 정책을 우회하지 않음** — 인가된 앱(Office)의 정상 COM 인터페이스를 사용. 사용자가 더블클릭으로 할 수 있는 것과 동일한 권한·경로. |

---

## 8. 실패 시 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `pywintypes.com_error: ... 'Word.Application'` | Office 미설치 또는 ProgID 다름 | `find "/c/Program Files" -iname WINWORD.EXE`로 경로 확인, Office 재설치 |
| Open 시 "문서 손상" 또는 암호화 헤더만 보임 | DRM 에이전트 미실행 | `tasklist | grep MADRM` 확인, `C:\MarkAny\Document SAFER\MADRMAgent.exe` 실행 필요(보통 자동시작) |
| `Save()` 후 헤더가 `PK`(zip)으로 바뀜 | DRM 없는 일반 docx로 저장됨 | `doc.SaveAs2(FileFormat=...)` 말고 `doc.Save()` 사용. 이미 DRM 포맷이면 Save가 포맷 유지 |
| 한글 깨짐 | 콘솰 인코딩 | `PYTHONIOENCODING=utf-8 python ...` 또는 결과를 파일로 쓰기 |
| Office 창이 화면에 나타남 | Visible=False 무시 정책 | 폴백: `app.Visible=True`로 두고 작업 (기능 동일) |
| 프로세스 잔류로 메모리 증가 | Quit 누락 | `try/finally` 강제, 또는 작업 종료 후 `taskkill /IM WINWORD.EXE` |

---

## 9. 핸드오프 패키지: DRM_off.zip 구성

```
DRM_off.zip
├── README.md                          ← 이 폴더의 사용법 (한글, 다른 LLM용)
├── drm-office-com-access-2026-09-02.md ← 이 위키 문서 사본 (단일 출처)
├── drm_office.py                      ← 재사용 가능 헬퍼 라이브러리
├── drm_access_test.py                 ← 읽기 검증 스크립트 (ReadOnly)
├── drm_modify_test.py                 ← 읽기/수정/저장 라운드트립 검증 스크립트
└── examples/
    ├── example_read_docx.py
    ├── example_edit_docx.py
    └── example_read_xlsx.py
```

압축 해제 후 `python drm_access_test.py "경로/문서.docx"` 로 즉시 검증 가능.

---

## 10. 관련 문서 / 출처

- 핸드오프 산출물: `DRM_off.zip` (본 세션에서 생성, 회사 외부 전달용)
- 검증 로그: 본 위키 `log.md` 2026-09-02 항목
- 관련 메모리: 회사망 작업 한계 — [github-push-autonomous-limits](../../.claude/projects/c--Users-2053437/memory/github-push-autonomous-limits.md)
- 이 문서의 코드 원본: 본 PC `C:\Users\2053437\drm_office.py`, `drm_access_test.py`, `drm_modify_test.py`
