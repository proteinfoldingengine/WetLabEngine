"""Author reconciliation of downloaded original archives and pinned input bytes."""
import hashlib,json,pathlib,re,zipfile
BASE=pathlib.Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
inputs=json.loads((BASE/'source_inputs.json').read_text())
artifacts=json.loads((BASE/'artifacts.json').read_text())
ledger={'scientific_commit':'a20f56bb0e02f49a7120e925f1900ad5a3e63fb5','scope_commit':'eefa97449ef540587450fa91bf207b9cff3482b6','tests_commit':'6a8c60c5ba6923fa7e1ee8ed5d44d15647f2f568','run_id':37943399282,'artifacts':[],'reviews':{}}
for name,folder in [('verification','verification'),('review','math'),('publication','publication')]:
 p=BASE/('original-'+name+'.zip');data=p.read_bytes();a=next(a for a in artifacts if a['name']=='c3-admission-'+name);assert a['digest']=='sha256:'+sha(data)
 with zipfile.ZipFile(p) as z:
  assert all(not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts for n in z.namelist())
  z.extractall(BASE/folder);members={n:sha(z.read(n)) for n in z.namelist()}
 ledger['artifacts'].append({'id':a['id'],'name':a['name'],'bytes':len(data),'sha256':sha(data),'members_sha256':members,'permanent_path':'original-'+name+'.zip'})
cert=(BASE/'verification/certificate.json').read_bytes();assert cert==(BASE/'certificate.json').read_bytes()
assert (BASE/'verification/provenance.txt').read_text()=='scientific_sha='+ledger['scientific_commit']+'\nworkflow_sha='+ledger['scientific_commit']+'\n'
ledger['certificate']={'bytes':len(cert),'sha256':sha(cert),'local_actions_byte_equal':True,'counts':json.loads((BASE/'verification/counts.json').read_text())}
for phase,folder in [('mathematical','math'),('publication','publication/admission_publication')]:
 raw=(BASE/folder/'review.txt').read_bytes();m=json.loads((BASE/folder/'manifest.json').read_text());assert m['response_sha256']==sha(raw)
 assert m['research_commit']==m['workflow_commit']==ledger['scientific_commit']
 for n,h in m['input_sha256'].items():
  if n.startswith('EVIDENCE/'):data=(BASE/'verification'/n[9:]).read_bytes()
  elif n.startswith('MATH_REVIEW/'):data=(BASE/'math'/n[12:]).read_bytes()
  elif n=='PUBLICATION_GATE':data=(BASE/'publication/admission_gate.json').read_bytes()
  else:data=inputs[n].encode()
  assert sha(data)==h,(phase,n)
 obj=json.loads(re.sub(r'^```(?:json)?\s*|\s*```$','',raw.decode().strip()))
 assert obj['verdict']=='ACCEPTED' and not obj['missing_assumptions'] and not obj['counterexamples'],obj
 ledger['reviews'][phase]={'verdict':obj['verdict'],'input_count':len(m['input_sha256']),'response_sha256':sha(raw),'model':m['model'],'tokens':m['tokens'],'attempts':m['attempts']}
gate=json.loads((BASE/'publication/admission_gate.json').read_text());assert gate['status']=='PASS' and gate['scientific_commit']==ledger['scientific_commit'] and gate['certificate_reproduced_byte_exact'] and gate['independent_full_reconstruction']
ledger['publication_gate']=gate;ledger['author_reconciliation']='PASS: original archive digests, all member hashes, all review input hashes, both response hashes, execution provenance, byte-identical local/Actions certificate and separate reproduction gate'
(BASE/'EVIDENCE.json').write_text(json.dumps(ledger,indent=2,sort_keys=True)+'\n');print(json.dumps(ledger,indent=2))
