---
name: dgx-h100-official-specs
description: NVIDIA DGX H100/H200 공식 component descriptions — CPU, GPU, 메모리, 네트워크, 전력 상세 스펙
metadata:
  type: reference
  created: 2026-08-27
  source: https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html
  verified: 2026-08-27
  supersedes: none
tags: [dgx-h100, h100, nvidia, gpu, cpu, system-memory, nvlink, infiniband, datasheet]
---

# NVIDIA DGX H100/H200 — 공식 Component Descriptions

> **출처**: NVIDIA DGX H100/H200 Systems User Guide (docs.nvidia.com/dgx)
> **본문**: https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html

---

## Component Description (Table 1)

| Component | H100 | H200 |
|---|---|---|
| **GPU** | 8 x NVIDIA H100 GPUs (640 GB total GPU memory) | 8 x NVIDIA H200 GPUs (1,128 GB total GPU memory) |
| **CPU** | 2 x Intel Xeon 8480C PCIe Gen5 CPUs | 2 x Intel Xeon 8480C PCIe Gen5 CPUs |
| CPU 코어/주파수 | 56코어 × 2 = 112 코어 (2.0/2.9/3.8 GHz) | 56코어 × 2 = 112 코어 (2.0/2.9/3.8 GHz) |
| **NVSwitch** | 4 x 4th gen NVLink (900 GB/s GPU-to-GPU) | 4 x 4th gen NVLink (900 GB/s GPU-to-GPU) |
| **Storage (OS)** | 2 x 1.92 TB NVMe M.2 SSD (RAID 1) | 2 x 1.92 TB NVMe M.2 SSD (RAID 1) |
| **Storage (Data Cache)** | 8 x 3.84 TB NVMe U.2 SED (RAID 0) | 8 x 3.84 TB NVMe U.2 SED (RAID 0) |
| **Network (Cluster)** | 4 x OSFP ports → 8 x ConnectX-7 IB (400Gbps) | 4 x OSFP ports → 8 x ConnectX-7 IB (400Gbps) |
| **Network (Mgmt)** | 2 x ConnectX-7 Dual Port Ethernet (400GbE) | 2 x ConnectX-7 Dual Port Ethernet (400GbE) |
| **System Memory** | 2 TB (32 x DIMM DDR5) | 2 TB (32 x DIMM DDR5) |
| **BMC** | 1 GbE RJ45 (Redfish, IPMI, SNMP, KVM, Web UI) | 1 GbE RJ45 (Redfish, IPMI, SNMP, KVM, Web UI) |
| **Power Supply** | 6 x 3.3 kW (최대 10.2kW @ 200-240V) | 6 x 3.3 kW (최대 10.2kW @ 200-240V) |

---

## Mechanical Specifications (Table 2)

| 항목 | 값 |
|---|---|
| Form Factor | 8U Rackmount |
| Height | 14" (356 mm) |
| Width | 19" (482.3 mm) max |
| Depth | 35.3" (897.1 mm) max |
| System Weight | 287.6 lbs (130.45 kg) max |

---

## Power Specifications (Table 3)

| 입력 | 사양 |
|---|---|
| **전원** | 6 x 3.3 kW PSU, balanced 분산 |
| **200-240V AC** | 10.2 kW 최대 · 3300W @ 200-240V, 16A, 50-60Hz |

---

## 분석 참고: 예전 잘못된 정보 교정

| 항목 | 이전에 쓴 것 (오류) | 공식 문서 (정확) |
|---|---|---|
| CPU | ~~8 x AMD EPYC 9004~~ | **2 x Intel Xeon 8480C** (56코어 × 2 = 112 코어) |
| GPU/서버 | ~~32 GPU/server (잘못된 SuperPOD 혼동)~~ | **8 GPU/server** (8U 단일 서버) |
| System Memory | 미명기 (또는 과대 추정) | **2TB (32 x DIMM DDR5)** |
| NVLink | 600 GB/s (추정치) | **900 GB/s GPU-to-GPU (4th gen NVLink)** |
| GPU 전력(TDP) | ~700W/GPU | **700W/GPU 공식 (전력 10.2kW = 8×700 + CPU + 기타)** |

> ⚠️ H100 SXM5의 GPU당 HBM3는 80GB이며, 단일 서버(8 GPU) = 640GB 총 GPU 메모리입니다.

---

## SuperPOD (8개 서버 조합) — 공식 문서 기반 재계산

> DGX H100 SuperPOD는 **4대 DGX H100 서버** + 네트워킹/스토리지 관리로 구성됩니다.
> (참조: NVIDIA DGX SuperPOD datasheet)

| 항목 | 값 |
|---|---|
| DGX H100 서버 | 4대 (8U × 4 = 32U) |
| GPU 총수 | 8 × 4 = **32 GPU** |
| 총 HBM3 | 640GB × 4 = **2,560GB = 2.5TB** |
| 총 CPU | 2 × 4 = **8개 Xeon 8480C** |
| 총 코어 | 112 × 4 = **448 코어** |
| 총 System Memory | 2TB × 4 = **8TB** |
| 총 GPU 전력 | 700W × 32 = **22.4kW** |
| 총 CPU 전력 | (2×112코어, ~250W/개) × 8 = **~2.0kW** |
| SuperPOD 총 전력 | **~40kW** (네트워킹·스토리지 포함) |

---

## v3 분석과의 정합성

- **H100 GPU 32개 / HBM 2.56TB** — v3 분석(§1.3)의 "32 GPU / 80GB×32"와 **일치** ✅
- **CPU 구성** — v3 분석에서는 CPU 명기 안 함. 신규 정보이나 v3 핵심(TPS/MW 역산)에 영향 없음 ✅
- **NVLink 900 GB/s** — v3 분석에서는 GPU당 3.35 TB/s(HBM 대역폭)만 사용. NVLink는 GPU-간 통신용이므로 v3 역산에 영향 없음 ✅
- **System Memory 2TB/서버** — v3 분석에서는 "System Memory"를 명기하지 않았음. 신규 추가 정보 ✅
- **전력 ~40kW** — v3 분석의 "~40kW SuperPOD"와 **일치** ✅

**결론**: CPU/SYSTEM_MEMORY/NVLink 신규 정보는 v3 핵심 분석(가중치·HBM·TPS/MW 역산)에 **영향 없음**. v3 분석의 수치는 그대로 유효합니다.
