from hashlib import sha256
import json
import lzma
from pathlib import Path
import sys
import zipfile

root = Path(__file__).resolve().parent
meta = json.loads((root / 'MANIFEST.json').read_bytes())
archives = {}
for key, entry in meta['archives'].items():
    path = root / (key+'.zip')
    assert 'sha256:'+sha256(path.read_bytes()).hexdigest() == entry['digest']
    z = archives[key] = zipfile.ZipFile(path)
    assert z.testzip() is None
    if 'SHA256SUMS' in z.namelist():
        for row in z.read('SHA256SUMS').decode().splitlines():
            digest, name = row.split(None,1)
            assert sha256(z.read(name.strip())).hexdigest() == digest
for key, entry in meta['previous_reviews'].items():
    path = root / (key+'.zip')
    assert 'sha256:'+sha256(path.read_bytes()).hexdigest() == entry['digest']
    with zipfile.ZipFile(path) as old:
        assert old.testzip() is None
        earlier = json.loads(old.read('review.txt'))
        assert earlier['verdict'] == 'ACCEPTED'
        assert earlier['check_values']['states_per_arm'] == (189 if key=='earlier_schema_review' else 9)
sci = Path(sys.argv[1])
review, replay, pub, foundation = (archives[k] for k in ('review','replay','publication','foundation'))
vr = json.loads(review.read('review.txt'))
receipt = json.loads(review.read('receipt.json'))
response = json.loads(review.read('response.json'))
parts = response['candidates'][0]['content']['parts']
answer = '\n'.join(p['text'] for p in parts if 'text' in p and not p.get('thought')).strip().encode()
assert answer == review.read('review.txt') == pub.read('review.txt')
assert pub.read('response.json') == review.read('response.json')
assert json.loads(pub.read('receipt.json')) == receipt
assert json.loads(pub.read('publication_audit.json')) == {'audit':'PASS',**receipt}
for key, name in [('response','response.json'),('request','request.json'),('prompt','prompt.txt')]:
    assert receipt[key+'_sha256'] == sha256(review.read(name)).hexdigest()
assert json.loads(review.read('request.json'))['contents'][0]['parts'][0]['text'].encode()==review.read('prompt.txt')
assert receipt['checkout_sha'] == receipt['workflow_sha'] == meta['review_commit']
assert int(receipt['run_id']) == meta['run']
assert vr['verdict']=='ACCEPTED' and vr['native_bridge_status']=='OPEN'
assert all(vr[k]==[] for k in ('findings','missing_assumptions','counterexamples'))
assert vr['check_values']==dict(B_to_F_jumps=[1,9],old_B=[[8,1,1],[6,3,1]],child_jumps=[[4,4],[1,9]],parent_jump=25,post_B_states_per_arm=189,written_states_per_arm=9,terminal_visibility=[12,12])
assert set(vr['proof_checks'])=={'work','visibility','locality','compatibility','scale','scope'}
assert replay.read('result.json')==pub.read('result.json')==(sci/'result.json').read_bytes()
assert replay.read('raw.json')==pub.read('raw.json')==lzma.decompress((sci/'raw.json.xz').read_bytes())
assert sha256(lzma.decompress(foundation.read('certificates.json.xz'))).hexdigest()=='21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6'
print(json.dumps({'model':receipt['model_returned'],'verdict':vr['verdict'],'values':vr['check_values'],'visibility':vr['proof_checks']['visibility'],'scope':vr['limitations']}))
