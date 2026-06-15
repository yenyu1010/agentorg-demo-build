# Football Manager — Dispatch Protocol

所有 worker dispatch prompt 必須包含以下四個 Block，缺一不可。

## 1. Identity Block

```
You are the {AgentName} agent.

Bootstrap files (read in this order, absolute paths):
  /home/user/agentorg-demo-build/agents/football/{agent-name}/agent.yaml
  /home/user/agentorg-demo-build/agents/football/{agent-name}/soul.md
  /home/user/agentorg-demo-build/agents/football/{agent-name}/org.md
  /home/user/agentorg-demo-build/agents/football/{agent-name}/tools.md

Bootstrap once, then start workflow.
```

## 2. Worklog Block

```
WORKLOG: You must punch your own clock using scripts/worklog.sh.
  First action:  FILE=$(bash scripts/worklog.sh start football/{agent-name} sonnet "{summary}" manager "{trace_id}" "{parent_task_id}")
  Last action:   bash scripts/worklog.sh end "$FILE" completed "{output}"
  If you fail:   bash scripts/worklog.sh end "$FILE" failed "{error}"
```

## 3. Memory Block

```
MEMORY: Before starting, read agents/football/{agent-name}/memory/MEMORY.md.
Before finishing, save new learnings to agents/football/{agent-name}/memory/ per agents/protocols/memory-protocol.md.
```

## 4. Task Block

詳見 `workflow/dispatch-flow.md` 各 worker 的 Task Block 範本。

---

## Dispatch Order

| Round | Agents | 模式 | 前置條件 |
|-------|--------|------|---------|
| Round 1 | odds-analyst + form-analyst | 並行（run_in_background: true） | classify 完成 |
| verify_round1 | Manager 自執行 | inline | Round 1 兩者均完成 |
| Round 2 | value-modeler | 串行（run_in_background: false） | verify_round1 通過 |

## 快速參照

| Worker | Bootstrap 根路徑 |
|--------|----------------|
| odds-analyst | `/home/user/agentorg-demo-build/agents/football/odds-analyst/` |
| form-analyst | `/home/user/agentorg-demo-build/agents/football/form-analyst/` |
| value-modeler | `/home/user/agentorg-demo-build/agents/football/value-modeler/` |
