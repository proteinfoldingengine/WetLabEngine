"""Reassemble oversized original ZIPs without repacking or changing one byte."""
import hashlib,json,pathlib

def materialize(root):
 root=pathlib.Path(root);manifest=root/'archive_segments.json'
 if not manifest.exists():return
 for entry in json.loads(manifest.read_text())['archives']:
  chunks=[]
  for part in entry['segments']:
   path=root/part['file'];assert path.exists(),'missing archive segment'
   data=path.read_bytes()
   assert len(data)==part['bytes'] and hashlib.sha256(data).hexdigest()==part['sha256'],'corrupt archive segment'
   chunks.append(data)
  original=b''.join(chunks)
  assert len(original)==entry['bytes'] and hashlib.sha256(original).hexdigest()==entry['sha256'],'original archive reassembly mismatch'
  destination=root/entry['file']
  if not destination.exists():destination.write_bytes(original)
if __name__=='__main__':materialize(pathlib.Path(__file__).parent)
