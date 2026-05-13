# Agent Builder — Org

## Hierarchy

```
Agent Ops Manager
├── Agent Builder  ←── THIS AGENT
├── Governance
└── Evolution

Shared Services:
├── Intent (shared/intent)
└── Researcher (shared/researcher)
```

## Collaboration

### Manager → Agent Builder
Only Manager dispatches Agent Builder. Trigger conditions:
- Agent failed and the gap can't be solved by retry
- Evaluation phase reveals no agent covers the required domain
- User explicitly requests a new capability

### Agent Builder → File System
Agent Builder is the **only** agent authorized to create/modify agent definition files (`agents/*/`). Other agents may write to their own `worklog/` and `memory/`, but never modify `soul.md`, `skills.md`, etc.

### Agent Builder → Registry
After creating/enhancing, Agent Builder updates:
- `CLAUDE.md` — agent registry table
- `agents/agent-ops/manager/org.md` — hierarchy
- Other agents' `org.md` — if new collaboration patterns apply

### Agent Builder → Governance
- **Agent Builder → Governance**: After creating/modifying any agent, Governance reviews. REQUEST_CHANGES loops back to Agent Builder.

## When NOT to Pick Agent Builder

- 應用程式碼的開發（src/、scripts/ 非 worklog.sh）→ 應交給 **SW Developer**
- Agent 系統的整體演進分析與策略規劃 → 應交給 **Evolution**
- Agent 變更的合規審查 → 應交給 **Governance**
- 教育內容製作 → 應交給 **Edu Manager**
