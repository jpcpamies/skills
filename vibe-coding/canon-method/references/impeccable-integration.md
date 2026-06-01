# Integración con Impeccable (referencia verificada)

> Datos verificados en impeccable.style/docs, /slop, getting-started y github.com/pbakaus/impeccable (Skill 3.1.1, may 2026).
> No inventes comandos ni URLs. Si dudas de la versión, `npx impeccable skills help` o teclea `/impeccable`.

## Qué es
Skill/CLI de calidad de diseño determinista para harnesses de IA (Claude Code soportado de primera clase).
Arquitectura de dos archivos que TODOS sus comandos leen: `PRODUCT.md` (estrategia, OBLIGATORIO) + `DESIGN.md` (visual, recomendado).

## Instalación (siempre la última versión, sin repo local)
```bash
npx impeccable skills install   # autodetecta el harness, instala el build compilado
npx impeccable skills update    # actualizar
npx impeccable skills help      # listar comandos / verificar versión
```
Alternativas: plugin de Claude Code `/plugin marketplace add pbakaus/impeccable`; genérico `npx skills add pbakaus/impeccable`;
o descargar el ZIP de impeccable.style. El CLI detector no necesita instalación: `npx impeccable detect`.

## Setup en el proyecto CANON
- **NO ejecutar `teach`/`init`.** CANON ya generó `PRODUCT.md` + `DESIGN.md`. Ponlos en raíz o `/docs/` (Impeccable resuelve por fallback).
- Nota: la doc oficial usa indistintamente `teach` (SKILL.md) e `init` (tutorial) para el setup — da igual, lo saltamos.
- Opcional: `/impeccable document` cuando haya código, para reconciliar `DESIGN.md` con tokens reales (tiene "seed mode" si no hay tokens).

## 23 comandos (verificados)
- Create/Build: `craft`, `shape`, `teach`, `document`, `extract`
- Evaluate: `audit`, `critique`
- Refine: `polish`, `bolder`, `quieter`, `distill`, `harden`, `onboard`
- Enhance: `animate`, `colorize`, `typeset`, `layout`, `delight`, `overdrive`
- Fix: `clarify`, `adapt`, `optimize`
- Iterate: `live`
- Gestión: `pin <cmd>` / `unpin <cmd>` (ej. `pin audit` → `/audit`).

Solo los comandos System (`teach`/`document`/`extract`) modifican `DESIGN.md`; el resto solo lo leen.

## Mapa de comandos por fase (para el project-plan)
- Feature nueva → `shape` → `craft`. Iteración visual → `live`.
- Cierre de feature visual → `critique` → `polish`.
- Pasada técnica → `audit` → `harden`. Dimensional → `typeset`/`colorize`/`layout`.
- Pre-commit/CI → `npx impeccable detect src/` (determinista, sin LLM, sin API key).
- Pre-ship → `optimize`, `harden`, `polish`.

## Catálogo anti-slop (46 patrones; ~41 deterministas + 5 LLM)
Top a evitar (para Don'ts de DESIGN.md y §13 de CLAUDE.md), fuente impeccable.style/slop:
1. Borde-acento lateral en tarjeta redondeada (side-tab) — el tell nº1.
2. Paleta IA: degradados morado/violeta, cian-sobre-oscuro.
3. Una sola fuente para todo (Inter/Geist/Space Grotesk) → jerarquía plana.
4. Tarjetas anidadas (card dentro de card).
5. Texto gris sobre fondo de color.
6. Texto con degradado (gradient text) en headings/métricas.
7. Icono en cuadradito redondeado encima de cada heading.
8. Eyebrow/pill chip + headline gigante (héroe SaaS por defecto).
9. Easing con rebote/elástico (usar ease-out exponencial).
10. Copy buzzword (streamline, supercharge, world-class) + sobreuso de em-dash.
