"""Author reconciliation of original run artifacts and exact immutable inputs."""
if not __debug__: raise RuntimeError("audit requires assertions enabled")
import hashlib,json,pathlib,re,zipfile
P=pathlib.Path(__file__).parent;O=P/'originals' if (P/'originals').exists() else P;input_file=P/'review_inputs.json' if (P/'review_inputs.json').exists() else P/'review_input_readbacks.json';packet=json.loads(input_file.read_text());science=packet['scientific_commit'];docs={k:v.encode() for k,v in packet['documents'].items()}
assert science==json.loads((P/'binding.json').read_text())['scientific_commit']
def digest(b):return hashlib.sha256(b).hexdigest()
from reassemble_archives import materialize
materialize(O)
archives={}
metadata=[]
RUN=json.loads((P/'binding.json').read_text())['workflow_run']
JOB_NAMES={'verification','fresh-reproduction','mathematical-review','publication-audit'}
TESTS={'contracts.log':30,'inherited_source_escape.log':42,'inherited_cover_static.log':35,'inherited_nonuniform_reserve.log':34,'inherited_weak_trace.log':32,'inherited_fingerprint_lock.log':33,'inherited_private_cover.log':26,'inherited_moving_cover.log':28,'inherited_saturated_handover.log':26,'inherited_slack_handover.log':24,'inherited_handover_graph.log':20,'inherited_anchored_release.log':20,'inherited_local_progress.log':17,'inherited_capacity_gap.log':20,'inherited_saturated_transfer.log':22,'inherited_label_release.log':26,'inherited_footprint.log':22,'inherited_fixed_family.log':28}
DOCS={'COUPLED_C3_COVER_STATIC_CLOSEOUT.md', 'reserve_activation/PLAN.md', 'COUPLED_C3_SOURCE_ESCAPE_CLOSEOUT.md', 'COUPLED_C3_RESERVE_ACTIVATION_REPORT.md', 'reserve_activation/producer.py', 'COUPLED_C3_ORIGIN_REENTRY_DECISION.md', 'reserve_activation/test_activation.py', 'COUPLED_C3_COVERAGE_ORIGIN_SCREEN.md', 'COUPLED_C3_RESERVE_ACTIVATION_RESULT.md', 'COUPLED_C3_RESERVE_ACTIVATION_ANALYTICAL_REVIEW.md', 'COUPLED_C3_AUTONOMY_CLOSEOUT.md', 'reserve_activation/independent.py', 'COUPLED_C3_RESERVE_ACTIVATION_REVIEW.md', 'COUPLED_C3_RESERVE_ACTIVATION_SCOPE.md'}
assert set(docs)==DOCS
VERIFICATION=set(TESTS)|{'certificate.json','certificate.sha256','counts.json','frozen_proof_scope.md','independent.json','independent.log','independent.py','producer.py','provenance.txt','red.log','test_activation.py','certificate.json.identities.jsonl.gz','identities.sha256'}

runmeta=json.loads((O/'run_metadata.json').read_text());assert runmeta['id']==RUN and runmeta['head_sha']==science and runmeta['conclusion']=='success' and runmeta['head_branch']=='research/uqcf-overlapping-guard-exchange'
jobs=json.loads((O/'jobs_metadata.json').read_text())['jobs'];assert len(jobs)==4 and {j['name'] for j in jobs}==JOB_NAMES and len({j['id'] for j in jobs})==4 and all(j['conclusion']=='success' and j['run_id']==RUN and all(s['conclusion']=='success' for s in j['steps']) for j in jobs)
artifactmeta=json.loads((O/'artifact_metadata.json').read_text())['artifacts'];assert len(artifactmeta)==4 and {a['name'] for a in artifactmeta}=={'c3-reserve-activation-'+n for n in JOB_NAMES} and all(a['workflow_run']['id']==RUN and a['workflow_run']['head_sha']==science for a in artifactmeta)
expected_digests={a['name']+'.zip':a['digest'].removeprefix('sha256:') for a in artifactmeta}
for file in sorted(O.glob('*.zip')):
 b=file.read_bytes();assert digest(b)==expected_digests[file.name]
 with zipfile.ZipFile(file) as z:
  contents={n:z.read(n) for n in z.namelist()};assert len(contents)==len(z.namelist())
 assert len(b)==next(a['size_in_bytes'] for a in artifactmeta if a['name']==file.stem)
 archives[file.stem]=contents;metadata.append({'file':file.name,'size':len(b),'sha256':digest(b),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'members':{k:digest(v) for k,v in contents.items()}})
verification=archives['c3-reserve-activation-verification'];fresh=archives['c3-reserve-activation-fresh-reproduction'];math=archives['c3-reserve-activation-mathematical-review'];pub=archives['c3-reserve-activation-publication-audit']
assert len(archives)==4
assert set(verification)==VERIFICATION and set(fresh)==VERIFICATION|{'fresh_independent.json'}
assert set(math)=={'manifest.json','review.txt'}
assert set(pub)=={'reserve_activation_gate.json','reserve_activation_publication/manifest.json','reserve_activation_publication/review.txt'}
assert all(fresh[n]==verification[n] for n in VERIFICATION)
assert verification['certificate.json']==fresh['certificate.json']
# A local regeneration is checked when present; CI/fresh/publication reproductions
# remain bound by original artifacts and the verified publication gate.
if (P/'certificate.json').exists():assert fresh['certificate.json']==(P/'certificate.json').read_bytes()
assert digest(fresh['certificate.json'])==json.loads((P/'binding.json').read_text())['certificate_sha256']
assert digest(fresh['certificate.json.identities.jsonl.gz'])==json.loads(fresh['certificate.json'])['identity_archive_sha256']
expected=f'scientific_sha={science}\nworkflow_sha={science}\n'.encode();assert verification['provenance.txt']==fresh['provenance.txt']==expected
counts=json.loads(fresh['counts.json'])
certificate=json.loads(fresh['certificate.json'])
assert certificate['counts']==counts
assert fresh['certificate.sha256'].decode().split()[0]==digest(fresh['certificate.json'])
assert fresh['identities.sha256'].decode().split()[0]==digest(fresh['certificate.json.identities.jsonl.gz'])
assert counts=={'abstract_candidates': 173230, 'abstract_edges': 46947, 'abstract_sources': 5054, 'abstract_states': 47151, 'abstract_terminals': 21685, 'distinct_states': 75326, 'hidden_checks': 303865084, 'native_edits': 67134, 'native_macros': 16422, 'native_positive': 7488, 'native_sources': 8192, 'slice_occurrences': 75326}
assert len(certificate['record_sha256'])==13246

if (P/'counts.json').exists():assert counts==json.loads((P/'counts.json').read_text())
for name in ['independent.json','fresh_independent.json']:assert json.loads(fresh[name])['accepted'] is True and json.loads(fresh[name])['counts']==counts
assert verification['frozen_proof_scope.md']==docs['COUPLED_C3_RESERVE_ACTIVATION_RESULT.md']
for name in ['producer.py','independent.py','test_activation.py']:assert fresh[name]==docs['reserve_activation/'+name]
test_counts={}
for name,b in verification.items():
 if name=='contracts.log' or name.startswith('inherited_'):
  text=b.decode();n=re.findall(r'Ran (\d+) tests',text);assert len(n)==1 and re.search(r'\nOK\s*$',text);test_counts[name]=int(n[0])
assert test_counts==TESTS and sum(test_counts.values())==485
assert b'Ran 1 test' in fresh['red.log'] and b'ModuleNotFoundError' in fresh['red.log'] and b'FAILED (errors=1)' in fresh['red.log']
mathmanifest=json.loads(math['manifest.json']);mathraw=math['review.txt'];gate=pub['reserve_activation_gate.json'];pubmanifest=json.loads(pub['reserve_activation_publication/manifest.json']);pubraw=pub['reserve_activation_publication/review.txt']
for m,raw,is_pub in [(mathmanifest,mathraw,False),(pubmanifest,pubraw,True)]:
 expected_inputs=DOCS|{'EVIDENCE/'+n for n in (VERIFICATION|{'fresh_independent.json'})}
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
 name=item['job_name'];filename=name.replace('-','_')+'_job.log';job=next(j for j in jobs if j['name']==name);artifact=next(a for a in artifactmeta if a['name']=='c3-reserve-activation-'+name)
 assert item['file']==filename and item['job_id']==job['id'] and item['run_id']==RUN
 assert item['endpoint']==f"https://api.github.com/repos/proteinfoldingengine/WetLabEngine/actions/jobs/{job['id']}/logs"
 b=(O/filename).read_bytes();t=b.decode();assert len(b)==item['bytes'] and digest(b)==item['sha256']
 assert 'Current runner version:' in t[:200] and f'Complete job name: {name}' in t
 assert science in t and f"Artifact c3-reserve-activation-{name} has been successfully uploaded!" in t and f"Artifact ID is {artifact['id']}" in t
 assert 'Cleaning up orphan processes' in t[-3000:]
 if name in {'mathematical-review','publication-audit'}:assert 'Reserve-activation independent verdict: ACCEPTED' in t
 logs[filename]={'size':len(b),'sha256':digest(b),'job_id':job['id'],'run_id':RUN,'complete_markers_verified':True}
result={'status':'ACCEPTED_AUTHOR_RECONCILIATION','scientific_commit':science,'workflow_run':RUN,'scope_freeze':'bf40d757b903256f66f9f809b767db7d9ab0826f','certificate_sha256':digest(fresh['certificate.json']),'counts':counts,'test_counts':test_counts,'tests_total':485,'initial_red_loader_tests':1,'final_new_tests':30,'mathematical_verdict':'ACCEPTED','publication_verdict':'ACCEPTED','math_verified_inputs':len(mathmanifest['input_sha256']),'publication_verified_inputs':len(pubmanifest['input_sha256']),'math_attempts':mathmanifest['attempts'],'publication_attempts':pubmanifest['attempts'],'math_response_sha256':digest(mathraw),'publication_response_sha256':digest(pubraw),'original_archives':metadata,'complete_job_logs':logs, 'limitations':['Exact monotone fixed-anchor activation template only, not unrestricted reachability','5054abstract matrices and8192native K4,3sources; canonical native choices/routes only','Protected one-hidden finite pairs checked with exact factorization; arbitraryhidden safety analytical','Exact reversal only with no intervening changes, no arbitrary use or shortest-path theorem','Native acquisition-origin-enforcement-selection-progress and broadC3/C4-C6 OPEN']}
(P/'author_reconciliation.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','tests_total','math_verified_inputs','publication_verified_inputs','mathematical_verdict','publication_verdict']}))
