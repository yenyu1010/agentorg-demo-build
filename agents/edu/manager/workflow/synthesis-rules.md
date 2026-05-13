# Edu Manager — Synthesis Rules

After all agents return, Edu Manager follows these rules:

## 1. Check Status

- `completed` → include in synthesis
- `failed` → retry once with refined prompt. If still fails, report gap to user with partial results.

## 2. Verify Output Files

Check all generated files:
- File path exists (Glob or Bash ls)
- File size > 0 bytes
- Format matches requested output_format

If verification fails, retry doc-generator once.

## 3. Synthesize Report

Report to user includes:
- 產出檔案路徑（每個 format 一行）
- 受眾 profile（audience_profile used）
- 內容摘要（3-5 bullet points from content-designer output）
- 教材章節結構（如有）

## 4. 工時打卡明細格式

依 Edu Manager soul.md 原則 #6：

**標準格式（agents >= 2）**：

```
| Agent | input_summary | output_summary | started_at | ended_at | duration_s | status |
|-------|---------------|----------------|------------|----------|------------|--------|
| edu-researcher | ... | ... | ... | ... | ... | completed |
| shared/researcher | ... | ... | ... | ... | ... | completed |
| content-designer | ... | ... | ... | ... | ... | completed |
| doc-generator | ... | ... | ... | ... | ... | completed |
| **總計** | 4 agents | | | | {total}s | {pass}/{fail} |
```

- 時間來自 worklog JSON 的實際時間戳，不得粗估
- 所有被派遣的 agent 都必須出現
- 缺 worklog 或 failed 的 agent 標註原因

## 5. Failure Recovery

| Situation | Action |
|-----------|--------|
| edu-researcher 失敗 | Retry once；若再失敗，僅用 shared/researcher 結果繼續 |
| content-designer 失敗 | Retry once with more structured prompt |
| doc-generator 失敗 | Retry once；若再失敗，交付 content_draft（Markdown 格式）給使用者 |
| 全部失敗 | 誠實回報，建議使用者改用 /dev 協助診斷 |
