"""Publication-only archive repair: original ZIP chunks, no science/model rerun."""
import hashlib,io,json,os,subprocess,sys,time,urllib.error,urllib.request,zipfile
from pathlib import Path
repo=os.environ['GITHUB_REPOSITORY']; run='41540085233'; attempt='1'
science='c721762f4890a81036fb2bff11d394881384496f'
root=Path('ResearchHistory/UQCF-GEM/research/physical-bridge/native_owner_correspondence/evidence')/('run-'+run+'-attempt-'+attempt)
limit=40*1024*1024
def digest(raw): return hashlib.sha256(raw).hexdigest()
if len(sys.argv)>1 and sys.argv[1]=='readback':
    ref=sys.argv[2]
    rows=(root/'SHA256SUMS').read_text().splitlines()
    for line in rows:
        expected,name=line.split('  ',1)
        raw=subprocess.check_output(['git','show',ref+':'+str(root/name)])
        assert digest(raw)==expected,name
    print('Remote commit readback PASS:',ref,'files',len(rows));sys.exit(0)
root.mkdir(parents=True,exist_ok=True)
headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
base='https://api.github.com/repos/'+repo
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
opener=urllib.request.build_opener(NoRedirect)
def api(path):
    with urllib.request.urlopen(urllib.request.Request(base+path,headers=headers),timeout=60) as r:return r.read()
def download(path):
    try:
        with opener.open(urllib.request.Request(base+path,headers=headers),timeout=60) as r:return r.read()
    except urllib.error.HTTPError as e:
        if e.code not in (301,302,303,307,308):raise
        target=e.headers['Location'];assert target.startswith('https://')
        with urllib.request.urlopen(target,timeout=180) as r:return r.read()
def write(name,obj): (root/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
# Wait for the original frozen run, including its archive job, to finish.
for _ in range(90):
    run_info=json.loads(api('/actions/runs/'+run))
    assert run_info['head_sha']==science
    if run_info['status']=='completed':break
    time.sleep(10)
else: raise RuntimeError('Original run still active')
items=json.loads(api('/actions/runs/'+run+'/artifacts?per_page=100'))['artifacts']
expected={f'owner-correspondence-{part}-{attempt}' for part in ('verification','review','publication')}
items=[v for v in items if v['name'] in expected]
assert len(items)==3 and {x['name'] for x in items}==expected
receipts=[]; binaries=[]
for item in items:
    raw=download('/actions/artifacts/'+str(item['id'])+'/zip'); h=digest(raw)
    assert item['digest']=='sha256:'+h and not item['expired']
    name=item['name']; zipname=name+'.zip'; parts=[]
    if len(raw)>limit:
        for i,start in enumerate(range(0,len(raw),limit)):
            part=raw[start:start+limit]; pn=zipname+f'.part-{i:03d}'; (root/pn).write_bytes(part)
            parts.append(dict(file=pn,bytes=len(part),sha256=digest(part)))
        write(zipname+'.parts.json',dict(original_file=zipname,bytes=len(raw),sha256=h,parts=parts,
              reconstruction='Concatenate parts in listed order as raw bytes; verify total byte count and SHA-256.'))
        rebuilt=b''.join((root/p['file']).read_bytes() for p in parts)
        assert rebuilt==raw;del rebuilt
    else:(root/zipname).write_bytes(raw)
    dest=root/name;dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        declared=json.loads(z.read('artifact_manifest.json'))
        actual={m.filename for m in z.infolist() if not m.is_dir() and m.filename!='artifact_manifest.json'}
        assert actual==set(declared)
        for member in z.infolist():
            target=dest/member.filename;assert target.resolve().is_relative_to(dest.resolve())
            if member.is_dir():continue
            data=z.read(member)
            if member.filename!='artifact_manifest.json':
                assert declared[member.filename]==dict(bytes=len(data),sha256=digest(data))
            if len(data)>limit:
                binaries.append(dict(logical_path=str(target.relative_to(root)),bytes=len(data),sha256=digest(data),
                                     source_zip=zipname,zip_member=member.filename,
                                     reconstruction='Reconstruct the original ZIP if chunked, then extract this exact member.'))
            else:
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    receipts.append(dict(id=item['id'],name=name,zip_bytes=len(raw),api_digest=item['digest'],
                         download_sha256=h,member_count=len(actual)+1,chunked=bool(parts)))
review=json.loads((root/'owner-correspondence-review-1/verdict.json').read_bytes())
assert review['verdict']=='ACCEPTED' and all(review[k]==[] for k in ('findings','missing_assumptions','counterexamples'))
assert review['native_bridge_status']=='NOT_DERIVED'
for part in ('verification','publication'):
    receipt=json.loads((root/f'owner-correspondence-{part}-1/receipt.json').read_bytes())
    assert receipt['status']=='PASS' and receipt['checkout_sha']==science
jobs=json.loads(api('/actions/runs/'+run+'/jobs?per_page=100'))['jobs']
assert all(next(j for j in jobs if j['name']==name)['conclusion']=='success' for name in ('verification','review','publication'))
logs=[]
for job in jobs:
    assert job['status']=='completed'
    raw=download('/actions/jobs/'+str(job['id'])+'/logs'); name='job-'+str(job['id'])+'.log';(root/name).write_bytes(raw)
    logs.append(dict(id=job['id'],name=job['name'],conclusion=job['conclusion'],file=name,bytes=len(raw),sha256=digest(raw)))
write('LARGE_MEMBERS.json',binaries)
failed_repair_logs=[]
for prior_run in ('41541044219',):
    prior_jobs=json.loads(api('/actions/runs/'+prior_run+'/jobs?per_page=100'))['jobs']
    for job in prior_jobs:
        assert job['status']=='completed'
        raw=download('/actions/jobs/'+str(job['id'])+'/logs');name='prior-repair-job-'+str(job['id'])+'.log';(root/name).write_bytes(raw)
        failed_repair_logs.append(dict(run_id=prior_run,job_id=job['id'],conclusion=job['conclusion'],file=name,sha256=digest(raw)))
write('DOWNLOAD_AUDIT.json',dict(status='PASS',science_sha=science,original_run=run,original_conclusion=run_info['conclusion'],
      repair_run=os.environ['GITHUB_RUN_ID'],repair_sha=os.environ['GITHUB_SHA'],artifacts=receipts,completed_job_logs=logs,
      review_verdict=review['verdict'],native_bridge_status='NOT_DERIVED',failed_repair_logs=failed_repair_logs,
      storage='Original ZIP bytes preserved. Large ZIPs are chunked; large extracted members remain recoverable from those exact original ZIPs.'))
assert all(p.stat().st_size<=limit for p in root.rglob('*') if p.is_file())
(root/'SHA256SUMS').write_text(''.join(digest(p.read_bytes())+'  '+str(p.relative_to(root))+'\n' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
print('Original ZIP API digests, exact member manifests and reconstructed chunks PASS; no science or model rerun.')
