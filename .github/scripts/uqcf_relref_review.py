"""Integrity and secret-safe Gemini review for relational_reference_admission. Executes no science modules."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
REL = 'ResearchHistory/UQCF-GEM/research/physical-bridge/relational_reference_admission'
BASE = ROOT / REL
SOURCE_PARENT = '8129e79ee00608b6fc760532eff6360019e5f43a'
ARGUMENT_COMMIT = '05b43cdabe3368784f5384d05d6fdec9cb4e7e94'
INDEX_COMMIT = '75054cf359b34c274366becc9850d0c6281f92ae'
CONTRACT_COMMIT = 'a22c4b3a512cb6d54521c7191ded99547f291c48'
MODEL = 'gemini-3.1-pro-preview'
REQUIRED = {REL + '/' + n for n in ('ADMISSION.md', 'INDEX_APPEND.md', 'RECONSTRUCTION_CONTRACT.md', 'REVIEW_INSTRUCTIONS.txt',
            'source_packet.json', 'source_identities.json')} | {
            '.github/scripts/uqcf_relref_formula.py', '.github/scripts/uqcf_relref_checker.py',
            '.github/scripts/uqcf_relref_reconstruct.py', '.github/scripts/uqcf_relref_review.py',
            '.github/scripts/uqcf_relref_publication.py', '.github/workflows/uqcf-gem-relational-reference-review.yml'}
SCOPE = 'document identities only; no numerical science or inherited replay'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def strict(data):
    def unique(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise ValueError('duplicate JSON key')
            out[k] = v
        return out
    def reject(_):
        raise ValueError('non-finite JSON constant')
    obj = json.loads(data, object_pairs_hook=unique, parse_constant=reject)
    if type(obj) is not dict:
        raise ValueError('JSON object required')
    return obj


def write(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], stderr=subprocess.DEVNULL)


def parent(c):
    return git('show', '-s', '--format=%P', c).decode().strip()


def identity():
    head = git('rev-parse', 'HEAD').decode().strip()
    ident = {k: os.environ[v] for k, v in {'scientific_sha': 'GITHUB_SHA', 'workflow_sha': 'UQCF_WORKFLOW_SHA',
             'run_id': 'GITHUB_RUN_ID', 'run_attempt': 'GITHUB_RUN_ATTEMPT'}.items()}
    if head != ident['scientific_sha'] or head != ident['workflow_sha']:
        raise ValueError('source/workflow identity mismatch')
    if (parent(head) != CONTRACT_COMMIT or parent(CONTRACT_COMMIT) != INDEX_COMMIT
            or parent(INDEX_COMMIT) != ARGUMENT_COMMIT or parent(ARGUMENT_COMMIT) != SOURCE_PARENT):
        raise ValueError('checkpoint ancestry mismatch')
    ident.update(source_parent=SOURCE_PARENT, argument_commit=ARGUMENT_COMMIT, contract_commit=CONTRACT_COMMIT)
    return ident


def safe(name):
    p = Path(name)
    if p.is_absolute() or '..' in p.parts or str(p) != name:
        raise ValueError('invalid relative path')
    return p


def validate():
    ident = identity()
    inputs = strict((BASE / 'input_manifest.json').read_bytes())
    if set(inputs) != REQUIRED:
        raise ValueError('input membership mismatch')
    for name, expected in inputs.items():
        data = (ROOT / safe(name)).read_bytes()
        if expected != {'bytes': len(data), 'sha256': sha(data), 'git_blob': blob(data)}:
            raise ValueError('input digest mismatch')
        if git('show', ident['scientific_sha'] + ':' + name) != data:
            raise ValueError('checkout mismatch')
    if git('show', ARGUMENT_COMMIT + ':' + REL + '/ADMISSION.md') != (BASE / 'ADMISSION.md').read_bytes():
        raise ValueError('frozen argument altered')
    for n in ('RECONSTRUCTION_CONTRACT.md', 'REVIEW_INSTRUCTIONS.txt'):
        if git('show', CONTRACT_COMMIT + ':' + REL + '/' + n) != (BASE / n).read_bytes():
            raise ValueError('frozen contract altered')
    packet = strict((BASE / 'source_packet.json').read_bytes())
    if packet['source_parent'] != SOURCE_PARENT:
        raise ValueError('source parent mismatch')
    expected = json.loads((BASE / 'source_identities.json').read_bytes())
    files = packet['files']
    if len(files) != len(expected) or len({f['path'] for f in files}) != len(files):
        raise ValueError('source membership mismatch')
    actual = []
    for item in files:
        name = str(safe(item['path']))
        data = item['content'].encode()
        if item['ref'] != SOURCE_PARENT or blob(data) != item['git_blob'] or git('show', SOURCE_PARENT + ':' + name) != data:
            raise ValueError('source blob mismatch')
        actual.append({'path': name, 'ref': SOURCE_PARENT, 'git_blob': blob(data), 'bytes': len(data), 'sha256': sha(data)})
    if sorted(actual, key=lambda x: x['path']) != sorted(expected, key=lambda x: x['path']):
        raise ValueError('source identity mismatch')
    return ident, inputs, packet


def check_artifact(root, required):
    if any(p.is_symlink() for p in root.rglob('*')):
        raise ValueError('artifact symlink')
    manifest = strict((root / 'file_manifest.json').read_bytes())
    files = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p != root / 'file_manifest.json'}
    if files != set(manifest) or not required <= files:
        raise ValueError('artifact membership mismatch')
    for name, e in manifest.items():
        data = (root / safe(name)).read_bytes()
        if e != {'bytes': len(data), 'sha256': sha(data)}:
            raise ValueError('artifact altered')


def seal(out):
    write(out / 'file_manifest.json', {str(p.relative_to(out)): {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
          for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'file_manifest.json'})


def prompt_for(ident, certificate_text):
    text = (BASE / 'REVIEW_INSTRUCTIONS.txt').read_text() + '\nEXACT IDENTITY\n' + json.dumps(ident, sort_keys=True)
    for n in ('ADMISSION.md', 'RECONSTRUCTION_CONTRACT.md'):
        text += '\n\nFROZEN DOCUMENT ' + n + '\n' + (BASE / n).read_text()
    text += '\n\nRECONSTRUCTION CERTIFICATE (this run, reconstruction job)\n' + certificate_text
    text += '\n\nPINNED SOURCE PACKET (evidence at source parent)\n' + (BASE / 'source_packet.json').read_text()
    return text


def main():
    phase = sys.argv[1]
    out = Path('relref_' + phase)
    out.mkdir(exist_ok=True)
    try:
        ident, inputs, packet = validate()
        write(out / 'provenance.json', ident)
        if phase == 'integrity':
            write(out / 'integrity.json', {'verified': True, 'source_count': len(packet['files']), 'inputs': inputs, 'scope': SCOPE})
            seal(out)
            print('Exact document integrity verified:', len(inputs), 'inputs,', len(packet['files']), 'pinned sources')
            return
        if phase != 'review':
            raise ValueError('unknown phase')
        integ = Path('relref_integrity')
        check_artifact(integ, {'provenance.json', 'integrity.json'})
        if strict((integ / 'provenance.json').read_bytes()) != ident:
            raise ValueError('integrity provenance mismatch')
        recon = Path('relref_reconstruction')
        check_artifact(recon, {'certificate.json', 'provenance.json', 'reconstruction.log'})
        rp = strict((recon / 'provenance.json').read_bytes())
        if any(rp.get(k) != ident[k] for k in ('scientific_sha', 'workflow_sha', 'run_id', 'run_attempt')):
            raise ValueError('reconstruction provenance mismatch')
        cert_text = (recon / 'certificate.json').read_text()
        if strict(cert_text.encode())['status'] != 'GREEN':
            raise ValueError('reconstruction not GREEN')
        prompt = prompt_for(ident, cert_text)
        (out / 'prompt.txt').write_text(prompt)
        key = os.environ.get('GEMINI_API_KEY')
        if not key:
            raise ValueError('missing Actions secret')
        endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/' + MODEL
        # One availability check and one generation request; no speculative retries or model fallbacks.
        with urllib.request.urlopen(urllib.request.Request(endpoint, headers={'x-goog-api-key': key}), timeout=60) as resp:
            availability = resp.read()
        (out / 'model_availability.json').write_bytes(availability)
        avail = strict(availability)
        if avail.get('name') != 'models/' + MODEL or 'generateContent' not in avail.get('supportedGenerationMethods', []):
            raise ValueError('model unavailable')
        payload = {'contents': [{'parts': [{'text': prompt}]}],
                   'generationConfig': {'temperature': 0, 'maxOutputTokens': 32768, 'responseMimeType': 'application/json'}}
        req = urllib.request.Request(endpoint + ':generateContent', data=json.dumps(payload).encode(),
                                     headers={'Content-Type': 'application/json', 'x-goog-api-key': key}, method='POST')
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = resp.read()
        (out / 'response.json').write_bytes(data)
        result = strict(data)
        cands = result.get('candidates')
        if type(cands) is not list or len(cands) != 1 or cands[0].get('finishReason') != 'STOP':
            raise ValueError('incomplete response')
        content = cands[0].get('content')
        if type(content) is not dict or content.get('role') != 'model':
            raise ValueError('invalid content')
        texts = []
        for part in content.get('parts', []):
            if part.get('thought') is True:
                continue
            if type(part.get('text')) is not str or set(part) - {'text', 'thought', 'thoughtSignature'}:
                raise ValueError('unexpected part')
            texts.append(part['text'])
        raw = '\n'.join(texts).strip()
        if not raw:
            raise ValueError('empty response')
        (out / 'review.txt').write_text(raw)
        verdict = strict(raw.encode())
        if verdict.get('verdict') not in ('ACCEPTED', 'REVISE', 'FAIL') or not all(
                type(verdict.get(k)) is list for k in ('findings', 'missing_assumptions', 'counterexamples', 'limitations')):
            raise ValueError('invalid review schema')
        write(out / 'verdict.json', verdict)
        write(out / 'review_manifest.json', {**ident, 'model_requested': MODEL, 'model_returned': result.get('modelVersion'),
              'prompt_sha256': sha(prompt.encode()), 'raw_api_response_sha256': sha(data), 'review_sha256': sha(raw.encode()),
              'certificate_sha256': sha(cert_text.encode()), 'inputs': inputs})
        seal(out)
        print('GEMINI_RAW_REVIEW_BEGIN\n' + raw + '\nGEMINI_RAW_REVIEW_END')
        if not (verdict['verdict'] == 'ACCEPTED' and not any(verdict[k] for k in ('findings', 'missing_assumptions', 'counterexamples'))):
            raise SystemExit('Independent review requires reconciliation (verdict ' + verdict['verdict'] + ').')
    except SystemExit:
        raise
    except Exception as exc:
        # Never print exception strings, URLs or headers: they may carry credentials.
        write(out / 'infrastructure_failure.json', {'status': 'INFRASTRUCTURE_FAILURE_NOT_MATHEMATICAL_VERDICT',
              'error_type': type(exc).__name__, 'error_class_message': str(exc) if isinstance(exc, ValueError) else None,
              'http_status': exc.code if isinstance(exc, urllib.error.HTTPError) else None})
        seal(out)
        raise SystemExit('Review infrastructure failed; sanitized evidence retained.')


if __name__ == '__main__':
    main()
