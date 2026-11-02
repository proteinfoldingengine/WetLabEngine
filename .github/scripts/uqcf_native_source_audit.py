"""Bounded source audit, unchanged inherited replay, and exact review readback."""
from pathlib import Path
import hashlib
import json
import lzma
import os
import shutil
import subprocess
import sys
import urllib.error

SCIENCE = '2f7a788f551face7b69521b0d07d2ec3e3ea3871'
BASE = Path('ResearchHistory/UQCF-GEM/research/physical-bridge/native_joint_source_audit')
CONTROLLER = Path(__file__).resolve().parents[2]
MODEL = 'gemini-3.1-pro-preview'
DOCS = ('PLAN.md', 'PROMPT.txt', 'SOURCE_PACKET.json')

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(out, name, obj):
    (out / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')

def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)

def require(ok, message):
    if not ok:
        raise ValueError(message)

def identity(root):
    return dict(source_sha=SCIENCE, checkout_sha=git(root, 'rev-parse', 'HEAD').decode().strip(),
                controller_sha=git(CONTROLLER, 'rev-parse', 'HEAD').decode().strip(),
                workflow_sha=os.environ.get('UQCF_WORKFLOW_SHA'),
                run_id=os.environ.get('GITHUB_RUN_ID'), run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'))

def documents():
    docs = {n: (CONTROLLER / BASE / n).read_bytes() for n in DOCS}
    freeze = json.loads((CONTROLLER / BASE / 'FREEZE.json').read_bytes())
    require(freeze['source_sha'] == SCIENCE, 'Frozen source revision mismatch')
    require(freeze['documents'] == {n: sha(v) for n, v in docs.items()}, 'Frozen documents mismatch')
    for path, expected in freeze['controller_files'].items():
        require(sha((CONTROLLER / path).read_bytes()) == expected, 'Frozen controller file mismatch')
    return docs

def build_prompt(docs):
    raw = docs['PROMPT.txt']
    for name in ('PLAN.md', 'SOURCE_PACKET.json'):
        raw += ('\nEXACT DOCUMENT ' + name + '\nUTF8-BYTES ' + str(len(docs[name])) + '\n').encode()
        raw += docs[name] + b'\nEND EXACT DOCUMENT\n'
    return raw

def integrity(root, out):
    info = identity(root)
    require(info['checkout_sha'] == SCIENCE, 'Wrong source checkout')
    require(info['workflow_sha'] in (None, info['controller_sha']), 'Wrong workflow/controller checkout')
    docs = documents()
    packet = json.loads(docs['SOURCE_PACKET.json'])
    require(packet['source_commit'] == SCIENCE, 'Wrong packet revision')
    seen, rows = set(), []
    for source in packet['sources']:
        p = source['path']
        require(p not in seen and not p.startswith('/') and '..' not in Path(p).parts, 'Invalid or duplicate path')
        seen.add(p)
        raw = git(root, 'show', SCIENCE + ':' + p)
        blob = git(root, 'rev-parse', SCIENCE + ':' + p).decode().strip()
        require(raw == source['content'].encode(), 'Source bytes mismatch')
        require(len(raw) == source['bytes'] and sha(raw) == source['sha256'] and blob == source['git_blob'], 'Source identity mismatch')
        rows.append({k: source[k] for k in ('path', 'bytes', 'sha256', 'git_blob')})
    require(len(rows) == 19, 'Unexpected source set')
    for n, raw in docs.items():
        (out / n).write_bytes(raw)
    shutil.copyfile(CONTROLLER / BASE / 'FREEZE.json', out / 'FREEZE.json')
    write(out, 'integrity.json', dict(info, status='PASS', sources=rows,
          documents={n: sha(v) for n, v in docs.items()}, scientific_execution=False))
    return docs

def parse_response(raw):
    data = json.loads(raw)
    require(not data.get('promptFeedback', {}).get('blockReason'), 'Blocked review')
    candidates = data.get('candidates')
    require(isinstance(candidates, list) and len(candidates) == 1, 'Expected one response')
    candidate = candidates[0]
    require(candidate.get('finishReason') == 'STOP', 'Incomplete response')
    parts = candidate.get('content', {}).get('parts', [])
    answer = '\n'.join(p['text'] for p in parts if not p.get('thought', False) and isinstance(p.get('text'), str)).strip().encode()
    result = json.loads(answer)
    require(result.get('outcome') in ('CANDIDATE', 'NO_CANDIDATE', 'INSUFFICIENT_SOURCE'), 'Invalid audit outcome')
    require(result.get('native_bridge_status') in ('PROPOSED_DERIVATION', 'NOT_DERIVED'), 'Invalid native status')
    for key in ('candidate_tests', 'source_corrections', 'limitations'):
        require(isinstance(result.get(key), list), 'Missing audit list: ' + key)
    require(bool(result.get('strongest_positive_reconstruction')) and bool(result.get('next_native_obligation')), 'Missing substantive reconstruction')
    require(isinstance(result.get('next_native_obligation'), str), 'Invalid next obligation')
    if result['outcome'] == 'CANDIDATE':
        require(bool(result.get('new_derivation')), 'Candidate lacks derivation')
    else:
        require(isinstance(result.get('first_unsupported_arrow'), dict), 'Missing unsupported arrow')
        require(result['native_bridge_status'] == 'NOT_DERIVED', 'Unbacked bridge status')
    model = data.get('modelVersion', '')
    require(model == MODEL or model.startswith(MODEL + '-'), 'Wrong returned model')
    return answer, result, model

def review(root, out):
    docs = integrity(root, out)
    prompt = build_prompt(docs)
    (out / 'prompt.txt').write_bytes(prompt)
    sys.path.insert(0, str(root / '.github/scripts'))
    from uqcf_preparability_review import call_model
    response = call_model(out, os.environ['GEMINI_API_KEY'], prompt)
    answer, result, model = parse_response(response)
    (out / 'review.txt').write_bytes(answer)
    write(out, 'result.json', result)
    write(out, 'review_identity.json', dict(identity(root), status='AUDIT_RESPONSE_COMPLETE',
          model=model, outcome=result['outcome'], prompt_sha256=sha(prompt), response_sha256=sha(response),
          scientific_acceptance=False, native_bridge_status='NOT_DERIVED_PENDING_SEPARATE_ADJUDICATION'))
    print('Audit response complete:', result['outcome'], '; no automatic scientific acceptance.', flush=True)

def check_manifest(folder):
    records = json.loads((folder / 'artifact_manifest.json').read_bytes())
    actual = {str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file() and p.name != 'artifact_manifest.json'}
    require(set(records) == actual, 'Artifact file inventory mismatch')
    for name, row in records.items():
        require(not name.startswith('/') and '..' not in Path(name).parts, 'Unsafe artifact path')
        raw = (folder / name).read_bytes()
        require(row == dict(bytes=len(raw), sha256=sha(raw)), 'Artifact bytes mismatch')

def snapshot(root, out, docs):
    uq = 'ResearchHistory/UQCF-GEM/'
    prefixes = [uq + 'foundational-closure-verification', uq + 'demos/v16.15F-graded-obstruction-descent']
    paths = set(git(root, 'ls-tree', '-r', '--name-only', SCIENCE, *prefixes).decode().splitlines())
    parent = uq + 'demos/v15.56-response-selector-obstruction/'
    paths.update(p for p in git(root, 'ls-tree', '-r', '--name-only', SCIENCE, parent).decode().splitlines() if '/' not in p[len(parent):])
    paths.update(s['path'] for s in json.loads(docs['SOURCE_PACKET.json'])['sources'])
    paths.update(['.github/scripts/uqcf_preparability_review.py', '.github/scripts/uqcf_preparability_integrity.py'])
    stage = uq + 'research/physical-bridge/receiver_delivery_boundary/'
    for directory, suffix, evidence in [('', '', 'evidence/actions-41313483346/evidence/'), ('successor_t241/', '_s', 'successor_t241/evidence/actions-41335726832/')]:
        paths.update(stage + directory + n + suffix + '.py' for n in ('produce', 'verify', 'test_controls'))
        paths.update(stage + evidence + n for n in ('certificate.json', 'verification.json', 'controls.json', 'SHA256SUMS', 'publication.json', 'environment.txt'))
    with (out / 'source-snapshot.zip').open('wb') as f:
        subprocess.run(['git', 'archive', '--format=zip', SCIENCE, *sorted(paths)], cwd=root, stdout=f, check=True)
    write(out, 'source-snapshot-files.json', {p: git(root, 'rev-parse', SCIENCE + ':' + p).decode().strip() for p in sorted(paths)})
    control_paths = [str(BASE), '.github/scripts/uqcf_native_source_audit.py', '.github/workflows/uqcf-native-source-audit.yml']
    with (out / 'controller-snapshot.zip').open('wb') as f:
        subprocess.run(['git', 'archive', '--format=zip', 'HEAD', *control_paths], cwd=CONTROLLER, stdout=f, check=True)

def stack(root, out, previous=None, reviewed=None):
    docs = integrity(root, out)
    snapshot(root, out, docs)  # Snapshot committed inputs before any producer writes.
    import sympy, mpmath
    require(sys.version_info[:2] == (3, 11) and sympy.__version__ == '1.13.3' and mpmath.__version__ == '1.3.0', 'Dependency mismatch')
    commands, deterministic = [], []
    def call(name, argv, cwd=root, capture=False):
        log = out / (name if capture else name + '.log')
        with log.open('wb') as f:
            if capture:
                with (out / (name + '.stderr.log')).open('wb') as e:
                    result = subprocess.run(argv, cwd=cwd, stdout=f, stderr=e)
            else:
                result = subprocess.run(argv, cwd=cwd, stdout=f, stderr=subprocess.STDOUT)
        commands.append(dict(name=name, argv=argv, cwd=str(cwd.relative_to(root)), exit_code=result.returncode))
        write(out, 'commands.json', commands)
        print(name, 'exit', result.returncode, flush=True)
        require(result.returncode == 0, 'Failed command: ' + name)
        if capture:
            deterministic.append(name)
    uq = root / 'ResearchHistory/UQCF-GEM'
    fcv = uq / 'foundational-closure-verification'
    historical = uq / 'demos/v16.15F-graded-obstruction-descent'
    stage = uq / 'research/physical-bridge/receiver_delivery_boundary'
    call('dependencies', [sys.executable, '-m', 'pip', 'freeze'])
    call('fcv-publication-checksums', ['sha256sum', '-c', 'PUBLICATION_SHA256SUMS'], fcv)
    call('fcv-tests', [sys.executable, 'tests/test_fcv.py'], fcv)
    call('parent-tests', [sys.executable, '-m', 'unittest', '-v', 'test_pruning_consistency_audit'], uq / 'demos/v15.56-response-selector-obstruction')
    call('historical-tests', [sys.executable, '-m', 'unittest', '-v'], historical)
    call('historical-reproduction', [sys.executable, 'gate.py'], historical)
    shutil.copyfile(historical / 'result.json', fcv / 'evidence/REPRODUCED_1615F.json')
    call('fcv-producer', [sys.executable, 'produce_certificates.py'], fcv)
    call('fcv-independent-verifier', [sys.executable, 'verify_certificates.py'], fcv)
    for name in ('certificates.json.xz', 'PRODUCTION.json', 'VERIFICATION.json', 'REPRODUCED_1615F.json'):
        target = 'fcv-' + name
        shutil.copyfile(fcv / 'evidence' / name, out / target)
        deterministic.append(target)
    require(sha(lzma.decompress((out / 'fcv-certificates.json.xz').read_bytes())) == '21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6', 'FCV canonical universe changed')
    require(json.loads((out / 'fcv-VERIFICATION.json').read_bytes())['all_valid'] is True, 'FCV verification failed')
    for tag, directory, suffix, evidence in [('original', stage, '', stage / 'evidence/actions-41313483346/evidence'), ('successor', stage / 'successor_t241', '_s', stage / 'successor_t241/evidence/actions-41335726832')]:
        call(tag + '-publication-checksums', ['sha256sum', '-c', 'SHA256SUMS'], evidence)
        producer = directory / ('produce' + suffix + '.py')
        certificate = tag + '-certificate.json'
        call(certificate, [sys.executable, '-B', str(producer)], capture=True)
        call(tag + '-verification.json', [sys.executable, '-B', str(directory / ('verify' + suffix + '.py')), str(out / certificate), str(producer)], capture=True)
        call(tag + '-controls.json', [sys.executable, '-B', 'test_controls' + suffix + '.py', str(out / certificate), producer.name], directory, capture=True)
        for name in ('certificate.json', 'verification.json', 'controls.json'):
            require((out / (tag + '-' + name)).read_bytes() == (evidence / name).read_bytes(), 'Frozen boundary bytes changed')
    if previous:
        check_manifest(previous)
        prior = json.loads((previous / 'receipt.json').read_bytes())
        require(prior['identity'] == identity(root), 'Verification/publication identity mismatch')
        for name in deterministic + ['source-snapshot.zip', 'controller-snapshot.zip']:
            require((out / name).read_bytes() == (previous / name).read_bytes(), 'Fresh replay mismatch: ' + name)
    if reviewed:
        check_manifest(reviewed)
        require((reviewed / 'prompt.txt').read_bytes() == build_prompt(docs), 'Review prompt mismatch')
        request = json.loads((reviewed / 'request.json').read_bytes())
        require(request['contents'][0]['parts'][0]['text'].encode() == build_prompt(docs), 'Model request mismatch')
        require(request['generationConfig'] == dict(temperature=0, maxOutputTokens=32768, responseMimeType='application/json'), 'Model configuration mismatch')
        answer, result, model = parse_response((reviewed / 'response.json').read_bytes())
        require(answer == (reviewed / 'review.txt').read_bytes() and result == json.loads((reviewed / 'result.json').read_bytes()), 'Parsed review mismatch')
        row = json.loads((reviewed / 'review_identity.json').read_bytes())
        require(all(row[k] == v for k, v in identity(root).items()), 'Review identity mismatch')
        require(row['model'] == model and row['response_sha256'] == sha((reviewed / 'response.json').read_bytes()), 'Review receipt mismatch')
        require(row['prompt_sha256'] == sha(build_prompt(docs)) and row['outcome'] == result['outcome'], 'Review prompt/outcome receipt mismatch')
        require(row['status'] == 'AUDIT_RESPONSE_COMPLETE' and row['scientific_acceptance'] is False
                and row['native_bridge_status'] == 'NOT_DERIVED_PENDING_SEPARATE_ADJUDICATION', 'Review status receipt mismatch')
        metadata = json.loads((reviewed / 'model_metadata.json').read_bytes())
        require(metadata.get('name') == 'models/' + MODEL and 'generateContent' in metadata.get('supportedGenerationMethods', []), 'Model metadata mismatch')
        for name, raw in docs.items():
            require((reviewed / name).read_bytes() == raw, 'Review frozen document mismatch')
        require((reviewed / 'FREEZE.json').read_bytes() == (CONTROLLER / BASE / 'FREEZE.json').read_bytes(), 'Review freeze mismatch')
        write(out, 'review-readback.json', dict(status='PASS', outcome=result['outcome'], model=model,
              response_sha256=row['response_sha256'], scientific_acceptance=False))
    write(out, 'receipt.json', dict(status='PASS', identity=identity(root), fresh_replay=bool(previous),
          deterministic_files=deterministic, source_audit_only=True, native_bridge_status='NOT_DERIVED'))

def main():
    require(len(sys.argv) in (4, 6), 'Usage: script verify|review|replay SOURCE OUT [PREVIOUS REVIEWED]')
    mode, source, target = sys.argv[1:4]
    root, out = Path(source).resolve(), Path(target).resolve()
    out.mkdir(parents=True, exist_ok=True)
    try:
        if mode == 'verify':
            stack(root, out)
        elif mode == 'review':
            review(root, out)
        elif mode == 'replay':
            stack(root, out, Path(sys.argv[4]).resolve(), Path(sys.argv[5]).resolve())
        else:
            raise ValueError('Unknown mode')
    except Exception as exc:
        # Do not print request headers, keys, HTTP bodies or exception text.
        write(out, 'failure.json', dict(status='INCOMPLETE', error_type=type(exc).__name__,
              http_status=getattr(exc, 'code', None)))
        raise SystemExit('Audit incomplete; sanitized failure and existing evidence retained.')
    finally:
        write(out, 'artifact_manifest.json', {
            str(p.relative_to(out)): dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes()))
            for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'artifact_manifest.json'})

if __name__ == '__main__':
    main()
