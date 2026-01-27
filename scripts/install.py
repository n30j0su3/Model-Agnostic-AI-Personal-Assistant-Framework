#!/usr/bin/env python3
import argparse
import datetime
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

from i18n import (
    Translator,
    detect_language,
    load_translations,
    select_language,
    set_language_in_master,
)
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
CLI_ORDER = ["opencode", "claude", "gemini", "codex"]
CLI_LABELS = {
    "opencode": "OpenCode",
    "claude": "Claude Code",
    "gemini": "Gemini CLI",
    "codex": "Codex",
}

LANGUAGE = "es"
TRANSLATOR = Translator({}, LANGUAGE)


def t(key, default=None, **kwargs):
    return TRANSLATOR.t(key, default, **kwargs)


def check_python_version():
    if sys.version_info < MIN_PYTHON:
        version = ".".join(str(v) for v in sys.version_info[:3])
        required = ".".join(str(v) for v in MIN_PYTHON)
        print(t("install.python.error", "[ERROR] Python {required}+ requerido. Version actual: {version}.", required=required, version=version))
        return False
    return True


def check_command(command):
    return shutil.which(command) is not None


def check_powershell_execution_policy():
    if os.name != "nt":
        return
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-ExecutionPolicy"],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return
    policy = (result.stdout or "").strip()
    if not policy:
        return
    normalized = policy.strip().lower()
    if normalized in {"restricted", "undefined"}:
        print(
            t(
                "install.ps.policy.warn",
                "[WARN] PowerShell tiene ExecutionPolicy '{policy}'. Esto puede bloquear opencode.ps1.",
                policy=policy,
            )
        )
        print(
            t(
                "install.ps.policy.fix",
                "[INFO] Solucion: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force",
            )
        )


def get_npm_prefix():
    cmd = ["npm", "config", "get", "prefix"]
    if os.name == "nt":
        npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
        if npm_cmd:
            cmd[0] = npm_cmd
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        else:
            result = subprocess.run("npm config get prefix", shell=True, capture_output=True, text=True, check=False)
    else:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return ""
    return (result.stdout or "").strip()


def save_env_vars(repo_root, npm_prefix=""):
    env_path = Path(repo_root) / ".context" / "env_vars.json"
    data = {}
    if env_path.exists():
        try:
            data = json.loads(env_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    if npm_prefix:
        data["npm_prefix"] = npm_prefix
    if not data:
        return
    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def ensure_master_context(repo_root):
    master_path = Path(repo_root) / ".context" / "MASTER.md"
    if master_path.exists():
        return
    template_path = Path(repo_root) / ".context" / "MASTER.template.md"
    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
    else:
        content = "# Personal Assistant - Master Context\n"
    master_path.parent.mkdir(parents=True, exist_ok=True)
    master_path.write_text(content.rstrip() + "\n", encoding="utf-8")


def ensure_opencode_config(repo_root):
    config_path = Path(repo_root) / "opencode.jsonc"
    if config_path.exists():
        return
    template_path = Path(repo_root) / "opencode.jsonc.template"
    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
        config_path.write_text(content.rstrip() + "\n", encoding="utf-8")


def run_sync(repo_root):
    sync_script = repo_root / "scripts" / "sync-context.py"
    if not sync_script.exists():
        print(t("install.sync.missing", "[ERROR] No se encontro scripts/sync-context.py."))
        return False
    result = subprocess.run([sys.executable, str(sync_script)], cwd=repo_root)
    if result.returncode != 0:
        print(t("install.sync.error", "[ERROR] sync-context.py fallo."))
        return False
    return True


def run_vendor_assets(repo_root):
    script_path = repo_root / "scripts" / "vendor_assets.py"
    if not script_path.exists():
        print(t("install.assets.missing", "[WARN] No se encontro scripts/vendor_assets.py."))
        return True
    result = subprocess.run([sys.executable, str(script_path)], cwd=repo_root)
    if result.returncode != 0:
        print(t("install.assets.error", "[WARN] Descarga de assets fallida. Ejecuta scripts/vendor_assets.py manualmente."))
        return False
    return True


def run_docs_manifest(repo_root):
    script_path = repo_root / "scripts" / "generate_docs_index.py"
    if not script_path.exists():
        print(t("install.docs.missing", "[WARN] No se encontro scripts/generate_docs_index.py."))
        return True
    result = subprocess.run([sys.executable, str(script_path)], cwd=repo_root)
    if result.returncode != 0:
        print(t("install.docs.error", "[WARN] Generacion de docs_manifest fallida."))
        return False
    return True


def prompt_profile():
    print(t("install.profile.title", "\nSelecciona tu perfil de instalacion:"))
    print(t("install.profile.basic", "  [1] Basico  - Personal, Professional, Content"))
    print(t("install.profile.pro", "  [2] Pro     - Todos los workspaces"))
    while True:
        selection = input(t("install.profile.prompt", "Seleccion (1/2) [1]: ")).strip() or "1"
        if selection in {"1", "2"}:
            return "basic" if selection == "1" else "pro"
        print(t("install.profile.invalid", "[WARN] Seleccion invalida. Usa 1 o 2."))


def prompt_yes_no(message, default=False):
    suffix = "[s/N]" if LANGUAGE == "es" else "[y/N]"
    if default:
        suffix = "[S/n]" if LANGUAGE == "es" else "[Y/n]"
    choice = input(f"{message} {suffix}: ").strip().lower()
    if not choice:
        return default
    return choice in {"s", "si", "y", "yes"}


def update_master_workspaces(repo_root, active_workspaces):
    master_path = repo_root / ".context" / "MASTER.md"
    if not master_path.exists():
        print(t("install.master.missing", "[WARN] No se encontro .context/MASTER.md. Se omite actualizacion."))
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
        print(t("install.workspaces.missing", "[WARN] Seccion 'Active Workspaces' no encontrada en MASTER.md."))
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


def save_profile(repo_root, profile, active_workspaces, llm_validated, default_cli):
    profile_path = repo_root / ".context" / "profile.md"
    profile_label = "Basico" if profile == "basic" else "Pro"
    workspaces_label = ", ".join([ws for ws in WORKSPACE_ORDER if ws in active_workspaces])
    llm_label = "Si" if llm_validated else "No"
    default_cli_label = default_cli or "N/D"
    content = (
        "# Perfil de Instalacion\n\n"
        f"- **Perfil**: {profile_label}\n"
        f"- **Fecha**: {datetime.date.today().isoformat()}\n"
        f"- **Workspaces activos**: {workspaces_label}\n"
        f"- **LLM validado**: {llm_label}\n"
        f"- **CLI default**: {default_cli_label}\n"
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
        print(t("install.master.missing", "[WARN] No se encontro .context/MASTER.md. Se omite configuracion guiada."))
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

    print(t("install.preferences.title", "\nConfiguracion de preferencias"))
    print(t("install.preferences.hint", "(Enter para mantener el valor actual)"))
    primary_input = input(f"{t('preferences.primary', 'Idioma principal')} [{primary_default}]: ").strip()
    secondary_input = input(f"{t('preferences.secondary', 'Idioma secundario')} [{secondary_default}]: ").strip()
    print(t("preferences.focus.hint", "Sugerencias: Operacion diaria, Feature Session, Investigacion, Personal."))
    focus_input = input(f"{t('preferences.focus', 'Enfoque actual')} [{focus_default}]: ").strip()
    response_input = input(f"{t('preferences.response', 'Estilo de respuesta')} [{response_default}]: ").strip()

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
    print(t("install.preferences.done", "[OK] Preferencias actualizadas en .context/MASTER.md"))


def check_llm_environment():
    missing_vars = [var for var in LLM_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        print(t("install.llm.vars.missing", "[WARN] Faltan variables de entorno para LLM:"))
        for var in missing_vars:
            print(f"  - {var}")
    else:
        print(t("install.llm.vars.ok", "[OK] Variables de entorno LLM configuradas."))

    missing_cmds = [cmd for cmd in LLM_CLI_COMMANDS if not check_command(cmd)]
    if missing_cmds:
        print(t("install.llm.clis.missing", "[WARN] CLIs LLM no detectadas en PATH:"))
        for cmd in missing_cmds:
            print(f"  - {cmd}")
    else:
        print(t("install.llm.clis.ok", "[OK] CLIs LLM detectadas."))

    local_cmds = [cmd for cmd in LOCAL_LLM_COMMANDS if check_command(cmd)]
    if local_cmds:
        detected = ", ".join(local_cmds)
        print(t("install.llm.locals.ok", "[OK] LLM locales detectados: {detected}.", detected=detected))
    else:
        print(t("install.llm.locals.none", "[INFO] LLM locales no detectados (opcional): ollama, lms."))


def detect_available_clis():
    return [cmd for cmd in LLM_CLI_COMMANDS if check_command(cmd)]


def _open_node_download():
    link = t("node.manual.link", "Descarga directa: https://nodejs.org/en/download")
    print(link)
    try:
        webbrowser.open("https://nodejs.org/en/download")
    except Exception:
        return


def ensure_node():
    if check_command("npm"):
        return True
    print(t("node.missing", "[WARN] npm no detectado. Node.js es necesario para instalar OpenCode."))

    os_name = platform.system()
    if os_name == "Windows":
        if not check_command("winget"):
            _open_node_download()
            return False
        if not prompt_yes_no(t("node.install.ask", "Deseas instalar Node.js ahora?"), default=True):
            _open_node_download()
            return False
        print(t("node.install.start", "[INFO] Instalando Node.js..."))
        result = subprocess.run(
            [
                "winget",
                "install",
                "-e",
                "--id",
                "OpenJS.NodeJS.LTS",
                "--accept-source-agreements",
                "--accept-package-agreements",
            ],
            check=False,
        )
        if result.returncode != 0:
            print(t("node.install.fail", "[WARN] No se pudo instalar Node.js automaticamente."))
            _open_node_download()
            return False
        if check_command("npm"):
            print(t("node.install.ok", "[OK] Node.js instalado."))
            return True
        print(t("node.install.restart", "[INFO] Reinicia la terminal y vuelve a ejecutar el instalador."))
        return False

    if os_name == "Darwin":
        if check_command("brew") and prompt_yes_no(
            t("node.install.ask", "Deseas instalar Node.js ahora?"), default=False
        ):
            print(t("node.install.start", "[INFO] Instalando Node.js..."))
            result = subprocess.run(["brew", "install", "node"], check=False)
            if result.returncode == 0 and check_command("npm"):
                print(t("node.install.ok", "[OK] Node.js instalado."))
                return True
            print(t("node.install.fail", "[WARN] No se pudo instalar Node.js automaticamente."))
        print(t("node.manual.brew", "macOS: brew install node"))
        _open_node_download()
        return False

    if check_command("apt"):
        if prompt_yes_no(t("node.install.ask", "Deseas instalar Node.js ahora?"), default=False):
            print(t("node.install.start", "[INFO] Instalando Node.js..."))
            result = subprocess.run(["sudo", "apt", "install", "-y", "nodejs", "npm"], check=False)
            if result.returncode == 0 and check_command("npm"):
                print(t("node.install.ok", "[OK] Node.js instalado."))
                return True
            print(t("node.install.fail", "[WARN] No se pudo instalar Node.js automaticamente."))
        print(t("node.manual.apt", "Debian/Ubuntu: sudo apt install nodejs npm"))
        _open_node_download()
        return False

    if check_command("dnf"):
        if prompt_yes_no(t("node.install.ask", "Deseas instalar Node.js ahora?"), default=False):
            print(t("node.install.start", "[INFO] Instalando Node.js..."))
            result = subprocess.run(["sudo", "dnf", "install", "-y", "nodejs", "npm"], check=False)
            if result.returncode == 0 and check_command("npm"):
                print(t("node.install.ok", "[OK] Node.js instalado."))
                return True
            print(t("node.install.fail", "[WARN] No se pudo instalar Node.js automaticamente."))
        print(t("node.manual.dnf", "Fedora/RHEL: sudo dnf install nodejs npm"))
        _open_node_download()
        return False

    if check_command("pacman"):
        if prompt_yes_no(t("node.install.ask", "Deseas instalar Node.js ahora?"), default=False):
            print(t("node.install.start", "[INFO] Instalando Node.js..."))
            result = subprocess.run(["sudo", "pacman", "-S", "nodejs", "npm"], check=False)
            if result.returncode == 0 and check_command("npm"):
                print(t("node.install.ok", "[OK] Node.js instalado."))
                return True
            print(t("node.install.fail", "[WARN] No se pudo instalar Node.js automaticamente."))
        print(t("node.manual.pacman", "Arch: sudo pacman -S nodejs npm"))
        _open_node_download()
        return False

    print(t("node.manual.generic", "Instala Node.js con tu gestor de paquetes."))
    _open_node_download()
    return False


def install_opencode():
    if not ensure_node():
        return False
    print(t("cli.install.start", "[INFO] Instalando OpenCode..."))
    cmd = ["npm", "install", "-g", "opencode-ai"]
    if os.name == "nt":
        npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
        if npm_cmd:
            cmd[0] = npm_cmd
            result = subprocess.run(cmd, check=False)
        else:
            result = subprocess.run("npm install -g opencode-ai", shell=True, check=False)
    else:
        result = subprocess.run(cmd, check=False)
    if result.returncode == 0:
        print(t("cli.install.ok", "[OK] OpenCode instalado."))
        prefix = get_npm_prefix()
        if prefix:
            save_env_vars(Path(__file__).resolve().parents[1], npm_prefix=prefix)
        return True
    print(t("cli.install.fail", "[WARN] No se pudo instalar OpenCode. Instala manualmente."))
    return False


def choose_default_cli():
    detected = detect_available_clis()
    if not detected:
        print(t("cli.none", "No se detecto ninguna CLI de IA instalada."))
        print(f"  1. {t('cli.option.opencode', 'OpenCode (recomendado)')}")
        print(f"  5. {t('cli.option.help', 'No se como hacerlo')}")
        print(f"  6. {t('cli.option.skip', 'Continuar sin CLI')}")
        choice = input(t("cli.select", "Selecciona [1-6]: ")).strip()
        if choice == "1":
            return "opencode" if install_opencode() else ""
        if choice == "5":
            print(t("cli.docs", "Guia: docs/quickstart.mdx"))
            return ""
        return ""

    print(t("cli.detected", "CLIs detectadas: {clis}", clis=", ".join(detected)))
    print(t("cli.default.prompt", "Selecciona la CLI por defecto:"))
    options = {}
    index = 1
    for cli in CLI_ORDER:
        if cli in detected:
            label = CLI_LABELS.get(cli, cli)
            print(f"  {index}. {label}")
            options[str(index)] = cli
            index += 1

    help_idx = str(index)
    print(f"  {help_idx}. {t('cli.option.help', 'No se como hacerlo')}")
    skip_idx = str(index + 1)
    print(f"  {skip_idx}. {t('cli.option.skip', 'Continuar sin CLI')}")

    choice = input(t("cli.select", "Selecciona [1-6]: ")).strip()
    if choice == help_idx:
        print(t("cli.docs", "Guia: docs/quickstart.mdx"))
        return ""
    if choice == skip_idx:
        return ""
    selected = options.get(choice)
    if selected:
        print(t("cli.default.set", "CLI por defecto: {cli}", cli=CLI_LABELS.get(selected, selected)))
        return selected
    return ""


def main():
    parser = argparse.ArgumentParser(description="Instalador multiplataforma del framework.")
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
    parser.add_argument(
        "--lang",
        choices=["es", "en"],
        help="Selecciona idioma (es/en).",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    translations = load_translations(repo_root)
    profile_path = repo_root / ".context" / "profile.md"

    ensure_master_context(repo_root)
    ensure_opencode_config(repo_root)

    selected_lang = args.lang
    if not selected_lang and not profile_path.exists():
        selected_lang = select_language(translations)
    if not selected_lang:
        selected_lang = detect_language(repo_root)

    set_language_in_master(repo_root, selected_lang)
    global LANGUAGE, TRANSLATOR
    LANGUAGE = selected_lang
    TRANSLATOR = Translator(translations, selected_lang)

    print(t("install.welcome", "Bienvenido al Personal Assistant Framework"))

    os_name = platform.system()
    print(t("install.system", "[INFO] Sistema detectado: {os}", os=os_name))
    print(t("install.repo", "[INFO] Repo: {path}", path=repo_root))
    check_powershell_execution_policy()

    if not check_python_version():
        sys.exit(1)

    if not check_command("git"):
        print(t("install.git.warn", "[WARN] Git no detectado en PATH. Si ya clonaste el repo, ignora este aviso."))

    setup_repository(repo_root, translator=TRANSLATOR)

    profile = args.profile or prompt_profile()
    active_workspaces = BASIC_WORKSPACES if profile == "basic" else PRO_WORKSPACES
    profile_label = "Basico" if profile == "basic" else "Pro"
    print(t("install.profile.selected", "[INFO] Perfil seleccionado: {profile}", profile=profile_label))

    default_cli = choose_default_cli()

    llm_validate = args.llm
    if profile == "pro" and not args.llm:
        llm_validate = prompt_yes_no(t("install.llm.ask", "Validar configuracion de LLM?"), default=False)

    update_master_workspaces(repo_root, active_workspaces)
    save_profile(repo_root, profile, active_workspaces, llm_validate, default_cli)

    if prompt_yes_no(
        t("install.preferences.ask", "Configurar preferencias personales ahora (idioma, enfoque, estilo)?"),
        default=True,
    ):
        configure_preferences(repo_root)

    if not run_sync(repo_root):
        sys.exit(1)

    run_vendor_assets(repo_root)
    run_docs_manifest(repo_root)

    if llm_validate:
        check_llm_environment()

    print(t("install.complete", "[OK] Instalacion completada."))
    print(t("install.next", "[NEXT] Edita .context/MASTER.md y vuelve a correr sync-context si haces cambios."))


if __name__ == "__main__":
    main()
