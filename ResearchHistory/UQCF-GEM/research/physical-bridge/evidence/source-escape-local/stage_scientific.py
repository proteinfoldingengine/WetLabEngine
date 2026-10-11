"""Stage scientifically verified texts for leased publication; refuse incomplete runs."""
import pathlib,json,hashlib,ast
P=pathlib.Path(__file__).parent;B='ResearchHistory/UQCF-GEM/research/physical-bridge/'
assert json.loads((P/'fresh_comparison.json').read_text())['byte_equal'] is True
assert json.loads((P/'fresh_independent_result.json').read_text())['accepted'] is True
inherited=json.loads((P/'inherited/results.json').read_text());assert sum(x['tests'] for x in inherited)==413 and all(x['exit_code']==0 for x in inherited)
mapping={n:B+'source_escape/'+n for n in ['producer.py','independent.py','test_escape.py','red.log','initial_test_syntax_failure.log']}
mapping.update({n:B+'COUPLED_C3_SOURCE_ESCAPE_'+n for n in ['REPORT.md','REVIEW.md']})
mapping.update({'workflow.yml':'.github/workflows/uqcf-gem-c3-source-escape.yml','review_runner.py':'.github/scripts/c3_source_escape_review.py'})
local=['CODE_REVIEW.md','archive_failure.json','independent_attempt1_failure.log','fresh_independent.log','fresh_independent_result.json','producer_full.log','producer_rerun.log','fresh_producer.log','fresh_comparison.json','tests_attempt1.log','tests_attempt1.exit','progress.md','stage_scientific.py']
local+=['inherited/'+f.name for f in sorted((P/'inherited').iterdir()) if f.is_file()]
for n in local:mapping[n]=B+'evidence/source-escape-local/'+n
entries=[];manifest=[]
for local,path in mapping.items():
 data=(P/local).read_bytes();entries.append(dict(path=path,mode='100644',type='blob',content=data.decode()));manifest.append(dict(path=path,local=local,sha256=hashlib.sha256(data).hexdigest(),git_blob_sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()))
(P/'scientific_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(P/'scientific_entries.json').write_text(json.dumps(entries)+'\n');print(len(entries),'scientific texts staged')
