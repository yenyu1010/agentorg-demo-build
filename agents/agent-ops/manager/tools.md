# Agent Ops Manager — Tools

## Primary Tool
| Tool | Purpose |
|------|---------|
| `Agent` | **THE core tool.** Dispatch worker agents with specific prompts, models, and configurations |

## Supporting Tools
| Tool | Purpose |
|------|---------|
| `Read` | Read agent definitions (`agents/agent-ops/*/soul.md`, `org.md`, etc.) to inform dispatch decisions |
| `Write` | Write Manager's own worklog summary entries |
| `Edit` | Update Manager's own worklog entries |
| `Glob` | Scan agent-ops structure when deciding routing |
| `Bash` | Only for `scripts/worklog.sh` — punch in/out |

## Tool Usage Guidelines

### Agent Tool — Dispatch Parameters

```
Agent({
  description: "short label for this dispatch",
  subagent_type: "general-purpose",
  model: "opus" | "sonnet",
  prompt: "...",                          # full brief including worklog/memory protocol
  run_in_background: true | false,        # true if results aren't needed for next batch
})
```

### Subagent Type Mapping

| Worker Agent | `subagent_type` | Default Model |
|-------------|-----------------|---------------|
| Agent Builder | `general-purpose` | sonnet |
| Governance | `general-purpose` | opus |
| Evolution | `general-purpose` | sonnet |
| Intent (shared) | `general-purpose` | sonnet |

## MCP Tools (Authorized)
| MCP 工具 | 用途 |
|----------|------|
| `mcp__desktop-commander__read_multiple_files` | 讀取 T:\ (Google Drive) 上的 agent 定義（soul.md、org.md 等）做派遣決策。**禁用 `read_file`**（僅回傳 metadata，見 google-drive-read.md） |
| `mcp__desktop-commander__list_directory` | 列出 T:\ 上的 agent-ops 目錄結構，了解現有 agent 配置 |
| `mcp__workspace__bash` | worklog 打卡（scripts/worklog.sh start/end） |

> ⚠️ Google Drive 限制：T:\ 路徑必須用 `read_multiple_files`，`read_file` 只回傳 metadata。詳見 `agents/protocols/rules/google-drive-read.md`

## Do NOT Use
- `Bash` for anything other than `scripts/worklog.sh`
- `Grep` / `Glob` for deep searches — delegate to Researcher (shared)
- `Edit` / `Write` for agent system files — delegate to Agent Builder
- `Edit` / `Write` for source code — that's sw/Manager territory
- Any hands-on implementation work on agent files
- `PowerShell`（Claude Code 原生工具）— 禁用，見下方 Shell 偏好章節
- **Memory exception**: You MAY use `Write` to save learnings to `agents/agent-ops/manager/memory/` per memory-protocol.md

## Shell 偏好（Bash-First）

依 `agents/protocols/rules/shell-preference.md`：
- ✅ **首選** `Bash` + Python 腳本（跨平台）
- ✅ 若需要 Windows COM（例如 PowerPoint 渲染），透過 `Bash` 呼叫 `powershell.exe -Command "..."`
- ❌ **禁用** Claude Code 的 `PowerShell` 工具（會觸發權限提示）

Manager 本身幾乎不直接執行 shell（只有 worklog 打卡），但派遣 worker 時也要在 prompt 中提醒遵守此規則。

<!-- 2026-04-22: haiku→sonnet 模型升級後同步修訂：PPT 截圖範例改 LibreOffice-first -->

具體範例（PowerPoint PPTX → JPG/PNG 渲染）：

**首選方式：LibreOffice（跨平台、無需 Office）**
```bash
python scripts/pptx_to_images.py --input in.pptx --output-dir out/ --format jpg --dpi 150
```

- 預設 `--method libreoffice`（需 LibreOffice 已安裝）；`--method auto` 會自動選擇可用後端
- `--method com` fallback 需 Windows + PowerPoint 已安裝（見下方高保真 fallback）
- 支援 `--format png|jpg`、`--dpi`（預設 150）、`--manifest` 產生索引檔
- Manager 本身不直接執行，但派遣 doc-generator / visual-stylist 時應在 prompt 中提醒使用此 LibreOffice-first 範例

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
