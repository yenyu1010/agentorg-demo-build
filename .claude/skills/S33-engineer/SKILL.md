# S33-Engineer

## Skill Name
S33-engineer

## Description
工程師團隊入口。負責所有程式開發、Bug 修復、重構、技術問題解答與資訊系統相關任務。
透過 Manager → Analyst → Developer → Reviewer → Tester 的完整流程，確保交付品質。

## Trigger
使用者輸入 `/S33-engineer` 後附上任務描述，例如：
- `/S33-engineer 幫我寫一個 Python 爬蟲抓取商品價格`
- `/S33-engineer 我的 Node.js API 回傳 500 錯誤，幫我 debug`
- `/S33-engineer 重構這段 Java 程式碼讓它更好維護`

## Entry Point
啟動後，將使用者請求交給 `engineer/manager`，由 Manager 驅動完整開發流程。

## Dispatch
```yaml
agent: engineer/manager
model: sonnet
pass_user_query: true
```

## Scope
### 負責範圍
- 新功能開發（任何程式語言）
- Bug 修復與除錯
- 程式碼重構
- 技術問題解答（架構、演算法、工具選型）
- 腳本與自動化工具
- API 設計與整合

### 不負責範圍（轉介其他 Skill）
- 教育內容製作 → `/S33-edu`
- Agent 系統修改 → `/S33-agent`
- 法務合約問題 → `/S33-lawyer`

## Flow Summary
```
使用者 → /S33-engineer → engineer/manager
  → system-analyst（需求分析 + 設計）
  → [HITL 確認設計]
  → developer（實作程式碼）
  → code-reviewer（審查品質）
  → tester（測試驗證）
  → 交付報告（程式碼路徑 + 使用說明）
```
