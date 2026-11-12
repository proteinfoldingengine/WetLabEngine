"""Durably preserve original successful AND failed run evidence.
No model calls. Retry archival includes artifacts from the originating attempt.
"""
import hashlib,io,json,os,re,urllib.error,urllib.request,zipfile,subprocess,sys
from pathlib import Path
PREFIX='fixed-quantum-recovery'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def select_artifacts(items):
    return [a for a in items if re.fullmatch(PREFIX+r'-(verification|review|publication)-[0-9]+',a['name'])]
def disposition(states,errors,missing,verdict):
    complete=all(states.get(k)=='success' for k in ('verification','review','publication')) and not errors and not missing
    return dict(preservation_status='COMPLETE' if not errors and not missing else 'PARTIAL',
        scientific_pipeline_complete=complete,
        accepted=bool(complete and verdict and verdict.get('verdict')=='ACCEPTED'),
        reviewer_verdict=verdict.get('verdict') if verdict else None,
        native_bridge='NOT_DERIVED')
def chunk_large(directory,limit=40*1024*1024):
    maps=[]
    for f in sorted(directory.rglob('*')):
        if not f.is_file() or f.stat().st_size<=limit:continue
        raw=f.read_bytes();parts=[]
        for i in range(0,len(raw),limit):
            block=raw[i:i+limit];name=str(f.relative_to(directory))+'.part-'+str(i//limit).zfill(4)
            (directory/name).write_bytes(block);parts.append(dict(file=name,bytes=len(block),sha256=sha(block)))
        assert b''.join((directory/p['file']).read_bytes() for p in parts)==raw
        maps.append(dict(file=str(f.relative_to(directory)),bytes=len(raw),sha256=sha(raw),parts=parts));f.unlink()
    (directory/'CHUNKS.json').write_text(json.dumps(maps,indent=2,sort_keys=True)+'\n')
def sums(directory):
    target=directory/'SHA256SUMS'
    target.write_text(''.join(sha(f.read_bytes())+'  '+str(f.relative_to(directory))+'\n' for f in sorted(directory.rglob('*')) if f.is_file() and f!=target))
def readback(root,ref):
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert sha(subprocess.check_output(['git','show',ref+':'+str(root/name)]))==digest,name
    for m in json.loads((root/'CHUNKS.json').read_text()):
        h=hashlib.sha256();size=0
        for part in m['parts']:
            raw=subprocess.check_output(['git','show',ref+':'+str(root/part['file'])]);h.update(raw);size+=len(raw)
        assert h.hexdigest()==m['sha256'] and size==m['bytes']
def main():
    repo=os.environ['GITHUB_REPOSITORY'];run=os.environ['GITHUB_RUN_ID'];attempt=os.environ['GITHUB_RUN_ATTEMPT']
    root=Path('ResearchHistory/UQCF-GEM/research/physical-bridge/fixed_quantum_recovery_review/evidence')/('run-'+run+'-attempt-'+attempt)
    root.mkdir(parents=True,exist_ok=True)
    if len(sys.argv)>1 and sys.argv[1]=='readback':
        readback(root,sys.argv[2]);print('Committed original evidence and chunks verified');return
    headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    base='https://api.github.com/repos/'+repo
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs):return None
    opener=urllib.request.build_opener(NoRedirect)
    def api(path):
        with urllib.request.urlopen(urllib.request.Request(base+path,headers=headers),timeout=60) as response:return response.read()
    def download(path):
        request=urllib.request.Request(base+path,headers=headers)
        try:
            with opener.open(request,timeout=60) as response:return response.read()
        except urllib.error.HTTPError as exc:
            if exc.code not in (301,302,303,307,308):raise
            target=exc.headers['Location'];assert target.startswith('https://')
            # Strip bearer authorization on signed-storage redirect.
            with urllib.request.urlopen(target,timeout=180) as response:return response.read()
    items=[];page=1
    while True:
        listing=json.loads(api('/actions/runs/'+run+'/artifacts?per_page=100&page='+str(page)))
        items+=listing['artifacts']
        if len(listing['artifacts'])<100:break
        page+=1
    items=select_artifacts(items);receipts=[];errors=[]
    for item in items:
        name=item['name']
        try:
            raw=download('/actions/artifacts/'+str(item['id'])+'/zip')
            (root/(name+'.zip')).write_bytes(raw)  # preserve before validating
            receipt=dict(id=item['id'],name=name,bytes=len(raw),api_digest=item.get('digest'),download_sha256=sha(raw))
            receipts.append(receipt)
            assert item.get('digest')=='sha256:'+sha(raw) and item.get('expired') is False
            dest=root/name;dest.mkdir(exist_ok=True)
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                for member in archive.infolist():
                    target=dest/member.filename;assert target.resolve().is_relative_to(dest.resolve())
                    if member.is_dir():target.mkdir(parents=True,exist_ok=True)
                    else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(archive.read(member))
            manifest=dest/'artifact_manifest.json';declared=json.loads(manifest.read_bytes())
            actual={str(f.relative_to(dest)) for f in dest.rglob('*') if f.is_file() and f!=manifest}
            assert actual==set(declared)
            for rel,value in declared.items():
                target=dest/rel;assert target.resolve().is_relative_to(dest.resolve())
                data=target.read_bytes();assert len(data)==value['bytes'] and sha(data)==value['sha256']
            receipt['manifest_status']='VALID';receipt['members']=len(actual)+1
        except Exception as exc:
            errors.append(dict(stage='artifact',name=name,error_type=type(exc).__name__,http_status=getattr(exc,'code',None)))
    jobs=json.loads(api('/actions/runs/'+run+'/jobs?per_page=100'))['jobs'];logs=[];states={}
    for job in jobs:
        if job['name'] in ('verification','review','publication'):states[job['name']]=job['conclusion']
        if job['status']!='completed' or job['conclusion']=='skipped':continue
        try:
            raw=download('/actions/jobs/'+str(job['id'])+'/logs');name='job-'+str(job['id'])+'.log';(root/name).write_bytes(raw)
            logs.append(dict(id=job['id'],name=job['name'],conclusion=job['conclusion'],file=name,bytes=len(raw),sha256=sha(raw)))
        except Exception as exc:
            errors.append(dict(stage='job_log',job_id=job['id'],error_type=type(exc).__name__,http_status=getattr(exc,'code',None)))
    # On a retry, reused originating receipts are authoritative for already successful stages.
    for stage in ('verification','publication'):
        for item in items:
            if item['name'].startswith(PREFIX+'-'+stage+'-'):
                path=root/item['name']/'receipt.json'
                if path.exists():
                    receipt=json.loads(path.read_bytes())
                    if receipt.get('status')=='PASS' and receipt.get('checkout_sha')==os.environ['GITHUB_SHA'] and str(receipt.get('run_id'))==run:states[stage]='success'
    verdict=None
    path=root/(PREFIX+'-review-1')/'verdict.json'
    if path.exists():
        verdict=json.loads(path.read_bytes())
        identity_path=path.parent/'review_identity.json'
        if identity_path.exists():
            identity=json.loads(identity_path.read_bytes())
            if identity.get('checkout_sha')==os.environ['GITHUB_SHA'] and str(identity.get('run_id'))==run:states['review']='success'
    missing=[stage for stage in ('verification','review','publication') if not any(a['name'].startswith(PREFIX+'-'+stage+'-') for a in items)]
    result=dict(disposition(states,errors,missing,verdict),run_id=run,attempt=attempt,workflow_sha=os.environ['UQCF_WORKFLOW_SHA'],checkout_sha=os.environ['GITHUB_SHA'],artifacts=receipts,completed_job_logs=logs,job_states=states,validation_errors=errors,missing_stage_artifacts=missing)
    (root/'DOWNLOAD_AUDIT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    chunk_large(root);sums(root)
    print('Evidence preserved:',result['preservation_status'],'; reviewer verdict:',result['reviewer_verdict'])
    print(str(root))
if __name__=='__main__':main()

