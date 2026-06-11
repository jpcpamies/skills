---
name: actualiza-los-skills
description: Sincroniza y publica el repo de skills de Jordi Pàmies. Úsalo SIEMPRE que el usuario diga "actualiza el manifesto", "actualiza los manifests", "actualiza los skills", "deploy los skills", "deploya las skills", "publica las skills", "registra la skill nueva", "sincroniza los manifests", "sube los cambios del repo de skills", "actualiza el plugin", o cuando haya añadido/editado/movido una skill a mano y quiera dejar el repo listo para que las superficies (Cowork / Claude Code) lo detecten. Revisa qué skills hay en disco, registra en `.claude-plugin/plugin.json` las que falten, recoloca las que estén sueltas en la raíz (preguntando antes a qué categoría van), mantiene el README en sync y —lo más importante— SUBE la versión del plugin en cada cambio para que los marketplaces detecten la actualización incremental. Luego hace commit con mensaje descriptivo y te pide permiso para el push.
---

# Actualiza los skills — sincroniza y publica el repo de skills

Deja el repo de skills de Jordi (`jordipamies-skills`) coherente y **publicable**: cada skill que
existe en disco está registrada en el manifest, cada skill suelta está en su categoría, el README
cuenta la verdad, y —sobre todo— **la versión del plugin ha subido**, que es la única señal que
los marketplaces de las superficies usan para detectar un cambio.

## ⚠️ Regla de oro del versionado (lee esto primero)

**El número de versión es el ÚNICO disparador que tienen los marketplaces (Cowork, Claude Code)
para detectar que el plugin cambió. Si la versión no sube, las superficies NO refrescan la skill,
por muy editado que esté el código.** Por tanto:

- **Nunca dejes el repo con cambios sin haber subido la versión.** Un cambio sin bump es un cambio
  invisible para el marketplace.
- **Fuente única de verdad:** el campo `version` de `.claude-plugin/plugin.json`. **No** pongas
  versión en el frontmatter de las skills ni en `marketplace.json` (esa decisión ya está tomada en
  el repo). `marketplace.json` apunta al plugin entero (`source: "./"`) y no se versiona aparte.
- **Esquema SemVer `MAJOR.MINOR.PATCH`:**
  - **Skill nueva** registrada (o recolocada + registrada) → **+MINOR**, y `PATCH` vuelve a `0`
    (ej. `0.4.0 → 0.5.0`).
  - **Edición** de una skill ya existente, *fix*, o cambios de README/manifest → **+PATCH**
    (ej. `0.4.0 → 0.4.1`).
  - **Cambio rompedor** o reestructura grande → **+MAJOR** (ej. `0.x.y → 1.0.0`), **solo con el OK
    explícito del usuario**.
  - **Si no detectas ningún cambio** pero te piden deploy → **pregunta** si subir `+PATCH` igualmente
    para *forzar* la re-detección (a veces es justo lo que se quiere).
- **Garantía:** al terminar, la versión tiene que ser **estrictamente mayor** que la que había.
  Si dudas qué salto aplicar, aplica al menos `+PATCH`.

## Flujo

```
0. Reconoce el repo  →  1. Escanea skills en disco  →  2. Diagnostica
→  3. Recoloca sueltas (pregunta)  →  4. Registra en plugin.json
→  5. Sube la versión (reglas de arriba)  →  6. Actualiza el README
→  7. Valida  →  8. Commit + pide permiso para push  →  9. Cierre
```

## Paso 0 — Reconoce el repo

Lee `.claude-plugin/plugin.json` (array `skills` + `version`), `.claude-plugin/marketplace.json`
y `README.md`. Forma el inventario de lo que el manifest dice que existe.

## Paso 1 — Escanea las skills en disco

Lista todas las carpetas que contienen un `SKILL.md`. Una skill = una carpeta con `SKILL.md`. Las
categorías son las carpetas de primer nivel (`contenido/`, `metodo-canon/`, `prompting/`,
`investigacion/`, `base-de-conocimiento/`, …). **Excluye siempre** lo que viva bajo
`descatalogados/`: está fuera del plugin a propósito; no lo registres nunca.

## Paso 2 — Diagnostica

Cruza disco ↔ manifest y clasifica:

- **(a) Skills nuevas sin registrar:** carpeta `<categoria>/<nombre>/SKILL.md` en disco que **no**
  está en el array `skills` de `plugin.json`.
- **(b) Skills sueltas en la raíz:** un `SKILL.md` directamente bajo una carpeta de primer nivel que
  **no es una categoría** (es decir, la propia carpeta de la skill cuelga de la raíz). Convención
  del repo: toda skill vive en `<categoria>/<nombre>/`, nunca suelta.
- **(c) Entradas muertas:** rutas registradas en `plugin.json` cuyo `SKILL.md` ya **no existe** en
  disco. **No las borres automáticamente: avísalas** para que el usuario decida.

## Paso 3 — Recoloca las skills sueltas (SIEMPRE pregunta antes)

Por cada skill suelta del paso 2(b): **pregunta al usuario a qué categoría debe ir** (propón la más
coherente según el tema de la skill, leyendo su `SKILL.md`). **No muevas nada sin confirmación.** Con
el OK, mueve la carpeta a `<categoria>/<nombre>/` y continúa. Si no hay categoría que encaje, ofrece
crear una nueva (kebab-case, coherente con las existentes).

## Paso 4 — Registra en el manifest

Añade al array `skills` de `.claude-plugin/plugin.json` la ruta de cada skill nueva o recién
recolocada, en la forma `"./<categoria>/<nombre>"`. Agrupa por categoría para mantener el orden por
temas. No dupliques entradas ya presentes.

## Paso 5 — Sube la versión

Aplica las **reglas de oro del versionado** de arriba sobre el campo `version` de `plugin.json`.
Decide el salto (minor / patch / major / patch-forzado) según lo que detectaste en los pasos 2–4 y
escribe la nueva versión. **Esto no es opcional:** si tocaste cualquier cosa, la versión sube.

## Paso 6 — Actualiza el README

Mantén `README.md` en sync con lo que acabas de cambiar:

- **Tabla "Skills incluidas":** añade/edita la fila de la skill (columna *Skill*, *Categoría*, *Qué
  hace*), en la posición que respete el orden por temas.
- **Árbol de "Estructura":** refleja la nueva carpeta bajo su categoría.
- **Nota de familia** (si la skill entra en una familia documentada, p. ej. Método Canon):
  menciónala donde corresponda.

## Paso 7 — Valida

Antes de commitear, comprueba (un pequeño script de validación es ideal):

- `plugin.json` y `marketplace.json` son **JSON parseable**.
- **Cada ruta** del array `skills` existe en disco **con su `SKILL.md`**.
- **No queda ninguna skill suelta** en la raíz.
- La **versión nueva > versión anterior**.

Si algo falla, **no sigas al commit**: arréglalo o repórtalo.

## Paso 8 — Commit y push (pide permiso)

1. Haz `git add` de lo cambiado y un **commit con mensaje convencional y descriptivo**, p. ej.:
   - Skill nueva: `feat(<categoria>): add <nombre> skill + register + v<nueva>`
   - Edición/fix: `chore(skills): <qué cambió> + v<nueva>`
   - Recolocación: `refactor(skills): mover <nombre> a <categoria> + v<nueva>`
2. **Pide permiso explícito para el push.** Solo si el usuario dice que sí, haz `git push`. Así no
   tiene que abrir GitHub Desktop.

> **Consciencia de entorno (importante).** En el **sandbox de Cowork** git suele estar bloqueado:
> puede haber un `.git/index.lock` colgado que no se puede borrar (`Operation not permitted`) y no
> hay credenciales para push HTTPS. Si `git add`/`commit`/`push` fallan por esto, **no finjas que
> funcionó**: explica el bloqueo, deja los comandos listos para pegar, y recomienda ejecutar esta
> skill desde **Claude Code en el Mac** (git nativo + credenciales de GitHub Desktop), donde el
> flujo commit → permiso → push sí funciona. Para limpiar un lock colgado en el Mac:
> `rm -f .git/index.lock`.

## Paso 9 — Cierre

Resume en pocas líneas: qué skills se registraron/recolocaron, las entradas muertas detectadas (si
las hay), **la versión nueva** (`vX.Y.Z`), y el **estado del push** (hecho / pendiente / bloqueado +
qué hacer).

---

## Reglas de oro (recordatorio final)

- **Nunca** dejes cambios sin subir la versión: un cambio sin bump no lo ve el marketplace.
- La versión vive **solo** en `plugin.json`. `marketplace.json` no se versiona.
- **Pregunta antes** de mover una skill suelta y **antes** de hacer push.
- **No borres** entradas muertas del manifest por tu cuenta: avísalas.
- **Respeta `descatalogados/`:** nunca lo registres.
- Sé honesto con el entorno: si git está bloqueado, dilo y entrega los comandos.
