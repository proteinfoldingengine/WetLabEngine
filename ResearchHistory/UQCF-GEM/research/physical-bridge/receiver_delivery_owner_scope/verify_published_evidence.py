from pathlib import Path
import hashlib,io,json,zipfile,subprocess,sys
repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip());base=repo/'ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_delivery_owner_scope'
run=sys.argv[1];root=base/'evidence'/('recovery-'+run)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(path,ref='HEAD'):return subprocess.check_output(['git','show',ref+':'+path],cwd=repo)
checks=0
for line in (root/'SHA256SUMS').read_text().splitlines():
 digest,name=line.split('  ',1);assert sha((root/name).read_bytes())==digest;checks+=1
receipt=json.loads((root/'DOWNLOAD_AUDIT.json').read_bytes());assert receipt['status']=='PASS'
artifacts={};count=0
for a in receipt['artifacts']:
 chunks=[]
 for part in a['parts']:
  b=(root/part['file']).read_bytes();assert len(b)==part['bytes'] and sha(b)==part['sha256'];chunks.append(b)
 b=b''.join(chunks);assert sha(b)==a['download_sha256'] and a['api_digest']=='sha256:'+sha(b) and len(b)==a['zip_bytes']
 z=zipfile.ZipFile(io.BytesIO(b));manifest=json.loads(z.read('artifact_manifest.json'));assert set(z.namelist())==set(manifest)|{'artifact_manifest.json'}
 for n,v in manifest.items():
  data=z.read(n);assert len(data)==v['bytes'] and sha(data)==v['sha256'];count+=1
  expanded=root/a['run_id']/a['name']/n
  if expanded.exists():assert expanded.read_bytes()==data
 artifacts[(a['run_id'],a['name'])]=z
orig=artifacts[('41322904153','owner-scope-stack-1')];fresh=artifacts[(run,'owner-recovery-replay')];failed=artifacts[('41323575062','owner-recovery-replay')]
outputs=['certificates.json.xz','PRODUCTION.json','VERIFICATION.json','REPRODUCED_1615F.json']
for n in outputs:assert orig.read(n)==fresh.read(n)
a=json.loads(orig.read('REPRODUCED_1615F.json'));b=json.loads(failed.read('REPRODUCED_1615F.json'));oldid=a.pop('execution_head');newid=b.pop('execution_head');assert a==b and oldid=='a17595036ca21c435a9061ad844d92dd88d0a000' and newid=='cf796b98f9605f4f6145d072937be3c0f76f0d9a'
snapshot=zipfile.ZipFile(io.BytesIO(orig.read('source-snapshot.zip')));assert snapshot.comment.decode()==oldid
for n in ['DERIVATION.md','SOURCE_PACKET.json','REVIEW_PLAN.md','FREEZE.json']:
 path=str((base/n).relative_to(repo));assert snapshot.read(path)==git(path)==git(path,'a7cc94aa8ba05ca64f0342fe23a90df8cdbbb2b4')
packet=json.loads((base/'SOURCE_PACKET.json').read_bytes())
for s in packet['sources']:
 data=git(s['path'],packet['source_commit']);assert sha(data)==s['full_sha256'] and data==s['content'].encode() and len(data)==s['full_bytes']
review=artifacts[('41322904153','owner-scope-review-1')];v=json.loads(review.read('verdict.json'));response=json.loads(review.read('response.json'))
assert response['modelVersion']=='gemini-3.1-pro-preview' and response['candidates'][0]['finishReason']=='STOP'
answer='\n'.join(p['text'] for p in response['candidates'][0]['content']['parts'] if not p.get('thought',False) and isinstance(p.get('text'),str)).strip().encode();assert answer==review.read('review.txt') and json.loads(answer)==v
assert v['verdict']=='ACCEPTED' and all(v[k]==[] for k in ['findings','missing_assumptions','counterexamples']) and v['native_bridge_status']=='NOT_DERIVED'
verification=json.loads(orig.read('VERIFICATION.json'));assert verification['all_valid'] and all(x['rejected'] for x in verification['deliberate_defects'])
result=dict(status='PASS',readback_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),recovery_run=run,files_hash_checked=checks,original_zip_artifacts=len(artifacts),manifest_members_checked=count,complete_source_documents=6,source_snapshot_commit=oldid,exact_reproduced_outputs={n:sha(orig.read(n)) for n in outputs},failed_replay_difference='execution_head only; all other parsed fields identical',raw_gemini_response_sha256=sha(review.read('response.json')),model=response['modelVersion'],verdict=v['verdict'],defect_count=0,coverage=verification['coverage'],rejecting_controls=len(verification['deliberate_defects']),native_bridge='NOT_DERIVED')
print(json.dumps(result,indent=2,sort_keys=True))
for name in ['fcv-tests.log','parent-tests.log','historical-tests.log']:
 print(name,orig.read(name).decode()[-1200:])
