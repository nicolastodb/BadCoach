"""Generate BadCoach PWA icons as PNG files."""
import math, os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), 'icons')
os.makedirs(OUT, exist_ok=True)

BG   = (10, 22, 40)        # #0a1628
GREEN= (0, 230, 118)       # #00e676
CYAN = (0, 229, 255)       # #00e5ff

def draw_icon(size, maskable=False):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)

    pad = size * 0.1 if maskable else 0
    r   = int(size * 0.18)

    # Background rounded rect
    d.rounded_rectangle([pad, pad, size-pad, size-pad], radius=r, fill=BG)

    cx, cy = size / 2, size * 0.58  # shuttlecock center

    # --- feathers ---
    stem_len = size * 0.27
    angles   = [-50, -25, 0, 25, 50]  # degrees from top
    alphas   = [120, 180, 255, 180, 120]
    for ang, alpha in zip(angles, alphas):
        rad = math.radians(ang - 90)
        ex  = cx + math.cos(rad) * stem_len * 1.0
        ey  = cy + math.sin(rad) * stem_len * 1.0
        # neck point
        nx  = cx + math.cos(rad) * stem_len * 0.55
        ny  = cy + math.sin(rad) * stem_len * 0.55
        w   = max(2, int(size * 0.011))
        col = GREEN + (alpha,)
        d.line([(cx, cy), (ex, ey)], fill=col, width=w)

    # arc across feather tips
    top_y  = cy - stem_len * 0.97
    arc_r  = stem_len * 0.58
    arc_box = [cx - arc_r, top_y - arc_r * 0.3,
               cx + arc_r, top_y + arc_r * 0.7]
    d.arc(arc_box, start=200, end=340, fill=GREEN+(160,), width=max(2, int(size*0.01)))

    # cork
    cr  = int(size * 0.042)
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=GREEN)
    ir  = int(cr * 0.6)
    d.ellipse([cx-ir, cy-ir, cx+ir, cy+ir], fill=BG)
    dr  = int(cr * 0.3)
    d.ellipse([cx-dr, cy-dr, cx+dr, cy+dr], fill=GREEN)

    # "BC" text
    fs = int(size * 0.18)
    try:
        from PIL import ImageFont
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', fs)
    except Exception:
        font = ImageFont.load_default()
    text = 'BC'
    bbox = d.textbbox((0,0), text, font=font)
    tw   = bbox[2] - bbox[0]
    th   = bbox[3] - bbox[1]
    tx   = (size - tw) / 2 - bbox[0]
    ty   = size * 0.8 - th / 2 - bbox[1]
    d.text((tx, ty), text, font=font, fill=CYAN)

    return img

for sz in (192, 512):
    draw_icon(sz).save(os.path.join(OUT, f'icon-{sz}.png'))
    print(f'icon-{sz}.png saved')

draw_icon(512, maskable=True).save(os.path.join(OUT, 'icon-maskable-512.png'))
print('icon-maskable-512.png saved')
