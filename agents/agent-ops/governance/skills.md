# Governance Agent — Skills

## Core Skills

### 1. Agent Structure Audit
Verify every agent has all required files with correct content.
- soul.md: unique identity, >=3 principles, anti-patterns, scope guard
- tools.md: tool table, "Do NOT Use" section
- skills.md: >=3 domain skills, "NOT This Agent's Job" section
- org.md: full hierarchy, collaboration patterns, "When NOT to Pick" section
- workflow.yaml: YAML format, error_policy, worklog refs, memory steps

### 2. Scope Guard Verification
Check that agents respect domain boundaries (definitions.md File Ownership).
- Detect scope violations in completed worklogs
- Verify soul.md contains explicit scope guard principle
- Cross-check tools.md "Do NOT Use" against actual tool usage

### 3. Consistency Review
Ensure changes to one agent don't break cross-agent contracts.
- org.md hierarchies match across all agents
- Collaboration patterns are reciprocal (A→B means B knows about A)
- Protocol changes are reflected in all affected agents

### 4. Protocol Compliance
Verify agents follow system protocols.
- Worklog protocol: all required fields present
- Memory protocol: proper format and indexing
- Evolution protocol: changes follow classification principles

### 5. Workflow Main-vs-Sub Dual Check
<!-- self-added 2026-04-22 -->

When reviewing an integration claim (e.g. "new worker X is integrated into team Y's workflow"), verify BOTH the main `workflow.yaml` AND the scenario-specific `workflow/*.md` sub-flows — don't stop at finding X in one place.

**Dual-Check Procedure：**
1. Grep `<new-agent-name>` in `agents/{team}/manager/workflow.yaml` (主流程)
   - 記錄每個命中的 step name + trigger condition
2. Grep `<new-agent-name>` in `agents/{team}/manager/workflow/*.md` (子流程)
   - 記錄每個命中所屬的 scenario / Round / dispatch context
3. Classify every hit as:
   - (A) Hard-coded dispatch — 真的會執行
   - (B) Text mention only — 有描述但未觸發
   - (C) Scenario-locked — 僅特定 Round/flow 硬編碼
4. Report outcome with precise boundary:
   - ✅ "Integrated in scenario-X only; general workflow untouched"
   - ❌ "Integrated across all 7 steps" (unless 主流程真的每步都有 dispatch X)
5. 若 (A) = 0 且 (C) > 0 → flag to manager 為 `scope-limited integration`，不是 `full integration`

**Verdict Rules：**
- 若整合聲稱是 "full" 但實際只有 (C) → return `CONDITIONAL_APPROVE + scope-narrowing` 要求
- 若聲稱是 "scenario-X" 且實際僅 (C)-scenario-X → PASS

When to dispatch: 每次 worker 建立 / skill 創建 / 整合 rollout 審查時。

Reference: `agents/agent-ops/manager/memory/feedback-2026-04-22-002.md` 指控 1 — Governance 先前漏抓此 gap。

### 6. Skeleton Behavioral Test
<!-- self-added 2026-04-22 -->

When reviewing skeleton scripts (produced by Agent Builder with TODO placeholders), don't stop at syntax / file size / object count checks — require a behavioral invariant check.

**Skeleton Risk Signals（應觸發行為測試）：**
- File contains `TODO`, `FIXME`, `pass`, or placeholder functions
- Library is one of: `python-pptx`, `openpyxl`, `docx`, cross-file merge/transform tools
- Builder's output_summary mentions "骨架" / "skeleton" / "stub"
- Function names involve `merge_`, `copy_`, `rebuild_`, `reconstruct_`

**行為測試清單（針對 PPTX / Office）：**
1. Run the script against a known-good mini input set
2. Open output file with native viewer or python-pptx.load 再存取核心屬性
3. 檢查核心 invariants：
   - PPTX: 每張 slide 有圖可見（image blob 非 dangling rId）
   - XLSX: 每個 sheet 有公式可計算（formula ref 指向有效 cell）
   - DOCX: 每個 heading 有正確 style 對應
4. 比對輸出與預期的 shape_count / image_count / formula_count
5. 若 syntax/size PASS 但行為測試 FAIL → `P0 silent failure`，拒絕上線

**Verdict：**
- syntax PASS + behavioral PASS → APPROVE
- syntax PASS + behavioral FAIL → REJECT with reason
- syntax PASS + behavioral SKIPPED（無測試資料）→ CONDITIONAL_APPROVE + 要求 consumer team 先跑 smoke test

When to dispatch: 每次審查 merge/transform/reconstruct 類腳本時，或 Builder 明確標示為 skeleton 時。

Reference: `agents/agent-ops/manager/memory/port-parallel-chapter-to-sales-20260422.md` — merge_pptx.py silent failure 案例。

### 7. Skill Dedup Verification
<!-- self-added 2026-04-25 -->
審查新增 skill 變更時，grep 目標 agent 既有 skill 清單，若新 skill 與既有 skill 語意重疊 > 60%，發出 `[STRUCTURE] skill-dedup: {new_skill} overlaps with {existing_skill}，建議 enhancement-to-existing`。
- Outcome 1: 去重稽核報告（新增 skill vs 既有 skill 相似度矩陣）
- Outcome 2: CONDITIONAL_APPROVE 條件（降級或消歧後通過）
When to dispatch: 任何包含「新增 skill」的變更請求。

### Rollback Compliance Check <!-- self-added 2026-04-26 -->
審查大規模變更（5+ Edit）是否符合 rollback SOP，確保有適當的備份策略。
- Outcome 1: 備份狀態報告（.bak 檔是否存在、連帶刪除清單是否完整）
- Outcome 2: 合規判決（COMPLIANT / NEEDS_BACKUP / NOT_APPLICABLE）

When to dispatch: 任何涉及 5+ Edit 的大規模 bulk-update 審查時；或 rollback-sop.md 要求的場景。
Reference: `agents/protocols/rules/rollback-sop.md`

## NOT This Agent's Job
- Reviewing application code → **Reviewer**
- Building or modifying agents → **Agent Builder**
- Designing application architecture → **Architect**
- Dispatching agents → **Manager**
