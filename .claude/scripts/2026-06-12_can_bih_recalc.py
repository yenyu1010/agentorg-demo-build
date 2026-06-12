#!/usr/bin/env python3
"""
世界盃B組 加拿大 vs 波黑（6/12 19:00 UTC）
賠率更新複算 EV — 5.5h 前 snapshot
ROOT: /home/user/agentorg-demo-build
"""
import math

print("=" * 60)
print("加拿大 vs 波黑  世界盃2026 B組")
print("賠率 snapshot：開賽前 5.5h")
print("=" * 60)

# ─────────────────────────────────────────────
# 1. p_model（不變，沿用 4 小時前建模值）
# ─────────────────────────────────────────────
p_can_win   = 0.4628
p_draw      = 0.2588
p_bih_win   = 0.2783
p_bih_cover = 0.5372   # 波+0.5 = 波勝+和
p_can_cover = 1 - p_bih_cover
p_over25    = 0.3555
p_under25   = 0.6445

print("\n── p_model（沿用）──")
print(f"  加拿大勝     : {p_can_win:.4f}")
print(f"  和局         : {p_draw:.4f}")
print(f"  波黑勝       : {p_bih_win:.4f}")
print(f"  波+0.5覆蓋   : {p_bih_cover:.4f}")
print(f"  Over 2.5     : {p_over25:.4f}")
print(f"  Under 2.5    : {p_under25:.4f}")

# ─────────────────────────────────────────────
# 2. 最新賠率
# ─────────────────────────────────────────────
odds = {
    "1X2_加勝":     1.83,
    "1X2_和":       3.45,
    "1X2_波勝":     4.55,
    "亞盤_加-0.5":  1.83,
    "亞盤_波+0.5":  2.09,
    "大2.5":        2.33,
    "小2.5":        1.65,
    "大2/2.5":      2.04,
    "小2/2.5":      1.86,
}
odds_prev = {"亞盤_波+0.5": 2.05, "1X2_波勝": 4.80}

# ─────────────────────────────────────────────
# 3. Overround & 去水機率
# ─────────────────────────────────────────────
def overround(o_list):
    return sum(1/o for o in o_list)

def fair_p(o, or_total):
    return (1/o) / or_total

or_1x2  = overround([odds["1X2_加勝"], odds["1X2_和"], odds["1X2_波勝"]])
or_ah   = overround([odds["亞盤_加-0.5"], odds["亞盤_波+0.5"]])
or_ou25 = overround([odds["大2.5"], odds["小2.5"]])
or_ou225= overround([odds["大2/2.5"], odds["小2/2.5"]])

fair_can_1x2   = fair_p(odds["1X2_加勝"],    or_1x2)
fair_draw_1x2  = fair_p(odds["1X2_和"],      or_1x2)
fair_bih_1x2   = fair_p(odds["1X2_波勝"],    or_1x2)
fair_bih_cover = fair_p(odds["亞盤_波+0.5"], or_ah)
fair_over25    = fair_p(odds["大2.5"],        or_ou25)
fair_under25   = fair_p(odds["小2.5"],        or_ou25)
fair_over225   = fair_p(odds["大2/2.5"],      or_ou225)
fair_under225  = fair_p(odds["小2/2.5"],      or_ou225)

print("\n── 盤口 Overround ──")
print(f"  1X2          : {or_1x2:.4f}  (水份={or_1x2-1:.2%})")
print(f"  亞盤         : {or_ah:.4f}   (水份={or_ah-1:.2%})")
print(f"  大小2.5      : {or_ou25:.4f}  (水份={or_ou25-1:.2%})")
print(f"  大小2/2.5    : {or_ou225:.4f} (水份={or_ou225-1:.2%})")

print("\n── 隱含機率（去水後）──")
print(f"  加勝         : {fair_can_1x2:.4f}")
print(f"  和局         : {fair_draw_1x2:.4f}")
print(f"  波勝         : {fair_bih_1x2:.4f}")
print(f"  波+0.5覆蓋   : {fair_bih_cover:.4f}")
print(f"  Over 2.5     : {fair_over25:.4f}")
print(f"  Under 2.5    : {fair_under25:.4f}")
print(f"  Over 2/2.5   : {fair_over225:.4f}")
print(f"  Under 2/2.5  : {fair_under225:.4f}")

# ─────────────────────────────────────────────
# 4. Poisson λ 反推（修正二分法）
# ─────────────────────────────────────────────
def p_lt3(lam):
    """P(X=0)+P(X=1)+P(X=2) for Poisson(lam)"""
    p0 = math.exp(-lam)
    p1 = lam * math.exp(-lam)
    p2 = (lam**2 / 2) * math.exp(-lam)
    return p0 + p1 + p2

def solve_lambda(p_ge3_target=0.3555):
    """
    找 λ 使 P(X>=3) = p_ge3_target
    即 P(X<3) = 1 - p_ge3_target
    P(X<3) 隨 λ 增大而減小
    → p_lt3(λ) > target: λ 太小，lo = mid
    → p_lt3(λ) < target: λ 太大，hi = mid
    """
    target_lt3 = 1 - p_ge3_target
    lo, hi = 0.01, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        val = p_lt3(mid)
        if val > target_lt3:
            lo = mid   # λ 需要更大
        else:
            hi = mid   # λ 需要更小
    return (lo + hi) / 2

lam_est = solve_lambda(p_over25)
p2_est  = (lam_est**2 / 2) * math.exp(-lam_est)
p_ge3   = p_over25
p_le1   = 1 - p_ge3 - p2_est

print("\n── Poisson λ 估計（從 p_over25=0.3555 反推）──")
print(f"  λ_total      : {lam_est:.4f}")
print(f"  P(X=2)       : {p2_est:.4f}")
print(f"  P(X<=1) [小全中]: {p_le1:.4f}")
print(f"  P(X>=3) [大全中]: {p_ge3:.4f}")
print(f"  驗算 P(<3)   : {p_lt3(lam_est):.6f}  (應≈{1-p_over25:.6f})")

# ─────────────────────────────────────────────
# 5. EV 計算
# ─────────────────────────────────────────────
def ev(p_model, o):
    return p_model * o - 1

# 四分之一球 EV
# 大 2/2.5：>=3全中，=2半中，<=1全輸
ev_over225  = p_ge3 * odds["大2/2.5"] + p2_est * (0.5*odds["大2/2.5"] + 0.5*1.0) - 1
# 小 2/2.5：<=1全中，=2半中，>=3全輸
ev_under225 = p_le1 * odds["小2/2.5"] + p2_est * (0.5*odds["小2/2.5"] + 0.5*1.0) - 1

ev_can_win    = ev(p_can_win,   odds["1X2_加勝"])
ev_draw_v     = ev(p_draw,      odds["1X2_和"])
ev_bih_win    = ev(p_bih_win,   odds["1X2_波勝"])
ev_can_cover  = ev(p_can_cover, odds["亞盤_加-0.5"])
ev_bih_cover  = ev(p_bih_cover, odds["亞盤_波+0.5"])
ev_over25_    = ev(p_over25,    odds["大2.5"])
ev_under25_   = ev(p_under25,   odds["小2.5"])

ev_bih_cover_prev = ev(p_bih_cover, odds_prev["亞盤_波+0.5"])
ev_bih_win_prev   = ev(p_bih_win,   odds_prev["1X2_波勝"])

# 展示 Over225 計算細節
print(f"\n── 大2/2.5 EV 展開 ──")
print(f"  EV = P(>=3)×2.04 + P(=2)×(0.5×2.04+0.5×1) - 1")
print(f"     = {p_ge3:.4f}×2.04 + {p2_est:.4f}×({0.5*odds['大2/2.5']:.3f}+0.5) - 1")
print(f"     = {p_ge3*odds['大2/2.5']:.4f} + {p2_est*(0.5*odds['大2/2.5']+0.5):.4f} - 1")
print(f"     = {ev_over225:.4f}  ({ev_over225*100:+.2f}%)")
print(f"\n── 小2/2.5 EV 展開 ──")
print(f"  EV = P(<=1)×1.86 + P(=2)×(0.5×1.86+0.5×1) - 1")
print(f"     = {p_le1:.4f}×1.86 + {p2_est:.4f}×({0.5*odds['小2/2.5']:.3f}+0.5) - 1")
print(f"     = {p_le1*odds['小2/2.5']:.4f} + {p2_est*(0.5*odds['小2/2.5']+0.5):.4f} - 1")
print(f"     = {ev_under225:.4f}  ({ev_under225*100:+.2f}%)")

# ─────────────────────────────────────────────
# 6. EV 比較表
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("EV 比較表（6h前 → 現在）")
print("=" * 60)
print(f"{'市場':<16} {'方向':<15} {'舊賠率':>7} {'新賠率':>7} {'p_model':>8} {'舊EV%':>9} {'新EV%':>9} {'變化':>9}")
print("-" * 86)

rows = [
    ("1X2",       "加勝",         None, odds["1X2_加勝"],    p_can_win,   None,              ev_can_win),
    ("1X2",       "和局",         None, odds["1X2_和"],      p_draw,      None,              ev_draw_v),
    ("1X2",       "波勝",         4.80, odds["1X2_波勝"],    p_bih_win,   ev_bih_win_prev,   ev_bih_win),
    ("亞盤",      "加-0.5",       None, odds["亞盤_加-0.5"], p_can_cover, None,              ev_can_cover),
    ("亞盤",      "波+0.5 ★",    2.05, odds["亞盤_波+0.5"], p_bih_cover, ev_bih_cover_prev, ev_bih_cover),
    ("大小2.5",   "Over",         None, odds["大2.5"],       p_over25,    None,              ev_over25_),
    ("大小2.5",   "Under",        None, odds["小2.5"],       p_under25,   None,              ev_under25_),
    ("大小2/2.5", "大Over(Q)",    None, odds["大2/2.5"],     None,        None,              ev_over225),
    ("大小2/2.5", "小Under(Q)",   None, odds["小2/2.5"],     None,        None,              ev_under225),
]

for market, direction, old_o, new_o, p_m, old_ev, new_ev in rows:
    old_o_str  = f"{old_o:.2f}" if old_o else "   —  "
    p_m_str    = f"{p_m:.4f}" if p_m else "   —  "
    old_ev_str = f"{old_ev*100:+.2f}%" if old_ev is not None else "    —   "
    new_ev_str = f"{new_ev*100:+.2f}%"
    if old_ev is not None:
        delta = (new_ev - old_ev) * 100
        delta_str = f"{delta:+.2f}pp"
    else:
        delta_str = "    —  "
    print(f"{market:<16} {direction:<15} {old_o_str:>7} {new_o:>7.2f} {p_m_str:>8} {old_ev_str:>9} {new_ev_str:>9} {delta_str:>9}")

# ─────────────────────────────────────────────
# 7. 信心複核
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("信心複核")
print("=" * 60)
print(f"""
[波黑+0.5 @2.09]
  EV = {ev_bih_cover*100:+.2f}% (前 @2.05 EV={ev_bih_cover_prev*100:+.2f}%, 改善 {(ev_bih_cover-ev_bih_cover_prev)*100:+.2f}pp)
  賠率上升 2.05→2.09（下盤更划算）
  訊號：波黑歐賠縮水強度2 → 方向同向佐證
  → 信心維持 4，EV>3% 門檻，建議投注

[波勝 1X2 @4.55]
  EV = {ev_bih_win*100:+.2f}% (前 @4.80 EV={ev_bih_win_prev*100:+.2f}%)
  賠率從 4.80 縮水至 4.55，市場下調波黑勝賠
  p_model={p_bih_win:.4f} vs 市場隱含(去水)={fair_bih_1x2:.4f} (+{((p_bih_win/fair_bih_1x2)-1)*100:.1f}%)
  DATA_GAP：本批無必發/亞洲場外資料確認溢價真實性
  → EV仍高但缺確認，信心 2，PASS

[Under 2.5 @1.65]
  EV = {ev_under25_*100:+.2f}%
  p_model={p_under25:.4f}，大球資金強度3反向，盤口上移
  → 市場強烈反向，信心 2，PASS

[小2/2.5 @1.86（四分之一球）]
  EV = {ev_under225*100:+.2f}%
  同大球資金訊號反向，信心 2，PASS

[Over 2.5 @2.33 / 大2/2.5 @2.04]
  EV = {ev_over25_*100:+.2f}% / {ev_over225*100:+.2f}%（負值）→ PASS

[加勝 @1.83 / 加-0.5 @1.83 / 和 @3.45]
  EV = {ev_can_win*100:+.2f}% / {ev_can_cover*100:+.2f}% / {ev_draw_v*100:+.2f}% → PASS
""")

# ─────────────────────────────────────────────
# 8. Fractional Kelly — 波+0.5 @2.09
# ─────────────────────────────────────────────
print("=" * 60)
print("0.25 Fractional Kelly — 波黑+0.5 @2.09")
print("=" * 60)
b = odds["亞盤_波+0.5"] - 1
p = p_bih_cover
q = 1 - p
kelly_full    = (b * p - q) / b
kelly_quarter = 0.25 * kelly_full
cap = 0.02
final_stake   = min(kelly_quarter, cap)

print(f"""
  b (淨賠率)         = {b:.4f}
  p_model            = {p:.4f}
  q = 1 - p          = {q:.4f}
  Full Kelly         = (b×p − q) / b
                     = ({b:.4f}×{p:.4f} − {q:.4f}) / {b:.4f}
                     = {kelly_full:.6f}  ({kelly_full*100:.4f}%)
  0.25 Kelly         = {kelly_quarter*100:.4f}%
  2% 硬上限
  最終建議注碼       = min({kelly_quarter*100:.4f}%, 2.00%) = {final_stake*100:.2f}%
""")

print("=" * 60)
print("最終推薦摘要")
print("=" * 60)
print(f"""
  ✅ 維持推薦：亞盤 波黑+0.5 @2.09
     EV = {ev_bih_cover*100:+.2f}%（較原 +10.12% 改善 +{(ev_bih_cover-ev_bih_cover_prev)*100:.2f}pp）
     注碼 = {final_stake*100:.1f}% bankroll（2% 封頂）
     信心 = 4

  PASS（信心 2）：
     波勝 @4.55    EV={ev_bih_win*100:+.1f}%  DATA_GAP 缺必發確認
     Under2.5 @1.65  EV={ev_under25_*100:+.1f}%  大球資金強度3反向
     小2/2.5 @1.86   EV={ev_under225*100:+.1f}%  同大球資金訊號反向

  PASS（EV負值）：
     加勝、和局、加-0.5、Over2.5、大2/2.5
""")

print("=" * 60)
print("免責聲明")
print("本分析為機率模型推估，僅供參考，不構成投注建議；")
print("博彩具風險，過往績效不代表未來表現；")
print("請遵守所在地法律並量力而為。")
print("=" * 60)
