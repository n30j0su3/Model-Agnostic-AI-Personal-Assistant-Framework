# 🛠 DELEGACIÓN DE TAREAS: CODEX (GTP5.2) - FASE 2

**Objetivo:** Implementar sistemas de telemetría, logging y base de conocimiento de forma independiente al núcleo.

## Tarea 1: Logging y Tracking (BL-091 & BL-092)
**Contexto:** Necesitamos registrar la actividad de la IA para optimización futura.
- **BL-091:** Crear un script `scripts/prompt_logger.py` que registre en `logs/prompts.jsonl`: timestamp, agente, skill usado, y el prompt (con opción de anonimización).
- **BL-092:** Implementar una lógica en el logger para estimar tokens (4 caracteres = 1 token aprox. si no hay API de conteo) y registrar el proveedor (Gemini, Claude, etc.).
- **Integración:** El script debe ser ejecutable de forma independiente: `python scripts/prompt_logger.py --log "mensaje" --agent "name"`.

## Tarea 2: Centralized Knowledge Base (BL-103 & BL-106)
**Contexto:** Consolidar URLs y mejores prácticas en un módulo de referencia.
- **Acción:** Crear `config/knowledge_base.json` y `docs/architecture/knowledge-base.mdx`.
- **Contenido:** Investigar y listar URLs de: Context7, Agent Skills (.cc), Serena, DeepSeek, y Arxiv (Papers AI). 
- **Estructura:** Clasificar por Categoría (Agentes, Frameworks, Papers, Herramientas).

## Tarea 3: Persistencia del Backlog (Continuación)
- Finalizar la lógica de reescritura de Markdown en `scripts/server.py` para que el CRUD del Dashboard sea 100% funcional.

**Restricciones:**
- No depender de cambios en `pa.py` o `sync-context.py` (Gemini se encarga de eso).
- Los scripts deben ser "plug-and-play".

---
*Instrucción generada por el Orquestador (Gemini) el 2026-01-29.*