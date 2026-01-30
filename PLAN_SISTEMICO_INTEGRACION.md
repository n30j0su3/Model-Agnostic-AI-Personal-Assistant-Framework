# Plan Sistémico de Integración: Trazabilidad, Sincronización y Portabilidad

**Versión del Plan:** 1.0.0  
**Fecha:** 2026-01-29  
**Objetivos del Backlog:** BL-013, BL-014, BL-016, BL-018, BL-086

---

## 1. Fase de Investigación: Unificación de Historial (BL-013, BL-086)

### Contexto Actual
El historial vive fragmentado en `sessions/` en archivos Markdown. Consultar sesiones pasadas consume demasiados tokens si se leen archivos completos.

### Propuesta Técnica
- **Arquitectura de Memoria:** Adoptar el patrón de `OmniMemory` ya existente.
- **Formato de Registro:** Implementar `scripts/history_engine.py` que registre cada interacción en `sessions/history.jsonl`.
- **Estructura del Log:** `{"timestamp": "ISO", "agent": "name", "prompt": "...", "summary": "...", "tokens": 0, "status": "ok"}`.
- **Indexación:** Crear un `index.json` ligero que mapee fechas con offsets del archivo JSONL para evitar cargar todo el archivo.

---

## 2. Fase de Implementación: Pipeline de Sincronización Coherente (BL-014)

### Mejoras a `scripts/sync-context.py`
- **Validación de Esquemas:** Integrar un check de presencia de secciones obligatorias antes de propagar cambios de `MASTER.md` a los perfiles de herramientas.
- **Gestión de Estados:** Si el contexto está "corrupto" (marcadores rotos), el script debe entrar en modo recuperación en lugar de apendizar basura.
- **Pre-sync Hook:** Ejecutar automáticamente `scripts/context-validate.py` antes de iniciar la sincronización.

---

## 3. Fase de Estandarización: Estructura y Portabilidad (BL-016, BL-018)

### Estructura Extensible (BL-016)
- **Aislamiento Core:** Reforzar la distinción entre `agents/core/` y `agents/custom/`.
- **Manifest de Integridad:** Crear un archivo `manifest.json` en la raíz que liste los archivos protegidos que el instalador/actualizador no debe sobreescribir si han sido modificados por el usuario.

### Compatibilidad Multiplataforma (BL-018)
- **Abstracción de Comandos:** Crear una clase `PlatformHelper` en un nuevo script `scripts/utils.py`.
- **Refactorización de Rutas:** Reemplazar todas las concatenaciones de strings con `/` o `\` por operadores de `pathlib.Path`.
- **Correcciones Urgentes:**
    - Sustituir `os.system('cls')` por una función que detecte `nt` o `posix`.
    - Estandarizar el uso de `sys.executable` para llamadas a subprocesos Python.

---

## 4. Cronograma de Ejecución

| Fase | Tarea | Agente Responsable | Prioridad |
| :--- | :--- | :--- | :--- |
| 1 | Refactorización Multiplataforma (`pathlib` + `utils.py`) | Gemini (Orquestador) | Alta |
| 2 | Motor de Historial JSONL (`history_engine.py`) | CODEX (Implementador) | Alta |
| 3 | Robustez de Sincronización (Hooks + Validation) | Gemini (Orquestador) | Media |
| 4 | Dashboard Integration (Vista de Historial) | CODEX (Implementador) | Media |

---

## 5. Criterios de Aceptación
- [ ] `pa.py` se ejecuta sin errores de ruta en Linux/macOS.
- [ ] Cada interacción de la IA genera una entrada en `sessions/history.jsonl`.
- [ ] La sincronización de contexto falla con un mensaje claro si `MASTER.md` está vacío.
- [ ] Los agentes pueden consultar el historial de los últimos 3 días sin leer archivos MD pesados.

---

*Plan generado automáticamente por el Orquestador Framework.
