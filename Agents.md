# Neural Gateway & Framework Bootstrapper

> ⚠️ **RESTRICCIÓN OBLIGATORIA NO NEGOCIABLE - COMANDO /init**
> 
> Si eres invocado mediante el comando `/init`:
> - ❌ **PROHIBIDO** modificar, crear o cambiar este archivo (`AGENTS.md`)
> - ❌ **PROHIBIDO** cualquier acción de escritura en archivos de configuración
> - ❌ **PROHIBIDO** ejecutar instalaciones o configuraciones iniciales
> - ✅ **OBLIGATORIO** iniciar el Framework en modo desarrollo (feature-session) INMEDIATAMENTE
> - ✅ Ejecutar: `python scripts/pa.py --feature` (o `dev.bat` / `./dev.sh`)
> 
> **Esta regla es INQUEBRANTABLE sin excepciones.**

---

## Activation Sequence (Standard)

1. **Read AI instructions**: Lee `AI_INSTRUCTIONS.md` para conocer el flujo y reglas del repo
2. **Load master context**: Lee `.context/MASTER.md` y el archivo del modelo específico (`.context/opencode.md`, `.context/claude.md`, `.context/gemini.md`)
3. **Check session state**: `sessions/SESSION.md` es un ejemplo público. Para registros reales, usa `sessions/templates/daily-session.md` en tu entorno privado
4. **Engage orchestrator**: Usa `@orchestrator` vía `python scripts/pa.py` para tareas multi-step

## Framework Instruments

- **Context engine** (`.context/`): Todas las decisiones deben alinearse con este directorio
- **Session management** (`sessions/`): El repo público solo contiene plantillas. Los datos reales viven en el repo privado o carpetas ignoradas
- **Control panel**: `python scripts/pa.py` ofrece estado, orquestación y acceso al backlog (`docs/backlog.md`)
- **Decision Engine**: `@decision-engine` en `skills/core/decision-engine/` - Optimización de tokens/contexto local priorizado sobre llamadas remotas
- **Skills & agents**: `skills/` aloja herramientas; `agents/AGENTS.md` documenta roles

## Garantías del Framework para Cada Interacción

El Framework DEBE garantizar automáticamente mediante sus componentes existentes:

### 1. Optimización de Tokens/Quota (Decision Engine)
- **Componente**: `@decision-engine` (`skills/core/decision-engine/`)
- **Mecanismo**: 3-tier routing (LOCAL → DELEGATE → REMOTE)
- **Prioridad**: Contexto local (.context/, codebase, logs) sobre llamadas a IA remota
- **Implementación**: 
  - 8 reglas locales en `local-rules.json` (time_date, math_calc, list_files, show_backlog, etc.)
  - Router en `scripts/route.py` con `--explain`, `--list-rules`, `--list-agents`
  - Selección inteligente de modelos vía `.context/models.md`

### 2. Delegación Orquestada (Clean Context Windows)
- **Componente**: `@orchestrator` (`agents/core/orchestrator/`)
- **Mecanismo**: Progressive Disclosure Protocol
- **Protocolo**:
  1. Leer SOLO metadata al inicio (MASTER.md, SESSION.md, catalog.json)
  2. NO leer AGENT.md files al startup (ahorro de tokens)
  3. Usar `local:get_agent_details` solo cuando se necesite detalle
  4. Dividir tareas en subtareas con dependencias definidas
  5. Ejecutar en paralelo cuando sea seguro
- **Trazabilidad**: Logs en `logs/orchestrator/YYYY-MM-DD.jsonl`
- **Compactación**: `agents/core/session-manager/scripts/compact.py` limita tareas completadas (máx 10)

### 3. Mejora de Prompts (Prompt Enhancement)
- **Componente**: `@prompt-improvement` (`skills/core/prompt-improvement/`)
- **Mecanismo**: Templates estandarizados y refinamiento automático
- **Estándares soportados**:
  - RAG-ready prompts
  - Few-shot prompting
  - JSON structured prompts
  - Internal reasoning (thinking before responding)
  - Guardrails y quality criteria
- **Template recomendado**:
  ```
  Rol: [rol principal]
  Tarea: [que debe hacer]
  Contexto: [datos y fuentes]
  Restricciones: [límites y reglas]
  Formato de salida: [estructura exacta]
  Criterios de calidad: [cómo evaluar]
  ```
- **Acción**: Si instrucciones del usuario son pobres/ambiguas, usar `@prompt-improvement` o `@feature-architect` para refinamiento ANTES de ejecutar

---

## Build/Test/Development Commands

### Inicio del Framework

```bash
# Windows: Iniciar sesión de features (MODO OBLIGATORIO tras /init)
dev.bat

# macOS/Linux: Iniciar sesión de features (MODO OBLIGATORIO tras /init)
./dev.sh

# Alternativa directa
python scripts/pa.py --feature
```

### Context Management

```bash
# Sincronizar contexto entre archivos
python scripts/sync-context.py

# Validar integridad del contexto
python scripts/context-validate.py      # Exit code 0 = éxito

# Crear snapshot del contexto
python scripts/context-version.py snapshot

# Listar snapshots
python scripts/context-version.py list

# Ver estadísticas
python scripts/context-version.py stats

# Limpiar snapshots antiguos
python scripts/context-version.py clean --older 30
```

### Orquestación y Routing

```bash
# Ejecutar orquestación de tarea compleja
python agents/core/orchestrator/scripts/orchestrate.py "<tarea>"

# Probar decision-engine
python skills/core/decision-engine/scripts/route.py "<instrucción>" --explain

# Listar reglas de routing local
python skills/core/decision-engine/scripts/route.py --list-rules

# Listar agentes disponibles
python skills/core/decision-engine/scripts/route.py --list-agents
```

### Testing (Manual)

**Nota:** Este proyecto usa testing manual. No hay pytest/unittest configurado.

```bash
# Testear script directamente
python scripts/<script_name>.py --help

# Ejemplo: Testear i18n
python -c "from scripts.i18n import get_translator; t = get_translator('.'); print(t.t('test'))"

# Validar que script no tiene errores de sintaxis
python -m py_compile scripts/<script_name>.py
```

### Git Workflow y Publicación

```bash
# Sincronizar remotos (privado + público)
python scripts/sync-remotes.py --private-remote origin

# Publicar a release público (sanitizado)
python scripts/publish-release.py --push

# Validar que no hay cambios locales pendientes antes de publicar
git status --porcelain
```

---

## Code Style Guidelines

### Python Standards

- **Python Version:** 3.11+ (mínimo definido en `scripts/install.py` como `MIN_PYTHON = (3, 11)`)
- **Indentation:** 4 spaces (no tabs)
- **Line Length:** 100 characters máximo
- **Encoding:** UTF-8 para todos los archivos

### Naming Conventions

```python
# Variables y funciones: snake_case
def my_function():
    local_variable = "value"

# Constantes: UPPER_CASE a nivel de módulo
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LANGUAGE = "es"
MIN_PYTHON = (3, 11)

# Clases: PascalCase
class Translator:
    def translate(self, text: str) -> str:
        pass

# Funciones privadas: _leading_underscore
def _internal_helper():
    pass
```

### Import Order

```python
#!/usr/bin/env python3
"""Docstring breve del módulo."""

# 1. Standard library imports
import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# 2. Third-party imports (actualmente ninguno en este proyecto)

# 3. Local/project imports
from i18n import get_translator, Translator
from install import configure_preferences, MIN_PYTHON
```

### String Formatting

- **Usar f-strings** para contenido dinámico
- **Usar comillas dobles** para strings (consistente con codebase existente)

```python
# Correcto
message = f"Hello, {name}!"
path = REPO_ROOT / "scripts" / "pa.py"
result = f"[OK] Processed {count} items in {duration:.2f}s"

# Evitar
message = "Hello, {}!".format(name)           # Estilo viejo
path = "%s/scripts/pa.py" % REPO_ROOT        # Formato %
```

### Error Handling

```python
from pathlib import Path

file_path = Path("config.txt")
try:
    content = file_path.read_text(encoding="utf-8")
except FileNotFoundError:
    print(f"[ERROR] File not found: {file_path}")
    return None
except PermissionError:
    print(f"[ERROR] Permission denied: {file_path}")
    return False
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
    return False
```

### Logging Style (Estandarizado)

```python
print("[OK] Operation completed successfully")
print("[INFO] Processing file...")
print("[WARN] Deprecated feature used, consider updating")
print("[ERROR] Failed to execute command: details here")
```

### File Operations (Obligatorio pathlib)

```python
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
config_path = REPO_ROOT / "config" / "i18n.json"

# Lectura
if config_path.exists():
    content = config_path.read_text(encoding="utf-8")

# Escritura (asegurar que existan directorios padre)
config_path.parent.mkdir(parents=True, exist_ok=True)
config_path.write_text(data, encoding="utf-8")
```

### Shebang y Headers

Todos los scripts ejecutables deben incluir:

```python
#!/usr/bin/env python3
"""Breve descripción de lo que hace este módulo."""
```

---

## Remote Strategy (BL-111 / BL-112)

- **`upstream`**: Repo público fijo: `https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git`
  - Solo publicar ejemplos y documentación
  - NUNCA sesiones reales ni datos privados
  
- **`origin`**: Repo privado de trabajo (ej: `Model-Agnostic-AI-Personal-Assistant-Framework-dev`)
  - Almacena trazabilidad, sesiones y datos operativos
  
- **Instalaciones limpias**: `scripts/setup_repo.py` configura `origin` junto al `upstream` fijo

- **Sincronización**: Ejecutar `scripts/sync-remotes.py` para empujar cambios core al `upstream` (público) y tu `origin` (privado) sin exponer logs

## Git Workflow

- **main**: Rama privada de desarrollo (trabajar aquí)
- **public-release**: Rama pública sanitizada (NUNCA trabajar directamente)
- **Branches**: Crear feature branches desde `main` para cambios significativos

### Commit Guidelines

- Escribir mensajes de commit en español (idioma primario: es)
- Usar prefijos para claridad:
  - `feat:` Nueva característica
  - `fix:` Corrección de bug
  - `docs:` Cambios de documentación
  - `refactor:` Refactorización de código
  - `sync:` Sincronización de contexto
  - `agent:` Cambios relacionados a agentes
  - `skill:` Cambios relacionados a skills

---

## Privacy Rules (Estrictas)

1. **Nunca subas sesiones reales a `upstream`**: `sessions/SESSION.md` y los históricos son solo plantillas
2. **Registra tu trabajo**: Usa `sessions/templates/daily-session.md`, copia a un archivo local o workspace privado ignorado
3. **Cierra cada sesión**: Ejecuta `python scripts/sync-remotes.py --private-remote origin` para garantizar trazabilidad en tu remoto privado
4. **Datos sensibles**: Nunca expongas credenciales, API keys o datos personales en commits al upstream

---

## Localization (i18n)

- **Idioma primario**: Spanish (es)
- **Idioma secundario**: English (en)
- **Path de traducciones**: `config/i18n.json`
- **Regla**: Los agentes deben consultar estos archivos para usar terminología consistente

```python
from scripts.i18n import get_translator

t = get_translator(REPO_ROOT)
message = t.t("key", "Default message", variable=value)
```

---

## Multi-Model Orchestration

El framework soporta múltiples herramientas de IA configuradas en `.context/models.md`:

| ID | CLI | Nombre | Fortalezas |
|----|-----|--------|------------|
| claude-sonnet | claude | Claude Sonnet 4 | Código, análisis profundo |
| claude-opus | claude | Claude Opus 4 | Razonamiento complejo |
| gemini-pro | gemini | Gemini 2.5 Pro | Contexto largo, análisis |
| gemini-flash | gemini | Gemini 2.5 Flash | Respuestas rápidas |
| gpt-4 | codex | GPT-4 | General, plugins |
| local-ollama | ollama | Ollama (local) | Privacidad, offline |

### Reglas de Selección

- `código`, `implementar`, `feature` → claude-sonnet
- `debug`, `error`, `bug` → claude-opus
- `rápido`, `buscar`, `investigar` → gemini-flash
- `documento`, `largo`, `análisis` → gemini-pro
- `privado`, `offline`, `local` → local-ollama

---

## Core Agents (7 Total)

Ubicados en `agents/core/` y `agents/custom/`:

| Agente | Estado | Propósito |
|--------|--------|-----------|
| **@session-manager** | OPERATIVO | Gestión de sesiones diarias, recordatorios, cierre de día |
| **@orchestrator** | OPERATIVO | Orquesta tareas multi-step, delega a agents/skills, resume resultados con trazabilidad |
| **@feature-architect** | OPERATIVO | Arquitecto de producto, evalúa y ejecuta features del backlog sin solapamientos |
| **@context-sync** | OPERATIVO | Automatiza sincronización entre MASTER.md y archivos específicos |
| **@github-deployer** | OPERATIVO | Gestión de trazabilidad en GitHub (commits, tags, deploys) |
| **@conflict-guard** | OPERATIVO | Detecta colisiones y solapamientos técnicos antes de integrar features |
| **@brutal-critic** | OPERATIVO | Crítica despiadada de contenido y papers para asegurar calidad máxima |

---

## Core Skills (14 Total)

Ubicados en `skills/core/`:

| Skill | Propósito |
|-------|-----------|
| **@decision-engine** | Routing y optimización (local vs delegate vs remote) |
| **@prompt-improvement** | Mejora de prompts con estándares modernos |
| **@task-management** | Tracking de tareas across workspaces |
| **@context-evaluator** | Evaluación de calidad usando LLM-as-a-Judge |
| **@code-reviewer** | Code reviews, detección de bugs, estándares Clean Code |
| **@content-optimizer** | Optimización SEO y legibilidad |
| **@paper-summarizer** | Análisis de documentos técnicos/papers |
| **@prd-generator** | Generación de Product Requirements Documents |
| **@json-prompt-generator** | Generación de prompts estructurados JSON |
| **@mcp-builder** | Guía para creación de servidores MCP |
| **@ui-ux-pro-max** | Generación de design systems profesionales |
| **@docx** | Manipulación de documentos Word |
| **@pptx** | Creación/edición de PowerPoints |
| **@pdf** | Manipulación de PDFs |
| **@xlsx** | Creación/análisis de spreadsheets |

Para crear nuevos agentes o skills, seguir el estándar en `docs/guides/creating-agents.md`.

---

*Framework Version: 1.6.3-alpha*  
*Stage: Alpha*  
*Single Source of Truth: .context/MASTER.md*
