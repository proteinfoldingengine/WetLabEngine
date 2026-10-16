"""Independent immutable evidence publication readback; no science execution.
Run beside FINAL_RAW.zip and the published attempt-2 evidence/audit files.
"""
import base64, hashlib, io, json, stat, zipfile
from pathlib import Path
OUT=Path(__file__).resolve().parent
SHA='ffa6017c232525bc3f87476dfa393128e3129857'
PARENT='1dc576e1476e9a91ce84db6d54061e3353fb14ce'
BASE='ResearchHistory/UQCF-GEM/research/physical-bridge/history_orientation/resume_20261016/'
CONT='ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md'
def parse(b):
 def uniq(rows):
  d={}
  for k,v in rows:
   if k in d:raise ValueError('duplicate JSON key')
   d[k]=v
  return d
 def reject(v):raise ValueError('nonfinite JSON')
 return json.loads(b,object_pairs_hook=uniq,parse_constant=reject)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def content(r):
 o=r['result']['structuredContent']
 if o.get('encoding')=='base64':return base64.b64decode(''.join(o['content'].split()),validate=True)
 return o['content'].encode()
def safe(z):
 n=z.namelist();assert len(n)==len(set(n));assert all(not Path(x).is_absolute() and '..' not in Path(x).parts and str(Path(x))==x for x in n)
 assert not any(stat.S_ISLNK(x.external_attr>>16) for x in z.infolist());return set(n)
if not __debug__:raise SystemExit('Assertions must be enabled')
with zipfile.ZipFile(OUT/'FINAL_RAW.zip') as z:
 names=safe(z);seal=parse(z.read('file_manifest.json'));assert names==set(seal)|{'file_manifest.json'}
 for n,e in seal.items():assert e==ident(z.read(n))
 raw={n:parse(z.read(n)) for n in seal}
commit,comparison=[parse(r['structuredContent']['content']) for r in raw['metadata_connector.json']]
assert commit['sha']==SHA and [p['sha'] for p in commit['parents']]==[PARENT]
assert commit['commit']['tree']['sha']=='9b7fea1d79106d294b82977d57175490c5aead3e'
assert commit['author']['login']==commit['committer']['login']=='proteinfolding-gpt'
assert comparison['status']=='ahead' and comparison['ahead_by']==comparison['total_commits']==1 and comparison['behind_by']==0
changes={f['filename']:f for f in comparison['files']};assert len(changes)==17
assert {p for p,f in changes.items() if f['status']=='modified'}=={CONT}
assert sum(f['status']=='added' for f in changes.values())==16
rows=[r for r in raw['blobs_connector.json'] if not r['result'].get('isError')]+raw['binary_readback_connector.json']
assert len(rows)==17 and {r['path'] for r in rows}==set(changes)
files={r['path']:content(r) for r in rows}
for r in rows:
 d=ident(files[r['path']]);assert d['git_blob']==r['blob_sha']==changes[r['path']]['sha']
 if r['path'].endswith('.zip'):assert d['git_blob']==r['result']['structuredContent']['sha']
manifest=parse(files[BASE+'MANIFEST.json']);assert set(manifest['files'])==set(changes)-{BASE+'MANIFEST.json'}
assert manifest['parent_commit']==PARENT and manifest['run_id']==38927950314 and manifest['run_attempt']==2
assert manifest['status']=='REVIEW_BLOCKED_HTTP429'
for p,e in manifest['files'].items():assert ident(files[p])==e
parent=raw['parent_continuation_connector.json']['structuredContent']['content'].encode()
assert len(parent)==93602 and files[CONT].startswith(parent) and len(files[CONT])-len(parent)==1127
with zipfile.ZipFile(io.BytesIO(files[BASE+'AUDIT_RAW.zip'])) as z:
 safe(z);prior_source=parse(z.read('source_connector.json'));prior_seal=parse(z.read('file_manifest.json'))
 for n,e in prior_seal.items():assert ident(z.read(n))==e
 frozen={(r['ref'],r['path']):r['result']['structuredContent']['content'].encode() for r in prior_source}
assert len(raw['frozen_readback_connector.json'])==14
for r in raw['frozen_readback_connector.json']:
 b=content(r);assert b==frozen[('a42ca9e248c438081f31dcaba2ba5c6ffb36cec0',r['path'])];assert ident(b)['git_blob']==r['result']['structuredContent']['sha']
audit=parse(files[BASE+'AUDIT.json']);assert audit['status']=='EVIDENCE_INTEGRITY_PASS' and audit['scientific_status']=='REVIEW_BLOCKED_HTTP429' and audit['gemini_acceptance'] is False
for a in audit['artifacts']:
 b=files[BASE+'evidence/'+a['name']+'.zip'];assert ident(b)=={k:a[k] for k in ['bytes','sha256','git_blob']}
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  names=safe(z);m=parse(z.read('file_manifest.json'));assert names==set(m)|{'file_manifest.json'}
  for n,e in m.items():assert e=={k:ident(z.read(n))[k] for k in ['bytes','sha256']}
  if a['name']=='history-review-2':
   assert not names & {'response.json','review.txt','verdict.json'}
   for n in ['infrastructure_failure.json','model_availability.json','provenance.json']:assert z.read(n)==files[BASE+'evidence/'+n]
for l in audit['logs']:assert ident(files[BASE+'evidence/'+l['name']+'.log'])=={k:l[k] for k in ['bytes','sha256','git_blob']}
report={'status':'PUBLICATION_INTEGRITY_PASS','evidence_commit':SHA,'tree_sha':commit['commit']['tree']['sha'],'parent_commit':PARENT,'author':commit['author']['login'],'committer':commit['committer']['login'],'changed_paths':17,'added_paths':16,'modified_paths':[CONT],'manifest_bound_files':16,'all_changed_bytes_independently_read':True,'binary_archives_fully_decoded_and_hashed':3,'original_actions_archives':2,'complete_job_logs':2,'frozen_source_and_manifest_paths_unchanged':14,'continuation_append_only':True,'continuation_parent_bytes':93602,'continuation_append_bytes':1127,'scientific_status':'REVIEW_BLOCKED_HTTP429','gemini_acceptance':False,'native_milestone':'OPEN','science_executed':False,'external_writes_by_auditor':False,'checked':[{'path':p,**ident(b)} for p,b in sorted(files.items())],'scope':'Independent immutable publication-byte and provenance audit, not mathematical review or native-mechanism/numbered-stage closure.'}
(OUT/'FINAL_AUDIT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('PASS: 17 immutable changed files, 16 manifest entries, 3 decoded ZIPs, 14 frozen inputs, bot authorship and append-only continuation. REVIEW_BLOCKED_HTTP429.')
