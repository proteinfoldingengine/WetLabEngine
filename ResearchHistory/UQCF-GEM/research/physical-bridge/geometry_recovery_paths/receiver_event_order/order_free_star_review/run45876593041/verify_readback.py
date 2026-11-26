"""Check the raw first review, its schema rejection and the already-passing data replay."""
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZipFile
here=Path(__file__).resolve().parent
meta=json.loads((here/'MANIFEST.json').read_bytes())
for name,info in meta['archives'].items():
    payload=(here/(name+'.zip')).read_bytes()
    assert len(payload)==info['bytes'] and sha256(payload).hexdigest()==info['sha256']
with ZipFile(here/'order-free-star-review.zip') as z:
    parts=json.loads(z.read('response.json'))['candidates'][0]['content']['parts']
    answer=json.loads('\n'.join(p['text'] for p in parts if 'text' in p and not p.get('thought')))
    assert 'verdict' not in answer and answer['program_status']=='ACCEPTED'
    assert json.loads(z.read('request.json'))['contents'][0]['parts'][0]['text'].encode()==z.read('prompt.txt')
    assert json.loads(z.read('archive.json'))=={'archived_states':[2099,1243]}
    assert json.loads(z.read('trace.json'))['census']['same_first_gained_leaf']==1248
print('PASS: failed review preserved as returned')
