"""One-time import. Existing assets are kept; the published site uses local files only."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import io,json,urllib.request,time
from PIL import Image
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'assets-manifest.json').read_text())
def download(item):
 rel,url=item; dest=root/'docs'/rel
 if dest.exists(): return
 dest.parent.mkdir(parents=True,exist_ok=True)
 for attempt in range(3):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'FamilyCompassMigration/1.0'})
   data=urllib.request.urlopen(req,timeout=60).read()
   im=Image.open(io.BytesIO(data));im.thumbnail((1800,2200))
   im.save(dest,'WEBP',quality=90,method=4)
   return
  except Exception:
   if attempt==2:raise
   time.sleep(2)
with ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(download,manifest.items()))
missing=[p for p in manifest if not (root/'docs'/p).is_file()]
assert not missing,missing
print(f'All {len(manifest)} illustrations are stored locally in docs/assets.')
