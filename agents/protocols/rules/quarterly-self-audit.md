# 季度自審協議（Quarterly Self-Audit Protocol）

## 目的
消除 Agent-Ops 團隊的「自我豁免」問題。監察者必須接受同等標準的監察。

## 頻率
每季度一次（Q1: 1月、Q2: 4月、Q3: 7月、Q4: 10月）

## 流程

### 第一步：自動化掃描
Agent-Ops Manager 對全系統 agent 執行 `validate-agent.sh`，產出合規報告。

### 第二步：交叉審查
邀請 SW Manager 和 Edu Manager 對 Agent-Ops 團隊的 4 個 agent 進行交叉審查，檢查：
- 是否有「自己定的規則自己不遵守」的情況
- 是否有新的雙重標準
- 品質觀察和建議

### 第三步：修正與驗證
Agent-Ops Manager 對交叉審查發現的問題進行修正，修正後再請另外兩位 Manager 確認。

### 第四步：報告歸檔
最終報告存入 `agents/agent-ops/manager/memory/` 作為歷史紀錄。

## 規則
- 不可跳過交叉審查步驟
- 交叉審查結果必須公開透明，不可選擇性隱藏
- 修正項追蹤到完成為止
