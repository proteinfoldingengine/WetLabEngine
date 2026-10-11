import pathlib,json,hashlib
P=pathlib.Path(__file__).resolve().parent;B='ResearchHistory/UQCF-GEM/research/physical-bridge/';E=B+'evidence/reserve-activation-local/'
assert json.loads((P/'independent_result.json').read_text())['accepted']
assert json.loads((P/'fresh_comparison.json').read_text())['byte_equal']
r=json.loads((P/'inherited/results.json').read_text());assert all(x['exit_code']==0 for x in r) and sum(x['tests'] for x in r)==455
assert 'Ran 30 tests' in (P/'tests_final.log').read_text() and (P/'tests_final.log').read_text().rstrip().endswith('OK')
m={n:B+'reserve_activation/'+n for n in ['producer.py','independent.py','test_activation.py','red.log']}
m.update({n:B+'COUPLED_C3_RESERVE_ACTIVATION_'+n for n in ['REPORT.md','REVIEW.md']})
m.update({'workflow.yml':'.github/workflows/uqcf-gem-c3-reserve-activation.yml','review_runner.py':'.github/scripts/c3_reserve_activation_review.py'})
names=['CODE_REVIEW.md','freeze_binding.json','freeze_readback.json','progress.md','tests_attempt1.log','tests_attempt2.log','tests_final.log','native_classification_red.log','inherited_launcher_failure.log','run_inherited.py','initial_output_manifest.json','initial_producer_full.log','initial_fresh_producer.log','producer_full.log','producer_full.exit','fresh_producer.log','fresh_producer.exit','independent_full.log','independent_full.exit','independent_result.json','fresh_comparison.json','stage_scientific.py']
for n in names:m[n]=E+n
for f in sorted((P/'inherited').iterdir()):
 if f.is_file():m['inherited/'+f.name]=E+'inherited/'+f.name
entries=[];manifest=[]
for local,path in m.items():
 b=(P/local).read_bytes();entries.append(dict(path=path,mode='100644',type='blob',content=b.decode()));manifest.append(dict(path=path,local=local,sha256=hashlib.sha256(b).hexdigest(),git_blob_sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
(P/'scientific_entries.json').write_text(json.dumps(entries)+'\n');(P/'scientific_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(len(entries),'texts staged')
