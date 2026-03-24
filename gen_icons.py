"""
Generate BadCoach PWA icons — reproduction fidèle du logo original.
Design : fond blanc #F4F6F7, teal #87BFCA, volant + cercle + COACH vertical.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT    = os.path.join(os.path.dirname(__file__), 'icons')
os.makedirs(OUT, exist_ok=True)

BG     = (244, 246, 247)   # #F4F6F7
ACCENT = (135, 191, 202)   # #87BFCA

# Fontes : essayer Impact/FreeSansBold/défaut dans l'ordre
FONT_CANDIDATES = [
    '/usr/share/fonts/truetype/msttcorefonts/Impact.ttf',
    '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]

def best_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try: return ImageFont.truetype(path, size)
            except: pass
    return ImageFont.load_default()

def sc(v, s): return v * s / 512   # scale helper

def draw_icon(size, maskable=False):
    s   = size
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img, 'RGBA')

    pad = int(s * 0.10) if maskable else 0
    r   = max(4, int(s * 0.172))

    # Fond arrondi
    d.rounded_rectangle([pad, pad, s-pad, s-pad], radius=r, fill=BG+(255,))

    # ── Cercle (raquette) ───────────────────────────────────
    cx  = int(sc(210, s));  cy = int(sc(252, s));  cr = int(sc(196, s))
    lw  = max(2, int(sc(13, s)))
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], outline=ACCENT+(255,), width=lw)

    # ── Plumes ──────────────────────────────────────────────
    def pts(*coords):
        return [(sc(x, s), sc(y, s)) for x, y in zip(coords[::2], coords[1::2])]

    d.polygon(pts(180,374, 70,62,  108,44,  200,366), fill=ACCENT+(255,))
    d.polygon(pts(195,364, 180,40, 220,34,  230,364), fill=ACCENT+(255,))
    d.polygon(pts(222,366, 272,46, 308,64,  246,376), fill=ACCENT+(255,))

    # ── Liège ────────────────────────────────────────────────
    lx, ly  = sc(176,s), sc(378,s)
    lw2, lh = sc(72,s),  sc(35,s)
    lr      = max(2, int(sc(5,s)))
    d.rounded_rectangle([lx, ly, lx+lw2, ly+lh], radius=lr, fill=ACCENT+(255,))
    sy_sep  = sc(391,s);  sh_sep = max(2, int(sc(7,s)))
    d.rectangle([lx, sy_sep, lx+lw2, sy_sep+sh_sep], fill=BG+(255,))
    ex, ey  = sc(212,s), sc(413,s)
    erx, ery= sc(36,s),  sc(19,s)
    d.ellipse([ex-erx, ey-ery, ex+erx, ey+ery], fill=ACCENT+(255,))

    # ── COACH vertical — lettres empilées ───────────────────
    fs   = max(6, int(sc(72, s)))
    fnt  = best_font(fs)
    gap  = max(1, int(sc(4, s)))
    x_c  = sc(394, s)
    y_c  = sc(54, s)
    for ch in 'COACH':
        bb  = d.textbbox((0, 0), ch, font=fnt)
        cw  = bb[2] - bb[0]
        ch_h = bb[3] - bb[1]
        d.text((x_c - bb[0] - cw/2, y_c - bb[1]),
               ch, font=fnt, fill=ACCENT+(255,))
        y_c += ch_h + gap

    # Composite sur fond opaque pour exports
    out = Image.new('RGB', (s, s), BG)
    out.paste(img, mask=img.split()[3])
    return out


# PNG 192 & 512
for sz in (192, 512):
    draw_icon(sz).save(os.path.join(OUT, f'icon-{sz}.png'))
    print(f'icon-{sz}.png saved')

# Maskable 512 (safe zone 80%)
draw_icon(512, maskable=True).save(os.path.join(OUT, 'icon-maskable-512.png'))
print('icon-maskable-512.png saved')

# Apple-touch-icon 180×180
draw_icon(180).save(os.path.join(OUT, 'apple-touch-icon.png'))
print('apple-touch-icon.png (180x180) saved')
