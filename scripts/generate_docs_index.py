#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = REPO_ROOT / "docs"
MANIFEST_PATH = DOCS_ROOT / "docs_manifest.js"

EXCLUDE_DIRS = {"lib"}
EXCLUDE_FILES = {"index.html", "dashboard.html", "status.js", "docs_manifest.js"}
EXTENSIONS = {".md", ".mdx"}


def prettify_label(path):
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            if line.startswith("# "):
                return line.lstrip("# ").strip()
    except Exception:
        pass
    return path.stem.replace("-", " ").replace("_", " ").title()


def collect_docs():
    items = []
    for path in DOCS_ROOT.rglob("*"):
        if path.is_dir() and path.name in EXCLUDE_DIRS:
            continue
        if path.is_file():
            if path.name in EXCLUDE_FILES:
                continue
            if path.suffix.lower() not in EXTENSIONS:
                continue
            rel_path = path.relative_to(DOCS_ROOT).as_posix()
            items.append({
                "label": prettify_label(path),
                "path": rel_path,
            })
    items.sort(key=lambda item: item["label"].lower())
    return items


def write_manifest(items):
    content = "window.DOCS_MANIFEST = " + json.dumps(items, ensure_ascii=True, indent=2) + ";\n"
    MANIFEST_PATH.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Genera el indice de documentacion local.")
    parser.add_argument("--output", help="Ruta alternativa de salida")
    args = parser.parse_args()
    items = collect_docs()
    output_path = Path(args.output) if args.output else MANIFEST_PATH
    content = "window.DOCS_MANIFEST = " + json.dumps(items, ensure_ascii=True, indent=2) + ";\n"
    output_path.write_text(content, encoding="utf-8")
    print(f"[OK] Docs manifest generado: {output_path} ({len(items)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
