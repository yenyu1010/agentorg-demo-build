# Engineer Flow — engineer/manager 完整流程

## 流程總覽
```
parse_request → session_init → analyze_requirements → [HITL] → develop → review_code → test → deliver
```

---

## session_init（Manager 直接執行）
1. task_id：`{task_short}-{YYYYMMDD}`（例：`login-feature-20260513`）
2. output_path：`$CLAUDE_PROJECT_DIR/output/engineer/{task_id}/`
3. 建立目錄：`mkdir -p "$output_path"`
4. 寫入 `00_context.md`：task_id、task_type、language、scope、使用者需求

---

## parse_request（Manager 直接執行）
- `task_type`：新功能 / Bug修復 / 重構 / 技術問題 / 其他
- `language`：程式語言
- `scope`：任務範圍
- `output_format`：程式碼 / 技術文件 / 分析報告

---

## analyze_requirements（engineer/system-analyst）

**Input:**
```json
{
  "user_query": "使用者需求描述",
  "task_type": "任務類型",
  "language": "程式語言",
  "output_path": "task 目錄路徑",
  "task_id": "task ID"
}
```

**Expected Output:**
```json
{
  "requirements": ["功能需求列表"],
  "design": "系統設計方案（架構、模組、資料流）",
  "tech_stack": ["建議技術堆疊"],
  "risks": ["潛在風險"],
  "estimated_steps": ["實作步驟"],
  "output_file": "01_design.md"
}
```

---

## hitl_gate（Manager 直接執行）
```
🏗️ 系統設計確認

需求摘要：{requirements}

設計方案：{design}

技術堆疊：{tech_stack}

實作步驟：{estimated_steps}

潛在風險：{risks}

---
請確認設計方向：
- `confirm` → 開始開發
- `modify: <說明>` → 調整設計
- `abort` → 停止
```

---

## develop（engineer/developer）

**Input:**
```json
{
  "design": "01_design.md 的設計方案",
  "requirements": "需求列表",
  "language": "程式語言",
  "output_path": "task 目錄路徑",
  "task_id": "task ID"
}
```

**Expected Output:**
```json
{
  "code_files": ["產出的程式碼檔案路徑"],
  "implementation_notes": "實作說明",
  "output_file": "02_implementation.md"
}
```

---

## review_code（engineer/code-reviewer）

**Input:**
```json
{
  "code_files": "developer 產出的程式碼",
  "requirements": "原始需求",
  "output_path": "task 目錄路徑"
}
```

**Expected Output:**
```json
{
  "verdict": "PASS | REVISE",
  "issues": ["發現的問題列表"],
  "suggestions": ["改善建議"],
  "output_file": "03_review.md"
}
```

| verdict | Manager 動作 |
|---------|-------------|
| PASS | 繼續 test |
| REVISE | 退回 developer 修改（最多 1 次）|

---

## test（engineer/tester）

**Input:**
```json
{
  "code_files": "程式碼檔案",
  "requirements": "原始需求",
  "output_path": "task 目錄路徑"
}
```

**Expected Output:**
```json
{
  "test_cases": ["測試案例列表"],
  "results": "測試結果",
  "verdict": "PASS | FAIL",
  "output_file": "04_test_report.md"
}
```

---

## deliver（Manager 直接執行）
報告包含：
- 產出程式碼路徑
- 功能說明
- 如何執行/使用
- 已知限制
- 工時打卡明細表
