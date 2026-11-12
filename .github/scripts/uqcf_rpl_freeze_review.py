#!/usr/bin/env python3
"""Integrity + Gemini review for recoverable_pruning_ledger freeze. No science modules beyond freeze docs."""
import hashlib, json, os, sys, urllib.error, urllib.request
from pathlib import Path

MODEL = 'gemini-3.1-pro-preview'
REL = 'ResearchHistory/UQCF-GEM/research/physical-bridge/constructions/recoverable_pruning_ledger'
DOCS = ('FROZEN_ARGUMENT.md', 'FREEZE.md', 'PREREGISTRATION.md', 'ADVERSE_REVIEW_RESPONSE.md', 'REVIEW_INSTRUCTIONS.txt')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')


def seal(out):
    write(out / 'file_manifest.json', {
        str(p.relative_to(out)): {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
        for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'file_manifest.json'
    })


def root():
    # workflow checks out to research_snapshot or repo root
    for cand in (Path('research_snapshot'), Path('.')):
        if (cand / REL / 'FROZEN_ARGUMENT.md').exists():
            return cand
    raise SystemExit('freeze packet not found')


def integrity(out):
    R = root()
    base = R / REL
    manifest = json.loads((base / 'input_manifest.json').read_text())
    checked = {}
    for name in DOCS + ('STATUS.md', 'code/producer.py', 'code/checker.py',
                        'evidence/producer_summary.json', 'evidence/checker_report.json'):
        path = REL + '/' + name
        data = (R / path).read_bytes()
        expected = manifest.get(path)
        if not expected:
            raise ValueError('missing manifest entry ' + path)
        got = {'bytes': len(data), 'sha256': sha(data),
               'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}
        if got != expected:
            raise ValueError('digest mismatch ' + path)
        checked[path] = got
    # checker must have PASS
    report = json.loads((base / 'evidence/checker_report.json').read_text())
    if report.get('status') != 'PASS':
        raise ValueError('checker not PASS')
    summary = json.loads((base / 'evidence/producer_summary.json').read_text())
    if not summary.get('producer_pass'):
        raise ValueError('producer_pass false')
    ident = {
        'scientific_sha': os.environ.get('GITHUB_SHA'),
        'workflow_sha': os.environ.get('UQCF_WORKFLOW_SHA'),
        'run_id': os.environ.get('GITHUB_RUN_ID'),
        'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
        'model_requested': MODEL,
    }
    write(out / 'provenance.json', ident)
    write(out / 'integrity.json', {'verified': True, 'checked': checked, 'checker_status': 'PASS',
                                   'stream_sha256': summary['tree_stats']['stream_sha256']})
    seal(out)
    print('integrity OK', len(checked), 'documents')


def review(out):
    R = root()
    base = R / REL
    integ = Path('rpl_integrity')
    if not (integ / 'integrity.json').exists():
        raise ValueError('missing integrity artifact')
    instr = (base / 'REVIEW_INSTRUCTIONS.txt').read_text()
    prompt = instr
    for n in DOCS:
        if n == 'REVIEW_INSTRUCTIONS.txt':
            continue
        raw = (base / n).read_bytes()
        prompt += f'\n\nEXACT DOCUMENT {n}\nUTF8-BYTES {len(raw)}\n'
        prompt += raw.decode('utf-8') + '\nEND EXACT DOCUMENT\n'
    # Attach bounded reconstruction certificate (producer/checker summary only)
    prompt += '\n\nBOUNDED RECONSTRUCTION CERTIFICATE\n'
    prompt += (base / 'evidence/checker_report.json').read_text()
    prompt += (base / 'evidence/producer_summary.json').read_text()
    (out / 'prompt.txt').write_text(prompt)
    key = os.environ.get('GEMINI_API_KEY')
    if not key:
        raise ValueError('missing GEMINI_API_KEY')
    endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/' + MODEL
    with urllib.request.urlopen(urllib.request.Request(endpoint, headers={'x-goog-api-key': key}), timeout=60) as resp:
        availability = resp.read()
    (out / 'model_availability.json').write_bytes(availability)
    avail = json.loads(availability)
    if avail.get('name') != 'models/' + MODEL or 'generateContent' not in avail.get('supportedGenerationMethods', []):
        raise ValueError('model unavailable')
    payload = {'contents': [{'parts': [{'text': prompt}]}],
               'generationConfig': {'temperature': 0, 'maxOutputTokens': 32768, 'responseMimeType': 'application/json'}}
    req = urllib.request.Request(endpoint + ':generateContent', data=json.dumps(payload).encode(),
                                 headers={'Content-Type': 'application/json', 'x-goog-api-key': key}, method='POST')
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = resp.read()
    (out / 'response.json').write_bytes(data)
    result = json.loads(data)
    cands = result.get('candidates')
    if not isinstance(cands, list) or len(cands) != 1 or cands[0].get('finishReason') != 'STOP':
        raise ValueError('incomplete response')
    texts = []
    for part in cands[0].get('content', {}).get('parts', []):
        if part.get('thought') is True:
            continue
        if isinstance(part.get('text'), str):
            texts.append(part['text'])
    raw = '\n'.join(texts).strip()
    if not raw:
        raise ValueError('empty response')
    (out / 'review.txt').write_text(raw)
    verdict = json.loads(raw)
    if verdict.get('verdict') not in ('ACCEPTED', 'REVISE', 'FAIL'):
        raise ValueError('invalid verdict')
    for k in ('findings', 'missing_assumptions', 'counterexamples', 'limitations'):
        if not isinstance(verdict.get(k), list):
            raise ValueError('invalid array ' + k)
    write(out / 'verdict.json', verdict)
    write(out / 'review_manifest.json', {
        'scientific_sha': os.environ.get('GITHUB_SHA'),
        'workflow_sha': os.environ.get('UQCF_WORKFLOW_SHA'),
        'run_id': os.environ.get('GITHUB_RUN_ID'),
        'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
        'model_requested': MODEL,
        'model_returned': result.get('modelVersion'),
        'prompt_sha256': sha(prompt.encode()),
        'raw_api_response_sha256': sha(data),
        'review_sha256': sha(raw.encode()),
        'verdict': verdict.get('verdict'),
        'native_bridge_status': verdict.get('native_bridge_status'),
    })
    seal(out)
    print('GEMINI_RAW_REVIEW_BEGIN\n' + raw + '\nGEMINI_RAW_REVIEW_END')
    # Do not fail the job on REVISE/FAIL — record verdict for author reconciliation.
    print('recorded verdict', verdict.get('verdict'))


def main():
    phase = sys.argv[1]
    out = Path('rpl_' + phase)
    out.mkdir(exist_ok=True)
    try:
        if phase == 'integrity':
            integrity(out)
        elif phase == 'review':
            review(out)
        else:
            raise ValueError('unknown phase')
    except Exception as exc:
        write(out / 'infrastructure_failure.json', {
            'status': 'INFRASTRUCTURE_FAILURE_NOT_MATHEMATICAL_VERDICT',
            'error_type': type(exc).__name__,
            'error_class_message': str(exc) if isinstance(exc, ValueError) else None,
            'http_status': getattr(exc, 'code', None) if isinstance(exc, urllib.error.HTTPError) else None,
        })
        seal(out)
        raise SystemExit('Review infrastructure failed; sanitized evidence retained.')


if __name__ == '__main__':
    main()
