# Governance Review Flow

## 輸入（來自 Manager）

```json
{
  "action": "governance_review",
  "changes": "changed files or agent names",
  "reason": "why review is needed",
  "requestor": "agent or user who triggered the review",
  "review_scope": "full | scope_guard | structure | protocol | consistency"
}
```

### review_scope 說明

| 值 | 執行步驟 | 用途 |
|---|---------|------|
| `full` | [1]→[2]→[3]→[4]→[5]→[6] | 完整審查（預設值） |
| `scope_guard` | [1]→[2]→[6] | 只做 Scope Guard 檢查 |
| `structure` | [1]→[3]→[6] | 只做結構一致性檢查 |
| `protocol` | [1]→[4]→[6] | 只做協定合規檢查（含參數級驗證） |
| `consistency` | [1]→[5]→[6] | 只做一致性交叉檢查 |

Manager 可以並行派遣 4 個 Governance instance，各帶不同 review_scope，比單次 full review 更可靠。

## 完整審查流程

```
[1] 確認審查範圍
  Read 來源請求，明確：
    - 哪些 agent system 檔案被新增或修改？
    - 修改的目的與理由是什麼？
    - 是否涉及多個 agent 的協作關係？
  On error → partial_review（記錄 UNABLE TO VERIFY）
  │
  ▼
[2] Scope Guard 檢查
  Skip if: review_scope ∉ {full, scope_guard}
  Read agents/definitions.md → File Ownership 表格
  逐一驗證每個修改的檔案：
    - 修改者是否為該檔案的合法擁有者？
    - 是否有 agent 修改了不屬於自己的檔案（如 src/、scripts/）？
    - Developer / Agent Builder 邊界是否清晰？
  Flag: [SCOPE] {agent} modified {file} — should be {correct_agent}
  On error → partial_review
  │
  ▼
[3] 結構一致性檢查
  Skip if: review_scope ∉ {full, structure}
  Glob agents/*/soul.md, tools.md, skills.md, org.md, workflow.yaml
  對每個被修改的 agent，驗證：
    - soul.md：是否有唯一 identity、>=3 principles、anti-patterns、打卡天條？
    - tools.md：是否有 "Do NOT Use" 區段？
    - skills.md：是否有 "NOT This Agent's Job" 區段？
    - org.md：是否有 "When NOT to Pick" 區段？
    - workflow.yaml：是否有 error_policy 和每步 on_error？
  Flag: [STRUCTURE] {agent}/{file} missing {required_section}
  On error → partial_review
  │
  ▼
[4] 協定合規檢查
  Skip if: review_scope ∉ {full, protocol}
  Read agents/worklog-protocol.md
  Read agents/memory-protocol.md
  Read agents/evolution-protocol.md（如存在）
  驗證：
    - workflow.yaml 是否包含 check_memory 和 save_memory 步驟？
    - worklog.sh 呼叫格式是否符合協定？
    - Memory 路徑格式是否正確（{agent}/memory/MEMORY.md）？
    - Manager 的 log_start 命令是否包含正確的 dispatched_by 參數？
      Manager（dispatched_by=user）：命令尾部有 "user" 參數且使用 "$TASK_SUMMARY" 而非 hardcoded 字串
      Worker（dispatched_by=manager）：由 dispatch prompt 控制，workflow.yaml 可使用 "$DISPATCHED_BY"
      驗證方式：Read workflow.yaml → 檢查 log_start command 字串
    - dispatch-protocol.md（或同等文件）的 Worklog Block 是否包含 trace_id 和 parent_task_id？
      驗證方式：Grep dispatch-protocol.md for "trace_id" AND "parent_task_id"
  Flag: [PROTOCOL] {agent} violates {protocol} — {detail}
  Flag: [PROTOCOL] {agent}/workflow.yaml log_start missing "user" parameter — trace_id will not be generated
  Flag: [PROTOCOL] {agent}/workflow/dispatch-protocol.md Worklog Block missing trace_id/parent_task_id
  On error → partial_review
  │
  ▼
[5] 一致性交叉檢查
  Skip if: review_scope ∉ {full, consistency}
  Grep 新增或修改的 org.md，確認：
    - 階層關係是否與其他 agent 的 org.md 互相一致？
    - 新 agent 是否已同步更新 CLAUDE.md registry 和 manager/org.md？
    - collaboration patterns 是否雙向對稱（A 知道 B，B 也知道 A）？
  Flag: [CONSISTENCY] {file} hierarchy mismatch — {detail}
  On error → partial_review
  │
  ▼
[6] 產出審查意見
  格式：
    verdict: APPROVE | REQUEST_CHANGES | REJECT
    scope_violations:    "[SCOPE] ..."
    structure_gaps:      "[STRUCTURE] ..."
    protocol_issues:     "[PROTOCOL] ..."
    consistency_issues:  "[CONSISTENCY] ..."
    recommendations:     "改善建議（非強制）"

  判準：
    - APPROVE：零 Flag，或僅有 recommendations
    - REQUEST_CHANGES：有 [STRUCTURE] / [PROTOCOL] / [CONSISTENCY] Flag
    - REJECT：有 [SCOPE] Flag（scope violation 必須阻止）

RETURN 審查結果給 Manager
```
