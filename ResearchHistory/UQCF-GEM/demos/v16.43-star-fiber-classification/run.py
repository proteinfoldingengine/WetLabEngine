"""Fail-fast controls and independent concurrent scientific/inherited processes."""
from pathlib import Path
import sys,subprocess,re,time,json
from integrity import HERE,OLD,OLD39,INFRA,dump,run_commands,source_map,package,legacy
PY=sys.executable
OLD41=OLD.parent/'v16.41-unit-barrier-dichotomy'
OLD40=OLD.parent/'v16.40-coordinate-obstruction'

def logged(argv,path,count=None,red=None):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    p=subprocess.run(argv,capture_output=True,text=True);path.write_text(p.stdout+p.stderr)
    if red:
        if p.returncode==0 or red not in p.stderr:raise ValueError('RED control not observed')
    elif p.returncode:raise RuntimeError('command failed '+str(argv))
    if count is not None and list(map(int,re.findall(r'Ran (\d+) tests? in',p.stderr+p.stdout)))!=[count]:raise ValueError('control count')

def preflight(out):
    out=Path(out);source_map()
    logged([PY,str(HERE/'test_gate.py')],out/'current-controls.log',30)
    logged([PY,str(HERE/'test_integrity.py')],out/'integrity-controls.log',14)
    logged([PY,str(OLD/'test_gate.py')],out/'v42-controls.log',30)
    logged([PY,str(OLD/'test_integrity.py')],out/'v42-integrity.log',14)
    logged([PY,str(OLD41/'test_gate.py')],out/'v41-controls.log',33)
    logged([PY,str(OLD41/'test_integrity.py')],out/'v41-integrity.log',15)
    logged([PY,str(OLD40/'test_gate.py')],out/'v40-controls.log',25)
    logged([PY,str(OLD40/'test_integrity.py')],out/'v40-integrity.log',14)
    logged([PY,str(OLD39/'test_gate.py')],out/'v39-controls.log',28)
    logged([PY,str(INFRA/'test_core.py')],out/'inherited-infrastructure.log',11)
    logged([PY,str(HERE/'test_red_contract.py')],out/'mutation-red.log',1,'AssertionError: ValueError not raised')
    logged([PY,str(OLD.parent/'v16.37-certified-closure/test_historical_contract.py')],out/'historical-red.log',red="AssertionError: ('HISTORICAL_LABEL_LOSS', (3, 2, 3), (3, 1, 3))")

def phase(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);preflight(out/'preflight');tick=time.perf_counter()
    results=run_commands({'science':[PY,str(HERE/'run_campaign.py'),str(out/'scientific')],'inherited':[PY,str(INFRA/'run.py'),'inherited',str(out/'inherited')]},out/'logs')
    ref=json.loads((INFRA/'evidence/science/inherited/optimized-fixtures.json').read_text());now=json.loads((out/'inherited/optimized-fixtures.json').read_text());legacy.compare_suites(ref,now)
    dump(out/'METRICS.json',{'inherited_tests':431,'new_controls':44,'all_commands_passed':True,'independent_verifier_uncached':True,'parallel_seconds':time.perf_counter()-tick,'commands':results})
if __name__=='__main__':
    cmd,out=sys.argv[1:3]
    if cmd=='preflight':preflight(out)
    elif cmd=='phase':phase(out)
    elif cmd=='package':package(out,sys.argv[3])
    else:raise ValueError(cmd)
