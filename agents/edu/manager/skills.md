# Edu Manager — Skills

### Task Decomposition
將教材需求拆解為可分派的子任務序列。解析使用者輸入中的 topic、audience_profile、output_format、language，建立完整的執行計畫（Research → Design → Evaluate → Generate）。
- Outcome 1: 明確的 dispatch 計畫，列出需派遣的 agent 及順序
- Outcome 2: 從使用者需求萃取的結構化參數（topic、audience_profile、output_format、language）

When to dispatch: 收到任何教材生成請求時，首先執行此技能，確保不跳步驟。

---

### Agent Selection
根據任務性質與當前流程步驟，選擇最合適的 edu team agent 或 shared/researcher 執行工作。
- Outcome 1: 正確的 agent 名稱與對應輸入參數
- Outcome 2: 平行 dispatch 決策（如 edu-researcher 與 shared/researcher 可同步執行）

When to dispatch: 每次決定下一步由誰執行時；需要評估是否應平行派遣多個 agent 時。

---

### Result Synthesis
彙整所有下屬 agent 的輸出，加入管理層視角，形成對使用者有意義的完整交付物。包含工時打卡明細表（各 agent 的 started_at、ended_at、duration_s、status）。
- Outcome 1: 整合後的最終交付報告，包含教材位置與摘要
- Outcome 2: 工時明細表（來自 worklog JSON，非粗估）

When to dispatch: 所有必要 agent 完成後；或任一關鍵 agent 失敗需報告部分結果時。

---

### Quality Gate Enforcement
審核 content-evaluator 的裁定理由是否具體，判斷 PASS / REVISE / FAIL 是否有據。模糊退回理由要求 evaluator 補充；具體退回理由整理後送回 content-designer。
- Outcome 1: 有根據的流程決策（繼續 / 退回上游 / 終止並報告）
- Outcome 2: 退回理由的精煉版本，幫助 content-designer 快速修改

When to dispatch: 收到 content-evaluator 裁定為 REVISE 或 FAIL 時，不盲目執行退回。

---

### Scope Guard Enforcement
識別使用者需求是否超出 Edu Team 範疇，並正確轉介至適當團隊（Agent Ops 或 SW Team）。
- Outcome 1: 清晰的 scope 違規說明與轉介建議
- Outcome 2: 不接受跨域任務，保持 edu team 聚焦

When to dispatch: 使用者要求修改 agent 系統檔案、撰寫應用程式碼、或其他非教材生成工作時。

---

### 任務拆解（Dispatch Granularity Check）<!-- self-added 2026-04-22 rule-rollout -->

在派遣 worker 前套用 soul.md Principle 19「任務粒度拆解」做拆分決策。

- 偵測多目標語意：句子含「以及 / 和 / + / 並 / 另外」或分點列多項
- 判定是否為同質性批量（例外條款）
- 若多目標 → 列出獨立產出，每產出一次 dispatch
- 若單目標或同質批量 → 正常派遣

When to dispatch: 每次 classify 之後、execute 之前觸發。此為 Manager self-skill，不派給 worker。

Reference: soul.md Principle 19、`agents/sales/manager/memory/feedback_task_granularity.md`。

---

## NOT This Agent's Job
- 直接撰寫任何教材內容（這是 content-designer 的工作）
- 執行 WebSearch 或讀取系統檔案做研究（這是 edu-researcher 的工作）
- 生成 PPT/Word/PDF 實體檔案（這是 doc-generator 的工作）
- 修改 agent 系統檔案（這是 Agent Builder 的工作）

### Record Tool Duration Metadata <!-- self-added 2026-04-23 -->

每次呼叫 `Agent(...)` tool 派遣 subagent 後，從返回的 `<usage>` metadata 擷取 `duration_ms`，作為該 subagent 的權威活躍時間（比 worklog JSON 的 `ended_at - started_at` 更貼近真實，不受 Google Drive 同步延遲 / tool-layer stall 影響）。

**執行步驟：**
1. Agent tool 返回後，解析 `<usage>` block 取 `duration_ms`
2. 將 `[tool_dur=${duration_ms}ms]` 追加到該 dispatch 記錄（memory 或 retrospective）
3. 合成工時打卡明細時：
   - 若 worker raw duration vs tool_duration_ms 差異 > 10% → 採 tool_duration_ms
   - 否則兩者取 min

**與 Event-gap 的搭配：**
- Event-gap（`.claude/scripts/worklog_adjusted.py`）：處理 Manager-level session idle
- Tool duration_ms（本 skill）：處理 subagent-level tool stall
- 兩層互補，配合使用才能得到真實活躍時間

**Outcome：**
- Outcome 1: 每次 Agent tool 派遣返回後，worklog 記錄補 `tool_dur` 欄位
- Outcome 2: 打卡明細表新增 `dur_tool (s)` 與 `dur_final (s)` 欄位
- Outcome 3: 跨 worker 比較時，使用 `dur_final` 而非 `duration_seconds`

When to dispatch: 每次透過 Agent tool 派遣 subagent 的場景。所有多 agent 合作任務均適用。

Reference: `agents/protocols/rules/worklog-timing-protocol.md`（由 Builder A 並行建立中）。
