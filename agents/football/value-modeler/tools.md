# Value Betting Modeler — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 odds-analyst 與 form-analyst 的結構化輸出報告 |
| `Write` | 寫入建模報告至 output_path、寫入 memory/track-record.md |
| `Bash` | 執行 worklog.sh 打卡、執行 Python 計算腳本（隱含機率、Poisson、Kelly） |

## MCP Tools (Authorized)

| MCP 工具 | 用途 |
|----------|------|
| `mcp__desktop-commander__read_multiple_files` | 讀取 Google Drive（T:\）上的上游報告檔案 |
| `mcp__desktop-commander__write_file` | 寫入建模報告到 T:\ 路徑 |
| `mcp__workspace__bash` | 執行 worklog.sh 打卡、執行 Python 計算腳本 |

> 注意：本 agent 不需要 Gmail 或 Calendar，資料來自上游 agent 而非外部網路。

## Do NOT Use

| Tool | Reason |
|------|--------|
| `Agent` | Worker 不派遣其他 agent |
| `WebSearch` | 原始資料由 odds-analyst 和 form-analyst 提供，不自行抓取 |
| `WebFetch` | 同上 |
| `Edit` | 不修改他人的 agent 定義檔案 |
