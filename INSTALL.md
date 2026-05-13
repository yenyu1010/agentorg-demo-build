# AgentOrg Demo — 安裝指南

> 從 USB 拿到 `AgentOrg-Demo.zip`？跟著這份做完就能跑。預估 **10 分鐘**（不含下載 Claude Code 與 LibreOffice 的時間）。

---

## TL;DR — 給趕時間的人

```bash
# 1. 解壓
unzip AgentOrg-Demo.zip -d C:\AgentOrg-Demo

# 2. 裝 Python 套件（Claude Code 已裝省略）
pip install python-pptx python-docx Pillow

# 3. 開 Claude Code
cd C:\AgentOrg-Demo && claude

# 4. 在 Claude Code 裡輸入
/tuq-edu 給我做一份「Python 入門」的 30 分鐘簡報大綱
```

看到 manager 開始派遣 worker = 成功。

完整版往下看。

---

## 一、安裝前確認

### 必須裝的

| 工具 | 用途 | 下載 |
|---|---|---|
| **Claude Code** | 跑 agent 的引擎 | <https://docs.claude.com/claude-code> |
| **Python 3.10+** | edu team 生成 PPT/Word/PDF 用 | <https://www.python.org/downloads/> |
| **Bash** | worklog 打卡腳本必須的 shell | Windows 用 [Git Bash](https://git-scm.com/download/win)；macOS / Linux 內建 |

### 選裝的（看你要做什麼）

| 工具 | 何時要裝 |
|---|---|
| **LibreOffice** | 要把 pptx 轉 PDF / 預覽圖時。不裝就停在 pptx |
| **Node.js 18+** | 用 `generate_pptx.js` 路線時。純 Python 路線可不裝 |

### 確認版本

開一個 terminal 檢查：

```bash
claude --version       # 任何版本都行
python --version       # 3.10 以上
bash --version         # 任何版本
```

三個都能跑出版本號才繼續下一步。

---

## 二、解壓位置（重要）

### ✅ 推薦放這裡

| 系統 | 路徑 |
|---|---|
| Windows | `C:\AgentOrg-Demo\` |
| macOS | `~/AgentOrg-Demo/` |
| Linux | `~/AgentOrg-Demo/` |

### ❌ 不要放這裡

- 路徑含中文或空格（會踩 Bash 編碼坑）
- Google Drive / OneDrive / Dropbox **同步資料夾**（同步衝突會讓 worklog 寫入失敗）
- 桌面、下載、我的文件（這些通常被 OneDrive 同步）
- USB 直接執行（讀寫慢、拔掉就掛）

### 解壓指令

**Windows（PowerShell）**
```powershell
Expand-Archive -Path "$env:USERPROFILE\Downloads\AgentOrg-Demo.zip" -DestinationPath "C:\AgentOrg-Demo" -Force
```

**Windows（Git Bash） / macOS / Linux**
```bash
unzip ~/Downloads/AgentOrg-Demo.zip -d ~/AgentOrg-Demo
```

---

## 三、裝 Python 套件

```bash
pip install python-pptx python-docx Pillow
```

只有 edu team 的 `doc-generator` 會用到。**不裝**這幾個套件 demo 還是能跑，只是無法產 pptx/docx。

如果你電腦同時有 Python 2 和 3，用 `pip3`。

---

## 四、第一次啟動

```bash
cd C:\AgentOrg-Demo        # 或你解壓的位置
claude
```

Claude Code 啟動後，**確認 cwd 在解壓資料夾內**。`.claude/skills/` 下的兩個 skill 會自動載入：

```
/tuq-edu     — 教材生成入口（研究 → 設計 → PPT/Word/PDF）
/tuq-agent   — Agent 系統管理入口（建立、修改、治理 agent）
```

### 驗證安裝成功

在 Claude Code 裡輸入 `/`，看下拉選單有沒有 `tuq-edu` 與 `tuq-agent`。**有 → 安裝成功**。

如果只看到 `tuq-bni / tuq-sales` 等其他不在 demo 內的，代表你 cwd 弄錯了（指到別的 AgentOrg 安裝去了）。

---

## 五、跑第一個任務

```
/tuq-edu 給我做一份「Python 入門」的 30 分鐘簡報大綱，受眾是完全沒寫過程式的高中生
```

正常會看到：

1. `edu/manager` 接收需求、派遣
2. `edu-researcher` 研究主題、找 reference
3. `content-designer` 設計章節結構
4. `visual-stylist` 設計配色
5. `doc-generator` 生成 pptx
6. `qa-reviewer` 驗收

產出檔案會放在 **你執行 Claude Code 的當前目錄**下的 `tuq_log/output/`。

---

## 六、選用：全域安裝（任何資料夾都能 `/tuq-edu`）

如果你不想每次都 `cd` 到 demo 資料夾才能用，跑這個：

```bash
cd C:\AgentOrg-Demo
bash scripts/setup-global-skills.sh
```

它會在 `~/.claude/skills/` 建 symlink / Junction 指向 demo 的 skill 資料夾。

### Windows 注意事項

需要符合**任一個**條件才能建 Junction：

- 用「**以系統管理員身份執行**」的 Git Bash / PowerShell 跑
- 或事先打開**開發者模式**（設定 → 隱私權與安全性 → 開發人員專用）

### macOS / Linux 注意事項

如果 `cd` 出 demo 資料夾後 `/tuq-edu` 還是找不到 ROOT，加一條環境變數：

```bash
# ~/.zshrc 或 ~/.bashrc
export AGENTORG_ROOT="$HOME/AgentOrg-Demo"
```

加完 `source ~/.zshrc` 重新載入。

---

## 七、可選：LibreOffice（要 PDF 才裝）

| 系統 | 安裝指令 |
|---|---|
| Windows | <https://www.libreoffice.org/download/> 下載 .msi |
| macOS | `brew install --cask libreoffice` |
| Ubuntu / Debian | `sudo apt install libreoffice` |
| Fedora / RHEL | `sudo dnf install libreoffice` |

裝完不用設定，`pptx_to_images.py` 與 `gen-pptx-from-json.py` 會自動偵測 `soffice` 指令。

---

## 八、疑難排解

### Q1. `/tuq-edu` 沒出現在 skill 下拉選單

**檢查順序：**

```bash
# 1. 確認 cwd 對
pwd                                              # 應該是解壓資料夾
ls .claude/skills/                               # 應該看到 tuq-edu, tuq-agent

# 2. 重開 Claude Code session
# Ctrl+C 退出，重新 claude

# 3. 全域安裝若沒生效
ls ~/.claude/skills/                             # 應該看到 tuq-edu, tuq-agent symlink
```

### Q2. doc-generator 報錯 `ModuleNotFoundError: No module named 'pptx'`

```bash
pip install python-pptx python-docx Pillow
```

如果裝了還是失敗，檢查 Python 版本是否一致：

```bash
which python      # 你呼叫的 python
which pip         # pip 對應的 python
# 兩者要指到同一個 Python 安裝
```

### Q3. worklog.sh 報錯 `python3: command not found`

Windows 上 Python 可能叫 `python` 不叫 `python3`。建一個 alias：

```bash
# Git Bash 用戶 — ~/.bashrc 加
alias python3=python
```

或修 `scripts/_worklog_helper.py` 第一行 shebang 為 `#!/usr/bin/env python`。

### Q4. Bash 跑腳本一直跳「Permission denied」

Windows 環境下檔案沒有 +x 權限是正常的，用 `bash <script>` 而不是直接執行：

```bash
bash scripts/setup-global-skills.sh    # ✅
./scripts/setup-global-skills.sh       # ❌ 在 Windows 會失敗
```

### Q5. `setup-global-skills.sh` 失敗：`mklink: Access is denied`

Windows Junction 建立需要管理員或開發者模式（見第六節）。

### Q6. agent 跑到一半「找不到 agents/sw/...」之類的路徑

這是正常的。本 demo 只有 `agent-ops` + `edu` 兩個 team。`agents/protocols/definitions.md` 是完整 AgentOrg 的定義文件，會提到 `sw / sales / bni / finance / platform / shared` 等不在 demo 內的 team。詳見 `README.md` 第七節。

### Q7. 想砍掉重來

```bash
cd C:\AgentOrg-Demo
# 清空所有 worklog 與 memory（保留結構）
find agents -path '*/worklog/*' -type f -delete
find agents -path '*/memory/*' -type f ! -name MEMORY.md -delete
```

或直接刪整個資料夾再重新解壓 zip。

---

## 九、完全沒接觸過 Claude Code 的人

跳過這份 INSTALL.md 沒救，先看官方教學：

- 官方文件：<https://docs.claude.com/claude-code>
- 用什麼帳號：Anthropic API key（要付費）或 Claude.ai Pro/Max 帳號
- 第一次設定：跟著官方 quickstart 跑一遍 hello world，確認 `claude` 指令能用、能呼叫 LLM，再回來裝這個 demo

---

## 十、安裝完了，下一步？

| 想做什麼 | 看哪裡 |
|---|---|
| 系統架構是什麼？ | `README.md` 第四、五節 |
| Agent 怎麼設計的？ | `agents/agent-ops/manager/soul.md` |
| 想新增 agent？ | 用 `/tuq-agent` 請 agent-builder 幫你做 |
| 想改現有 agent？ | 同上，用 `/tuq-agent` |
| 不在 demo 內的 team 哪裡來的？ | `README.md` 第七節 |
| Worklog / memory 怎麼用？ | `agents/protocols/worklog-protocol.md` 與 `memory-protocol.md` |

---

來源：AgentOrg Demo  
最後更新：2026-04-28
