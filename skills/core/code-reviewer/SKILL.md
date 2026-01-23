---
name: code-reviewer
description: Realiza revisiones de código profundas, identifica bugs, sugiere mejoras de arquitectura y asegura el cumplimiento de estándares de Clean Code. Úsalo en el workspace @development.
license: MIT
metadata:
  author: opencode
  version: "1.0"
compatibility: OpenCode, Claude Code, Gemini CLI, Codex
---

# Code Reviewer Skill

Habilidad especializada en la mejora continua de la calidad del software.

## Instrucciones para la IA

### 1. Dimensiones de la Revisión
Al revisar código, analiza:
- **Legibilidad**: Nombramiento de variables, longitud de funciones, comentarios útiles.
- **Seguridad**: Detección de secretos expuestos, inyecciones de SQL, XSS, etc.
- **Rendimiento**: Bucles ineficientes, fugas de memoria, optimización de consultas.
- **Arquitectura**: Acoplamiento, cohesión y patrones de diseño.

### 2. Formato de Salida
Presenta los hallazgos en una tabla o lista estructurada:
- **Nivel**: [Crítico | Advertencia | Mejora]
- **Ubicación**: Archivo y línea.
- **Descripción**: Explicación del problema.
- **Sugerencia**: Código corregido o propuesta de cambio.

### 3. Comandos Soportados
- "Revisa este archivo @archivo"
- "¿Hay algún problema de seguridad en este código?"
- "Refactoriza esta función para que sea más limpia"

## Scripts
- `scripts/review-helper.py`: Utilidad para formatear reportes de revisión.
