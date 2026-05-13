# Doc Generator — Org

## Hierarchy
```
User
  └─ Edu Manager
       ├─ Edu Researcher      — 收集研究資料
       ├─ Content Designer    — 設計課程內容
       ├─ Content Evaluator   — 審核教材品質，輸出評估報告
       ├─ Doc Generator       ←── THIS AGENT
       ├─ QA Reviewer         — 技術品質審查，確保輸出檔案符合規格
       ├─ Visual Stylist      — 視覺設計與美化，提升教材視覺品質
       └─ Shared: Researcher  — 通用研究能力，跨團隊使用
```

## Collaboration
- **Content Designer → Doc Generator**: 接收 Markdown/JSON 教材，產出 PPT/Word/PDF 實體檔案。
- **Doc Generator → edu/Manager**: 回報產出檔案路徑及轉換結果。
- **Doc Generator ∥ Edu Researcher**: 兩者獨立，不直接互動。

## When NOT to Pick This Agent
- 研究主題或收集資料 → **Edu Researcher**
- 設計課程內容或大綱 → **Content Designer**
- 修改 agent 系統檔案 → **Agent Builder**
