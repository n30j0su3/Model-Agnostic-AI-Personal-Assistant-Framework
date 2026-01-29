# Neural Gateway & Framework Bootstrapper

Este archivo ejecuta un checklist obligatorio antes de abrir cualquier sesion o ejecutar nuevas tareas. No saltes los pasos: el framework depende de un contexto controlado y de los agentes listados en `agents/AGENTS.md`.

## Activation Sequence
1. **Read AI instructions**: Lee `AI_INSTRUCTIONS.md` para conocer el flujo y las reglas del repo.
2. **Load master context**: Lee `.context/MASTER.md` y el archivo de contexto del modelo (.context/opencode.md, .context/claude.md, .context/gemini.md).
3. **Check session state**: `sessions/SESSION.md` es un ejemplo publico. Para registros reales, usa `sessions/templates/daily-session.md` en tu entorno privado.
4. **Engage orchestrator**: Usa `@orchestrator` via `python scripts/pa.py` para tareas multi-step.

## Framework Instruments
- **Context engine** (`.context/`): Todas las decisiones deben alinearse con este directorio.
- **Session management** (`sessions/`): El repo publico solo contiene plantillas. Los datos reales viven en el repo privado o en carpetas ignoradas.
- **Control panel**: `python scripts/pa.py` ofrece estado, orquestacion y acceso al backlog (`docs/backlog.md`).
- **Skills & agents**: `skills/` aloja herramientas; `agents/AGENTS.md` documenta roles como `@feature-architect` y `@context-sync`.

## Remote Strategy (BL-111 / BL-112)
- **`upstream`** es el repo publico fijo: `https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git`. Solo publica ejemplos y documentacion.
- **`origin`** es el repo privado de trabajo (ej: `Model-Agnostic-AI-Personal-Assistant-Framework-dev`). Almacena trazabilidad, sesiones y datos operativos.
- **Instalaciones limpias**: `scripts/setup_repo.py` solicita el repo privado y configura `origin` junto al `upstream` fijo.
- **Sincronizacion**: Ejecuta `scripts/sync-remotes.py` para empujar cambios core al `upstream` (publico) y tu `origin` (privado) sin exponer logs.

## Dev HQ Workflow
- Usa `dev.bat` o `dev.sh` para iniciar la sesion de features en este entorno.
- Trabaja en `main` (privado) y publica con `scripts/publish-release.py` hacia `public-release`.

## Privacidad estricta
1. **Nunca subas sesiones reales a `upstream`.** `sessions/SESSION.md` y los historicos solo son plantillas.
2. **Registra tu trabajo en `sessions/templates/daily-session.md`.** Copia la plantilla a un archivo local o al workspace privado ignorado.
3. **Cierra cada sesion con `python scripts/sync-remotes.py --private-remote origin`.** Garantiza trazabilidad en tu remoto privado.

---
*Identity: Model-Agnostic Personal Assistant Framework v1.x*
*Single Source of Truth: .context/MASTER.md*
