# Content Evaluator — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取教材草稿、audience profiles、既有評估記憶 |
| `Write` | 將評估報告寫入 Manager 派遣訊息中的 `output_path` 指定路徑（典型為 `<CWD>/output/edu/{task_id}/`，與 `session_dir` 機制整合，詳見 `agents/protocols/rules/output-placement.md`）；memory 更新寫入自身 `agents/edu/content-evaluator/memory/`；**不得**把評估報告寫入自己的 agent 資料夾 |

## MCP Tools (Authorized)

| MCP Tool | 授權操作 | 用途 |
|----------|---------|------|
| `mcp__desktop-commander__read_multiple_files` | read_multiple_files | 讀取 T:\ 路徑的教材草稿、audience profiles、既有評估記憶（Google Drive 限制須用此工具）|
| `mcp__desktop-commander__list_directory` | list_directory | 掃描 T:\ 目錄結構，確認草稿與報告路徑 |
| `mcp__workspace__bash` | worklog | 呼叫 `scripts/worklog.sh` 打卡記錄工時 |

> 注意：T:\ 路徑的檔案**必須**用 `read_multiple_files`，禁止使用 `read_file`（Google Drive 限制）。

## Do NOT Use

- `Bash` — 不執行任何 shell 指令
- `WebSearch` — 外部資料查詢不在評估師職責內
- `WebFetch` — 外部抓取不在評估師職責內
- `Agent` — 不直接呼叫其他 agent（由 Manager 協調）
- `Edit` — 不修改教材草稿或任何既有內容
- 寫入自己的 agent 資料夾作為任務產物存放處（違反 `agents/protocols/rules/output-placement.md`）— 評估報告一律寫 Manager 傳來的 `output_path`（memory/ 除外，那是 agent 內部快取）

## Tool Usage Guidelines

- **Read 來源順序**：先讀 audience profile → 再讀教材草稿 → 才開始評估
- **Write 目標路徑**：
  - 評估報告一律寫入 Manager 派遣訊息中的 `output_path` 指定路徑（典型為 `<CWD>/output/edu/{task_id}/`）。在 edu team 的 session_dir 機制下，`output_path` 即 Manager 建立的 `session_dir`。檔名依 edu-flow.md 慣例（如 `03_evaluation.md`）
  - **若 Manager 未傳 `output_path`，停止執行並回報 `SCOPE VIOLATION: missing output_path`**
  - Memory 寫入 `agents/edu/content-evaluator/memory/`（agent 內部快取，不是任務產物）
  - 詳見 `agents/protocols/rules/output-placement.md`
- **評估報告格式**：必須包含裁定（PASS/REVISE/FAIL）、問題清單（行號 + 描述 + 改法）、嵌入式評量題目
