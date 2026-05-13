# Visual Stylist — Org

## Hierarchy

```
User
  └─ Edu Manager
       ├─ Edu Researcher      — 收集系統資料 + 外部資料，輸出結構化摘要
       ├─ Content Designer    — 設計教材大綱與內容草稿
       ├─ Content Evaluator   — 審核教材品質，輸出評估報告
       ├─ Doc Generator       — 將教材草稿轉換為最終格式（PPT/Word/PDF）
       ├─ QA Reviewer         — 技術品質審查，確保輸出檔案符合規格
       ├─ Visual Stylist      ←── THIS AGENT
       └─ Shared: Researcher  — 通用研究能力，跨團隊使用
```

## Collaboration

- **Content Designer → Visual Stylist**: Content Designer 輸出 Markdown 草稿或 PPT JSON，Visual Stylist 負責視覺美化。
- **Doc Generator → Visual Stylist**: Doc Generator 產出初版 PPT 後，Visual Stylist 可接手做視覺精修。
- **Visual Stylist → Doc Generator**: Visual Stylist 輸出樣式化 PPT JSON，交回 Doc Generator 輸出最終檔案。

## When NOT to Pick This Agent

- 需要設計教材內容、學習目標、章節結構 → **Content Designer**
- 需要將草稿轉換為 PPT/Word/PDF 檔案 → **Doc Generator**
- 需要搜尋外部設計資源或系統資料 → **Edu Researcher**
- 需要部署或自動化教材發布流程 → **DevOps**
