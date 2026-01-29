#!/usr/bin/env python3
import getpass
import json
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path

from i18n import get_translator


GITHUB_API = "https://api.github.com"
DEFAULT_VISIBILITY_PRIVATE = True
DEFAULT_REPO_NAME = "personal-assistant-framework"
OFFICIAL_UPSTREAM = (
    "https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git"
)
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
sessions/
logs/
workspaces/
.context/
"""


def run_cmd(args, cwd=None, capture_output=False):
    return subprocess.run(
        args,
        cwd=cwd,
        capture_output=capture_output,
        text=capture_output,
        check=False,
    )


def get_env_token():
    return os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN") or ""


def prompt_github_token(t):
    token = get_env_token()
    if token:
        return token
    print(
        t(
            "repo.token.info",
            "[INFO] Ingresa un token de GitHub con scope 'repo' si no usas gh CLI.",
        )
    )
    return getpass.getpass("GitHub Token: ").strip()


def get_remote_url(repo_root, remote_name):
    result = run_cmd(
        ["git", "remote", "get-url", remote_name], cwd=repo_root, capture_output=True
    )
    if result.returncode != 0:
        return ""
    return (result.stdout or "").strip()


def has_git():
    return shutil.which("git") is not None


def has_gh():
    return shutil.which("gh") is not None


def gh_authenticated():
    if not has_gh():
        return False
    result = run_cmd(
        ["gh", "auth", "status", "--hostname", "github.com"], capture_output=True
    )
    return result.returncode == 0


def git_global_configured():
    name = run_cmd(
        ["git", "config", "--global", "user.name"], capture_output=True
    ).stdout.strip()
    email = run_cmd(
        ["git", "config", "--global", "user.email"], capture_output=True
    ).stdout.strip()
    return bool(name or email)


def pygithub_available():
    try:
        import github  # type: ignore[import-not-found]

        return True
    except Exception:
        return False


def ensure_gitignore(repo_root):
    gitignore_path = repo_root / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(GITIGNORE_TEMPLATE, encoding="utf-8")
    else:
        content = gitignore_path.read_text(encoding="utf-8")
        criticals = ["sessions/", "logs/", "workspaces/"]
        changed = False
        for c in criticals:
            if c not in content:
                content += f"\n{c}"
                changed = True
        if changed:
            gitignore_path.write_text(content, encoding="utf-8")


def ensure_initial_commit(repo_root, t):
    if not has_git():
        print(t("repo.git.missing", "[WARN] Git no esta disponible."))
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
        print(
            t(
                "repo.commit.warn",
                "[WARN] No se pudo crear el commit inicial. Revisa tu configuracion de Git.",
            )
        )
        return False
    return True


def prompt_choice(
    prompt, options, invalid_message="[WARN] Opcion invalida. Intenta de nuevo."
):
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(invalid_message)


def prompt_yes_no(message, default=False, language="es"):
    suffix = "[s/N]" if language == "es" else "[y/N]"
    if default:
        suffix = "[S/n]" if language == "es" else "[Y/n]"
    choice = input(f"{message} {suffix}: ").strip().lower()
    if not choice:
        return default
    return choice in {"s", "si", "y", "yes"}


def create_repo_gh(repo_root, repo_name, private, t):
    if not gh_authenticated():
        return False
    if not ensure_initial_commit(repo_root, t):
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


def create_repo_pygithub(token, repo_name, private, t):
    try:
        from github import Github
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


def create_repo_api(token, repo_name, private, t):
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


def ensure_remote(repo_root, clone_url, remote_name="origin"):
    existing = run_cmd(
        ["git", "remote", "get-url", remote_name], cwd=repo_root, capture_output=True
    )
    if existing.returncode == 0:
        run_cmd(["git", "remote", "set-url", remote_name, clone_url], cwd=repo_root)
        return
    run_cmd(["git", "remote", "add", remote_name, clone_url], cwd=repo_root)


def prompt_private_repo_url(t):
    prompt = t("repo.private.url", "URL del repo privado (https://... o git@...): ")
    return input(prompt).strip()


def configure_private_remote(repo_root, t):
    print(t("repo.private.title", "\nConfigurar repo privado (origin)"))
    print(t("repo.private.create", "  1. Crear repo privado en GitHub"))
    print(t("repo.private.use", "  2. Usar URL de repo privado existente"))
    print(t("repo.private.skip", "  3. Omitir por ahora"))

    choice = prompt_choice(
        t("repo.private.prompt", "\nSelecciona [1-3]: "),
        {"1", "2", "3"},
    )

    if choice == "1":
        repo_name = prompt_repo_name(repo_root, t)
        return create_repo_remote(repo_root, repo_name, True, t)

    if choice == "2":
        url = prompt_private_repo_url(t)
        if not url:
            print(t("repo.private.empty", "[WARN] No se proporciono URL."))
            return False
        if not ensure_initial_commit(repo_root, t):
            return False
        ensure_remote(repo_root, url, "origin")
        push_main(repo_root, t, "origin")
        return True

    return False


def push_main(repo_root, t, remote_name="origin"):
    run_cmd(["git", "branch", "-M", "main"], cwd=repo_root)
    push = run_cmd(["git", "push", "-u", remote_name, "main"], cwd=repo_root)
    if push.returncode != 0:
        print(t("repo.push.warn", f"[WARN] No se pudo subir el repo a {remote_name}."))


def create_repo_remote(repo_root, repo_name, private, t):
    if gh_authenticated():
        return create_repo_gh(repo_root, repo_name, private, t)

    token = prompt_github_token(t)
    if not token:
        print(
            t(
                "repo.token.missing",
                "[WARN] Token no proporcionado. Se omite la creacion remota.",
            )
        )
        return False

    if not ensure_initial_commit(repo_root, t):
        return False

    clone_url = ""
    if pygithub_available():
        clone_url = create_repo_pygithub(token, repo_name, private, t)
    if not clone_url:
        clone_url = create_repo_api(token, repo_name, private, t)
    if not clone_url:
        return False

    ensure_remote(repo_root, clone_url, "origin")
    push_main(repo_root, t, "origin")
    return True


def prompt_repo_name(repo_root, t):
    default_name = repo_root.name or DEFAULT_REPO_NAME
    prompt = t(
        "repo.name.prompt", "Nombre del repositorio [{name}]: ", name=default_name
    )
    repo_name = input(prompt).strip()
    return repo_name or default_name


def setup_hybrid_upstream(repo_root, t):
    print(
        t(
            "repo.upstream.info",
            "\n[INFO] Configurando 'upstream' para recibir actualizaciones del Framework...",
        )
    )
    ensure_remote(repo_root, OFFICIAL_UPSTREAM, "upstream")
    print(
        t("repo.upstream.ok", "[OK] Upstream configurado: {url}", url=OFFICIAL_UPSTREAM)
    )


def configure_existing_repo(repo_root, t):
    upstream_url = get_remote_url(repo_root, "upstream")
    if not upstream_url:
        if prompt_yes_no(
            t("repo.upstream.ask", "Configurar upstream publico ahora?"), default=True
        ):
            setup_hybrid_upstream(repo_root, t)

    origin_url = get_remote_url(repo_root, "origin")
    if not origin_url:
        if prompt_yes_no(
            t("repo.private.ask", "Configurar repo privado (origin) ahora?"),
            default=True,
        ):
            configure_private_remote(repo_root, t)


def setup_repository(repo_root, translator=None):
    from i18n import get_translator

    repo_root = Path(repo_root)
    translator = translator or get_translator(repo_root)
    t = translator.t

    if not has_git():
        print(t("repo.git.missing", "[WARN] Git no esta disponible."))
        return
    if not git_global_configured():
        print(
            t(
                "repo.git.config",
                "[WARN] Git no esta configurado. Configura user.name/user.email y reintenta.",
            )
        )
        return

    if (repo_root / ".git").exists():
        configure_existing_repo(repo_root, t)
        return

    print(t("repo.not_detected", "\nRepositorio no detectado."))
    print(t("repo.mode.title", "Selecciona el modo de inicio:"))
    print(
        t("repo.mode.hybrid", "  1. Hibrido (Privado + Upstream Publico) [Recomendado]")
    )
    print(t("repo.mode.github", "  2. Privado Standalone (Solo Backup)"))
    print(t("repo.mode.local", "  3. Local (Solo historial, sin Nube)"))
    print(t("repo.mode.sandbox", "  4. Sandbox (Sin Git)"))

    choice = prompt_choice(
        t("repo.mode.prompt", "\nSelecciona [1-4]: "), {"1", "2", "3", "4"}
    )

    if choice == "1":
        repo_name = prompt_repo_name(repo_root, t)
        if not create_repo_remote(repo_root, repo_name, True, t):
            configure_private_remote(repo_root, t)
        setup_hybrid_upstream(repo_root, t)
    elif choice == "2":
        repo_name = prompt_repo_name(repo_root, t)
        if not create_repo_remote(repo_root, repo_name, True, t):
            configure_private_remote(repo_root, t)
        if prompt_yes_no(
            t("repo.upstream.ask", "Configurar upstream publico ahora?"), default=True
        ):
            setup_hybrid_upstream(repo_root, t)
    elif choice == "3":
        ensure_initial_commit(repo_root, t)
    else:
        ensure_gitignore(repo_root)


def main():
    repo_root = Path(__file__).resolve().parents[1]
    setup_repository(repo_root)


if __name__ == "__main__":
    main()
