# Agent SLO Definitions

## 1. 目的

為每個 agent 類型定義服務品質目標（SLO），讓 Evolution 和 Governance 有量化基準進行監控和改善。

## 2. SLO 指標定義

### 2.1 成功率 (Success Rate)
計算：completed / (completed + failed) × 100%
數據源：agents/worklogs/index.jsonl

### 2.2 平均耗時 (Avg Duration)
計算：avg(duration_seconds) for completed tasks
數據源：agents/worklogs/index.jsonl

### 2.3 靜默失敗 (Silent Failures)
計算：started 但超過 10 分鐘無 end 的任務
數據源：各 agent worklog/ 目錄中 status="started" 的檔案

## 3. SLO 目標值

### Manager 類
| 指標 | 目標 | 警戒值 |
|------|------|--------|
| 成功率 | ≥ 95% | < 90% |
| 平均耗時 | ≤ 300s | > 450s |
| 靜默失敗 | 0 | > 0 |

### Worker 類 (opus)
| 指標 | 目標 | 警戒值 |
|------|------|--------|
| 成功率 | ≥ 90% | < 85% |
| 平均耗時 | ≤ 120s | > 180s |
| 靜默失敗 | 0 | > 0 |

### Worker 類 (sonnet)
| 指標 | 目標 | 警戒值 |
|------|------|--------|
| 成功率 | ≥ 90% | < 85% |
| 平均耗時 | ≤ 90s | > 150s |
| 靜默失敗 | 0 | > 0 |

<!-- 2026-04-27: Worker 類 (haiku) SLO 區塊已移除（user policy: ban haiku，全系統不再使用 haiku 層級）。原 SLO 標準已併入 Worker 類 (sonnet)。詳見 agents/protocols/rules/no-haiku-policy.md。 -->

## 4. 監控流程

- `scripts/worklog-report.sh` 產出健康報告
- Evolution agent 在 team-review 時對照 SLO 目標
- 連續 2 週低於警戒值 → 觸發 Evolution 分析

## 5. 與現有協議的關係

- 引用 worklog-protocol.md（數據源）
- 引用 team-review-protocol.md（監控觸發）
- 引用 self-growth.md（agent 自我改善觸發）
