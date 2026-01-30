#!/usr/bin/env python3
"""
ETL de Estadísticas del Framework.
Analiza sesiones y logs para generar un resumen JSON consumible por el dashboard.html.
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime

# Configuración
REPO_ROOT = Path(__file__).resolve().parents[1]
SESSIONS_DIR = REPO_ROOT / "sessions"
DOCS_DIR = REPO_ROOT / "docs"
STATS_FILE = DOCS_DIR / "stats.json"

def scan_sessions():
    """Escanea archivos markdown en sessions/ buscando patrones de uso."""
    stats = {
        "total_sessions": 0,
        "total_tokens_estimated": 0,
        "last_activity": None,
        "sessions_by_date": {},
        "tools_usage": {
            "opencode": 0,
            "gemini": 0,
            "claude": 0
        }
    }

    # Patrones simples (regex) para extraer info de los logs si existen
    # Asumimos formato libre o estructurado
    
    for session_file in SESSIONS_DIR.glob("**/*.md"):
        if session_file.name == "SESSION.md" or "template" in str(session_file):
            continue
            
        stats["total_sessions"] += 1
        content = session_file.read_text(encoding="utf-8", errors="ignore")
        
        # Estimación muy burda de tokens (4 chars = 1 token)
        tokens = len(content) // 4
        stats["total_tokens_estimated"] += tokens
        
        # Detectar herramientas
        if "opencode" in content.lower(): stats["tools_usage"]["opencode"] += 1
        if "gemini" in content.lower(): stats["tools_usage"]["gemini"] += 1
        if "claude" in content.lower(): stats["tools_usage"]["claude"] += 1
        
        # Fecha mod
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        date_str = mtime.strftime("%Y-%m-%d")
        stats["sessions_by_date"][date_str] = stats["sessions_by_date"].get(date_str, 0) + 1
        
        if stats["last_activity"] is None or mtime > datetime.fromisoformat(stats["last_activity"]):
            stats["last_activity"] = mtime.isoformat()

    return stats

def main():
    print("[INFO] Iniciando ETL de estadísticas...")
    data = scan_sessions()
    
    # Enriquecer con datos del sistema
    data["generated_at"] = datetime.now().isoformat()
    data["framework_version"] = (REPO_ROOT / "VERSION").read_text().strip() if (REPO_ROOT / "VERSION").exists() else "unknown"
    
    # Escribir JSON
    STATS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[OK] Estadísticas generadas en: {STATS_FILE}")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
