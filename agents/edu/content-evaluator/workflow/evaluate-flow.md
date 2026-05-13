# Content Evaluator — Evaluate Flow

完整的教材評估流程。由 workflow.yaml route 到此。

## 流程步驟

### 1. 讀取教材草稿
- 工具：`Read`
- 來源：content-designer 的輸出（Markdown 或 JSON）
- 若無草稿：停止並回報 `DRAFT_NOT_FOUND`

### 2. 讀取對應 Audience Profile
- 工具：`Read`
- 路徑：`agents/edu/content-designer/workflow/audience-profiles.md`
- 找出與教材匹配的 audience profile
- 若無匹配 profile：停止並回報 `PROFILE_NOT_FOUND`

### 3. 用 Bloom's Taxonomy 評估學習目標
評估維度：
- **可測量性**：動詞是否具體（avoid: 了解、知道；prefer: 描述、分析、應用）
- **層次覆蓋**：是否覆蓋記憶→理解→應用→分析四個層次
- **與內容對齊**：學習目標是否對應章節內容

記分：每個目標 0-2 分（0=不可測量，1=部分可測量，2=完全可測量）

### 4. 評估內容深度、用語、範例適合度
評估維度：
| 維度 | 說明 |
|------|------|
| 內容深度 | 與 audience 的 level 是否匹配（太淺/適中/太深） |
| 用語風格 | 術語密度、句子長度、是否符合 language_level |
| 範例相關性 | 範例是否貼近 audience 的產業背景 |
| 結構清晰度 | 章節邏輯、過渡句、摘要是否完整 |

記分：每個維度 1-5 分

### 5. 設計嵌入式評量題目
每章設計 2-3 題，題型分配：
- **選擇題**：測試記憶和理解層次
- **情境題**：測試應用和分析層次
- **開放題**：測試評估和創造層次（選用）

輸出格式：
```
assessment:
  chapter_1:
    - type: multiple_choice
      question: "..."
      options: ["A. ...", "B. ...", "C. ...", "D. ..."]
      answer: "B"
      bloom_level: 記憶
    - type: scenario
      question: "..."
      bloom_level: 應用
```

### 6. 產出評估報告
最終報告格式：
```
evaluation_report:
  verdict: PASS | REVISE | FAIL
  overall_score: [0-100]
  scores:
    learning_objectives: [0-10]
    content_depth: [1-5]
    language_fit: [1-5]
    example_relevance: [1-5]
    structure_clarity: [1-5]
  findings:
    strengths: [列表]
    issues: [列表，含嚴重度 high/medium/low]
  recommendations:
    - [具體修改建議，含位置參考]
  assessment: [嵌入式評量題目]
```

**判定標準：**
- PASS：overall_score ≥ 80，無 high severity issue
- REVISE：overall_score 60-79，或有 medium/high issue 需修正
- FAIL：overall_score < 60，或有 high severity issue 且影響核心學習

## 注意事項
- 評估標準以 audience profile 為基準，不以通用標準評判
- REVISE 必須提供可執行的具體建議（指出章節、段落）
- FAIL 必須說明根本原因，讓 content-designer 知道如何重做
