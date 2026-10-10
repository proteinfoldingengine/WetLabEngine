"""Author reconciliation of original run artifacts and exact immutable inputs."""
import hashlib,json,pathlib,re,zipfile
P=pathlib.Path(__file__).parent;O=P/'originals' if (P/'originals').exists() else P;input_file=P/'review_inputs.json' if (P/'review_inputs.json').exists() else P/'review_input_readbacks.json';packet=json.loads(input_file.read_text());science=packet['scientific_commit'];docs={k:v.encode() for k,v in packet['documents'].items()}
def digest(b):return hashlib.sha256(b).hexdigest()
archives={}
metadata=[]
runmeta=json.loads((O/'run_metadata.json').read_text());assert runmeta['head_sha']==science and runmeta['conclusion']=='success'
jobs=json.loads((O/'jobs_metadata.json').read_text())['jobs'];assert len(jobs)==4 and all(j['conclusion']=='success' for j in jobs)
artifactmeta=json.loads((O/'artifact_metadata.json').read_text())['artifacts'];assert len(artifactmeta)==4
expected_digests={a['name']+'.zip':a['digest'].removeprefix('sha256:') for a in artifactmeta}
for file in sorted(O.glob('*.zip')):
 b=file.read_bytes();assert digest(b)==expected_digests[file.name]
 with zipfile.ZipFile(file) as z:contents={n:z.read(n) for n in z.namelist()}
 archives[file.stem]=contents;metadata.append({'file':file.name,'size':len(b),'sha256':digest(b),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'members':{k:digest(v) for k,v in contents.items()}})
verification=archives['c3-saturated-handover-verification'];fresh=archives['c3-saturated-handover-fresh-reproduction'];math=archives['c3-saturated-handover-mathematical-review'];pub=archives['c3-saturated-handover-publication-audit']
assert len(archives)==4
assert verification['certificate.json']==fresh['certificate.json']
# A local regeneration is checked when present; CI/fresh/publication reproductions
# remain bound by original artifacts and the verified publication gate.
if (P/'certificate.json').exists():assert fresh['certificate.json']==(P/'certificate.json').read_bytes()
assert digest(fresh['certificate.json'])=='de22bef5b724490c5c138de88b1708aa6644f837a1304acc24534f2136028bdb'
expected=f'scientific_sha={science}\nworkflow_sha={science}\n'.encode();assert verification['provenance.txt']==fresh['provenance.txt']==expected
counts=json.loads(fresh['counts.json'])
if (P/'counts.json').exists():assert counts==json.loads((P/'counts.json').read_text())
for name in ['independent.json','fresh_independent.json']:assert json.loads(fresh[name])['status']=='ACCEPTED' and json.loads(fresh[name])['counts']==counts
assert verification['frozen_proof_scope.md']==docs['COUPLED_C3_SATURATED_HANDOVER_RESULT.md']
for name in ['producer.py','independent.py','test_saturated.py']:assert fresh[name]==docs['saturated_handover/'+name]
test_counts={}
for name,b in verification.items():
 if name=='contracts.log' or name.startswith('inherited_'):
  text=b.decode();n=re.findall(r'Ran (\d+) tests',text);assert len(n)==1 and re.search(r'\nOK\s*$',text);test_counts[name]=int(n[0])
assert test_counts['contracts.log']==26 and sum(test_counts.values())==225
assert b'Ran 24 tests' in fresh['red.log'] and b'FAILED (failures=5, errors=18)' in fresh['red.log']
assert b'Ran 26 tests' in fresh['witness_red.log'] and b'FAILED (failures=1)' in fresh['witness_red.log']
mathmanifest=json.loads(math['manifest.json']);mathraw=math['review.txt'];gate=pub['saturated_handover_gate.json'];pubmanifest=json.loads(pub['saturated_handover_publication/manifest.json']);pubraw=pub['saturated_handover_publication/review.txt']
for m,raw,is_pub in [(mathmanifest,mathraw,False),(pubmanifest,pubraw,True)]:
 assert m['research_commit']==m['workflow_commit']==science
 assert m['attempts'] and m['attempts'][-1]['status']=='RESPONSE_RECEIVED'
 assert all(a['status'] in ['RESPONSE_RECEIVED','INFRASTRUCTURE_ERROR'] for a in m['attempts']),m['attempts']
 for name,d in m['input_sha256'].items():
  if name.startswith('EVIDENCE/'):b=fresh[name[9:]]
  elif name.startswith('MATH_REVIEW/'):b=math[name[12:]]
  elif name=='PUBLICATION_GATE':b=gate
  else:b=docs[name]
  assert digest(b)==d,name
 assert digest(raw)==m['response_sha256']
 text=raw.decode().strip();text=re.sub(r'^```(?:json)?\s*|\s*```$','',text).strip();verdict=json.loads(text)
 assert verdict['verdict']=='ACCEPTED' and not verdict['missing_assumptions'] and not verdict['counterexamples']
G=json.loads(gate);assert G['status']=='PASS' and G['scientific_commit']==science and G['certificate_reproduced_byte_exact'] and G['independent_full_reconstruction'] and G['response_sha256']==mathmanifest['response_sha256'];assert G['verified_review_inputs']==len(mathmanifest['input_sha256'])
logs={}
for f in O.glob('*_job.log'):logs[f.name]={'size':f.stat().st_size,'sha256':digest(f.read_bytes())}
assert len(logs)==4
result={'status':'ACCEPTED_AUTHOR_RECONCILIATION','scientific_commit':science,'workflow_run':38079576180,'scope_freeze':'851a80a803b47696466c1cee3c3605e2744457ed','certificate_sha256':digest(fresh['certificate.json']),'counts':counts,'test_counts':test_counts,'tests_total':225,'initial_red_tests':24,'witness_red_tests':26,'mathematical_verdict':'ACCEPTED','publication_verdict':'ACCEPTED','math_verified_inputs':len(mathmanifest['input_sha256']),'publication_verified_inputs':len(pubmanifest['input_sha256']),'math_attempts':mathmanifest['attempts'],'publication_attempts':pubmanifest['attempts'],'math_response_sha256':digest(mathraw),'publication_response_sha256':digest(pubraw),'original_archives':metadata,'complete_job_logs':logs,'limitations':['fully saturated crossed-block family; persistent actual3cover','achieved4r+6, no native optimality','finite r2..5 and147 permutation union; universal theorem proof-based','exact count quotient for first vacancy, not exact labelled targets','polynomial vertices only fixedk','broadC3/generalC4/nativeobserver-access-outcome-progress OPEN']}
(P/'author_reconciliation.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','tests_total','math_verified_inputs','publication_verified_inputs','mathematical_verdict','publication_verdict']}))
