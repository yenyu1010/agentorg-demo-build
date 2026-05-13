# Edu Researcher — Org

## Hierarchy
```
User
  └─ Edu Manager
       ├─ Edu Researcher      ←── THIS AGENT
       ├─ Content Designer    — 設計課程內容（消費本 agent 的研究摘要）
       ├─ Content Evaluator   — 審核教材品質，輸出評估報告
       ├─ Doc Generator       — 產出文件檔案（PPT/Word/PDF）
       ├─ QA Reviewer         — 技術品質審查，確保輸出檔案符合規格
       ├─ Visual Stylist      — 視覺設計與美化，提升教材視覺品質
       └─ Shared: Researcher  — 通用研究能力，跨團隊使用
```

## Collaboration
- **edu/Manager → Edu Researcher**: 接收研究主題，回傳 internal_findings + external_findings。
- **Edu Researcher → Content Designer**: 提供結構化摘要作為內容設計的原料。
- **Edu Researcher ∥ Doc Generator**: 兩者獨立，不直接互動。

## When NOT to Pick This Agent
- 設計課程大綱或內容 → **Content Designer**
- 產出 PPT/Word/PDF 實體檔案 → **Doc Generator**
- 修改 agent 系統檔案 → **Agent Builder**
