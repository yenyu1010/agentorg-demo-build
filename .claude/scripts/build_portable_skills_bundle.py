#!/usr/bin/env python3
"""把 S33-football skill 打包成 portable-skills-bundle (for Hermes Agent)。"""
import os, re, json, shutil, datetime

ROOT = "/home/user/agentorg-demo-build"
SKILL_SRC = os.path.join(ROOT, ".claude/skills/S33-football")
OUT = "/tmp/portable-skills-export"
BUNDLE = os.path.join(OUT, "portable-skills-bundle")
SKILL_NAME = "S33-football"
AUX_DIRS = ["references", "scripts", "templates", "assets"]

# ---- 重建輸出目錄 ----
if os.path.exists(OUT): shutil.rmtree(OUT)
skill_out = os.path.join(BUNDLE, "skills", SKILL_NAME)
os.makedirs(skill_out)

# ---- 讀 SKILL.md ----
with open(os.path.join(SKILL_SRC, "SKILL.md"), encoding="utf-8") as f:
    raw = f.read()

# ---- 解析 / 補 frontmatter (name, description, version) ----
m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
notes = []
if m:
    fm, body = m.group(1), m.group(2)
else:
    fm, body = "", raw
    notes.append("原 SKILL.md 無 YAML frontmatter，已新增。")

def get_field(fm, key):
    mm = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return mm.group(1).strip() if mm else None

name = get_field(fm, "name") or SKILL_NAME
desc = get_field(fm, "description") or "Football match analysis skill."
ver  = get_field(fm, "version")
if not ver:
    ver = "1.0.0"
    notes.append("frontmatter 缺 version，已補 1.0.0。")

# ---- Claude 專屬用語 → 通用 / Hermes 相容 ----
def sanitize(text):
    repl = [
        (r"Claude Code", "Hermes Agent（或相容的 agent runtime）"),
        (r"Claude tools", "agent tools"),
        (r"\.claude/skills", ".hermes/skills"),
        (r"\.claude/", ".hermes/"),
        (r"`\.claude`", "`.hermes`"),
        (r"CLAUDE_PLUGIN_ROOT", "HERMES_PLUGIN_ROOT"),
    ]
    for a, b in repl:
        text = re.sub(a, b, text)
    return text

body_s = sanitize(body)
desc_s = sanitize(desc)

# ---- 重組 frontmatter(只保留通用必要欄位 + 保留 allowed-tools 若有) ----
allowed = get_field(fm, "allowed-tools")
fm_lines = [f"name: {name}", f"description: {desc_s}", f'version: "{ver}"']
if allowed:
    fm_lines.append(f"allowed-tools: {allowed}")
new_skill = "---\n" + "\n".join(fm_lines) + "\n---\n" + body_s
with open(os.path.join(skill_out, "SKILL.md"), "w", encoding="utf-8") as f:
    f.write(new_skill)

# ---- 複製輔助資料夾(若存在) ----
for d in AUX_DIRS:
    src = os.path.join(SKILL_SRC, d)
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(skill_out, d))

# ---- manifest.json ----
manifest = {
    "bundle": "portable-skills-bundle",
    "bundle_version": "1.0.0",
    "generated": datetime.date.today().isoformat(),
    "skills": [{
        "name": name,
        "path": f"skills/{SKILL_NAME}",
        "description": desc_s,
        "source": ".claude/skills/S33-football (agentorg-demo-build)",
        "target": "$HERMES_SKILLS_DIR | $HOME/.hermes/skills (Linux/macOS) | $HOME/AppData/Local/hermes/skills (Git Bash)"
    }],
}
with open(os.path.join(BUNDLE, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# ---- install.sh ----
install = r'''#!/usr/bin/env bash
# Portable skills installer (Git Bash / Linux / macOS)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -n "${HERMES_SKILLS_DIR:-}" ]; then
  TARGET="$HERMES_SKILLS_DIR"
elif printf '%s' "${OSTYPE:-}$(uname -s 2>/dev/null)" | grep -qiE 'mingw|msys|cygwin|windows'; then
  TARGET="$HOME/AppData/Local/hermes/skills"
else
  TARGET="$HOME/.hermes/skills"
fi

echo "Installing skills to: $TARGET"
mkdir -p "$TARGET"
cp -R "$SCRIPT_DIR/skills/." "$TARGET/"
echo "Done. Installed skills:"
ls -1 "$TARGET"
'''
with open(os.path.join(BUNDLE, "install.sh"), "w", encoding="utf-8") as f:
    f.write(install)
os.chmod(os.path.join(BUNDLE, "install.sh"), 0o755)

# ---- README.md ----
readme = f"""# Portable Skills Bundle (for Hermes Agent)

可攜式 skill bundle，匯出自 agentorg-demo-build。

## 內含
- `skills/{SKILL_NAME}/SKILL.md` — {name}（version {ver}）
- `manifest.json` — skill 清單(name/path/description/source/target)
- `install.sh` — 跨平台安裝器

## 安裝
```bash
bash install.sh
```
安裝路徑(依序)：
1. `$HERMES_SKILLS_DIR`(若有設定)
2. Git Bash(Windows)：`$HOME/AppData/Local/hermes/skills`
3. Linux/macOS：`$HOME/.hermes/skills`

或自訂：`HERMES_SKILLS_DIR=/your/path bash install.sh`

## 匯入後注意(人工檢查)
- SKILL.md 的「Step 0 根目錄定位」原依賴 agentorg 專案結構(找 `agents/protocols/definitions.md`)。
  搬到 Hermes 後，這個 skill 是「足球分析組」的**入口**，它要能找到 `agents/football/manager/agent.yaml`。
  請確認 Hermes 內有對應的 agents/football 結構(見足球 bundle: hermes-football-bundle)。
- frontmatter 的 `HERMES_PLUGIN_ROOT`(原 CLAUDE_PLUGIN_ROOT)：若 Hermes runtime 用別的 plugin 變數名，請對應改。
- 符號連結反查路徑已由 `.claude/skills` 改為 `.hermes/skills`，與 install.sh 預設一致。

## 來源
- 匯出自 agentorg-demo-build @ {datetime.date.today().isoformat()}
- 原專案保留完整副本(本次為「複製」)
"""
with open(os.path.join(BUNDLE, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)

# ---- 打包 ----
tar_path = os.path.join(OUT, "portable-skills-bundle.tar.gz")
import tarfile
with tarfile.open(tar_path, "w:gz") as t:
    t.add(BUNDLE, arcname="portable-skills-bundle")

print("BUNDLE_DIR:", BUNDLE)
print("TARBALL:", tar_path)
print("NOTES:", "; ".join(notes) if notes else "(無)")
print("\n--- 結構 ---")
for dp, dn, fn in os.walk(BUNDLE):
    for x in sorted(fn):
        print(os.path.relpath(os.path.join(dp, x), OUT))
