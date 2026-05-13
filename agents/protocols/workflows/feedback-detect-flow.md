# 回饋偵測流程（Feedback Detection Flow）

## 適用角色
Manager (L2)、Director (L3)、Officer (L4)

## 觸發時機
在 classify 步驟中執行，或作為獨立的 feedback_detect 步驟在 classify 之前執行。

## 執行步驟

```
[1] 掃描用戶訊息語意
  │
  ├─ 偵測負面回饋語意
  │   關鍵詞/語意：錯了、寫得很爛、重來、不對、太差、不是我要的、
  │               terrible, wrong, redo, not what I wanted
  │
  ├─ 偵測正面回饋語意
  │   關鍵詞/語意：很好、不錯、讚、正確、完美、繼續這樣做、
  │               great, correct, perfect, keep it up
  │
  └─ 中性（無回饋語意）→ 跳到正常流程
  │
  ▼
[2] 保存 Feedback Memory
  檔案：agents/{team}/{agent}/memory/feedback-{YYYY-MM-DD}-{seq}.md
  格式：
    ---
    topic: user-feedback
    created: {ISO date}
    agent: {agent-name}
    trigger: user_feedback
    sentiment: positive | negative
    ---
    ## 用戶原話
    > "{用戶訊息}"
    ## 當時任務
    {上一次任務的摘要，可從最新 worklog 取得}
    ## 分析
    {為什麼用戶這樣說}
    ## 教訓
    {正面：繼續什麼做法 / 負面：下次怎麼改}
  │
  ▼
[3] 更新 MEMORY.md 索引
  在 memory/MEMORY.md 追加一行：
  - [user-feedback-{date}](feedback-{date}-{seq}.md) — {sentiment}: {一句話摘要}
  │
  ▼
[4] 回覆用戶確認
  - 負面回饋 → "已記錄您的回饋，我會在後續工作中改進。" + 若有後續任務則繼續執行
  - 正面回饋 → "感謝回饋，已記錄成功做法。" + 若有後續任務則繼續執行
  │
  ▼
[5] 繼續正常 workflow（classify → execute → ...）
```

## 回饋聚合檢查（Background Dispatch）

每次保存 feedback memory 後，Manager 應以 background 方式派遣 agent 進行聚合檢查，不阻斷用戶的主任務：

```yaml
- id: feedback_aggregate
  action: dispatch_agent
  agent: self  # Manager 自行處理，或委派給 Evolution
  run_in_background: true
  prompt: |
    掃描 memory/ 目錄中的 feedback-*.md 檔案。
    若同類回饋 ≥ 3：
      1. 合併為 pattern memory
      2. 考慮升級為 skill（依 memory-hygiene.md §7）
    若不足 3 → 無動作
```

**重要**：`run_in_background: true` 確保用戶任務不被阻斷。聚合結果靜默寫入 memory/，下次任務時自動生效。

## 備註
- 語意偵測不限於精確關鍵字，應理解上下文（如「這什麼東西」= 負面）
- 回饋保存失敗不應阻斷正常流程（on_error: continue）
- 此 flow 由 `agents/protocols/rules/feedback-memory.md` 定義規則
