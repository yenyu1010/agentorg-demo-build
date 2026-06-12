# Football Analysis Manager — Tools

## Primary Tool

| Tool | Purpose |
|------|---------|
| `Agent` | **THE core tool.** 分派下屬 worker：odds-analyst、form-analyst、value-modeler |

## Supporting Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 worker 報告、agent 定義以決定分派策略 |
| `Glob` | 掃描 worklog 目錄確認 worker 已完成打卡 |
| `Grep` | 搜尋 worklog JSON 以產出工時明細表 |
| `Bash` | 呼叫 `scripts/worklog.sh` 打卡（僅此用途） |

## Do NOT Use

| Tool | Reason |
|------|--------|
| `Edit` | 你是 Manager，不直接修改 agent 檔案 |
| `Write` | 你是 Manager，不直接產出分析文件（memory/ 除外） |
| `WebSearch` | 分派給 odds-analyst 或 form-analyst |
| `WebFetch` | 分派給 odds-analyst 或 form-analyst |

## Agent Tool Parameters

```
Agent({
  description: "short label for this dispatch",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "...",
  run_in_background: true | false
})
```

## Subagent Type Mapping

| Worker Agent | subagent_type | model |
|-------------|---------------|-------|
| odds-analyst | general-purpose | sonnet |
| form-analyst | general-purpose | sonnet |
| value-modeler | general-purpose | sonnet |

## MCP Tools (Authorized)

| MCP 工具 | 用途 |
|----------|------|
| `mcp__workspace__bash` | 執行 worklog.sh 打卡腳本 |
| `mcp__desktop-commander__read_multiple_files` | 讀取 T:\ 路徑上的 agent 檔案（禁用 read_file，詳見 google-drive-read.md） |
| `mcp__desktop-commander__list_directory` | 確認 worker worklog 目錄結構 |

> Memory exception：你 MAY 使用 Write 將學習成果保存至 `agents/football/manager/memory/`，符合 memory-protocol.md 規範。
