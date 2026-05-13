# Agent Anatomy Rules

## 1. 適用範圍
所有 agents/ 目錄下的 agent 都必須遵守此規範。

## 2. 角色分類
### 分類判定條件

| Type | 判定條件 |
|------|---------|
| Officer (L4) | agent.yaml 中 type == "officer"，reports_to == "user"，管理多個 Director |
| Director (L3) | agent.yaml 中 type == "director"，reports_to 為 officer 或 "user"，管理多個 Manager |
| Manager (L2) | agent.yaml 中 type == "manager"，reports_to 為 director 或 "user"（向下相容），管理多個 Worker |
| Worker (L1) | agent.yaml 中 type == "worker"，reports_to 為某個 manager，無下屬 |

**層級關係（低→高）**：Worker (L1) → Manager (L2) → Director (L3) → Officer (L4) → user

> **向下相容注意**：現有 Manager 的 reports_to == "user" 仍然合法（表示尚未導入 Director/Officer 層）。

### 舊判定條件（保留供參考）
- **Manager / Orchestrator**：agent.yaml 中 reports_to == "user" 或有下屬 agent 向其回報；tools.md 包含 Agent 工具；workflow.yaml 包含 dispatch_agent 或 dispatch_agents_parallel 動作
- **Worker**：agent.yaml 中 reports_to 指向某個 manager；tools.md 不包含 Agent 工具；無下屬

## 3. 通用必備檔案（所有 Type 共用）
| 檔案 | 必備 | 用途 | 可編輯者 |
|------|:----:|------|---------|
| agent.yaml | ✅ | 入口：bootstrap 順序、dispatch 路由 | Agent Builder only |
| soul.md | ✅ | 人格、原則、反模式 | Agent Builder only |
| tools.md | ✅ | 系統能力授權 | Agent Builder only |
| skills.md | ✅ | 領域專業知識 | Agent 可新增；刪除/修改需審批 |
| org.md | ✅ | 組織角色與回報關係 | Agent Builder only |
| workflow.yaml | ✅ | 執行工作流步驟 | Agent 可新增步驟；刪除/修改需審批 |
| memory/MEMORY.md | ✅ | 持久記憶索引 | Agent 自主讀寫 |
| worklog/.gitkeep | ✅ | 執行日誌目錄 | Agent 自主寫入 |

### 3.1 禁止出現的目錄（Hard Rule）

agent 資料夾只能放**身份與行為定義**，禁止出現任務產物目錄。以下目錄一律禁止：

| 禁止目錄 | 說明 |
|---------|------|
| `output/` | 任務產物 |
| `deliverables/` | 交付物 |
| `artifacts/` | 產出檔案 |
| `products/` | 產品/成品 |

所有任務產物必須寫到 `<CWD>/output/{team}/{task_id}/`，由 Manager 派遣時傳遞 `output_path` 參數決定。

**⚠️ 禁止目錄**：agent 資料夾下禁止出現任何任務產物目錄（`output/`, `deliverables/`, `artifacts/`, `products/`）。詳見下方 §3.1 與 [`output-placement.md`](output-placement.md)。

`output-placement.md` 是本規則在產物放置方面的詳細延伸規範（從屬補充）。

## 3.5 tools.md MCP 工具集規範

### 目的
Subagent 在 Cowork 環境下自動繼承所有已連接的 MCP 工具（desktop-commander、gmail、calendar、workspace__bash、memory 等）。tools.md 必須明確列出該 agent 被授權使用的 MCP 工具，讓 agent 知道自己的完整能力。

### tools.md 必含段落
1. **Primary Tools** — 核心工具（Agent 用於 Manager、Read/Write/Edit 用於 Worker 等）
2. **MCP Tools (Authorized)** — 該 agent 被授權使用的 MCP 工具及其用途。參考 `agents/protocols/mcp-registry.md`
3. **Do NOT Use** — 明確禁止的工具

### MCP 工具分類（依 mcp-registry.md）
| 類別 | 工具前綴 | 適用場景 |
|------|---------|---------|
| 檔案系統（Google Drive） | mcp__desktop-commander__ | 讀寫 T:\ 路徑檔案。**注意**：read_file 在 T:\ 只回傳 metadata，必須用 read_multiple_files（見 google-drive-read.md） |
| Shell 執行 | mcp__workspace__bash | 執行腳本（worklog.sh 等） |
| Gmail | mcp__b1592d31*__gmail_* | 郵件操作 |
| Google Calendar | mcp__972626e3*__* | 日曆操作 |
| Memory（Knowledge Graph） | mcp__memory__* / mcp__server-memory__* | 持久化知識圖譜 |
| Chrome 瀏覽器 | mcp__Claude_in_Chrome__* | 網頁自動化 |
| 網路搜尋 | WebSearch, mcp__workspace__web_fetch | 線上搜尋與擷取 |

### Agent 職責→工具集對應原則
- **所有 agent**：desktop-commander（讀寫 T:\）、workspace__bash（worklog 打卡）
- **需要研究的 agent**：加上 WebSearch、web_fetch、Chrome
- **需要溝通的 agent**：加上 Gmail、Calendar
- **需要記憶的 agent**：加上 memory / server-memory
- **Manager 專屬**：Agent 工具（subagent 無法使用）、ToolSearch（subagent 無法使用）

## 4. agent.yaml 必填欄位
詳見 `agents/protocols/definitions.md` §Agent Entry Point Schema。必填欄位：`agent`、`title`、`display_name`、`team`、`type`、`reports_to`、`bootstrap`（順序：soul.md → org.md → tools.md）、`workflow`、`dispatch.model`、`dispatch.trigger`、`dispatch.not_for`。

| 欄位 | 說明 |
|------|------|
| `title` | agent 的英文職稱，用於系統內部識別與 dispatch 路由。 |
| `display_name` | 用戶可見的繁體中文顯示名稱。用於報告、worklog 明細、deliver 步驟中面向用戶的輸出。遵循 `naming-convention.md`：用戶看到的用中文，系統內部用英文 `title`。 |

**`type` 欄位允許值**：`worker | manager | director | officer`

> 現有 agent.yaml 若未含 `type` 欄位，依 reports_to 推斷：reports_to == "user" 視為 manager，否則視為 worker。新建 agent 必須明確填寫 type。

## 5. soul.md 通用規範
### 必含章節
- Identity（身份描述，必須獨特不可複製貼上）
- Principles（至少 4 條原則）
- Anti-patterns（至少 3 條反模式）

### 必含原則
- 打卡是天條（worklog 首尾必執行）
- Scope Guard（超出領域必須拒絕）
- 計算委派（任何數學計算必須委派 shared/calculator，不可心算）
- 回饋偵測（偵測用戶正/負面回饋語意，觸發 memory 保存，依 feedback-memory.md）
- 逐次驗證（每個 worker 完成後立即驗證其聲稱與實際產出一致，依 inline-verify-flow.md）

## 6. Manager 專屬規範
### soul.md 必含原則（8 條）
1. Never do the work yourself
2. Maximize parallelism
3. Pick the right agent
4. Brief thoroughly
5. Every agent punches their own clock
6. Fail gracefully
7. Respond in user's language
8. Split large tasks

### workflow.yaml 必含步驟
log_start → feedback_detect → classify/route → [hitl_gate] → execute → [governance] → verify → synthesize → deliver → log_end
- feedback_detect 引用共用流程：`agents/protocols/workflows/feedback-detect-flow.md`
- 方括號步驟可選但建議
- hitl_gate 建議包含：依 hitl-protocol.md 判斷風險等級，Tier 3 操作暫停等待用戶 `confirm` / `abort` / `modify` 嚴格 token
- synthesize 必須獨立（不可埋在 deliver 子動作）
- classify 步驟必須包含回饋偵測（依 agents/protocols/rules/feedback-memory.md）
- 偵測到用戶回饋時，先保存 memory 再繼續處理任務
- execute 步驟必須包含 inline verification：每次 agent 返回後依 `agents/protocols/workflows/inline-verify-flow.md` 逐項驗證，通過才派下一個

### skills.md 必含技能
- Task Decomposition
- Agent Selection / Dispatch
- Result Synthesis

### tools.md
- 必須含 Agent 工具
- 必須包含 "MCP Tools (Authorized)" 章節，列出該 Manager 被授權使用的 MCP 工具（參考 §3.5）

### Worklog
- 使用 Manager-Specific Fields（dispatch_summary）
- 報告末尾必含打卡明細表

## 6.5 Director 專屬規範
Director 規範是 Manager 規範的**超集**（繼承所有 Manager 要求並新增以下）。

### soul.md 必含原則（10 條）
1–8. 同 Manager 原有 8 條
9. Cross-team coordination — 跨 team 任務時，協調相關 Manager 的優先順序與資源
10. Escalation judgment — 判斷何時需上報 Officer 決策，何時自行處理

### workflow.yaml 必含步驟
log_start → feedback_detect → classify → dispatch_managers → [hitl_gate] → synthesize → deliver → log_end
- feedback_detect 引用共用流程：`agents/protocols/workflows/feedback-detect-flow.md`
- hitl_gate 依 hitl-protocol.md 判斷，跨 team 操作建議納入
- dispatch_managers 必須支援並行派遣多個 Manager
- classify 步驟必須包含回饋偵測（依 agents/protocols/rules/feedback-memory.md）
- 偵測到用戶回饋時，先保存 memory 再繼續處理任務
- dispatch_managers 步驟必須包含 inline verification：每次 Manager 返回後依 `agents/protocols/workflows/inline-verify-flow.md` 逐項驗證，通過才派下一個

### skills.md 必含技能
- Multi-team Coordination
- Manager Selection & Dispatch
- Cross-team Result Synthesis
- Resource Prioritization

### tools.md
- 必須含 Agent 工具
- 可派遣 Manager 和 Worker
- 必須包含 "MCP Tools (Authorized)" 章節，列出該 Director 被授權使用的 MCP 工具（參考 §3.5）

### Worklog
- 使用 Manager-Specific Fields（dispatch_summary）
- 報告末尾必含打卡明細表及跨 team 協調摘要

## 6.6 Officer 專屬規範
Officer 規範是 Director 規範的**超集**（繼承所有 Director 要求並新增以下）。

### soul.md 必含原則（12 條）
1–10. 同 Director 原有 10 條
11. Strategic vision — 從組織整體角度評估任務優先順序，非單一 team 視角
12. Policy authority — 有權制定跨組織政策，但修改需經 Governance 審查

### workflow.yaml 必含步驟
log_start → feedback_detect → strategic_classify → dispatch_directors → [hitl_gate] → synthesize → policy_check → deliver → log_end
- feedback_detect 引用共用流程：`agents/protocols/workflows/feedback-detect-flow.md`
- hitl_gate 依 hitl-protocol.md，Officer 層操作預設為高風險，建議強制啟用
- policy_check 必須在 deliver 前執行，確認輸出符合組織政策
- strategic_classify 步驟必須包含回饋偵測（依 agents/protocols/rules/feedback-memory.md）
- 偵測到用戶回饋時，先保存 memory 再繼續處理任務
- dispatch_directors 步驟必須包含 inline verification：每次 Director 返回後依 `agents/protocols/workflows/inline-verify-flow.md` 逐項驗證，通過才派下一個

### skills.md 必含技能
- Organizational Strategy
- Director Selection & Dispatch
- Cross-organization Synthesis
- Policy Making & Enforcement

### tools.md
- 必須含 Agent 工具
- 可派遣 Director、Manager（跳級派遣允許，但需記錄原因）
- 必須包含 "MCP Tools (Authorized)" 章節，列出該 Officer 被授權使用的 MCP 工具（參考 §3.5）

### Worklog
- 使用 Manager-Specific Fields（dispatch_summary）
- 報告末尾必含打卡明細表、跨組織協調摘要及政策決策記錄

<!-- self-added 2026-04-27 — dispatch-path rollout -->
## 6.7 Manager Dispatch Prompt 必含 Worker Bootstrap Paths（Hard Rule）

**規則**：Manager（含 Director / Officer，凡有派遣行為的角色）派遣 worker 時，dispatch prompt 必須在 Identity Block 列出 worker 的 4 個 bootstrap 檔案絕對路徑：
- `agent.yaml`
- `soul.md`
- `org.md`
- `tools.md`

**理由**：worker subagent 從零開始無 context。若 prompt 只寫「You are the X agent」而不給 path，worker 必須先反查 dispatch caller（manager）才能找到自己的定義，浪費 round trip 與 token。違反 Manager soul.md Principle 4「Brief thoroughly — 從零開始就要 context 完整」精神。

**範本**：
```
You are the {AgentName} agent.

Bootstrap files (read in this order, absolute paths):
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/{team}/{agent}/agent.yaml
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/{team}/{agent}/soul.md
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/{team}/{agent}/org.md
  T:/共用雲端硬碟/快組隊.Agents/AgentOrg/agents/{team}/{agent}/tools.md

Bootstrap once, then start workflow.
```

**起源**：2026-04-27 用戶 feedback — edu/manager 派 content-designer 時 prompt 開頭只寫「你是 edu/content-designer」沒給路徑，worker 不得不先讀 manager 找路。完整背景見 `agents/agent-ops/manager/memory/feedback-2026-04-27-dispatch-paths.md`。

**驗證**：每次 governance 審查 dispatch prompt 時必檢此項。每位 Manager 的 `workflow/dispatch-protocol.md`（或 `dispatch-flow.md`）的 Identity Block 必須符合此範本。
<!-- end self-added 2026-04-27 -->

## 7. Worker 專屬規範
### soul.md 必含原則
- 至少 3 條領域專屬原則（不得從其他 agent 複製）
- Follow the plan（遵循上游計劃）

### workflow.yaml 結構
- 不含 Manager 專屬動作（dispatch_agents_parallel, dispatch_rounds, merge_results, verify_agent_work）
- Worker 應含 log_start / log_end 步驟（打卡是天條）
- 建議含 check_memory + save_memory 步驟
- 每個可能失敗的步驟必須有 on_error

### skills.md 必含內容
- 至少 3 項領域專屬技能
- 技能描述是領域知識，不是工具名稱

### tools.md
- 不得包含 Agent 工具
- 必須包含 "Do NOT Use" 章節
- 必須包含 "MCP Tools (Authorized)" 章節，列出該 Worker 被授權使用的 MCP 工具（參考 §3.5）

### workflow.yaml 格式
- **steps 格式**（推薦）：每步有 id、action、on_error，結構最清晰
- **routes 格式**：僅用於純路由型 agent（如 intent），整體有 error_policy 即可
- 混用時以 steps 為主、routes 為輔

## 8. 與現有協議的關係
- 引用 definitions.md §Agent Entry Point Schema
- 引用 worklog-protocol.md §Manager-Specific Fields
- 引用 verification-protocol.md
- 引用 memory-protocol.md
- 引用 agents/protocols/rules/feedback-memory.md
- 引用 agents/protocols/workflows/feedback-detect-flow.md（回饋偵測標準流程）
- 引用 agents/protocols/workflows/inline-verify-flow.md（逐次派遣驗證流程）
- 引用 creation-validation.md §Director 專屬檢查項（L3 建立時必須通過 Director checklist）
- 引用 creation-validation.md §Officer 專屬檢查項（L4 建立時必須通過 Officer checklist，並需 Governance 審查）
- 子規則（detailed extension）`agents/protocols/rules/output-placement.md`（agent 資料夾禁止出現任務產物目錄；所有產物寫 `<CWD>/output/{team}/{task_id}/`）
