# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Demo Scope

This is a **portable demo** of the AgentOrg multi-agent orchestration system. It contains two teams:

- `agents/agent-ops/` — Agent system management
- `agents/edu/` — Educational content production

The full system has additional teams (sw, sales, bni, finance, platform) that are intentionally NOT shipped here.

`agents/protocols/definitions.md` may reference those missing teams — those references are documentary only and do not block execution of agent-ops or edu work.

## Quick Setup

See `INSTALL.md` for step-by-step setup with troubleshooting. TL;DR:

1. Copy this folder to a stable path (e.g. `C:\AgentOrg-Demo\` or `~/AgentOrg-Demo/`)
2. Open Claude Code with cwd set to this folder — `/tuq-edu` and `/tuq-agent` auto-load
3. Optional: `bash scripts/setup-global-skills.sh` for global skill access from any folder
4. Install Python deps: `pip install python-pptx python-docx Pillow`

## Architecture Overview

**AgentOrg** is a multi-agent orchestration system. A Manager agent receives user requests, decomposes them, and dispatches specialized worker agents.

### Core Concepts

- **Agent**: An autonomous Claude instance with a defined role, domain expertise (skills), system capabilities (tools), and personality (soul)
- **Manager**: The entry point. Decomposes requests, selects agents, dispatches work in parallel, synthesizes results
- **Tool**: System capability (Read, Write, Edit, Bash, Grep, Glob, Agent, WebSearch, WebFetch)
- **Skill**: Domain knowledge pattern — how to combine tools to solve domain-specific problems
- **Scope Guard**: Every agent must refuse work outside its domain

### Teams (in this demo)

```
AgentOrg-Demo/
├── agents/agent-ops/        # Agent system management
│   ├── manager/             # Orchestrates all agent ops work
│   ├── agent-builder/       # Create and modify agents
│   ├── governance/          # Policy and oversight
│   └── evolution/           # Evolve agent capabilities
├── agents/edu/              # Education / content team
│   ├── manager/
│   ├── edu-researcher/      # Research educational topics
│   ├── content-designer/    # Design educational content structure
│   ├── content-evaluator/   # Evaluate and improve content
│   ├── doc-generator/       # Generate documentation (pptx / docx)
│   ├── visual-stylist/      # Visual design and presentation
│   └── qa-reviewer/         # Quality assurance for content
└── agents/protocols/        # Shared protocols (worklog, memory, scope guard, ...)
```

## Agent Anatomy

Every agent directory contains:

| File | Purpose | Editable By |
|------|---------|------------|
| `agent.yaml` | Agent entry point — bootstrap sequence, dispatch model, trigger rules | Agent Builder only |
| `README.md` | Dispatch rules — when/how to use this agent | Agent Builder only |
| `soul.md` | Personality, principles, anti-patterns | Agent Builder only |
| `tools.md` | System capabilities granted to this agent | Agent Builder only |
| `skills.md` | Domain expertise patterns | Agent can add new skills; removing/modifying requires approval |
| `org.md` | Organizational role and reporting | Agent Builder only |
| `workflow.yaml` | Execution workflow steps (skeleton router, each step refs a flow file) | Agent can add steps; removing/modifying requires approval |
| `memory/` | Persistent agent memory (markdown files) | Agent can read/write |
| `workflow/` | Detailed step-level flow definitions (`XXX-flow.md`) | Agent can read/add; modifying existing requires approval |
| `worklog/` | Timestamped execution logs (JSON) | Agent creates after each run |

## Self-Update Rules

**Cardinal Rule**: 加法自己來，減法和擴權要審批 (Addition is self-serve, subtraction and privilege expansion require approval)

### What Agents Can Do Alone
- Write to `worklog/` — create new timestamped execution log
- Read/write `memory/` — store and recall learned patterns
- **Add** new skills to `skills.md` — mark with `<!-- self-added {date} -->`
- **Add** new steps to `workflow.yaml` — mark with `# self-added {date}`

### What Requires Agent Builder Approval
- **Delete** from `skills.md`
- **Modify** `tools.md`, `soul.md`, `org.md`, `README.md`, `agent.yaml`
- **Delete/modify** existing steps in `workflow.yaml`

## Scope Guard Pattern

When an agent receives out-of-scope work, it MUST refuse:

```
SCOPE VIOLATION: This task belongs to {correct_agent}, not {self}.
Reason: {why this is out of scope}
Recommended agent: {correct_agent}
```

## Worklog Requirement (天條 — Sacred Rule)

Every agent **must** log work:
- **Before starting**: `bash scripts/worklog.sh start ...`
- **After completing**: `bash scripts/worklog.sh end ...`
- **Failure to log**: Treated as task failure

Worklogs land in `agents/{team}/{agent}/worklog/{timestamp}_{agent}.json`.

## Dispatch Entry Points

In this demo there are **four** entry skills:

- `/S33-edu` — All edu / content / training material work
- `/S33-agent` — All agent system modification (create / edit / govern agents)
- `/S33-lawyer` — All legal, contract, compliance and risk analysis work
- `/S33-engineer` — All software development, bug fix, refactoring and IT technical questions

Type any of these in Claude Code with cwd set to this folder.

## Key Protocols

| Protocol | File |
|----------|------|
| Definitions | `agents/protocols/definitions.md` |
| Worklog | `agents/protocols/worklog-protocol.md` |
| Memory | `agents/protocols/memory-protocol.md` |
| Verification | `agents/protocols/verification-protocol.md` |
| HITL | `agents/protocols/hitl-protocol.md` |
| Agent Anatomy | `agents/protocols/rules/agent-anatomy.md` |
| Self-Growth | `agents/protocols/rules/self-growth.md` |

## Common Conventions

- **Language**: Most agents operate in 繁體中文 with English code/file names
- **Timestamps**: ISO 8601 in worklogs and memory
- **No executable code in `soul.md`**: Soul files describe behavior, not scripts
- **Output placement**: When called from outside the project, agents write to `tuq_log/output/` in the caller's cwd

## 市場估價類問題強制流程（self-added 2026-05-17）

**教訓來源**：回答台北中山區渭水路房產估價時，未查詢實價登錄數據，直接用訓練記憶給出 47–52 萬/坪，實際成交行情為 73–79 萬/坪，低估約 40%，屬嚴重失誤。

**任何涉及「現在值多少錢」的問題，必須執行以下流程，缺一不可：**

1. **先搜尋，再開口** — 使用 WebSearch 查詢實價登錄、5168、樂屋網等平台的路段成交數據；禁止用訓練資料印象直接給價格數字
2. **驗證微地段** — 地址 → 最近捷運站 → 商圈定性；不能只看行政區，要查具體街廓與周邊地標
3. **找至少 3–5 筆實際成交案例** — 列出成交時間、坪數、單價、來源；同類型（屋齡、產品型態）優先
4. **用比較法做系統性調整** — 屋齡、樓層、坪數、朝向、屋況、車位，每個因子要有數值依據
5. **標示資料來源** — 每個關鍵數字說明出處；若無法搜尋，必須明說「以下為記憶估算，需實際查證」

**禁止行為**：
- 不查詢直接給單價範圍
- 用行政區均價套用於特定街廓（如忠孝新生站商圈 ≠ 中山區整體）
- 把開價（掛牌價）當成交價引用

## Bash Execution Rule (Strict)

**Do NOT** run `for`, `while`, `find`, or multi-line inline scripts directly in Bash tool calls.

For batch operations, **first** write the logic into `.sh` or `.js` under `.claude/scripts/`, **then** run with `bash .claude/scripts/your_script.sh`.

This prevents permission interception that aborts execution.
