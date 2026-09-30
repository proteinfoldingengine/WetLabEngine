import sys,zipfile,hashlib,json,tarfile,io,gzip,re
from pathlib import Path
p=Path(sys.argv[1]);expected=sys.argv[2];out=Path(sys.argv[3])
digest=hashlib.sha256(p.read_bytes()).hexdigest()
assert 'sha256:'+digest==expected
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 names=z.namelist();assert len(names)==len(set(names))
 assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names)
 z.extractall(out)
manifest=json.loads((out/'MANIFEST.json').read_text())
actual={str(f.relative_to(out)) for f in out.rglob('*') if f.is_file() and f.name!='MANIFEST.json'}
assert set(manifest)==actual
for name,h in manifest.items():assert hashlib.sha256((out/name).read_bytes()).hexdigest()==h,name
src=json.loads((out/'SOURCE_MANIFEST.json').read_text())
with tarfile.open(out/'SOURCE.tar.gz','r:gz') as t:
 members=t.getmembers();assert len(members)==len(src)
 assert {m.name for m in members}==set(src)
 for m in members:assert m.isfile() and hashlib.sha256(t.extractfile(m).read()).hexdigest()==src[m.name],m.name
s=json.loads((out/'scientific/SUMMARY.json').read_text())
raw=gzip.decompress((out/'scientific/CERTIFICATE.json.gz').read_bytes())
assert len(raw)==s['raw_bytes'] and hashlib.sha256(raw).hexdigest()==s['raw_sha256']
tests={}
for f in (out/'logs').glob('*.log'):
 counts=[int(n) for n in re.findall(r'Ran (\d+) tests? in',f.read_text())]
 if counts:tests[f.name]={'total':sum(counts),'suites':counts}
print(json.dumps({'zip_sha256':digest,'manifest_members':len(manifest),'source_members':len(src),'metadata':json.loads((out/'METADATA.json').read_text()),'summary':s,'verification':json.loads((out/'scientific/VERIFY.json').read_text()),'tests':tests},sort_keys=True))
