# Model-agnostic AI Personal Assistant

Framework "estándar" para interactuar con IA en modo "Personal Assistant", optimizando la productividad y manteniendo el contexto local.

## Características
- **Agnóstico al Modelo**: Compatible con OpenCode, Claude Code, Gemini CLI y Codex.
- **Contexto Local**: Todo se almacena en archivos `.md` en la carpeta `.context/`.
- **Multi-Tool**: Diseñado para trabajar con múltiples terminales AI simultáneamente.
- **Skills & Agents**: Sistema extensible basado en estándares open-source (Agent Skills spec).
- **Sesión del Día**: Trazabilidad completa y gestión de tareas en lenguaje natural.

## Inicio Rápido

1. **Revisar el Plan**: Consulta `plan-trabajo-v0.md` para entender las fases del proyecto.
2. **Configurar Perfil**: Edita `.context/MASTER.md` con tu información personal.
3. **Sincronizar**: Utiliza los scripts en `scripts/` para mantener tus terminales alineadas.

## Estructura
- `.context/`: Conocimiento central del asistente.
- `agents/`: Agentes especializados (AGENTS.md).
- `skills/`: Habilidades invocables (SKILLS.md).
- `sessions/`: Log diario y gestión de tareas (SESSION.md).
- `workspaces/`: Contextos multidisciplinarios separados.

---
Basado en las mejores prácticas de **theNetworkChuck** y estándares OpenSource.
