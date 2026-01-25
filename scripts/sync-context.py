#!/usr/bin/env python3
import os
import logging
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configuración de logs corregida
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "context-sync.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a'),
        logging.StreamHandler()
    ]
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTEXT_DIR = REPO_ROOT / ".context"
TOOLS = ["opencode", "claude", "gemini", "agents"]
START_MARKER = "<!-- MASTER-CONTEXT-START -->"
END_MARKER = "<!-- MASTER-CONTEXT-END -->"


def run_context_snapshot():
    script_path = REPO_ROOT / "scripts" / "context-version.py"
    if not script_path.exists():
        logging.warning("context-version.py no encontrado. Se omite snapshot.")
        return False
    result = subprocess.run([sys.executable, str(script_path), "snapshot"], cwd=REPO_ROOT)
    if result.returncode != 0:
        logging.warning("Snapshot de contexto fallo.")
        return False
    logging.info("Snapshot de contexto creado.")
    return True


def run_context_validate():
    script_path = REPO_ROOT / "scripts" / "context-validate.py"
    if not script_path.exists():
        logging.warning("context-validate.py no encontrado. Se omite validacion.")
        return False
    result = subprocess.run([sys.executable, str(script_path)], cwd=REPO_ROOT)
    if result.returncode != 0:
        logging.warning("Validacion de contexto reporto errores.")
        return False
    logging.info("Validacion de contexto completada.")
    return True

def get_master_content():
    master_path = CONTEXT_DIR / "MASTER.md"
    if not master_path.exists():
        template_path = CONTEXT_DIR / "MASTER.template.md"
        if template_path.exists():
            logging.warning("MASTER.md no encontrado. Usando MASTER.template.md.")
            content = template_path.read_text(encoding='utf-8')
            try:
                master_path.write_text(content, encoding='utf-8')
            except Exception:
                pass
            return content
        logging.error(f"MASTER.md no encontrado en {master_path}")
        return None
    return master_path.read_text(encoding='utf-8')

def sync_tool(tool_name, master_content):
    tool_file = CONTEXT_DIR / f"{tool_name}.md"
    sync_block = f"{START_MARKER}\n{master_content}\n{END_MARKER}"
    
    if not tool_file.exists():
        logging.info(f"Creando nuevo archivo de contexto para {tool_name}")
        tool_file.write_text(f"# {tool_name.capitalize()} Context\n\n{sync_block}", encoding='utf-8')
        return

    content = tool_file.read_text(encoding='utf-8')
    
    if START_MARKER in content and END_MARKER in content:
        parts = content.split(START_MARKER)
        header = parts[0]
        footer_part = parts[1].split(END_MARKER)
        if len(footer_part) > 1:
            footer = footer_part[1]
            new_content = f"{header}{sync_block}{footer}"
            tool_file.write_text(new_content, encoding='utf-8')
            logging.info(f"Contexto actualizado para {tool_name}")
        else:
            logging.error(f"Error parseando marcadores en {tool_name}.md")
    else:
        tool_file.write_text(f"{content}\n\n{sync_block}", encoding='utf-8')
        logging.warning(f"Marcadores no encontrados en {tool_name}.md. Se ha apendizado el contexto.")

def main():
    logging.info("Iniciando sincronización de contexto...")
    run_context_snapshot()
    master_content = get_master_content()
    if not master_content:
        return

    for tool in TOOLS:
        try:
            sync_tool(tool, master_content)
        except Exception as e:
            logging.error(f"Error sincronizando {tool}: {str(e)}")

    run_context_validate()

if __name__ == "__main__":
    main()
