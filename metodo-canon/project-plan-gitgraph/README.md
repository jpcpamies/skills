# Project Plan Git Graph — la *vista* del Método Canon

Convierte el `PROJECT_PLAN.md` de un repo en un diagrama Mermaid `gitGraph` que se lee **de un
vistazo** y codifica el estado del plan **por color**. Es la *vista* de la familia: no edita el
plan ni impone doctrina — lo *lee* y lo pinta como un árbol estilo Git.

> **Entregable único:** un archivo `.mermaid` **validado** (compila en mermaid.live). Nada de HTML,
> render ni artefacto — si lo quieres ver, lo pegas tú en [mermaid.live](https://mermaid.live).

## Estado por color

El grafo abre con un bloque `%%{init}%%` que fija los colores de rama (`git0..gitN`, asignados por
**orden de creación** de rama, no por nombre):

- 🟢 **verde** — cerrado / hecho
- 🔴 **rojo** — donde estás AHORA (NEXT), un solo commit `type: HIGHLIGHT`
- 🟠 **naranja** — por hacer
- ⚪ **gris** — descartado / diferido

Cada commit lleva además un tag explícito: `✅ CERRADO`, `👉 ESTAS AQUI`, `⏳`, `🎯 hito`,
`❌ cancelada`, `⏸ diferida`. Color y tag siempre coinciden.

## Estructura de ramas

- **`main`** — fases cerradas agrupadas en eras (cada commit = un grupo; el tag dice cuántas) + el pivote.
- **`<fase>-hecho`** — sub-fases ya cerradas de la fase activa.
- **`ESTAS-AQUI`** — el NEXT (1 commit `HIGHLIGHT`).
- **`por-hacer`** — lo pendiente en orden + el hito go-live. Sin merge.
- **`descartado`** — canceladas + diferidas. Sin merge.

## Instalación

Corre en **Claude Code** sobre el repo del proyecto. Se distribuye en el plugin `jordipamies-skills`:

```bash
/plugin marketplace add jpcpamies/skills
/plugin install jordipamies-skills@jordipamies-skills
/reload-plugins
```

## Cómo se usa

Invoca con: *"muéstrame el project plan"*, *"git graph del plan"*, *"pasa el plan a un gitGraph"*,
*"el árbol del proyecto"*. El skill lee el `PROJECT_PLAN.md`, extrae las fases, construye el
`gitGraph`, lo **valida con el parser real** y te entrega el `.mermaid`.

## Validación

```bash
node scripts/validate_gitgraph.mjs <ruta-al-archivo>.mermaid
```

El script corre heurísticas + el parser real de Mermaid. **Se autoinstala** el parser en un
directorio temporal del SO la primera vez; **nunca** instala nada dentro de esta carpeta, para que
quede siempre limpia (solo `SKILL.md`, `references/`, `scripts/`) y se pueda comprimir y subir a la
superficie sin errores de "caracteres inválidos".
