#!/usr/bin/env python3
"""完整版 Hermes bundle：S33-football skill + football agents + 共用相依(protocols/worklog.sh) + 一鍵安裝。"""
import os, re, json, shutil, datetime, tarfile

ROOT = "/home/user/agentorg-demo-build"
OUT = "/tmp/hermes-complete-export"
BUNDLE = os.path.join(OUT, "hermes-football-complete")

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(BUNDLE)

# ---------- 1) skill (sanitized + version) ----------
def sanitize(t):
    for a, b in [(r"Claude Code", "Hermes Agent（或相容的 agent runtime）"),
                 (r"Claude tools", "agent tools"),
                 (r"\.claude/skills", ".hermes/skills"),
                 (r"\.claude/", ".hermes/"), (r"`\.claude`", "`.hermes`"),
                 (r"CLAUDE_PLUGIN_ROOT", "HERMES_PLUGIN_ROOT")]:
        t = re.sub(a, b, t)
    return t

skill_out = os.path.join(BUNDLE, "skills", "S33-football")
os.makedirs(skill_out)
with open(os.path.join(ROOT, ".claude/skills/S33-football/SKILL.md"), encoding="utf-8") as f:
    raw = f.read()
m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
fm, body = (m.group(1), m.group(2)) if m else ("", raw)
def gf(fm, k):
    mm = re.search(rf"^{k}:\s*(.+)$", fm, re.M); return mm.group(1).strip() if mm else None
name = gf(fm, "name") or "S33-football"
desc = sanitize(gf(fm, "description") or "Football analysis entry skill.")
allowed = gf(fm, "allowed-tools")
fm_lines = [f"name: {name}", f"description: {desc}", 'version: "1.0.0"']
if allowed: fm_lines.append(f"allowed-tools: {allowed}")
with open(os.path.join(skill_out, "SKILL.md"), "w", encoding="utf-8") as f:
    f.write("---\n" + "\n".join(fm_lines) + "\n---\n" + sanitize(body))

# ---------- 2) football agents (定義+memory, 去 runtime worklog) ----------
shutil.copytree(os.path.join(ROOT, "agents/football"), os.path.join(BUNDLE, "agents/football"))
for dp, dn, fn in os.walk(os.path.join(BUNDLE, "agents/football")):
    if os.path.basename(dp) == "worklog":
        for x in fn:
            if x.endswith(".json"): os.remove(os.path.join(dp, x))

# ---------- 3) 共用相依: protocols + worklog.sh + 公式腳本 ----------
shutil.copytree(os.path.join(ROOT, "agents/protocols"), os.path.join(BUNDLE, "agents/protocols"))
os.makedirs(os.path.join(BUNDLE, "scripts"))
shutil.copy(os.path.join(ROOT, "scripts/worklog.sh"), os.path.join(BUNDLE, "scripts/worklog.sh"))
os.makedirs(os.path.join(BUNDLE, "_scripts"))
shutil.copy(os.path.join(ROOT, ".claude/scripts/half_goal_from_line.py"), os.path.join(BUNDLE, "_scripts/half_goal_from_line.py"))

# ---------- 4) manifest.json ----------
manifest = {
    "bundle": "hermes-football-complete",
    "bundle_version": "1.0.0",
    "generated": datetime.date.today().isoformat(),
    "skills": [{
        "name": "S33-football", "path": "skills/S33-football",
        "description": desc,
        "source": ".claude/skills/S33-football (agentorg-demo-build)",
        "target": "$HERMES_SKILLS_DIR | $HOME/.hermes/skills | $HOME/AppData/Local/hermes/skills"
    }],
    "agents": [{
        "name": "football", "path": "agents/football",
        "description": "足球分析組: manager + odds-analyst + form-analyst + value-modeler (含 skills/memory)",
        "source": "agents/football (agentorg-demo-build)",
        "target": "$HERMES_HOME/agents/football"
    }],
    "shared_dependencies": [
        {"name": "protocols", "path": "agents/protocols", "target": "$HERMES_HOME/agents/protocols"},
        {"name": "worklog.sh", "path": "scripts/worklog.sh", "target": "$HERMES_HOME/scripts/worklog.sh"}
    ],
    "root_env": "AGENTORG_ROOT 應指向 $HERMES_HOME(含 agents/protocols/definitions.md), 供 skill Step 0 定位根目錄"
}
with open(os.path.join(BUNDLE, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# ---------- 5) install.sh ----------
install = r'''#!/usr/bin/env bash
# Hermes football — 一鍵安裝 (Git Bash / Linux / macOS)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 根目錄(放 agents/protocols/scripts)
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"

# skills 目錄
if [ -n "${HERMES_SKILLS_DIR:-}" ]; then
  SKILLS_DIR="$HERMES_SKILLS_DIR"
elif printf '%s' "${OSTYPE:-}$(uname -s 2>/dev/null)" | grep -qiE 'mingw|msys|cygwin|windows'; then
  SKILLS_DIR="$HOME/AppData/Local/hermes/skills"
else
  SKILLS_DIR="$HERMES_HOME/skills"
fi

echo "HERMES_HOME = $HERMES_HOME"
echo "SKILLS_DIR  = $SKILLS_DIR"

mkdir -p "$SKILLS_DIR" "$HERMES_HOME/agents" "$HERMES_HOME/scripts"
cp -R "$SCRIPT_DIR/skills/." "$SKILLS_DIR/"
cp -R "$SCRIPT_DIR/agents/." "$HERMES_HOME/agents/"
cp -R "$SCRIPT_DIR/scripts/." "$HERMES_HOME/scripts/"
cp -R "$SCRIPT_DIR/_scripts" "$HERMES_HOME/" 2>/dev/null || true
chmod +x "$HERMES_HOME/scripts/worklog.sh" 2>/dev/null || true

echo
echo "安裝完成。"
echo "  skills → $SKILLS_DIR"
echo "  agents → $HERMES_HOME/agents (含 football + protocols)"
echo "  worklog.sh → $HERMES_HOME/scripts"
echo
echo ">>> 最後一步(讓 skill 找得到根目錄): 把下面這行加進你的 shell profile <<<"
echo "    export AGENTORG_ROOT=\"$HERMES_HOME\""
'''
with open(os.path.join(BUNDLE, "install.sh"), "w", encoding="utf-8") as f:
    f.write(install)
os.chmod(os.path.join(BUNDLE, "install.sh"), 0o755)

# ---------- 6) README.md ----------
readme = f"""# Hermes Football — Complete Bundle (裝完即用)

足球分析組完整包：**入口 skill + 4 個 agent + 共用相依**，一鍵安裝。

## 結構
```
hermes-football-complete/
├── manifest.json
├── install.sh
├── skills/S33-football/SKILL.md     # 斜線指令入口(已通用化, version 1.0.0)
├── agents/
│   ├── football/                    # manager + odds-analyst + form-analyst + value-modeler (含 skills/memory)
│   └── protocols/                   # 共用協定(worklog/memory/hitl/verification + workflows)
├── scripts/worklog.sh               # 打卡天條腳本
└── _scripts/half_goal_from_line.py  # 即場進球公式
```

## 安裝
```bash
bash install.sh
# 然後照畫面提示,把 export AGENTORG_ROOT=... 加進 shell profile
```
路徑：
- skills → `$HERMES_SKILLS_DIR` 或 `$HOME/.hermes/skills`(Git Bash: AppData/Local/hermes/skills)
- agents/scripts → `$HERMES_HOME`(預設 `$HOME/.hermes`)
- 自訂：`HERMES_HOME=/x HERMES_SKILLS_DIR=/y bash install.sh`

## 為什麼要 AGENTORG_ROOT
skill 的 Step 0 會定位「根目錄」(找 `agents/protocols/definitions.md`)。設好 `AGENTORG_ROOT=$HERMES_HOME` 是**最穩**的定位方式(skill 的方式 B),省去 symlink/路徑推斷的不確定。

## 人工檢查(剩這幾項)
1. **AGENTORG_ROOT 必設**：沒設的話 skill 可能定位不到 agents。install.sh 會印出該設什麼。
2. **reports_to 鏈**：football/manager 的 agent.yaml 寫 `reports_to: user`；若 Hermes 有上層 Officer/Director 要調。
3. **HERMES_PLUGIN_ROOT**：skill 內 plugin 變數已從 Claude 改名;若 Hermes runtime 用別的變數名,對應改。
4. **runtime 差異**：skill 提到「subagent 葉節點限制」是 Claude Code 行為;若 Hermes 的 subagent 能再分派,該段限制可放寬(不影響安裝,只影響 manager 是否能在 subagent 內 dispatch)。

## 來源
匯出自 agentorg-demo-build @ {datetime.date.today().isoformat()}(複製,原專案保留)。
"""
with open(os.path.join(BUNDLE, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)

# ---------- 7) 打包 ----------
tar_path = os.path.join(OUT, "hermes-football-complete.tar.gz")
with tarfile.open(tar_path, "w:gz") as t:
    t.add(BUNDLE, arcname="hermes-football-complete")

nfiles = sum(len(fn) for _, _, fn in os.walk(BUNDLE))
print("TARBALL:", tar_path)
print("檔數:", nfiles, " 解開大小:", end=" ")
print(os.popen(f"du -sh {BUNDLE}").read().split()[0])
print("頂層:")
for x in sorted(os.listdir(BUNDLE)): print("  ", x)
