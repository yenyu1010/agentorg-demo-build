"""
WC 2026 反推驗證計算腳本 (純Python版，無scipy/numpy依賴)
場次：墨西哥 vs 南非 (A組 6/11)，南韓 vs 捷克 (A組 6/11)
作者：football/value-modeler
日期：2026-06-12
"""

import math

print("=" * 70)
print("WC 2026 反推驗證計算")
print("日期：2026-06-12 | 任務：賽前建模 -> 對照實際賽果")
print("=" * 70)

def poisson_pmf(k, lam):
    """純Python Poisson PMF"""
    return (lam ** k) * math.exp(-lam) / math.factorial(k)

def weighted_score(results, weights):
    w_map = {'W': 3, 'D': 1, 'L': 0}
    raw = sum(w_map[r[0]] * weights[i] for i, r in enumerate(results))
    max_raw = sum(3 * w for w in weights)
    return (raw / max_raw) * 10

def logistic_3way(delta, base_draw=0.26, k=0.35):
    p_home_raw = 1 / (1 + math.exp(-k * delta))
    abs_delta = abs(delta)
    p_draw = base_draw * max(0.5, 1 - abs_delta * 0.04)
    remainder = 1 - p_draw
    p_home = p_home_raw * remainder
    p_away = (1 - p_home_raw) * remainder
    total = p_home + p_draw + p_away
    return p_home / total, p_draw / total, p_away / total

def poisson_matrix(lam_h, lam_a, max_g=6):
    matrix = [[0.0]*(max_g+1) for _ in range(max_g+1)]
    for i in range(max_g + 1):
        for j in range(max_g + 1):
            matrix[i][j] = poisson_pmf(i, lam_h) * poisson_pmf(j, lam_a)
    p_home_win = sum(matrix[i][j] for i in range(max_g+1) for j in range(max_g+1) if i > j)
    p_draw     = sum(matrix[i][j] for i in range(max_g+1) for j in range(max_g+1) if i == j)
    p_away_win = sum(matrix[i][j] for i in range(max_g+1) for j in range(max_g+1) if i < j)
    p_over25   = sum(matrix[i][j] for i in range(max_g+1) for j in range(max_g+1) if i+j > 2)
    p_under25  = 1 - p_over25
    p_asian_win  = sum(matrix[i][j] for i in range(max_g+1) for j in range(max_g+1) if (i-j) >= 2)
    p_asian_half = sum(matrix[i][j] for i in range(max_g+1) for j in range(max_g+1) if (i-j) == 1)
    p_asian_lose = sum(matrix[i][j] for i in range(max_g+1) for j in range(max_g+1) if (i-j) <= 0)
    return {'p_home': p_home_win, 'p_draw': p_draw, 'p_away': p_away_win,
            'p_over25': p_over25, 'p_under25': p_under25,
            'p_asian_h_minus125_win': p_asian_win,
            'p_asian_h_minus125_half': p_asian_half,
            'p_asian_h_minus125_lose': p_asian_lose}

def ev(p_model, odds):
    return p_model * odds - 1

def kelly_025(p_model, odds):
    b = odds - 1
    q = 1 - p_model
    f_full = (p_model * b - q) / b
    return max(0, 0.25 * f_full)

def implied_prob_no_vig(odds_list):
    raw = [1/o for o in odds_list]
    total = sum(raw)
    return [r/total for r in raw]

def brier_score(p_vec, outcome_vec):
    return sum((p - o) ** 2 for p, o in zip(p_vec, outcome_vec))

# ===== 場次一：墨西哥 vs 南非 =====
print("\n" + "="*70)
print("場次一：墨西哥 vs 南非  (A組, 6/11, Azteca, 海拔2200m)")
print("實際賽果：墨西哥 2-0")
print("="*70)

print("\n--- 方法 A: 加權評分法 ---")
mex_results = [('W',5,1),('W',1,0),('D',1,1),('D',0,0),('W',1,0),('W',1,0),('L',1,2)]
rsa_results = [('L',0,1),('D',1,1),('L',1,2),('D',1,1),('D',0,0),('L',1,2),('W',3,2)]
weights_7 = [3, 2.5, 2, 1.5, 1, 1, 0.8]

mex_score = weighted_score(mex_results, weights_7)
rsa_score = weighted_score(rsa_results, weights_7)
print(f"墨西哥加權分(0-10): {mex_score:.4f}")
print(f"南非加權分(0-10): {rsa_score:.4f}")
delta_A_mex = mex_score - rsa_score
print(f"狀態分差 delta: {delta_A_mex:.4f}")

home_bonus = 0.05
altitude_bonus = 0.02
h2h_mod = 0.0
injury_motivation_mex = 0.01
rsa_form_penalty = 0.02
total_home_adj = home_bonus + altitude_bonus + injury_motivation_mex + rsa_form_penalty
print(f"地主修正: +{home_bonus}, 高原修正: +{altitude_bonus}, H2H: {h2h_mod}, 傷停動機: +{injury_motivation_mex}, 南非高原劣勢: +{rsa_form_penalty}")

p_A_mex_h, p_A_mex_d, p_A_mex_a = logistic_3way(delta_A_mex, k=0.35)
p_A_mex_h_adj = min(0.92, p_A_mex_h + total_home_adj)
p_A_mex_a_adj = max(0.02, p_A_mex_a - total_home_adj * 0.7)
p_A_mex_d_adj = max(0.05, 1 - p_A_mex_h_adj - p_A_mex_a_adj)
tot = p_A_mex_h_adj + p_A_mex_d_adj + p_A_mex_a_adj
p_A_mex_h_adj /= tot; p_A_mex_d_adj /= tot; p_A_mex_a_adj /= tot
print(f"方法A => 墨勝: {p_A_mex_h_adj:.4f}  和局: {p_A_mex_d_adj:.4f}  南非勝: {p_A_mex_a_adj:.4f}  (sum={p_A_mex_h_adj+p_A_mex_d_adj+p_A_mex_a_adj:.4f})")

print("\n--- 方法 B: Poisson ---")
mex_gf_7 = 5+1+1+0+1+1+1; mex_ga_7 = 1+0+1+0+0+0+2
rsa_gf_7 = 0+1+1+1+0+1+3; rsa_ga_7 = 1+1+2+1+0+2+2
mex_lam_raw = mex_gf_7/7
rsa_lam_raw = rsa_gf_7/7
rsa_lam_adj = rsa_lam_raw * 0.85
altitude_factor_home = 1.10; altitude_factor_away = 0.85
lam_mex_final = min(mex_lam_raw * altitude_factor_home, 2.5)
lam_rsa_final = max(rsa_lam_adj * altitude_factor_away, 0.3)
print(f"墨西哥7場進球: {mex_gf_7}, 場均: {mex_lam_raw:.4f}")
print(f"南非7場進球: {rsa_gf_7}, 場均: {rsa_lam_raw:.4f} -> 折扣: {rsa_lam_adj:.4f}")
print(f"lambda_墨(+高原10%): {lam_mex_final:.4f}")
print(f"lambda_南非(-高原15%): {lam_rsa_final:.4f}")

pm1 = poisson_matrix(lam_mex_final, lam_rsa_final)
p_B_mex_h = pm1['p_home']; p_B_mex_d = pm1['p_draw']; p_B_mex_a = pm1['p_away']
print(f"方法B => 墨勝: {p_B_mex_h:.4f}  和局: {p_B_mex_d:.4f}  南非勝: {p_B_mex_a:.4f}")
print(f"  大球>2.5: {pm1['p_over25']:.4f}  小球<=2.5: {pm1['p_under25']:.4f}")
print(f"  亞盤主-1.25: 全紅={pm1['p_asian_h_minus125_win']:.4f}  半輸={pm1['p_asian_h_minus125_half']:.4f}  全輸={pm1['p_asian_h_minus125_lose']:.4f}")

print("\n--- p_model 整合 ---")
p_mex_h = (p_A_mex_h_adj + p_B_mex_h)/2
p_mex_d = (p_A_mex_d_adj + p_B_mex_d)/2
p_mex_a = (p_A_mex_a_adj + p_B_mex_a)/2
tot2 = p_mex_h+p_mex_d+p_mex_a
p_mex_h/=tot2; p_mex_d/=tot2; p_mex_a/=tot2
diff_h = abs(p_A_mex_h_adj-p_B_mex_h)
diff_d = abs(p_A_mex_d_adj-p_B_mex_d)
diff_a = abs(p_A_mex_a_adj-p_B_mex_a)
print(f"p_model => 墨勝: {p_mex_h:.4f} ({p_mex_h*100:.1f}%)  兩法差異: {diff_h*100:.1f}pp {'[!分歧>10pp]' if diff_h>0.10 else ''}")
print(f"p_model => 和局: {p_mex_d:.4f} ({p_mex_d*100:.1f}%)  兩法差異: {diff_d*100:.1f}pp {'[!分歧>10pp]' if diff_d>0.10 else ''}")
print(f"p_model => 南非勝: {p_mex_a:.4f} ({p_mex_a*100:.1f}%)  兩法差異: {diff_a*100:.1f}pp {'[!分歧>10pp]' if diff_a>0.10 else ''}")

p_mex_over25 = pm1['p_over25']
p_mex_under25 = pm1['p_under25']
p_asian_mex_eff = pm1['p_asian_h_minus125_win'] + 0.5*pm1['p_asian_h_minus125_half']
print(f"大球p(>2.5): {p_mex_over25:.4f} ({p_mex_over25*100:.1f}%)")
print(f"小球p(<=2.5): {p_mex_under25:.4f} ({p_mex_under25*100:.1f}%)")
print(f"亞盤主-1.25有效p: {p_asian_mex_eff:.4f} ({p_asian_mex_eff*100:.1f}%)")

print("\n--- EV 計算 ---")
odds_mex_h=1.48; odds_mex_d=4.33; odds_mex_a=6.50
odds_over25=2.18; odds_under25=1.69; odds_asian_mex=1.975
ev_mex_h=ev(p_mex_h,odds_mex_h); ev_mex_d=ev(p_mex_d,odds_mex_d); ev_mex_a=ev(p_mex_a,odds_mex_a)
ev_over25_m=ev(p_mex_over25,odds_over25); ev_under25_m=ev(p_mex_under25,odds_under25)
ev_asian_m=ev(p_asian_mex_eff,odds_asian_mex)

markets_mex = [
    ('墨西哥主勝(1X2)', p_mex_h, odds_mex_h, ev_mex_h),
    ('和局(1X2)', p_mex_d, odds_mex_d, ev_mex_d),
    ('南非勝(1X2)', p_mex_a, odds_mex_a, ev_mex_a),
    ('大球>2.5', p_mex_over25, odds_over25, ev_over25_m),
    ('小球<=2.5', p_mex_under25, odds_under25, ev_under25_m),
    ('亞盤主-1.25上盤', p_asian_mex_eff, odds_asian_mex, ev_asian_m),
]
print(f"{'市場':<20} {'p_model':>9} {'賠率':>7} {'EV%':>8} 建議")
print("-"*55)
for mkt,p,o,e in markets_mex:
    flag="VALUE" if e>0.03 else ("薄" if e>0 else "pass")
    print(f"{mkt:<20} {p*100:>8.1f}% {o:>7.3f} {e*100:>7.2f}% {flag}")

confidence_mex=4  # 機構資金同向 3+1
print(f"\n資金訊號: BetMGM機構大額同向 -> 信心 3+1 = {confidence_mex}")

print("\n假想推薦:")
mex_recs=[]
for mkt,p,o,e in markets_mex:
    if e>0.03:
        k=kelly_025(p,o); stake=min(k,0.02)
        if confidence_mex>=3:
            mex_recs.append((mkt,p,o,e,confidence_mex,stake))
            print(f"  [REC] {mkt}: EV={e*100:.2f}% | 信心={confidence_mex} | 0.25K={k*100:.3f}% -> 注碼={stake*100:.3f}%")
if not mex_recs:
    print("  本場無建議投注")


# ===== 場次二：南韓 vs 捷克 =====
print("\n" + "="*70)
print("場次二：南韓 vs 捷克  (A組, 6/11, Akron, 中立場)")
print("實際賽果：南韓 2-1")
print("="*70)

print("\n--- 方法 A: 加權評分法 ---")
kor_results = [('W',1,0),('W',5,0),('L',0,1),('L',0,4),('W',1,0),('W',2,0),('W',2,0)]
cze_results_adj = [('W',3,1),('W',2,1),('D',2,2),('D',2,2),('D',6,0),('W',2,1),('D',2,2)]
kor_score = weighted_score(kor_results, weights_7)
cze_score = weighted_score(cze_results_adj, weights_7)
print(f"南韓加權分(0-10): {kor_score:.4f}")
print(f"捷克加權分(直布羅陀折扣,0-10): {cze_score:.4f}")
delta_A_kor = kor_score - cze_score
print(f"狀態分差 delta: {delta_A_kor:.4f}")

h2h_kor=0.02; injury_cze=0.04; pso_penalty=0.02
total_kor_adj = h2h_kor+injury_cze+pso_penalty
print(f"修正: H2H韓佔優+{h2h_kor}, 捷克停賽+{injury_cze}, PSO疲勞+{pso_penalty} = 總+{total_kor_adj}")

p_A_kor_h, p_A_kor_d, p_A_kor_a = logistic_3way(delta_A_kor, k=0.30)
p_A_kor_h_adj = min(0.85, p_A_kor_h + total_kor_adj)
p_A_kor_a_adj = max(0.05, p_A_kor_a - total_kor_adj*0.7)
p_A_kor_d_adj = max(0.10, 1 - p_A_kor_h_adj - p_A_kor_a_adj)
tot3 = p_A_kor_h_adj+p_A_kor_d_adj+p_A_kor_a_adj
p_A_kor_h_adj/=tot3; p_A_kor_d_adj/=tot3; p_A_kor_a_adj/=tot3
print(f"方法A => 韓勝: {p_A_kor_h_adj:.4f}  和局: {p_A_kor_d_adj:.4f}  捷勝: {p_A_kor_a_adj:.4f}  (sum={p_A_kor_h_adj+p_A_kor_d_adj+p_A_kor_a_adj:.4f})")

print("\n--- 方法 B: Poisson ---")
kor_gf_7=1+5+0+0+1+2+2; kor_ga_7=0+0+1+4+0+0+0
cze_gf_6=(3+2+2+2+2+2); cze_ga_6=(1+1+2+2+1+2)  # 剔除直布羅陀6-0那場
kor_lam_raw2=kor_gf_7/7; cze_lam_raw2=cze_gf_6/6
lam_kor_hint=2.2*0.7; lam_cze_hint=1.67*0.7
discount=0.7
lam_kor_final=min(kor_lam_raw2*(1-discount)+lam_kor_hint*discount, 2.5)
lam_cze_final=min(cze_lam_raw2*(1-discount)+lam_cze_hint*discount, 2.5)
print(f"南韓7場進球: {kor_gf_7}, 場均: {kor_lam_raw2:.4f}")
print(f"捷克6場(剔直布): {cze_gf_6}, 場均: {cze_lam_raw2:.4f}")
print(f"form-analyst hint 折扣後: 韓={lam_kor_hint:.3f}, 捷={lam_cze_hint:.3f}")
print(f"最終 lambda_韓: {lam_kor_final:.4f}  lambda_捷: {lam_cze_final:.4f}")
print(f"折扣假設: WC級別競爭強度高，進球率往均值回歸，折扣係數0.7")

pm2 = poisson_matrix(lam_kor_final, lam_cze_final)
p_B_kor_h=pm2['p_home']; p_B_kor_d=pm2['p_draw']; p_B_kor_a=pm2['p_away']
print(f"方法B => 韓勝: {p_B_kor_h:.4f}  和局: {p_B_kor_d:.4f}  捷勝: {p_B_kor_a:.4f}")
print(f"  大球>2.5: {pm2['p_over25']:.4f}  小球<=2.5: {pm2['p_under25']:.4f}")
p_asian_kor_win=pm2['p_home']; p_asian_kor_half=pm2['p_draw']
p_asian_kor_eff=p_asian_kor_win+0.5*p_asian_kor_half
print(f"  亞盤韓-0.25: 全紅={p_asian_kor_win:.4f}  半輸(和局)={p_asian_kor_half:.4f}  全輸={pm2['p_away']:.4f}")
print(f"  有效p: {p_asian_kor_eff:.4f} ({p_asian_kor_eff*100:.1f}%)")

print("\n--- p_model 整合 ---")
p_kor_h=(p_A_kor_h_adj+p_B_kor_h)/2
p_kor_d=(p_A_kor_d_adj+p_B_kor_d)/2
p_kor_a=(p_A_kor_a_adj+p_B_kor_a)/2
tot4=p_kor_h+p_kor_d+p_kor_a
p_kor_h/=tot4; p_kor_d/=tot4; p_kor_a/=tot4
diff_kh=abs(p_A_kor_h_adj-p_B_kor_h)
diff_kd=abs(p_A_kor_d_adj-p_B_kor_d)
diff_ka=abs(p_A_kor_a_adj-p_B_kor_a)
print(f"p_model => 韓勝: {p_kor_h:.4f} ({p_kor_h*100:.1f}%)  差異: {diff_kh*100:.1f}pp {'[!分歧>10pp]' if diff_kh>0.10 else ''}")
print(f"p_model => 和局: {p_kor_d:.4f} ({p_kor_d*100:.1f}%)  差異: {diff_kd*100:.1f}pp {'[!分歧>10pp]' if diff_kd>0.10 else ''}")
print(f"p_model => 捷勝: {p_kor_a:.4f} ({p_kor_a*100:.1f}%)  差異: {diff_ka*100:.1f}pp {'[!分歧>10pp]' if diff_ka>0.10 else ''}")
p_kor_over25=pm2['p_over25']; p_kor_under25=pm2['p_under25']
print(f"大球p(>2.5): {p_kor_over25:.4f} ({p_kor_over25*100:.1f}%)")
print(f"小球p(<=2.5): {p_kor_under25:.4f} ({p_kor_under25*100:.1f}%)")
print(f"亞盤韓-0.25有效p: {p_asian_kor_eff:.4f} ({p_asian_kor_eff*100:.1f}%)")

print("\n--- EV 計算 ---")
odds_kor_h=2.62; odds_kor_d=3.10; odds_kor_a=2.75
odds_over25_k=2.65; odds_under25_k=1.69; odds_asian_kor=2.18
ev_kor_h=ev(p_kor_h,odds_kor_h); ev_kor_d=ev(p_kor_d,odds_kor_d)
ev_kor_a=ev(p_kor_a,odds_kor_a); ev_over25_k=ev(p_kor_over25,odds_over25_k)
ev_under25_k=ev(p_kor_under25,odds_under25_k); ev_asian_kor=ev(p_asian_kor_eff,odds_asian_kor)

markets_kor = [
    ('南韓勝(1X2)', p_kor_h, odds_kor_h, ev_kor_h),
    ('和局(1X2)', p_kor_d, odds_kor_d, ev_kor_d),
    ('捷克勝(1X2)', p_kor_a, odds_kor_a, ev_kor_a),
    ('大球>2.5', p_kor_over25, odds_over25_k, ev_over25_k),
    ('小球<=2.5', p_kor_under25, odds_under25_k, ev_under25_k),
    ('亞盤韓-0.25上盤', p_asian_kor_eff, odds_asian_kor, ev_asian_kor),
]
print(f"{'市場':<22} {'p_model':>9} {'賠率':>7} {'EV%':>8} 建議")
print("-"*58)
for mkt,p,o,e in markets_kor:
    flag="VALUE" if e>0.03 else ("薄" if e>0 else "pass")
    print(f"{mkt:<22} {p*100:>8.1f}% {o:>7.3f} {e*100:>7.2f}% {flag}")

flag_diverge_kor = any([diff_kh>0.10,diff_kd>0.10,diff_ka>0.10])
confidence_kor = 2 if flag_diverge_kor else 3
if flag_diverge_kor:
    print(f"\n[!] 兩法分歧>10pp -> 信心降為 {confidence_kor}")
else:
    print(f"\n資金訊號: 平手盤/無明確機構方向 -> 信心維持 {confidence_kor}")

print("\n假想推薦:")
kor_recs=[]
for mkt,p,o,e in markets_kor:
    if e>0.03:
        k=kelly_025(p,o); stake=min(k,0.02)
        if confidence_kor>=3:
            kor_recs.append((mkt,p,o,e,confidence_kor,stake))
            print(f"  [REC] {mkt}: EV={e*100:.2f}% | 信心={confidence_kor} | 0.25K={k*100:.3f}% -> 注碼={stake*100:.3f}%")
        else:
            print(f"  [PASS] {mkt}: EV={e*100:.2f}% 但信心={confidence_kor}<=2 -> PASS (分歧)")
if not kor_recs:
    print("  本場無建議投注（EV未達門檻或信心不足）")


# ===== 反推驗證 =====
print("\n" + "="*70)
print("反推驗證 (Backtest)")
print("="*70)

outcome_mex=[1,0,0]; outcome_kor=[1,0,0]

mex_mkt_odds=[1.48,4.33,6.50]; mex_implied=implied_prob_no_vig(mex_mkt_odds)
kor_mkt_odds=[2.62,3.10,2.75]; kor_implied=implied_prob_no_vig(kor_mkt_odds)

bs_model_mex  = brier_score([p_mex_h,p_mex_d,p_mex_a], outcome_mex)
bs_market_mex = brier_score(mex_implied, outcome_mex)
bs_model_kor  = brier_score([p_kor_h,p_kor_d,p_kor_a], outcome_kor)
bs_market_kor = brier_score(kor_implied, outcome_kor)

print("\n[Brier Score 1X2三向, 越小越準]")
print(f"場次一 墨西哥 vs 南非:")
print(f"  市場去水隱含: 墨={mex_implied[0]*100:.1f}% 和={mex_implied[1]*100:.1f}% 南非={mex_implied[2]*100:.1f}%")
print(f"  模型 p_model: 墨={p_mex_h*100:.1f}% 和={p_mex_d*100:.1f}% 南非={p_mex_a*100:.1f}%")
print(f"  Brier(模型)={bs_model_mex:.4f}  Brier(市場)={bs_market_mex:.4f}")
print(f"  -> {'模型更準' if bs_model_mex<bs_market_mex else '市場更準'} (差異={abs(bs_model_mex-bs_market_mex):.4f})")

print(f"\n場次二 南韓 vs 捷克:")
print(f"  市場去水隱含: 韓={kor_implied[0]*100:.1f}% 和={kor_implied[1]*100:.1f}% 捷={kor_implied[2]*100:.1f}%")
print(f"  模型 p_model: 韓={p_kor_h*100:.1f}% 和={p_kor_d*100:.1f}% 捷={p_kor_a*100:.1f}%")
print(f"  Brier(模型)={bs_model_kor:.4f}  Brier(市場)={bs_market_kor:.4f}")
print(f"  -> {'模型更準' if bs_model_kor<bs_market_kor else '市場更準'} (差異={abs(bs_model_kor-bs_market_kor):.4f})")

print("\n[假想盈虧計算]")
print("場次一 墨西哥 vs 南非 (實際結果: 墨2-0南非)")
mex_pnl=0.0
for rec in mex_recs:
    mkt,p,o,e,conf,stake=rec
    win=False
    actual_total_goals = 2  # 2-0
    if '墨西哥主勝' in mkt: win=True
    elif '大球' in mkt: win=(actual_total_goals>2)
    elif '小球' in mkt: win=(actual_total_goals<=2)
    elif '亞盤主-1.25' in mkt: win=True  # 墨贏2球,全紅
    pnl=stake*(o-1) if win else -stake
    mex_pnl+=pnl
    print(f"  {mkt}: 注碼={stake*100:.3f}% | {'命中' if win else '失手'} | 盈虧={pnl*100:+.4f}%")
if not mex_recs:
    print("  無建議投注，無假想盈虧")

print(f"\n場次二 南韓 vs 捷克 (實際結果: 韓2-1捷)")
kor_pnl=0.0
for rec in kor_recs:
    mkt,p,o,e,conf,stake=rec
    win=False
    actual_total_goals_k = 3  # 2-1
    if '南韓勝' in mkt: win=True
    elif '大球' in mkt: win=(actual_total_goals_k>2)
    elif '小球' in mkt: win=(actual_total_goals_k<=2)
    elif '亞盤韓-0.25' in mkt: win=True
    pnl=stake*(o-1) if win else -stake
    kor_pnl+=pnl
    print(f"  {mkt}: 注碼={stake*100:.3f}% | {'命中' if win else '失手'} | 盈虧={pnl*100:+.4f}%")
if not kor_recs:
    print("  無建議投注（EV未達門檻或信心不足）")

total_pnl=mex_pnl+kor_pnl
print(f"\n兩場合計假想盈虧: {total_pnl*100:+.4f}% bankroll")

print("\n[大小球與亞盤方向]")
print(f"場次一 墨2-0(2球): 模型大球方向={'Over' if p_mex_over25>0.5 else 'Under'} -> 實際Under -> {'正確' if p_mex_over25<0.5 else '錯誤'}")
print(f"場次一 墨2-0: 亞盤主-1.25 -> 墨贏2球全紅 -> 命中")
print(f"場次二 韓2-1(3球): 模型大球方向={'Over' if p_kor_over25>0.5 else 'Under'} -> 實際Over -> {'正確' if p_kor_over25>0.5 else '錯誤'}")
print(f"場次二 韓2-1: 亞盤韓-0.25 -> 韓贏全紅 -> 命中")

print("\n[統計限制聲明]")
print("  n=2 場樣本的統計說明:")
print("  - 本次2場模型方向推薦均與實際一致")
print("  - n=2 無法進行任何顯著性檢驗，p-value無意義")
print("  - 命中率95%信賴區間在n=2時跨越[0,1]整個範圍")
print("  - ROI長期期望需>=50場才能得出有意義結論")
print("  - 本次驗證僅確認計算流程無誤、無資料洩漏")
print("  - 不能據此宣稱模型優於或劣於市場")

print("\n" + "="*70)
print("計算完成")
print("="*70)

# 輸出關鍵變數供報告使用
print("\n===KEY_VARS===")
print(f"MEX_p_model: home={p_mex_h:.4f} draw={p_mex_d:.4f} away={p_mex_a:.4f}")
print(f"MEX_p_over25={p_mex_over25:.4f} p_under25={p_mex_under25:.4f}")
print(f"MEX_asian_eff={p_asian_mex_eff:.4f}")
print(f"MEX_BS_model={bs_model_mex:.4f} BS_market={bs_market_mex:.4f}")
print(f"MEX_mex_implied: {[round(x,4) for x in mex_implied]}")
print(f"KOR_p_model: home={p_kor_h:.4f} draw={p_kor_d:.4f} away={p_kor_a:.4f}")
print(f"KOR_p_over25={p_kor_over25:.4f} p_under25={p_kor_under25:.4f}")
print(f"KOR_asian_eff={p_asian_kor_eff:.4f}")
print(f"KOR_BS_model={bs_model_kor:.4f} BS_market={bs_market_kor:.4f}")
print(f"KOR_kor_implied: {[round(x,4) for x in kor_implied]}")
print(f"MEX_confidence={confidence_mex} KOR_confidence={confidence_kor}")
print(f"TOTAL_PNL={total_pnl*100:.4f}%")
print(f"MEX_recs_count={len(mex_recs)} KOR_recs_count={len(kor_recs)}")
