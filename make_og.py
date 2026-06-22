#!/usr/bin/env python3
"""Render the Glimwed Open Graph share image (1200x630) using brand assets."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
ROSE  = (230, 108, 149)
INK   = (28, 28, 28)
CREAM = (252, 248, 246)
BLUSH = (246, 231, 235)
LEFT  = 112
USABLE = W - LEFT - 90

GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
MONT    = "Montserrat-410.ttf"
WORDMARK = "/Users/kobojane/Desktop/glimwed/glimwed_parisienne_pink.png"

# --- background: plain white ---------------------------------------------
img = Image.new("RGB", (W, H), (255, 255, 255))

d = ImageDraw.Draw(img)

def tracked_width(text, font, tracking):
    return sum(d.textlength(c, font=font) + tracking for c in text) - tracking

def draw_tracked(xy, text, font, fill, tracking=0, stroke=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill, stroke_width=stroke, stroke_fill=fill)
        x += d.textlength(ch, font=font) + tracking

def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

# --- wordmark: trim transparent padding, scale to target height ----------
mark = Image.open(WORDMARK).convert("RGBA")
mark = mark.crop(mark.getbbox())
LOGO_H = 170
logo_w = round(mark.width * LOGO_H / mark.height)
mark = mark.resize((logo_w, LOGO_H), Image.LANCZOS)

# --- assemble a vertically-centered stack with generous gaps -------------
LABEL_GREY = (90, 80, 84)    # matches the old glimwed.com tone
URL_GREY   = (170, 160, 163) # lighter

f_eye = ImageFont.truetype("Cormorant.ttf", 26)
f_eye.set_variation_by_axes([600])           # SemiBold on the weight axis
f_tag = ImageFont.truetype("Cormorant.ttf", 42)
f_tag.set_variation_by_axes([500])           # Medium on the weight axis
f_url = ImageFont.truetype(MONT, 23)
f_cta = ImageFont.truetype(MONT, 24)

eye_txt = "YOUR VISUAL WEDDING PLANNER"
tag_txt = "Plan every detail by vision boards, and see it all come together."
tag_lines = wrap(tag_txt, f_tag, USABLE)
tag_lh = 50

# CTA pill metrics
CTA_TXT = "Start your free board"
CTA_PADX, CTA_PADY = 34, 17
_asc, _desc = f_cta.getmetrics()
PILL_H = _asc + _desc + 2 * CTA_PADY
PILL_W = round(d.textlength(CTA_TXT, font=f_cta)) + 2 * CTA_PADX

GAP_LOGO = 56   # logo -> label (air below the wordmark)

blocks = [
    ("logo", LOGO_H),
    ("eye",  30),
    ("tag",  tag_lh * len(tag_lines)),
    ("cta",  PILL_H),
]
#       logo->eye   eye->tag   tag->cta
gaps = [GAP_LOGO,   22,        50]
total = sum(h for _, h in blocks) + sum(gaps)
y = (H - total) // 2

for i, (kind, h) in enumerate(blocks):
    if kind == "eye":
        draw_tracked((LEFT, y), eye_txt, f_eye, INK, tracking=6)
    elif kind == "logo":
        img.paste(mark, (LEFT - 4, y), mark)
    elif kind == "tag":
        ly = y
        for line in tag_lines:
            d.text((LEFT, ly), line, font=f_tag, fill=INK)
            ly += tag_lh
    elif kind == "cta":
        # rose pill button
        d.rounded_rectangle([LEFT, y, LEFT + PILL_W, y + PILL_H],
                            radius=PILL_H // 2, fill=ROSE)
        d.text((LEFT + CTA_PADX, y + CTA_PADY), CTA_TXT, font=f_cta, fill=(255, 255, 255))
    y += h + (gaps[i] if i < len(gaps) else 0)

img.save("og-image.png", "PNG")
print("wrote og-image.png", img.size, "logo", mark.size)
