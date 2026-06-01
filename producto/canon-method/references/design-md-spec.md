# Spec destilado de DESIGN.md (formato Google Stitch)

> Fuente canónica verificada: github.com/google-labs-code/design.md (paquete npm `@google/design.md`, versión `alpha`).
> Sigue ESTE spec, no resúmenes de segunda mano. Impeccable consume el mismo formato → interoperable sin fricción.

## Estructura: dos capas
1. **YAML front matter** — tokens legibles por máquina (entre `---`).
2. **Cuerpo markdown** — la prosa que explica el *porqué*, en secciones `##`.

## Secciones canónicas (8) — opcionales, pero las presentes en ESTE orden
1. Overview (alias: Brand & Style)
2. Colors
3. Typography
4. Layout (alias: Layout & Spacing)
5. Elevation & Depth (alias: Elevation)
6. Shapes
7. Components
8. Do's and Don'ts

Regla dura: **prohibido duplicar un heading `##`** (el parser lo rechaza). Un heading desconocido se preserva sin error.

## Token schema (YAML)
```yaml
version: alpha
name: <string>
description: <string>   # opcional
colors:
  <token>: "#1A1C1E"    # hex sRGB
typography:
  <token>:
    fontFamily: <string>
    fontSize: <dimension>   # px/em/rem
    fontWeight: <number>    # opcional
    lineHeight: <number>    # opcional
    letterSpacing: <dim>    # opcional
rounded:
  <scale>: <dimension>
spacing:
  <scale>: <dimension|number>
components:
  <name>:
    <prop>: <string | "{path.to.token}">
```

## Tipos de token
- Color: `#` + hex sRGB.
- Dimension: número + unidad (`px`, `em`, `rem`); también valores como `-0.02em`.
- Referencia: `{path.to.token}` (ej. `{colors.primary}`).
- Typography: objeto con fontFamily, fontSize, fontWeight, lineHeight, letterSpacing, fontFeature, fontVariation.

## Componentes
Propiedades válidas: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`.
Variantes (hover/pressed/disabled) = entradas separadas con clave relacionada: `button-primary-hover` (NO anidadas).

## Nombres semánticos (no aparienciales)
Usa `primary`, `surface`, `accent`, `on-primary` — NO `blue`, `gray`.

## Convenciones CANON sobre el spec
- Empieza el Overview con el **Creative North Star** (la metáfora nombrada).
- Color en OKLCH conceptual; nunca #000/#fff puros (tinta hacia el hue de marca).
- Tipografía Two-Voice (display distintiva + body refinada); evita Inter/Geist/Space Grotesk por defecto.
- La sección **Do's and Don'ts** se alimenta del catálogo anti-slop (ver `impeccable-integration.md`): side-stripe borders,
  nested cards, gradient text, gray-on-color, paletas morado/cian, bounce easing, icon-tile sobre heading, em-dash spam.
- Verificación opcional: `npx @google/design.md lint DESIGN.md` (chequea refs rotas, contraste WCAG, orden de secciones).
```
