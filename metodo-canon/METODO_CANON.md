# Método Canon

> Un método repetible para construir aplicaciones web full-stack con IA, **de la idea al deploy**.
> No es una herramienta: es una **familia de skills** que trabajan a través de varias superficies
> (Cowork → Claude Code) compartiendo una misma doctrina. Su objetivo es imponer **tu manera** de
> trabajar a la IA — el mismo criterio, el mismo orden y la misma disciplina en cada sesión, cada
> proyecto y cada ampliación futura.

---

## Por qué existe

**Autonomía ≠ consistencia.** Un modelo capaz no es un modelo predecible. Si le pides a la IA que
construya tu app "como crea conveniente", obtendrás algo distinto cada vez. El Método Canon resuelve
esto convirtiendo *tu forma de trabajar* en un conjunto de documentos y skills que la IA está
obligada a seguir. La repetibilidad es el corazón del método.

**CANON** es ese principio, y también un acrónimo de lo que impone:

| Letra | Principio | Qué significa en la práctica |
|---|---|---|
| **C** | **C**onsistencia | Mismo criterio y mismo formato en todo el ciclo de vida. |
| **A** | **A**tomicidad | Cada unidad de trabajo = 1 objetivo, verificable y commiteable sola. |
| **N** | **N**orth Star | El diseño visual (`DESIGN.md`) se define *antes* y se *aplica*, nunca se improvisa. |
| **O** | **O**rden | El "Golden Order" de fases: cimientos antes que features, backend antes que frontend. |
| **N** | **N**on-slop | Cada cambio visual evita los tics del "AI-slop" y pasa un control de calidad. |

---

## El ciclo de vida — dos superficies, una doctrina

El método cruza dos superficies de Claude. En **Cowork** se hace la génesis (donde es cómodo subir
una base de conocimiento: PDFs de reuniones, manuales, capturas de identidad visual e interfaces).
En **Claude Code** se construye y se mantiene (donde vive el código).

```
┌─ COWORK ───────────────────────────┐     ┌─ CLAUDE CODE (repo local) ──────────────────────────────┐
│                                     │     │                                                          │
│  carpeta del proyecto + base de     │     │  [abres la carpeta]  →  "lee todo esto y empieza"        │
│  conocimiento (pdfs, manuales,      │     │            │                                             │
│  capturas de UI y de marca)         │     │            ▼                                             │
│            │                        │ los │   CLAUDE.md §6 «Estado A»  ←  BOOTSTRAP (no es un skill)  │
│            ▼                        │  5  │   · crea PROJECT_PLAN.md (Tier S) desde Golden Order+PRD  │
│  entrevista-prd-a-proyecto          │ docs│   · Fase 0/1: scaffold + stack + Impeccable              │
│  entrevista Validate → PRD → Design │ ───►│            │                                             │
│            │                        │     │            ▼  build loop (gobernado por CLAUDE.md §8)     │
│            ▼                        │     │                                                          │
│  PRD · PRODUCT · DESIGN             │     │   grill-me ──► añade ──► [construir] ──► revisa           │
│  CLAUDE.md · FRAMEWORK_DEV          │     │   (diseña)    (ubica)                    (audita/sanea)   │
│  (el humano los copia al repo) ─────┼─────┘                                                          │
└─────────────────────────────────────┘     └──────────────────────────────────────────────────────────┘
```

> En el diagrama, `añade` = `anade-esto-al-project-plan`, `revisa` = `valida-el-project-plan`, y
> `grill-me` es la dependencia externa (ver más abajo). Slugs completos en la tabla siguiente.

Lo que mantiene unidas las dos superficies son **dos columnas compartidas** (ver más abajo): el
**Canon Plan Standard** (cómo debe ser el plan) y el **FRAMEWORK_DEV Golden Order** (en qué orden se
construye). Ambas viajan dentro de los documentos que la génesis genera, así que el método se
**auto-propaga**: quien recibe los documentos recibe la doctrina.

---

## La familia de skills

| Paso | Skill | Superficie | Rol | Entrada → Salida |
|---|---|---|---|---|
| **génesis** | `entrevista-prd-a-proyecto` | Cowork | Entrevista guiada (Validate → PRD → Design), con el patrón grill-me integrado. | idea + base de conocimiento → **5 documentos de gobierno** |
| **· bootstrap** | *(no es un skill)* `CLAUDE.md §6` | Claude Code | Lee los 5 docs y arranca el proyecto. | 5 docs → `PROJECT_PLAN.md` (Tier S) + scaffold del stack |
| **diseño** | `grill-me` *(externo · Pocock)* | Claude Code | Interroga el diseño de una feature hasta resolver cada rama del árbol de decisión. | feature difusa → diseño cerrado |
| **ubica** | `anade-esto-al-project-plan` | Claude Code | Coloca el trabajo ya diseñado en el plan (fase nueva o sub-fase), respetando el orden. | contexto de feature → entrada en `PROJECT_PLAN.md` |
| **audita** | `valida-el-project-plan` | Claude Code | Audita la salud del plan contra el Standard y lo sanea (con autorización). | plan → `AUDIT_PROJECT_PLAN.md` + reencauce |
| **visualiza** | `project-plan-gitgraph` | Claude Code | Convierte el plan en un diagrama Mermaid `gitGraph` con el **estado por color** (verde cerrado · rojo NEXT · naranja por hacer · gris descartado), validado con el parser real. | `PROJECT_PLAN.md` → `git-graph.mermaid` (solo el archivo; lo pegas en mermaid.live) |

> **`project-plan-gitgraph` es la *vista* de la familia, no un paso del ciclo.** No edita el plan ni
> impone doctrina: lo *lee* (o lo infiere del historial de git si no hay documento formal) y lo pinta
> como un árbol estilo Git. Apoya las mismas convenciones del **Canon Plan Standard** (estados de fase,
> hitos, eras) para que el mismo plan produzca siempre el mismo grafo. Útil tras `valida-el-project-plan`
> para ver de un vistazo el avance.

> **`grill-me` vive en dos sitios (dual-place).** Su *patrón* —interrogar de forma incansable, rama a
> rama del árbol de diseño, una pregunta a la vez con respuesta recomendada— está **integrado dentro
> de la génesis** (`entrevista-prd-a-proyecto`), donde la fuente a consumir es la base de conocimiento
> subida en vez de un codebase. Como **skill standalone** es una dependencia externa de Matt Pocock
> que el build loop usa en Claude Code; **no se empaqueta ni se distribuye** con este plugin. Si
> quieres el `grill-me` suelto, instálalo aparte.

---

## Las dos columnas compartidas

Toda la familia se apoya en dos artefactos que definen, respectivamente, **cómo debe ser el plan** y
**en qué orden se construye**. Sin ellos, los skills serían herramientas sueltas que casualmente
tocan el mismo archivo; con ellos, son un método.

### 1. El Canon Plan Standard — *cómo debe ser el plan*

La doctrina de qué es un `PROJECT_PLAN` de alto rendimiento: principio rector ("el plan es la masa"),
**invariantes universales** vs **bindings de proyecto**, **tiers S/M/L** que escalan con el tamaño,
plantilla de fase única, trazabilidad y gestión de memorias.

→ Fuente: [`valida-el-project-plan/references/canon-plan-standard.md`](valida-el-project-plan/references/canon-plan-standard.md)

Lo emite `entrevista-prd-a-proyecto` (como `CLAUDE.md §0`), lo conforma `anade-esto-al-project-plan` y
lo hace cumplir `valida-el-project-plan`. Su rasgo clave es la **adaptación al tamaño**: un proyecto
nuevo nace como un solo archivo (**Tier S**) y crece hacia el sistema en capas (índice + CHANGELOG +
`archive/`, **Tier L**) solo cuando los gatillos de promoción lo piden. Nunca te preocupas por el
tamaño del plan: el método te dice cuándo disgregarlo.

### 2. El FRAMEWORK_DEV Golden Order — *en qué orden se construye*

El esqueleto de fases reutilizable y stack-agnostic (Fases 0–11): BOOTSTRAP → SETUP → DATABASE → UI
FOUNDATION → DESIGN SYSTEM → BACKEND API → CONNECTIONS → AUTH → CORE FEATURES → PAYMENTS → POLISH →
DEPLOYMENT. Las fases del `PROJECT_PLAN` derivan de aquí, adaptadas al PRD del proyecto.

→ Fuente: [`entrevista-prd-a-proyecto/references/FRAMEWORK_DEV.md`](entrevista-prd-a-proyecto/references/FRAMEWORK_DEV.md)

---

## Los documentos que gobiernan el proyecto

La génesis (`entrevista-prd-a-proyecto`) produce cinco documentos en dos capas. A ellos se suma el
`PROJECT_PLAN.md`, que nace ya en Claude Code (bootstrap).

**Capa de producto** (*qué construir*, por proyecto):
- `PRD.md` — negocio, IA, datos, pantallas, monetización, métricas.
- `PRODUCT.md` — estrategia y marca (lo lee el motor de calidad Impeccable).
- `DESIGN.md` — sistema visual en formato Google Stitch (tokens + North Star + Don'ts).

**Capa de proceso** (*cómo trabajar*, reutilizable):
- `CLAUDE.md` — comportamiento de Claude Code; **incluye el Canon Plan Standard como §0**.
- `FRAMEWORK_DEV.md` — el Golden Order (se copia a `docs/`).

**El estado vivo** (nace en Claude Code):
- `PROJECT_PLAN.md` — la única fuente de verdad de qué hacer ahora y qué se hizo. Gobernado por el
  Canon Plan Standard.

---

## Cómo se usa, paso a paso

1. **Cowork — génesis.** Crea la carpeta del proyecto, sube la base de conocimiento (PDFs, manuales,
   capturas de marca e interfaces) y lanza `entrevista-prd-a-proyecto`. Te entrevistará en tres
   bloques (Validate → PRD → Design) y generará los 5 documentos.
2. **Transferencia.** Copia los 5 documentos a la carpeta de tu repo de GitHub en local.
3. **Claude Code — arranque.** Abre la carpeta, activa el modo de máxima potencia (ultracode) y di
   *"lee todo esto y empieza"*. Claude Code leerá `CLAUDE.md`, entrará en el **Estado A** y:
   creará el `PROJECT_PLAN.md` (Tier S, conforme al Standard) desde el Golden Order + PRD, parará
   para tu OK, y luego hará el scaffold del stack (Fase 0/1).
4. **Build loop.** A partir de ahí, el ciclo de cada feature: `grill-me` (cierra el diseño) →
   `anade-esto-al-project-plan` (lo ubica en el plan) → construir (gobernado por `CLAUDE.md §8`) → y,
   cuando el plan crezca, `valida-el-project-plan` para auditarlo y promocionarlo de tier.

---

## Distribución — extrapolable a otros

La familia se publica como un **plugin de Claude Code** (MIT, público), instalable por cualquiera:

```bash
/plugin marketplace add jpcpamies/skills
/plugin install jordipamies-skills@jordipamies-skills
/reload-plugins
```

La extrapolabilidad no depende de que el otro conozca tu doctrina: `entrevista-prd-a-proyecto` la
**inyecta** en el `CLAUDE.md` de su proyecto. A partir de ahí, su Claude Code construye con tu mismo
criterio, y `anade-esto-al-project-plan` / `valida-el-project-plan` mantienen su plan con tu mismo
estándar — con *sus* convenciones de casa (bindings), no las tuyas impuestas.

> **Nota sobre `grill-me`:** no se distribuye dentro del plugin (su patrón ya va integrado en la
> génesis). Quien quiera el skill `grill-me` suelto en su build loop lo instala por separado.

---

## Descatalogado: `entrevista-prd` (track No-Code anterior)

En `descatalogados/entrevista-prd` se conserva, solo como referencia histórica, el skill
`entrevista-prd`: una entrada más ligera que conducía una entrevista de 12 preguntas y generaba un
**PRD en PDF** orientado a construir con herramientas **No-Code/Low-Code** (Lovable, Bolt, V0,
Cursor). Lo **sustituye** la génesis `entrevista-prd-a-proyecto`, que cubre ese arranque y además
produce los 5 documentos markdown que gobiernan un desarrollo full-stack en Claude Code. `entrevista-prd`
**no se registra en `plugin.json`** ni se distribuye.

---

## Estado de la familia

> Consolidación bajo el Canon Plan Standard. Estado a 2026-06-07:

- ✅ **Canon Plan Standard** redactado (la columna), bajo `valida-el-project-plan/references/`.
- ✅ Familia renombrada a slugs descriptivos y carpeta-método `metodo-canon/`.
- ✅ Patrón grill-me integrado en la génesis (auto-resolución desde la KB · incansable · árbol 1-a-1
  con recomendación).
- ✅ Etiqueta de familia `[Superficie · Método Canon]` al inicio de cada `description`.
- ✅ Añadida la *vista* de la familia: `project-plan-gitgraph` (Claude Code · gitGraph del plan con estado por color).
- ⏳ `valida-el-project-plan` — `SKILL.md` auditor en construcción sobre el Standard.
- ⏳ Alineación al Standard de `anade-esto-al-project-plan` (plantilla única §6 + consciencia de tier)
  y de `generate-claude` (emitir el Standard como `CLAUDE.md §0` + crear el plan en Tier S).

---

*Método Canon · familia `metodo-canon` · by Jordi Pàmies · MIT.*
