# -*- coding: utf-8 -*-
import os
import json
import requests
from cover_engine import generate_studio_cover, OUTPUT_DIR, SERVER_URL, SUPERUSER_EMAIL, SUPERUSER_PASS

# Dictionary of specialized metadata for each plugin
PLUGIN_METADATA = {
    'AVPro Video': {
        'cat': 'tool', 'glyph': 'video', 'sub': 'High-Performance GPU Video Playback & Streaming Engine'
    },
    'Best HTTP v3': {
        'cat': 'data', 'glyph': 'network', 'sub': 'Next-Gen Multi-Protocol Networking & WebSocket Engine'
    },
    'Build Report Tool': {
        'cat': 'tool', 'glyph': 'report', 'sub': 'Precise Package Build Size & Dependency Analysis Tool'
    },
    'Calm Water': {
        'cat': 'env', 'glyph': 'water', 'sub': 'Lightweight Stylized Water & Dynamic Caustics Shader'
    },
    'ChineseInput WebGL': {
        'cat': 'ui', 'glyph': 'input', 'sub': 'Native IME Chinese Input Bridge for WebGL Applications'
    },
    'Crest Ocean System URP': {
        'cat': 'env', 'glyph': 'ocean', 'sub': 'Advanced Dynamic Ocean Simulation, Waves & Caustics'
    },
    'DOTween': {
        'cat': 'core', 'glyph': 'tween', 'sub': 'Industry Standard High-Performance Animation & Tween Engine'
    },
    'Destructible 2D': {
        'cat': 'physics', 'glyph': 'model', 'sub': 'Real-Time 2D Sprite Slicing, Fracture & Destruction'
    },
    'Dialogue System for Unity v2.2.39': {
        'cat': 'core', 'glyph': 'dialogue', 'sub': 'Complete Branching Dialogue, Quest & Narrative Framework'
    },
    'Dialogue System for Unity v2.2.48': {
        'cat': 'core', 'glyph': 'dialogue', 'sub': 'Complete Branching Dialogue, Quest & Narrative Framework'
    },
    'Easy Save 3': {
        'cat': 'data', 'glyph': 'save', 'sub': 'Fast, Encrypted Game Save & Serialization Architecture'
    },
    'Enviro Sky and Weather': {
        'cat': 'env', 'glyph': 'weather', 'sub': 'Complete Dynamic Sky, Clouds, Weather & Lighting Suite'
    },
    'Enviro 3': {
        'cat': 'env', 'glyph': 'weather', 'sub': 'Next-Gen Volumetric Clouds, Atmosphere & Weather System'
    },
    'Final IK': {
        'cat': 'anim', 'glyph': 'ik', 'sub': 'Industry Leading Full-Body Inverse Kinematics Solution'
    },
    'Find Reference 2': {
        'cat': 'tool', 'glyph': 'inspector', 'sub': 'Ultra-Fast Asset Dependency & Reference Finder'
    },
    'Graphy': {
        'cat': 'tool', 'glyph': 'chart', 'sub': 'Real-Time Performance, FPS, Memory & Audio Monitor'
    },
    'Gravity Engine': {
        'cat': 'physics', 'glyph': 'model', 'sub': 'N-Body Orbital Mechanics & Real-Time Gravitation Physics'
    },
    'Heavy Sword Animation': {
        'cat': 'anim', 'glyph': 'sword', 'sub': 'Professional Heavy Weapon Combat Animation Library'
    },
    'Highlight Plus URP': {
        'cat': 'vfx', 'glyph': 'shader', 'sub': 'All-in-One Mesh Outline, Glow, Overlay & Rim Effects'
    },
    'Highlighting System': {
        'cat': 'vfx', 'glyph': 'shader', 'sub': 'High-Visibility Edge Silhouette & Highlighting Effects'
    },
    'In-Game Debug Console': {
        'cat': 'tool', 'glyph': 'code', 'sub': 'Interactive Command Prompt & Mobile In-Game Console'
    },
    'Liquid Volume Pro 2': {
        'cat': 'vfx', 'glyph': 'water', 'sub': 'Volumetric Liquid Container Shader & Fluid Simulation'
    },
    'Liquid Volume Pro': {
        'cat': 'vfx', 'glyph': 'water', 'sub': 'Volumetric Container Liquid & Glass Physics Shader'
    },
    'Magica Cloth 2': {
        'cat': 'physics', 'glyph': 'cloth', 'sub': 'High-Speed Burst & Jobs Powered Cloth & Hair Physics'
    },
    'MessagePack C#': {
        'cat': 'data', 'glyph': 'save', 'sub': 'Extremely Fast Binary Serializer for C# & Unity'
    },
    'MicroVerse - Roads': {
        'cat': 'env', 'glyph': 'road', 'sub': 'Non-Destructive Procedural Road Spline Generator'
    },
    'Newtonsoft Json.NET': {
        'cat': 'data', 'glyph': 'save', 'sub': 'Standard High-Performance JSON Framework for Unity'
    },
    'ParrelSync': {
        'cat': 'tool', 'glyph': 'network', 'sub': 'Multiplayer Local Editor Clone & Synchronization Tool'
    },
    'Runtime Inspector & Hierarchy': {
        'cat': 'tool', 'glyph': 'inspector', 'sub': 'Full Runtime Object Hierarchy & Property Inspection'
    },
    'Standalone File Browser': {
        'cat': 'tool', 'glyph': 'inspector', 'sub': 'Native OS File Open & Save Dialog Wrappers'
    },
    'Straight Sword Animation Set': {
        'cat': 'anim', 'glyph': 'sword', 'sub': 'Authentic Combat Motion Library for Swordplay'
    },
    'Tenkoku Dynamic Sky': {
        'cat': 'env', 'glyph': 'weather', 'sub': 'Astronomically Accurate Sky, Solar & Lunar Simulator'
    },
    'TEXDraw': {
        'cat': 'ui', 'glyph': 'code', 'sub': 'Dynamic LaTeX Mathematical Expression Renderer for UI'
    },
    'TriLib 2 - Model Loader': {
        'cat': 'core', 'glyph': 'model', 'sub': 'Cross-Platform Runtime 3D Model Importer (FBX, OBJ, GLTF)'
    },
    'Ultimate Character Controller': {
        'cat': 'anim', 'glyph': 'anim', 'sub': 'AAA Grade First & Third Person Character Physics Framework'
    },
    'UniStorm Weather v3': {
        'cat': 'env', 'glyph': 'weather', 'sub': 'Customizable Dynamic Sky, Clouds, Lightning & Rain'
    },
    'UniStorm Volumetric v5.4.1': {
        'cat': 'env', 'glyph': 'weather', 'sub': 'Volumetric Cloud Shaders, Procedural Storms & Atmosphere'
    },
    'UniTask': {
        'cat': 'core', 'glyph': 'async', 'sub': 'Zero-Allocation Async/Await Integration for Unity'
    },
    'Unity Logs Viewer': {
        'cat': 'tool', 'glyph': 'code', 'sub': 'On-Device Mobile & Desktop Diagnostic Log Reporter'
    },
    'VR Panorama 360 PRO': {
        'cat': 'tool', 'glyph': 'vr', 'sub': 'Stereoscopic 360 Panorama & 8K VR Video Capture Engine'
    },
    'Volumetric Light Beam': {
        'cat': 'vfx', 'glyph': 'shader', 'sub': 'Physically-Based Volumetric Dust & Spotlight Beams'
    },
    'Vuplex 3D WebView': {
        'cat': 'ui', 'glyph': 'webview', 'sub': 'Interactive 3D Web Browser Inside Unity (Chromium Engine)'
    },
    'Weather Maker': {
        'cat': 'env', 'glyph': 'weather', 'sub': 'Complete 2D/3D Weather, Skybox, Precipitation & Fog'
    },
    'XCharts 3 & Demo': {
        'cat': 'ui', 'glyph': 'chart', 'sub': 'Enterprise Real-Time Data Visualization & Charting Suite'
    },
    'XCharts 3 Core': {
        'cat': 'ui', 'glyph': 'chart', 'sub': 'Lightweight Core Data Charting & Visualization Library'
    },
    'AVPro Video 增强集成包': {
        'cat': 'tool', 'glyph': 'video', 'sub': 'Professional Video Engine with Extended Decoders & Samples'
    }
}

def main():
    print("1. Authenticating Superuser...")
    auth = requests.post(f'{SERVER_URL}/api/collections/_superusers/auth-with-password',
                         json={'identity': SUPERUSER_EMAIL, 'password': SUPERUSER_PASS}).json()
    token = auth['token']
    headers = {'Authorization': token}

    print("2. Fetching all models from server...")
    records = requests.get(f'{SERVER_URL}/api/collections/models/records?perPage=100', headers=headers).json().get('items', [])
    print(f"Total records found: {len(records)}")

    success_count = 0
    for idx, rec in enumerate(records, 1):
        mid = rec['id']
        raw_title = rec['title']
        author = rec.get('author', 'Unity Community')
        version = rec.get('version', '1.0.0')

        # Extract unity version from title (e.g. "Unity 2018.4+")
        clean_title = raw_title.split('(')[0].strip()
        unity_ver = 'Unity 2018.4+'
        if '(' in raw_title and ')' in raw_title:
            inside = raw_title.split('(')[-1].split(')')[0].strip()
            if 'unity' in inside.lower():
                unity_ver = inside

        # Find matching metadata
        meta = PLUGIN_METADATA.get(clean_title, None)
        if not meta:
            # fallback fuzzy match
            for k, v in PLUGIN_METADATA.items():
                if k.lower() in clean_title.lower() or clean_title.lower() in k.lower():
                    meta = v
                    break
        if not meta:
            meta = {'cat': 'tool', 'glyph': 'default', 'sub': 'Professional Certified Unity Package Extension'}

        out_img = os.path.join(OUTPUT_DIR, f'cover_{mid}.png')
        generate_studio_cover(
            clean_title=clean_title,
            unity_ver=unity_ver,
            author=author,
            version=version,
            category_type=meta['cat'],
            subtitle=meta['sub'],
            glyph_type=meta['glyph'],
            out_path=out_img
        )

        # Upload and replace preview_images
        old_previews = rec.get('preview_images', [])
        data = {'preview_images-': old_previews} if old_previews else {}
        with open(out_img, 'rb') as f_img:
            files = {'preview_images': (f'cover_{mid}.png', f_img, 'image/png')}
            patch_resp = requests.patch(f'{SERVER_URL}/api/collections/models/records/{mid}',
                                        headers=headers, data=data, files=files)
            if patch_resp.status_code == 200:
                print(f"[{idx:2d}/{len(records)}] OK: {clean_title} -> {meta['cat']}")
                success_count += 1
            else:
                print(f"[{idx:2d}/{len(records)}] FAIL: {clean_title} ({patch_resp.status_code}) {patch_resp.text[:80]}")

    print(f"\nFinished updating covers: {success_count}/{len(records)} updated successfully.")

if __name__ == '__main__':
    main()
