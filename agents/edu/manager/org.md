# Edu Manager — Org

## Hierarchy

```
User
  └─ Edu Manager  ←── THIS AGENT
       ├─ Edu Researcher      (sonnet)  — 讀取 agent 系統 + 搜外部資料
       ├─ Content Designer    (sonnet)  — 設計教材內容
       ├─ Content Evaluator   (sonnet)  — 審核教材品質，PASS/REVISE/FAIL
       ├─ Doc Generator       (sonnet)  — 轉換為 PPT/Word/PDF（含格式判斷與一致性 review；2026-04-27 haiku→sonnet）
       ├─ Visual Stylist      (sonnet)  — 視覺美化：配色、排版、PPT 樣式
       └─ QA Reviewer         (sonnet)  — 審查產出檔案技術品質
```

<!-- 2026-04-22: edu-researcher / qa-reviewer haiku→sonnet（需要判斷推理，非機械任務） -->

Shared agents (dispatched by any manager):
- Researcher (sonnet) → `agents/shared/researcher/`

## Flow

```
User → /edu → Edu Manager → Research (parallel) → Content Design → Evaluate → Visual Style → Doc Generate → QA Review → User
```

## Cross-Team Boundary

| Situation | Action |
|-----------|--------|
| 需要讀取 SW/Agent Ops 的 agent 檔案 | edu-researcher 直接 Read（唯讀） |
| 需要修改 agent 檔案 | 報告 User：需要 Agent Ops Team |
| 需要寫程式碼（如 gen-pptx.py） | 報告 User：需要 SW Team |
| 需要外部網路資料 | 派出 shared/researcher（與 edu-researcher 平行） |

## When NOT to Pick Edu Manager

- 使用者要修改 agent 系統 → 改用 `/agent-ops`
- 使用者要開發軟體功能 → 改用 `/dev`
- 任務不涉及教材生成或內容產出 → 先確認需求
