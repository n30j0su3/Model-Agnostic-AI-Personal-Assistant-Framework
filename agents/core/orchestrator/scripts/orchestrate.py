#!/usr/bin/env python3
import argparse
import ast
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from task_queue import TaskQueue


ROOT = Path(__file__).resolve().parents[4]
DECISION_ENGINE_SCRIPT = ROOT / "skills/core/decision-engine/scripts/route.py"
LOG_DIR = ROOT / "logs/orchestrator"
SESSION_PATH = ROOT / "sessions/SESSION.md"
BACKLOG_VIEW = ROOT / "docs/backlog.view.md"
CATALOG_PATH = ROOT / "agents/core/orchestrator/catalog.json"


def load_catalog():
    if not CATALOG_PATH.exists():
        return {}
    try:
        return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def get_agent_details(agent_name):
    catalog = load_catalog()
    agent_info = catalog.get(agent_name)
    if not agent_info:
        return {"error": f"Agent {agent_name} not found in catalog"}

    loc = agent_info.get("location")
    if not loc or loc == "N/D":
        return {"error": f"Location for {agent_name} unknown"}

    agent_dir = ROOT / loc
    agent_md = agent_dir / "AGENT.md"
    if not agent_md.exists():
        return {"error": f"AGENT.md not found at {agent_md}"}

    return {
        "metadata": agent_info,
        "full_instructions": agent_md.read_text(encoding="utf-8"),
    }


def read_text_limited(path, limit=2000):
    if not path.exists():
        return f"[missing] {path}"
    data = path.read_text(encoding="utf-8")
    if len(data) > limit:
        return data[:limit] + "\n...[truncated]"
    return data


def split_tasks(text):
    parts = re.split(
        r"\s*(?:;|\n|\band\b|\by\b|\bthen\b|\bluego\b)\s*", text, flags=re.IGNORECASE
    )
    tasks = [part.strip() for part in parts if part.strip()]
    return tasks or [text.strip()]


def run_decision_engine(text, threshold):
    if not DECISION_ENGINE_SCRIPT.exists():
        return {"type": "REMOTE_LLM", "reason": "decision-engine missing"}
    cmd = [
        sys.executable,
        str(DECISION_ENGINE_SCRIPT),
        text,
        "--threshold",
        str(threshold),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return {
            "type": "REMOTE_LLM",
            "reason": (result.stderr or "decision-engine error").strip(),
        }
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"type": "REMOTE_LLM", "reason": "decision-engine output invalid"}


def safe_eval(expr):
    node = ast.parse(expr, mode="eval")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp):
            left = _eval(n.left)
            right = _eval(n.right)
            if isinstance(n.op, ast.Add):
                return left + right
            if isinstance(n.op, ast.Sub):
                return left - right
            if isinstance(n.op, ast.Mult):
                return left * right
            if isinstance(n.op, ast.Div):
                return left / right
            if isinstance(n.op, ast.FloorDiv):
                return left // right
            if isinstance(n.op, ast.Mod):
                return left % right
            if isinstance(n.op, ast.Pow):
                return left**right
        if isinstance(n, ast.UnaryOp):
            operand = _eval(n.operand)
            if isinstance(n.op, ast.UAdd):
                return +operand
            if isinstance(n.op, ast.USub):
                return -operand
        raise ValueError("Unsupported expression")

    return _eval(node)


def run_script(script_path):
    if not script_path.exists():
        return {"error": f"Missing script: {script_path}"}
    cmd = [sys.executable, str(script_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    payload = {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
    if result.returncode != 0:
        payload["error"] = payload.get("stderr") or "Script failed"
    return payload


def extract_math_expression(text):
    match = re.search(r":\s*(.+)$", text)
    if match:
        return match.group(1).strip()
    return None


def execute_local_action(action, task_text):
    if action == "local:system_time":
        return {"output": datetime.now().isoformat()}
    if action == "local:list_files":
        items = sorted([p.name for p in ROOT.iterdir()])
        return {"output": items}
    if action == "local:show_backlog":
        return {"output": read_text_limited(BACKLOG_VIEW)}
    if action == "local:show_session":
        return {"output": read_text_limited(SESSION_PATH)}
    if action == "local:sync_context":
        return run_script(ROOT / "scripts/sync-context.py")
    if action == "local:update_framework":
        return run_script(ROOT / "scripts/update.py")
    if action == "local:get_agent_details":
        # Extract agent name from task text or description
        match = re.search(r"@([a-zA-Z0-9\-]+)", task_text)
        if match:
            return get_agent_details(f"@{match.group(1)}")
        return {"error": "No agent mention found (@agent-name)"}
    if action == "local:math_eval":
        expr = extract_math_expression(task_text)
        if not expr:
            return {"error": "No expression found"}
        try:
            value = safe_eval(expr)
            return {"output": value}
        except Exception as exc:
            return {"error": f"Math error: {exc}"}
    return {"error": f"Unknown local action: {action}"}


def build_summary(tasks):
    completed = [t for t in tasks if t.get("status") == "done"]
    failed = [t for t in tasks if t.get("status") == "failed"]
    delegated = [t for t in tasks if t.get("route") == "DELEGATE"]
    remote = [t for t in tasks if t.get("route") == "REMOTE_LLM"]

    parts = []
    if completed:
        parts.append(f"Completado local: {len(completed)}")
    if delegated:
        parts.append(f"Delegado: {len(delegated)}")
    if remote:
        parts.append(f"Requiere LLM remoto: {len(remote)}")
    if failed:
        parts.append(f"Fallido: {len(failed)}")
    if not parts:
        parts.append("Sin acciones ejecutadas")

    next_steps = []
    agents = sorted({t.get("agent") for t in delegated if t.get("agent")})
    if agents:
        next_steps.append("Ejecutar agentes delegados: " + ", ".join(agents))
    if remote:
        next_steps.append("Resolver tareas que requieren LLM remoto")
    if failed:
        next_steps.append("Revisar errores y reintentar tareas fallidas")

    return " | ".join(parts), next_steps


def append_session_summary(summary):
    if not SESSION_PATH.exists():
        return
    lines = SESSION_PATH.read_text(encoding="utf-8").splitlines()
    note_line = f"- {datetime.now().strftime('%Y-%m-%d %H:%M')} Orchestrator: {summary}"
    insert_at = None
    for idx, line in enumerate(lines):
        if line.strip() == "## Notes & Decisions":
            insert_at = idx + 1
            break
    if insert_at is None:
        lines.extend(["", "## Orchestrator Log", "", note_line])
    else:
        while insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1
        lines.insert(insert_at, note_line)
    SESSION_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_jsonl(payload):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

def log_thinking(task_id, step, reasoning, result="pending"):
    now = datetime.now()
    thinking_dir = ROOT / "sessions" / now.strftime("%Y") / now.strftime("%m")
    thinking_dir.mkdir(parents=True, exist_ok=True)
    log_path = thinking_dir / "thinking.jsonl"
    entry = {
        "timestamp": now.isoformat(),
        "task_id": task_id,
        "step": step,
        "reasoning": reasoning,
        "result": result
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Orchestrator CLI")
    parser.add_argument("input", nargs="?", help="Texto de entrada")
    parser.add_argument(
        "--threshold", type=int, default=2, help="Umbral decision-engine"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="No ejecuta acciones locales"
    )
    parser.add_argument(
        "--no-session-log", action="store_true", help="No escribe en SESSION.md"
    )
    parser.add_argument("--no-jsonl", action="store_true", help="No escribe JSONL")
    args = parser.parse_args()

    if args.input:
        text = args.input
    else:
        if sys.stdin.isatty():
            print("[ERROR] Debes proporcionar un texto de entrada.")
            return 1
        text = sys.stdin.read()

    start = time.time()
    task_texts = split_tasks(text)

    queue = TaskQueue()
    for idx, task_text in enumerate(task_texts, start=1):
        decision = run_decision_engine(task_text, args.threshold)
        queue.add(
            {
                "id": idx,
                "description": task_text,
                "route": decision.get("type"),
                "agent": decision.get("agent"),
                "action": decision.get("action"),
                "status": "pending",
            }
        )

    for task in queue.all():
        log_thinking(task["id"], f"Procesando: {task['description']}", f"Ruta decidida: {task['route']}")
        if task.get("route") == "LOCAL_EXECUTION":
            queue.set_status(task["id"], "running")
            if args.dry_run:
                queue.set_status(task["id"], "done", result={"output": "dry-run"})
                log_thinking(task["id"], "Ejecución Local", "Modo dry-run activado", "dry-run")
                continue
            result = execute_local_action(task.get("action"), task.get("description"))
            if result.get("error"):
                queue.set_status(
                    task["id"], "failed", error=result.get("error"), result=result
                )
                log_thinking(task["id"], "Ejecución Local", f"Error: {result.get('error')}", "failed")
            else:
                queue.set_status(task["id"], "done", result=result)
                log_thinking(task["id"], "Ejecución Local", "Completado exitosamente", "done")
        elif task.get("route") == "DELEGATE":
             log_thinking(task["id"], "Delegación", f"Delegando al agente {task.get('agent')}", "delegated")
        elif task.get("route") == "REMOTE_LLM":
             log_thinking(task["id"], "LLM Remoto", "Requiere procesamiento por modelo externo", "pending_remote")

    summary, next_steps = build_summary(queue.all())
    payload = {
        "session_id": datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{os.getpid()}",
        "input": text.strip(),
        "tasks": queue.all(),
        "summary": summary,
        "next_steps": next_steps,
        "execution_time_ms": int((time.time() - start) * 1000),
        "timestamp": datetime.now().isoformat(),
    }

    if not args.no_jsonl:
        write_jsonl(payload)
    if not args.no_session_log:
        append_session_summary(summary)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
