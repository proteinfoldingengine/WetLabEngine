"""Independent remote byte audit (GitHub API readback) of the relational-reference review run.
Written separately from the review script; shares no code with it."""
import base64
import hashlib
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
REL = 'ResearchHistory/UQCF-GEM/research/physical-bridge/relational_reference_admission'
BASE = ROOT / REL
OUT = Path('relref_publication')
API = 'https://api.github.com/repos/proteinfoldingengine/WetLabEngine'
CHAIN = ['a22c4b3a512cb6d54521c7191ded99547f291c48', '75054cf359b34c274366becc9850d0c6281f92ae',
         '05b43cdabe3368784f5384d05d6fdec9cb4e7e94', '8129e79ee00608b6fc760532eff6360019e5f43a']


def parse(data):
    def unique(pairs):
        d = {}
        for k, v in pairs:
            assert k not in d, 'duplicate key'
            d[k] = v
        return d
    def bad(_):
        raise ValueError('nonfinite')
    return json.loads(data, object_pairs_hook=unique, parse_constant=bad)


def h(b):
    return hashlib.sha256(b).hexdigest()


def gblob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def get(path):
    req = urllib.request.Request(API + path, headers={'Accept': 'application/vnd.github+json',
                                 'Authorization': 'Bearer ' + os.environ['GH_READ_TOKEN']})
    with urllib.request.urlopen(req, timeout=60) as r:
        assert 'rel="next"' not in r.headers.get('Link', ''), 'pagination not inspected'
        return parse(r.read())


def put(name, obj):
    (OUT / name).write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')


def manifest_ok(root, required):
    assert not any(p.is_symlink() for p in root.rglob('*'))
    m = parse((root / 'file_manifest.json').read_bytes())
    files = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p != root / 'file_manifest.json'}
    assert set(m) == files and required <= files, 'artifact membership'
    for n, e in m.items():
        d = (root / n).read_bytes()
        assert e == {'bytes': len(d), 'sha256': h(d)}, 'artifact digest'
    return m


def run():
    OUT.mkdir(exist_ok=True)
    head = os.environ['GITHUB_SHA']
    assert head == os.environ['UQCF_WORKFLOW_SHA']
    commit = get('/commits/' + head)
    assert commit['author']['login'] == commit['committer']['login'] == 'proteinfolding-grokbot'
    sha = head
    for expected_parent in CHAIN:
        c = get('/git/commits/' + sha)
        assert [p['sha'] for p in c['parents']] == [expected_parent], 'ancestry'
        sha = expected_parent
    inputs = parse((BASE / 'input_manifest.json').read_bytes())
    checked = []
    def remote(blob_id, data, label):
        r = get('/git/blobs/' + blob_id)
        assert r['encoding'] == 'base64'
        got = base64.b64decode(r['content'])
        assert got == data and r['size'] == len(data) and gblob(got) == blob_id
        checked.append({'path': label, 'git_blob': blob_id, 'bytes': len(data), 'sha256': h(data)})
    for name, rec in sorted(inputs.items()):
        data = (ROOT / name).read_bytes()
        assert rec == {'bytes': len(data), 'sha256': h(data), 'git_blob': gblob(data)}
        assert get('/contents/' + name + '?ref=' + head)['sha'] == rec['git_blob']
        remote(rec['git_blob'], data, name)
    adm = REL + '/ADMISSION.md'
    assert get('/contents/' + adm + '?ref=' + CHAIN[2])['sha'] == inputs[adm]['git_blob'], 'frozen argument'
    for n in ('RECONSTRUCTION_CONTRACT.md', 'REVIEW_INSTRUCTIONS.txt'):
        assert get('/contents/' + REL + '/' + n + '?ref=' + CHAIN[0])['sha'] == inputs[REL + '/' + n]['git_blob'], 'frozen contract'
    mpath = REL + '/input_manifest.json'
    mbytes = (BASE / 'input_manifest.json').read_bytes()
    remote(get('/contents/' + mpath + '?ref=' + head)['sha'], mbytes, mpath)
    packet = parse((BASE / 'source_packet.json').read_bytes())
    assert packet['source_parent'] == CHAIN[3]
    for s in packet['files']:
        assert get('/contents/' + s['path'] + '?ref=' + CHAIN[3])['sha'] == s['git_blob'], 'source origin'
        remote(s['git_blob'], s['content'].encode(), 'source:' + s['path'])
    recon = Path('relref_reconstruction')
    manifest_ok(recon, {'certificate.json', 'provenance.json', 'reconstruction.log'})
    cert_bytes = (recon / 'certificate.json').read_bytes()
    cert = parse(cert_bytes)
    assert cert['status'] == 'GREEN' and cert['failures'] == [] and cert['record_count'] == cert['declared_count']
    review = Path('relref_review')
    req = {'provenance.json', 'prompt.txt', 'model_availability.json', 'response.json', 'review.txt', 'verdict.json', 'review_manifest.json'}
    manifest_ok(review, req)
    m = parse((review / 'review_manifest.json').read_bytes())
    assert m['scientific_sha'] == m['workflow_sha'] == head
    assert m['run_id'] == os.environ['GITHUB_RUN_ID'] and m['run_attempt'] == os.environ['GITHUB_RUN_ATTEMPT']
    assert m['inputs'] == inputs and m['certificate_sha256'] == h(cert_bytes)
    prompt = (review / 'prompt.txt').read_bytes()
    assert m['prompt_sha256'] == h(prompt)
    for n in ('ADMISSION.md', 'RECONSTRUCTION_CONTRACT.md', 'REVIEW_INSTRUCTIONS.txt'):
        assert (BASE / n).read_bytes() in prompt, 'prompt omits frozen ' + n
    assert cert_bytes in prompt, 'prompt omits certificate'
    assert m['model_requested'] == 'gemini-3.1-pro-preview'
    avail = parse((review / 'model_availability.json').read_bytes())
    assert avail['name'] == 'models/gemini-3.1-pro-preview' and 'generateContent' in avail['supportedGenerationMethods']
    resp_bytes = (review / 'response.json').read_bytes()
    assert m['raw_api_response_sha256'] == h(resp_bytes)
    resp = parse(resp_bytes)
    assert len(resp['candidates']) == 1 and resp['candidates'][0]['finishReason'] == 'STOP'
    assert m['model_returned'] == resp.get('modelVersion')
    texts = [p['text'] for p in resp['candidates'][0]['content']['parts'] if p.get('thought') is not True]
    raw = '\n'.join(texts).strip().encode()
    assert raw == (review / 'review.txt').read_bytes() and m['review_sha256'] == h(raw)
    verdict = parse((review / 'verdict.json').read_bytes())
    assert verdict == parse(raw)
    assert verdict['verdict'] == 'ACCEPTED' and all(verdict[k] == [] for k in ('findings', 'missing_assumptions', 'counterexamples'))
    put('remote_readback.json', {'verified': True, 'scientific_sha': head, 'run_id': os.environ['GITHUB_RUN_ID'],
        'run_attempt': os.environ['GITHUB_RUN_ATTEMPT'], 'author': commit['author']['login'], 'tree_sha': commit['commit']['tree']['sha'],
        'ancestry': [head] + CHAIN, 'checked': checked, 'certificate_sha256': h(cert_bytes), 'review_manifest': m,
        'scope': 'source, certificate and reviewed-byte consistency; not mathematical reconstruction or native mechanism certification'})
    d = (OUT / 'remote_readback.json').read_bytes()
    put('file_manifest.json', {'remote_readback.json': {'bytes': len(d), 'sha256': h(d)}})
    print('Immutable publication and source bytes verified:', len(checked))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('assertions required')
    try:
        run()
    except Exception as exc:
        OUT.mkdir(exist_ok=True)
        put('failure.json', {'status': 'PUBLICATION_AUDIT_FAILED', 'error_type': type(exc).__name__,
                             'assertion': str(exc) if isinstance(exc, AssertionError) else None})
        raise SystemExit('Publication audit failed; sanitized evidence retained.')
