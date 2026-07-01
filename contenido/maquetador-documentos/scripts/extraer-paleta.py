#!/usr/bin/env python3
"""
extraer-paleta.py — muestrea los colores de un artefacto de marca.

Imprime tres cosas:
  1) DOMINANTES   (quantize)  -> sirven para --paper y fondos.
  2) ACENTOS      (saturados) -> el color de marca (--accent).
  3) REGIONES     (--regions) -> color real de zonas concretas (numerales, wordmark),
                                 que suelen ser poco saturadas y no salen en el quantize.

Uso:
  python3 extraer-paleta.py marca.png
  python3 extraer-paleta.py marca.png --colors 12
  python3 extraer-paleta.py marca.png --regions 40,300,100,380 250,150,560,195
"""
import argparse, colorsys
from collections import Counter

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Falta Pillow. Instala:  pip install pillow --break-system-packages")


def hexof(r, g, b): return f"#{r:02X}{g:02X}{b:02X}"


def dominantes(im, n):
    q = im.resize((140, max(1, int(140 * im.size[1] / im.size[0])))) \
          .quantize(colors=n, method=Image.MEDIANCUT).convert("RGB")
    return sorted(q.getcolors(), reverse=True)


def acentos(im, n=12):
    c = Counter()
    for r, g, b in im.getdata():
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > 0.18 and 0.25 < v < 0.92:           # saturado, ni muy oscuro ni muy claro
            c[(r // 12 * 12, g // 12 * 12, b // 12 * 12)] += 1
    return c.most_common(n)


def region(im, box):
    crop = im.crop(box)
    c = Counter()
    for r, g, b in crop.getdata():
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if not (v > 0.90 and s < 0.10):            # descarta el fondo claro
            c[(r, g, b)] += 1
    return [hexof(*rgb) for rgb, _ in c.most_common(6)]


def main():
    ap = argparse.ArgumentParser(description="Muestrea la paleta de un artefacto de marca.")
    ap.add_argument("image")
    ap.add_argument("--colors", type=int, default=10, help="nº de dominantes (quantize)")
    ap.add_argument("--regions", nargs="*", default=[],
                    help="cajas x0,y0,x1,y1 a muestrear (numerales, wordmark...)")
    a = ap.parse_args()

    im = Image.open(a.image).convert("RGB")
    print(f"# {a.image}  size={im.size[0]}x{im.size[1]}")

    print("\n## DOMINANTES (paper / fondos)")
    for cnt, (r, g, b) in dominantes(im, a.colors):
        print(f"  {hexof(r,g,b)}  x{cnt}")

    print("\n## ACENTOS saturados (accent de marca)")
    for (r, g, b), cnt in acentos(im):
        h = int(colorsys.rgb_to_hsv(r/255, g/255, b/255)[0] * 360)
        print(f"  {hexof(r,g,b)}  hue={h:3d}  x{cnt}")

    for spec in a.regions:
        box = tuple(int(x) for x in spec.split(","))
        print(f"\n## REGION {box}")
        print("  " + "  ".join(region(im, box)))


if __name__ == "__main__":
    main()
