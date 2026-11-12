"""Rerun the unchanged inherited FCV stack; preserve every exit and log."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
ROOT=Path.cwd(); P=ROOT/'ResearchHistory/UQCF-GEM/foundational-closure-verification'
D=ROOT/'ResearchHistory/UQCF-GEM/demos'; mode=sys.argv[1]
assert mode in ('verify','replay')
out=ROOT/('rd8_stack' if mode=='verify' else 'rd8_replay');out.mkdir(exist_ok=True)
rows=[]
def call(name,argv,cwd):
    with (out/(name+'.log')).open('wb') as f:
        r=subprocess.run(argv,cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
    rows.append(dict(stage=name,command=argv,cwd=str(Path(cwd).relative_to(ROOT)),exit_code=r.returncode))
    (out/'commands.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(name, 'exit',r.returncode,flush=True)
    if r.returncode: raise RuntimeError('Inherited stage failed: '+name)
def save_manifest():
    data={str(f.relative_to(out)):{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(out.rglob('*')) if f.is_file() and f.name!='artifact_manifest.json'}
    (out/'artifact_manifest.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
try:
    (P/'evidence').mkdir(exist_ok=True)
    if mode=='verify':
        call('rd8-exact-witnesses',[sys.executable,'.github/scripts/uqcf_rd8_witnesses.py'],ROOT)
        call('dependencies',[sys.executable,'-m','pip','freeze'],ROOT)
        call('fcv-tests',[sys.executable,'tests/test_fcv.py'],P)
        call('parent-tests',[sys.executable,'-m','unittest','-v','test_pruning_consistency_audit'],D/'v15.56-response-selector-obstruction')
        call('historical-tests',[sys.executable,'-m','unittest','-v'],D/'v16.15F-graded-obstruction-descent')
    call('historical-reproduction',[sys.executable,'gate.py'],D/'v16.15F-graded-obstruction-descent')
    shutil.copyfile(D/'v16.15F-graded-obstruction-descent/result.json',P/'evidence/REPRODUCED_1615F.json')
    call('producer',[sys.executable,'produce_certificates.py'],P)
    call('independent-verifier',[sys.executable,'verify_certificates.py'],P)
    names=['certificates.json.xz','PRODUCTION.json','VERIFICATION.json','REPRODUCED_1615F.json']
    for n in names: shutil.copyfile(P/'evidence'/n,out/n)
    assert json.loads((out/'VERIFICATION.json').read_text())['all_valid'] is True
    if mode=='replay':
        first=ROOT/'rd8_stack'
        for n in names: assert (out/n).read_bytes()==(first/n).read_bytes(), 'Fresh reproduction mismatch: '+n
    if mode=='verify':
        prefixes=[str(P.relative_to(ROOT)),str((D/'v15.56-response-selector-obstruction').relative_to(ROOT)),str((D/'v16.15F-graded-obstruction-descent').relative_to(ROOT))]
        candidates=subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD',*prefixes],text=True).splitlines()
        paths=[p for p in candidates if '/evidence/' not in p and p.endswith(('.py','.json','.md','.txt'))]
        paths += subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD','ResearchHistory/UQCF-GEM/research/physical-bridge/rd8_correction_review'],text=True).splitlines()
        paths += [str(p.relative_to(ROOT)) for p in (ROOT/'.github/scripts').glob('uqcf_rd8_*.py')]
        paths += ['.github/scripts/uqcf_preparability_review.py','.github/workflows/uqcf-rd8-correction-review.yml']
        with (out/'source-snapshot.zip').open('wb') as f: subprocess.run(['git','archive','--format=zip','HEAD',*paths],stdout=f,check=True)
    receipt=dict(status='PASS',mode=mode,checkout_sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),workflow_sha=os.environ.get('UQCF_WORKFLOW_SHA'),run_id=os.environ.get('GITHUB_RUN_ID'),run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),commands=rows,fresh_byte_reproduction=mode=='replay',native_bridge='NOT_DERIVED')
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
except Exception as exc:
    (out/'failure.json').write_text(json.dumps(dict(status='FAILED',error_type=type(exc).__name__,detail=str(exc)),indent=2)+'\n')
    raise
finally: save_manifest()
