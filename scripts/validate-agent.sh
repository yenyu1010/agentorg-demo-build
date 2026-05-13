#!/usr/bin/env bash
# validate-agent.sh — 驗證 agent 結構是否符合 creation-validation.md
# 用法: bash scripts/validate-agent.sh <team/agent>
# 範例: bash scripts/validate-agent.sh sw/developer
#       bash scripts/validate-agent.sh edu/content-designer

set -uo pipefail

AGENT_PATH="$1"
AGENT_DIR="agents/${AGENT_PATH}"
PASS=0
FAIL=0
WARN=0

# 顏色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

check_pass() { echo -e "  ${GREEN}✓${NC} $1"; PASS=$((PASS + 1)); }
check_fail() { echo -e "  ${RED}✗${NC} $1"; FAIL=$((FAIL + 1)); }
check_warn() { echo -e "  ${YELLOW}⚠${NC} $1"; WARN=$((WARN + 1)); }

echo "=== Agent Validation: ${AGENT_PATH} ==="
echo ""

# --- 通用檢查 ---
echo "[通用檢查]"

# G1: 目錄存在
[ -d "$AGENT_DIR" ] && check_pass "G1: 目錄存在" || { check_fail "G1: 目錄 $AGENT_DIR 不存在"; exit 1; }

# G2: worklog/.gitkeep
[ -f "$AGENT_DIR/worklog/.gitkeep" ] && check_pass "G2: worklog/.gitkeep 存在" || check_fail "G2: worklog/.gitkeep 缺失"

# G3: memory/MEMORY.md
[ -f "$AGENT_DIR/memory/MEMORY.md" ] && check_pass "G3: memory/MEMORY.md 存在" || check_fail "G3: memory/MEMORY.md 缺失"

# G4: agent.yaml 存在
[ -f "$AGENT_DIR/agent.yaml" ] && check_pass "G4: agent.yaml 存在" || check_fail "G4: agent.yaml 缺失"

# G4b: agent.yaml 必填欄位
if [ -f "$AGENT_DIR/agent.yaml" ]; then
  for field in "agent:" "title:" "team:" "reports_to:" "bootstrap:" "workflow:" "dispatch:"; do
    grep -q "$field" "$AGENT_DIR/agent.yaml" 2>/dev/null || check_fail "G4b: agent.yaml 缺少 $field"
  done
  # bootstrap 順序: soul.md 在 org.md 前，org.md 在 tools.md 前
  SOUL_LINE=$(grep -n "soul.md" "$AGENT_DIR/agent.yaml" 2>/dev/null | head -1 | cut -d: -f1)
  ORG_LINE=$(grep -n "org.md" "$AGENT_DIR/agent.yaml" 2>/dev/null | head -1 | cut -d: -f1)
  TOOLS_LINE=$(grep -n "tools.md" "$AGENT_DIR/agent.yaml" 2>/dev/null | head -1 | cut -d: -f1)
  if [ -n "$SOUL_LINE" ] && [ -n "$ORG_LINE" ] && [ -n "$TOOLS_LINE" ]; then
    if [ "$SOUL_LINE" -lt "$ORG_LINE" ] && [ "$ORG_LINE" -lt "$TOOLS_LINE" ]; then
      check_pass "G5: bootstrap 順序正確 (soul→org→tools)"
    else
      check_fail "G5: bootstrap 順序錯誤"
    fi
  else
    check_fail "G5: bootstrap 缺少必要檔案"
  fi
fi

# G6: soul.md
if [ -f "$AGENT_DIR/soul.md" ]; then
  check_pass "G6: soul.md 存在"
  grep -qi "identity" "$AGENT_DIR/soul.md" && check_pass "G6b: soul.md 含 Identity" || check_fail "G6b: soul.md 缺 Identity"
  grep -qi "principles" "$AGENT_DIR/soul.md" && check_pass "G6c: soul.md 含 Principles" || check_fail "G6c: soul.md 缺 Principles"
  grep -qi "anti-pattern" "$AGENT_DIR/soul.md" && check_pass "G6d: soul.md 含 Anti-patterns" || check_fail "G6d: soul.md 缺 Anti-patterns"
  grep -qi "worklog\|打卡" "$AGENT_DIR/soul.md" && check_pass "G6e: soul.md 含打卡天條" || check_fail "G6e: soul.md 缺打卡天條"
  grep -qi "scope.*violation\|scope.*guard\|越權拒絕" "$AGENT_DIR/soul.md" && check_pass "G6f: soul.md 含 Scope Guard" || check_fail "G6f: soul.md 缺 Scope Guard"
else
  check_fail "G6: soul.md 缺失"
fi

# G7: tools.md
if [ -f "$AGENT_DIR/tools.md" ]; then
  check_pass "G7: tools.md 存在"
  grep -qi "do not use\|not use\|禁用" "$AGENT_DIR/tools.md" && check_pass "G7b: tools.md 含 Do NOT Use" || check_fail "G7b: tools.md 缺 Do NOT Use"
else
  check_fail "G7: tools.md 缺失"
fi

# G8: org.md
if [ -f "$AGENT_DIR/org.md" ]; then
  check_pass "G8: org.md 存在"
  grep -qi "when not to pick\|不應選" "$AGENT_DIR/org.md" && check_pass "G8b: org.md 含 When NOT to Pick" || check_fail "G8b: org.md 缺 When NOT to Pick"
else
  check_fail "G8: org.md 缺失"
fi

# G9: skills.md
if [ -f "$AGENT_DIR/skills.md" ]; then
  check_pass "G9: skills.md 存在"
  SKILL_COUNT=$(grep -c "^###" "$AGENT_DIR/skills.md" 2>/dev/null || echo 0)
  [ "$SKILL_COUNT" -ge 3 ] && check_pass "G9b: skills.md 有 ${SKILL_COUNT} 個技能 (≥3)" || check_fail "G9b: skills.md 僅 ${SKILL_COUNT} 個技能 (<3)"
else
  check_fail "G9: skills.md 缺失"
fi

# G10: workflow.yaml
if [ -f "$AGENT_DIR/workflow.yaml" ]; then
  check_pass "G10: workflow.yaml 存在"
  grep -q "error_policy" "$AGENT_DIR/workflow.yaml" && check_pass "G10b: workflow.yaml 含 error_policy" || check_fail "G10b: workflow.yaml 缺 error_policy"
  grep -q "on_error" "$AGENT_DIR/workflow.yaml" && check_pass "G10c: workflow.yaml 含 on_error" || check_warn "G10c: workflow.yaml 缺 on_error（可能使用 routes 格式）"
else
  check_fail "G10: workflow.yaml 缺失"
fi

echo ""

# --- 角色判定 ---
IS_MANAGER=false
if [ -f "$AGENT_DIR/agent.yaml" ]; then
  if grep -q "reports_to:.*user" "$AGENT_DIR/agent.yaml" 2>/dev/null; then
    # Check if it also has subordinates (dispatch action in workflow)
    if grep -q "dispatch_agent\|dispatch_rounds\|dispatch_agents_parallel" "$AGENT_DIR/workflow.yaml" 2>/dev/null; then
      IS_MANAGER=true
    fi
  fi
  if [ -f "$AGENT_DIR/tools.md" ] && grep -q "Agent" "$AGENT_DIR/tools.md" 2>/dev/null && ! grep -qi "do not use" "$AGENT_DIR/tools.md" 2>/dev/null; then
    IS_MANAGER=true
  fi
  # Better check: if Agent is in the authorized tools section (not in Do NOT Use)
  if [ -f "$AGENT_DIR/tools.md" ]; then
    # Check if Agent appears BEFORE "Do NOT Use" section
    DONOT_LINE=$(grep -n -i "do not use\|not use" "$AGENT_DIR/tools.md" 2>/dev/null | head -1 | cut -d: -f1)
    AGENT_LINE=$(grep -n "| Agent\|| \`Agent\`" "$AGENT_DIR/tools.md" 2>/dev/null | head -1 | cut -d: -f1)
    if [ -n "$AGENT_LINE" ] && [ -n "$DONOT_LINE" ]; then
      if [ "$AGENT_LINE" -lt "$DONOT_LINE" ]; then
        IS_MANAGER=true
      else
        IS_MANAGER=false
      fi
    fi
  fi
fi

if $IS_MANAGER; then
  echo "[Manager 專屬檢查]"
  # M1: workflow 含 log_start/log_end
  grep -q "log_start" "$AGENT_DIR/workflow.yaml" && check_pass "M1: log_start 存在" || check_fail "M1: log_start 缺失"
  grep -q "log_end" "$AGENT_DIR/workflow.yaml" && check_pass "M1b: log_end 存在" || check_fail "M1b: log_end 缺失"
  # M2: verify
  grep -qi "verify\|qa.review" "$AGENT_DIR/workflow.yaml" && check_pass "M2: verify/qa_review 步驟存在" || check_fail "M2: verify 步驟缺失"
  # M3: synthesize
  grep -qi "synthe" "$AGENT_DIR/workflow.yaml" && check_pass "M3: synthesize 步驟存在" || check_fail "M3: synthesize 步驟缺失"
  # M4: tools.md 含 Agent
  grep -q "Agent" "$AGENT_DIR/tools.md" && check_pass "M4: tools.md 含 Agent 工具" || check_fail "M4: tools.md 缺 Agent 工具"
else
  echo "[Worker 專屬檢查]"
  # W1: tools.md 不含 Agent (in authorized section)
  # Already handled above
  check_pass "W1: 非 Manager（已驗證）"
  # W4: 不含 Manager 專屬動作
  if grep -q "dispatch_agents_parallel\|dispatch_rounds\|merge_results\|verify_agent_work" "$AGENT_DIR/workflow.yaml" 2>/dev/null; then
    check_fail "W4: workflow.yaml 含 Manager 專屬動作"
  else
    check_pass "W4: workflow.yaml 無 Manager 專屬動作"
  fi
fi

# --- S1: ref 檔案存在性 ---
echo ""
echo "[系統整合檢查]"
if [ -f "$AGENT_DIR/workflow.yaml" ]; then
  REF_MISSING=0
  while IFS= read -r ref; do
    ref=$(echo "$ref" | sed 's/.*ref: *//' | sed 's/#.*//' | sed 's/[[:space:]}"]*$//' | tr -d '"')
    # Strip common path prefixes that point back to the agent's own directory
    clean_ref=$(echo "$ref" | sed "s|^\.claude/agents/${AGENT_PATH}/||" | sed "s|^agents/${AGENT_PATH}/||")
    if [ -n "$ref" ] && [ "$ref" != "soul.md" ]; then
      if [ -f "$AGENT_DIR/$clean_ref" ] || [ -f "$AGENT_DIR/$ref" ] || [ -f "$ref" ]; then
        : # pass
      else
        check_fail "S1: ref 檔案不存在: $ref"
        REF_MISSING=$((REF_MISSING + 1))
      fi
    fi
  done < <(grep "ref:" "$AGENT_DIR/workflow.yaml" 2>/dev/null)
  [ "$REF_MISSING" -eq 0 ] && check_pass "S1: 所有 ref 檔案存在"
fi

# --- 彙總 ---
echo ""
echo "=== 結果 ==="
TOTAL=$((PASS + FAIL + WARN))
echo -e "  通過: ${GREEN}${PASS}${NC} / ${TOTAL}"
echo -e "  失敗: ${RED}${FAIL}${NC}"
echo -e "  警告: ${YELLOW}${WARN}${NC}"
echo ""
if [ "$FAIL" -eq 0 ]; then
  echo -e "  ${GREEN}PASS${NC} — Agent ${AGENT_PATH} 符合規範"
else
  echo -e "  ${RED}FAIL${NC} — Agent ${AGENT_PATH} 有 ${FAIL} 項未通過"
fi
