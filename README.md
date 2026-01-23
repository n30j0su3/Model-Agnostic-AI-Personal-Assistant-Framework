# Model-Agnostic AI Personal Assistant Framework v1.0

> "One Framework to rule them all, One Context to find them."

Un framework estandarizado para interactuar con IAs en modo "Personal Assistant", diseñado para la máxima productividad multidisciplinaria con contexto local y sin vendor lock-in.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Agnostic](https://img.shields.io/badge/Model-Agnostic-orange)

## 🚀 Características Principales

- 🤖 **Multi-Tool Workflow**: Trabaja con OpenCode, Claude Code, Gemini CLI y Codex simultáneamente.
- 📁 **Contexto Local**: Todo tu conocimiento reside en archivos `.md` bajo tu control.
- 🌐 **Multidisciplinario**: 5 Workspaces pre-configurados (Personal, Professional, Research, Content, Development).
- 🛠 **Skills & Agents**: Sistema extensible basado en el estándar [Agent Skills](https://agentskills.io).
- 📝 **Trazabilidad Total**: Gestión de sesiones diarias con archivo histórico automático.
- 🎨 **Diseño Inteligente**: Integración nativa con `@ui-ux-pro-max` para interfaces profesionales.

## 📁 Estructura del Proyecto

```text
├── .context/       # Conocimiento central (MASTER.md)
├── agents/         # Agentes especializados (@session-manager, etc.)
├── skills/         # Habilidades modulares (@xlsx, @pdf, @task-mgmt)
├── workspaces/     # Espacios aislados por disciplina
├── sessions/       # Logs diarios y trazabilidad
├── scripts/        # Automatización y sincronización
└── docs/           # Documentación profesional (Mintlify style)
```

## 🛠 Instalación Rápida

1. **Clonar el repo**:
   ```bash
   git clone https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git
   ```
2. **Configurar tu perfil**:
   Edita `.context/MASTER.md` con tus preferencias.
3. **Sincronizar**:
   ```bash
   python scripts/sync-context.py
   ```

## 📖 Documentación

La documentación completa está disponible en la carpeta `docs/`. Sigue el estándar de Mintlify para una experiencia de lectura superior.

---
Hecho con ❤️ por el equipo de **Advanced Agentic Coding**.
Basado en las filosofías de **theNetworkChuck**.
