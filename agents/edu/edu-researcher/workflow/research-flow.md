# Edu Researcher — Research Flow

完整的教育研究流程。由 workflow.yaml route 到此。

## 流程步驟

### 1. 掃描 Agent 系統目錄結構
- 工具：`Glob`
- 動作：掃描 `agents/` 下所有相關目錄
- 模式：`**/{soul,org}.md`
- 目的：取得整個 agent 系統的目錄清單

### 2. 逐一讀取目標 Agent 文件
- 工具：`Read`（逐一呼叫，不批次）
- 目標：依研究需求，讀取相關 agent 的 `soul.md` 和 `org.md`
- 順序：一次讀一個檔案，讀完再讀下一個
- 記錄：整理每個 agent 的角色、能力、限制

### 3. 結構化摘要（Internal Findings）
輸出格式：
```
internal_findings:
  agents_reviewed: [列表]
  key_capabilities: [整理]
  gaps_identified: [整理]
  relevant_patterns: [整理]
```

### 4. 搜尋外部相關資料
- 工具：`WebSearch`
- 查詢：根據使用者要求的主題構建搜尋詞
- 數量：最多 3-5 個搜尋查詢
- 錯誤處理：搜尋失敗時標記 external_findings 為空，繼續執行

### 5. 抓取關鍵文章
- 工具：`WebFetch`
- 依據：從步驟 4 的搜尋結果中挑選最相關的 URL
- 數量：最多 3 篇文章
- 錯誤處理：個別 URL 失敗時跳過，繼續其他 URL

### 6. 結構化摘要（External Findings）
輸出格式：
```
external_findings:
  sources: [列表，含 URL 和標題]
  key_insights: [整理]
  best_practices: [整理]
  research_gaps: [整理]
```

### 7. 合併輸出
最終輸出結構：
```
research_output:
  topic: [研究主題]
  internal_findings:
    agents_reviewed: [...]
    key_capabilities: [...]
    gaps_identified: [...]
    relevant_patterns: [...]
  external_findings:
    sources: [...]
    key_insights: [...]
    best_practices: [...]
    research_gaps: [...]
  summary: [一段整合性結語]
```

## 注意事項
- 步驟 1-3 是 internal research（agent 系統內部）
- 步驟 4-6 是 external research（外部網路資源）
- 步驟 7 合併兩者，提供給 content-designer 使用
- 若 internal 和 external 有衝突，在 summary 中標記並說明
