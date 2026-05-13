# Lawyer Manager — Dispatch Protocol

When dispatching each worker agent, include ALL of the following blocks in the prompt:

## 1. Identity Block

```
You are the {AgentName} agent.

Bootstrap files (read in this order):
  <ROOT>/agents/lawyer/{agent-name}/agent.yaml
  <ROOT>/agents/lawyer/{agent-name}/soul.md
  <ROOT>/agents/lawyer/{agent-name}/org.md
  <ROOT>/agents/lawyer/{agent-name}/tools.md

Bootstrap once, then start workflow.
```

## 2. Worklog Block

```
WORKLOG: You must punch your own clock using scripts/worklog.sh.
  First action:  FILE=$(bash scripts/worklog.sh start lawyer/{agent-name} sonnet "{summary}" manager "{trace_id}" "{parent_task_id}")
  Last action:   bash scripts/worklog.sh end "$FILE" completed "{output}"
  If you fail:   bash scripts/worklog.sh end "$FILE" failed "{error}"
```

## 3. Memory Block

```
MEMORY: Before starting, read agents/lawyer/{agent-name}/memory/MEMORY.md.
Before finishing, save new learnings to agents/lawyer/{agent-name}/memory/ per agents/protocols/memory-protocol.md.
```

## 4. Task Block

| Field | Description |
|-------|-------------|
| `goal` | 任務目標 |
| `case_type` | 案件類型 |
| `jurisdiction` | 適用法域（預設台灣） |
| `output_path` | **必填**。Manager 建立的絕對路徑 |
| `task_id` | **必填**。格式 `{case_short}-{YYYYMMDD}` |
| `language` | 使用者語言 |

## Dispatch Order

| Step | Agents | Parallel? |
|------|--------|-----------|
| Case Analysis | case-analyzer | 否 |
| HITL Gate 1 | Manager 自執行 | 否 |
| Law Research | law-researcher + shared/researcher | 平行 |
| Risk Assessment | risk-assessor | 否 |
| HITL Gate 2 | Manager 自執行 | 否 |
| Doc Generation | doc-generator | 否 |
