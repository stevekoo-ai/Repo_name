# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""
Jensen Huang Inference Economics — 단일 계산 엔진 (SSOT)

모든 파생 숫자(12점 좌표, 사용자 역산, KV cache, HBM/MainMem 점유율,
전력 역산, 99% HBM 전력 역산)를 한 곳에서 계산해 손계산 오류를 제거한다.

공식 모음
=========
- 사용자 역산     : users        = (TPS/MW × 1e6 × MW) / x
- 총 KV cache     : kv_total_GB  = ctx × users × kv_per_tok_MB / 1024
- per-user KV     : kv_per_user_GB = ctx × kv_per_tok_MB / 1024
- 총 필요 용량    : total_GB     = llm_GB + kv_total_GB
- HBM 초과율      : hbm_ratio    = total_GB / hbm_GB          (>1 = 초과)
- MainMem 초과율  : main_ratio   = max(0, total_GB - hbm_GB) / mainmem_GB
- 전력 역산(특정 점유율 p)
                  : P_MW         = users × x / (TPS_MW × 1e6)
                                      where users = (p×hbm - llm) / kv_per_user
"""
import json

# =====================================================================
# 1. GPU 상수 (SSOT)  — 단위: GB(GiB, ÷1024), MW
# =====================================================================
GPU = {
    'H100': dict(
        mw          = 0.040,     # Rack 운영 전력 [MW]  (40 kW, NVIDIA 공식)
        hbm_GB      = 2_560,     # 80 GB × 32 GPU
        mainmem_GB  = 8_192,     # 2 TB × 4 server
        gpu_cnt     = 32,
        tdp_w       = 700,       # GPU TDP
    ),
    'B300': dict(
        mw          = 0.121,     # 121 kW (GB300 NVL72, 웹 121~132kW 대역)
        hbm_GB      = 20_736,    # 288 GB × 72 GPU
        mainmem_GB  = 18_432,    # LPDDR5X 256 GB × 72
        gpu_cnt     = 72,
        tdp_w       = 1_400,
    ),
    'R100': dict(
        mw          = 0.101,     # ★ 101 kW (MaxLPS 소프트웨어 최적화, HBM 99% 안착)
        hbm_GB      = 20_736,    # 288 GB × 72 GPU (HBM4)
        mainmem_GB  = 18_432,    # base MainMemory (SOCAMM 80TB/CXL 별도)
        socamm_GB   = 80_000,    # 2nd stage (R100 전용)
        cxl_GB      = 100_000,   # 3rd stage (R100 전용)
        gpu_cnt     = 72,
        tdp_w       = 2_300,     # Max 상한
    ),
}

# =====================================================================
# 2. 그래프 12점 좌표  — x (context 레벨), TPS/MW (Y축)
# =====================================================================
X = {50: 'Free 32K', 100: 'Medium 128K', 200: 'High 128K', 400: 'Premium 400K'}
CONTEXT = {50: 32_000, 100: 128_000, 200: 128_000, 400: 400_000}

# TPS/MW (백만 단위). None = 1차 사망 (모델 로드 불가)
POINTS = {
    'H100': {50: 0.15, 100: 0.06, 200: None, 400: None},
    'B300': {50: 0.70, 100: 0.60, 200: 0.15, 400: 0.07},
    'R100': {50: 1.65, 100: 1.60, 200: 0.70, 400: 0.20},
}

# =====================================================================
# 3. LLM 스펙 (x=50/100/200/400)  — kv_per_tok [MB], llm weight [GB]
# =====================================================================
LLM = {
    50:  dict(name='Qwen3-235B-A22B',  attn='GQA',  kv_per_tok_MB=0.193,  llm_GB=470),
    100: dict(name='Kimi K2.5',        attn='MLA',  kv_per_tok_MB=0.072,  llm_GB=2_000),
    200: dict(name='GPT MoE 2T',       attn='GQA',  kv_per_tok_MB=0.246,  llm_GB=4_000),
    400: dict(name='GPT MoE 2T',       attn='GQA',  kv_per_tok_MB=0.246,  llm_GB=4_000),
}

# =====================================================================
# 4. 핵심 함수
# =====================================================================
def kv_per_user_GB(x):
    """맥락당 사용자 1명의 KV cache [GB]"""
    return CONTEXT[x] * LLM[x]['kv_per_tok_MB'] / 1024


def users_from_tps(gpu, x, tps_m=0):
    """TPS/MW → 동시 사용자 수. tps_m=None(1차사망)이면 None."""
    if tps_m is None:
        return None
    return (tps_m * 1e6 * GPU[gpu]['mw']) / x


def kv_total_GB(gpu, x, tps_m=None):
    """사용자 수 기반 총 KV cache [GB]"""
    u = users_from_tps(gpu, x, tps_m)
    if u is None:
        return None, None
    kv = CONTEXT[x] * u * LLM[x]['kv_per_tok_MB'] / 1024
    return kv, u


def total_GB(gpu, x, tps_m=None):
    """총 필요 용량 = LLM + KV [GB]"""
    kv, u = kv_total_GB(gpu, x, tps_m)
    if kv is None:
        return None, None, None
    return LLM[x]['llm_GB'] + kv, kv, u


def hbm_main_ratios(gpu, x, tps_m=None):
    """(총필요, HBM초과율, MainMem초과율)"""
    tot, kv, u = total_GB(gpu, x, tps_m)
    if tot is None:
        return None, None, None, None, u
    h = GPU[gpu]['hbm_GB']
    m = GPU[gpu]['mainmem_GB']
    hbm_ratio = tot / h                      # >1 = HBM 초과
    spill = max(0.0, tot - h)                # HBM 넘친 spill
    main_ratio = spill / m if m else 0.0     # spill이 MainMem 차지 % (상한 1)
    return tot, kv, u, hbm_ratio, main_ratio


def power_for_hbm_ratio(gpu, x, ratio=0.99):
    """특정 HBM 점유율(ratio)이 되도록 Rack 전력을 역산 [MW].
    Free 티어(x=50)를 결정 제약으로 사용.
    """
    hbm = GPU[gpu]['hbm_GB']
    target_total = ratio * hbm
    kv_target = target_total - LLM[x]['llm_GB']
    u = kv_target / kv_per_user_GB(x)
    tps_m = POINTS[gpu][x]                    # 이 GPU, 이 x의 TPS/MW
    p = (u * x) / (tps_m * 1e6)
    return p, u, kv_target


# =====================================================================
# 5. 출력: 12점 좌표 + 사용자 역산
# =====================================================================
def print_12_points():
    print('=' * 74)
    print('12개 점 좌표  (X = x 레벨, Y = TPS/MW)')
    print('=' * 74)
    hdr = (f"{'GPU':<6}{'x':>5}{'등급':<16}{'TPS/MW':>9}{'MW':>8}"
           f"{'사용자':>10}{'설명':<8}")
    print(hdr)
    print('-' * 74)
    for gpu in GPU:
        for x in X:
            tps_m = POINTS[gpu][x]
            if tps_m is None:
                print(f"{gpu:<6}{x:>5}{X[x]:<16}{'사망':>9}{GPU[gpu]['mw']:>8.3f}"
                      f"{'—':>10}  1차사망●")
                continue
            u = users_from_tps(gpu, x, tps_m)
            print(f"{gpu:<6}{x:>5}{X[x]:<16}{tps_m:>9.2f}M{GPU[gpu]['mw']:>8.3f}"
                  f"{u:>10,.0f}  {'실재' if gpu!='H100' or x<=100 else ''}")


# =====================================================================
# 6. 출력: HBM / MainMem 점유율 (전력 시나리오 반영 가능)
# =====================================================================
def print_capacity(mw_override=None, roster=None):
    """기본 GPU.mw 사용. mw_override로 특정 GPU 전력 교체 가능."""
    gpus = roster or list(GPU)
    print()
    print('=' * 104)
    print('KV Cache vs HBM/MainMemory  (LLM + KV ≤ HBM + MainMem 검증)')
    print('=' * 104)
    hdr = (f"{'GPU':<6}{'x':>5}{'등급':<16}{'사용자':>8}{'KV_GB':>11}"
           f"{'총필요GB':>11}{'HBM률':>8}{'MR률':>8}  상태")
    print(hdr)
    print('-' * 104)
    for gpu in gpus:
        mw = mw_override.get(gpu, GPU[gpu]['mw']) if mw_override else GPU[gpu]['mw']
        for x in X:
            tps_m = POINTS[gpu][x]
            if tps_m is None:
                print(f"{gpu:<6}{x:>5}{X[x]:<16}{'—':>8}{'—':>11}{'—':>11}"
                      f"{'—':>8}{'—':>8}  1차사망●")
                continue
            tot, kv, u = total_GB(gpu, x, tps_m)
            hbm_r = tot / GPU[gpu]['hbm_GB']
            spill = max(0.0, tot - GPU[gpu]['hbm_GB'])
            m_r = spill / GPU[gpu]['mainmem_GB']
            ok = '✓ 안착' if tot <= GPU[gpu]['hbm_GB'] + GPU[gpu]['mainmem_GB'] else '✗ 초과'
            print(f"{gpu:<6}{x:>5}{X[x]:<16}{u:>8,.0f}{kv:>11,.0f}"
                  f"{tot:>11,.0f}{hbm_r*100:>7.0f}%{m_r*100:>7.0f}%  {ok}")

    # R100 spill → SOCAMM/CXL 흡수 요약
    print()
    for gpu in gpus:
        if 'socamm_GB' not in GPU[gpu]:
            continue
        mw = mw_override.get(gpu, GPU[gpu]['mw']) if mw_override else GPU[gpu]['mw']
        print(f"--- {gpu} 3-Stage Memory 흡수 ({mw*1000:.0f} kW) ---")
        for x in X:
            tps_m = POINTS[gpu][x]
            if tps_m is None:
                continue
            tot, kv, u = total_GB(gpu, x, tps_m)
            soc = GPU[gpu]['socamm_GB']
            spray = max(0.0, tot - GPU[gpu]['hbm_GB'] - GPU[gpu]['mainmem_GB'])
            print(f"  x={x:<4} 총필요 {tot:>10,.0f} GB | HBM+MainMem "
                  f"{GPU[gpu]['hbm_GB']+GPU[gpu]['mainmem_GB']:>8,.0f} | "
                  f"추가 socamm필요 {spray:>10,.0f} GB / SOCAMM {soc:,.0f} "
                  f"({spray/soc*100:.1f}%)")


# =====================================================================
# 7. 전력 시나리오 비교 (R100) — 사용자/안착 검증
# =====================================================================
def print_power_scenarios():
    print()
    print('=' * 78)
    print('R100 전력 시나리오 비교 — Free(x=50) 결정 제약')
    print('=' * 78)
    scenarios = {
        '101 kW (MaxLPS)': 0.101,
        '120 kW (공급망 하한)': 0.120,
        '144 kW (Nominal ★)': 0.144,
        '165.6 kW (GPU-only Max-P)': 0.1656,
        '199 kW (기존 위키 정격)': 0.199,
    }
    hdr = (f"{'시나리오':<24}{'P_MW':>7}{'Free사용자':>12}{'총필요GB':>12}"
           f"{'vs 39,168':>12}  상태")
    print(hdr)
    print('-' * 78)
    hbm_plus_main = GPU['R100']['hbm_GB'] + GPU['R100']['mainmem_GB']
    for name, mw in scenarios.items():
        # 임시로 R100 전력 교체
        old = GPU['R100']['mw']
        GPU['R100']['mw'] = mw
        tot, kv, u = total_GB('R100', 50, POINTS['R100'][50])
        GPU['R100']['mw'] = old
        ratio = tot / hbm_plus_main
        ok = '✓' if ratio <= 1 else '✗ 초과'
        print(f"{name:<24}{mw:>7.3f}{u:>12,.0f}{tot:>12,.0f}"
              f"{ratio*100:>11.0f}%  {ok}")


# =====================================================================
# 8. 99% HBM 전력 역산 (R100 여러 티어별)
# =====================================================================
def print_99pct_hbm_inverse():
    print()
    print('=' * 78)
    print('"LLM+KV = HBM 99%" 전력 역산 (R100, 각 x 티어별)')
    print('=' * 78)
    hdr = (f"{'x':>5}{'등급':<16}{'kv/u_GB':>10}{'targetKV':>12}{'사용자':>10}"
           f"{'P_MW역산':>10}")
    print(hdr)
    print('-' * 78)
    for x in X:
        kvpu = kv_per_user_GB(x)
        hbm = GPU['R100']['hbm_GB']
        target = 0.99 * hbm - LLM[x]['llm_GB']
        u = target / kvpu
        p = (u * x) / (POINTS['R100'][x] * 1e6)
        print(f"{x:>5}{X[x]:<16}{kvpu:>10.2f}{target:>12,.0f}{u:>10,.0f}"
              f"{p:>10.4f} MW")


# =====================================================================
# MAIN
# =====================================================================
if __name__ == '__main__':
    print('JENSEN CHART CALC ENGINE  (kv ÷ 1024 규약)')
    print_12_points()
    print_capacity()
    print_power_scenarios()
    print_99pct_hbm_inverse()
