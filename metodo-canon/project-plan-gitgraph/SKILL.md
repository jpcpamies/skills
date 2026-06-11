---
name: project-plan-gitgraph
description: >-
  [Claude Code · Método Canon] Convierte el `PROJECT_PLAN.md` del repo en un diagrama Mermaid `gitGraph` que codifica el estado del plan POR COLOR (verde = cerrado, rojo = donde estás AHORA/NEXT, naranja = por hacer, gris = descartado). Úsalo SIEMPRE que el usuario diga "muéstrame el project plan", "grafo del plan", "git graph del plan", "diagrama del plan en Mermaid", "pasa el plan a un gitGraph", "el árbol del proyecto", "cómo va el proyecto en un git graph", o pida visualizar el estado/roadmap del proyecto como un árbol estilo Git/GitHub. Lee el PROJECT_PLAN.md como índice y abre `docs/plan/CHANGELOG.md` o `docs/plan/archive/*` solo si necesita estado/fecha concretos. ENTREGABLE ÚNICO: un archivo `.mermaid` VALIDADO con el parser real (compila en mermaid.live). NADA de HTML, render ni artefacto: el usuario lo pega él mismo en mermaid.live. Nunca entrega el código solo como bloque de chat con triple comilla.
---

# project-plan-gitgraph

Convierte el `PROJECT_PLAN.md` de **este repo** en un diagrama Mermaid `gitGraph` que muestra, **de un vistazo y codificado por color**, lo cerrado, el punto donde estás ahora (NEXT), lo que queda y lo descartado. Pensado para correr en **Claude Code** sobre el repo del proyecto.

## Resultado esperado

**Un solo archivo `.mermaid` validado.** Nada más.

- **NADA de HTML, ni render, ni artefacto.** Si el usuario quiere verlo, lo pega él mismo en [mermaid.live](https://mermaid.live).
- El archivo debe **compilar con el parser real** antes de entregarlo (paso 5).

> **Regla de oro (no la rompas):** entrega el **archivo** `.mermaid`. **Nunca** entregues el código únicamente como bloque ```mermaid en el chat: al copiarlo, las líneas de triple comilla viajan con él y mermaid.live falla con `Lexer error on line 1, column 1: unexpected character ->`<-`. Si el usuario quiere el texto para copiar, dale el archivo, no el bloque de chat.

## Procedimiento

### 1. Leer la fuente del plan (índice → detalle solo si hace falta)

1. Abre el **`PROJECT_PLAN.md`** (raíz o `docs/`). Es el **índice**: léelo entero.
2. Abre `docs/plan/CHANGELOG.md` o `docs/plan/archive/*` **solo** si necesitas un estado o una fecha concreta que el índice no da. **No leas todo el histórico.**
3. **Sin `PROJECT_PLAN.md`:** como último recurso, infiere las fases de `git log --oneline` + `git tag`. **Avisa** de que el grafo es inferido del historial, no de un plan escrito.

### 2. Extraer el modelo de fases

Para cada fase / sub-fase saca: **id/título**, **estado**, **fecha** (si hay) y **a qué flujo pertenece** (núcleo cerrado, fase activa, pendiente, descartado). Mapea los marcadores del plan a estos cuatro estados de color:

| Color | Estado | Señales típicas en el plan |
|---|---|---|
| 🟢 **verde** | cerrado / hecho | ✅, `[x]`, "COMPLETE", "cerrada", "mergeada" |
| 🔴 **rojo** | donde estás AHORA (NEXT) | "NEXT", "en curso", "in progress", ▶, "activo" — **solo uno** |
| 🟠 **naranja** | por hacer | `[ ]`, "pendiente", "⏳", "TODO", "por hacer" |
| ⚪ **gris** | descartado / diferido | "CANCELADA", "cancelled", "descartada", "diferida", "stand-by", "aplazada" |

Prioridades (`P0`/`P1`) o bloqueos ("bloquea go-live") van **dentro del tag**, nunca en una rama aparte.

### 3. Codificar el ESTADO POR COLOR (bloque `%%{init}%%`)

El grafo abre con un bloque de tema que fija los colores de rama:

```
%%{init: {'theme':'base','themeVariables':{'git0':'#16a34a','git1':'#16a34a','git2':'#dc2626','git3':'#ea580c','git4':'#9ca3af'}}}%%
%% COLORES POR ORDEN DE CREACION DE RAMA (no por nombre): git0=main(verde) git1=<fase>-hecho(verde) git2=ESTAS-AQUI(rojo) git3=por-hacer(naranja) git4=descartado(gris)
```

- Paleta: **verde** `#16a34a` (cerrado), **rojo** `#dc2626` (NEXT), **naranja** `#ea580c` (por hacer), **gris** `#9ca3af` (descartado).
- **CRÍTICO — `git0..gitN` se asignan por ORDEN DE CREACIÓN de rama, NO por nombre.** `main` es siempre `git0`; la siguiente rama declarada con `branch` es `git1`, la siguiente `git2`, etc. Si cambias el orden de los `branch`, debes reasignar los colores. **Deja siempre el comentario `%%` recordándolo** (segunda línea de arriba) y mapea cada `gitN` a su rama.
- El bloque `%%{init}%%` va en **una sola línea** (si lo partes en varias, las líneas intermedias rompen el parser). El comentario `%%` va aparte.

### 4. Construir el `gitGraph` — estructura de ramas

Crea las ramas en **este orden** para que el mapeo de color de arriba cuadre (main=git0, luego git1, git2, git3, git4):

- **`main`** (verde, `git0`) = **fases cerradas agrupadas en eras**. Cada commit = un grupo; el `tag` dice cuántas fases (`✅ CERRADO · N fases`) y **la suma de los N = total de fases completadas**. Mantén `main` en ~8–12 commits. **Marca el pivote** del proyecto (cambio de PRD/marca/v2) como un **commit propio** en `main` antes de ramificar.
- **`<fase>-hecho`** (verde, `git1`) = **sub-fases ya cerradas de la fase activa** (p. ej. `auth-hecho`). Sale de `main`. Sus commits son las sub-fases con tag `✅ CERRADO`.
- **`ESTAS-AQUI`** (rojo, `git2`) = **UN solo commit** con `type: HIGHLIGHT` y tag `"👉 ESTAS AQUI · <id> (NEXT)"`. Sale de `<fase>-hecho` (continúa la fase activa). **Solo uno** en todo el grafo.
- **`por-hacer`** (naranja, `git3`) = lo pendiente **en orden** + el **hito go-live** al final. Sale de `ESTAS-AQUI`. **SIN `merge`.**
- **`descartado`** (gris, `git4`) = canceladas + diferidas. Sale de `main`. **SIN `merge`.**

`type: HIGHLIGHT` aparece **una sola vez**: en el commit de `ESTAS-AQUI`. Si genuinamente hay dos frentes activos, consúltalo; por defecto, un único NEXT.

### 5. TAGS explícitos (se lee de un vistazo qué está cerrado vs abierto)

| Estado | Tag |
|---|---|
| Cerrado (rollup en main) | `"✅ CERRADO · N fases"` |
| Cerrado (sub-fase) | `"✅ CERRADO"` |
| Pivote | `"🔀 pivote ..."` |
| NEXT (donde estás) | `"👉 ESTAS AQUI · <id> (NEXT)"` |
| Por hacer | `"⏳ ..."` (p. ej. `"⏳ por hacer"`, `"⏳ P0 bloquea go-live"`) |
| Hito / go-live | `"🎯 hito ..."` |
| Cancelada | `"❌ ... cancelada"` |
| Diferida | `"⏸ ... diferida"` |

Prioridad/bloqueo (`P0`, `bloquea go-live`) va **dentro** del tag.

### 6. Sintaxis segura

(Detalle y ejemplo completo validado en `reference/conventions.md`.)

- `id` siempre **entre comillas** y **único en todo el grafo** (Mermaid lo exige).
- `type:` va **antes** de `tag:`.
- **No metas comillas dobles ni backticks dentro de un `id`/`tag`.** Sí valen espacios y `-`, `.`, `,`, `+`, `/`, `:`, `·`, `✅`, `👉`, `⏳`, `🎯`, `❌`, `⏸`, `🔀`.
- `checkout <rama>` solo a ramas ya declaradas con `branch`.
- `por-hacer` y `descartado` **no hacen `merge`**.
- Orientación por defecto **LR** (como GitHub). Para planes muy largos, `gitGraph TB:` (vertical).

### 7. VALIDAR (obligatorio, antes de entregar)

El validador instala el parser **en la carpeta del propio skill**, no en el repo del usuario, así no contamina su proyecto (la carpeta del skill tiene su `.gitignore`):

```
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"   # o la ruta de esta skill
( cd "$SKILL_DIR" && npm i @mermaid-js/parser >/dev/null 2>&1 )
node "$SKILL_DIR/scripts/validate_gitgraph.mjs" <ruta-al-archivo>.mermaid
```

En la práctica, desde la carpeta del skill:

```
cd <ruta-de-esta-skill> && npm i @mermaid-js/parser >/dev/null 2>&1
node scripts/validate_gitgraph.mjs <ruta-absoluta-al-archivo>.mermaid
```

El validador corre heurísticas (fence ```, ids duplicados, comillas sin cerrar, `checkout` a ramas inexistentes, falta del bloque de color) **y** el parser real de Mermaid. Si sale `NO COMPILA`, lee la línea/columna del error, corrige y repite. **No entregues nada con exit code ≠ 0.**

### 8. Entregar

- Guarda **el archivo** (p. ej. `docs/plan/git-graph.mermaid` o junto al `PROJECT_PLAN.md`).
- Entrega **solo el archivo `.mermaid`**. NADA de HTML, render ni artefacto.
- Recuerda al usuario que, si lo quiere ver, lo pega en [mermaid.live](https://mermaid.live).
- **No** pegues el código como único bloque ```mermaid en el chat (rompe mermaid.live al copiar).

## Recordatorios

- **El estado se lee por COLOR** (verde/rojo/naranja/gris) **y por TAG** (✅/👉/⏳/🎯/❌/⏸). Que ambos coincidan.
- `git0..gitN` = **orden de creación de rama**, no nombre. Deja el comentario que lo recuerda.
- Agrupa lo hecho (eras en `main`), detalla la fase activa, marca **un** NEXT.
- Si la fuente se infirió de git (sin `PROJECT_PLAN.md`), dilo claramente.
- Mismo plan → mismo grafo: respeta la convención de ramas, colores y tags para que sea reproducible.
