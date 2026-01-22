# Personal Assistant Agents Index

## Core Agents

### @session-manager
- **Propósito**: Gestión de sesiones diarias, recordatorios y cierre de día.
- **Estado**: OPERATIVO.
- **Ubicación**: `agents/core/session-manager/`

### @context-sync
- **Propósito**: Automatizar la sincronización entre MASTER.md y archivos específicos.
- **Estado**: Lógica base en `scripts/sync-context.py`.
- **Ubicación**: `agents/core/context-sync/`

### @github-deployer
- **Propósito**: Gestión de trazabilidad en GitHub (commits, tags, deploys).
- **Estado**: Pendiente.
- **Ubicación**: `agents/core/github-deployer/`

## Workspace Agents
*Agentes especializados por área (se activan según el workspace activo).*

---
Para crear un nuevo agente, sigue el estándar en `docs/guides/creating-agents.md`.
