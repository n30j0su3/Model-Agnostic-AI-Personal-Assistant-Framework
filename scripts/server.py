#!/usr/bin/env python3
import http.server
import json
import os
import socketserver
import subprocess
import urllib.parse
from pathlib import Path

# Config
PORT = 8000
REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"

class FrameworkRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS_DIR), **kwargs)

    def do_GET(self):
        # API Endpoints
        if self.path.startswith("/api/status"):
            self.send_json(self.get_system_status())
            return
        
        # Serve static files from docs/
        # If path is root, serve index.html
        if self.path == "/":
            self.path = "/index.html"
            
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/sync":
            success = self.run_sync()
            self.send_json({"success": success})
            return
        
        if self.path == "/api/open-cli":
            # Start pa.py in a new window? Hard to do from browser to OS securely.
            # Maybe just return instruction.
            self.send_json({"success": False, "message": "Browser cannot launch CLI directly."})
            return

        self.send_error(404, "Endpoint not found")

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def get_system_status(self):
        # Basic checks
        has_git = (REPO_ROOT / ".git").exists()
        last_sync = "Unknown"
        # Try to find last sync time from logs or file stats
        try:
            opencode_md = REPO_ROOT / ".context" / "opencode.md"
            if opencode_md.exists():
                last_sync =  os.path.getmtime(opencode_md) # timestamp
        except:
            pass
            
        return {
            "version": "1.6.4-beta", # Should read VERSION file
            "stage": "BETA",
            "mode": "hybrid" if has_git else "local",
            "orchestration": "active",
            "last_sync": str(last_sync)
        }

    def run_sync(self):
        try:
            subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "sync-context.py")], check=True)
            return True
        except:
            return False

import sys

def main():
    print(f"Starting Dashboard Server at http://localhost:{PORT}")
    print(f"Serving directory: {DOCS_DIR}")
    try:
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
