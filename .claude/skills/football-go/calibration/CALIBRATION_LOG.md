# Football Go — FG-Score 校準日誌 (Calibration Log)

> **這是 dev / 驗證用語料區，不是 production。** `football-go` 的正式 skill 是上層的
> `SKILL.md` + `scripts/water_level_analyzer.py`。本資料夾只負責「累積實戰場次 → 批次回測 →
> 等門檻穩了再決定要不要把 FG-Score 寫進 analyzer」。

## 決策紀錄 (2026-06-15, 由使用者拍板)

**先記下、累積多場一起跑;再驗幾場、門檻穩了才寫進 skill —— 不要現在就把過擬合的規則固化。**

- ❌ 暫不把 FG-Score 併入 `water_level_analyzer.py`。
- ✅ 持續蒐集「已標記結果」的場次,丟進 `matches/`,用 `fg_score.py` 批次跑。
- ✅ 待樣本夠(目標正反各 5+)、`2.0 分水嶺`門檻在新場次上仍站得住,再走 Agent Ops
  (Manager → Agent Builder 實作、順手修 §C bug → Governance 審) 正式寫入。
- ⚠️ 連帶待辦:production analyzer 的 §C「降盤前大球升水檢查」有 bug(錨定全場第一次大球降水,
  導致每個降盤都被連坐),整合 FG-Score 時一併修正。

## 如何加一場

1. 把該場做成 JSON(schema 同 `matches/*.json`:`pre_match{handicap,total_line,over_odds_open}`
   + `snapshots[{minute,score,line,over_odds,under_odds}]`),命名 `隊名_日期.json`,放進 `matches/`。
2. 跑批次回測:
   ```bash
   python3 .claude/skills/football-go/calibration/fg_score.py \
     .claude/skills/football-go/calibration/matches/*.json
   ```
3. 把結果與「實際 HT 是否進球」對照,更新下方記分板。

## FG-Score v0.2 公式摘要

**選場 Gate(不過→SKIP)**:`|讓球| ≥ 0.5` 且 `開盤大小球 ≥ 2.5`
**計分(0~100)**:C1 開盤線強度(20) + C2 降盤動能(30) + C3 大球升水到頂循環(25)
+ C4 小球升水波(15) + C5 參考規則 223/334/757(10)
**v0.2 關鍵修正 — 2.0 分水嶺停損 P**:破蛋前(仍 0-0)盤口最低線
`≥2.0 → 0` / `1.75 → -25` / `≤1.5 → -45`
**門檻**:`≥70 STRONG GO` / `50-69 GO` / `30-49 WAIT/ABORT` / `<30 或選場不過 SKIP`

## 核心假設(待證偽)

降盤+大球升水是**必要非充分**;真正分水嶺是**盤口 2.0**:
- 卡在 2.0、大球升頂 → 進場(追上半大/破蛋盤入手)
- 跌破 2.0 仍 0-0 → 停損/放棄(市場已把首半球定價出去)

**最該優先蒐集的「打臉場」**:
1. 盤口卡 2.0、大球升頂、上半場卻 0-0 → 若有,2.0 規則破。
2. 盤口跌破 2.0、上半場卻照進 → 若有,停損閥太兇、會錯殺。

## 記分板 (Scoreboard)

| # | 賽事 | 日期 | 開盤線 | 破蛋前最低線 | v0.1 | v0.2 | v0.2 判讀 | 實際 HT | 對錯 |
|---|------|------|:---:|:---:|:---:|:---:|---|---|:---:|
| 1 | 诺梅卡柳 vs 派德 | 06-14 | 2.75 | 2.0 | 82 | 82 | 🟢 STRONG GO | 35′ 1-0(有球) | ✓ |
| 2 | 海于格松 vs 兰黑姆 | 06-14 | 3.5 | 3.5 | 51 | 51 | 🟡 GO | 6-12′ 2-1(有球) | ✓ |
| 3 | 阿斯塔纳 vs 伊特什 | 06-14 | 2.75 | 2.0 | 60 | 60 | 🟡 GO | 38/43′ 2-0(有球) | ✓ |
| 4 | 桑德尼斯 vs 斯托曼 | 06-14 | 3.0 | 1.5 | 85 | 40 | ⚪ WAIT/ABORT | 0-0(失敗) | ✓(避開) |

**目前**:4 場(3 正 1 反),v0.2 全中。但這是「4 個點畫一條線」,屬過擬合,**尚未證明 edge**。
**下一步**:累積到正反各 5+ 場、特別是上面兩種打臉場,再評估固化。
