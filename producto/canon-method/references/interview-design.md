# Bloque 3 — Design (North Star)

> El bloque nuevo y diferencial de CANON. Integra la entrevista de `/impeccable teach` para que generemos PRODUCT.md +
> DESIGN.md upfront y el proyecto pueda SALTARSE teach. Una pregunta a la vez, con sugerencias tailored.
> PIDE referencias visuales (capturas, URLs, marcas nombradas). Cierra con confirmación antes de generar archivos.

Antes de empezar di: "Ahora el sistema visual. Puedes pasarme capturas de pantalla, URLs de inspiración o nombres de
marcas/productos que te gusten. Cuanto más concreto, menos genérico saldrá el diseño."

## D1 — Register (decisión de primer orden)
"¿Esto es una superficie de MARCA (landing, marketing, portfolio: el diseño ES el producto) o de PRODUCTO (app, dashboard, herramienta: el diseño SIRVE al producto)?"
- → `PRODUCT` Register. Condiciona todos los defaults (tipografía, energía de motion, color).

## D2 — Brand personality en 3 palabras reales
"Define la personalidad de marca en 3 palabras CONCRETAS. 'Cálido, mecánico y opinado' es mejor que 'moderno y limpio'."
- Rechaza adjetivos vacíos (moderno, limpio, profesional). Pide palabras con carácter.
- (Reutiliza el eje Personality de Validate V6.) → `PRODUCT` Brand Personality.

## D3 — Referencias visuales (named, no adjetivos)
"¿Qué marcas, productos u objetos impresos te gustan visualmente? Nómbralos. Si tienes capturas o URLs, pásamelas."
- Si el usuario pasa imágenes/URLs, analízalas: extrae paleta, tipografía, densidad, tono.
- → semilla de `DESIGN` (colores, tipografía) + `PRODUCT` (referencias).

## D4 — Anti-references (qué NO debe parecer)
"¿A qué NO quieres parecerte? Nombra marcas/estéticas concretas a evitar."
- (Reutiliza el eje Design de Validate V6.) → `PRODUCT` Anti-references + `DESIGN` Don'ts.

## D5 — Creative North Star
"Vamos a nombrar el sistema: una metáfora que lo gobierne todo. Ejemplos: 'The Editorial Sanctuary', 'Terminal Nativo', 'Cuaderno de Campo'. ¿Qué metáfora captura la sensación que buscas?"
- Propón 2-3 North Stars derivados de D2-D4.
- → `DESIGN` Overview (el North Star encabeza el documento).

## D6 — Estrategia de color
"¿Qué estrategia de color? Restrained (neutros tintados + 1 acento ≤10%), Committed (1 color satura 30-60%), Full palette (3-4 roles), o Drenched (la superficie ES el color)."
- Default product = Restrained; brand identity = Committed. Recuerda: OKLCH, nunca #000/#fff puros (tinta hacia el hue de marca).
- → `DESIGN` Colors.

## D7 — Dirección tipográfica (Two-Voice)
"Tipografía con personalidad, NO Inter/Geist/Space Grotesk por defecto (son tells de AI slop). Propón un par display + body. ¿Registro editorial, técnico/mono, geométrico, humanista?"
- Two-Voice Rule: una display distintiva para títulos + una body refinada. Jerarquía por escala+peso (ratio ≥1.25).
- → `DESIGN` Typography.

## D8 — Energía de motion y forma
"¿Cuánta energía de movimiento? (sobrio / vivo / cinematográfico). ¿Esquinas (radios) marcadas o suaves? Recuerda: nada de bounce/elastic, ease-out exponencial; cards ≤12-16px."
- → `DESIGN` (Layout/Elevation/Shapes según aplique) + notas de motion en Overview.

## D9 — Accesibilidad
"Baseline de accesibilidad: ¿WCAG 2.1 AA en todo (recomendado)? ¿prefers-reduced-motion respetado? ¿contraste verificado?"
- → `PRODUCT` Accessibility & Inclusion.

## Cierre del bloque
Resume el sistema visual y confirma: "Con esto genero los 5 documentos del Canon Method. ¿Procedo?"
Tras el OK, sigue `generate-prd.md`, `generate-product.md`, `generate-design.md`, y luego `generate-claude.md`.
