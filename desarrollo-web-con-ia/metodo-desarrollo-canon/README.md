# Canon Method — skill de planificación de apps

**CANON** = **C**onsistencia · **A**tomicidad · **N**orth Star · **O**rden · **N**on-slop.
Un método *spec-driven* para construir apps web full-stack con Claude Code: una entrevista guiada genera los documentos
que gobiernan todo el ciclo de vida. *Canon* = un estándar correcto y **repetible**: trabajar siempre de la misma manera.

> **Principio fundacional:** autonomía ≠ consistencia. Estos documentos no le enseñan a Claude qué hacer; le imponen
> *tu* manera de hacerlo — mismo criterio, mismo orden, misma disciplina, siempre.

## Qué genera (5 documentos, 2 capas)

**Capa de producto** (qué construir): `PRD.md` · `PRODUCT.md` · `DESIGN.md`
**Capa de proceso** (cómo trabajar): `CLAUDE.md` · `FRAMEWORK_DEV.md`

## Instalación (Claude Code)

```bash
# Por proyecto
cp -r canon ~/ruta-al-proyecto/.claude/skills/
# O global (todos los proyectos)
cp -r canon ~/.claude/skills/
```
Recarga el harness y teclea `/` — debería aparecer `canon`. (También instalable como skill de Cowork.)

## Cómo se usa

Invoca con: *"método canon"*, *"nuevo proyecto"*, *"crear un PRD"*, *"validar mi idea"*, o *"¿cómo funciona canon?"*.
La entrevista va en tres bloques con confirmación intermedia:

1. **Validate** — viabilidad (painkiller vs vitamin, founder-market fit, ICP, diferenciación). Veredicto.
2. **PRD** — negocio, IA, datos, pantallas, monetización, stack.
3. **Design** — register, personalidad, referencias visuales, North Star, color, tipografía. (Pide capturas/URLs.)

Al terminar genera los 5 documentos y te explica las dos capas y los siguientes pasos.

## Receta con Claude Code

1. Coloca los 5 archivos en la carpeta del proyecto.
2. Abre la carpeta en Claude Code → lee `CLAUDE.md` (Estado A) → copia `FRAMEWORK_DEV.md` (incluido en el skill) a `docs/` → escribe `PROJECT_PLAN.md` → **STOP** para tu OK.
3. Ejecuta: **Fase 0** scaffold + `npx impeccable skills install` + saltar `teach` (PRODUCT.md/DESIGN.md ya existen).
4. **Build loop** atómico siguiendo el Golden Order, aplicando `DESIGN.md` y puliendo con Impeccable.

## Framework incluido (sin descargas)

El `FRAMEWORK_DEV.md` viaja **dentro del skill**, en `references/FRAMEWORK_DEV.md`.
Cuando se planifica un proyecto, se **copia** desde ahí a `docs/FRAMEWORK_DEV.md`.
No se descarga de internet — funciona siempre, también sin red.

## Estructura del skill

```
canon/
  SKILL.md                     Spine + routing + tono + warm start + resumibilidad
  README.md                    Este archivo
  references/
    methodology.md             El Canon Method (modo explicación)
    interview-validate.md      Bloque 1 — viabilidad
    interview-prd.md           Bloque 2 — las 12 preguntas del PRD
    interview-design.md        Bloque 3 — sistema visual (integra teach de Impeccable)
    generate-prd.md            Cómo escribir PRD.md (incl. §12 metodología Impeccable)
    generate-product.md        Cómo escribir PRODUCT.md (formato Impeccable)
    generate-design.md         Cómo escribir DESIGN.md (formato Stitch)
    generate-claude.md         Cómo escribir CLAUDE.md (plantilla reutilizable)
    design-md-spec.md          Spec destilado de Google Stitch DESIGN.md
    impeccable-integration.md  Comandos/instalación/anti-slop verificados
    integration-bootstrap.md   Paso 0 de integraciones externas (plugin/MCP/SDK oficiales)
    FRAMEWORK_DEV.md           El Golden Order de construcción (se copia a docs/ del proyecto)
```

*Canon Method · v2.0 · creado por Jordi Pàmies*
*(v2.0 añade el bootstrap de integraciones externas: §14 del CLAUDE.md + references/integration-bootstrap.md)*
