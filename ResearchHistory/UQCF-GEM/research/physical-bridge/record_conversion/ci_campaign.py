"""Execution plumbing: preserve exact inputs, per-suite logs and reproduction."""
import hashlib, json, os, pathlib, re, shutil, subprocess, sys
ROOT=pathlib.Path('research_snapshot').resolve()
BASE=ROOT/'ResearchHistory/UQCF-GEM/research/physical-bridge'
HERE=BASE/'record_conversion'
NATIVE=ROOT/'ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary'
SUITES=[('record_conversion','test_conversion.py'),('escape_obstruction','test_obstruction.py'),('reserve_activation','test_activation.py'),('source_escape','test_escape.py'),('cover_static','test_cover_static.py'),('nonuniform_reserve','test_nonuniform.py'),('weak_trace','test_weak.py'),('fingerprint_lock','test_fingerprint.py'),('private_cover','test_private.py'),('moving_cover','test_moving.py'),('saturated_handover','test_saturated.py'),('slack_handover','test_slack.py'),('handover_graph','test_handover.py'),('anchored_release','test_anchored.py'),('local_progress','test_progress.py'),('capacity_gap','test_capacity.py'),('saturated_transfer','test_transfer.py'),('label_release','test_release.py'),('footprint','test_footprint.py'),('fixed_family','test_fixed_family.py'),('star_carrier','test_star.py')]
def sha(data):return hashlib.sha256(data).hexdigest()
def write(path,obj):path.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def run(args,cwd,log):
    with log.open('wb') as f:
        result=subprocess.run(args,cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
    print(log.name, 'exit',result.returncode,flush=True)
    if result.returncode:raise RuntimeError('command failed; complete log retained: '+str(log))
def manifest(out):
    write(out/'file_manifest.json',{str(p.relative_to(out)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(out.rglob('*')) if p.is_file() and p.name!='file_manifest.json'})
def check_manifest(out):
    m=json.loads((out/'file_manifest.json').read_text())
    actual={str(p.relative_to(out)) for p in out.rglob('*') if p.is_file() and p.name!='file_manifest.json'}
    if set(m)!=actual:raise ValueError('manifest membership')
    for name,info in m.items():
        data=(out/name).read_bytes()
        if info!={'bytes':len(data),'sha256':sha(data)}:raise ValueError('manifest hash '+name)
def provenance(out):
    commit=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
    if commit!=os.environ['GITHUB_SHA']:raise ValueError('workflow/scientific mismatch')
    write(out/'provenance.json',{'scientific_sha':commit,'workflow_sha':os.environ['GITHUB_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'run_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'freeze_commit':'9128d216c3b81da52c37a1e87f2021370bdb669e'})
def primary(out):
    run([sys.executable,str(HERE/'producer.py'),str(out/'certificate.json')],HERE,out/'producer.log')
    run([sys.executable,str(HERE/'independent.py'),str(out/'certificate.json'),str(out/'independent.json')],HERE,out/'independent.log')
    run([sys.executable,str(HERE/'native_crosscheck.py'),str(out/'certificate.json'),str(NATIVE),str(out/'native_check.json')],HERE,out/'native_check.log')
def main(mode):
    out=pathlib.Path('conversion_'+mode).resolve();out.mkdir(exist_ok=True)
    provenance(out)
    if mode=='verification':
        for name in ('producer.py','independent.py','test_conversion.py','native_crosscheck.py','ci_campaign.py','PLAN.md','ANALYTICAL_REVIEW.md','REVIEW_INPUT_SCOPE.md','red.log','source_readbacks.json','freeze_binding.json','CODE_REVIEW.md'):
            shutil.copyfile(HERE/name,out/name)
        for suffix in ('RESULT','SCOPE','REPORT'):
            name='COUPLED_C3_RECORD_CONVERSION_'+suffix+'.md';shutil.copyfile(BASE/name,out/name)
        shutil.copyfile(ROOT/'.github/scripts/c3_record_conversion_review.py',out/'c3_record_conversion_review.py')
        shutil.copyfile(ROOT/'.github/workflows/uqcf-gem-c3-record-conversion.yml',out/'uqcf-gem-c3-record-conversion.yml')
        # Bind all inherited analytical inputs to their actual checkout bytes.
        bound=out/'bound_sources';bound.mkdir()
        for item in json.loads((HERE/'source_readbacks.json').read_text()):
            data=(ROOT/item['path']).read_bytes()
            if sha(data)!=item['sha256']:raise ValueError('analytical source changed: '+item['path'])
            (bound/pathlib.Path(item['path']).name).write_bytes(data)
        # The imported coverage helper is included alongside the pinned native verifier.
        shutil.copyfile(NATIVE/'coverage.py',bound/'coverage.py')
        primary(out)
        counts={}
        for folder,test in SUITES:
            log=out/(folder+'_tests.log')
            run([sys.executable,'-m','unittest','-v',test],BASE/folder,log)
            text=log.read_text();matches=re.findall(r'^Ran (\d+) tests? in ',text,re.M)
            if len(matches)!=1 or not re.search(r'^OK\s*$',text,re.M):raise ValueError('unittest result missing')
            counts[folder]=int(matches[0])
        if counts['record_conversion']!=23 or sum(counts.values())!=527:raise ValueError('unexpected test count')
        write(out/'test_counts.json',{'per_suite':counts,'new':23,'inherited':sum(counts.values())-23,'total':sum(counts.values())})
    elif mode in ('reproduction','gate'):
        verification=pathlib.Path('conversion_verification').resolve();check_manifest(verification)
        if json.loads((verification/'provenance.json').read_text())['scientific_sha']!=os.environ['GITHUB_SHA']:raise ValueError('wrong evidence source')
        primary(out)
        for name in ('certificate.json','independent.json','native_check.json'):
            if (out/name).read_bytes()!=(verification/name).read_bytes():raise ValueError('fresh bytes mismatch '+name)
        write(out/'reproduction.json',{'status':'VERIFIED','byte_identical':['certificate.json','independent.json','native_check.json'],'certificate_sha256':sha((out/'certificate.json').read_bytes())})
        if mode=='gate':
            repro=pathlib.Path('conversion_reproduction');check_manifest(repro)
            if json.loads((repro/'provenance.json').read_text())['scientific_sha']!=os.environ['GITHUB_SHA']:raise ValueError('reproduction provenance')
            review=pathlib.Path('conversion_review');m=json.loads((review/'manifest.json').read_text());raw=(review/'review.txt').read_bytes()
            if m['response_sha256']!=sha(raw) or m['research_commit']!=os.environ['GITHUB_SHA'] or m['workflow_commit']!=os.environ['GITHUB_SHA']:raise ValueError('math review provenance')
            obj=json.loads(re.sub(r'^```(?:json)?\s*|\s*```$','',raw.decode()).strip())
            if obj['verdict']!='ACCEPTED' or obj['missing_assumptions'] or obj['counterexamples']:raise ValueError('math review not accepted')
            for name,digest in m['input_sha256'].items():
                path=verification/name[9:] if name.startswith('EVIDENCE/') else repro/name[13:] if name.startswith('REPRODUCTION/') else ROOT/name[7:] if name.startswith('SOURCE/') else BASE/name
                if sha(path.read_bytes())!=digest:raise ValueError('review input hash '+name)
            write(out/'publication_gate.json',{'status':'VERIFIED','mathematical_inputs_verified':len(m['input_sha256']),'response_sha256':sha(raw),'native_access_derived':False,'guaranteed_write':False})
    else:raise ValueError(mode)
    manifest(out)
if __name__=='__main__':main(sys.argv[1])
