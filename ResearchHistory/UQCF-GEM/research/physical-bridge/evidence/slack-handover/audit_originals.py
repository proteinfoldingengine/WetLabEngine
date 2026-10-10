"""Author reconciliation of original run artifacts and exact immutable inputs."""
import hashlib,json,pathlib,re,zipfile
P=pathlib.Path(__file__).parent;O=P/'originals' if (P/'originals').exists() else P;input_file=P/'review_inputs.json' if (P/'review_inputs.json').exists() else P/'review_input_readbacks.json';packet=json.loads(input_file.read_text());science=packet['scientific_commit'];docs={k:v.encode() for k,v in packet['documents'].items()}
def digest(b):return hashlib.sha256(b).hexdigest()
archives={}
metadata=[]
for file in sorted(O.glob('*.zip')):
 b=file.read_bytes()
 with zipfile.ZipFile(file) as z:contents={n:z.read(n) for n in z.namelist()}
 archives[file.stem]=contents;metadata.append({'file':file.name,'size':len(b),'sha256':digest(b),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'members':{k:digest(v) for k,v in contents.items()}})
verification=archives['c3-slack-handover-verification'];fresh=archives['c3-slack-handover-fresh-reproduction'];math=archives['c3-slack-handover-mathematical-review'];pub=archives['c3-slack-handover-publication-audit']
assert len(archives)==4
assert verification['certificate.json']==fresh['certificate.json']
# A local regeneration is checked when present; CI/fresh/publication reproductions
# remain bound by original artifacts and the verified publication gate.
if (P/'certificate_current.json').exists():assert fresh['certificate.json']==(P/'certificate_current.json').read_bytes()
assert digest(fresh['certificate.json'])=='39537e4a3dd193ebe8df8791d9d6a29a67f3766a2762a7beea46ecea3bb304f3'
expected=f'scientific_sha={science}\nworkflow_sha={science}\n'.encode();assert verification['provenance.txt']==fresh['provenance.txt']==expected
counts=json.loads(fresh['counts.json'])
if (P/'counts_current.json').exists():assert counts==json.loads((P/'counts_current.json').read_text())
for name in ['independent.json','fresh_independent.json']:assert json.loads(fresh[name])['status']=='ACCEPTED' and json.loads(fresh[name])['counts']==counts
assert verification['frozen_proof_scope.md']==docs['COUPLED_C3_SLACK_HANDOVER_RESULT.md']
for name in ['producer.py','independent.py','test_slack.py']:assert fresh[name]==docs['slack_handover/'+name]
test_counts={}
for name,b in verification.items():
 if name=='contracts.log' or name.startswith('inherited_'):
  text=b.decode();n=re.findall(r'Ran (\d+) tests',text);assert len(n)==1 and re.search(r'\nOK\s*$',text);test_counts[name]=int(n[0])
assert test_counts['contracts.log']==24 and sum(test_counts.values())==199
assert b'Ran 21 tests' in fresh['red.log'] and b'FAILED (failures=10, errors=11)' in fresh['red.log']
assert b'Ran 22 tests' in fresh['upper_four_red.log'] and b'FAILED (failures=1)' in fresh['upper_four_red.log']
assert b'AssertionError' in fresh['full_scope_failure.log']
mathmanifest=json.loads(math['manifest.json']);mathraw=math['review.txt'];gate=pub['slack_handover_gate.json'];pubmanifest=json.loads(pub['slack_handover_publication/manifest.json']);pubraw=pub['slack_handover_publication/review.txt']
for m,raw,is_pub in [(mathmanifest,mathraw,False),(pubmanifest,pubraw,True)]:
 assert m['research_commit']==m['workflow_commit']==science
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
result={'status':'ACCEPTED_AUTHOR_RECONCILIATION','scientific_commit':science,'workflow_run':38067111288,'scope_freeze':'6f2f90d80d1b9e6bb309527051a347835d7b5d0a','certificate_sha256':digest(fresh['certificate.json']),'counts':counts,'test_counts':test_counts,'tests_total':199,'initial_red_tests':21,'upper_four_red_tests':22,'mathematical_verdict':'ACCEPTED','publication_verdict':'ACCEPTED','math_verified_inputs':len(mathmanifest['input_sha256']),'publication_verified_inputs':len(pubmanifest['input_sha256']),'math_response_sha256':digest(mathraw),'publication_response_sha256':digest(pubraw),'original_archives':metadata,'complete_job_logs':logs,'limitations':['mixed-floor positive family, not fully saturated','scripted exacttau3; rawBFS3..4','finite onehidden masks; universal theorem proof-based','four optimal toANYfirstvacancy; batch cost achieved','broadC3/generalC4/nativeobserver-access-outcome-progress OPEN']}
(P/'author_reconciliation.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','tests_total','math_verified_inputs','publication_verified_inputs','mathematical_verdict','publication_verdict']}))
