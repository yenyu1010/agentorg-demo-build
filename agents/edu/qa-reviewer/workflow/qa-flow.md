# QA Flow — edu/qa-reviewer

完整的品質審查流程，從讀取原始草稿到產出 PASS/FAIL 報告。

## 1. 讀取原始教材草稿

- 讀取 Content Designer 產出的原始 Markdown 草稿（對照基準）
- 記錄草稿中的：章節數量、重點條目總數、圖表數量（若有）
- 若草稿不存在：停止並回報「無基準草稿，無法進行內容對照」，不繼續執行

## 2. 用 Bash 檢查每個產出檔案

> **注意：** 產出檔案使用中文命名（遵循 `agents/protocols/rules/naming-convention.md`），Bash 指令需正確處理 UTF-8 路徑。

對 Doc Generator 輸出目錄中的每個檔案執行：

**存在性與大小檢查**
```bash
ls -la {output_dir}/*.{xlsx,pptx,docx,pdf}
```
- 每個檔案必須存在且 size > 0 bytes

**PPTX 頁數驗證**
```bash
python -c "from pptx import Presentation; p=Presentation('{file}'); print(len(p.slides))"
```
- 投影片數量應與草稿章節數一致（±1 頁容差）

**DOCX 基本驗證**
```bash
python -c "from docx import Document; d=Document('{file}'); print(len(d.paragraphs))"
```
- 段落數 > 0

**PDF 格式驗證**
```bash
file {file}   # 確認為 PDF 格式
pdfinfo {file} | grep Pages   # 確認頁數 > 0
```

若任一檔案檢查失敗：記錄檔案名稱與失敗原因，繼續檢查其他檔案

## 3. 比對原始草稿 vs 最終檔案

- 比對草稿中每個章節標題是否出現在最終 PPT / Word 中
- 比對重點條目數量：最終產出條目數 ≥ 草稿條目數 × 0.9（允許 10% 精簡）
- 檢查是否有草稿內容被完全遺漏（整個章節消失）
- 若對照無法進行（檔案無法讀取）：停止並回報，不得宣告 PASS

## 4. 產出 QA 報告

```
## QA 報告

### 審查對象
- 原始草稿：{draft_path}
- 審查檔案：{output_dir}

### 檢查結果

| 項目 | 結果 | 說明 |
|------|------|------|
| PPTX 存在且非空 | PASS/FAIL | {說明} |
| PPTX 頁數符合 | PASS/FAIL | 草稿 {N} 章節 vs 投影片 {M} 頁 |
| DOCX 存在且非空 | PASS/FAIL | {說明} |
| PDF 存在且格式正確 | PASS/FAIL | {說明} |
| 章節標題完整 | PASS/FAIL | 缺失：{列表} |
| 重點條目完整度 | PASS/FAIL | 草稿 {N} 條 vs 產出 {M} 條 |

### 整體判定：PASS / FAIL

### Bug List
| # | 檔案 | 頁碼/位置 | 問題描述 | 嚴重度 |
|---|------|----------|---------|--------|
| 1 | {file} | {page} | {desc} | HIGH/MED/LOW |

### 建議
（提供給 Doc Generator 或 Content Designer 的改善建議）
```

## 5. 嚴重度定義

| 嚴重度 | 定義 |
|--------|------|
| HIGH | 內容遺漏、檔案損毀、無法開啟 |
| MED | 格式錯誤、版面跑版、頁數不符 |
| LOW | 字型不一致、小排版問題 |

## 錯誤處理

| 情況 | 處理方式 |
|------|---------|
| 草稿不存在 | 停止並回報，等待重新分派 |
| 產出檔案全部缺失 | 立即 FAIL，回報 Doc Generator 未完成 |
| 部分檔案缺失 | 針對缺失項目記錄 HIGH bug，其餘繼續審查 |
| 對照無法進行 | 停止並回報，不得宣告 PASS |
| 頁數驗證工具不可用 | 標記「頁數未驗證」，降級為 MED 警告 |
