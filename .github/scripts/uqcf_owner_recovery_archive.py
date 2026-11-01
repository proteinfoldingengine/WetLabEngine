"""Preserve original and recovery bytes, including the original schema failure."""
import hashlib,io,json,os,urllib.error,urllib.request,zipfile
from pathlib import Path
repo=os.environ['GITHUB_REPOSITORY']; recovery=os.environ['GITHUB_RUN_ID']; head=os.environ['GITHUB_SHA']
original='41322904153'; oldhead='a17595036ca21c435a9061ad844d92dd88d0a000'
root=Path('ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_delivery_owner_scope/evidence')/('recovery-'+recovery)
root.mkdir(parents=True,exist_ok=True)
headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
base='https://api.github.com/repos/'+repo
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
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
def sha(b):return hashlib.sha256(b).hexdigest()
receipts=[];jobs_all=[];records={};limit=40*1024*1024
for run,expected,expected_head in [(original,{'owner-scope-integrity-1','owner-scope-stack-1','owner-scope-review-1'},oldhead),(recovery,{'owner-recovery-publication','owner-recovery-replay'},head)]:
 listing=json.loads(api('/actions/runs/'+run+'/artifacts?per_page=100'))
 items=listing['artifacts'];assert {x['name'] for x in items}==expected and len(items)==len(expected)
 for item in items:
  assert str(item['workflow_run']['id'])==run and item['workflow_run']['head_sha']==expected_head
  raw=download('/actions/artifacts/'+str(item['id'])+'/zip');assert item['digest']=='sha256:'+sha(raw) and not item['expired']
  name=item['name']; dest=root/name;dest.mkdir();parts=[]
  for i,start in enumerate(range(0,len(raw),limit)):
   chunk=raw[start:start+limit]; fn=name+'.zip.part%03d'%i;(root/fn).write_bytes(chunk);parts.append(dict(file=fn,bytes=len(chunk),sha256=sha(chunk)))
  assert sha(b''.join((root[x['file']]).read_bytes() for x in parts))==sha(raw)
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   names=z.namelist();assert len(names)==len(set(names))
   assert 'artifact_manifest.json' in names
   manifest=json.loads(z.read('artifact_manifest.json'))
   assert set(names)==set(manifest)|{'artifact_manifest.json'}
   refs=[]
   for n in names:
    assert (dest/n).resolve().is_relative_to(dest.resolve())
    data=z.read(n)
    if n!='artifact_manifest.json':assert manifest[n]==dict(bytes=len(data),sha256=sha(data))
    if len(data)<=limit:
     (dest/n).parent.mkdir(parents=True,exist_ok=True);(dest/n).write_bytes(data)
    else:refs.append(dict(member=n,bytes=len(data),sha256=sha(data),container_parts=[p['file'] for p in parts]))
    if n in ('receipt.json','publication.json','verdict.json','review_identity.json'):records[(name,n)]=json.loads(data)
   if refs:(dest/'LARGE_MEMBER_REFERENCES.json').write_text(json.dumps(refs,indent=2)+'\n')
  receipts.append(dict(run_id=run,id=item['id'],name=name,zip_bytes=len(raw),api_digest=item['digest'],download_sha256=sha(raw),parts=parts,member_count=len(names)))
 jobs=json.loads(api('/actions/runs/'+run+'/jobs?per_page=100'))['jobs']
 expected_outcomes={'verification':'success','argument-review':'failure','publication-audit':'skipped','durable-archive':'skipped'} if run==original else {'publication-recovery':'success'}
 for jobname,outcome in expected_outcomes.items():
  matches=[j for j in jobs if j['name']==jobname];assert len(matches)==1 and matches[0]['conclusion']==outcome
 for j in jobs:
  if j['status']=='completed' and j['conclusion']!='skipped':
   log=download('/actions/jobs/'+str(j['id'])+'/logs');fn='job-'+str(j['id'])+'.log';(root/fn).write_bytes(log)
   jobs_all.append(dict(run_id=run,id=j['id'],name=j['name'],conclusion=j['conclusion'],file=fn,sha256=sha(log)))
 (root/('jobs-'+run+'.json')).write_text(json.dumps(jobs,indent=2)+'\n')
v=records[('owner-scope-review-1','verdict.json')]
assert v['verdict']=='ACCEPTED' and all(v[k]==[] for k in ['findings','missing_assumptions','counterexamples']) and v['native_bridge_status']=='NOT_DERIVED'
a=records[('owner-recovery-publication','publication.json')]
assert a['status']=='PASS' and a['checkout_sha']==oldhead and a['run_id']==original and a['auditor_run_id']==recovery and a['auditor_checkout_sha']==head
for artifact,run,sha_head in [('owner-scope-stack-1',original,oldhead),('owner-recovery-replay',recovery,head)]:
 r=records[(artifact,'receipt.json')];assert r['status']=='PASS' and r['run_id']==run and r['checkout_sha']==sha_head
(root/'DOWNLOAD_AUDIT.json').write_text(json.dumps(dict(status='PASS',original_run=original,recovery_run=recovery,auditor_head=head,artifacts=receipts,completed_job_logs=jobs_all,native_bridge='NOT_DERIVED'),indent=2,sort_keys=True)+'\n')
(root/'SHA256SUMS').write_text(''.join(sha(f.read_bytes())+'  '+str(f.relative_to(root))+'\n' for f in sorted(root.rglob('*')) if f.is_file() and f.name!='SHA256SUMS'))
print('All original artifact digests, members, split reconstruction and exact run outcomes verified.')
print(str(root))
