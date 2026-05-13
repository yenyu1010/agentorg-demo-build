# Lawyer Flow — lawyer/manager 完整流程

## 流程總覽

```
parse_request → session_init → analyze_case → [HITL Gate 1] → research_law → assess_risk → [HITL Gate 2] → generate_docs → deliver
```

---

## session_init（Manager 直接執行）

1. 決定 `task_id`：格式 `{case_short}-{YYYYMMDD}`（例：`contract-dispute-20260513`）
2. 組合 `output_path`：`$CLAUDE_PROJECT_DIR/output/lawyer/{task_id}/`
3. 建立目錄：`mkdir -p "$output_path"`
4. 寫入 `$output_path/00_context.md`，包含：task_id、case_type、jurisdiction、urgency、output_format、language、使用者原始問題

---

## parse_request（Manager 直接執行）

**解析欄位：**
- `case_type`：合約糾紛 / 勞資問題 / 智財 / 消費者保護 / 刑事 / 其他
- `jurisdiction`：台灣（預設）/ 其他
- `urgency`：urgent / normal（預設 normal）
- `output_format`：法律意見書 / 合約審查報告 / 風險摘要（預設法律意見書）
- `language`：zh-TW / en

---

## analyze_case（lawyer/case-analyzer）

**Input:**
```json
{
  "user_query": "使用者原始描述",
  "case_type": "案件類型",
  "jurisdiction": "適用法域",
  "output_path": "task 目錄路徑",
  "task_id": "task ID"
}
```

**Expected Output:**
```json
{
  "case_summary": "案情摘要（300字以內）",
  "key_facts": ["關鍵事實列表"],
  "parties": {"主張方": "...", "相對方": "..."},
  "legal_issues": ["核心法律爭點"],
  "applicable_law_areas": ["初步判斷的法律領域"],
  "missing_info": ["尚需釐清的資訊"],
  "output_file": "01_case_analysis.md"
}
```

**Post-Dispatch Verification：**
- Glob `{output_path}/01_case_analysis.md`，確認存在且 size > 0
- 確認 `legal_issues` 至少 1 條
- Glob `agents/lawyer/case-analyzer/worklog/` 確認有新 JSON

---

## hitl_gate_1（Manager 直接執行）

Manager 向使用者呈現：

```
📋 案情確認

案情摘要：{case_summary}

關鍵事實：
{key_facts}

核心法律爭點：
{legal_issues}

尚需釐清：
{missing_info}

---
請確認以上案情是否正確？
- 回覆 `confirm` → 繼續進行法條研究
- 回覆 `modify: <補充說明>` → 補充修正後重新分析
- 回覆 `abort` → 停止
```

只接受 `confirm` / `modify: ...` / `abort`，其他回覆視為 `abort`。

---

## research_law（lawyer/law-researcher + shared/researcher，並行）

**Input:**
```json
{
  "legal_issues": "case_analysis 的爭點列表",
  "applicable_law_areas": "初步法律領域",
  "jurisdiction": "適用法域",
  "output_path": "task 目錄路徑",
  "task_id": "task ID"
}
```

**Expected Output:**
```json
{
  "relevant_laws": ["法條列表（含條號、條文內容摘要）"],
  "relevant_cases": ["相關判例（含案號、要旨）"],
  "regulations": ["相關行政規則、函令"],
  "legal_principles": ["適用法律原則"],
  "output_file": "02_law_research.md"
}
```

**Post-Dispatch Verification：**
- Glob `{output_path}/02_law_research.md`，確認存在
- 確認 `relevant_laws` 至少 1 條

---

## assess_risk（lawyer/risk-assessor）

**Input:**
```json
{
  "case_analysis": "01_case_analysis.md 的內容",
  "law_research": "02_law_research.md 的內容",
  "output_path": "task 目錄路徑",
  "task_id": "task ID"
}
```

**Expected Output:**
```json
{
  "risk_level": "high | medium | low",
  "possible_outcomes": ["可能的法律結果（勝訴/敗訴/和解等）"],
  "key_risks": ["主要風險點"],
  "recommendations": ["建議行動方案"],
  "time_limits": ["重要時效期限"],
  "output_file": "03_risk_assessment.md"
}
```

---

## hitl_gate_2（Manager 直接執行）

Manager 向使用者呈現：

```
⚖️ 風險評估結果

風險等級：{risk_level}

可能結果：
{possible_outcomes}

主要風險：
{key_risks}

建議方案：
{recommendations}

重要時效：
{time_limits}

---
確認以上評估後，將產出 {output_format}。
- 回覆 `confirm` → 產出文件
- 回覆 `modify: <說明>` → 調整評估方向
- 回覆 `abort` → 停止

⚠️ 本分析僅供參考，不構成正式法律意見。重要決策請諮詢持照律師。
```

---

## generate_docs（lawyer/doc-generator）

**Input:**
```json
{
  "case_analysis": "01_case_analysis.md",
  "law_research": "02_law_research.md",
  "risk_assessment": "03_risk_assessment.md",
  "output_format": "法律意見書 | 合約審查報告 | 風險摘要",
  "language": "zh-TW | en",
  "output_path": "task 目錄路徑",
  "task_id": "task ID"
}
```

**Expected Output:**
```json
{
  "files": ["產出的檔案絕對路徑列表"],
  "status": "completed | partial | failed",
  "output_file": "04_legal_document.docx"
}
```

---

## deliver（Manager 直接執行）

報告包含：
- 產出檔案路徑
- 案情摘要
- 法律結論（3-5 bullet points）
- 建議行動
- 重要時效
- 工時打卡明細表
- **⚠️ 免責聲明**：本分析僅供參考，不構成正式法律意見。如涉及重大法律決策，請諮詢持照律師。
