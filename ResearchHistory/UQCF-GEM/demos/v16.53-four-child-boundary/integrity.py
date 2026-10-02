"""v16.53 execution bindings; immutable parent sources plus explicit new sources."""
from pathlib import Path
import snapshot
import importlib.util,json,os,subprocess,sys,tarfile,gzip,io,re,hashlib,ast
ROOT=Path.cwd();HERE=ROOT/'ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary'
OLD=HERE.parent/'v16.52-recursive-ternary-composition';OLD39=HERE.parent/'v16.39-theorem-validation';INFRA=ROOT/'tools/retained_ci'
PARENT='b6bf95798ec5892963c29f4020f8b75069fd2e3b'
PREREG='8fcc46597ab7c2b83fe9dd2fd0611a07e66169cd'
WORKFLOW='.github/workflows/v16.53-four-child-boundary.yml'
spec=importlib.util.spec_from_file_location('retained_core_v40',INFRA/'core.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
dump=legacy.dump;sha=legacy.sha;run_commands=legacy.run_commands
verify_manifest=legacy.verify_manifest;write_manifest=legacy.write_manifest
unpack_zip=legacy.unpack_zip;replace_directory=legacy.replace_directory

def anchored(path):return legacy.anchored_file(ROOT,PARENT,str(path.relative_to(ROOT)))

MODULES=('test_bootstrap','test_gate','test_mechanisms','test_feasibility','test_lifting','test_integration','test_campaign','test_integrity','test_review')
COUNTS=(1,7,2,2,6,11,7,4,3)
def current_test_manifest():
    import bindings
    manifest=json.loads((HERE/'TEST_MANIFEST_CAMPAIGN.json').read_text())
    bindings.verify(manifest,{m:(HERE/(m+'.py')).read_text() for m in MODULES})
    if manifest['count']!=sum(COUNTS):raise ValueError('test total')
    return manifest

def source_map(check_execution=False):
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if check_execution and any(os.environ.get(key,head)!=head for key in ('GITHUB_SHA','GITHUB_WORKFLOW_SHA')):raise ValueError('execution head before science')
    if subprocess.check_output(['git','show','-s','--format=%P',PREREG],text=True).strip()!=PARENT:raise ValueError('prospective direct parent before science')
    subprocess.run(['git','merge-base','--is-ancestor',PREREG,head],check=True)
    protocol=str((HERE/'NATIVE_ADMISSIBILITY.md').relative_to(ROOT))
    if subprocess.check_output(['git','show',PREREG+':'+protocol])!=(HERE/'NATIVE_ADMISSIBILITY.md').read_bytes():raise ValueError('preregistration changed before execution')
    for ref,names in [('8216591e29f9bdda3065315d5650dbc3e8fd7160',('FOUR_CHILD_INTERFACE.md','INDEPENDENT_PROOF_REVIEW.md','SCOPE.md')),('f07526ea971117d0584782f62b3503dee5792d76',('EXECUTION_PLAN.md','VALIDATION_PROTOCOL.md'))]:
        for name in names:
            relative=str((HERE/name).relative_to(ROOT))
            if subprocess.check_output(['git','show',ref+':'+relative])!=(HERE/name).read_bytes():raise ValueError('accepted proof/approved plan changed')
    frozen_path=OLD/'evidence/science/SOURCE_MANIFEST.json';frozen=json.loads(anchored(frozen_path))
    for name,digest in frozen.items():
        if sha((ROOT/name).read_bytes())!=digest:raise ValueError('frozen parent source: '+name)
    sources=dict(frozen);sources[str(frozen_path.relative_to(ROOT))]=sha(frozen_path.read_bytes())
    fixture_reference=INFRA/'evidence/science/inherited/optimized-fixtures.json'
    sources[str(fixture_reference.relative_to(ROOT))]=sha(anchored(fixture_reference))
    for path in (OLD/'evidence/science/scientific').rglob('*'):
        if path.is_file():sources[str(path.relative_to(ROOT))]=sha(anchored(path))
    paths=[p for p in HERE.iterdir() if p.is_file() and p.name not in ('REPORT.md','PUBLICATION_MANIFEST.json')]+[ROOT/WORKFLOW,ROOT/'.github/workflows/v16.53-red.yml']
    for path in paths:sources[str(path.relative_to(ROOT))]=sha(path.read_bytes())
    tree={}
    for row in subprocess.check_output(['git','ls-tree','-r','--full-tree','HEAD'],text=True).splitlines():
        metadata,name=row.split('\t',1);mode,kind,oid=metadata.split()
        if kind=='blob':tree[name]=oid
    for name in sources:
        data=(ROOT/name).read_bytes();oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if tree.get(name)!=oid:raise ValueError('source differs from execution commit: '+name)
    return dict(sorted(sources.items()))

def science_files(root):
    root=Path(root);return {str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
def scientific_equal(a,b):
    aa,bb=science_files(a),science_files(b)
    parent=science_files(OLD/'evidence/science/scientific')
    expected={'CERTIFICATE.json.gz','SUMMARY.json','VERIFY.json'}|{'parent52/'+n for n in parent}
    if len(parent)!=42 or set(aa)!=expected or aa!=bb:raise ValueError('scientific membership/bytes differ')

def metadata_valid(m,head,run_id,attempt,phase):
    wanted={'head':head,'trigger_sha':head,'workflow_sha':head,'run_id':str(run_id),'run_attempt':str(attempt),'phase':phase,'verified_parent':PARENT,'preregistration':PREREG}
    if any(m.get(k)!=v for k,v in wanted.items()):raise ValueError('embedded provenance')

def package(out,phase):
    out=Path(out);head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    meta={'head':head,'trigger_sha':os.environ['GITHUB_SHA'],'workflow_sha':os.environ['GITHUB_WORKFLOW_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'run_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'phase':phase,'verified_parent':PARENT,'preregistration':PREREG,'python':sys.version}
    metadata_valid(meta,head,os.environ['GITHUB_RUN_ID'],os.environ['GITHUB_RUN_ATTEMPT'],phase)
    if subprocess.check_output(['git','show','-s','--format=%P',PREREG],text=True).strip()!=PARENT:raise ValueError('preregistration parent')
    subprocess.run(['git','merge-base','--is-ancestor',PREREG,head],check=True)
    protocol=str((HERE/'NATIVE_ADMISSIBILITY.md').relative_to(ROOT))
    if subprocess.check_output(['git','show',PREREG+':'+protocol])!=(HERE/'NATIVE_ADMISSIBILITY.md').read_bytes():raise ValueError('preregistration changed')
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
    parent_equal(out/'scientific/parent52',OLD/'evidence/science/scientific')
    metrics=json.loads((out/'METRICS.json').read_text())
    if metrics.get('inherited_tests')!=1150 or metrics.get('new_controls')!=43 or not metrics.get('all_commands_passed'):raise ValueError('execution coverage')
    suites=json.loads((out/'inherited/SUITES.json').read_text())
    expected_paths=[s for s in (OLD39/'inherited.txt').read_text().splitlines() if s.strip()]
    expected_counts=[8,26,12,16,4,8,5,28,3,5,30,28,11,28,2,22,3,22]
    if [r['path'] for r in suites]!=expected_paths or [r['tests'] for r in suites]!=expected_counts:raise ValueError('retained suite membership')
    logs={f'inherited/suite-{i:02}.log':c for i,c in enumerate(expected_counts)}
    logs.update({'preflight/parent52/parent51/parent50/parent49/current-controls.log': 56, 'preflight/parent52/parent51/parent50/parent49/v48-controls.log': 50, 'preflight/parent52/parent51/parent50/parent49/v48-integrity.log': 33, 'preflight/parent52/parent51/parent50/parent49/v47-controls.log': 54, 'preflight/parent52/parent51/parent50/parent49/v47-integrity.log': 33, 'preflight/parent52/parent51/parent50/parent49/v46-controls.log': 42, 'preflight/parent52/parent51/parent50/parent49/v46-integrity.log': 33, 'preflight/parent52/parent51/parent50/parent49/v45-controls.log': 38, 'preflight/parent52/parent51/parent50/parent49/v45-integrity.log': 31, 'preflight/parent52/parent51/parent50/parent49/v44-controls.log': 37, 'preflight/parent52/parent51/parent50/parent49/v44-integrity.log': 19, 'preflight/parent52/parent51/parent50/parent49/v43-controls.log': 30, 'preflight/parent52/parent51/parent50/parent49/v43-integrity.log': 14, 'preflight/parent52/parent51/parent50/parent49/v42-controls.log': 30, 'preflight/parent52/parent51/parent50/parent49/v42-integrity.log': 14, 'preflight/parent52/parent51/parent50/parent49/v41-controls.log': 33, 'preflight/parent52/parent51/parent50/parent49/v41-integrity.log': 15, 'preflight/parent52/parent51/parent50/parent49/v40-controls.log': 25, 'preflight/parent52/parent51/parent50/parent49/v40-integrity.log': 14, 'preflight/parent52/parent51/parent50/parent49/integrity-controls.log': 33, 'preflight/parent52/parent51/parent50/parent49/v39-controls.log': 28, 'preflight/parent52/parent51/parent50/parent49/inherited-infrastructure.log': 11, 'preflight/parent52/parent51/parent50/current-controls.log': 27, 'preflight/parent52/parent51/parent50/integrity-controls.log': 33, 'preflight/parent52/parent51/current-controls.log': 44, 'preflight/parent52/parent51/integrity-controls.log': 33})
    logs.update({'preflight/parent52/current-controls.log':41,'preflight/parent52/integrity-controls.log':33,'preflight/parent52/recursive-behavior.log':2,'preflight/parent52/review-controls.log':3})
    logs.update({'preflight/'+m+'.log':c for m,c in zip(MODULES,COUNTS)})
    for name,count in logs.items():
        content=(out/name).read_text()
        if list(map(int,re.findall(r'Ran (\d+) tests? in',content)))!=[count] or not re.search(r'^OK$',content,re.M):raise ValueError('retained passing test log '+name)
    inherited=json.loads((HERE/'TEST_MANIFEST_INHERITED.json').read_text())
    if inherited['count']!=1150 or inherited['parent']!=PARENT:raise ValueError('inherited manifest binding')
    actual_count=0
    for name,entry in inherited['suites'].items():
        text=(ROOT/name).read_text()
        if sha(text.encode())!=entry['source_sha256']:raise ValueError('inherited assertion source')
        found=[]
        for cls in ast.parse(text).body:
            if isinstance(cls,ast.ClassDef):
                for node in cls.body:
                    if isinstance(node,ast.FunctionDef) and node.name.startswith('test_'):found.append({'identity':cls.name+'.'+node.name,'expected':'PASS','assertions_sha256':sha(ast.get_source_segment(text,node).encode())})
        if found!=entry['tests'] or len(found)!=entry['count']:raise ValueError('inherited exact identities/assertions')
        actual_count+=len(found)
    if actual_count!=1150:raise ValueError('inherited identity count')
    manifest=current_test_manifest()
    for module,log in ((m,'preflight/'+m+'.log') for m in MODULES):
        text=(out/log).read_text()
        identities=sorted(re.findall(r'^test_\w+ \(([^)]+)\) \.\.\. ok$',text,re.M))
        expected_ids=sorted(r['identity'].replace(module+'.','__main__.',1) for r in manifest['tests'] if r['identity'].startswith(module+'.'))
        if identities!=expected_ids:raise ValueError('exact test identities '+module)
    if sum(logs.values())!=1193:raise ValueError('full test count')
    commands=json.loads((out/'logs/COMMANDS.json').read_text())
    if set(commands)!={'science','inherited'} or any(r['returncode']!=0 for r in commands.values()):raise ValueError('execution commands')
    legacy.compare_suites(json.loads((INFRA/'evidence/science/inherited/optimized-fixtures.json').read_text()),json.loads((out/'inherited/optimized-fixtures.json').read_text()))
    if "AssertionError: None is not an instance of <class 'list'>" not in (out/'preflight/parent52/parent51/parent50/parent49/fork-red.log').read_text():raise ValueError('fork RED missing')
    if "AssertionError: None is not an instance of <class 'list'>" not in (out/'preflight/parent52/parent51/parent50/parent49/recursive-red.log').read_text():raise ValueError('recursive RED missing')
    if "AssertionError: None is not an instance of <class 'list'>" not in (out/'preflight/parent52/parent51/parent50/parent49/saturated-red.log').read_text():raise ValueError('saturated RED missing')
    if 'AssertionError: ValueError not raised' not in (out/'preflight/parent52/parent51/parent50/parent49/mutation-red.log').read_text():raise ValueError('mutation RED missing')
    if "AssertionError: ('HISTORICAL_LABEL_LOSS', (3, 2, 3), (3, 1, 3))" not in (out/'preflight/parent52/parent51/parent50/parent49/historical-red.log').read_text():raise ValueError('historical RED missing')
    red=(out/'preflight/parent52/parent51/parent50/current-red.log').read_text()
    if 'MISSING_RECURSIVE_BINARY_INTERFACE' not in red or 'ValueError not raised' not in red or 'FAILED (failures=2)' not in red:raise ValueError('prospective RED missing')
    if json.loads((out/'scientific/VERIFY.json').read_text()).get('status')!='VERIFIED':raise ValueError('science unverified')
    result=json.loads((out/'scientific/VERIFY.json').read_text())
    report=json.loads((out/'scientific/SUMMARY.json').read_text())
    validate_summary(report,result)
    print(json.dumps({'package':'VERIFIED','source_members':len(expected)}))


def parent_equal(a,b):
    aa,bb=science_files(a),science_files(b)
    if len(aa)!=42 or aa!=bb:raise ValueError('parent science membership/bytes')


def validate_summary(report,result):
    if report['finite_result']!=result or report['preregistered_outcome']!=result['outcome'] or report.get('general_claim')!='See independently reviewed FOUR_CHILD_INTERFACE.md for finite ordered arity2/3/4 trees; finite cases validate implementation and do not replace the proof.':raise ValueError('report outcome drift')
