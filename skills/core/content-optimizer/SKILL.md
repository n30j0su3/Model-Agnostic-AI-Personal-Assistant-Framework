---
name: content-optimizer
description: Optimiza borradores de texto para SEO, legibilidad y engagement. Ajusta el tono de voz y la estructura del contenido. Úsalo en el workspace @content.
license: MIT
metadata:
  author: opencode
  version: "1.0"
compatibility: OpenCode, Claude Code, Gemini CLI, Codex
---

# Content Optimizer Skill

Habilidad diseñada para maximizar el alcance y la claridad de tus textos.

## Instrucciones para la IA

### 1. Checklist de Optimización
- **SEO**: Presencia de palabras clave, etiquetas H1-H3 lógicas, meta-descripciones.
- **Legibilidad**: Uso de voz activa, párrafos cortos, evitar jerga innecesaria.
- **Engagement**: Fuerza del Hook inicial, CTA (Call to Action) claro.
- **Tono**: Asegurar que coincida con la voz definida en `workspaces/content/CONTEXT.md`.

### 2. Flujo de Trabajo
1. Analizar el borrador actual en `workspaces/content/drafts/`.
2. Proporcionar un reporte de "Antes y Después".
3. Sugerir 3 variaciones de títulos (Hooks) de alto impacto.

### 3. Comandos Soportados
- "Optimiza este post para SEO"
- "Revisa el tono de este guion"
- "Dame 5 ideas de títulos para @archivo"

## Scripts
- `scripts/seo-checker.py`: Script para validar densidad de keywords y estructura.
