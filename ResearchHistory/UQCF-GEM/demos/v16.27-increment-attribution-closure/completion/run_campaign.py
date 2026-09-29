"""Run the fixed v16.27 completion campaign; fail closed, record every executed command."""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys

P=Path(__file__).resolve().parent
ROOT=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=P,text=True).strip())
U=ROOT/'ResearchHistory/UQCF-GEM'
E=P/'evidence'
E.mkdir(exist_ok=True)
commands=[
    ('contract',P,['test_contract.py'],11),
    ('completion',P,['test_complete.py'],23),
    ('producer',P,['producer.py'],None),
    ('verifier',P,['verifier.py'],None),
    ('historical-v1627',P.parent,['test_gate.py'],5),
    ('v1626',U/'demos/v16.26-consistency-increment-law',['test_gate.py'],8),
    ('v1625',U/'demos/v16.25-pruning-refinement-closure',['test_gate.py'],11),
    ('v1624',U/'demos/v16.24-consistency-order',['test_gate.py'],28),
    ('v1624-validation',U/'demos/v16.24-consistency-order',['test_validation.py'],2),
    ('v1623',U/'demos/v16.23-overlap-descent',['test_gate.py'],22),
    ('v1623-schema',U/'demos/v16.23-overlap-descent',['test_schema.py'],3),
    ('v1622',U/'demos/v16.22-response-selection-closure',['-m','unittest','discover','-v'],20),
    ('v1621',U/'foundational-closure-verification',['tests/test_fcv.py'],22),
    ('exact-parent',U/'demos/v15.56-response-selector-obstruction',['-m','unittest','-v','test_pruning_consistency_audit'],15),
    ('historical-producer',P.parent,['engine.py'],None)]
records=[]
env=dict(os.environ,V27_VERIFIER='verifier',V27_EVIDENCE=str(E))
status='INVALID_EXECUTION'
try:
    for name,cwd,args,count in commands:
        cmd=[sys.executable]+args
        with (E/(name+'.log')).open('wb') as log:
            result=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
        text=(E/(name+'.log')).read_text()
        tests=[int(x) for x in re.findall(r'Ran (\d+) tests?',text)]
        r={'name':name,'cwd':str(cwd.relative_to(ROOT)),'command':cmd,'exit_code':result.returncode,'tests':tests}
        records.append(r);(E/'COMMANDS.json').write_text(json.dumps(records,indent=2)+'\n')
        print(json.dumps(r),flush=True)
        if result.returncode!=0 or (count is not None and tests!=[count]):
            print(text[-14000:],flush=True);raise RuntimeError('execution or coverage failure: '+name)
    new=json.loads((E/'VERIFICATION.json').read_text())['original']
    old=json.loads((E/'historical-producer.log').read_text())
    comparison={k:{'original':old[k],'independent':new[n]} for k,n in [('endpoints','endpoints'),('multi_path','multi_path'),('paths','paths'),('path_dependent','dependent')]}
    matched=all(x['original']==x['independent'] for x in comparison.values())
    (E/'HISTORICAL_COMPARISON.json').write_text(json.dumps({'counts':comparison,'matched':matched,'note':'comparison only; independent verification did not call historical producer'},indent=2)+'\n')
    status='COMPLETED'
finally:
    folders=[P.parent,U/'demos/v16.26-consistency-increment-law',U/'demos/v16.25-pruning-refinement-closure',U/'demos/v16.24-consistency-order',U/'demos/v16.23-overlap-descent',U/'demos/v16.22-response-selection-closure',U/'foundational-closure-verification']
    sources={}
    for folder in folders:
        for f in folder.rglob('*.py'):
            if 'evidence' not in f.relative_to(folder).parts and '__pycache__' not in f.parts:sources[str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
    meta={'execution_status':status,'sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'run':os.environ.get('GITHUB_RUN_ID'),'attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
          'python':platform.python_version(),'dependencies':{n:importlib.metadata.version(n) for n in ('sympy','mpmath')},
          'commands':records,'tests_passed':sum(sum(r['tests']) for r in records if r['exit_code']==0),
          'source_sha256':sources,'scope':'v16.27 and stated retained-research regressions, not unrelated protein engine'}
    (E/'EXECUTION.json').write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
    archive=subprocess.check_output(['git','archive','--format=zip','HEAD',str(P.parent.relative_to(ROOT)),'.github/workflows/uqcf-v1627-completion.yml'],cwd=ROOT)
    (E/'SOURCE.zip').write_bytes(archive)
    files=sorted(f for f in E.rglob('*') if f.is_file() and f.name!='SHA256SUMS')
    (E/'SHA256SUMS').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(E))+'\n' for f in files))
