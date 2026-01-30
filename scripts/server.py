#!/usr/bin/env python3
import http.server
import json
import os
import socketserver
import subprocess
import urllib.parse
from datetime import datetime
from pathlib import Path
import sys

# Config
PORT = 8085
REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
BACKLOG_PATH = DOCS_DIR / "backlog.md"
LOG_DIR = REPO_ROOT / "logs"
BACKLOG_LOG_PATH = LOG_DIR / "backlog-changes.jsonl"


def _normalize_cell(value):
    text = str(value).strip()
    text = text.replace("\r", " ").replace("\n", " ")
    text = text.replace("|", "/")
    return text


def _find_table_bounds(lines):
    header_idx = None
    for idx, line in enumerate(lines):
        lower = line.strip().lower()
        if lower.startswith("| id |") and "prioridad" in lower and "estado" in lower:
            header_idx = idx
            break
    if header_idx is None:
        return None
    end_idx = header_idx
    for idx in range(header_idx + 1, len(lines)):
        if lines[idx].strip().startswith("|"):
            end_idx = idx
            continue
        break
    return header_idx, end_idx


def _count_existing_rows(lines, header_idx, end_idx):
    table_lines = lines[header_idx : end_idx + 1]
    count = 0
    for line in table_lines:
        stripped = line.strip().lower()
        if not stripped.startswith("|"):
            continue
        if stripped.startswith("| id |"):
            continue
        if stripped.startswith("| ---"):
            continue
        count += 1
    return count


def _build_table_lines(items):
    header = "| ID | Item | Prioridad | Estado | Criterios de aceptacion |"
    separator = "| --- | --- | --- | --- | --- |"
    rows = []
    for item in items:
        row = "| {id} | {label} | {priority} | {status} | {desc} |".format(
            id=_normalize_cell(item["id"]),
            label=_normalize_cell(item["label"]),
            priority=_normalize_cell(item["priority"]),
            status=_normalize_cell(item["status"]),
            desc=_normalize_cell(item.get("desc") or item.get("criteria", "")),
        )
        rows.append(row)
    return [header, separator] + rows


def _validate_items(items):
    if not isinstance(items, list):
        raise ValueError("'items' debe ser una lista")
    if not items:
        raise ValueError("'items' no puede estar vacio")
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Item en index {idx} debe ser un objeto")
        missing = [
            key for key in ("id", "label", "priority", "status") if not item.get(key)
        ]
        if missing:
            raise ValueError(f"Item {idx} faltan campos: {', '.join(missing)}")


def _update_backlog_table(items, allow_shrink=False):
    if not BACKLOG_PATH.exists():
        raise RuntimeError("backlog.md no encontrado")
    content = BACKLOG_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()
    bounds = _find_table_bounds(lines)
    if not bounds:
        raise RuntimeError("No se encontro la tabla del backlog")
    header_idx, end_idx = bounds
    existing_count = _count_existing_rows(lines, header_idx, end_idx)
    if existing_count and len(items) < existing_count and not allow_shrink:
        raise ValueError(
            f"No se permite reducir el backlog de {existing_count} a {len(items)} sin allow_shrink"
        )
    new_table = _build_table_lines(items)
    new_lines = lines[:header_idx] + new_table + lines[end_idx + 1 :]
    new_content = "\n".join(new_lines)
    if content.endswith("\n"):
        new_content += "\n"
    BACKLOG_PATH.write_text(new_content, encoding="utf-8")
    return {"previous_count": existing_count, "new_count": len(items)}


def _log_backlog_change(payload):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with BACKLOG_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


class FrameworkRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS_DIR), **kwargs)

    def do_GET(self):
        # API Endpoints
        if self.path.startswith("/api/status"):
            self.send_json(self.get_system_status())
            return

        # Backlog Read
        if self.path.startswith("/api/backlog"):
            try:
                content = (DOCS_DIR / "backlog.md").read_text(encoding="utf-8")
                self.send_json({"content": content})
            except Exception as e:
                self.send_error(500, str(e))
            return

        # Serve static files from docs/
        if self.path == "/":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("content-length", "0"))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
        except:
            self.send_error(400, "Invalid JSON")
            return

        if self.path == "/api/backlog":
            items = data.get("items")
            allow_shrink = bool(data.get("allow_shrink", False))
            try:
                _validate_items(items)
                result = _update_backlog_table(items, allow_shrink=allow_shrink)
                _log_backlog_change(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "action": "update_backlog",
                        "client": self.client_address[0]
                        if self.client_address
                        else "unknown",
                        "user_agent": self.headers.get("User-Agent", ""),
                        "previous_count": result["previous_count"],
                        "new_count": result["new_count"],
                        "allow_shrink": allow_shrink,
                    }
                )
                self.send_json({"success": True, "count": len(items)})
            except ValueError as e:
                self.send_error(400, str(e))
            except Exception as e:
                self.send_error(500, f"Failed to save: {e}")
            return

        if self.path == "/api/sync":
            success = self.run_sync()
            self.send_json({"success": success})
            return

        self.send_error(404, "Endpoint not found")

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def get_system_status(self):
        has_git = (REPO_ROOT / ".git").exists()
        last_sync = "Unknown"
        version = "Unknown"
        try:
            opencode_md = REPO_ROOT / ".context" / "opencode.md"
            if opencode_md.exists():
                last_sync = datetime.fromtimestamp(
                    os.path.getmtime(opencode_md)
                ).isoformat()

            ver_file = REPO_ROOT / "VERSION"
            if ver_file.exists():
                version = ver_file.read_text().strip()
        except:
            pass

        return {
            "version": version,
            "stage": "ALPHA",
            "mode": "hybrid" if has_git else "local",
            "orchestration": "active",
            "last_sync": str(last_sync),
        }

    def run_sync(self):
        try:
            subprocess.run(
                [sys.executable, str(REPO_ROOT / "scripts" / "sync-context.py")]
            )
            return True
        except:
            return False


def main():
    print(f"Starting Dashboard Server at http://localhost:{PORT}")
    print(f"Serving directory: {DOCS_DIR}")
    try:
        # Allow address reuse
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", PORT), FrameworkRequestHandler) as httpd:
            print("Server running. Press Ctrl+C to stop.")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
            print("\nServer stopped.")
    except OSError as e:
        print(f"Error starting server: {e}")


if __name__ == "__main__":
    main()
