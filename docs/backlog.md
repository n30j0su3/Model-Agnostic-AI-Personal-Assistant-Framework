# Backlog del Framework

Ultima actualizacion: 2026-01-23

## Versionado

- Estandar: SemVer (MAJOR.MINOR.PATCH).
- Al agregar caracteristicas: incrementa MINOR y registra en el historial.
- Al corregir bugs: incrementa PATCH.
- Cambios incompatibles: incrementa MAJOR.
- Siempre actualiza el badge de version en `README.md` y este historial.

## Historial de cambios

- 2026-01-23: Backlog inicial creado con items BL-001 a BL-019.
- 2026-01-23: Se agrego columna Estado y se marcaron BL-001 a BL-007 como Hecho.
- 2026-01-23: Release 1.1.0 (instalador multiplataforma, nuevos pasos de instalacion, skill json-prompt-generator).
- 2026-01-23: Se agregaron items BL-020 a BL-027 y backlog local de scopes.
- 2026-01-23: Release 1.2.0 (skills prd-generator y mcp-builder, backlog local, backlog ampliado).
- 2026-01-23: Release 1.3.0 (documento de jerarquia de scopes y navegacion de docs).
- 2026-01-23: Se agregaron items BL-029 y BL-030 (instalador basico/pro y configuracion guiada).

| ID | Item | Prioridad | Estado | Criterios de aceptacion |
| --- | --- | --- | --- | --- |
| BL-001 | Guia "para dummies" con prerequisitos de hardware y software | Alta | Hecho | README incluye requisitos claros y un paso a paso de instalacion completa | 
| BL-002 | Instalacion de LLMs (IA) paso a paso | Alta | Hecho | README detalla cuentas, API keys, configuracion y validacion basica | 
| BL-003 | Instalador todo-en-uno en comando unico | Alta | Hecho | README incluye un comando para Windows y otro para macOS/Linux | 
| BL-004 | FAQ basico para usuarios no tecnicos | Alta | Hecho | README incluye al menos 5 preguntas frecuentes con respuestas cortas | 
| BL-005 | Frase insignia en README | Media | Hecho | La frase aparece en la introduccion del README | 
| BL-006 | Agradecimientos formales en README | Media | Hecho | Se incluye seccion de agradecimientos con el texto solicitado | 
| BL-007 | Skill json-prompt-generator | Alta | Hecho | Skill creado en `skills/core/json-prompt-generator` con instrucciones y ejemplo | 
| BL-008 | Orquestacion multi-modelo con conmutacion rapida | Media | Pendiente | Flujo unificado documentado para OpenCode, Claude, Gemini y Codex | 
| BL-009 | Gestion de contexto local versionado | Media | Pendiente | Estructura `.context/` definida y versionada sin lock-in | 
| BL-010 | Workspaces multidisciplinarios aislados | Media | Pendiente | Workspaces claramente separados por disciplina y documentados | 
| BL-011 | Sistema de agentes especializados con roles claros | Media | Pendiente | Catalogo de agentes con responsabilidades y uso recomendado | 
| BL-012 | Skills modulares para tareas recurrentes | Media | Pendiente | Libreria de skills con index y versionado actualizado | 
| BL-013 | Trazabilidad diaria automatica | Media | Pendiente | Sesiones diarias registradas y accesibles desde `sessions/` | 
| BL-014 | Pipeline de sincronizacion coherente | Media | Pendiente | Script de sync mantiene coherencia entre herramientas | 
| BL-015 | Documentacion integrada estilo Mintlify | Baja | Pendiente | Docs consistentes y navegables en `docs/` | 
| BL-016 | Estructura de carpetas estable y extensible | Baja | Pendiente | Convenciones de nombres y ubicaciones estandarizadas | 
| BL-017 | Scripts de automatizacion para sync y normalizacion | Baja | Pendiente | Scripts documentados y reutilizables en `scripts/` | 
| BL-018 | Compatibilidad multiplataforma | Baja | Pendiente | Rutas y comandos probados en Windows/macOS/Linux | 
| BL-019 | Diseno de interfaz soportado por skill UI/UX | Baja | Pendiente | Skill UI/UX disponible y referenciado en docs | 
| BL-020 | Revisar jerarquia de scopes (agents/skills/workspaces) | Media | Hecho | Backlog borrador local con sugerencias en `docs/backlog.local.md` | 
| BL-021 | Agregar skill prd-generator | Alta | Hecho | Skill creado en `skills/core/prd-generator` y listado en el indice | 
| BL-022 | Agregar skill mcp-builder | Alta | Hecho | Skill creado en `skills/core/mcp-builder` y listado en el indice | 
| BL-023 | Evaluar skill docker-claude-skill | Baja | Pendiente | Fuente: https://github.com/wrsmith108/docker-claude-skill | 
| BL-024 | Evaluar skill claude-skill-version-sync | Baja | Pendiente | Fuente: https://github.com/wrsmith108/claude-skill-version-sync | 
| BL-025 | Evaluar skill claude-skill-docker-optimizer | Baja | Pendiente | Fuente: https://github.com/wrsmith108/claude-skill-docker-optimizer | 
| BL-026 | Evaluar skill RchGrav-claudebox | Baja | Pendiente | Fuente: https://agent-skills.cc/skills/RchGrav-claudebox | 
| BL-027 | Evaluar skill vibe-to-docker | Baja | Pendiente | Fuente: https://github.com/wrsmith108/vibe-to-docker | 
| BL-028 | Documentar jerarquia de scopes en docs | Media | Hecho | Documento creado en `docs/architecture/scopes.mdx` | 
| BL-029 | Selector de instalacion basica vs pro | Alta | Pendiente | Instalador ofrece seleccion de perfil en primera ejecucion | 
| BL-030 | Configuracion guiada del perfil al instalar | Alta | Pendiente | Permite configurar `.context/MASTER.md` ahora o despues con preferencias avanzadas opcionales | 
