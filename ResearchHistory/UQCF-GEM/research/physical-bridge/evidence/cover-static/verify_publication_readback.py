"""Verify exact GitHub text readbacks and tree identities against local bytes."""
import hashlib,json,pathlib,sys
P=pathlib.Path(__file__).parent
packet=json.loads(pathlib.Path(sys.argv[1]).read_text())
entries=json.loads((P/'publication_entries.json').read_text())
by_path={r['path']:r for r in packet['texts']}
assert len(by_path)==len(entries)==len(packet['texts'])
ledger=[]
for e in entries:
 r=by_path[e['path']];b=e['content'].encode()
 assert r['content']==e['content']
 sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert r['sha']==sha
 ledger.append(dict(path=e['path'],sha256=hashlib.sha256(b).hexdigest(),git_blob_sha=sha,exact_bytes=True))
expected=json.loads((P/'binary_entries.json').read_text());actual={r['path']:r['sha'] for r in packet['binary']}
assert len(actual)==len(expected)==len(packet['binary'])
for e in expected:
 b=(P/'originals'/e['path'].split('/')[-1]).read_bytes()
 assert actual[e['path']]==e['sha']==hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert packet['branch_head']==packet['commit']
out=dict(commit=packet['commit'],branch_head=packet['branch_head'],texts=ledger,binary=expected,status='PASS')
pathlib.Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(commit=out['commit'],texts=len(ledger),binary=len(expected),status='PASS')))
