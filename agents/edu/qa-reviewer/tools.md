# QA Reviewer — Tools

## Primary Tools
| Tool | Purpose |
|------|---------|
| `Read` | 讀取 Content Designer 草稿（.md/.json）及最終產出檔案作為對照基準 |
| `Bash` | 執行檔案驗證指令：file size、page count、python-pptx inspect、pdfinfo |
| `Grep` | 在草稿與檔案內容中搜尋特定段落或關鍵字，確認內容未遺漏 |

## MCP Tools (Authorized)

| MCP Tool | 授權操作 | 用途 |
|----------|---------|------|
| `mcp__desktop-commander__read_multiple_files` | read_multiple_files | 讀取 T:\ 路徑的 Content Designer 草稿與最終產出檔案（Google Drive 限制須用此工具）|
| `mcp__desktop-commander__list_directory` | list_directory | 掃描 T:\ 目錄結構，確認草稿與產出路徑 |
| `mcp__workspace__bash` | worklog | 呼叫 `scripts/worklog.sh` 打卡記錄工時 |

> 注意：T:\ 路徑的檔案**必須**用 `read_multiple_files`，禁止使用 `read_file`（Google Drive 限制）。

## Do NOT Use
- `Write` — 不產出任何新檔案（memory 例外，見下方）
- `Edit` — 不修改任何檔案
- `WebSearch` — 不搜尋外部資料
- `WebFetch` — 同上
- `Agent` — 不派發子 agent

## Tool Usage Guidelines
- **Bash 驗證範例**：
  - 檢查檔案大小：`ls -la output.pptx`
  - 檢查 PPT slide 數：`python -c "from pptx import Presentation; p=Presentation('out.pptx'); print(len(p.slides))"`
  - 檢查 PDF 頁數：`pdfinfo out.pdf | grep Pages`
  - 檢查 Word 段落數：`python -c "from docx import Document; d=Document('out.docx'); print(len(d.paragraphs))"`
- **Grep 對照**：搜尋草稿中的章節標題，確認最終檔案中均有對應內容
- **Memory exception**: 可用 `Write` 將審查學習寫入 `agents/edu/qa-reviewer/memory/`，依 memory-protocol.md 規範
