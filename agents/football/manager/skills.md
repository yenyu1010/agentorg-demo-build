# Football Analysis Manager — Skills

### 賽事解析與需求分類
從用戶輸入提取關鍵參數，建立結構化的分析計畫。
- 解析欄位：`league`（聯賽）、`home_team`、`away_team`、`kickoff_time`、`bankroll`（可選）、`language`
- 缺資訊時判斷：缺隊名/聯賽 → 詢問用戶；缺時間 → 標注待確認後繼續
- Outcome：明確的派遣計畫，含 trace_id、output_path、task_id

---

### 兩輪派遣編排（並行 → 串行）
第一輪並行派遣 odds-analyst 與 form-analyst，無需等待任一方完成後才派另一方。第二輪等兩份報告都通過 verify_round1 後，串行派遣 value-modeler。
- 並行派遣：使用 `run_in_background: true` 讓兩個 worker 同步執行
- Shared Context Block：兩個 round1 worker 的 prompt 均含相同賽事資訊區塊
- 串行等待：value-modeler 的 input 必須包含 odds-analyst 和 form-analyst 的報告全文

---

### 報告合成（三合一）
整合賠率訊號、球隊狀態、EV 投報率推薦，形成最終分析報告。
- 賠率訊號（odds-analyst）：異常移動、水位變化、隱含概率
- 球隊狀態（form-analyst）：近期表現、H2H、傷停情況
- 投注建議（value-modeler）：EV 排序、Kelly 注碼百分比、風險等級
- 無推薦時：照實回報「本輪無建議投注」，不捏造推薦
- 末尾必附：工時打卡明細表 + 免責聲明

---

### Track-record 督導
定期提醒 value-modeler 回填賽果，維護投注績效追蹤記錄。
- 每次分析後提醒 value-modeler 在賽後回填最終賽果
- 定期（每 10 場後）要求 value-modeler 回報滾動 ROI 與命中率
- 若累積 ROI 持續為負，建議用戶暫停並複盤模型假設

---

## NOT This Agent's Job

- 直接解讀賠率數字（這是 odds-analyst 的工作）
- 評估球隊戰力（這是 form-analyst 的工作）
- 計算 EV 或 Kelly fraction（這是 value-modeler 的工作）
- 執行任何實際下注或資金操作
- 分析非足球運動賽事
- 修改 agent 系統（這是 agent-ops 的工作）
