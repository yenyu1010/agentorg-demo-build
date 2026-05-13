---
name: tuq-edu
description: 教育組入口。接收教材需求，分派研究→設計→生成 PPT/Word/PDF。
allowed-tools: Glob Grep Read Bash
---

## User Request

$ARGUMENTS

## Step 0 — 定位 AgentOrg 根目錄（必做，只做一次）

本 skill 的所有檔案路徑都相對於 AgentOrg 專案根目錄（以下稱 `<ROOT>`）。
依序嘗試下列 4 種方式，第一個成功者即採用：

**方式 A — Plugin 模式（marketplace install）**
若下一行的 `${CLAUDE_PLUGIN_ROOT}` 已被 Claude Code 替換成實際路徑（非字面量），取之；否則跳過。
> CLAUDE_PLUGIN_ROOT: `${CLAUDE_PLUGIN_ROOT}`

**方式 B — 環境變數覆寫**
```bash
bash -c 'echo "${AGENTORG_ROOT:-}"'
```
非空且該路徑下存在 `agents/protocols/definitions.md` 則取之。

**方式 C — 全域 symlink 反查（setup-global-skills.sh install）**
```bash
python3 -c "import os; p=os.path.realpath(os.path.expanduser('~/.claude/skills/tuq-edu/SKILL.md')); r=os.path.abspath(os.path.join(os.path.dirname(p),'..','..','..')); print(r if os.path.isfile(os.path.join(r,'agents','protocols','definitions.md')) else '')"
```
輸出非空則取之。（反推 3 層：`tuq-edu/` → `skills/` → `.claude/` → `<ROOT>`）

**方式 D — CWD 上溯**
從當前工作目錄向上逐層檢查是否存在 `agents/protocols/definitions.md`，命中即為 `<ROOT>`。

**四者皆失敗時**：停止執行並回報
「無法定位 AgentOrg 根目錄。請執行 `bash scripts/setup-global-skills.sh` 完成全域安裝，或設定環境變數 `AGENTORG_ROOT=<AgentOrg 絕對路徑>`」。

取得 `<ROOT>` 後，**後續所有 Read/Glob/Grep 一律使用絕對路徑** `<ROOT>/agents/...`，嚴禁相對路徑。

## Step 0.5 — 初始化 tuq_log/（呼叫端工作區）

當 CWD 不等於 `<ROOT>` 時，在 CWD 建立本地工作區：

```bash
TUQ_LOG="$(pwd)/tuq_log"
mkdir -p "$TUQ_LOG/worklogs" "$TUQ_LOG/output" "$TUQ_LOG/tmp"
# 防止被呼叫端的 git 追蹤
if [ ! -f "$TUQ_LOG/.gitignore" ]; then echo "*" > "$TUQ_LOG/.gitignore"; fi
```

當 CWD 等於 `<ROOT>` 時，跳過此步驟（agent 產出直接留在 AgentOrg 內）。

後續所有 agent dispatch 時傳入 worklog mirror 路徑：
- `--mirror-to "$TUQ_LOG/worklogs"` 加在 `scripts/worklog.sh` 呼叫中
- Agent 產出寫入 `$TUQ_LOG/output/`
- 暫存檔寫入 `$TUQ_LOG/tmp/`

## Instructions

You are the Edu Manager.
讀取 agent.yaml 入口，依其 bootstrap sequence 與 workflow 執行：
`<ROOT>/agents/edu/manager/agent.yaml`

Bootstrap sequence (defined in agent.yaml):
1. Read `<ROOT>/agents/edu/manager/soul.md` (identity, principles)
2. Read `<ROOT>/agents/edu/manager/org.md` (organization, hierarchy)
3. Read `<ROOT>/agents/edu/manager/tools.md` (authorized tools)
4. Execute `<ROOT>/agents/edu/manager/workflow.yaml` (workflow steps including log_start/log_end)

## language

繁體中文
