# Edu Researcher — Tools

## Primary Tools
| Tool | Purpose |
|------|---------|
| `Read` | 讀取 agent 系統檔案（soul.md, workflow.yaml, org.md 等） |
| `Glob` | 找出所有 agent 目錄與相關檔案 |
| `Grep` | 搜尋關鍵字或模式 |
| `Bash` | 唯讀指令（ls, cat）查閱系統結構 |
| `WebSearch` | 搜尋外部最新資料、技術文章、教育素材 |
| `WebFetch` | 抓取關鍵文章完整內容 |

## MCP Tools (Authorized)

| MCP Tool | 授權操作 | 用途 |
|----------|---------|------|
| `mcp__desktop-commander__read_multiple_files` | read_multiple_files | 讀取 T:\ 路徑的 agent 系統檔案（soul.md, workflow.yaml, org.md 等，Google Drive 限制須用此工具）|
| `mcp__desktop-commander__list_directory` | list_directory | 掃描 T:\ 目錄結構，找出 agent 目錄與相關檔案 |
| `mcp__workspace__bash` | worklog | 呼叫 `scripts/worklog.sh` 打卡記錄工時 |
| `WebSearch` / `mcp__workspace__web_fetch` | 搜尋教育資源 | 搜尋外部最新資料、技術文章、教育素材並擷取完整內容 |

> 注意：T:\ 路徑的檔案**必須**用 `read_multiple_files`，禁止使用 `read_file`（Google Drive 限制）。

## Do NOT Use
- `Edit` — 不修改任何非 memory/ 的檔案
- `Write` — 僅限 `memory/` 目錄（紀錄研究心得）
- `Agent` — 不派發子 agent

## Tool Usage Guidelines
- **Bash 只做唯讀操作**：ls、cat、find 查閱，不執行寫入或修改指令
- **逐一讀檔**：避免一次 Read 太多大型檔案，分批處理
- **WebSearch 後 WebFetch**：先搜尋找到 URL，再抓取完整內容
