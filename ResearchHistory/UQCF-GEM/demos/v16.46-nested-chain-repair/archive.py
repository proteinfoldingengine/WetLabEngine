"""Lossless bounded-size Git retention of the complete API artifact ZIP."""
from pathlib import Path
import json,hashlib
LIMIT=24*1024*1024
def digest(data):return hashlib.sha256(data).hexdigest()
def retain(path,limit=LIMIT):
 path=Path(path);data=path.read_bytes();folder=path.with_suffix('.chunks');folder.mkdir()
 rows=[]
 for offset in range(0,len(data),limit):
  part=data[offset:offset+limit];name=f'{len(rows):05d}.part';(folder/name).write_bytes(part);rows.append({'name':name,'size':len(part),'sha256':digest(part)})
 record={'schema':1,'size':len(data),'sha256':digest(data),'limit':limit,'chunks':rows}
 (folder/'ARCHIVE.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
 verify(folder,'sha256:'+digest(data));path.unlink();return folder
def verify(folder,expected_digest):
 folder=Path(folder);r=json.loads((folder/'ARCHIVE.json').read_text())
 if set(r)!={'schema','size','sha256','limit','chunks'} or r['schema']!=1 or type(r['limit'])is not int or not 0<r['limit']<=LIMIT:raise ValueError('archive metadata')
 rows=r['chunks'];names=[f'{i:05d}.part' for i in range(len(rows))]
 if not rows or [x['name'] for x in rows]!=names or {p.name for p in folder.iterdir()}!=set(names)|{'ARCHIVE.json'}:raise ValueError('archive membership')
 parts=[]
 for i,row in enumerate(rows):
  if set(row)!={'name','size','sha256'}:raise ValueError('chunk metadata')
  data=(folder/row['name']).read_bytes()
  if len(data)!=row['size'] or digest(data)!=row['sha256'] or not 0<len(data)<=r['limit'] or (i<len(rows)-1 and len(data)!=r['limit']):raise ValueError('chunk bytes')
  parts.append(data)
 data=b''.join(parts)
 if len(data)!=r['size'] or digest(data)!=r['sha256'] or 'sha256:'+digest(data)!=expected_digest:raise ValueError('archive API digest')
 return data

def verify_extracted(data,root,expected_digest):
 """Verify raw API ZIP and equality to every retained extracted byte."""
 import tempfile,zipfile,io
 if 'sha256:'+digest(data)!=expected_digest:raise ValueError('raw ZIP digest')
 root=Path(root)
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  members=[m for m in z.infolist() if not m.is_dir()]
  names=[m.filename for m in members]
  if len(names)!=len(set(names)) or any(Path(n).is_absolute() or '..' in Path(n).parts for n in names):raise ValueError('raw ZIP membership')
  actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
  if set(names)!=actual:raise ValueError('raw/extracted membership')
  for name in names:
   if z.read(name)!=(root/name).read_bytes():raise ValueError('raw/extracted content')
