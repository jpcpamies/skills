# Skills de Jordi Pàmies

Colección pública de *agent skills* para Claude Code / Cowork: IA aplicada,
creación de contenido y productividad.

## Instalación

```bash
/plugin marketplace add jpcpamies/skills
/plugin install jordipamies-skills@jordipamies-skills
/reload-plugins
```

> Sustituye `jpcpamies/skills` por tu `usuario/repo` real cuando lo publiques.

## Skills incluidas

| Skill | Categoría | Qué hace |
|-------|-----------|----------|
| `linkedin-ghostwriter` | contenido | Genera posts de LinkedIn de alto engagement. Personalízalo copiando `references/perfil-template.md` a `references/perfil.md`. |
| `transcripcion-depurada` | contenido | Depura transcripciones de voz a texto (Wispr, Whisper, cualquier STT). |
| `canon-method` | producto | Planificación full-stack de apps para desarrollo con IA (Validate → PRD → Design). |
| `prd-interview` | producto | Entrevista estructurada para convertir una idea de app en un PRD. |
| `master-prompt-craft` | prompting | Genera master prompts en formato C.R.A.F.T. |
| `asistente-de-investigacion` | investigacion | Flujo de investigación científica con evidencia Q1 (Consensus, NotebookLM). |

## Estructura
Las skills viven en carpetas de **categoría en la raíz del repo** (no hay carpeta
`skills/` intermedia). Cada skill se registra explícitamente en `plugin.json`.

```
skills/
├── .claude-plugin/{plugin.json, marketplace.json}
├── contenido/
│   └── linkedin-ghostwriter/{SKILL.md, references/}
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
