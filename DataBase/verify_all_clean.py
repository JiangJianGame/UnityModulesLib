# -*- coding: utf-8 -*-
import requests, io
from PIL import Image

auth = requests.post('http://127.0.0.1:5050/api/collections/_superusers/auth-with-password',
                     json={'identity': 'admin@modules.local', 'password': 'Admin12345678'}).json()
headers = {'Authorization': auth['token']}
recs = requests.get('http://127.0.0.1:5050/api/collections/models/records?perPage=100', headers=headers).json().get('items', [])

print(f"=== VERIFYING ALL {len(recs)} PLUGINS IN POCKETBASE ===")

duplicates_found = 0
invalid_covers = 0

for r in sorted(recs, key=lambda x: x['title']):
    title = r['title']
    col, rid = r['collectionId'], r['id']
    imgs = r.get('preview_images', [])
    
    if len(imgs) == 0:
        print(f"ERROR: {title} has 0 images!")
        invalid_covers += 1
        continue
        
    loaded = []
    for idx, fn in enumerate(imgs):
        url = f'http://127.0.0.1:5050/api/files/{col}/{rid}/{fn}'
        resp = requests.get(url)
        im = Image.open(io.BytesIO(resp.content))
        w, h = im.size
        # Check cover resolution
        if idx == 0 and (w < 800 or h < 450):
            print(f"WARN: {title} cover is small: {w}x{h}")
            invalid_covers += 1
        im_g = im.convert('L').resize((32, 32))
        thumb = list(im_g.getdata())
        loaded.append((fn, (w, h), thumb))
        
    # Check pairwise duplicates
    for i in range(len(loaded)):
        for j in range(i + 1, len(loaded)):
            diff = sum(abs(a - b) for a, b in zip(loaded[i][2], loaded[j][2])) / 1024.0
            if diff < 12.0:
                print(f"DUPLICATE DETECTED in [{title}]: {loaded[i][0]} vs {loaded[j][0]} (diff: {diff:.2f})")
                duplicates_found += 1

print("\n=== VERIFICATION SUMMARY ===")
print(f"Total Plugins Checked : {len(recs)}")
print(f"Duplicate Pairs Found : {duplicates_found}")
print(f"Invalid Covers Found  : {invalid_covers}")
if duplicates_found == 0 and invalid_covers == 0:
    print("SUCCESS: ALL PLUGINS ARE 100% CLEAN AND PROMINENT!")
