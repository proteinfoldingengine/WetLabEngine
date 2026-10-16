"""Reproduce stabilization readback checks using retained compact API evidence.
Usage: python audit_final.py [directory-containing-three-AUDIT_RAW-archives]
"""
import base64
import hashlib
import json
from pathlib import Path
import stat
import sys
import zipfile

HERE=Path(__file__).resolve().parent
ARCHIVES=Path(sys.argv[1]) if len(sys.argv)>1 else HERE
SHA='200ad70c4472469c30ffa8f34dee25174dc579b3'
PARENT='7d1f528dbd807ed39bb41bb36a221b084d5f9f52'
TREE='35b0ffd08ed734fdc51f3e54ed6f976b71e3aaf1'
BASE='ResearchHistory/UQCF-GEM/research/physical-bridge/'
PREFIX=BASE+'history_orientation/accepted_closeout/'
CONT=BASE+'COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md'

def parse(data):
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise ValueError('duplicate JSON key')
            d[k]=v
        return d
    def reject(v):raise ValueError('nonfinite JSON')
    return json.loads(data,object_pairs_hook=unique,parse_constant=reject)

def identity(b):return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest())

def api(row):
    assert not row.get('isError');return parse(row['structuredContent']['content'])

def decode(row):
    assert not row.get('isError');s=row['structuredContent'];assert s['encoding']=='base64'
    b=base64.b64decode(s['content']);assert identity(b)['git_blob']==s['sha'];return b

if not __debug__:raise SystemExit('Assertions must be enabled')
with zipfile.ZipFile(HERE/'FINAL_AUDIT_RAW.zip') as z:
    names=z.namelist();assert len(names)==len(set(names))
    assert all(not Path(n).is_absolute() and '..' not in Path(n).parts and str(Path(n))==n for n in names)
    assert not any(stat.S_ISLNK(i.external_attr>>16) for i in z.infolist())
    raw={n:z.read(n) for n in names}
seal=parse(raw['file_manifest.json']);assert set(raw)==set(seal)|{'file_manifest.json'}
for n,i in seal.items():assert identity(raw[n])==i
meta={r['name']:api(r['result']) for r in parse(raw['final_metadata_connector.json'])}
c=meta['commit'];assert c['sha']==SHA and c['commit']['tree']['sha']==TREE and [p['sha'] for p in c['parents']]==[PARENT]
assert c['author']['login']==c['committer']['login']=='proteinfolding-gpt'
assert meta['head']['object']['sha']==SHA and meta['head']['ref']=='refs/heads/research/uqcf-overlapping-guard-exchange'
assert len(c['files'])==11 and sum(f['status']=='added' for f in c['files'])==10
assert [(f['filename'],f['status']) for f in c['files'] if f['status']!='added']==[(CONT,'modified')]
files={};identities={}
for r in parse(raw['final_readback_rows.json']):
    assert r['ref']==SHA and r['path'] not in identities
    if 'result' in r:
        b=decode(r['result']);files[r['path']]=b;identities[r['path']]=identity(b)
    else:
        assert r['path'].endswith('.zip')
        b=(ARCHIVES/Path(r['path']).name).read_bytes();identities[r['path']]=identity(b)
        assert identities[r['path']]==r['computed_from_fresh_connector_content']
        assert identities[r['path']]['git_blob']==r['connector_sha']
assert set(identities)=={f['filename'] for f in c['files']}
for f in c['files']:assert f['sha']==identities[f['filename']]['git_blob']
m=parse(files[PREFIX+'MANIFEST.json'])
assert m['parent_commit']==PARENT and m['native_interaction']=='OPEN' and m['scientific_status']=='ACCEPTED_CONDITIONAL_ANALYTICAL_SCREEN'
assert set(m['files'])==set(identities)-{PREFIX+'MANIFEST.json'} and len(m['files'])==10
for p,i in m['files'].items():assert identities[p]==i
old=decode(parse(raw['final_parent_continuation_connector.json']))
append=files[PREFIX+'INDEX_APPEND.md'];assert len(old)==94729 and len(append)==1699
assert files[CONT]==old+append and len(files[CONT])==96428
audit=parse(files[PREFIX+'AUDIT.json']);assert audit['evidence_commit']==PARENT and audit['scientific_status']==m['scientific_status']
assert audit['native_interaction']==audit['broad_C3_C4_C6']=='OPEN'
for n,i in audit['raw_archives'].items():assert identities[PREFIX+n]==i
assert b'Native interaction and broad C3/C4' in files[BASE+'history_orientation/STATUS.md']
assert b'unsupported' in files[PREFIX+'README.md'] and b'modelVersion' in files[PREFIX+'README.md']
report=dict(status='IMMUTABLE_STABILIZATION_PUBLICATION_PASS',commit=SHA,parent=PARENT,tree=TREE,author=c['author']['login'],committer=c['committer']['login'],head_at_readback=meta['head']['object']['sha'],files=identities,changed_files=11,added_files=10,manifest_entries=10,continuation=dict(prior_bytes=len(old),append_bytes=len(append),published_bytes=len(files[CONT]),append_only=True),prior_raw_archives_reused=True,raw_readback=identity((HERE/'FINAL_AUDIT_RAW.zip').read_bytes()),scope='Publication/source identity and exact bytes only; no scientific execution or further Gemini review.',scientific_status=m['scientific_status'],native_interaction='OPEN',broad_C3_C4_C6='OPEN',no_numerical_replay=True,no_numbered_closure=True,receipt_qualifications_preserved=True)
(HERE/'FINAL_AUDIT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print('PASS: immutable stabilization commit, GPT identity, sole parent, tree, 11 complete file identities, 10-entry manifest and exact 1699-byte append.')
