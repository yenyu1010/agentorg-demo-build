#!/usr/bin/env bash
# 打包 football agents 核心 → 可攜 bundle 給 Hermes Agent
set -e
ROOT=/home/user/agentorg-demo-build
OUT=/tmp/hermes-export
BUNDLE="$OUT/football"
rm -rf "$OUT"; mkdir -p "$BUNDLE"

# 1) 複製 agent 定義 + memory，排除 runtime worklog 日誌(保留空目錄結構)
cd "$ROOT/agents"
cp -r football/. "$BUNDLE/"
# 清掉 worklog 下的執行日誌(只留 .gitkeep)
find "$BUNDLE" -path "*/worklog/*.json" -delete

# 2) 一併帶上「足球專屬」的分析腳本(公式+各場 calc)
mkdir -p "$BUNDLE/_scripts"
cp "$ROOT/.claude/scripts/half_goal_from_line.py" "$BUNDLE/_scripts/" 2>/dev/null || true

# 3) 寫 MANIFEST
cat > "$BUNDLE/MANIFEST.md" <<'MD'
# Football Analysis Team — 可攜 Bundle (for Hermes Agent)

## 內含(核心)
- manager / odds-analyst / form-analyst / value-modeler 四個 agent 完整定義
  (soul.md / skills.md / tools.md / org.md / agent.yaml / workflow.yaml / workflow/*.md)
- 各 agent 的 memory/ (含累積學問):
  - value-modeler/memory/calibration-notes.md  ← 公式校準證據、待調係數
  - value-modeler/memory/track-record.md       ← 每筆推薦的歷史與盈虧
  - manager/memory/*.md                        ← 任務回顧
- value-modeler/skills.md 已含: §1c滾球 / §1d水位對照 / §1e即場進球公式+操作規則 / §1f走地民間訊號庫 / §5b勝率軸
- _scripts/half_goal_from_line.py             ← 即場進球公式腳本
- worklog/ 僅保留空結構(.gitkeep),已移除 runtime 日誌

## 搬進 Hermes Agent 後,需另外確保的「外部相依」(本 bundle 未含,因屬共用基建)
1. scripts/worklog.sh                 — 打卡腳本(天條),agent 每次開收工要呼叫
2. agents/protocols/                  — worklog-protocol / memory-protocol / hitl / verification 等
   (football agent 的 workflow 會 ref 這些 protocol)
3. (選用) .claude/skills/S33-football/SKILL.md — 斜線指令入口(你這次選「只搬 agents 核心」,未含)
4. reports_to 鏈: manager/agent.yaml 寫 reports_to: user;若 Hermes 有上層 Officer/Director,需調整

## 啟動方式(在 Hermes Agent 內)
- 直接呼叫 football/manager/agent.yaml 的 bootstrap;或建一個入口 skill 指向它
- value-modeler 是核心,公式/技巧都在它的 skills.md

## 版本
- 匯出自 agentorg-demo-build @ 2026-06-15
- 原專案保留完整副本(本次為「複製」非「移動」)
MD

# 4) 打包
cd "$OUT"
tar -czf "$OUT/hermes-football-bundle.tar.gz" football
echo "BUNDLE: $OUT/hermes-football-bundle.tar.gz"
echo "檔數: $(find "$BUNDLE" -type f | wc -l)  大小: $(du -sh "$OUT/hermes-football-bundle.tar.gz" | cut -f1)"
