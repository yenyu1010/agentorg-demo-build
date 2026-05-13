#!/usr/bin/env bash
# scripts/worklog.sh — Agent worklog punch-clock
#
# Usage:
#   start: FILE=$(bash scripts/worklog.sh start <agent> <model> "<summary>" [<dispatched_by>] [<trace_id>] [<parent_task_id>])
#   end:   bash scripts/worklog.sh end "$FILE" <completed|failed> "<output_summary>"
#
# Examples:
#   # Top-level Manager (auto-generates trace_id):
#   FILE=$(bash scripts/worklog.sh start agent-ops/manager opus "refactor workflow.yaml" user)
#
#   # Worker dispatched by Manager (inherits trace_id and parent_task_id):
#   FILE=$(bash scripts/worklog.sh start agent-ops/governance sonnet "audit changes" manager "$TRACE_ID" "$PARENT_TASK_ID")
#
#   bash scripts/worklog.sh end "$FILE" completed "workflow.yaml simplified to 8 steps"
#
# Backward compatible: existing calls without trace_id/parent_task_id still work (default to empty string / null).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Pass all arguments (including --mirror-to if present) directly to the Python helper.
# The Python helper handles --mirror-to extraction itself, so no special treatment
# is needed here — full backward compatibility is preserved.
exec python3 "$SCRIPT_DIR/_worklog_helper.py" "$@"
