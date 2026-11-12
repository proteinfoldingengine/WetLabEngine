"""Read published Git evidence independently; run from repository root."""
import ast,hashlib,io,json,subprocess,sys,zipfile
from pathlib import Path
repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
base=repo/'ResearchHistory/UQCF-GEM/research/physical-bridge/rd8_correction_review'
run=sys.argv[1];root=base/'evidence'/('run-'+run+'-attempt-1')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(p,ref):return subprocess.check_output(['git','show',ref+':'+p],cwd=repo)
receipt=json.loads((root/'DOWNLOAD_AUDIT.json').read_bytes());assert receipt['status']=='PASS' and receipt['run_id']==run
head=receipt['checkout_sha'];freeze='5c4fba4b5601a386ab196d1e551173a5a0d77199'
files={}
for line in (root/'SHA256SUMS').read_text().splitlines():
 digest,p=line.split('  ',1);assert sha((root/p).read_bytes())==digest;files[p]=digest
assert set(files)=={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='SHA256SUMS'}
zs={};members=0
for a in receipt['artifacts']:
 data=(root/(a['name']+'.zip')).read_bytes();assert len(data)==a['zip_bytes'] and sha(data)==a['download_sha256'] and a['api_digest']=='sha256:'+sha(data)
 z=zipfile.ZipFile(io.BytesIO(data));m=json.loads(z.read('artifact_manifest.json'));assert set(z.namelist())==set(m)|{'artifact_manifest.json'}
 for n,v in m.items():
  b=z.read(n);assert sha(b)==v['sha256'] and len(b)==v['bytes'];assert b==(root/a['name']/n).read_bytes();members+=1
 zs[a['name']]=z
review=zs['rd8-correction-review-1'];original=zs['rd8-correction-stack-1'];replay=zs['rd8-correction-replay-1'];pub=zs['rd8-correction-publication-1']
outputs=['certificates.json.xz','PRODUCTION.json','VERIFICATION.json','REPRODUCED_1615F.json']
for n in outputs:assert original.read(n)==replay.read(n)
for z in [original,replay]:
 r=json.loads(z.read('receipt.json'));assert r['status']=='PASS' and r['checkout_sha']==head and r['run_id']==run and all(x['exit_code']==0 for x in r['commands'])
assert json.loads(pub.read('publication.json'))['status']=='PASS'
ri=json.loads(review.read('review_identity.json'));assert ri['checkout_sha']==head and ri['run_id']==run and ri['scientific_sha']==freeze
names=['DERIVATION.md','SOURCE_PACKET.json','REVIEW_PLAN.md','FREEZE.json'];docs={n:(base/n).read_bytes() for n in names}
for n,b in docs.items():assert b==git(str((base/n).relative_to(repo)),freeze)
f=json.loads(docs['FREEZE.json']);assert f['documents']=={n:sha(b) for n,b in docs.items() if n!='FREEZE.json'}
p=json.loads(docs['SOURCE_PACKET.json'])
for s in p['sources']:
 b=git(s['path'],s.get('source_commit',p['source_commit']));assert sha(b)==s['full_sha256'] and len(b)==s['full_bytes'];assert b[s['byte_start']:s['byte_end']]==s['content'].encode();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['git_blob']
tree=ast.parse(git('.github/scripts/uqcf_rd8_review.py',head));header=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HEADER' for t in n.targets))
prompt=header.encode()
for n in names:prompt+=('\nEXACT DOCUMENT '+n+'\nUTF8-BYTES '+str(len(docs[n]))+'\n').encode()+docs[n]+b'\nEND EXACT DOCUMENT\n'
assert prompt==review.read('prompt.txt') and sha(prompt)==ri['prompt_sha256']
request={'contents':[{'role':'user','parts':[{'text':prompt.decode()}]}],'generationConfig':{'temperature':0,'maxOutputTokens':32768,'responseMimeType':'application/json'}}
assert (json.dumps(request,ensure_ascii=False,sort_keys=True)+'\n').encode()==review.read('request.json')
raw=review.read('response.json');assert sha(raw)==ri['response_sha256'];response=json.loads(raw);assert response['modelVersion']=='gemini-3.1-pro-preview' and len(response['candidates'])==1 and response['candidates'][0]['finishReason']=='STOP' and not response.get('promptFeedback',{}).get('blockReason')
answer='\n'.join(p['text'] for p in response['candidates'][0]['content']['parts'] if not p.get('thought',False) and isinstance(p.get('text'),str)).strip().encode();assert answer==review.read('review.txt')
v=json.loads(answer);assert v==json.loads(review.read('verdict.json'));assert v['verdict']=='ACCEPTED' and all(v[k]==[] for k in ['findings','missing_assumptions','counterexamples']) and v['native_bridge_status']=='NOT_DERIVED'
snapshot=zipfile.ZipFile(io.BytesIO(original.read('source-snapshot.zip')));assert snapshot.comment.decode()==head
for name in snapshot.namelist():
 if not name.endswith('/'):assert snapshot.read(name)==git(name,head)
ver=json.loads(original.read('VERIFICATION.json'));assert ver['all_valid'] and all(x['rejected'] for x in ver['deliberate_defects'])
supplement=base/'publication/source_supplement'
sm=json.loads((supplement/'MANIFEST.json').read_bytes());sb=(supplement/'uqcf_preparability_integrity.py').read_bytes()
assert sm['source_commit']==head and sb==git(sm['path'],head) and sha(sb)==sm['sha256'] and len(sb)==sm['bytes']
assert hashlib.sha1(b'blob '+str(len(sb)).encode()+b'\0'+sb).hexdigest()==sm['git_blob']
result=dict(status='PASS',supplemental_import_verified=True,run_id=run,execution_sha=head,scientific_freeze=freeze,readback_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),zip_artifacts=len(zs),member_checks=members,stored_file_checks=len(files),source_documents=len(p['sources']),snapshot_members=len(snapshot.namelist()),raw_response_sha256=sha(raw),verdict=v['verdict'],model=response['modelVersion'],exact_output_hashes={n:sha(original.read(n)) for n in outputs},native_bridge='NOT_DERIVED')
print(json.dumps(result,indent=2,sort_keys=True))
if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
