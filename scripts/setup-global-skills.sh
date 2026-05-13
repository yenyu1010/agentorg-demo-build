#!/usr/bin/env bash
# =============================================================================
# setup-global-skills.sh
# 用途：動態掃描 AgentOrg 專案的 .claude/skills/ 下所有 skill 子目錄，
#       並在用戶級 ~/.claude/skills/ 建立 Junction（Windows）或 symlink
#       （macOS/Linux），讓任何專案都能呼叫 /tuq-* 等全域 skill。
#
# 使用方式：
#   bash scripts/setup-global-skills.sh
#
# 執行環境：
#   - Windows：需要在有系統管理員權限的 shell（或已開啟開發者模式）執行
#   - macOS/Linux：一般用戶即可
#
# 輸出摘要：
#   LINKED   - 成功建立新的 Junction/symlink
#   SKIPPED  - 目標已存在且是 Junction/symlink，無需重建
#   WARNING  - 目標已存在但不是 Junction/symlink（普通目錄），需手動處理
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# 路徑設定
# ---------------------------------------------------------------------------
# 腳本所在目錄的上一層即為 AgentOrg 專案根目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$PROJECT_ROOT/.claude/skills"

# 用戶級目標目錄
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
  # Windows（Git Bash / MSYS2 / Cygwin）
  DST_DIR="$USERPROFILE/.claude/skills"
  IS_WINDOWS=true
else
  # macOS / Linux
  DST_DIR="$HOME/.claude/skills"
  IS_WINDOWS=false
fi

# ---------------------------------------------------------------------------
# 前置檢查
# ---------------------------------------------------------------------------
if [[ ! -d "$SRC_DIR" ]]; then
  echo "ERROR: 來源目錄不存在：$SRC_DIR"
  exit 1
fi

echo "=== setup-global-skills.sh ==="
echo "來源目錄：$SRC_DIR"
echo "目標目錄：$DST_DIR"
echo ""

# 確保目標根目錄存在
mkdir -p "$DST_DIR"

# ---------------------------------------------------------------------------
# 計數器
# ---------------------------------------------------------------------------
COUNT_LINKED=0
COUNT_SKIPPED=0
COUNT_WARNING=0

# ---------------------------------------------------------------------------
# 判斷路徑是否為 Junction（Windows）或 symlink（Unix）
# ---------------------------------------------------------------------------
is_junction_or_symlink() {
  local path="$1"
  if [[ -L "$path" ]]; then
    # Unix symlink
    return 0
  fi
  if [[ "$IS_WINDOWS" == "true" ]]; then
    # Windows：用 PowerShell 判斷是否為 Junction
    local result
    result=$(powershell.exe -NoProfile -Command \
      "(Get-Item -LiteralPath '$path' -ErrorAction SilentlyContinue).LinkType" 2>/dev/null || true)
    if [[ "$result" == "Junction" ]]; then
      return 0
    fi
  fi
  return 1
}

# ---------------------------------------------------------------------------
# 建立 Junction（Windows）或 symlink（Unix）
# ---------------------------------------------------------------------------
create_link() {
  local src="$1"
  local dst="$2"

  if [[ "$IS_WINDOWS" == "true" ]]; then
    # 轉換為 Windows 路徑格式供 PowerShell 使用
    local win_src win_dst
    win_src=$(cygpath -w "$src" 2>/dev/null || echo "$src" | sed 's|/|\\|g')
    win_dst=$(cygpath -w "$dst" 2>/dev/null || echo "$dst" | sed 's|/|\\|g')
    powershell.exe -NoProfile -Command \
      "New-Item -ItemType Junction -Path '$win_dst' -Target '$win_src'" \
      > /dev/null 2>&1
  else
    ln -s "$src" "$dst"
  fi
}

# ---------------------------------------------------------------------------
# 動態掃描並處理每個 skill 子目錄
# ---------------------------------------------------------------------------
for skill_dir in "$SRC_DIR"/*/; do
  # 確認是目錄（排除萬用字元未匹配的情況）
  [[ -d "$skill_dir" ]] || continue

  skill_name="$(basename "$skill_dir")"
  # 去掉尾部斜線以取得完整路徑
  skill_src="${skill_dir%/}"
  skill_dst="$DST_DIR/$skill_name"

  if [[ -e "$skill_dst" ]] || [[ -L "$skill_dst" ]]; then
    # 目標已存在 — 判斷類型
    if is_junction_or_symlink "$skill_dst"; then
      echo "  SKIPPED  $skill_name  （已是 Junction/symlink，略過）"
      COUNT_SKIPPED=$((COUNT_SKIPPED + 1))
    else
      echo "  WARNING  $skill_name  （目標存在且為普通目錄，請手動處理：$skill_dst）"
      COUNT_WARNING=$((COUNT_WARNING + 1))
    fi
  else
    # 目標不存在 — 建立連結
    if create_link "$skill_src" "$skill_dst"; then
      echo "  LINKED   $skill_name  → $skill_src"
      COUNT_LINKED=$((COUNT_LINKED + 1))
    else
      echo "  WARNING  $skill_name  （建立連結失敗，請確認權限）"
      COUNT_WARNING=$((COUNT_WARNING + 1))
    fi
  fi
done

# ---------------------------------------------------------------------------
# 摘要輸出
# ---------------------------------------------------------------------------
echo ""
echo "=============================="
echo "摘要："
echo "  LINKED  : $COUNT_LINKED"
echo "  SKIPPED : $COUNT_SKIPPED"
echo "  WARNING : $COUNT_WARNING"
echo "=============================="

if [[ "$COUNT_WARNING" -gt 0 ]]; then
  echo ""
  echo "有 $COUNT_WARNING 個項目需要手動處理（見上方 WARNING 訊息）。"
  exit 1
fi

# ---------------------------------------------------------------------------
# 權限檢查提示
# ---------------------------------------------------------------------------
echo ""
echo "=== 權限檢查 ==="
echo "AgentOrg 需要以下 bypass 權限才能正常運作："
echo "  Bash(*), Read, Write, Edit, Glob, Grep, Agent, WebFetch(*), WebSearch(*), Skill(*)"
echo ""
echo "建議在你的專案中開啟 AgentOrg 後，Claude 會自動讀取 .claude/settings.json 中的權限。"
echo "若仍被詢問權限，請在 Claude Code 中執行："
echo "  /allowed-tools"
echo "確認以上工具已允許。"

echo "完成。"
