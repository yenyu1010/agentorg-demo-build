# Odds Analyst — Fetch Odds Flow

## 目的

從 titan007.com 抓取指定賽事的歐賠與亞盤資料，並依 fallback 策略處理抓取失敗情況。

## 主要抓取流程

### 步驟 1：定位賽事 ID

若 `match_id` 已知（來自 memory 或 manager 提供）：
- 直接跳至步驟 2

若 `match_id` 未知：
- WebFetch `https://www.titan007.com` 主站賽程頁
- 在頁面中搜尋 `{home_team}` 或 `{away_team}` 關鍵詞
- 提取對應賽事的 `match_id`（通常為 6-8 位數字）

### 步驟 2：抓取歐賠資料

```
WebFetch: https://vip.titan007.com/changeDetail/europe/{match_id}.aspx
```

目標數據：
- 各公司初盤（1/X/2 賠率）
- 各公司即時盤（最新 1/X/2 賠率）
- 時間戳（每次賠率變動記錄）

目標公司（優先抓取）：
| 公司 | 代號 |
|------|------|
| Bet365 | bet365 |
| 威廉希爾 | WillHill |
| 易勝博 | Unibet |
| 澳門彩票 | Macau |
| 皇冠 | Crown |
| 10Bet | 10Bet |
| Pinnacle | Pinnacle |

### 步驟 3：抓取亞盤資料

```
WebFetch: https://vip.titan007.com/changeDetail/asia/{match_id}.aspx
```

目標數據：
- 初盤盤口（Handicap）與水位（Odds）
- 即時盤口與水位
- 大小球盤口與水位

### 步驟 4：記錄成功 URL Pattern

首次成功抓取後，將以下內容寫入 `memory/titan007-data-map.md`：
```markdown
## {competition} 格式（{date} 確認）
- 歐賠：https://vip.titan007.com/changeDetail/europe/{match_id}.aspx
- 亞盤：https://vip.titan007.com/changeDetail/asia/{match_id}.aspx
- match_id 位置：主站賽程頁 → 賽事行連結的數字段
```

## Fallback 策略

| 順序 | 觸發條件 | 行動 |
|------|---------|------|
| 1 | WebFetch 被擋（403/404/空頁面） | 改用 WebSearch |
| 2 | WebSearch 結果無有效賠率數據 | 回報 manager，請用戶貼上賠率數據 |
| 3 | 任何情況 | **絕不編造數字** |

### Fallback 1：WebSearch

```
搜尋詞：球探網 {home_team} vs {away_team} 賠率
備用詞：titan007 {home_team} {away_team} odds
```

提取搜尋結果中的賠率數字，標注「來源：搜尋結果（可信度較低，請核實）」

### Fallback 2：請用戶提供

回報格式：
```
⚠️ 無法自動抓取賠率數據
賽事：{MATCH_SUMMARY}
嘗試路徑：
  - WebFetch titan007 歐賠頁：{URL}（失敗原因：{reason}）
  - WebSearch：無有效結果

請用戶直接貼上以下格式的賠率數據，分析師將據此進行計算：
| 公司 | 主勝 | 和局 | 客勝 |
|------|------|------|------|
| （請填入） | | | |
```

## 輸出

- `RAW_EUROPE_ODDS`：各公司歐賠原始數據（JSON 結構）
- `RAW_ASIA_ODDS`：亞盤盤口/水位數據（JSON 結構）
- `FETCH_METHOD`：資料來源方式（`titan007_direct` / `websearch` / `user_provided`）
- `FETCH_TIMESTAMP`：資料抓取時間（ISO 8601）
