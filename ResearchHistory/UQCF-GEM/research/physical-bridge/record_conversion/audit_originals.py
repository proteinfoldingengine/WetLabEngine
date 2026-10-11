"""Check original archives, complete logs, exact inputs and raw reviews."""
import hashlib,json,pathlib,re,zipfile

def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,reason):
    if not ok:raise ValueError(reason)
def parse(b):return json.loads(b)
def load(p):
    o=p/'originals';meta=parse((o/'artifact_metadata.json').read_bytes());archives={};identities=[]
    for a in meta['artifacts']:
        path=o/(a['name']+'.zip');data=path.read_bytes()
        require(len(data)==a['size_in_bytes'] and sha(data)==a['digest'].removeprefix('sha256:'),'archive bytes')
        with zipfile.ZipFile(path) as z:
            names=z.namelist();require(len(names)==len(set(names)),'duplicate archive member')
            require(all(not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts for n in names),'unsafe member')
            archives[a['name']]={n:z.read(n) for n in names}
        identities.append({'file':path.name,'bytes':len(data),'sha256':sha(data),'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),'members':{n:sha(b) for n,b in archives[a['name']].items()}})
    sources={}
    def source_file(local,published):
        candidates=[p/pathlib.Path(local).name,p.parent/pathlib.Path(published).name]
        candidates.extend(root/published for root in p.parents)
        return next(f for f in candidates if f.is_file())
    for item in parse((p/'scientific_manifest.json').read_bytes()):sources[pathlib.Path(item['path']).name]=source_file(item['local'],item['path']).read_bytes()
    for n,local in [('COUPLED_C3_RECORD_CONVERSION_RESULT.md','RESULT.md'),('COUPLED_C3_RECORD_CONVERSION_SCOPE.md','SCOPE.md'),('PLAN.md','PLAN.md'),('ANALYTICAL_REVIEW.md','ANALYTICAL_REVIEW.md'),('REVIEW_INPUT_SCOPE.md','REVIEW_INPUT_SCOPE.md'),('source_readbacks.json','source_readbacks.json')]:sources[n]=source_file(local,n).read_bytes()
    return {'archives':archives,'identities':identities,'artifact_meta':meta,'binding':parse((p/'binding.json').read_bytes()),'run':parse((o/'run_metadata.json').read_bytes()),'jobs':parse((o/'jobs_metadata.json').read_bytes()),'log_sources':parse((o/'job_log_sources.json').read_bytes()),'logs':{f.name:f.read_bytes() for f in o.glob('*_job.log')},'sources':sources,'local_certificate':(p/'certificate.json').read_bytes()}
def member_manifest(a):
    m=parse(a['file_manifest.json']);require(set(m)==set(a)-{'file_manifest.json'},'member manifest coverage')
    for n,info in m.items():require(info=={'bytes':len(a[n]),'sha256':sha(a[n])},'member digest '+n)
def check(p):
    b=p['binding'];science=b['scientific_commit'];rid=b['workflow_run'];run=p['run'];jobs=p['jobs']['jobs'];met=p['artifact_meta']['artifacts'];a=p['archives']
    require(run['id']==rid and run['head_sha']==science and run['conclusion']=='success' and run['head_branch']=='research/uqcf-overlapping-guard-exchange','run binding')
    names={'verification','reproduction','mathematical-review','publication-audit'}
    require(len(jobs)==4 and {j['name'] for j in jobs}==names and len({j['id'] for j in jobs})==4,'job coverage')
    for j in jobs:require(j['run_id']==rid and j['conclusion']=='success' and all(s['conclusion']=='success' for s in j['steps']),'job result')
    expected={'conversion-verification','conversion-reproduction','conversion-review','conversion-gate','conversion-publication'}
    require(set(a)==expected and len(met)==5 and {m['name'] for m in met}==expected,'archive coverage')
    for m in met:require(m['workflow_run']['id']==rid and m['workflow_run']['head_sha']==science,'artifact binding')
    v=a['conversion-verification'];f=a['conversion-reproduction'];g=a['conversion-gate'];math=a['conversion-review'];pub=a['conversion-publication']
    for archive in (v,f,g):member_manifest(archive)
    fresh_names={'certificate.json','independent.json','native_check.json','producer.log','independent.log','native_check.log','provenance.json','reproduction.json','file_manifest.json'}
    require(set(f)==fresh_names and set(g)==fresh_names|{'publication_gate.json'},'fresh member coverage')
    require(set(math)==set(pub)=={'manifest.json','review.txt','response.json','prompt.txt'},'review member coverage')
    for ar in (v,f,g):
        prov=parse(ar['provenance.json']);require(prov['scientific_sha']==prov['workflow_sha']==science and str(prov['run_id'])==str(rid) and prov['freeze_commit']==b['freeze_commit'],'provenance')
        require(ar['certificate.json']==p['local_certificate'] and sha(ar['certificate.json'])==b['certificate_sha256'],'certificate equality')
    for n in ('independent.json','native_check.json'):
        require(v[n]==f[n]==g[n],'reproduction '+n)
    summary=parse(v['independent.json']);require(summary=={'complete_canonical_record_equality':True,'guaranteed_write':False,'native_access_derived':False,'positive_valid':124,'rejected':1488,'requested':1984,'saved_slice_occurrences':6634,'source_erased_positive':31,'status':'VERIFIED','valid':496},'independent counts')
    native=parse(v['native_check.json']);require(native['status']=='VERIFIED' and native['native_slice_occurrences']==6637 and native['forgery_native_valid'] is True,'native comparison')
    for ar in (f,g):require(parse(ar['reproduction.json'])=={'status':'VERIFIED','byte_identical':['certificate.json','independent.json','native_check.json'],'certificate_sha256':b['certificate_sha256']},'reproduction record')
    # Immutable source copies are compared with locally read-back scientific files.
    for n,data in p['sources'].items():
        if n!='progress.md':require(v[n]==data,'scientific source '+n)
    for item in parse(v['freeze_binding.json'])['files']:
        data=v[pathlib.Path(item['path']).name]
        require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['git_blob'],'immutable freeze binding')
    bindings=parse(v['source_readbacks.json'])
    bound={'bound_sources/'+pathlib.Path(i['path']).name for i in bindings}|{'bound_sources/coverage.py'}
    for item in bindings:require(sha(v['bound_sources/'+pathlib.Path(item['path']).name])==item['sha256'],'analytical source '+item['path'])
    suites={'record_conversion':23,'escape_obstruction':9,'reserve_activation':30,'source_escape':42,'cover_static':35,'nonuniform_reserve':34,'weak_trace':32,'fingerprint_lock':33,'private_cover':26,'moving_cover':28,'saturated_handover':26,'slack_handover':24,'handover_graph':20,'anchored_release':20,'local_progress':17,'capacity_gap':20,'saturated_transfer':22,'label_release':26,'footprint':22,'fixed_family':28,'star_carrier':10}
    # Prior stage totals are context; exact per-suite values below are checked from logs.
    actual={}
    for folder in suites:
        text=v[folder+'_tests.log'].decode();hits=re.findall(r'^Ran (\d+) tests? in ',text,re.M)
        require(len(hits)==1 and re.search(r'^OK\s*$',text,re.M),'suite log '+folder);actual[folder]=int(hits[0])
    require(actual==suites and sum(actual.values())==527,'per-suite test totals')
    require(parse(v['test_counts.json'])=={'per_suite':actual,'new':23,'inherited':504,'total':527},'test summary')
    # Per-suite numbers are read from original output; the fixed suite names prevent omission/substitution.
    source_names=set(p['sources'])-{'progress.md'}
    expected_v=source_names|bound|{x+'_tests.log' for x in suites}|{'certificate.json','independent.json','native_check.json','producer.log','independent.log','native_check.log','provenance.json','test_counts.json','file_manifest.json'}
    require(set(v)==expected_v,'verification exact members')
    require(b'FAILED (failures=23)' in v['red.log'] and b'expected RED: implementation absent' in v['red.log'],'genuine RED')
    reviews={};input_counts={}
    for name,ar,is_pub in [('mathematical',math,False),('publication',pub,True)]:
        m=parse(ar['manifest.json']);raw=ar['review.txt']
        require(m['research_commit']==m['workflow_commit']==science,'review commit')
        inputs={'EVIDENCE/'+n:data for n,data in v.items()}|{'REPRODUCTION/'+n:data for n,data in f.items()}
        if is_pub:inputs|={'MATH_REVIEW/'+n:math[n] for n in ('review.txt','manifest.json')};inputs|={'GATE/'+n:data for n,data in g.items()}
        require(set(m['input_sha256'])==set(inputs),'review input coverage')
        for n,data in inputs.items():require(m['input_sha256'][n]==sha(data),'review input '+n)
        require(m['response_sha256']==sha(raw) and m['raw_api_response_sha256']==sha(ar['response.json']) and m['prompt_sha256']==sha(ar['prompt.txt']),'raw review hashes')
        prompt=ar['prompt.txt'].decode()
        for label,data in inputs.items():
            if pathlib.PurePosixPath(label).name=='certificate.json':
                body=f"Complete canonical certificate retained as original artifact; not reproduced in prompt. bytes={len(data)} sha256={sha(data)}. Independent full reconstruction and fresh byte equality are separately logged."
            else:body=data.decode()
            require('DOCUMENT '+label+'\n'+body in prompt,'actual prompt input '+label)
        api=parse(ar['response.json']);reconstructed='\n'.join(part.get('text','') for candidate in api.get('candidates',[]) for part in candidate.get('content',{}).get('parts',[]) if isinstance(part.get('text'),str)).strip().encode()
        require(reconstructed==raw,'API/raw answer match')
        obj=parse(re.sub(rb'^```(?:json)?\s*|\s*```$',b'',raw).strip())
        require(obj['verdict']=='ACCEPTED' and all(isinstance(obj[k],list) for k in ('findings','missing_assumptions','counterexamples','limitations')) and not obj['missing_assumptions'] and not obj['counterexamples'],'actual review verdict')
        require(m['attempts'][-1]['status']=='RESPONSE_RECEIVED','review attempts')
        reviews[name]=obj;input_counts[name]=len(inputs)
    gate=parse(g['publication_gate.json']);require(gate=={'status':'VERIFIED','mathematical_inputs_verified':input_counts['mathematical'],'response_sha256':sha(math['review.txt']),'native_access_derived':False,'guaranteed_write':False},'publication gate')
    require(len(p['log_sources'])==4 and {i['job_name'] for i in p['log_sources']}==names,'log coverage')
    for i in p['log_sources']:
        job=next(j for j in jobs if j['name']==i['job_name']);raw=p['logs'][i['file']];text=raw.decode()
        require(i['job_id']==job['id'] and i['run_id']==rid and i['endpoint']==f"https://api.github.com/repos/proteinfoldingengine/WetLabEngine/actions/jobs/{job['id']}/logs",'log provenance')
        require(len(raw)==i['bytes'] and sha(raw)==i['sha256'],'log digest')
        require('Current runner version:' in text[:300] and 'Complete job name: '+job['name'] in text and science in text and 'Cleaning up orphan processes' in text[-4000:],'complete log markers')
        if job['name'] in ('mathematical-review','publication-audit'):require('Record-conversion independent verdict: ACCEPTED' in text,'logged verdict')
    return {'status':'VERIFIED','scientific_commit':science,'workflow_run':rid,'certificate_sha256':b['certificate_sha256'],'test_counts':actual,'scientific_tests':527,'new_tests':23,'inherited_tests':504,'review_inputs':input_counts,'reviews':reviews,'original_archives':p['identities'],'native_slice_occurrences':6637,'canonical_requested':1984,'valid':496,'positive':124,'source_erased_positive':31}
if __name__=='__main__':
    p=pathlib.Path(__file__).parent;result=check(load(p));(p/'author_reconciliation.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('reviews','original_archives')},sort_keys=True))
