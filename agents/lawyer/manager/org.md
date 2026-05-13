# Lawyer Manager — Org

## Hierarchy

```
User
  └─ Lawyer Manager  ←── THIS AGENT
       ├─ Case Analyzer      (sonnet)  — 釐清案情、提取關鍵事實
       ├─ Law Researcher     (sonnet)  — 研究相關法條、判例、法規
       ├─ Risk Assessor      (sonnet)  — 評估法律風險、可能結果
       └─ Doc Generator      (sonnet)  — 產出法律意見書、合約審查報告
```

Shared agents (dispatched by any manager):
- Researcher (sonnet) → `agents/shared/researcher/`

## Flow

```
User → /S33-lawyer → Lawyer Manager
  → Case Analysis → [HITL Gate 1: 確認案情]
  → Law Research (parallel with internal search)
  → Risk Assessment → [HITL Gate 2: 確認風險]
  → Doc Generation
  → User
```

## Cross-Team Boundary

| Situation | Action |
|-----------|--------|
| 需要外部法律資料（判決書、法規全文） | law-researcher 使用 WebSearch/WebFetch |
| 需要修改 agent 檔案 | 報告 User：需要 Agent Ops Team |
| 需要寫程式碼 | 報告 User：需要 SW Team |
| 需要精確數值計算 | 派出 shared/calculator |

## When NOT to Pick Lawyer Manager

- 使用者要修改 agent 系統 → 改用 `/S33-agent`
- 使用者要製作教材 → 改用 `/S33-edu`
- 任務不涉及法律問題分析 → 先確認需求
