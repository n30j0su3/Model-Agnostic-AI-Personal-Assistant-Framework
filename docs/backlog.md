# Backlog del Framework

Ultima actualizacion: 2026-01-26

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
- 2026-01-23: Se agrego item BL-031 (workspace Homelab).
- 2026-01-23: Release 1.4.0 (workspace Homelab y documentacion).
- 2026-01-23: Se agrego item BL-032 (plantillas Homelab).
- 2026-01-23: Se agregaron items BL-033 a BL-038 (README contexto, calendario, input multicanal, skills de contenido).
- 2026-01-23: Se implemento BL-029 (selector de instalacion basica vs pro).
- 2026-01-23: Se implemento BL-030 (configuracion guiada del perfil al instalar).
- 2026-01-23: Se implemento BL-033 (contexto user-friendly en README).
- 2026-01-23: Se ajustaron prioridades BL-008, BL-009 y BL-032.
- 2026-01-23: Se implemento BL-008 (orquestacion multi-modelo opcional).
- 2026-01-23: Se implemento BL-039 (panel de control global pa.py).
- 2026-01-23: Se implementaron BL-040 y BL-041 (dashboard y agradecimientos).
- 2026-01-23: Se implemento BL-009 (gestion de contexto local versionado).
- 2026-01-23: Se agrego item BL-042 (modulo de pruebas del framework).
- 2026-01-24: Se agrego item BL-043 (seccion rapida de caracteristicas y despliegue seguro).
- 2026-01-24: Se agregaron items BL-044 a BL-057 (prompting, research, mantenimiento, branding y expansion).
- 2026-01-24: Se implemento BL-043 (flujo documentado y vista filtrada del backlog).
- 2026-01-24: Se agrego item BL-058 (tips rapidos de uso del framework).
- 2026-01-24: Release 1.5.0 (auto-actualizacion, backlog en Feature Session y setup inteligente de repositorio).
- 2026-01-24: Se agrego item BL-063 (setup inteligente de repositorio).
- 2026-01-24: Release 1.6.0 (i18n ES/EN, selector CLI y init robusto).
- 2026-01-24: Release 1.6.1 (launcher Windows instala dependencias).
- 2026-01-24: Release 1.6.2 (launcher Windows robusto sin cierre).
- 2026-01-24: Release 1.6.3 (bootstrap Node.js para OpenCode).
- 2026-01-25: Se agrego item BL-067 (auditoria UX instaladores/docs y mensajes).
- 2026-01-25: Se agrego item BL-068 (agent feature-architect).
- 2026-01-25: Se implemento BL-044 (skill prompt-improvement con referencias y update programable).
- 2026-01-25: Se implemento BL-046 (desinstalador seguro con modos completo/parcial).
- 2026-01-25: Se implemento BL-061 (historico configurable local/online con soporte a repos locales).
- 2026-01-26: Se agregaron items BL-069 a BL-082 (core-logic, evaluaciones y nuevas skills).
- 2026-01-26: Se agrego prioridad CORE VITALS y se reasignaron items esenciales.
- 2026-01-26: Limpieza de backlog (fusiones, dependencias y renombres).
- 2026-01-26: Se implemento BL-060 (decision engine local-first).
- 2026-01-26: Se agrego item BL-083 (acceso a documentacion local).
- 2026-01-26: Se implementaron BL-083 y BL-084 (docs offline y assets locales).
- 2026-01-26: Se agrego item BL-085 (UX docs/dashboard no tecnico).

| ID | Item | Prioridad | Estado | Criterios de aceptacion |
| --- | --- | --- | --- | --- |
| BL-001 | Guia "para dummies" con prerequisitos de hardware y software | Alta | Hecho | README incluye requisitos claros y un paso a paso de instalacion completa |
| BL-002 | Instalacion de LLMs (IA) paso a paso | Alta | Hecho | README detalla cuentas, API keys, configuracion y validacion basica |
| BL-003 | Instalador todo-en-uno en comando unico | Alta | Hecho | README incluye un comando para Windows y otro para macOS/Linux |
| BL-004 | FAQ basico para usuarios no tecnicos | Alta | Hecho | README incluye al menos 5 preguntas frecuentes con respuestas cortas |
| BL-005 | Frase insignia en README | Media | Hecho | La frase aparece en la introduccion del README |
| BL-006 | Agradecimientos formales en README | Media | Hecho | Se incluye seccion de agradecimientos con el texto solicitado |
| BL-007 | Skill json-prompt-generator | Alta | Hecho | Skill creado en `skills/core/json-prompt-generator` con instrucciones y ejemplo |
| BL-008 | Orquestacion multi-modelo con conmutacion rapida | Alta | Hecho | Flujo unificado documentado para OpenCode, Claude, Gemini y Codex |
| BL-009 | Gestion de contexto local versionado | Alta | Hecho | Estructura `.context/` definida y versionada sin lock-in |
| BL-010 | Workspaces multidisciplinarios aislados | Media | Pendiente | Workspaces claramente separados por disciplina y documentados |
| BL-011 | Sistema de agentes especializados con roles claros | Media | Pendiente | Catalogo de agentes con responsabilidades y uso recomendado |
| BL-012 | Skills modulares para tareas recurrentes | Media | Pendiente | Libreria de skills con index y versionado actualizado |
| BL-013 | Trazabilidad diaria automatica | Media | Pendiente | Sesiones diarias registradas y accesibles desde `sessions/`. Dependencias: BL-014 |
| BL-014 | Pipeline de sincronizacion coherente | Media | Pendiente | Script de sync mantiene coherencia entre herramientas e incluye automatizaciones en `scripts/` |
| BL-015 | Documentacion integrada estilo Mintlify | Baja | Pendiente | Docs consistentes y navegables en `docs/` |
| BL-016 | Estructura de carpetas estable y extensible | Baja | Pendiente | Convenciones de nombres y ubicaciones estandarizadas |
| BL-017 | Scripts de automatizacion para sync y normalizacion | N/A | N/A | Unificado con BL-014 |
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
| BL-029 | Selector de instalacion basica vs pro | Alta | Hecho | Instalador ofrece seleccion de perfil en primera ejecucion |
| BL-030 | Configuracion guiada del perfil al instalar | Alta | Hecho | Permite configurar `.context/MASTER.md` ahora o despues con preferencias avanzadas opcionales |
| BL-031 | Agregar workspace Homelab | Alta | Hecho | Workspace creado y documentado en `workspaces/homelab/` |
| BL-032 | Plantillas Homelab (inventario, servicios, mantenimiento) | Baja | Pendiente | Plantillas listas para completar en `workspaces/homelab/` |
| BL-033 | Integrar contexto “user-friendly” al inicio del README | Alta | Hecho | README incluye el texto completo sobre “sin MIEDO” y paradigma AI/IA |
| BL-034 | Sistema de calendario, control y estimacion de actividades | Media | Pendiente | Integra skills/tecnologias open-source y evalua integracion con Google/Outlook |
| BL-035 | Sistema de entrada multi-canal de ideas/tareas/objetivos | Media | Pendiente | Ingreso via WhatsApp/Telegram con clasificacion por workspace y deteccion de recursos faltantes; contexto guardado en .md |
| BL-036 | Integrar skill writing-style | Baja | Pendiente | Skill integrada desde https://github.com/jrenaldi79/writing-style |
| BL-037 | Integrar skill agentman-social-media con tono configurable | Baja | Pendiente | Skill integrada y permite elegir tono/intencion acorde al contexto |
| BL-038 | Integrar skill running-marketing-campaigns-agent-skill | Baja | Pendiente | Skill integrada desde https://github.com/SpillwaveSolutions/running-marketing-campaigns-agent-skill |
| BL-039 | Panel de control global para configuraciones | Alta | Hecho | Script `scripts/pa.py` permite gestionar sincronizacion, preferencias, orquestacion y launcher |
| BL-040 | Documentar dashboard.html en README | Alta | Hecho | Seccion Documentacion incluye proposito y uso de `dashboard.html` |
| BL-041 | Agradecimientos a NetworkChuck | Alta | Hecho | Seccion de agradecimientos menciona a NetworkChuck con cita |
| BL-042 | Modulo de pruebas del framework configurable | Media | Pendiente | Sistema de pruebas ajustado a preferencias del usuario para validar el framework |
| BL-043 | Seccion rapida de caracteristicas (dogfooding, backlog y despliegue seguro) | Alta | Hecho | Cada seccion revisa backlog, documenta cambios, usa el framework y valida privacidad antes de deploy |
| BL-044 | Integrar skill de prompt-improvement con estandares modernos | Alta | Hecho | Skill con buenas practicas (CoT, RAG, few-shot, JSON prompts), referencias confiables y actualizacion programable por usuario |
| BL-045 | Planear framework/skill de investigacion multiproposito | Alta | Pendiente | Skill global con modos de investigacion (sencilla, deep-research, profesional) y flujo guiado opcional |
| BL-046 | Integrar desinstalador del framework (completo o parcial) | Alta | Hecho | Proceso seguro de desinstalacion documentado y con opcion parcial |
| BL-047 | TaskManager para programar mantenimiento y automatizaciones | Alta | Pendiente | Sistema para planear/personalizar ejecucion de scripts de mantenimiento y automatizaciones, incluye job cada 30 dias |
| BL-048 | Planear/Integrar script de mantenimiento del framework (cada 30 dias) | N/A | N/A | Unificado con BL-047 |
| BL-049 | Planear/Integrar script de verificacion de jerarquia y overlaps | N/A | N/A | Unificado con BL-069 |
| BL-050 | Guia de obtencion de API keys (OpenAI/Gemini/Claude/OpenRouter) | Alta | Pendiente | Docs para OpenAI, Gemini, Claude, OpenRouter y similares con pasos claros |
| BL-051 | Mantener `dashboard.html` actualizado | Alta | Pendiente | `dashboard.html` siempre actualizado, con enlaces internos/externos y narrativa completa. Insumos: BL-043, BL-040 |
| BL-052 | Integrar marca "FreakingJSON" (ASCII/Metadata/Theme) | Media | Pendiente | Integrar "FreakingJSON" en instaladores (ASCII alta compatibilidad), docs y metadatos por defecto. Usar estandares opensource actuales para colores/personalizacion user-friendly |
| BL-053 | Crear themes de personalizacion por workspaces y agentes | Media | Pendiente | Temas seleccionables con buenas practicas y guia de uso. Dependencias: BL-052 |
| BL-054 | Planear sistema de plugins para expandir capacidades del framework | Media | Pendiente | Arquitectura de plugins basada en estandares opensource actualizados |
| BL-055 | Planear skills de video editing/creacion opensource | Baja | Pendiente | Roadmap de skills con herramientas como FFmpeg y NCA-Toolkit |
| BL-056 | Planear skill de automatizacion de contenido multiplataforma | Baja | Pendiente | Automatizacion con noticias, videos, transcripciones, TTS, imagenes y APIs |
| BL-057 | Planear skill/framework para romhacks multiplataforma | Baja | Pendiente | Flujo de edicion, parcheo y build con recursos opensource y docs publicas |
| BL-058 | Integrar tips rapidos/recomendados de uso del framework | N/A | N/A | Unificado con BL-081 |
| BL-059 | Actualizacion automatica del framework (configurable/programable) | Alta | Hecho | Script de actualizacion con fallback sin Git y opcion en pa.py |
| BL-060 | CORE SKILL de evaluacion/decision de instrucciones (local-first) | CORE VITALS | Hecho | Skill creada en `skills/core/decision-engine` con router local-first, reglas y delegacion. Plan tecnico en `docs/architecture/decision-engine.mdx` |
| BL-061 | Historico de contexto configurable (online/local) | Media | Hecho | Usuario puede elegir entre sincronizacion online (GitHub) o local para historicos y contexto, reduciendo barreras de entrada |
| BL-062 | Unificado con BL-050 | N/A | N/A | La tarea de documentar tutoriales de API Keys se fusiona con el item existente BL-050 |
| BL-063 | Setup inteligente de repositorio (GitHub/local/sandbox) | Alta | Hecho | Flujo interactivo en el instalador con cascada gh -> PyGithub -> API nativa |
| BL-064 | Selector de idioma ES/EN en instalador y panel | Alta | Hecho | Framework permite elegir idioma y usa strings centralizados en config/i18n.json |
| BL-065 | Seleccion de CLI por defecto + asistencia de instalacion | Alta | Hecho | Instalador detecta CLIs, permite elegir default y ofrece instalar OpenCode |
| BL-066 | Inicializacion robusta de contexto IA | Alta | Hecho | .cursorrules y AI_INSTRUCTIONS.md apuntan a .context/ y launcher imprime prompt magico |
| BL-067 | Auditoria UX end-to-end (instaladores, mensajes y docs) | Alta | Pendiente | Experiencia guiada, clara y amigable para usuarios no tecnicos en instalacion, actualizacion y uso inicial |
| BL-068 | Agent @feature-architect para Feature Sessions | CORE VITALS | Pendiente | Agent creado con bootstrap, clarificacion, evaluacion, ejecucion y herramienta de backlog compatible |
| BL-069 | CORE-LOGIC: validar overlaps/conflictos al integrar skills/dependencias | CORE VITALS | Pendiente | Feature-architect verifica rutas y conflictos funcionales antes de integrar una nueva feature. Incluye verificacion periodica (script) y dependencias: BL-068 |
| BL-070 | Evaluar skills ralph/prd para reforzar agente feature-architect | Alta | Pendiente | Comparativa e integracion solo si mejora robustez segun estandares actuales. Dependencias: BL-068 |
| BL-071 | Evaluar skills session-logs/context-files/multi-tool para session-manager | CORE VITALS | Pendiente | Integracion si aporta mejoras verificables y compatibles. Dependencias: BL-060 |
| BL-072 | Evaluar si session-tracking debe integrarse en session-manager | CORE VITALS | Pendiente | Decision documentada y criterio alineado a la filosofia del framework. Dependencias: BL-060 |
| BL-073 | Evaluar skills git/github para mejorar github-deployer | CORE VITALS | Pendiente | Integracion si aporta mejoras verificables y compatibles. Dependencias: BL-060 |
| BL-074 | Implementar core-skill de data visualization (Seaborn/Matplotlib) | Alta | Pendiente | Skill documentada y alineada a estandares opensource actuales |
| BL-075 | Implementar core-skill "council of the wise" | Alta | Pendiente | Skill integrada desde fuente indicada y documentada |
| BL-076 | Integrar summarize + transcript-to-content (sin referencia a clawdbot) | Media | Pendiente | Skills integradas sin referencia directa a clawdbot en docs, incluye transcripcion de contenido |
| BL-077 | Implementar core-skill de transcripcion de contenido | N/A | N/A | Unificado con BL-076 |
| BL-078 | Evaluar/Integrar skill/agent Google Workspace (No Cloud Console) | Media | Pendiente | Opcion para Gmail/Calendar/Drive/Docs/Sheets documentada |
| BL-079 | Instalador: ofrecer instalar CLI elegido o guiar instalacion (pa.bat) | Baja | Pendiente | Opcion en instalador con links internos/externos |
| BL-080 | Integrar buenas practicas de uso Gemini (docs) | Baja | Pendiente | Guia basada en la doc indicada y adaptada al framework. Dependencias: BL-050 |
| BL-081 | Integrar referencias de cheat-sheet/troubleshooting y tips rapidos | Baja | Pendiente | Docs y dashboard incluyen seccion de tips rapidos y referencias relevantes |
| BL-082 | Integrar gestor/banco de skills instalables | Baja | Pendiente | Sistema para buscar/instalar skills sin conflictos ni overlaps |
| BL-083 | Acceso a documentacion local del framework | Baja | Hecho | Cockpit carga docs locales con manifest (`docs/docs_manifest.js`) y visor integrado |
| BL-084 | Vendoring de assets offline para docs/cockpit | CORE VITALS | Hecho | Assets locales en `docs/lib/` y script de descarga `scripts/vendor_assets.py` |
| BL-085 | UX docs/dashboard no tecnico (sin dependencias extra) | CORE VITALS | Pendiente | Dashboard ofrece opciones claras, abre archivos sin confusion y funciona en navegador sin requerir Python o instalaciones ocultas |
