# Convención y ejemplo canónico

## Estado → tag

| Estado | Tag | Notas |
|---|---|---|
| Hecho | `"N ✓"` (rollup) o `"✓"` | En `main`, N = nº de fases del grupo; los N suman el total completado |
| En curso | `"▶ NEXT"` + `type: HIGHLIGHT` | Solo los frentes realmente activos |
| Por hacer | `"pend."` / `"post"` / `"agendada"` | |
| Cancelada | `"cancelada"` | Rama `descartes`, sin merge |
| Diferida | `"diferida"` | Rama `descartes`, sin merge |
| Hito | `"hito ..."` | Go-live / release; puede ir en `main` o en `roadmap` |
| Prioridad / bloqueo | `"P0"`, `"P0 bloquea go-live"` | Va en el tag, nunca en una rama |

## Flujo → rama

- `main` — núcleo entregado, agrupado en eras (rollups). ≤ ~8–12 commits.
- `<epic>` (p. ej. `feature`) — la fase grande activa; commits = sus hitos/sub-fases.
- `hardening` / `qa` — refuerzo, seguridad, tests (si existe como bloque).
- `roadmap` — futuro. **Sin merge.**
- `descartes` — canceladas + diferidas. **Sin merge.**

Marca el pivote (cambio de PRD/marca/v2) como un commit en `main` antes de ramificar.

## Reglas de sintaxis que evitan el 99% de los errores

1. **No entregues el código solo como bloque ```mermaid en chat.** Las comillas triples rompen mermaid.live (`Lexer error on line 1`). Entrega archivo o render.
2. `id` entre comillas y **único** en todo el grafo.
3. `type: HIGHLIGHT` **antes** de `tag:`.
4. Nada de comillas dobles ni backticks dentro de un `id`/`tag`. Sí: espacios `-` `.` `,` `+` `/` `:` `✓` `▶`.
5. `checkout <rama>` solo a ramas ya declaradas con `branch`.
6. `roadmap` y `descartes` no hacen `merge`.

## Ejemplo canónico (validado, compila)

Cuerpo de `gitGraph` real (proyecto marketplace multi-tenant). Úsalo como patrón de estilo:

```
gitGraph
    commit id: "1-7 Cimientos" tag: "7 ✓"
    commit id: "13-19 Nucleo del alumno" tag: "7 ✓"
    commit id: "21-26 Pagos + contenido" tag: "5 ✓"
    commit id: "27-34 Admin + integraciones" tag: "8 ✓"
    commit id: "35-39 Pre-lanzamiento" tag: "5 ✓"
    commit id: "40-42 Identidad + Teams" tag: "3 ✓"
    commit id: "45,49,51 Pulido" tag: "3 ✓"
    commit id: "Pivot PRD V6" tag: "marca nueva"
    branch descartes
    checkout descartes
    commit id: "Phase 46 Dev/Prod" tag: "cancelada"
    commit id: "Phase MCP-X TS2589" tag: "cancelada"
    commit id: "19.9 GIF picker" tag: "diferida"
    checkout main
    branch feature
    checkout feature
    commit id: "H1 Foundation 43.1-43.7" tag: "✓ DNS pend."
    commit id: "H2 Migracion 43.8" tag: "✓"
    commit id: "43.10 Pagina Sobre" tag: "✓"
    commit id: "43.11a Plan picker" tag: "✓"
    branch hardening
    checkout hardening
    commit id: "C1 Unicidad compras" tag: "P0 ✓"
    commit id: "C2 Webhook Connect" tag: "P0 ✓"
    commit id: "C3 Aislamiento academy_id" type: HIGHLIGHT tag: "▶ NEXT"
    checkout feature
    commit id: "43.11b Crea tu academia" type: HIGHLIGHT tag: "▶ NEXT"
    commit id: "43.9 Canje de codigo" tag: "pend."
    commit id: "43.12 Email Resend" tag: "P0 bloquea go-live"
    checkout hardening
    commit id: "C4 Enlace guest checkout" tag: "post"
    commit id: "C5 Tests del dinero" tag: "post"
    checkout main
    branch roadmap
    checkout roadmap
    commit id: "Go-live con cliente piloto" tag: "hito bloq 43.12+C3"
    commit id: "Fase 2 post-MVP" tag: "futuro"
```

## Cómo se lee

- Bajar por `main` = la historia entregada (cada commit es un grupo de fases, el tag dice cuántas).
- Una rama que sale y **no vuelve** = trabajo abierto (activo o futuro) o descartado.
- Commit resaltado (HIGHLIGHT, `▶ NEXT`) = lo que se está haciendo ahora mismo.
- Tag con `P0`/`bloquea` = riesgo o dependencia crítica.
