#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

from install import (
    configure_preferences,
    LLM_CLI_COMMANDS,
    LLM_ENV_VARS,
    LOCAL_LLM_COMMANDS,
    MIN_PYTHON,
)
from orchestrate import (
    DEFAULT_MODELS,
    MODELS_PATH,
    cmd_disable,
    cmd_init,
    cmd_list,
    cmd_recommend,
    cmd_status,
    cmd_switch,
    ensure_initialized,
    load_models_content,
    parse_active_models,
    parse_catalog,
)
from i18n import get_translator
from utils import PlatformHelper, get_repo_root

REPO_ROOT = get_repo_root()
TRANSLATOR = get_translator(REPO_ROOT)
LANGUAGE = TRANSLATOR.language
CLI_LABELS = {
    "opencode": "OpenCode",
    "claude": "Claude",
    "gemini": "Gemini",
    "codex": "Codex",
    "ollama": "Ollama",
}


def t(key, default=None, **kwargs):
    return TRANSLATOR.t(key, default, **kwargs)


def init_repo_root():
    os.chdir(REPO_ROOT)


def setup_unicode():
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not reconfigure:
            continue
        try:
            reconfigure(encoding="utf-8")
        except Exception:
            continue


def clear_screen():
    PlatformHelper.clear_screen()


def print_header():
    print("╔═══════════════════════════════════════════════════════╗")
    print("║   Personal Assistant Framework - Control Panel        ║")
    print("╚═══════════════════════════════════════════════════════╝")


def pause(message=None):
    if message is None:
        message = t("pause.prompt", "Presiona Enter para continuar...")
    input(f"\n{message}")


def prompt_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(t("menu.invalid", "[WARN] Opcion invalida. Intenta de nuevo."))


def prompt_yes_no(message, default=False):
    suffix = "[s/N]" if LANGUAGE == "es" else "[y/N]"
    if default:
        suffix = "[S/n]" if LANGUAGE == "es" else "[Y/n]"
    choice = input(f"{message} {suffix}: ").strip().lower()
    if not choice:
        return default
    return choice in {"s", "si", "y", "yes"}


def run_sync_context():
    sync_script = REPO_ROOT / "scripts" / "sync-context.py"
    if not sync_script.exists():
        print("[ERROR] No se encontro scripts/sync-context.py.")
        return False
    result = PlatformHelper.run_command([PlatformHelper.get_python_executable(), str(sync_script)], cwd=REPO_ROOT, capture_output=False)
    return result.returncode == 0


def run_context_version(args):
    script_path = REPO_ROOT / "scripts" / "context-version.py"
    if not script_path.exists():
        print("[ERROR] No se encontro scripts/context-version.py.")
        return False
    result = PlatformHelper.run_command([PlatformHelper.get_python_executable(), str(script_path), *args], cwd=REPO_ROOT, capture_output=False)
    return result.returncode == 0


def run_context_validate():
    script_path = REPO_ROOT / "scripts" / "context-validate.py"
    if not script_path.exists():
        print("[ERROR] No se encontro scripts/context-validate.py.")
        return False
    result = PlatformHelper.run_command([PlatformHelper.get_python_executable(), str(script_path)], cwd=REPO_ROOT, capture_output=False)
    return result.returncode == 0


def menu_sync():
    print("\n🔄 Sincronizando contexto...")
    if run_sync_context():
        print("[OK] Contexto sincronizado.")
    else:
        print("[ERROR] Fallo la sincronizacion de contexto.")
    pause()


def menu_profile():
    print("\n⚙️  Configuracion de perfil")
    configure_preferences(REPO_ROOT)
    pause()


def get_orchestration_state():
    if not MODELS_PATH.exists():
        return "No activada", None, None
    content = load_models_content()
    if not content.strip():
        return "Archivo vacio", None, None
    primary, fallback = parse_active_models(content)
    return "Activa", primary, fallback


def orchestration_info():
    print(
        "\nEsta opcion es opcional y no reemplaza la configuracion nativa de cada terminal."
    )
    print(
        "Sirve como punto central para cambiar modelos rapidamente con .context/models.md."
    )
    print(
        "Si prefieres usar cada terminal con su configuracion propia, puedes ignorarla."
    )


def menu_orchestration():
    while True:
        clear_screen()
        print("-- 🎛️ Orquestacion Multi-Modelo --")
        state, primary, fallback = get_orchestration_state()
        if state == "Activa":
            print(f"Estado: ✅ {state} | Modelo: {primary} | Fallback: {fallback}")
            print("\n  1. 📋 Ver estado completo")
            print("  2. 🔀 Cambiar modelo principal")
            print("  3. 🔁 Cambiar modelo fallback")
            print("  4. 💡 Recomendar modelo para tarea")
            print("  5. ❌ Desactivar orquestacion")
            print("  0. ⬅️  Volver")
            choice = prompt_choice("\nSelecciona: ", {"0", "1", "2", "3", "4", "5"})
            if choice == "0":
                return
            if choice == "1":
                cmd_status()
                pause()
            elif choice == "2":
                cmd_list()
                model_id = input("\nID del modelo principal: ").strip()
                if model_id:
                    cmd_switch(model_id, is_fallback=False)
                pause()
            elif choice == "3":
                cmd_list()
                model_id = input("\nID del modelo fallback: ").strip()
                if model_id:
                    cmd_switch(model_id, is_fallback=True)
                pause()
            elif choice == "4":
                task_text = input("\nDescribe la tarea: ").strip()
                if task_text:
                    cmd_recommend(task_text)
                pause()
            elif choice == "5":
                cmd_disable()
                pause()
        else:
            print(f"Estado: ⚠️ {state}")
            print("\n  1. ✅ Activar orquestacion")
            print("  2. ℹ️  Que es esto?")
            print("  0. ⬅️  Volver")
            choice = prompt_choice("\nSelecciona: ", {"0", "1", "2"})
            if choice == "0":
                return
            if choice == "1":
                cmd_init()
                pause()
            elif choice == "2":
                orchestration_info()
                pause()


def status_line(ok, label, warning=False):
    icon = "✅" if ok else "⚠️" if warning else "❌"
    print(f"{icon} {label}")


def menu_health():
    print("\n📊 Estado del Sistema\n")
    python_ok = sys.version_info >= MIN_PYTHON
    version_text = ".".join(str(v) for v in sys.version_info[:3])
    min_text = ".".join(str(v) for v in MIN_PYTHON)
    status_line(python_ok, f"Python {version_text} (min {min_text})")

    git_ok = shutil.which("git") is not None
    status_line(git_ok, "Git disponible", warning=not git_ok)

    master_ok = (REPO_ROOT / ".context" / "MASTER.md").exists()
    status_line(master_ok, ".context/MASTER.md existe", warning=not master_ok)

    profile_ok = (REPO_ROOT / ".context" / "profile.md").exists()
    status_line(profile_ok, ".context/profile.md existe", warning=not profile_ok)

    orchestration_ok = MODELS_PATH.exists()
    status_line(orchestration_ok, "Orquestacion activada", warning=not orchestration_ok)

    for var in LLM_ENV_VARS:
        status_line(bool(os.getenv(var)), f"{var} configurada", warning=True)

    for cmd in LLM_CLI_COMMANDS:
        status_line(shutil.which(cmd) is not None, f"CLI {cmd} detectada", warning=True)

    for cmd in LOCAL_LLM_COMMANDS:
        detected = shutil.which(cmd) is not None
        status_line(detected, f"CLI local {cmd} detectada", warning=True)

    pause()


def menu_context_maintenance():
    while True:
        clear_screen()
        print("-- 🛠️ Mantenimiento de Snapshots --")
        print("\n  1. 🗑️  Limpiar snapshots antiguos (por dias)")
        print("  2. 📦 Exportar backup completo (.zip)")
        print("  3. 📥 Importar backup (.zip)")
        print("  4. 📊 Metricas y estadisticas")
        print("  5. 🧹 Eliminar snapshot especifico")
        print("  0. ⬅️  Volver")
        choice = prompt_choice("\nSelecciona: ", {"0", "1", "2", "3", "4", "5"})
        if choice == "0":
            return
        if choice == "1":
            days = input("\nEliminar snapshots mas antiguos de cuantos dias? ").strip()
            if days.isdigit():
                run_context_version(["clean", "--older", days])
            else:
                print("[WARN] Ingresa un numero valido.")
            pause()
        elif choice == "2":
            run_context_version(["export"])
            pause()
        elif choice == "3":
            path = input("\nRuta al backup .zip: ").strip()
            if path:
                if prompt_yes_no("Importar backup y sobrescribir archivos?"):
                    run_context_version(["import", path, "--force"])
            pause()
        elif choice == "4":
            run_context_version(["stats"])
            pause()
        elif choice == "5":
            run_context_version(["list"])
            timestamp = input("\nTimestamp del snapshot a eliminar: ").strip()
            if timestamp:
                if prompt_yes_no("Eliminar snapshot seleccionado?"):
                    run_context_version(["delete", timestamp, "--force"])
            pause()


def menu_context_management():
    while True:
        clear_screen()
        print("-- 📁 Gestion de Contexto --")
        print("\n  1. 📷 Crear snapshot")
        print("  2. 📋 Listar snapshots")
        print("  3. ⏪ Restaurar snapshot")
        print("  4. 🔍 Comparar con snapshot")
        print("  5. ✅ Validar consistencia")
        print("  6. 🛠️  Mantenimiento de snapshots")
        print("  0. ⬅️  Volver")
        choice = prompt_choice("\nSelecciona: ", {"0", "1", "2", "3", "4", "5", "6"})
        if choice == "0":
            return
        if choice == "1":
            run_context_version(["snapshot"])
            pause()
        elif choice == "2":
            run_context_version(["list"])
            pause()
        elif choice == "3":
            run_context_version(["list"])
            timestamp = input("\nTimestamp a restaurar: ").strip()
            if timestamp:
                if prompt_yes_no(
                    "Restaurar snapshot y sobrescribir archivos actuales?"
                ):
                    run_context_version(["restore", timestamp, "--force"])
            pause()
        elif choice == "4":
            run_context_version(["list"])
            timestamp = input("\nTimestamp para comparar: ").strip()
            if timestamp:
                run_context_version(["diff", timestamp])
            pause()
        elif choice == "5":
            run_context_validate()
            pause()
        elif choice == "6":
            menu_context_maintenance()


def menu_backlog():
    print("\n📋 Backlog de Desarrollo (Vista Filtrada)\n")
    backlog_path = REPO_ROOT / "docs" / "backlog.view.md"
    if backlog_path.exists():
        try:
            print(backlog_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[ERROR] No se pudo leer el archivo: {e}")
    else:
        print("[WARN] No se encontro docs/backlog.view.md")

    print("\n💡 Tip: Usa 'docs/backlog.md' para ver el historial completo.")
    pause()


def menu_decision_engine():
    print("\n🧭 Decision Engine\n")
    script_path = (
        REPO_ROOT / "skills" / "core" / "decision-engine" / "scripts" / "route.py"
    )
    if not script_path.exists():
        print("[ERROR] No se encontro skills/core/decision-engine/scripts/route.py")
        pause()
        return

    print("  1. Evaluar instruccion")
    print("  2. Listar reglas locales")
    print("  3. Listar agentes y keywords")
    print("  0. Volver")
    choice = prompt_choice("\nSelecciona: ", {"0", "1", "2", "3"})
    if choice == "0":
        return

    if choice == "1":
        text = input("\nInstruccion a evaluar: ").strip()
        if not text:
            print("[WARN] No se proporciono texto.")
            pause()
            return
        args = [sys.executable, str(script_path), text, "--explain"]
        subprocess.run(args, cwd=REPO_ROOT)
    elif choice == "2":
        args = [sys.executable, str(script_path), "--list-rules"]
        subprocess.run(args, cwd=REPO_ROOT)
    elif choice == "3":
        args = [sys.executable, str(script_path), "--list-agents"]
        subprocess.run(args, cwd=REPO_ROOT)

    pause()


def menu_orchestrator_agent():
    print("\n🤖 Orquestador Inteligente\n")
    script_path = (
        REPO_ROOT / "agents" / "core" / "orchestrator" / "scripts" / "orchestrate.py"
    )
    if not script_path.exists():
        print("[ERROR] No se encontro agents/core/orchestrator/scripts/orchestrate.py")
        pause()
        return

    print("  1. Ejecutar orquestacion (Input)")
    print("  2. Ver logs recientes")
    print("  0. Volver")
    choice = prompt_choice("\nSelecciona: ", {"0", "1", "2"})
    if choice == "0":
        return

    if choice == "1":
        text = input("\nTarea compleja a orquestar: ").strip()
        if not text:
            print("[WARN] No se proporciono texto.")
            pause()
            return
        args = [sys.executable, str(script_path), text]
        subprocess.run(args, cwd=REPO_ROOT)
    elif choice == "2":
        log_dir = REPO_ROOT / "logs" / "orchestrator"
        if log_dir.exists():
            logs = sorted(log_dir.glob("*.jsonl"))
            if logs:
                print(f"\nUltimo log: {logs[-1].name}")
                print(logs[-1].read_text(encoding="utf-8"))
            else:
                print("\nNo hay logs disponibles.")
        else:
            print("\nDirectorio de logs no encontrado.")

    pause()


def menu_update():
    update_script = REPO_ROOT / "scripts" / "update.py"
    if not update_script.exists():
        print("[ERROR] No se encontro scripts/update.py.")
        pause()
        return
    result = subprocess.run([sys.executable, str(update_script)], cwd=REPO_ROOT)
    if result.returncode == 0:
        print("[OK] Actualizacion completada.")
    else:
        print("[WARN] Actualizacion incompleta o cancelada.")
    pause()


def get_active_model_cli():
    if MODELS_PATH.exists():
        content = load_models_content()
        if content.strip():
            primary, _ = parse_active_models(content)
            models = parse_catalog(content) or DEFAULT_MODELS
            for model in models:
                if model["id"] == primary:
                    return primary, model["cli"]
            return primary, None
    return None, None


def load_default_cli():
    profile_path = REPO_ROOT / ".context" / "profile.md"
    if not profile_path.exists():
        return None
    for line in profile_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- **CLI default**:"):
            value = line.split(":", 1)[1].strip()
            return value if value and value != "N/D" else None
    return None


def show_magic_prompt(cli=None):
    context_map = {
        "opencode": ".context/opencode.md",
        "claude": ".context/claude.md",
        "gemini": ".context/gemini.md",
        "codex": ".context/agents.md",
    }
    cli_key = cli or ""
    context_file = context_map.get(cli_key, ".context/MASTER.md")
    prompt_text = t(
        "launcher.prompt", "Lee {context} e inicia la sesion.", context=context_file
    )
    print(
        "\n" + t("launcher.magic", "Copia esto en tu IA: {prompt}", prompt=prompt_text)
    )
    pause()


def list_cli_options():
    for idx, cli in enumerate(CLI_LABELS.keys(), start=1):
        label = CLI_LABELS[cli]
        detected = shutil.which(cli) is not None
        status = "✅" if detected else "⚠️"
        print(f"  {idx}. {status} {label} ({cli})")


def select_cli():
    cli_list = list(CLI_LABELS.keys())
    list_cli_options()
    choice = prompt_choice(
        "\nSelecciona: ", {str(i) for i in range(1, len(cli_list) + 1)}
    )
    return cli_list[int(choice) - 1]


def launch_cli(cli):
    if not cli:
        print("[WARN] No se encontro CLI para el modelo seleccionado.")
        pause()
        return
    executable = shutil.which(cli)
    if executable is None:
        if not prompt_yes_no(
            f"CLI '{cli}' no detectada. Intentar ejecutar de todos modos?"
        ):
            return
        executable = cli
    print(f"[INFO] Lanzando {cli}...")
    try:
        if os.name == "nt" and str(executable).lower().endswith((".cmd", ".bat")):
            subprocess.run(str(executable), check=False, shell=True)
        else:
            subprocess.run([str(executable)], check=False)
    except FileNotFoundError:
        print(f"[ERROR] No se pudo ejecutar '{cli}'. Verifica que este en PATH.")
        pause()


def menu_launcher():
    while True:
        clear_screen()
        print("-- 🚀 " + t("menu.option.launch", "Iniciar Sesion AI") + " --")
        model_id, model_cli = get_active_model_cli()
        default_cli = load_default_cli()
        if model_id:
            print(
                t(
                    "launcher.model.active",
                    "Modelo activo: {model} (CLI: {cli})",
                    model=model_id,
                    cli=model_cli or "N/D",
                )
            )
        else:
            print(
                t(
                    "launcher.model.none",
                    "Modelo activo: N/D (orquestacion no activada)",
                )
            )
            if default_cli:
                print(
                    t("launcher.default.cli", "CLI por defecto: {cli}", cli=default_cli)
                )

        valid_choices = {"0", "2"}
        print("\n  2. 📝 " + t("launcher.option.manual", "Elegir otra CLI manualmente"))
        if model_id:
            print("  1. ▶️  " + t("launcher.option.active", "Iniciar con modelo activo"))
            valid_choices.add("1")
        elif default_cli:
            print(
                "  1. ▶️  " + t("launcher.option.default", "Iniciar con CLI por defecto")
            )
            valid_choices.add("1")
        print("  0. ⬅️  " + t("launcher.option.back", "Volver"))

        prompt_range = "0-2" if "1" in valid_choices else "0-2"
        choice = prompt_choice(
            t("menu.prompt", "\nSelecciona una opcion [{range}]: ", range=prompt_range),
            valid_choices,
        )
        if choice == "0":
            return
        if choice == "1":
            selected_cli = model_cli if model_id else default_cli
            show_magic_prompt(selected_cli)
            if model_id:
                if not model_cli:
                    print("[WARN] No hay CLI asociada al modelo activo.")
                    pause()
                    continue
                launch_cli(model_cli)
            elif default_cli:
                launch_cli(default_cli)
        elif choice == "2":
            print("\nCLIs disponibles:")
            cli = select_cli()
            show_magic_prompt(cli)
            launch_cli(cli)


def check_maintenance_tasks():
    """BL-047: TaskManager para programar mantenimiento cada 30 dias."""
    maint_file = REPO_ROOT / ".context" / ".last_maint"
    now = datetime.now()
    should_run = False
    
    if not maint_file.exists():
        should_run = True
    else:
        try:
            last_maint_str = maint_file.read_text(encoding="utf-8").strip()
            last_maint = datetime.fromisoformat(last_maint_str)
            if now - last_maint > timedelta(days=30):
                should_run = True
        except Exception:
            should_run = True
            
    if should_run:
        print("\n" + t("diag.maint.running", "🛠️ Ejecutando mantenimiento programado (cada 30 dias)..."))
        # Clean snapshots older than 30 days
        run_context_version(["clean", "--older", "30"])
        # Export a full backup
        run_context_version(["export"])
        # Update timestamp
        maint_file.write_text(now.isoformat(), encoding="utf-8")
        print(t("diag.maint.ok", "[OK] Mantenimiento completado."))


def run_diagnostics():
    print(t("diag.running", "Ejecutando diagnostico pre-arranque..."))
    # Check Context Integrity
    if run_context_validate():
        print(t("diag.context.ok", "[OK] Integridad de contexto validada."))
    else:
        print(t("diag.context.fail", "[WARN] Errores en integridad de contexto."))
    
    # Run Scheduled Maintenance
    check_maintenance_tasks()
    
    # Check Git Status (if applicable)
    if (REPO_ROOT / ".git").exists():
        res = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True, text=True)
        if res.stdout.strip():
            print(t("diag.git.dirty", "[INFO] Tienes cambios locales pendientes en Git."))
        else:
            print(t("diag.git.clean", "[OK] Repositorio limpio."))

def main_menu(feature_mode=False):
    # Auto-Run Diagnostics and Sync on Startup
    run_diagnostics()
    print(t("sync.running", "Sincronizando contexto..."))
    if run_sync_context():
        print(t("sync.ok", "[OK] Contexto sincronizado."))
    else:
        print(t("sync.fail", "[WARN] Fallo sincronizacion automatica."))
    time.sleep(1) # Brief pause to read status

    while True:
        # clear_screen() <- Quitamos o comentamos para la primera iteracion si queremos persistencia
        print_header()
        if feature_mode:
            print(
                "         🚀 "
                + t("menu.feature.banner", "Feature Session Mode Active")
                + " 🚀"
            )
            print("───────────────────────────────────────────────────────")

        print("\n  1. 🔄 " + t("menu.option.sync", "Sincronizar Contexto"))
        print(
            "  2. ⚙️  "
            + t("menu.option.profile", "Configurar Perfil (Idioma, Enfoque, Estilo)")
        )
        print("  3. 🎛️  " + t("menu.option.orchestration", "Orquestacion Multi-Modelo"))
        print("  4. 📊 " + t("menu.option.health", "Estado del Sistema"))
        print("  5. 🚀 " + t("menu.option.launch", "Iniciar Sesion AI"))
        print("  6. 📁 " + t("menu.option.context", "Gestion de Contexto"))
        print("  7. 🔄 " + t("menu.option.update", "Buscar actualizaciones"))
        print("  8. 🧭 " + t("menu.option.decision", "Decision Engine"))
        print("  9. 🤖 " + t("menu.option.orchestrator", "Orquestador Inteligente"))
        print("  11. 🖥️  " + t("menu.option.server", "Iniciar Servidor Dashboard"))
        if feature_mode:
            print("  10. 📋 " + t("menu.option.backlog", "Ver Backlog"))
        print("  0. 🚪 " + t("menu.option.exit", "Salir"))

        valid_choices = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "11"}
        if feature_mode:
            valid_choices.add("10")

        prompt_range = "0-11" if feature_mode else "0-11"
        choice = prompt_choice(
            t("menu.prompt", "\nSelecciona una opcion [{range}]: ", range=prompt_range),
            valid_choices,
        )
        if choice == "0":
            return
        if choice == "11":
             subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "server.py")])
        if choice == "1":
            menu_sync()
        elif choice == "2":
            menu_profile()
        elif choice == "3":
            menu_orchestration()
        elif choice == "4":
            menu_health()
        elif choice == "5":
            menu_launcher()
        elif choice == "6":
            menu_context_management()
        elif choice == "7":
            menu_update()
        elif choice == "8":
            menu_decision_engine()
        elif choice == "9":
            menu_orchestrator_agent()
        elif choice == "10" and feature_mode:
            menu_backlog()


def main():
    parser = argparse.ArgumentParser(
        description="Personal Assistant Framework Control Panel"
    )
    parser.add_argument(
        "--feature",
        action="store_true",
        help="Activar modo de sesion de caracteristicas (Feature Session)",
    )
    args = parser.parse_args()

    init_repo_root()
    setup_unicode()
    main_menu(feature_mode=args.feature)


if __name__ == "__main__":
    main()
