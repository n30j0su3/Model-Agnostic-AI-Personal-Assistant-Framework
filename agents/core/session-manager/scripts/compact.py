#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SESSION_PATH = ROOT / "sessions" / "SESSION.md"


def compact_session(max_completed=10):
    if not SESSION_PATH.exists():
        print(f"[ERROR] No se encontro {SESSION_PATH}")
        return False

    content = SESSION_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()

    new_lines = []
    in_completed_section = False
    completed_tasks = []

    # Simple state machine to parse sections
    for line in lines:
        if line.strip() == "### Completed Today":
            in_completed_section = True
            new_lines.append(line)
            continue

        if in_completed_section:
            if line.startswith("###") or line.startswith("##"):
                # End of completed section
                if len(completed_tasks) > max_completed:
                    summary_count = len(completed_tasks) - max_completed
                    new_lines.extend(completed_tasks[:max_completed])
                    new_lines.append(
                        f"- [x] ... y {summary_count} tareas mas completadas anteriormente."
                    )
                else:
                    new_lines.extend(completed_tasks)

                in_completed_section = False
                new_lines.append(line)
            elif line.strip().startswith("- [x]"):
                completed_tasks.append(line)
            else:
                if not line.strip() and not completed_tasks:
                    # Skip empty lines before first task
                    pass
                else:
                    new_lines.append(line)
            continue

        new_lines.append(line)

    # If we reached end of file while in completed section
    if in_completed_section:
        if len(completed_tasks) > max_completed:
            summary_count = len(completed_tasks) - max_completed
            new_lines.extend(completed_tasks[:max_completed])
            new_lines.append(
                f"- [x] ... y {summary_count} tareas mas completadas anteriormente."
            )
        else:
            new_lines.extend(completed_tasks)

    SESSION_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Compactador de Contexto para SESSION.md"
    )
    parser.add_argument(
        "--max", type=int, default=10, help="Maximo de tareas completadas a mantener"
    )
    args = parser.parse_args()

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Compactando SESSION.md...")
    if compact_session(args.max):
        print("[OK] Compactacion completada.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
