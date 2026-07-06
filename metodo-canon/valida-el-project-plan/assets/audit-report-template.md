# AUDIT_PROJECT_PLAN — {{NOMBRE_DEL_REPO}}

> Informe generado por `valida-el-project-plan` (Método Canon) contra el Canon Plan Standard.
> Fecha: {{FECHA}} · Plan auditado: `{{RUTA_DEL_PLAN}}` · **Modo: read-only** (este informe no modifica
> el plan; el reencauce solo se ejecuta con autorización explícita).

## Veredicto

**{{SANO | CON DEUDA | CRÍTICO}}** — {{una frase}}

- **Tier detectado:** {{S | M | L}} — {{justificación con métricas: p. ej. "1 archivo, 6 fases cerradas,
  estado vivo ~80 líneas → cabe holgado; Tier S correcto"}}
- **Invariantes rotos (duros):** {{n}} · **Desajustes (blandos):** {{n}}
- **Bindings del repo detectados:** notación de estado `{{B1}}` · numeración `{{B2}}` · convención de
  commit `{{B3}}` · gate de cierre `{{B4}}` · rutas de capas `{{B6}}`.

## Hallazgos por eje

| Eje | Severidad | Hallazgo | Evidencia | Acción propuesta |
|---|---|---|---|---|
| B · Tier | {{duro/blando/ok}} | {{…}} | {{métrica}} | {{…}} |
| A · Fuente única (I1) | {{…}} | {{…}} | {{…}} | {{…}} |
| C · Estado de un vistazo (I2/§5) | {{…}} | {{…}} | {{líneas vs umbral}} | {{…}} |
| D · Cerrado fuera de la vista (I4) | {{…}} | {{…}} | {{…}} | {{…}} |
| E · Atomicidad + plantilla (I5/§6) | {{…}} | {{…}} | {{…}} | {{…}} |
| F · Trazabilidad (I3/§7) | {{…}} | {{…}} | {{…}} | {{…}} |
| G · Continuidad / NEXT (I6) | {{…}} | {{…}} | {{…}} | {{…}} |
| H · Memorias (I7/§8) | {{…}} | {{…}} | {{refs RESUELVE/ROTA}} | {{…}} |
| I · Coherencia dashboard (§10) | {{…}} | {{…}} | {{contadores vs tablas}} | {{…}} |
| J · Transición de tier (§4/§9) | {{…}} | {{…}} | {{gatillo}} | {{…}} |
| K · CLAUDE.md §0 operativo (§0/§9) | {{…}} | {{…}} | {{¿existe CLAUDE.md? ¿§0? ¿0.A coincide con el tier?}} | {{plantar/refrescar §0}} |

> Orden: defectos duros antes que blandos; lo que hace perder el hilo del estado, primero.

## Reencauce propuesto (requiere tu OK antes de ejecutar)

{{Lista ordenada y atómica. Ejemplos según el caso:}}

1. {{p. ej. "Promoción S→M (§9): crear `CHANGELOG.md`, mover el log del pie, dejar en el archivo solo
   estado vivo + rollup + cola."}}
2. {{p. ej. "Disgregar índice (§5): sacar el detalle de las fases 3–5 cerradas a `archive/`."}}
3. {{p. ej. "Arreglar drift (§10): el dashboard dice 45 fases, las tablas suman 38 — recontar."}}
4. {{p. ej. "Versionar la memoria `[[decision-x]]` (§8): hoy solo vive en local; moverla a
   `docs/decisions/`."}}
5. {{p. ej. "Plantar el `CLAUDE.md §0` (eje K): el repo no lleva la copia operativa del Standard; copiar
   `assets/claude-md-seccion-0.md` como §0 del `CLAUDE.md`, con 0.A instanciado a Tier {{S/M/L}} y los
   bindings detectados." — o "Refrescar el §0: el repo se promocionó a Tier L pero el §0 sigue en Tier S."}}

**Tras ejecutar (si se autoriza):** re-medir el estado vivo, correr el checklist de coherencia §10, **refrescar
el `CLAUDE.md §0`** (bloque 0.A al tier vigente), y no publicar solo si el repo separa el push del humano.

## Checklist de coherencia (§10) — estado

- [ ] Contadores del dashboard cuadran con las tablas.
- [ ] La tabla de archivos lista todos los ficheros reales de `archive/`.
- [ ] La "Active Work" está limpia; el rollup refleja el estado real.
- [ ] Cada `[[memoria]]` referenciada resuelve a un archivo del repo.
- [ ] El estado vivo está dentro del presupuesto de su tier.
- [ ] El tier es el correcto (ni infra, ni sobre-ingeniería).
- [ ] Existe un puntero NEXT / reanudación claro.
- [ ] El `CLAUDE.md` lleva el §0 operativo y su bloque 0.A (tier + bindings) coincide con la realidad.
