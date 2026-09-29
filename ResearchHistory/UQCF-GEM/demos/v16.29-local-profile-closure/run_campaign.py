"""Execute .29 and the 198 scoped inherited tests; record failures, never default success."""
from pathlib import Path
import hashlib,importlib.metadata,json,os,platform,re,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=P,text=True).strip())
U=ROOT/'ResearchHistory/UQCF-GEM';E=P/'evidence';E.mkdir(exist_ok=True)
V27=U/'demos/v16.27-increment-attribution-closure'
commands=[('v1629-tests',P,['test_gate.py'],30),('producer',P,['producer.py'],None),('verifier',P,['verifier.py'],None),
 ('v1628-tests',U/'demos/v16.28-diamond-attribution-closure',['test_gate.py'],28),
 ('v1627-contract',V27/'completion',['test_contract.py'],11),('v1627-complete',V27/'completion',['test_complete.py'],23),
 ('v1627-original',V27,['test_gate.py'],5),('v1626',U/'demos/v16.26-consistency-increment-law',['test_gate.py'],8),
 ('v1625',U/'demos/v16.25-pruning-refinement-closure',['test_gate.py'],11),('v1624',U/'demos/v16.24-consistency-order',['test_gate.py'],28),
 ('v1624-validation',U/'demos/v16.24-consistency-order',['test_validation.py'],2),('v1623',U/'demos/v16.23-overlap-descent',['test_gate.py'],22),
 ('v1623-schema',U/'demos/v16.23-overlap-descent',['test_schema.py'],3),('v1622',U/'demos/v16.22-response-selection-closure',['-m','unittest','discover','-v'],20),
 ('v1621',U/'foundational-closure-verification',['tests/test_fcv.py'],22),('exact-parent',U/'demos/v15.56-response-selector-obstruction',['-m','unittest','-v','test_pruning_consistency_audit'],15)]
records=[];status='INVALID_EXECUTION';env=dict(os.environ,V27_VERIFIER='verifier',V27_EVIDENCE=str(E/'inherited-v27'))
try:
 for name,cwd,args,count in commands:
  cmd=[sys.executable]+args
  with (E/(name+'.log')).open('wb') as log:r=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
  text=(E/(name+'.log')).read_text();tests=[int(x) for x in re.findall(r'Ran (\d+) tests?',text)]
  record={'name':name,'cwd':str(cwd.relative_to(ROOT)),'command':cmd,'exit_code':r.returncode,'tests':tests};records.append(record)
  (E/'COMMANDS.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(record),flush=True)
  if r.returncode!=0 or (count is not None and tests!=[count]):
   print(text[-22000:],flush=True);raise RuntimeError('failed command or test coverage: '+name)
 status='COMPLETED'
finally:
 sources={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in P.iterdir() if f.is_file() and f.suffix in ('.py','.md','.json')}
 meta={'execution_status':status,'sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'run':os.environ.get('GITHUB_RUN_ID'),
       'attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),'python':platform.python_version(),'dependencies':{n:importlib.metadata.version(n) for n in ('sympy','mpmath')},
       'commands':records,'tests_passed':sum(sum(r['tests']) for r in records if r['exit_code']==0),'sources':sources,'scope':'v16.29 + 198 retained-research regressions; unrelated protein engine excluded'}
 (E/'EXECUTION.json').write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
 (E/'SOURCE.zip').write_bytes(subprocess.check_output(['git','archive','--format=zip','HEAD',str(P.relative_to(ROOT)),'.github/workflows/uqcf-v1629-local-profile.yml'],cwd=ROOT))
 files=sorted(f for f in E.rglob('*') if f.is_file() and f.name!='SHA256SUMS')
 (E/'SHA256SUMS').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(E))+'\n' for f in files))
