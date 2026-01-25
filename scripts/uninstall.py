#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def repo_root():
    return Path(__file__).resolve().parents[1]


def path_list(root, names):
    return [root / name for name in names]


def remove_path(path, dry_run=False):
    if not path.exists():
        print(f"[SKIP] No existe: {path}")
        return
    if dry_run:
        print(f"[DRY] Eliminaria: {path}")
        return
    try:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        print(f"[OK] Eliminado: {path}")
    except Exception as exc:
        print(f"[WARN] No se pudo eliminar {path}: {exc}")


def prompt_choice(prompt, options):
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print("[WARN] Opcion invalida. Intenta de nuevo.")


def prompt_yes_no(message, default=False):
    suffix = "[s/N]" if not default else "[S/n]"
    choice = input(f"{message} {suffix}: ").strip().lower()
    if not choice:
        return default
    return choice in {"s", "si", "y", "yes"}


def require_confirm_phrase(phrase):
    value = input(f"Escribe '{phrase}' para continuar: ").strip()
    return value == phrase


def uninstall_opencode(dry_run=False):
    if shutil.which("npm") is None:
        print("[WARN] npm no detectado. No se puede desinstalar OpenCode automaticamente.")
        return
    if dry_run:
        print("[DRY] Ejecutaria: npm uninstall -g @anthropic-ai/opencode")
        return
    cmd = ["npm", "uninstall", "-g", "@anthropic-ai/opencode"]
    if sys.platform.startswith("win"):
        npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
        if npm_cmd:
            cmd[0] = npm_cmd
            result = subprocess.run(cmd, check=False)
        else:
            result = subprocess.run("npm uninstall -g @anthropic-ai/opencode", shell=True, check=False)
    else:
        result = subprocess.run(cmd, check=False)
    if result.returncode == 0:
        print("[OK] OpenCode desinstalado.")
    else:
        print("[WARN] No se pudo desinstalar OpenCode. Puedes hacerlo manualmente.")


def main():
    parser = argparse.ArgumentParser(description="Desinstalador del Personal Assistant Framework")
    parser.add_argument("--mode", choices=["complete", "reset", "system"], help="Modo de desinstalacion")
    parser.add_argument("--yes", action="store_true", help="Omitir confirmaciones")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar lo que se eliminaria")
    parser.add_argument("--remove-git", action="store_true", help="Eliminar .git (solo modo complete)")
    parser.add_argument("--remove-opencode", action="store_true", help="Desinstalar OpenCode global (npm)")
    args = parser.parse_args()

    root = repo_root()

    config_paths = [".context", "sessions"]
    data_paths = ["workspaces", "logs"]
    cache_paths = [".opencode", ".claude", ".gemini", ".codex", "opencode.jsonc"]

    if not args.mode:
        print("\nDesinstalador del Framework")
        print("  1. Completo (configuracion + datos + caches)")
        print("  2. Reset de configuracion (solo contexto y sesiones)")
        print("  3. Limpieza de sistema (solo caches de herramientas)")
        print("  4. Salir")
        selection = prompt_choice("Selecciona [1-4]: ", {"1", "2", "3", "4"})
        if selection == "4":
            print("[INFO] Cancelado.")
            return
        args.mode = {"1": "complete", "2": "reset", "3": "system"}[selection]

    if args.mode == "reset":
        targets = config_paths
    elif args.mode == "system":
        targets = cache_paths
    else:
        targets = config_paths + data_paths + cache_paths

    targets = path_list(root, targets)
    if args.mode == "complete" and args.remove_git:
        targets.append(root / ".git")

    print("\nSe eliminaran las siguientes rutas:")
    for path in targets:
        print(f"- {path}")

    if not args.yes:
        print("\n[WARN] Esta accion es potencialmente irreversible.")
        if args.mode == "complete":
            if not require_confirm_phrase("ELIMINAR"):
                print("[INFO] Cancelado.")
                return
        else:
            if not prompt_yes_no("Confirmas la desinstalacion?"):
                print("[INFO] Cancelado.")
                return

    for path in targets:
        remove_path(path, dry_run=args.dry_run)

    if args.remove_opencode:
        uninstall_opencode(dry_run=args.dry_run)
    elif args.mode in {"complete", "system"} and not args.yes:
        if prompt_yes_no("Deseas desinstalar OpenCode (npm -g)?", default=False):
            uninstall_opencode(dry_run=args.dry_run)

    print("\n[OK] Proceso finalizado.")
    if args.mode == "complete":
        print("[INFO] Para eliminar el framework por completo, borra la carpeta del proyecto.")


if __name__ == "__main__":
    main()
