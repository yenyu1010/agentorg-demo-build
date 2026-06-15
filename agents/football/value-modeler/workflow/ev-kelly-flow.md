# Value Modeler — EV & Kelly Flow（期望值計算、注碼建議、排序輸出）

## 目的

對所有可投市場計算 EV，套用 Fractional Kelly 得出注碼，融合賠率訊號修正信心係數，排序輸出最終建議並附免責聲明。

## 步驟

### 1. 撰寫 EV + Kelly 腳本（追加至同一計算腳本）

```python
# ── EV & Kelly 計算（追加至 {match_id}_calc.py）────────────────

# 從 odds-analyst 報告填入實際賠率
markets = {
    "主勝":   {"p_model": p_home, "odds": {主勝賠率}},
    "和局":   {"p_model": p_draw, "odds": {和局賠率}},
    "客勝":   {"p_model": p_away, "odds": {客勝賠率}},
    "大球2.5":{"p_model": p_over25_B, "odds": {大球賠率}},
    # 亞盤：需依盤口調整 p_model（見下方說明）
}

# 亞盤覆蓋機率調整（以 -0.5 球亞盤為例）
# p_ah_home = sum 主勝機率；p_ah_away = sum 客勝機率 + 和局一半
# 依實際盤口從 Poisson 矩陣重新加總

results = []
for market_name, m in markets.items():
    p   = m["p_model"]
    o   = m["odds"]
    ev  = p * o - 1

    # Kelly
    b   = o - 1
    q   = 1 - p
    f_full  = (p * b - q) / b if b > 0 else -1
    f_kelly = max(0, 0.25 * f_full)
    f_capped = min(f_kelly, 0.02)   # 單場 2% 上限

    pass_reason = None
    if ev < 0.03:
        pass_reason = f"EV={ev:.1%} < 3% 門檻"
    if f_full <= 0:
        pass_reason = "Kelly f* ≤ 0，無正期望"

    results.append({
        "market":       market_name,
        "p_model":      round(p, 4),
        "implied_p":    round(1/o, 4),
        "odds":         o,
        "ev_pct":       round(ev * 100, 2),
        "kelly_pct":    round(f_capped * 100, 2),
        "pass_reason":  pass_reason,
    })

print("\n=== EV & Kelly 計算結果 ===")
for r in results:
    status = "PASS" if r["pass_reason"] else "VALUE"
    print(f"  [{status}] {r['market']}: p={r['p_model']} implied={r['implied_p']} "
          f"EV={r['ev_pct']}% Kelly={r['kelly_pct']}% "
          f"{'→ ' + r['pass_reason'] if r['pass_reason'] else ''}")
```

### 2. 賠率訊號融合（信心修正）

從 odds-analyst 報告讀取 `sharp_signal` 和 `water_level_change`，依下表調整每個推薦市場的信心係數：

| 條件 | 信心修正 | 附注 |
|------|---------|------|
| sharp_signal 與 p_model 同向 | +1 | — |
| sharp_signal 與 p_model 反向 | −1 | 附「市場可能知道你不知道的事」 |
| water_level_change > 15% | −1 | — |
| 模型分歧（estimate-flow 標注） | −1 | — |
| 無異常訊號 | 0 | — |

**信心係數上限/下限**：1–5（修正後若超出範圍，截斷至邊界值）

**強制 pass 條件**（信心修正後）：
- 信心 ≤ 2 → 強制 pass，附「訊號異常，降級棄投」

### 3. 最優投報率排序

1. 對所有非 pass 市場計算：`score = EV% × 信心係數`
2. 降序排列，取 Top 3（或全部通過門檻者）
3. 若**所有市場均 pass** → 輸出「本輪無建議投注」並說明主因

### 4. 輸出報告

```markdown
# 價值投注建模報告

## 場次：{match_id} — {主隊} vs {客隊}（{比賽日期}）

## 模型輸入摘要
- odds-analyst：{檔案路徑}
- form-analyst：{檔案路徑}

## 勝率估計

| 項目 | 方法 A（加權評分法） | 方法 B（簡化 Poisson） | p_model |
|------|-------------------|--------------------|---------|
| 主勝 | {p_home_A} | {p_home_B} | {p_home} |
| 和局 | {p_draw_A} | {p_draw_B} | {p_draw} |
| 客勝 | {p_away_A} | {p_away_B} | {p_away} |
| 大球 | — | {p_over25_B} | {p_over25_B} |

{若有分歧，插入：⚠️ 模型分歧（差異 > 10pp），信心係數已降級}

## 建議投注（Top Picks）

| 場次 | 市場 | 方向 | 賠率 | p_model | 隱含p | EV% | 0.25Kelly注碼% | 信心(1-5) |
|------|------|------|------|---------|-------|-----|---------------|-----------|
| {match} | {market} | {direction} | {odds} | {p} | {imp} | {ev} | {kelly} | {conf} |

{若全部 pass：本輪無建議投注。主因：{最主要的 pass 原因}}

## 計算明細

### Python 腳本輸出
\`\`\`
{完整的 stdout 輸出貼在此處}
\`\`\`

## 訊號修正說明
{逐條說明信心係數調整原因}

<!-- user-approved 2026-06-13 -->
## 高勝率參考榜（Win-Probability Tier）

> ⚠️ **勝率高≠會賺：EV 為負的高勝率單長期必虧（贏的次數多但單注賺得少、輸一次賠得多）。此榜供「低波動偏好」自行斟酌，模型的正式推薦仍以 EV 軸為準。**

篩選條件：p_model（含退款折算後的有效勝率）≥ 55%，涵蓋亞盤、大小球、獨贏，按勝率降序。

| 市場 | 方向 | 賠率 | 勝率% | 退款率% | EV% | 長期每注期望 | 分層 |
|------|------|------|-------|---------|-----|------------|------|
| {market} | {direction} | {odds} | {p_eff%} | {push%} | {ev%} | {ev_unit} | {★/◐/✗} |

**分層規則**：
- **★推薦**（EV ≥ +3%）：與 EV 主表一致，可按 Kelly 注碼投入
- **◐可考慮**（−3% < EV < +3%）：接近公平價，購買的是低波動而非正期望，注碼宜減半
- **✗不建議**（EV ≤ −3%）：長期必輸，勝率僅供背景參考，不建議以此為由投入

**退款處理規則**：整數盤 push 退款、四分之一盤半退需折算 p_eff 與退款率，所有計算以 Python 腳本完成並附於「Python 腳本輸出」欄。

若無市場達 55% 門檻 → 輸出「本輪無高勝率市場（所有市場 p_model < 55%）」。

---

> ⚠️ 本分析為機率模型推估，僅供參考，不構成投注建議；博彩具風險，過往績效不代表未來表現；請遵守所在地法律並量力而為。
```

### 5. 寫入輸出

```
Write: {output_path}/03_value_model_report.md
```

### 6. 更新追蹤記錄

將本次推薦（包含 pass 決定）追加至 `agents/football/value-modeler/memory/track-record.md`：

```markdown
| {日期} | {match_id} | {市場} | {方向} | {賠率} | {p_model} | {EV%} | {注碼%} | 待確認 |
```

pass 項目亦記錄（結果欄填「PASS」），用於長期校準。
