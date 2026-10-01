"""Deterministic content-addressed source snapshots with complete path bindings."""
from pathlib import Path
import tarfile,gzip,io,hashlib,json
FORMAT={'schema':1,'representation':'sha256-objects','path_manifest':'SOURCE_MANIFEST.json'}
def sha(data):return hashlib.sha256(data).hexdigest()
def write(root,mapping,path):
 root=Path(root);objects={}
 for name,digest in sorted(mapping.items()):
  data=(root/name).read_bytes()
  if sha(data)!=digest:raise ValueError('source mapping content')
  objects[digest]=data
 with Path(path).open('wb') as f:
  with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as gz:
   with tarfile.open(fileobj=gz,mode='w') as tf:
    for digest,data in sorted(objects.items()):
     info=tarfile.TarInfo('objects/'+digest);info.size=len(data);info.mode=0o644;info.mtime=0;tf.addfile(info,io.BytesIO(data))
def verify(path,mapping,expected,format_marker):
 if format_marker!=FORMAT or mapping!=expected:raise ValueError('source format/path identities')
 wanted={'objects/'+d for d in expected.values()};objects={}
 with tarfile.open(path,'r:gz') as tf:
  members=tf.getmembers();names=[m.name for m in members]
  if len(names)!=len(set(names)) or set(names)!=wanted:raise ValueError('source object membership')
  for member in members:
   if not member.isfile():raise ValueError('nonregular source object')
   data=tf.extractfile(member).read();digest=member.name.removeprefix('objects/')
   if sha(data)!=digest:raise ValueError('source object content')
   objects[digest]=data
 return {name:objects[digest] for name,digest in expected.items()}

def read_json(path):
 def unique(pairs):
  result={}
  for key,value in pairs:
   if key in result:raise ValueError('duplicate JSON mapping identity')
   result[key]=value
  return result
 return json.loads(Path(path).read_text(),object_pairs_hook=unique)
