#!/usr/bin/env python3
import argparse
import difflib
import shutil
import sys
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTEXT_DIR = REPO_ROOT / ".context"
VERSIONS_DIR = CONTEXT_DIR / "versions"
BACKUPS_DIR = CONTEXT_DIR / "backups"
TIMESTAMP_FMT = "%Y-%m-%d_%H%M%S"
SNAPSHOT_RE = re.compile(r"(\d{4}-\d{2}-\d{2}_\d{6})_(.+)")

TOKEN_CHARS_PER = 4
DELTA_FACTOR = 0.2
PRICE_LOW = 0.01
PRICE_HIGH = 0.03


def ensure_dirs():
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)


def list_context_files():
    if not CONTEXT_DIR.exists():
        return []
    files = []
    for path in CONTEXT_DIR.glob("*.md"):
        if path.name in {".gitkeep"}:
            continue
        files.append(path)
    return sorted(files)


def collect_snapshots():
    snapshots = {}
    if not VERSIONS_DIR.exists():
        return snapshots
    for path in VERSIONS_DIR.iterdir():
        if not path.is_file():
            continue
        match = SNAPSHOT_RE.match(path.name)
        if not match:
            continue
        timestamp = match.group(1)
        snapshots.setdefault(timestamp, []).append(path)
    return snapshots


def human_bytes(size):
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} GB"


def confirm_action(message):
    choice = input(f"{message} [s/N]: ").strip().lower()
    return choice in {"s", "si", "y", "yes"}


def snapshot():
    ensure_dirs()
    files = list_context_files()
    if not files:
        print("[WARN] No hay archivos .md en .context para snapshot.")
        return 1
    timestamp = datetime.now().strftime(TIMESTAMP_FMT)
    for file_path in files:
        dest = VERSIONS_DIR / f"{timestamp}_{file_path.name}"
        shutil.copy2(file_path, dest)
    print(f"[OK] Snapshot creado: {timestamp} ({len(files)} archivos)")
    return 0


def list_snapshots():
    snapshots = collect_snapshots()
    if not snapshots:
        print("[INFO] No hay snapshots disponibles.")
        return 0
    print("[INFO] Snapshots disponibles:")
    for timestamp in sorted(snapshots.keys(), reverse=True):
        files = snapshots[timestamp]
        total_size = sum(f.stat().st_size for f in files)
        print(f"  - {timestamp} ({len(files)} archivos, {human_bytes(total_size)})")
    return 0


def restore_snapshot(timestamp, force=False):
    snapshots = collect_snapshots()
    files = snapshots.get(timestamp)
    if not files:
        print(f"[ERROR] Snapshot '{timestamp}' no encontrado.")
        return 1
    if not force and not confirm_action("Restaurar snapshot y sobrescribir archivos actuales?"):
        print("[INFO] Operacion cancelada.")
        return 0
    for file_path in files:
        match = SNAPSHOT_RE.match(file_path.name)
        if not match:
            continue
        original_name = match.group(2)
        dest = CONTEXT_DIR / original_name
        shutil.copy2(file_path, dest)
    print(f"[OK] Snapshot restaurado: {timestamp}")
    return 0


def diff_snapshot(timestamp):
    snapshots = collect_snapshots()
    files = snapshots.get(timestamp)
    if not files:
        print(f"[ERROR] Snapshot '{timestamp}' no encontrado.")
        return 1
    has_diff = False
    for file_path in sorted(files, key=lambda p: p.name):
        match = SNAPSHOT_RE.match(file_path.name)
        if not match:
            continue
        original_name = match.group(2)
        current_path = CONTEXT_DIR / original_name
        snapshot_text = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
        current_text = []
        if current_path.exists():
            current_text = current_path.read_text(encoding="utf-8", errors="replace").splitlines()
        diff = list(
            difflib.unified_diff(
                current_text,
                snapshot_text,
                fromfile=f"current/{original_name}",
                tofile=f"snapshot/{file_path.name}",
                lineterm="",
            )
        )
        if diff:
            has_diff = True
            print("\n".join(diff))
    if not has_diff:
        print("[INFO] No hay diferencias con el snapshot.")
    return 0


def clean_snapshots(days):
    snapshots = collect_snapshots()
    if not snapshots:
        print("[INFO] No hay snapshots para limpiar.")
        return 0
    cutoff = datetime.now() - timedelta(days=days)
    removed = 0
    for timestamp, files in snapshots.items():
        try:
            snapshot_time = datetime.strptime(timestamp, TIMESTAMP_FMT)
        except ValueError:
            continue
        if snapshot_time < cutoff:
            for file_path in files:
                file_path.unlink(missing_ok=True)
                removed += 1
    print(f"[OK] Snapshots eliminados: {removed} archivos.")
    return 0


def export_backup():
    ensure_dirs()
    timestamp = datetime.now().strftime(TIMESTAMP_FMT)
    backup_path = BACKUPS_DIR / f"context_backup_{timestamp}.zip"
    with zipfile.ZipFile(backup_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in CONTEXT_DIR.rglob("*"):
            if path.is_dir():
                continue
            if BACKUPS_DIR in path.parents:
                continue
            relative = path.relative_to(CONTEXT_DIR)
            archive.write(path, arcname=relative)
    print(f"[OK] Backup creado: {backup_path}")
    return 0


def is_within_context(path):
    try:
        path.resolve().relative_to(CONTEXT_DIR.resolve())
        return True
    except ValueError:
        return False


def import_backup(zip_path, force=False):
    source = Path(zip_path)
    if not source.exists():
        print(f"[ERROR] Backup no encontrado: {zip_path}")
        return 1
    if not force and not confirm_action("Importar backup y sobrescribir archivos existentes?"):
        print("[INFO] Operacion cancelada.")
        return 0
    with zipfile.ZipFile(source, "r") as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            dest_path = CONTEXT_DIR / member.filename
            if not is_within_context(dest_path):
                print(f"[WARN] Ruta ignorada por seguridad: {member.filename}")
                continue
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member, "r") as source_file:
                with open(dest_path, "wb") as target_file:
                    shutil.copyfileobj(source_file, target_file)
    print("[OK] Backup importado.")
    return 0


def stats():
    snapshots = collect_snapshots()
    snapshot_files = [file for files in snapshots.values() for file in files]
    backups = []
    if BACKUPS_DIR.exists():
        backups = [file for file in BACKUPS_DIR.iterdir() if file.is_file()]

    snapshot_size = sum(file.stat().st_size for file in snapshot_files)
    backup_size = sum(file.stat().st_size for file in backups)
    total_size = snapshot_size + backup_size

    timestamps = sorted(snapshots.keys())
    oldest = timestamps[0] if timestamps else "N/A"
    newest = timestamps[-1] if timestamps else "N/A"

    context_files = list_context_files()
    context_chars = 0
    for file_path in context_files:
        context_chars += len(file_path.read_text(encoding="utf-8", errors="replace"))
    context_tokens = max(1, int(context_chars / TOKEN_CHARS_PER))

    session_files = []
    sessions_dir = REPO_ROOT / "sessions"
    if sessions_dir.exists():
        session_files = [p for p in sessions_dir.rglob("*.md") if "templates" not in p.parts]
    session_count = max(1, len([p for p in session_files if p.name != "SESSION.md"]))

    total_tokens = context_tokens * session_count
    framework_tokens = int(total_tokens * DELTA_FACTOR)
    saved_tokens = max(0, total_tokens - framework_tokens)
    saved_percent = (saved_tokens / total_tokens) * 100 if total_tokens else 0
    cost_low = (saved_tokens / 1000) * PRICE_LOW
    cost_high = (saved_tokens / 1000) * PRICE_HIGH

    print("=== Uso de Espacio ===")
    print(f"Snapshots:  {len(snapshot_files)} archivos ({human_bytes(snapshot_size)})")
    print(f"Backups:    {len(backups)} archivos ({human_bytes(backup_size)})")
    print(f"Total:      {human_bytes(total_size)}")
    print(f"Mas antiguo: {oldest}")
    print(f"Mas reciente: {newest}")

    print("\n=== Estimacion de Tokens Ahorrados ===")
    print(f"Contexto promedio: ~{context_tokens} tokens")
    print(f"Sesiones estimadas: {session_count}")
    print(f"Total sin framework: ~{total_tokens} tokens")
    print(f"Total con framework: ~{framework_tokens} tokens")
    print(f"Ahorro estimado: ~{saved_tokens} tokens ({saved_percent:.1f}%)")
    print(f"Costo aprox: ${cost_low:.2f} - ${cost_high:.2f} USD")

    print("\n=== Beneficios Adicionales ===")
    print("- Contexto persistente sin re-prompt completo")
    print("- Sin vendor lock-in (archivos locales)")
    print("- Snapshots para restauracion rapida")
    print("- Sync rapido y repetible")
    return 0


def delete_snapshot(timestamp, force=False):
    snapshots = collect_snapshots()
    files = snapshots.get(timestamp)
    if not files:
        print(f"[ERROR] Snapshot '{timestamp}' no encontrado.")
        return 1
    if not force and not confirm_action("Eliminar snapshot seleccionado?"):
        print("[INFO] Operacion cancelada.")
        return 0
    removed = 0
    for file_path in files:
        file_path.unlink(missing_ok=True)
        removed += 1
    print(f"[OK] Snapshot eliminado: {timestamp} ({removed} archivos)")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Context versioning utilities")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("snapshot", help="Crea un snapshot del contexto")
    subparsers.add_parser("list", help="Lista snapshots disponibles")

    restore_parser = subparsers.add_parser("restore", help="Restaura un snapshot")
    restore_parser.add_argument("timestamp", help="Timestamp del snapshot")
    restore_parser.add_argument("--force", action="store_true", help="No pedir confirmacion")

    diff_parser = subparsers.add_parser("diff", help="Comparar con snapshot")
    diff_parser.add_argument("timestamp", help="Timestamp del snapshot")

    clean_parser = subparsers.add_parser("clean", help="Eliminar snapshots antiguos")
    clean_parser.add_argument("--older", type=int, required=True, help="Dias de retencion")

    subparsers.add_parser("export", help="Exporta backup en zip")

    import_parser = subparsers.add_parser("import", help="Importa backup desde zip")
    import_parser.add_argument("path", help="Ruta al archivo zip")
    import_parser.add_argument("--force", action="store_true", help="No pedir confirmacion")

    subparsers.add_parser("stats", help="Muestra metricas y estadisticas")

    delete_parser = subparsers.add_parser("delete", help="Eliminar snapshot")
    delete_parser.add_argument("timestamp", help="Timestamp del snapshot")
    delete_parser.add_argument("--force", action="store_true", help="No pedir confirmacion")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    if args.command == "snapshot":
        return snapshot()
    if args.command == "list":
        return list_snapshots()
    if args.command == "restore":
        return restore_snapshot(args.timestamp, force=args.force)
    if args.command == "diff":
        return diff_snapshot(args.timestamp)
    if args.command == "clean":
        return clean_snapshots(args.older)
    if args.command == "export":
        return export_backup()
    if args.command == "import":
        return import_backup(args.path, force=args.force)
    if args.command == "stats":
        return stats()
    if args.command == "delete":
        return delete_snapshot(args.timestamp, force=args.force)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
