# Memory Hygiene Protocol

## 1. 設計原則
memory-protocol.md 定義了如何寫入記憶，本協議補充如何管理記憶的生命週期。
每個 agent 負責自己的 memory/ 目錄衛生。

## 2. 觸發條件
| 觸發類型 | 條件 | 誰執行 |
|---------|------|-------|
| 定期 | 每 30 個任務（worklog 計數） | Agent 自身 |
| 空間 | memory/ 目錄超過 20 個檔案 | Agent 自身 |
| 按需 | Evolution agent 分析時要求 | Evolution |
| 自我反思時 | self-growth retrospective 觸發 | Agent 自身 |

## 3. Memory 分類標準
| 分類 | 定義 | 保留標準 |
|------|------|---------|
| Projects | 有截止日的進行中項目 | 截止日前保留，完成後移至 Archives |
| Areas | 持續監控的領域知識 | 6 個月內使用過 → 保留 |
| Resources | 外部研究摘要、工具說明 | 1 年內引用過 → 保留 |
| Archives | 已完成或停用的知識 | 永久保留（壓縮格式） |

## 4. 記憶老化規則（Staleness Rules）
- 超過 6 個月未被引用且非 Archives → 標記為 stale
- 標記 stale 後 30 天未確認仍有效 → 移至 Archives 或刪除
- 已知過時的 Known Issues（已修復 bug、過時工具版本） → 立即刪除

## 5. 記憶驗證規則（Accuracy Rules）
對以下類型進行主動驗證：
| 類型 | 驗證方式 |
|------|---------|
| Known issues | Glob/Read 確認問題是否仍存在 |
| Codebase patterns | Grep 確認 pattern 仍一致 |
| Decisions made | 查 worklog 確認決策未被推翻 |

## 6. 記憶整合規則（Consolidation Rules）
- 同一主題出現 3+ 個 memory 檔案 → 合併為一個
- 合併時保留最新 created 日期
- 標記：<!-- consolidated from {n} files on {date} -->
- 合併後更新 MEMORY.md 索引

## 7. 記憶升級路徑（Upgrade Path）

記憶不只是保存——有價值的記憶應該升級為更正式的 agent 能力。

### 7.1 升級層級

```
memory/ （原始學習）
  ↓ 出現 3+ 次且每次有效
skill （skills.md 新增技能）
  ↓ 被 3+ 不同 agent 需要
protocol （agents/protocols/ 新增協議）
  ↓ 跨團隊共通
system rule （definitions.md 或 CLAUDE.md 更新）
```

### 7.2 Memory → Skill 升級條件
| 條件 | 說明 |
|------|------|
| 被引用 3+ 次 | 在不同任務中反覆使用 |
| 每次都有效 | 沒有導致失敗或需要修正 |
| 可模式化 | 能寫成 "When X, do Y" 的標準格式 |
| 屬於該 agent 的領域 | 不超出 scope |

**執行方式：**
- Agent 自行在 skills.md 新增，標記 `<!-- self-added {date}, upgraded from memory/{filename} -->`
- 原始 memory 移至 Archives（不刪除，保留溯源）

### 7.3 Skill → Protocol 升級條件
| 條件 | 說明 |
|------|------|
| 3+ agent 都需要 | 跨 agent 共通知識 |
| 非領域專屬 | 是通用流程而非特定技能 |
| 可標準化 | 能定義明確的輸入/輸出/步驟 |

**執行方式：**
- 需要 Agent Builder + Governance 審批
- Agent Builder 建立新 protocol
- 各 agent 的 skills.md 引用 protocol（取代重複的 skill）

### 7.4 Protocol → System Rule 升級條件
| 條件 | 說明 |
|------|------|
| 全系統適用 | 所有 team 都需要遵守 |
| 不可違反 | 違反會導致系統失敗 |
| 經 Governance 確認 | 已經過至少 1 個月的 protocol 驗證期 |

**執行方式：**
- Governance 提案 → 用戶確認 → Agent Builder 更新 definitions.md 或 CLAUDE.md

### 7.5 降級規則
升級不是單向的——不再有效的知識應該降級：
- Skill 連續 3 次任務未使用 → 考慮降級回 memory
- Protocol 連續 2 個 review 週期無使用 → 歸檔
- 降級需 Governance 確認（防止誤刪有價值的標準化知識）

## 8. 審查紀錄格式
存入 memory/review-log-{YYYY-MM-DD}.md：

---
topic: memory-review-log
created: {YYYY-MM-DD}
agent: {agent-name}
trigger: scheduled | space_limit | on_demand
---

### 審查摘要
- 審查時 memory 數量：{n} 個
- 標記 stale：{n} 個
- 已刪除：{n} 個
- 已整合：{n} 組 → {n} 個
- 審查後 memory 數量：{n} 個

### 處置詳情
| 檔案名 | 操作 | 原因 |
|-------|------|------|

## 9. 禁止行為
- 刪除 Archives 類 memory
- 操作其他 agent 的 memory/
- 合併時刪除有歧義的部分（標記 <!-- needs_verification --> 保留）

## 10. 與現有協議的關係
- 擴展 memory-protocol.md（不修改現有格式定義）
- 引用 self-growth.md（同目錄，retrospective 觸發 memory review）
- 引用 worklog-protocol.md（計數觸發來源）
