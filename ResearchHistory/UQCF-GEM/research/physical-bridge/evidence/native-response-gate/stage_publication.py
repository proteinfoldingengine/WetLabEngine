"""Stage the native-response candidate gate, not a scientific campaign."""
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
B = 'ResearchHistory/UQCF-GEM/research/physical-bridge/'
E = B+'evidence/native-response-gate/'

def hashes(data):
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest())

a = json.loads((P/'source_readbacks.json').read_text())
assert a['commit'] == '284b1f8b2e6200e358fc7d92a4be9f35292930fb'
assert len(a['sources']) == 27
for x in a['sources']:
    assert hashes((P/'sources'/x['path']).read_bytes()) == dict(bytes=x['bytes'], sha256=x['sha256'], git_blob=x['sha']), x['path']
assert '**ACCEPTED**' in (P/'REVIEW.md').read_text()
indices = ['COUPLED_C3_C4_DEFICIT_CONTINUATION.md','POST_A12_THEOREM_FIRST_SYNTHESIS.md']
for n in indices:
    assert (P/n).read_bytes().startswith((P/'sources'/B/n).read_bytes())
mapping = {
    'GATE.md':B+'COUPLED_C3_TARGET_BLIND_RESPONSE_GATE.md',
    'OBSTRUCTION_REGISTER.md':B+'COUPLED_C3_SOURCE_RESPONSE_OBSTRUCTION_REGISTER.md',
    'REVIEW.md':B+'COUPLED_C3_TARGET_BLIND_RESPONSE_REVIEW.md',
    **{n:B+n for n in indices},
    **{n:E+n for n in ['PLAN.md','PLAN_CURRENT.md','PUBLICATION.md','source_readbacks.json','stage_publication.py']},
}
for n in ['binding.json','immutable_readback.json']:
    if (P/n).exists(): mapping[n] = E+n
entries = []
manifest = {'classification':'prospective candidate gate and bounded source assessment; no scientific execution', 'source_commit':a['commit'], 'files':{}}
for local, remote in mapping.items():
    b = (P/local).read_bytes()
    entries.append(dict(path=remote, mode='100644', type='blob', content=b.decode()))
    manifest['files'][remote] = hashes(b)
t = json.dumps(manifest, indent=2, sort_keys=True)+'\n'
(P/'publication_hash_manifest.json').write_text(t)
entries.append(dict(path=E+'publication_hash_manifest.json',mode='100644',type='blob',content=t))
(P/'publication_entries.json').write_text(json.dumps(entries)+'\n')
print(json.dumps({'texts':len(entries),'sources_verified':len(a['sources']),'indices_append_only':True,'new_scientific_tests':0}))
