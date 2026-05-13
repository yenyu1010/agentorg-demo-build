<!-- 2026-04-27: Identity Block updated with explicit bootstrap paths (rollout from agent-anatomy.md §6.7) -->
# Edu Manager — Dispatch Protocol

When dispatching each worker agent, include ALL of the following blocks in the prompt:

## 1. Identity Block

```
You are the {AgentName} agent.

Bootstrap files (read in this order, absolute paths):
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/edu/{agent-name}/agent.yaml
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/edu/{agent-name}/soul.md
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/edu/{agent-name}/org.md
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/edu/{agent-name}/tools.md

Bootstrap once, then start workflow.
```

For shared/researcher:
```
You are the Researcher agent.

Bootstrap files (read in this order, absolute paths):
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/shared/researcher/agent.yaml
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/shared/researcher/soul.md
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/shared/researcher/org.md
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/shared/researcher/tools.md

Bootstrap once, then start workflow.
```

## 2. Worklog Block

```
WORKLOG: You must punch your own clock using scripts/worklog.sh.
  First action:  FILE=$(bash scripts/worklog.sh start edu/{agent-name} {model} "{summary}" manager "{trace_id}" "{parent_task_id}")
  Last action:   bash scripts/worklog.sh end "$FILE" completed "{output}"
  If you fail:   bash scripts/worklog.sh end "$FILE" failed "{error}"
```

NOTE:
- dispatched_by 固定為 "manager"（Manager 自己打卡時傳 "user"，並省略 trace_id/parent_task_id，系統會自動生成 trace_id）。
- `{trace_id}` = Manager 自己的 trace_id（從 Manager 的 worklog JSON 讀取）。
- `{parent_task_id}` = Manager 自己的 task_id（從 Manager 的 worklog JSON 讀取）。

## 3. Memory Block

```
MEMORY: Before starting, read agents/edu/{agent-name}/memory/MEMORY.md.
Before finishing, save new learnings to agents/edu/{agent-name}/memory/ per agents/protocols/memory-protocol.md.
```

## 4. Task Block

| Field | Description |
|-------|-------------|
| `goal` | 任務目標 |
| `topic` | 教材主題 |
| `audience_profile` | executive \| developer \| power-user |
| `output_format` | xlsx \| docx \| pptx（pdf 為次要選項，使用者明確要求時才產出） |
| `research_context` | 上一步 agent 回傳的結果（非第一步則必填） |
| `language` | 使用者語言 |
| `output_path` | **必填**。Manager 在 `session_init` 步驟建立的絕對路徑（典型 `$CLAUDE_PROJECT_DIR/output/edu/{task_id}/`）。Worker 所有產物寫入此路徑。詳見 `agents/protocols/rules/output-placement.md` |
| `task_id` | **必填**。格式 `{topic_short}-{YYYYMMDD}`，例：`agent-training-20260422` |
| `session_dir` | 同 `output_path`（保留相容名稱，edu team 內部術語） |

> ⚠️ 若 Manager 漏傳 `output_path`，Worker 必須立即回報 `SCOPE VIOLATION: missing output_path` 並停工；不得自行寫入 agent 資料夾。

## 5. Language Block

```
LANGUAGE: Respond in {user's language}.
```

## Dispatch Order

| Step | Agents | Parallel? | Input | Output |
|------|--------|-----------|-------|--------|
| session_init | Manager 自執行 | 否（強制首步） | (無) | output_path + task_id |
| Research | edu-researcher + shared/researcher | 平行（同時派出） | parsed_request + output_path + task_id | research_results |
| Design | content-designer | 否（等 Research 完成） | research_results + parsed_request + output_path + task_id | content_draft |
| Evaluate | content-evaluator | 否（等 Design 完成） | content_draft + output_path + task_id | verdict |
| Visual Styling | visual-stylist | 否（等 Evaluate PASS） | evaluated_content + output_path + task_id | style_guide |
| Generate | doc-generator | 否（等 Visual Styling 完成） | content_draft + output_format + output_path + task_id | files |
| QA | qa-reviewer | 否（等 Generate 完成） | generated_files + output_path + task_id | verdict |
