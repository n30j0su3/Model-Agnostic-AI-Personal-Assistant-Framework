# Claude Context

<!-- MASTER-CONTEXT-START -->
# Personal Assistant - Master Context

## Localization (i18next)
- **Primary Language**: Spanish (es)
- **Secondary Language**: English (en)
- **Translation Path**: docs/i18n/{{lng}}/common.json
- **Rule**: Los agentes deben consultar estos archivos para usar terminología consistente en las respuestas del sistema.

## Active Workspaces
- [x] Personal: Configurado y activo.
- [x] Professional: Configurado y activo.
- [x] Research: Configurado y activo.
- [x] Content: Configurado y activo.
- [x] Development: Configurado y activo.

## Current Focus
Implementación inicial del framework "Model-agnostic AI Personal Assistant".

## Preferences
- Response style: Conciso pero detallado cuando es necesario.
- Decision making: Presenta opciones con pros/contras.
- Proactivity: Sugiere mejoras cuando las identifiques.

## Key Files Reference
- Sessions: sessions/SESSION.md
- Plan: plan-trabajo-v0.md

## Rules
1. Siempre verifica el contexto antes de responder sobre proyectos.
2. Actualiza SESSION.md después de tareas importantes.
3. Pregunta si falta información crítica o contexto.
4. Mantén respuestas accionables y alineadas con el plan de trabajo.
5. Utiliza los agentes y skills definidos en sus respectivos directorios.

## Feature Session Protocol
**Trigger**: Solicitud explícita de iniciar una Feature Session (palabras clave: "feature session", "seccion rapida", "/feature").
**Behavior**:
1. **Case A (Init)**: Si `sessions/SESSION.md` tiene estado "Closed" o "New":
   - **Output**: Bienvenida explícita al "🚀 Feature Session Mode".
   - **Explain**: "Modo de desarrollo activo (Dogfooding). Backlog filtrado y scripts de mantenimiento habilitados."
2. **Case B (Resume)**: Si `sessions/SESSION.md` tiene estado "Open/Active" y contexto previo de desarrollo:
   - **Output**: "✅ Feature Session Mode: Active" (sin explicaciones redundantes).
   - **Action**: Proceder con las tareas pendientes.
**Nota**: No iniciar Feature Session solo por leer `MASTER.md`.

<!-- MASTER-CONTEXT-END -->