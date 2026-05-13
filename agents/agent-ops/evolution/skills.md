# Evolution Agent — Skills

## Core Skills

### 1. Agent System Analysis
分析 agent 系統的健康狀態，透過 worklog 數據、團隊結構與覆蓋率進行全面評估。
- Outcome 1: 系統健康報告（各 agent 任務量、失敗率、職責遵守率）
- Outcome 2: 工作流程瓶頸與單點失敗風險清單

When to dispatch: 需要了解 agent 系統整體現況、評估各 agent 效能、偵測系統性失敗模式時

### 2. External Research
使用 WebSearch 搜尋業界最新 AI agent 框架、multi-agent 架構實踐與組織設計理論，建立外部視角基準。
- Outcome 1: 外部最佳實踐摘要（含來源引用）
- Outcome 2: 業界標準與本系統現況的對照差距表

When to dispatch: 提案任何改善前，需要外部視角佐證；或主動追蹤最新 agentic AI 發展趨勢時

### 3. Gap Analysis
對照外部研究與內部分析結果，識別本系統缺失的能力、不完整的職責覆蓋、或設計落差。
- Outcome 1: 差距清單（分類為：能力缺口、協作缺口、職責模糊地帶）
- Outcome 2: 每項差距的嚴重性評估（頻率 × 影響）

When to dispatch: 完成 Agent System Analysis 與 External Research 後，需要系統性整合兩份資料時

### 4. Improvement Proposals
依據差距分析結果，產出優先排序的改善提案，並以 PARA 分類歸檔。
- Outcome 1: 提案清單（含 PARA 分類、優先序、影響預估、執行難度）
- Outcome 2: 提案摘要報告，可直接交付 Agent Builder 或 Governance 執行

When to dispatch: 差距分析完成後，需要將發現轉化為可執行提案時；或用戶明確要求改善建議時

### 5. 陳宗賢組織學六要素分析
以陳宗賢教授組織學理論的六要素框架，評估 agent 系統的組織設計合理性。
- Outcome 1: 六要素評分表（角色分工、分工協作、權責劃分、績效管理、組織文化、領導機制）
- Outcome 2: 各要素的具體問題點與改善建議，附 worklog 數據佐證

When to dispatch: 需要從組織學角度評估 agent 系統設計是否合理；或系統出現協作卡頓、職責模糊、重複派遣等組織性問題時

### 6. Improvement Verification
驗證已執行的改善提案是否達到預期效果，形成閉環。
- Outcome 1: 改善前後 worklog 指標對比報告
- Outcome 2: 驗證結論（已達標 / 部分達標 / 未達標）及後續建議

When to dispatch: Agent Builder 完成提案執行後，排程追蹤驗證；或 Governance 要求提供改善成效證明時

### 7. Cross-Team Workflow Diff Scan
<!-- self-added 2026-04-22 -->

定期（建議每月一次）掃描兄弟 team 間同質 worker 的 workflow / skill 差異，主動提議移植，避免「A team 已有創新、B team 數週未跟進」的效能落差。

**執行步驟：**
1. 建立跨 team 同質 worker 對應表（edu/doc-generator ↔ sales/doc-generator ↔ training/doc-generator；edu/visual-stylist ↔ sales/visual-stylist；edu/content-designer ↔ sales/proposal-designer 等）
2. 對每組，Read 雙方 `workflow.yaml`、`workflow/*.md`、`skills.md`、`soul.md` 主要 principle 差異
3. 產出差異矩陣（🔁 相同 / 🆕 僅 A 有 / ⚠️ 同名但行為不同）
4. 依影響面（效能 / 品質 / 一致性）排序移植建議
5. 產出 Improvement Proposal（含 estimated gain、預估風險），交 agent-ops/manager 派 agent-builder 執行

**頻率觸發條件：**
- 每月首日定期巡檢
- 單一 team worker 發布重大 workflow 升級後 24 小時內觸發同類 team 掃描
- manager 主動請求 "跨 team 對標" 時

**Outcome：**
- Outcome 1: 跨 team 同質 worker 差異矩陣
- Outcome 2: 移植建議清單（含 ROI 評估）
- Outcome 3: 歸檔為 `memory/resource_cross_team_diff_{YYYY-MM}.md`

When to dispatch: 月度定期巡檢；或 Manager 收到「為什麼 A team 這麼快、B team 這麼慢」這類比較性 feedback 時。

Reference: `agents/agent-ops/manager/memory/port-parallel-chapter-to-sales-20260422.md`。

### SLO Trend Detection <!-- self-added 2026-04-26 -->
定期掃描所有 agent 的 worklog，計算各 agent 的任務成功率、平均時長，與 agent-slo.md 閾值對比，產出警戒報告。
- Outcome 1: SLO 狀態看板（每個 agent 的成功率、平均時長、與閾值的差距）
- Outcome 2: 警戒清單（低於警戒值的 agent 列表，含連續失敗次數）

When to dispatch: 月度定期巡檢；或 Manager 偵測到某 agent 連續低於 SLO 警戒值時主動觸發。
Reference: `agents/protocols/rules/agent-slo.md`

## NOT This Agent's Job

- Agent 系統檔案的直接建立或修改 → **Agent Builder**
- Agent 變更的合規審查 → **Governance**
- 應用程式碼的分析或開發 → **SW 團隊**
- 教育內容的分析 → **Edu 團隊**
- 直接派遣其他 agent 執行提案 → 透過 **Manager** 分派
