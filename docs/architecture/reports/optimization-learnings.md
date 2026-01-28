# Optimization Learnings Report

**Fecha**: 2026-01-27
**Estado**: Inicial
**Fuente**: Sesion de trabajo BL-095 a BL-098

---

## Aprendizajes Clave

### 1. Progressive Disclosure en Orquestacion
- **Observacion**: Cargar el `AGENT.md` completo de todos los agentes en el prompt inicial del orquestador consume demasiados tokens innecesarios.
- **Solucion**: Se implemento `catalog.json` con metadatos minimos. El orquestador solo lee las instrucciones completas cuando decide delegar a un agente especifico.
- **Impacto**: Reduccion estimada de ~40% en el prompt de sistema del orquestador.

### 2. Compactacion de Contexto (Session Manager)
- **Observacion**: El archivo `SESSION.md` crece rapidamente en sesiones productivas, superando las 100 lineas y diluyendo la atencion del modelo.
- **Solucion**: Rutina `compact.py` que mantiene solo las ultimas 10-15 tareas completadas y resume el resto en una linea.
- **Impacto**: Mantiene el archivo de sesion dentro de un rango de tokens constante y predecible.

### 3. Dashboard Offline (Zero Latency)
- **Observacion**: Depender de servidores externos para docs o UI introduce latencia y puntos de fallo.
- **Solucion**: `docs/index.html` ahora usa librerias vendorizadas en `docs/lib/`.
- **Impacto**: Carga instantanea y funcionalidad completa sin internet. Ahorro de quota al no tener que "consultar" el estado visualmente via LLM (el usuario lo ve directamente).

## Metricas de Referencia (Estimadas)

| Recurso | Antes | Despues (Optimizacion) |
|---------|-------|------------------------|
| Prompt Orquestador | ~2000 tokens | ~800 tokens |
| Session File | Crecimiento lineal infinito | Crecimiento logaritmico (compactado) |
| UI Dashboard | N/A (Solo texto) | Interactivo (0 tokens LLM) |

## Recomendaciones Futuras

1.  **Cache L1/L2/L3 (BL-093)**: Implementar cuanto antes para evitar releer archivos estaticos (`AGENTS.md`, `SKILLS.md`) en cada turno.
2.  **Log-Rotation**: Mover logs antiguos de `sessions/` a un archivo de archivo mensual para no saturar el `glob`.
