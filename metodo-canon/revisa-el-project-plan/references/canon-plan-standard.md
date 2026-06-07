# Canon Plan Standard

> **La columna vertebral del Método Canon.** Este documento define, una sola vez y de forma
> portable, qué es un `PROJECT_PLAN` de alto rendimiento profesional. Es la doctrina que toda la
> familia comparte. No describe un proyecto concreto: describe el **estándar** contra el que se
> crea, se mantiene y se audita cualquier plan.

---

## 0. Qué es esto y quién lo usa

Este Standard tiene **tres consumidores** dentro del Método Canon, y los tres hablan exactamente
este lenguaje:

| Consumidor | Superficie | Qué hace con el Standard |
|---|---|---|
| `metodo-desarrollo-canon` (`generate-claude`) | Cowork | **Emite** este Standard como sección §0 del `CLAUDE.md` que genera, instanciado en el tier que toque (un proyecto nuevo nace en **Tier S**). |
| `planifica` | Claude Code | **Conforma**: cada fase/subfase que inserta respeta §6 (plantilla única) y el tier vigente. |
| `revisa-project-plan` | Claude Code | **Hace cumplir**: audita el plan real contra §2 (invariantes), §4 (tier correcto), §5/§7/§8 y §10. |

**Regla de sincronización (crítica).** La fuente canónica de este texto vive aquí
(`revisa-project-plan/references/canon-plan-standard.md`). Su copia operativa viaja dentro del
`CLAUDE.md §0` que `generate-canon` planta en cada repo. Ambas copias deben mantenerse alineadas;
si divergen, **manda esta**.

**Por qué importa la portabilidad.** El estándar no obliga a nadie a conocer la doctrina de
antemano: `canon` la **inyecta** en el `CLAUDE.md` de cualquier proyecto. A partir de ahí,
`planifica` y `revisa` funcionan en *ese* repo con *sus* convenciones. El método se auto-propaga.

---

## 1. Principio rector — "el plan es la masa"

El `PROJECT_PLAN` es la **única fuente de verdad** de *qué hacer ahora* y *qué se hizo ya*. Cada
ciclo de desarrollo se **lee del plan y se escribe en el plan**. El corolario es estricto:

> **Si el trabajo ocurrió pero el plan no se actualizó, el trabajo NO está hecho.**

El plan, el log, el commit y el cierre humano son **una sola transacción**. Ninguno se da por bueno
sin los demás.

---

## 2. Invariantes universales

Estos principios valen para **todo proyecto, todo tamaño, todo stack, todo equipo**. No dependen del
tier ni de la convención de la casa. Son la **línea dura** de la auditoría: si uno falla, hay un
defecto real, no una cuestión de estilo.

- **I1 · Fuente única de verdad.** El estado vivo del proyecto se lee en un solo lugar. No hay dos
  sitios que afirmen cosas distintas sobre "qué toca ahora".
- **I2 · El estado vivo se lee de un vistazo.** Lo que está pasando *ahora* cabe sin scroll mental;
  la historia no compite con el estado. (En cómo se materializa esto interviene el tier — §4.)
- **I3 · Lo cerrado es trazable.** Cada unidad de trabajo cerrada forma una cadena verificable de
  principio a fin (§7). La *forma* de la cadena es un binding; su *existencia* es invariante.
- **I4 · Lo cerrado sale de la vista activa.** El detalle del pasado se va a la historia; el detalle
  del futuro se reduce a una línea de cola. La vista activa solo muestra el presente y el siguiente
  paso.
- **I5 · Atomicidad.** Cada unidad de trabajo tiene **un** objetivo, es verificable de forma
  independiente y se puede cerrar (y commitear) sola.
- **I6 · Continuidad.** Todo bloque de trabajo deja un **puntero NEXT / punto de reanudación**
  explícito, para que la siguiente sesión —u otra persona— sepa dónde retomar sin reconstruir
  contexto.
- **I7 · Toda referencia resuelve.** Cualquier memoria, decisión o documento que el plan cite debe
  existir, ser legible y estar versionado donde un agente nuevo pueda alcanzarlo (§8). Una cita que
  no resuelve es un defecto de continuidad.

---

## 3. Bindings de proyecto

Estos son los **mandos que cada repo ajusta a su gusto**. NO son ley universal. `revisa` los **lee**
del repo (o los detecta), nunca los impone; `canon` los **declara** explícitamente en el `CLAUDE.md`
que genera, para que el enforcer sepa contra qué medir.

- **B1 · Notación de estado.** `✅ / ⏳ / 📌`, checkboxes `[x]`, etiquetas `DONE/WIP` — lo que el
  equipo prefiera, usado de forma consistente.
- **B2 · Esquema de numeración.** `Fase X.Y`, numeración semántica, IDs de ticket — cualquiera,
  mientras sea predecible y jerárquico.
- **B3 · Convención de commit que ancla la trazabilidad.** Prefijo `tipo(X.Y): …`, Conventional
  Commits, `#issue` — la que sea, mientras enlace commit ⇄ entrada del plan.
- **B4 · Gate de cierre.** Qué significa "validado": un **VALIDATE humano**, CI en verde, review
  aprobado, un check de QA. El método Canon por defecto usa VALIDATE humano, pero el invariante
  (I3) solo exige que *exista* un gate y que se registre.
- **B5 · Cifras de los umbrales de tier.** Los números concretos (§4) — ajústalos al proyecto sin
  tocar el principio.
- **B6 · Rutas de las capas.** `docs/plan/`, `docs/plan/archive/`, `.claude/memory/`,
  `docs/decisions/` — la organización física de archivos.

> **Heurística para el auditor:** antes de marcar un fallo de trazabilidad o de formato, pregúntate
> si lo que ves contradice un **invariante** (§2) o solo un **binding** distinto del tuyo. Imponer
> tus bindings a un repo ajeno produce falsos positivos.

---

## 4. Tiers — el plan escala con el proyecto

Un plan no tiene una sola forma correcta: tiene la forma correcta **para su tamaño**. El error
clásico es auditar un proyecto pequeño con la vara de uno grande (y reprobar un monolito sano), o
montar la maquinaria de uno grande en uno pequeño (capas vacías, ceremonia inútil). Por eso **lo
primero es clasificar el tier**, y solo después juzgar contra el canon de *ese* tier.

| Tier | Cuándo | Topología correcta |
|---|---|---|
| **S — Semilla** | Proyecto joven, pocas fases cerradas, el estado vivo cabe holgado. | **Todo en un solo `PROJECT_PLAN.md`.** Sin capas, sin `archive/`, sin CHANGELOG separado: un mini-log al pie del propio archivo basta. *Esto es correcto, no es deuda.* |
| **M — Crece** | La historia empieza a empujar; el estado vivo se acerca a su límite de "un vistazo". | **Índice + CHANGELOG separado** (cronológico, inverso). Aún sin `archive/`: la historia cabe en el changelog. |
| **L — Maduro** | Muchas fases cerradas; el detalle histórico ya no cabe ni en un changelog. | **Índice ligero + CHANGELOG + `archive/*.md`** + (opcional) `backlog.md` (specs de fases futuras) + `docs/decisions/` (memorias versionadas). |

**Gatillos de promoción** (señales, no dogma — se evalúan, no se cronometran):

- **S → M:** el estado vivo deja de leerse de un vistazo · el mini-log al pie compite en tamaño con
  el estado actual · aparecen suficientes fases cerradas como para que repasarlas estorbe.
- **M → L:** el CHANGELOG ya no basta para contener la historia · vuelve a colarse detalle de fases
  cerradas en el índice · el índice se infla más allá de su presupuesto.

**Degradación (sobre-ingeniería):** si encuentras capas vacías o casi vacías —`archive/` sin
contenido real, `backlog.md` testimonial, un CHANGELOG con dos líneas— para un proyecto que cabría
holgado en un archivo, **estás por encima de tu tier**: simplifica hacia abajo.

**Umbral de referencia (binding, ajústalo — §B5):** índice/estado vivo ≤ **~200 líneas**; archivo de
historia ≤ **~2000 líneas** (al superarlo, partir en dos). El **principio** es invariante ("se lee de
un vistazo / no obliga a leer historia para saber el estado"); **el número es un binding**.

---

## 5. El índice es un índice

Aplica desde **Tier M** (cuando el índice ya es un archivo separado de la historia). El índice
contiene **SOLO**:

- Cabecera del sistema documental (qué capa es qué, dónde vive cada cosa).
- Dashboard de estado (contadores que cuadran con las tablas — §10).
- Tabla de fases completadas (rollup, una fila por fase).
- Tareas diferidas.
- La **fase activa como rollup**: estado por sub-fase + puntero **NEXT**.
- La cola de pendientes **como one-liners** (el detalle de cada fase futura vive en `backlog.md`).

El índice **NO** contiene: detalle `TASK/ACTION/VALIDATION` de sub-fases cerradas (→ `archive/`), ni
specs completas de fases futuras (→ una línea de cola + `backlog.md`).

> En **Tier S** no hay índice separado: el archivo único *es* el plan. Pero la **sección de estado
> vivo** de ese archivo debe seguir cumpliendo I2 (leerse de un vistazo), con la historia condensada
> al pie. El principio es el mismo; cambia solo el número de archivos.

**Disparador de enforcement:** tras cerrar cualquier sub-fase, si el estado vivo supera su
presupuesto de tier, **disgregar/archivar es la siguiente acción**, no algo cosmético para "luego".
Un índice inflado es un fallo de proceso: es lo que hace perder el hilo del estado.

---

## 6. La unidad de trabajo — plantilla de entrada única

Toda fase o sub-fase del plan usa **esta misma estructura** (la escribe `planifica`, la instancia el
bootstrap, la verifica `revisa`). Una sola plantilla en toda la familia: sin dialectos.

```markdown
## [ID y título]          ← p. ej. "Fase 44: Calendario" o "Fase 43.2: Calendario en el panel"

## Objetivo
Qué resuelve, desde la perspectiva del usuario o del producto. Una o dos frases.

## Alcance
El trabajo concreto que entra en esta fase.

## Dependencias y secuencia
De qué depende, qué desbloquea, y por qué va aquí y no antes/después (respetando el orden de
desarrollo del FRAMEWORK_DEV: backend antes que frontend, estático antes que integraciones, etc.).

## Decisiones clave
Las decisiones ya tomadas en el contexto (módulos, interfaces tocadas, cambios de esquema,
contratos de API, interacciones concretas).

## Definición de hecho (DoD)
Los criterios observables que indican que está completa. Cómo se sabrá que funciona.

## Fuera de alcance
Qué queda explícitamente fuera (y a qué fase pertenece, si procede).

## Notas
Cualquier otra nota relevante.
```

**Reglas de la entrada:**
- **No** incluyas rutas de archivo concretas ni snippets de código: caducan rápido y ensucian el
  plan.
- **Excepción:** si un prototipo produjo un snippet que codifica una decisión con más precisión que
  la prosa (una máquina de estados, un reducer, un esquema, una forma de tipo), inclúyelo dentro de
  la decisión correspondiente, recortado a lo esencial, anotando que viene de un prototipo.

---

## 7. Trazabilidad — forma, no formato

Cada sub-fase cerrada forma una **cadena completa y mutuamente alcanzable**. Los **eslabones** son
invariantes (I3); su **formato** es un binding (§3):

```
entrada en el plan  ⇄  commit (B3: su convención)  ⇄  línea de log  ⇄  cierre registrado (B4: su gate)
```

- En un repo con VALIDATE humano, el último eslabón es ese OK escrito.
- En un repo sin gate humano, es lo que cierre el trabajo allí (CI verde, review aprobado).
- Lo invariante es que **lo cerrado sea trazable de punta a punta**. Si falta un eslabón, la
  sub-fase no es trazable y se trata como **no hecha** (I1 + §1).

> **Nota para el auditor:** la correspondencia commit ⇄ plan se infiere de la convención del repo
> (B3), no de la tuya. Si el repo no usa prefijos `(X.Y)`, no marques "sin trazabilidad": detecta
> *su* convención y mide contra ella.

---

## 8. Memorias y decisiones — el "por qué"

Las memorias capturan el **porqué** que el código y el git no guardan: decisiones de
arquitectura/producto, correcciones de rumbo, gotchas reproducibles, puntos de reanudación.

- **Regla de versionado (crítica).** Toda memoria que sostenga una **decisión viva citada por el
  plan** debe estar **versionada en el repo** (`.claude/memory/` o `docs/decisions/`). Una memoria
  citada que solo vive en un almacén local de la máquina es un **riesgo de continuidad**: si cambia
  la máquina, el plan cita fantasmas.
- **Integridad de enlaces.** Cada `[[slug]]` citado en el plan resuelve a un archivo existente y
  legible (I7). Citar lo inalcanzable es un defecto.
- **Cuándo escribir una.** Cuando una decisión es no obvia, fue contestada, o hará falta para
  retomar después. No memorices lo que el repo ya registra (estructura, fixes pasados, historia de
  git).

---

## 9. Transición de tier — cómo se promociona (no opcional)

Cuando salta un gatillo de promoción (§4), la transición es una operación **atómica y con
autorización**, no algo que se deja a medias:

- **S → M:** crear el CHANGELOG separado; mover el log cronológico del pie al CHANGELOG; dejar en el
  archivo principal solo estado vivo + rollup + cola.
- **M → L:** crear `archive/`; mover el detalle de las fases cerradas al archivo histórico; dejar en
  el índice solo rollup + cola + tabla de completadas; parquear specs futuras en `backlog.md`;
  versionar en `docs/decisions/` las memorias que el plan cite.

Tras **cualquier** transición o reencauce: **re-medir** el estado vivo y correr el checklist de
coherencia (§10). Si el repo separa push del humano, no se publica solo.

---

## 10. Checklist de coherencia — lo que `revisa` hace cumplir

Auto-auditoría que impide que el índice se desincronice de la realidad:

- [ ] Los contadores del dashboard **cuadran** con las tablas (sin drift tipo "45 vs 38").
- [ ] La tabla de archivos lista **todos** los ficheros realmente presentes en `archive/` (sin
      huérfanos en ninguna dirección).
- [ ] La "Active Work" está limpia; el rollup refleja el estado real de las sub-fases.
- [ ] Cada `[[memoria]]` referenciada resuelve a un archivo del repo (§8 / I7).
- [ ] El estado vivo está **dentro del presupuesto de su tier** (§4). Si no → disgregar ahora.
- [ ] El **tier es el correcto**: ni infra (monolito que ya pide capas), ni sobre-ingeniería (capas
      vacías para un proyecto trivial).
- [ ] Existe un puntero **NEXT / reanudación** claro (I6).

---

## Apéndice — mapa de la familia

```
metodo-desarrollo-canon  ──emite──►   CLAUDE.md §0  (copia operativa de este Standard, instanciada a Tier S)
                                            │
planifica  ──conforma──►  cada entrada respeta §6 y el tier vigente
                                            │
revisa-project-plan  ──hace cumplir──►  audita contra §2 · §4 · §5 · §7 · §8 · §10
```

*Canon Plan Standard · fuente canónica: `revisa-project-plan/references/canon-plan-standard.md` ·
mantener sincronizada con la copia embebida en `generate-claude` · v1 (2026-06-07).*
