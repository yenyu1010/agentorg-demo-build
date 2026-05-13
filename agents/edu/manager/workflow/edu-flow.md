# Edu Flow — edu/manager 完整流程

## 流程總覽
parse_request → [Manager] → research → [Manager] → design_content → [Manager] → evaluate_content → [Manager] → visual_styling → [Manager] → generate_docs → [Manager] → qa_review → deliver

Manager 在每個步驟之間是主動決策點，不只是最後合成。

---

## 架構原則

### Worker 只面對 Manager
- Manager 是流程中唯一的決策者
- 所有 worker 的輸出只交給 Manager，worker 之間不直接溝通
- Manager 有權在任何 handoff 點退回（不只是 evaluate 後）

### Manager 審核 Worker 的判斷
當 worker 回報需要退回時（例如 evaluate 回報 REVISE），Manager 不盲目執行：
1. 審核退回理由是否具體、有據
2. 如果理由模糊 → 要求 worker 重新評估或補充說明
3. 如果理由充分 → 整理後帶入，退回給上游 worker

**評估 revision_notes 是否充分的標準**：
- 具體指出哪個章節 / 頁面有問題
- 說明問題是什麼（不只是「需要改進」）
- 有 Bloom's Taxonomy 依據
- 給出明確的修改方向
不符合以上任一條 → Manager 退回 evaluator 要求補充，而非直接讓 content-designer 重做

---

## 派遣訊息通用規範（所有 worker 派遣共用）

每一次派遣 worker，Task Block 都必須包含以下欄位（詳見 `agents/protocols/rules/output-placement.md`）：

```
output_path: <session_init 建立的絕對路徑，例：$CLAUDE_PROJECT_DIR/output/edu/agent-training-20260422/>
task_id: <session_init 決定的 task_id，例：agent-training-20260422>
session_dir: <同 output_path，為保持 edu team 既有術語相容>
```

Worker 收到後：
- 所有任務產物寫入 `output_path`（= session_dir）
- 若 brief 缺 `output_path`，Worker 必須回報 `SCOPE VIOLATION: missing output_path` 並停工
- Worker 不得寫回自己的 agent 資料夾（memory/ 除外，那是 agent 內部快取）
- 檔名依本 flow 慣例（`01_research.md`、`02_design_draft.md`、`03_evaluation.md`、`04_style_guide.json`、`05_qa_report.md` 等）

---

## 步驟 Handshake 定義

### session_init（Manager 直接執行，parse_request 之前）

Manager 在開工時立即執行，無需分派。

**動作：**
1. 決定 `task_id`：格式 `{topic_short}-{YYYYMMDD}`（kebab-case，topic_short 取 topic 關鍵字；例：`agent-training-20260422`、`transformer-basics-20260422`）
2. 組合 `output_path`（= session_dir）：`output_path = "$CLAUDE_PROJECT_DIR/output/edu/{task_id}/"`（fallback `"$PWD/output/edu/{task_id}/"`）
3. 建立目錄：`mkdir -p "$output_path"`
4. 寫入 `$output_path/00_context.md`，包含：task_id、topic、audience_profile、output_format、language、用戶特殊需求
5. 將 `output_path`（= session_dir）與 `task_id` 記錄為本次任務的全局變數，傳遞給所有後續 dispatch（在派遣 brief 的 Task Block 必填）
6. 產出資料夾使用中文子資料夾（如 `教材成品/` 在 `$output_path` 底下），中間產物維持英文（如 `research/`、`tmp/`）

**遵循：**
- `agents/protocols/rules/output-placement.md`（`output_path` 必傳、Worker 缺 `output_path` 須拒絕）
- `agents/protocols/rules/session-directory.md`（session_dir 內部檔案命名）
- **整合說明**：在本規則下，`session_dir` 即 `output_path`（`<CWD>/output/edu/{task_id}/`）。舊的 `sessions/YYYY-MM-DD_{topic_short}` 路徑慣例由本規則的 `output/edu/{task_id}/` 取代，但 session_dir 內部的 `00_context.md`、`01_research.md` … 等檔案命名維持不變。

**on_error:** continue（目錄建立失敗不阻擋流程，但必須記錄警告並回報用戶）

---

### parse_request（Manager 直接執行）

Manager 直接執行，無需分派。

**解析欄位：**
- `topic`：教材主題
- `audience_profile`：`executive | developer | power-user`
- `output_format`：`xlsx | docx | pptx`（PDF 為可選輸出，不列入預設三選一，僅使用者明確要求時加入）
- `language`：`zh-TW | en`

**Manager handoff → research：**
確認 topic / audience_profile / output_format 均有值後，才派出 research。

**on_error:** report_and_stop

---

### research（edu/edu-researcher + shared/researcher，並行）

**Input:**
```json
{
  "topic": "從 parse_request 提取的主題",
  "scope": "要讀取的 agent 系統目錄範圍",
  "external_search": "需要搜尋的外部關鍵詞",
  "session_dir": "manager 建立的 session 目錄路徑，worker 應從此讀取前序輸出並將產出寫入此目錄",
  "output_path": "session_init 建立的絕對路徑",
  "task_id": "格式 {topic_short}-{YYYYMMDD}"
}
```

**Expected Output:**
```json
{
  "internal_findings": "agent 系統結構化摘要",
  "external_findings": "外部資料摘要",
  "format": "markdown",
  "output_file": "寫入 session_dir 的檔案名稱（如 01_research.md）"
}
```

**Post-Dispatch Verification（Manager 自執行）：**
- `output_file`：Glob `{session_dir}/01_research.md`（或 agent 宣稱的路徑），確認存在且 size > 0
- `internal_findings`：Grep session_dir 下研究檔，確認有實質內容（非「暫無」、非空白）
- worklog：Glob `agents/edu/edu-researcher/worklog/` 確認有新 JSON
- 遵循：`agents/protocols/rules/output-verification.md`

**Manager handoff → design_content：**
Manager 確認 internal_findings 非空、external_findings 有可用數據後，才派出 content-designer。
若研究結果不足：重試一次，仍不足則告知使用者並請求補充資料。

**on_error:** retry_once

---

### design_content（edu/content-designer）

**Input:**
```json
{
  "research_results": "research 步驟的產出",
  "audience_profile": "executive | developer | power-user",
  "output_format": "xlsx | docx | pptx",
  "language": "zh-TW | en",
  "revision_instructions": "（僅 REVISE 迴圈時填入）Manager 從 evaluate 帶來的具體修改指示",
  "session_dir": "manager 建立的 session 目錄路徑，worker 應從此讀取前序輸出並將產出寫入此目錄",
  "output_path": "session_init 建立的絕對路徑",
  "task_id": "格式 {topic_short}-{YYYYMMDD}"
}
```

**Expected Output:**
```json
{
  "content_draft": "Markdown 格式的教材草稿",
  "slide_json": "PPT 用的 JSON 結構（如果 format=pptx）",
  "learning_objectives": "學習目標列表",
  "output_file": "寫入 session_dir 的檔案名稱（如 02_design_draft.md）"
}
```

**Post-Dispatch Verification（Manager 自執行）：**
- `output_file`：Glob `{session_dir}/02_design_draft.md`，確認存在且 size > 0
- `content_draft`：Read 該檔，確認包含至少 3 個章節標題（非骨架佔位符）
- `learning_objectives`：Grep 確認至少 3 條學習目標存在
- worklog：Glob `agents/edu/content-designer/worklog/` 確認有新 JSON
- 遵循：`agents/protocols/rules/output-verification.md`

**Manager handoff → evaluate_content：**
Manager 確認 content_draft 非空、learning_objectives 有至少 3 條後，才派出 content-evaluator。
若草稿明顯不完整：Manager 直接退回 content-designer 並附說明，不浪費 evaluator token。

**on_error:** retry_once

---

### evaluate_content（edu/content-evaluator）

> 遵循：`agents/protocols/rules/evaluator-rerun.md`

**Input:**
```json
{
  "content_draft": "design_content 的產出",
  "audience_profile": "同上",
  "learning_objectives": "同上",
  "session_dir": "manager 建立的 session 目錄路徑，worker 應從此讀取前序輸出並將產出寫入此目錄",
  "output_path": "session_init 建立的絕對路徑",
  "task_id": "格式 {topic_short}-{YYYYMMDD}"
}
```

**Expected Output:**
```json
{
  "verdict": "PASS | REVISE | FAIL",
  "blooms_assessment": "Bloom's Taxonomy 各層次評估結果",
  "revision_notes": "REVISE 時必填。格式：[頁碼/章節] [問題描述] [Bloom's 層次不符點] [建議修改方向]，不得少於 3 條具體改進項，不允許只說「請改進」",
  "assessment_questions": "嵌入式評量題目",
  "output_file": "寫入 session_dir 的檔案名稱（如 03_evaluation.md）"
}
```

**Post-Dispatch Verification（Manager 自執行）：**
- `output_file`：Glob `{session_dir}/03_evaluation.md`，確認存在
- `verdict`：確認回傳值為 PASS、REVISE 或 FAIL 三選一（非空）
- REVISE 時：`revision_notes` 至少 3 條，每條包含具體章節+問題+方向
- worklog：Glob `agents/edu/content-evaluator/worklog/` 確認有新 JSON
- 遵循：`agents/protocols/rules/output-verification.md`

**Manager handoff → 決策路由：**

| verdict | Manager 動作 |
|---------|-------------|
| PASS | 派出 doc-generator，附上 content_draft + assessment_questions |
| REVISE | 1. Manager 審核 revision_notes 是否充分（見架構原則）<br>2. 充分 → 整理後退回 design_content<br>3. 不充分 → 退回 evaluator 補充說明（最多 1 次）<br>**4. content-designer 完成修訂後，必須重新派遣 evaluate_content 確認。Manager 不得自行判定 PASS（見 agents/protocols/rules/evaluator-rerun.md）** |
| FAIL | 回報使用者，說明失敗原因，不繼續流程 |

REVISE 最多迴圈 2 次。第 2 次仍 REVISE 時，Manager 回報使用者並交付現有草稿。

**on_error:** retry_once

---

### visual_styling（edu/visual-stylist）

**Input:**
```json
{
  "evaluated_content": "evaluate 通過的內容",
  "audience_profile": "影響視覺策略",
  "output_format": "pptx 需要完整 styling；docx/xlsx 較簡單；pdf 為可選次要格式",
  "session_dir": "manager 建立的 session 目錄路徑，worker 應從此讀取前序輸出並將產出寫入此目錄",
  "output_path": "session_init 建立的絕對路徑",
  "task_id": "格式 {topic_short}-{YYYYMMDD}"
}
```

**Expected Output:**
```json
{
  "styled_content": "加入視覺建議的內容",
  "style_guide": "配色、字型、版面規範（須符合 brand-colors-guide.md）",
  "output_file": "寫入 session_dir 的檔案名稱（如 04_style_guide.json）"
}
```

**Post-Dispatch Verification（Manager 自執行）：**
- `output_file`：Glob `{session_dir}/04_style_guide.json`，確認存在且 size > 0
- `style_guide`：Read 確認包含色彩定義（至少含 primary_color 或 brand_color 欄位）
- worklog：Glob `agents/edu/visual-stylist/worklog/` 確認有新 JSON
- 遵循：`agents/protocols/rules/output-verification.md`

**Manager handoff → generate_docs：**
Manager 確認 styled_content 非空、style_guide 包含色彩定義後，才派出 doc-generator。

**on_error:** retry_once

---

### generate_docs（edu/doc-generator）

**Input:**
```json
{
  "styled_content": "visual_styling 的產出",
  "formats": ["xlsx", "docx", "pptx"],
  "output_dir": "目標輸出目錄（用戶可見資料夾使用中文名，遵循 agents/protocols/rules/naming-convention.md）",
  "session_dir": "manager 建立的 session 目錄路徑，worker 應從此讀取前序輸出並將產出寫入此目錄",
  "output_path": "session_init 建立的絕對路徑",
  "task_id": "格式 {topic_short}-{YYYYMMDD}"
}
```

> 注意：`output_dir` 即 `output_path`，保留名稱為向下相容。

**Expected Output:**
```json
{
  "files": ["產出的檔案絕對路徑列表"],
  "status": "completed | partial | failed",
  "output_file": "寫入 session_dir 的檔案名稱（如 05_qa_report.md）"
}
```

### 並行生成模式（投影片 ≥ 10 張時啟用）<!-- updated 2026-04-15 -->
Manager 應同時派遣多個 doc-generator 實例（每章一個），而非單一串行執行。
派遣指令包含：chapter_id、slides_range、design_draft 對應章節部分。
所有章節完成後，額外派遣一次 doc-generator 執行 Merge 任務。
預期時間節省：原本串行 N 章 × T 秒 → 並行後約 T 秒（單章時間）+ 合併時間

**Post-Dispatch Verification（Manager 自執行）：**
- `files` 列表：Glob 每個宣稱的輸出檔案路徑，確認存在且 size > 0
- `status`：確認為 `completed` 或 `partial`（非 `failed`）
- worklog：Glob `agents/edu/doc-generator/worklog/` 確認有新 JSON
- 遵循：`agents/protocols/rules/output-verification.md`

**Manager handoff → qa_review：**
Manager 確認每個應產出的檔案存在且大小 > 0 後，才派出 qa-reviewer。
若任何檔案缺失：Manager 重試 doc-generator 一次（附具體錯誤訊息）。

**on_error:** retry_once

---

### qa_review（edu/qa-reviewer）

**Input:**
```json
{
  "generated_files": "generate_docs 的檔案路徑",
  "original_draft": "content_draft 作為對照基準"
}
```

**Expected Output:**
```json
{
  "verdict": "PASS | FAIL",
  "bug_list": "發現的問題列表（如果有）",
  "file_checks": "每個檔案的檢查結果"
}
```

**Post-Dispatch Verification（Manager 自執行）：**
- `verdict`：確認為 PASS 或 FAIL（非空）
- `file_checks`：確認包含每個受測檔案的結果
- worklog：Glob `agents/edu/qa-reviewer/worklog/` 確認有新 JSON
- 遵循：`agents/protocols/rules/output-verification.md`

**Manager handoff → deliver：**

| verdict | Manager 動作 |
|---------|-------------|
| PASS | 進入 synthesize，回報使用者所有產出 |
| FAIL | 將 bug_list 整理後退回 doc-generator 重做（最多 1 次）|

**on_error:** retry_once

---

### merge-chapters（edu/doc-generator，固定最後合併步驟）<!-- added 2026-04-15 -->

## merge-chapters
### Merge Agent 職責（固定最後一步）
1. 掃描 `tmp/workshop_ch*_*.pptx` 所有暫存檔
2. 依 chapter_id 順序合併（使用 anthropic-skills:pptx 或 python-pptx）
3. 輸出最終 PPTX 至專案根目錄
4. 驗證：總頁數 = 各章節頁數加總
5. 清理 `tmp/` 暫存檔
6. 回報 Edu Manager：最終檔名、總頁數、生成耗時

---

### deliver（Manager 直接執行）

Manager 合成最終報告，按以下步驟執行：

#### Step 1 — 讀取所有 worker worklogs

用 Glob 掃描本次任務中所有被派遣 agent 的 worklog 檔案：
```
agents/edu/*/worklog/*.json
agents/shared/*/worklog/*.json
```

篩選條件：`trace_id` 等於本次任務的 trace_id。

#### Step 2 — 組裝彙整表

從每個 worklog JSON 讀取實際時間戳，組裝工時打卡明細表：

```
| Agent | input_summary | output_summary | started_at | ended_at | duration_s | status |
|-------|---------------|----------------|------------|----------|------------|--------|
| edu-researcher | ... | ... | ... | ... | ... | completed |
| ...其他 agents... |
| **總計** | {N} agents | | | | {total}s | {pass}/{fail} |
```

- 時間必須來自 worklog JSON 實際時間戳，不得粗估
- 缺 worklog 或 failed 的 agent 標註原因

#### Step 3 — 合成報告

報告包含：
- 產出檔案路徑（每個 format 一行）
- 產出檔案使用中文檔名（遵循 agents/protocols/rules/naming-convention.md）
- 受眾 profile（audience_profile used）
- 內容摘要（3-5 bullet points）
- 評量題目（來自 content-evaluator，如有）
- 工時打卡明細表（Step 2 的表格）
