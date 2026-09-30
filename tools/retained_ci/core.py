"""Execution and integrity helpers. No scientific verifier results are cached."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import hashlib,json,shutil,subprocess,time,tarfile,gzip,io,os,sys,zipfile
ROOT=Path.cwd()
HERE=ROOT/'tools/retained_ci'
STAGE=ROOT/'ResearchHistory/UQCF-GEM/demos/v16.39-theorem-validation'
PARENT='e789ce42bac28e084a4f0264180b738534d69923'

def dump(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def sha(data):return hashlib.sha256(data).hexdigest()
def fixture_cache(fn):
    cache={}
    def fresh(bound=4):
        if bound not in cache:cache[bound]=deepcopy(fn(bound))
        return deepcopy(cache[bound])
    return fresh

def replace_directory(source,target):
    source,target=Path(source),Path(target)
    if not source.is_dir():raise ValueError('missing fresh directory')
    if source.resolve()==target.resolve() or source.resolve() in target.resolve().parents or target.resolve() in source.resolve().parents:raise ValueError('overlapping directories')
    if target.exists():shutil.rmtree(target)
    shutil.copytree(source,target)

def run_commands(commands,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    origin=time.perf_counter()
    def run(item):
        name,argv=item;start=time.perf_counter()
        with (out/(name+'.log')).open('w') as log:
            p=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT)
        return name,{'argv':argv,'returncode':p.returncode,'start_seconds':start-origin,'end_seconds':time.perf_counter()-origin}
    with ThreadPoolExecutor(max_workers=2) as pool:results=dict(pool.map(run,commands.items()))
    dump(out/'COMMANDS.json',results)
    if any(r['returncode'] for r in results.values()):raise RuntimeError('command failure; all peer logs retained')
    return results

def verify_manifest(root):
    root=Path(root);manifest=json.loads((root/'MANIFEST.json').read_text())
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json'}
    if set(manifest)!=actual:raise ValueError('manifest membership')
    for name,digest in manifest.items():
        if Path(name).is_absolute() or '..' in Path(name).parts or sha((root/name).read_bytes())!=digest:raise ValueError('manifest hash/path')
    return manifest

def write_manifest(root):
    root=Path(root)
    dump(root/'MANIFEST.json',{str(p.relative_to(root)):sha(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file() and p!=root/'MANIFEST.json'})

def scientific_equal(a,b):
    a,b=Path(a),Path(b);expected={'CERTIFICATE.json.gz','SUMMARY.json','VERIFY.json'}
    if {p.name for p in a.iterdir()}!=expected or {p.name for p in b.iterdir()}!=expected:raise ValueError('scientific membership')
    if any((a/n).read_bytes()!=(b/n).read_bytes() for n in expected):raise ValueError('scientific bytes changed')

def compare_suites(a,b):
    if not a['success'] or not b['success'] or a['tests']!=b['tests']:raise ValueError('test identities/outcomes changed')
    if a['fixture_hashes']!=b['fixture_hashes']:raise ValueError('fixture bytes changed')
    if a['verifier_calls']!=b['verifier_calls'] or not b['verifier_uncached']:raise ValueError('verifier coverage changed')

def source_paths():
    frozen=json.loads((STAGE/'evidence/science/SOURCE_MANIFEST.json').read_text())
    for p,h in frozen.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('frozen scientific source changed: '+p)
    paths={ROOT/p for p in frozen}
    paths.update(HERE.glob('*.py'));paths.add(HERE/'PROTOCOL.md')
    paths.add(ROOT/'.github/workflows/retained-ci-optimization.yml')
    return sorted(paths)

def source_map():return {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in source_paths()}

def package(out,phase):
    out=Path(out);head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if head!=os.environ['GITHUB_SHA'] or head!=os.environ['GITHUB_WORKFLOW_SHA']:raise ValueError('execution SHA mismatch')
    subprocess.run(['git','merge-base','--is-ancestor',PARENT,head],check=True)
    pre='9e234a484fa8943a380e95b8f781c4268cb0cc18'
    subprocess.run(['git','merge-base','--is-ancestor',pre,head],check=True)
    if subprocess.check_output(['git','show','-s','--format=%P',pre],text=True).strip()!=PARENT:raise ValueError('protocol parent')
    frozen=subprocess.check_output(['git','show',pre+':tools/retained_ci/PROTOCOL.md'])
    if frozen!=(HERE/'PROTOCOL.md').read_bytes():raise ValueError('protocol changed')
    metadata={'head':head,'trigger_sha':os.environ['GITHUB_SHA'],'workflow_sha':os.environ['GITHUB_WORKFLOW_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'run_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'phase':phase,'python':sys.version,'verified_parent':PARENT}
    dump(out/'METADATA.json',metadata);sources=source_map();dump(out/'SOURCE_MANIFEST.json',sources)
    with (out/'SOURCE.tar.gz').open('wb') as f:
        with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as gz:
            with tarfile.open(fileobj=gz,mode='w') as tf:
                for name in sources:
                    data=(ROOT/name).read_bytes();info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644;info.mtime=0;tf.addfile(info,io.BytesIO(data))
    write_manifest(out);verify_package(out)

def verify_package(out):
    out=Path(out);verify_manifest(out)
    expected=source_map();recorded=json.loads((out/'SOURCE_MANIFEST.json').read_text())
    if recorded!=expected:raise ValueError('source membership/content')
    with tarfile.open(out/'SOURCE.tar.gz','r:gz') as tf:
        members=tf.getmembers()
        if len(members)!=len(expected) or {m.name for m in members}!=set(expected):raise ValueError('source archive membership')
        for m in members:
            if not m.isfile() or sha(tf.extractfile(m).read())!=expected[m.name]:raise ValueError('source archive content')
    scientific_equal(out/'scientific',STAGE/'evidence/science/scientific')
    print(json.dumps({'package':'VERIFIED','source_members':len(expected)}))

def unpack_zip(data,digest,destination):
    if 'sha256:'+sha(data)!=digest:raise ValueError('API artifact digest')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or z.testzip() is not None:raise ValueError('ZIP duplicate/CRC')
        if any(Path(n).is_absolute() or '..' in Path(n).parts for n in names):raise ValueError('ZIP path')
        z.extractall(destination)
