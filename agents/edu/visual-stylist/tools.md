# Visual Stylist — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取教材草稿、PPT JSON、受眾 profile、品牌色彩指南 |
| `Write` | 產出視覺設計規範、修改後的 PPT JSON、樣式建議報告 |
| `Bash` | 執行 python-pptx 腳本調整投影片樣式（字型、配色、版面）|

## MCP Tools (Authorized)

| MCP Tool | 授權操作 | 用途 |
|----------|---------|------|
| `mcp__desktop-commander__read_multiple_files` | read_multiple_files | 讀取 T:\ 路徑的教材草稿、PPT JSON、受眾 profile、品牌色彩指南（Google Drive 限制須用此工具）|
| `mcp__desktop-commander__write_file` | write_file | 將視覺設計規範、修改後的 PPT JSON、樣式建議報告寫入 T:\ 指定路徑 |
| `mcp__desktop-commander__list_directory` | list_directory | 掃描 T:\ 目錄結構，確認輸入/輸出路徑 |
| `mcp__workspace__bash` | worklog、執行樣式腳本 | 呼叫 `scripts/worklog.sh` 打卡；執行 python-pptx 樣式腳本調整投影片字型、配色、版面 |

> 注意：T:\ 路徑的檔案**必須**用 `read_multiple_files`，禁止使用 `read_file`（Google Drive 限制）。

## Do NOT Use

- `WebSearch` — 外部搜尋由 Edu Researcher 負責
- `WebFetch` — 外部抓取由 Edu Researcher 負責
- `Agent` — 不直接呼叫其他 agent（由 Manager 協調）
- `Edit` — 不修改內容草稿（僅透過 Write 產出新的樣式化版本）
- `PowerShell`（Claude Code 原生工具）— 禁用，見下方 Shell 偏好章節

## Shell 偏好（Bash-First）

依 `agents/protocols/rules/shell-preference.md`：
- ✅ **首選** `Bash` + Python 腳本（跨平台）
- ✅ 若需要 Windows COM（例如 PowerPoint 渲染），透過 `Bash` 呼叫 `powershell.exe -Command "..."`
- ❌ **禁用** Claude Code 的 `PowerShell` 工具（會觸發權限提示）

具體範例（PowerPoint PPTX → JPG 渲染）：
```bash
powershell.exe -Command "
\$ppt = New-Object -ComObject PowerPoint.Application;
\$pres = \$ppt.Presentations.Open('T:\path\to.pptx', \$true, \$false, \$false);
\$pres.SaveAs('T:\out\dir', 17);
\$pres.Close();
\$ppt.Quit()
"
```

## Memory Exception

- 可以 Write 到 `edu/visual-stylist/memory/` 保存受眾視覺偏好、品牌規範快取

## Tool Usage Guidelines

- **Read 來源順序**：先讀 audience profile → 再讀 brand-colors-guide.md → 再讀教材草稿/PPT JSON
- **Write 目標路徑**：視覺規範寫入 `output/` 或 Manager 指定路徑；記憶寫入 `memory/`
- **Bash 用途限制**：僅用於執行 python-pptx 樣式腳本和 worklog 打卡，不做內容處理
