#!/usr/bin/env python3
"""
Skill Sync Script
Sincroniza, valida y genera el índice global de skills del framework.
Siguiendo la especificación de https://agentskills.io/specification
"""

import os
import yaml
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path("skills")
INDEX_FILE = SKILLS_DIR / "SKILLS.md"

def parse_skill(skill_path):
    """Parsea el frontmatter de un SKILL.md."""
    try:
        content = skill_path.read_text(encoding='utf-8')
        parts = content.split("---")
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            # Obtener ruta relativa de forma robusta
            rel_path = os.path.relpath(skill_path.parent, os.getcwd()).replace("\\", "/")
            return {
                "name": frontmatter.get("name"),
                "description": frontmatter.get("description"),
                "path": rel_path,
                "metadata": frontmatter.get("metadata", {}),
                "valid": True
            }
    except Exception as e:
        print(f"Error parseando {skill_path}: {e}")
    return None

def sync_skills():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando sincronizacion de skills...")
    
    skills = []
    # Buscar todos los archivos SKILL.md
    for skill_file in SKILLS_DIR.rglob("SKILL.md"):
        if skill_file.resolve() != INDEX_FILE.resolve():
            skill_data = parse_skill(skill_file)
            if skill_data:
                skills.append(skill_data)

    if not skills:
        print("INFO: No se encontraron skills individuales.")
        return

    # Generar contenido del índice
    content = [
        "# Personal Assistant Skills Index",
        "",
        "Este archivo es generado automáticamente por `scripts/skill-sync.py`.",
        "",
        "## Available Skills",
        ""
    ]

    # Ordenar por nombre
    skills.sort(key=lambda x: x['name'])

    for s in skills:
        content.append(f"### @{s['name']}")
        content.append(f"- **Descripcion**: {s['description']}")
        content.append(f"- **Ubicacion**: `{s['path']}`")
        if s['metadata'] and s['metadata'].get('version'):
            content.append(f"- **Version**: {s['metadata']['version']}")
        content.append("")

    content.append("---\n*Ultima actualizacion: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*")

    INDEX_FILE.write_text("\n".join(content), encoding='utf-8')
    print(f"OK: Indice generado en {INDEX_FILE} ({len(skills)} skills detectados)")

if __name__ == "__main__":
    sync_skills()
