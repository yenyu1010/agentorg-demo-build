# Edu Manager — Tools

## Primary Tool

| Tool | Purpose |
|------|---------|
| `Agent` | **THE core tool.** 分派下屬 agent，包含 edu-researcher、content-designer、doc-generator、shared/researcher |

## Supporting Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 agent 定義（soul.md、org.md）以決定分派策略 |
| `Glob` | 快速掃描專案結構，確認產出路徑 |
| `Grep` | 搜尋 worklog JSON 以產出工時明細 |
| `Bash` | 呼叫 `scripts/worklog.sh` 打卡（僅此用途） |

## MCP Tools (Authorized)

| MCP Tool | 授權操作 | 用途 |
|----------|---------|------|
| `mcp__desktop-commander__read_multiple_files` | read_multiple_files | 讀取 T:\ 路徑的 agent 定義、org.md、soul.md 等（Google Drive 限制須用此工具）|
| `mcp__desktop-commander__list_directory` | list_directory | 掃描 T:\ 專案目錄結構，確認產出路徑 |
| `mcp__workspace__bash` | worklog | 呼叫 `scripts/worklog.sh` 打卡記錄工時 |

> 注意：T:\ 路徑的檔案**必須**用 `read_multiple_files`，禁止使用 `read_file`（Google Drive 限制）。

## Do NOT Use

| Tool | Reason |
|------|--------|
| `Edit` | 你是 Manager，不直接修改檔案；分派給下屬 |
| `Write` | 你是 Manager，不直接產出教材；分派給下屬 |
| `WebSearch` | 分派給 shared/researcher |
| `WebFetch` | 分派給 shared/researcher |

## Agent Tool Parameters

```
Agent({
  description: "short label for this dispatch",
  subagent_type: "general-purpose" | "Explore",
  model: "opus" | "sonnet",
  prompt: "...",          # full brief including worklog/memory protocol
  run_in_background: true | false,
  isolation: "none"       # edu agents don't write conflicting code files
})
```

### Subagent Type Mapping

| Worker Agent | subagent_type |
|-------------|---------------|
| edu-researcher | Explore |
| content-designer | general-purpose |
| doc-generator | general-purpose |
| shared/researcher | Explore |

- **Memory exception**: You MAY use `Write` to save learnings to `agents/edu/manager/memory/` per memory-protocol.md
