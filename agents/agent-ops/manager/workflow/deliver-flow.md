### Step 1: worklog_summary（manager_self）

讀取所有被派遣 agent 的 worklog JSON，產出打卡明細表：

```
| Agent | input_summary | output_summary | started_at | ended_at | duration_s | status |
|-------|---------------|----------------|------------|----------|------------|--------|
| **總計** | {N} agents | | | | {total}s | {pass}/{fail} |
```

- 時間必須來自 worklog JSON 實際時間戳，不得粗估
- 缺 worklog 或 failed 的 agent 標註原因

**on_error:** skip_table（繼續回覆，但不附打卡表）

---

### Step 2: respond_to_user（manager_self）

將 synthesize 結果與 worklog_summary 表合併，以用戶語言回覆。

**on_error:** respond_partial（用現有資料回覆，說明有部分資料缺失）
