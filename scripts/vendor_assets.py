#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LIB_DIR = REPO_ROOT / "docs" / "lib"
MANIFEST_PATH = LIB_DIR / "manifest.json"

ASSETS = {
    "alpine.min.js": "https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js",
    "marked.min.js": "https://cdn.jsdelivr.net/npm/marked/marked.min.js",
    "lucide.min.js": "https://unpkg.com/lucide@latest/dist/umd/lucide.min.js",
    "tailwind.js": "https://cdn.tailwindcss.com",
}


def fetch_asset(url):
    request = urllib.request.Request(url, headers={"User-Agent": "PA-Framework"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def write_manifest(entries):
    payload = {
        "updated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "assets": entries,
    }
    MANIFEST_PATH.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def vendor_assets(force=False):
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    manifest_entries = []

    for name, url in ASSETS.items():
        target_path = LIB_DIR / name
        if target_path.exists() and not force:
            manifest_entries.append({
                "name": name,
                "url": url,
                "bytes": target_path.stat().st_size,
                "cached": True,
            })
            continue

        try:
            data = fetch_asset(url)
        except Exception as exc:
            print(f"[ERROR] No se pudo descargar {name}: {exc}")
            return False

        target_path.write_bytes(data)
        manifest_entries.append({
            "name": name,
            "url": url,
            "bytes": len(data),
            "cached": False,
        })
        print(f"[OK] Asset descargado: {name} ({len(data)} bytes)")

    write_manifest(manifest_entries)
    print(f"[OK] Manifest generado: {MANIFEST_PATH}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Descarga assets locales para el Cockpit (offline).")
    parser.add_argument("--force", action="store_true", help="Re-descargar assets existentes")
    args = parser.parse_args()
    success = vendor_assets(force=args.force)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
