# Value Modeler — Estimate Flow（雙法勝率估計）

## 目的

以方法 A（加權評分法）與方法 B（簡化 Poisson）各自估計主勝 / 和 / 客勝機率，取平均得到 p_model，並偵測兩法分歧。

## 步驟

### 1. 撰寫 Python 計算腳本

在 `{output_path}/scripts/{YYYY-MM-DD}_{match_id}_calc.py` 撰寫以下邏輯：

```python
# ── 輸入（從 ingest 步驟填入實際數值）──────────────────────────
home_score      = {home_score}
away_score      = {away_score}
h2h_home_rate   = {h2h_home_win_rate}
key_abs_home    = {key_absences_home}
key_abs_away    = {key_absences_away}
motivation      = {motivation_flag}    # True/False
lambda_home     = {home_lambda}
lambda_away     = {away_lambda}
neutral_venue   = False                # 中立場地旗標

import math
from scipy.stats import poisson        # 若環境無 scipy 改用手算 e^-λ * λ^k / k!

# ── 方法 A：加權評分法 ────────────────────────────────────────
delta = (home_score - away_score) / 100.0
home_adv = 0.0 if neutral_venue else 0.05
h2h_adj  = 0.03 if h2h_home_rate > 0.65 else (-0.03 if h2h_home_rate < 0.35 else 0.0)
abs_adj  = (-0.04 if key_abs_home >= 2 else 0.0) + (0.04 if key_abs_away >= 2 else 0.0)
motiv_adj = 0.03 if motivation else 0.0
raw = 0.5 + delta * 0.4 + home_adv + h2h_adj + abs_adj + motiv_adj
raw = max(0.05, min(0.90, raw))        # 限制在合理區間

# logistic 轉換並分配和局
p_home_A  = raw
draw_base = 0.27 - 0.18 * abs(2 * raw - 1)   # 越接近 50/50 和局越高
p_draw_A  = max(0.05, draw_base)
p_away_A  = 1.0 - p_home_A - p_draw_A
p_away_A  = max(0.05, p_away_A)
# 正規化
total = p_home_A + p_draw_A + p_away_A
p_home_A /= total; p_draw_A /= total; p_away_A /= total

# ── 方法 B：簡化 Poisson ──────────────────────────────────────
matrix = {}
for i in range(7):     # 主隊 0-6 球
    for j in range(7): # 客隊 0-6 球
        ph = (lambda_home**i * math.exp(-lambda_home)) / math.factorial(i)
        pa = (lambda_away**j * math.exp(-lambda_away)) / math.factorial(j)
        matrix[(i, j)] = ph * pa

p_home_B = sum(v for (i,j), v in matrix.items() if i > j)
p_draw_B = sum(v for (i,j), v in matrix.items() if i == j)
p_away_B = sum(v for (i,j), v in matrix.items() if i < j)
# 正規化（截斷至 6 球以上有少量損失）
total_B = p_home_B + p_draw_B + p_away_B
p_home_B /= total_B; p_draw_B /= total_B; p_away_B /= total_B

# 大球機率（> 2.5 球）
p_over25_B = sum(v for (i,j), v in matrix.items() if (i+j) > 2)

# ── 整合 ─────────────────────────────────────────────────────
p_home = (p_home_A + p_home_B) / 2
p_draw = (p_draw_A + p_draw_B) / 2
p_away = (p_away_A + p_away_B) / 2

diverge_home = abs(p_home_A - p_home_B) > 0.10
diverge_away = abs(p_away_A - p_away_B) > 0.10

# ── 輸出 ─────────────────────────────────────────────────────
print("=== 方法 A（加權評分法）===")
print(f"  p_home={p_home_A:.4f}  p_draw={p_draw_A:.4f}  p_away={p_away_A:.4f}")
print("=== 方法 B（簡化 Poisson）===")
print(f"  p_home={p_home_B:.4f}  p_draw={p_draw_B:.4f}  p_away={p_away_B:.4f}")
print(f"  p_over25={p_over25_B:.4f}")
print("=== 整合 p_model ===")
print(f"  p_home={p_home:.4f}  p_draw={p_draw:.4f}  p_away={p_away:.4f}")
if diverge_home or diverge_away:
    print("⚠️  模型分歧（差異 > 10pp）→ 信心降級")
```

### 2. 執行腳本

```bash
python3 {output_path}/scripts/{YYYY-MM-DD}_{match_id}_calc.py
```

捕獲輸出（stdout），完整附於報告中。

### 3. 記錄中間結果

| 項目 | 方法 A | 方法 B | p_model |
|------|--------|--------|---------|
| p_home | — | — | — |
| p_draw | — | — | — |
| p_away | — | — | — |
| p_over25 | N/A | — | — |
| 模型分歧 | — | — | 是/否 |

### 4. 分歧處理

- 差異 ≤ 10pp → 正常取平均，信心基準值 3
- 差異 > 10pp → 信心基準值降為 2，報告標注「⚠️ 模型分歧，請謹慎參考」
