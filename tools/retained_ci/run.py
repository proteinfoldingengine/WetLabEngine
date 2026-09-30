"""Fail-fast preflight, full parallel replay and measured inherited fixture reuse."""
from pathlib import Path
import subprocess,sys,time,json,re
from core import STAGE,HERE,dump,run_commands,scientific_equal,compare_suites,package
PY=sys.executable

def logged(argv,path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w') as f:subprocess.run(argv,stdout=f,stderr=subprocess.STDOUT,check=True)

def preflight(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    logged([PY,str(HERE/'test_core.py')],out/'infrastructure.log')
    logged([PY,str(STAGE/'test_gate.py')],out/'current-controls.log')
    logged([PY,str(STAGE/'publication.py'),'verify'],out/'frozen-publication.log')
    p=subprocess.run([PY,str(STAGE.parent/'v16.37-certified-closure/test_historical_contract.py')],capture_output=True,text=True)
    (out/'historical-red.log').write_text(p.stdout+p.stderr)
    if p.returncode==0 or "AssertionError: ('HISTORICAL_LABEL_LOSS', (3, 2, 3), (3, 1, 3))" not in p.stderr:raise ValueError('historical RED not preserved')

def inherited(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    subprocess.run([PY,str(STAGE.parent/'v16.38-six-vertex-barriers/replay_parent.py')],check=True)
    paths=[p for p in (STAGE/'inherited.txt').read_text().splitlines() if p.strip()]
    expected=[8,26,12,16,4,8,5,28,3,5,30,28,11,28,2,22,3,22]
    if len(paths)!=len(expected):raise ValueError('inherited command membership')
    records=[]
    for index,(path,count) in enumerate(zip(paths,expected)):
        argv=[PY,path]
        if '/v16.36-' in path:argv=[PY,str(HERE/'fixture_suite.py'),str(out/'optimized-fixtures.json'),'reuse']
        tick=time.perf_counter();log=out/f'suite-{index:02}.log';logged(argv,log)
        counts=list(map(int,re.findall(r'Ran (\d+) tests? in',log.read_text())))
        if counts!=[count]:raise ValueError('inherited test count '+path)
        records.append({'path':path,'tests':count,'seconds':time.perf_counter()-tick})
    dump(out/'SUITES.json',records);print(json.dumps({'inherited_tests':sum(x['tests'] for x in records),'commands':len(records)}))

def phase(out,benchmark=False):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);preflight(out/'preflight')
    if benchmark:logged([PY,str(HERE/'fixture_suite.py'),str(out/'baseline-fixtures.json'),'baseline'],out/'baseline-fixtures.log')
    tick=time.perf_counter()
    commands={'science':[PY,str(STAGE/'run_campaign.py'),str(out/'scientific')],'inherited':[PY,str(HERE/'run.py'),'inherited',str(out/'inherited')]}
    timings=run_commands(commands,out/'logs');elapsed=time.perf_counter()-tick
    scientific_equal(out/'scientific',STAGE/'evidence/science/scientific')
    metrics={'parallel_phase_seconds':elapsed,'commands':timings,'inherited_tests':261,'current_controls':28,'scientific_bytes_identical':True}
    optimized=json.loads((out/'inherited/optimized-fixtures.json').read_text())
    if benchmark:
        baseline=json.loads((out/'baseline-fixtures.json').read_text());compare_suites(baseline,optimized)
        metrics['fixture_benchmark']={'baseline_seconds':baseline['seconds'],'optimized_seconds':optimized['seconds'],'ratio':baseline['seconds']/optimized['seconds'],'baseline_producer_seconds':baseline['producer_seconds'],'optimized_producer_seconds':optimized['producer_seconds'],'baseline_generations':baseline['producer_generations'],'optimized_generations':optimized['producer_generations'],'verifier_calls_each':optimized['verifier_calls'],'same_runner':True,'limitation':'single paired run; optimized suite shares CPU with concurrent science'}
    else:
        reference=json.loads((HERE/'evidence/science/inherited/optimized-fixtures.json').read_text()) if (HERE/'evidence/science').exists() else json.loads(Path('out/download/science/inherited/optimized-fixtures.json').read_text())
        compare_suites(reference,optimized)
    dump(out/'METRICS.json',metrics);print(json.dumps(metrics))

if __name__=='__main__':
    cmd,out=sys.argv[1:3]
    if cmd=='preflight':preflight(out)
    elif cmd=='inherited':inherited(out)
    elif cmd=='phase':phase(out,'--benchmark' in sys.argv)
    elif cmd=='package':package(out,sys.argv[3])
    else:raise ValueError(cmd)
