#!/usr/bin/env python3
"""
Value Model: France vs Senegal — WC2026
2026-06-17T03:00 MetLife Stadium
value-modeler agent | trace_id: 2026-06-17T02:33:00Z
"""

import math

print("=" * 65)
print("STEP 1: 市場隱含機率 (去除抽水，還原真實隱含)")
print("=" * 65)

# Raw European odds (現場即時)
odds_home   = 1.49   # 法勝
odds_draw   = 4.50   # 平局
odds_away   = 6.70   # 塞勝

raw_home = 1 / odds_home
raw_draw = 1 / odds_draw
raw_away = 1 / odds_away
overround = raw_home + raw_draw + raw_away

# Shin normalization (去水)
mkt_home = raw_home / overround
mkt_draw = raw_draw / overround
mkt_away = raw_away / overround

print(f"歐賠原始：法勝 {odds_home} / 平 {odds_draw} / 塞勝 {odds_away}")
print(f"原始隱含：{raw_home:.4f} / {raw_draw:.4f} / {raw_away:.4f}  (超額={overround:.4f})")
print(f"去水後市場隱含：法勝 {mkt_home:.4f} / 平 {mkt_draw:.4f} / 塞勝 {mkt_away:.4f}")

# Cross-check with odds-analyst quoted probabilities
print(f"\n賠率分析師報告去水：法勝 64.4% / 平 21.3% / 塞勝 14.3%")
print(f"本計算去水：法勝 {mkt_home*100:.1f}% / 平 {mkt_draw*100:.1f}% / 塞勝 {mkt_away*100:.1f}%")

print("\n" + "=" * 65)
print("STEP 2: 加權評分法 勝率估算")
print("=" * 65)

# Weight config (default — no calibration yet)
# 四維評分（基於 form_analysis 摘要）
# 分量：整體狀態(40%)、進攻(25%)、防守(20%)、動機(15%)

# 法國評分 (0–10)
fr_form     = 8.0   # 整體近況強，熱身1勝1負但科特迪瓦場次輪換
fr_attack   = 9.0   # 姆巴佩47球/季 + 奧利塞帽子戲法
fr_defense  = 8.5   # 薩利巴健康，世界級後防
fr_motive   = 9.5   # 奪冠熱門 + 姆巴佩歷史紀錄動機 ★★★★★

# 塞內加爾評分 (0–10)
sn_form     = 7.0   # 4場熱身2勝1平1負，中規中矩
sn_attack   = 6.5   # 馬內34歲+對美梅開二度，但缺乏縱深進攻選項
sn_defense  = 7.5   # 庫利巴利健康，4-3-3防守反擊體系紀律好
sn_motive   = 8.5   # 2022遺憾+馬內謝幕 ★★★★☆

w_form, w_att, w_def, w_mot = 0.40, 0.25, 0.20, 0.15

fr_score = fr_form*w_form + fr_attack*w_att + fr_defense*w_def + fr_motive*w_mot
sn_score = sn_form*w_form + sn_attack*w_att + sn_defense*w_def + sn_motive*w_mot

print(f"法國評分：form={fr_form} att={fr_attack} def={fr_defense} mot={fr_motive}")
print(f"  加權分：{fr_score:.3f}")
print(f"塞內加爾評分：form={sn_form} att={sn_attack} def={sn_defense} mot={sn_motive}")
print(f"  加權分：{sn_score:.3f}")

total_score = fr_score + sn_score
ratio_fr = fr_score / total_score
ratio_sn = sn_score / total_score

# Dixon-Coles style: allocate draw based on competitive gap
gap = ratio_fr - ratio_sn
base_draw = 0.22  # World Cup group stage base draw rate
# 差距越大，平局機率越低
draw_adj = base_draw * (1 - gap * 0.8)
draw_adj = max(0.12, min(draw_adj, 0.28))

ws_home = ratio_fr * (1 - draw_adj)
ws_draw = draw_adj
ws_away = ratio_sn * (1 - draw_adj)

# renormalize
ws_total = ws_home + ws_draw + ws_away
ws_home /= ws_total
ws_draw /= ws_total
ws_away /= ws_total

print(f"\n分數比：法國={ratio_fr:.4f} 塞內加爾={ratio_sn:.4f}  差距={gap:.4f}")
print(f"平局調整率：{draw_adj:.4f}")
print(f"加權評分法 p_model：法勝={ws_home:.4f} 平={ws_draw:.4f} 塞勝={ws_away:.4f}")

print("\n" + "=" * 65)
print("STEP 3: 簡化 Poisson 法")
print("=" * 65)

# λ from form_analysis
lam_h = 2.1   # 法國期望進球
lam_a = 0.9   # 塞內加爾期望進球

def poisson_pmf(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

max_goals = 7
p_home_win = 0.0
p_draw     = 0.0
p_away_win = 0.0

score_table = {}
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        p = poisson_pmf(lam_h, i) * poisson_pmf(lam_a, j)
        score_table[(i, j)] = p
        if i > j:
            p_home_win += p
        elif i == j:
            p_draw += p
        else:
            p_away_win += p

# renorm for truncation
total_p = p_home_win + p_draw + p_away_win
p_home_win /= total_p
p_draw     /= total_p
p_away_win /= total_p

print(f"λ：法國={lam_h} / 塞內加爾={lam_a}")
print(f"Poisson p_model：法勝={p_home_win:.4f} 平={p_draw:.4f} 塞勝={p_away_win:.4f}")

# Top 10 score lines
sorted_scores = sorted(score_table.items(), key=lambda x: -x[1])
print("\n最可能比分 Top 10：")
for score, prob in sorted_scores[:10]:
    print(f"  {score[0]}-{score[1]}  {prob*100:.2f}%")

print("\n" + "=" * 65)
print("STEP 4: 市場訊號調整 & 模型融合")
print("=" * 65)

# Signal adjustments:
# - 亞盤降線：法讓1/1.5 → 降至法讓1球 = 市場對法國信心略退
# - 高塞水1.04：支持塞勝（但仍是小機率事件）
# - H2H：2002年塞內加爾1-0法國（唯一正式記錄，有心理效應）
# - 大球水1.04破1.00：異常，但小球資金主導

# Asian handicap signal: reduce France dominance by ~3-5%
# 訊號為 moderate，小幅下調法勝，上調塞勝/平局

signal_adj_home = -0.030   # 亞盤降線訊號
signal_adj_draw = +0.012   # 平局輕微上調
signal_adj_away = +0.018   # 塞勝輕微上調

# Blending weights: form+odds 各方法
# Poisson: 40% (有 λ 基礎)
# Weighted Score: 35%
# Market implied: 25% (市場訊號中度)

blend_poisson = 0.40
blend_ws      = 0.35
blend_mkt     = 0.25

blend_home = p_home_win*blend_poisson + ws_home*blend_ws + mkt_home*blend_mkt
blend_draw = p_draw*blend_poisson + ws_draw*blend_ws + mkt_draw*blend_mkt
blend_away = p_away_win*blend_poisson + ws_away*blend_ws + mkt_away*blend_mkt

# Apply signal adjustments
blend_home += signal_adj_home
blend_draw += signal_adj_draw
blend_away += signal_adj_away

# Final renormalize
blend_total = blend_home + blend_draw + blend_away
blend_home /= blend_total
blend_draw /= blend_total
blend_away /= blend_total

print("融合權重：Poisson 40% / 加權評分 35% / 市場隱含 25%")
print("訊號調整：亞盤降線 →  法勝 -3.0% / 平 +1.2% / 塞勝 +1.8%")
print(f"\n融合 p_model（調整後）：")
print(f"  法勝：{blend_home:.4f} ({blend_home*100:.2f}%)")
print(f"  平局：{blend_draw:.4f} ({blend_draw*100:.2f}%)")
print(f"  塞勝：{blend_away:.4f} ({blend_away*100:.2f}%)")

print("\n" + "=" * 65)
print("STEP 5: 各市場 EV 計算")
print("=" * 65)

def calc_ev(p_model, odds):
    return p_model * odds - 1.0

# 1. 法勝（歐賠 1.49）
ev1 = calc_ev(blend_home, 1.49)

# 2. 平局（歐賠 4.50）
ev2 = calc_ev(blend_draw, 4.50)

# 3. 塞勝（歐賠 6.70）
ev3 = calc_ev(blend_away, 6.70)

# 4. 亞盤：法受讓1球
# 法受讓1球：若法國贏1球+則贏；若法國輸或平則輸；若法國贏恰好1球則退半注
# P(法勝 >= 2球) 需計算
p_fr_win_by2plus = sum(v for (i,j), v in score_table.items() if i - j >= 2) / total_p
p_fr_win_by1_exact = sum(v for (i,j), v in score_table.items() if i - j == 1) / total_p
p_sn_win_or_draw = sum(v for (i,j), v in score_table.items() if i <= j) / total_p

# 亞盤法受讓1球下注法國：
# 贏 = 法2球差以上 (水 0.85)
# 半贏 = 法贏1球差 (退半注，即 0.5×(0.85-1) + 0.5×0.85 的有效賠率)
# 輸 = 平或塞勝
# 有效賠率計算（1/1球線）
# 下注1u：
#   p(win_full)  = p_fr_win_by2plus
#   p(win_half)  = p_fr_win_by1_exact → 贏 0.5×(0.85-1)u = 退半 → net = +0.5×0.85 -0.5 = -0.075 per unit half... wait
#   實際上：全注1u，贏1球差時：退0.5u，剩0.5u以1.85賠率算
# 正確EV for 亞盤法讓1球（水 0.85，即賠 1.85倍）：
# EV = p_full * (1.85-1) + p_half * (0.5*(1.85-1) - 0.5*1) + p_lose * (-1)
# wait, standard Asian handicap: odds quoted are "return on win"
# 亞盤水 0.85 意指：投1u，贏則收 0.85u淨利（即賠率 1.85）
# 半勝（贏1球）：退半注，另半注贏，淨利 = 0.5 * 0.85
# 全輸（平/塞勝）：輸1u

ev_ah_fr_full  = p_fr_win_by2plus * 0.85
ev_ah_fr_half  = p_fr_win_by1_exact * (0.5 * 0.85 - 0.5 * 1.0)
ev_ah_fr_lose  = p_sn_win_or_draw * (-1.0)
ev_ah_fr = ev_ah_fr_full + ev_ah_fr_half + ev_ah_fr_lose

# 亞盤塞受讓1球（水 1.04，即賠 2.04倍）
# 塞受讓1球：若塞勝或平 → 全勝；若法贏1球差 → 半輸；若法贏2球+ → 全輸
ev_ah_sn_win   = p_sn_win_or_draw * 1.04   # 塞勝或平全收
ev_ah_sn_half  = p_fr_win_by1_exact * (-0.5 * 1.0 + 0.5 * 1.04)  # 半輸半退
ev_ah_sn_lose  = p_fr_win_by2plus * (-1.0)
ev_ah_sn = ev_ah_sn_win + ev_ah_sn_half + ev_ah_sn_lose

# 5. 大小球 2.75
# P(total >= 3) = under/over split
p_over_2_75 = sum(v for (i,j), v in score_table.items() if i+j >= 3) / total_p
p_under_2_75 = sum(v for (i,j), v in score_table.items() if i+j <= 2) / total_p
# 2.75線 = 2.5/3 混線
# 投大球：total >= 3全贏；total == 2半贏半退；total <= 1全輸
# 投小球：total <= 2全贏；total == 3半輸半退；total >= 4全輸... wait
# 2.75 = (2.5 + 3) / 2 混線：
# 大球 2.75（水 1.04）：
#   total >= 3: 全贏淨 1.04
#   total == 2: 半贏（0.5×1.04）
#   total <= 1: 全輸 -1
# 小球 2.75（水 0.84）：
#   total <= 2: 全贏淨 0.84
#   total == 3: 半輸（-0.5×1）
#   total >= 4: 全輸 -1

p_total_ge3 = sum(v for (i,j), v in score_table.items() if i+j >= 3) / total_p
p_total_eq2 = sum(v for (i,j), v in score_table.items() if i+j == 2) / total_p
p_total_le1 = sum(v for (i,j), v in score_table.items() if i+j <= 1) / total_p
p_total_le2 = sum(v for (i,j), v in score_table.items() if i+j <= 2) / total_p
p_total_eq3 = sum(v for (i,j), v in score_table.items() if i+j == 3) / total_p
p_total_ge4 = sum(v for (i,j), v in score_table.items() if i+j >= 4) / total_p

ev_over_275 = p_total_ge3 * 1.04 + p_total_eq2 * (0.5 * 1.04) + p_total_le1 * (-1.0)
ev_under_275 = p_total_le2 * 0.84 + p_total_eq3 * (-0.5) + p_total_ge4 * (-1.0)

print(f"Poisson 分布（λh={lam_h}, λa={lam_a}）：")
print(f"  法贏2球+   : {p_fr_win_by2plus:.4f} ({p_fr_win_by2plus*100:.2f}%)")
print(f"  法贏1球差   : {p_fr_win_by1_exact:.4f} ({p_fr_win_by1_exact*100:.2f}%)")
print(f"  平/塞勝    : {p_sn_win_or_draw:.4f} ({p_sn_win_or_draw*100:.2f}%)")
print(f"  total<=1   : {p_total_le1:.4f}  total==2: {p_total_eq2:.4f}  total>=3: {p_total_ge3:.4f}")
print(f"  total==3   : {p_total_eq3:.4f}  total>=4: {p_total_ge4:.4f}")
print()

markets = [
    ("法勝（歐賠 1.49）",           ev1,         blend_home, 1.49),
    ("平局（歐賠 4.50）",           ev2,         blend_draw, 4.50),
    ("塞勝（歐賠 6.70）",           ev3,         blend_away, 6.70),
    ("亞盤 法讓1球（水 0.85）",     ev_ah_fr,    None,       None),
    ("亞盤 塞受讓1球（水 1.04）",   ev_ah_sn,    None,       None),
    ("大球 2.75（水 1.04）",        ev_over_275, p_total_ge3,None),
    ("小球 2.75（水 0.84）",        ev_under_275,p_total_le2,None),
]

print(f"{'市場':<28} {'p_model':>8} {'賠率':>6} {'EV':>8} {'Value?':>8}")
print("-" * 62)
for name, ev, pm, od in markets:
    pm_str = f"{pm:.4f}" if pm else "  (混合)"
    od_str = f"{od:.2f}" if od else "  AH"
    flag = "★ VALUE" if ev > 0.03 else ("△ 低EV" if ev > 0 else "✗ 無")
    print(f"{name:<28} {pm_str:>8} {od_str:>6} {ev:>+8.4f} {flag:>8}")

print("\n" + "=" * 65)
print("STEP 6: Kelly 注碼建議（0.25× Fractional Kelly）")
print("=" * 65)

def kelly_fraction(p, b, fraction=0.25):
    """
    b = 淨賠率 (odds - 1)
    fraction = Kelly 分數
    """
    q = 1 - p
    k_full = (b * p - q) / b
    k_frac = k_full * fraction
    return max(0, k_full), max(0, k_frac)

print(f"\n{'市場':<28} {'p_model':>8} {'b(淨賠)':>8} {'KF全注%':>9} {'KF 0.25×%':>10} {'信心':>4}")
print("-" * 72)

# 信心評分：基於訊號強度、EV幅度、市場一致性
confidence_map = {
    "法勝（歐賠 1.49）":          (blend_home, 0.49, ev1,         2),
    "平局（歐賠 4.50）":          (blend_draw, 3.50, ev2,         2),
    "塞勝（歐賠 6.70）":          (blend_away, 5.70, ev3,         1),
    "亞盤 法讓1球（水 0.85）":    (None,       None, ev_ah_fr,    2),
    "亞盤 塞受讓1球（水 1.04）":  (None,       None, ev_ah_sn,    3),
    "大球 2.75（水 1.04）":       (p_total_ge3,1.04, ev_over_275, 2),
    "小球 2.75（水 0.84）":       (p_total_le2,0.84, ev_under_275,3),
}

kelly_results = {}
for name, (pm, b, ev, conf) in confidence_map.items():
    if pm is not None and b is not None:
        k_full, k_frac = kelly_fraction(pm, b)
        kelly_results[name] = (pm, b, ev, k_full, k_frac, conf)
        print(f"{name:<28} {pm:>8.4f} {b:>8.2f} {k_full*100:>8.2f}% {k_frac*100:>9.2f}% {conf:>4}/5")
    else:
        # AH: approximate effective probability
        if "法讓" in name:
            p_eff = p_fr_win_by2plus + 0.5 * p_fr_win_by1_exact
            b_eff = 0.85
            ev_eff = ev_ah_fr
        else:
            p_eff = p_sn_win_or_draw + 0.5 * p_fr_win_by1_exact
            b_eff = 1.04
            ev_eff = ev_ah_sn
        k_full, k_frac = kelly_fraction(p_eff, b_eff)
        kelly_results[name] = (p_eff, b_eff, ev_eff, k_full, k_frac, confidence_map[name][3])
        print(f"{name:<28} {p_eff:>8.4f}* {b_eff:>7.2f} {k_full*100:>8.2f}% {k_frac*100:>9.2f}% {confidence_map[name][3]:>4}/5")

print("\n* 亞盤 p_eff = 有效勝率（全勝+0.5×半勝）")

print("\n" + "=" * 65)
print("STEP 7: 最優建議排序 & 最終結論")
print("=" * 65)

# 篩選條件：EV > 3% AND 信心 >= 2
valid = [(name, vals) for name, vals in kelly_results.items()
         if vals[2] > 0.03 and vals[5] >= 2]
valid.sort(key=lambda x: -x[1][2])  # sort by EV desc

if valid:
    print(f"\n✅ 有效 Value 市場（EV > 3%, 信心 ≥ 2）：")
    for rank, (name, (pm, b, ev, kf, kfrac, conf)) in enumerate(valid, 1):
        print(f"\n  #{rank} {name}")
        print(f"     p_model={pm:.4f}  b={b:.2f}  EV={ev:+.4f} ({ev*100:+.2f}%)")
        print(f"     Full Kelly = {kf*100:.2f}%  0.25× Kelly = {kfrac*100:.2f}%")
        print(f"     信心={conf}/5  建議注碼 = {kfrac*100:.1f}% of bankroll")
else:
    print("\n❌ 無市場通過 EV > 3% + 信心 ≥ 2 門檻 → 本輪建議：不投注")

# Print all EVs for reference
print(f"\n── 各市場 EV 彙整 ──")
for name, (pm, b, ev, kf, kfrac, conf) in kelly_results.items():
    print(f"  {name:<30} EV={ev:+.4f} ({ev*100:+.2f}%)")

print("\n" + "=" * 65)
print("STEP 8: 總結數據輸出")
print("=" * 65)

print(f"""
方法          法勝      平局     塞勝
─────────────────────────────────────────
市場隱含      {mkt_home:.4f}  {mkt_draw:.4f}  {mkt_away:.4f}
加權評分法    {ws_home:.4f}  {ws_draw:.4f}  {ws_away:.4f}
Poisson法     {p_home_win:.4f}  {p_draw:.4f}  {p_away_win:.4f}
─────────────────────────────────────────
融合p_model   {blend_home:.4f}  {blend_draw:.4f}  {blend_away:.4f}
""")

print("免責聲明：本分析為機率模型推估，僅供參考，不構成投注建議；")
print("博彩具風險，過往績效不代表未來表現；請遵守所在地法律並量力而為。")
