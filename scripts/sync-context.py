#!/usr/bin/env python3
import os
import logging
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

CONTEXT_DIR = Path(".context")
TOOLS = ["opencode", "claude", "gemini", "agents"]
START_MARKER = "<!-- MASTER-CONTEXT-START -->"
END_MARKER = "<!-- MASTER-CONTEXT-END -->"

def get_master_content():
    master_path = CONTEXT_DIR / "MASTER.md"
    if not master_path.exists():
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
    master_content = get_master_content()
    if not master_content:
        return

    for tool in TOOLS:
        try:
            sync_tool(tool, master_content)
        except Exception as e:
            logging.error(f"Error sincronizando {tool}: {str(e)}")

if __name__ == "__main__":
    main()
