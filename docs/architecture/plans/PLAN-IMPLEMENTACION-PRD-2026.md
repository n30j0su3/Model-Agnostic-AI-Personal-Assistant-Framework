# Plan de Implementación: Framework PRD 2026
**Autor:** @feature-architect | **Fecha:** 2026-01-28
**Objetivo:** Desplegar las capacidades definidas en el PRD 2026 (BL-112, BL-085, BL-093).

## Fase 1: Cimientos de Seguridad (BL-112)
**Objetivo:** Garantizar que el desarrollo paralelo sea seguro y que la privacidad del usuario esté protegida por defecto.

- [ ] **Estrategia Dual-Remote en `setup_repo.py`**:
    - Modificar el menú de inicialización para ofrecer "Modo Híbrido".
    - Configurar `origin` (Privado) para todo el contenido.
    - Configurar `upstream` (Público) solo para pull de updates.
    - Script de validación `.gitignore` estricto para `sessions/` y `logs/`.

- [ ] **Estandarización de PRs (BL-111)**:
    - Crear plantilla de PR en `.github/PULL_REQUEST_TEMPLATE.md` (local).
    - Crear script de pre-commit o hook que valide "No-Pollution".

## Fase 2: El Mago de Configuración (BL-085)
**Objetivo:** Mejorar la experiencia de `pa.bat` para que sea un verdadero asistente de instalación.

- [ ] **Mejora de `pa.bat`**:
    - Convertirlo en un menú interactivo antes de lanzar Python si es posible, o delegar rápido a un script TUI.
    - Detección robusta de dependencias.

- [ ] **Wizard Interactivo (`scripts/wizard.py`)**:
    - Nuevo script para guiar paso a paso:
        1. Selección de Idioma (persistente).
        2. Configuración de Workspaces (crear carpetas).
        3. Configuración de Identidad AI (Nombre, Estilo).

## Fase 3: Operación Inteligente (Core-Agents)
**Objetivo:** Que el framework "piense" antes de actuar por defecto.

- [ ] **Orquestación por Defecto**:
    - Modificar `pa.py` para que el modo interactivo pase los inputs al `@orchestrator` en lugar de ir directo al LLM, o dar la opción clara.

- [ ] **Base de Conocimiento Local (BL-093)**:
    - Implementar almacenamiento estructurado de "Thinking" en `sessions/`.

## Fase 4: Dashboard y Frontend
**Objetivo:** Visualización y control sin comandos.

- [ ] **Dashboard Reactivo**:
    - Actualizar `dashboard.html` para leer estados desde archivos locales (JSON generation scripts).

---

## Ejecución Inmediata
Se procederá con la **Fase 1** (Dual-Remote) y **Fase 2** (Wizard) en esta sesión.
