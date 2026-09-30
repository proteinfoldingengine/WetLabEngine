"""Integrity inspection only; does not execute research code."""
import hashlib,json,sys,tarfile
from pathlib import Path
package=Path(sys.argv[1]); remote=json.loads(Path(sys.argv[2]).read_text())
source=json.loads((package/'SOURCE_MANIFEST.json').read_text())
with tarfile.open(package/'SOURCE.tar.gz','r:gz') as archive:
    for member in archive.getmembers():
        data=archive.extractfile(member).read()
        git_hash=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert remote.get(member.name)==git_hash, member.name
        assert hashlib.sha256(data).hexdigest()==source[member.name],member.name
print(json.dumps({'all_source_members_match_remote_git_blobs':len(source)}))
