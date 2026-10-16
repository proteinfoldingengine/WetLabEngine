"""Independent remote byte audit of an analytical document checkpoint."""
import base64
import hashlib
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'ResearchHistory/UQCF-GEM/research/physical-bridge/history_orientation'
OUT = Path('history_publication')
PREFIX = 'https://api.github.com/repos/proteinfoldingengine/WetLabEngine'

def parse(data):
    def unique(pairs):
        result = {}
        for key,value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def reject(value):
        raise ValueError('nonfinite JSON value')
    return json.loads(data,object_pairs_hook=unique,parse_constant=reject)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def request(path):
    headers = {'Accept':'application/vnd.github+json','Authorization':'Bearer '+os.environ['GH_READ_TOKEN']}
    with urllib.request.urlopen(urllib.request.Request(PREFIX+path,headers=headers),timeout=60) as r:
        if 'rel="next"' in r.headers.get('Link',''):
            raise ValueError('paginated response not fully inspected')
        return parse(r.read())

def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')

def run():
    OUT.mkdir(exist_ok=True)
    head = os.environ['GITHUB_SHA']
    assert head == os.environ['UQCF_WORKFLOW_SHA']
    commit = request('/commits/'+head)
    assert commit['author']['login'] == commit['committer']['login'] == 'proteinfolding-gpt'
    assert [p['sha'] for p in commit['parents']] == ['23c55d38a27e5081a1c92b3ed03f37adfb446687']
    first = request('/git/commits/23c55d38a27e5081a1c92b3ed03f37adfb446687')
    assert [p['sha'] for p in first['parents']] == ['68fcd6d6118f7cb30bdca88814d1a5dc8260f0da']
    contract = request('/git/commits/68fcd6d6118f7cb30bdca88814d1a5dc8260f0da')
    assert [p['sha'] for p in contract['parents']] == ['24dbac1a7da1a2484dd3d28f66c3b62c7ae632af']
    inputs = parse((BASE/'input_manifest.json').read_bytes())
    prefix = str(BASE.relative_to(ROOT))+'/'
    required = {prefix+n for n in ('CONTRACT.md','RESULT.md','source_packet.json','source_identities.json','CODEX_ARGUMENT_REVIEW.md','INFRASTRUCTURE_REVIEW.md','REVIEW_INSTRUCTIONS.txt','RETRY.md','RETRY_INFRASTRUCTURE_REVIEW.md')}
    required.update({'.github/scripts/uqcf_analytical_repair_review.py','.github/scripts/uqcf_history_orientation_review.py',
        '.github/scripts/uqcf_history_orientation_publication.py','.github/workflows/uqcf-gem-history-orientation.yml'})
    assert set(inputs) == required
    expected_changed = set(inputs) - {'.github/scripts/uqcf_analytical_repair_review.py',str((BASE/'CONTRACT.md').relative_to(ROOT))}
    expected_changed.add(str((BASE/'input_manifest.json').relative_to(ROOT)))
    cumulative = request('/compare/68fcd6d6118f7cb30bdca88814d1a5dc8260f0da...'+head)
    assert cumulative['status'] == 'ahead' and cumulative['ahead_by'] == 2
    assert {f['filename'] for f in cumulative['files']} == expected_changed
    assert all(f['status'] == 'added' for f in cumulative['files'])
    checked = []
    def remote_blob(blob_id,expected,name):
        response = request('/git/blobs/'+blob_id)
        assert response['encoding'] == 'base64'
        data = base64.b64decode(response['content'])
        assert data == expected
        assert response['size'] == len(data)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == blob_id
        checked.append({'path':name,'git_blob':blob_id,'bytes':len(data),'sha256':sha(data)})
    file_index = {x['filename']:x for x in cumulative['files']}
    for name,record in inputs.items():
        data = (ROOT/name).read_bytes()
        assert record == {'bytes':len(data),'sha256':sha(data),'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}
        if name in file_index:
            assert file_index[name]['sha'] == record['git_blob']
        else:
            content = request('/contents/'+name+'?ref='+head)
            assert content['sha'] == record['git_blob']
        remote_blob(record['git_blob'],data,name)
    manifest_path = str((BASE/'input_manifest.json').relative_to(ROOT))
    remote_blob(file_index[manifest_path]['sha'],(BASE/'input_manifest.json').read_bytes(),manifest_path)
    packet = parse((BASE/'source_packet.json').read_bytes())
    assert packet['source_parent'] == '24dbac1a7da1a2484dd3d28f66c3b62c7ae632af'
    for source in packet['files']:
        # Bind blob to the declared original path, not just an unbound blob hash.
        origin = request('/contents/'+source['path']+'?ref='+packet['source_parent'])
        assert origin['sha'] == source['git_blob']
        remote_blob(source['git_blob'],source['content'].encode(),'original:'+source['path'])
    review = Path('history_review')
    manifest = parse((review/'file_manifest.json').read_bytes())
    required_review = {'provenance.json','prompt.txt','model_availability.json','response.json','review.txt','verdict.json','review_manifest.json'}
    assert not any(p.is_symlink() for p in review.rglob('*'))
    assert set(manifest) == required_review == {str(p.relative_to(review)) for p in review.rglob('*') if p.is_file() and p != review/'file_manifest.json'}
    for name,entry in manifest.items():
        data = (review/name).read_bytes()
        assert entry == {'bytes':len(data),'sha256':sha(data)}
    verdict = parse((review/'verdict.json').read_bytes())
    assert type(verdict) is dict
    assert all(type(verdict.get(k)) is list for k in ('findings','missing_assumptions','counterexamples','limitations'))
    assert verdict['verdict'] == 'ACCEPTED'
    assert all(verdict[k] == [] for k in ('findings','missing_assumptions','counterexamples'))
    assert verdict == parse((review/'review.txt').read_bytes())
    m = parse((review/'review_manifest.json').read_bytes())
    assert m['scientific_sha'] == m['workflow_sha'] == head
    assert m['run_id'] == os.environ['GITHUB_RUN_ID'] and m['run_attempt'] == os.environ['GITHUB_RUN_ATTEMPT']
    assert m['inputs'] == inputs
    expected_identity = {'scientific_sha':head,'workflow_sha':head,'run_id':os.environ['GITHUB_RUN_ID'],
        'run_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'source_parent':'24dbac1a7da1a2484dd3d28f66c3b62c7ae632af',
        'contract_commit':'68fcd6d6118f7cb30bdca88814d1a5dc8260f0da'}
    assert parse((review/'provenance.json').read_bytes()) == expected_identity
    assert all(m[k] == v for k,v in expected_identity.items())
    expected_prompt = (BASE/'REVIEW_INSTRUCTIONS.txt').read_text() + '\nEXACT IDENTITY\n' + json.dumps(expected_identity,sort_keys=True)
    for name in ('CONTRACT.md','RESULT.md'):
        expected_prompt += '\n\nCURRENT DOCUMENT '+name+'\n'+(BASE/name).read_text()
    expected_prompt += '\n\nPINNED FULL SOURCE PACKET\n'+(BASE/'source_packet.json').read_text()
    assert (review/'prompt.txt').read_bytes() == expected_prompt.encode()
    available = parse((review/'model_availability.json').read_bytes())
    assert available['name'] == 'models/gemini-3.1-pro-preview'
    assert 'generateContent' in available['supportedGenerationMethods']
    assert m['model_requested'] == 'gemini-3.1-pro-preview' 
    assert m['prompt_sha256'] == sha((review/'prompt.txt').read_bytes())
    assert m['review_sha256'] == sha((review/'review.txt').read_bytes())
    assert m['raw_api_response_sha256'] == sha((review/'response.json').read_bytes())
    response = parse((review/'response.json').read_bytes())
    assert type(response.get('candidates')) is list and len(response['candidates']) == 1
    assert type(response['candidates'][0]) is dict and type(response['candidates'][0].get('content')) is dict
    assert response['candidates'][0]['content']['role'] == 'model'
    assert m['model_returned'] == response.get('modelVersion')
    assert response['candidates'][0]['finishReason'] == 'STOP'
    parts = response['candidates'][0]['content']['parts']
    assert type(parts) is list and parts and all(type(p) is dict for p in parts)
    texts = []
    for part in parts:
        if part.get('thought') is True:
            continue
        assert type(part.get('text')) is str and not (set(part) - {'text','thought','thoughtSignature'})
        texts.append(part['text'])
    raw = '\n'.join(texts).strip()
    assert raw
    assert raw.encode() == (review/'review.txt').read_bytes()
    write('remote_readback.json',{'verified':True,'scientific_sha':head,'workflow_sha':head,'run_id':os.environ['GITHUB_RUN_ID'],
        'run_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'author':commit['author']['login'],'parents':[p['sha'] for p in commit['parents']],
        'tree_sha':commit['commit']['tree']['sha'],'changed_paths':sorted(expected_changed),'checked':checked,
        'review_manifest':m,'scope':'source and reviewed-byte consistency, not independent mathematical reconstruction or native mechanism certification'})
    write('file_manifest.json',{'remote_readback.json':{'bytes':(OUT/'remote_readback.json').stat().st_size,'sha256':sha((OUT/'remote_readback.json').read_bytes())}})
    print('Immutable publication and source bytes verified:',len(checked))

if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Audit requires assertions enabled; optimized execution rejected.')
    try:
        run()
    except Exception as exc:
        OUT.mkdir(exist_ok=True)
        write('failure.json',{'status':'PUBLICATION_AUDIT_FAILED','error_type':type(exc).__name__})
        raise SystemExit('Publication audit failed; sanitized evidence retained.')
