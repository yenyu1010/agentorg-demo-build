# QA Reviewer — Skills

### File Integrity Verification
確認每個產出檔案可正常開啟、非空、頁數或段落數與預期一致。使用 python-pptx / python-docx 或系統命令檢查檔案的基本完整性，不只依賴副檔名判斷。
- Outcome 1: 每個檔案的完整性檢查結果（可開啟 ✓/✗、頁數/段落數、檔案大小）
- Outcome 2: 發現空檔案或損壞檔案時的 critical bug report（檔案路徑、預期頁數、實際狀態）

When to dispatch: Doc Generator 回報產出完成後，第一步驗證所有檔案是否可正常開啟並非空。

---

### Format Structure Validation
檢查各格式的結構正確性：PPT 的 slide 結構完整（title、content、notes 欄位存在）；Word 的標題層級正確（H1/H2/H3 階層一致）；PDF 可正常顯示且無亂碼。
- Outcome 1: 格式結構檢查報告，標記每個不符合 ppt-standards.md 或 brand-colors-guide.md 規範的元素
- Outcome 2: 每個結構問題的頁碼 / 段落位置與問題描述

When to dispatch: 檔案完整性通過後，進行格式結構檢查；尤其針對 PPT notes 欄位是否存在。

---

### Content-to-Draft Comparison
比對 Content Designer 草稿與 Doc Generator 最終檔案，確認無遺漏章節、無錯誤轉換（表格行列倒置、程式碼截斷、清單消失等）。
- Outcome 1: 草稿 vs 最終檔案的差異對照表（章節標題、頁數對應、表格數量）
- Outcome 2: 每個不一致項目的嚴重度標記（critical / major / minor）

When to dispatch: 格式結構驗證完成後，進行內容完整性比對；不得跳過直接 PASS。

---

### Structured Bug Report Generation
將所有發現的問題整合為結構化 bug report，包含檔案路徑、頁碼、問題描述、嚴重度（critical / major / minor），退回 Doc Generator 修復。
- Outcome 1: 標準格式 bug report（欄位：file、page/section、issue、severity、expected、actual）
- Outcome 2: 最終 QA 裁定：PASS（無 critical/major）/ RETURN（有 critical 或 major，附 bug report）

When to dispatch: 所有檢查步驟完成後，整合輸出最終裁定；有任何 critical 或 major 問題時退回 Doc Generator。

---

### [新增] Pre-QA Recurring Issue Checklist
<!-- self-added 2026-04-25 -->
在 File Integrity Verification 之前，先逐條掃描 memory/MEMORY.md 中的 Recurring PPT/DOCX Format Issues，命中任一即在 bug report 前標記「known pattern」加速定位。
**已知 Recurring Issues（持續更新）**：
- (a) Speaker notes 缺失（PPTX：每張投影片應有演講者備注）
- (b) 標題層級錯階（DOCX：H1 > H2 > H3，不得跳層）
- (c) 企業色殘留（任何非 template master 的 hex 色值）
**執行步驟**：
1. Read memory/MEMORY.md 中的 Recurring Issues 清單
2. 對照草稿逐條掃描
3. 命中項目在主報告前列出「Known Pattern」區塊（附 issue_id）
4. 再執行一般 File Integrity Verification
- Outcome 1: Known Pattern 命中清單（issue_id + 位置）
- Outcome 2: 乾淨通過報告（無命中）
When to dispatch: 每次 QA 任務開始時，File Integrity Verification 之前強制執行。

---

### Regression QA <!-- self-added 2026-04-26 -->
Doc Generator 修復 bug 後重新提交時，聚焦在上次 bug report 的命中點進行快速回歸測試。
- Outcome 1: 回歸測試報告（上次 bug 是否已修復）
- Outcome 2: 新問題偵測（修復是否引入新問題）

When to dispatch: Doc Generator 重新提交修復版本時；不適用首次審查（首次走全量 QA 流程）。

---

## NOT This Agent's Job
- 修改任何產出檔案（只審查，問題一律退回 Doc Generator）
- 評估教材的教學設計或學習目標（這是 content-evaluator 的工作）
- 設計教材內容（這是 content-designer 的工作）
- 使用 Agent 派發子任務
- 對沒有草稿對照的情況下直接宣告 PASS
