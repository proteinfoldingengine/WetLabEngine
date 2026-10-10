"""Authenticate retained publication invocation failure separately from success."""
import pathlib,json,hashlib,zipfile,re
P=pathlib.Path(__file__).parent
D=P/'failed_attempt' if (P/'failed_attempt').exists() else P/'failed-attempt'
O=D/'originals' if (D/'originals').exists() else D
meta=json.loads((D/'metadata.json').read_text());run=meta['run'];jobs=meta['jobs']['jobs'];artifacts=meta['artifacts']['artifacts']
SCIENCE='f7c4b9af140aec9fedb13f505d1edac94269f3df';RUN=38082779963
def sha(b):return hashlib.sha256(b).hexdigest()
assert run['id']==RUN and run['head_sha']==SCIENCE and run['conclusion']=='failure'
assert {j['name']:j['conclusion'] for j in jobs}=={'verification':'success','fresh-reproduction':'success','mathematical-review':'success','publication-audit':'failure'}
assert all(j['run_id']==RUN for j in jobs)
pub=next(j for j in jobs if j['name']=='publication-audit')
assert next(s for s in pub['steps'] if s['name']=='Exact provenance and fresh independent publication gate')['conclusion']=='failure'
assert next(s for s in pub['steps'] if s['name']=='Separate Gemini publication audit')['conclusion']=='skipped'
assert {a['name'] for a in artifacts}=={'c3-private-cover-'+n for n in ['verification','fresh-reproduction','mathematical-review']}
assert all(a['workflow_run']['id']==RUN and a['workflow_run']['head_sha']==SCIENCE for a in artifacts)
archives={};identities={}
for a in artifacts:
 p=O/(a['name']+'.zip');b=p.read_bytes();assert sha(b)==a['digest'].removeprefix('sha256:')
 with zipfile.ZipFile(p) as z:archives[a['name']]={n:z.read(n) for n in z.namelist()}
 identities[p.name]={'bytes':len(b),'sha256':sha(b),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
v=archives['c3-private-cover-verification'];f=archives['c3-private-cover-fresh-reproduction'];m=archives['c3-private-cover-mathematical-review']
assert set(f)==set(v)|{'fresh_independent.json'} and all(f[n]==v[n] for n in v)
assert sha(v['certificate.json'])=='f4dad9a0dba31d85764f3dea65ec2c0325da38d9429ddb6d2ca36e81cb577b48'
assert v['provenance.txt']==f'scientific_sha={SCIENCE}\nworkflow_sha={SCIENCE}\n'.encode()
packet=json.loads((D/'review_inputs.json').read_text());assert packet['scientific_commit']==SCIENCE
current=P/'review_inputs.json' if (P/'review_inputs.json').exists() else P/'review_input_readbacks.json'
assert packet['documents']==json.loads(current.read_text())['documents']
manifest=json.loads(m['manifest.json']);assert set(m)=={'manifest.json','review.txt'}
assert manifest['research_commit']==manifest['workflow_commit']==SCIENCE
assert set(manifest['input_sha256'])==set(packet['documents'])|{'EVIDENCE/'+n for n in f if n!='certificate.json'}
assert len(manifest['input_sha256'])==33
for name,digest in manifest['input_sha256'].items():
 b=f[name[9:]] if name.startswith('EVIDENCE/') else packet['documents'][name].encode();assert sha(b)==digest
assert sha(m['review.txt'])==manifest['response_sha256']
review=json.loads(re.sub(r'^```(?:json)?\s*|\s*```$','',m['review.txt'].decode().strip()).strip())
assert review['verdict']=='ACCEPTED' and not review['missing_assumptions'] and not review['counterexamples']
logs={}
for job in jobs:
 name=job['name'];p=O/(name.replace('-','_')+'_job.log');b=p.read_bytes();t=b.decode()
 assert 'Current runner version:' in t[:200] and f'Complete job name: {name}' in t and SCIENCE in t and 'Cleaning up orphan processes' in t[-3000:]
 if name=='publication-audit':
  assert 'IndexError: list index out of range' in t and 'sys.argv[2]' in t and 'No artifacts will be uploaded' in t
  assert 'Private-cover independent verdict:' not in t
 else:
  a=next(a for a in artifacts if a['name']=='c3-private-cover-'+name)
  assert f"Artifact ID is {a['id']}" in t and f"Artifact c3-private-cover-{name} has been successfully uploaded!" in t
 logs[p.name]={'bytes':len(b),'sha256':sha(b),'job_id':job['id'],'run_id':RUN}
result={'status':'ACCEPTED_RETAINED_FAILURE','run':RUN,'scientific_commit':SCIENCE,'cause':'publication checker output-path argument omitted; IndexError after reconstruction','publication_gemini_review':'NOT_RUN','mathematical_verdict':'ACCEPTED','mathematical_response_sha256':sha(m['review.txt']),'mathematical_attempts':manifest['attempts'],'certificate_unchanged':True,'reviewed_scientific_inputs_unchanged':True,'archives':identities,'complete_logs':logs}
(P/'failed_attempt_reconciliation.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':result['status'],'run':RUN,'publication_review':'NOT_RUN'}))
