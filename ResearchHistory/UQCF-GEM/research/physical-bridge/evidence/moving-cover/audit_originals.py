"""Author reconciliation of original run artifacts and exact immutable inputs."""
import hashlib,json,pathlib,re,zipfile
P=pathlib.Path(__file__).parent;O=P/'originals' if (P/'originals').exists() else P;input_file=P/'review_inputs.json' if (P/'review_inputs.json').exists() else P/'review_input_readbacks.json';packet=json.loads(input_file.read_text());science=packet['scientific_commit'];docs={k:v.encode() for k,v in packet['documents'].items()}
def digest(b):return hashlib.sha256(b).hexdigest()
archives={}
metadata=[]
RUN=38080966096
JOB_NAMES={'verification','fresh-reproduction','mathematical-review','publication-audit'}
TESTS={'contracts.log':28,'inherited_saturated_handover.log':26,'inherited_slack_handover.log':24,'inherited_handover_graph.log':20,'inherited_anchored_release.log':20,'inherited_local_progress.log':17,'inherited_capacity_gap.log':20,'inherited_saturated_transfer.log':22,'inherited_label_release.log':26,'inherited_footprint.log':22,'inherited_fixed_family.log':28}
DOCS={'COUPLED_C3_MOVING_COVER_RESULT.md','COUPLED_C3_MOVING_COVER_REVIEW.md','COUPLED_C3_MOVING_COVER_REPORT.md','COUPLED_C3_FOOTPRINT_CLOSEOUT.md','COUPLED_C3_ANCHORED_RELEASE_CLOSEOUT.md','COUPLED_C3_HANDOVER_GRAPH_CLOSEOUT.md','COUPLED_C3_SATURATED_HANDOVER_CLOSEOUT.md','moving_cover/producer.py','moving_cover/independent.py','moving_cover/test_moving.py'}
assert set(docs)==DOCS
VERIFICATION=set(TESTS)|{'certificate.json','certificate.sha256','counts.json','frozen_proof_scope.md','independent.json','independent.log','independent.py','producer.py','provenance.txt','red.log','test_moving.py'}

runmeta=json.loads((O/'run_metadata.json').read_text());assert runmeta['id']==RUN and runmeta['head_sha']==science and runmeta['conclusion']=='success' and runmeta['head_branch']=='research/uqcf-overlapping-guard-exchange'
jobs=json.loads((O/'jobs_metadata.json').read_text())['jobs'];assert len(jobs)==4 and {j['name'] for j in jobs}==JOB_NAMES and len({j['id'] for j in jobs})==4 and all(j['conclusion']=='success' and j['run_id']==RUN and all(s['conclusion']=='success' for s in j['steps']) for j in jobs)
artifactmeta=json.loads((O/'artifact_metadata.json').read_text())['artifacts'];assert len(artifactmeta)==4 and {a['name'] for a in artifactmeta}=={'c3-moving-cover-'+n for n in JOB_NAMES} and all(a['workflow_run']['id']==RUN and a['workflow_run']['head_sha']==science for a in artifactmeta)
expected_digests={a['name']+'.zip':a['digest'].removeprefix('sha256:') for a in artifactmeta}
for file in sorted(O.glob('*.zip')):
 b=file.read_bytes();assert digest(b)==expected_digests[file.name]
 with zipfile.ZipFile(file) as z:contents={n:z.read(n) for n in z.namelist()}
 archives[file.stem]=contents;metadata.append({'file':file.name,'size':len(b),'sha256':digest(b),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'members':{k:digest(v) for k,v in contents.items()}})
verification=archives['c3-moving-cover-verification'];fresh=archives['c3-moving-cover-fresh-reproduction'];math=archives['c3-moving-cover-mathematical-review'];pub=archives['c3-moving-cover-publication-audit']
assert len(archives)==4
assert set(verification)==VERIFICATION and set(fresh)==VERIFICATION|{'fresh_independent.json'}
assert set(math)=={'manifest.json','review.txt'}
assert set(pub)=={'moving_cover_gate.json','moving_cover_publication/manifest.json','moving_cover_publication/review.txt'}
assert all(fresh[n]==verification[n] for n in VERIFICATION)
assert verification['certificate.json']==fresh['certificate.json']
# A local regeneration is checked when present; CI/fresh/publication reproductions
# remain bound by original artifacts and the verified publication gate.
if (P/'certificate.json').exists():assert fresh['certificate.json']==(P/'certificate.json').read_bytes()
assert digest(fresh['certificate.json'])=='1fc3b973ab9328df08f99cdcb83a6d151cde7203e0d17415c2b0603cd6cf985c'
expected=f'scientific_sha={science}\nworkflow_sha={science}\n'.encode();assert verification['provenance.txt']==fresh['provenance.txt']==expected
counts=json.loads(fresh['counts.json'])
certificate=json.loads(fresh['certificate.json'])
classification={}
for case in certificate['cases']:
 for target,reachable in zip(range(-1,len(case['source'])),case['reachable']):
  persistent=any(q['reachable'] for q in case['covers'] if q['target']==target)
  assert not persistent or reachable
  key=('any' if target<0 else 'prescribed')+('_moving_required' if reachable and not persistent else '_persistent_possible' if persistent else '_unreachable')
  classification[key]=classification.get(key,0)+1
assert classification=={'any_persistent_possible':99,'any_unreachable':81,'prescribed_moving_required':24,'prescribed_persistent_possible':477,'prescribed_unreachable':411}

if (P/'counts.json').exists():assert counts==json.loads((P/'counts.json').read_text())
for name in ['independent.json','fresh_independent.json']:assert json.loads(fresh[name])['status']=='ACCEPTED' and json.loads(fresh[name])['counts']==counts
assert verification['frozen_proof_scope.md']==docs['COUPLED_C3_MOVING_COVER_RESULT.md']
for name in ['producer.py','independent.py','test_moving.py']:assert fresh[name]==docs['moving_cover/'+name]
test_counts={}
for name,b in verification.items():
 if name=='contracts.log' or name.startswith('inherited_'):
  text=b.decode();n=re.findall(r'Ran (\d+) tests',text);assert len(n)==1 and re.search(r'\nOK\s*$',text);test_counts[name]=int(n[0])
assert test_counts==TESTS and sum(test_counts.values())==253
assert b'Ran 22 tests' in fresh['red.log'] and b'FAILED (failures=20)' in fresh['red.log']
mathmanifest=json.loads(math['manifest.json']);mathraw=math['review.txt'];gate=pub['moving_cover_gate.json'];pubmanifest=json.loads(pub['moving_cover_publication/manifest.json']);pubraw=pub['moving_cover_publication/review.txt']
for m,raw,is_pub in [(mathmanifest,mathraw,False),(pubmanifest,pubraw,True)]:
 expected_inputs=DOCS|{'EVIDENCE/'+n for n in (VERIFICATION|{'fresh_independent.json'})-{'certificate.json'}}
 if is_pub:expected_inputs|={'MATH_REVIEW/manifest.json','MATH_REVIEW/review.txt','PUBLICATION_GATE'}
 assert set(m['input_sha256'])==expected_inputs
 assert m['research_commit']==m['workflow_commit']==science
 assert m['attempts'] and m['attempts'][-1]['status']=='RESPONSE_RECEIVED'
 assert all(a.get('status')=='RESPONSE_RECEIVED' or 'http_status' in a or 'error_type' in a for a in m['attempts']),m['attempts']
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
bindings=json.loads((O/'job_log_sources.json').read_text())
assert len(bindings)==4 and {b['job_name'] for b in bindings}==JOB_NAMES
assert {f.name for f in O.glob('*_job.log')}=={n.replace('-','_')+'_job.log' for n in JOB_NAMES}
for item in bindings:
 name=item['job_name'];filename=name.replace('-','_')+'_job.log';job=next(j for j in jobs if j['name']==name);artifact=next(a for a in artifactmeta if a['name']=='c3-moving-cover-'+name)
 assert item['file']==filename and item['job_id']==job['id'] and item['run_id']==RUN
 assert item['endpoint']==f"https://api.github.com/repos/proteinfoldingengine/WetLabEngine/actions/jobs/{job['id']}/logs"
 b=(O/filename).read_bytes();t=b.decode();assert len(b)==item['bytes'] and digest(b)==item['sha256']
 assert 'Current runner version:' in t[:200] and f'Complete job name: {name}' in t
 assert science in t and f"Artifact c3-moving-cover-{name} has been successfully uploaded!" in t and f"Artifact ID is {artifact['id']}" in t
 assert 'Cleaning up orphan processes' in t[-3000:]
 if name in {'mathematical-review','publication-audit'}:assert 'Moving-cover independent verdict: ACCEPTED' in t
 logs[filename]={'size':len(b),'sha256':digest(b),'job_id':job['id'],'run_id':RUN,'complete_markers_verified':True}
result={'status':'ACCEPTED_AUTHOR_RECONCILIATION','scientific_commit':science,'workflow_run':38080966096,'scope_freeze':'dbe4c779be4ddde37017328b84ede84169659d5d','certificate_sha256':digest(fresh['certificate.json']),'counts':counts,'finite_classification':classification,'test_counts':test_counts,'tests_total':253,'initial_red_tests':22,'final_new_tests':28,'mathematical_verdict':'ACCEPTED','publication_verdict':'ACCEPTED','math_verified_inputs':len(mathmanifest['input_sha256']),'publication_verified_inputs':len(pubmanifest['input_sha256']),'math_attempts':mathmanifest['attempts'],'publication_attempts':pubmanifest['attempts'],'math_response_sha256':digest(mathraw),'publication_response_sha256':digest(pubraw),'original_archives':metadata,'complete_job_logs':logs,'limitations':['prescribed e vacancy forces moving cover; first b vacancy has persistent4cover','coretau4; FULLhidden3..4','achieved4r+8, no native optimality','finite90sources180cases3426cover-targetjobs plus31familycases; universal theorem proof-based','exact marked quotient for reserve predicates, not exact labelled targets','polynomial vertices only fixedk','broadC3/generalC4/nativeobserver-access-outcome-progress OPEN']}
(P/'author_reconciliation.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','tests_total','math_verified_inputs','publication_verified_inputs','mathematical_verdict','publication_verdict']}))
