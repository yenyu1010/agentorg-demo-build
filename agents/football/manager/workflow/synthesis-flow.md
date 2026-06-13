# Football Manager — Synthesis Flow

## 流程總覽

```
synthesize → deliver
```

---

## synthesize（Manager 直接執行）

整合三份報告，形成最終足球分析報告。

### 合成結構

```
# 足球賽事分析報告

## 賽事資訊
- 聯賽：{league}
- 對陣：{home_team} vs {away_team}
- 開賽：{kickoff_time}
- 分析時間：{analysis_timestamp}
- trace_id：{trace_id}

## 1. 賠率訊號摘要（odds-analyst）
- 隱含勝率（去水後）：主 {X.X%} / 平 {X.X%} / 客 {X.X%}
- 亞盤：{line}，走向支持{主/客}
- 大小球：{line}，走向{大/小}
- 異常訊號：{anomalies}
- 訊號強度：{signal_strength}

## 2. 球隊狀態摘要（form-analyst）
- 主隊近況：{home_form.recent_record}，主場 {home_form.home_record}
- 客隊近況：{away_form.recent_record}，客場 {away_form.away_record}
- H2H：{h2h_summary}
- 傷停：主隊 {injuries.home} / 客隊 {injuries.away}
- 動機：主隊 {motivation.home} / 客隊 {motivation.away}
- 狀態訊號：{form_signal}

## 3. 價值投注建議（value-modeler）
### 模型勝率估計
| 方法 | 主勝 | 平局 | 客勝 |
|------|------|------|------|
| 加權評分法 | {X.X%} | {X.X%} | {X.X%} |
| Poisson 法 | {X.X%} | {X.X%} | {X.X%} |
| 混合 | {X.X%} | {X.X%} | {X.X%} |

### EV 計算結果
{ev_table 完整展示}

### 最優推薦
{若有推薦：}
- 投注方向：{market}
- 期望值（EV）：{ev}
- 建議注碼：{kelly_fraction}（0.25× Kelly）
- 信心度：{confidence}

{若無推薦（誠實回報）：}
- **本輪無建議投注**
- 原因：{no_bet_reason}

<!-- user-approved 2026-06-13 -->
## 4. 勝率參考榜（命中率軸）

> ⚠️ **勝率高≠會賺：EV 為負的高勝率單長期必虧。此榜供「低波動偏好」自行斟酌，正式推薦仍以 EV 軸為準。**

{從 value-modeler 的「高勝率參考榜」原樣轉載，保留分層標示（★ / ◐ / ✗）}

**Manager 合成規範**：
- ◐（可考慮）與 ✗（不建議）級的高勝率單**不得**在綜合評估或摘要中被包裝為「推薦」或「強力建議」
- 若用戶詢問某 ◐/✗ 單，Manager 應說明其分層含義及長期期望，不主動鼓勵投入

## 5. 綜合評估

{三合一合成評論，100字以內：賠率訊號與球隊狀態是否一致？EV 是否支持投注？}

---

### 賽後提醒
請在賽後將最終賽果回填至 value-modeler 的 track-record 記憶，以持續優化模型準確度。

---

## deliver（Manager 直接執行）

最終報告交付給用戶，末尾**必須**附上以下兩項：

### 工時打卡明細表

| Agent | 任務 | 開始時間 | 結束時間 | 狀態 |
|-------|------|---------|---------|------|
| football/manager | 分析協調 | {start} | {end} | completed |
| football/odds-analyst | 賠率分析 | {start} | {end} | completed/failed |
| football/form-analyst | 球隊狀態分析 | {start} | {end} | completed/failed |
| football/value-modeler | EV/Kelly 建模 | {start} | {end} | completed/failed |

（工時數據來源：Grep worklog/ 目錄下各 JSON 的 start_time / end_time 欄位）

### 免責聲明（固定文字，不得省略、不得修改）

> **本分析為機率模型推估，僅供參考，不構成投注建議；博彩具風險，過往績效不代表未來表現；請遵守所在地法律並量力而為。**
