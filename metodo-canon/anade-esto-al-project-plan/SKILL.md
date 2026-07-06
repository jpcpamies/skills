---
name: anade-esto-al-project-plan
description: >
  [Claude Code · Método Canon] Actualiza el `PROJECT_PLAN.md` del proyecto de código en el que estás
  trabajando, en Claude Code. Toma todo el contexto cargado en la conversación actual (típicamente tras una
  sesión de Grill Me sobre una nueva característica) y ubica ese trabajo en el plan: como una fase nueva o como
  una subfase de una fase existente. NO entrevista al usuario (Grill Me ya ha hecho las preguntas) y NO toca el
  PRD ni los demás documentos del Método Canon. Es la skill que ubica el trabajo ya diseñado en el plan, justo
  después de Grill Me. Úsala SIEMPRE que el usuario diga "planifica", "ahora planifica", "planifica esto",
  "añade esto al project plan", "actualiza el project plan", "añade esto al plan", "mete esta característica en
  el plan" o "ubica esto en el plan", o cuando se haya cargado el contexto de una nueva feature y se quiera
  situarla en el plan de fases del proyecto de código actual. Es para Claude Code, donde existe un
  `PROJECT_PLAN.md` en la raíz del proyecto. NO confundir con el skill `actualizar-plan` (superficie de Cowork,
  seguimiento del temario del Máster IA con Jose Augusto vía `plan-data.js`).
metadata:
  author: Jordi Pàmies
  surface: Claude Code
---

Esta skill toma el contexto de la conversación actual y tu entendimiento del codebase, y actualiza el **`PROJECT_PLAN.md` del proyecto de código en el que estás trabajando**. NO entrevistes al usuario — sintetiza lo que ya sabes. Normalmente Grill Me ya ha recorrido el árbol de diseño y ha resuelto las preguntas en los turnos anteriores; tu trabajo es coger todo ese contexto valioso y ubicarlo en el plan.

El plan vive en un archivo llamado **`PROJECT_PLAN.md`**, en la **raíz del proyecto** — la misma carpeta donde se está ejecutando esta sesión de Claude Code. Léelo desde ahí. Si no existe, díselo al usuario y confirma con él si quieres crearlo antes de continuar: esta skill **actualiza un plan existente**, no asume su creación sin permiso.

Esta skill **NO modifica el PRD** ni `PRODUCT.md`, `DESIGN.md`, `CLAUDE.md` ni `FRAMEWORK_DEV.md`. Solo actualiza el `PROJECT_PLAN.md`. Si en algún momento se quiere un reporte global de características, ese se extrae del PRD + el Project Plan + el codebase, no de aquí.

> **Esta skill _conforma_ el Canon Plan Standard.** La plantilla de abajo es la **plantilla de entrada
> única (§6)** del Standard — la misma en toda la familia, sin dialectos. Y toda inserción respeta el
> **tier** vigente del plan (§4): en **Tier S** (un solo archivo) la entrada va inline; desde **Tier M/L**
> una fase *futura* entra como **one-liner en la cola** (su detalle vive en `backlog.md`) y nunca infla el
> índice por encima de su presupuesto. Si al ubicar el trabajo detectas que el plan se ha pasado de tier,
> **no lo reorganices aquí**: eso es trabajo de `valida-el-project-plan`. Doctrina:
> [`../valida-el-project-plan/references/canon-plan-standard.md`](../valida-el-project-plan/references/canon-plan-standard.md).

## Proceso

1. Explora el repo y **lee el `PROJECT_PLAN.md` de la raíz** para entender el estado: en qué fase estás, qué fases existen, su orden y la lógica de secuenciación. Fíjate en el formato real del archivo (su numeración y su estilo de entrada) para luego escribir igual — son los *bindings* del repo y se respetan, no se sustituyen. Identifica también el **tier** del plan (¿un solo archivo? ¿índice + CHANGELOG? ¿+ `archive/`?) para saber dónde debe caer el detalle de lo que vas a añadir. Usa el glosario de dominio (*ubiquitous language*) del proyecto en toda la actualización. Localiza y lee el `FRAMEWORK_DEV` del proyecto —normalmente dentro de `docs/`— para conocer las directrices de desarrollo y la lógica de secuenciación de fases, y respétalas, junto con cualquier ADR de la zona que estés tocando.

2. Decide la **ubicación** del nuevo trabajo dentro del plan: ¿una fase nueva de nivel superior, o una subfase de una fase existente? Prefiere encajarlo como subfase de una fase existente cuando pertenezca a ella de forma natural; crea una fase nueva solo cuando el trabajo no encaje en ninguna existente. Tanto si es subfase como si es fase nueva, colócala en la posición del plan que mejor siga las directrices de desarrollo del `FRAMEWORK_DEV` (p. ej. backend antes que frontend); no rompas el orden ni las dependencias existentes.

   Comprueba con el usuario que esta ubicación encaja con sus expectativas **antes** de escribir.

3. Escribe la actualización en el `PROJECT_PLAN.md`, **en el mismo formato que ya usa el archivo** (respeta su estructura, su numeración y su estilo de entrada). Si el plan está recién creado, vacío o su formato es ambiguo, usa la plantilla de abajo como base. Mantén cada fase o subfase como una unidad coherente y atómica.

<phase-entry-template>

## [ID y título de la fase/subfase]

P. ej. "Fase 44: Calendario de sesiones" (fase nueva) o "Fase 43.2: Calendario dentro del panel de academia" (subfase). Usa el esquema de numeración que ya tenga el plan.

## Objetivo

Qué resuelve esta fase, desde la perspectiva del usuario o del producto. Una o dos frases.

## Alcance

Qué entra en esta fase: el trabajo concreto que se va a hacer.

## Dependencias y secuencia

De qué fases depende esta, qué fases desbloquea, y dónde se inserta en el orden del plan. Justifica por qué va aquí y no antes o después, respetando el `FRAMEWORK_DEV`.

## Decisiones clave

Las decisiones que ya se tomaron en el contexto cargado (Grill Me): módulos a construir o modificar, interfaces que se tocan, cambios de esquema, contratos de API, interacciones específicas.

NO incluyas rutas de archivo concretas ni snippets de código: caducan rápido y ensucian el plan.

Excepción: si un prototipo produjo un snippet que codifica una decisión con más precisión que la prosa (una máquina de estados, un reducer, un esquema, una forma de tipo), inclúyelo dentro de la decisión correspondiente y anota brevemente que viene de un prototipo. Recórtalo a lo esencial — no es una demo funcional, solo las partes que importan.

## Definición de hecho

Los criterios que indican que esta fase está completa. Cómo se sabrá que funciona, en términos de comportamiento observable.

## Fuera de alcance

Qué queda explícitamente fuera de esta fase (y, si procede, a qué otra fase pertenece).

## Notas

Cualquier otra nota relevante sobre la fase.

</phase-entry-template>
