# Agent Builder Checklist

Run this before reporting completion. **ALL must pass.**

## For Create

### Structure

- [ ] `agents/{name}/` directory exists
- [ ] `agent.yaml` exists with all required fields (agent, title, team, reports_to, bootstrap, workflow, dispatch.model, dispatch.trigger, dispatch.not_for)
- [ ] `agent.yaml` bootstrap sequence includes soul.md, org.md, tools.md in that order
- [ ] `agent.yaml` dispatch.model is appropriate（參見 evaluation-protocol.md Haiku Eligibility）：
      - `haiku` **禁用**（2026-04-27 user policy: ban haiku；全 sonnet/opus）
      - `sonnet` 為預設（所有 researcher / reviewer / evaluator / designer / 審查類 一律 sonnet 起跳）
      - `opus` 用於複雜架構決策、關鍵審查、governance
- [ ] If `skills.md` exists, `agent.yaml` declares `skills: skills.md`
- [ ] Agent name is lowercase, hyphenated
- [ ] `worklog/.gitkeep` exists
- [ ] `memory/MEMORY.md` exists with agent-specific header

### README.md

- [ ] Has role (one sentence)
- [ ] Has "When to Dispatch" criteria
- [ ] Has dispatch config (subagent_type, model)

### soul.md

- [ ] Has unique identity (NOT copied from another agent)
- [ ] Has >= 3 principles specific to this domain
- [ ] Has "Anti-patterns to Avoid" section
- [ ] Has scope guard principle: agent knows what's NOT its job and will refuse (ref definitions.md Scope Guard)
- [ ] Has 打卡天條 principle: agent knows it MUST call `scripts/worklog.sh start` before work and `scripts/worklog.sh end` after work, failure = critical defect

### tools.md

- [ ] Has tool table (Tool | Purpose)
- [ ] Has **"Do NOT Use"** section with explicit prohibited tools
- [ ] Has usage guidelines
- [ ] Has **memory exception**: All agents (including read-only) MUST include `Write` exception for their own `memory/` directory
- [ ] **Permission whitelist**: 確認 agent 需要的 Bash 指令已加入 project settings.json 的 `permissions.allow`（如 `Bash(scripts/...)`, `Bash(python ...)`）。設定檔位置：`~/.claude/projects/{project}/settings.json`

### skills.md

- [ ] Has >= 3 domain-specific skills (NOT generic)
- [ ] Has **"NOT This Agent's Job"** section
- [ ] Skills are domain knowledge, not tool names (see definitions.md)

### workflow.yaml

- [ ] Is YAML format (not .md)
- [ ] Has `error_policy` block at top
- [ ] Does NOT have log_start/log_end steps (Manager handles worklog via scripts/worklog.sh)
- [ ] Has `check_memory` step
- [ ] Has `save_memory` step
- [ ] Every step that can fail has `on_error`
- [ ] Any `ref:` flow files follow the format defined in `workflow/flow-file-format.md` (Format A or B, ≥2 steps each)

### org.md

- [ ] Has complete hierarchy showing ALL agents (including Intent, Agent Builder)
- [ ] Has collaboration patterns
- [ ] Has **"When NOT to Pick This Agent"** section

### System Updates

- [ ] CLAUDE.md Agent Registry table updated
- [ ] `agents/agent-ops/manager/org.md` hierarchy updated
- [ ] Other agents' org.md updated if collaboration patterns change
- [ ] No file exceeds ~60 lines
- [ ] No domain overlap with existing agents (verified by reading all README.md + skills.md)
- [ ] Governance Agent has reviewed and approved the new agent (or creation is queued for review)

### Manager/Orchestrator Agents (if applicable)

- [ ] Workflow includes "Summary Worklog" as final step
- [ ] Summary worklog schema includes `dispatch_summary` field

## For Create Skill

- [ ] `.claude/skills/{name}/SKILL.md` exists
- [ ] Frontmatter has `name`, `description`, `allowed-tools: Glob Grep Read`
- [ ] Contains `$ARGUMENTS` placeholder
- [ ] Points to correct `target_manager_soul` path
- [ ] File is <= 15 lines (thin entry point only, no flow logic)
- [ ] Summary worklog schema includes `verification_results` field
- [ ] `dispatched_by` is set to `"user"` (not `"manager"`)

## For Enhance

- [ ] Target file was read before editing
- [ ] Change is marked with `<!-- added {date}: {reason} -->`
- [ ] Modified file was read back to verify edit applied
- [ ] No file exceeds ~60 lines after edit (split if needed)
- [ ] Enhancement stays within agent's existing domain
- [ ] No new domain overlap introduced
