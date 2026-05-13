# Styling Flow — edu/visual-stylist

完整的視覺設計流程，從讀取教材到輸出帶有視覺屬性的 PPT JSON。

## 1. 讀取教材內容

- 讀取 Content Designer 產出的 Markdown 草稿或 PPT JSON 結構
- 確認教材類型（投影片 / Word 文件 / PDF 參考）
- 識別每頁的主題標題與重點數量，作為版面規劃依據
- 若輸入不存在或格式無法識別：停止並回報，不繼續執行

## 2. 確認受眾 Profile

- 讀取 `agents/edu/content-designer/workflow/audience-profiles.md`
- 根據 profile 決定視覺策略：
  - **executive**：簡潔大字、少子彈、高對比色
  - **developer**：程式碼友善字型、淺色背景、資訊密度較高
  - **power-user**：圖表優先、資料可視化、標準企業色調
- 若 profile 檔案不存在：預設使用 executive 策略，在報告中標記「profile 未確認」

## 3. 制定視覺規範

- 參照 `agents/edu/content-designer/workflow/brand-colors-guide.md` 取得品牌色票
- 輸出視覺規範（Visual Spec），包含：
  - **配色方案**：主色 / 輔色 / 強調色（hex code）
  - **字型選擇**：標題字型、內文字型、程式碼字型（若適用）
  - **版面結構**：每頁最多重點數（3 / 5 / 7）、圖片位置
  - **投影片主題**：背景樣式、標題框樣式、內文框樣式
- 若品牌色票不存在：使用系統預設（白底 / 深灰字 / 藍色強調），標記於報告

## 4. 修改 PPT JSON 加入 Styling 屬性

- 在每個 slide 物件中加入 `style` 欄位，包含：
  - `background_color`、`title_font`、`body_font`
  - `accent_color`、`max_bullets`
- 不改動 `content` 欄位（文字內容由 Content Designer 負責）
- 若修改失敗（格式錯誤、欄位衝突）：診斷後重試一次，仍失敗則返回 Visual Spec 並附上手動套用說明

## 5. 提供 Word / PDF 格式建議

- 輸出 `word_style_notes`：段落樣式（Heading 1/2、Body Text）、行距、邊距
- 輸出 `pdf_export_notes`：字型嵌入建議、頁碼位置、封面設計提示
- 此步驟為建議性輸出，不阻擋流程；失敗時略過並標記

## 6. 產出摘要

```
## 視覺設計摘要

### 受眾 Profile
- 類型：{executive / developer / power-user}
- 視覺策略：{說明}

### 視覺規範
- 主色：{hex}　輔色：{hex}　強調色：{hex}
- 標題字型：{name}　內文字型：{name}
- 每頁最多重點：{N}

### 產出
- [ ] PPT JSON 已加入 style 屬性
- [ ] Word 格式建議（word_style_notes）
- [ ] PDF 匯出建議（pdf_export_notes）

### 警告 / 標記事項
（profile 未確認 / 品牌色票缺失 / 手動套用說明）
```

## 錯誤處理

| 情況 | 處理方式 |
|------|---------|
| 教材內容不存在 | 停止並回報，等待重新分派 |
| profile 缺失 | 預設 executive 策略，報告中標記 |
| 品牌色票缺失 | 使用系統預設色，報告中標記 |
| PPT JSON 修改失敗 | 重試一次；仍失敗則返回 Visual Spec + 手動說明 |
