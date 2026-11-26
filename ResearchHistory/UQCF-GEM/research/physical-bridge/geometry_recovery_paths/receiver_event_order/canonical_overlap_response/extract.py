"""Read the immutable archive without any GitHub Actions service or external download."""
import base64, io, json, sys, zipfile
from hashlib import sha1, sha256
from pathlib import Path
a,out=map(Path,sys.argv[1:])
m=a/'manifest.json'
assert sha1(b'blob '+str(m.stat().st_size).encode()+b'\0'+m.read_bytes()).hexdigest()=='617c5f2a7b81075e8ad5f9afadf1127e36d3255a'
summary=json.loads(m.read_bytes());pieces=[]
for row in sorted(summary['parts'],key=lambda r:r['file']):
    if row['file'].startswith('publication.zip.b64.part-'):
        b=(a/row['file']).read_bytes()
        assert sha256(b).hexdigest()==row['sha256']
        assert sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob']
        pieces.append(b)
assert len(pieces)==3
archive=base64.b64decode(b''.join(pieces))
assert sha256(archive).hexdigest()=='57dbc794880b1eb39d40de4c4b40e1900f5cdd9410edd762fb2558b1f6f0e613'
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    raw=z.read('raw.json')
assert sha256(raw).hexdigest()=='319c43442aee53b9da4e94bc2005841bcaba39629318d285b2b4f9d11838f515'
out.write_bytes(raw)
