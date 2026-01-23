#!/usr/bin/env python3
import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

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
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    os_name = platform.system()
    print(f"[INFO] Sistema detectado: {os_name}")
    print(f"[INFO] Repo: {repo_root}")

    if not check_python_version():
        sys.exit(1)

    if not check_command("git"):
        print("[WARN] Git no detectado en PATH. Si ya clonaste el repo, ignora este aviso.")

    if not run_sync(repo_root):
        sys.exit(1)

    if args.llm:
        check_llm_environment()

    print("[OK] Instalacion completada.")
    print("[NEXT] Edita .context/MASTER.md y vuelve a correr sync-context si haces cambios.")


if __name__ == "__main__":
    main()
