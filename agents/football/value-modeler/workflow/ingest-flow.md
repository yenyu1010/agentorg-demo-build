# Value Modeler — Ingest Flow

## 目的

讀取並驗證上游兩份結構化報告，確認包含建模所需的所有欄位。

## 步驟

### 1. 讀取上游報告

```
Read: {output_path}/01_odds_analysis.md        # odds-analyst 產出
Read: {output_path}/02_form_analysis.md        # form-analyst 產出
```

### 2. 驗證 odds_analysis 必含欄位

| 欄位 | 說明 |
|------|------|
| `match_id` | 場次識別碼 |
| `market_odds` | 各市場賠率（1X2、亞盤、大小球） |
| `implied_prob` | 各市場去水後隱含機率 |
| `line_movement` | 盤口移動紀錄 |
| `sharp_signal` | 機構資金方向（bullish_home / bullish_away / neutral） |
| `water_level_change` | 水位變化量（百分比） |

### 3. 驗證 form_analysis 必含欄位

| 欄位 | 說明 |
|------|------|
| `match_id` | 與上游一致 |
| `home_score` | 主隊狀態評分（0–100） |
| `away_score` | 客隊狀態評分（0–100） |
| `h2h_home_win_rate` | 近 5 場 H2H 主方勝出比例 |
| `home_lambda` | 主隊場均進球 λ（Poisson 用） |
| `away_lambda` | 客隊場均進球 λ（Poisson 用） |
| `key_absences_home` | 主隊核心缺陣球員數 |
| `key_absences_away` | 客隊核心缺陣球員數 |
| `motivation_flag` | 關鍵晉級場次旗標（True/False） |

### 4. 驗證失敗處理

若任一必要欄位缺失：
1. 停止建模
2. 輸出：`INPUT_ERROR: {欄位名稱} 缺失於 {報告名稱}，無法建模。請回報 football/manager 重新派遣對應 analyst。`
3. 呼叫 `log_end`（狀態：failed）

### 5. 建立 session 計算目錄

```bash
mkdir -p {output_path}/scripts/
```

計算腳本統一放此目錄，命名格式：`{YYYY-MM-DD}_{match_id}_calc.py`
