# Memory Protocol

Each agent has a persistent memory at `agents/{team}/{agent}/memory/`. This memory survives across sessions and helps the agent avoid repeating mistakes or re-discovering known facts.

## What to Remember

| Category | Example |
|----------|---------|
| **Codebase patterns** | "This project uses Zustand for state management, not Redux" |
| **User preferences** | "User prefers functional components over class components" |
| **Lessons learned** | "The test database needs to be reset between integration tests" |
| **Known issues** | "Build fails on Node 18 due to native module incompatibility" |
| **Decisions made** | "Chose PostgreSQL over SQLite for the session store (decision date: 2026-04-13)" |
| **User feedback** | "用戶說程式碼缺少錯誤處理 → 下次 dispatch 時明確要求" |

## What NOT to Remember

- Raw worklog data (that goes in worklog/)
- Temporary debugging state
- Information already in the codebase itself

## Memory File Format

Save each memory as a separate `.md` file in `agents/{team}/{agent}/memory/`:

```markdown
---
topic: {descriptive topic}
created: {ISO date}
agent: {agent-name}
---

{Content of the memory — keep it concise and actionable}
```

## MEMORY.md Index

Each agent has a `agents/{team}/{agent}/memory/MEMORY.md` index file. When adding a new memory, append a one-line entry:

```markdown
- [{Topic}]({filename}.md) — {one-line summary}
```

## Feedback Memory（用戶回饋觸發）

當用戶對 agent 產出表達正面或負面回饋時，Manager/Director/Officer 必須自動保存 feedback memory。

詳細規則見 `agents/protocols/rules/feedback-memory.md`。

### 回饋偵測觸發關鍵語意
- **負面**：錯了、寫得很爛、重來、不對、太差、不是我要的
- **正面**：很好、不錯、讚、正確、完美、繼續這樣做

### Feedback Memory 格式
保存到 `memory/feedback-{YYYY-MM-DD}-{seq}.md`，必含：
- 用戶原話
- 當時任務
- 分析（為什麼）
- 教訓（下次怎麼做）

## Instructions for Agent Manager

When dispatching an agent, include:

```
MEMORY: Before starting work, check agents/{team}/{agent}/memory/MEMORY.md for
relevant prior knowledge. Before finishing, save any new learnings worth
retaining to agents/{team}/{agent}/memory/ following agents/protocols/memory-protocol.md.
```

## 打卡後 Memory Check（強制）

所有 Manager 在 `log_end`（打卡結束）**之後**，必須執行 `memory_check` 步驟：

1. 回顧本輪任務中是否有以下任一情況：
   - 用戶糾正/回饋（語句含「不對」「搞錯」「應該是」「不是這樣」等）
   - 審查結果（Evolution/Governance/QA 的發現）
   - 新學到的 lesson（工具用法、概念釐清、流程改善）
   - 跨 team 影響的決策

2. 若有，立即：
   - 寫入 `agents/<team>/<agent>/memory/` 目錄（一個 .md 檔 per entry）
   - 更新 `MEMORY.md` 索引

3. 若無新 memory，不做任何事（不產出空檔案）。

**違反此規則 = memory protocol 違規，等同打卡違規。**
