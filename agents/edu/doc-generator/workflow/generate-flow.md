# Generate Flow — edu/doc-generator

完整的文件生成流程，從讀取帶樣式的內容到產出可交付的 XLSX / DOCX / PPTX 檔案（PDF 為可選次要輸出）。

## 1. 讀取 Styled Content

- 讀取 Visual Stylist 產出的 PPT JSON（含 `style` 屬性）或 Markdown 草稿
- 確認目標格式清單（XLSX / DOCX / PPTX 為預設三選一；PDF 為次要選項，僅使用者明確要求時加入）
- 確認輸出目錄路徑（由 Manager task 指定，預設 `output/`）
- 產出檔名使用繁體中文（遵循 `agents/protocols/rules/naming-convention.md`）；中間產物（tmp/、merge 暫存）維持英文
- 若輸入檔案不存在或格式無法識別：停止並回報，不繼續執行

## 套件策略（Fail-Fast）<!-- updated 2026-04-15 -->
不做預先驗證。直接執行：
1. 優先：呼叫 anthropic-skills:pptx / docx / xlsx
2. 若 Skill 工具不可用 → 嘗試本地腳本
3. 若本地腳本也失敗 → 回報錯誤給 Manager，由 Manager 決定

移除一切 `pip install`、`pip check`、`import` 預驗證步驟。

## 2. 根據目標格式選擇工具鏈

| 目標格式 | 工具 | 輸入 | 備註 |
|---------|------|------|------|
| Excel (.xlsx) | `anthropic-skills:xlsx` 或 `openpyxl`（`scripts/xlsx_generator.py`） | JSON 結構化資料 | **預設格式之一** |
| Word (.docx) | `anthropic-skills:docx` 或 `python-docx`（`scripts/gen-docx.py`） | Markdown | **預設格式之一** |
| PPT (.pptx) | `anthropic-skills:pptx` 或 `python-pptx`（`scripts/gen-pptx.py`） | PPT JSON | **預設格式之一** |
| PDF (.pdf) | `libreoffice --headless --convert-to pdf`（`scripts/gen-pdf.sh`） | Word (.docx) | **次要格式，僅使用者明確要求時執行** |

- PDF 必須先完成 Word 生成（依賴關係），且僅在使用者明確要求時才執行
- 若格式不在上表中：回報「不支援的格式」，不嘗試其他方法

## 3. 執行生成腳本

對每個目標格式依序執行：

**Excel 生成**
```
python scripts/xlsx_generator.py --input {json_path} --output {output_dir}/{filename}.xlsx
```
（或使用 `Skill(skill="anthropic-skills:xlsx")` 原生產出）

**Word 生成**
```
python scripts/gen-docx.py --input {md_path} --output {output_dir}/{filename}.docx
```

**PPT 生成**
```
python scripts/gen-pptx.py --input {json_path} --output {output_dir}/{filename}.pptx
```

**PDF 生成**（次要格式，依賴 Word 先完成；僅使用者明確要求時執行）
```
bash scripts/gen-pdf.sh {output_dir}/{filename}.docx {output_dir}/{filename}.pdf
```

- 每個腳本失敗時：記錄腳本名稱、錯誤訊息、輸入路徑，重試最多 2 次
- 2 次重試後仍失敗：回報該格式失敗，繼續處理其他格式

## 4. 驗證產出檔案

對每個應生成的檔案執行：
- `ls -la {output_path}` — 確認檔案存在
- 檔案大小 > 0 bytes
- 若為 PDF：`pdfinfo {file}` 或 `file {file}` 確認格式正確

若驗證失敗：重試生成一次；仍失敗則回報哪些檔案缺失或為空

## 5. 驗證企業標準合規

對每個生成的 PPT 執行以下企業標準檢查（參考 `workflow/ppt-standards.md`）：

### 尺寸驗證
- 確認投影片寬度 = 10"
- 確認投影片高度 = 7.5"

### 色彩驗證
- 確認主色（標題、背景）= #61B520（品牌綠）
- 確認輔色（副標題、邊框）= #D6EFA8（淺綠底色）
- 確認強調色（CTA）= #5DABE2（品牌藍）

### 字體驗證
- 確認所有文字使用 Calibri 字體族
- 標題使用 Bold 粗體

### 邊距驗證
- 確認四周邊距 ≥ 0.3"
- 確認內容寬度 ≤ 9"

### 不符合處理
- 不符合標準的 PPT 視為生成失敗
- 記錄不符項目清單（尺寸/色彩/字體/邊距中的哪些）
- 需重新執行第 3 章「執行生成腳本」進行修復

## 7. 產出摘要

```
## 文件生成摘要

### 輸入
- 來源：{styled_json / markdown}
- 目標格式：{XLSX / DOCX / PPTX}（PDF 為次要，僅使用者明確要求時列入）

### 產出檔案
- [ ] {中文檔名}.xlsx　{size} bytes
- [ ] {中文檔名}.docx　{size} bytes
- [ ] {中文檔名}.pptx　{size} bytes
- [ ] {中文檔名}.pdf　{size} bytes（次要格式，僅明確要求時產出）

### 企業標準合規
- 尺寸檢查：PASS / FAIL （10" × 7.5"）
- 色彩檢查：PASS / FAIL （品牌綠 #61B520）
- 字體檢查：PASS / FAIL （Calibri）
- 邊距檢查：PASS / FAIL （≥ 0.3"）

### 失敗項目
（腳本名稱、錯誤訊息、重試次數）

### 交給 QA Reviewer
- 產出目錄：{output_dir}
- 原始草稿路徑：{source_md}（供內容對照用）
- 企業標準合規報告：{pass/fail 項目清單}
```

## 並行章節生成流程（Parallel Chapter Mode）<!-- updated 2026-04-15 -->

### 觸發條件
- 投影片總數 ≥ 10 張
- 或 Edu Manager 明確指定 parallel: true

### 流程圖
```
Edu Manager
  ├─ 並行派遣 N 個 doc-generator（每章一個）
  │   ├─ Agent 1 → tmp/ch1.pptx
  │   ├─ Agent 2 → tmp/ch2.pptx
  │   └─ Agent N → tmp/chN.pptx
  └─ 等所有章節完成後 → 派 Merge Agent
       └─ 合併 → 最終 PPTX → 清理 tmp/
```

### Merge Agent 合併腳本（優先用 anthropic-skills:pptx merge 功能）
若 anthropic-skills 不支援合併，使用本地 python-pptx：
```python
# scripts/merge_pptx.py（由 doc-generator 首次使用時自助建立）
from pptx import Presentation

def merge_presentations(input_files: list[str], output_file: str):
    merged = Presentation(input_files[0])
    for f in input_files[1:]:
        src = Presentation(f)
        for slide in src.slides:
            # 複製 slide 至 merged（保留 layout）
            ...
    merged.save(output_file)
```

### 注意事項
- 各章節 Agent 使用相同的 slide master / 配色（從 ppt-standards.md 載入）
- tmp/ 暫存檔命名：`tmp/workshop_ch{chapter_num}_{timestamp}.pptx`
- Merge 後必須驗證：總頁數 = 各章節頁數加總
- 清理 tmp/ 後再回報 Edu Manager

---

## 8. 錯誤處理

| 情況 | 處理方式 |
|------|---------|
| 輸入檔案不存在 | 停止並回報，等待重新分派 |
| 不支援的格式 | 回報，跳過該格式 |
| 腳本執行失敗 | 重試最多 2 次；附錯誤輸出後繼續其他格式 |
| 檔案驗證失敗 | 重試生成一次；仍失敗則列入缺失清單回報 |
| 企業標準不符 | 視為生成失敗，重新執行第 3 章生成腳本；記錄不符項目 |
