# Optional: generate pre-masked circular PNGs (transparent background)
# 1) pip install pillow
# 2) put source logos in: images/clients_src/
# 3) run: python tools/make_circle_logos.py

import os
from PIL import Image, ImageOps, ImageDraw

SRC_DIR = "images/clients_src"
OUT_DIR = "images/clients"
SIZE = 512          # output png size
PAD = 0.14          # padding inside circle (0.14 = ~14%)

os.makedirs(OUT_DIR, exist_ok=True)

def make_square(im):
  # fit into square with padding (keeps logo centered)
  im = im.convert("RGBA")
  w, h = im.size
  side = max(w, h)
  bg = Image.new("RGBA", (side, side), (0, 0, 0, 0))
  bg.paste(im, ((side - w)//2, (side - h)//2))
  return bg

def circle_mask(size):
  mask = Image.new("L", (size, size), 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0, 0, size-1, size-1), fill=255)
  return mask

mask = circle_mask(SIZE)

for fname in os.listdir(SRC_DIR):
  if not fname.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
    continue

  src_path = os.path.join(SRC_DIR, fname)
  base = os.path.splitext(fname)[0]
  out_path = os.path.join(OUT_DIR, f"{base}.png")

  im = Image.open(src_path)
  im = make_square(im)

  # scale down a bit so the logo has breathing room in the circle
  target_inner = int(SIZE * (1 - PAD*2))
  im = ImageOps.contain(im, (target_inner, target_inner))
  canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
  canvas.paste(im, ((SIZE - im.size[0])//2, (SIZE - im.size[1])//2), im)

  # apply circle alpha mask
  final = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
  final.paste(canvas, (0, 0), mask)

  final.save(out_path, "PNG")
  print("Wrote:", out_path)
