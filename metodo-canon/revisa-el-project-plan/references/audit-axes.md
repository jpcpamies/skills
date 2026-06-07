# Ejes de auditoría (A–K)

> Catálogo de lo que `revisa-el-project-plan` comprueba. Cada eje cita su fuente en el **Canon Plan
> Standard** (`canon-plan-standard.md`), se evalúa **relativo al tier** y se mide contra los **bindings
> del repo auditado**, nunca contra los tuyos. Para cada eje: qué mide · cuándo es **defecto duro**
> (invariante roto) · cuándo es **desajuste blando** (binding/tier distinto, no un fallo) · qué evidencia
> recoger para el informe.

**Antes de recorrer los ejes:** clasifica el tier (eje B) — condiciona cómo se juzgan todos los demás.

---

## A · Fuente única de verdad — I1

- **Mide:** que el estado vivo ("qué toca ahora") se lea en **un solo lugar**. No dos sitios que afirmen
  cosas distintas (p. ej. el plan dice una fase activa y un README/issue dice otra).
- **Duro:** existen dos fuentes que se contradicen sobre el estado actual.
- **Blando:** hay punteros redundantes pero **consistentes** (no es defecto; anótalo como nota).
- **Evidencia:** ubicación del plan; cualquier otra fuente de estado y si concuerda.

## B · Clasificación de tier — §4 (eje de control)

- **Mide:** el tier real (**S / M / L**) cruzando topología (¿un archivo? ¿índice + CHANGELOG? ¿+
  `archive/`?) con los gatillos de promoción y las métricas de `scan-plan.sh`.
- **Duro (infra-tier):** un monolito que ya pide capas — el estado vivo no se lee de un vistazo, la
  historia ahoga el presente → debería promocionar (S→M o M→L).
- **Duro (sobre-ingeniería):** capas vacías o testimoniales (`archive/` casi vacío, `backlog.md` de dos
  líneas, CHANGELOG anémico) para un proyecto que cabría holgado en un archivo → **simplifica hacia
  abajo**.
- **Blando:** está en el borde de un gatillo pero aún cabe: anótalo como "vigilar", no como defecto.
- **Evidencia:** tier asignado + 1-2 frases justificándolo con las métricas concretas.

## C · El estado vivo se lee de un vistazo — I2, §5

- **Mide:** que el estado vivo quepa en su **presupuesto de tier** (umbral binding §B5; referencia
  ~200 líneas para índice/estado vivo). En Tier S, la sección de estado del archivo único cumple I2 con
  la historia condensada al pie; desde Tier M, el índice contiene solo lo del §5 (cabecera, dashboard,
  completadas como rollup, fase activa como rollup + NEXT, cola como one-liners).
- **Duro:** el estado vivo supera su presupuesto, o el índice (Tier M/L) arrastra detalle
  `TASK/ACTION/VALIDATION` de sub-fases cerradas o specs completas de fases futuras.
- **Blando:** roza el umbral pero aún se lee de un vistazo.
- **Evidencia:** líneas del estado vivo medidas vs umbral del repo; qué detalle sobra en el índice.

## D · Lo cerrado sale de la vista activa — I4

- **Mide:** que el detalle del pasado se vaya a la historia (pie del archivo en S; CHANGELOG en M;
  `archive/*.md` en L) y el del futuro se reduzca a una línea de cola.
- **Duro:** fases cerradas con todo su detalle siguen en la vista activa para un tier que ya debería
  haberlas archivado.
- **Blando:** en Tier S, tener el log cerrado al pie del mismo archivo **es correcto** — no lo marques.
- **Evidencia:** dónde vive el detalle de lo cerrado; si compite con el estado actual.

## E · Atomicidad y plantilla única — I5, §6

- **Mide:** que cada fase/sub-fase tenga **un** objetivo, sea verificable y commiteable sola, y use la
  **plantilla única §6** (Objetivo · Alcance · Dependencias y secuencia · Decisiones clave · DoD · Fuera
  de alcance · Notas). Una sola plantilla en todo el plan: sin dialectos.
- **Duro:** unidades que mezclan varios objetivos no separables; o ausencia de **Definición de hecho**
  (sin DoD no se puede cerrar); o dialectos de plantilla incompatibles dentro del mismo plan.
- **Blando:** el repo usa nombres de sección equivalentes pero consistentes (binding de formato) — mapea
  y no marques. Rutas de archivo o snippets de código en la entrada: marca como ruido salvo la excepción
  §6 (snippet que codifica una decisión, recortado).
- **Evidencia:** ejemplos de entradas sin DoD o multi-objetivo.

## F · Trazabilidad — I3, §7

- **Mide:** que cada sub-fase cerrada forme la cadena **plan ⇄ commit ⇄ log ⇄ cierre**, medida contra la
  convención del repo: commit (B3), gate de cierre (B4). El método por defecto usa **VALIDATE humano**;
  otro repo puede cerrar con CI verde o review aprobado.
- **Duro:** falta un eslabón de algo marcado como cerrado (cerrado sin commit rastreable, o sin registro
  del gate) → se trata como **no hecho**.
- **Blando:** el repo no usa prefijos `tipo(X.Y)`: **detecta su convención** (Conventional Commits,
  `#issue`, etc.) y mide contra ella. No marques "sin trazabilidad" por no usar la tuya.
- **Evidencia:** convención detectada; sub-fases cerradas con cadena incompleta.

## G · Continuidad / puntero NEXT — I6

- **Mide:** que exista un **NEXT / punto de reanudación** explícito para que la siguiente sesión retome
  sin reconstruir contexto.
- **Duro:** no hay puntero de reanudación, o apunta a algo ya cerrado/inexistente.
- **Blando:** el puntero usa otra etiqueta (`AHORA`, `▶`, "siguiente") pero existe y resuelve.
- **Evidencia:** dónde está el NEXT y a qué apunta.

## H · Memorias y decisiones — I7, §8

- **Mide:** que cada `[[memoria]]`/decisión citada por el plan **resuelva** a un archivo existente y
  legible, y que las memorias que sostienen una **decisión viva** estén **versionadas en el repo**
  (`.claude/memory/`, `docs/decisions/`), no solo en un almacén local de la máquina.
- **Duro:** cita rota (`scan-plan.sh` la marca ROTA); o decisión viva citada que solo vive fuera del repo
  → riesgo de continuidad.
- **Blando:** memorias de "por qué" no citadas por el plan: no es obligatorio versionarlas.
- **Evidencia:** lista de `[[refs]]` y su estado (RESUELVE/ROTA) del scan.

## I · Coherencia del dashboard — §10

- **Mide (sobre todo Tier M/L):** que los contadores del dashboard **cuadren** con las tablas (sin drift
  "45 vs 38"); que la tabla de archivos liste **todos** los ficheros reales de `archive/` (sin huérfanos
  en ninguna dirección); que la "Active Work" refleje el estado real.
- **Duro:** drift entre contadores y tablas; ficheros de `archive/` no listados o listados sin existir.
- **Blando:** en Tier S sin dashboard formal, este eje casi no aplica — verifica solo que el recuento al
  pie no mienta.
- **Evidencia:** números del dashboard vs recuento real del scan.

## J · Transición de tier pendiente — §4 (gatillos), §9

- **Mide:** si saltó un **gatillo de promoción** (S→M: el estado vivo deja de leerse de un vistazo, el
  mini-log compite con el estado; M→L: el CHANGELOG ya no contiene la historia, el índice se infla) y la
  transición está pendiente o a medias.
- **Duro:** gatillo claramente disparado y sin actuar → el §5 dice que disgregar/archivar es la
  **siguiente acción**, no algo cosmético para "luego".
- **Blando:** gatillo no disparado: mantener el tier actual es lo correcto.
- **Evidencia:** qué gatillo, con qué métrica; acción de §9 que tocaría (y que solo se ejecuta con OK).

## K · El CLAUDE.md §0 — la copia operativa del Standard — §0 (Standard), §9

- **Mide:** que el `CLAUDE.md` del repo lleve, como **§0** (lo primero), la **copia operativa del Canon Plan
  Standard**: el principio "el plan es la masa", el bloque de **tier y bindings declarados (0.A)**, y los
  protocolos de lectura/escritura/archivado/memoria/trazabilidad. Es lo que hace que Claude Code **mantenga**
  el plan con la metodología; sin él, montar la infraestructura (archive/, CHANGELOG, capas) no sirve: nadie
  la mantiene y el plan se vuelve a desordenar. La génesis lo planta en Cowork; en un repo adoptado directo en
  Claude Code puede no existir, y `revisa` debe plantarlo (con OK).
- **Duro (ausente):** no hay `CLAUDE.md`, o lo hay pero **sin §0** operativo → el repo no declara su estándar
  ni sus bindings; defecto de proceso y de continuidad (el auditor ni siquiera tiene de dónde leer los
  bindings y cae a detectarlos del plan).
- **Duro (desfasado):** el §0 existe pero **contradice la infraestructura/el tier reales** — p. ej. el repo se
  promocionó a Tier L (hay `archive/` + CHANGELOG) pero el §0 sigue describiendo Tier S, o el bloque 0.A
  declara un tier/bindings que no son los del repo. Tras una transición de tier, un §0 sin refrescar es deuda.
- **Blando:** el §0 existe y es coherente pero usa otros títulos de sub-sección, o omite una capa que el tier
  aún no necesita: mapea y no marques. Diferencias de redacción respecto a la canónica que no cambian el
  contenido: nota, no defecto.
- **Evidencia:** ¿existe `CLAUDE.md`? ¿tiene §0? ¿el tier/bindings de 0.A coinciden con la topología real y
  con el tier del eje B? — del scan (`CLAUDE.md` / marcador del §0) y de la lectura.
- **Acción (solo con OK):** plantar o refrescar el §0 al principio del `CLAUDE.md` desde
  `assets/claude-md-seccion-0.md`, instanciado al tier del eje B y a los bindings detectados. Reemplaza un §0
  existente, nunca lo duplica.

---

## Cómo puntuar el conjunto

- **Veredicto = el peor eje con defecto duro.** Cualquier invariante roto ⇒ veredicto al menos "con
  deuda"; varios o uno de continuidad/fuente-única ⇒ "crítico".
- **Un §0 ausente (eje K) pesa como duro de continuidad:** la infraestructura sin la doctrina que la
  mantiene se vuelve a desordenar. Cuenta para el veredicto aunque el resto del plan esté limpio hoy.
- **Tier correcto + cero duros + §0 coherente + bindings respetados ⇒ "sano"** aunque el formato no sea el
  tuyo.
- Ordena los hallazgos por severidad (duro antes que blando) y por coste de continuidad (lo que hace
  perder el hilo del estado va primero).
