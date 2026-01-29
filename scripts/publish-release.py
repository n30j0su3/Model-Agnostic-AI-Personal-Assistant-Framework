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
        print("[ERROR] Hay cambios sin commit. Haz commit o stash antes de publicar.")
        return False
    return True


def branch_exists(branch):
    result = run_git(["show-ref", "--verify", f"refs/heads/{branch}"], check=False)
    return result.returncode == 0


def checkout(branch):
    run_git(["checkout", branch])


def protect_paths(public_head, paths):
    for path in paths:
        check = run_git(["ls-tree", "-r", public_head, "--name-only", path], check=False, capture_output=True)
        if check.stdout.strip():
            run_git(["checkout", public_head, "--", path], check=False)

def delete_paths(paths):
    for path in paths:
        # If it's a file, remove it from index. If it's a directory, remove recursively.
        if Path(path).is_dir():
            run_git(["rm", "-rf", "--cached", path], check=False)
        else:
            run_git(["rm", "--cached", path], check=False)


def has_staged_changes():
    result = run_git(["diff", "--cached", "--quiet"], check=False)
    return result.returncode != 0


def main():
    parser = argparse.ArgumentParser(
        description="Publish sanitized changes to public-release"
    )
    parser.add_argument(
        "--private-branch",
        default="main",
        help="Rama privada con el desarrollo completo (default: main)",
    )
    parser.add_argument(
        "--public-branch",
        default="public-release",
        help="Rama publica limpia (default: public-release)",
    )
    parser.add_argument(
        "--public-remote",
        default="upstream",
        help="Remote publico (default: upstream)",
    )
    parser.add_argument(
        "--message",
        default="release: publish sanitized update",
        help="Mensaje de commit para la publicacion",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Hacer push automatico a remoto publico",
    )
    args = parser.parse_args()

    if not ensure_clean():
        return 1

    if not branch_exists(args.private_branch):
        print(f"[ERROR] Rama privada no encontrada: {args.private_branch}")
        return 1
    if not branch_exists(args.public_branch):
        print(f"[ERROR] Rama publica no encontrada: {args.public_branch}")
        return 1

    original_branch = git_output(["rev-parse", "--abbrev-ref", "HEAD"])
    public_head = git_output(["rev-parse", args.public_branch])

    checkout(args.public_branch)

    merge = run_git(
        ["merge", "--no-ff", "--no-commit", args.private_branch], check=False
    )
    if merge.returncode != 0:
        print("[ERROR] Merge fallido. Resuelve conflictos y vuelve a intentar.")
        run_git(["merge", "--abort"], check=False)
        if original_branch != args.public_branch:
            checkout(original_branch)
        return 1

    protect_paths(
        public_head,
        [
            "docs/backlog.md",
            "docs/backlog.view.md",
            "sessions",
        ],
    )

    delete_paths(
        [
            "dev.bat",
            "dev.sh",
            "docs/workflow/dev-workflow.md",
            "scripts/publish-release.py",
            ".context/DEV_ENVIRONMENT.md",
        ],
    )

    if not has_staged_changes():
        print("[INFO] No hay cambios para publicar.")
        if original_branch != args.public_branch:
            checkout(original_branch)
        return 0

    run_git(["commit", "-m", args.message])

    if args.push:
        run_git(["push", args.public_remote, args.public_branch])

    if original_branch != args.public_branch:
        checkout(original_branch)

    print("[OK] Publicacion completada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
