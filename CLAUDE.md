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

## Bash Execution Rule (Strict)

**Do NOT** run `for`, `while`, `find`, or multi-line inline scripts directly in Bash tool calls.

For batch operations, **first** write the logic into `.sh` or `.js` under `.claude/scripts/`, **then** run with `bash .claude/scripts/your_script.sh`.

This prevents permission interception that aborts execution.
