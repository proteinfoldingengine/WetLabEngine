"""Review-infrastructure controls only; no scientific program is executed."""
import hashlib, json, tempfile
from pathlib import Path
import uqcf_shifted_boundary_response_review as review
import uqcf_shifted_boundary_response_publication as audit
import uqcf_preparability_review as model

p=review.BASE
packet=json.loads((p/'SOURCE_PACKET.json').read_text())
sources=[{'full':review.remote(r['commit'], r['path']).decode('utf-8')} for r in packet['sources']]
rejected=0
for source,record in zip(sources,packet['sources'],strict=True):
    raw=source['full'].encode()
    assert review.verify_source_excerpt(record,raw)==audit.audit_source_excerpt(record,raw)
    for field,value in [('full_bytes',len(raw)+1),('full_sha256','0'*64),('git_blob','0'*40),('byte_start',-1),('byte_end',len(raw)+1),('content',record['content']+'tamper')]:
        bad=dict(record); bad[field]=value
        for checker in (review.verify_source_excerpt,audit.audit_source_excerpt):
            try: checker(bad,raw)
            except ValueError: rejected+=1
            else: raise AssertionError((record['path'],field))
review.BASE=p
docs=review.inputs()
expected=review.HEADER.encode()
for name in review.FILES:
    expected+=f'\nEXACT DOCUMENT {name}\nUTF8-BYTES {len(docs[name])}\n'.encode()+docs[name]+b'\nEND EXACT DOCUMENT\n'
assert review.prompt(docs)==expected
with tempfile.TemporaryDirectory() as directory:
    target=Path(directory)
    for name,raw in docs.items(): (target/name).write_bytes(raw)
    (target/'RESULT.md').write_bytes(docs['RESULT.md']+b'tamper')
    review.BASE=target
    try: review.inputs()
    except ValueError: rejected+=1
    else: raise AssertionError('Altered proof passed freeze')
assert review.SCIENCE==audit.SCIENCE=='6ee2d3f4e686a661466bbba930090c60149d138e'
assert model.MODEL==audit.MODEL=='gemini-3.1-pro-preview'
print(json.dumps({'status':'PASS','source_identity_pairs':len(sources),'rejecting_infrastructure_controls':rejected,'prompt_bytes':len(expected),'prompt_sha256':hashlib.sha256(expected).hexdigest(),'scientific_execution':False}))
