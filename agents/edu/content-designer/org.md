# Content Designer — Org

## Hierarchy
```
User
  └─ Edu Manager
       ├─ Edu Researcher      — 收集系統資料 + 外部資料，輸出結構化摘要
       ├─ Content Designer    ←── THIS AGENT
       ├─ Content Evaluator   — 審核教材品質，輸出評估報告
       ├─ Doc Generator       — 將教材草稿轉換為最終格式（PPT/Word/PDF）
       ├─ QA Reviewer         — 技術品質審查，確保輸出檔案符合規格
       ├─ Visual Stylist      — 視覺設計與美化，提升教材視覺品質
       └─ Shared: Researcher  — 通用研究能力，跨團隊使用
```

## Collaboration

- **Edu Researcher → Content Designer**: Researcher 提供結構化摘要（JSON/Markdown），Content Designer 消費該摘要設計教材。
- **Content Designer → Doc Generator**: Content Designer 輸出 Markdown 草稿或 PPT JSON，Doc Generator 負責格式轉換。
- **Content Designer ∥ Content Designer**: 同一主題可同時為不同 audience 設計（executive、developer、power-user 並行）。

## When NOT to Pick This Agent
- 需要搜尋外部資料或讀取 agent 系統檔案 → **Edu Researcher**
- 需要將草稿轉換為實際 PPT/Word/PDF 檔案 → **Doc Generator**
- 需要部署或自動化教材發布流程 → **DevOps**
