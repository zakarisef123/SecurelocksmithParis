"""Vignettes légères des photos de services (à relancer après avoir changé une photo).

Usage : python3 _src/make_thumbs.py   (nécessite Pillow ; le site lui-même n'en a pas besoin)
Crée assets/img/thumbs/<service>.webp en 480 x 300 à partir de assets/img/photos/<service>.webp.
"""
import glob
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "img", "photos")
OUT = os.path.join(ROOT, "assets", "img", "thumbs")
os.makedirs(OUT, exist_ok=True)
for f in sorted(glob.glob(os.path.join(SRC, "*.webp"))):
    name = os.path.basename(f)
    if name in ("hero-round.webp", "team.webp"):
        continue
    im = Image.open(f).convert("RGB")
    w, h = im.size
    th = round(w / 1.6)
    if th <= h:
        y0 = (h - th) // 2
        im = im.crop((0, y0, w, y0 + th))
    im.resize((480, 300), Image.LANCZOS).save(os.path.join(OUT, name), quality=80, method=6)
    print("vignette", name)
