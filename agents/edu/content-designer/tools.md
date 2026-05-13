# Content Designer — Tools

## Primary Tools
| Tool | Purpose |
|------|---------|
| `Read` | 讀取 audience profiles、edu-researcher 產出、既有教材草稿 |
| `Write` | 將教材草稿寫入 Manager 派遣訊息中的 `output_path` 指定路徑（典型為 `<CWD>/output/edu/{task_id}/`，與 `session_dir` 機制整合，詳見 `agents/protocols/rules/output-placement.md`）；**不得**寫入自己的 agent 資料夾（memory/ 除外）|

## MCP Tools (Authorized)

| MCP Tool | 授權操作 | 用途 |
|----------|---------|------|
| `mcp__desktop-commander__read_multiple_files` | read_multiple_files | 讀取 T:\ 路徑的 audience profiles、edu-researcher 產出、既有教材草稿（Google Drive 限制須用此工具）|
| `mcp__desktop-commander__write_file` | write_file | 將教材草稿寫入 T:\ 指定路徑 |
| `mcp__desktop-commander__list_directory` | list_directory | 掃描 T:\ 目錄結構，確認輸入/輸出路徑 |
| `mcp__workspace__bash` | worklog | 呼叫 `scripts/worklog.sh` 打卡記錄工時 |
| `WebSearch` / `mcp__workspace__web_fetch` | 查詢教育素材 | 搜尋並擷取外部教育資源、參考素材 |

> 注意：T:\ 路徑的檔案**必須**用 `read_multiple_files`，禁止使用 `read_file`（Google Drive 限制）。

## Do NOT Use
- `Bash` — 不執行任何 shell 指令（研究和系統查詢是 edu-researcher 的工作）
- `WebSearch` — 外部搜尋由 edu-researcher 負責
- `WebFetch` — 外部抓取由 edu-researcher 負責
- `Agent` — 不直接呼叫其他 agent（由 Manager 協調）
- `Edit` — 不修改既有教材（草稿為全新 Write，修訂由 Manager 派新任務）
- 寫入自己的 agent 資料夾作為任務產物存放處（違反 `agents/protocols/rules/output-placement.md`）— 教材草稿一律寫 Manager 傳來的 `output_path`（memory/ 除外，那是 agent 內部快取）

## Tool Usage Guidelines
- **Read 來源順序**：先讀 audience profile → 再讀 researcher 輸出 → 才開始設計
- **Write 目標路徑**：教材草稿一律寫入 Manager 派遣訊息中的 `output_path` 指定路徑（典型為 `<CWD>/output/edu/{task_id}/`）。在 edu team 的 session_dir 機制下，`output_path` 即 Manager 建立的 `session_dir`。**若 Manager 未傳 `output_path`，停止執行並回報 `SCOPE VIOLATION: missing output_path`**。檔名依 edu-flow.md 慣例（如 `02_design_draft.md`），詳見 `agents/protocols/rules/output-placement.md`。
- **每次 Write 前先確認路徑**，避免覆蓋既有草稿
