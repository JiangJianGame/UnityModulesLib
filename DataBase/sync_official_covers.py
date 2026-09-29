# -*- coding: utf-8 -*-
"""
Official Cover Synchronization Pipeline
Fetches authentic Unity Asset Store / official hero images for all 46 plugins,
standardizes to 16:9 (800x450), overlays clean official Unity version pill,
and updates PocketBase records.
"""

import os
import re
import gzip
import shutil
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont

SERVER_URL = 'http://127.0.0.1:5050'
SUPERUSER_EMAIL = 'admin@modules.local'
SUPERUSER_PASS = 'Admin12345678'
COVERS_DIR = r"D:\UnityItems\UnityModulesLib\DataBase\official_covers"
os.makedirs(COVERS_DIR, exist_ok=True)

# 46 Plugins official asset store pages or direct official CDN links
OFFICIAL_SOURCES = {
    'AVPro Video': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/94a94839-5eb7-4da9-b101-559e38fbd5bd.png'
    },
    'AVPro Video 增强集成包': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/94a94839-5eb7-4da9-b101-559e38fbd5bd.png'
    },
    'Best HTTP v3': {
        'url': 'https://assetstore.unity.com/packages/tools/network/best-http-3-264667'
    },
    'Build Report Tool': {
        'url': 'https://assetstore.unity.com/packages/tools/utilities/build-report-tool-8164'
    },
    'Calm Water': {
        'url': 'https://assetstore.unity.com/packages/vfx/shaders/calm-water-19288'
    },
    'ChineseInput WebGL': {
        'url': 'https://assetstore.unity.com/packages/tools/gui/chineseinput-webgl-131109'
    },
    'Crest Ocean System URP': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/c4d2bf2c-12cc-4c8e-a1f9-fac42bea35e3.jpg'
    },
    'DOTween': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/2e9fc555-b4d2-4f7b-9b82-5eaf30a853e3.png'
    },
    'Destructible 2D': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/eb62d0cc-b22d-4a7d-933b-dbcece3bd9b8.jpg'
    },
    'Dialogue System for Unity v2.2.39': {
        'url': 'https://assetstore.unity.com/packages/tools/behavior-ai/dialogue-system-for-unity-11672'
    },
    'Dialogue System for Unity v2.2.48': {
        'url': 'https://assetstore.unity.com/packages/tools/behavior-ai/dialogue-system-for-unity-11672'
    },
    'Easy Save 3': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/d8fb8676-e6cb-492a-863b-b08383ee9bd3.png'
    },
    'Enviro Sky and Weather': {
        'url': 'https://assetstore.unity.com/packages/tools/particles-effects/enviro-sky-and-weather-33963'
    },
    'Enviro 3': {
        'url': 'https://assetstore.unity.com/packages/tools/particles-effects/enviro-3-sky-and-weather-236601'
    },
    'Final IK': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/aea4b049-1964-46a9-a30c-07ed1131758d.png'
    },
    'Find Reference 2': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/92fc8551-4a95-4058-bb2c-cebf3d32acfd.jpg'
    },
    'Graphy': {
        'url': 'https://assetstore.unity.com/packages/tools/gui/graphy-ultimate-fps-counter-115480'
    },
    'Gravity Engine': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/377342f0-a154-407a-913a-48e0c9777e08.jpg'
    },
    'Heavy Sword Animation': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/87748799-25da-4161-83c0-f4298c45b00d.jpg'
    },
    'Highlight Plus URP': {
        'url': 'https://assetstore.unity.com/packages/vfx/shaders/highlight-plus-2-all-in-one-outline-selection-effects-321005'
    },
    'Highlighting System': {
        'url': 'https://assetstore.unity.com/packages/tools/particles-effects/highlighting-system-4183'
    },
    'In-Game Debug Console': {
        'url': 'https://assetstore.unity.com/packages/tools/gui/in-game-debug-console-68068'
    },
    'Liquid Volume Pro 2': {
        'url': 'https://assetstore.unity.com/packages/vfx/shaders/liquid-volume-pro-2-129967'
    },
    'Liquid Volume Pro': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/4b068b10-4fea-4c36-bdfc-61dc84e880e6.jpg'
    },
    'Magica Cloth 2': {
        'url': 'https://assetstore.unity.com/packages/tools/physics/magica-cloth-2-242307'
    },
    'MessagePack C#': {
        'direct': 'https://msgpack.org/images/logo.png',
        'is_logo': True
    },
    'MicroVerse - Roads': {
        'url': 'https://assetstore.unity.com/packages/tools/terrain/microverse-roads-238477'
    },
    'Newtonsoft Json.NET': {
        'url': 'https://assetstore.unity.com/packages/tools/input-management/json-net-for-unity-11347'
    },
    'ParrelSync': {
        'direct': 'https://cdn.jsdelivr.net/gh/VeriorPies/ParrelSync@master/Images/ScreenShot%201.png'
    },
    'Runtime Inspector & Hierarchy': {
        'url': 'https://assetstore.unity.com/packages/tools/gui/runtime-inspector-hierarchy-111349'
    },
    'Standalone File Browser': {
        'direct': 'https://cdn.jsdelivr.net/gh/gkngkc/UnityStandaloneFileBrowser@master/Images/sfb_win.jpg'
    },
    'Straight Sword Animation Set': {
        'url': 'https://assetstore.unity.com/packages/3d/animations/straight-sword-animation-set-125032'
    },
    'Tenkoku Dynamic Sky': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/17239fed-00f1-418e-9d8e-433070333732.jpg'
    },
    'TEXDraw': {
        'url': 'https://assetstore.unity.com/packages/tools/gui/texdraw-51426'
    },
    'TriLib 2 - Model Loader': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/6e354f4f-dfdb-4f54-8853-f6077fd5304d.jpg'
    },
    'Ultimate Character Controller': {
        'url': 'https://assetstore.unity.com/packages/tools/game-toolkits/ultimate-character-controller-233710'
    },
    'UniStorm Weather v3': {
        'url': 'https://assetstore.unity.com/packages/tools/particles-effects/unistorm-volumetric-clouds-sky-modular-weather-and-cloud-shadows-2714'
    },
    'UniStorm Volumetric v5.4.1': {
        'url': 'https://assetstore.unity.com/packages/tools/particles-effects/unistorm-volumetric-clouds-sky-modular-weather-and-cloud-shadows-2714'
    },
    'UniTask': {
        'direct': 'https://cysharp.github.io/UniTask/img/Icon.png',
        'is_logo': True
    },
    'Unity Logs Viewer': {
        'url': 'https://assetstore.unity.com/packages/tools/utilities/unity-logs-viewer-reporter-12064'
    },
    'VR Panorama 360 PRO': {
        'url': 'https://assetstore.unity.com/packages/tools/animation/vr-panorama-360-pro-renderer-v5-155097'
    },
    'Volumetric Light Beam': {
        'url': 'https://assetstore.unity.com/packages/vfx/shaders/volumetric-light-beam-99888'
    },
    'Vuplex 3D WebView': {
        'direct': 'https://assetstorev1-prd-cdn.unity3d.com/key-image/434c2b86-1906-49c9-95a1-6f495ad5267f.png'
    },
    'Weather Maker': {
        'url': 'https://assetstore.unity.com/packages/tools/particles-effects/weather-maker-volumetric-clouds-and-weather-system-for-unity-60955'
    },
    'XCharts 3 & Demo': {
        'local': r'D:\UnityItems\UnityModulesLib\xcharts3.0.png'
    },
    'XCharts 3 Core': {
        'local': r'D:\UnityItems\UnityModulesLib\xcharts3.0.png'
    }
}

def resolve_og_image(url):
    cmd = ['curl.exe', '-s', '-L', '--compressed', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', url]
    res = subprocess.run(cmd, capture_output=True, text=True, errors='ignore')
    if res.returncode == 0:
        m = re.search(r'property=[\"\']og:image[\"\']\s+content=[\"\']([^\"\']+)[\"\']', res.stdout)
        if m:
            return m.group(1)
        m2 = re.search(r'name=[\"\']twitter:image[\"\']\s+content=[\"\']([^\"\']+)[\"\']', res.stdout)
        if m2:
            return m2.group(1)
    return None

def process_and_style_cover(raw_img_path, unity_ver, is_logo, out_path):
    W, H = 800, 450
    try:
        # Check if gzip compressed
        with open(raw_img_path, 'rb') as f:
            buf = f.read()
        if buf[:2] == b'\x1f\x8b':
            try:
                buf = gzip.decompress(buf)
                with open(raw_img_path, 'wb') as f:
                    f.write(buf)
            except Exception as e:
                print(f"Gzip decompress error: {e}")

        with Image.open(raw_img_path) as src:
            if is_logo:
                # Place centered logo on studio dark gradient
                base = Image.new('RGB', (W, H), (14, 18, 28))
                draw_b = ImageDraw.Draw(base)
                for y in range(H):
                    t = y / float(H)
                    r = int(10 * (1 - t) + 20 * t)
                    g = int(14 * (1 - t) + 28 * t)
                    b = int(24 * (1 - t) + 48 * t)
                    draw_b.line([(0, y), (W, y)], fill=(r, g, b))
                # Resize logo maintaining aspect ratio (max 260x260)
                src_rgba = src.convert('RGBA')
                src_rgba.thumbnail((280, 280), Image.Resampling.LANCZOS)
                lw, lh = src_rgba.size
                lx = (W - lw) // 2
                ly = (H - lh) // 2
                base.paste(src_rgba, (lx, ly), src_rgba)
                final_img = base
            else:
                # Convert to RGB and crop/fit to 16:9
                src_rgb = src.convert('RGB')
                w, h = src_rgb.size
                target_ratio = 16.0 / 9.0
                curr_ratio = w / float(h)
                if abs(curr_ratio - target_ratio) > 0.05:
                    if curr_ratio > target_ratio:
                        new_w = int(h * target_ratio)
                        offset = (w - new_w) // 2
                        src_rgb = src_rgb.crop((offset, 0, offset + new_w, h))
                    else:
                        new_h = int(w / target_ratio)
                        offset = (h - new_h) // 2
                        src_rgb = src_rgb.crop((0, offset, w, offset + new_h))
                final_img = src_rgb.resize((W, H), Image.Resampling.LANCZOS)

        # Overlay crisp, elegant official Unity Version Capsule at Top-Right
        draw = ImageDraw.Draw(final_img)
        font_pill = ImageFont.truetype(r'C:\Windows\Fonts\bahnschrift.ttf', 15)
        
        unity_text = unity_ver.upper()
        tw = len(unity_text) * 9 + 48
        x1 = W - 24 - tw
        y1 = 20
        x2 = W - 24
        y2 = 52
        
        # Dark glass capsule background with crisp emerald outline
        draw.rounded_rectangle([x1, y1, x2, y2], radius=16, fill=(10, 18, 14), outline=(16, 185, 129), width=2)
        # Unity Cube Logo
        cx, cy = x1 + 20, (y1 + y2) // 2
        # Draw 3D cube
        draw.polygon([(cx, cy - 8), (cx + 7, cy - 4), (cx, cy), (cx - 7, cy - 4)], fill=(220, 240, 255), outline=(16, 185, 129))
        draw.polygon([(cx - 7, cy - 4), (cx, cy), (cx, cy + 8), (cx - 7, cy + 4)], fill=(160, 190, 210), outline=(16, 185, 129))
        draw.polygon([(cx + 7, cy - 4), (cx, cy), (cx, cy + 8), (cx + 7, cy + 4)], fill=(190, 220, 235), outline=(16, 185, 129))
        # Text
        draw.text((x1 + 34, y1 + 6), unity_text, font=font_pill, fill=(52, 211, 153))

        # Thin outer frame
        draw.rectangle([0, 0, W - 1, H - 1], outline=(35, 45, 65), width=1)
        final_img.save(out_path, quality=95)
        return True
    except Exception as e:
        print(f"Error styling cover {raw_img_path}: {e}")
        return False

def main():
    print("1. Authenticating with PocketBase...")
    auth = requests.post(f'{SERVER_URL}/api/collections/_superusers/auth-with-password',
                         json={'identity': SUPERUSER_EMAIL, 'password': SUPERUSER_PASS}).json()
    token = auth['token']
    headers = {'Authorization': token}

    print("2. Fetching records from models collection...")
    records = requests.get(f'{SERVER_URL}/api/collections/models/records?perPage=100', headers=headers).json().get('items', [])
    print(f"Found {len(records)} records.")

    success_count = 0
    for idx, rec in enumerate(records, 1):
        mid = rec['id']
        raw_title = rec['title']
        clean_title = raw_title.split('(')[0].strip()

        # Determine unity version
        unity_ver = 'Unity 2018.4+'
        if '(' in raw_title and ')' in raw_title:
            inside = raw_title.split('(')[-1].split(')')[0].strip()
            if 'unity' in inside.lower():
                unity_ver = inside

        src_info = OFFICIAL_SOURCES.get(clean_title)
        if not src_info:
            # Try fuzzy match
            for k, v in OFFICIAL_SOURCES.items():
                if k.lower() in clean_title.lower() or clean_title.lower() in k.lower():
                    src_info = v
                    break

        img_url = None
        local_path = None
        is_logo = False
        if src_info:
            local_path = src_info.get('local')
            img_url = src_info.get('direct')
            is_logo = src_info.get('is_logo', False)
            if not img_url and not local_path and 'url' in src_info:
                img_url = resolve_og_image(src_info['url'])

        raw_img_path = os.path.join(COVERS_DIR, f"raw_{mid}.png")
        final_img_path = os.path.join(COVERS_DIR, f"final_{mid}.png")

        if local_path and os.path.exists(local_path):
            print(f"[{idx:2d}/{len(records)}] Using local official source for '{clean_title}'...", end='', flush=True)
            shutil.copyfile(local_path, raw_img_path)
        elif img_url:
            print(f"[{idx:2d}/{len(records)}] Downloading official image for '{clean_title}'...", end='', flush=True)
            cmd = ['curl.exe', '-s', '-L', '--compressed', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', img_url, '-o', raw_img_path]
            subprocess.run(cmd)
        else:
            print(f"[{idx:2d}/{len(records)}] No official image found for '{clean_title}'")
            continue

        if os.path.exists(raw_img_path) and os.path.getsize(raw_img_path) > 100:
            styled = process_and_style_cover(raw_img_path, unity_ver, is_logo, final_img_path)
            if styled:
                # Upload to PocketBase
                old_previews = rec.get('preview_images', [])
                data = {'preview_images-': old_previews} if old_previews else {}
                with open(final_img_path, 'rb') as f_img:
                    files = {'preview_images': (f'official_{mid}.png', f_img, 'image/png')}
                    patch_res = requests.patch(f'{SERVER_URL}/api/collections/models/records/{mid}',
                                               headers=headers, data=data, files=files)
                    if patch_res.status_code == 200:
                        print(" OK! (Official Uploaded)")
                        success_count += 1
                    else:
                        print(f" PATCH Fail ({patch_res.status_code})")
            else:
                print(" Style Fail")
        else:
            print(" Download Empty")

    print(f"\nDone! Successfully updated {success_count}/{len(records)} official covers.")

if __name__ == '__main__':
    main()
