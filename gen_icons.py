"""Generate BadCoach PWA icons as PNG files — logo style (BAD / COACH)."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT   = os.path.join(os.path.dirname(__file__), 'icons')
os.makedirs(OUT, exist_ok=True)

BG    = (10, 22, 40)        # #0a1628
WHITE = (255, 255, 255)
GREEN = (0, 230, 118)       # #00e676
MUTED = (255, 255, 255, 90) # rgba

FONT_BOLD = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
FONT_MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def center_text(d, img_size, y_center, text, font, fill):
    """Draw text horizontally centered at y_center."""
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x  = (img_size - tw) / 2 - bbox[0]
    y  = y_center - th / 2  - bbox[1]
    d.text((x, y), text, font=font, fill=fill)
    return tw, th

def draw_icon(size, maskable=False, opaque=False):
    mode = 'RGB' if opaque else 'RGBA'
    bg   = BG    if opaque else (0, 0, 0, 0)
    img  = Image.new(mode, (size, size), bg)
    d    = ImageDraw.Draw(img)

    pad = int(size * 0.10) if maskable else 0
    r   = int(size * 0.175)

    # Background
    if not opaque:
        d.rounded_rectangle([pad, pad, size - pad, size - pad], radius=r, fill=BG)

    # --- Logo text ---
    # "BAD" : white, large
    # "COACH" : green, same size
    # Stacked, vertically centered with a thin separator line

    fs   = int(size * 0.255)   # font size ≈ 25 % of icon size
    font = load_font(FONT_BOLD, fs)

    # Measure both words
    bb_bad   = d.textbbox((0, 0), 'BAD',   font=font)
    bb_coach = d.textbbox((0, 0), 'COACH', font=font)
    h_bad    = bb_bad[3]   - bb_bad[1]
    h_coach  = bb_coach[3] - bb_coach[1]
    gap      = int(size * 0.04)   # gap between words
    sep_h    = max(2, int(size * 0.005))

    # Total block height
    total_h = h_bad + gap + sep_h + gap + h_coach
    block_y = (size - total_h) / 2

    # "BAD"
    center_text(d, size, block_y + h_bad / 2, 'BAD', font, WHITE)

    # Separator line
    sep_y = int(block_y + h_bad + gap)
    margin = int(size * 0.22)
    d.rectangle([margin, sep_y, size - margin, sep_y + sep_h],
                fill=(0, 230, 118, 100 if not opaque else 80))

    # "COACH"
    center_text(d, size,
                block_y + h_bad + gap + sep_h + gap + h_coach / 2,
                'COACH', font, GREEN)

    # "LIVE" — small mono text below
    fs_live  = int(size * 0.065)
    font_live = load_font(FONT_MONO, fs_live)
    live_fill = (255, 255, 255, 70) if not opaque else (120, 140, 160)
    live_y    = block_y + total_h + int(size * 0.07)
    center_text(d, size, live_y, 'LIVE', font_live, live_fill)

    return img


for sz in (192, 512):
    draw_icon(sz).save(os.path.join(OUT, f'icon-{sz}.png'))
    print(f'icon-{sz}.png saved')

draw_icon(512, maskable=True).save(os.path.join(OUT, 'icon-maskable-512.png'))
print('icon-maskable-512.png saved')

# iOS apple-touch-icon : 180×180, opaque (pas d'alpha), full bleed
draw_icon(180, opaque=True).save(os.path.join(OUT, 'apple-touch-icon.png'))
print('apple-touch-icon.png (180x180 opaque) saved')
