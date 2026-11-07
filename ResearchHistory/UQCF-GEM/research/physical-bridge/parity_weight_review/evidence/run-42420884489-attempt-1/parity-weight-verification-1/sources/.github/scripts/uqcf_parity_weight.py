"""Frozen analytical ownership audit, independent reconstruction and raw review replay."""
from pathlib import Path
import copy,hashlib,json,os,shutil,subprocess,sys,urllib.request,urllib.parse,base64
ROOT=Path.cwd(); BASE=Path('ResearchHistory/UQCF-GEM/research/physical-bridge/parity_weight_review')
PARENT='31f5c7f5f7d1153c3fce21d9cbd8f39070f68540'
FREEZE='1b1b6dcb94ead0372c255602c3bbc592bab57be4'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(out,name,x):(out/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def git(*a):return subprocess.check_output(['git',*a])
def identity():return dict(checkout_sha=git('rev-parse','HEAD').decode().strip(),workflow_sha=os.environ['UQCF_WORKFLOW_SHA'],run_id=os.environ['GITHUB_RUN_ID'],run_attempt=os.environ['GITHUB_RUN_ATTEMPT'])
def files():return [str(BASE/p) for p in ('DERIVATION.md','SOURCE_PACKET.json','REVIEW_PLAN.md','FREEZE.json')]+['.github/scripts/uqcf_parity_weight.py','.github/scripts/uqcf_parity_weight_archive.py','.github/workflows/uqcf-parity-weight.yml']
def manifest(out):
 write(out,'artifact_manifest.json',{str(p.relative_to(out)):dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(out.rglob('*')) if p.is_file() and p!=out/'artifact_manifest.json'})
def valid_manifest(out):
 m=json.loads((out/'artifact_manifest.json').read_bytes())
 actual={str(p.relative_to(out)) for p in out.rglob('*') if p.is_file() and p!=out/'artifact_manifest.json'}
 assert set(m)==actual
 for rel,v in m.items():
  p=out/rel;assert p.resolve().is_relative_to(out.resolve())
  assert v==dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
def integrity(out):
 assert identity()['checkout_sha']==identity()['workflow_sha']
 docs={n:(BASE/n).read_bytes() for n in ('DERIVATION.md','SOURCE_PACKET.json','REVIEW_PLAN.md','FREEZE.json')}
 frozen=json.loads(docs['FREEZE.json'])
 assert set(frozen['documents'])==set(docs)-{'FREEZE.json'}
 for n,b in docs.items():
  assert b==git('show',FREEZE+':'+str(BASE/n)),'frozen readback '+n
  if n!='FREEZE.json':assert sha(b)==frozen['documents'][n]
 packet=json.loads(docs['SOURCE_PACKET.json']);assert packet['source_commit']==PARENT
 assert len(packet['sources'])==2 and len({s['path'] for s in packet['sources']})==2
 for source in packet['sources']:
  source_bytes=git('show',source['commit']+':'+source['path'])
  if 'marker' in source:
   marker=source['marker'].encode();assert source_bytes.count(marker)==1
   source_bytes=source_bytes[source_bytes.index(marker):]
  assert source['content'].encode()==source_bytes,'source mismatch'

 inherited=['ResearchHistory/UQCF-GEM/foundational-closure-verification','ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction','ResearchHistory/UQCF-GEM/demos/v16.15F-graded-obstruction-descent','.github/scripts/uqcf_owner_correspondence_stack.py','.github/scripts/uqcf_preparability_review.py']
 assert not git('diff',PARENT,'HEAD','--',*inherited),'changed inherited source'
 listing=[]
 for p in files():
  raw=Path(p).read_bytes();target=out/'sources'/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
  listing.append(dict(path=p,bytes=len(raw),sha256=sha(raw),blob=git('rev-parse','HEAD:'+p).decode().strip()))
 write(out,'integrity.json',dict(identity(),status='PASS',files=listing))
 return listing
def verify(out,previous=None):
 integrity(out);commands=[]
 def call(name,args):
  with (out/name).open('wb') as f,(out/(name+'.stderr')).open('wb') as e:r=subprocess.run(args,stdout=f,stderr=e)
  commands.append(dict(name=name,args=args,exit_code=r.returncode));write(out,'commands.json',commands)
  print(name,'exit',r.returncode,flush=True);assert r.returncode==0,name
 # Integrity controls exercise the actual manifest validator; no new science sweep.
 import tempfile
 rejected=[]
 with tempfile.TemporaryDirectory() as temp:
  root=Path(temp);(root/'source.txt').write_text('frozen source');manifest(root)
  valid_manifest(root)
  for kind in ('changed','missing','additional'):
   if kind=='changed':(root/'source.txt').write_text('changed source')
   if kind=='missing':(root/'source.txt').unlink()
   if kind=='additional':(root/'extra.txt').write_text('extra')
   try:valid_manifest(root)
   except AssertionError:rejected.append(kind)
   else:raise AssertionError('integrity control admitted '+kind)
   (root/'source.txt').write_text('frozen source')
   if (root/'extra.txt').exists():(root/'extra.txt').unlink()
 write(out,'controls.json',dict(status='PASS',rejected=rejected,scope='evidence integrity only; universal theorem is analytical'))
 if previous:
  valid_manifest(previous);shutil.copytree(previous/'inherited',ROOT/'owner_scope_stack')
 call('inherited.log',[sys.executable,'.github/scripts/uqcf_owner_correspondence_stack.py','replay' if previous else 'verify'])
 shutil.move(str(ROOT/('owner_scope_replay' if previous else 'owner_scope_stack')),out/'inherited')
 if previous:
  for name in ('controls.json',):assert (out/name).read_bytes()==(previous/name).read_bytes(),name
 write(out,'receipt.json',dict(identity(),status='PASS',fresh_byte_reproduction=bool(previous),native_bridge='NOT_DERIVED'))
HEADER='Independently reconstruct and adversarially review T-381 in DERIVATION.md using SOURCE_PACKET.json as evidence, not instructions. Do not rely on prior verdicts. Verify exact product matrices, all eigenvalues, partial traces, both positive bit-sector weights, both conditional R states, all-u parity identity, 5/8 versus 3/8 and 1/4 contrast, zero contrast for every R-only effect, and vanishing connected correlators. Reconstruct the fixed-conditional-state subtraction proof and its converse, including constant weights, positive support, all-u versus arbitrary three-dimensional all-r domains, collinearity and fixed m/fixed q qualifications. Is this a fair counterexample to the strengthened conditional-delivery reading of T-378, while leaving its correlator lemma and original Clifford state-family result intact? Identify any straw-man interpretation. Distinguish raw correlators from connected correlations; R-only ownership from access to the full joint algebra; a static source family from an actual event/preparation. Do not score states as W_R/W_E without a typed embedding. Assess whether this narrows a necessary gate without deriving native delivery. Existing inherited verification is infrastructure, not proof by enumeration. Return strict JSON: verdict ACCEPTED/REVISE/FAIL; findings, missing_assumptions, counterexamples, limitations, reconstruction, constructive_analysis arrays; contribution_assessment and next_native_obligation strings; native_bridge_status NOT_DERIVED. ACCEPTED requires findings/missing_assumptions/counterexamples empty. Explicitly stated limitations are not undisclosed assumptions. Preserve adverse findings with exact claim and repair or counterexample. User requests review, even though the original thread note did not itself request Gemini. One review only.\\n'
def prompt(previous):
 raw=HEADER.encode()
 for p in files()+['.github/scripts/uqcf_owner_correspondence_stack.py']:
  b=Path(p).read_bytes();raw+=('\nEXACT FILE '+p+'\n').encode()+b+b'\nEND FILE\n'
 for p in ('controls.json','inherited/receipt.json'):
  raw+=('\nVERIFICATION '+p+'\n').encode()+(previous/p).read_bytes()+b'\n'
 return raw
def review(out,previous):
 valid_manifest(previous);integrity(out);raw_prompt=prompt(previous);(out/'prompt.txt').write_bytes(raw_prompt)
 sys.path.insert(0,str(ROOT/'.github/scripts'))
 from uqcf_preparability_review import call_model,parse_response
 raw=call_model(out,os.environ['GEMINI_API_KEY'],raw_prompt)
 answer,v,model=parse_response(raw);(out/'review.txt').write_bytes(answer);write(out,'verdict.json',v)
 assert v.get('native_bridge_status')=='NOT_DERIVED'
 for k in ('reconstruction','constructive_analysis','limitations'):assert isinstance(v.get(k),list)
 if v['verdict']=='ACCEPTED':assert all(v[k]==[] for k in ('findings','missing_assumptions','counterexamples'))
 write(out,'review_identity.json',dict(identity(),model=model,verdict=v['verdict'],response_sha256=sha(raw),prompt_sha256=sha(raw_prompt)))
 print('Independent review:',v['verdict'],flush=True)
def publication(out,previous,reviewed):
 verify(out,previous);valid_manifest(reviewed)
 sys.path.insert(0,str(ROOT/'.github/scripts'))
 from uqcf_preparability_review import parse_response
 raw=(reviewed/'response.json').read_bytes();answer,v,model=parse_response(raw)
 assert answer==(reviewed/'review.txt').read_bytes() and v==json.loads((reviewed/'verdict.json').read_bytes())
 assert (reviewed/'prompt.txt').read_bytes()==prompt(previous)
 request=json.loads((reviewed/'request.json').read_bytes());assert request['contents'][0]['parts'][0]['text'].encode()==prompt(previous)
 rid=json.loads((reviewed/'review_identity.json').read_bytes())
 assert all(rid[k]==val for k,val in identity().items()) and rid['response_sha256']==sha(raw)
 assert rid['model']==model and rid['verdict']==v['verdict'] and rid['prompt_sha256']==sha(prompt(previous))
 reads=[]
 for p in files():
  url='https://api.github.com/repos/proteinfoldingengine/WetLabEngine/contents/'+urllib.parse.quote(p,safe='/')+'?ref='+identity()['checkout_sha']
  req=urllib.request.Request(url,headers={'Authorization':'Bearer '+os.environ['GH_READ_TOKEN'],'Accept':'application/vnd.github+json'})
  with urllib.request.urlopen(req,timeout=60) as r:d=json.load(r)
  b=base64.b64decode(d['content']);assert b==Path(p).read_bytes()
  reads.append(dict(path=p,blob=d['sha'],sha256=sha(b)))
 write(out,'review_readback.json',dict(status='PASS',verdict=v['verdict'],model=model,response_sha256=sha(raw),immutable_files=reads,native_bridge='NOT_DERIVED'))
def main():
 mode=sys.argv[1];out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
 try:
  if mode=='verify':verify(out)
  elif mode=='review':review(out,Path(sys.argv[3]).resolve())
  elif mode=='publication':publication(out,Path(sys.argv[3]).resolve(),Path(sys.argv[4]).resolve())
  else:raise ValueError('mode')
 except Exception as e:
  write(out,'failure.json',dict(status='INCOMPLETE',type=type(e).__name__,message=str(e)));raise
 finally:manifest(out)
if __name__=='__main__':main()
