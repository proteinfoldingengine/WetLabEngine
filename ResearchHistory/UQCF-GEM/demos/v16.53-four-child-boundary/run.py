"""Inherited 1150 checks, 42 frozen controls, fresh 45-file science."""
from pathlib import Path
import sys,subprocess,re,time,json,os,base64,zipfile,io,hashlib,ast
from integrity import HERE,OLD,INFRA,dump,run_commands,source_map,package,legacy,current_test_manifest,MODULES,COUNTS
PY=sys.executable
def logged(argv,path,count):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    result=subprocess.run(argv,capture_output=True,text=True);s=result.stdout+result.stderr;path.write_text(s)
    if result.returncode or list(map(int,re.findall(r'Ran (\d+) tests? in',s)))!=[count] or not re.search(r'^OK$',s,re.M):raise ValueError('test command failed: '+str(argv))
def audit_red(prefix,expected):
    receipt=json.loads((HERE/(prefix+'_RECEIPT.json')).read_text());data=base64.b64decode((HERE/(prefix+'.zip.b64')).read_bytes())
    if 'sha256:'+hashlib.sha256(data).hexdigest()!=receipt['digest']:raise ValueError('RED original archive digest')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        result=json.loads(z.read('RESULT.json'))
        if result['head']!=receipt['head'] or int(result['run'])!=receipt['run'] or result['errors'] or result['failures']!=expected:raise ValueError('RED provenance/outcome')
        all_logs=''
        for module in result['phase']['modules']:
            source=z.read('source/'+module+'.py').decode();log=z.read(module+'.log').decode();all_logs+=log
            path=str((HERE/(module+'.py')).relative_to(Path.cwd()))
            if subprocess.check_output(['git','show',receipt['head']+':'+path]).decode()!=source:raise ValueError('RED Git source binding')
            ids=sorted('__main__.'+c.name+'.'+f.name for c in ast.parse(source).body if isinstance(c,ast.ClassDef) for f in c.body if isinstance(f,ast.FunctionDef) and f.name.startswith('test_'))
            seen=sorted(re.findall(r'^test_\w+ \(([^)]+)\) \.\.\. (?:ok|FAIL)$',log,re.M))
            if ids!=seen or 'ERROR:' in log:raise ValueError('RED exact test identities')
        if any(s not in all_logs for s in result['phase']['signatures']):raise ValueError('RED assertion signature')
        for name,digest in result['source'].items():
            if hashlib.sha256(z.read('source/'+name)).hexdigest()!=digest:raise ValueError('RED source digest')
    return all_logs
def preflight(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);source_map(check_execution=True);current_test_manifest()
    subprocess.run([PY,str(OLD/'run.py'),'preflight',str(out/'parent52')],check=True)
    os.environ['V1653_TEST_OUTPUT']=str((out/'attempts').resolve())
    for module,count in zip(MODULES,COUNTS):logged([PY,str(HERE/(module+'.py'))],out/(module+'.log'),count)
    for prefix,count in [('PREIMPLEMENTATION_RED',2),('MECHANISMS_RED',2),('INTEGRATION_RED',10),('CAMPAIGN_RED',10),('REVIEW_RED',3)]:
        (out/(prefix+'.log')).write_text(audit_red(prefix,count))
def phase(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);preflight(out/'preflight');tick=time.perf_counter()
    commands=run_commands({'science':[PY,str(HERE/'run_campaign.py'),str(out/'scientific')],'inherited':[PY,str(INFRA/'run.py'),'inherited',str(out/'inherited')]},out/'logs')
    legacy.compare_suites(json.loads((INFRA/'evidence/science/inherited/optimized-fixtures.json').read_text()),json.loads((out/'inherited/optimized-fixtures.json').read_text()))
    dump(out/'METRICS.json',{'inherited_tests':1150,'new_controls':42,'all_commands_passed':True,'independent_verifier_recomputed':True,'parallel_seconds':time.perf_counter()-tick,'commands':commands})
if __name__=='__main__':
    cmd,out=sys.argv[1:3]
    if cmd=='preflight':preflight(out)
    elif cmd=='phase':phase(out)
    elif cmd=='package':package(out,sys.argv[3])
    else:raise ValueError(cmd)
