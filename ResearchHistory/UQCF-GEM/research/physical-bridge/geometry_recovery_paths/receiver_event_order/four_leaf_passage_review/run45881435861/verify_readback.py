"""Verify downloaded bytes, scientific outputs, raw external review and foundation certificate."""
from contextlib import ExitStack
from hashlib import sha1,sha256
import json
import lzma
from pathlib import Path
from zipfile import ZipFile

root=Path(__file__).resolve().parent
meta=json.loads((root/'MANIFEST.json').read_bytes())
def digest(b):return sha256(b).hexdigest()
def blob(b):return sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with ExitStack() as stack:
    zs={}
    for name,entry in meta['archives'].items():
        f=root/(name+'.zip')
        assert f.stat().st_size==entry['bytes'] and digest(f.read_bytes())==entry['sha256']
        z=zs[name]=stack.enter_context(ZipFile(f))
        assert z.testzip() is None
        if 'SHA256SUMS' in z.namelist():
            for line in z.read('SHA256SUMS').decode().splitlines():
                h,p=line.split(None,1);assert digest(z.read(p.strip()))==h
    r=zs['four-leaf-passage-review'];p=zs['four-leaf-passage-publication'];f=zs['four-leaf-passage-foundation']
    for name in ('search.json','replay.json','verification.json','receipt.json','review.txt','response.json'):
        assert r.read(name)==p.read(name)
    rec=json.loads(r.read('receipt.json'))
    assert rec['checkout_sha']==rec['workflow_sha']==meta['science'] and int(rec['run_id'])==meta['run']
    assert json.loads(p.read('publication_audit.json'))=={'audit':'PASS',**rec}
    for k in ('prompt','request','response'):
        name=k+('.txt' if k=='prompt' else '.json')
        assert digest(r.read(name))==rec[k+'_sha256']
    assert json.loads(r.read('request.json'))['contents'][0]['parts'][0]['text'].encode()==r.read('prompt.txt')
    response=json.loads(r.read('response.json'));parts=response['candidates'][0]['content']['parts']
    answer='\n'.join(x['text'] for x in parts if 'text' in x and not x.get('thought')).strip()
    assert answer.encode()==r.read('review.txt')
    a=json.loads(answer);assert (a['verdict'],a['program_status'],a['native_bridge_status'])==('ACCEPTED','DERIVED','OPEN')
    assert all(a[k]==[] for k in ('findings','missing_assumptions','counterexamples'))
    assert rec['model_requested']=='gemini-3.1-pro-preview' and rec['model_returned']==response['modelVersion']
    for path,sha in rec['source_blobs'].items():
        if '/four_leaf_local_passage/' in path:
            assert blob(p.read(Path(path).name))==sha
    v=json.loads(r.read('verification.json'));assert v['archive_states']==2507 and v['paired_q']['2-3']==288
    x=json.loads(r.read('replay.json'))['cases'][1];assert x['counts']['receiver_comparisons']==86400
    if 'source.json' in r.namelist():
        assert r.read('source.json')==p.read('source.json')
        c=json.loads(r.read('source.json'))['cases']
        assert len(c)==11 and [(z['source'],z['leaf']) for z in c if z['first_loss']==2]==[(0,1)]
    assert f.read('SHA256SUMS')==p.read('foundation-checksums.txt')
    assert f.read('workflow-head.txt').decode().strip()==meta['science']
    assert f.read('inherited-head.txt').decode().strip()==meta['historical']
    report=json.loads(f.read('TEST_RECEIPT.json'));assert report['passed'] and report['tests_run']==22
    assert json.loads(f.read('VERIFICATION.json'))['all_valid'] and json.loads(f.read('REPRODUCED_1615F.json'))['all_valid']
    assert digest(lzma.decompress(f.read('certificates.json.xz')))=='21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6'
print('PASS',meta['run'],a['verdict'],rec['model_returned'])
