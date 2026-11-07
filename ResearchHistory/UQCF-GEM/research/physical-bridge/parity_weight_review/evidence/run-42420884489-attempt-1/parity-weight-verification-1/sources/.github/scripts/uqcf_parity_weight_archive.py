"""Download original run ZIPs, verify API digests and member manifests, retain raw bytes."""
import hashlib,io,json,os,urllib.error,urllib.request,zipfile,subprocess,sys
from pathlib import Path
repo=os.environ['GITHUB_REPOSITORY']; run=os.environ['GITHUB_RUN_ID']; attempt=os.environ['GITHUB_RUN_ATTEMPT']
root=Path('ResearchHistory/UQCF-GEM/research/physical-bridge/parity_weight_review/evidence')/('run-'+run+'-attempt-'+attempt)
root.mkdir(parents=True,exist_ok=True)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def chunk_large(directory, limit=40*1024*1024):
    # The map retains the original logical filename, size and digest.
    maps=[]
    for f in sorted(directory.rglob('*')):
        if not f.is_file() or f.stat().st_size<=limit:continue
        raw=f.read_bytes();parts=[]
        for i in range(0,len(raw),limit):
            block=raw[i:i+limit];name=str(f.relative_to(directory))+'.part-'+str(i//limit).zfill(4)
            target=directory/name;target.write_bytes(block)
            parts.append(dict(file=name,bytes=len(block),sha256=sha(block)))
        rebuilt=b''.join((directory/part['file']).read_bytes() for part in parts)
        assert rebuilt==raw
        maps.append(dict(file=str(f.relative_to(directory)),bytes=len(raw),sha256=sha(raw),parts=parts));f.unlink()
    (directory/'CHUNKS.json').write_text(json.dumps(maps,indent=2,sort_keys=True)+'\n')
def sums(directory):
    (directory/'SHA256SUMS').write_text(''.join(sha(f.read_bytes())+'  '+str(f.relative_to(directory))+'\n' for f in sorted(directory.rglob('*')) if f.is_file() and f.name!='SHA256SUMS'))
if len(sys.argv)>1 and sys.argv[1]=='readback':
    for directory in (root,):
        for line in (directory/'SHA256SUMS').read_text().splitlines():
            digest,name=line.split('  ',1)
            assert sha(subprocess.check_output(['git','show',sys.argv[2]+':'+str(directory/name)]))==digest,name
        for m in json.loads((directory/'CHUNKS.json').read_text()):
            h=hashlib.sha256();size=0
            for part in m['parts']:
                b=subprocess.check_output(['git','show',sys.argv[2]+':'+str(directory/part['file'])]);h.update(b);size+=len(b)
            assert h.hexdigest()==m['sha256'] and size==m['bytes']
    print('Committed original bytes and all chunk reconstructions verified');sys.exit(0)
headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
base='https://api.github.com/repos/'+repo
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
opener=urllib.request.build_opener(NoRedirect)
def api(path):
    with urllib.request.urlopen(urllib.request.Request(base+path,headers=headers),timeout=60) as r:return r.read()
def download_path(path):
    req=urllib.request.Request(base+path,headers=headers)
    try:
        with opener.open(req,timeout=60) as r:return r.read()
    except urllib.error.HTTPError as e:
        if e.code not in (301,302,303,307,308):raise
        target=e.headers['Location']
        if not target.startswith('https://'):raise ValueError('Non-HTTPS artifact redirect')
        # No authorization header is forwarded to the signed storage URL.
        with urllib.request.urlopen(target,timeout=180) as r:return r.read()
listing=json.loads(api('/actions/runs/'+run+'/artifacts?per_page=100'))
expected={f'parity-weight-{part}-{attempt}' for part in ('verification','review','publication')}
items=[x for x in listing['artifacts'] if x['name'] in expected]
assert len(items)==len(expected) and {x['name'] for x in items}==expected
receipts=[]
for item in items:
    raw=download_path('/actions/artifacts/'+str(item['id'])+'/zip'); digest=hashlib.sha256(raw).hexdigest()
    assert item.get('digest')=='sha256:'+digest, 'API artifact digest mismatch'
    assert item.get('expired') is False
    name=item['name']; (root/(name+'.zip')).write_bytes(raw)
    dest=root/name;dest.mkdir()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for member in z.infolist():
            target=dest/member.filename
            assert target.resolve().is_relative_to(dest.resolve()), 'Unsafe ZIP member'
            if member.is_dir(): target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(member))
    m=dest/'artifact_manifest.json'; assert m.is_file()
    declared=json.loads(m.read_bytes())
    actual={str(f.relative_to(dest)) for f in dest.rglob('*') if f.is_file() and f!=m}
    assert actual==set(declared), 'Missing or additional evidence member'
    for rel,v in declared.items():
        f=dest/rel; assert f.resolve().is_relative_to(dest.resolve())
        data=f.read_bytes(); assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
    receipts.append(dict(id=item['id'],name=name,zip_bytes=len(raw),api_digest=item['digest'],download_sha256=digest,member_count=len(actual)+1))
review=json.loads((root/f'parity-weight-review-{attempt}'/'verdict.json').read_bytes())
assert review['verdict'] in ('ACCEPTED','REVISE','FAIL')
assert review['native_bridge_status']=='NOT_DERIVED'
for part in ('verification','publication'):
    receipt=json.loads((root/f'parity-weight-{part}-{attempt}'/'receipt.json').read_bytes())
    assert receipt['status']=='PASS' and str(receipt['run_id'])==run and receipt['checkout_sha']==os.environ['GITHUB_SHA']
jobs=json.loads(api('/actions/runs/'+run+'/jobs?per_page=100'))['jobs']
job_logs=[]
for job in jobs:
    if job['status']=='completed':
        log=download_path('/actions/jobs/'+str(job['id'])+'/logs')
        name='job-'+str(job['id'])+'.log';(root/name).write_bytes(log)
        job_logs.append(dict(id=job['id'],name=job['name'],conclusion=job['conclusion'],file=name,bytes=len(log),sha256=hashlib.sha256(log).hexdigest()))
assert len(job_logs)>=3 and all(j['conclusion']=='success' for j in job_logs)
(root/'DOWNLOAD_AUDIT.json').write_text(json.dumps(dict(status='PASS',run_id=run,attempt=attempt,workflow_sha=os.environ['UQCF_WORKFLOW_SHA'],checkout_sha=os.environ['GITHUB_SHA'],artifacts=receipts,completed_job_logs=job_logs,native_bridge='NOT_DERIVED'),indent=2,sort_keys=True)+'\n')
chunk_large(root);sums(root)
print('Original ZIP digests, complete manifests and reversible chunks verified.')
print(str(root))
