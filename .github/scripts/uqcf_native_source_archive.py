"""Publish exact completed source-audit evidence; never call a model or rerun science."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile

RUN = 41486442606
CONTROLLER = '340a9465a92e8ffd387bd26d31c8fe2f5e33f3fe'
SOURCE = '2f7a788f551face7b69521b0d07d2ec3e3ea3871'
ROOT = Path('ResearchHistory/UQCF-GEM/research/physical-bridge/native_joint_source_audit/evidence/run-41486442606-attempt-1')
EXPECTED = {
 'native-source-audit-verification-1': (13161939280, '1060d99a5606505113268991c3aaff8c019b3b657b42fdc8524292ede92faaa9'),
 'native-source-audit-review-1': (13161934934, '0ba8c47888793eaef98fce14bd833251591d8eb18b1daeb6d0c873a42eb31cd7'),
 'native-source-audit-publication-1': (13163605957, '8d26257fc6d0c32ad12fc2beee9b834fa2af8cad0e49ae4a0e909b61f6e1f0d5'),
}
def sha(raw): return hashlib.sha256(raw).hexdigest()
def unpack(raw, dest):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        files=[x for x in z.infolist() if not x.is_dir()]
        names=[x.filename for x in files]
        assert len(names)==len(set(names)), 'duplicate ZIP members'
        manifest=json.loads(z.read('artifact_manifest.json'))
        assert set(names)-{'artifact_manifest.json'}==set(manifest), 'coverage mismatch'
        for item in files:
            target=dest/item.filename
            assert target.resolve().is_relative_to(dest.resolve()), 'unsafe ZIP member'
            raw_member=z.read(item)
            if item.filename!='artifact_manifest.json':
                assert manifest[item.filename]==dict(bytes=len(raw_member),sha256=sha(raw_member)), item.filename
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(raw_member)
    return len(manifest)
def check_packet(root):
    v=root/'native-source-audit-verification-1'
    p=root/'native-source-audit-publication-1'
    r=root/'native-source-audit-review-1'
    vr=json.loads((v/'receipt.json').read_bytes())
    pr=json.loads((p/'receipt.json').read_bytes())
    for receipt in (vr,pr):
        assert receipt['status']=='PASS'
        assert receipt['identity']['source_sha']==receipt['identity']['checkout_sha']==SOURCE
        assert receipt['identity']['controller_sha']==CONTROLLER
        assert receipt['identity']['run_id']==str(RUN)
    assert pr['fresh_replay'] is True
    names=pr['deterministic_files']
    assert names==vr['deterministic_files'] and len(names)==10 and len(set(names))==10
    for name in names: assert (v/name).read_bytes()==(p/name).read_bytes(), name
    assert sha((r/'response.json').read_bytes())=='bbd986bb16622c927bdefdd44d3445ac2f1f5ea7ced4eee380ee94f6f47f1948'
    assert json.loads((r/'result.json').read_bytes())['outcome']=='NO_CANDIDATE'
    return names
def readback(ref):
    rows=(ROOT/'SHA256SUMS').read_text().splitlines()
    for row in rows:
        expected,name=row.split('  ',1)
        raw=subprocess.check_output(['git','show',ref+':'+str(ROOT/name)])
        assert sha(raw)==expected,name
    for name,(_,expected) in EXPECTED.items():
        raw=subprocess.check_output(['git','show',ref+':'+str(ROOT/(name+'.zip'))])
        assert sha(raw)==expected,name
    print(json.dumps(dict(status='PASS',remote_ref=ref,commit=subprocess.check_output(['git','rev-parse',ref],text=True).strip(),verified_files=len(rows),original_zip_count=3,scientific_acceptance=False,native_bridge_status='NOT_DERIVED')))
def main():
    if len(sys.argv)>1 and sys.argv[1]=='readback': return readback(sys.argv[2])
    ROOT.mkdir(parents=True,exist_ok=True)
    base='https://api.github.com/repos/'+os.environ['GITHUB_REPOSITORY']
    headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs): return None
    opener=urllib.request.build_opener(NoRedirect)
    def api(path):
        with opener.open(urllib.request.Request(base+path,headers=headers),timeout=60) as r:return r.read()
    def download(path):
        try:return api(path)
        except urllib.error.HTTPError as e:
            if e.code not in (301,302,303,307,308):raise
            target=e.headers['Location'];assert target.startswith('https://')
            with urllib.request.urlopen(target,timeout=180) as r:return r.read()
    run=json.loads(api('/actions/runs/'+str(RUN)))
    assert run['status']=='completed' and run['conclusion']=='success' and run['head_sha']==CONTROLLER and run['run_attempt']==1
    items=json.loads(api('/actions/runs/'+str(RUN)+'/artifacts?per_page=100'))['artifacts']
    assert len(items)==3 and {a['name'] for a in items}==set(EXPECTED)
    audit=[]
    for item in items:
        name=item['name'];artifact_id,expected=EXPECTED[name]
        assert item['id']==artifact_id and item['digest']=='sha256:'+expected and not item['expired']
        raw=download('/actions/artifacts/'+str(artifact_id)+'/zip')
        assert sha(raw)==expected and len(raw)==item['size_in_bytes']
        (ROOT/(name+'.zip')).write_bytes(raw)
        count=unpack(raw,ROOT/name)
        audit.append(dict(id=artifact_id,name=name,bytes=len(raw),sha256=expected,manifest_members=count))
    deterministic=check_packet(ROOT)
    jobs=json.loads(api('/actions/runs/'+str(RUN)+'/jobs?per_page=100'))['jobs']
    assert {j['name'] for j in jobs}=={'verification','review','publication'} and len(jobs)==3
    logs=[]
    for job in jobs:
        assert job['status']=='completed' and job['conclusion']=='success'
        raw=download('/actions/jobs/'+str(job['id'])+'/logs')
        name='job-'+str(job['id'])+'.log';(ROOT/name).write_bytes(raw)
        logs.append(dict(job_id=job['id'],name=job['name'],file=name,bytes=len(raw),sha256=sha(raw)))
    report=dict(status='ARTIFACT_BYTES_AND_ORIGINAL_FRESH_REPLAY_VERIFIED',original_run=RUN,source_sha=SOURCE,controller_sha=CONTROLLER,archive_run=os.environ['GITHUB_RUN_ID'],archive_controller=os.environ['GITHUB_SHA'],artifacts=audit,job_logs=logs,deterministic_files=deterministic,scientific_acceptance=False,review_disposition='NO_CANDIDATE_WITH_MATERIAL_ERRORS_AND_INCOMPLETE_COVERAGE',native_bridge_status='NOT_DERIVED')
    (ROOT/'DOWNLOAD_AUDIT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    (ROOT/'SHA256SUMS').write_text(''.join(sha(p.read_bytes())+'  '+str(p.relative_to(ROOT))+'\n' for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
    print('Exact original ZIPs, all 85 manifest members, 10 deterministic replay outputs and 3 completed-job logs preserved. No science/model rerun.')
if __name__=='__main__': main()
