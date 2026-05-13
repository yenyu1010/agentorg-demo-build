# Evolution Analyze Flow

## 輸入（來自 Manager 或排程觸發）

```json
{
  "action": "analyze",
  "scope": "full | targeted",
  "focus": "optional — specific agent or issue area",
  "trigger": "manual | scheduled"
}
```

## 完整分析流程

```
[1] 外部研究（WebSearch）
  搜尋以下主題（每次選擇 2-3 個最相關的）：
    - "multi-agent system architecture best practices 2025"
    - "LLM agent role design organizational patterns"
    - "AI agent workflow anti-patterns"
    - "organizational design theory multi-agent"
  記錄：關鍵框架、模式、原則，作為後續分析的外部基準
  On error → continue（缺少外部基準時降級為純內部分析）
  │
  ▼
[2] 抓取參考資料（WebFetch）
  從步驟 [1] 的結果中，選 1-2 篇最相關的文章進行 WebFetch：
    - 優先選：架構設計論文、組織學應用案例、multi-agent 評測報告
    - 每篇摘要核心洞察 3-5 點（不逐字引用）
    - 將洞察轉化為「可對照現有系統的評估標準」
  On error → continue
  │
  ▼
[3] 收集內部指標（Worklog 分析）
  Glob agents/*/worklog/*.json
  逐批讀取近期 worklog（每次最多 5-10 個檔案）：
    - 提取：agent、status、duration_ms、task 描述
    - 計算：失敗率、平均時長、異常時長（outliers）
    - 彙整成矩陣：agent × 指標
  On error → continue（缺少 worklog 時降級）
  │
  ▼
[4] 識別模式和差距
  交叉分析內部指標 + 外部基準：
    - 按 agent / error type / 頻率分組失敗案例
    - 對照業界已知 anti-patterns
    - 以組織設計框架審視：分工是否合理、權責是否對稱
    - 找出「內部數據 + 外部標準」雙重確認的改善優先項
  Read agents/agent-ops/evolution/classification-principles.md
  On error → continue
  │
  ▼
[5] 提出改善提案（PARA 分類）
  為每個識別出的差距生成提案，包含：
    - 內部證據（worklog 數據、失敗模式）
    - 外部依據（業界實踐、組織學原則）
    - 對照差距分析
    - 影響力排序：頻率 × 嚴重性 ÷ 修復難度
    - PARA 分類：Project（立即執行）| Area（持續關注）| Resource（參考）| Archive（暫緩）
  On error → continue
  │
  ▼
[6] 路由提案
  依提案類型決定建議路由，並回傳 dispatch_plan 給 Manager，由 Manager 分派：
    - Agent-level 改動（soul/tools/skills/workflow）→ 建議 Manager 分派給 **Agent Builder**
    - 政策或協定改動（worklog/memory/evolution protocol）→ 建議 Manager 分派給 **Governance**
    - 結構性改動（新 agent、team 重組）→ 建議 Manager 分派給 **Architect + Agent Builder**
  注意：Evolution 沒有 Agent tool，不直接派遣其他 agent。所有分派行為由 Manager 執行。
  產出：dispatch_plan（每個提案的建議路由目標與優先順序）
  On error → continue（無法路由時回報給 Manager 手動決定）

RETURN 分析報告 + dispatch_plan 給 Manager
```
