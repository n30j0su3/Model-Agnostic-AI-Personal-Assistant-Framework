#!/usr/bin/env python3
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTEXT_DIR = REPO_ROOT / ".context"
WORKSPACES_DIR = REPO_ROOT / "workspaces"
START_MARKER = "<!-- MASTER-CONTEXT-START -->"
END_MARKER = "<!-- MASTER-CONTEXT-END -->"
TOOLS = ["opencode", "claude", "gemini", "agents"]


def report(status, message):
    print(f"[{status}] {message}")


def load_master():
    master_path = CONTEXT_DIR / "MASTER.md"
    if not master_path.exists():
        report("ERROR", "MASTER.md no encontrado en .context")
        return None
    content = master_path.read_text(encoding="utf-8", errors="replace")
    return content


def validate_master(content):
    required_sections = [
        "## Localization",
        "## Active Workspaces",
        "## Current Focus",
        "## Preferences",
        "## Rules",
    ]
    missing = [section for section in required_sections if section not in content]
    if missing:
        report("WARN", f"MASTER.md sin secciones requeridas: {', '.join(missing)}")
        return False
    report("OK", "MASTER.md contiene secciones requeridas")
    return True


def parse_active_workspaces(content):
    active = []
    for line in content.splitlines():
        match = re.match(r"- \[x\] ([^:]+):", line)
        if match:
            active.append(match.group(1).strip())
    return active


def validate_workspaces(active):
    if not active:
        report("WARN", "No hay workspaces activos en MASTER.md")
        return
    for workspace in active:
        folder = WORKSPACES_DIR / workspace.lower()
        if not folder.exists():
            report("WARN", f"Workspace activo sin carpeta: {workspace}")
            continue
        report("OK", f"Workspace activo presente: {workspace}")


def validate_tool_contexts():
    for tool in TOOLS:
        tool_path = CONTEXT_DIR / f"{tool}.md"
        if not tool_path.exists():
            report("WARN", f"Contexto no encontrado para {tool}")
            continue
        content = tool_path.read_text(encoding="utf-8", errors="replace")
        if START_MARKER not in content or END_MARKER not in content:
            report("WARN", f"Marcadores faltantes en {tool}.md")
        else:
            report("OK", f"Marcadores presentes en {tool}.md")


def validate_profile():
    profile_path = CONTEXT_DIR / "profile.md"
    if not profile_path.exists():
        report("WARN", "profile.md no encontrado")
        return
    content = profile_path.read_text(encoding="utf-8", errors="replace")
    required_fields = ["- **Perfil**:", "- **Workspaces activos**:"]
    missing = [field for field in required_fields if field not in content]
    if missing:
        report("WARN", f"profile.md sin campos: {', '.join(missing)}")
    else:
        report("OK", "profile.md contiene campos requeridos")


def validate_manifest():
    manifest_path = CONTEXT_DIR / "manifest.md"
    if not manifest_path.exists():
        report("WARN", "manifest.md no encontrado")
        return
    report("OK", "manifest.md presente")


def validate_models():
    models_path = CONTEXT_DIR / "models.md"
    if not models_path.exists():
        report("WARN", "models.md no encontrado (orquestacion opcional)")
        return
    content = models_path.read_text(encoding="utf-8", errors="replace")
    if "## Configuracion Activa" not in content:
        report("WARN", "models.md sin seccion de configuracion activa")
    else:
        report("OK", "models.md contiene configuracion activa")


def main():
    master_content = load_master()
    if master_content is None:
        return 1

    validate_master(master_content)
    validate_workspaces(parse_active_workspaces(master_content))
    validate_tool_contexts()
    validate_profile()
    validate_manifest()
    validate_models()
    return 0


if __name__ == "__main__":
    sys.exit(main())
