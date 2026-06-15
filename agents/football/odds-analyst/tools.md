# Odds Movement Analyst — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 manager 傳入的賽事參數與 memory/ 內的歷史 URL pattern |
| `Write` | 寫入賠率報告（僅限 output_path 與 memory/）、更新 worklog |
| `WebFetch` | 抓取 titan007.com 歐賠頁、亞盤頁（主要資料來源） |
| `WebSearch` | 當 WebFetch 被擋或頁面動態載入失敗時的 fallback 搜尋 |
| `Bash` | 呼叫 `scripts/worklog.sh start/end` 打卡（僅此用途） |

## MCP Tools (Authorized)

| MCP 工具 | 用途 |
|----------|------|
| `mcp__workspace__bash` | worklog 打卡（scripts/worklog.sh start/end） |

> 本 agent 不需要 Gmail / Calendar / Google Drive 存取。若未來需要從雲端硬碟讀取賽事清單，須由 Agent Builder 更新 tools.md 並經 Governance 審查。

## Do NOT Use

| Tool | Reason |
|------|--------|
| `Agent` | Worker 不派遣其他 agent；協調由 football/manager 負責 |
| `Edit` | 不修改其他 agent 的定義檔案 |
| `Write`（限制） | 僅允許寫入 `memory/`、`worklog/`、及 manager 指定的 `output_path`；禁止寫入其他 agent 目錄 |
