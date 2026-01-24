#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
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

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_LABELS = {
    "opencode": "OpenCode",
    "claude": "Claude",
    "gemini": "Gemini",
    "codex": "Codex",
    "ollama": "Ollama",
}


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
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("╔═══════════════════════════════════════════════════════╗")
    print("║   Personal Assistant Framework - Control Panel        ║")
    print("╚═══════════════════════════════════════════════════════╝")


def pause(message="Presiona Enter para continuar..."):
    input(f"\n{message}")


def prompt_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("[WARN] Opcion invalida. Intenta de nuevo.")


def prompt_yes_no(message, default=False):
    suffix = "[s/N]" if not default else "[S/n]"
    choice = input(f"{message} {suffix}: ").strip().lower()
    if not choice:
        return default
    return choice in {"s", "si", "y", "yes"}


def run_sync_context():
    sync_script = REPO_ROOT / "scripts" / "sync-context.py"
    if not sync_script.exists():
        print("[ERROR] No se encontro scripts/sync-context.py.")
        return False
    result = subprocess.run([sys.executable, str(sync_script)], cwd=REPO_ROOT)
    return result.returncode == 0


def run_context_version(args):
    script_path = REPO_ROOT / "scripts" / "context-version.py"
    if not script_path.exists():
        print("[ERROR] No se encontro scripts/context-version.py.")
        return False
    result = subprocess.run([sys.executable, str(script_path), *args], cwd=REPO_ROOT)
    return result.returncode == 0


def run_context_validate():
    script_path = REPO_ROOT / "scripts" / "context-validate.py"
    if not script_path.exists():
        print("[ERROR] No se encontro scripts/context-validate.py.")
        return False
    result = subprocess.run([sys.executable, str(script_path)], cwd=REPO_ROOT)
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
    print("\nEsta opcion es opcional y no reemplaza la configuracion nativa de cada terminal.")
    print("Sirve como punto central para cambiar modelos rapidamente con .context/models.md.")
    print("Si prefieres usar cada terminal con su configuracion propia, puedes ignorarla.")


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
                if prompt_yes_no("Restaurar snapshot y sobrescribir archivos actuales?"):
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


def list_cli_options():
    for idx, cli in enumerate(CLI_LABELS.keys(), start=1):
        label = CLI_LABELS[cli]
        detected = shutil.which(cli) is not None
        status = "✅" if detected else "⚠️"
        print(f"  {idx}. {status} {label} ({cli})")


def select_cli():
    cli_list = list(CLI_LABELS.keys())
    list_cli_options()
    choice = prompt_choice("\nSelecciona: ", {str(i) for i in range(1, len(cli_list) + 1)})
    return cli_list[int(choice) - 1]


def launch_cli(cli):
    if not cli:
        print("[WARN] No se encontro CLI para el modelo seleccionado.")
        pause()
        return
    executable = shutil.which(cli)
    if executable is None:
        if not prompt_yes_no(f"CLI '{cli}' no detectada. Intentar ejecutar de todos modos?"):
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
        print("-- 🚀 Iniciar Sesion AI --")
        model_id, model_cli = get_active_model_cli()
        if model_id:
            print(f"Modelo activo: {model_id} (CLI: {model_cli or 'N/D'})")
        else:
            print("Modelo activo: N/D (orquestacion no activada)")
        print("\n  1. ▶️  Iniciar con modelo activo")
        print("  2. 📝 Elegir otra CLI manualmente")
        print("  0. ⬅️  Volver")
        choice = prompt_choice("\nSelecciona: ", {"0", "1", "2"})
        if choice == "0":
            return
        if choice == "1":
            if not model_cli:
                print("[WARN] No hay CLI asociada al modelo activo.")
                pause()
                continue
            launch_cli(model_cli)
        elif choice == "2":
            print("\nCLIs disponibles:")
            cli = select_cli()
            launch_cli(cli)


def main_menu(feature_mode=False):
    while True:
        clear_screen()
        print_header()
        if feature_mode:
            print("         🚀 Feature Session Mode Active 🚀")
            print("───────────────────────────────────────────────────────")
        
        print("\n  1. 🔄 Sincronizar Contexto")
        print("  2. ⚙️  Configurar Perfil (Idioma, Enfoque, Estilo)")
        print("  3. 🎛️  Orquestacion Multi-Modelo")
        print("  4. 📊 Estado del Sistema")
        print("  5. 🚀 Iniciar Sesion AI")
        print("  6. 📁 Gestion de Contexto")
        print("  7. 🔄 Buscar actualizaciones")
        if feature_mode:
            print("  8. 📋 Ver Backlog")
        print("  0. 🚪 Salir")

        valid_choices = {"0", "1", "2", "3", "4", "5", "6", "7"}
        if feature_mode:
            valid_choices.add("8")

        prompt_range = "0-8" if feature_mode else "0-7"
        choice = prompt_choice(
            f"\nSelecciona una opcion [{prompt_range}]: ",
            valid_choices,
        )
        if choice == "0":
            return
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
        elif choice == "8" and feature_mode:
            menu_backlog()


def main():
    parser = argparse.ArgumentParser(description="Personal Assistant Framework Control Panel")
    parser.add_argument("--feature", action="store_true", help="Activar modo de sesion de caracteristicas (Feature Session)")
    args = parser.parse_args()

    init_repo_root()
    setup_unicode()
    main_menu(feature_mode=args.feature)


if __name__ == "__main__":
    main()
