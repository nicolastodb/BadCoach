"""
Generate BadCoach PWA icons — fond navy app, raquette + volant verts.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT    = os.path.join(os.path.dirname(__file__), 'icons')
os.makedirs(OUT, exist_ok=True)

BG      = (10,  22,  40)    # #0a1628 — fond navy app
GREEN   = (0,   230, 118)   # #00e676
CYAN    = (0,   229, 255)   # #00e5ff
WHITE   = (255, 255, 255)

FONT_BOLD = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'

def font(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

def scale(v, s): return v * s / 512

def draw_icon(size, maskable=False):
    s   = size
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img, 'RGBA')

    pad = int(s * 0.10) if maskable else 0
    r   = max(4, int(s * 0.172))

    # Fond arrondi navy
    d.rounded_rectangle([pad, pad, s-pad, s-pad], radius=r, fill=BG+(255,))

    cx  = int(scale(220, s))
    cy  = int(scale(210, s))
    cr  = int(scale(168, s))
    lw  = max(2, int(scale(16, s)))

    # Cercle raquette
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], outline=GREEN+(255,), width=lw)

    # Cordages horizontaux
    for raw_y in (162, 210, 258):
        y = int(scale(raw_y, s))
        x0, x1 = int(scale(56,s)), int(scale(384,s))
        d.line([(x0,y),(x1,y)], fill=GREEN+(110,), width=max(1,int(scale(7,s))))

    # Cordages verticaux
    for raw_x in (148, 220, 292):
        x = int(scale(raw_x, s))
        y0, y1 = int(scale(44,s)), int(scale(376,s))
        d.line([(x,y0),(x,y1)], fill=GREEN+(110,), width=max(1,int(scale(7,s))))

    # Manche
    mx, my = int(scale(366,s)), int(scale(348,s))
    mw, mh = int(scale(24,s)), int(scale(120,s))
    d.rounded_rectangle([mx,my,mx+mw,my+mh], radius=max(2,mw//2), fill=GREEN+(255,))

    # Plumes volant
    def pts(*coords):
        return [(int(scale(x,s)), int(scale(y,s)))
                for x,y in zip(coords[::2], coords[1::2])]

    d.polygon(pts(420,120, 392,296, 412,300, 448,126), fill=CYAN+(255,))
    d.polygon(pts(448,118, 444,300, 464,298, 478,122), fill=CYAN+(255,))
    d.polygon(pts(472,122, 496,296, 476,300, 460,126), fill=CYAN+(255,))

    # Liège
    ex, ey = int(scale(444,s)), int(scale(310,s))
    rx1, ry1 = int(scale(28,s)), int(scale(15,s))
    rx2, ry2 = int(scale(19,s)), int(scale(10,s))
    d.ellipse([ex-rx1, ey-ry1, ex+rx1, ey+ry1], fill=CYAN+(255,))
    d.ellipse([ex-rx2, ey-ry2, ex+rx2, ey+ry2], fill=BG+(255,))

    # Texte BAD
    fs = max(8, int(scale(60, s)))
    fnt = font(FONT_BOLD, fs)
    bb  = d.textbbox((0,0), 'BAD', font=fnt)
    tw  = bb[2]-bb[0]
    tx  = (s - tw) // 2 - bb[0]
    ty  = int(scale(390, s)) - bb[1]
    d.text((tx, ty), 'BAD', font=fnt, fill=WHITE+(255,))

    # Texte COACH
    fs2 = max(6, int(scale(50, s)))
    fnt2 = font(FONT_BOLD, fs2)
    bb2  = d.textbbox((0,0), 'COACH', font=fnt2)
    tw2  = bb2[2]-bb2[0]
    tx2  = (s - tw2) // 2 - bb2[0]
    ty2  = int(scale(450, s)) - bb2[1]
    d.text((tx2, ty2), 'COACH', font=fnt2, fill=GREEN+(255,))

    # Composite sur fond opaque pour exports
    out = Image.new('RGB', (s, s), BG)
    out.paste(img, mask=img.split()[3])
    return out

# PNG 192 & 512
for sz in (192, 512):
    draw_icon(sz).save(os.path.join(OUT, f'icon-{sz}.png'))
    print(f'icon-{sz}.png saved')

# Maskable 512
draw_icon(512, maskable=True).save(os.path.join(OUT, 'icon-maskable-512.png'))
print('icon-maskable-512.png saved')

# Apple-touch-icon 180×180
draw_icon(180).save(os.path.join(OUT, 'apple-touch-icon.png'))
print('apple-touch-icon.png (180x180) saved')
