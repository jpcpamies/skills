# Generar DESIGN.md

> Escribe `DESIGN.md` siguiendo el spec Stitch (ver `design-md-spec.md`). Lo leen Impeccable y Claude Code.
> Colócalo en la raíz del proyecto o en `/docs/`. Usa las respuestas del bloque de Diseño (D1-D9).

## Pasos
1. **YAML front matter** con tokens derivados de las respuestas:
   - `name`: nombre del sistema (puede ser el North Star).
   - `colors`: paleta semántica (primary, secondary, accent, surface, on-primary…) según la estrategia de color (D6). Hex sRGB.
   - `typography`: pares display/body (D7) con fontFamily/fontSize/weight/lineHeight (Two-Voice, ratio ≥1.25).
   - `rounded`, `spacing`: escalas coherentes (radios suaves ≤12-16px en cards).
   - `components`: al menos button-primary (+ variante hover), input, card, usando referencias `{...}`.
2. **Cuerpo markdown** con las secciones canónicas presentes (en orden), sin duplicar headings:
   - **Overview** — abre con el **Creative North Star** (D5) y una frase de "physical scene" (quién, dónde, qué luz, qué humor) que justifique tema claro/oscuro. Resume la personalidad (D2).
   - **Colors** — explica el porqué de cada rol (no solo el hex). OKLCH conceptual; nunca #000/#fff puros.
   - **Typography** — la lógica Two-Voice y la jerarquía.
   - **Layout** / **Elevation** / **Shapes** — solo si aportan; si no, fold en Overview.
   - **Components** — el porqué de los tokens de componente.
   - **Do's and Don'ts** — Do's del North Star + **Don'ts del catálogo anti-slop** (ver `impeccable-integration.md`), adaptados a las anti-references del usuario (D4).
3. (Opcional) sugiere validar con `npx @google/design.md lint DESIGN.md`.

## Reglas
- No inventes tokens que el usuario no haya implicado; si faltan, usa defaults razonables y márcalos.
- Coherencia con `PRODUCT.md` (mismo register, misma personalidad, mismas anti-references).
- El `DESIGN.md` es la fuente de verdad visual del proyecto — escríbelo para que Claude Code pueda construir desde él.

Tras escribir los tres de producto (PRD, PRODUCT, DESIGN), continúa con `generate-claude.md`.
