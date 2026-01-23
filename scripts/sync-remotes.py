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
        print("[ERROR] Hay cambios sin commit. Haz commit o stash antes de sincronizar.")
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
    parser.add_argument("--private-remote", default="private", help="Nombre del remote privado")
    parser.add_argument("--private-url", help="URL del remote privado si no existe")
    parser.add_argument("--main-branch", default="main", help="Nombre de la rama principal")
    parser.add_argument(
        "--no-private-context",
        action="store_true",
        help="No sincronizar la rama private-context",
    )
    args = parser.parse_args()

    if not ensure_clean():
        return 1

    original_branch = current_branch()
    if original_branch != args.main_branch:
        checkout(args.main_branch)

    if not ensure_remote(args.private_remote, args.private_url):
        return 1

    push_branch("origin", args.main_branch)
    push_branch(args.private_remote, args.main_branch)

    if not args.no_private_context:
        private_branch = "private-context"
        if not branch_exists(private_branch):
            run_git(["checkout", "-b", private_branch])
        merge_main_into_private(args.main_branch, private_branch)
        push_branch(args.private_remote, private_branch)

    if current_branch() != original_branch:
        checkout(original_branch)

    print("[OK] Sincronizacion completa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
