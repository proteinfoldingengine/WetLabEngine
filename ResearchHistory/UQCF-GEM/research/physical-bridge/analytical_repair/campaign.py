"""Exact evidence, inherited regressions, reproduction and review provenance gates."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BASE=HERE.parent
SOURCE_PARENT='1ef7d25cedd5af6be6e72fea4e5963414a92cc0a'
CONTRACT_COMMIT='cbefdb85f21cd9606d1a9260d38176c2dc068b91'
CONTRACT_SHA256='77017270c4dbb26935940a4542982b5b0e528f5aebcc64771361df2be11a08aa'
BRIDGE='ResearchHistory/UQCF-GEM/research/physical-bridge/'
REPAIR=BRIDGE+'analytical_repair/'
FOUR=('covariant_refinement_boundary','center_access_growth','center_growth_law_screen','covariant_outcome_register')
SUITES=[('record_conversion','test_conversion.py'),('escape_obstruction','test_obstruction.py'),('reserve_activation','test_activation.py'),('source_escape','test_escape.py'),('cover_static','test_cover_static.py'),('nonuniform_reserve','test_nonuniform.py'),('weak_trace','test_weak.py'),('fingerprint_lock','test_fingerprint.py'),('private_cover','test_private.py'),('moving_cover','test_moving.py'),('saturated_handover','test_saturated.py'),('slack_handover','test_slack.py'),('handover_graph','test_handover.py'),('anchored_release','test_anchored.py'),('local_progress','test_progress.py'),('capacity_gap','test_capacity.py'),('saturated_transfer','test_transfer.py'),('label_release','test_release.py'),('footprint','test_footprint.py'),('fixed_family','test_fixed_family.py'),('star_carrier','test_star.py')]
MANDATORY_PATHS={
    *[BRIDGE+folder+'/'+name for folder in FOUR for name in ('RESULT.md','INDEX_APPEND.md','ANALYTICAL_REVIEW_RAW.md')],
    *[REPAIR+name for name in ('CONTRACT.md','CORRECTIONS.md','INDEX_APPEND.md','CODEX_ARGUMENT_REVIEW.md','STAGE1_AUDIT.md','STAGE1_SOURCE_EVIDENCE.json','STAGE1_REVIEW_BINDINGS.json','producer.py','independent.py','test_verification.py','test_infrastructure.py','campaign.py','red.log','publication_manifest.json')],
    '.github/workflows/uqcf-gem-analytical-repair.yml',
    '.github/scripts/uqcf_analytical_repair_review.py',
    'ResearchHistory/UQCF-GEM/AGENTS.md',
    'ResearchHistory/UQCF-GEM/v15/v15.11/REPORT.md',
    'ResearchHistory/UQCF-GEM/v15/v15.11/ontology_continuity_audit.py',
    *[BRIDGE+name for name in ('COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md','COUPLED_C3_PHYSICAL_FRONTIER_DECISION.md','NATIVE_EVENT_MILESTONE.md','STANDING_DIRECTIVE.md','covariant_outcome_register/REVIEW_RESPONSE.md','collective_covariance_candidate/RESULT.md','pruning_cover_record/RESULT.md','record_compatibility_bridge/RESULT.md','retained_reader_write/RESULT.md','record_conversion/ci_campaign.py')],
}


def safe_relative(name):
    if not isinstance(name,str) or not name or Path(name).is_absolute() or '..' in Path(name).parts or str(Path(name))!=name:
        raise ValueError('unsafe or noncanonical relative path')
    return name


def expected_provenance():
    sha=os.environ['GITHUB_SHA']
    workflow_sha=os.environ['UQCF_WORKFLOW_SHA']
    if not re.fullmatch('[0-9a-f]{40}',sha) or workflow_sha!=sha:
        raise ValueError('actual workflow/scientific SHA mismatch')
    return {'scientific_sha':sha,'workflow_sha':workflow_sha,
            'run_id':os.environ['GITHUB_RUN_ID'],'run_attempt':os.environ['GITHUB_RUN_ATTEMPT'],
            'source_parent':SOURCE_PARENT,'contract_commit':CONTRACT_COMMIT,
            'contract_sha256':CONTRACT_SHA256}


def validate_provenance(obj):
    for key,value in expected_provenance().items():
        if obj.get(key)!=value or type(obj.get(key)) is not type(value):
            raise ValueError('upstream provenance mismatch: '+key)


def upstream(directory):
    check_manifest(directory)
    name='review_manifest.json' if directory.name in ('repair_review','repair_publication') else 'provenance.json'
    validate_provenance(json.loads((directory/name).read_text()))


def publication_paths():
    publication=json.loads((HERE/'publication_manifest.json').read_text())
    if publication.get('source_parent')!=SOURCE_PARENT or publication.get('contract_commit')!=CONTRACT_COMMIT:
        raise ValueError('publication manifest provenance')
    paths=publication['changed_paths']
    if not isinstance(paths,list) or not paths or paths!=sorted(set(paths)):
        raise ValueError('publication paths must be sorted and unique')
    for name in paths:safe_relative(name)
    return set(paths)


def validate_inputs(bound):
    if bound.get('source_parent')!=SOURCE_PARENT or bound.get('contract_commit')!=CONTRACT_COMMIT:
        raise ValueError('input manifest frozen source identity mismatch')
    files=bound['files']
    required=MANDATORY_PATHS | (publication_paths()-{REPAIR+'input_manifest.json'})
    if not required.issubset(files):
        raise ValueError('missing required source paths: '+repr(sorted(required-set(files))))
    for name in files:safe_relative(name)
    if digest((HERE/'CONTRACT.md').read_bytes())!=CONTRACT_SHA256:
        raise ValueError('prospective contract bytes changed')
    if files[REPAIR+'CONTRACT.md']['sha256']!=CONTRACT_SHA256:
        raise ValueError('manifest contract hash changed')

def validate_review_verdict(verdict):
    if verdict.get('verdict')!='ACCEPTED' or any(verdict.get(key)!=[] for key in ('missing_assumptions','counterexamples','findings')):
        raise ValueError('review unresolved or incomplete')


def validate_remote_commits(commit, compare, publication):
    """Bind cumulative repair history and the current head's direct parent."""
    sha=os.environ['GITHUB_SHA']
    prior=publication.get('prior_repair_commits',[])
    if (not isinstance(prior,list) or any(not isinstance(item,str) or not re.fullmatch('[0-9a-f]{40}',item) for item in prior)
            or len(set(prior))!=len(prior) or sha in prior or CONTRACT_COMMIT in prior):
        raise ValueError('invalid prior repair commit identities')
    expected=prior+[sha]
    parent=prior[-1] if prior else CONTRACT_COMMIT
    if commit.get('sha')!=sha or [p['sha'] for p in commit['parents']]!=[parent]:
        raise ValueError('remote commit parent mismatch')
    commits=compare.get('commits',[])
    if (type(compare.get('total_commits')) is not int or compare['total_commits']!=len(expected)
            or [item['sha'] for item in commits]!=expected):
        raise ValueError('remote cumulative commit identity mismatch')
    parent=CONTRACT_COMMIT
    for item in commits:
        if [p['sha'] for p in item['parents']]!=[parent]:
            raise ValueError('remote cumulative commit parent mismatch')
        parent=item['sha']


def validate_remote(directory):
    audit=json.loads((directory/'remote_readback.json').read_text())
    sha=os.environ['GITHUB_SHA']
    bound=json.loads((HERE/'input_manifest.json').read_text())
    validate_inputs(bound)
    required=publication_paths() | set(bound['files'])
    if audit.get('verified') is not True or audit.get('scientific_sha')!=sha or audit.get('parent')!=CONTRACT_COMMIT or audit.get('continuation_parent')!=SOURCE_PARENT:
        raise ValueError('remote publication audit identity mismatch')
    if set(audit.get('files',{}))!=required:
        raise ValueError('remote publication path set mismatch')
    for name,info in audit['files'].items():
        data=(ROOT/safe_relative(name)).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if info!={'bytes':len(data),'sha256':digest(data),'git_blob':blob,'ref':sha}:
            raise ValueError('remote publication bytes mismatch: '+name)
    appendix=(HERE/'INDEX_APPEND.md').read_bytes()
    current=(BASE/'COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md').read_bytes()
    if not appendix or not current.endswith(appendix):
        raise ValueError('continuation appendix mismatch')
    prior=current[:-len(appendix)]
    prior_blob=hashlib.sha1(b'blob '+str(len(prior)).encode()+b'\0'+prior).hexdigest()
    if audit.get('continuation_parent_blob')!=prior_blob or audit.get('continuation_appendix_sha256')!=digest(appendix):
        raise ValueError('continuation parent binding mismatch')
    commit=json.loads((directory/'commit.json').read_text())
    compare=json.loads((directory/'compare.json').read_text())
    publication=json.loads((HERE/'publication_manifest.json').read_text())
    validate_remote_commits(commit,compare,publication)
    files=compare.get('files',[])
    if sorted(f['filename'] for f in files)!=sorted(publication_paths()) or any(f['status'] not in ('added','modified') for f in files):
        raise ValueError('remote changed-path boundary mismatch')


def dump(p,x):
    p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def digest(b): return hashlib.sha256(b).hexdigest()
def manifest(out):
    dump(out/'file_manifest.json',{str(p.relative_to(out)):{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(out.rglob('*')) if p.is_file() and p!=out/'file_manifest.json'})
def check_manifest(out):
    m=json.loads((out/'file_manifest.json').read_text())
    for name in m:safe_relative(name)
    actual={str(p.relative_to(out)) for p in out.rglob('*') if p.is_file() and p!=out/'file_manifest.json'}
    if set(m)!=actual: raise ValueError('artifact membership mismatch')
    for name,expected in m.items():
        data=(out/name).read_bytes()
        if expected!={'bytes':len(data),'sha256':digest(data)}: raise ValueError('artifact hash mismatch: '+name)
def run(args,cwd,log,expected=0):
    with log.open('wb') as f:
        r=subprocess.run(args,cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
    print(log.name,'exit',r.returncode,flush=True)
    if r.returncode!=expected: raise RuntimeError('Unexpected command status: '+str(log))
def identity(out):
    head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
    obj=expected_provenance()
    if head!=obj['scientific_sha']:raise ValueError('checkout/scientific SHA mismatch')
    obj['scope']='finite exact regression evidence, not continuum proof or native-mechanism validation'
    dump(out/'provenance.json',obj)
def primary(out):
    run([sys.executable,str(HERE/'producer.py'),str(out/'certificate.json')],HERE,out/'producer.log')
    run([sys.executable,str(HERE/'independent.py'),str(out/'certificate.json'),str(out/'independent.json')],HERE,out/'independent.log')
def mutations(out):
    source=json.loads((out/'certificate.json').read_text())
    bad=out/'rejecting_controls';bad.mkdir()
    cases={}
    def case(name,fn):
        obj=copy.deepcopy(source);fn(obj);cases[name]=obj
    case('missing',lambda x:x['records'].pop())
    case('duplicate',lambda x:x['records'].append(x['records'][0]))
    case('substitution',lambda x:x['records'][0].update(id='substituted'))
    case('wrong_value',lambda x:x['records'][0].update(value='7/1'))
    case('false_provenance',lambda x:x.update(source_parent='0'*40))
    case('false_coverage',lambda x:x['domain'].update(n=[2,3]))
    case('invalid_domain',lambda x:x['domain']['n'].append(1))
    def false_identical(x):
        next(v for v in x['records'] if v['id']=='identical_centralizer')['value']['false_contrast']='1/2'
    case('identical_state_false_contrast',false_identical)
    def false_product(x):
        next(v for v in x['records'] if v['id']=='block_product')['value']='1/2'
    case('false_product_attainment',false_product)
    summary={}
    for name,obj in cases.items():
        p=bad/(name+'.json');dump(p,obj)
        result=bad/(name+'_verdict.json')
        run([sys.executable,str(HERE/'independent.py'),str(p),str(result)],HERE,bad/(name+'.log'),expected=1)
        verdict=json.loads(result.read_text())
        if verdict.get('verified') is not False:raise ValueError('mutation not rejected: '+name)
        summary[name]={'rejected':True,'input_sha256':digest(p.read_bytes()),'verdict_sha256':digest(result.read_bytes())}
    dump(out/'rejecting_controls.json',summary)
def regression(out):
    tree=ast.parse((BASE/'record_conversion/ci_campaign.py').read_text())
    suites=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SUITES' for t in n.targets))
    if suites!=SUITES:raise ValueError('inherited exact suite identities/order changed')
    counts={}
    for folder,test in suites:
        log=out/(folder+'_tests.log')
        run([sys.executable,'-m','unittest','-v',test],BASE/folder,log)
        txt=log.read_text();m=re.findall(r'^Ran (\d+) tests? in ',txt,re.M)
        if len(m)!=1 or not re.search(r'^OK\s*$',txt,re.M):raise ValueError('missing test verdict')
        counts[folder]=int(m[0])
    if counts['record_conversion']!=23 or sum(counts.values())!=527:raise ValueError('inherited count changed; inspect exact logs')
    dump(out/'inherited_counts.json',{'per_suite':counts,'total':sum(counts.values()),'meaning':'inherited regression coverage only'})
def main(mode):
    out=Path('repair_'+mode).resolve();out.mkdir(exist_ok=True)
    identity(out)
    try:
        if mode=='integrity':
            bound=json.loads((HERE/'input_manifest.json').read_text())
            validate_inputs(bound)
            copied=out/'sources';copied.mkdir()
            for name,expected in bound['files'].items():
                data=(ROOT/name).read_bytes()
                if {'bytes':len(data),'sha256':digest(data)}!=expected:raise ValueError('source changed: '+name)
                dst=copied/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
            shutil.copyfile(HERE/'input_manifest.json',out/'input_manifest.json')
            dump(out/'integrity.json',{'verified':True,'file_count':len(bound['files']),'contract_commit':bound['contract_commit']})
        elif mode=='verification':
            upstream(Path('repair_integrity'))
            primary(out);mutations(out)
            run([sys.executable,'-m','unittest','-v','test_verification.py'],HERE,out/'repair_tests.log')
            run([sys.executable,'-m','unittest','-v','test_infrastructure.py'],HERE,out/'infrastructure_tests.log')
            run([sys.executable,'-m','unittest','-v','test_publication_readback.py'],HERE,out/'publication_readback_tests.log')
            run([sys.executable,'-m','unittest','-v','test_uqcf_analytical_review.py'],ROOT/'.github/scripts',out/'review_client_tests.log')
            regression(out)
        elif mode=='reproduction':
            v=Path('repair_verification');upstream(v)
            if json.loads((v/'provenance.json').read_text())['scientific_sha']!=os.environ['GITHUB_SHA']:raise ValueError('wrong verification source')
            primary(out)
            for name in ['certificate.json','independent.json']:
                if (out/name).read_bytes()!=(v/name).read_bytes():raise ValueError('fresh byte mismatch')
            dump(out/'reproduction.json',{'verified':True,'byte_identical':['certificate.json','independent.json']})
        elif mode=='gate':
            for phase in ['integrity','verification','reproduction']:
                upstream(Path('repair_'+phase))
            for phase in ['review','publication']:
                directory=Path('repair_'+phase);upstream(directory)
                m=json.loads((directory/'review_manifest.json').read_text());raw=(directory/'review.txt').read_bytes()
                validate_provenance(m)
                if m['scientific_sha']!=os.environ['GITHUB_SHA'] or m['workflow_sha']!=os.environ['GITHUB_SHA'] or m['response_sha256']!=digest(raw):raise ValueError('review identity mismatch')
                verdict=json.loads((directory/'verdict.json').read_text())
                parsed=json.loads(re.sub(r'^```(?:json)?\s*|\s*```$','',raw.decode()).strip())
                if parsed!=verdict:raise ValueError('parsed review/verdict discrepancy')
                validate_review_verdict(verdict)
                for name,h in m['input_sha256'].items():
                    if digest(Path(name).read_bytes())!=h:raise ValueError('review input bytes changed: '+name)
            remote=Path('repair_remote_publication');upstream(remote)
            validate_remote(remote)
            dump(out/'gate.json',{'status':'VERIFICATION_AND_REVIEW_PASSED_PENDING_FINAL_PUBLICATION_READBACK','native_milestone_achieved':False,'numbered_stage_closed':False,'publication_readback_still_required':True})
        else:raise ValueError(mode)
    finally:
        manifest(out)
if __name__=='__main__':main(sys.argv[1])
