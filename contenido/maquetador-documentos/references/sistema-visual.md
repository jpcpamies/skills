# Sistema visual — arquitectura CSS y catálogo de componentes

Cómo está construida `assets/plantilla-base.css` y cómo recomponerla para cualquier identidad. La idea es
**no tocar la estructura**: solo cambias los tokens del `:root` (color + tipografía) y eliges qué componentes
usar. Todos los componentes ya están resueltos para WeasyPrint.

---

## 1. Tokens (`:root`) — lo único que sueles cambiar

```css
:root{
  --paper:#FBFAF8;   /* fondo de página */
  --ink:#1E1B17;     /* títulos, wordmark — el tono más oscuro */
  --body:#3C3A36;    /* texto cuerpo, un punto más suave que --ink */
  --muted:#8A8478;   /* etiquetas, eyebrow, metadatos */
  --muted-soft:#A8A293;
  --accent:#9A7B4F;  /* filetes, numerales, código, badges — EL color de marca */
  --accent-faint:#D9CDB8; /* numerales gigantes y fondos suaves del acento */
  --line:#E6E1D8;    /* filete fino */
  --line-soft:#F0ECE3;
  --serif:'Lora', Georgia, serif;        /* titulares y cuerpo editorial */
  --sans:'Poppins','Helvetica Neue',Arial,sans-serif; /* labels, tablas, badges */
}
```

**Regla de los 5 tonos:** casi cualquier identidad se cubre con `paper · ink · body · muted · accent` (+ sus
líneas). Si extraes de un artefacto, mapea: fondo→`--paper`, texto/wordmark→`--ink`, cuerpo→`--body`,
labels→`--muted`, el color de marca o el de los numerales/filetes→`--accent`.

**Pareja tipográfica:** una serif para titulares/cuerpo editorial y una sans para labels/tablas suele bastar.
Si la marca es "producto/tech", invierte: sans para todo y serif solo para acentos. Parejas que funcionan:
Lora+Poppins (editorial cálido), Playfair Display+Inter (lujo), EB Garamond+Work Sans (clásico), Fraunces+
Mona Sans (moderno-editorial). Usa lo que haya en `fc-list`; si no, instala el `.ttf`.

---

## 2. `@page` — márgenes, pie y numeración

```css
@page{
  size:A4;                       /* o letter; añade ' landscape' para horizontal */
  margin:18mm 17mm 20mm 17mm;    /* generoso = aire = premium */
  @bottom-left   { content:"Marca"; ... }              /* running footer */
  @bottom-center { content:"Tagline"; font-style:italic; ... }
  @bottom-right  { content:counter(page) " / " counter(pages); ... }
}
@page:first{ @bottom-left{content:none} @bottom-center{content:none} @bottom-right{content:none} }
```

El pie y la numeración SIEMPRE con `@page`, nunca con divs. `@page:first` limpia el pie en la portada.

---

## 3. Catálogo de componentes (clases de la plantilla)

| Componente | Clase(s) | Para qué |
|---|---|---|
| **Masthead / portada** | `.masthead`, `.brandline`, `.brandtag`, `.rule-center` | Logo + tagline + filete centrado, arriba de la página 1. |
| **Cabecera de documento** | `.eyebrow`, `h1.doc-title`, `.meta`, `.lead` | Etiqueta superior, título grande serif, línea de metadatos, párrafo de entrada. |
| **Índice** | `.toc`, `.toc-item` (`.code`/`.name`) | Lista de bloques con código y descripción al lado. |
| **Bloque de sección** | `.block`, `.block-head`, `.block-letter`, `.partidas`, `.partida` | Letra/numeral gigante tenue + kicker + título + intro en cursiva + lista de partidas con código. |
| **Pull quote** | `.pq` | Cita centrada con filetes arriba/abajo. Da respiro entre secciones. |
| **Encabezado de sección numerada** | `.sec-eyebrow`, `h2.sec`, `.sec-rule` | "Sección 1" + título + filete corto del acento. |
| **Tabla de datos/precio** | `table.price`, `tr.subtotal`, `tr.grand` | Cabecera con filete del acento, filas con hairline, subtotales sombreados, total con doble filete. `td` numéricos a la derecha con `tabular-nums`. |
| **Tabla comparativa** | `table.grid`, `.colstar`, `.yes`/`.no`, `.lvl`/`.price` | Comparativa por columnas con **columna destacada sombreada** y check/guion del acento. |
| **Tarjeta de nivel/opción** | `.tier`, `.tier.star`, `.badge` | Caja con nombre + precio + descripción + lista; la destacada lleva borde y fondo del acento + badge. |
| **Salto/decoy** | `.jump` | Caja con borde-izquierda de acento para resaltar un argumento. |
| **Caja suave** | `.box` (`.bt` título, `.big` cifra) | Bloques tipo "el número en perspectiva", "mínimo garantizado", "cómo seguimos". |
| **Rejilla de pago** | `.pay-grid`, `.pay-col`, `.pay-row` | 2-3 columnas de opciones lado a lado (flex, no grid). |
| **Cierre** | `.closing`, `.signoff`, `.note`, `.divider` | Logo pequeño + frase de cierre + nota legal/fecha. |

Cada componente está en el CSS con un comentario `/* ---------- Nombre ---------- */`. Borra los que no uses.

---

## 4. Reglas de maquetación que mantienen el acabado

- **`break-inside:avoid`** en tarjetas, cajas, filas de partida y `.pay-col` → no se parten entre páginas.
- **`break-after:avoid`** en cabeceras de bloque → no quedan colgadas al final de página.
- **Márgenes generosos + mucho `line-height`** (1.55–1.75 en cuerpo) = sensación premium.
- **`font-variant-numeric:tabular-nums`** en columnas de cifras → números alineados.
- **Filetes hairline** (`1px`/`1.4px` en tonos `--line`/`--accent`), nunca bordes gruesos.
- **Jerarquía por tamaño y color, no por negrita everywhere**: eyebrow pequeña en `--muted`, título grande en
  `--ink`, acentos en `--accent`.
- **Numerales/letras gigantes tenues** (`--accent-faint`) como ancla visual de cada sección — barato y muy
  editorial.

---

## 5. Adaptar la plantilla a una identidad nueva (checklist)

1. Cambia los **5 tonos** del `:root` (extraídos o elegidos).
2. Cambia la **pareja tipográfica** (`--serif`/`--sans`) por fuentes disponibles.
3. Sustituye el **logo** del masthead (SVG inline de la plantilla → tu PNG recortado) y el del cierre.
4. Ajusta el **tagline**, el pie de `@page` y el `size`/orientación si hace falta.
5. Elige el **subconjunto de componentes** que pide el documento; borra el resto.
6. Renderiza, **mira**, corrige. (Paso 5 del SKILL.)

> Lo que hace que parezca caro no es ningún componente concreto: es la **coherencia** (5 tonos, 2 fuentes,
> mucho aire) + el **bucle de revisión visual**.

---

## 6. Ejemplo renderizado (la vara de calidad)

[`ejemplo-render.pdf`](ejemplo-render.pdf) es `assets/plantilla-documento.html` ya convertido a PDF con la
hoja base (marca de demostración «Atelier Nord»). Reúne **todos** los componentes en 3 páginas. Ábrelo
antes de empezar para ver el objetivo de acabado, y compáralo con tu render durante el bucle de revisión
(paso 5 del SKILL).
