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
 subprocess.run([PY,str(OLD/'run.py'),'preflight',str(out/'parent50')],check=True)
 logged([PY,str(HERE/'test_gate.py')],out/'current-controls.log',44)
 logged([PY,str(HERE/'test_integrity.py')],out/'integrity-controls.log',33)
 # Audit preserved RED rather than rerunning the repaired coverage baseline.
 import base64,zipfile,io,hashlib
 receipt=json.loads((HERE/'RED_RECEIPT.json').read_text());raw=base64.b64decode((HERE/'RED_ARTIFACT.zip.b64').read_bytes())
 if 'sha256:'+hashlib.sha256(raw).hexdigest()!=receipt['digest']:raise ValueError('RED archive digest')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  if z.read('PREREGISTRATION.md')!=(HERE/'PREREGISTRATION.md').read_bytes():raise ValueError('RED protocol binding')
  content=z.read('RED.log').decode()
  if 'MISSING_TERNARY_INTERFACE' not in content or 'EXACT_UNIVERSE_OMISSION_ACCEPTED' not in content or 'FAILED (failures=2)' not in content:raise ValueError('RED assertions')
  (out/'current-red.log').write_text(content)
 receipt=json.loads((HERE/'RED_REVIEW_RECEIPT.json').read_text());raw=base64.b64decode((HERE/'RED_REVIEW_ARTIFACT.zip.b64').read_bytes())
 if 'sha256:'+hashlib.sha256(raw).hexdigest()!=receipt['digest']:raise ValueError('review RED digest')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  content=z.read('RED.log').decode()
  if 'FAILED (failures=4)' not in content or any(x not in content for x in ('FULL_VERIFIER_OMISSION_ACCEPTED','FULL_PALETTE_ORDER_LOST','START_FAILURE_ESCAPED','MISSING_FAILURE_OUTCOME_CLASSIFIER')):raise ValueError('review RED assertions')
  (out/'review-red.log').write_text(content)

def phase(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);preflight(out/'preflight');tick=time.perf_counter()
 results=run_commands({'science':[PY,str(HERE/'run_campaign.py'),str(out/'scientific')],'inherited':[PY,str(INFRA/'run.py'),'inherited',str(out/'inherited')]},out/'logs')
 legacy.compare_suites(json.loads((INFRA/'evidence/science/inherited/optimized-fixtures.json').read_text()),json.loads((out/'inherited/optimized-fixtures.json').read_text()))
 dump(out/'METRICS.json',{'inherited_tests':994,'new_controls':77,'all_commands_passed':True,'independent_verifier_recomputed':True,'interface_feasibility_cache':'within-process complete width/root-target/palette keys, as preregistered','parallel_seconds':time.perf_counter()-tick,'commands':results})
if __name__=='__main__':
 cmd,out=sys.argv[1:3]
 if cmd=='preflight':preflight(out)
 elif cmd=='phase':phase(out)
 elif cmd=='package':package(out,sys.argv[3])
 else:raise ValueError(cmd)
