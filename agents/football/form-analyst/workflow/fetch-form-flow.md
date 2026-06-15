# Form Analyst — Fetch Form Flow

## 目標

從 titan007.com 和 WebSearch 抓取對陣兩隊的近期數據，建立原始資料層。

---

## 步驟

### 1. 讀取 titan007-data-map（若存在）

讀取 `memory/titan007-data-map.md`，確認是否有已知的可用 URL pattern。
若有，直接使用已知 pattern；若無，進入探索模式。

### 2. titan007 入口導航（探索模式）

```
入口：https://www.titan007.com
路徑：賽程頁 → 找目標賽事（日期篩選）→ 點擊賽事 → 進入分析頁
```

使用 `WebFetch` 抓取以下資料（每隊各一次）：
- 近期戰績頁（近 10 場）
- H2H 對賽往績頁（近 10 次）
- 聯賽積分排名頁

記錄成功的 URL pattern，準備寫入 memory。

### 3. 傷停情報抓取（WebSearch）

```
搜尋關鍵字範本：
  "{home_team} injury news {match_date}"
  "{away_team} injury suspension {match_date}"
  "{home_team} vs {away_team} team news"
```

使用 `WebSearch` 執行上述查詢，記錄每條傷停消息的來源網站與發布日期。
只採用比賽日前 72 小時內的資訊；超過 72 小時標注「資訊時效可能不足」。

### 4. Fallback 機制（按序執行）

| 條件 | 動作 |
|------|------|
| titan007 正常回應 | 繼續流程，記錄 URL pattern |
| titan007 無法訪問/找不到賽事 | 切換至 WebSearch 補充戰績（標注：「來源：WebSearch，非 titan007」） |
| WebSearch 資料不足以計算加權分 | 回報 manager：「資料缺口：{team} 近期戰績資料不足，請用戶提供」，暫停分析 |

**嚴禁**：在任何 fallback 情況下編造或推測戰績數字。

### 5. 資料結構化

將抓取的原始資料整理為以下結構，供 analyze-flow 使用：

```
raw_data:
  home_team:
    recent_matches: [{date, opponent, venue, score, result}×N]  # N=6-10
    home_matches:   [{date, opponent, score, result}×M]         # 主場場次
    h2h:            [{date, home_team_role, score, result}×K]   # K=5-10
    league_rank:    {position, points, played}
    injuries:       [{player, status, source, date}]
  away_team:
    recent_matches: [...]
    away_matches:   [...]
    h2h:            [...]  # 與上方 h2h 同一列表，客隊視角
    league_rank:    {position, points, played}
    injuries:       [...]
  data_sources:
    titan007_urls:  [...]
    websearch_hits: [{query, source_name, article_date}]
    fetch_timestamp: {ISO8601}
```
