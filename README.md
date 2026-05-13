# AgentOrg Demo — Agent Ops & Edu Teams

這是 **AgentOrg** 多代理人編排系統的精簡示範包，只含兩個 team：

- **`agent-ops/`** — Agent 系統管理：建立、演化、治理 agent 自身
- **`edu/`** — 教材內容團隊：研究 → 設計 → 生成 PPT / Word / PDF

完整版本還包含 sw、sales、bni、finance、platform 等 team。本示範包**已經移除歷史 worklog/memory** 與內部專案產出檔，是一個乾淨可跑的起點。

---

## 安裝

**👉 詳細步驟請看 [INSTALL.md](INSTALL.md)**

最快路徑（裝過 Claude Code 的人）：

```bash
unzip AgentOrg-Demo.zip -d C:\AgentOrg-Demo
cd C:\AgentOrg-Demo
pip install python-pptx python-docx Pillow
claude
# 然後在 Claude Code 裡輸入 /tuq-edu 或 /tuq-agent
```

---

## 一、第一次跑跑看

### 範例 1：請 edu team 做一份簡報

在 Claude Code 裡輸入：

```
/tuq-edu 幫我做一份「Claude Code 入門」30 分鐘的教學簡報，目標受眾是新進工程師
```

`tuq-edu` skill 會：
1. 派 `edu-researcher` 研究主題
2. 派 `content-designer` 設計章節結構
3. 派 `visual-stylist` 設計視覺風格
4. 派 `doc-generator` 產出 pptx
5. 派 `qa-reviewer` 驗收
6. 產出檔案放在 `tuq_log/output/`

### 範例 2：請 Agent Ops 同步 / 修改 agent

```
/tuq-agent 幫 edu/manager 加一條 skill：「跨 team 協作時主動同步 agent-ops/manager」
```

Agent Ops Manager 會派 `agent-builder` 執行修改，並由 `governance` 審查。

---

## 二、目錄結構

```
AgentOrg-Demo/
├── .claude/
│   ├── settings.json          # Claude Code 權限設定
│   └── skills/                # skill 鏡像（auto-load）
│       ├── tuq-agent/
│       └── tuq-edu/
├── agents/
│   ├── agent-ops/             # Agent 系統管理 team
│   │   ├── manager/
│   │   ├── agent-builder/
│   │   ├── governance/
│   │   └── evolution/
│   ├── edu/                   # 教材團隊
│   │   ├── manager/
│   │   ├── edu-researcher/
│   │   ├── content-designer/
│   │   ├── content-evaluator/
│   │   ├── visual-stylist/
│   │   ├── doc-generator/
│   │   └── qa-reviewer/
│   ├── protocols/             # 共用協議（worklog / memory / scope guard 等）
│   └── worklogs/              # 中央 worklog index（空）
├── skills/
│   ├── tuq-agent/SKILL.md     # Agent Ops 入口
│   └── tuq-edu/SKILL.md       # Edu 入口
├── scripts/
│   ├── worklog.sh             # 每個 agent 必跑的打卡腳本
│   ├── setup-global-skills.sh # 全域 skill 安裝
│   ├── convert_md_to_docx*.py # Word 生成
│   ├── generate_pptx.py / .js # PPT 生成
│   └── ...
├── CLAUDE.md                  # 專案指引（給 Claude Code 讀）
├── INSTALL.md                 # 安裝指南
└── README.md                  # 本檔
```

---

## 三、Agent 解剖學

每個 agent 資料夾長這樣：

| 檔案 | 用途 |
|------|------|
| `agent.yaml` | 入口：bootstrap 順序 + dispatch 模型 + 觸發規則 |
| `soul.md` | 人格、原則、反模式 |
| `tools.md` | 系統能力（Read / Write / Bash / Agent ...） |
| `skills.md` | 領域技能 |
| `org.md` | 組織角色與回報關係 |
| `workflow.yaml` | 執行流程骨架（每步指向 `workflow/*.md`） |
| `workflow/` | 每個步驟的詳細流程 |
| `memory/` | 跨會話記憶（agent 自己讀寫） |
| `worklog/` | 每次執行的時間戳記日誌 |

**核心規則**：「加法自己來，減法和擴權要審批。」Agent 可以加 skill / 加 workflow step / 寫 memory / 寫 worklog；要刪、改 soul/tools 必須走 Agent Builder。

詳見 `agents/protocols/definitions.md` 和 `agents/protocols/rules/agent-anatomy.md`。

---

## 四、常見問題

### Q1. 跑了之後沒看到 `/tuq-edu` skill？

→ 看 [INSTALL.md](INSTALL.md) 第八節 Q1

### Q2. doc-generator 報錯 `python-pptx not found`？

→ 看 [INSTALL.md](INSTALL.md) 第八節 Q2

### Q3. 想把這個 demo 砍掉重來？

→ 看 [INSTALL.md](INSTALL.md) 第八節 Q7

### Q4. `agents/protocols/definitions.md` 與 `rdv-protocol.md` 提到一堆不在 demo 內的 team / agent？

對。完整版有 6 個 team，這個 demo 只取 2 個。詳見「五、與完整 AgentOrg 的差異」。簡單說：那些是參考資料，本 demo 不會也不能 dispatch 它們。

---

## 五、與完整 AgentOrg 的差異

完整 AgentOrg 系統包含 **6 個 team / 30+ agent**。本 demo 是其中一個子集，**只含 agent-ops + edu**。

`agents/protocols/` 下的 markdown 檔（特別是 `definitions.md`、`rdv-protocol.md`）是**完整系統**的協議文件，會提到下列**不在這個 demo** 的 team / agent：

| 缺席的 team / agent | 用途 | 引用之處 |
|---|---|---|
| `agents/sw/` | 軟體開發（manager / architect / developer / reviewer / tester / devops） | definitions.md File Ownership 表 |
| `agents/sales/` | 業務 / 提案（manager / industry-researcher / partnership-strategist / proposal-designer 等） | definitions.md, rdv-protocol.md §11.3 |
| `agents/bni/` | BNI 會員資料分析（manager / extract / label / industry-groups 等） | definitions.md File Ownership |
| `agents/finance/` | 財務請款（manager / billing-builder / billing-renderer / billing-qa） | definitions.md §「Finance Team」全段 |
| `agents/platform/` | DGX GB10 + Goose 平台維運 | definitions.md §「Platform Team」全段 |
| `agents/shared/calculator/` | 共用計算 agent（精確數值計算委派目標） | definitions.md §「計算委派規則」 |

**讀到這些路徑時**：
- 知道是參考用即可，不必跟著去找
- 本 demo 兩個 manager（agent-ops/manager、edu/manager）都已經自我隔離，不會 dispatch 它們
- 若你想新增 team，可請 `agent-ops/agent-builder` 幫忙建立（這就是 agent-ops team 的工作）

完整 AgentOrg 是內部系統，本 demo 已剔除歷史 worklog / memory / 實際產出檔，只保留 agent 定義（soul / skills / workflow），讓你看清楚架構並有起點可跑。

---

## 六、進一步閱讀

- [INSTALL.md](INSTALL.md) — 安裝指南 + 疑難排解
- `CLAUDE.md` — 給 Claude Code 看的專案指引
- `agents/protocols/definitions.md` — Agent 系統定義
- `agents/protocols/rules/agent-anatomy.md` — Manager / Worker 強制結構
- `agents/protocols/worklog-protocol.md` — 打卡規則（天條）
- `agents/protocols/memory-protocol.md` — 記憶協議

---

來源：AgentOrg（內部）  
匯出時間：2026-04-28
