"""Stage the event-binding source probe, not a scientific campaign."""
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
B = 'ResearchHistory/UQCF-GEM/research/physical-bridge/'
E = B+'evidence/event-binding-probe/'

def hashes(data):
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest())

a = json.loads((P/'source_readbacks.json').read_text())
assert a['commit'] == 'ba999041ae68e3d4bde4b88164d962c7ae41d49b'
assert len(a['sources']) == 13
for x in a['sources']:
    assert hashes((P/'sources'/x['path']).read_bytes()) == dict(bytes=x['bytes'], sha256=x['sha256'], git_blob=x['sha']), x['path']
assert '**ACCEPTED**' in (P/'REVIEW.md').read_text()
indices = ['COUPLED_C3_C4_DEFICIT_CONTINUATION.md','POST_A12_THEOREM_FIRST_SYNTHESIS.md','COUPLED_C3_SOURCE_RESPONSE_OBSTRUCTION_REGISTER.md']
for n in indices:
    assert (P/n).read_bytes().startswith((P/'sources'/B/n).read_bytes())
mapping = {
    'RESULT.md':B+'COUPLED_C3_EVENT_BINDING_PROBE.md',
    'REVIEW.md':B+'COUPLED_C3_EVENT_BINDING_PROBE_REVIEW.md',
    **{n:B+n for n in indices},
    **{n:E+n for n in ['PLAN.md','PLAN_CURRENT.md','PUBLICATION.md','source_readbacks.json','stage_publication.py']},
}
for n in ['binding.json','immutable_readback.json','integration_readbacks.json']:
    if (P/n).exists(): mapping[n] = E+n
entries = []
manifest = {'classification':'event-binding producer source assessment; no scientific execution', 'source_commit':a['commit'], 'files':{}}
for local, remote in mapping.items():
    b = (P/local).read_bytes()
    entries.append(dict(path=remote, mode='100644', type='blob', content=b.decode()))
    manifest['files'][remote] = hashes(b)
t = json.dumps(manifest, indent=2, sort_keys=True)+'\n'
(P/'publication_hash_manifest.json').write_text(t)
entries.append(dict(path=E+'publication_hash_manifest.json',mode='100644',type='blob',content=t))
(P/'publication_entries.json').write_text(json.dumps(entries)+'\n')
print(json.dumps({'texts':len(entries),'sources_verified':len(a['sources']),'indices_append_only':True,'new_scientific_tests':0}))
