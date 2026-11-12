"""Download original run ZIPs, verify API digests and member manifests, retain raw bytes."""
import hashlib,io,json,os,urllib.error,urllib.request,zipfile
from pathlib import Path
repo=os.environ['GITHUB_REPOSITORY']; run=os.environ['GITHUB_RUN_ID']; attempt=os.environ['GITHUB_RUN_ATTEMPT']
root=Path('ResearchHistory/UQCF-GEM/research/physical-bridge/rd8_correction_review/evidence')/('run-'+run+'-attempt-'+attempt)
root.mkdir(parents=True,exist_ok=True)
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
expected={f'rd8-correction-{part}-{attempt}' for part in ('integrity','stack','review','publication','replay')}
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
    manifests=list(dest.rglob('artifact_manifest.json')); assert len(manifests)==1
    m=manifests[0]; declared=json.loads(m.read_bytes())
    actual={str(f.relative_to(m.parent)) for f in m.parent.rglob('*') if f.is_file() and f!=m}
    assert actual==set(declared), 'Missing or additional evidence member'
    for rel,v in declared.items():
        f=m.parent/rel; assert f.resolve().is_relative_to(m.parent.resolve())
        data=f.read_bytes();assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
    receipts.append(dict(id=item['id'],name=name,zip_bytes=len(raw),api_digest=item['digest'],download_sha256=digest,member_count=len(actual)+1))
review=json.loads((root/f'rd8-correction-review-{attempt}'/'verdict.json').read_bytes())
assert review['verdict']=='ACCEPTED' and all(review[k]==[] for k in ('findings','missing_assumptions','counterexamples'))
assert review['native_bridge_status']=='NOT_DERIVED'
for part,name in [('stack','receipt.json'),('replay','receipt.json'),('publication','publication.json')]:
    receipt=json.loads((root/f'rd8-correction-{part}-{attempt}'/name).read_bytes())
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
(root/'SHA256SUMS').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(root))+'\n' for f in sorted(root.rglob('*')) if f.is_file() and f.name!='SHA256SUMS'))
print('Original artifact ZIP digests and all complete member manifests verified; raw evidence retained.')
print(str(root))
