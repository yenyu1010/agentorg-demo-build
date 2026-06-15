# Football Manager — Classify Flow

## 流程總覽

```
feedback_detect → parse_match_info → check_completeness → session_init
```

---

## feedback_detect

> **此步驟已提升為 workflow.yaml 頂層獨立步驟**（在 classify 之前執行）。
> 詳細邏輯見 `agents/protocols/workflows/feedback-detect-flow.md`。
> 本 flow 不重複實作，避免雙重執行。

---

## parse_match_info（Manager 直接執行）

**解析以下欄位：**

| 欄位 | 說明 | 缺失處理 |
|------|------|---------|
| `league` | 聯賽名稱（英超、西甲、Champions League 等） | 詢問用戶，停止流程 |
| `home_team` | 主隊名稱 | 詢問用戶，停止流程 |
| `away_team` | 客隊名稱 | 詢問用戶，停止流程 |
| `kickoff_time` | 開賽時間（ISO 8601 或自然語言） | 標注「時間待確認」，繼續 |
| `bankroll` | 用戶資金（可選，僅用於注碼示意） | 省略，value-modeler 以百分比表示 |
| `language` | 回應語言 | 預設 zh-TW |

**用戶確認詢問範本（缺 league / home_team / away_team 時）：**

```
請提供以下資訊以便進行分析：

- 聯賽名稱：（例：英超、西甲、UEFA Champions League）
- 主隊名稱：
- 客隊名稱：
- 開賽時間（可選）：
```

---

## session_init（Manager 直接執行）

1. 決定 `task_id`：格式 `{league_short}-{home_short}vs{away_short}-{YYYYMMDD}`
   - 例：`epl-mancityvsmunited-20260612`
2. 決定 `trace_id`：使用當前 timestamp（例：`2026-06-12T06:08:00Z`）或由上游傳入
3. 組合 `output_path`：`$CLAUDE_PROJECT_DIR/output/football/{task_id}/`
4. 建立目錄（Manager 以 Bash 執行）
5. 寫入 `$output_path/00_context.md`，包含：
   - task_id、trace_id、league、home_team、away_team、kickoff_time、bankroll（若有）、language、用戶原始問題、分析開始時間
