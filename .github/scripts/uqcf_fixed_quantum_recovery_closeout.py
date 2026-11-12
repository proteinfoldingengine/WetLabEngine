"""Publication-only final receipt: original four completed job logs; no science/model call."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,urllib.error,urllib.request
REPO='proteinfoldingengine/WetLabEngine'
RUN='42821167329';ATTEMPT='1';WORKFLOW='b60733e069a622ef7923a445b0676eb9a71fef16'
ARCHIVE='524d23353badc8d0b4e6b251dddbf270f5bcac73'
BASE=Path('ResearchHistory/UQCF-GEM/research/physical-bridge/fixed_quantum_recovery_review')
EVIDENCE=BASE/('evidence/run-'+RUN+'-attempt-'+ATTEMPT)
OUT=EVIDENCE/'closeout'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
if len(sys.argv)>1 and sys.argv[1]=='readback':
    manifest=json.loads((OUT/'MANIFEST.json').read_bytes())
    for name,v in manifest.items():
        raw=git('show',sys.argv[2]+':'+str(OUT/name));assert len(raw)==v['bytes'] and sha(raw)==v['sha256']
    raw=git('show',sys.argv[2]+':'+str(OUT/'MANIFEST.json'));assert raw==(OUT/'MANIFEST.json').read_bytes()
    print('All additive closeout bytes match immutable remote commit '+sys.argv[2]);sys.exit(0)
assert os.environ['GITHUB_REPOSITORY']==REPO
OUT.mkdir(parents=True,exist_ok=True)
headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
api_base='https://api.github.com/repos/'+REPO
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
opener=urllib.request.build_opener(NoRedirect)
def api(path):
    with urllib.request.urlopen(urllib.request.Request(api_base+path,headers=headers),timeout=60) as r:return r.read()
def download(path):
    try:
        with opener.open(urllib.request.Request(api_base+path,headers=headers),timeout=60) as r:return r.read()
    except urllib.error.HTTPError as e:
        if e.code not in (301,302,303,307,308):raise
        target=e.headers['Location'];assert target.startswith('https://')
        with urllib.request.urlopen(target,timeout=180) as r:return r.read()
runraw=api('/actions/runs/'+RUN);run=json.loads(runraw)
assert run['head_sha']==WORKFLOW and str(run['run_attempt'])==ATTEMPT
assert run['status']=='completed' and run['conclusion']=='success'
(OUT/'original_run.json').write_bytes(runraw)
jobsraw=api('/actions/runs/'+RUN+'/attempts/'+ATTEMPT+'/jobs?per_page=100');jobs=json.loads(jobsraw)['jobs']
assert len(jobs)==4 and {j['name'] for j in jobs}=={'verification','review','publication','archive'}
(OUT/'original_jobs.json').write_bytes(jobsraw)
prior=json.loads(git('show',ARCHIVE+':'+str(EVIDENCE/'DOWNLOAD_AUDIT.json')))
old_logs={x['id']:x for x in prior['completed_job_logs']};rows=[]
for job in jobs:
    assert job['status']=='completed' and job['conclusion']=='success'
    raw=download('/actions/jobs/'+str(job['id'])+'/logs');name='job-'+str(job['id'])+'.log'
    (OUT/name).write_bytes(raw)
    if job['id'] in old_logs:assert sha(raw)==old_logs[job['id']]['sha256']
    if job['name']=='archive':assert b'Committed original evidence and chunks verified' in raw
    rows.append(dict(id=job['id'],name=job['name'],conclusion=job['conclusion'],file=name,bytes=len(raw),sha256=sha(raw)))
assert git('show',ARCHIVE+':'+str(EVIDENCE/'fixed-quantum-recovery-review-1/response.json'))==(EVIDENCE/'fixed-quantum-recovery-review-1/response.json').read_bytes()
write('CLOSEOUT.json',dict(status='PASS',scope='Publication-only additive original-run log preservation; no model call or scientific execution',original_run_id=RUN,original_run_attempt=ATTEMPT,scientific_sha='02f6504bb4fe026557fbcef97fb12cc0775c82d9',original_workflow_checkout_sha=WORKFLOW,source_archive_sha=ARCHIVE,source_archive_manifest_sha256=sha(git('show',ARCHIVE+':'+str(EVIDENCE/'SHA256SUMS'))),source_archive_readback_confirmed_in_completed_log=True,completed_original_job_logs=rows,closeout_run_id=os.environ['GITHUB_RUN_ID'],closeout_attempt=os.environ['GITHUB_RUN_ATTEMPT'],closeout_checkout_sha=os.environ['GITHUB_SHA'],native_bridge='NOT_DERIVED'))
write('MANIFEST.json',{p.name:dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='MANIFEST.json'})
print('Original run and all four completed logs preserved. No Gemini or scientific run.')
