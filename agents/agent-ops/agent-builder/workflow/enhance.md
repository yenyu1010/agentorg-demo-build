# 強化 Agent 工作流程

## Manager 輸入
```json
{
  "action": "enhance_agent",
  "agent": "agent-name",
  "enhancement_type": "skill | tool | principle | workflow_step",
  "description": "要新增或修改的內容",
  "reason": "為何需要此強化"
}
```

## 執行步驟

```
[1] （Manager 透過 scripts/worklog.sh 處理 worklog — agent 自身不寫 worklog）
  │
  ▼
[2] 讀取目標檔案
  根據 enhancement_type 判斷要修改哪個檔案：
    skill         → agents/{agent}/skills.md
    tool          → agents/{agent}/tools.md
    principle     → agents/{agent}/soul.md
    workflow_step → agents/{agent}/workflow.yaml
  │
  ▼
[3] 讀取分類原則
  確認強化內容不與其他 agent 產生職責重疊
  │
  ▼
[4] 套用變更
  編輯目標檔案：
    - 加入新內容，不改寫現有內容
    - 標記新增處：<!-- added {date}: {reason} -->
    - 若編輯後超過 ~60 行 → 拆成資料夾 + 路由器
  │
  ▼
[5] 驗證變更
  - 重新讀取已修改的檔案，確認編輯已正確套用
  - 確認檔案長度 <= ~60 行
  - 確認未引入職責重疊
  │
  ▼
[6] 自動化合規驗證（必須通過）
  執行 `bash scripts/validate-agent.sh {team}/{agent}` 對強化後的 agent 進行自動化結構驗證。

  規則：
  - 驗證結果必須為 PASS（零 FAIL）才可交付
  - 若有 FAIL 項目，返回對應步驟修正，然後重跑驗證
  - WARN 項目記錄但不阻擋交付
  - 驗證結果須附在回報給 Manager 的輸出中

  指令：bash scripts/validate-agent.sh {team}/{agent}
  │
  ▼
[7] （Manager 透過 scripts/worklog.sh 處理 worklog 結束）
  │
  ▼
回傳摘要給 Manager（須含驗證結果）
```
