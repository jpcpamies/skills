#!/usr/bin/env bash
# render.sh — renderiza HTML+CSS a PDF con WeasyPrint y rasteriza cada página
# a PNG para el bucle de revisión visual (paso 5 del SKILL).
#
# Uso:   bash render.sh documento.html documento.pdf [dpi]
# Ej.:   bash render.sh propuesta.html propuesta.pdf 90
#
# Las imágenes/CSS referenciadas se resuelven desde la carpeta del HTML.
set -euo pipefail

IN="${1:?Uso: render.sh entrada.html salida.pdf [dpi]}"
OUT="${2:?Falta la ruta de salida .pdf}"
DPI="${3:-90}"
export PATH="$PATH:$HOME/.local/bin"

# --- Dependencias (instala solo lo que falte) ---
python3 -c "import weasyprint" 2>/dev/null || pip install weasyprint --break-system-packages -q
python3 -c "import PIL"        2>/dev/null || pip install pillow     --break-system-packages -q
command -v pdftoppm >/dev/null 2>&1 || echo "AVISO: poppler-utils (pdftoppm) no está; no podré rasterizar para revisar."

# --- Render HTML -> PDF (usa -m para no depender del PATH) ---
echo "Renderizando $IN -> $OUT ..."
python3 -m weasyprint "$IN" "$OUT"

# --- Info + rasterizado de revisión ---
if command -v pdfinfo >/dev/null 2>&1; then
  echo "Páginas: $(pdfinfo "$OUT" 2>/dev/null | awk '/Pages/{print $2}')"
fi
if command -v pdftoppm >/dev/null 2>&1; then
  base="$(dirname "$OUT")/review_$(basename "${OUT%.pdf}")"
  pdftoppm -png -r "$DPI" "$OUT" "$base" >/dev/null 2>&1
  echo "Revisión (mira estas PNG):"
  ls -1 "${base}"*.png
fi
echo "Hecho."
