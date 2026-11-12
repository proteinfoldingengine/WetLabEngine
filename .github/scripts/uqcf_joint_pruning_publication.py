"""Separate immutable source/excerpt and raw-review audit; no science execution."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request


SCIENCE = '53ec6fda214192502206b83f4f4f51b6c6f2f2d4'
PREFIX = 'ResearchHistory/UQCF-GEM/research/physical-bridge/joint_pruning_review/'
OUT = Path('joint_pruning_review')
TARGET = Path('joint_pruning_publication')
NAMES = ('RESULT.md', 'SOURCE_PACKET.json', 'FREEZE.json')
MODEL = 'gemini-3.1-pro-preview'


def fetch(sha, path):
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('An immutable commit SHA is required')
    url = ('https://raw.githubusercontent.com/proteinfoldingengine/WetLabEngine/'
           + sha + '/' + urllib.parse.quote(path, safe='/'))
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def audit_source_excerpt(source, full):
    """Independently reconstruct full-file identity and the exact byte interval."""
    path = source.get('path')
    if not isinstance(path, str) or not path or path.startswith('/') or '..' in Path(path).parts:
        raise ValueError('Invalid dependency path')
    length = len(full)
    full_sha = hashlib.sha256(full).hexdigest()
    git_blob = hashlib.sha1(('blob %d\0' % length).encode('ascii') + full).hexdigest()
    if type(source.get('full_bytes')) is not int or source['full_bytes'] != length:
        raise ValueError('Dependency full byte length mismatch')
    if source.get('full_sha256') != full_sha or source.get('git_blob') != git_blob:
        raise ValueError('Dependency full-source digest mismatch')
    start, end = source.get('byte_start'), source.get('byte_end')
    if type(start) is not int or type(end) is not int:
        raise ValueError('Dependency slice bounds must be integers')
    if start < 0 or end <= start or end > length:
        raise ValueError('Dependency slice is outside the source')
    content = source.get('content')
    if not isinstance(content, str):
        raise ValueError('Dependency excerpt is not UTF-8 text')
    actual_excerpt = full[start:end]
    if content.encode('utf-8') != actual_excerpt:
        raise ValueError('Dependency exact UTF-8 excerpt mismatch')
    return {
        'path': path, 'full_bytes': length, 'full_sha256': full_sha,
        'git_blob': git_blob, 'byte_start': start, 'byte_end': end,
        'excerpt_bytes': len(actual_excerpt),
        'excerpt_sha256': hashlib.sha256(actual_excerpt).hexdigest(),
    }


def audit():
    manifest = json.loads((OUT / 'artifact_manifest.json').read_bytes())
    required = {
        'integrity.json', 'prompt.txt', 'model_metadata.json', 'request.json',
        'response.json', 'review.txt', 'verdict.json', 'review_identity.json',
    }
    if not required.issubset(manifest):
        raise ValueError('Incomplete original review evidence')
    for name, expected in manifest.items():
        if Path(name).name != name:
            raise ValueError('Invalid artifact path')
        raw = (OUT / name).read_bytes()
        if len(raw) != expected['bytes'] or hashlib.sha256(raw).hexdigest() != expected['sha256']:
            raise ValueError('Artifact mismatch')

    integrity = json.loads((OUT / 'integrity.json').read_bytes())
    review = json.loads((OUT / 'review_identity.json').read_bytes())
    if integrity.get('status') != 'PASS' or integrity.get('scientific_execution') is not False:
        raise ValueError('Invalid integrity evidence')
    for field in ('scientific_sha', 'checkout_sha', 'workflow_sha', 'run_id', 'run_attempt'):
        if integrity[field] != review[field]:
            raise ValueError('Review/integrity identity mismatch')
    current = {
        'scientific_sha': SCIENCE,
        'checkout_sha': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'workflow_sha': os.environ.get('UQCF_WORKFLOW_SHA'),
        'run_id': os.environ.get('GITHUB_RUN_ID'),
        'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
    }
    if any(review[key] != value for key, value in current.items()):
        raise ValueError('Wrong reviewed workflow, checkout or run')

    if set(integrity['documents']) != set(NAMES):
        raise ValueError('Unexpected scientific document set')
    documents = {name: fetch(SCIENCE, PREFIX + name) for name in NAMES}
    records = {}
    for name, raw in documents.items():
        raw.decode('utf-8')
        records[name] = hashlib.sha256(raw).hexdigest()
        if records[name] != integrity['documents'][name]:
            raise ValueError('Remote scientific document mismatch')
    freeze = json.loads(documents['FREEZE.json'])
    if freeze.get('documents') != {name: records[name] for name in NAMES if name != 'FREEZE.json'}:
        raise ValueError('Immutable freeze mismatch')

    # Rebuild every prompt byte, including the header from this exact workflow
    # checkout. No substring-only or parsed-JSON equivalence is accepted.
    from uqcf_joint_pruning_review import HEADER

    expected_prompt = HEADER.encode('utf-8')
    for name in NAMES:
        raw = documents[name]
        expected_prompt += ('\nEXACT DOCUMENT ' + name + '\nUTF8-BYTES ' + str(len(raw)) + '\n').encode('utf-8')
        expected_prompt += raw + b'\nEND EXACT DOCUMENT\n'
    prompt = (OUT / 'prompt.txt').read_bytes()
    if prompt != expected_prompt or hashlib.sha256(prompt).hexdigest() != review['prompt_sha256']:
        raise ValueError('Exact prompt bytes mismatch')

    packet = json.loads(documents['SOURCE_PACKET.json'])
    if packet['source_commit'] != integrity.get('source_commit'):
        raise ValueError('Dependency commit mismatch')
    if not isinstance(packet.get('sources'), list) or not packet['sources']:
        raise ValueError('Empty or invalid source packet')
    fetched, sources, seen = {}, [], set()
    for source, locked in zip(packet['sources'], integrity['sources'], strict=True):
        path = source['path']
        source_sha = source['commit']
        cache_key = (source_sha, path)
        if cache_key not in fetched:
            fetched[cache_key] = fetch(source_sha, path)
        actual = audit_source_excerpt(source, fetched[cache_key])
        actual['commit'] = source_sha
        key = (source_sha, path, actual['byte_start'], actual['byte_end'])
        if key in seen or actual != locked:
            raise ValueError('Dependency identity, excerpt manifest or uniqueness mismatch')
        seen.add(key)
        sources.append(actual)

    metadata = json.loads((OUT / 'model_metadata.json').read_bytes())
    if metadata.get('name') != 'models/' + MODEL or 'generateContent' not in metadata.get('supportedGenerationMethods', []):
        raise ValueError('Requested model availability evidence mismatch')
    request_raw = (OUT / 'request.json').read_bytes()
    expected_request = {
        'contents': [{'role': 'user', 'parts': [{'text': prompt.decode('utf-8')}]}],
        'generationConfig': {
            'temperature': 0, 'maxOutputTokens': 32768,
            'responseMimeType': 'application/json',
        },
    }
    expected_request_raw = (json.dumps(expected_request, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8')
    if request_raw != expected_request_raw:
        raise ValueError('Exact model request bytes or generation configuration mismatch')
    raw_response = (OUT / 'response.json').read_bytes()
    if hashlib.sha256(raw_response).hexdigest() != review['response_sha256']:
        raise ValueError('Raw response digest mismatch')
    response = json.loads(raw_response)
    returned = response.get('modelVersion')
    if (returned != review['model_returned'] or not isinstance(returned, str)
            or not (returned == MODEL or returned.startswith(MODEL + '-'))):
        raise ValueError('Returned model mismatch')
    if response.get('promptFeedback', {}).get('blockReason'):
        raise ValueError('Review prompt was blocked')
    candidates = response.get('candidates')
    if not isinstance(candidates, list) or len(candidates) != 1 or candidates[0].get('finishReason') != 'STOP':
        raise ValueError('Incomplete review')
    answer = '\n'.join(
        part['text'] for part in candidates[0]['content']['parts']
        if not part.get('thought', False) and isinstance(part.get('text'), str)
    ).strip().encode('utf-8')
    if answer != (OUT / 'review.txt').read_bytes():
        raise ValueError('Raw answer bytes mismatch')
    verdict = json.loads(answer)
    if verdict != json.loads((OUT / 'verdict.json').read_bytes()):
        raise ValueError('Stored verdict mismatch')
    if verdict.get('verdict') != 'ACCEPTED' or any(verdict.get(key) != [] for key in ('findings', 'missing_assumptions', 'counterexamples')):
        raise ValueError('Non-acceptance or unresolved substantive findings')
    if verdict.get('native_bridge_status') != 'NOT_DERIVED':
        raise ValueError('Native scope mismatch')

    receipt = dict(
        current, status='PASS', documents=records, source_commit=packet['source_commit'],
        source_count=len(sources), sources=sources, model=returned,
        prompt_sha256=hashlib.sha256(prompt).hexdigest(),
        response_sha256=hashlib.sha256(raw_response).hexdigest(),
        native_bridge='NOT_DERIVED', scientific_execution=False,
    )
    (TARGET / 'publication.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('Separate exact full-source, byte-excerpt, prompt and raw-review publication audit PASS.')


def main():
    TARGET.mkdir(exist_ok=True)
    try:
        audit()
    except Exception as exc:
        if isinstance(exc, urllib.error.HTTPError):
            (TARGET / 'http-error.bin').write_bytes(exc.read())
        failure = {'status': 'PUBLICATION_AUDIT_FAILED', 'error_type': type(exc).__name__, 'http_status': getattr(exc, 'code', None)}
        (TARGET / 'failure.json').write_text(json.dumps(failure, indent=2) + '\n', encoding='utf-8')
        raise SystemExit('Publication audit failed; sanitized failure and original review evidence retained.')
    finally:
        manifest = {
            path.name: {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in TARGET.iterdir() if path.is_file() and path.name != 'artifact_manifest.json'
        }
        (TARGET / 'artifact_manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
