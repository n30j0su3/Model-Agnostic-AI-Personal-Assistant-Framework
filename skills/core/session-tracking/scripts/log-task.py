#!/usr/bin/env python3
import sys
import os
from pathlib import Path

SESSION_FILE = Path("sessions/SESSION.md")

def log_task(description, status="pending"):
    if not SESSION_FILE.exists():
        print("Error: SESSION.md no encontrado.")
        return

    content = SESSION_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    # Mapeo de iconos
    icons = {"pending": "[ ]", "progress": "[~]", "completed": "[x]"}
    icon = icons.get(status, "[ ]")
    new_task = f"- {icon} {description}"

    # Encontrar la sección de Tasks
    try:
        task_index = lines.index("## Tasks")
        # Insertar después de la subsección correspondiente o simplemente al inicio de Tasks
        lines.insert(task_index + 2, new_task)
        
        SESSION_FILE.write_text("\n".join(lines), encoding='utf-8')
        print(f"✓ Tarea registrada: {description} ({status})")
    except ValueError:
        print("Error: No se encontró la sección ## Tasks en SESSION.md")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python log-task.py \"descripción\" [status]")
    else:
        desc = sys.argv[1]
        stat = sys.argv[2] if len(sys.argv) > 2 else "pending"
        log_task(desc, stat)
