# Doc Generator — Tools

## Primary Tools
| Tool | Purpose |
|------|---------|
| `Read` | 讀取 Content Designer 產出的 Markdown/JSON 輸入檔案 |
| `Bash` | 執行 Python 腳本（gen-pptx.py、gen-docx.py）和 libreoffice CLI |
| `Write` | 若需要建立臨時中間檔案（如暫存 JSON）才使用 |

## MCP Tools (Authorized)

| MCP Tool | 授權操作 | 用途 |
|----------|---------|------|
| `mcp__desktop-commander__read_multiple_files` | read_multiple_files | 讀取 T:\ 路徑的 Markdown/JSON 輸入檔案（Google Drive 限制須用此工具）|
| `mcp__desktop-commander__write_file` | write_file | 將生成的 PPT/Word/PDF 或臨時中間檔寫入 T:\ 指定路徑 |
| `mcp__desktop-commander__list_directory` | list_directory | 掃描 T:\ 目錄結構，確認輸入/輸出路徑 |
| `mcp__workspace__bash` | worklog、執行文件生成腳本 | 呼叫 `scripts/worklog.sh` 打卡；執行 `gen-pptx.py`、`gen-docx.py`、`libreoffice` CLI 等生成腳本 |

> 注意：T:\ 路徑的檔案**必須**用 `read_multiple_files`，禁止使用 `read_file`（Google Drive 限制）。

## Do NOT Use
- `WebSearch` — 不搜尋外部資料，轉換是純技術任務
- `WebFetch` — 同上
- `Agent` — 不派發子 agent
- `Edit` — 不修改輸入內容，只讀取後傳給腳本
- `PowerShell`（Claude Code 原生工具）— 禁用，見下方 Shell 偏好章節

## Shell 偏好（Bash-First）

依 `agents/protocols/rules/shell-preference.md`：
- ✅ **首選** `Bash` + Python 腳本（跨平台）
- ✅ 若需要 Windows COM（例如 PowerPoint 渲染），透過 `Bash` 呼叫 `powershell.exe -Command "..."`
- ❌ **禁用** Claude Code 的 `PowerShell` 工具（會觸發權限提示）

<!-- 2026-04-22: haiku→sonnet 模型升級後同步修訂：PPT 截圖範例改 LibreOffice-first -->

具體範例（PowerPoint PPTX → JPG/PNG 渲染）：

**首選方式：LibreOffice（跨平台、無需 Office）**
```bash
python scripts/pptx_to_images.py --input in.pptx --output-dir out/ --format jpg --dpi 150
```

- 預設 `--method libreoffice`（需 LibreOffice 已安裝）；`--method auto` 會自動選擇可用後端
- `--method com` fallback 需 Windows + PowerPoint 已安裝（見下方高保真 fallback）
- 支援 `--format png|jpg`、`--dpi`（預設 150）、`--manifest` 產生索引檔

**高保真 fallback（SmartArt / 嵌入字型失真時）：PowerPoint COM**
當 LibreOffice 渲染 SmartArt、複雜動畫、或嵌入字型出現失真，切換為 COM 後端：
```bash
python scripts/pptx_to_images.py --input in.pptx --output-dir out/ --format jpg --method com
```

或直接以 bash 呼叫 powershell.exe（僅在腳本不可用時使用）：
```bash
powershell.exe -Command "
\$ppt = New-Object -ComObject PowerPoint.Application;
\$pres = \$ppt.Presentations.Open('T:\path\to.pptx', \$true, \$false, \$false);
\$pres.SaveAs('T:\out\dir', 17);
\$pres.Close();
\$ppt.Quit()
"
```

## Tool Usage Guidelines
- **Bash 執行腳本**：`python gen-pptx.py input.json output.pptx`、`libreoffice --headless --convert-to pdf input.docx`
- **Write 僅用於產出**：最終 PPT/Word/PDF 實體檔案，或必要的臨時中間檔
- **驗證產出**：執行完腳本後，用 Bash 確認輸出檔案存在且非空（`ls -la output.pptx`）
- **Memory exception**: You MAY use `Write` to save learnings to `agents/edu/doc-generator/memory/` per memory-protocol.md

## PPT 生成企業標準合規

### 色彩與尺寸標準
- 所有 PPT 生成必須參考 `workflow/ppt-standards.md`
- `gen-pptx.py` 應接受 `--colors` 參數指定企業色彩配置
  - 預設值：`ppt-standards.md` 中定義的企業標準色
  - 範例：`python gen-pptx.py --input input.json --output output.pptx --colors "brand-green:#61B520,light-green:#D6EFA8"`

### 輸出驗證
- 色彩合規檢查：確認主色為 #61B520（品牌綠）、副色為 #D6EFA8（淺綠底色）
- 尺寸合規檢查：確認投影片尺寸為 10" × 7.5"
- 字體合規檢查：確認使用 Calibri 字體
- 邊距合規檢查：確認邊距至少 0.3"

## PPT 生成色彩驗證

**gen-pptx.py 實現方式**：
- 腳本內硬編碼企業色彩常數，拒絕接受 brand-colors-guide.md 外的色值
- 產出前自動驗證：掃描生成的 PPT XML，確認主色為 #61B520（品牌綠）、輔色為 #D6EFA8（淺綠底色）
- 若驗證失敗，拒絕儲存檔案，回報「色彩合規性失敗」

**外部驗證步驟**（generate-flow.md 第 5 章執行）：
- 驗證軟體：定期檢查 PPT 內嵌色彩，記錄違反企業標準的色值
- 失敗處理：色彩驗證失敗視同生成失敗，強制重新執行 gen-pptx.py
