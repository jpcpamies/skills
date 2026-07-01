#!/usr/bin/env python3
"""
extraer-logo.py — recorta un logo de un artefacto, vuelve transparente el fondo y
recorta al contenido, para que se funda en la página (sin caja blanca/crema).

Uso:
  python3 extraer-logo.py marca.png masthead.png --box 120,60,693,250
  python3 extraer-logo.py marca.png logo.png --box 120,60,693,250 --bg 238,233,222

--box     x0,y0,x1,y1 del lockup (logo + wordmark). Ajusta mirando el recorte.
--bg      umbral de fondo a transparentar: un pixel con r>R y g>G y b>B se vuelve
          transparente. Por defecto 238,233,222 (blanco/crema claro). Sube/baja según
          el fondo del artefacto.
"""
import argparse

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Falta Pillow. Instala:  pip install pillow --break-system-packages")


def main():
    ap = argparse.ArgumentParser(description="Recorta un logo y transparenta el fondo.")
    ap.add_argument("image")
    ap.add_argument("out")
    ap.add_argument("--box", required=True, help="x0,y0,x1,y1")
    ap.add_argument("--bg", default="238,233,222", help="umbral RGB de fondo a transparentar")
    a = ap.parse_args()

    box = tuple(int(x) for x in a.box.split(","))
    R, G, B = (int(x) for x in a.bg.split(","))

    im = Image.open(a.image).convert("RGB").crop(box).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, _ = px[x, y]
            if r > R and g > G and b > B:          # fondo claro -> transparente
                px[x, y] = (r, g, b, 0)

    bbox = im.getbbox()                            # recorta al contenido visible
    if bbox:
        im = im.crop(bbox)
    im.save(a.out)
    print(f"OK -> {a.out}  size={im.size[0]}x{im.size[1]}  (fondo transparente)")


if __name__ == "__main__":
    main()
