# Evaluacion de Feature Propuesta

Entrada:
- Descripcion de la feature: [DESCRIPCION]

Paso 0: Clarificacion (obligatorio si falta info)

- [ ] Problema claro
- [ ] Usuario objetivo
- [ ] Criterios de exito
- [ ] Prioridad definida

Si falta algo, usar `prompts/clarify.md`.

Paso 1: Unicidad

- [ ] Revisar `skills/SKILLS.md`
- [ ] Revisar `agents/AGENTS.md`
- [ ] Revisar `docs/backlog.md`
- Resultado: [Unico / Similar a ...]

Paso 1.5: Conflict-guard

- [ ] Generar input segun `docs/architecture/conflict-guard-interface.mdx`
- [ ] Ejecutar `python scripts/conflict_guard.py --input <archivo>.json`
- [ ] Registrar resultado en FAR

Paso 2: Filosofia

- [ ] Local-first
- [ ] User-friendly
- [ ] Reduce friccion
- Resultado: [Cumple / No cumple]

Paso 3: Simplicidad

- [ ] Se puede resolver con herramientas actuales
- [ ] Evita nuevas dependencias innecesarias
- Resultado: [Simple / Complejo]

Paso 4: Scope

- [ ] Es skill o agent
- [ ] Workspace recomendado
- Resultado: [Skill/Agent + workspace]

Recomendacion final:

- [ ] Aprobar
- [ ] Rechazar
- [ ] Reformular

Justificacion:
[Texto breve]
