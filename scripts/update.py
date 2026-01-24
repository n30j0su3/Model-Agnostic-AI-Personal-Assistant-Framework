#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO = "https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework"
VERSION_PATH = REPO_ROOT / "VERSION"
EXCLUDE_ROOTS = {".context", "sessions", "workspaces", "config", "logs"}
EXCLUDE_SUBPATHS = {("agents", "custom"), ("skills", "custom")}


def parse_version(version_text):
    cleaned = version_text.strip().lstrip("v")
    parts = cleaned.split(".")
    if len(parts) < 3:
        return cleaned, ()
    try:
        return cleaned, tuple(int(part) for part in parts[:3])
    except ValueError:
        return cleaned, ()


def read_local_version():
    if not VERSION_PATH.exists():
        return "", ()
    return parse_version(VERSION_PATH.read_text(encoding="utf-8"))


def normalize_repo_url(url):
    if not url:
        return DEFAULT_REPO
    if url.endswith(".git"):
        url = url[: -len(".git")]
    if url.startswith("git@"):
        try:
            host_repo = url.split("@", 1)[1]
            host, repo = host_repo.split(":", 1)
            return f"https://{host}/{repo}"
        except ValueError:
            return DEFAULT_REPO
    if url.startswith("https://") or url.startswith("http://"):
        return url
    return DEFAULT_REPO


def detect_repo_url():
    if (REPO_ROOT / ".git").exists() and shutil.which("git"):
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return normalize_repo_url(result.stdout.strip())
        except Exception:
            return DEFAULT_REPO
    return DEFAULT_REPO


def build_raw_version_url(repo_url):
    if repo_url.startswith("https://github.com/"):
        path = repo_url.split("https://github.com/", 1)[1].strip("/")
        return f"https://raw.githubusercontent.com/{path}/main/VERSION"
    return f"{repo_url.rstrip('/')}/raw/main/VERSION"


def build_zip_url(repo_url):
    return f"{repo_url.rstrip('/')}/archive/refs/heads/main.zip"


def fetch_remote_version(url):
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            data = response.read().decode("utf-8").strip()
        return parse_version(data)
    except Exception as exc:
        print(f"[ERROR] No se pudo obtener la version remota: {exc}")
        return "", ()


def is_update_available(local_tuple, remote_tuple):
    if not local_tuple or not remote_tuple:
        return False
    return remote_tuple > local_tuple


def prompt_yes_no(message, default=False):
    suffix = "[s/N]" if not default else "[S/n]"
    choice = input(f"{message} {suffix}: ").strip().lower()
    if not choice:
        return default
    return choice in {"s", "si", "y", "yes"}


def create_snapshot():
    script_path = REPO_ROOT / "scripts" / "context-version.py"
    if not script_path.exists():
        return True
    try:
        result = subprocess.run([sys.executable, str(script_path), "snapshot"], cwd=REPO_ROOT)
        return result.returncode == 0
    except Exception as exc:
        print(f"[WARN] No se pudo crear snapshot: {exc}")
        return False


def should_skip(rel_path):
    if not rel_path.parts:
        return False
    if rel_path.parts[0] in EXCLUDE_ROOTS:
        return True
    if len(rel_path.parts) >= 2:
        for excluded in EXCLUDE_SUBPATHS:
            if rel_path.parts[:2] == excluded:
                return True
    return False


def copy_tree(source_root, target_root):
    for root, dirs, files in os.walk(source_root):
        rel_root = Path(root).relative_to(source_root)
        if should_skip(rel_root):
            dirs[:] = []
            continue
        for dirname in list(dirs):
            if should_skip(rel_root / dirname):
                dirs.remove(dirname)
        for filename in files:
            rel_file = rel_root / filename
            if should_skip(rel_file):
                continue
            source_file = Path(root) / filename
            target_file = target_root / rel_file
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target_file)


def update_with_git():
    result = subprocess.run(["git", "pull", "--ff-only"], cwd=REPO_ROOT)
    if result.returncode != 0:
        print("[ERROR] Git pull fallo. Revisa tu repositorio.")
        return False
    return True


def update_with_zip(zip_url):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        zip_path = tmp_path / "update.zip"
        try:
            with urllib.request.urlopen(zip_url, timeout=30) as response:
                zip_path.write_bytes(response.read())
        except Exception as exc:
            print(f"[ERROR] No se pudo descargar el zip: {exc}")
            return False

        try:
            with zipfile.ZipFile(zip_path) as zip_ref:
                zip_ref.extractall(tmp_path)
        except Exception as exc:
            print(f"[ERROR] No se pudo extraer el zip: {exc}")
            return False

        extracted_dirs = [path for path in tmp_path.iterdir() if path.is_dir()]
        if not extracted_dirs:
            print("[ERROR] Zip sin contenido valido.")
            return False
        source_root = extracted_dirs[0]
        copy_tree(source_root, REPO_ROOT)
    return True


def run_update(force=False):
    repo_url = detect_repo_url()
    raw_url = build_raw_version_url(repo_url)
    zip_url = build_zip_url(repo_url)
    local_text, local_tuple = read_local_version()
    remote_text, remote_tuple = fetch_remote_version(raw_url)

    if not remote_text:
        return False

    print(f"[INFO] Version local: {local_text or 'N/D'}")
    print(f"[INFO] Version remota: {remote_text}")

    if not local_tuple:
        print("[WARN] VERSION local no valido o inexistente.")
    if not remote_tuple:
        print("[WARN] VERSION remota no valida.")

    update_available = is_update_available(local_tuple, remote_tuple)
    if not update_available and not force:
        print("[OK] Framework actualizado.")
        return True

    if update_available:
        print("[INFO] Hay una nueva version disponible.")
    if not force and not prompt_yes_no("Actualizar ahora?", default=False):
        print("[INFO] Actualizacion cancelada.")
        return False

    if not create_snapshot():
        if not prompt_yes_no("Continuar sin snapshot?", default=False):
            print("[INFO] Actualizacion cancelada.")
            return False

    if (REPO_ROOT / ".git").exists() and shutil.which("git"):
        print("[INFO] Metodo de actualizacion: Git")
        return update_with_git()

    print("[INFO] Metodo de actualizacion: Descarga directa")
    return update_with_zip(zip_url)


def main():
    parser = argparse.ArgumentParser(description="Actualizador del framework")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Forzar actualizacion aunque versiones coincidan",
    )
    args = parser.parse_args()
    success = run_update(force=args.force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
