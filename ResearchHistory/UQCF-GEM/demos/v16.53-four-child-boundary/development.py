"""Pinned GitHub-only development evidence; expected RED failures are explicit."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
phase=json.loads((HERE/'DEV_PHASE.json').read_text());failures=errors=0;logs=''
import re
for module in phase['modules']:
    p=subprocess.run([sys.executable,str(HERE/(module+'.py'))],capture_output=True,text=True)
    s=p.stdout+p.stderr;(out/(module+'.log')).write_text(s);logs+=s
    failures+=sum(map(int,re.findall(r'failures=(\d+)',s)))
    errors+=sum(map(int,re.findall(r'errors=(\d+)',s)))
    if p.returncode and not re.search(r'FAILED \(',s):raise RuntimeError('non-test failure '+module)
    if not re.search(r'Ran \d+ tests? in',s):raise RuntimeError('missing tests '+module)
sources={};prior_archives={}
for p in sorted(HERE.iterdir()):
    if p.is_file():
        b=p.read_bytes()
        if p.name.endswith('.zip.b64'):
            prior_archives[p.name]=hashlib.sha256(b).hexdigest();continue
        dest=out/'source'/p.name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(b);sources[p.name]=hashlib.sha256(b).hexdigest()
meta={'head':os.environ['GITHUB_SHA'],'run':os.environ['GITHUB_RUN_ID'],'phase':phase,'failures':failures,'errors':errors,'source':sources,'prior_archive_hashes':prior_archives}
(out/'RESULT.json').write_text(json.dumps(meta,sort_keys=True,indent=2)+'\n')
print(logs)
assert errors==0 and failures==phase['failures'],(failures,errors,phase)
assert all(signature in logs for signature in phase['signatures'])
