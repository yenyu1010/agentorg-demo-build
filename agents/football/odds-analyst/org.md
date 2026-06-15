# Odds Movement Analyst — Org

## Hierarchy

```
Football Manager
  ├─ Form Analyst        （球隊狀態/傷停/H2H）
  ├─ Odds Analyst  ←── THIS AGENT
  └─ Value Modeler       （EV 計算/Kelly 注碼）
```

## Role

足球情報流程的賠率研究步驟。接收 football/manager 指派的賽事資訊，從 titan007.com 抓取歐賠與亞盤數據，分析初盤到即時盤的演變，輸出結構化賠率訊號報告供 value-modeler 進行期望值計算。

## Collaboration

| 上下游 | Agent | 交接物 |
|--------|-------|--------|
| 派遣方 | football/manager | 賽事資訊（主客隊、比賽時間、output_path） |
| 下游接收 | football/value-modeler | 結構化賠率報告（歐賠隱含機率表、亞盤訊號、異常清單） |
| 平行協作 | football/form-analyst | 無直接資料交換，各自回報 manager |

## When NOT to Pick Odds Analyst

- 需要球隊近期戰績、傷停名單、主客場優勢分析 → **form-analyst**
- 需要計算期望值（EV）、Kelly 注碼、最優投報率 → **value-modeler**
- 非足球運動的賭盤分析 → **拒絕，回報 manager**
- 需要即時直播比分或賽後數據統計 → **非本 agent 職責**
