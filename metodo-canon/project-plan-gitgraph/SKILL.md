---
name: project-plan-gitgraph
description: >-
  [Cowork · Método Canon] Genera un diagrama Mermaid en formato gitGraph del progreso del plan de un proyecto (fases hechas vs. fases por delante) a partir del código base. Úsalo SIEMPRE que el usuario diga "muéstrame el project plan", "grafo del plan", "git graph del plan", "diagrama del plan en Mermaid", "pasa el plan a un gitGraph", "el árbol del proyecto", "cómo va el proyecto en un git graph", o pida visualizar el estado/roadmap del proyecto como un árbol estilo Git/GitHub. Detecta la fuente del plan (PROJECT_PLAN.md, ROADMAP, docs/plan, CHANGELOG) y, si no hay documento formal, infiere las fases del historial de git. Produce código Mermaid VALIDADO (que compila en mermaid.live), lo guarda como archivo .mermaid y lo renderiza en un artefacto. Nunca entrega el código solo como bloque de chat con triple comilla.
---

# project-plan-gitgraph

Convierte el plan de un proyecto en un diagrama **Mermaid `gitGraph`** que muestra, de un vistazo, lo **hecho** vs. lo **que queda por delante**. Pensado para correr en la superficie de Cowork sobre un repo con acceso al código base.

## Resultado esperado

1. Un archivo `git-graph.mermaid` **validado** (compila sin errores).
2. El diagrama **renderizado** en un artefacto (Mermaid por CDN).

> **Regla de oro (no la rompas):** entrega el código como **archivo** (`present_files`) y/o **renderizado**. **Nunca** lo entregues únicamente como bloque ```mermaid en el chat: al copiarlo, las líneas de triple comilla viajan con él y mermaid.live falla con `Lexer error on line 1, column 1: unexpected character ->\`<-`. Si el usuario quiere el texto para copiar, dale el archivo.

## Procedimiento

### 1. Localizar la fuente del plan (detectar → fallback)

Busca en este orden y usa la primera que exista:

1. `PROJECT_PLAN.md` (raíz o `docs/`). Si sigue un sistema por capas, su detalle vive en `docs/plan/archive/*`, `docs/plan/CHANGELOG.md` y `docs/plan/backlog.md`.
2. `ROADMAP.md`, `PLAN.md`, `docs/plan/`, `docs/roadmap/`, `TODO.md`.
3. `CHANGELOG.md` (o carpeta `CHANGELOG/`).
4. **Sin documento formal:** infiere las fases de `git log --oneline`, tags (`git tag`) y milestones. **Avisa al usuario** de que el grafo es inferido del historial, no de un plan escrito.

Lee el **índice** primero. Abre archivos de `archive/`/`CHANGELOG` solo para fechas o estado concreto cuando haga falta. **No leas todo el histórico.**

### 2. Extraer el modelo de fases

Para cada fase / sub-fase saca: **id/título**, **estado**, **fecha** (si hay) y **a qué flujo de trabajo pertenece**. Mapea marcadores a estados canónicos:

| Estado | Señales típicas en el plan | Tag en el grafo |
|---|---|---|
| `done` | ✅, `[x]`, "COMPLETE", "cerrada", "mergeada" | `"N ✓"` o `"✓"` |
| `active` | "NEXT", "en curso", "in progress", ▶, "activo" | `"▶ NEXT"` + `type: HIGHLIGHT` |
| `pending` | `[ ]`, "pendiente", "⏳", "TODO", "por hacer" | `"pend."` |
| `cancelled` | "CANCELADA", "cancelled", "descartada" | `"cancelada"` |
| `deferred` | "stand-by", "diferida", "deferred", "aplazada" | `"diferida"` |
| `milestone` | "hito", "go-live", "release", "lanzamiento" | tag con el hito |

Prioridades (`P0`/`P1`) o bloqueos ("bloquea go-live") van **en el tag**, no en una rama.

### 3. Agrupar en ramas (convención)

- **`main`** = núcleo ya entregado. **Agrupa las fases completadas en "eras"/hitos** (rollups) para que `main` no pase de ~8–12 commits. El tag de cada rollup = nº de fases del grupo + `✓`; **la suma de esos tags debe igualar el total de fases completadas**.
- **Una rama por epic/flujo activo** (la fase grande en curso). Sus commits = sus sub-fases o hitos (H1, H2, H3…).
- **`hardening`** (o `qa`) = rama de refuerzo/seguridad/tests si ese trabajo existe como bloque aparte.
- **`roadmap`** = lo que queda por delante. **Sin `merge`** (aún no integrado).
- **`descartes`** = canceladas + diferidas. **Sin `merge`** (callejón sin salida).
- `type: HIGHLIGHT` **solo** en los commits realmente activos (los "NEXT"). Si hay 2 frentes activos, 2 HIGHLIGHT; no más.

Marca el punto de inflexión del proyecto (pivote, cambio de PRD, v2) como un commit propio en `main` antes de abrir las ramas nuevas.

### 4. Construir el `gitGraph`

Sintaxis segura (detalle y ejemplo completo en `reference/conventions.md`):

```
gitGraph
    commit id: "..." tag: "..."
    branch <rama>
    checkout <rama>
    commit id: "..." type: HIGHLIGHT tag: "▶ NEXT"
    checkout main
```

- `id` siempre **entre comillas** y **único en todo el grafo** (Mermaid lo exige).
- `type:` va **antes** de `tag:`.
- Sanea: **no metas comillas dobles ni backticks dentro de un `id`/`tag`**. Sí valen espacios, `-`, `.`, `,`, `+`, `/`, `:`, `✓`, `▶`.
- Orientación por defecto **LR** (como GitHub). Para planes muy largos puedes usar `gitGraph TB:` (vertical).
- Opcional: front matter con `--- / title: ... / ---` para titular el diagrama.

### 5. VALIDAR (obligatorio, antes de entregar)

```
# en el sandbox, una vez:
npm i @mermaid-js/parser >/dev/null 2>&1
node scripts/validate_gitgraph.mjs <ruta-al-archivo>.mermaid
```

El validador corre heurísticas (fence ```, ids duplicados, comillas sin cerrar, `checkout` a ramas inexistentes) **y** el parser real de Mermaid. Si sale `NO COMPILA`, lee la línea/columna del error, corrige y repite. **No entregues nada con exit code ≠ 0.**

### 6. Guardar y renderizar

- Guarda el archivo (p. ej. `docs/plan/git-graph.mermaid` o junto al plan detectado).
- **Renderiza en un artefacto**: usa `show_widget` cargando Mermaid desde CDN (patrón en `assets/render_template.html`) — o, si prefieres un archivo abrible offline, copia `render_template.html`, sustituye `__MERMAID_CODE__` por el cuerpo del `gitGraph` (sin front matter ni fences) y guárdalo como `git-graph.html`.
- Entrega con `present_files` el `.mermaid` (para copiar) y muestra el render.
- Si el usuario eligió también `.md`: crea un `.md` con el bloque dentro de una valla ```mermaid — eso GitHub **sí** lo pinta al abrir el archivo (el problema de las comillas es solo al pegar en mermaid.live).

## Recordatorios

- Si la fuente se infirió de git (sin plan formal), dilo claramente.
- Mantén el grafo legible: **agrupa lo hecho, detalla lo activo.**
- Mismo plan → mismo grafo: respeta la convención de tags y ramas para que sea reproducible.
