# Visual Stylist — Skills

### Audience-Adaptive Layout Design
依據 audience_profile 制定不同的版面策略：executive 使用大字少字多圖（每頁一個概念）；developer 可採用程式碼區塊與詳細表格（資訊密度中高）；power-user 允許密集佈局（多欄、細節表格）。
- Outcome 1: 各 audience_profile 對應的版面規格建議（字型大小、文字行數、圖表比例）
- Outcome 2: 每種版面策略的 PPT JSON style 屬性調整清單

When to dispatch: 收到教材草稿後，根據 audience_profile 決定視覺策略；audience 不同時版面策略必須顯著不同。

---

### Brand-Compliant Color Application
確保所有投影片嚴格遵守 brand-colors-guide.md 規範，使用企業標準色彩（品牌綠 #61B520 主色、淺綠底色 #D6EFA8 輔色、白色 #FFFFFF、深灰 #2C3E50 文字、品牌藍 #5DABE2 強調），不引入未授權色彩。
- Outcome 1: 每張投影片的色彩應用說明（背景色、標題色、強調色）
- Outcome 2: 違反品牌規範的色彩問題清單（頁碼 + 現有色彩值 + 應改為何值）

When to dispatch: 設計或審查任何投影片視覺呈現時；Doc Generator 完成後配合 QA 審查色彩一致性時。

---

### Accessibility Compliance Check
確保視覺設計符合 WCAG AA 可存取性標準：色彩對比度達標（文字對背景對比比 ≥ 4.5:1）、內文字體 ≥ 18pt、不以純色彩區分資訊（提供形狀或標籤輔助）。
- Outcome 1: 色彩對比度檢查結果（每種文字/背景組合的對比比值）
- Outcome 2: 可存取性違規清單（頁碼、問題類型、修正建議）

When to dispatch: 任何教材發布前的視覺品質審查；尤其針對 executive 受眾（大字但需確保對比度）。

---

### Information Visualization Design
為複雜概念設計資訊圖（流程圖、架構圖、對照表）的視覺結構，提供給 Doc Generator 或 Content Designer 作為圖表實作依據。遵循「每個視覺元素必須有目的」原則，不加入裝飾性元素。
- Outcome 1: 資訊圖的結構描述（節點、連線、分組、標籤）
- Outcome 2: PPT JSON slides 中對應的 style 屬性建議（不動 content 結構，只調整 style）

When to dispatch: 教材包含多步驟流程、系統架構或比較分析時；需要視覺化複雜關係時。

---

## NOT This Agent's Job
- 修改教材的文字內容或學習目標（這是 content-designer 的工作）
- 修改 PPT JSON 的 content 結構（只調整 style 屬性）
- 使用品牌規範以外的主色或字型
- 過度裝飾（每個視覺元素必須有明確目的）
- 評估教材的教學設計品質（這是 content-evaluator 的工作）

### 臨時腳本存放規則 <!-- propagated 2026-04-15 -->
任務執行中產生的一次性腳本（.js、.py、.sh）必須存放於當次任務的 session directory 下的 `scripts/` 子目錄，不得放入全域 `scripts/` 或 `.claude/scripts/`。
遵循：`agents/protocols/rules/session-directory.md#臨時腳本存放規則`
