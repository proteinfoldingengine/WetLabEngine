"""Offline, standard-library publication evidence audit. No scientific code executed.
Run beside the three AUDIT_RAW_*.zip archives with normal (not -O) Python.
"""
import base64
from collections import defaultdict
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = 'a42ca9e248c438081f31dcaba2ba5c6ffb36cec0'
PARENT = '24dbac1a7da1a2484dd3d28f66c3b62c7ae632af'
FIRST = '23c55d38a27e5081a1c92b3ed03f37adfb446687'
CONTRACT = '68fcd6d6118f7cb30bdca88814d1a5dc8260f0da'
PUBLICATION = '7d1f528dbd807ed39bb41bb36a221b084d5f9f52'
PREVIOUS = '07bccacc3f17f97e3cd9cc9fe486a47cb04c9faa'
PREFIX = 'ResearchHistory/UQCF-GEM/research/physical-bridge/history_orientation/'
IDENT = dict(scientific_sha=SOURCE,workflow_sha=SOURCE,source_parent=PARENT,contract_commit=CONTRACT,run_id='38927950314',run_attempt='3')

def parse(b):
    def unique(pairs):
        d = {}
        for k,v in pairs:
            if k in d: raise ValueError('duplicate JSON key')
            d[k] = v
        return d
    def reject(x): raise ValueError('nonfinite JSON')
    return json.loads(b,object_pairs_hook=unique,parse_constant=reject)

def identity(b):
    return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest())

def unzip(b,full_identity=False):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=z.namelist()
        assert len(names)==len(set(names))
        assert all(not Path(n).is_absolute() and '..' not in Path(n).parts and str(Path(n))==n for n in names)
        assert not any(stat.S_ISLNK(i.external_attr>>16) for i in z.infolist())
        d={n:z.read(n) for n in names}
    seal=parse(d['file_manifest.json'])
    assert set(d)==set(seal)|{'file_manifest.json'}
    for n,v in seal.items():
        expected=identity(d[n])
        if not full_identity: expected.pop('git_blob')
        assert v==expected,n
    return d

def api(row):
    assert not row.get('isError')
    return parse(row['structuredContent']['content'])

def decode_rows(rows):
    files={}
    for row in rows:
        r=row['result']; assert not r.get('isError')
        r=r['structuredContent']; assert r['encoding']=='base64'
        b=base64.b64decode(r['content']);assert identity(b)['git_blob']==r['sha']
        key=(row['ref'],row['path']);assert key not in files;files[key]=b
    return files

if not __debug__: raise SystemExit('Assertions must be enabled')
raw={};raw_ids={}
for n in ['AUDIT_RAW_PUBLICATION.zip','AUDIT_RAW_SOURCES.zip','AUDIT_RAW_ACTIONS.zip']:
    b=(HERE/n).read_bytes();raw_ids[n]=identity(b)
    for k,v in unzip(b,True).items():
        if k=='file_manifest.json':continue
        assert k not in raw;raw[k]=v
published=decode_rows(parse(raw['published_connector.json']))
assert len(published)==14 and {k[0] for k in published}=={PUBLICATION}
evidence={p.split('resume_20261016_attempt3/')[1]:b for (_,p),b in published.items()}
files=decode_rows(parse(raw['source_connector.json']));assert len(files)==33
snap={p:b for (ref,p),b in files.items() if ref==SOURCE}
inputs=parse(snap[PREFIX+'input_manifest.json']);assert len(inputs)==13
assert set(snap)==set(inputs)|{PREFIX+'input_manifest.json'}
for p,ident in inputs.items():assert identity(snap[p])==ident
packet=parse(snap[PREFIX+'source_packet.json']);assert packet['source_parent']==PARENT and len(packet['files'])==19
originals=[]
for row in packet['files']:
    b=files[(PARENT,row['path'])];assert b==row['content'].encode() and row['ref']==PARENT
    ident=identity(b);assert row['git_blob']==ident['git_blob'];originals.append(dict(path=row['path'],ref=PARENT,**ident))
assert len({r['path'] for r in originals})==19
assert sorted(originals,key=lambda r:r['path'])==sorted(parse(snap[PREFIX+'source_identities.json']),key=lambda r:r['path'])
meta=parse(raw['metadata_retained.json']);run=api(meta['run']);jobs=api(meta['jobs']);artifacts=api(meta['raw_artifacts'])
current=api(parse(raw['current_run_connector.json']))
assert current==parse(evidence['evidence/run.json'])
assert jobs==parse(evidence['evidence/jobs.json']) and artifacts==parse(evidence['evidence/artifacts.json'])
assert run['id']==38927950314 and run['run_attempt']==3 and run['head_sha']==SOURCE and run['conclusion']=='success' and run['status']=='completed'
assert run['head_branch']=='research/uqcf-overlapping-guard-exchange'
assert jobs['total_count']==3 and len(jobs['jobs'])==3
job_ids={'integrity':117160704838,'mathematical-review':117160867575,'publication-audit':117161256836}
assert {j['name']:j['id'] for j in jobs['jobs']}==job_ids
assert all(j['run_attempt']==3 and j['head_sha']==SOURCE and j['run_id']==38927950314 and j['conclusion']=='success' and j['status']=='completed' for j in jobs['jobs'])
pubcommit=api(meta['receipt_commit']);previous=api(meta['parent_commit'])
assert pubcommit['sha']==PUBLICATION and [p['sha'] for p in pubcommit['parents']]==[PREVIOUS]
assert pubcommit['author']['login']==pubcommit['committer']['login']=='proteinfolding-grokbot'
assert len(pubcommit['files'])==14 and all(f['status']=='added' for f in pubcommit['files'])
assert {f['filename'] for f in pubcommit['files']}=={p for _,p in published}
for f in pubcommit['files']:assert identity(published[(PUBLICATION,f['filename'])])['git_blob']==f['sha']
anc={r['sha']:api(r['result']) for r in parse(raw['ancestry_connector.json'])}
for sha,parent in [(SOURCE,FIRST),(FIRST,CONTRACT),(CONTRACT,PARENT)]:assert anc[sha]['sha']==sha and [p['sha'] for p in anc[sha]['parents']]==[parent]
assert anc[SOURCE]['author']['login']==anc[SOURCE]['committer']['login']=='proteinfolding-gpt'
compare=api(parse(raw['compare_connector.json']))
expected_changed=set(inputs)-{'.github/scripts/uqcf_analytical_repair_review.py',PREFIX+'CONTRACT.md'}|{PREFIX+'input_manifest.json'}
assert compare['status']=='ahead' and compare['ahead_by']==2 and compare['behind_by']==0
assert {f['filename'] for f in compare['files']}==expected_changed and all(f['status']=='added' for f in compare['files'])
for f in compare['files']:assert f['sha']==identity(snap[f['filename']])['git_blob']
archives={};archive_report=[]
assert artifacts['total_count']==3 and len(artifacts['artifacts'])==3
for a in artifacts['artifacts']:
    b=evidence['evidence/'+a['name']+'.zip'];ident=identity(b)
    assert b==raw['downloads/github-actions-artifact-'+str(a['id'])+'.zip']
    assert ident['bytes']==a['size_in_bytes'] and 'sha256:'+ident['sha256']==a['digest']
    assert a['workflow_run']['id']==38927950314 and a['workflow_run']['head_sha']==SOURCE
    members=unzip(b);archives[a['name']]=members
    archive_report.append(dict(id=a['id'],name=a['name'],**ident,members=sorted(members)))
assert set(archives)=={'history-integrity-3','history-review-3','history-publication-3'}
integ=archives['history-integrity-3'];review=archives['history-review-3'];publication=archives['history-publication-3']
assert set(integ)=={'file_manifest.json','integrity.json','input_manifest.json','provenance.json'}|{'snapshot/'+n for n in inputs}
assert integ['input_manifest.json']==snap[PREFIX+'input_manifest.json']
assert parse(integ['integrity.json'])==dict(verified=True,source_count=19,inputs=inputs,scope='document identities only; no numerical science or inherited replay')
for n in inputs:assert integ['snapshot/'+n]==snap[n]
assert parse(integ['provenance.json'])==parse(review['provenance.json'])==IDENT
assert set(review)=={'file_manifest.json','provenance.json','model_availability.json','prompt.txt','response.json','review.txt','review_manifest.json','verdict.json'}
for n in set(review)-{'file_manifest.json','prompt.txt'}:assert review[n]==evidence['evidence/'+n]
prompt=snap[PREFIX+'REVIEW_INSTRUCTIONS.txt'].decode()+'\nEXACT IDENTITY\n'+json.dumps(IDENT,sort_keys=True)
for n in ['CONTRACT.md','RESULT.md']:prompt+='\n\nCURRENT DOCUMENT '+n+'\n'+snap[PREFIX+n].decode()
prompt+='\n\nPINNED FULL SOURCE PACKET\n'+snap[PREFIX+'source_packet.json'].decode()
assert prompt.encode()==review['prompt.txt']
manifest=parse(review['review_manifest.json']);assert all(manifest[k]==v for k,v in IDENT.items()) and manifest['inputs']==inputs
for field,n in [('prompt_sha256','prompt.txt'),('raw_api_response_sha256','response.json'),('review_sha256','review.txt')]:assert manifest[field]==identity(review[n])['sha256']
response=parse(review['response.json']);assert len(response['candidates'])==1
candidate=response['candidates'][0];assert candidate['finishReason']=='STOP' and candidate['content']['role']=='model'
parts=candidate['content']['parts'];assert parts and all(type(p) is dict for p in parts)
texts=[]
for p in parts:
    if p.get('thought') is True:continue
    assert type(p.get('text')) is str and not(set(p)-{'text','thought','thoughtSignature'});texts.append(p['text'])
assert '\n'.join(texts).strip().encode()==review['review.txt']
verdict=parse(review['verdict.json']);assert verdict==parse(review['review.txt']) and verdict['verdict']=='ACCEPTED'
assert all(verdict[k]==[] for k in ['findings','missing_assumptions','counterexamples']) and len(verdict['limitations'])==5
available=parse(review['model_availability.json']);assert available['name']=='models/gemini-3.1-pro-preview' and 'generateContent' in available['supportedGenerationMethods']
assert manifest['model_requested']==manifest['model_returned']==response['modelVersion']=='gemini-3.1-pro-preview'
assert set(publication)=={'file_manifest.json','remote_readback.json'}
readback=parse(publication['remote_readback.json']);assert readback['verified'] is True and readback['review_manifest']==manifest
assert all(readback[k]==IDENT[k] for k in ['scientific_sha','workflow_sha','run_id','run_attempt'])
assert readback['parents']==[FIRST] and readback['author']=='proteinfolding-gpt' and readback['tree_sha']==anc[SOURCE]['commit']['tree']['sha']
assert set(readback['changed_paths'])==expected_changed
expected_checked=[dict(path=p,**identity(b)) for p,b in snap.items()]+[dict(path='original:'+r['path'],**{k:r[k] for k in ['bytes','sha256','git_blob']}) for r in originals]
assert len(readback['checked'])==33 and sorted(readback['checked'],key=lambda r:r['path'])==sorted(expected_checked,key=lambda r:r['path'])
combined=defaultdict(list)
for line in evidence['evidence/run_attempt3.log'].decode().splitlines():
    name,step,text=line.split('\t',2);assert name in job_ids and step;combined[name].append(text)
def normalize(line):return re.sub(r'^\ufeff?\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+Z ?', '', line)
log_report=[]
for name,jid in job_ids.items():
    b=meta['log_'+str(jid)]['structuredContent']['content'].encode();lines=b.decode().splitlines()
    assert list(map(normalize,lines))==list(map(normalize,combined[name]))
    assert SOURCE.encode() in b
    log_report.append(dict(name=name,job_id=jid,lines=len(lines),**identity(b)))
assert run['run_started_at']=='2026-10-16T19:39:35Z' and run['created_at']=='2026-10-16T19:39:36Z'
assert previous['commit']['committer']['date']=='2026-10-16T19:40:46Z'
report=dict(status='EVIDENCE_INTEGRITY_PASS_WITH_RECEIPT_QUALIFICATIONS',scientific_status='ACCEPTED_CONDITIONAL_ANALYTICAL_SCREEN',identity=IDENT,evidence_commit=PUBLICATION,published_files=[dict(path=p,**identity(b)) for (_,p),b in published.items()],artifacts=archive_report,logs=log_report,combined_log=dict(**identity(evidence['evidence/run_attempt3.log']),comparison='All job messages and ordering equal after removing job/step prefixes and timestamp tokens; raw byte equality is not claimed.'),source_files_verified=33,frozen_inputs_verified=13,pinned_originals_verified=19,full_prompt=identity(review['prompt.txt']),raw_response=identity(review['response.json']),review=identity(review['review.txt']),verdict=verdict,model_requested=manifest['model_requested'],generation_model_version=response['modelVersion'],availability_version=available['version'],workflow_publication_scope=readback['scope'],source_author=anc[SOURCE]['author']['login'],retry_operator=run['triggering_actor']['login'],receipt_qualifications=['Pre-rerun live-head claim is unsupported by recorded chronology; exact historical branch ref was not reconstructed.','Availability version and generation modelVersion are separate metadata.','Quota explanation is attributed user report, not independently established service diagnosis.'],chronology=dict(attempt_started_at=run['run_started_at'],attempt_created_at=run['created_at'],previous_commit_timestamp=previous['commit']['committer']['date']),raw_archives=raw_ids,no_scientific_execution=True,no_external_writes=True,native_interaction='OPEN',broad_C3_C4_C6='OPEN',numbered_stage_closure=False,inherited_numerical_replay=False,stabilization_commit_readback='separate step after publication')
(HERE/'AUDIT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print('PASS: 14 published files, 3 original ZIPs, 33 source paths, full prompt/response/verdict binding, 1018 log lines. Receipt qualifications retained.')
