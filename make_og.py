#!/usr/bin/env python3
"""Render the Glimwed Open Graph share image (1200x630) using brand colors."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
ROSE  = (230, 108, 149)
PETAL = (234, 202, 205)
TAUPE = (201, 183, 168)
INK   = (28, 28, 28)
CREAM = (252, 248, 246)
BLUSH = (246, 231, 235)

GEORGIA_IT = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
GEORGIA    = "/System/Library/Fonts/Supplemental/Georgia.ttf"
MONT       = "Montserrat-410.ttf"

img = Image.new("RGB", (W, H), CREAM)
px = img.load()
# diagonal gradient cream -> blush
for y in range(H):
    for x in range(W):
        t = (x / W * 0.45) + (y / H * 0.55)
        px[x, y] = tuple(round(CREAM[i] + (BLUSH[i] - CREAM[i]) * t) for i in range(3))

d = ImageDraw.Draw(img)

# decorative palette dots, top-right
for cx, cy, col in [(1010, 120, ROSE), (1082, 120, PETAL), (1046, 184, TAUPE)]:
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=col)

def draw_tracked(draw, xy, text, font, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x

# eyebrow
f_eye = ImageFont.truetype(MONT, 26)
draw_tracked(d, (112, 150), "WEDDING VISION BOARD", f_eye, ROSE, tracking=8)

# wordmark — size down until it fits the usable width
usable = W - 112 - 90
size = 150
while size > 80:
    f = ImageFont.truetype(GEORGIA_IT, size)
    if d.textlength("Glimwed", font=f) <= usable:
        break
    size -= 2
f_word = ImageFont.truetype(GEORGIA_IT, size)
d.text((106, 210), "Glimwed", font=f_word, fill=ROSE)

# tagline — shrink to fit width
tag = "Your wedding's whole look, in one beautiful board."
tsize = 44
while tsize > 24:
    f_tag = ImageFont.truetype(GEORGIA, tsize)
    if d.textlength(tag, font=f_tag) <= usable:
        break
    tsize -= 1
f_tag = ImageFont.truetype(GEORGIA, tsize)
d.text((112, 408), tag, font=f_tag, fill=INK)

# accent rule
d.rounded_rectangle([112, 488, 232, 491], radius=2, fill=ROSE)

# url
f_url = ImageFont.truetype(MONT, 24)
draw_tracked(d, (112, 520), "glimwed.com", f_url, (90, 80, 84), tracking=3)

img.save("og-image.png", "PNG")
print("wrote og-image.png", img.size)
