# MCP Server Registry

## 1. 目的
集中列出所有可用的 MCP 伺服器及其用途，讓 Manager 在 dispatch 時能為 agent 選擇正確的工具。

## 2. 如何使用此 Registry
- Manager 在 dispatch 前查閱此表，決定 agent 是否需要額外 MCP 工具
- Agent Builder 在建立新 agent 的 tools.md 時參考此表
- 新增 MCP 伺服器時必須更新此 registry

## 3. 已註冊的 MCP 伺服器

| Server Name | 用途 | 提供的工具 | 適用 Agent | 狀態 |
|------------|------|-----------|-----------|------|
| claude_ai_Gmail | Gmail 信箱操作 | gmail_create_draft, gmail_get_profile, gmail_list_drafts, gmail_list_labels, gmail_read_message, gmail_read_thread, gmail_search_messages | 需要處理電子郵件的 agent | 已啟用 |
| claude_ai_Google_Calendar | Google 日曆管理 | gcal_create_event, gcal_delete_event, gcal_find_meeting_times, gcal_find_my_free_time, gcal_get_event, gcal_list_calendars, gcal_list_events, gcal_respond_to_event, gcal_update_event | 需要排程或會議管理的 agent | 已啟用 |

> 備註：以上 MCP 伺服器來自 `.claude/settings.local.json` 中的 permissions allow 清單（工具名稱前綴為 `mcp__`）。

## 4. 如何新增 MCP 伺服器
1. 在 `.claude/settings.json` 或 `.claude/settings.local.json` 中設定 MCP 伺服器
2. 更新此 registry（在 §3 表格中新增一列）
3. 更新相關 agent 的 tools.md（如果 agent 需要使用）
4. Governance 審查

## 5. MCP 與 tools.md 的關係
- tools.md 列出 agent 被授權使用的「系統能力」
- MCP 伺服器提供的工具是額外的擴展能力
- Agent 使用 MCP 工具前，其 tools.md 必須明確授權

## 6. 與現有協議的關係
- 引用 agent-anatomy.md §tools.md 規範
- 引用 definitions.md §Tool 定義
