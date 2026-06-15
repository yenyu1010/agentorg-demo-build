import math

# ============================================================
# Value Model: 智利天主大学 vs 康塞普西翁大学
# 2026-06-15 (賽後覆盤)
# ============================================================

print("=" * 60)
print("智利天主大学 vs 康塞普西翁大学 — 雙法勝率模型計算")
print("=" * 60)

# -------------------------------------------------------
# 方法一：加權評分法 (Weighted Scoring Method)
# -------------------------------------------------------
print("\n【方法一：加權評分法】")

# 動機修正
# 主隊★★★★★(爭冠)=高動機係數 1.0
# 客隊★★☆☆☆(中游)=低動機係數 0.6
# 平局動機調整：客隊高動機->平局機率微降

# 近期主場戰績近5場全勝，場均進3.8球失1.2球
home_form_score = 0.90   # 近5場主場全勝
away_form_score = 0.35   # 客場近5場1勝1平3負

# H2H: 主場壓倒性 (2026: 5-1, 2-2 客場平)
h2h_home = 0.85

# 讓球/市場隱含主隊強勢
market_signal_home = 0.80

# 動機
home_motivation = 1.00   # 爭冠
away_motivation = 0.50   # 中游保位

# 加權評分
# 近況50%, H2H20%, 市場訊號20%, 動機10%
w_form, w_h2h, w_market, w_motiv = 0.50, 0.20, 0.20, 0.10

home_score = (home_form_score * w_form + h2h_home * w_h2h +
              market_signal_home * w_market + home_motivation * w_motiv)
away_score = (away_form_score * w_form + (1 - h2h_home) * w_h2h +
              (1 - market_signal_home) * w_market + away_motivation * w_motiv)

print(f"主隊綜合評分: {home_score:.4f}")
print(f"客隊綜合評分: {away_score:.4f}")

# 將評分轉換為勝率 (logistic-style scaling)
total_score = home_score + away_score
# 平局基礎機率依聯賽水準設定
draw_base = 0.15  # 智利甲強強對弱，平局率偏低

home_raw = home_score / (home_score + away_score)
away_raw = away_score / (home_score + away_score)

# 縮放後保留平局空間
home_ws = home_raw * (1 - draw_base)
away_ws = away_raw * (1 - draw_base)
draw_ws = draw_base

# 正規化
total_ws = home_ws + draw_ws + away_ws
home_ws /= total_ws
draw_ws /= total_ws
away_ws /= total_ws

print(f"\n加權評分法 p_model:")
print(f"  主勝: {home_ws:.4f} ({home_ws*100:.1f}%)")
print(f"  平局: {draw_ws:.4f} ({draw_ws*100:.1f}%)")
print(f"  客勝: {away_ws:.4f} ({away_ws*100:.1f}%)")

# -------------------------------------------------------
# 方法二：簡化 Poisson 分布法
# -------------------------------------------------------
print("\n【方法二：簡化 Poisson 分布法】")

lambda_home = 3.0   # 從 form_analysis
lambda_away = 0.9   # 從 form_analysis

print(f"λ_home = {lambda_home}, λ_away = {lambda_away}")

def poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / math.factorial(k)

# Calculate score matrix (up to 7 goals each)
max_goals = 8
score_matrix = {}
for h in range(max_goals):
    for a in range(max_goals):
        score_matrix[(h, a)] = poisson_pmf(h, lambda_home) * poisson_pmf(a, lambda_away)

p_home_pois = sum(v for (h, a), v in score_matrix.items() if h > a)
p_draw_pois = sum(v for (h, a), v in score_matrix.items() if h == a)
p_away_pois = sum(v for (h, a), v in score_matrix.items() if h < a)

# Normalize for truncation
total_pois = p_home_pois + p_draw_pois + p_away_pois
p_home_pois /= total_pois
p_draw_pois /= total_pois
p_away_pois /= total_pois

print(f"\nPoisson 法 p_model:")
print(f"  主勝: {p_home_pois:.4f} ({p_home_pois*100:.1f}%)")
print(f"  平局: {p_draw_pois:.4f} ({p_draw_pois*100:.1f}%)")
print(f"  客勝: {p_away_pois:.4f} ({p_away_pois*100:.1f}%)")

# -------------------------------------------------------
# 大小球 Poisson
# -------------------------------------------------------
print("\n【大小球 Poisson — Over/Under 2.5】")

lambda_total = lambda_home + lambda_away
print(f"λ_total = {lambda_total:.2f}")

# P(total > 2.5) = P(total >= 3)
p_over25 = 1 - sum(poisson_pmf(k, lambda_total) for k in range(3))
p_under25 = 1 - p_over25
print(f"P(Over 2.5):  {p_over25:.4f} ({p_over25*100:.1f}%)")
print(f"P(Under 2.5): {p_under25:.4f} ({p_under25*100:.1f}%)")

# -------------------------------------------------------
# 混合模型 (Blended)
# -------------------------------------------------------
print("\n【混合模型 (60% Poisson + 40% 加權評分法)】")

w_pois, w_ws = 0.60, 0.40

home_blend = w_pois * p_home_pois + w_ws * home_ws
draw_blend = w_pois * p_draw_pois + w_ws * draw_ws
away_blend = w_pois * p_away_pois + w_ws * away_ws

# Normalize
total_blend = home_blend + draw_blend + away_blend
home_blend /= total_blend
draw_blend /= total_blend
away_blend /= total_blend

print(f"  主勝: {home_blend:.4f} ({home_blend*100:.1f}%)")
print(f"  平局: {draw_blend:.4f} ({draw_blend*100:.1f}%)")
print(f"  客勝: {away_blend:.4f} ({away_blend*100:.1f}%)")

# -------------------------------------------------------
# 市場隱含機率 (去水後)
# -------------------------------------------------------
print("\n【市場隱含機率（去水後）】")
imp_home = 0.62
imp_draw = 0.15
imp_away = 0.23
print(f"  主勝: {imp_home:.2f}, 平局: {imp_draw:.2f}, 客勝: {imp_away:.2f}")

# -------------------------------------------------------
# EV 計算
# -------------------------------------------------------
print("\n【EV 計算】")
print("EV = (p_model / p_implied) - 1")

# 主勝 1X2
odds_home = 1 / imp_home   # decimal odds from implied
ev_home = (home_blend / imp_home) - 1
print(f"\n主勝: model={home_blend:.4f}, impl={imp_home:.2f}, 隱含賠率={odds_home:.2f}")
print(f"  EV = {ev_home*100:+.2f}%")

# 平局
odds_draw = 1 / imp_draw
ev_draw = (draw_blend / imp_draw) - 1
print(f"\n平局: model={draw_blend:.4f}, impl={imp_draw:.2f}, 隱含賠率={odds_draw:.2f}")
print(f"  EV = {ev_draw*100:+.2f}%")

# 客勝
odds_away = 1 / imp_away
ev_away = (away_blend / imp_away) - 1
print(f"\n客勝: model={away_blend:.4f}, impl={imp_away:.2f}, 隱含賠率={odds_away:.2f}")
print(f"  EV = {ev_away*100:+.2f}%")

# -------------------------------------------------------
# 亞盤主讓一球/球半
# -------------------------------------------------------
print("\n【亞盤：主隊讓一球/球半 (-1/-1.5)】")
# 讓一球/球半組合盤 (Asian Handicap split -1/-1.5)
# 主讓-1全紅需主贏≥2，主讓-1半場需主贏≥3 (對半)
# 簡化: 使用 Poisson 計算各比分機率

p_home_by_2plus = sum(v for (h, a), v in score_matrix.items() if (h - a) >= 2)
p_home_by_3plus = sum(v for (h, a), v in score_matrix.items() if (h - a) >= 3)
p_home_by_1 = sum(v for (h, a), v in score_matrix.items() if (h - a) == 1)

# AH -1/-1.5 split:
# 贏差≥2: 全紅 (prob = p_home_by_2plus)
# 贏差=1: 半輸 (prob = p_home_by_1, 半注退回半注輸)
# 不贏或平: 全輸

p_ah_win_full = p_home_by_2plus / total_pois   # normalize
p_ah_win_half = p_home_by_1 / total_pois
p_ah_lose = 1 - p_ah_win_full - p_ah_win_half

# 亞盤典型水位 1.90/1.90 (去水各50%)
ah_imp = 0.50
# 有效EV: E[收益] = p_full*1 + p_half*0.5*return + p_lose*(-1)
# 假設賠率1.92 (含水)
ah_odds = 1.92
# EV per unit stake (去水盤 ~1.90):
ah_ev_per_unit = (p_ah_win_full * (ah_odds - 1) +
                  p_ah_win_half * ((ah_odds - 1) * 0.5) +
                  p_ah_lose * (-1))
# Compare with fair value
fair_prob_ah = p_ah_win_full + p_ah_win_half * 0.5
implied_prob_ah = 1 / ah_odds
ev_ah = (fair_prob_ah / implied_prob_ah) - 1

print(f"  P(主贏≥2球/全紅): {p_ah_win_full:.4f} ({p_ah_win_full*100:.1f}%)")
print(f"  P(主贏恰1球/半紅): {p_ah_win_half:.4f} ({p_ah_win_half*100:.1f}%)")
print(f"  P(輸/退): {p_ah_lose:.4f} ({p_ah_lose*100:.1f}%)")
print(f"  亞盤等效勝率(加權): {fair_prob_ah:.4f} ({fair_prob_ah*100:.1f}%)")
print(f"  假設賠率 {ah_odds}, 隱含機率={implied_prob_ah:.4f}")
print(f"  EV = {ev_ah*100:+.2f}%")

# -------------------------------------------------------
# 大球 2.5
# -------------------------------------------------------
print("\n【大小球 Over/Under 2.5】")
# Over 2.5 隱含機率從盤口估計 ~0.72 (強主隊場均3.8+0.9=4.7球)
# 典型市場 Over2.5 賠率在 1.40-1.50
imp_over25 = 0.72   # 市場隱含 (strong home team)
odds_over25 = 1.42  # approximate market odds
ev_over25 = (p_over25 / imp_over25) - 1
print(f"  Model P(Over 2.5): {p_over25:.4f} ({p_over25*100:.1f}%)")
print(f"  Market implied: {imp_over25:.2f} (賠率~{odds_over25})")
print(f"  EV = {ev_over25*100:+.2f}%")

# -------------------------------------------------------
# Kelly 建議 (0.25× Fractional Kelly)
# -------------------------------------------------------
print("\n【0.25× Fractional Kelly 計算】")
print("Kelly f = (b*p - q) / b，其中 b = 賠率-1, p = model prob, q = 1-p")
print("0.25× Kelly = f * 0.25")
print("上限: 2.0% of bankroll\n")

markets = [
    ("主勝 1X2",    home_blend,   odds_home,     imp_home),
    ("平局 1X2",    draw_blend,   odds_draw,     imp_draw),
    ("客勝 1X2",    away_blend,   odds_away,     imp_away),
    ("亞盤主隊讓一球/球半", fair_prob_ah, ah_odds, implied_prob_ah),
    ("大球 Over 2.5", p_over25,  odds_over25,   imp_over25),
]

EV_THRESHOLD = 0.03
CONF_THRESHOLD = 2.5  # 以 EV/σ 替代信心分數

results = []
for name, p_m, odds, p_imp in markets:
    b = odds - 1
    q = 1 - p_m
    kelly_f = (b * p_m - q) / b if b > 0 else 0
    kelly_025 = max(0, kelly_f * 0.25)
    kelly_025_capped = min(kelly_025, 0.020)
    ev = (p_m / p_imp) - 1
    recommended = ev >= EV_THRESHOLD and kelly_025 > 0
    results.append({
        "market": name, "p_model": p_m, "p_implied": p_imp,
        "ev": ev, "kelly_full": kelly_f,
        "kelly_025": kelly_025_capped,
        "recommended": recommended
    })
    print(f"市場: {name}")
    print(f"  p_model={p_m:.4f}, p_impl={p_imp:.4f}")
    print(f"  EV={ev*100:+.2f}%, Kelly={kelly_f*100:.2f}%, 0.25K={kelly_025*100:.2f}% (capped={kelly_025_capped*100:.2f}%)")
    print(f"  推薦: {'✅ YES' if recommended else '❌ NO (EV<3% 或 Kelly≤0)'}")
    print()

# -------------------------------------------------------
# 結論
# -------------------------------------------------------
print("=" * 60)
print("【結論】")
pos_ev = [(r["market"], r["ev"], r["kelly_025"]) for r in results if r["recommended"]]
if pos_ev:
    best = max(pos_ev, key=lambda x: x[1])
    print(f"最優推薦: {best[0]} — EV={best[1]*100:+.2f}%, 注碼={best[2]*100:.3f}% bankroll")
else:
    print("無建議投注 (無市場達 EV≥3% 門檻)")

