#!/usr/bin/env python3
import getpass
import json
import shutil
import subprocess
import urllib.request
from pathlib import Path


GITHUB_API = "https://api.github.com"
DEFAULT_VISIBILITY_PRIVATE = True
DEFAULT_REPO_NAME = "personal-assistant-framework"
GITIGNORE_TEMPLATE = """# ignore
.env
node_modules/
__pycache__/
*.log
.claude/
.gemini/
.codex/
.opencode/package-lock.json
.opencode/run-quota.ts
.opencode/temp-quota/
"""


def run_cmd(args, cwd=None, capture_output=False):
    return subprocess.run(
        args,
        cwd=cwd,
        capture_output=capture_output,
        text=capture_output,
        check=False,
    )


def has_git():
    return shutil.which("git") is not None


def has_gh():
    return shutil.which("gh") is not None


def gh_authenticated():
    if not has_gh():
        return False
    result = run_cmd(["gh", "auth", "status", "--hostname", "github.com"], capture_output=True)
    return result.returncode == 0


def git_global_configured():
    name = run_cmd(["git", "config", "--global", "user.name"], capture_output=True).stdout.strip()
    email = run_cmd(["git", "config", "--global", "user.email"], capture_output=True).stdout.strip()
    return bool(name or email)


def pygithub_available():
    try:
        import github  # type: ignore[import-not-found]  # noqa: F401
        return True
    except Exception:
        return False


def ensure_gitignore(repo_root):
    gitignore_path = repo_root / ".gitignore"
    if gitignore_path.exists():
        return
    gitignore_path.write_text(GITIGNORE_TEMPLATE, encoding="utf-8")


def ensure_initial_commit(repo_root):
    if not has_git():
        print("[WARN] Git no esta disponible.")
        return False
    if not (repo_root / ".git").exists():
        run_cmd(["git", "init"], cwd=repo_root)
    ensure_gitignore(repo_root)
    head_check = run_cmd(["git", "rev-parse", "--verify", "HEAD"], cwd=repo_root)
    if head_check.returncode == 0:
        return True
    run_cmd(["git", "add", "."], cwd=repo_root)
    commit = run_cmd(["git", "commit", "-m", "Initial setup"], cwd=repo_root)
    if commit.returncode != 0:
        print("[WARN] No se pudo crear el commit inicial. Revisa tu configuracion de Git.")
        return False
    return True


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


def create_repo_gh(repo_root, repo_name, private):
    if not gh_authenticated():
        return False
    if not ensure_initial_commit(repo_root):
        return False
    visibility = "--private" if private else "--public"
    cmd = [
        "gh",
        "repo",
        "create",
        repo_name,
        visibility,
        "--source=.",
        "--remote=origin",
        "--push",
    ]
    result = run_cmd(cmd, cwd=repo_root)
    return result.returncode == 0


def create_repo_pygithub(token, repo_name, private):
    try:
        from github import Github  # type: ignore[import-not-found]
    except Exception:
        return ""
    client = Github(token)
    try:
        user = client.get_user()
        repo = user.create_repo(repo_name, private=private)
        return repo.clone_url
    except Exception as exc:
        print(f"[ERROR] PyGithub fallo: {exc}")
        return ""


def create_repo_api(token, repo_name, private):
    payload = json.dumps({"name": repo_name, "private": private}).encode("utf-8")
    request = urllib.request.Request(
        f"{GITHUB_API}/user/repos",
        data=payload,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "pa-framework-setup",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data.get("clone_url", "")
    except Exception as exc:
        print(f"[ERROR] API GitHub fallo: {exc}")
        return ""


def ensure_remote(repo_root, clone_url):
    existing = run_cmd(["git", "remote", "get-url", "origin"], cwd=repo_root, capture_output=True)
    if existing.returncode == 0:
        run_cmd(["git", "remote", "set-url", "origin", clone_url], cwd=repo_root)
        return
    run_cmd(["git", "remote", "add", "origin", clone_url], cwd=repo_root)


def push_main(repo_root):
    run_cmd(["git", "branch", "-M", "main"], cwd=repo_root)
    push = run_cmd(["git", "push", "-u", "origin", "main"], cwd=repo_root)
    if push.returncode != 0:
        print("[WARN] No se pudo subir el repo a GitHub. Puedes intentar manualmente.")


def create_repo_remote(repo_root, repo_name, private):
    if gh_authenticated():
        return create_repo_gh(repo_root, repo_name, private)

    token = getpass.getpass("GitHub Token (PAT): ").strip()
    if not token:
        print("[WARN] Token vacio. Se cancela la creacion remota.")
        return False

    clone_url = ""
    if pygithub_available():
        clone_url = create_repo_pygithub(token, repo_name, private)
    if not clone_url:
        clone_url = create_repo_api(token, repo_name, private)
    if not clone_url:
        return False

    if not ensure_initial_commit(repo_root):
        return False
    ensure_remote(repo_root, clone_url)
    push_main(repo_root)
    return True


def prompt_repo_name(repo_root):
    default_name = repo_root.name or DEFAULT_REPO_NAME
    repo_name = input(f"Nombre del repositorio [{default_name}]: ").strip()
    return repo_name or default_name


def setup_repository(repo_root):
    repo_root = Path(repo_root)
    if (repo_root / ".git").exists():
        return
    if not has_git():
        print("[INFO] Git no detectado. Se omite la inicializacion de repositorio.")
        return
    if not git_global_configured():
        print("[INFO] Git global no configurado. Se omite la inicializacion de repositorio.")
        return

    print("\nRepositorio no detectado.")
    print("Selecciona el modo de inicio:")
    print("  1. GitHub (privado + sincronizacion)")
    print("  2. Local (solo historial en Git)")
    print("  3. Sandbox (sin Git, sin cambios extra)")
    choice = prompt_choice("\nSelecciona [1-3]: ", {"1", "2", "3"})

    if choice == "1":
        private = prompt_yes_no("Crear repositorio privado?", default=DEFAULT_VISIBILITY_PRIVATE)
        repo_name = prompt_repo_name(repo_root)
        if create_repo_remote(repo_root, repo_name, private):
            print("[OK] Repositorio creado y sincronizado.")
        else:
            print("[WARN] No se pudo crear el repositorio remoto.")
    elif choice == "2":
        if ensure_initial_commit(repo_root):
            print("[OK] Repositorio local inicializado.")
        else:
            print("[WARN] No se pudo inicializar el repositorio local.")
    else:
        ensure_gitignore(repo_root)
        print("[INFO] Sandbox activo. No se creo repositorio Git.")


def main():
    repo_root = Path(__file__).resolve().parents[1]
    setup_repository(repo_root)


if __name__ == "__main__":
    main()
