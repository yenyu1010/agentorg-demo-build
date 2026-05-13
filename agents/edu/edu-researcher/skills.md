# Edu Researcher — Skills

### Internal System File Extraction
系統性讀取 agent 系統相關檔案（soul.md、workflow.yaml、org.md、skills.md、README.md 等），萃取教材所需的結構化資料。忠實呈現檔案內容，不添加推測或個人詮釋。
- Outcome 1: 結構化的系統知識摘要（JSON 或 Markdown 格式），涵蓋架構關係、角色定義、流程步驟
- Outcome 2: 每個資料點的來源引用（檔案路徑 + 行號），確保可追溯

When to dispatch: 教材主題涉及 agent 系統內部架構、流程或配置時；content-designer 需要準確的系統資料時。

---

### External Knowledge Research
使用 WebSearch 與 WebFetch 搜尋教材主題的最新外部資料（技術文件、最佳實踐、業界案例），並與內部系統資料並列呈現。
- Outcome 1: 外部資料摘要（來源 URL、發布日期、核心重點），與內部資料區隔標示
- Outcome 2: 內外部資料的異同對照，標記哪些外部最佳實踐在內部系統中已實現或有落差

When to dispatch: 教材需要引用外部技術標準或最新趨勢時；topic 有已知的業界最佳實踐時。

---

### Structured Research Summary Output
將收集的所有資料整合為統一格式的結構化摘要，方便 Content Designer 直接消費。每個欄位語意清楚，避免輸出格式不統一。
- Outcome 1: 標準格式的研究摘要（包含 topic、source_type、key_facts、data_points、references 欄位）
- Outcome 2: 資料缺口說明（無法找到的資料及原因），讓 Content Designer 知道哪些需要合理推估

When to dispatch: 所有研究工作（內部掃描、外部搜尋）完成後，整合輸出時執行。

---

### Context-Scoped File Batching
為避免上下文溢出，對大量系統檔案採用逐一或分批讀取策略，每批完成後立即整理摘要再進行下一批。
- Outcome 1: 不遺漏任何目標檔案的完整讀取計畫，及每批的摘要紀錄
- Outcome 2: 當某批讀取後發現已有足夠資料，提前終止並回報已收集內容

When to dispatch: 研究任務涉及超過 10 個檔案時；或系統提示上下文使用率超過 60% 時。

---

## NOT This Agent's Job
- 加工或設計教材內容（這是 content-designer 的工作）
- 對研究資料添加主觀詮釋或改善建議
- 使用 Edit / Write 修改非 memory/ 的檔案
- 評估教材品質（這是 content-evaluator 的工作）
