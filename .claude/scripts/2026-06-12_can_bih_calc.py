#!/usr/bin/env python3
"""
2026 FIFA World Cup Group B — Canada vs Bosnia-Herzegovina
Date: 2026-06-12 19:00 UTC | Venue: BMO Field, Toronto (Canada home)
Value-Modeler EV Calculation Script
"""

import math
from itertools import product

print("=" * 70)
print("2026 WC B 組 — 加拿大 (CAN) vs 波黑 (BIH)")
print("賽前 ~6h 實際推薦 | 2026-06-12 19:00 UTC")
print("=" * 70)

# ─────────────────────────────────────────────
# 上游輸入（來自 form-analyst + odds-analyst）
# ─────────────────────────────────────────────

# Form scores
can_form_raw     = 6.0
bih_form_full    = 6.1
bih_form_normal  = 3.9

# Injury adjustments
can_inj_adj  = -0.03
bih_inj_adj  = -0.02

# Home/neutral
home_bonus   = +0.05
h2h_adj      = 0.00

# Poisson λ (raw)
lambda_can_att_raw = 1.3
lambda_bih_att_raw = 0.7

MEAN_GOAL = 1.2
MR_FACTOR = 0.70

# Odds (小數賠率)
odds_home      = 1.84
odds_draw      = 3.45
odds_away      = 4.80
odds_ahc_can   = 1.84
odds_ahc_bih   = 2.05
odds_over_225  = 2.05
odds_under_225 = 1.83

# ─────────────────────────────────────────────
# 方法 A
# ─────────────────────────────────────────────
print("\n【方法 A：加權評分法 — Logistic Mapping】")
print("-" * 50)

def method_a(can_form, bih_form, label):
    k = 0.40
    can_adj = can_form + can_inj_adj + home_bonus + h2h_adj
    bih_adj = bih_form + bih_inj_adj
    delta   = can_adj - bih_adj
    p_net   = 1 / (1 + math.exp(-k * delta))
    DRAW_BASE = 0.255
    p_draw  = DRAW_BASE * (1 - abs(p_net - 0.5))
    p_home  = p_net * (1 - p_draw)
    p_away  = (1 - p_net) * (1 - p_draw)
    total   = p_home + p_draw + p_away
    p_home /= total; p_draw /= total; p_away /= total
    print(f"  [{label}]")
    print(f"    加拿大調整分 = {can_form} + {can_inj_adj}(傷) + {home_bonus}(地主) = {can_adj:.2f}")
    print(f"    波黑調整分   = {bih_form} + {bih_inj_adj}(傷) = {bih_adj:.2f}")
    print(f"    Δ = {delta:.2f}  p_net = {p_net:.4f}  p_draw = {p_draw:.4f}")
    print(f"    p(加勝)={p_home:.4f} | p(和)={p_draw:.4f} | p(波勝)={p_away:.4f}  總和={p_home+p_draw+p_away:.6f}")
    return p_home, p_draw, p_away

pA1_h, pA1_d, pA1_a = method_a(can_form_raw, bih_form_full,   "A1 — 波黑含點球 6.1")
pA2_h, pA2_d, pA2_a = method_a(can_form_raw, bih_form_normal, "A2 — 波黑正常時間 3.9")

pA_h = (pA1_h + pA2_h) / 2
pA_d = (pA1_d + pA2_d) / 2
pA_a = (pA1_a + pA2_a) / 2
print(f"\n  方法 A 平均: 加勝={pA_h:.4f} | 和={pA_d:.4f} | 波勝={pA_a:.4f}")

# ─────────────────────────────────────────────
# 方法 B
# ─────────────────────────────────────────────
print("\n【方法 B：簡化 Poisson (0–6 矩陣)】")
print("-" * 50)

def poisson_pmf(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

lam_can = MR_FACTOR * lambda_can_att_raw + (1 - MR_FACTOR) * MEAN_GOAL
lam_bih = MR_FACTOR * lambda_bih_att_raw + (1 - MR_FACTOR) * MEAN_GOAL

print(f"  均值回歸後: λ_CAN={lam_can:.4f} | λ_BIH={lam_bih:.4f}  (MR={MR_FACTOR})")

GOALS = range(7)
matrix = {}
for i in GOALS:
    for j in GOALS:
        matrix[(i,j)] = poisson_pmf(lam_can, i) * poisson_pmf(lam_bih, j)

total_matrix = sum(matrix.values())
for k in matrix:
    matrix[k] /= total_matrix

pB_h = sum(matrix[(i,j)] for i,j in product(GOALS,GOALS) if i > j)
pB_d = sum(matrix[(i,j)] for i,j in product(GOALS,GOALS) if i == j)
pB_a = sum(matrix[(i,j)] for i,j in product(GOALS,GOALS) if i < j)
print(f"  Poisson 1X2: 加勝={pB_h:.4f} | 和={pB_d:.4f} | 波勝={pB_a:.4f}  總和={pB_h+pB_d+pB_a:.6f}")

pB_over25    = sum(matrix[(i,j)] for i,j in product(GOALS,GOALS) if i+j > 2)
pB_exactly2  = sum(matrix[(i,j)] for i,j in product(GOALS,GOALS) if i+j == 2)
pB_under2    = sum(matrix[(i,j)] for i,j in product(GOALS,GOALS) if i+j < 2)
pB_under25   = sum(matrix[(i,j)] for i,j in product(GOALS,GOALS) if i+j < 3)

print(f"  Over2.5={pB_over25:.4f} | Exactly2={pB_exactly2:.4f} | Under2={pB_under2:.4f} | Under2.5={pB_under25:.4f}")

pB_can_ah = pB_h
pB_bih_ah = pB_d + pB_a
print(f"  AH -0.5: CAN上盤贏={pB_can_ah:.4f} | BIH下盤贏={pB_bih_ah:.4f}")

# ─────────────────────────────────────────────
# 整合 p_model
# ─────────────────────────────────────────────
print("\n【p_model = (A + B) / 2】")
print("-" * 50)

pm_h = (pA_h + pB_h) / 2
pm_d = (pA_d + pB_d) / 2
pm_a = (pA_a + pB_a) / 2
pm_can_ah = pm_h
pm_bih_ah = pm_d + pm_a

print(f"  p_model: 加勝={pm_h:.4f} | 和={pm_d:.4f} | 波勝={pm_a:.4f}  總和={pm_h+pm_d+pm_a:.6f}")
print(f"  p_model AH: 加-0.5={pm_can_ah:.4f} | 波+0.5={pm_bih_ah:.4f}")

# OU 2.25 以 Poisson 為準
pm_ov_win  = pB_over25
pm_ov_half = pB_exactly2
pm_ov_lose = pB_under2

print(f"\n  OU2.25 基底(Poisson): 全贏(>2)={pm_ov_win:.4f} | 半輸(=2)={pm_ov_half:.4f} | 全輸(<2)={pm_ov_lose:.4f}")

# 分歧檢測
print("\n【分歧檢測 (>10pp)】")
for label, va, vb in [("主勝", pA_h, pB_h), ("和", pA_d, pB_d), ("客勝", pA_a, pB_a)]:
    diff = abs(va - vb)
    flag = " *** 模型分歧，信心降級 ***" if diff > 0.10 else " OK"
    print(f"  {label}: A={va:.4f} B={vb:.4f} 差={diff:.4f}{flag}")

# ─────────────────────────────────────────────
# EV
# ─────────────────────────────────────────────
print("\n【EV 計算】")
print("-" * 50)

def ev_simple(p, odds):
    return p * odds - 1

ev_home   = ev_simple(pm_h,    odds_home)
ev_draw   = ev_simple(pm_d,    odds_draw)
ev_away   = ev_simple(pm_a,    odds_away)
ev_can_ah = ev_simple(pm_can_ah, odds_ahc_can)
ev_bih_ah = ev_simple(pm_bih_ah, odds_ahc_bih)

b_ov = odds_over_225 - 1
b_un = odds_under_225 - 1

ev_over225  = pm_ov_win * b_ov + pm_ov_half * (-0.5) + pm_ov_lose * (-1)
ev_under225 = pm_ov_lose * b_un + pm_ov_half * (0.5 * b_un) + pm_ov_win * (-1)

print(f"  主勝(加拿大) odds={odds_home} p={pm_h:.4f} 隱含={1/odds_home:.4f} EV={ev_home*100:.2f}%")
print(f"  和局          odds={odds_draw} p={pm_d:.4f} 隱含={1/odds_draw:.4f} EV={ev_draw*100:.2f}%")
print(f"  客勝(波黑)   odds={odds_away} p={pm_a:.4f} 隱含={1/odds_away:.4f} EV={ev_away*100:.2f}%")
print(f"  亞盤 加-0.5  odds={odds_ahc_can} p={pm_can_ah:.4f} 隱含={1/odds_ahc_can:.4f} EV={ev_can_ah*100:.2f}%")
print(f"  亞盤 波+0.5  odds={odds_ahc_bih} p={pm_bih_ah:.4f} 隱含={1/odds_ahc_bih:.4f} EV={ev_bih_ah*100:.2f}%")
print(f"  大球 2.25    odds={odds_over_225} EV={ev_over225*100:.2f}%  (四分之一球盤)")
print(f"  小球 2.25    odds={odds_under_225} EV={ev_under225*100:.2f}%  (四分之一球盤)")

# ─────────────────────────────────────────────
# 訊號融合
# ─────────────────────────────────────────────
print("\n【訊號融合 & 信心係數（基準=3）】")
print("-" * 50)
print("  主勝(加拿大):  降盤-0.75→-0.5 + 歐賠走寬 1.79→1.84 → 信心 -1 = 2")
print("                「市場可能知道你不知道的事」(Davies 缺陣資訊流出?)")
print("  和局:          無明顯訊號 → 信心 = 3")
print("  客勝(波黑):    必發掛牌 5.20 vs 均價 4.61 (溢價=散戶多壓波黑客勝); 主勝成交 75% → 信心 -1 = 2")
print("  亞盤 加-0.5:   資金流向反向 → 信心 -1 = 2  ★ 市場可能知道你不知道的事")
print("  亞盤 波+0.5:   降盤資金湧入波黑下盤 → 與模型同向 → 信心 +1 = 4")
print("  大球 2.25:     大球資金強度 3/5, 機構 2.5 盤水 1.20-1.25 → 輕微同向 → 信心 = 3")
print("  小球 2.25:     市場大球偏向 → 反向 → 信心 -1 = 2")

conf = {
    "主勝":  2,
    "和局":  3,
    "客勝":  2,
    "加-0.5": 2,
    "波+0.5": 4,
    "大球":  3,
    "小球":  2,
}

# ─────────────────────────────────────────────
# Kelly
# ─────────────────────────────────────────────
print("\n【0.25 Kelly & 最終決策 (EV≥3% AND 信心≥3)】")
print("-" * 50)

EV_MIN   = 0.03
CONF_MIN = 3
K_FRAC   = 0.25
CAP      = 0.02

def kelly(p, odds, label, ev, conf_val):
    b = odds - 1
    q = 1 - p
    if b <= 0:
        print(f"  {label}: PASS (b≤0)")
        return None
    f_star = (p * b - q) / b
    stake  = max(0, min(K_FRAC * f_star, CAP))
    go = ev >= EV_MIN and conf_val >= CONF_MIN and f_star > 0
    reasons = []
    if ev < EV_MIN:  reasons.append(f"EV={ev*100:.2f}%<3%")
    if conf_val < CONF_MIN: reasons.append(f"信心{conf_val}<{CONF_MIN}")
    if f_star <= 0:  reasons.append("f*<0")
    verdict = "推薦" if go else "PASS"
    print(f"  {label}: p={p:.4f} odds={odds:.2f} EV={ev*100:.2f}% f*={f_star:.4f} "
          f"注碼={stake*100:.3f}% 信心={conf_val} → {verdict}"
          + (f"  ({', '.join(reasons)})" if reasons else ""))
    return stake if go else None

# AH 用 pm_can_ah / pm_bih_ah 的簡化 EV p；OU 用有效 p 顯示
# OU 有效 p (供 kelly 的 p*odds 展示等效)
p_over_eff  = pm_ov_win + pm_ov_half * 0.5  # 非直接 kelly，但用於 f* 估算
p_under_eff = pm_ov_lose + pm_ov_half * 0.5

rows = [
    ("主勝(加拿大)",  pm_h,        odds_home,     ev_home,    conf["主勝"]),
    ("和局",          pm_d,        odds_draw,     ev_draw,    conf["和局"]),
    ("客勝(波黑)",    pm_a,        odds_away,     ev_away,    conf["客勝"]),
    ("亞盤 加-0.5",  pm_can_ah,   odds_ahc_can,  ev_can_ah,  conf["加-0.5"]),
    ("亞盤 波+0.5",  pm_bih_ah,   odds_ahc_bih,  ev_bih_ah,  conf["波+0.5"]),
    ("大球 2.25",    p_over_eff,  odds_over_225, ev_over225, conf["大球"]),
    ("小球 2.25",    p_under_eff, odds_under_225,ev_under225,conf["小球"]),
]

stakes = {}
for label, p, odds, ev, conf_val in rows:
    s = kelly(p, odds, label, ev, conf_val)
    stakes[label] = s

# ─────────────────────────────────────────────
# 最終輸出
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("【全市場 EV 排序表】")
print("=" * 70)
print(f"  {'市場':<14} {'賠率':>5} {'p_model':>8} {'隱含p':>7} {'EV%':>7} {'信心':>4} {'決策'}")
print(f"  {'-'*14} {'-'*5} {'-'*8} {'-'*7} {'-'*7} {'-'*4} {'-'*6}")

sorted_rows = sorted(rows, key=lambda x: x[3], reverse=True)
for label, p, odds, ev, conf_val in sorted_rows:
    implied = 1/odds
    verdict = "推薦" if stakes[label] is not None else "PASS"
    print(f"  {label:<14} {odds:>5.2f} {p:>8.4f} {implied:>7.4f} {ev*100:>7.2f} {conf_val:>4} {verdict}")

print("\n【最終推薦表】")
recommend = [(l, o, p, ev, cv, stakes[l]) for l, p, o, ev, cv in rows if stakes[l] is not None]
if not recommend:
    print("\n  ❌ 本場無建議投注")
    print("  所有市場均未同時通過 EV≥3% + 信心≥3 雙重門檻。")
else:
    print(f"\n  {'場次':<20} {'市場':<14} {'方向':>8} {'賠率':>5} {'p_model':>8} {'隱含p':>7} {'EV%':>7} {'注碼%':>7} {'信心':>4}")
    for label, odds_v, p, ev, cv, stake in recommend:
        implied = 1/odds_v
        print(f"  {'加拿大 vs 波黑':<20} {label:<14} {'上盤':>8} {odds_v:>5.2f} {p:>8.4f} {implied:>7.4f} {ev*100:>7.2f} {stake*100:>7.3f} {cv:>4}")

print("\n【角球盤 — 定性評論（不計算 EV）】")
print("-" * 50)
print("  盤口 9.0 球  大 @2.02 / 小 @1.78")
print("  App 數據：加拿大場均角球 7.2 + 波黑 5.0 = 12.2（樣本不明、不可信）")
print("  → 不計算 EV；定性觀察：若加拿大強攻可能偏大，但數據未驗證。")

print("\n【敏感度說明】")
print("-" * 50)
print(f"  波黑評分敏感度:  A1(含點球6.1) 加勝={pA1_h:.4f}  A2(正常時間3.9) 加勝={pA2_h:.4f}")
print(f"  均值回歸: λ_CAN {lambda_can_att_raw}→{lam_can:.3f}  λ_BIH {lambda_bih_att_raw}→{lam_bih:.3f}  (MR=0.70)")
print(f"  Davies 缺陣: 本模型-0.03保守值；若視為-0.05，加拿大勝率再降~1pp")
print(f"  波黑λ=0.7可能低估（強度混雜）：若λ→1.0，波黑勝率升約4-6pp，大球概率升")

print("\n" + "=" * 70)
print("計算完畢")
print("=" * 70)
