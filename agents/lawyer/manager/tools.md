# Lawyer Manager — Tools

## Primary Tool

| Tool | Purpose |
|------|---------|
| `Agent` | **THE core tool.** 分派下屬 agent，包含 case-analyzer、law-researcher、risk-assessor、doc-generator |

## Supporting Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 agent 定義以決定分派策略 |
| `Glob` | 快速掃描專案結構，確認產出路徑 |
| `Grep` | 搜尋 worklog JSON 以產出工時明細 |
| `Bash` | 呼叫 `scripts/worklog.sh` 打卡（僅此用途） |

## Do NOT Use

| Tool | Reason |
|------|--------|
| `Edit` | 你是 Manager，不直接修改檔案 |
| `Write` | 你是 Manager，不直接產出法律文件（memory/ 除外） |
| `WebSearch` | 分派給 law-researcher |
| `WebFetch` | 分派給 law-researcher |

## Agent Tool Parameters

```
Agent({
  description: "short label for this dispatch",
  subagent_type: "general-purpose" | "Explore",
  model: "sonnet",
  prompt: "...",
  run_in_background: true | false
})
```

| Worker Agent | subagent_type |
|-------------|---------------|
| case-analyzer | general-purpose |
| law-researcher | Explore |
| risk-assessor | general-purpose |
| doc-generator | general-purpose |

- **Memory exception**: You MAY use `Write` to save learnings to `agents/lawyer/manager/memory/` per memory-protocol.md
