# 建立 Agent 工作流程

## Manager 輸入
```json
{
  "action": "create_agent",
  "name": "agent-name",
  "domain": "一句話描述此 agent 的職責",
  "reason": "為何現有 agent 無法涵蓋此需求",
  "reference_agent": "用作範本的現有 agent（選填）"
}
```

## 執行步驟

```
[1] （Manager 透過 scripts/worklog.sh 處理 worklog — agent 自身不寫 worklog）
  │
  ▼
[2] 讀取分類原則
  讀取 agents/agent-ops/evolution/classification-principles.md
  讀取 agents/definitions.md（tool vs skill、自我更新規則）
  │
  ▼
[3] 確認無職責重疊
  Glob agents/*/README.md → 逐一讀取
  Grep agents/*/skills.md，搜尋相似領域關鍵字
  若有重疊 → 停止，向 Manager 回報，建議改為強化現有 agent
  │
  ▼
[4] 讀取範本 agent
  若有提供 reference_agent → 讀取其所有檔案
  若未提供 → 讀取性質最相近的 agent
  │
  ▼
[5] 建立目錄
  Bash: mkdir -p agents/{name}/{worklog,memory}
  │
  ▼
[6] 建立所有必要檔案
  - agent.yaml   — 入口點：agent 名稱、title、team、reports_to、bootstrap 序列、
                   workflow 指標、dispatch 設定（model + trigger + not_for）。
                   必填欄位：agent, title, team, reports_to, bootstrap, workflow,
                   dispatch.model, dispatch.trigger, dispatch.not_for。
                   選填：skills（僅當 skills.md 存在時）。
                   完整規格見 agents/protocols/definitions.md「Agent Entry Point Schema」。
  - README.md    — 角色、何時派遣、dispatch 設定
  - soul.md      — 獨特身份、>=3 條原則、打卡天條原則、反模式（禁止複製貼上）
  - tools.md     — 工具表 + 「Do NOT Use」區塊 + 使用指引
  - skills.md    — >=3 個領域專屬技能 + 「NOT This Agent's Job」區塊
  - workflow.yaml — YAML 格式，必須包含：
      • error_policy 區塊
      • WORKER agent：不含 log_start/log_end 步驟（agent 在執行時直接呼叫 worklog.sh）
      • MANAGER/ORCHESTRATOR agent：應包含 log_start 和 log_end 作為 shell action 步驟
        （使用 action: shell，command: "bash scripts/worklog.sh start/end ..." — 不是
        worklog_start/worklog_end，這些不存在）
      • 每個可能失敗的步驟都要有 on_error
      • check_memory 步驟
      • save_memory 步驟
      • **Worker workflow.yaml R-D-V 結構（W5）**：
        - 必須包含至少三段：Research（assess/research/diagnose）→ Plan → Execute
        - 每段 ref 獨立的 `workflow/XXX-flow.md`
        - 參考金標準：同 team 最完整的 agent，或 `agents/platform/gb10-sysadmin/workflow.yaml`
      • **Manager log_start 命令格式（M1b）**：
        - 命令尾部必須有 "user" 參數，使用 "$TASK_SUMMARY"（非 hardcoded 字串）
      • **Manager dispatch-protocol.md Worklog Block（M11）**：
        - 必須含 trace_id 和 parent_task_id 欄位
  - org.md       — 完整層級結構（含所有 9+ 個 agent）、協作模式、
                   「When NOT to Pick This Agent」區塊
  - worklog/.gitkeep
  - memory/MEMORY.md，含 agent 專屬標頭
  - **若 agent 角色為 manager/orchestrator：**
    - workflow 必須在最後加入「Summary Worklog」步驟
    - Summary worklog schema 必須包含 `dispatch_summary` 和 `verification_results`
    - 見 `agents/worklog-protocol.md` Manager 專屬欄位說明
  │
  ▼
[7] 更新登錄表
  編輯 CLAUDE.md → 在 Agent Registry 表中新增一列
  編輯 agents/agent-ops/manager/org.md → 加入層級結構
  若有新的協作模式，編輯其他相關 agent 的 org.md
  │
  ▼
[8] 同團隊 org.md 連鎖更新
  新 agent 建立後，更新同團隊所有其他 agent 的 org.md hierarchy，確保新成員出現在層級圖中。
  規則：
  - 讀取新 agent 所屬 team 的所有 agent 的 org.md
  - 在每個 org.md 的 Hierarchy 部分加入新 agent
  - 移除任何「（尚未建立）」等過時備註
  - 此步驟不可跳過——layer 圖過時是歷史上最常見的合規問題
  │
  ▼
[9] 執行 checklist（checklist.md）— 所有項目必須通過
  │
  ▼
[10] 自動化合規驗證（必須通過）
  執行 `bash scripts/validate-agent.sh {team}/{agent}` 對新建的 agent 進行自動化結構驗證。

  規則：
  - 驗證結果必須為 PASS（零 FAIL）才可交付
  - 若有 FAIL 項目，返回對應步驟修正，然後重跑驗證
  - WARN 項目記錄但不阻擋交付
  - 驗證結果須附在回報給 Manager 的輸出中

  指令：bash scripts/validate-agent.sh {team}/{agent}
  │
  ▼
[10.5] 新 team 自動建立 skill 入口
  若正在建立的 agent 是**新 team 的第一個 agent**（team 目錄之前不存在）：
    1. 自動觸發 create-skill.md 流程，建立 `skills/tuq-{team}/SKILL.md`
    2. 執行步驟 [5.5] 的全域 Junction 建立
    3. 更新 settings.local.json 加入 Skill(tuq-{team}) 和 Skill(tuq-{team}:*) 權限
  若非新 team（加入既有 team）：跳過此步驟
  │
  ▼
[11] （Manager 透過 scripts/worklog.sh 處理 worklog 結束）
  │
  ▼
回傳摘要給 Manager（須含驗證結果）
```
