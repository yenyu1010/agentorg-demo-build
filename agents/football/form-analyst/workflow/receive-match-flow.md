# Form Analyst — Receive Match Flow

## 目的

解析 football/manager 指派的賽事資訊，確認必要參數齊全後進入近況抓取流程。

## 步驟

### 1. 解析輸入參數

從 manager dispatch prompt 中提取：

| 參數 | 說明 | 必填 |
|------|------|:----:|
| `home_team` | 主隊名稱（繁體中文或英文） | ✅ |
| `away_team` | 客隊名稱（繁體中文或英文） | ✅ |
| `match_datetime` | 比賽時間（ISO 8601 格式） | ✅ |
| `competition` | 賽事名稱（例：英超、歐冠） | ✅ |
| `output_path` | 報告寫入路徑 | ✅ |
| `focus_notes` | 特別關注點（傷停、換帥、主場優勢等） | 選填 |

### 2. 參數驗證

- 若 `home_team` 或 `away_team` 缺失 → **中止任務**，回報 manager：「缺少必要賽事資訊，無法進行近況分析。」
- 若 `match_datetime` 缺失 → 繼續，但在報告中標注「比賽時間未知，近況時效性無法確認」
- 若 `output_path` 缺失 → 使用預設路徑 `output/football/form-analyst/{YYYYMMDD}_{home_team}_vs_{away_team}/`

### 3. 初始化任務摘要

設定 `MATCH_SUMMARY` 變數：
```
MATCH_SUMMARY="{competition} | {home_team} vs {away_team} | {match_datetime}"
```

### 4. 記錄特別關注點

若 `focus_notes` 存在，將其存入 `FOCUS_CONTEXT` 變數，在 `fetch-form-flow` 與 `analyze-flow` 中優先針對關注點蒐集資料與評論。

### 5. 讀取 memory/MEMORY.md（若存在）

若 `memory/MEMORY.md` 存在，載入已知的 URL pattern 與近況評估偏好，供 fetch-form-flow 使用。

## 輸出

- `MATCH_CONTEXT`：包含所有已解析參數的結構化物件，傳遞給後續步驟
- `FOCUS_CONTEXT`：特別關注點（若有），在分析步驟中優先處理
