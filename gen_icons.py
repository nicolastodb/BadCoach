"""
Generate BadCoach PWA icons — logo faithful to the provided image.
Design: white rounded-rect bg, teal shuttle + circle + COACH (vertical) + LIVE.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT   = os.path.join(os.path.dirname(__file__), 'icons')
os.makedirs(OUT, exist_ok=True)

BG      = (244, 246, 247)   # #F4F6F7  — fond blanc légèrement chaud
ACCENT  = (135, 191, 202)   # #87BFCA  — bleu-teal du logo

FONT_BOLD  = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
FONT_REG   = '/usr/share/fonts/truetype/freefont/FreeSans.ttf'

def font(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

def scale(v, s): return v * s / 512

def draw_icon(size, maskable=False, opaque=False):
    s = size
    mode = 'RGB' if opaque else 'RGBA'
    bg   = BG    if opaque else (0, 0, 0, 0)
    img  = Image.new(mode, (s, s), bg)
    d    = ImageDraw.Draw(img, 'RGBA')

    pad = int(s * 0.10) if maskable else 0
    r   = int(s * 0.172)

    # Background rounded rect
    d.rounded_rectangle([pad, pad, s - pad, s - pad], radius=r, fill=BG)

    # ── Cercle outline ────────────────────────────────────
    cx, cy, cr = scale(208, s), scale(252, s), scale(196, s)
    lw = max(2, int(scale(13, s)))
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr],
              outline=ACCENT, width=lw)

    # ── Plumes ────────────────────────────────────────────
    def pts(*coords):
        return [(scale(x, s), scale(y, s)) for x, y in
                zip(coords[::2], coords[1::2])]

    # Plume gauche
    d.polygon(pts(180,374, 70,62, 108,44, 200,366), fill=ACCENT)
    # Plume centrale
    d.polygon(pts(195,364, 180,40, 220,34, 230,364), fill=ACCENT)
    # Plume droite
    d.polygon(pts(222,366, 272,46, 308,64, 246,376), fill=ACCENT)

    # ── Liège ─────────────────────────────────────────────
    lx, ly  = scale(176, s), scale(378, s)
    lw2, lh = scale(72, s),  scale(35, s)
    lr      = max(2, int(scale(5, s)))
    d.rounded_rectangle([lx, ly, lx+lw2, ly+lh], radius=lr, fill=ACCENT)
    # Ligne séparatrice blanche
    sep_y = scale(391, s)
    sep_h = max(2, int(scale(7, s)))
    d.rectangle([lx, sep_y, lx+lw2, sep_y+sep_h], fill=BG)
    # Dôme bas
    ex, ey, erx, ery = scale(212,s), scale(413,s), scale(36,s), scale(19,s)
    d.ellipse([ex-erx, ey-ery, ex+erx, ey+ery], fill=ACCENT)

    # ── Texte COACH (vertical — chaque lettre empilée) ────
    fs_c  = max(8, int(scale(72, s)))
    fnt_c = font(FONT_BOLD, fs_c)
    letters = list('COACH')
    x_c  = scale(383, s)
    y_c  = scale(94, s)
    for ch in letters:
        bb = d.textbbox((0,0), ch, font=fnt_c)
        cw = bb[2]-bb[0]
        ch_h = bb[3]-bb[1]
        d.text((x_c - bb[0] + (scale(72,s)-cw)/2, y_c - bb[1]),
               ch, font=fnt_c, fill=ACCENT)
        y_c += ch_h + max(1, int(scale(4, s)))

    # ── Texte LIVE (horizontal) ────────────────────────────
    fs_l  = max(6, int(scale(34, s)))
    fnt_l = font(FONT_REG, fs_l)
    bb_l  = d.textbbox((0,0), 'LIVE', font=fnt_l)
    d.text((scale(334, s) - bb_l[0], scale(454, s) - bb_l[1]),
           'LIVE', font=fnt_l, fill=ACCENT)

    if opaque:
        return img
    # Composite sur fond blanc pour exports non-transparents (iOS)
    return img

# ── PNG 192 & 512 ──────────────────────────────────────────
for sz in (192, 512):
    draw_icon(sz).save(os.path.join(OUT, f'icon-{sz}.png'))
    print(f'icon-{sz}.png saved')

# ── Maskable 512 ──────────────────────────────────────────
draw_icon(512, maskable=True).save(os.path.join(OUT, 'icon-maskable-512.png'))
print('icon-maskable-512.png saved')

# ── Apple-touch-icon 180×180 opaque ───────────────────────
draw_icon(180, opaque=True).save(os.path.join(OUT, 'apple-touch-icon.png'))
print('apple-touch-icon.png (180x180 opaque) saved')
