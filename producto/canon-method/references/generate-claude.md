# Generar CLAUDE.md (capa de proceso)

> Escribe el `CLAUDE.md` del proyecto. ~80% es plantilla fija (esqueleto invariante); ~20% se rellena del PRD (stack,
> estructura, comandos) y del DESIGN.md (visual checklist §13). Hereda el enfoque del gold standard "Isla de los Toros":
> ya reconciliado con Impeccable (§12) y con Two-Voice (sin "Inter para todo").

También: deja en el `CLAUDE.md` (o ejecuta como paso de cierre) la instrucción de traer el framework:
`curl -fsSL https://raw.githubusercontent.com/jpcpamies/canon-framework/main/FRAMEWORK_DEV.md -o docs/FRAMEWORK_DEV.md` (o copia la versión incluida en el skill si no hay red).

Incluye SIEMPRE la §14 (Integraciones externas). Si el PRD (P9) lista integraciones concretas, nómbralas ahí.

## Plantilla (rellena los [slots] desde el PRD/DESIGN)

```markdown
# CLAUDE.md — [Nombre del Proyecto]
> Guía unificada: stack, convenciones, ciclo de desarrollo y reglas de IA. Canon Method.

## 1. Stack Tecnológico
[Del PRD P12. Ej: React 18 (Vite), TS strict, Tailwind v4, shadcn/ui; backend [Convex|Express+Supabase|Hono+Turso];
auth [Clerk|Supabase]; routing Wouter; + librerías específicas del proyecto.]

## 2. Estructura de Carpetas
[Según el stack. client/server/shared o src/+convex/. Incluye docs/ (PRD.md, FRAMEWORK_DEV.md, PRODUCT.md, DESIGN.md) y PROJECT_PLAN.md.]

## 3. Comandos
[Según el stack: install, dev, build, typecheck, db sync/deploy.]

## 4. Reglas de Estilo
- TypeScript strict, sin `any`. Componentes funcionales, hooks.
- Identificadores/comentarios en inglés. UI/textos en español (España peninsular).
- Mobile-first real (375px primero). Imports absolutos con alias `@/`.
- [Reglas específicas del stack: validadores, naming de tablas, auth.]
- Sistema visual: ver `docs/DESIGN.md` (fuente de verdad). Two-Voice (display + body); NO Inter para todo.

## 5. Rol
Eres el lead developer. Planificas y ejecutas directamente. Autonomía completa tras autorización.
Atomicidad: cada subfase = 1-3 archivos, un objetivo, commiteable sola.

## 6. Session Start Protocol
### Estado A: No existe PROJECT_PLAN.md
1. Lee `PRD.md` (y `docs/`: FRAMEWORK_DEV.md, PRODUCT.md, DESIGN.md).
2. Si falta `docs/FRAMEWORK_DEV.md`, tráelo: `curl -fsSL https://raw.githubusercontent.com/jpcpamies/canon-framework/main/FRAMEWORK_DEV.md -o docs/FRAMEWORK_DEV.md`.
3. Crea `PROJECT_PLAN.md` siguiendo el Golden Order de FRAMEWORK_DEV.md adaptado al PRD (subfases atómicas).
4. STOP. Espera "OK".
### Estado B: existe, sin tareas completadas → lee plan, resume, presenta primera tarea → §8.
### Estado C: existe, con tareas completadas → lee plan, reporta estado (fase actual, última/próxima, progreso) → §8.

## 7. Output Rules
Minimalista, ejecutivo, sin redundancia. Conversación en español; código/commits en inglés.

## 8. Development Cycle
A. Present Task (NEXT: [X.Y] — Title / Files / Authorized? → STOP, espera "yes").
B. Execute (autonomía total; reintenta 3x; tras 3 fallos STOP + recomendación).
C. Validate (criterios breves; espera confirmación humana).
D. Close: marca [x] en PROJECT_PLAN + Note; commit `type(X.Y): desc` (≤60 chars, sin Co-Authored-By);
   Security Check condicional (si tocó backend/auth: queries sin auth, inputs sin validar, secretos, fuga entre usuarios, any sensible);
   NUNCA `git push` (lo hace el humano en GitHub Desktop); reporte breve → siguiente tarea.
Todo lo de D es automático, sin pedir permiso.

## 9. Handoff Protocol
Si una tarea requiere acción humana externa (dashboards, DNS, assets): formato HANDOFF con pasos, espera "Done".

## 10. Restricciones Operativas
[Del PRD P9: coste objetivo, límites de rendimiento, mobile targets ≥44px, etc.]

## 11. Qué NO hacer
[Específico del proyecto: no sobredimensionar stack, no abstraer prematuramente, no `--amend`/`push --force`, etc.]

## 12. Impeccable (capa de calidad — Non-slop)
Integra Impeccable (https://impeccable.style). Sintaxis `/impeccable <command> [target]`.
- Setup (Fase 0): `npx impeccable skills install`. NO `teach`/`init` (PRODUCT.md + DESIGN.md ya existen en docs/).
- Contexto: `docs/PRODUCT.md` + `docs/DESIGN.md` (Impeccable los resuelve por fallback a docs/).
- Cuándo invocar (auto, en §8.B): pantalla/componente nuevo → `shape`+`craft`; refinar UI → `polish`/`layout`;
  antes de cerrar visual → `critique`/`audit`; pre-commit → `npx impeccable detect`.
- Cuándo NO: tareas de backend/schema/lógica sin cambio visual.
- Reportar en §8.D: línea `Visual: corrí /impeccable <X>` cuando aplique.
- Anti-patrón: rechazar peticiones monolíticas ("mejora todo el diseño"); granularidad = una pantalla/eje por invocación.

## 13. Visual checklist (obligatorio antes de cerrar subfase visual)
[Derivado del DESIGN.md de este proyecto + bans absolutos de Impeccable. Ej:]
1. Nada de `text-slate-*`/`bg-slate-*` directo → usar tokens semánticos del DESIGN.md.
2. Confirmaciones con `<AlertDialog>`, avisos con toast; nunca `window.confirm/alert`.
3. Touch targets ≥44px en móvil.
4. Títulos en la display del DESIGN.md (Two-Voice); h1/h2 NUNCA en Inter.
5. `backdrop-blur` solo en overlays estructurales.
6. Sin em-dash literal en JSX.
7. Sin microlabel `text-xs uppercase tracking-wide` (salvo carve-out canónico).
8. Sin `border-l/r` >1px (side-stripe ban).
9. Sin nested cards, glass decorativo, gradient text, negro puro fuera de chrome.
10. Icon-only buttons con `aria-label`.
Cerrar subfase visual: correr `/impeccable polish` o `audit` antes de marcar [x]; reportar `Visual: corrí /impeccable <X>`.

## 14. Integraciones externas (bootstrap — paso 0)
Cuando una tarea del PROJECT_PLAN toque un servicio externo (pagos, auth, email, DB, storage, SMS, etc.), ANTES de codear:
1. Descubre qué tooling oficial para Claude Code publica ese servicio (plugin / MCP / agent skills / docs `.md`·`llms.txt`). NO asumas que existe.
2. Propón un plan de instalación numerado y espera OK; verifica la sintaxis de los CLI en la doc oficial (cambian).
3. Instala solo lo que exista; si no hay nada oficial, fallback a docs vía `llms.txt`/`.md` o SDK + doc a mano.
4. Empieza en sandbox/test; OAuth o restricted key en env (nunca claves en el repo); confirmación humana para acciones irreversibles.
5. Reparte: qué hará el MCP y qué hará el humano en el dashboard (claves, webhooks/secretos, onboarding, OAuth inicial).
Protocolo completo y ejemplo (Stripe): `docs/` no aplica aquí — seguir `references/integration-bootstrap.md` del skill Canon. Si el usuario tiene playbook propio de errores, úsalo; ante discrepancia con la doc oficial, manda la oficial.
```

## Cierre del método
Tras escribir los 5 archivos, EXPLICA al usuario (esto es parte del valor):
- **Capa de producto:** PRD.md, PRODUCT.md, DESIGN.md (qué construir).
- **Capa de proceso:** CLAUDE.md, FRAMEWORK_DEV.md (cómo trabajar).
- **Siguientes pasos en Claude Code:** abrir la carpeta → Claude Code lee CLAUDE.md (Estado A) → trae el framework →
  escribe PROJECT_PLAN.md → STOP para tu OK → Fase 0 (scaffold + `npx impeccable skills install` + saltar teach) → build loop.
