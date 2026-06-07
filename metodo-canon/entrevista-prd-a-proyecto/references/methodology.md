# El Método Canon — metodología y ciclo de vida

> Modo explicación. Si el usuario pregunta "¿cómo funciona?", "¿cuál es la secuencia?", "explícame la metodología",
> resume este documento con tus palabras. NO arranques ninguna entrevista.

## Qué es CANON

Un método **spec-driven** para construir aplicaciones web full-stack con Claude Code: primero se escribe la
especificación completa (en documentos), y de ahí Claude Code planifica y construye. CANON cubre desde la idea hasta
el ship, y garantiza que cada proyecto se haga **de la misma manera**.

**CANON** = **C**onsistencia · **A**tomicidad · **N**orth Star · **O**rden · **N**on-slop.
Y la palabra *canon* lo resume: un estándar correcto y **repetible**.

## El principio fundacional

**Autonomía ≠ consistencia.** Un modelo capaz no es un modelo predecible. Los documentos del método no le enseñan a
Claude qué hacer — eso ya lo sabe. Le imponen *tu* manera de hacerlo: mismo criterio, mismo orden, misma disciplina,
siempre. Esa repetibilidad es lo que convierte proyectos sueltos en un método. Un canon.

## Las dos herramientas

- **CANON (este skill)** — el *planificador*. Corre **una vez**, al principio. Te entrevista y genera los documentos.
- **Impeccable** — el *motor de calidad*. Corre **en continuo**, durante el build, dentro de Claude Code. Aplica,
  evalúa, refina y endurece el diseño sobre el código real, y detecta "AI slop" de forma determinista.

CANON opera sobre la *intención* (texto). Impeccable opera sobre el *código renderizado* (píxeles). No compiten:
CANON prepara el terreno y deja las instrucciones; Impeccable ejecuta la calidad durante la construcción.

## Las dos capas de documentos

**Capa de producto** (qué construir — por proyecto):
- `PRD.md`, `PRODUCT.md`, `DESIGN.md`.

**Capa de proceso** (cómo trabajar — reutilizable entre proyectos):
- `CLAUDE.md`, `FRAMEWORK_DEV.md`.

## El ciclo de vida, etapa por etapa

**Etapa 0 — Invocación.** Lanzas el skill CANON y respondes la entrevista guiada (sugerencias tailored; en diseño, referencias visuales).

**Etapa 1 — Validate (C: Concepto validado).** Mini-entrevista de viabilidad: problema núcleo (*painkiller vs vitamin*),
founder-market fit, ICP ligero, diferenciación en 5 ejes. Veredicto: seguir / pivotar / descartar. Gate antes de gastar esfuerzo.

**Etapa 2 — Specify (A: Arquitectura especificada).** De tus respuestas nacen los tres documentos de producto:
`PRD.md` (negocio/IA/datos/pantallas/monetización), `PRODUCT.md` (estrategia/marca para Impeccable),
`DESIGN.md` (sistema visual, formato Stitch).

**Etapa 3 — North Star (N).** Dentro del bloque de diseño se fija el *Creative North Star*: una metáfora nombrada que
gobierna todo el sistema visual. El diseño deja de improvisarse.

**Etapa 4 — Process (Orden, O).** CANON copia el `FRAMEWORK_DEV.md` incluido en el skill (carpeta `references/`) a `/docs/` y genera
el `CLAUDE.md` ya cableado (ciclo de desarrollo + integración Impeccable + visual checklist derivada del DESIGN.md).

→ *Aquí termina el trabajo de CANON: una carpeta con 5 archivos en 2 capas.*

**Etapa 5 — Plan.** Abres la carpeta en Claude Code. Lee `CLAUDE.md` → Estado A → lee PRD + framework → escribe
`PROJECT_PLAN.md` → para y espera tu OK.

**Etapa 6 — Bootstrap.** Scaffold del proyecto según el stack → instala Impeccable (`npx impeccable skills install`)
→ se salta `teach` porque `PRODUCT.md`/`DESIGN.md` ya existen.

**Etapa 7 — Build loop (Non-slop, N).** Ciclos atómicos (Present → Execute → Validate → Close) siguiendo el Golden
Order, aplicando el `DESIGN.md` y tejiendo Impeccable: `shape`/`craft` por feature, `critique`/`polish` y
`audit`/`harden` antes de cerrar, `detect` en pre-commit, `live` para iterar en navegador.

**Etapa 8 — Ship & Extend.** `harden`/`optimize` antes de publicar. Las ampliaciones futuras reentran al loop
respetando framework + Impeccable. Por eso la capa de proceso es persistente.

## Cómo mapea CANON al ciclo

| Letra | Significado | Dónde vive en el ciclo |
|---|---|---|
| **C** | Consistencia | El método entero: trabajar siempre igual (capa de proceso) |
| **A** | Atomicidad | El ciclo de desarrollo: 1 tarea verificable, validar antes de avanzar |
| **N** | North Star | El `DESIGN.md`: norte creativo nombrado, diseño dirigido |
| **O** | Orden | El `FRAMEWORK_DEV.md`: el Golden Order de construcción |
| **N** | Non-slop | Impeccable: calidad determinista, cero AI-slop, hasta el ship |
