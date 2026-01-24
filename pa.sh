#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[ERROR] Python no encontrado. Instala Python 3.11+."
  exit 1
fi

if [ ! -f "${ROOT_DIR}/.context/profile.md" ]; then
  echo "[INFO] Primera ejecucion detectada. Iniciando instalador..."
  "${PYTHON_BIN}" "${ROOT_DIR}/scripts/install.py"
fi

"${PYTHON_BIN}" "${ROOT_DIR}/scripts/pa.py" "$@"
