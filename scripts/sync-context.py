#!/usr/bin/env python3
"""
Context Sync Script
Sincroniza el contexto entre todas las terminales-AI (OpenCode, Claude, Gemini, Codex)
"""

import os
from pathlib import Path
from datetime import datetime

CONTEXT_DIR = Path(".context")
TOOLS = ["opencode", "claude", "gemini", "agents"]

def sync_context():
    master_path = CONTEXT_DIR / "MASTER.md"
    if not master_path.exists():
        print(f"Error: {master_path} no existe.")
        return

    master_content = master_path.read_text()
    
    # Marcadores para la sincronización
    start_marker = "<!-- MASTER-CONTEXT-START -->"
    end_marker = "<!-- MASTER-CONTEXT-END -->"
    
    sync_block = f"{start_marker}\n{master_content}\n{end_marker}"

    for tool in TOOLS:
        tool_file = CONTEXT_DIR / f"{tool}.md"
        if tool_file.exists():
            content = tool_file.read_text()
            
            if start_marker in content and end_marker in content:
                # Reemplazar bloque existente
                new_content = []
                keep = True
                for line in content.splitlines():
                    if start_marker in line:
                        new_content.append(sync_block)
                        keep = False
                    elif end_marker in line:
                        keep = True
                        continue
                    if keep:
                        new_content.append(line)
                tool_file.write_text("\n".join(new_content))
            else:
                # Apendizar al final si no existen los marcadores
                tool_file.write_text(f"{content}\n\n{sync_block}")
            
            print(f"✓ Contexto sincronizado para: {tool}")
        else:
            # Crear archivo básico si no existe
            tool_file.write_text(f"# {tool.capitalize()} Context\n\n{sync_block}")
            print(f"i Archivo creado y sincronizado: {tool}.md")

if __name__ == "__main__":
    sync_context()
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Sincronización completa.")
