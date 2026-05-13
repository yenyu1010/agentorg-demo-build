### classify（dispatch shared/intent）

委派 shared/intent agent 進行任務分類。Manager 不自行分析。

**Dispatch:**
- Agent: shared/intent
- Model: sonnet（一致性優先；2026-04-27 user policy: ban haiku）
- Input: 用戶原始請求

**Expected Output:** `intent_result`
```json
{
  "task_type": "query | create | modify | delete | analyze",
  "target_agent": "目標 agent（若識別到）",
  "target_files": ["可能影響的檔案"],
  "risk_level": "none | lightweight | full_review",
  "dispatch_plan": ["建議派遣的 agent 列表"]
}
```

**on_error:** Manager 自行 inline 分類（fallback）
