# Skills de Jordi Pàmies

Colección pública de *agent skills* para Claude Code / Cowork: IA aplicada,
creación de contenido y productividad.

## Instalación

```bash
/plugin marketplace add jpcpamies/skills
/plugin install jordipamies-skills@jordipamies-skills
/reload-plugins
```

## Skills incluidas

| Skill | Categoría | Qué hace |
|-------|-----------|----------|
| `redactor-linkedin` | contenido | Ghostwriter de LinkedIn: posts de alto engagement con neuropsicología, estructura signature y escaneo de privacidad. |
| `transcripcion-depurada` | contenido | Depura transcripciones de voz a texto (Wispr, Whisper, cualquier STT); identifica y separa hablantes. |
| `maquetador-documentos` | contenido | Convierte contenido que ya tienes en un PDF con **acabado editorial de marca** (HTML/CSS → WeasyPrint): extrae paleta, tipografía y logo de un artefacto, o te **pregunta el estilo** si no hay dirección. Solo maqueta; el contenido lo traes tú. |
| `entrevista-prd-a-proyecto` | metodo-canon | **Génesis del Método Canon** (Cowork): entrevista Validate → PRD → Design y genera los 5 documentos de gobierno. |
| `anade-esto-al-project-plan` | metodo-canon | **Método Canon** (Claude Code): ubica el trabajo ya diseñado en el `PROJECT_PLAN.md` (plantilla única + consciencia de tier). |
| `valida-el-project-plan` | metodo-canon | **Método Canon** (Claude Code): audita la salud del `PROJECT_PLAN.md` contra el Canon Plan Standard y lo sanea con tu OK. |
| `auditar-proyecto` | metodo-canon | **Método Canon** (Claude Code): auditoría senior de código + seguridad + coherencia plan↔código de cualquier repo; entrega un reporte priorizado y un backlog accionable. Read-only. |
| `project-plan-gitgraph` | metodo-canon | **Método Canon** (Claude Code): visualiza el `PROJECT_PLAN.md` como un diagrama Mermaid `gitGraph` con el **estado codificado por color** (verde cerrado · rojo NEXT · naranja por hacer · gris descartado). Entregable único: un archivo `.mermaid` validado con el parser real (sin HTML ni render; lo pegas tú en mermaid.live). |
| `prompt-maestro-craft` | prompting | Genera master prompts en formato C.R.A.F.T. (Contexto, Rol, Acción, Formato, Target). |
| `investigacion-cientifica` | investigacion | Flujo de investigación científica con evidencia Q1 (Consensus.app, NotebookLM). |
| `conocimiento-youtube` | base-de-conocimiento | Descarga incremental de transcripciones de canales/playlists de YouTube → base de conocimiento (.txt + unified.md + registry.json). |
| `actualiza-los-skills` | productividad | **Deploy de este repo**: registra en el manifest las skills nuevas, recoloca las sueltas (preguntando), mantiene el README en sync y **sube la versión** del plugin para que las superficies detecten el cambio; luego commit + permiso para push. |

> **Método Canon** es una *familia* de skills que cubren el ciclo idea→deploy a través de dos
> superficies (Cowork → Claude Code), unidas por el **Canon Plan Standard**: tres skills de ciclo
> (`entrevista-prd-a-proyecto`, `anade-esto-al-project-plan`, `valida-el-project-plan`),
> `auditar-proyecto`, que **audita** el código y su coherencia con el plan, y
> `project-plan-gitgraph`, que **visualiza** el plan como un `gitGraph`. Ver
> [`metodo-canon/METODO_CANON.md`](metodo-canon/METODO_CANON.md). El skill `grill-me` que el método usa en
> el build loop es una dependencia externa (Matt Pocock) y **no** se distribuye aquí; su patrón va integrado
> en la génesis. En `metodo-canon/descatalogados/` se conserva `entrevista-prd` (track No-Code anterior), no
> registrado en el plugin.

## Estructura
Las skills viven en carpetas de **categoría en la raíz del repo** (no hay carpeta `skills/`
intermedia). Cada skill se registra explícitamente en `.claude-plugin/plugin.json`.

```
skills/
├── .claude-plugin/{plugin.json, marketplace.json}
├── contenido/
│   ├── redactor-linkedin/{SKILL.md, references/}
│   ├── transcripcion-depurada/SKILL.md
│   └── maquetador-documentos/{SKILL.md, references/, assets/, scripts/}
├── metodo-canon/
│   ├── METODO_CANON.md             (doc de la familia)
│   ├── entrevista-prd-a-proyecto/  (génesis · Cowork)
│   ├── anade-esto-al-project-plan/ (ubica · Claude Code)
│   ├── valida-el-project-plan/     (audita el plan · Claude Code · + Canon Plan Standard)
│   ├── auditar-proyecto/           (audita el código · Claude Code · seguridad + coherencia plan↔código)
│   ├── project-plan-gitgraph/      (visualiza · Claude Code · gitGraph del plan, estado por color)
│   └── descatalogados/             (no registrados)
├── productividad/
│   └── actualiza-los-skills/       (deploy · mantiene este repo + sube la versión del plugin)
└── <otra-categoría>/<otra-skill>/SKILL.md
```

## Cómo añadir una skill nueva
1. Crea `<categoría>/<nombre>/SKILL.md` (ej. `contenido/mi-skill/SKILL.md`).
2. Añade la ruta al array `skills` de `.claude-plugin/plugin.json`
   (ej. `"./contenido/mi-skill"`).
3. Commit + push (con GitHub Desktop o git).

## Licencia
MIT — ver [LICENSE](LICENSE). Las skills son plantillas: personalízalas con tu
propio perfil y datos.
