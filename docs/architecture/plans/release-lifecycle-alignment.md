# Software Release Life Cycle (SRLC) Alignment Plan

**Fecha**: 2026-01-27
**Estado**: Implementando
**Prioridad**: Alta (Core Consistency)

---

## Diagnostico Actual

El framework se encuentra en la version `1.6.3`. Aunque el numero sugiere un producto maduro (Major 1), el ritmo de desarrollo, la falta de estabilidad en las APIs internas y la ausencia de una suite de pruebas completa indican que el estado real es **ALPHA**.

---

## Estrategia de Versionado (2026 Standard)

A partir de hoy, seguiremos estrictamente el Ciclo de Vida de Lanzamiento de Software, integrando etiquetas de estado en el versionado SemVer.

### 1. Etapas Definidas

| Etapa | Rango de Version | Foco | Estabilidad |
|-------|------------------|------|-------------|
| **Alpha** | `1.x.x-alpha` | Funcionalidad Core, Arquitectura | Inestable (Breaking changes frecuentes) |
| **Beta** | `1.x.x-beta` | UX, Refinamiento, Docs, Performance | Parcial (Feature freeze, solo bugs) |
| **RC (Release Candidate)** | `1.x.x-rc` | Pulido final, Seguridad | Alta (Candidato a Stable) |
| **Stable** | `2.x.x` | Produccion, Soporte Largo Plazo | Produccion |

### 2. Estado del Proyecto: ALPHA

Declaramos oficialmente que el framework esta en fase **ALPHA**.
- **Proximo hito**: Completar CORE VITALS del backlog.
- **Transicion a Beta**: Estimada para la version `1.8.0` o cuando el Dashboard UX (BL-085) este operativo.

---

## Acciones de Implementacion

### A. Marcado de Repositorio
- Actualizar `README.md` con el badge de estado.
- Actualizar `CHANGELOG.md` con la declaracion de etapa Alpha.
- Modificar `VERSION` para incluir sufijo `-alpha` (opcional, evaluando impacto en scripts de update). *Decision: Mantener SemVer puro en el archivo VERSION pero documentar etapa en metadatos para evitar romper scripts de bash/cmd.*

### B. Canales de Actualizacion (Update Channels)
El script `scripts/update.py` se modificara para soportar:
- `stable`: Solo versiones marcadas como estables.
- `canary`: (Actual por defecto) Ultimos commits/alpha.

### C. Trazabilidad de Cambios
Cada entrada en el `CHANGELOG.md` debe especificar si incluye **Breaking Changes**.

---

## Criterios de Calidad para Releases

1. **Alpha -> Beta**:
   - [ ] Cobertura de "Core Vitals" > 90%.
   - [ ] Estabilidad de `scripts/pa.py` probada en 3 entornos (Win/Mac/Linux).
   - [ ] Sin "todo" criticos en el codigo core.

2. **Beta -> RC**:
   - [ ] Documentacion completa para usuario no tecnico.
   - [ ] Dashboard funcional sin errores de consola.
   - [ ] Auditoria de seguridad de API Keys completada.

---

## Notas de Auditoria

- Se priorizara la transparencia: el usuario siempre sabra que esta usando una version Alpha.
- Se evitara el "version bloat": no incrementaremos Major hasta un cambio radical de paradigma.
