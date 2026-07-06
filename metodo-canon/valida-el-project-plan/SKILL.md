---
name: valida-el-project-plan
description: >
  [Claude Code · Método Canon] Audita la salud de un `PROJECT_PLAN.md` contra el Canon Plan Standard y,
  con tu OK, lo sanea. Para Claude Code, en el repo del proyecto. Localiza el plan, clasifica su tier
  (S/M/L) y audita los ejes de calidad (fuente única, estado vivo de un vistazo, atomicidad, trazabilidad,
  continuidad/NEXT, memorias, coherencia del dashboard, transición de tier, y presencia del `CLAUDE.md §0`
  operativo), siempre relativo al tier y leyendo los bindings del repo sin imponer los suyos. Escribe
  `AUDIT_PROJECT_PLAN.md`. Read-only por defecto: el reencauce (disgregar, archivar, promocionar de tier, y
  plantar/refrescar el `CLAUDE.md §0` que hace que Claude Code mantenga la metodología) solo tras tu
  autorización. Úsalo cuando
  el usuario diga "valida el project plan", "revisa el project plan", "audita el plan", "¿está sano el
  plan?", "el plan se ha desordenado" o tras cerrar varias fases. Es el auditor del Método Canon, tras la
  génesis y anade-esto-al-project-plan.
license: MIT
metadata:
  author: Jordi Pàmies
  surface: Claude Code
---

# Valida el Project Plan — el auditor del Método Canon

`valida-el-project-plan` es el **enforcer** de la familia: hace cumplir el **Canon Plan Standard** sobre
el `PROJECT_PLAN` real de un repo. No diseña ni ubica trabajo (eso son `grill-me` y
`anade-esto-al-project-plan`): **mide la salud del plan, la reporta, y solo sanea con tu permiso.**

> **Read-only por defecto.** Auditar nunca modifica el plan ni el `CLAUDE.md`. El reencauce (disgregar el
> estado vivo, archivar historia, promocionar de tier, arreglar drift y **plantar/refrescar el `CLAUDE.md
> §0`**) es una **segunda fase explícita** que solo ocurre tras tu autorización.

> **Monta la infraestructura Y deja las instrucciones.** Disgregar el plan o promocionar de tier monta capas
> (`archive/`, CHANGELOG…), pero esas capas solo se **mantienen** si el `CLAUDE.md` lleva, como **§0**, la
> copia operativa del Standard que le dice a Claude Code cómo leer/escribir/archivar el plan. Por eso el
> reencauce **siempre** revisa el §0: si falta (típico en un repo adoptado directo en Claude Code, sin pasar
> por la génesis de Cowork) o quedó desfasado tras una transición de tier, lo planta/refresca al principio del
> `CLAUDE.md`. Sin §0, montar la infraestructura no sirve: nadie la mantiene y el plan se vuelve a desordenar.

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
   la génesis), úsalo como verdad de los bindings. Si **no existe `CLAUDE.md` o no tiene §0**, anótalo como
   **hallazgo del eje K** (defecto duro de continuidad: el repo no declara su estándar) y **detecta** los
   bindings del propio plan: qué notación de estado usa, qué numeración, qué convención de commit, qué gate de
   cierre. Esos bindings detectados son los que luego instanciarán el §0 que plantes en el reencauce.
3. **Mide, no opines.** Corre [`scripts/scan-plan.sh`](scripts/scan-plan.sh) `<raíz>` para obtener
   métricas objetivas (líneas del estado vivo, nº de fases, capas presentes, marcadores, referencias
   `[[memoria]]` y su resolución). La medición es determinista; la interpretación es tuya.
4. **Clasifica el tier (S/M/L)** con los gatillos del §4, cruzando las métricas con la topología real
   (¿un archivo? ¿índice + CHANGELOG? ¿índice + CHANGELOG + `archive/`?).
5. **Audita los ejes** siguiendo [`references/audit-axes.md`](references/audit-axes.md) (ejes A–K). Cada
   eje se evalúa **relativo al tier** y contra los **bindings del repo**. Clasifica cada hallazgo como
   defecto de invariante (duro) o desajuste de binding/tier (blando), siempre con su evidencia. El **eje K**
   comprueba que el `CLAUDE.md` lleve el §0 operativo coherente con el tier real (ausente o desfasado = duro).
6. **Escribe el informe.** Vuelca el resultado en `AUDIT_PROJECT_PLAN.md` en la raíz del repo auditado,
   usando [`assets/audit-report-template.md`](assets/audit-report-template.md): veredicto + tier +
   hallazgos priorizados + reencauce propuesto. Aquí termina el modo read-only.
7. **Reencauce (solo con OK).** Si el usuario autoriza, ejecuta las acciones del §9 (transición de tier)
   y del §5 (disgregar el índice inflado): operación atómica, re-medir al final, correr el checklist §10,
   y **no publiques solo** si el repo separa el push del humano.
8. **Planta/refresca el `CLAUDE.md §0` (parte del reencauce, con el mismo OK).** Si el eje K marcó el §0 como
   ausente o desfasado, copia [`assets/claude-md-seccion-0.md`](assets/claude-md-seccion-0.md) — la **única
   copia canónica** de las instrucciones — como **§0** del `CLAUDE.md` (lo primero del archivo), rellenando el
   bloque **0.A** con el **tier del eje B** y los **bindings detectados** (paso 2). Reemplaza un §0 existente,
   **nunca lo dupliques**. Si no hay `CLAUDE.md`, créalo con ese §0 como cabecera. Tras una transición de tier
   (paso 7), refrescar el §0 no es opcional: la infraestructura nueva solo se mantiene si el §0 la describe.
   - **Idioma (regla fija).** **Detecta el idioma** en que está escrito el `CLAUDE.md` destino (si no hay
     `CLAUDE.md`, el del `PROJECT_PLAN.md`; si tampoco es claro, deja el español canónico) y vuelca la
     plantilla **traducida** a ese idioma. **Mismas instrucciones, distinto idioma:** no mantienes una versión
     por idioma — hay una sola copia canónica (en español) y la traduces al plantar. Traducir cambia la prosa,
     **no** la estructura ni los identificadores estables: códigos de sección (0.A, 0.0–0.9), bindings
     (B1–B6), invariantes (I1–I7), marcadores `S/M/L`/`NEXT` y rutas de archivo se mantienen sin traducir.

## Reglas de oro

- **El plan es la masa (§1).** Lo que ocurrió pero no se escribió en el plan, no está hecho. Audita esa
  transacción (plan ⇄ commit ⇄ log ⇄ cierre).
- **Tier primero, juicio después.** No repruebes un Tier S sano por "monolito", ni dejes pasar capas
  vacías en un proyecto trivial (sobre-ingeniería → simplifica hacia abajo).
- **Bindings ajenos, no propios.** Detecta la convención del repo y mide contra ella; el número del
  umbral es un binding, el principio es invariante.
- **Una cita que no resuelve es un defecto (I7).** Cada `[[memoria]]` referenciada debe existir, ser
  legible y estar versionada en el repo.
- **Infraestructura sin §0 es deuda (eje K).** Montar capas sin dejar en el `CLAUDE.md §0` las instrucciones
  para mantenerlas garantiza que el plan se vuelva a desordenar. Auditar siempre comprueba el §0; el reencauce
  lo planta/refresca instanciado al tier y bindings reales.
- **Conservador con la escritura.** Auditar es seguro; sanear (incluido plantar el §0) necesita permiso.
