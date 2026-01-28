# Plan de Ejecucion Secuencial: Optimizacion y UX

**Prioridad**: Alta (Respetando Quota)
**Orden de Ejecucion**: BL-097 -> BL-098 -> BL-085

---

## Fase 1: BL-097 Context Evaluator (Skill)
**Objetivo**: Crear un marco para evaluar la calidad de las respuestas de los agentes.
**Enfoque**: Implementacion ligera basada en estandares de *Agent Skills*.

### Tareas
1. Crear estructura `skills/core/context-evaluator/`.
2. Crear `SKILL.md` definiendo el protocolo "LLM-as-a-Judge".
3. Implementar script `scripts/evaluate.py` que acepte `prompt`, `response` y `criteria` (rubrica).
4. Crear rubrica base `rubrics/general.json`.

---

## Fase 2: BL-098 Context Compaction (Session Manager)
**Objetivo**: Evitar saturacion de contexto en sesiones largas mediante resumen inteligente.
**Enfoque**: Algoritmo "U-Shaped" (mantiene inicio y fin, resume el medio).

### Tareas
1. Modificar `agents/core/session-manager/AGENT.md` para incluir la capacidad de compactacion.
2. Crear `agents/core/session-manager/scripts/compact.py`.
   - Input: `SESSION.md`.
   - Logic: Si lineas > 500 -> Identificar secciones -> Resumir bloques completados -> Reescribir.
3. Integrar en el flujo de `scripts/pa.py` o trigger manual.

---

## Fase 3: BL-085 UX Dashboard (Cockpit Upgrade)
**Objetivo**: Que el Dashboard sea una herramienta util para usuarios no tecnicos, no solo un visor de docs.
**Enfoque**: Single Page Application (SPA) ligera sin dependencias externas (solo lo que vendorizamos en `docs/lib`).

### Tareas
1. Analizar `docs/index.html` actual.
2. Rediseñar para incluir:
   - Estado del sistema (Health check visual).
   - Accesos directos a "Acciones Rapidas" (que te den el comando para copiar).
   - Visor de Backlog amigable.
3. Asegurar que funcione 100% offline (file://).

---

## Estrategia de Quota

- Al finalizar cada Fase, se hara un "checkpoint":
  - Verificar tests basicos.
  - **Reiniciar contexto** (si fuera posible en la herramienta) o solicitar al usuario que limpie si estamos al limite.
  - Proceder a la siguiente.
