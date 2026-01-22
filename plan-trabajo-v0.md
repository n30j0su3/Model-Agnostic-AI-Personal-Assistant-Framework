# Model-Agnostic AI Personal Assistant Framework

## Plan de Trabajo v0

---

## 1. Visión General del Proyecto

### 1.1 Objetivo

Crear un **framework estandarizado** para interactuar con AI en modo "Personal Assistant" que permita:

- Gestionar, optimizar y mejorar la productividad personal y laboral
- Trabajar con múltiples terminales-AI simultáneamente (OpenCode, Gemini CLI, Claude Code, Codex)
- Mantener contexto local en archivos `.md` (sin vendor lock-in)
- Soportar tareas multidisciplinarias con contextos separados
- Implementar sistema de sesión diaria con trazabilidad completa

### 1.2 Filosofía Core

> "I own my context. Nothing annoys me more than when AI tries to fence me in, give me vendor lock-in. No, I reject that." - NetworkChuck

**Principios fundamentales:**

1. **Todo es un folder**: El proyecto completo es portable, versionable y tuyo
2. **Model-agnostic**: Funciona con cualquier terminal-AI actual o futura
3. **Context-first**: El contexto es el activo más valioso, debe persistir
4. **Progressive disclosure**: Cargar información solo cuando es necesaria
5. **Natural language**: Interacción en lenguaje natural, sin comandos crípticos

---

## 2. Prerequisitos

### 2.1 Cuentas Requeridas

| Servicio | Tipo | Propósito | Costo |
|----------|------|-----------|-------|
| **GitHub** | Obligatorio | Versionado, trazabilidad, backup | Gratis |
| **Google Account** | Obligatorio | Gemini CLI | Gratis |
| **OpenCode** | Recomendado | Terminal-AI principal | Gratis (múltiples providers) |
| **Anthropic (Claude Pro)** | Opcional | Claude Code + Agents avanzados | $20/mes |
| **OpenAI (ChatGPT Plus)** | Opcional | Codex CLI | $20/mes |

### 2.2 Software Base

```bash
# 1. Node.js y npm (requerido para instalación de herramientas)
node --version  # >= 18.x recomendado
npm --version   # >= 9.x recomendado

# 2. Git (para versionado y GitHub)
git --version   # >= 2.40 recomendado

# 3. Python 3 (para scripts y skills)
python3 --version  # >= 3.10 recomendado

# 4. Terminal moderna
# - Windows: Windows Terminal + WSL2 (recomendado)
# - macOS: iTerm2 o Terminal nativa
# - Linux: Cualquier terminal moderna
```

---

## 3. Arquitectura del Framework

### 3.1 Estructura de Directorios

```
personal-assistant/
├── .context/                         # Contexto para terminales-AI
│   ├── MASTER.md                    # Contexto principal compartido
│   ├── opencode.md                  # Contexto específico OpenCode
│   ├── claude.md                    # Contexto específico Claude Code
│   ├── gemini.md                    # Contexto específico Gemini CLI
│   └── agents.md                    # Contexto específico Codex
│
├── agents/                           # Agentes especializados
│   ├── AGENTS.md                    # Índice y configuración global de agentes
│   ├── core/                        # Agentes del sistema
│   └── custom/                      # Agentes del usuario
│
├── skills/                           # Sistema de habilidades (Agent Skills spec)
│   ├── SKILLS.md                    # Índice de skills disponibles
│   ├── core/                        # Skills del sistema
│   └── custom/                      # Skills del usuario
│
├── workspaces/                       # Espacios de trabajo por área
│   ├── personal/
│   ├── professional/
│   ├── research/
│   ├── content/
│   └── development/
│
├── sessions/                         # Registro de sesiones diarias
│   ├── SESSION.md                   # Sesión actual
│   ├── 2026/                        # Archivo histórico
│   └── templates/
│
├── logs/                             # Logs y trazabilidad
├── docs/                             # Documentación (Mintlify style)
├── scripts/                          # Automatización
├── config/                           # Configuración
├── .gitignore
├── README.md
└── CHANGELOG.md
```

---

## 4. Fases de Implementación

### Fase 1: Fundación (Semana 1-2)
- Estructura de directorios base
- Implementación de MASTER.md
- Configuración de context files multi-tool
- Script de sincronización de contexto (`sync-context.py`)

### Fase 2: Sistema de Sesiones (Semana 3-4)
- Implementación de SESSION.md y templates
- Skill `session-tracking` compatible con agentskills.io
- Sistema de resumen diario automático

### Fase 3: Agentes y Skills (Semana 5-8)
- Agentes core: `session-manager`, `context-sync`, `github-deployer`
- Skills core: `task-management`, `daily-summary`
- Integración con UI/UX Pro Max para interfaces

### Fase 4: Especialización y Polish (Semana 9-12)
- Configuración de Workspaces (Personal, Professional, Research, etc.)
- Documentación estilo Mintlify
- Internacionalización con i18next
- Release v1.0

---

**Versión**: 0.1.0  
**Última actualización**: 2026-01-22  
**Autor**: Personal Assistant Framework Team  
**Licencia**: MIT
