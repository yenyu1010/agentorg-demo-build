#!/usr/bin/env python3
"""
2026 FIFA World Cup D Group — USA vs Paraguay
Match: 2026-06-13 01:00 UTC | SoFi Stadium, LA (sea level, USA home)
value-modeler EV calculation script
"""

import math
from itertools import product

print("=" * 60)
print("USA vs PARAGUAY — EV MODEL")
print("2026-06-13 01:00 UTC | SoFi Stadium, LA")
print("=" * 60)

# ─────────────────────────────────────────────
# METHOD A: WEIGHTED SCORING (Logistic)
# ─────────────────────────────────────────────
print("\n── METHOD A: WEIGHTED SCORING ──")

form_usa = 4.8
form_par = 7.0
raw_diff = form_usa - form_par  # -2.2

# Quality correction: USA losses all vs top-10 opponents (Germany, Portugal, Belgium)
# Reduce effective penalty by 40%
quality_discount = 0.40
adjusted_diff = raw_diff * (1 - quality_discount)

print(f"Raw form diff (USA - PAR): {raw_diff:.2f}")
print(f"Opponent quality discount (40%): adjusted diff = {adjusted_diff:.4f}")

home_boost   =  0.05   # USA home/host nation
h2h_boost    =  0.03   # USA H2H advantage
injury_pen   = -0.02   # Enciso doubtful

form_logit_coeff = 0.15
form_logit = adjusted_diff * form_logit_coeff

total_logit_adj = form_logit + home_boost + h2h_boost + injury_pen
print(f"Form logit contribution : {form_logit:.4f}")
print(f"Home boost              : +{home_boost}")
print(f"H2H boost               : +{h2h_boost}")
print(f"Enciso injury penalty   : {injury_pen}")
print(f"Total logit adj (USA +) : {total_logit_adj:.4f}")

# De-vig market
o_usa, o_draw, o_par = 2.07, 3.20, 4.05
p_raw_usa  = 1/o_usa; p_raw_draw = 1/o_draw; p_raw_par = 1/o_par
vig = p_raw_usa + p_raw_draw + p_raw_par
p_mkt_usa  = p_raw_usa  / vig
p_mkt_draw = p_raw_draw / vig
p_mkt_par  = p_raw_par  / vig
print(f"\nMarket vig: {vig:.4f} ({(vig-1)*100:.2f}%)")
print(f"p_mkt_USA={p_mkt_usa:.4f}  p_mkt_draw={p_mkt_draw:.4f}  p_mkt_par={p_mkt_par:.4f}")

# Multinomial logit shift
def logit(p): return math.log(p/(1-p))
def sigmoid(x): return 1/(1+math.exp(-x))

l_usa  = logit(p_mkt_usa)  + total_logit_adj
l_draw = logit(p_mkt_draw)
l_par  = logit(p_mkt_par)  - total_logit_adj

p_adj_u = sigmoid(l_usa); p_adj_d = sigmoid(l_draw); p_adj_p = sigmoid(l_par)
tot = p_adj_u+p_adj_d+p_adj_p
p_A_usa  = p_adj_u/tot
p_A_draw = p_adj_d/tot
p_A_par  = p_adj_p/tot

print(f"\nMethod A results:")
print(f"  p_A_USA ={p_A_usa:.4f}  p_A_draw={p_A_draw:.4f}  p_A_par={p_A_par:.4f}")

# ─────────────────────────────────────────────
# METHOD B: POISSON MODEL
# ─────────────────────────────────────────────
print("\n── METHOD B: POISSON MODEL ──")

lambda_usa = 1.35   # lower-mid of 1.30-1.55; Paraguay elite defence (0.56 GA/game)
lambda_par = 0.90   # mid of 0.85-0.95; USA home defence improvement
print(f"lambda_USA={lambda_usa}  lambda_PAR={lambda_par}")

def poisson_pmf(k, lam):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

MAX_G = 7
score_matrix = {}
for gu in range(MAX_G+1):
    for gp in range(MAX_G+1):
        score_matrix[(gu,gp)] = poisson_pmf(gu, lambda_usa) * poisson_pmf(gp, lambda_par)

total_prob = sum(score_matrix.values())
print(f"Score matrix total prob (sanity): {total_prob:.6f}")

p_B_usa  = sum(v for (u,p),v in score_matrix.items() if u>p)
p_B_draw = sum(v for (u,p),v in score_matrix.items() if u==p)
p_B_par  = sum(v for (u,p),v in score_matrix.items() if u<p)
tb = p_B_usa+p_B_draw+p_B_par
p_B_usa/=tb; p_B_draw/=tb; p_B_par/=tb

print(f"Method B 1X2: p_B_USA={p_B_usa:.4f}  p_B_draw={p_B_draw:.4f}  p_B_par={p_B_par:.4f}")

# Totals
p_B_total = {}
for tg in range(MAX_G*2+1):
    p_B_total[tg] = sum(v for (u,p),v in score_matrix.items() if u+p==tg)

p_over2_win  = sum(v for g,v in p_B_total.items() if g>2)
p_over2_push = p_B_total.get(2,0)
p_under2_win = sum(v for g,v in p_B_total.items() if g<2)

print(f"O/U 2.0: over_win={p_over2_win:.4f}  push={p_over2_push:.4f}  under_win={p_under2_win:.4f}")

# ─────────────────────────────────────────────
# p_model AVERAGE
# ─────────────────────────────────────────────
print("\n── p_MODEL (AVERAGE A+B) ──")

p_m_usa  = (p_A_usa  + p_B_usa)  / 2
p_m_draw = (p_A_draw + p_B_draw) / 2
p_m_par  = (p_A_par  + p_B_par)  / 2

print(f"p_model_USA ={p_m_usa:.4f}  p_model_draw={p_m_draw:.4f}  p_model_par={p_m_par:.4f}")
print(f"Sum={p_m_usa+p_m_draw+p_m_par:.6f}")

div_usa  = abs(p_A_usa -p_B_usa )*100
div_draw = abs(p_A_draw-p_B_draw)*100
div_par  = abs(p_A_par -p_B_par )*100
print(f"\nDivergence: USA={div_usa:.2f}pp {'⚠>10pp' if div_usa>10 else 'OK'}  "
      f"Draw={div_draw:.2f}pp {'⚠>10pp' if div_draw>10 else 'OK'}  "
      f"PAR={div_par:.2f}pp {'⚠>10pp' if div_par>10 else 'OK'}")

# Handicap probabilities
p_m_usa_minus05  = (p_A_usa + p_B_usa) / 2          # USA wins only
p_m_par_plus05   = (p_A_draw+p_A_par + p_B_draw+p_B_par) / 2  # draw or PAR

# PAR +0.25
p_m_par025_win  = (p_A_par  + p_B_par)  / 2
p_m_par025_half = (p_A_draw + p_B_draw) / 2
p_m_par025_loss = (p_A_usa  + p_B_usa)  / 2

print(f"\nPAR +0.5 p_model = {p_m_par_plus05:.4f}")
print(f"PAR +0.25: win={p_m_par025_win:.4f}  half={p_m_par025_half:.4f}  loss={p_m_par025_loss:.4f}")

# ─────────────────────────────────────────────
# EV CALCULATION
# ─────────────────────────────────────────────
print("\n── EV CALCULATION ──")

o_par_plus05 = 1.82
o_over2      = 1.85
o_under2     = 2.03
o_par025     = 2.15

ev_usa      = p_m_usa      * o_usa      - 1
ev_draw     = p_m_draw     * o_draw     - 1
ev_par      = p_m_par      * o_par      - 1
ev_usa_m05  = p_m_usa_minus05 * o_usa   - 1   # same odds as moneyline
ev_par_p05  = p_m_par_plus05  * o_par_plus05 - 1
ev_over2    = p_over2_win * (o_over2-1) - p_under2_win * 1   # push at 2
ev_under2   = p_under2_win * (o_under2-1) - p_over2_win * 1  # push at 2
# PAR +0.25: full win + half win combo
ev_par025   = (p_m_par025_win  * (o_par025-1)
             + p_m_par025_half * ((o_par025-1)/2)
             - p_m_par025_loss * 1)

rows = [
    ("主勝 USA",          o_usa,      p_m_usa,         1/o_usa,         ev_usa),
    ("和局",              o_draw,     p_m_draw,        1/o_draw,        ev_draw),
    ("客勝 PAR",          o_par,      p_m_par,         1/o_par,         ev_par),
    ("亞盤 USA -0.5",     o_usa,      p_m_usa_minus05, 1/o_usa,         ev_usa_m05),
    ("亞盤 PAR +0.5",     o_par_plus05, p_m_par_plus05, 1/o_par_plus05, ev_par_p05),
    ("大 Over 2.0",       o_over2,    p_over2_win,     1/o_over2,       ev_over2),
    ("小 Under 2.0",      o_under2,   p_under2_win,    1/o_under2,      ev_under2),
    ("亞盤 PAR +0.25(馬*)",o_par025,  p_m_par025_win,  1/o_par025,      ev_par025),
]

print(f"\n{'市場':<26} {'賠率':>6} {'p_model':>9} {'隱含p(去水)':>12} {'EV%':>8}")
print("-" * 65)
for r in rows:
    print(f"  {r[0]:<24} {r[1]:>6.2f}  {r[2]:>9.4f}  {r[3]:>10.4f}  {r[4]*100:>+7.2f}%")

# ─────────────────────────────────────────────
# SIGNAL FUSION & CONFIDENCE
# ─────────────────────────────────────────────
print("\n── SIGNAL FUSION & CONFIDENCE ──")

def eval_mkt(name, ev, base, adjs):
    conf = base
    for reason, adj in adjs:
        conf += adj
    conf = max(1, min(5, conf))
    passes = ev*100 >= 3.0 and conf >= 3
    return conf, passes

signals = {
    "主勝 USA": (ev_usa, 3, [("資金流向巴拉圭受讓方向(反向)", -1)]),
    "亞盤 PAR +0.5": (ev_par_p05, 3, [
        ("資金流向巴拉圭受讓同向", +1),
        ("和局縮水同向(巴不輸)", +1),
    ]),
    "小 Under 2.0": (ev_under2, 3, [
        ("大小降盤2.25→2.0資金壓小球", +1),
        ("和局縮水同向低比分", +1),
    ]),
    "亞盤 PAR +0.25(馬*)": (ev_par025, 3, [
        ("資金流向巴拉圭受讓同向", +1),
        ("和局縮水支持和局機率", +1),
        ("威*** +0.25 盤口來源受限", -1),
    ]),
}

print(f"\n{'市場':<26} {'EV%':>8} {'基礎':>5} {'調整':>6} {'信心':>5} {'通過':>8} {'動作':>8}")
print("-" * 68)

recs = []
for name, (ev, base, adjs) in signals.items():
    adj_sum = sum(a for _,a in adjs)
    conf, passes = eval_mkt(name, ev, base, adjs)
    action = "✅ 建議" if passes else "❌ PASS"
    print(f"  {name:<24} {ev*100:>+7.2f}%  {base:>4}  {adj_sum:>+5}  {conf:>4}  "
          f"{'EV≥3%,信心≥3' if passes else 'FAIL':>10}  {action}")
    if passes:
        recs.append((name, ev, conf,
                     {"亞盤 PAR +0.5": (o_par_plus05, p_m_par_plus05),
                      "小 Under 2.0": (o_under2, p_under2_win),
                      "亞盤 PAR +0.25(馬*)": (o_par025, None)}.get(name)))

# ─────────────────────────────────────────────
# FRACTIONAL KELLY
# ─────────────────────────────────────────────
print("\n── FRACTIONAL KELLY (0.25×, 2% cap) ──")

kelly_out = []
for name, ev, conf, mkt in recs:
    if mkt is None:
        continue
    odds_k, p_k = mkt
    b = odds_k - 1

    if "PAR +0.25" in name:
        p_eff = p_m_par025_win + 0.5 * p_m_par025_half
        q_eff = 1 - p_eff
        kf = (b * p_eff - q_eff) / b
    elif "Under 2.0" in name:
        # Kelly with push: only win/loss matter for Kelly fraction
        # push reclaims stake, so effectively p_win and p_loss compete
        # b_eff = (odds-1), effective q = p_loss (push returns stake)
        kf = (p_under2_win * b - p_over2_win) / b
    else:  # PAR +0.5
        kf = (b * p_k - (1 - p_k)) / b

    k25    = kf * 0.25
    stake  = min(k25, 0.02)
    print(f"\n  {name}:")
    print(f"    Full Kelly={kf*100:.2f}%  0.25×Kelly={k25*100:.2f}%  Stake={stake*100:.2f}% bankroll")
    kelly_out.append((name, odds_k, ev*100, conf, stake*100))

# ─────────────────────────────────────────────
# SENSITIVITY ANALYSIS
# ─────────────────────────────────────────────
print("\n── SENSITIVITY ANALYSIS ──")

print("\n1. Enciso injury (帶傷首發 → 徹底缺陣，λ_PAR 0.90→0.70)")
lp_enc = 0.70
sm_enc = {}
for gu in range(MAX_G+1):
    for gp in range(MAX_G+1):
        sm_enc[(gu,gp)] = poisson_pmf(gu, lambda_usa) * poisson_pmf(gp, lp_enc)
p_enc_usa  = sum(v for (u,p),v in sm_enc.items() if u>p)
p_enc_draw = sum(v for (u,p),v in sm_enc.items() if u==p)
p_enc_par  = sum(v for (u,p),v in sm_enc.items() if u<p)
par05_enc  = p_enc_draw + p_enc_par
ev_par05_enc = par05_enc * o_par_plus05 - 1

p_enc_total = {}
for tg in range(MAX_G*2+1):
    p_enc_total[tg] = sum(v for (u,p),v in sm_enc.items() if u+p==tg)
p_enc_under_win = sum(v for g,v in p_enc_total.items() if g<2)
p_enc_over_win  = sum(v for g,v in p_enc_total.items() if g>2)
ev_under_enc = p_enc_under_win*(o_under2-1) - p_enc_over_win

print(f"  p(PAR +0.5): {p_m_par_plus05:.4f} → {par05_enc:.4f}")
print(f"  EV(PAR +0.5): {ev_par_p05*100:+.2f}% → {ev_par05_enc*100:+.2f}%  still positive: {'YES' if ev_par05_enc>0 else 'NO'}")
print(f"  EV(Under 2.0): {ev_under2*100:+.2f}% → {ev_under_enc*100:+.2f}% (Under improves if Enciso misses)")

print("\n2. USA quality-discount sensitivity")
print(f"  {'Disc%':>6} {'adj_diff':>9} {'p_A_USA':>9} {'p_A_PAR':>9} {'EV PAR+0.5':>12}")
for disc in [0.20, 0.30, 0.40, 0.50, 0.60]:
    adj = raw_diff * (1-disc)
    fl  = adj * form_logit_coeff
    tot = fl + home_boost + h2h_boost + injury_pen
    lu  = logit(p_mkt_usa)  + tot
    ld  = logit(p_mkt_draw)
    lp  = logit(p_mkt_par)  - tot
    pu=sigmoid(lu); pd=sigmoid(ld); pp=sigmoid(lp); t=pu+pd+pp
    pu/=t; pd/=t; pp/=t
    ev_p05 = (pd+pp) * o_par_plus05 - 1
    print(f"  {disc*100:>5.0f}%  {adj:>9.3f}  {pu:>9.4f}  {pp:>9.4f}  {ev_p05*100:>+11.2f}%")

print("\n3. Odds sensitivity (PAR +0.5)")
for test_odds in [1.75, 1.78, 1.82, 1.86, 1.90]:
    ev_t = p_m_par_plus05 * test_odds - 1
    print(f"  @{test_odds:.2f} → EV={ev_t*100:+.2f}%  {'PASS ≥3%' if ev_t*100>=3 else 'FAIL <3%'}")

# ─────────────────────────────────────────────
# CANADA CONTEXT
# ─────────────────────────────────────────────
print("\n── CANADA PARALLEL ──")
print("加拿大 WC 首場：同款「地主熱門被降盤」模式，最終 1-1（+0.5 全紅）。")
print("n=1 樣本，僅作脈絡，不得因此加碼。")

# ─────────────────────────────────────────────
# FINAL TABLE
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("FINAL RECOMMENDATION TABLE")
print("="*60)
if kelly_out:
    print(f"\n{'市場':<28} {'賠率':>6} {'EV%':>8} {'信心':>5} {'注碼% bankroll':>16}")
    print("-" * 68)
    for name, odds, ev, conf, stake in kelly_out:
        print(f"  {name:<26} {odds:>6.2f} {ev:>+7.2f}%  {conf:>4}  {stake:>15.2f}%")
else:
    print("\n  本輪無建議投注")

print("\n注：注碼為 bankroll % (0.25× Kelly, 上限 2%)")
print("    PAR +0.25 為馬* 報價；投注前確認最新賠率及平台可用性")

print("\n─── 免責聲明 ───────────────────────────────")
print("本分析為機率模型推估，僅供參考，不構成投注建議；")
print("博彩具風險，過往績效不代表未來表現；請遵守所在地法律並量力而為。")
print("────────────────────────────────────────────")
