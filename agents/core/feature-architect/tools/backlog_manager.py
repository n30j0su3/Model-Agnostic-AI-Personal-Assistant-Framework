#!/usr/bin/env python3
import argparse
import datetime
import json
import re
import sys
from pathlib import Path


def find_repo_root(start_path):
    start = Path(start_path).resolve()
    for candidate in [start] + list(start.parents):
        if (candidate / "docs" / "backlog.md").exists():
            return candidate
    return None


def load_lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def save_lines(path, lines):
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_table_header(lines):
    for idx, line in enumerate(lines):
        if line.strip().startswith("| ID |"):
            return idx
    return -1


def parse_row(line):
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    if len(parts) < 5:
        return None
    if len(parts) > 5:
        parts = parts[:4] + [" | ".join(parts[4:]).strip()]
    return {
        "id": parts[0],
        "item": parts[1],
        "priority": parts[2],
        "status": parts[3],
        "criteria": parts[4],
    }


def format_row(row):
    return f"| {row['id']} | {row['item']} | {row['priority']} | {row['status']} | {row['criteria']} |"


def parse_table(lines):
    header_idx = find_table_header(lines)
    if header_idx == -1:
        raise ValueError("Table header not found")
    data_start = header_idx + 2
    data_end = data_start
    rows = []
    while data_end < len(lines):
        line = lines[data_end]
        if not line.strip().startswith("|"):
            break
        row = parse_row(line)
        if row:
            rows.append(row)
        data_end += 1
    return header_idx, data_start, data_end, rows


def update_last_updated(lines, date_str):
    for idx, line in enumerate(lines):
        if line.startswith("Ultima actualizacion:"):
            lines[idx] = f"Ultima actualizacion: {date_str}"
            return


def add_history(lines, message):
    history_idx = -1
    for idx, line in enumerate(lines):
        if line.strip() == "## Historial de cambios":
            history_idx = idx
            break
    if history_idx == -1:
        raise ValueError("Historial section not found")

    table_idx = find_table_header(lines)
    if table_idx == -1:
        raise ValueError("Table header not found")

    last_entry_idx = None
    for idx in range(history_idx + 1, table_idx):
        if lines[idx].strip().startswith("- "):
            last_entry_idx = idx
    insert_at = (last_entry_idx + 1) if last_entry_idx is not None else (history_idx + 1)
    date_str = datetime.date.today().isoformat()
    lines.insert(insert_at, f"- {date_str}: {message}")

    table_idx = find_table_header(lines)
    if table_idx > 0 and lines[table_idx - 1].strip() != "":
        lines.insert(table_idx, "")


def next_id(rows):
    max_num = 0
    for row in rows:
        match = re.match(r"BL-(\d+)", row["id"])
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"BL-{max_num + 1:03d}"


def output(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=True, indent=2))
        return
    if isinstance(data, list):
        for row in data:
            print(f"{row['id']} | {row['priority']} | {row['status']} | {row['item']}")
        return
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
        return
    print(data)


def cmd_list(lines, args):
    _, _, _, rows = parse_table(lines)
    status_filter = args.status.lower() if args.status else None
    priority_filter = args.priority.lower() if args.priority else None
    filtered = []
    for row in rows:
        if status_filter and row["status"].lower() != status_filter:
            continue
        if priority_filter and row["priority"].lower() != priority_filter:
            continue
        filtered.append(row)
    output(filtered, args.json)


def cmd_get(lines, args):
    _, _, _, rows = parse_table(lines)
    for row in rows:
        if row["id"] == args.id:
            output(row, args.json)
            return
    print(f"ERROR: ID not found: {args.id}")
    sys.exit(1)


def cmd_next_id(lines, args):
    _, _, _, rows = parse_table(lines)
    output({"next_id": next_id(rows)}, args.json)


def cmd_add(lines, args, backlog_path):
    header_idx, data_start, data_end, rows = parse_table(lines)
    new_id = next_id(rows)
    row = {
        "id": new_id,
        "item": args.item,
        "priority": args.priority,
        "status": args.status,
        "criteria": args.criteria,
    }
    rows.append(row)
    new_lines = lines[:data_start] + [format_row(r) for r in rows] + lines[data_end:]
    update_last_updated(new_lines, datetime.date.today().isoformat())
    if args.history:
        add_history(new_lines, args.history)
    save_lines(backlog_path, new_lines)
    output({"ok": True, "id": new_id}, args.json)


def cmd_update(lines, args, backlog_path):
    header_idx, data_start, data_end, rows = parse_table(lines)
    updated = False
    for row in rows:
        if row["id"] != args.id:
            continue
        if args.status:
            row["status"] = args.status
        if args.item:
            row["item"] = args.item
        if args.priority:
            row["priority"] = args.priority
        if args.criteria:
            row["criteria"] = args.criteria
        updated = True
        break
    if not updated:
        print(f"ERROR: ID not found: {args.id}")
        sys.exit(1)
    new_lines = lines[:data_start] + [format_row(r) for r in rows] + lines[data_end:]
    update_last_updated(new_lines, datetime.date.today().isoformat())
    if args.history:
        add_history(new_lines, args.history)
    elif args.status:
        add_history(new_lines, f"Se actualizo {args.id} a estado {args.status}.")
    save_lines(backlog_path, new_lines)
    output({"ok": True, "id": args.id}, args.json)


def cmd_history(lines, args, backlog_path):
    add_history(lines, args.message)
    update_last_updated(lines, datetime.date.today().isoformat())
    save_lines(backlog_path, lines)
    output({"ok": True}, args.json)


def cmd_audit(lines, args):
    _, _, _, rows = parse_table(lines)
    issues = []
    seen = set()
    for row in rows:
        rid = row["id"]
        if rid in seen:
            issues.append(f"Duplicate ID: {rid}")
        seen.add(rid)
        if not re.match(r"BL-\d{3}$", rid):
            issues.append(f"Invalid ID format: {rid}")
        if not row["item"]:
            issues.append(f"Empty item for {rid}")
        if not row["priority"]:
            issues.append(f"Empty priority for {rid}")
        if not row["status"]:
            issues.append(f"Empty status for {rid}")
    output({"ok": len(issues) == 0, "issues": issues}, args.json)


def build_parser():
    parser = argparse.ArgumentParser(description="Backlog manager for docs/backlog.md")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    list_cmd = sub.add_parser("list", help="List backlog items")
    list_cmd.add_argument("--status", help="Filter by status")
    list_cmd.add_argument("--priority", help="Filter by priority")

    get_cmd = sub.add_parser("get", help="Get backlog item by ID")
    get_cmd.add_argument("id", help="Backlog ID")

    next_cmd = sub.add_parser("next-id", help="Get next backlog ID")

    add_cmd = sub.add_parser("add", help="Add backlog item")
    add_cmd.add_argument("--item", required=True, help="Item description")
    add_cmd.add_argument("--priority", required=True, help="Priority")
    add_cmd.add_argument("--criteria", required=True, help="Acceptance criteria")
    add_cmd.add_argument("--status", default="Pendiente", help="Status")
    add_cmd.add_argument("--history", help="History message")

    update_cmd = sub.add_parser("update", help="Update backlog item")
    update_cmd.add_argument("id", help="Backlog ID")
    update_cmd.add_argument("--status", help="Status")
    update_cmd.add_argument("--item", help="Item description")
    update_cmd.add_argument("--priority", help="Priority")
    update_cmd.add_argument("--criteria", help="Acceptance criteria")
    update_cmd.add_argument("--history", help="History message")

    history_cmd = sub.add_parser("history", help="Add history entry")
    history_cmd.add_argument("message", help="History message")

    audit_cmd = sub.add_parser("audit", help="Audit backlog integrity")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    repo_root = find_repo_root(__file__)
    if not repo_root:
        print("ERROR: repo root not found")
        sys.exit(1)
    backlog_path = repo_root / "docs" / "backlog.md"
    lines = load_lines(backlog_path)

    if args.command == "list":
        cmd_list(lines, args)
        return
    if args.command == "get":
        cmd_get(lines, args)
        return
    if args.command == "next-id":
        cmd_next_id(lines, args)
        return
    if args.command == "add":
        cmd_add(lines, args, backlog_path)
        return
    if args.command == "update":
        cmd_update(lines, args, backlog_path)
        return
    if args.command == "history":
        cmd_history(lines, args, backlog_path)
        return
    if args.command == "audit":
        cmd_audit(lines, args)
        return


if __name__ == "__main__":
    main()
