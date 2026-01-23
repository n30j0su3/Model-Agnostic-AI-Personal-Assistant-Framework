# Model-Agnostic AI Personal Assistant Framework v1.4.0

> "One Framework to rule them all, One Context to find them."
> "El Conocimiento verdadero trasciende a lo público".

Un framework estandarizado para interactuar con IAs en modo "Personal Assistant", diseñado para la máxima productividad multidisciplinaria con contexto local y sin vendor lock-in.

![Version](https://img.shields.io/badge/version-1.4.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Agnostic](https://img.shields.io/badge/Model-Agnostic-orange)

## 🚀 Características Principales

- 🤖 **Multi-Tool Workflow**: Trabaja con OpenCode, Claude Code, Gemini CLI y Codex simultáneamente.
- 📁 **Contexto Local**: Todo tu conocimiento reside en archivos `.md` bajo tu control.
- 🌐 **Multidisciplinario**: 6 Workspaces pre-configurados (Personal, Professional, Research, Content, Development, Homelab).
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

## 🧰 Pre-requisitos (Hardware y Software)

- **Hardware minimo**: CPU 4 nucleos, 8 GB RAM, 2 GB libres en disco.
- **Hardware recomendado**: CPU 8 nucleos, 16 GB RAM, SSD.
- **GPU (opcional)**: Recomendada si usaras modelos locales o flujos pesados.
- **Sistema operativo**: Windows 10/11, macOS 12+ o Linux moderno.
- **Software base**: Git 2.30+, Python 3.11+ y un editor (VS Code u otro).
- **Cuentas IA**: Acceso a proveedores como OpenAI, Anthropic o Google si usaras sus APIs.

## 🧭 Instalación Completa (Para Dummies)

1. **Instala Git** desde https://git-scm.com y reinicia la terminal.
2. **Instala Python 3.11+** desde https://www.python.org y confirma con `python --version`.
3. **Crea una carpeta** para el proyecto y abre una terminal dentro.
4. **Clona el repo**:
   ```bash
   git clone https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git
   ```
5. **Entra a la carpeta**:
   ```bash
   cd Model-Agnostic-AI-Personal-Assistant-Framework
   ```
6. **Configura tu perfil** editando `.context/MASTER.md`.
7. **Sincroniza el contexto**:
   ```bash
   python scripts/sync-context.py
   ```
8. **Verifica** que se generaron archivos de contexto en `.context/` y `sessions/`.
9. **Listo**: ya puedes iniciar sesiones y activar skills.

## 🤖 Instalación de LLMs (IA) Paso a Paso

1. **Crea cuentas** en los proveedores que vayas a usar (OpenAI, Anthropic, Google, etc.).
2. **Obtén tus API Keys** desde el panel de cada proveedor.
3. **Instala las CLIs** oficiales (OpenCode, Claude Code, Gemini CLI, Codex) siguiendo sus docs.
4. **Configura las variables de entorno** con tus claves.
   ```bash
   # macOS/Linux
   export OPENAI_API_KEY="<TU_API_KEY>"
   export ANTHROPIC_API_KEY="<TU_API_KEY>"
   export GEMINI_API_KEY="<TU_API_KEY>"
   ```
   ```powershell
   # Windows PowerShell
   setx OPENAI_API_KEY "<TU_API_KEY>"
   setx ANTHROPIC_API_KEY "<TU_API_KEY>"
   setx GEMINI_API_KEY "<TU_API_KEY>"
   ```
5. **Prueba cada CLI** con un comando simple (por ejemplo `--version` o un prompt corto).
6. **Vincula el contexto** ejecutando `python scripts/sync-context.py` si aun no lo hiciste.
7. **Valida la configuracion LLM** con el instalador:
   ```bash
   python scripts/install.py --llm
   ```

### 🧠 Modelos locales (Opcional)

- **Ollama (Windows/macOS/Linux)**
  1. Instala desde https://ollama.com
  2. Descarga un modelo:
     ```bash
     ollama pull llama3
     ```
  3. Prueba el modelo:
     ```bash
     ollama run llama3
     ```
  4. Configura tu herramienta LLM para apuntar al endpoint local que expone Ollama.

- **LM Studio (Windows/macOS/Linux)**
  1. Instala desde https://lmstudio.ai
  2. Descarga un modelo desde la app.
  3. Activa el servidor local desde la interfaz y usa el endpoint que te muestre la app.

## 🧩 Instalador Todo-en-Uno (Comando Unico)

```powershell
# Windows PowerShell
git clone https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git; cd Model-Agnostic-AI-Personal-Assistant-Framework; python scripts/install.py
```

```bash
# macOS/Linux
git clone https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git && cd Model-Agnostic-AI-Personal-Assistant-Framework && python3 scripts/install.py
```

Luego edita `.context/MASTER.md` con tus preferencias personales.

## 🐍 Instalador Python (Multiplataforma)

- **Windows**:
  ```powershell
  python scripts/install.py
  # o
  py -3 scripts/install.py
  ```
- **macOS/Linux**:
  ```bash
  python3 scripts/install.py
  ```

Para validar LLMs agrega `--llm`.

## 🧪 Instalador por SO (Opcional)

- **Windows PowerShell**:
  ```powershell
  .\scripts\install.ps1
  ```
- **macOS/Linux**:
  ```bash
  bash scripts/install.sh
  ```

## ❓ FAQ Basico

- **¿Necesito saber programar?** No. Esta guia esta pensada para principiantes.
- **¿Donde vive mi conocimiento?** En archivos `.md` dentro de `.context/`, bajo tu control.
- **¿Que pasa si no tengo API key?** Puedes usar el framework, pero sin ejecutar modelos remotos.
- **¿Como actualizo el framework?** Entra al repo y ejecuta `git pull`.
- **¿Esto es gratis?** El framework es MIT, pero los proveedores de IA pueden cobrar por uso.

## 🙏 Agradecimientos

Gracias a Dios por la Gracia, la Revelacion y el Discernimiento necesarios para llegar a la construccion del framework, a mi familia por su amor y paciencia, y al resto de mis seres amados y queridos (ellos saben quienes son, se los he dicho muchas veces).

## 📖 Documentación

La documentación completa está disponible en la carpeta `docs/`. Sigue el estándar de Mintlify para una experiencia de lectura superior.

---
Hecho con ❤️ por el equipo de **Advanced Agentic Coding**.
Basado en las filosofías de **theNetworkChuck**.
