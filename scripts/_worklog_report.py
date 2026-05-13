#!/usr/bin/env python3
"""
Worklog Report Generator — called by worklog-report.sh.

Reads agents/worklogs/index.jsonl and individual worklog files to produce
a Markdown health report for all agents.

Silent failure detection:
  - A task is a silent failure if its individual worklog file has status="started"
    AND it started more than 10 minutes ago (no end recorded).
"""
import sys
import json
import os
import glob
from datetime import datetime, timezone
from collections import defaultdict


SILENT_FAILURE_THRESHOLD_SECONDS = 600  # 10 minutes


def now_utc():
    return datetime.now(timezone.utc)


def parse_iso(s):
    if s is None:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def fmt_seconds(s):
    if s is None:
        return "N/A"
    return f"{int(s)}s"


def find_repo_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def load_index(repo_root):
    index_path = os.path.join(repo_root, "agents", "worklogs", "index.jsonl")
    entries = []
    if not os.path.isfile(index_path):
        return entries
    with open(index_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def find_silent_failures(repo_root):
    """
    Scan all individual worklog files for tasks with status="started"
    that began more than SILENT_FAILURE_THRESHOLD_SECONDS ago.
    Returns a dict: agent -> count of silent failures
    """
    silent = defaultdict(int)
    now = now_utc()

    pattern = os.path.join(repo_root, "agents", "**", "worklog", "*.json")
    worklog_files = glob.glob(pattern, recursive=True)

    for fpath in worklog_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        if data.get("status") != "started":
            continue

        started_at = parse_iso(data.get("started_at"))
        if started_at is None:
            continue

        elapsed = (now - started_at).total_seconds()
        if elapsed > SILENT_FAILURE_THRESHOLD_SECONDS:
            agent = data.get("agent", "unknown")
            silent[agent] += 1

    return silent


def compute_agent_stats(entries, silent_failures):
    """
    Aggregate per-agent statistics from index.jsonl entries.
    """
    agents = defaultdict(lambda: {
        "total": 0,
        "completed": 0,
        "failed": 0,
        "durations": [],
    })

    for entry in entries:
        agent = entry.get("agent", "unknown")
        status = entry.get("status", "unknown")
        duration = entry.get("duration_seconds")

        agents[agent]["total"] += 1

        if status == "completed":
            agents[agent]["completed"] += 1
            if duration is not None:
                agents[agent]["durations"].append(duration)
        elif status == "failed":
            agents[agent]["failed"] += 1

    result = {}
    for agent, stats in agents.items():
        total = stats["total"]
        completed = stats["completed"]
        failed = stats["failed"]
        durations = stats["durations"]

        denominator = completed + failed
        success_rate = (completed / denominator * 100) if denominator > 0 else None

        avg_duration = (sum(durations) / len(durations)) if durations else None
        max_duration = max(durations) if durations else None

        result[agent] = {
            "total": total,
            "completed": completed,
            "failed": failed,
            "success_rate": success_rate,
            "avg_duration": avg_duration,
            "max_duration": max_duration,
            "silent_failures": silent_failures.get(agent, 0),
        }

    return result


def render_report(agent_stats, generated_at):
    lines = []
    lines.append("# Agent Health Report")
    lines.append(f"Generated: {generated_at}")
    lines.append("")

    # ── Per-Agent Stats ───────────────────────────────────────────────────────
    lines.append("## Per-Agent Stats")
    lines.append("")
    header = "| Agent | Tasks | Completed | Failed | Silent Failures | Success% | Avg Duration | Max Duration |"
    separator = "|-------|-------|-----------|--------|-----------------|----------|-------------|-------------|"
    lines.append(header)
    lines.append(separator)

    sorted_agents = sorted(agent_stats.items(), key=lambda x: x[0])
    for agent, stats in sorted_agents:
        success_pct = f"{stats['success_rate']:.1f}%" if stats['success_rate'] is not None else "N/A"
        avg_dur = fmt_seconds(stats['avg_duration'])
        max_dur = fmt_seconds(stats['max_duration'])
        row = (
            f"| {agent} "
            f"| {stats['total']} "
            f"| {stats['completed']} "
            f"| {stats['failed']} "
            f"| {stats['silent_failures']} "
            f"| {success_pct} "
            f"| {avg_dur} "
            f"| {max_dur} |"
        )
        lines.append(row)

    lines.append("")

    # ── System Summary ────────────────────────────────────────────────────────
    lines.append("## System Summary")
    lines.append("")

    total_tasks = sum(s["total"] for s in agent_stats.values())
    total_completed = sum(s["completed"] for s in agent_stats.values())
    total_failed = sum(s["failed"] for s in agent_stats.values())
    total_silent = sum(s["silent_failures"] for s in agent_stats.values())

    denom = total_completed + total_failed
    overall_rate = (total_completed / denom * 100) if denom > 0 else 0.0

    # Busiest agent (most total tasks)
    busiest = max(agent_stats.items(), key=lambda x: x[1]["total"], default=(None, None))
    busiest_name = f"{busiest[0]} ({busiest[1]['total']} tasks)" if busiest[0] else "N/A"

    # Slowest agent (highest avg_duration among agents with data)
    agents_with_duration = [
        (a, s) for a, s in agent_stats.items() if s["avg_duration"] is not None
    ]
    if agents_with_duration:
        slowest = max(agents_with_duration, key=lambda x: x[1]["avg_duration"])
        slowest_name = f"{slowest[0]} ({fmt_seconds(slowest[1]['avg_duration'])})"
    else:
        slowest_name = "N/A"

    lines.append(f"- Total tasks: {total_tasks}")
    lines.append(f"- Overall success rate: {overall_rate:.1f}%")
    lines.append(f"- Total failed: {total_failed}")
    lines.append(f"- Total silent failures: {total_silent}")
    lines.append(f"- Busiest: {busiest_name}")
    lines.append(f"- Slowest avg: {slowest_name}")
    lines.append("")

    return "\n".join(lines)


def main():
    repo_root = find_repo_root()

    entries = load_index(repo_root)
    silent_failures = find_silent_failures(repo_root)
    agent_stats = compute_agent_stats(entries, silent_failures)

    generated_at = now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")
    report = render_report(agent_stats, generated_at)

    print(report)


if __name__ == "__main__":
    main()
