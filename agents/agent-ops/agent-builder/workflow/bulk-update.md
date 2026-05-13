# 批次更新工作流程

## Manager 輸入
```json
{
  "action": "bulk_update",
  "targets": ["agent-name-1", "agent-name-2", "..."],
  "change_spec": "精確描述每個 agent 要新增或修改的內容",
  "target_file": "每個 agent 中要修改的檔案（例如 agent.yaml, skills.md）",
  "reason": "為何需要此批次變更"
}
```

## 執行步驟

```
[1] （Manager 透過 scripts/worklog.sh 處理 worklog）
  │
  ▼
[2] 讀取一個目標作為樣本
  讀取清單中第一個 agent 的 target_file。
  驗證 change_spec 是否適用（檔案存在、目標內容在場）。
  若樣本失敗 → 停止，向 Manager 回報。
  │
  ▼
[3] 規劃批次
  針對 targets 中的每個 agent：
    - 確認 target_file 存在
    - 記錄任何 agent 特有的差異（例如不同的 model、不同的 team）
  若 targets 超過 5 個 agent，先向 Manager 回報計劃並等待確認。
  │
  ▼
[4] 分批執行（每批最多 5 個 agent）
  針對目前批次中的每個 agent：
    - 讀取 target_file
    - 套用 change_spec（新增/修改內容）
    - 標記：<!-- bulk-update {date}: {reason} -->

  ### 每批次完成後驗證

  對本批次修改的每個 agent 執行 `bash scripts/validate-agent.sh {team}/{agent}`。
  任何 FAIL 項目必須在進入下一批次之前修正。

  回報批次完成（含驗證結果）後，再開始下一批。
  │
  ▼
[5] 驗證批次
  針對每個已修改的 agent：
    - 讀取已修改的檔案
    - 確認變更已正確套用
    - 標記任何看起來有誤的 agent
  │
  ▼
[6] 更新登錄表（若有需要）
  若批次更新新增了跨 agent 的關係，
  更新 CLAUDE.md 及受影響的 org.md 檔案。
  │
  ▼
[7] （Manager 處理 worklog 結束）
  │
  ▼
回傳批次更新摘要（成功數、失敗數、標記的 agent）
```

## 安全規則
- **每批最多 5 個 agent，避免上下文遺失**
- **每批完成後必須驗證，再進行下一批**
- **超過 10 個 agent 時：開始前先向 Manager 確認**
- **每次批次更新的編輯均需標記，確保可追溯**
