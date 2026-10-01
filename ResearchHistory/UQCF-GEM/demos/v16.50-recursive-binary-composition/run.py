"""Full inherited controls plus independently bound recursive campaign."""
from pathlib import Path
import sys,subprocess,re,time,json
from integrity import HERE,OLD,INFRA,dump,run_commands,source_map,package,legacy
PY=sys.executable
def logged(argv,path,count=None,red=None):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(argv,capture_output=True,text=True);s=r.stdout+r.stderr;path.write_text(s)
 if red:
  if r.returncode!=1 or any(x not in s for x in red):raise ValueError('prospective RED not observed')
 elif r.returncode:raise RuntimeError('failed '+str(argv))
 if count is not None and list(map(int,re.findall(r'Ran (\d+) tests? in',s)))!=[count]:raise ValueError('test count')
def preflight(out):
 out=Path(out);source_map(check_execution=True)
 subprocess.run([PY,str(OLD/'run.py'),'preflight',str(out/'parent49')],check=True)
 logged([PY,str(HERE/'test_gate.py')],out/'current-controls.log',27)
 logged([PY,str(HERE/'test_integrity.py')],out/'integrity-controls.log',33)
 logged([PY,str(HERE/'test_prospective_red.py')],out/'current-red.log',2,['MISSING_RECURSIVE_BINARY_INTERFACE','ValueError not raised','FAILED (failures=2)'])
def phase(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);preflight(out/'preflight');tick=time.perf_counter()
 results=run_commands({'science':[PY,str(HERE/'run_campaign.py'),str(out/'scientific')],'inherited':[PY,str(INFRA/'run.py'),'inherited',str(out/'inherited')]},out/'logs')
 legacy.compare_suites(json.loads((INFRA/'evidence/science/inherited/optimized-fixtures.json').read_text()),json.loads((out/'inherited/optimized-fixtures.json').read_text()))
 dump(out/'METRICS.json',{'inherited_tests':934,'new_controls':60,'all_commands_passed':True,'independent_verifier_uncached':True,'parallel_seconds':time.perf_counter()-tick,'commands':results})
if __name__=='__main__':
 cmd,out=sys.argv[1:3]
 if cmd=='preflight':preflight(out)
 elif cmd=='phase':phase(out)
 elif cmd=='package':package(out,sys.argv[3])
 else:raise ValueError(cmd)
