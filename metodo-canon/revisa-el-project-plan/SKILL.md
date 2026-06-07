---
name: revisa-el-project-plan
description: >
  [Claude Code · Método Canon] Audita la salud de un `PROJECT_PLAN.md` contra el Canon Plan Standard y,
  con tu OK, lo sanea. Para Claude Code, en el repo del proyecto. Localiza el plan, clasifica su tier
  (S/M/L) y audita los ejes de calidad (fuente única, estado vivo de un vistazo, atomicidad, trazabilidad,
  continuidad/NEXT, memorias, coherencia del dashboard, transición de tier), siempre relativo al tier y
  leyendo los bindings del repo sin imponer los suyos. Escribe `AUDIT_PROJECT_PLAN.md`. Read-only por
  defecto: el reencauce (disgregar, archivar, promocionar de tier) solo tras tu autorización. Úsalo cuando
  el usuario diga "revisa el project plan", "audita el plan", "¿está sano el plan?", "el plan se ha
  desordenado" o tras cerrar varias fases. Es el auditor del Método Canon, tras la génesis y
  anade-esto-al-project-plan.
license: MIT
metadata:
  author: Jordi Pàmies
  surface: Claude Code
---

# Revisa el Project Plan — el auditor del Método Canon

`revisa-el-project-plan` es el **enforcer** de la familia: hace cumplir el **Canon Plan Standard** sobre
el `PROJECT_PLAN` real de un repo. No diseña ni ubica trabajo (eso son `grill-me` y
`anade-esto-al-project-plan`): **mide la salud del plan, la reporta, y solo sanea con tu permiso.**

> **Read-only por defecto.** Auditar nunca modifica el plan. El reencauce (disgregar el estado vivo,
> archivar historia, promocionar de tier, arreglar drift) es una **segunda fase explícita** que solo
> ocurre tras tu autorización.

## La doctrina vive en el Standard

Toda la vara de medir está en [`references/canon-plan-standard.md`](references/canon-plan-standard.md)
— **léelo entero antes de auditar**. Lo esencial para no equivocarte:

- **Invariantes (§2, I1–I7)** = línea dura: si uno falla, hay un defecto real, no una cuestión de estilo.
- **Bindings (§3, B1–B6)** = los mandos de cada repo (notación de estado, numeración, convención de
  commit, gate de cierre, rutas de capas). **Se leen del repo, NUNCA se imponen.** Imponer tus bindings
  a un repo ajeno produce falsos positivos.
- **Tiers (§4, S/M/L)** = el plan escala con el proyecto. **Clasifica el tier primero**; un monolito en
  un solo archivo es *correcto* en Tier S, no es deuda.

## Proceso

1. **Localiza el plan.** `PROJECT_PLAN.md` en la raíz (o donde lo ponga el binding §B6 del repo). Si no
   aparece, pregunta su ubicación antes de seguir — no inventes.
2. **Lee los bindings del repo.** Si existe `CLAUDE.md §0` (la copia operativa del Standard que planta
   la génesis), úsalo como verdad de los bindings. Si no, **detéctalos** del propio plan: qué notación
   de estado usa, qué numeración, qué convención de commit, qué gate de cierre.
3. **Mide, no opines.** Corre [`scripts/scan-plan.sh`](scripts/scan-plan.sh) `<raíz>` para obtener
   métricas objetivas (líneas del estado vivo, nº de fases, capas presentes, marcadores, referencias
   `[[memoria]]` y su resolución). La medición es determinista; la interpretación es tuya.
4. **Clasifica el tier (S/M/L)** con los gatillos del §4, cruzando las métricas con la topología real
   (¿un archivo? ¿índice + CHANGELOG? ¿índice + CHANGELOG + `archive/`?).
5. **Audita los ejes** siguiendo [`references/audit-axes.md`](references/audit-axes.md) (ejes A–J). Cada
   eje se evalúa **relativo al tier** y contra los **bindings del repo**. Clasifica cada hallazgo como
   defecto de invariante (duro) o desajuste de binding/tier (blando), siempre con su evidencia.
6. **Escribe el informe.** Vuelca el resultado en `AUDIT_PROJECT_PLAN.md` en la raíz del repo auditado,
   usando [`assets/audit-report-template.md`](assets/audit-report-template.md): veredicto + tier +
   hallazgos priorizados + reencauce propuesto. Aquí termina el modo read-only.
7. **Reencauce (solo con OK).** Si el usuario autoriza, ejecuta las acciones del §9 (transición de tier)
   y del §5 (disgregar el índice inflado): operación atómica, re-medir al final, correr el checklist §10,
   y **no publiques solo** si el repo separa el push del humano.

## Reglas de oro

- **El plan es la masa (§1).** Lo que ocurrió pero no se escribió en el plan, no está hecho. Audita esa
  transacción (plan ⇄ commit ⇄ log ⇄ cierre).
- **Tier primero, juicio después.** No repruebes un Tier S sano por "monolito", ni dejes pasar capas
  vacías en un proyecto trivial (sobre-ingeniería → simplifica hacia abajo).
- **Bindings ajenos, no propios.** Detecta la convención del repo y mide contra ella; el número del
  umbral es un binding, el principio es invariante.
- **Una cita que no resuelve es un defecto (I7).** Cada `[[memoria]]` referenciada debe existir, ser
  legible y estar versionada en el repo.
- **Conservador con la escritura.** Auditar es seguro; sanear necesita permiso.
