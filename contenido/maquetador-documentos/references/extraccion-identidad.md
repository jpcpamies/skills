# Extracción de identidad visual

Cómo conseguir la paleta, las tipografías y el logo para que el documento *sea* de la marca, no solo
"bonito". Tres caminos: **artefacto**, **dirección explícita**, o **preguntar**.

---

## Camino A · Hay un artefacto de marca (logo, web, PDF, captura, doc existente)

Es el mejor caso: el 80 % de la identidad se deduce del artefacto. No reinventes — **extrae y reutiliza**.

### A.1 · Paleta exacta
```bash
python3 scripts/extraer-paleta.py marca.png
# tonos sutiles (numerales, wordmark): pásale regiones x0,y0,x1,y1
python3 scripts/extraer-paleta.py marca.png --regions 40,300,100,380  250,150,560,195
```
El script imprime tres cosas: **dominantes** (quantize — sirven para `--paper` y fondos), **acentos
saturados** (filtro de saturación — el color de marca, `--accent`), y, si pasas `--regions`, el color real de
zonas concretas. Mapea los hex a los 5 tokens (ver `sistema-visual.md §1`). Ojo: los acentos elegantes suelen
ser **poco saturados** (tierras, champagne, salvia) y no salen en el quantize general → por eso el muestreo
por región de numerales/filetes/wordmark.

### A.2 · Tipografías
```bash
fc-list | grep -iE "garamond|cormorant|playfair|lora|inter|poppins|work sans"
```
Identifica la familia del artefacto (o la más parecida) y comprueba si está disponible. Si no, instala el
`.ttf` (o cárgalo con `@font-face`). Para el **wordmark** suele bastar una serif en mayúsculas con mucho
`letter-spacing`; no hace falta la fuente exacta del logo si reutilizas el logo como imagen.

### A.3 · Logo (reutiliza el real)
```bash
python3 scripts/extraer-logo.py marca.png masthead.png --box 120,60,693,250
```
Recorta el logo del artefacto, vuelve **transparente** el fondo (claro/crema/blanco) y recorta al contenido.
Así se funde en la página sin caja. Para encontrar la `--box`: abre el artefacto, estima las coordenadas del
lockup (logo + wordmark) y ajusta mirando el recorte. Reutilizar el logo real da **continuidad perfecta** con
el material existente de la marca.

---

## Camino B · Dirección explícita

El usuario da colores ("verde botella y crema"), fuentes ("algo serif elegante") o un vibe ("tipo Aesop /
Stripe / un periódico"). Tradúcelo a los 5 tokens + pareja tipográfica y **confírmalo en una frase** antes de
construir. Ejemplos de traducción de vibe → arranque:

| Vibe | paper · ink · accent | serif / sans |
|---|---|---|
| Editorial cálido (Kinfolk, Aesop) | crema · marrón casi negro · tierra/champagne | Lora / Poppins |
| Lujo silencioso (boutique) | marfil · negro cálido · oro apagado | Playfair Display / Inter |
| Producto/tech (SaaS, Stripe) | blanco frío · gris tinta · azul/índigo | Inter / Inter (un peso de acento) |
| Corporativo serio (consultoría) | blanco roto · azul marino · azul medio | Source Serif / Source Sans |
| Naturaleza/orgánico | hueso · verde oscuro · salvia/arcilla | Fraunces / Work Sans |

Son **puntos de partida**, no dogmas: ajústalos a lo que diga el usuario.

---

## Camino C · No hay dirección → pregunta (antes de construir)

Si no hay artefacto ni dirección, **pregunta** (en Cowork con la herramienta de opción múltiple; cubre estas
dimensiones, una pregunta por dimensión o agrupadas):

1. **¿Hay un artefacto de marca?** (logo / web / PDF / captura / "no, empezamos de cero"). Si lo hay → Camino A.
2. **Paleta / tono:** claro y cálido · oscuro y sobrio · un color corporativo concreto (¿cuál?) · neutro b/n.
3. **Tipografía:** serif elegante (editorial) · sans moderna (producto) · mixto serif+sans.
4. **Formalidad y uso:** propuesta a cliente · informe interno · dossier premium · one-pager.
5. **Formato:** A4 / carta · vertical u horizontal · denso o con mucho aire.

Con las respuestas, elige una fila de la tabla de vibes como base, fija los **5 tokens + 2 fuentes**, y
propón la dirección en una frase ("voy con crema + tinta marrón + acento champagne, Lora para titulares y
Poppins para etiquetas, A4 con mucho aire — ¿ok?"). Luego construye.

---

## Verificación de identidad (antes de dar por bueno el estilo)

- ¿Los 5 tokens tienen **contraste** suficiente? (`--body` sobre `--paper` debe leerse cómodo; el `--accent`
  no debe competir con el texto.)
- ¿La pareja tipográfica **existe** en el entorno? (`fc-list`); si no, instalada o `@font-face`.
- ¿El logo se **funde** (fondo transparente, sin caja) y tiene resolución suficiente para su tamaño impreso?
- ¿La identidad es **coherente** con el material existente de la marca, si lo hay?
