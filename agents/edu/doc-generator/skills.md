# Doc Generator — Skills

### Markdown-to-PPTX Conversion
優先使用 `anthropic-skills:pptx` 將 Content Designer 提供的 JSON slides array 轉換為 PowerPoint 實體檔案；若 Skill 不可用則 fallback 至本地 `scripts/gen-pptx.py`（python-pptx）。保留每張投影片的 title、content、notes 欄位，套用企業色彩規範（brand-colors-guide.md 與 ppt-standards.md）。不做預先套件驗證，失敗直接 fallback。
- Outcome 1: 可正常開啟的 .pptx 檔案，投影片數量與 JSON slides 一致
- Outcome 2: 轉換腳本執行日誌（腳本名稱、輸入路徑、輸出路徑、耗時）

When to dispatch: output_format 包含 pptx，且 content-evaluator 裁定 PASS 後；收到 JSON slides array 輸入時。

---

### Markdown-to-DOCX Conversion
優先使用 `anthropic-skills:docx` 將 Content Designer 的完整 Markdown 教材轉換為 Word 文件；若 Skill 不可用則 fallback 至本地 `scripts/gen-docx.py`（python-docx）。正確對應標題層級（H1→Heading 1、H2→Heading 2）、程式碼區塊、表格與清單樣式。不做預先套件驗證，失敗直接 fallback。
- Outcome 1: 格式正確的 .docx 檔案，標題層級、表格、程式碼均正確呈現
- Outcome 2: 轉換腳本執行日誌與任何格式對應警告

When to dispatch: output_format 包含 docx；收到完整 Markdown 教材輸入時。

---

### PDF Export via LibreOffice CLI
> 注意：PDF 為次要格式，僅在使用者明確要求時才觸發。

當 python 轉換工具不可用或輸出格式為 PDF 時，使用 LibreOffice headless CLI（`libreoffice --headless --convert-to pdf`）作為後備，將 docx 或 pptx 轉為 PDF。
- Outcome 1: 可正常顯示的 .pdf 檔案
- Outcome 2: 詳細的錯誤回報（腳本名稱、錯誤訊息、輸入路徑），便於 qa-reviewer 追蹤

When to dispatch: output_format 包含 pdf；或主要轉換工具（python-pptx / python-docx）失敗時作為後備方案。

---

### Conversion Error Reporting
當任何格式轉換步驟失敗時，產出結構化的錯誤報告，包含失敗的腳本名稱、完整錯誤訊息與輸入檔案路徑，不靜默略過任何失敗。
- Outcome 1: 結構化錯誤報告（腳本、錯誤碼、訊息、輸入路徑）
- Outcome 2: 建議的修復方向（環境問題 / 輸入格式問題 / 依賴套件問題）

When to dispatch: 任何轉換步驟拋出異常或輸出檔案不完整時，立即執行此技能。

---

### Workshop-Scale PPT Generation
使用 `scripts/workshop_pptx.py` 生成大型工作坊教材投影片（20+ 頁），支援 speaker notes、暫停點標記、多色配色區塊、計時標籤等 Workshop 特有元素。嚴格遵守企業色彩（#61B520 品牌綠 + #5DABE2 品牌藍）。
- Outcome 1: 完整 .pptx 檔案（含每頁 speaker notes、Workshop 專用格式）
- Outcome 2: 色彩合規驗證通過報告

When to dispatch: 當 output_format=pptx 且 topic_type=workshop/training 且 estimated_slides > 15 時，優先於 gen-pptx.py。一般小型 PPT 仍用 gen-pptx.py。

<!-- self-added 2026-04-15 by agent-builder (修補 workshop 場景缺口) -->

---

### XLSX Generation
使用 Claude 內建 anthropic-skills:xlsx 產出 Excel 表格教材（教學計畫表、評量表、學習追蹤表）。

- 優先策略：呼叫 `Skill(skill="anthropic-skills:xlsx")`，由 Claude 原生處理
- Fallback：若 Skill 工具不可用，使用 openpyxl 本地腳本（`scripts/xlsx_generator.py`，尚未建立，首次使用時自行加法建立）
- 輸入：結構化資料（表頭 + 行資料 JSON）、Sheet 名稱、欄寬建議
- 輸出：`.xlsx` 檔案，符合企業配色（標題列 #61B520 品牌綠底白字）

When to dispatch：使用者要求表格型教材、評量追蹤表、學習紀錄表、課程計畫表，或 output_format 包含 xlsx 時。
<!-- self-added 2026-04-15 -->

---

### Chapter PPTX Merge <!-- self-added 2026-04-22 -->
輸入多個 chapter_*.pptx，以 python-pptx copy_slide 邏輯依序併入單一母檔，保留 master slide 與 brand 配色；輸出最終 Workshop/Onboarding *.pptx 並清理 tmp/。
- Outcome 1: 單一合併 pptx 檔案，slide count = Σ(chapter_i.slide_count)
- Outcome 2: 合併後企業色保留、layout 繼承正確
- Outcome 3: tmp/chapter_*.pptx 清理

When to dispatch: 在 Chapter Parallel Generation 完成後作為最終合併步驟。

⚠️ silent-failure risk：merge_pptx.py 若只 copy XML 不 rebuild image rId → 圖片失效。需 Governance 行為測試。

---

### Chapter Parallel Generation  <!-- self-added 2026-04-15 -->
將 Workshop 投影片依章節（Part）拆分，由 Manager 並行派遣多個 doc-generator 實例，各自生成一個章節的投影片，最後由 Merge Agent 合併為單一 PPTX。

**適用條件**：投影片總數 ≥ 10 張，且內容可按章節分割時。

**章節分配範例（6-Part Workshop）**：
- Agent 1：封面 + Part 1（破冰）
- Agent 2：Part 2（安裝）
- Agent 3：Part 3（工作流程）
- Agent 4：Part 4（Live Demo）
- Agent 5：Part 5（小組練習）
- Agent 6：Part 6（Q&A）+ 結語

**每個章節 Agent 的輸出**：
- 暫存 PPTX 片段：`tmp/workshop_ch{N}_2026-04-15.pptx`
- 回報：章節名稱、投影片數、生成是否成功

**Merge Agent 職責**：
- 收集所有章節 PPTX
- 依序合併為單一檔案（保留 master slide 與配色）
- 輸出：最終 `AgentOrg_Workshop_v2_*.pptx`
- 清理 `tmp/` 暫存檔

When to dispatch：Edu Manager 派工時說明 total_slides ≥ 10，或明確要求「並行生成」。

---

### [新增] Merge Integrity Pre-check
<!-- self-added 2026-04-25 -->
Chapter PPTX Merge 完成後立即執行 rId integrity check，防止 silent-failure（圖片失效）。
**執行步驟**：
1. python-pptx 讀出 merged PPTX 中所有 slide 的 image shape
2. 驗證每個 image shape 的 rId → blob 對應是否存在
3. 任何 broken rId 即記錄到 worklog task_context 並標 critical bug
4. 觸發 qa-reviewer 重驗
**觸發條件**：任何呼叫 merge_pptx.py 的操作完成後必須執行。
- Outcome 1: rId integrity report（broken count / total count）
- Outcome 2: 若有 broken rId，附上修復建議（重新 copy image blob，重建 rId mapping）
When to dispatch: merge_pptx.py 執行完成後，回傳 Manager 前強制執行。

---

## NOT This Agent's Job
- 修改輸入教材的文字、順序或結構（格式忠實，不增刪內容）
- 評估教材的教學設計品質（這是 content-evaluator 的工作）
- 審查產出檔案的最終品質（這是 qa-reviewer 的工作）
- 使用 WebSearch / WebFetch 搜尋外部資料
- 在產出檔案中加入未經授權的頁眉、頁腳或浮水印

### 臨時腳本存放規則 <!-- propagated 2026-04-15 -->
任務執行中產生的一次性腳本（.js、.py、.sh）必須存放於當次任務的 session directory 下的 `scripts/` 子目錄，不得放入全域 `scripts/` 或 `.claude/scripts/`。
遵循：`agents/protocols/rules/session-directory.md#臨時腳本存放規則`
