#!/usr/bin/env python3
"""History engine to build local telemetry stats."""

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SESSIONS_DIR = REPO_ROOT / "sessions"
LOGS_DIR = REPO_ROOT / "logs"
PROMPTS_LOG = LOGS_DIR / "prompts.jsonl"
DOCS_DIR = REPO_ROOT / "docs"
DEFAULT_OUTPUT = DOCS_DIR / "stats.json"


def _estimate_tokens(text):
    if not text:
        return 0
    return int(math.ceil(len(text) / 4))


def _parse_iso(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _safe_read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def scan_sessions(sessions_dir):
    stats = {
        "total_sessions": 0,
        "total_tokens_estimated": 0,
        "last_activity": None,
        "sessions_by_date": {},
        "tools_usage": {"opencode": 0, "gemini": 0, "claude": 0},
    }

    for session_file in sessions_dir.glob("**/*.md"):
        if session_file.name == "SESSION.md":
            continue
        if "template" in str(session_file).lower():
            continue

        stats["total_sessions"] += 1
        content = _safe_read_text(session_file)
        stats["total_tokens_estimated"] += _estimate_tokens(content)

        lowered = content.lower()
        if "opencode" in lowered:
            stats["tools_usage"]["opencode"] += 1
        if "gemini" in lowered:
            stats["tools_usage"]["gemini"] += 1
        if "claude" in lowered:
            stats["tools_usage"]["claude"] += 1

        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        date_str = mtime.strftime("%Y-%m-%d")
        stats["sessions_by_date"][date_str] = (
            stats["sessions_by_date"].get(date_str, 0) + 1
        )

        if not stats["last_activity"] or mtime > datetime.fromisoformat(
            stats["last_activity"]
        ):
            stats["last_activity"] = mtime.isoformat()

    return stats


def scan_prompt_logs(log_path):
    summary = {
        "total_prompts": 0,
        "tokens_estimated": 0,
        "by_provider": {},
        "by_agent": {},
        "by_skill": {},
        "last_prompt": None,
    }

    if not log_path.exists():
        return summary

    for line in _safe_read_text(log_path).splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        summary["total_prompts"] += 1

        provider = str(entry.get("provider", "unknown")).strip() or "unknown"
        agent = str(entry.get("agent", "unknown")).strip() or "unknown"
        skill = str(entry.get("skill", ""))

        summary["by_provider"][provider] = summary["by_provider"].get(provider, 0) + 1
        summary["by_agent"][agent] = summary["by_agent"].get(agent, 0) + 1
        if skill:
            summary["by_skill"][skill] = summary["by_skill"].get(skill, 0) + 1

        token_est = entry.get("token_estimate")
        if token_est is None:
            token_est = _estimate_tokens(entry.get("prompt", ""))
        summary["tokens_estimated"] += int(token_est)

        ts = _parse_iso(entry.get("timestamp"))
        if ts and (
            not summary["last_prompt"] or ts > _parse_iso(summary["last_prompt"])
        ):
            summary["last_prompt"] = ts.isoformat()

    return summary


def build_history(sessions_dir, prompts_log):
    history = scan_sessions(sessions_dir)
    history["prompt_stats"] = scan_prompt_logs(prompts_log)
    history["generated_at"] = datetime.now().isoformat()
    version_file = REPO_ROOT / "VERSION"
    history["framework_version"] = (
        version_file.read_text(encoding="utf-8").strip()
        if version_file.exists()
        else "unknown"
    )
    return history


def write_output(data, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=True), encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description="Generate local history stats JSON")
    parser.add_argument(
        "--output", default=str(DEFAULT_OUTPUT), help="Output JSON path"
    )
    parser.add_argument(
        "--sessions-dir", default=str(SESSIONS_DIR), help="Sessions directory to scan"
    )
    parser.add_argument(
        "--prompts-log", default=str(PROMPTS_LOG), help="Prompt log JSONL path"
    )
    parser.add_argument("--stdout", action="store_true", help="Print JSON to stdout")
    args = parser.parse_args()

    data = build_history(Path(args.sessions_dir), Path(args.prompts_log))

    if args.stdout:
        print(json.dumps(data, indent=2, ensure_ascii=True))
        return

    output_path = Path(args.output)
    write_output(data, output_path)
    print(f"[OK] History stats saved to {output_path}")


if __name__ == "__main__":
    main()
