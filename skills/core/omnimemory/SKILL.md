# OmniMemory (Context Cache L1/L2/L3)
**Versión:** 1.0 | **Estado:** Core Skill

## 1. Definición
OmniMemory es el sistema de gestión de memoria jerárquica del Framework. Permite a los agentes almacenar y recuperar información basada en la relevancia temporal y temática, optimizando el uso de tokens y manteniendo la coherencia a largo plazo.

## 2. Niveles de Memoria
- **L1 (Volátil/Sesión):** Almacenado en `.context/temp-quota/`. Contiene los logs de pensamiento de la tarea actual. Se limpia al cerrar la tarea.
- **L2 (Persistente/Reciente):** Almacenado en `sessions/`. Resúmenes de sesiones pasadas y logs de orquestación (`.jsonl`).
- **L3 (Consolidado/Base):** Almacenado en `.context/memory.md` y archivos de conocimiento en `workspaces/`. Hechos confirmados y patrones de éxito.

## 3. Instrucciones para Agentes
Cuando proceses una tarea compleja:
1. **Consulta L1/L2:** Busca si hay tareas similares o contexto relevante en las sesiones recientes.
2. **Loguea el "Thinking":** Guarda tus pasos de razonamiento en el formato estructurado de OmniMemory.
3. **Consolida en L3:** Si descubres un patrón o hecho importante, regístralo en la memoria de largo plazo al finalizar la sesión.

## 4. Estructura de Logs de Pensamiento
Cada log debe guardarse en `sessions/YYYY/MM/thinking.jsonl` con el siguiente esquema:
```json
{
  "timestamp": "ISO-8601",
  "task_id": "ID",
  "step": "Descripción del paso",
  "reasoning": "Por qué se tomó esta decisión",
  "result": "Resultado del paso"
}
```
