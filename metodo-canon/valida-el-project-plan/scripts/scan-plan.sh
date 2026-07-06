#!/usr/bin/env bash
# scan-plan.sh — medición determinista de un PROJECT_PLAN para el auditor del Método Canon.
#
# Uso:   scripts/scan-plan.sh [RAÍZ_DEL_REPO]      (por defecto, el directorio actual)
# Salida: métricas objetivas a stdout para alimentar la clasificación de tier (§4) y el
#         checklist de coherencia (§10). NO modifica nada. Los umbrales los interpreta el
#         skill revisa-el-project-plan, no este script (el número es un binding, §B5).

set -uo pipefail   # sin -e: grep devuelve 1 cuando no hay match y no debe abortar el scan.
ROOT="${1:-.}"

say() { printf '%s\n' "$*"; }
hr()  { printf -- '---\n'; }
# cuenta ocurrencias literales de un patrón fijo en un fichero (0 si no hay)
countf() { grep -oF "$2" "$1" 2>/dev/null | wc -l | tr -d ' '; }

say "# scan-plan · raíz: $ROOT"
hr

# 1. Localizar el plan ---------------------------------------------------------
PLAN=""
for cand in \
  "$ROOT/PROJECT_PLAN.md" \
  "$ROOT/docs/PROJECT_PLAN.md" \
  "$ROOT/docs/plan/PROJECT_PLAN.md" \
  "$ROOT/docs/plan/index.md"; do
  [ -f "$cand" ] && { PLAN="$cand"; break; }
done
if [ -z "$PLAN" ]; then
  PLAN="$(find "$ROOT" -maxdepth 3 -iname 'PROJECT_PLAN*.md' -not -path '*/node_modules/*' 2>/dev/null | head -1)"
fi

if [ -z "$PLAN" ] || [ ! -f "$PLAN" ]; then
  say "PLAN_FILE: (no encontrado)"
  say "NOTA: sin PROJECT_PLAN localizable. El skill debe preguntar su ubicación o su binding (§B6)."
  exit 0
fi
say "PLAN_FILE:  $PLAN"
say "PLAN_LINES: $(wc -l < "$PLAN" | tr -d ' ')"
hr

# 2. Capas presentes (topología → tier) ----------------------------------------
say "## Capas detectadas (topología)"
[ -f "$ROOT/CHANGELOG.md" ] && say "PRESENTE: CHANGELOG.md" || say "ausente:  CHANGELOG.md"

ARCHIVE_DIR="$(find "$ROOT" -maxdepth 3 -type d -iname 'archive' -not -path '*/node_modules/*' 2>/dev/null | head -1)"
if [ -n "$ARCHIVE_DIR" ]; then
  say "PRESENTE: archive/ → $ARCHIVE_DIR · ficheros: $(find "$ARCHIVE_DIR" -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')"
else
  say "ausente:  archive/"
fi

BACKLOG="$(find "$ROOT" -maxdepth 3 -iname 'backlog.md' -not -path '*/node_modules/*' 2>/dev/null | head -1)"
[ -n "$BACKLOG" ] && say "PRESENTE: backlog.md → $BACKLOG" || say "ausente:  backlog.md"

DECISIONS="$(find "$ROOT" -maxdepth 3 -type d -ipath '*docs/decisions*' 2>/dev/null | head -1)"
[ -n "$DECISIONS" ] && say "PRESENTE: docs/decisions/ → $DECISIONS" || say "ausente:  docs/decisions/"

MEMORY="$(find "$ROOT" -maxdepth 4 -type d -ipath '*.claude/memory*' 2>/dev/null | head -1)"
[ -n "$MEMORY" ] && say "PRESENTE: .claude/memory/ → $MEMORY" || say "ausente:  .claude/memory/"
hr

# 3. Métricas del plan ---------------------------------------------------------
say "## Métricas del plan"
say "H2 (## …):  $(grep -cE '^##[^#]' "$PLAN" 2>/dev/null)"
say "H3 (### …): $(grep -cE '^###[^#]' "$PLAN" 2>/dev/null)"
say "marca ✅:   $(countf "$PLAN" '✅')"
say "marca ⏳:   $(countf "$PLAN" '⏳')"
say "marca 📌:   $(countf "$PLAN" '📌')"
say "checkbox [x]: $(grep -oiE '\[x\]' "$PLAN" 2>/dev/null | wc -l | tr -d ' ')"
say "checkbox [ ]: $(countf "$PLAN" '[ ]')"
say "puntero NEXT/reanudación (líneas): $(grep -ciE 'NEXT|reanud' "$PLAN" 2>/dev/null)"
hr

# 4. Referencias de memoria [[slug]] y su resolución ---------------------------
say "## Referencias de memoria [[slug]]"
REFS="$(grep -oE '\[\[[^]]+\]\]' "$PLAN" 2>/dev/null | sed 's/\[\[//; s/\]\]//' | sort -u)"
if [ -z "$REFS" ]; then
  say "(ninguna)"
else
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    hit="$(find "$ROOT" -maxdepth 4 -type f -iname "*${ref}*" -not -path '*/node_modules/*' 2>/dev/null | head -1)"
    [ -n "$hit" ] && say "RESUELVE: [[$ref]] → $hit" || say "ROTA:     [[$ref]] (sin archivo)"
  done <<< "$REFS"
fi
hr

# 5. CLAUDE.md y su §0 operativo (eje K) -----------------------------------------
say "## CLAUDE.md y su §0 operativo (eje K)"
CLAUDE=""
for cand in "$ROOT/CLAUDE.md" "$ROOT/docs/CLAUDE.md" "$ROOT/.claude/CLAUDE.md"; do
  [ -f "$cand" ] && { CLAUDE="$cand"; break; }
done
if [ -z "$CLAUDE" ]; then
  say "CLAUDE_FILE: (no encontrado) → eje K DURO: sin CLAUDE.md no hay §0 que gobierne el plan."
else
  say "CLAUDE_FILE: $CLAUDE"
  # ¿Hay una sección §0 (encabezado '## 0' / '# 0')?
  if grep -qE '^#{1,3}[[:space:]]*0([.)[:space:]]|$)' "$CLAUDE" 2>/dev/null; then
    say "SECCION_0: presente"
  else
    say "SECCION_0: AUSENTE → eje K DURO: el CLAUDE.md no lleva §0 operativo."
  fi
  # Marcadores de la copia operativa del Standard (cualquiera basta).
  if grep -qiE 'Canon Plan Standard|el plan es la masa|the plan is the mass|Gesti(o|ó)n del PROJECT_PLAN|PROJECT_PLAN Management' "$CLAUDE" 2>/dev/null; then
    say "MARCADOR_STANDARD: presente (parece copia operativa del Standard)"
  else
    say "MARCADOR_STANDARD: ausente (si hay §0, revisar si es realmente la copia operativa del Standard)"
  fi
  # Bindings declarados (bloque 0.A) — señal de §0 instanciado al repo.
  grep -qiE 'Tier actual|bindings? declarad' "$CLAUDE" 2>/dev/null \
    && say "BLOQUE_0A: presente (tier/bindings declarados)" \
    || say "BLOQUE_0A: ausente (el §0 no declara tier ni bindings de este repo)"
fi
hr

say "FIN. Métricas objetivas; la interpretación (tier, defectos) la hace revisa-el-project-plan."
