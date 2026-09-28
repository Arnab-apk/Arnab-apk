"""
Prepare a portrait photo for clean ASCII conversion:
  1. remove the background (rembg with u2net) so the subject is isolated
  2. auto-crop any empty margins above/below the subject
  3. boost LOCAL contrast (CLAHE) so a flatly-lit face gains highlights and
     shadows -- this turns dark areas into recognizable features
  4. composite the subject onto pure white so the background reads as blank
     (white -> spaces in the ascii ramp)

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.
Run once whenever the source photo changes; the ascii SVG itself is static.

    python scripts/prep_photo.py <input.jpg> [output.png]
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

print(f"Loading input photo from: {INP}")
# 1. cut out the subject using cached u2net session
session = new_session("u2net")
cut = remove(Image.open(INP).convert("RGBA"), session=session)

# 2. auto-crop any large blank margins (e.g. phone screenshot letterboxing)
alpha_init = np.array(cut.split()[-1])
y_indices, x_indices = np.where(alpha_init > 15)
if len(y_indices) > 0:
    y_min, y_max = y_indices.min(), y_indices.max()
    y_span = y_max - y_min
    # if subject occupies less than 85% of vertical space, crop empty areas
    if y_span < cut.size[1] * 0.85:
        pad_top = int(y_span * 0.05)
        pad_bot = int(y_span * 0.03)
        min_y = max(0, y_min - pad_top)
        max_y = min(cut.size[1], y_max + pad_bot)
        cut = cut.crop((0, min_y, cut.size[0], max_y))
        print(f"Auto-cropped subject from Y=[{min_y}, {max_y}] -> size {cut.size}")

rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])                 # 0 = background

# 3. local-contrast the luminance (CLAHE)
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
gray = clahe.apply(gray)

# a touch of global lift so the face sits in the sparse end of the ramp
gray = cv2.convertScaleAbs(gray, alpha=1.05, beta=18)

# 4. paste onto white using the alpha mask (feathered a hair to avoid a halo)
mask = (alpha.astype(np.float32) / 255.0)
mask = cv2.GaussianBlur(mask, (0, 0), 1.0)
out = gray.astype(np.float32) * mask + 255.0 * (1.0 - mask)
out = np.clip(out, 0, 255).astype(np.uint8)

os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
Image.fromarray(out, mode="L").save(OUT)
print("Saved prepped image to:", OUT, out.shape)