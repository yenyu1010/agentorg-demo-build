# 規則推送協議（Rule Rollout Protocol）

## 適用時機
當 `agent-anatomy.md`、`creation-validation.md` 或 `definitions.md` 新增「必含原則」或「必備檔案」時，必須同步推送到所有現有 agent。

## 流程

1. **Governance 審查新規則** — 確認規則合理性和影響範圍
2. **Manager 評估影響面** — 列出需要更新的 agent 清單
3. **Agent Builder 執行 bulk-update** — 依 `bulk-update.md` 流程分批更新
4. **每批次跑 validate-agent.sh** — 確保更新後合規
5. **Manager 合成報告** — 確認推送完成率 100%

## 規則

- **不可只寫規則不推送** — 新增 protocol 必含原則後，Manager 必須在同一任務中觸發 bulk-update
- **推送順序** — Agent-Ops 團隊先行（以身作則），再推送 SW → Edu → Shared
- **推送紀錄** — 每次推送在 rule-rollout.md 末尾追加紀錄：
  ```
  ### {date} — {規則名稱}
  - 影響 agent 數：{N}
  - 推送狀態：完成/部分完成
  - 未推送原因（如有）：...
  ```

## 歷史推送紀錄

### 2026-04-14 — 計算委派原則
- 影響 agent 數：17（不含 calculator 自身）
- 推送狀態：完成
- 備註：全系統 21 agent 驗證通過

### 2026-04-22 — P18 任務粒度拆解（Dispatch Granularity）<!-- self-added -->

- **Trace ID**：20260422-p18-rollout
- **起源**：sales/manager（Principle 18），因「知識衛星」提案出現 138 分鐘 / 76 分鐘大包任務
- **觸發者**：david（user）
- **決策**：全面推廣（用戶選 B）
- **涵蓋 5 manager 的新編號**：
  - sw/manager → Principle 16
  - edu/manager → Principle 19
  - bni/manager → Principle 22
  - agent-ops/manager → Principle 22
  - platform/goose-ops/manager → Principle 21
- **加上原 sales/manager 的 Principle 18** → 共 6 manager 全覆蓋
- **連動檔案**：每個 manager 的 skills.md 都加對應 skill；詳細 feedback 在 `agents/sales/manager/memory/feedback_task_granularity.md`
- **後續義務**：未來新建 manager 時需預設含此 Principle（建議寫進 `creation-validation.md`）
