<!--
  Plantilla operativa del §0 — la copia del Canon Plan Standard que vive dentro del CLAUDE.md de un repo.

  Qué es: la sección que `valida-el-project-plan` PLANTA O REFRESCA al principio del `CLAUDE.md` del repo
  auditado, para que Claude Code sepa cómo leer, hacer crecer y mantener el plan (sin esto, el auditor monta
  la infraestructura pero nadie la mantiene → el plan se vuelve a desordenar).

  Cómo se usa:
  - Va SIEMPRE como §0, lo primero del `CLAUDE.md` (antes de stack/comandos/estilo). Si ya existe un §0, se
    REEMPLAZA por esta versión re-instanciada al tier vigente; nunca se duplica.
  - Rellena los {{slots}}: el tier detectado (B detectado en la auditoría) y los bindings reales del repo
    (B1–B6). No impongas tus números: usa los del repo.
  - Es agnóstica del proyecto a propósito (se puede levantar tal cual a cualquier CLAUDE.md). El detalle del
    proyecto (stack, rutas, comandos) vive en las secciones siguientes del CLAUDE.md, no aquí.

  Idioma (regla fija):
  - Esta es la ÚNICA copia canónica de las instrucciones, y está en español. No se mantiene una versión por
    idioma: hay esta y ya está.
  - Al plantar, DETECTA el idioma en que está escrito el CLAUDE.md del repo destino y vuelca esta plantilla
    TRADUCIDA a ese idioma. Si no hay CLAUDE.md, usa el idioma del PROJECT_PLAN.md; si tampoco es claro,
    deja el español canónico.
  - Traducir cambia el idioma, NO el contenido: mismas secciones, mismas instrucciones, mismos identificadores
    estables sin traducir — los códigos de sección (0.A, 0.0–0.9), los bindings (B1–B6), los invariantes
    (I1–I7), los marcadores `S/M/L` y `NEXT`, y las rutas de archivo. Solo se traduce la prosa.

  Sincronización: la doctrina canónica es `references/canon-plan-standard.md`. Esta copia operativa debe
  mantenerse alineada con ella; si divergen, manda la canónica.

  Borra este comentario al plantar.
-->

## 0. Gestión del PROJECT_PLAN — LEER PRIMERO (canónico, extraíble)

> Sección autocontenida y agnóstica del proyecto a propósito: es el estándar de cómo se lee, crece y se
> mantiene el plan de **este** repo. Es la copia operativa del **Canon Plan Standard** (fuente canónica:
> `metodo-canon/valida-el-project-plan/references/canon-plan-standard.md`). Si esta copia y la canónica
> divergen, **manda la canónica**.

### 0.A Tier y bindings de este repo (contra lo que mide el enforcer)

- **Tier actual:** `{{S | M | L}}` — {{una frase que lo justifique con métricas: p. ej. "1 archivo, 6 fases
  cerradas, estado vivo ~80 líneas → cabe holgado; Tier S correcto"}}
- **Bindings declarados** (los mandos de este repo; el auditor mide contra estos, no contra otros):
  - **B1 · Notación de estado:** `{{✅ / ⏳ / 📌 | checkboxes [x] | DONE/WIP}}`
  - **B2 · Numeración:** `{{Fase X.Y | numeración semántica | IDs de ticket}}`
  - **B3 · Convención de commit (ancla la trazabilidad):** `{{tipo(X.Y): … | Conventional Commits | #issue}}`
  - **B4 · Gate de cierre (qué significa "validado"):** `{{VALIDATE humano | CI en verde | review aprobado}}`
  - **B5 · Umbrales de tier:** índice/estado vivo ≤ `{{~200}}` líneas · archivo de historia ≤ `{{~2000}}` líneas
  - **B6 · Rutas de capas:** `{{PROJECT_PLAN.md · docs/plan/CHANGELOG.md · docs/plan/archive/ ·
    docs/plan/backlog.md · .claude/memory/ · docs/decisions/}}`

> Al promocionar de tier (§0.9) o cambiar un binding, **actualiza este bloque 0.A**: es la verdad que el
> auditor `valida-el-project-plan` lee para no imponer convenciones ajenas.

### 0.0 Principio rector — "el plan es la masa"

`PROJECT_PLAN.md` es la **única fuente de verdad** de *qué hacer ahora* y *qué se hizo ya*. Cada ciclo de
desarrollo se **lee del plan y se escribe en el plan**. El corolario es estricto:

- **Si el trabajo ocurrió pero el plan no se actualizó, el trabajo NO está hecho.**
- El plan, el log/CHANGELOG, el commit y el cierre humano (VALIDATE) son **una sola transacción**. Ninguno se
  da por bueno sin los demás.

### 0.1 El sistema en capas — según el tier (no colapses las capas)

El plan escala con el proyecto. La topología correcta depende del **tier actual** (0.A):

| Capa | Archivo | Contiene | Límite (binding §B5) | Aplica desde |
|---|---|---|---|---|
| **Índice (estado vivo)** | `PROJECT_PLAN.md` | Estado actual, fase activa (solo rollup), cola pendiente | **≤ ~200 líneas** | Siempre |
| **Log cronológico** | `docs/plan/CHANGELOG.md` | Una entrada por sub-fase cerrada, inverso | sin límite | Tier **M** |
| **Historia (detalle)** | `docs/plan/archive/*.md` | TASK/ACTION/VALIDATION completo de fases cerradas | **≤ ~2000 líneas/fichero** | Tier **L** |
| **Backlog (futuro)** | `docs/plan/backlog.md` | Specs completas de fases **no empezadas** (el índice solo las lista como one-liner) | sin límite | Tier **L** (opcional) |
| **Decisiones (memoria versionada)** | `docs/decisions/*.md` | Copia en el repo de cada memoria que el plan cite (§0.6) | sin límite | Tier **L** (opcional) |

> **Tier S:** todo vive en un solo `PROJECT_PLAN.md` — sin capas, sin `archive/`, sin CHANGELOG separado: un
> mini-log al pie del propio archivo basta. *Esto es correcto, no es deuda.* Las filas de arriba describen el
> **destino** al promocionar, no una obligación inmediata.

### 0.2 El índice es un índice (desde Tier M — regla dura)

Desde Tier M, `PROJECT_PLAN.md` se mantiene **≤ ~200 líneas** y contiene SOLO: cabecera del sistema
documental, Dashboard de estado, tabla de fases completadas (rollup), tareas diferidas, la **fase activa como
rollup** (estado por sub-fase + puntero **NEXT**) y la cola de pendientes **como one-liners**.

**NO** contiene: detalle TASK/ACTION/VALIDATION de sub-fases cerradas (→ `archive/`), ni specs completas de
fases futuras (→ una línea de cola + `backlog.md`).

**Disparador de enforcement:** tras cerrar cualquier sub-fase, si el estado vivo supera su presupuesto de
tier, **disgregar/archivar es la siguiente acción**, no algo cosmético para "luego". Un índice inflado es un
fallo de proceso: es lo que hace perder el hilo del estado.

### 0.3 Protocolo de LECTURA (inicio de sesión)

Lee el **índice** (estado vivo) y nada más. Trae un archivo de `archive/` **solo** cuando necesites historia
de una fase concreta (extender o arreglar trabajo previo). **Nunca leas todos los archivos de historia al
arrancar.** En Tier S, el archivo único *es* el índice.

### 0.4 Protocolo de ESCRITURA (cada sub-fase cierra en el plan)

Cerrar una sub-fase **escribe en el plan** en el mismo aliento que el commit. Una sub-fase está **HECHA** solo
si TODO esto es cierto:

1. Código implementado y el check del proyecto en/por debajo de su baseline.
2. **VALIDATE** del gate de cierre registrado (B4).
3. Plan actualizado: sub-fase marcada en el rollup (B1), puntero **NEXT** avanzado.
4. Nota de 1 línea (archivos tocados, resultado, intentos fallidos si los hubo).
5. Commit con la convención del repo (B3).
6. Entrada de log/CHANGELOG (desde Tier M; en Tier S, el mini-log al pie).
7. Security check si tocó código de servidor/compartido/auth.

### 0.5 Protocolo de ARCHIVADO (al cerrar una FASE — Tier L)

Cuando cierra una **fase** (no solo una sub-fase): mueve el detalle completo a `archive/`, añade la línea de
CHANGELOG, añade la fila a la tabla de completadas, limpia la "Active Work" y parte el archivo de historia si
pasó de ~2000 líneas. **No dejes que una fase cerrada siga viviendo en el índice.** (En Tier S/M no hay
`archive/`: la historia condensada vive al pie o en el CHANGELOG.)

### 0.6 Gestión de MEMORIAS (el "por qué")

Las memorias capturan el **porqué** que el código y el git no guardan: decisiones de arquitectura/producto,
correcciones de rumbo, gotchas reproducibles, puntos de reanudación.

- **Versionado (crítico):** toda memoria que sostenga una **decisión viva citada por el plan** debe estar
  **versionada en el repo** (`.claude/memory/` o `docs/decisions/`). Una memoria citada que solo vive en un
  almacén local de la máquina es un **riesgo de continuidad**: si cambia la máquina, el plan cita fantasmas.
- **Integridad de enlaces:** cada `[[slug]]` citado en el plan resuelve a un archivo existente y legible.
- **Cuándo escribir una:** cuando una decisión es no obvia, fue contestada, o hará falta para retomar después.
  No memorices lo que el repo ya registra.

### 0.7 Invariante de trazabilidad (100%)

Cada sub-fase cerrada forma una cadena completa y mutuamente alcanzable; los **eslabones** son invariantes, su
**formato** es un binding (B3/B4):

```
entrada del plan  ⇄  commit (B3)  ⇄  línea de log/CHANGELOG  ⇄  cierre registrado (B4: VALIDATE)
```

Si falta un eslabón, la sub-fase no es trazable y se trata como **no hecha**.

### 0.8 Checklist de coherencia (al cerrar una fase)

- [ ] Los contadores del Dashboard **cuadran** con la tabla de completadas (sin drift "45 vs 38").
- [ ] La tabla de archivos lista **todos** los ficheros reales de `archive/` (Tier L).
- [ ] La "Active Work" está limpia; el rollup refleja el estado real de las sub-fases.
- [ ] Cada `[[memoria]]` referenciada resuelve a un archivo del repo.
- [ ] El estado vivo está **dentro del presupuesto de su tier**. Si no → disgregar ahora.
- [ ] El **tier es el correcto** (ni infra, ni sobre-ingeniería) y el bloque 0.A lo refleja.
- [ ] Existe un puntero **NEXT / reanudación** claro.

### 0.9 Transición de tier (cuando el plan crece)

Cuando salta un gatillo de promoción, la transición es atómica y deja el §0.A re-instanciado al nuevo tier:

- **S → M:** crear `docs/plan/CHANGELOG.md`; mover el log del pie al CHANGELOG; dejar en el archivo principal
  solo estado vivo + rollup + cola.
- **M → L:** crear `archive/`; mover el detalle de las fases cerradas; dejar en el índice solo rollup + cola +
  completadas; parquear specs futuras en `backlog.md`; versionar en `docs/decisions/` las memorias que el plan
  cite.

Tras cualquier transición: **re-medir** el estado vivo, correr el checklist (§0.8), **actualizar el bloque
0.A** y no publicar solo si el repo separa el push del humano. El skill `valida-el-project-plan` audita y, con
tu OK, ejecuta esta transición y refresca este §0.
