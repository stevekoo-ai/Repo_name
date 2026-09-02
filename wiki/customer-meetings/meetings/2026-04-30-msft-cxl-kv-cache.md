# MSFT — CXL KV Cache 미팅 (2026-04-30)

> **Source**: [sources/msft-cxl-kv-cache-meeting-2026-04-30.md](../../../sources/msft-cxl-kv-cache-meeting-2026-04-30.md) (불변 원문)
> **작성자**: 구병호(KOO BYEONG HO) DRAM Solution
> **날짜**: 2026-04-30
> **자사 참석자**: 강욱성 담당님, 심응보 팀장님, 이상돈 TL님, 구병호 TL
> **상대방 참석자**: Phyllis Ng (Microsoft)
> **관계**: MSFT = customer
> **성격**: MSFT KV Cache 이슈에 대한 SK hynix CXL DM Pooling 제안 — **2026-08-11 풀링 미팅 pathfinding의 직접 전신**

---

## 핵심 요약

| # | 주제 | 결론 / 핵심 팩트 |
|---|------|------------------|
| 1 | KV Cache 문제 + CXL DM Pooling 제안 | SSD 대비 CXL 10~100배 빠름 / RDMA 대비 지연 90% 감소(레이어 바이패스) / 비용 ~66% 효율 |
| 2 | MSFT 단계 | CXL **Path-finding** 단계 / CXL memory pooling AI 유스케이스 검토 중 / SW path-finding 집중(메모리 쉐어링, 동적/정적 할당) |
| 3 | AIC vs LPDDR AIC 비교 | Phyllis에게 제시 (원문 표 비어있으나 비교 논의됨) |
| 4 | 긍정 반응 | 낮은 전력 소비 관심 / **KV Cache 오프로딩 실험 결과 공유 제안 — 검토 동의** |
| 5 | 우려사항 | **Multi-sourcing 리스크** / AIC 방식은 서버 기구·열 설계 맞춤 카드 설계 가능(표준 FF 얽매이지 않아 유리) / **TCO 검증 필요**("Competitive TCO" 상세 분석 요구) |
| 6 | Action items | MSFT 전문가(Terry, Amanda, Rajesh) 추가(by Phyllis) → KV Cache Usage-Scenario + TCO 경쟁력 follow-up 미팅 |

---

## 상세 정리

### 1) KV Cache 문제 + SK Hynix CXL DM Pooling 제안
SK hynix가 Microsoft의 KV Cache 이슈에 대해 **CXL DM(Disaggregated Memory) Pooling 아키텍처** 제안:
- **속도**: SSD 대비 CXL = 10~100배 빠름
- **지연**: 기존 RDMA 대비 CXL은 레이어를 바이패스 → **지연시간 90% 감소**
- **비용**: CXL 하드웨어 ≈ **66% 더 비용 효율적**

**Phyllis feedback**: Microsoft는 현재 CXL에 대해 **Path-finding 단계**. CXL memory pooling의 AI 유스케이스 검토 중. 현재 **소프트웨어 path-finding에 집중** (메모리 쉐어링, 동적/정적 할당 등).

### 2) AIC vs SK Hynix CXL LPDDR Add-in Card 비교
Phyllis에게 두 폼팩터 비교 제시 (원문 표 내용 미기재, 비교 항목 자체는 논의됨).

**Phyllis feedback**:

**긍정적 반응**:
- 낮은 전력 소비에 긍정적 관심
- **AI KV Cache 오프로딩 실험 결과 공유 제안** → 같이 검토 진행 **동의**

**우려사항**:
- **Multi-sourcing 리스크** (단일 벤더 종속 우려)
- 현재 Add-in Card 방식 = 서버 기구/열 설계에 맞춤 카드 설계 가능 → **표준 폼팩터에 얽매이지 않아 유리** (AIC 장점으로 인식)
- **TCO 검증 필요**: "Competitive TCO" 주장에 대해 **더 상세한 TCO 분석 필요**

### Action Items
- MSFT의 CXL 관련 전문가 **Terry, Amanda, Rajesh** 추가 (by Phyllis Ng)
- **KV Cache Usage-Scenario** + **TCO 경쟁력** follow-up 미팅 진행

---

## 후속 액션 / 미해결

- [ ] **KV Cache 오프로딩 실험 결과 공유** (Phyllis 동의 → 후속 미팅에서)
- [ ] MSFT 전문가(Terry, Amanda, Rajesh) 참여 follow-up 미팅 setup
- [ ] **TCO 상세 분석** 준비 ("Competitive TCO" 주장 뒷받침)
- [ ] **Multi-sourcing 리스크** 대응 방안 (단일 벤더 우려 해소)
- [ ] KV Cache Usage-Scenario 정의 (MSFT와 공동)

## 관련 — 시계열 진화 (★ 핵심 인사이트)
> 본 04-30 미팅은 **2026-08-11 CXL 메모리 풀링 미팅**의 직접 전신. MSFT가 04-30 pathfinding → 08-11 pathfinding 단계 유지 + Pooled Appliance 시 협력.

- 2026-08-11 미팅(3개월 후): [2026-08-11-cxl-pooling.md](2026-08-11-cxl-pooling.md) — MSFT pathfinding 단계 유지, Pooled Appliance 시 협력. 본 04-30의 KV Cache 오프로딩 제안이 08-11 NVIDIA KV cache CXL 전환(★★★)과 Neo-Cloud 풀링 고객 맥락으로 확장.
- 2026-05-07 HPE: [2026-05-07-hpe-cxl-gen2.md](2026-05-07-hpe-cxl-gen2.md) — AIC Acceptance 역할(05-07) ↔ 본 04-30 AIC 표준 FF 얽매이지 않아 유리(04-30) 일관.
- by-customer: [msft.md](../by-customer/msft.md)
