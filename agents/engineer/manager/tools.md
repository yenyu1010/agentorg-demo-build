# Engineer Manager — Tools

## Primary Tool

| Tool | Purpose |
|------|---------|
| `Agent` | **THE core tool.** 分派下屬 agent |

## Supporting Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 agent 定義以決定分派策略 |
| `Glob` | 掃描專案結構 |
| `Grep` | 搜尋 worklog JSON |
| `Bash` | 呼叫 `scripts/worklog.sh` 打卡 |

## Do NOT Use

| Tool | Reason |
|------|--------|
| `Edit` | 你是 Manager，不直接修改程式碼 |
| `Write` | 你是 Manager，不直接產出程式碼（memory/ 除外） |
| `WebSearch` | 分派給 system-analyst 或 developer |

## Agent Tool Parameters

| Worker Agent | subagent_type |
|-------------|---------------|
| system-analyst | general-purpose |
| developer | general-purpose |
| code-reviewer | general-purpose |
| tester | general-purpose |
