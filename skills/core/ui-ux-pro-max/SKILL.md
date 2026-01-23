---
name: ui-ux-pro-max
description: Inteligencia de diseño profesional. Genera sistemas de diseño (colores, tipografía, efectos) basados en reglas de industria y UX. Úsalo para landing pages, dashboards y interfaces complejas.
license: Proprietary
metadata:
  author: nextlevelbuilder
  version: "2.0"
compatibility: OpenCode, Claude Code, Cursor, Windsurf, Trae.
---

# UI/UX Pro Max Skill

Este skill añade una capa de razonamiento estético y funcional a las tareas de desarrollo de interfaces.

## Capacidades
- **Diseño Inteligente**: Genera un sistema de diseño (Design System) en segundos analizando el nicho de mercado.
- **67 Estilos de UI**: Glassmorphism, Brutalism, Minimalist, AI-Native, etc.
- **100 Reglas de Industria**: Reglas específicas para SaaS, Fintech, Healthcare, E-commerce, etc.
- **Accesibilidad**: Validación WCAG AA integrada.

## Instrucciones para la IA
Cuando el usuario pida construir una interfaz:
1. Invoca el motor de razonamiento de `ui-ux-pro-max`.
2. Presenta el sistema de diseño recomendado (Colores, Tipografía, Patrones).
3. Implementa el código (HTML/Tailwind, React, etc.) siguiendo estas reglas.

## Comandos Técnicos (vía CLI)
```bash
# Generar sistema de diseño (Ejemplo SaaS)
python .opencode/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" --design-system
```

## Referencias
- `MASTER.md` del sistema de diseño una vez generado.
- Documentación oficial en https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
