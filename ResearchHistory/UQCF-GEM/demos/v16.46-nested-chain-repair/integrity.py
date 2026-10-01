"""v16.46 execution bindings; immutable parent sources plus explicit new sources."""
from pathlib import Path
import snapshot
import importlib.util,json,os,subprocess,sys,tarfile,gzip,io,re,hashlib
ROOT=Path.cwd();HERE=ROOT/'ResearchHistory/UQCF-GEM/demos/v16.46-nested-chain-repair'
OLD=HERE.parent/'v16.45-binary-fork-unit-barrier';OLD39=HERE.parent/'v16.39-theorem-validation';INFRA=ROOT/'tools/retained_ci'
PARENT='a859abae0d647daaa7167b4a98193e3d495bf3cb'
PREREG='9c0065b62f97fab1c35439201210b8bcfe0f3c7c'
WORKFLOW='.github/workflows/v16.46-nested-chain-repair.yml'
spec=importlib.util.spec_from_file_location('retained_core_v40',INFRA/'core.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
dump=legacy.dump;sha=legacy.sha;run_commands=legacy.run_commands
verify_manifest=legacy.verify_manifest;write_manifest=legacy.write_manifest
unpack_zip=legacy.unpack_zip;replace_directory=legacy.replace_directory

def anchored(path):return legacy.anchored_file(ROOT,PARENT,str(path.relative_to(ROOT)))

def source_map(check_execution=False):
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if check_execution and any(os.environ.get(key,head)!=head for key in ('GITHUB_SHA','GITHUB_WORKFLOW_SHA')):raise ValueError('execution head before science')
    if subprocess.check_output(['git','show','-s','--format=%P',PREREG],text=True).strip()!=PARENT:raise ValueError('prospective direct parent before science')
    subprocess.run(['git','merge-base','--is-ancestor',PREREG,head],check=True)
    protocol=str((HERE/'PREREGISTRATION.md').relative_to(ROOT))
    if subprocess.check_output(['git','show',PREREG+':'+protocol])!=(HERE/'PREREGISTRATION.md').read_bytes():raise ValueError('preregistration changed before execution')
    frozen_path=OLD/'evidence/science/SOURCE_MANIFEST.json';frozen=json.loads(anchored(frozen_path))
    for name,digest in frozen.items():
        if sha((ROOT/name).read_bytes())!=digest:raise ValueError('frozen parent source: '+name)
    sources=dict(frozen);sources[str(frozen_path.relative_to(ROOT))]=sha(frozen_path.read_bytes())
    fixture_reference=INFRA/'evidence/science/inherited/optimized-fixtures.json'
    sources[str(fixture_reference.relative_to(ROOT))]=sha(anchored(fixture_reference))
    for path in (OLD/'evidence/science/scientific').rglob('*'):
        if path.is_file():sources[str(path.relative_to(ROOT))]=sha(anchored(path))
    paths=list(HERE.glob('*.py'))+[p for p in HERE.glob('*.md') if p.name!='REPORT.md']+list(HERE.glob('RED_*'))+[ROOT/WORKFLOW,ROOT/'.github/workflows/v16.46-red.yml']
    for path in paths:sources[str(path.relative_to(ROOT))]=sha(path.read_bytes())
    tree={}
    for row in subprocess.check_output(['git','ls-tree','-r','--full-tree','HEAD'],text=True).splitlines():
        metadata,name=row.split('\t',1);mode,kind,oid=metadata.split()
        if kind=='blob':tree[name]=oid
    for name in sources:
        data=(ROOT/name).read_bytes();oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if tree.get(name)!=oid:raise ValueError('source differs from execution commit: '+name)
    return dict(sorted(sources.items()))

def scientific_equal(a,b):
    def files(root):
        root=Path(root);return {str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    aa,bb=files(a),files(b)
    expected={prefix+n for prefix in ('','parent45/','parent45/parent44/','parent45/parent44/parent43/','parent45/parent44/parent43/parent42/','parent45/parent44/parent43/parent42/parent41/','parent45/parent44/parent43/parent42/parent41/parent40/','parent45/parent44/parent43/parent42/parent41/parent40/parent39/') for n in ('CERTIFICATE.json.gz','SUMMARY.json','VERIFY.json')}
    if set(aa)!=expected or aa!=bb:raise ValueError('scientific membership/bytes differ')

def metadata_valid(m,head,run_id,attempt,phase):
    wanted={'head':head,'trigger_sha':head,'workflow_sha':head,'run_id':str(run_id),'run_attempt':str(attempt),'phase':phase,'verified_parent':PARENT,'preregistration':PREREG}
    if any(m.get(k)!=v for k,v in wanted.items()):raise ValueError('embedded provenance')

def package(out,phase):
    out=Path(out);head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    meta={'head':head,'trigger_sha':os.environ['GITHUB_SHA'],'workflow_sha':os.environ['GITHUB_WORKFLOW_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'run_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'phase':phase,'verified_parent':PARENT,'preregistration':PREREG,'python':sys.version}
    metadata_valid(meta,head,os.environ['GITHUB_RUN_ID'],os.environ['GITHUB_RUN_ATTEMPT'],phase)
    if subprocess.check_output(['git','show','-s','--format=%P',PREREG],text=True).strip()!=PARENT:raise ValueError('preregistration parent')
    subprocess.run(['git','merge-base','--is-ancestor',PREREG,head],check=True)
    protocol=str((HERE/'PREREGISTRATION.md').relative_to(ROOT))
    if subprocess.check_output(['git','show',PREREG+':'+protocol])!=(HERE/'PREREGISTRATION.md').read_bytes():raise ValueError('preregistration changed')
    import importlib.metadata
    meta['dependencies']={name:importlib.metadata.version(name) for name in ('sympy','mpmath')}
    if meta['dependencies']!={'sympy':'1.13.3','mpmath':'1.3.0'}:raise ValueError('dependency pins')
    dump(out/'METADATA.json',meta);sources=source_map();dump(out/'SOURCE_MANIFEST.json',sources)
    dump(out/'SOURCE_FORMAT.json',snapshot.FORMAT)
    snapshot.write(ROOT,sources,out/'SOURCE.tar.gz')
    write_manifest(out);verify_package(out)

def verify_package(out):
    out=Path(out);verify_manifest(out)
    expected=source_map();recorded=snapshot.read_json(out/'SOURCE_MANIFEST.json')
    if recorded!=expected:raise ValueError('source membership/content')
    snapshot.verify(out/'SOURCE.tar.gz',recorded,expected,snapshot.read_json(out/'SOURCE_FORMAT.json'))
    scientific_equal(out/'scientific',out/'scientific')
    parent_equal(out/'scientific/parent45',OLD/'evidence/science/scientific')
    metrics=json.loads((out/'METRICS.json').read_text())
    if metrics.get('inherited_tests')!=600 or metrics.get('new_controls')!=75 or not metrics.get('all_commands_passed'):raise ValueError('execution coverage')
    suites=json.loads((out/'inherited/SUITES.json').read_text())
    expected_paths=[s for s in (OLD39/'inherited.txt').read_text().splitlines() if s.strip()]
    expected_counts=[8,26,12,16,4,8,5,28,3,5,30,28,11,28,2,22,3,22]
    if [r['path'] for r in suites]!=expected_paths or [r['tests'] for r in suites]!=expected_counts:raise ValueError('retained suite membership')
    logs={f'inherited/suite-{i:02}.log':c for i,c in enumerate(expected_counts)}
    logs.update({'preflight/current-controls.log':42,'preflight/v45-controls.log':38,'preflight/v45-integrity.log':31,'preflight/v44-controls.log':37,'preflight/v44-integrity.log':19,'preflight/v43-controls.log':30,'preflight/v43-integrity.log':14,'preflight/v42-controls.log':30,'preflight/v42-integrity.log':14,'preflight/v41-controls.log':33,'preflight/v41-integrity.log':15,'preflight/v40-controls.log':25,'preflight/v40-integrity.log':14,'preflight/integrity-controls.log':33,'preflight/v39-controls.log':28,'preflight/inherited-infrastructure.log':11})
    for name,count in logs.items():
        content=(out/name).read_text()
        if list(map(int,re.findall(r'Ran (\d+) tests? in',content)))!=[count] or not re.search(r'^OK$',content,re.M):raise ValueError('retained passing test log '+name)
    commands=json.loads((out/'logs/COMMANDS.json').read_text())
    if set(commands)!={'science','inherited'} or any(r['returncode']!=0 for r in commands.values()):raise ValueError('execution commands')
    legacy.compare_suites(json.loads((INFRA/'evidence/science/inherited/optimized-fixtures.json').read_text()),json.loads((out/'inherited/optimized-fixtures.json').read_text()))
    if 'AssertionError: ValueError not raised' not in (out/'preflight/mutation-red.log').read_text():raise ValueError('mutation RED missing')
    if "AssertionError: ('HISTORICAL_LABEL_LOSS', (3, 2, 3), (3, 1, 3))" not in (out/'preflight/historical-red.log').read_text():raise ValueError('historical RED missing')
    if json.loads((out/'scientific/VERIFY.json').read_text()).get('status')!='VERIFIED':raise ValueError('science unverified')
    result=json.loads((out/'scientific/VERIFY.json').read_text())
    report=json.loads((out/'scientific/SUMMARY.json').read_text())
    validate_summary(report,result)
    print(json.dumps({'package':'VERIFIED','source_members':len(expected)}))


def parent_equal(a,b):
    def files(root):
        root=Path(root);return {str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    aa,bb=files(a),files(b)
    expected={prefix+n for prefix in ('','parent44/','parent44/parent43/','parent44/parent43/parent42/','parent44/parent43/parent42/parent41/','parent44/parent43/parent42/parent41/parent40/','parent44/parent43/parent42/parent41/parent40/parent39/') for n in ('CERTIFICATE.json.gz','SUMMARY.json','VERIFY.json')}
    if set(aa)!=expected or aa!=bb:raise ValueError('parent science membership/bytes')


def validate_summary(report,result):
    if report['finite_result']!=result or report['preregistered_outcome']!=result['outcome'] or report.get('general_claim')!='See independently reviewed THEOREM.md; finite results do not establish the universal unit-barrier claim.':raise ValueError('report outcome drift')
