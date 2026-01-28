# Plan BL-095: Orquestador Inteligente de Tareas y Delegacion

**Fecha**: 2026-01-27
**Estado**: Pendiente de ejecucion
**Prioridad**: Alta (100%)

---

## Resumen Ejecutivo

Crear un agent `@orchestrator` que coordine la ejecucion de tareas complejas, delegando a agents/skills existentes y presentando resultados consolidados.

---

## Decisiones Confirmadas

| Aspecto | Decision | Justificacion |
|---------|----------|---------------|
| Tipo de componente | Agent (con prompts LLM) | Flexibilidad para analizar tareas complejas |
| Autonomia | Auto-ejecutar | Sin confirmaciones intermedias, flujo continuo |
| Almacenamiento de logs | Dual | JSONL en `logs/orchestrator/` + resumen en SESSION.md |

---

## Analisis de Situacion Actual

### Componentes Existentes

| Componente | Estado | Funcion | Gaps |
|------------|--------|---------|------|
| `decision-engine` | MVP funcional | Routing de instrucciones | Solo decide, no ejecuta ni coordina |
| `route.py` | Funcional | CLI para routing | Decide pero no orquesta |
| `agent-routing.json` | 9 agentes mapeados | Keywords por agente | Sin capacidades formales |
| `task-management` | Skill basica | Tagging de tareas | Sin orquestacion |

### Gaps Criticos

1. No hay ejecucion coordinada post-routing
2. No hay resumen/agregacion de resultados
3. No hay plan de ejecucion multi-step
4. No hay tracking de estado de subtareas

---

## Arquitectura Propuesta

```
+-------------------------------------------------------------------+
|                        ORCHESTRATOR                                |
|                                                                    |
|  1. INTAKE --> 2. ANALYZE --> 3. PLAN --> 4. EXECUTE --> 5. SUMMARIZE |
|                                                                    |
|  +---------+   +----------+   +--------+   +----------+   +---------+ |
|  | Parse   |   | Decision |   | Task   |   | Dispatch |   | Collect | |
|  | Input   |   | Engine   |   | Queue  |   | & Track  |   | Results | |
|  +---------+   +----------+   +--------+   +----------+   +---------+ |
|                     |                            |                    |
|                     v                            v                    |
|              +----------------------------------------------+        |
|              |     AGENTS / SKILLS / LOCAL TOOLS            |        |
|              |  @feature-architect  @session-manager        |        |
|              |  @github-deployer    @context-sync           |        |
|              |  skills/core/*       scripts/*               |        |
|              +----------------------------------------------+        |
+----------------------------------------------------------------------+
```

---

## Flujo de Orquestacion

### Fase 1: INTAKE
Recibe input del usuario con contexto opcional.

```json
{
  "input": "Quiero agregar dark mode y actualizar el backlog",
  "context": { "session": "...", "user_prefs": "..." }
}
```

### Fase 2: ANALYZE
Usa decision-engine para clasificar y descomponer en subtareas.

```json
{
  "tasks": [
    { "id": 1, "description": "Agregar dark mode", "route": "DELEGATE", "agent": "@feature-architect" },
    { "id": 2, "description": "Actualizar backlog", "route": "LOCAL_EXECUTION", "action": "edit_backlog" }
  ]
}
```

### Fase 3: PLAN
Ordena tareas por dependencias y eficiencia.

```json
{
  "execution_order": [2, 1],
  "reason": "Backlog primero para registrar, luego feature",
  "parallel_safe": false
}
```

### Fase 4: EXECUTE
- Ejecuta secuencialmente o en paralelo segun plan
- Tracking de estado: `pending -> running -> done/failed`
- Timeout y retry configurable

### Fase 5: SUMMARIZE
Consolida resultados y genera resumen.

```json
{
  "summary": "Se completaron 2 tareas: backlog actualizado, feature dark mode planificada.",
  "results": [...],
  "next_steps": ["Revisar FAR generado", "Implementar CSS"]
}
```

---

## Estructura de Archivos

```
agents/core/orchestrator/
+-- AGENT.md              # Documentacion del orquestador
+-- prompts/
|   +-- analyze-task.md   # Prompt para analizar tarea
|   +-- plan-execution.md # Prompt para planificar ejecucion
|   +-- summarize.md      # Prompt para resumen final
+-- scripts/
|   +-- orchestrate.py    # CLI principal
|   +-- task_queue.py     # Cola de tareas en memoria
+-- schemas/
    +-- task.schema.json  # Schema de tarea
    +-- result.schema.json # Schema de resultado

logs/orchestrator/
+-- .gitkeep
+-- 2026-01-27.jsonl      # Logs de ejecucion por dia
```

---

## Entregables

| # | Archivo | Descripcion | Prioridad |
|---|---------|-------------|-----------|
| 1 | `agents/core/orchestrator/AGENT.md` | Documentacion completa del agent | Alta |
| 2 | `agents/core/orchestrator/prompts/analyze-task.md` | Prompt para descomponer tarea | Alta |
| 3 | `agents/core/orchestrator/prompts/plan-execution.md` | Prompt para ordenar ejecucion | Alta |
| 4 | `agents/core/orchestrator/prompts/summarize.md` | Prompt para resumen final | Alta |
| 5 | `agents/core/orchestrator/scripts/orchestrate.py` | CLI principal del orquestador | Alta |
| 6 | `agents/core/orchestrator/schemas/task.schema.json` | Schema de tarea | Media |
| 7 | `agents/core/orchestrator/schemas/result.schema.json` | Schema de resultado | Media |
| 8 | `logs/orchestrator/.gitkeep` | Directorio de logs | Baja |
| 9 | Actualizar `agent-routing.json` | Agregar @orchestrator | Media |
| 10 | Actualizar `docs/architecture/agents.mdx` | Documentar orquestador | Media |

---

## Dependencias con Componentes Existentes

```
@orchestrator
    +-- USA: decision-engine/route.py (routing)
    +-- DELEGA A: @feature-architect, @session-manager, @github-deployer, etc.
    +-- ESCRIBE: logs/orchestrator/YYYY-MM-DD.jsonl
    +-- ACTUALIZA: sessions/SESSION.md (resumen)
```

---

## Orden de Implementacion

| Paso | Accion | Dependencias |
|------|--------|--------------|
| 1 | Crear estructura de directorios | Ninguna |
| 2 | Escribir AGENT.md | Ninguna |
| 3 | Crear schemas (task, result) | Ninguna |
| 4 | Implementar orchestrate.py | Schemas, route.py |
| 5 | Escribir prompts (analyze, plan, summarize) | AGENT.md |
| 6 | Actualizar agent-routing.json | orchestrate.py |
| 7 | Crear directorio de logs | Ninguna |
| 8 | Actualizar docs/architecture/agents.mdx | AGENT.md |
| 9 | Smoke test manual | Todo lo anterior |

---

## Estimacion de Tiempo

| Fase | Tiempo estimado |
|------|-----------------|
| Estructura + AGENT.md | 10 min |
| Schemas | 5 min |
| orchestrate.py | 20 min |
| Prompts (3) | 15 min |
| Updates (routing, docs) | 10 min |
| **Total** | ~60 min |

---

## Schemas Propuestos

### task.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OrchestratorTask",
  "type": "object",
  "required": ["id", "description", "route"],
  "properties": {
    "id": { "type": "integer" },
    "description": { "type": "string" },
    "route": { "type": "string", "enum": ["LOCAL_EXECUTION", "DELEGATE", "REMOTE_LLM"] },
    "agent": { "type": "string" },
    "action": { "type": "string" },
    "status": { "type": "string", "enum": ["pending", "running", "done", "failed"] },
    "result": { "type": "object" },
    "error": { "type": "string" }
  }
}
```

### result.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OrchestratorResult",
  "type": "object",
  "required": ["session_id", "input", "tasks", "summary"],
  "properties": {
    "session_id": { "type": "string" },
    "input": { "type": "string" },
    "tasks": { "type": "array", "items": { "$ref": "task.schema.json" } },
    "summary": { "type": "string" },
    "next_steps": { "type": "array", "items": { "type": "string" } },
    "execution_time_ms": { "type": "integer" },
    "timestamp": { "type": "string", "format": "date-time" }
  }
}
```

---

## Criterios de Exito

- [ ] El orquestador descompone tareas complejas en subtareas
- [ ] Delega correctamente a agents/skills existentes
- [ ] Ejecuta sin confirmaciones intermedias
- [ ] Genera resumen consolidado al finalizar
- [ ] Logs duales (JSONL + SESSION.md)
- [ ] Documentacion completa en AGENT.md
- [ ] Integrado en agent-routing.json

---

## Riesgos y Mitigaciones

| Riesgo | Severidad | Mitigacion |
|--------|-----------|------------|
| Loops infinitos de delegacion | Alta | Limitar profundidad de delegacion a 3 niveles |
| Timeout en tareas largas | Media | Timeout configurable por tarea |
| Conflicto con decision-engine | Baja | Orquestador USA decision-engine, no lo reemplaza |
| Logs excesivos | Baja | Rotacion automatica por fecha |

---

## Notas Adicionales

- El orquestador NO reemplaza al decision-engine; lo usa como componente interno
- Auto-ejecucion significa que no pide confirmacion, pero respeta politicas de riesgo del decision-engine
- Los logs JSONL permiten auditoria posterior sin afectar SESSION.md

---

## Siguiente Paso

Cambiar a modo BUILD para ejecutar este plan.
