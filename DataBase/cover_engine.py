# -*- coding: utf-8 -*-
"""
Studio Cover Generator for Unity Modules & Plugins
Generates formal, classic, high-end commercial artwork covers (800x450, 16:9).
Uploads to PocketBase backend models collection.
"""

import os
import math
import requests
from PIL import Image, ImageDraw, ImageFont

SERVER_URL = 'http://127.0.0.1:5050'
SUPERUSER_EMAIL = 'admin@modules.local'
SUPERUSER_PASS = 'Admin12345678'
OUTPUT_DIR = r'D:\UnityItems\UnityModulesLib\DataBase\studio_covers'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Color Palettes by Category
PALETTES = {
    'tool': {
        'bg1': (7, 12, 22), 'bg2': (14, 24, 44),
        'accent': (56, 189, 248), 'accent_dark': (2, 132, 199),
        'glow': (14, 165, 233, 40), 'tag': 'SYSTEM TOOL'
    },
    'vfx': {
        'bg1': (15, 9, 27), 'bg2': (27, 15, 50),
        'accent': (192, 132, 252), 'accent_dark': (147, 51, 234),
        'glow': (168, 85, 247, 40), 'tag': 'SHADERS & VFX'
    },
    'env': {
        'bg1': (5, 18, 24), 'bg2': (11, 35, 45),
        'accent': (45, 212, 191), 'accent_dark': (13, 148, 136),
        'glow': (20, 184, 166, 40), 'tag': 'ENVIRONMENT'
    },
    'anim': {
        'bg1': (24, 13, 9), 'bg2': (44, 23, 15),
        'accent': (251, 146, 60), 'accent_dark': (234, 88, 12),
        'glow': (249, 115, 22, 40), 'tag': 'ANIMATION & RIG'
    },
    'core': {
        'bg1': (9, 13, 28), 'bg2': (18, 26, 56),
        'accent': (129, 140, 248), 'accent_dark': (79, 70, 229),
        'glow': (99, 102, 241, 40), 'tag': 'CORE UTILITY'
    },
    'physics': {
        'bg1': (22, 11, 18), 'bg2': (40, 20, 32),
        'accent': (244, 114, 182), 'accent_dark': (219, 39, 119),
        'glow': (236, 72, 153, 40), 'tag': 'PHYSICS & CLOTH'
    },
    'ui': {
        'bg1': (8, 18, 22), 'bg2': (15, 36, 44),
        'accent': (34, 211, 238), 'accent_dark': (8, 145, 178),
        'glow': (6, 182, 212, 40), 'tag': 'GUI & GRAPHICS'
    },
    'data': {
        'bg1': (7, 15, 24), 'bg2': (13, 30, 48),
        'accent': (96, 165, 250), 'accent_dark': (37, 99, 235),
        'glow': (59, 130, 246, 40), 'tag': 'DATA & NETWORK'
    }
}

def draw_unity_logo(draw, x, y, size, color):
    """Draw a clean geometric Unity-style cube icon"""
    h = size / 2.0
    # Top face
    draw.polygon([(x, y - h), (x + h * 0.866, y - h * 0.5), (x, y), (x - h * 0.866, y - h * 0.5)],
                 fill=(220, 235, 245), outline=color, width=1)
    # Left face
    draw.polygon([(x - h * 0.866, y - h * 0.5), (x, y), (x, y + h), (x - h * 0.866, y + h * 0.5)],
                 fill=(160, 180, 200), outline=color, width=1)
    # Right face
    draw.polygon([(x + h * 0.866, y - h * 0.5), (x, y), (x, y + h), (x + h * 0.866, y + h * 0.5)],
                 fill=(190, 210, 225), outline=color, width=1)

def draw_glyph(draw, glyph_type, ix, iy, ac):
    """Draw thematic high-tech vector glyph inside the hero emblem"""
    if glyph_type == 'video':
        # Double play triangle or play in lens
        draw.polygon([(ix - 18, iy - 26), (ix + 24, iy), (ix - 18, iy + 26)], fill=ac)
        draw.ellipse([ix - 32, iy - 32, ix + 32, iy + 32], outline=ac, width=2)
    elif glyph_type == 'network':
        nodes = [(ix - 22, iy - 16), (ix + 22, iy - 16), (ix, iy + 22)]
        for p1 in nodes:
            for p2 in nodes:
                draw.line([p1, p2], fill=ac, width=3)
        for p in nodes:
            draw.ellipse([p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8], fill=(255, 255, 255), outline=ac, width=2)
        draw.ellipse([ix - 5, iy - 2, ix + 5, iy + 8], fill=ac)
    elif glyph_type == 'shader':
        # Faceted gemstone
        draw.polygon([(ix, iy - 30), (ix + 26, iy - 6), (ix + 16, iy + 28), (ix - 16, iy + 28), (ix - 26, iy - 6)],
                     outline=ac, fill=(40, 30, 65), width=2)
        draw.line([(ix, iy - 30), (ix, iy + 28)], fill=ac, width=2)
        draw.line([(ix - 26, iy - 6), (ix + 26, iy - 6)], fill=ac, width=2)
        draw.polygon([(ix, iy - 30), (ix + 10, iy - 6), (ix, iy + 28)], fill=(65, 45, 95))
    elif glyph_type == 'water' or glyph_type == 'ocean':
        for offset in [-14, 0, 14]:
            pts = []
            for dx in range(-28, 30, 4):
                dy = int(math.sin(dx * 0.16) * 7)
                pts.append((ix + dx, iy + offset + dy))
            draw.line(pts, fill=ac, width=3)
    elif glyph_type == 'code' or glyph_type == 'inspector':
        # Curly brackets or code chevrons
        draw.line([(ix - 12, iy - 22), (ix - 24, iy), (ix - 12, iy + 22)], fill=ac, width=4)
        draw.line([(ix + 12, iy - 22), (ix + 24, iy), (ix + 12, iy + 22)], fill=ac, width=4)
        draw.line([(ix + 6, iy - 24), (ix - 6, iy + 24)], fill=(220, 235, 255), width=3)
    elif glyph_type == 'tween':
        # Smooth bezier curve with motion arrow
        draw.arc([ix - 26, iy - 26, ix + 26, iy + 26], start=45, end=270, fill=ac, width=4)
        draw.polygon([(ix + 22, iy - 10), (ix + 32, iy + 4), (ix + 16, iy + 8)], fill=ac)
        draw.ellipse([ix - 12, iy + 14, ix - 4, iy + 22], fill=(255, 255, 255))
    elif glyph_type == 'report' or glyph_type == 'chart':
        # Analytics bars
        bars = [(-22, 16), (-10, 32), (2, 22), (14, 42)]
        for bx, bh in bars:
            draw.rounded_rectangle([ix + bx, iy + 20 - bh, ix + bx + 8, iy + 20], radius=2, fill=ac)
        draw.line([(ix - 26, iy + 22), (ix + 26, iy + 22)], fill=(200, 220, 255), width=2)
    elif glyph_type == 'input':
        # Keyboard with cursor
        draw.rounded_rectangle([ix - 26, iy - 18, ix + 26, iy + 18], radius=4, outline=ac, fill=(20, 30, 48), width=2)
        draw.line([(ix - 16, iy), (ix - 16, iy + 10)], fill=ac, width=2)
        draw.line([(ix - 8, iy - 8), (ix + 12, iy - 8)], fill=(200, 220, 255), width=2)
        draw.line([(ix - 8, iy + 4), (ix + 8, iy + 4)], fill=ac, width=2)
    elif glyph_type == 'dialogue':
        # Overlapping chat bubbles
        draw.rounded_rectangle([ix - 26, iy - 24, ix + 10, iy + 2], radius=6, outline=ac, fill=(25, 35, 55), width=2)
        draw.polygon([(ix - 18, iy + 2), (ix - 24, iy + 10), (ix - 10, iy + 2)], fill=ac)
        draw.rounded_rectangle([ix - 6, iy - 8, ix + 26, iy + 18], radius=6, outline=(255, 255, 255), fill=(35, 45, 70), width=2)
        draw.polygon([(ix + 12, iy + 18), (ix + 20, iy + 26), (ix + 18, iy + 18)], fill=(255, 255, 255))
    elif glyph_type == 'save':
        # Storage database disc cylinder
        for dy in [-16, 0, 16]:
            draw.ellipse([ix - 22, iy + dy - 8, ix + 22, iy + dy + 8], outline=ac, fill=(20, 32, 50), width=2)
        draw.line([(ix - 22, iy - 16), (ix - 22, iy + 16)], fill=ac, width=2)
        draw.line([(ix + 22, iy - 16), (ix + 22, iy + 16)], fill=ac, width=2)
    elif glyph_type == 'sky' or glyph_type == 'weather':
        # Sun & Cloud
        draw.ellipse([ix - 6, iy - 24, ix + 20, iy + 2], fill=ac)
        draw.ellipse([ix - 26, iy - 6, ix + 4, iy + 20], fill=(220, 235, 255))
        draw.ellipse([ix - 10, iy - 14, ix + 18, iy + 20], fill=(220, 235, 255))
        draw.rounded_rectangle([ix - 22, iy + 6, ix + 14, iy + 20], radius=4, fill=(220, 235, 255))
    elif glyph_type == 'ik' or glyph_type == 'anim':
        # Kinematic joints / bones
        p1, p2, p3 = (ix - 18, iy + 18), (ix + 4, iy - 6), (ix + 20, iy + 16)
        draw.line([p1, p2], fill=ac, width=4)
        draw.line([p2, p3], fill=(220, 235, 255), width=4)
        for pt in [p1, p2, p3]:
            draw.ellipse([pt[0] - 6, pt[1] - 6, pt[0] + 6, pt[1] + 6], fill=(255, 255, 255), outline=ac, width=2)
    elif glyph_type == 'sword':
        # Crossed blades
        draw.line([(ix - 20, iy - 20), (ix + 20, iy + 20)], fill=ac, width=3)
        draw.line([(ix - 20, iy + 20), (ix + 20, iy - 20)], fill=(220, 235, 255), width=3)
        draw.line([(ix - 14, iy - 8), (ix - 8, iy - 14)], fill=ac, width=3)
        draw.line([(ix - 14, iy + 8), (ix - 8, iy + 14)], fill=(220, 235, 255), width=3)
    elif glyph_type == 'cloth':
        # Hanging cloth folds
        for dx in [-18, -6, 6, 18]:
            draw.arc([ix + dx - 10, iy - 20, ix + dx + 10, iy + 20], start=60, end=240, fill=ac, width=3)
        draw.line([(ix - 24, iy - 18), (ix + 24, iy - 18)], fill=(255, 255, 255), width=2)
    elif glyph_type == 'road':
        # Vanishing point highway
        draw.polygon([(ix - 26, iy + 22), (ix + 26, iy + 22), (ix + 6, iy - 20), (ix - 6, iy - 20)], fill=(24, 34, 52), outline=ac, width=2)
        draw.line([(ix, iy + 20), (ix, iy + 8)], fill=ac, width=3)
        draw.line([(ix, iy - 2), (ix, iy - 12)], fill=ac, width=2)
    elif glyph_type == 'async':
        # Lightning bolt
        draw.polygon([(ix + 4, iy - 28), (ix - 14, iy - 2), (ix + 2, iy - 2), (ix - 6, iy + 28), (ix + 16, iy + 2), (ix, iy + 2)], fill=ac)
    elif glyph_type == 'vr':
        # VR Goggles
        draw.rounded_rectangle([ix - 26, iy - 14, ix + 26, iy + 14], radius=8, outline=ac, fill=(20, 28, 44), width=3)
        draw.ellipse([ix - 18, iy - 6, ix - 6, iy + 6], fill=ac)
        draw.ellipse([ix + 6, iy - 6, ix + 18, iy + 6], fill=ac)
        draw.line([(ix - 26, iy), (ix - 32, iy)], fill=ac, width=2)
        draw.line([(ix + 26, iy), (ix + 32, iy)], fill=ac, width=2)
    elif glyph_type == 'webview':
        # Browser window with web globe
        draw.rounded_rectangle([ix - 24, iy - 18, ix + 24, iy + 18], radius=4, outline=ac, fill=(20, 28, 44), width=2)
        draw.line([(ix - 24, iy - 8), (ix + 24, iy - 8)], fill=ac, width=1)
        draw.ellipse([ix - 18, iy - 14, ix - 14, iy - 10], fill=ac)
        draw.ellipse([ix - 10, iy - 14, ix - 6, iy - 10], fill=(220, 235, 255))
    elif glyph_type == 'model':
        # 3D Wireframe Cube
        draw.polygon([(ix, iy - 24), (ix + 22, iy - 10), (ix, iy + 4), (ix - 22, iy - 10)], outline=ac, width=2)
        draw.polygon([(ix - 22, iy - 10), (ix, iy + 4), (ix, iy + 24), (ix - 22, iy + 10)], outline=ac, width=2)
        draw.polygon([(ix + 22, iy - 10), (ix, iy + 4), (ix, iy + 24), (ix + 22, iy + 10)], outline=ac, width=2)
    else:
        # Default Tech Diamond Sparkle
        draw.polygon([(ix, iy - 26), (ix + 8, iy - 8), (ix + 26, iy), (ix + 8, iy + 8),
                      (ix, iy + 26), (ix - 8, iy + 8), (ix - 26, iy), (ix - 8, iy - 8)], fill=ac)

def generate_studio_cover(clean_title, unity_ver, author, version, category_type, subtitle, glyph_type, out_path):
    W, H = 800, 450
    base_img = Image.new('RGB', (W, H), (10, 14, 24))
    pal = PALETTES.get(category_type, PALETTES['tool'])

    # 1. Gradient Background
    draw_base = ImageDraw.Draw(base_img)
    for y in range(H):
        t = y / float(H)
        r = int(pal['bg1'][0] * (1 - t) + pal['bg2'][0] * t)
        g = int(pal['bg1'][1] * (1 - t) + pal['bg2'][1] * t)
        b = int(pal['bg1'][2] * (1 - t) + pal['bg2'][2] * t)
        draw_base.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Ambient Studio Glow
    glow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    center_glow = (145, 235)
    for radius in range(240, 20, -12):
        alpha = int(pal['glow'][3] * (1.0 - radius / 240.0))
        c = (pal['glow'][0], pal['glow'][1], pal['glow'][2], alpha)
        glow_draw.ellipse([center_glow[0] - radius, center_glow[1] - radius,
                           center_glow[0] + radius, center_glow[1] + radius], fill=c)
    base_img = Image.alpha_composite(base_img.convert('RGBA'), glow_layer)

    # 3. Subtle Tech Grid Pattern
    tech_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tech_draw = ImageDraw.Draw(tech_layer)
    grid_color = (255, 255, 255, 10)
    for gx in range(40, W, 40):
        tech_draw.line([(gx, 0), (gx, H)], fill=grid_color, width=1)
    for gy in range(40, H, 40):
        tech_draw.line([(0, gy), (W, gy)], fill=grid_color, width=1)
    base_img = Image.alpha_composite(base_img, tech_layer)

    final_img = base_img.convert('RGB')
    draw = ImageDraw.Draw(final_img)

    # Fonts
    font_brand = ImageFont.truetype(r'C:\Windows\Fonts\bahnschrift.ttf', 13)
    font_tag = ImageFont.truetype(r'C:\Windows\Fonts\bahnschrift.ttf', 14)
    font_unity = ImageFont.truetype(r'C:\Windows\Fonts\bahnschrift.ttf', 15)
    font_subtitle = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 15)
    font_meta = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 13)

    # 4. Top Badges
    # Official Asset Pill
    draw.rounded_rectangle([40, 28, 175, 58], radius=15, fill=(18, 24, 38), outline=(45, 55, 75), width=1)
    draw.ellipse([54, 40, 62, 48], fill=pal['accent'])
    draw.text((72, 35), "OFFICIAL ASSET", font=font_brand, fill=(226, 232, 240))

    # Category Pill
    tag_w = len(pal['tag']) * 9 + 30
    draw.rounded_rectangle([190, 28, 190 + tag_w, 58], radius=15, fill=(18, 24, 38), outline=pal['accent_dark'], width=1)
    draw.text((205, 35), pal['tag'], font=font_tag, fill=pal['accent'])

    # Unity Version Capsule (Top Right)
    unity_display = unity_ver.upper()
    u_text_w = len(unity_display) * 9 + 48
    u_x = W - 40 - u_text_w
    draw.rounded_rectangle([u_x, 28, W - 40, 58], radius=15, fill=(14, 28, 22), outline=(16, 185, 129), width=1)
    # Draw geometric Unity cube next to text
    draw_unity_logo(draw, u_x + 22, 43, 14, (16, 185, 129))
    draw.text((u_x + 36, 35), unity_display, font=font_unity, fill=(52, 211, 153))

    # 5. Hero Emblem (Center Left)
    ix, iy = 145, 235
    s = 65
    # Outer double rounded square with gradient rim
    draw.rounded_rectangle([ix - s - 10, iy - s - 10, ix + s + 10, iy + s + 10], radius=24, fill=(18, 26, 42), outline=pal['accent'], width=2)
    draw.rounded_rectangle([ix - s, iy - s, ix + s, iy + s], radius=18, fill=(24, 34, 54))
    # Beveled highlight line at top of inner box
    draw.line([(ix - s + 10, iy - s + 2), (ix + s - 10, iy - s + 2)], fill=(255, 255, 255), width=1)

    # Draw thematic vector glyph
    draw_glyph(draw, glyph_type, ix, iy, pal['accent'])

    # 6. Typography
    tx = 250
    has_cn = any('\u4e00' <= ch <= '\u9fff' for ch in clean_title)

    # Choose adaptive font size based on length
    if len(clean_title) <= 16:
        font_size = 38
    elif len(clean_title) <= 24:
        font_size = 32
    else:
        font_size = 27

    if has_cn:
        title_font = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', font_size)
    else:
        title_font = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', font_size)

    # Title shadow & crisp text
    draw.text((tx + 2, 172), clean_title, font=title_font, fill=(0, 0, 0))
    draw.text((tx, 170), clean_title, font=title_font, fill=(255, 255, 255))

    # Subtitle
    draw.text((tx, 228), subtitle, font=font_subtitle, fill=(203, 213, 225))

    # Feature badges
    p1 = "PRODUCTION READY"
    p2 = f"VERSION {version}"
    px = tx
    for pill in [p1, p2]:
        pw = len(pill) * 8 + 24
        draw.rounded_rectangle([px, 268, px + pw, 296], radius=6, fill=(22, 30, 46), outline=(51, 65, 85), width=1)
        draw.text((px + 12, 274), pill, font=font_brand, fill=(148, 163, 184))
        px += pw + 12

    # 7. Bottom Bar & Commercial Seals
    draw.line([(40, 390), (W - 40, 390)], fill=(30, 41, 59), width=1)
    draw.line([(40, 390), (160, 390)], fill=pal['accent'], width=2)

    # Developer Tag
    draw.text((40, 408), f"DEVELOPER: {author.upper()}", font=font_meta, fill=(148, 163, 184))

    # Authenticity Seal
    status_text = "ENTERPRISE SOFTWARE SUITE  •  VERIFIED UNITY COMPATIBILITY"
    sw = len(status_text) * 7
    draw.text((W - 40 - sw, 408), status_text, font=font_meta, fill=(100, 116, 139))

    # Outer border
    draw.rectangle([0, 0, W - 1, H - 1], outline=(40, 50, 70), width=1)

    final_img.save(out_path, quality=95)
    return out_path
