"""Document-only source integrity and secret-safe review; executes no science modules."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'ResearchHistory/UQCF-GEM/research/physical-bridge/history_orientation'
PARENT = '24dbac1a7da1a2484dd3d28f66c3b62c7ae632af'
CONTRACT = '68fcd6d6118f7cb30bdca88814d1a5dc8260f0da'
FIRST = '23c55d38a27e5081a1c92b3ed03f37adfb446687'
MODEL = 'gemini-3.1-pro-preview'
spec = importlib.util.spec_from_file_location('review_helpers', ROOT / '.github/scripts/uqcf_analytical_repair_review.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], stderr=subprocess.DEVNULL)

def identity():
    head = git('rev-parse', 'HEAD').decode().strip()
    result = {k: os.environ[v] for k, v in {
        'scientific_sha':'GITHUB_SHA', 'workflow_sha':'UQCF_WORKFLOW_SHA',
        'run_id':'GITHUB_RUN_ID', 'run_attempt':'GITHUB_RUN_ATTEMPT'}.items()}
    if head != result['scientific_sha'] or head != result['workflow_sha']:
        raise ValueError('source/workflow identity mismatch')
    if git('show', '-s', '--format=%P', head).decode().strip() != FIRST or git('show', '-s', '--format=%P', FIRST).decode().strip() != CONTRACT or git('show', '-s', '--format=%P', CONTRACT).decode().strip() != PARENT:
        raise ValueError('checkpoint ancestry mismatch')
    result.update(source_parent=PARENT, contract_commit=CONTRACT)
    return result

def safe_path(name):
    p = Path(name)
    if p.is_absolute() or '..' in p.parts or str(p) != name:
        raise ValueError('invalid relative path')
    return p

def validate():
    ident = identity()
    inputs = helpers.strict_object((BASE / 'input_manifest.json').read_bytes())
    prefix = str(BASE.relative_to(ROOT)) + '/'
    required = {prefix + n for n in ('CONTRACT.md','RESULT.md','source_packet.json','source_identities.json',
                'CODEX_ARGUMENT_REVIEW.md','INFRASTRUCTURE_REVIEW.md','REVIEW_INSTRUCTIONS.txt','RETRY.md','RETRY_INFRASTRUCTURE_REVIEW.md')}
    required.update({'.github/scripts/uqcf_analytical_repair_review.py',
        '.github/scripts/uqcf_history_orientation_review.py', '.github/scripts/uqcf_history_orientation_publication.py',
        '.github/workflows/uqcf-gem-history-orientation.yml'})
    if set(inputs) != required:
        raise ValueError('input membership mismatch')
    for name, expected in inputs.items():
        p = ROOT / safe_path(name)
        data = p.read_bytes()
        if expected != {'bytes':len(data), 'sha256':digest(data), 'git_blob':blob(data)}:
            raise ValueError('input digest mismatch')
        if git('show', ident['scientific_sha'] + ':' + name) != data:
            raise ValueError('checkout mismatch')
    packet = helpers.strict_object((BASE / 'source_packet.json').read_bytes())
    if packet['source_parent'] != PARENT:
        raise ValueError('source parent mismatch')
    expected_sources = json.loads((BASE / 'source_identities.json').read_bytes())
    if len({r['path'] for r in expected_sources}) != len(expected_sources):
        raise ValueError('duplicate source identity')
    sources = packet['files']
    if len(sources) != len(expected_sources) or len({r['path'] for r in sources}) != len(sources):
        raise ValueError('source membership mismatch')
    actual = []
    for item in sources:
        name = str(safe_path(item['path']))
        data = item['content'].encode()
        if item['ref'] != PARENT or blob(data) != item['git_blob']:
            raise ValueError('source blob mismatch')
        if git('show', PARENT + ':' + name) != data:
            raise ValueError('source packet mismatch')
        actual.append({'path':name, 'ref':PARENT, 'git_blob':blob(data), 'bytes':len(data), 'sha256':digest(data)})
    if sorted(actual, key=lambda x:x['path']) != sorted(expected_sources, key=lambda x:x['path']):
        raise ValueError('source identity mismatch')
    contract_path = str((BASE / 'CONTRACT.md').relative_to(ROOT))
    if git('show', CONTRACT + ':' + contract_path) != (BASE / 'CONTRACT.md').read_bytes():
        raise ValueError('frozen contract altered')
    return ident, inputs, packet

def seal(out):
    write(out / 'file_manifest.json', {str(p.relative_to(out)):{'bytes':p.stat().st_size, 'sha256':digest(p.read_bytes())}
          for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'file_manifest.json'})

def main():
    phase = sys.argv[1]
    out = Path('history_' + phase)
    out.mkdir(exist_ok=True)
    try:
        ident, inputs, packet = validate()
        write(out / 'provenance.json', ident)
        if phase == 'integrity':
            write(out / 'integrity.json', {'verified':True, 'source_count':len(packet['files']), 'inputs':inputs,
                'scope':'document identities only; no numerical science or inherited replay'})
            for name in inputs:
                dest = out / 'snapshot' / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes((ROOT / name).read_bytes())
            (out / 'input_manifest.json').write_bytes((BASE / 'input_manifest.json').read_bytes())
            seal(out)
            print('Exact document integrity verified:', len(packet['files']), 'pinned sources')
            return
        if phase != 'review':
            raise ValueError('unknown phase')
        prior = Path('history_integrity')
        manifest = helpers.strict_object((prior / 'file_manifest.json').read_bytes())
        files = {str(p.relative_to(prior)) for p in prior.rglob('*') if p.is_file() and p != prior/'file_manifest.json'}
        required_artifact = {'provenance.json','integrity.json','input_manifest.json'} | {'snapshot/'+name for name in inputs}
        if any(p.is_symlink() for p in prior.rglob('*')):
            raise ValueError('artifact symlink')
        if files != set(manifest) or files != required_artifact:
            raise ValueError('integrity artifact membership mismatch')
        for name, expected in manifest.items():
            data = (prior / safe_path(name)).read_bytes()
            if expected != {'bytes':len(data),'sha256':digest(data)}:
                raise ValueError('integrity artifact altered')
        if helpers.strict_object((prior/'provenance.json').read_bytes()) != ident:
            raise ValueError('integrity artifact provenance mismatch')
        if helpers.strict_object((prior/'integrity.json').read_bytes()) != {'verified':True,'source_count':len(packet['files']),'inputs':inputs,'scope':'document identities only; no numerical science or inherited replay'}:
            raise ValueError('integrity verdict mismatch')
        if (prior/'input_manifest.json').read_bytes() != (BASE/'input_manifest.json').read_bytes():
            raise ValueError('input manifest artifact mismatch')
        for name in inputs:
            if (prior/'snapshot'/name).read_bytes() != (ROOT/name).read_bytes():
                raise ValueError('review snapshot mismatch')
        instruction = (BASE/'REVIEW_INSTRUCTIONS.txt').read_text()
        prompt = instruction + '\nEXACT IDENTITY\n' + json.dumps(ident,sort_keys=True)
        for name in ('CONTRACT.md','RESULT.md'):
            prompt += '\n\nCURRENT DOCUMENT '+name+'\n'+(BASE/name).read_text()
        prompt += '\n\nPINNED FULL SOURCE PACKET\n' + (BASE/'source_packet.json').read_text()
        (out/'prompt.txt').write_text(prompt)
        key = os.environ.get('GEMINI_API_KEY')
        if not key:
            raise ValueError('missing Actions secret')
        endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/' + MODEL
        # One availability check and one generation request; no speculative model retries.
        with urllib.request.urlopen(urllib.request.Request(endpoint,headers={'x-goog-api-key':key}),timeout=60) as response:
            availability = response.read()
        (out/'model_availability.json').write_bytes(availability)
        available = helpers.strict_object(availability)
        if available.get('name') != 'models/'+MODEL or 'generateContent' not in available.get('supportedGenerationMethods',[]):
            raise ValueError('model unavailable')
        payload = {'contents':[{'parts':[{'text':prompt}]}], 'generationConfig':{'temperature':0,'maxOutputTokens':16384,'responseMimeType':'application/json'}}
        req = urllib.request.Request(endpoint+':generateContent',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','x-goog-api-key':key},method='POST')
        with urllib.request.urlopen(req,timeout=240) as response:
            data = response.read()
        (out/'response.json').write_bytes(data)
        result = helpers.strict_object(data)
        raw = helpers.response_text(result)
        (out/'review.txt').write_text(raw)
        verdict = helpers.validate_verdict(helpers.strict_object(raw))
        write(out/'verdict.json',verdict)
        write(out/'review_manifest.json',{**ident,'model_requested':MODEL,'model_returned':result.get('modelVersion'),
            'prompt_sha256':digest(prompt.encode()),'raw_api_response_sha256':digest(data),'review_sha256':digest(raw.encode()),'inputs':inputs})
        seal(out)
        print('GEMINI_RAW_REVIEW_BEGIN\n'+raw+'\nGEMINI_RAW_REVIEW_END')
        if not helpers.accepted(verdict):
            raise SystemExit('Independent review requires reconciliation.')
    except Exception as exc:
        # No exception strings/URLs/headers: they may contain credentials.
        write(out/'infrastructure_failure.json',{'status':'INFRASTRUCTURE_FAILURE_NOT_MATHEMATICAL_VERDICT','error_type':type(exc).__name__,
            'http_status':exc.code if isinstance(exc,urllib.error.HTTPError) else None})
        seal(out)
        raise SystemExit('Review infrastructure failed; sanitized evidence retained.')

if __name__ == '__main__':
    main()
