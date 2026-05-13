# Agent Creation Validation Checklist

## 1. 使用時機
- Agent Builder 建立新 agent 後
- Governance 審查新 agent 時
- 定期審計全系統 agent 合規性時

## 2. 分類判斷
IF type == "officer" → Officer Anatomy
ELSE IF type == "director" → Director Anatomy
ELSE IF type == "manager" OR (reports_to == "user" AND has Agent tool) → Manager Anatomy
ELSE → Worker Anatomy

## 3. 通用檢查項（全部必通過）
| # | 類別 | 檢查項 | 驗證方式 |
|---|------|--------|---------|
| 1 | 目錄 | agents/{team}/{agent}/ 存在 | Glob |
| 2 | 目錄 | worklog/.gitkeep 存在 | Glob |
| 3 | 目錄 | memory/MEMORY.md 存在 | Read |
| 4 | agent.yaml | 所有必填欄位齊全 | Read + schema |
| 5 | agent.yaml | bootstrap 順序：soul→org→tools | Read |
| 6 | soul.md | Identity 獨特非複製 | Read |
| 7 | soul.md | 含打卡天條 | Grep |
| 8 | soul.md | 含 Scope Guard | Grep |
| 9 | soul.md | Anti-patterns 章節存在 | Read |
| 10 | tools.md | 含工具表 | Read |
| 11 | tools.md | 含 "Do NOT Use" 章節 | Grep |
| 12 | org.md | 完整層級圖 | Read |
| 13 | org.md | "When NOT to Pick" 章節 | Grep |
| 14 | skills.md | 存在 | Glob |
| 15 | skills.md | 至少 3 個技能 | Read |
| 16 | workflow.yaml | 有 error_policy | Read |
| 17 | workflow.yaml | 每步有 on_error | Read |
| 18 | soul.md | 含計算委派原則（或在 skills.md 中明確說明不涉及計算） | Grep |
| 19 | tools.md | 含 "MCP Tools (Authorized)" 章節 | Grep |
| 20 | tools.md | MCP 工具選擇符合 agent 職責（參考 mcp-registry.md 和 agent-anatomy.md §3.5） | Read |
| 21 | tools.md | 包含 Google Drive 讀取限制提醒（引用 google-drive-read.md） | Grep |

## 4. Manager 專屬檢查項
| # | 檢查項 | 驗證方式 |
|---|--------|---------|
| M1a | workflow.yaml 含 log_start/log_end 步驟 | Grep |
| M1b | Manager 的 log_start 命令格式正確：尾部有 "user" 參數，使用 "$TASK_SUMMARY"（非 hardcoded 字串） | Read workflow.yaml → 檢查 log_start command |
| M2 | workflow.yaml 含 verify 步驟 | Grep |
| M3 | workflow.yaml 含 synthesize 步驟 | Grep |
| M4 | tools.md 含 Agent 工具 | Grep |
| M5 | soul.md 含 8 條 Manager 必備原則 | Read |
| M6 | skills.md 含 dispatch/synthesis 技能 | Read |
| M7 | workflow.yaml 含 hitl_gate 步驟（引用 hitl-protocol.md） | Grep |
| M8 | hitl_gate 使用嚴格 token（confirm/abort/modify），非模糊措辭 | Read |
| M9 | workflow.yaml 含 feedback_detect 步驟（引用 feedback-detect-flow.md） | Grep |
| M10 | workflow.yaml execute 步驟引用 inline-verify-flow.md 或包含 inline_verify 機制 | Grep |
| M11 | workflow/dispatch-protocol.md Worklog Block 包含 trace_id 和 parent_task_id | Grep dispatch-protocol.md for "trace_id" AND "parent_task_id" |

## 4.5 Director 專屬檢查項（含全部 Manager 檢查項 M1-M11）
| # | 檢查項 | 驗證方式 |
|---|--------|---------|
| D1 | agent.yaml type == "director" | Read |
| D2 | soul.md 含 Cross-team coordination 原則 | Grep |
| D3 | soul.md 含 Escalation judgment 原則 | Grep |
| D4 | skills.md 含 Multi-team Coordination 技能 | Read |
| D5 | workflow.yaml 含 dispatch_managers 動作 | Grep |
| D6 | org.md 列出管轄的 Manager 清單 | Read |
| D7 | workflow.yaml 含 feedback_detect 步驟（引用 feedback-detect-flow.md） | Grep |
| D8 | workflow.yaml execute 步驟引用 inline-verify-flow.md | Grep |

## 4.6 Officer 專屬檢查項（含全部 Director 檢查項 M1-M11 + D1-D8）
| # | 檢查項 | 驗證方式 |
|---|--------|---------|
| O1 | agent.yaml type == "officer" | Read |
| O2 | reports_to == "user" | Read |
| O3 | soul.md 含 Strategic vision 原則 | Grep |
| O4 | soul.md 含 Policy authority 原則 | Grep |
| O5 | skills.md 含 Organizational Strategy 技能 | Read |
| O6 | workflow.yaml 含 dispatch_directors 動作 | Grep |
| O7 | workflow.yaml 含 policy_check 步驟 | Grep |
| O8 | workflow.yaml 含 feedback_detect 步驟（引用 feedback-detect-flow.md） | Grep |
| O9 | workflow.yaml execute 步驟引用 inline-verify-flow.md | Grep |

## 5. Worker 專屬檢查項
| # | 檢查項 | 驗證方式 |
|---|--------|---------|
| W1 | tools.md 不含 Agent 工具 | Grep (negative) |
| W2 | soul.md 含 ≥3 領域專屬原則 | Read |
| W3 | skills.md 有 domain-specific 技能 | Read |
| W4 | workflow.yaml 不含 Manager 專屬步驟（dispatch_agents_parallel, dispatch_rounds, merge_results, verify_agent_work） | Grep (negative) |
| W5 | workflow.yaml 含 R-D-V 結構 | Read |
| W6 | workflow.yaml 包含 `check_memory` + `save_memory` 步驟 | 新建 agent 必備，確保自我成長機制落地 |
| W7 | Manager 類 agent 包含 `feedback_detect` 步驟 | Manager 專屬，偵測用戶回饋 |

## 5.5 Team 級別檢查項
| # | 檢查項 | 驗證方式 | 說明 |
|---|--------|---------|------|
| T1 | 新建 team 必須有對應的 `skills/tuq-{team}/SKILL.md` 入口 | Glob | 確保 SKILL 檔案存在 |
| T2 | 新建 team 必須在 `~/.claude/skills/tuq-{team}/` 有全域 symlink | Bash: `ls -la ~/.claude/skills/tuq-{team}` | 確保用戶可透過 `/tuq-{team}` 存取。若缺失：執行 `bash scripts/setup-global-skills.sh` |
| T3 | 新建 team 必須在 `settings.local.json` 註冊 `Skill(tuq-{team})` 權限 | Grep | 確保 Claude Code 有執行權限 |

**W5: workflow.yaml 含 R-D-V 三段結構**
- Worker 的 workflow.yaml 至少含 3 個語意階段：
  - Research 段：`assess` / `research` / `diagnose`（至少一個）
  - Plan 段：`plan`（明確的規劃步驟）
  - Execute 段：`execute` / `configure` / `install` / `author`（至少一個）
- 每段須有獨立 `ref: workflow/XXX-flow.md`
- 驗證方式：Read workflow.yaml → 確認三段均存在
- 參考金標準：`agents/platform/gb10-sysadmin/workflow.yaml`（完整 R-D-V 結構）

## 6. 系統整合檢查
| # | 檢查項 | 驗證方式 |
|---|--------|---------|
| S1 | workflow.yaml 所有 ref: 指向存在的檔案 | Glob |
| S2 | org.md hierarchy 與實際目錄一致 | Read + Glob |
| S3 | CLAUDE.md Agent Anatomy 表已更新 | Read |

## 7. 完成判定
- 通用項 100% + 角色專屬項 100% + 系統整合 100% = PASS
- 任何 FAIL 項目阻止交付
- Worker: 通用 + W1-W5
- Manager: 通用 + M1-M11
- Director: 通用 + M1-M11 + D1-D8
- Officer: 通用 + M1-M11 + D1-D8 + O1-O9

## 8. 常見缺失（歷史審計發現）
- skills.md 遺漏（最常見，9/19 agents 於 2026-04-14 審計中發現）
- workflow.yaml 缺 on_error
- tools.md 缺 "Do NOT Use" 章節
- W4 已修訂（2026-04-14）：原規則禁止 Worker 含 log_start/log_end，與「打卡是天條」矛盾。現改為禁止 Worker 含 Manager 專屬動作（dispatch, merge, verify_agent_work）
- Manager workflow.yaml 缺 hitl_gate 步驟（2026-04-15 審計新增）
- tools.md 缺 MCP 工具集（2026-04-17 新增：agent 不知道自己可用 desktop-commander、bash 等 MCP 工具）
- tools.md 使用 read_file 而非 read_multiple_files 讀取 T:\ 路徑（2026-04-17 新增：觸發 Google Drive 空內容問題）
