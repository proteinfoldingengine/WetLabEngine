"""Durable v16.23 publication; fixed GitHub-only retrieval and fixed commands.

Artifact content and metadata are data, never executable hooks. No inherited
publisher is imported, no credentials are printed, and no external attestation
or network destination is used. Run only on the declared research branch.
"""
from pathlib import Path
import hashlib,io,json,lzma,os,re,subprocess,zipfile

REPO='proteinfoldingengine/WetLabEngine'
BRANCH='research/v16.23-overlap-descent'
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
RELP='ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent'
RUNS=[
 {'role':'wiring-red','run':36568025339,'job':109404706116,'artifact':11032433007,'sha':'d75bb1d9c043634a6f60c66d1a0153f39c7192c8','digest':'d8d9084ad86358f3aa9184b043b0e30ada86fe76b334d370f85997f1ac2c47cd','conclusion':'failure'},
 {'role':'initial-green','run':36569139253,'job':109408436653,'artifact':11032659764,'sha':'939293191fd5bdd13a086b1d86ac15af595a1b6d','digest':'1d1abd0de463042e3cd04b4f61ba07de4a662b3d8e4b702c0afbff43f6779af6','conclusion':'success'},
 {'role':'schema-red','run':36569553274,'job':109409840157,'artifact':11033676117,'sha':'54a3a1c57be3d749e86c88969b1556452235d513','digest':'a1aa0a0b39accacb9ca4ae3665deecc97c2b94c13495814ef4bbb216858bdcc3','conclusion':'failure'},
 {'role':'final-green','run':36570394253,'job':109412645015,'artifact':11033358321,'sha':'1a1a38db702b1da47a829f08ce2740e2d578ea27','digest':'5ced598cdb313dd1a9b3c932a858fac3ab4cbff8696c663289aed71556998b5a','conclusion':'success'},
]
RAW='a9b4d6c28dcb5ffbfcd5a997e2cb12668de37f4360846a45a6b8125985e8ff8a'
VHASH='76316091867ac1f6daf3cb8c9b5e8df3f67b23ded780afe79b853aa8568085bf'

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(raw):return hashlib.sha256(raw).hexdigest()

def api(endpoint):
    need(endpoint.startswith('actions/'),'unapproved API endpoint')
    return subprocess.check_output(['gh','api','--allow-escape-sequences','repos/'+REPO+'/'+endpoint])

def members(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        need(z.testzip() is None,'original ZIP CRC failure')
        names=z.namelist();need(len(names)==len(set(names)),'duplicate archive member')
        need(all(Path(n).name==n and not n.startswith('.') for n in names),'unsafe or nested evidence member')
        data={n:z.read(n) for n in names}
    for line in data['SHA256SUMS'].decode().splitlines():
        sha,name=line.split();need(name in data and digest(data[name])==sha,'original member hash failure: '+name)
    return data

def verified_archive(raw,run):
    need(digest(raw)==run['digest'],'original artifact digest mismatch')
    d=members(raw);meta=json.loads(d['EXECUTION.json'])
    need(meta['execution_sha']==run['sha'] and str(meta['run_id'])==str(run['run']) and str(meta['attempt'])=='1','original attempt/source mismatch')
    commands=json.loads(d['COMMANDS.json']);tests=json.loads(d['TEST_RECEIPT.json'])
    need(commands and commands[0]['name']=='tests','missing executed tests')
    if run['role']=='wiring-red':
        need(tests['tests_run']==22 and tests['failures']==22 and tests['errors']==0 and commands[0]['exit_code']==1,'wrong wiring RED')
        need('expected wiring RED: missing engine' in d['tests.log'].decode(),'wiring RED has wrong reason')
    elif run['role']=='schema-red':
        need(tests['tests_run']==22 and tests['failures']==0 and tests['errors']==0,'old controls failed before schema RED')
        need(commands[-1]['name']=='schema' and commands[-1]['exit_code']==1,'wrong substantive RED stage')
        text=d['schema.log'].decode();need('FAILED (failures=2)' in text and 'ValueError not raised' in text,'wrong substantive RED failure')
    else:
        expected=['tests','schema','v1622','v1621','parent','producer','verifier'] if run['role']=='final-green' else ['tests','v1622','v1621','parent','producer','verifier']
        need([c['name'] for c in commands]==expected and all(c['exit_code']==0 for c in commands),'incomplete scientific command evidence')
        need(tests['tests_run']==22 and tests['failures']==0 and tests['errors']==0,'current test failure')
        need(digest(lzma.decompress(d['certificates.json.xz']))==RAW,'changed full scientific certificate')
        for name,count in [('tests',22),('v1622',20),('v1621',22),('parent',15)]+([('schema',3)] if run['role']=='final-green' else []):
            text=d[name+'.log'].decode();need(re.search(r'Ran '+str(count)+r' tests?\b',text) and text.strip().endswith('OK'),'test count or success mismatch: '+name)
    return d

def verify_publication():
    for line in (P/'PUBLICATION_SHA256SUMS').read_text().splitlines():
        sha,name=line.split();need(digest((P/name).read_bytes())==sha,'publication checksum failure: '+name)
    print('All publication file hashes verified.')

def main():
    need(os.environ.get('GITHUB_REPOSITORY')==REPO and os.environ.get('GITHUB_REF_NAME')==BRANCH,'wrong publication repository/branch')
    e=P/'evidence';(e/'archives').mkdir(parents=True,exist_ok=True);(e/'history').mkdir(exist_ok=True)
    original={};registry=[]
    for run in RUNS:
        blob=api('artifacts/'+str(run['artifact'])+'/zip');data=verified_archive(blob,run);original[run['role']]=data
        (e/'archives'/(run['role']+'.zip')).write_bytes(blob)
        rraw=api('runs/'+str(run['run']));r=json.loads(rraw)
        need(r['head_sha']==run['sha'] and r['conclusion']==run['conclusion'] and r['run_attempt']==1,'run provenance mismatch')
        jobs=api('runs/'+str(run['run'])+'/jobs');j=json.loads(jobs)['jobs']
        need(any(x['id']==run['job'] and x['conclusion']==run['conclusion'] for x in j),'job provenance mismatch')
        (e/'history'/(run['role']+'-run.json')).write_bytes(rraw)
        (e/'history'/(run['role']+'-jobs.json')).write_bytes(jobs)
        (e/'history'/(run['role']+'-job.log')).write_bytes(api('jobs/'+str(run['job'])+'/logs'))
        registry.append(dict(run,attempt=1,bytes=len(blob)))
    final=original['final-green'];need(digest(final['VERIFICATION.json'])==VHASH,'final verifier receipt mismatch')
    for name,data in final.items():(e/('ORIGINAL_SHA256SUMS' if name=='SHA256SUMS' else name)).write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(final['source.zip'])) as z:
        for name in ['engine.py','verify.py','test_gate.py','test_schema.py','PROOFS.md','PREREGISTRATION.md','TYPE_LEDGER.md']:
            need(z.read(RELP+'/'+name)==(P/name).read_bytes(),'scientific source changed: '+name)
    commands=[('tests',P,['python','test_gate.py']),('schema',P,['python','test_schema.py']),('v1622',P.parent/'v16.22-response-selection-closure',['python','-m','unittest','discover','-v']),('v1621',ROOT/'ResearchHistory/UQCF-GEM/foundational-closure-verification',['python','tests/test_fcv.py']),('parent',P.parent/'v15.56-response-selector-obstruction',['python','-m','unittest','-v','test_pruning_consistency_audit']),('producer',P,['python','engine.py']),('verifier',P,['python','verify.py'])]
    fresh=[]
    for name,cwd,cmd in commands:
        with (e/('publication-'+name+'.log')).open('w') as log:r=subprocess.run(cmd,cwd=cwd,stdout=log,stderr=subprocess.STDOUT)
        fresh.append({'name':name,'command':cmd,'exit_code':r.returncode})
        (e/'PUBLICATION_COMMANDS.json').write_text(json.dumps(fresh,indent=2)+'\n')
        need(r.returncode==0,'fresh publication verification failed: '+name)
    for name in ['certificates.json.xz','VERIFICATION.json','PRODUCTION.json','TEST_RECEIPT.json']:
        need((e/name).read_bytes()==final[name],'fresh scientific output differs: '+name)
    pubjobs=json.loads(api('runs/'+os.environ['GITHUB_RUN_ID']+'/jobs'))['jobs']
    own=[j for j in pubjobs if j['name']=='publish'];need(len(own)==1,'publication job identity unavailable')
    v=json.loads(final['VERIFICATION.json']);receipt={'version':'16.23','scientific_execution_sha':RUNS[-1]['sha'],'publication_workflow_head':os.environ['GITHUB_SHA'],'publication_run':os.environ['GITHUB_RUN_ID'],'publication_job':own[0]['id'],'publication_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'original_runs':registry,'fresh_commands':fresh,'fresh_scientific_bytes_equal':True,'raw_certificate_sha256':RAW,'xz_certificate_sha256':digest(final['certificates.json.xz']),'verification_sha256':VHASH,'verification':v,'test_counts':{'new':25,'v1622':20,'v1621':22,'exact_parent':15},'review':'self-reviewed; algorithmically independent verifier, no separate reviewer','scope':BRANCH+'; not merged to main'}
    (P/'PUBLICATION_EVIDENCE.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    (P/'RUN_REGISTRY.json').write_text(json.dumps(registry,indent=2)+'\n')
    files=[f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='PUBLICATION_SHA256SUMS']
    files.append(P.parent.parent/'V16_23_REPORT.md')
    names=sorted(os.path.relpath(f,P) for f in files)
    (P/'PUBLICATION_SHA256SUMS').write_text(''.join(digest((P/name).read_bytes())+'  '+name+'\n' for name in names))
    verify_publication()

if __name__=='__main__':
    import sys
    if sys.argv[1:]==['--verify']:verify_publication()
    else:main()
