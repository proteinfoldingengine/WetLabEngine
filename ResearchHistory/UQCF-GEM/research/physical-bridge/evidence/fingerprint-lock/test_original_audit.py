"""Adversarial archive-audit controls; separate from the 312 scientific tests."""
import pathlib,tempfile,shutil,subprocess,json,hashlib,zipfile,re
P=pathlib.Path(__file__).parent;O=P/'originals' if (P/'originals').exists() else P

def sha(b):return hashlib.sha256(b).hexdigest()
def edit_json(p,fn):
 d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d)+'\n')
def edit_zip(root,name,fn):
 p=root/(name+'.zip')
 with zipfile.ZipFile(p) as z:d={n:z.read(n) for n in z.namelist()}
 fn(d)
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
  for n,b in d.items():z.writestr(n,b)
 def metadata(d):
  a=next(a for a in d['artifacts'] if a['name']==name);a['digest']='sha256:'+sha(p.read_bytes());a['size_in_bytes']=p.stat().st_size
 edit_json(root/'artifact_metadata.json',metadata)
def missing_input(root):
 def mutate(d):
  m=json.loads(d['manifest.json']);m['input_sha256'].pop('EVIDENCE/red.log');d['manifest.json']=json.dumps(m).encode()
 edit_zip(root,'c3-fingerprint-lock-mathematical-review',mutate)
def truncated_log(root):
 p=root/'verification_job.log';b=p.read_bytes();p.write_bytes(b[:b.rfind(b'Cleaning up orphan processes')-150])
 def update(d):
  a=next(a for a in d if a['job_name']=='verification');a['bytes']=p.stat().st_size;a['sha256']=sha(p.read_bytes())
 edit_json(root/'job_log_sources.json',update)
def wrong_run(root):edit_json(root/'run_metadata.json',lambda d:d.update(id=0))
def compensated_counts(root):
 def mutate(d):
  d['contracts.log']=d['contracts.log'].replace(b'Ran 33 tests',b'Ran 34 tests');d['inherited_fixed_family.log']=d['inherited_fixed_family.log'].replace(b'Ran 28 tests',b'Ran 27 tests')
 for name in ['verification','fresh-reproduction']:edit_zip(root,'c3-fingerprint-lock-'+name,mutate)
def missing_member(root):
 for name in ['verification','fresh-reproduction']:edit_zip(root,'c3-fingerprint-lock-'+name,lambda d:d.pop('independent.log'))
def missing_identities(root):
 for name in ['verification','fresh-reproduction']:edit_zip(root,'c3-fingerprint-lock-'+name,lambda d:d.pop('certificate.json.identities.jsonl.gz'))
def wrong_job(root):edit_json(root/'job_log_sources.json',lambda d:d[0].update(job_id=0))
controls=[('missing_review_input',missing_input,'expected_inputs'),('truncated_complete_log',truncated_log,'Cleaning up orphan processes'),('wrong_run_identity',wrong_run,"runmeta['id']"),('compensating_test_counts',compensated_counts,'test_counts==TESTS'),('omitted_archive_member',missing_member,'set(verification)==VERIFICATION'),('omitted_canonical_identity_archive',missing_identities,'set(verification)==VERIFICATION'),('wrong_job_binding',wrong_job,"item['job_id']==job['id']")]
results=[]
for name,mutation,expected in [('intact',None,None)]+controls:
 with tempfile.TemporaryDirectory() as td:
  root=pathlib.Path(td)
  for f in O.iterdir():
   if f.is_file():shutil.copyfile(f,root/f.name)
  shutil.copyfile(P/'audit_originals.py',root/'audit_originals.py')
  shutil.copyfile(P/'binding.json',root/'binding.json')
  readback=P/'review_inputs.json' if (P/'review_inputs.json').exists() else P/'review_input_readbacks.json';shutil.copyfile(readback,root/'review_input_readbacks.json')
  if mutation:mutation(root)
  p=subprocess.run(['python3',str(root/'audit_originals.py')],capture_output=True,text=True)
  if mutation:assert p.returncode!=0 and expected in p.stderr,(name,p.returncode,p.stderr)
  else:assert p.returncode==0,p.stderr
  results.append({'control':name,'exit_code':p.returncode,'expected_gate':expected,'status':'REJECTED_AS_REQUIRED' if mutation else 'ACCEPTED'})
out={'status':'ACCEPTED','scientific_tests_not_incremented':312,'controls':results};(P/'author_audit_controls.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
