#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_git(args, check=True, capture_output=False):
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=check,
        text=True,
        capture_output=capture_output,
    )
    return result


def git_output(args):
    return run_git(args, capture_output=True).stdout.strip()


def ensure_clean():
    status = git_output(["status", "--porcelain"])
    if status:
        print(
            "[ERROR] Hay cambios sin commit. Haz commit o stash antes de sincronizar."
        )
        return False
    return True


def remote_exists(name):
    remotes = git_output(["remote"]).splitlines()
    return name in remotes


def ensure_remote(name, url):
    if remote_exists(name):
        return True
    if not url:
        print(f"[ERROR] Remote '{name}' no existe y no se proporciono URL.")
        return False
    run_git(["remote", "add", name, url])
    print(f"[OK] Remote agregado: {name} -> {url}")
    return True


def current_branch():
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"])


def checkout(branch):
    run_git(["checkout", branch])


def branch_exists(branch):
    result = run_git(["show-ref", "--verify", f"refs/heads/{branch}"], check=False)
    return result.returncode == 0


def push_branch(remote, branch):
    run_git(["push", remote, branch])
    print(f"[OK] Push {branch} -> {remote}")


def merge_main_into_private(main_branch, private_branch):
    checkout(private_branch)
    result = run_git(["merge", main_branch, "--no-edit"], check=False)
    if result.returncode != 0:
        print("[ERROR] Merge fallido. Resuelve conflictos y vuelve a intentar.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Sync public and private remotes")
    parser.add_argument(
        "--public-remote", default="upstream", help="Nombre del remote publico"
    )
    parser.add_argument("--public-url", help="URL del remote publico si no existe")
    parser.add_argument(
        "--private-remote", default="origin", help="Nombre del remote privado"
    )
    parser.add_argument("--private-url", help="URL del remote privado si no existe")
    parser.add_argument(
        "--private-branch",
        default=None,
        help="Nombre de la rama privada a sincronizar (default: main)",
    )
    parser.add_argument(
        "--public-branch",
        default="public-release",
        help="Nombre de la rama publica a sincronizar (default: public-release)",
    )
    parser.add_argument(
        "--main-branch",
        default="main",
        help="(Deprecated) Alias de --private-branch",
    )
    parser.add_argument(
        "--allow-public-main",
        action="store_true",
        help="Permite push de main a remoto publico (no recomendado)",
    )
    args = parser.parse_args()

    private_branch = args.private_branch or args.main_branch
    public_branch = args.public_branch

    if not ensure_clean():
        return 1

    if not ensure_remote(args.public_remote, args.public_url):
        return 1
    if not ensure_remote(args.private_remote, args.private_url):
        return 1

    if (
        args.public_remote == "upstream"
        and public_branch == "main"
        and not args.allow_public_main
    ):
        print(
            "[ERROR] Bloqueado: no se permite push de main a upstream. "
            "Usa public-release o --allow-public-main."
        )
        return 1

    if not branch_exists(private_branch):
        print(f"[ERROR] Rama privada no encontrada: {private_branch}")
        return 1
    if not branch_exists(public_branch):
        print(f"[ERROR] Rama publica no encontrada: {public_branch}")
        return 1

    original_branch = current_branch()
    if original_branch != private_branch:
        checkout(private_branch)
    push_branch(args.private_remote, private_branch)

    if public_branch != private_branch:
        checkout(public_branch)
    push_branch(args.public_remote, public_branch)

    if current_branch() != original_branch:
        checkout(original_branch)

    print("[OK] Sincronizacion completa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
