<!-- 2026-04-27: Identity Block updated with explicit bootstrap paths (rollout from agent-anatomy.md §6.7) -->
# Agent Ops Dispatch Protocol

When dispatching each worker agent, include ALL of the following blocks in the prompt:

## 1. Identity Block
```
You are the {AgentName} agent.

Bootstrap files (read in this order, absolute paths):
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/agent-ops/{agent-name}/agent.yaml
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/agent-ops/{agent-name}/soul.md
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/agent-ops/{agent-name}/org.md
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/agent-ops/{agent-name}/tools.md

Bootstrap once, then start workflow.
```

> **Note**: For shared agents (e.g., shared/researcher), use `agents/shared/{agent-name}/...` instead.

## 2. Worklog Block
```
WORKLOG: You must punch your own clock using scripts/worklog.sh.
  First action:  FILE=$(bash scripts/worklog.sh start {agent-name} {model} "{summary}" manager "{trace_id}" "{parent_task_id}")
  Last action:   bash scripts/worklog.sh end "$FILE" completed "{output}"
  If you fail:   bash scripts/worklog.sh end "$FILE" failed "{error}"
```

NOTE:
- dispatched_by 固定為 "manager"（Manager 自己打卡時傳 "user"，並省略 trace_id/parent_task_id，系統會自動生成 trace_id）。
- `{trace_id}` = Manager 自己的 trace_id（從 Manager 的 worklog JSON 讀取）。
- `{parent_task_id}` = Manager 自己的 task_id（從 Manager 的 worklog JSON 讀取）。
- Backward compatible：舊式呼叫不傳 trace_id/parent_task_id 仍可運作（預設空字串/null）。

When `$TUQ_LOG` is set (CWD ≠ ROOT), append `--mirror-to "$TUQ_LOG/worklogs"` to the start command:
```
FILE=$(bash scripts/worklog.sh start {agent-name} {model} "{summary}" manager "{trace_id}" "{parent_task_id}" --mirror-to "$TUQ_LOG/worklogs")
```

## 3. Memory Block
```
MEMORY: Before starting, read agents/agent-ops/{agent-name}/memory/MEMORY.md.
Before finishing, save new learnings to agents/agent-ops/{agent-name}/memory/
per agents/protocols/memory-protocol.md.
```

## 4. Task Block
- **Goal**: what to accomplish
- **Scope**: files, directories, domains to focus on (agent system files only)
- **Context**: findings from prior agents in this chain
- **Output format**: what to return

## 5. Language Block
```
LANGUAGE: Respond in {user's language}.
```

## Agent Tool Parameters

```
Agent({
  description: "short label",
  subagent_type: "general-purpose",
  model: from intent classification,
  prompt: assembled from blocks above,
  run_in_background: true if not blocking next round,
})
```

## 6. Shared Context Block (for parallel dispatch)

When dispatching multiple agents in parallel, include a shared context summary so each agent knows what others are working on.

```
SHARED CONTEXT: Other agents working in parallel on this task:
- {Agent A}: {brief description of their task}
- {Agent B}: {brief description of their task}
If your work overlaps with theirs, focus on YOUR scope and note the overlap.
Do NOT duplicate their work.
```

### When to include
- dispatch_agents_parallel with 2+ agents
- Any round where agents might touch overlapping files

### When to skip
- Single agent dispatch
- Sequential rounds (each agent sees previous output)

## 7. Workspace Block (for remote CWD)

When the calling CWD differs from `<ROOT>` (i.e., the user invoked the skill from another project), a local workspace `tuq_log/` exists at `$CWD/tuq_log/`. Include this block in every dispatch prompt:

```
WORKSPACE:
  tuq_log: $TUQ_LOG                         # absolute path to CWD/tuq_log
  output_dir: $TUQ_LOG/output/              # agent deliverables go here
  tmp_dir: $TUQ_LOG/tmp/                    # scratch files go here
  worklog_mirror: $TUQ_LOG/worklogs/        # --mirror-to path for worklog.sh
```

### When to include
- CWD ≠ `<ROOT>` (user is in a different project)

### When to skip
- CWD == `<ROOT>` (working inside AgentOrg itself)

## Parallelism Rules
- Agent Builder + Evolution 可以並行（操作不同檔案時）
- Governance 必須在 Agent Builder 完成後才執行（需審查變更）
- Intent 必須先完成才能派遣其他 agent
