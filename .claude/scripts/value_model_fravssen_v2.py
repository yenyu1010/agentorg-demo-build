#!/usr/bin/env python3
"""
Value Model v2: France vs Senegal — WC2026
修正：加權評分法改用分差驅動（而非比率），修正平局分配邏輯
2026-06-17T03:00 MetLife Stadium
"""

import math

# ─────────────────────────────────────────────────────────────
# STEP 1: 市場隱含機率
# ─────────────────────────────────────────────────────────────
odds_home, odds_draw, odds_away = 1.49, 4.50, 6.70
raw_h, raw_d, raw_a = 1/odds_home, 1/odds_draw, 1/odds_away
OR = raw_h + raw_d + raw_a
mkt_home = raw_h / OR
mkt_draw = raw_d / OR
mkt_away = raw_a / OR
print(f"[市場去水] 法勝={mkt_home:.4f} 平={mkt_draw:.4f} 塞勝={mkt_away:.4f}  超額={OR:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 2: Poisson 法（λ from form_analysis）
# ─────────────────────────────────────────────────────────────
lam_h, lam_a = 2.1, 0.9
MAX = 8

def pmf(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

scores = {(i, j): pmf(lam_h, i) * pmf(lam_a, j) for i in range(MAX) for j in range(MAX)}
S = sum(scores.values())
scores = {k: v/S for k, v in scores.items()}

p_hw = sum(v for (i,j),v in scores.items() if i > j)
p_dr = sum(v for (i,j),v in scores.items() if i == j)
p_aw = sum(v for (i,j),v in scores.items() if i < j)
print(f"[Poisson]  法勝={p_hw:.4f} 平={p_dr:.4f} 塞勝={p_aw:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 3: 加權評分法 v2（修正版）
#
# 方法：Dixon-Coles 風格
# 1. 用評分差 → 期望進球差 → 調整 Poisson λ
# 2. 不直接轉換成勝率，避免線性比例誤差
#
# 法國 fr_score=8.575 / 塞內加爾 sn_score=7.200
# 最強球隊基準 λ_ref_h=2.1（來自 form_analysis）
# 評分差歸一化到 λ 修正
# ─────────────────────────────────────────────────────────────
fr_score, sn_score = 8.575, 7.200
diff = fr_score - sn_score          # +1.375 法國優勢
ref_diff_for_lam = 10.0 - 7.0       # 滿分差 3.0 對應 λ 修正 ±0.5
lambda_adj = (diff / ref_diff_for_lam) * 0.5   # +0.229

lam_h_ws = lam_h + lambda_adj   # 略微提升法進球（已是高水準）
lam_a_ws = lam_a - lambda_adj * 0.5  # 塞內加爾輕微壓低

scores_ws = {(i, j): pmf(lam_h_ws, i) * pmf(lam_a_ws, j) for i in range(MAX) for j in range(MAX)}
S_ws = sum(scores_ws.values())
scores_ws = {k: v/S_ws for k, v in scores_ws.items()}

ws_home = sum(v for (i,j),v in scores_ws.items() if i > j)
ws_draw = sum(v for (i,j),v in scores_ws.items() if i == j)
ws_away = sum(v for (i,j),v in scores_ws.items() if i < j)
print(f"[評分法v2] lam_adj={lambda_adj:+.4f} → λh={lam_h_ws:.3f}/λa={lam_a_ws:.3f}")
print(f"           法勝={ws_home:.4f} 平={ws_draw:.4f} 塞勝={ws_away:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 4: 市場訊號調整
# 亞盤降線（1/1.5→1）= 市場不確定法能贏1.5球+
# 訊號強度 moderate → 下調法勝 2.5%，上調平/塞各1.25%
# ─────────────────────────────────────────────────────────────
signal_adj_h = -0.025
signal_adj_d = +0.012
signal_adj_a = +0.013

# ─────────────────────────────────────────────────────────────
# STEP 5: 融合
# Poisson 50% / 評分法 30% / 市場隱含 20%
# ─────────────────────────────────────────────────────────────
bw_p, bw_s, bw_m = 0.50, 0.30, 0.20

raw_bh = p_hw*bw_p + ws_home*bw_s + mkt_home*bw_m + signal_adj_h
raw_bd = p_dr*bw_p + ws_draw*bw_s + mkt_draw*bw_m + signal_adj_d
raw_ba = p_aw*bw_p + ws_away*bw_s + mkt_away*bw_m + signal_adj_a
BT = raw_bh + raw_bd + raw_ba
blend_home = raw_bh / BT
blend_draw = raw_bd / BT
blend_away = raw_ba / BT
print(f"\n[融合v2]  法勝={blend_home:.4f} ({blend_home*100:.2f}%)  "
      f"平={blend_draw:.4f} ({blend_draw*100:.2f}%)  "
      f"塞勝={blend_away:.4f} ({blend_away*100:.2f}%)")

# ─────────────────────────────────────────────────────────────
# STEP 6: 亞盤 & 大小球計算（用 Poisson 原始 λ 2.1/0.9）
# ─────────────────────────────────────────────────────────────
p_fr2plus      = sum(v for (i,j),v in scores.items() if i-j >= 2)
p_fr1exact     = sum(v for (i,j),v in scores.items() if i-j == 1)
p_sn_or_draw   = sum(v for (i,j),v in scores.items() if i <= j)

p_tot_le1 = sum(v for (i,j),v in scores.items() if i+j <= 1)
p_tot_eq2 = sum(v for (i,j),v in scores.items() if i+j == 2)
p_tot_ge3 = sum(v for (i,j),v in scores.items() if i+j >= 3)
p_tot_eq3 = sum(v for (i,j),v in scores.items() if i+j == 3)
p_tot_ge4 = sum(v for (i,j),v in scores.items() if i+j >= 4)
p_tot_le2 = sum(v for (i,j),v in scores.items() if i+j <= 2)

# 亞盤 法讓1球 水0.85（投法）
ev_ah_fr = p_fr2plus*0.85 + p_fr1exact*(0.5*0.85 - 0.5) + p_sn_or_draw*(-1.0)
# 亞盤 塞受讓1球 水1.04（投塞）
ev_ah_sn = p_sn_or_draw*1.04 + p_fr1exact*(-0.5 + 0.5*1.04) + p_fr2plus*(-1.0)
# 大球 2.75 水1.04
ev_over  = p_tot_ge3*1.04 + p_tot_eq2*(0.5*1.04) + p_tot_le1*(-1.0)
# 小球 2.75 水0.84
ev_under = p_tot_le2*0.84 + p_tot_eq3*(-0.5) + p_tot_ge4*(-1.0)

# 歐賠三路
ev_hw = blend_home * 1.49 - 1
ev_dr = blend_draw * 4.50 - 1
ev_aw = blend_away * 6.70 - 1

print(f"\n[大小球 Poisson 分布]")
print(f"  total<=1={p_tot_le1:.4f}  total==2={p_tot_eq2:.4f}  total>=3={p_tot_ge3:.4f}")
print(f"  total==3={p_tot_eq3:.4f}  total>=4={p_tot_ge4:.4f}  total<=2={p_tot_le2:.4f}")
print(f"  法贏2+={p_fr2plus:.4f}  法贏1={p_fr1exact:.4f}  平/塞={p_sn_or_draw:.4f}")

print(f"\n[EV 彙整]")
rows = [
    ("法勝（歐賠 1.49）",          ev_hw, blend_home),
    ("平局（歐賠 4.50）",          ev_dr, blend_draw),
    ("塞勝（歐賠 6.70）",          ev_aw, blend_away),
    ("亞盤 法讓1球 水0.85",        ev_ah_fr, None),
    ("亞盤 塞受讓1球 水1.04",      ev_ah_sn, None),
    ("大球 2.75 水1.04",           ev_over, p_tot_ge3),
    ("小球 2.75 水0.84",           ev_under, p_tot_le2),
]

print(f"{'市場':<28} {'p_model':>8} {'EV':>9} {'Value?'}")
print("-" * 60)
for name, ev, pm in rows:
    pm_s = f"{pm:.4f}" if pm else " (混合)"
    flag = "★ VALUE" if ev > 0.03 else ("△" if ev > 0 else "✗")
    print(f"{name:<28} {pm_s:>8} {ev:>+9.4f}  {flag}")

# ─────────────────────────────────────────────────────────────
# STEP 7: Kelly
# ─────────────────────────────────────────────────────────────
def kelly(p, b, frac=0.25):
    q = 1 - p
    k = (b*p - q) / b
    return max(0, k), max(0, k*frac)

conf = {
    "法勝（歐賠 1.49）":       (blend_home, 0.49, ev_hw,   2),
    "平局（歐賠 4.50）":       (blend_draw, 3.50, ev_dr,   2),
    "塞勝（歐賠 6.70）":       (blend_away, 5.70, ev_aw,   1),  # 信心低
    "亞盤 法讓1球 水0.85":     (p_fr2plus + 0.5*p_fr1exact, 0.85, ev_ah_fr, 2),
    "亞盤 塞受讓1球 水1.04":   (p_sn_or_draw + 0.5*p_fr1exact, 1.04, ev_ah_sn, 3),
    "大球 2.75 水1.04":        (p_tot_ge3 + 0.5*p_tot_eq2, 1.04, ev_over, 2),
    "小球 2.75 水0.84":        (p_tot_le2 - 0.5*p_tot_eq2, 0.84, ev_under, 3),
}

print(f"\n[Kelly 0.25×]")
print(f"{'市場':<28} {'p_eff':>7} {'EV':>8} {'KF全注':>7} {'KF25%':>7} {'信心':>4}")
print("-" * 70)
valid = []
for name, (pm, b, ev, c) in conf.items():
    kf, kfrac = kelly(pm, b)
    print(f"{name:<28} {pm:.4f} {ev:>+8.4f} {kf*100:>6.2f}% {kfrac*100:>6.2f}% {c}/5")
    if ev > 0.03 and c >= 2:
        valid.append((name, pm, b, ev, kf, kfrac, c))

print(f"\n[篩選結論] EV>3% & 信心≥2：")
if valid:
    valid.sort(key=lambda x: -x[3])
    for r, (name, pm, b, ev, kf, kfrac, c) in enumerate(valid, 1):
        print(f"  #{r} {name}  EV={ev:+.4f}  0.25×Kelly={kfrac*100:.2f}%  信心={c}/5")
else:
    print("  ❌ 無市場通過門檻 → 本輪建議：不投注")

print(f"""
[三方法彙整表]
方法          法勝      平局     塞勝
─────────────────────────────────────
市場隱含      {mkt_home:.4f}  {mkt_draw:.4f}  {mkt_away:.4f}
評分法v2      {ws_home:.4f}  {ws_draw:.4f}  {ws_away:.4f}
Poisson       {p_hw:.4f}  {p_dr:.4f}  {p_aw:.4f}
─────────────────────────────────────
融合(最終)    {blend_home:.4f}  {blend_draw:.4f}  {blend_away:.4f}
""")
