#!/usr/bin/env python3
"""Erzeugt die ausgelieferten WebP-Bilder aus den Originalen (nur Pillow noetig).

  screenshots/*.png  ->  screenshots/*.webp   (640 px breit, reicht fuer 2x-Displays bei ~300 px Anzeige)
  CombatCoach_Avata_Logo.png -> assets/logo-128.webp   (Icon fuer Header/Karten; Hero nutzt weiter das PNG)

Aufruf aus dem Repo-Root:  python3 tools/optimize_images.py
"""
import glob, os
from PIL import Image

def save_webp(src, dst, width, quality=80):
    im = Image.open(src).convert("RGBA" if "logo" in dst else "RGB")
    h = round(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS)
    im.save(dst, "WEBP", quality=quality, method=6)
    return im.size, os.path.getsize(src), os.path.getsize(dst)

for png in sorted(glob.glob("screenshots/*.png")):
    size, a, b = save_webp(png, png[:-4] + ".webp", 640)
    print(f"{png:<34} {a/1024:7.0f} KB -> {b/1024:5.0f} KB  {size[0]}x{size[1]}")

size, a, b = save_webp("CombatCoach_Avata_Logo.png", "assets/logo-128.webp", 128, quality=88)
print(f"{'assets/logo-128.webp':<34} {a/1024:7.0f} KB -> {b/1024:5.0f} KB  {size[0]}x{size[1]}")
