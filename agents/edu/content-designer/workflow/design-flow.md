# Content Designer — Design Flow

完整的教材設計流程。由 workflow.yaml route 到此。

## 流程步驟

### 1. 讀取 Audience Profile
- 工具：`Read`
- 路徑：`agents/edu/content-designer/workflow/audience-profiles.md`
- 找出與本次任務匹配的 audience（依職稱、產業、語言）
- 若找不到匹配 profile，停止並回報：`AUDIENCE_NOT_FOUND`

### 2. 讀取研究結果
- 工具：`Read`
- 來源：edu-researcher 的輸出（`research_output`）
- 若無研究結果：以最小可用資訊繼續，並在報告中標記 `research_missing: true`

### 3. 設計教材大綱
輸出格式：
```
outline:
  title: [教材標題]
  target_audience: [audience id]
  learning_objectives:
    - [動詞 + 可測量指標]（符合 Bloom's Taxonomy）
  chapters:
    - id: 1
      title: [章節標題]
      key_points: [重點列表]
      estimated_minutes: [時間]
  total_duration: [總時長（分鐘）]
```
- 學習目標必須使用可測量動詞（描述、分析、應用、評估）
- 章節順序遵循「概念→實作→評量」結構

### 4. 撰寫完整內容
- 格式：Markdown
- 依據：outline + research_output + content-templates.md
- 每章必須包含：說明文字、範例、重點摘要
- 用語風格：參考 audience profile 的 language_level

### 5. 根據 output_format 結構化輸出
根據任務指定的 `output_format` 轉換：

**PPT → JSON（投影片結構）：**
```json
{
  "slides": [
    {
      "slide_number": 1,
      "title": "...",
      "content": ["..."],
      "notes": "...",
      "brand_colors": { "primary": "#...", "accent": "#..." }
    }
  ]
}
```
- 色彩應用：遵守 `brand-colors-guide.md`，主色用於標題，強調色用於重點

**Word/PDF → Markdown：**
- 保持 Markdown 格式
- 標題層級：`#` 章、`##` 節、`###` 小節
- 色彩標記：`[COLOR:primary]文字[/COLOR]` 表示需套用主色

## 注意事項
- audience-profiles.md 和 content-templates.md 是參考資源，不修改
- PPT 格式每張投影片不超過 5 個要點
- Word/PDF 格式每章節有明確的段落分隔
- 所有輸出最終都回傳給 content-evaluator 進行評估
