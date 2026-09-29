"""Full v16.31 pipeline. Preserve actual exit codes and historical failures."""
from pathlib import Path
import hashlib,importlib.metadata,json,os,platform,re,subprocess,sys,zipfile
P=Path(__file__).resolve().parent
ROOT=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=P,text=True).strip())
U=ROOT/'ResearchHistory/UQCF-GEM';E=P/'evidence';E.mkdir(exist_ok=True)
commands=[('v1631-review',P,['test_review.py'],4),('v1631-contract',P,['test_contract.py'],3),('v1631-tests',P,['test_gate.py'],28),
 ('producer',P,['producer.py'],None),('verifier',P,['verifier.py'],None),
 ('v1630',U/'demos/v16.30-interaction-component-closure',['test_gate.py'],5),
 ('v1629',U/'demos/v16.29-local-profile-closure',['test_gate.py'],30),
 ('v1628',U/'demos/v16.28-diamond-attribution-closure',['test_gate.py'],28),
 ('v1627-contract',U/'demos/v16.27-increment-attribution-closure/completion',['test_contract.py'],11),
 ('v1627-complete',U/'demos/v16.27-increment-attribution-closure/completion',['test_complete.py'],23),
 ('v1627-original',U/'demos/v16.27-increment-attribution-closure',['test_gate.py'],5),
 ('v1626',U/'demos/v16.26-consistency-increment-law',['test_gate.py'],8),
 ('v1625',U/'demos/v16.25-pruning-refinement-closure',['test_gate.py'],11),
 ('v1624',U/'demos/v16.24-consistency-order',['test_gate.py'],28),
 ('v1624-validation',U/'demos/v16.24-consistency-order',['test_validation.py'],2),
 ('v1623',U/'demos/v16.23-overlap-descent',['test_gate.py'],22),
 ('v1623-schema',U/'demos/v16.23-overlap-descent',['test_schema.py'],3),
 ('v1622',U/'demos/v16.22-response-selection-closure',['-m','unittest','discover','-v'],20),
 ('v1621',U/'foundational-closure-verification',['tests/test_fcv.py'],22),
 ('exact-parent',U/'demos/v15.56-response-selector-obstruction',['-m','unittest','-v','test_pruning_consistency_audit'],15)]
records=[];status='INVALID_EXECUTION';env=dict(os.environ,V27_VERIFIER='verifier',V27_EVIDENCE=str(E/'inherited-v27'),V31_LEGACY='0')
try:
 with (E/'legacy-contract-replay.log').open('wb') as log:
  r=subprocess.run([sys.executable,'test_contract.py'],cwd=P,env=dict(env,V31_LEGACY='1'),stdout=log,stderr=subprocess.STDOUT)
 legacy=json.loads((E/'LEGACY_CONTRACT.json').read_text())
 if r.returncode!=1 or legacy!={'legacy':True,'tests':3,'failures':3,'errors':0}:raise RuntimeError('legacy failure replay changed')
 (E/'LEGACY_REPLAY.json').write_text(json.dumps({'exit_code':r.returncode,'observed':legacy,'counted_as_passing_scientific_tests':False},indent=2)+'\n')
 for name,cwd,args,count in commands:
  cmd=[sys.executable]+args
  with (E/(name+'.log')).open('wb') as log:r=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
  text=(E/(name+'.log')).read_text();tests=[int(n) for n in re.findall(r'Ran (\d+) tests?',text)]
  record={'name':name,'cwd':str(cwd.relative_to(ROOT)),'command':cmd,'exit_code':r.returncode,'tests':tests}
  records.append(record);(E/'COMMANDS.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(record),flush=True)
  if r.returncode!=0 or (count is not None and tests!=[count]):print(text[-18000:],flush=True);raise RuntimeError('command/count failure '+name)
 status='COMPLETED'
finally:
 files=sorted(f for f in P.iterdir() if f.is_file() and f.suffix in ('.py','.md'))
 sources={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
 old=U/'demos/v16.30-interaction-component-closure/verifier.py';sources[str(old.relative_to(ROOT))]=hashlib.sha256(old.read_bytes()).hexdigest()
 meta={'execution_status':status,'sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
       'run':os.environ.get('GITHUB_RUN_ID'),'attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),'python':platform.python_version(),
       'dependencies':{n:importlib.metadata.version(n) for n in ('sympy','mpmath')},'commands':records,
       'tests_passed':sum(sum(r['tests']) for r in records if r['exit_code']==0),'sources':sources,
       'scope':'v16.31 and explicit inherited retained tests only; no unrelated files'}
 (E/'EXECUTION.json').write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
 with zipfile.ZipFile(E/'SOURCE.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
  for path in sorted(sources):z.write(ROOT/path,path)
 fs=sorted(f for f in E.rglob('*') if f.is_file() and f.name!='SHA256SUMS')
 (E/'SHA256SUMS').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(E))+'\n' for f in fs))
