# Rollback SOP（備份還原標準流程）

> 版本：v1.0
> 建立日期：2026-04-24
> 作者：agent-ops/agent-builder（gap-analysis 收斂 Batch D，補 Gov 路 3 警告）
> 適用：所有 agent 系統檔案的備份還原操作

## 命名慣例

- `{file}.bak.<YYYY-MM-DD>` = 該日期「第一次修改之前」的快照
- `{file}.bakN.<YYYY-MM-DD>` = 該日期「第 N 次修改之前」的快照（N 值大者較新）
- 規則：同一檔案當日多次修改時，每次修改前都做備份，序號遞增

## 還原規則（黃金法則）

**規則 1 — 序號大的是新狀態**：`.bak3` 比 `.bak2` 新，`.bak2` 比 `.bak` 新。
**規則 2 — 一路還原從新到舊**：要退回 N 代前，順序是 `.bakN → .bakN-1 → ... → .bak`。
**規則 3 — 永遠不直接跳**：除非要完全退到第一次改動前，否則不得跳過中間備份。

## 新建檔連帶刪除清單（Dangling Reference 防護）

以下新建檔若要刪除 rollback，必須連帶 revert 引用它的檔案：

| 刪除目標 | 必須同時 revert | 理由 |
|---|---|---|
| `agents/protocols/evidence-protocol.md` | `agents/sw/developer/soul.md`（移除 P9）/ `agents/sw/developer/skills.md`（移除 skill 6）/ `agents/sw/manager/workflow.yaml`（移除 references 區）/ `agents/protocols/dual-audit-protocol.md`（移除 reference） | Developer 與 Manager 文件明確 reference 此 protocol |
| `agents/protocols/dual-audit-protocol.md` | `agents/sw/manager/soul.md`（移除 P17 reference）/ `agents/sw/reviewer/soul.md`（移除 P9 reference）| Manager 與 Reviewer soul 引用 |
| `agents/sw/manager/workflow/dual-audit-flow.md` | `agents/sw/manager/workflow.yaml`（移除 `audit_doer_facts` 與 `audit_reviewer_process` 兩 step + references 區）/ `agents/protocols/dual-audit-protocol.md`（移除「參考實作」引用）| workflow 兩個新 step 直接 ref 此 flow |

## 完全 Rollback 順序（退回 gap-analysis 階段 1-3 前）

**前置**：盤點哪幾個 batch 要退。

**Batch D 回退**（若只退 Batch D）：
1. `cp reviewer/skills.md.bak2.2026-04-24 reviewer/skills.md`
2. `cp manager/workflow.yaml.bak3.2026-04-24 manager/workflow.yaml`
3. `rm protocols/rules/rollback-sop.md`
4. （若 evidence-protocol.md、dual-audit-protocol.md、dual-audit-flow.md 有 .bak2 也用 .bak2 覆蓋 current）

**Batch C 回退**（接續 D 或單獨）：
1. `cp reviewer/soul.md.bak.2026-04-24 reviewer/soul.md`
2. `cp reviewer/skills.md.bak.2026-04-24 reviewer/skills.md`
3. `cp manager/workflow.yaml.bak2.2026-04-24 manager/workflow.yaml`
4. `cp manager/workflow/dual-audit-flow.md.bak.2026-04-24 manager/workflow/dual-audit-flow.md`
5. `rm protocols/dual-audit-protocol.md`

**Batch B 回退**：
1. `cp manager/soul.md.bak.2026-04-24 manager/soul.md`
2. `cp manager/workflow.yaml.bak.2026-04-24 manager/workflow.yaml`
3. `rm manager/workflow/dual-audit-flow.md`

**Batch A 回退**：
1. `cp developer/soul.md.bak.2026-04-24 developer/soul.md`
2. `cp developer/skills.md.bak.2026-04-24 developer/skills.md`
3. `rm protocols/evidence-protocol.md`

## Rollback 後必做驗證

1. `grep -r "self-added 2026-04-24" agents/sw/ agents/protocols/` 應回 0 匹配（完全 rollback 情境）
2. `grep -r "evidence-protocol\|dual-audit" agents/sw/ agents/protocols/` 應全無匹配（完全 rollback 情境）
3. `python -c "import yaml; yaml.safe_load(open('agents/sw/manager/workflow.yaml'))"` 必須 exit 0
4. Manager 重新 dispatch 一次測試任務，確認 workflow 能跑完（不觸發 block_and_report）

## 版本歷程

| 版本 | 日期 | 作者 | 變更 |
|---|---|---|---|
| v1.0 | 2026-04-24 | agent-ops/agent-builder | 初版建立（gap-analysis Batch D，補 Gov 路 3 警告） |
