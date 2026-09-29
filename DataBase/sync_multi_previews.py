# -*- coding: utf-8 -*-
"""
Multi-Preview Image Synchronization Pipeline (Enhanced)
Fetches authentic official feature screenshots from Unity Asset Store and official repos,
combines them with the official hero cover (with Unity compatibility badge),
and updates PocketBase models so every plugin has a rich multi-image gallery.
"""

import os
import re
import gzip
import shutil
import subprocess
import tarfile
import requests
from PIL import Image

SERVER_URL = 'http://127.0.0.1:5050'
SUPERUSER_EMAIL = 'admin@modules.local'
SUPERUSER_PASS = 'Admin12345678'
BASE_COVERS_DIR = r"D:\UnityItems\UnityModulesLib\DataBase\official_covers"
GALLERY_DIR = r"D:\UnityItems\UnityModulesLib\DataBase\gallery_images"
os.makedirs(GALLERY_DIR, exist_ok=True)

# Complete map of 46 plugins to Asset Store URLs or mirror sources
PLUGIN_ASSET_STORE_URLS = {
    'AVPro Video': 'https://assetstore.unity.com/packages/tools/video/avpro-video-v3-ultra-edition-278896',
    'AVPro Video 增强集成包': 'https://assetstore.unity.com/packages/tools/video/avpro-video-v3-ultra-edition-278896',
    'Best HTTP v3': 'https://assetstore.unity.com/packages/tools/network/best-http-3-264667',
    'Build Report Tool': 'https://assetstore.unity.com/packages/tools/utilities/build-report-tool-8164',
    'Calm Water': 'https://assetstore.unity.com/packages/vfx/shaders/calm-water-19288',
    'ChineseInput WebGL': 'https://assetstore.unity.com/packages/tools/gui/chineseinput-webgl-131109',
    'Crest Ocean System URP': 'https://assetstore.unity.com/packages/tools/particles-effects/crest-ocean-system-urp-141674',
    'DOTween': 'https://assetstore.unity.com/packages/tools/visual-scripting/dotween-pro-32416',
    'Destructible 2D': 'https://assetstore.unity.com/packages/tools/sprite-management/destructible-2d-18125',
    'Dialogue System for Unity v2.2.39': 'https://assetstore.unity.com/packages/tools/behavior-ai/dialogue-system-for-unity-11672',
    'Dialogue System for Unity v2.2.48': 'https://assetstore.unity.com/packages/tools/behavior-ai/dialogue-system-for-unity-11672',
    'Easy Save 3': 'https://assetstore.unity.com/packages/tools/utilities/easy-save-the-complete-save-game-data-serializer-system-768',
    'Enviro Sky and Weather': 'https://assetstore.unity.com/packages/tools/particles-effects/enviro-3-sky-and-weather-236601',
    'Enviro 3': 'https://assetstore.unity.com/packages/tools/particles-effects/enviro-3-sky-and-weather-236601',
    'Final IK': 'https://assetstore.unity.com/packages/tools/animation/final-ik-14290',
    'Find Reference 2': 'https://assetstore.unity.com/packages/tools/utilities/find-reference-2-59092',
    'Graphy': 'https://assetstore.unity.com/packages/tools/gui/graphy-ultimate-fps-counter-stats-monitor-debugger-105778',
    'Gravity Engine': 'https://assetstore.unity.com/packages/tools/physics/gravity-engine-2-281698',
    'Heavy Sword Animation': 'https://assetstore.unity.com/packages/3d/animations/heavy-sword-animset-164746',
    'Highlight Plus URP': 'https://assetstore.unity.com/packages/vfx/shaders/highlight-plus-2-all-in-one-outline-selection-effects-321005',
    'Highlighting System': 'https://assetstore.unity.com/packages/tools/particles-effects/highlighting-system-41508',
    'In-Game Debug Console': 'https://assetstore.unity.com/packages/tools/gui/in-game-debug-console-68068',
    'Liquid Volume Pro 2': 'https://assetstore.unity.com/packages/vfx/shaders/liquid-volume-pro-2-129967',
    'Liquid Volume Pro': 'https://assetstore.unity.com/packages/vfx/shaders/liquid-volume-pro-2-129967',
    'Magica Cloth 2': 'https://assetstore.unity.com/packages/tools/physics/magica-cloth-2-242307',
    'MicroVerse - Roads': 'https://assetstore.unity.com/packages/tools/terrain/microverse-roads-238477',
    'Newtonsoft Json.NET': 'https://assetstore.unity.com/packages/tools/input-management/json-net-for-unity-11347',
    'Runtime Inspector & Hierarchy': 'https://assetstore.unity.com/packages/tools/gui/runtime-inspector-hierarchy-111349',
    'Straight Sword Animation Set': 'https://assetstore.unity.com/packages/3d/animations/straight-sword-animation-set-220752',
    'Tenkoku Dynamic Sky': 'https://assetstore.unity.com/packages/tools/particles-effects/tenkoku-dynamic-sky-34435',
    'TEXDraw': 'https://assetstore.unity.com/packages/tools/gui/texdraw-51426',
    'TriLib 2 - Model Loader': 'https://assetstore.unity.com/packages/tools/modeling/trilib-2-model-loader-package-157548',
    'Ultimate Character Controller': 'https://assetstore.unity.com/packages/tools/game-toolkits/ultimate-character-controller-233710',
    'UniStorm Weather v3': 'https://assetstore.unity.com/packages/tools/particles-effects/unistorm-volumetric-clouds-sky-modular-weather-and-cloud-shadows-2714',
    'UniStorm Volumetric v5.4.1': 'https://assetstore.unity.com/packages/tools/particles-effects/unistorm-volumetric-clouds-sky-modular-weather-and-cloud-shadows-2714',
    'Unity Logs Viewer': 'https://assetstore.unity.com/packages/tools/utilities/unity-logs-viewer-reporter-12064',
    'VR Panorama 360 PRO': 'https://assetstore.unity.com/packages/tools/animation/vr-panorama-360-pro-renderer-v5-155097',
    'Volumetric Light Beam': 'https://assetstore.unity.com/packages/vfx/shaders/volumetric-light-beam-99888',
    'Vuplex 3D WebView': 'https://assetstore.unity.com/packages/tools/gui/3d-webview-for-windows-and-macos-web-browser-154144',
    'Weather Maker': 'https://assetstore.unity.com/packages/tools/particles-effects/weather-maker-volumetric-clouds-and-weather-system-for-unity-60955'
}

# 6 Open Source / GitHub packages custom screenshot suppliers
OPEN_SOURCE_SCREENSHOTS = {
    'ParrelSync': [
        'https://cdn.jsdelivr.net/gh/VeriorPies/ParrelSync@master/Images/ScreenShot%202.png',
        'https://cdn.jsdelivr.net/gh/VeriorPies/ParrelSync@master/Images/AfterImported.png',
        'https://cdn.jsdelivr.net/gh/VeriorPies/ParrelSync@master/Images/UPM_1.png'
    ],
    'Standalone File Browser': [
        'https://cdn.jsdelivr.net/gh/gkngkc/UnityStandaloneFileBrowser@master/Images/sfb_mac.jpg',
        'https://cdn.jsdelivr.net/gh/gkngkc/UnityStandaloneFileBrowser@master/Images/sfb_linux.jpg',
        'https://cdn.jsdelivr.net/gh/gkngkc/UnityStandaloneFileBrowser@master/Images/win_import_1.jpg'
    ],
    'MessagePack C#': [
        'https://user-images.githubusercontent.com/46207/29754771-216b40e2-8bc7-11e7-8310-1c3602e80a08.png',
        'https://user-images.githubusercontent.com/46207/29754804-b5ba0f44-8bc7-11e7-9f6b-0c8f3c041237.png',
        'https://cloud.githubusercontent.com/assets/46207/23835765/55fe494e-07b0-11e7-98be-5e7a9411da40.png'
    ],
    'UniTask': [
        'https://user-images.githubusercontent.com/46207/83735571-83caea80-a68b-11ea-8d22-5e22864f0d24.png',
        'https://user-images.githubusercontent.com/46207/83527073-4434bf00-a522-11ea-86e9-3b3975b26266.png',
        'https://user-images.githubusercontent.com/46207/83702872-e0f17c80-a648-11ea-8183-7469dcd4f810.png'
    ]
}

def extract_screenshots_from_page(url, max_count=3):
    cmd = ['curl.exe', '-s', '-L', '--compressed', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', url]
    res = subprocess.run(cmd, capture_output=True, text=True, errors='ignore')
    if res.returncode != 0 or not res.stdout:
        return []
    
    # 1. Search in background-image and img tags
    bg_urls = re.findall(r'url\(&quot;(//assetstorev1-prd-cdn\.unity3d\.com/package-screenshot/[^&]+)&quot;\)', res.stdout)
    img_urls = re.findall(r'src="(//assetstorev1-prd-cdn\.unity3d\.com/package-screenshot/[^"]+)"', res.stdout)
    all_raw = list(dict.fromkeys(bg_urls + img_urls))
    
    hd_urls = []
    for u in all_raw:
        full = "https:" + u
        # If thumb.jpg, scaled.jpg is high-res version
        if '_thumb.jpg' in full:
            full = full.replace('_thumb.jpg', '_scaled.jpg')
        # If thumb.png, use thumb.png directly
        if full not in hd_urls:
            hd_urls.append(full)
            
    return hd_urls[:max_count]

def download_and_normalize_image(url, out_path):
    cmd = ['curl.exe', '-s', '-L', '--compressed', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', url, '-o', out_path]
    subprocess.run(cmd)
    if not os.path.exists(out_path) or os.path.getsize(out_path) < 100:
        return False
    
    # Gzip check
    with open(out_path, 'rb') as f:
        buf = f.read()
    if buf[:2] == b'\x1f\x8b':
        try:
            buf = gzip.decompress(buf)
            with open(out_path, 'wb') as f:
                f.write(buf)
        except:
            pass

    try:
        with Image.open(out_path) as im:
            # Normalize to RGB, max 1280x720, save as JPEG
            im_rgb = im.convert('RGB')
            w, h = im_rgb.size
            if w > 1280 or h > 720:
                im_rgb.thumbnail((1280, 720), Image.Resampling.LANCZOS)
            im_rgb.save(out_path, format='JPEG', quality=90)
        return True
    except Exception as e:
        print(f"Normalize error ({url}): {e}")
        return False

def extract_xcharts_screenshots():
    pkg_path = r'D:\Unity资源库\插件\XCharts-3.1.0.unitypackage'
    extracted = []
    target_names = ['linechart.png', 'linechart1.png', 'linechart2.png']
    if os.path.exists(pkg_path):
        with tarfile.open(pkg_path, 'r:gz') as tar:
            for m in tar.getmembers():
                if m.name.endswith('pathname'):
                    path = tar.extractfile(m).read().decode('utf-8', errors='ignore').strip()
                    for tname in target_names:
                        if path.endswith(tname):
                            guid = m.name.split('/')[1]
                            asset_m = tar.getmember(f'./{guid}/asset')
                            data = tar.extractfile(asset_m).read()
                            out_f = os.path.join(GALLERY_DIR, f"xcharts_{tname}")
                            with open(out_f, 'wb') as f:
                                f.write(data)
                            extracted.append(out_f)
    return extracted

def main():
    print("1. Authenticating with PocketBase...", flush=True)
    auth = requests.post(f'{SERVER_URL}/api/collections/_superusers/auth-with-password',
                         json={'identity': SUPERUSER_EMAIL, 'password': SUPERUSER_PASS}).json()
    headers = {'Authorization': auth['token']}

    print("2. Fetching records from models collection...", flush=True)
    records = requests.get(f'{SERVER_URL}/api/collections/models/records?perPage=100', headers=headers).json().get('items', [])
    print(f"Found {len(records)} records.\n", flush=True)

    xcharts_imgs = extract_xcharts_screenshots()

    success_count = 0
    for idx, rec in enumerate(records, 1):
        mid = rec['id']
        raw_title = rec['title']
        clean_title = raw_title.split('(')[0].strip()

        # Cover path
        cover_path = os.path.join(BASE_COVERS_DIR, f"final_{mid}.png")
        if not os.path.exists(cover_path):
            print(f"[{idx:2d}/{len(records)}] Cover not found for {clean_title}, skipping.", flush=True)
            continue

        # If already has >= 3 preview images, we can skip or keep
        current_previews = rec.get('preview_images', [])
        if len(current_previews) >= 3:
            print(f"[{idx:2d}/{len(records)}] {clean_title}: Already has {len(current_previews)} images, skipping.", flush=True)
            success_count += 1
            continue

        screenshot_files = []

        # Find screenshots
        if 'XCharts' in clean_title:
            screenshot_files = xcharts_imgs[:3]
        elif clean_title in OPEN_SOURCE_SCREENSHOTS:
            for s_idx, s_url in enumerate(OPEN_SOURCE_SCREENSHOTS[clean_title]):
                s_path = os.path.join(GALLERY_DIR, f"{mid}_ss_{s_idx}.jpg")
                if download_and_normalize_image(s_url, s_path):
                    screenshot_files.append(s_path)
        else:
            as_url = PLUGIN_ASSET_STORE_URLS.get(clean_title)
            if not as_url:
                for k, v in PLUGIN_ASSET_STORE_URLS.items():
                    if k.lower() in clean_title.lower() or clean_title.lower() in k.lower():
                        as_url = v
                        break
            if as_url:
                ss_urls = extract_screenshots_from_page(as_url, max_count=3)
                for s_idx, s_url in enumerate(ss_urls):
                    s_path = os.path.join(GALLERY_DIR, f"{mid}_ss_{s_idx}.jpg")
                    if download_and_normalize_image(s_url, s_path):
                        screenshot_files.append(s_path)

        if not screenshot_files:
            print(f"[{idx:2d}/{len(records)}] {clean_title}: No extra screenshots found.", flush=True)
            continue

        # Build multipart files payload
        files_payload = []
        files_payload.append(('preview_images', (f'official_{mid}.png', open(cover_path, 'rb'), 'image/png')))
        for s_idx, s_path in enumerate(screenshot_files):
            files_payload.append(('preview_images', (f'ss_{mid}_{s_idx}.jpg', open(s_path, 'rb'), 'image/jpeg')))

        old_previews = rec.get('preview_images', [])
        data_payload = {'preview_images-': old_previews} if old_previews else {}

        patch_res = requests.patch(f'{SERVER_URL}/api/collections/models/records/{mid}',
                                   headers=headers, data=data_payload, files=files_payload)
        
        # Close open file handles
        for _, file_tuple in files_payload:
            file_tuple[1].close()

        if patch_res.status_code == 200:
            total_imgs = len(files_payload)
            print(f"[{idx:2d}/{len(records)}] {clean_title}: OK! (Updated to {total_imgs} images)", flush=True)
            success_count += 1
        else:
            print(f"[{idx:2d}/{len(records)}] {clean_title}: Patch Error ({patch_res.status_code})", flush=True)

    print(f"\nAll done! Successfully verified multi-previews for {success_count}/{len(records)} packages.", flush=True)

if __name__ == '__main__':
    main()
