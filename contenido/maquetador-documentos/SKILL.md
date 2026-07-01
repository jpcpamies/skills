---
name: maquetador-documentos
description: >
  [Cowork · Producción visual] Convierte contenido que YA tienes en un PDF con acabado editorial de marca
  (HTML + CSS → WeasyPrint). Se ocupa SOLO de la maquetación y la identidad visual (paleta, tipografía,
  logo, retícula, componentes), no del contenido: el qué lo traes tú o lo genera otro skill. Úsalo cuando
  digas "maqueta este documento", "hazme un PDF bonito o premium", "un documento con mi identidad visual",
  "dale acabado visual a esto", "conviértelo en PDF con mi marca", "un informe, propuesta o dossier bien
  maquetado", "documento con estilo editorial", o tengas texto o datos listos y quieras un entregable visual
  de alto nivel. Si NO le das dirección visual clara, te PREGUNTA por el estilo (artefacto de marca, paleta,
  tipografía, tono, formato) antes de construir. Si le das un artefacto (logo, web, PDF, captura), extrae su
  paleta, empareja tipografías y reutiliza el logo real. No invoca grill-me ni experto-presupuestos; esos los
  añades tú aparte.
license: MIT
metadata:
  author: Jordi Pàmies
  surface: Cowork (sandbox con WeasyPrint)
---

# Maquetador de Documentos — acabado editorial de marca

`maquetador-documentos` toma **contenido que ya existe** y lo convierte en un **PDF con acabado de marca**:
escribe HTML + una hoja de estilos CSS a medida y la renderiza con **WeasyPrint**. Su único trabajo es la
**capa visual** — identidad, retícula, tipografía y componentes editoriales. El *qué* (el texto, las cifras,
la estructura argumental) lo traes tú o lo produce otro skill.

> 🎯 **Alcance — solo maquetación.** Esto NO escribe el contenido ni decide la oferta, la estrategia ni el
> argumento. Si necesitas generar el fondo (un presupuesto, un post, un acta, una investigación), usa el
> skill que toque ANTES y pásale a este el material ya redactado. Aquí solo se maqueta. No invoques otros
> skills desde aquí.

> ⚙️ **Entorno.** Un sandbox Linux con Python. El skill instala lo que falte: `weasyprint` (HTML/CSS→PDF) y
> `pillow` (muestreo de color y recorte de logo), y usa `poppler-utils` (`pdftoppm`, `pdftotext`, `pdfinfo`)
> para revisar y verificar. Las fuentes se resuelven vía `fontconfig` (`fc-list`).

## Lo que necesita antes de maquetar

**1 · El contenido** — el texto o los datos a maquetar (en el chat, un `.md`, un `.docx`, un PDF, lo que sea).

**2 · La identidad visual** — y aquí hay tres caminos:

| Situación | Qué hace el skill |
|---|---|
| Hay un **artefacto de marca** (logo, web, PDF, captura, documento existente) | **Extrae** la identidad: paleta exacta con `scripts/extraer-paleta.py`, empareja tipografías (`fc-list`) y reutiliza el logo real con `scripts/extraer-logo.py`. |
| Hay **dirección explícita** (colores, fuentes, vibe) | La aplica directamente sobre la plantilla base. |
| **No hay dirección** | **PREGUNTA** por el estilo antes de construir (siguiente sección). Nunca improvisa una identidad a ciegas. |

## Si no hay dirección visual: pregunta primero

Antes de escribir una línea de HTML, si el usuario no ha dado pistas claras de estilo, **pregúntale** (en
Cowork, con la herramienta de preguntas de opción múltiple; en otra superficie, en texto). Cubre como
mínimo:

- **¿Hay un artefacto de marca?** Un logo, una web, un PDF o una captura de la que extraer la identidad.
  Si lo hay, casi todo lo demás se deduce de ahí — pídelo.
- **Paleta / tono** — claro y cálido, oscuro y sobrio, un color corporativo concreto, mucho o poco color.
- **Tipografía** — serif elegante (editorial), sans moderna (producto/tech), o mixto serif+sans.
- **Formalidad y uso** — propuesta a cliente, informe interno, dossier premium, one-pager, etc.
- **Formato** — A4 / carta / slide; vertical u horizontal; densidad (mucho aire vs. compacto).

Con las respuestas, **propón una dirección concreta** (3-5 tokens de color + una pareja tipográfica + una
referencia de estilo) y confírmala en una frase antes de arrancar. Cómo traducir esas respuestas a un
sistema visual está en [`references/extraccion-identidad.md`](references/extraccion-identidad.md).

## Proceso de trabajo

### Paso 1 · Reúne contenido + identidad
Consigue el contenido y resuelve la identidad por uno de los tres caminos de arriba.

### Paso 2 · Extrae la identidad (si hay artefacto)
- **Paleta:** `python3 scripts/extraer-paleta.py <imagen>` → tokens hex (dominantes + acentos saturados +,
  si pasas `--regions`, muestreo de zonas concretas como numerales o wordmark).
- **Tipografías:** `fc-list | grep -iE "<familias>"`; si falta la deseada, usa la más cercana disponible o
  instala un `.ttf`.
- **Logo:** `python3 scripts/extraer-logo.py <imagen> salida.png --box x0,y0,x1,y1` → recorta, vuelve
  transparente el fondo y recorta al contenido, para que se funda en la página sin caja blanca.

Detalle y criterio en [`references/extraccion-identidad.md`](references/extraccion-identidad.md).

### Paso 3 · Construye el HTML + CSS
Parte de [`assets/plantilla-base.css`](assets/plantilla-base.css) y
[`assets/plantilla-documento.html`](assets/plantilla-documento.html). Ajusta **solo las variables de color y
tipografía** del `:root` y compón con los componentes ya hechos (masthead, eyebrow, letra-bloque, lead, pull
quote, tablas de datos/precio, tabla comparativa con columna destacada, tarjetas, cajas, rejilla de pago,
pie con numeración). La arquitectura y el catálogo de componentes están en
[`references/sistema-visual.md`](references/sistema-visual.md). Tienes esa misma plantilla **ya renderizada**
en [`references/ejemplo-render.pdf`](references/ejemplo-render.pdf) (marca de demostración «Atelier Nord»):
es la pieza de muestra y la **vara de calidad** a la que apuntar.

### Paso 4 · Renderiza
`bash scripts/render.sh documento.html documento.pdf [dpi]` → genera el PDF y, además, rasteriza cada página
a PNG (`review_*.png`) para poder revisarla.

### Paso 5 · Bucle de revisión visual — NO te lo saltes
**Mira** cada página rasterizada (en Cowork, con la herramienta de lectura de imágenes). Busca desbordes,
líneas viudas/huérfanas, saltos de página feos, contraste pobre, tablas que se cortan. Corrige el HTML/CSS y
**re-renderiza**. Repite hasta que esté impecable. Este bucle es lo que separa un PDF correcto de uno con
acabado de verdad.

### Paso 6 · Verifica y entrega
- `pdftotext` para comprobar que no se ha colado nada que no debía y que las cifras cuadran.
- Revisa que no haya **glifos rotos** (emojis sin fuente → caja `.notdef`).
- Guarda el PDF donde el usuario quiera y compártelo (en Cowork, con `present_files`).

## Gotchas de WeasyPrint (impórtate esto antes de construir)
- **No ejecuta JavaScript.** Todo es HTML + CSS estático.
- **Flexbox y `@page` sí; CSS Grid es limitado** según versión → usa **flexbox y tablas** para retículas.
- **Los emojis pueden no renderizar** (salen como caja `.notdef`); usa glifos de texto, dingbats con fuente,
  o SVG inline.
- **Imágenes locales:** referencia relativa al HTML (WeasyPrint resuelve desde la ubicación del HTML) o ruta
  absoluta. Para que un logo se funda, hazle el fondo transparente.
- **Tipografías:** del sistema vía fontconfig; para una concreta, instálala o usa `@font-face` con un `.ttf`
  local. Las **variable fonts** se exponen por familia (`font-weight`/`font-style` normales funcionan).
- **Numeración y pies de página:** se hacen con `@page` y `counter(page)`/`counter(pages)`, no con divs.

## Principio de oro
Calidad por **iteración visual**, no a ciegas. Extrae o pregunta la identidad, construye con los componentes,
**mira el resultado**, corrige. Un artefacto de marca real (logo + paleta + fuente) hace el 80 % del trabajo:
**reutilízalo, no lo reinventes** — un logo recortado del original da continuidad perfecta; uno "parecido",
no.
