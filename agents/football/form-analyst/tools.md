# Team Form Analyst — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 memory/、Manager 傳入的輸入文件 |
| `Write` | 寫入狀態報告至 output_path；寫入 memory/ 與 worklog/ |
| `WebFetch` | 抓取 titan007.com 賽事分析頁、H2H 往績頁 |
| `WebSearch` | 搜尋最新傷停資訊、陣容新聞、賽前消息（標注來源與日期） |
| `Bash` | 執行 `scripts/worklog.sh start/end` 打卡；禁止其他 Bash 操作 |

## MCP Tools (Authorized)

| MCP 工具 | 用途 |
|----------|------|
| `mcp__desktop-commander__read_multiple_files` | 讀取 T:\ (Google Drive) 上的 agent 定義檔或共用資料 |
| `mcp__desktop-commander__write_file` | 寫入報告至 T:\ 路徑（如 Manager 指定 output_path 在 Drive 上） |
| `mcp__desktop-commander__list_directory` | 列出 T:\ 目錄確認輸出位置 |
| `mcp__workspace__bash` | 執行 worklog.sh 打卡（mcp 環境備用） |

> ⚠️ T:\ 路徑必須用 `read_multiple_files`，`read_file` 在 Google Drive 只回傳 metadata。

## Do NOT Use

| Tool | Reason |
|------|--------|
| `Agent` | Worker 不派遣其他 agent |
| `Edit` | 不修改他人的 agent 定義檔案 |
| `mcp__b1592d31*__gmail_*` | 狀態分析不需寄送郵件 |
| `mcp__972626e3*__*` | 狀態分析不需日曆操作 |
