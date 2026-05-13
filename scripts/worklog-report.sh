#!/usr/bin/env bash
# scripts/worklog-report.sh — Agent worklog health report
#
# Usage:
#   bash scripts/worklog-report.sh
#
# Output: Markdown table to stdout showing per-agent and system-wide stats.
# Reads:  agents/worklogs/index.jsonl + individual worklog files (silent failures)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/_worklog_report.py" "$@"
