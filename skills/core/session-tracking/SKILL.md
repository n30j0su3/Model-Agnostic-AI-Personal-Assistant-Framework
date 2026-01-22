---
name: session-tracking
description: Gestiona sesiones de trabajo, registra tareas en SESSION.md y mantiene la trazabilidad diaria. Úsalo cuando el usuario quiera iniciar el día, registrar progreso o ver pendientes.
license: MIT
metadata:
  author: opencode
  version: "1.0"
compatibility: OpenCode, Claude Code, Gemini CLI, Codex
---

# Session Tracking Skill

Este skill permite al asistente gestionar el archivo `sessions/SESSION.md` de forma estructurada.

## Instrucciones para la IA

### 1. Registro de Tareas
Cuando el usuario mencione una tarea, utiliza el script `scripts/log-task.py` o edita directamente `sessions/SESSION.md` siguiendo este formato:
- `[ ]` Tarea pendiente
- `[~]` Tarea en progreso
- `[x]` Tarea completada

### 2. Estructura de SESSION.md
El archivo debe mantener siempre estas secciones:
- **Today's Focus**: El objetivo principal del día.
- **Tasks**: Divididas en Pending, In Progress y Completed Today.
- **Notes & Decisions**: Registro de decisiones importantes.
- **Reminders**: Recordatorios con hora si es necesario.

### 3. Comandos de Usuario Soportados
- "Añade la tarea [X]"
- "Estoy trabajando en [X]"
- "He terminado [X]"
- "¿Qué tengo pendiente?"

## Herramientas Relacionadas
- `scripts/log-task.py`: Script de conveniencia para actualizaciones rápidas.
- `sessions/templates/daily-session.md`: Template para archivar el día.
