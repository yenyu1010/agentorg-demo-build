#!/usr/bin/env python3
"""
大小球2.75 EV 深度驗算
問題：λ_h=2.1, λ_a=0.9 → E[total]=3.0，但市場線開在2.75，水0.84/1.04
這本身代表市場認為期望進球低於3.0，我們需要理解這個分歧。
"""
import math

def pmf(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

# 方案A：Poisson λ_h=2.1, λ_a=0.9（form_analysis 提供）
lam_h_a, lam_a_a = 2.1, 0.9
# 方案B：市場隱含λ（反推）
# 小球水0.84 → 市場對 Under 隱含機率 = 1/1.84 = 0.5435
# 若用對稱獨立Poisson估算，需要 P(total<=2) ≈ 0.5435
# 從水反推市場p_under：去水前小球水 0.84 → return 1.84 → p_implied = 1/1.84 = 0.5435
# 去水：over raw = 1/2.04 = 0.4902，under raw = 1/1.84 = 0.5435
# overround_ou = 0.4902 + 0.5435 = 1.0337
# p_under_mkt = 0.5435 / 1.0337 = 0.5257
# p_over_mkt  = 0.4902 / 1.0337 = 0.4743

p_over_raw  = 1 / (1 + 1.04)   # water 1.04 → decimal odds = 2.04
p_under_raw = 1 / (1 + 0.84)   # water 0.84 → decimal odds = 1.84
ou_OR = p_over_raw + p_under_raw
p_over_mkt  = p_over_raw / ou_OR
p_under_mkt = p_under_raw / ou_OR
print(f"大小球市場隱含（去水）：大球={p_over_mkt:.4f}  小球={p_under_mkt:.4f}")
print(f"暗示市場認為大球機率僅 {p_over_mkt*100:.1f}%")

# Poisson A
MAX = 10
scores_a = {}
for i in range(MAX):
    for j in range(MAX):
        scores_a[(i,j)] = pmf(lam_h_a, i) * pmf(lam_a_a, j)
Sa = sum(scores_a.values())
scores_a = {k: v/Sa for k, v in scores_a.items()}

p_tot_ge3_a = sum(v for (i,j),v in scores_a.items() if i+j >= 3)
p_tot_eq2_a = sum(v for (i,j),v in scores_a.items() if i+j == 2)
p_tot_le1_a = sum(v for (i,j),v in scores_a.items() if i+j <= 1)
p_tot_le2_a = sum(v for (i,j),v in scores_a.items() if i+j <= 2)
p_tot_eq3_a = sum(v for (i,j),v in scores_a.items() if i+j == 3)
p_tot_ge4_a = sum(v for (i,j),v in scores_a.items() if i+j >= 4)

print(f"\n[方案A λh=2.1/λa=0.9  E[total]={lam_h_a+lam_a_a}]")
print(f"  P(total<=2)={p_tot_le2_a:.4f}  P(total>=3)={p_tot_ge3_a:.4f}")
print(f"  P(total==2)={p_tot_eq2_a:.4f}")

# 大球2.75 EV (方案A)
ev_over_a  = p_tot_ge3_a*1.04 + p_tot_eq2_a*(0.5*1.04) + p_tot_le1_a*(-1.0)
ev_under_a = p_tot_le2_a*0.84 + p_tot_eq3_a*(-0.5) + p_tot_ge4_a*(-1.0)
print(f"  大球EV={ev_over_a:+.4f}  小球EV={ev_under_a:+.4f}")

# 關鍵問題：λ是否需要調整？
# 世界盃小組賽第1場，球隊偏謹慎，歷史均進球偏低
# 2022年世界盃小組賽平均進球：約2.44/場
# 2018年世界盃小組賽平均進球：約2.64/場
# 法塞H2H唯一正式記錄：0-1（低比分）
# form_analysis λ 來自近況×主場（WC中立場需折扣）

# 中立場折扣：法國 λh 原始 2.1 假設含主場優勢
# WC中立場：法國降至約 1.8-1.9
lam_h_b, lam_a_b = 1.85, 0.85   # 中立場調整

scores_b = {}
for i in range(MAX):
    for j in range(MAX):
        scores_b[(i,j)] = pmf(lam_h_b, i) * pmf(lam_a_b, j)
Sb = sum(scores_b.values())
scores_b = {k: v/Sb for k, v in scores_b.items()}

p_tot_ge3_b = sum(v for (i,j),v in scores_b.items() if i+j >= 3)
p_tot_eq2_b = sum(v for (i,j),v in scores_b.items() if i+j == 2)
p_tot_le1_b = sum(v for (i,j),v in scores_b.items() if i+j <= 1)
p_tot_le2_b = sum(v for (i,j),v in scores_b.items() if i+j <= 2)
p_tot_eq3_b = sum(v for (i,j),v in scores_b.items() if i+j == 3)
p_tot_ge4_b = sum(v for (i,j),v in scores_b.items() if i+j >= 4)

print(f"\n[方案B λh=1.85/λa=0.85  E[total]={lam_h_b+lam_a_b} 中立場調整]")
print(f"  P(total<=2)={p_tot_le2_b:.4f}  P(total>=3)={p_tot_ge3_b:.4f}")
ev_over_b  = p_tot_ge3_b*1.04 + p_tot_eq2_b*(0.5*1.04) + p_tot_le1_b*(-1.0)
ev_under_b = p_tot_le2_b*0.84 + p_tot_eq3_b*(-0.5) + p_tot_ge4_b*(-1.0)
print(f"  大球EV={ev_over_b:+.4f}  小球EV={ev_under_b:+.4f}")

# 方案C：市場反推 λ
# P(total<=2) ≈ 0.5257，找出對應的獨立Poisson λ_total
# 若 λ_h:λ_a ≈ 2.1:0.9 = 7:3 比例維持
# 嘗試不同 λ_total
print(f"\n[反推市場隱含 λ]")
print(f"市場 P(total<=2)={p_under_mkt:.4f}")
for lt in [x*0.1 for x in range(20, 35)]:
    lh = lt * 2.1 / 3.0
    la = lt * 0.9 / 3.0
    sc = {(i,j): pmf(lh,i)*pmf(la,j) for i in range(10) for j in range(10)}
    st = sum(sc.values())
    p_le2 = sum(v/st for (i,j),v in sc.items() if i+j <= 2)
    if abs(p_le2 - p_under_mkt) < 0.02:
        print(f"  λ_total={lt:.1f} (λh={lh:.2f}/λa={la:.2f}) → P(<=2)={p_le2:.4f}  差={p_le2-p_under_mkt:+.4f}")

# ─────────────────────────────────────────────────────────────
# 最終決定：使用保守估計 (方案B) 用於 OU，形成加權
# 原始Poisson (方案A, 50%) + 中立場折扣 (方案B, 50%)
# ─────────────────────────────────────────────────────────────
p_ge3_final = 0.5 * p_tot_ge3_a + 0.5 * p_tot_ge3_b
p_le2_final = 0.5 * p_tot_le2_a + 0.5 * p_tot_le2_b
p_eq2_final = 0.5 * p_tot_eq2_a + 0.5 * p_tot_eq2_b
p_le1_final = 0.5 * p_tot_le1_a + 0.5 * p_tot_le1_b
p_eq3_final = 0.5 * p_tot_eq3_a + 0.5 * p_tot_eq3_b
p_ge4_final = 0.5 * p_tot_ge4_a + 0.5 * p_tot_ge4_b

ev_over_f  = p_ge3_final*1.04 + p_eq2_final*(0.5*1.04) + p_le1_final*(-1.0)
ev_under_f = p_le2_final*0.84 + p_eq3_final*(-0.5)    + p_ge4_final*(-1.0)

print(f"\n[最終大小球分析（A×50% + B×50%）]")
print(f"  P(total>=3) = {p_ge3_final:.4f}  P(total<=2) = {p_le2_final:.4f}")
print(f"  大球EV = {ev_over_f:+.4f} ({ev_over_f*100:+.2f}%)")
print(f"  小球EV = {ev_under_f:+.4f} ({ev_under_f*100:+.2f}%)")
print(f"  市場隱含大球 = {p_over_mkt:.4f}，模型估大球 = {p_ge3_final:.4f}")
print(f"  模型 vs 市場差距 = {(p_ge3_final - p_over_mkt)*100:+.2f}%")
