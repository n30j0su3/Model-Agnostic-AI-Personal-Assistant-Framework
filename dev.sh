#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PRIVATE_URL="https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework-dev.git"
PUBLIC_URL="https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git"

echo "[INFO] Dev HQ launcher"

if ! command -v git >/dev/null 2>&1; then
  echo "[ERROR] Git es obligatorio para el entorno Dev HQ."
  exit 1
fi

ORIGIN_URL="$(git -C "${ROOT_DIR}" remote get-url origin 2>/dev/null || true)"
if [ -z "${ORIGIN_URL}" ]; then
  echo "[ERROR] Remote origin no configurado."
  exit 1
fi
if [ "${ORIGIN_URL}" != "${PRIVATE_URL}" ]; then
  echo "[ERROR] origin no apunta al repo privado esperado."
  echo "[INFO] Esperado: ${PRIVATE_URL}"
  echo "[INFO] Actual:   ${ORIGIN_URL}"
  exit 1
fi

UPSTREAM_URL="$(git -C "${ROOT_DIR}" remote get-url upstream 2>/dev/null || true)"
if [ -z "${UPSTREAM_URL}" ]; then
  echo "[ERROR] Remote upstream no configurado."
  exit 1
fi
if [ "${UPSTREAM_URL}" != "${PUBLIC_URL}" ]; then
  echo "[ERROR] upstream no apunta al repo publico esperado."
  echo "[INFO] Esperado: ${PUBLIC_URL}"
  echo "[INFO] Actual:   ${UPSTREAM_URL}"
  exit 1
fi

CURRENT_BRANCH="$(git -C "${ROOT_DIR}" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
if [ "${CURRENT_BRANCH}" = "public-release" ]; then
  echo "[ERROR] No ejecutes Dev HQ en public-release."
  echo "[INFO] Cambia a la rama privada (main)."
  exit 1
fi

"${ROOT_DIR}/pa.sh" --feature "$@"
