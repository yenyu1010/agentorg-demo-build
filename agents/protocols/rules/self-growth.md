# Self-Growth Protocol

## 1. 設計原則
Agent 可以透過「反思 → 提案 → 核准 → 應用」的閉環實現自我改進。
遵守 Cardinal Rule：加法自己來，減法和擴權要審批。

## 2. 觸發條件（三選一即觸發）
| 觸發類型 | 條件 | 說明 |
|---------|------|------|
| 任務計數 | 每完成 10 次任務 | 從 worklog 統計 |
| 失敗觸發 | 當次任務 status = failed | 立即反思 |
| 使用者糾正 | 使用者指出錯誤 | 記錄並反思 |

## 3. 自我反思流程（Retrospective Loop）

### Phase 0: Eligibility Check（前置篩選）<!-- self-added 2026-04-26 -->
在對任何 agent 執行 self-growth 分析之前，先確認其 eligibility：

1. 若 agent 目錄下存在 `notes.md`，讀取其 frontmatter
2. 若 frontmatter 包含 `self_growth_eligible: false`，則**跳過**此 agent 的所有 self-growth 步驟
3. 記錄跳過的 agent（在 dispatch 報告中列出 `skipped_agents`）

**適用案例：** `agents/paperclip-imported/*/notes.md` 的 5 個 agent 均標記 `self_growth_eligible: false`，Evolution 執行 self-growth scan 時應自動跳過這些 agent。

### Step 1: 收集數據
- 讀取自己最近 10 筆 worklog（或自上次反思以來）
- 統計：completed 率、平均 duration_seconds、failed 任務的 input_summary

### Step 2: 識別模式
- 是否有反覆出現的 failed 任務類型？
- 是否有特定任務耗時異常（> 2x 平均）？
- 是否有使用者糾正紀錄？

### Step 3: 提出改進
每個改進點必須有：
- 問題描述（引用具體 worklog task_id）
- 改進方向
- 預期效果

### Step 4: 分類執行
- 免審批 → 直接執行（見第 4 節）
- 需審批 → 提案給 Agent Builder + Governance（見第 5 節）

### Step 5: 記錄反思
存入 agents/{team}/{agent}/memory/retrospective-{YYYY-MM-DD}.md

## 4. 可自行改進的範圍（免審批）
遵循 definitions.md Self-Update Rules：
- 新增 skill 到 skills.md — 標記 <!-- self-added {date} -->
- 新增 workflow step 到 workflow.yaml — 標記 # self-added {date}
- 新增/更新 memory/ 中的記憶

## 5. 需要審批的改進
提交給 Agent Builder + Governance：
- 修改現有 soul.md 原則
- 修改 tools.md
- 刪除現有 skills
- 修改或刪除現有 workflow steps

### 提案格式
（見下方模板）

## 6. 成長指標（以 worklog 數據衡量）
| 指標 | 計算方式 | 目標方向 |
|------|---------|---------|
| 任務完成率 | completed / total | ↑ 升高 |
| 平均耗時 | avg(duration_seconds) | ↓ 降低 |
| 失敗恢復率 | recovered / total_failures | ↑ 升高 |
| 技能覆蓋度 | skills used / skills requested | ↑ 升高 |

## 7. 提案模板

---
type: self-growth-proposal
agent: {agent-name}
date: {YYYY-MM-DD}
trigger: task_count | failure | user_correction
evidence: [worklog task_ids]
---

### 問題描述
{具體描述，引用 worklog 數據}

### 改進方案
{改什麼、怎麼改}

### 預期效果
{可量化的改進指標}

### 影響範圍
{影響哪些其他 agent 或流程}

## 8. 禁止行為
- 在沒有 worklog 證據的情況下提案
- 將一次性反饋擴大為系統性改進
- 繞過審批直接修改受保護檔案

## 9. 與現有協議的關係
- 引用 definitions.md §Self-Update Rules
- 引用 memory-protocol.md（反思記錄格式）
- 引用 worklog-protocol.md（觸發計數來源）
- 引用 evolution-protocol.md（需 Agent Builder 的改進路徑）
