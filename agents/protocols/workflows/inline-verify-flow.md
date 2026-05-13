# 逐次派遣驗證流程（Inline Dispatch Verification）

## 目的
每個 worker agent 完成後，Manager 立即驗證其產出是否與聲稱一致，通過才進入下一步。不再等所有 agent 跑完才批次驗證。

## 適用角色
Manager (L2)、Director (L3)、Officer (L4) — 任何使用 Agent tool 派遣的角色。

## 觸發時機
每次 Agent tool 呼叫返回結果後，立即執行。

## 驗證步驟

```
Agent 返回結果
  │
  ▼
[1] 解析聲稱（Parse Claims）
  從 agent 回報中提取所有具體聲稱：
  - "已建立 {file_path}" → 記錄為 file_created
  - "已修改 {file_path}" → 記錄為 file_modified
  - "已刪除 {file_path}" → 記錄為 file_deleted
  - "已更新 {section} 在 {file}" → 記錄為 content_updated
  - "搜尋結果為 {result}" → 記錄為 search_result
  │
  ▼
[2] 逐項驗證（Verify Each Claim）
  對每個聲稱執行對應檢查：

  | 聲稱類型 | 驗證方式 |
  |---------|---------|
  | file_created | Glob 確認檔案存在 + Read 確認非空 |
  | file_modified | Read 確認關鍵修改內容確實存在 |
  | file_deleted | Glob 確認檔案不存在 |
  | content_updated | Grep 在指定檔案中搜尋關鍵內容 |
  | search_result | Grep 抽查 1-2 個結果確認正確 |
  │
  ▼
[3] 判定結果

  全部通過 → PASS，繼續下一步驟
  部分失敗 → PARTIAL
    - 失敗項 < 30% → 記錄差異，繼續（附警告）
    - 失敗項 ≥ 30% → 重新派遣該 agent（一次機會）
  全部失敗 → FAIL
    - 重新派遣，精煉 prompt（一次機會）
    - 二次失敗 → 報告 gap 給用戶
  │
  ▼
[4] 記錄驗證結果
  在 dispatch 結果中附加驗證摘要：
  ```
  VERIFY: {agent_name}
  Claims: {n} | Verified: {n} | Failed: {n}
  Status: PASS | PARTIAL | FAIL
  Failed items: {list if any}
  ```
```

## Manager 整合方式

在 workflow.yaml 的 execute 步驟中，每次 dispatch 後加入 inline verify：

```yaml
- id: execute
  action: dispatch_rounds
  ref: workflow/execute-flow.md
  inline_verify: agents/protocols/workflows/inline-verify-flow.md  # ← 引用此流程
  note: "每次 agent 返回後立即驗證，通過才派下一個"
```

或者在 dispatch prompt 的最後提醒自己：

```
INLINE VERIFY: Agent 返回後，依 agents/protocols/workflows/inline-verify-flow.md
逐項驗證其聲稱。全部通過才繼續下一步。
```

## 與現有 verification-protocol.md 的關係
- inline-verify 是「每次 dispatch 後」的即時驗證
- verification-protocol.md 的 verify 步驟是「全部完成後」的最終審查
- 兩者互補，不互斥：inline verify 確保每步正確，final verify 確保整體一致
- 有 inline verify 後，final verify 可以更輕量（只做交叉檢查和整體一致性）

## 備註
- 驗證應使用 Glob、Grep、Read 等輕量工具，不派遣新 agent
- 驗證失敗的重新派遣只允許一次（防止無限迴圈）
- 並行派遣的多個 agent：等全部返回後逐一驗證
