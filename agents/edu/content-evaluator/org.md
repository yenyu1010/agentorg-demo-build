# Content Evaluator — Org

## Hierarchy

```
User
  └─ Edu Manager
       ├─ Edu Researcher      — 收集系統資料 + 外部資料，輸出結構化摘要
       ├─ Content Designer    — 設計教材內容，輸出草稿
       ├─ Content Evaluator   ←── THIS AGENT
       ├─ Doc Generator       — 將教材草稿轉換為最終格式（PPT/Word/PDF）
       ├─ QA Reviewer         — 技術品質審查，確保輸出檔案符合規格
       ├─ Visual Stylist      — 視覺設計與美化，提升教材視覺品質
       └─ Shared: Researcher  — 通用研究能力，跨團隊使用
```

## Collaboration

- **Content Designer → Content Evaluator**: Designer 輸出教材草稿（Markdown），Evaluator 審核並產出評估報告（PASS/REVISE/FAIL + 具體建議）。
- **Content Evaluator → Content Designer**: REVISE/FAIL 時，回傳評估報告，Designer 根據建議修改後再送審。
- **Content Evaluator → Doc Generator**: PASS 後，Edu Manager 派出 Doc Generator 進行格式轉換。

## Flow in Edu Pipeline

```
Research → Design → [Evaluate → (REVISE loop)] → Generate
```

PASS 才能進入 Doc Generator。FAIL 回退至 Edu Manager 決定是否重新 Design。

## When to Pick This Agent

- Content Designer 完成草稿，需要品質審核
- 需要確認學習目標符合 Bloom's Taxonomy
- 需要設計嵌入式評量題目
- 需要受眾適配性檢查

## When NOT to Pick This Agent

- 需要撰寫或修改教材內容 → **Content Designer**
- 需要轉換教材格式（PPT/Word/PDF） → **Doc Generator**
- 需要搜尋外部資料 → **Edu Researcher**
- 需要修改 agent 系統檔案 → **Agent Ops Team**
