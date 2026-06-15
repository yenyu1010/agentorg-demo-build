#!/usr/bin/env bash
# Wait until no agent-builder worklog from this trace remains in "started" state.
TRACE="60505c39-47cf-47d7-acaf-00172a085309"
DIR="agents/agent-ops/agent-builder/worklog"
while true; do
  pending=$(grep -l "\"trace_id\": \"$TRACE\"" "$DIR"/*.json 2>/dev/null | xargs -r grep -l '"status": "started"' | wc -l)
  total=$(grep -l "\"trace_id\": \"$TRACE\"" "$DIR"/*.json 2>/dev/null | wc -l)
  if [ "$total" -ge 3 ] && [ "$pending" -eq 0 ]; then
    echo "BUILDERS_DONE: $total worklogs, 0 pending"
    exit 0
  fi
  sleep 5
done
