"""Reproduce evidence audit; hashes documents only, never imports scientific code.
Run: python audit_resume.py [evidence-directory]. AUDIT_RAW.zip must be adjacent.
"""
import hashlib
import json
from pathlib import Path
import stat
import sys
import zipfile

OUT = Path(__file__).resolve().parent
EVIDENCE = Path(sys.argv[1]) if len(sys.argv) > 1 else (OUT / 'evidence' if (OUT / 'evidence').is_dir() else OUT.parent / 'evidence')
PREFIX = 'ResearchHistory/UQCF-GEM/research/physical-bridge/history_orientation/'
SOURCE = 'a42ca9e248c438081f31dcaba2ba5c6ffb36cec0'
PARENT = '24dbac1a7da1a2484dd3d28f66c3b62c7ae632af'
FIRST = '23c55d38a27e5081a1c92b3ed03f37adfb446687'
CONTRACT = '68fcd6d6118f7cb30bdca88814d1a5dc8260f0da'
IDENT = {'scientific_sha':SOURCE, 'workflow_sha':SOURCE, 'run_id':'38927950314', 'run_attempt':'2', 'source_parent':PARENT, 'contract_commit':CONTRACT}

def parse(data):
    def unique(pairs):
        d = {}
        for k,v in pairs:
            if k in d: raise ValueError('duplicate JSON key')
            d[k] = v
        return d
    def reject(v): raise ValueError('nonfinite JSON')
    return json.loads(data,object_pairs_hook=unique,parse_constant=reject)

def identity(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}

def safe_zip(z):
    names=z.namelist()
    assert len(names)==len(set(names))
    assert all(not Path(n).is_absolute() and '..' not in Path(n).parts and str(Path(n))==n for n in names)
    assert not any(stat.S_ISLNK(i.external_attr >> 16) for i in z.infolist())
    return set(names)

def check_subset(a,b):
    for k,v in a.items():
        if k=='logs_url': assert v is None; continue
        if k=='steps' and v is None: assert b[k]==[]; continue
        if isinstance(v,dict): check_subset(v,b[k])
        elif isinstance(v,list):
            assert len(v)==len(b[k])
            for left,right in zip(v,b[k]):
                if isinstance(left,dict): check_subset(left,right)
                else: assert left==right
        else: assert v==b[k],k

if not __debug__: raise SystemExit('Assertions must be enabled')
with zipfile.ZipFile(OUT/'AUDIT_RAW.zip') as z:
    names=safe_zip(z)
    seal=parse(z.read('file_manifest.json'))
    assert names==set(seal)|{'file_manifest.json'}
    for n,entry in seal.items(): assert entry==identity(z.read(n))
    raw={n:parse(z.read(n)) for n in seal}
meta=[parse(r['result']['structuredContent']['content']) for r in raw['metadata_connector.json']]
run,jobs,artifacts,source,first,contract=meta
assert run==parse((EVIDENCE/'run.json').read_bytes())
assert run['id']==38927950314 and run['run_attempt']==2 and run['head_sha']==SOURCE
assert run['status']=='completed' and run['conclusion']=='failure'
assert run['actor']['login']==run['triggering_actor']['login']=='proteinfolding-gpt'
assert run['head_branch']=='research/uqcf-overlapping-guard-exchange'
assert jobs['total_count']==3 and artifacts['total_count']==4
check_subset(parse((EVIDENCE/'jobs.json').read_bytes()),jobs)
check_subset(parse((EVIDENCE/'artifacts.json').read_bytes()),artifacts)
assert {j['name']:j['conclusion'] for j in jobs['jobs']}=={'integrity':'success','mathematical-review':'failure','publication-audit':'skipped'}
assert {j['id'] for j in jobs['jobs']}=={117121436628,117121578885,117121785915}
assert all(j['run_id']==38927950314 and j['run_attempt']==2 and j['head_sha']==SOURCE for j in jobs['jobs'])
for c,sha,parent in [(source,SOURCE,FIRST),(first,FIRST,CONTRACT),(contract,CONTRACT,PARENT)]:
    assert c['sha']==sha and [p['sha'] for p in c['parents']]==[parent]
assert source['author']['login']==source['committer']['login']=='proteinfolding-gpt'
files={(r['ref'],r['path']):r['result']['structuredContent']['content'].encode() for r in raw['source_connector.json']}
assert len(files)==33
snap={path:data for (ref,path),data in files.items() if ref==SOURCE}
inputs=parse(snap[PREFIX+'input_manifest.json'])
assert len(inputs)==13 and set(snap)==set(inputs)|{PREFIX+'input_manifest.json'}
for name,entry in inputs.items(): assert identity(snap[name])==entry,name
packet=parse(snap[PREFIX+'source_packet.json'])
assert packet['source_parent']==PARENT and len(packet['files'])==19
sources=[]
for entry in packet['files']:
    data=entry['content'].encode(); assert data==files[(PARENT,entry['path'])]
    calculated=identity(data); assert entry['git_blob']==calculated['git_blob'] and entry['ref']==PARENT
    sources.append({'path':entry['path'],'ref':PARENT,**calculated})
assert len({x['path'] for x in sources})==19
assert sorted(sources,key=lambda x:x['path'])==sorted(parse(snap[PREFIX+'source_identities.json']),key=lambda x:x['path'])
report={'status':'EVIDENCE_INTEGRITY_PASS','scientific_status':'REVIEW_BLOCKED_HTTP429','identity':IDENT,'gemini_acceptance':False,'native_milestone':'OPEN','no_scientific_execution':True,'external_writes_by_auditor':False,'artifacts':[],'logs':[],'pinned_sources_verified':19,'frozen_inputs_verified':13,'source_files_and_manifest_remote_readback':33,'jobs':{j['name']:{'id':j['id'],'conclusion':j['conclusion']} for j in jobs['jobs']},'source_commit_author':source['author']['login'],'triggering_actor':run['triggering_actor']['login']}
new=[a for a in artifacts['artifacts'] if a['name'].endswith('-2')]
assert len(new)==2
for a in new:
    archive=EVIDENCE/(a['name']+'.zip'); data=archive.read_bytes(); d=identity(data)
    assert d['bytes']==a['size_in_bytes'] and 'sha256:'+d['sha256']==a['digest']
    assert a['workflow_run']['id']==38927950314 and a['workflow_run']['head_sha']==SOURCE
    with zipfile.ZipFile(archive) as z:
        names=safe_zip(z); manifest=parse(z.read('file_manifest.json'))
        assert names==set(manifest)|{'file_manifest.json'}
        for n,entry in manifest.items():
            b=z.read(n); assert entry=={k:identity(b)[k] for k in ['bytes','sha256']}
            extracted=EVIDENCE/a['name']/n
            if extracted.exists(): assert extracted.read_bytes()==b
        assert parse(z.read('provenance.json'))==IDENT
        if a['name']=='history-integrity-2':
            assert names=={'file_manifest.json','provenance.json','input_manifest.json','integrity.json'}|{'snapshot/'+n for n in inputs}
            assert z.read('input_manifest.json')==snap[PREFIX+'input_manifest.json']
            for n in inputs: assert z.read('snapshot/'+n)==snap[n]
            assert parse(z.read('integrity.json'))=={'verified':True,'source_count':19,'inputs':inputs,'scope':'document identities only; no numerical science or inherited replay'}
        else:
            assert a['name']=='history-review-2'
            assert names=={'file_manifest.json','provenance.json','prompt.txt','model_availability.json','infrastructure_failure.json'}
            prompt=snap[PREFIX+'REVIEW_INSTRUCTIONS.txt'].decode()+'\nEXACT IDENTITY\n'+json.dumps(IDENT,sort_keys=True)
            for n in ['CONTRACT.md','RESULT.md']: prompt+='\n\nCURRENT DOCUMENT '+n+'\n'+snap[PREFIX+n].decode()
            prompt+='\n\nPINNED FULL SOURCE PACKET\n'+snap[PREFIX+'source_packet.json'].decode()
            assert z.read('prompt.txt')==prompt.encode()
            report['prompt']=identity(prompt.encode())
            failure=parse(z.read('infrastructure_failure.json'))
            assert failure=={'error_type':'HTTPError','http_status':429,'status':'INFRASTRUCTURE_FAILURE_NOT_MATHEMATICAL_VERDICT'}
            available=parse(z.read('model_availability.json'))
            assert available['name']=='models/gemini-3.1-pro-preview' and 'generateContent' in available['supportedGenerationMethods']
            report['failure']=failure; report['model_available']=available['name']; report['raw_response_present']=False;report['mathematical_verdict_present']=False
        report['artifacts'].append({'id':a['id'],'name':a['name'],**d,'members':sorted(names)})
for row in raw['logs_connector.json']:
    job_id=row['job_id']; name={117121436628:'integrity',117121578885:'mathematical-review'}[job_id]
    b=(EVIDENCE/(name+'.log')).read_bytes()
    assert b==row['result']['structuredContent']['content'].encode()
    assert SOURCE.encode() in b
    if name=='integrity': assert b'Exact document integrity verified: 19 pinned sources' in b
    else: assert b'Review infrastructure failed; sanitized evidence retained.' in b
    report['logs'].append({'job_id':job_id,'name':name,**identity(b)})
report['scope']='Independent evidence/source/prompt/provenance byte audit; not mathematical review, native-mechanism certification, inherited numerical replay, or numbered-stage closure. Actions publication audit was skipped. Immutable publication readback remains a separate step.'
report['authorization']='Parent relay records user Continue, approved for one additional rerun after the historical stop. This audit does not independently authenticate chat authorization.'
report['audit_raw']=identity((OUT/'AUDIT_RAW.zip').read_bytes())
(OUT/'AUDIT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('PASS: attempt 2 archives, all members, 33 remote source paths, full prompt and logs; REVIEW_BLOCKED_HTTP429; no Gemini verdict.')
