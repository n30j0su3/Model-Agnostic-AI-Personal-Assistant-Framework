#!/usr/bin/env python3
import argparse
import datetime
import re
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from setup_repo import setup_repository
MIN_PYTHON = (3, 11)
LLM_ENV_VARS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
]
LLM_CLI_COMMANDS = [
    "opencode",
    "claude",
    "gemini",
    "codex",
]
LOCAL_LLM_COMMANDS = [
    "ollama",
    "lms",
]
WORKSPACE_ORDER = [
    "Personal",
    "Professional",
    "Research",
    "Content",
    "Development",
    "Homelab",
]
BASIC_WORKSPACES = {"Personal", "Professional", "Content"}
PRO_WORKSPACES = set(WORKSPACE_ORDER)


def check_python_version():
    if sys.version_info < MIN_PYTHON:
        version = ".".join(str(v) for v in sys.version_info[:3])
        required = ".".join(str(v) for v in MIN_PYTHON)
        print(f"[ERROR] Python {required}+ requerido. Version actual: {version}.")
        return False
    return True


def check_command(command):
    return shutil.which(command) is not None


def run_sync(repo_root):
    sync_script = repo_root / "scripts" / "sync-context.py"
    if not sync_script.exists():
        print("[ERROR] No se encontro scripts/sync-context.py.")
        return False
    result = subprocess.run([sys.executable, str(sync_script)], cwd=repo_root)
    if result.returncode != 0:
        print("[ERROR] sync-context.py fallo.")
        return False
    return True


def prompt_profile():
    print("\nSelecciona tu perfil de instalacion:")
    print("  [1] Basico  - Personal, Professional, Content")
    print("  [2] Pro     - Todos los workspaces")
    while True:
        selection = input("Seleccion (1/2) [1]: ").strip() or "1"
        if selection in {"1", "2"}:
            return "basic" if selection == "1" else "pro"
        print("[WARN] Seleccion invalida. Usa 1 o 2.")


def prompt_yes_no(message, default=False):
    suffix = "[s/N]" if not default else "[S/n]"
    choice = input(f"{message} {suffix}: ").strip().lower()
    if not choice:
        return default
    return choice in {"s", "si", "y", "yes"}


def update_master_workspaces(repo_root, active_workspaces):
    master_path = repo_root / ".context" / "MASTER.md"
    if not master_path.exists():
        print("[WARN] No se encontro .context/MASTER.md. Se omite actualizacion.")
        return

    lines = master_path.read_text(encoding="utf-8").splitlines()
    start_idx = None
    end_idx = None
    for idx, line in enumerate(lines):
        if line.strip() == "## Active Workspaces":
            start_idx = idx
            continue
        if start_idx is not None and idx > start_idx and line.startswith("## "):
            end_idx = idx
            break
    if start_idx is None:
        print("[WARN] Seccion 'Active Workspaces' no encontrada en MASTER.md.")
        return
    if end_idx is None:
        end_idx = len(lines)

    header_block = lines[: start_idx + 1]
    footer_block = lines[end_idx:]
    workspace_lines = []
    for workspace in WORKSPACE_ORDER:
        is_active = workspace in active_workspaces
        status_text = "Configurado y activo." if is_active else "No configurado."
        checkbox = "x" if is_active else " "
        workspace_lines.append(f"- [{checkbox}] {workspace}: {status_text}")
    workspace_lines.append("")
    lines = header_block + workspace_lines + footer_block
    master_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_profile(repo_root, profile, active_workspaces, llm_validated):
    profile_path = repo_root / ".context" / "profile.md"
    profile_label = "Basico" if profile == "basic" else "Pro"
    workspaces_label = ", ".join([ws for ws in WORKSPACE_ORDER if ws in active_workspaces])
    llm_label = "Si" if llm_validated else "No"
    content = (
        "# Perfil de Instalacion\n\n"
        f"- **Perfil**: {profile_label}\n"
        f"- **Fecha**: {datetime.date.today().isoformat()}\n"
        f"- **Workspaces activos**: {workspaces_label}\n"
        f"- **LLM validado**: {llm_label}\n"
    )
    profile_path.write_text(content, encoding="utf-8")


def _extract_line_value(lines, prefix):
    for line in lines:
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip()
    return ""


def configure_preferences(repo_root):
    master_path = repo_root / ".context" / "MASTER.md"
    if not master_path.exists():
        print("[WARN] No se encontro .context/MASTER.md. Se omite configuracion guiada.")
        return

    content = master_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    primary_default = _extract_line_value(lines, "- **Primary Language**:")
    secondary_default = _extract_line_value(lines, "- **Secondary Language**:")
    response_default = _extract_line_value(lines, "- Response style:")

    focus_start = None
    focus_end = None
    for idx, line in enumerate(lines):
        if line.strip() == "## Current Focus":
            focus_start = idx + 1
            continue
        if focus_start is not None and idx > focus_start and line.startswith("## "):
            focus_end = idx
            break
    if focus_start is not None and focus_end is None:
        focus_end = len(lines)
    focus_default = ""
    if focus_start is not None and focus_end is not None:
        focus_default = "\n".join(lines[focus_start:focus_end]).strip()

    print("\nConfiguracion de preferencias")
    print("(Enter para mantener el valor actual)")
    primary_input = input(f"Idioma principal [{primary_default}]: ").strip()
    secondary_input = input(f"Idioma secundario [{secondary_default}]: ").strip()
    focus_input = input(f"Enfoque actual [{focus_default}]: ").strip()
    response_input = input(f"Estilo de respuesta [{response_default}]: ").strip()

    primary_value = primary_input or primary_default
    secondary_value = secondary_input or secondary_default
    focus_value = focus_input or focus_default
    response_value = response_input or response_default

    if primary_value:
        content = re.sub(
            r"- \*\*Primary Language\*\*: .*",
            f"- **Primary Language**: {primary_value}",
            content,
        )
    if secondary_value:
        content = re.sub(
            r"- \*\*Secondary Language\*\*: .*",
            f"- **Secondary Language**: {secondary_value}",
            content,
        )
    if response_value:
        content = re.sub(
            r"- Response style: .*",
            f"- Response style: {response_value}",
            content,
        )

    if focus_start is not None and focus_end is not None:
        new_lines = content.splitlines()
        lines_prefix = new_lines[:focus_start]
        lines_suffix = new_lines[focus_end:]
        focus_lines = [focus_value, ""] if focus_value else [""]
        new_lines = lines_prefix + focus_lines + lines_suffix
        content = "\n".join(new_lines)

    master_path.write_text(content.rstrip() + "\n", encoding="utf-8")
    print("[OK] Preferencias actualizadas en .context/MASTER.md")


def check_llm_environment():
    missing_vars = [var for var in LLM_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        print("[WARN] Faltan variables de entorno para LLM:")
        for var in missing_vars:
            print(f"  - {var}")
    else:
        print("[OK] Variables de entorno LLM configuradas.")

    missing_cmds = [cmd for cmd in LLM_CLI_COMMANDS if not check_command(cmd)]
    if missing_cmds:
        print("[WARN] CLIs LLM no detectadas en PATH:")
        for cmd in missing_cmds:
            print(f"  - {cmd}")
    else:
        print("[OK] CLIs LLM detectadas.")

    local_cmds = [cmd for cmd in LOCAL_LLM_COMMANDS if check_command(cmd)]
    if local_cmds:
        detected = ", ".join(local_cmds)
        print(f"[OK] LLM locales detectados: {detected}.")
    else:
        print("[INFO] LLM locales no detectados (opcional): ollama, lms.")


def main():
    parser = argparse.ArgumentParser(
        description="Instalador multiplataforma del framework.")
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Valida configuracion de LLM (API keys y CLIs).",
    )
    parser.add_argument(
        "--profile",
        choices=["basic", "pro"],
        help="Selecciona perfil de instalacion: basic o pro.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    os_name = platform.system()
    print(f"[INFO] Sistema detectado: {os_name}")
    print(f"[INFO] Repo: {repo_root}")

    if not check_python_version():
        sys.exit(1)

    if not check_command("git"):
        print("[WARN] Git no detectado en PATH. Si ya clonaste el repo, ignora este aviso.")

    setup_repository(repo_root)

    profile = args.profile or prompt_profile()
    active_workspaces = BASIC_WORKSPACES if profile == "basic" else PRO_WORKSPACES
    profile_label = "Basico" if profile == "basic" else "Pro"
    print(f"[INFO] Perfil seleccionado: {profile_label}")

    llm_validate = args.llm
    if profile == "pro" and not args.llm:
        llm_validate = prompt_yes_no("Validar configuracion de LLM?", default=False)

    update_master_workspaces(repo_root, active_workspaces)
    save_profile(repo_root, profile, active_workspaces, llm_validate)

    if prompt_yes_no(
        "Configurar preferencias personales ahora (idioma, enfoque, estilo)?",
        default=True,
    ):
        configure_preferences(repo_root)

    if not run_sync(repo_root):
        sys.exit(1)

    if llm_validate:
        check_llm_environment()

    print("[OK] Instalacion completada.")
    print("[NEXT] Edita .context/MASTER.md y vuelve a correr sync-context si haces cambios.")


if __name__ == "__main__":
    main()
