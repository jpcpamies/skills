# Convención y ejemplo canónico

El estado del plan se codifica **dos veces** y deben coincidir: por **color de rama**
(bloque `%%{init}%%`) y por **tag** de cada commit.

## Estado → color → rama → tag

| Estado | Color | Rama | Tag |
|---|---|---|---|
| Cerrado (núcleo) | 🟢 verde `#16a34a` | `main` (rollups por era) | `"✅ CERRADO · N fases"` |
| Cerrado (sub-fase activa) | 🟢 verde `#16a34a` | `<fase>-hecho` | `"✅ CERRADO"` |
| Pivote del proyecto | 🟢 verde (en `main`) | `main` | `"🔀 pivote ..."` |
| Donde estás AHORA (NEXT) | 🔴 rojo `#dc2626` | `ESTAS-AQUI` (1 commit, `type: HIGHLIGHT`) | `"👉 ESTAS AQUI · <id> (NEXT)"` |
| Por hacer | 🟠 naranja `#ea580c` | `por-hacer` (**sin merge**) | `"⏳ ..."` |
| Hito / go-live | 🟠 naranja (en `por-hacer`) | `por-hacer` | `"🎯 hito ..."` |
| Cancelada | ⚪ gris `#9ca3af` | `descartado` (**sin merge**) | `"❌ ... cancelada"` |
| Diferida | ⚪ gris `#9ca3af` | `descartado` (**sin merge**) | `"⏸ ... diferida"` |
| Prioridad / bloqueo | — | (va en el tag) | `"... P0"`, `"... bloquea go-live"` |

## Color por ORDEN DE CREACIÓN de rama (no por nombre)

Mermaid asigna `git0..gitN` por el **orden en que aparecen los `branch`**, no por su nombre.
`main` es siempre `git0`. Con la estructura de ramas de este skill el orden es:

| Índice | Rama | Color |
|---|---|---|
| `git0` | `main` | verde `#16a34a` |
| `git1` | `<fase>-hecho` | verde `#16a34a` |
| `git2` | `ESTAS-AQUI` | rojo `#dc2626` |
| `git3` | `por-hacer` | naranja `#ea580c` |
| `git4` | `descartado` | gris `#9ca3af` |

Si reordenas los `branch`, **reasigna los colores** y actualiza el comentario `%%`.

## Reglas de sintaxis que evitan el 99% de los errores

1. **No entregues el código solo como bloque ```mermaid en chat.** Las comillas triples rompen mermaid.live (`Lexer error on line 1`). Entrega el archivo `.mermaid`.
2. El bloque `%%{init}%%` va en **una sola línea**. El comentario recordatorio va en una línea `%%` aparte. (Si partes el `init` en varias líneas, las intermedias rompen el parser.)
3. `id` entre comillas y **único** en todo el grafo.
4. `type: HIGHLIGHT` **antes** de `tag:`. Y aparece **una sola vez** (en `ESTAS-AQUI`).
5. Nada de comillas dobles ni backticks dentro de un `id`/`tag`. Sí: espacios `-` `.` `,` `+` `/` `:` `·` y los emojis de estado `✅ 👉 ⏳ 🎯 ❌ ⏸ 🔀`.
6. `checkout <rama>` solo a ramas ya declaradas con `branch`.
7. `por-hacer` y `descartado` no hacen `merge`.

## Ejemplo canónico (validado, compila con el parser real)

Patrón de estilo completo. La cadena de la fase activa es continua:
`main → <fase>-hecho → ESTAS-AQUI → por-hacer`; `descartado` cuelga de `main`.

```
%%{init: {'theme':'base','themeVariables':{'git0':'#16a34a','git1':'#16a34a','git2':'#dc2626','git3':'#ea580c','git4':'#9ca3af'}}}%%
%% COLORES POR ORDEN DE CREACION DE RAMA (no por nombre): git0=main(verde) git1=auth-hecho(verde) git2=ESTAS-AQUI(rojo) git3=por-hacer(naranja) git4=descartado(gris)
gitGraph
    commit id: "1-7 Cimientos" tag: "✅ CERRADO · 7 fases"
    commit id: "8-14 Nucleo alumno" tag: "✅ CERRADO · 7 fases"
    commit id: "15-20 Pagos + contenido" tag: "✅ CERRADO · 6 fases"
    commit id: "Pivote PRD V6" tag: "🔀 pivote marca nueva"
    branch auth-hecho
    checkout auth-hecho
    commit id: "21.1 Login Google" tag: "✅ CERRADO"
    commit id: "21.2 Sesiones" tag: "✅ CERRADO"
    commit id: "21.3 Roles" tag: "✅ CERRADO"
    branch ESTAS-AQUI
    checkout ESTAS-AQUI
    commit id: "21.4 Aislamiento academy_id" type: HIGHLIGHT tag: "👉 ESTAS AQUI · 21.4 (NEXT) · P0"
    branch por-hacer
    checkout por-hacer
    commit id: "21.5 Canje de codigo" tag: "⏳ por hacer"
    commit id: "21.6 Email Resend" tag: "⏳ P0 bloquea go-live"
    commit id: "Go-live piloto" tag: "🎯 hito · bloq 21.4+21.6"
    checkout main
    branch descartado
    checkout descartado
    commit id: "Phase 46 Dev/Prod" tag: "❌ cancelada"
    commit id: "19.9 GIF picker" tag: "⏸ diferida"
```

## Cómo se lee

- **Color** = estado: verde cerrado, rojo donde estás ahora, naranja por hacer, gris descartado.
- Bajar por `main` (verde) = la historia entregada; cada commit es un grupo de fases y el tag dice cuántas. La suma de los `N` = total completado.
- La cadena verde→rojo→naranja = la fase activa: lo que ya cerraste, el NEXT y lo que falta.
- Una rama que sale y **no vuelve** = trabajo abierto (`por-hacer`) o descartado (`descartado`).
- El commit rojo resaltado (`type: HIGHLIGHT`, `👉 ESTAS AQUI`) = lo que se está haciendo ahora mismo.
- Tag con `P0`/`bloquea` = riesgo o dependencia crítica.
