# Ejecucion de Feature BL-XXX

Prerequisitos:

1. La feature paso The Filter
2. Contexto claro (no hay dudas abiertas)
3. Dependencias identificadas

Pasos:

1. Generar FAR (ver `docs/architecture/feature-analysis-report.mdx`).
2. Ejecutar conflict-guard y registrar resultado en el FAR.
3. Marcar BL-XXX como "En Progreso" con `tools/backlog_manager.py`.
4. Implementar cambios.
5. Actualizar documentacion relevante.
6. Marcar BL-XXX como "Hecho".
7. Agregar entrada al historial.
8. Proponer version SemVer si aplica.

Notas:
- Si tocaste conflict-guard, ejecuta los smoke tests en docs/architecture/conflict-guard-interface.mdx.

Entrega:

- Resumen del cambio
- Archivos tocados
- Notas de verificacion
