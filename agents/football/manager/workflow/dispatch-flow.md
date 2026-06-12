# Football Manager — Dispatch Flow

## Dispatch Protocol（所有 worker 通用）

每份 dispatch prompt 必含以下四個 Block：

### Block 1 — Identity Block

```
You are the {AgentName} agent.

Bootstrap files (read in this order, absolute paths):
  /home/user/agentorg-demo-build/agents/football/{agent-name}/agent.yaml
  /home/user/agentorg-demo-build/agents/football/{agent-name}/soul.md
  /home/user/agentorg-demo-build/agents/football/{agent-name}/org.md
  /home/user/agentorg-demo-build/agents/football/{agent-name}/tools.md

Bootstrap once, then start workflow.
```

### Block 2 — Worklog Block

```
WORKLOG: You must punch your own clock using scripts/worklog.sh.
  First action:  FILE=$(bash scripts/worklog.sh start football/{agent-name} sonnet "{summary}" manager "{trace_id}" "{parent_task_id}")
  Last action:   bash scripts/worklog.sh end "$FILE" completed "{output}"
  If you fail:   bash scripts/worklog.sh end "$FILE" failed "{error}"
```

### Block 3 — Memory Block

```
MEMORY: Before starting, read agents/football/{agent-name}/memory/MEMORY.md.
Before finishing, save new learnings to agents/football/{agent-name}/memory/ per agents/protocols/memory-protocol.md.
```

### Block 4 — Task Block（各 worker 有差異，見下方）

---

## round1（並行派遣：odds-analyst + form-analyst）

**派遣方式：**
- `run_in_background: true`（兩個 worker 同步執行）
- 使用相同的 Shared Context Block（下方 Match Context）

### Match Context（Shared Context Block，兩個 worker 均含）

```
MATCH CONTEXT:
  league:       {league}
  home_team:    {home_team}
  away_team:    {away_team}
  kickoff_time: {kickoff_time}
  task_id:      {task_id}
  trace_id:     {trace_id}
  output_path:  {output_path}
```

### odds-analyst Task Block

```
TASK:
  goal: 從 titan007.com（球探網）抓取並分析「{home_team} vs {away_team}」的賠率數據。
  分析範圍：歐賠（初盤/終盤）、亞盤（初/終）、大小球（初/終）、水位變化、異常訊號偵測、去水後隱含機率。

EXPECTED OUTPUT（JSON）:
{
  "market_summary": "整體盤口概述（100字以內）",
  "implied_prob": {"home": 0.XX, "draw": 0.XX, "away": 0.XX},
  "asian_handicap": {"line": "0 / -0.5 / ...", "direction": "支持主/客"},
  "over_under": {"line": "2.5/3", "direction": "大/小"},
  "anomalies": ["異常訊號列表，例：水位驟降、賠率單向移動"],
  "signal_strength": "strong | moderate | weak | no_signal",
  "output_file": "{output_path}/01_odds_analysis.md"
}

如 titan007 抓取失敗，output 欄位設為 null，並在 anomalies 填入 "DATA_FETCH_FAILED"。
```

### form-analyst Task Block

```
TASK:
  goal: 分析「{home_team}（主場）vs {away_team}（客場）」的球隊近況。
  分析範圍：近 5–10 場戰績（主客場拆分）、H2H 近 5 場往績、傷停/停賽、動機/積分壓力、Poisson λ（進/失球期望）。

EXPECTED OUTPUT（JSON）:
{
  "home_form": {"recent_record": "W3D1L1", "home_record": "W2D1L0", "avg_goals_scored": X.X, "avg_goals_conceded": X.X},
  "away_form": {"recent_record": "...", "away_record": "...", "avg_goals_scored": X.X, "avg_goals_conceded": X.X},
  "h2h_summary": "近 5 場 H2H 摘要（50字以內）",
  "injuries": {"home": ["傷停球員列表"], "away": ["傷停球員列表"]},
  "motivation": {"home": "保級/爭冠/平穩", "away": "保級/爭冠/平穩"},
  "poisson_lambda": {"home_goals": X.X, "away_goals": X.X},
  "form_signal": "home_favored | away_favored | neutral | uncertain",
  "output_file": "{output_path}/02_form_analysis.md"
}
```

---

## verify_round1（inline verification）

依 `agents/protocols/workflows/inline-verify-flow.md` 逐項驗證：

**odds-analyst 驗證：**
- [ ] `01_odds_analysis.md` 存在且 size > 0
- [ ] `implied_prob` 三值加總接近 1.0（允許 ±0.03 去水誤差）
- [ ] `signal_strength` 有明確值
- [ ] odds-analyst/worklog/ 有新 JSON（打卡確認）

**form-analyst 驗證：**
- [ ] `02_form_analysis.md` 存在且 size > 0
- [ ] `poisson_lambda` 兩值均 > 0
- [ ] `form_signal` 有明確值
- [ ] form-analyst/worklog/ 有新 JSON（打卡確認）

**驗證不通過：** 重派失敗的 worker（細化 prompt，補充資料缺口），重試一次。重試仍失敗則向用戶說明並交付已完成的部分。

---

## round2（串行派遣：value-modeler）

**前置條件：** verify_round1 通過。

### value-modeler Task Block

```
TASK:
  goal: 整合兩份分析報告，建立雙法勝率模型，計算全市場 EV，給出 0.25× Fractional Kelly 注碼建議。

INPUT（必須附上全文）:
  odds_analysis: {01_odds_analysis.md 全文}
  form_analysis: {02_form_analysis.md 全文}

EXPECTED OUTPUT（JSON）:
{
  "win_prob_model": {
    "weighted_score_method": {"home": 0.XX, "draw": 0.XX, "away": 0.XX},
    "poisson_method": {"home": 0.XX, "draw": 0.XX, "away": 0.XX},
    "blended": {"home": 0.XX, "draw": 0.XX, "away": 0.XX}
  },
  "ev_table": [
    {"market": "主勝", "implied_prob": 0.XX, "model_prob": 0.XX, "ev": "+X.X%", "recommended": true/false},
    {"market": "平局", ...},
    {"market": "客勝", ...},
    {"market": "大球2.5", ...},
    {"market": "小球2.5", ...}
  ],
  "top_recommendation": {
    "market": "主勝 | 平局 | 客勝 | 大球 | 小球 | 無推薦",
    "ev": "+X.X% | N/A",
    "kelly_fraction": "X.X% of bankroll | N/A",
    "confidence": "high | medium | low | no_bet"
  },
  "no_bet_reason": "（若 top_recommendation.market == 無推薦，說明原因）",
  "track_record_reminder": "請在賽後回填最終賽果至 value-modeler/memory/ 的 track-record 表",
  "output_file": "{output_path}/03_value_model.md"
}
```

**dispatch 參數：**
```
Agent({
  description: "value-modeler：EV/Kelly 建模",
  subagent_type: "general-purpose",
  model: "sonnet",
  run_in_background: false
})
```
