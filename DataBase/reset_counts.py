import urllib.request
import json

url = 'http://127.0.0.1:5050/api/collections/models/records?perPage=100'
req = urllib.request.urlopen(url)
data = json.loads(req.read().decode('utf-8'))
items = data.get('items', [])
print(f"Found {len(items)} items to reset.")

for item in items:
    mid = item['id']
    patch_req = urllib.request.Request(
        f"http://127.0.0.1:5050/api/collections/models/records/{mid}",
        data=json.dumps({"view_Count": "0", "download_count": "0"}).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="PATCH"
    )
    urllib.request.urlopen(patch_req)

print("All items successfully reset to view_Count=0 and download_count=0.")
