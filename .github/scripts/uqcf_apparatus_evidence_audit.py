"""Evidence-only audit of a held review. Never changes the original acceptance verdict."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request


SCIENCE = '014f7afdfe9c060fc52a0901935eb5ade620e3e2'
PREFIX = 'ResearchHistory/UQCF-GEM/research/physical-bridge/source_generator_composition/apparatus_review/'
OUT = Path('apparatus_record_review')
TARGET = Path('apparatus_evidence_audit')
ARCHIVE = '3dc1f6b7bb79f167865ae0e2f6533bd9b188de5d'
REVIEW_HEAD = '0edc3b4ed82b2e866550426164a4f2cc335d6d50'
RESPONSE_HASH = '29d907ba7e466815a235e700724c82619db421fa4c2706756fca63b71e9a8d13'
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


def validate_constructive_response(verdict):
    entries = verdict.get('constructive_analysis')
    if type(entries) is not list or len(entries) == 0:
        raise ValueError('Missing constructive response')
    for item in entries:
        if isinstance(item, str):
            if not item.strip():
                raise ValueError('Blank constructive response entry')
        elif not isinstance(item, dict) or len(item) == 0:
            raise ValueError('Invalid constructive response entry')
    next_step = verdict.get('next_native_obligation')
    if type(next_step) is not str or len(next_step.strip()) == 0:
        raise ValueError('Missing next native obligation')


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
        'checkout_sha': REVIEW_HEAD,
        'workflow_sha': REVIEW_HEAD,
        'run_id': '40880862457',
        'run_attempt': '1',
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
    header_path = '.github/scripts/uqcf_apparatus_record_review.py'
    if fetch(REVIEW_HEAD, header_path) != Path(header_path).read_bytes():
        raise ValueError('Original review header implementation changed')
    from uqcf_apparatus_record_review import HEADER

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
        if path not in fetched:
            fetched[path] = fetch(packet['source_commit'], path)
        actual = audit_source_excerpt(source, fetched[path])
        key = (path, actual['byte_start'], actual['byte_end'])
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
    validate_constructive_response(verdict)
    # Preserve the original FAIL. This checker certifies bytes, not acceptance.
    if hashlib.sha256(raw_response).hexdigest() != RESPONSE_HASH:
        raise ValueError('Wrong held response')
    if (verdict.get('verdict') != 'ACCEPTED'
            or not isinstance(verdict.get('findings'), list) or len(verdict['findings']) != 7
            or any(verdict.get(key) != [] for key in ('missing_assumptions', 'counterexamples'))):
        raise ValueError('Original held verdict shape changed')
    failure = json.loads((OUT / 'failure-review.json').read_bytes())
    if failure != {'error_type': 'ValueError', 'http_status': None,
                   'status': 'REVIEW_NOT_ACCEPTED_OR_INFRASTRUCTURE_FAILURE'}:
        raise ValueError('Original failure evidence changed')

    # Fresh remote readback of ALL published evidence, including original ZIPs.
    archive_manifest = json.loads(fetch(ARCHIVE, PREFIX + 'EVIDENCE_MANIFEST.json'))
    if (archive_manifest['raw_verdict'] != 'ACCEPTED'
            or archive_manifest['original_acceptance_job'] != 'failure'
            or archive_manifest['original_publication_job'] != 'skipped'):
        raise ValueError('Original gate outcome was relabeled')
    archived = {}
    for entry in archive_manifest['files']:
        name = entry['path']
        if name.startswith('/') or '..' in Path(name).parts:
            raise ValueError('Unsafe evidence path')
        blob = fetch(ARCHIVE, PREFIX + 'evidence/' + name)
        if (len(blob) != entry['bytes'] or hashlib.sha256(blob).hexdigest() != entry['sha256']
                or hashlib.sha1(b'blob ' + str(len(blob)).encode('ascii') + b'\0' + blob).hexdigest() != entry['git_blob']):
            raise ValueError('Published evidence identity mismatch')
        archived[name] = blob
    for path in OUT.iterdir():
        if path.is_file() and archived.get('review/' + path.name) != path.read_bytes():
            raise ValueError('Original downloaded artifact differs from published evidence')
    import io, zipfile
    zip_locks = {
        'apparatus-record-integrity-1.zip': (1541, '093afb423a553a50c6de4000988410fd12bb58084847e311ef2d3a17ea201669', 'integrity'),
        'apparatus-record-review-1.zip': (63879, 'eccda4cbe82cfdb3416b9df4c01e1a74803fb9b6ba7d7ec5ce07afd47ffd2a25', 'review'),
    }
    for name, (length, expected_hash, directory) in zip_locks.items():
        raw = archived[name]
        if len(raw) != length or hashlib.sha256(raw).hexdigest() != expected_hash:
            raise ValueError('Original GitHub artifact digest mismatch')
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            names = z.namelist()
            if len(names) != len(set(names)):
                raise ValueError('Duplicate ZIP member')
            for member in names:
                if Path(member).name != member or archived.get(directory + '/' + member) != z.read(member):
                    raise ValueError('Original ZIP member mismatch')

    if verdict.get('native_bridge_status') != 'NOT_DERIVED':
        raise ValueError('Native scope mismatch')

    receipt = dict(
        current, status='EVIDENCE_MATCHED_REVIEW_GATE_HELD',
        raw_verdict='ACCEPTED', original_acceptance_job='failure', original_publication_job='skipped',
        archive_commit=ARCHIVE, archived_files=len(archived),
        audit_checkout_sha=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        audit_workflow_sha=os.environ.get('UQCF_WORKFLOW_SHA'),
        audit_run_id=os.environ.get('GITHUB_RUN_ID'),
        documents=records, source_commit=packet['source_commit'],
        source_count=len(sources), sources=sources, model=returned,
        prompt_sha256=hashlib.sha256(prompt).hexdigest(),
        response_sha256=hashlib.sha256(raw_response).hexdigest(),
        native_bridge='NOT_DERIVED', scientific_execution=False,
    )
    (TARGET / 'publication.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('Evidence identities MATCHED. Original review acceptance remains HELD; no scientific acceptance inferred.')


def main():
    TARGET.mkdir(exist_ok=True)
    try:
        audit()
    except Exception as exc:
        if isinstance(exc, urllib.error.HTTPError):
            (TARGET / 'http-error.bin').write_bytes(exc.read())
        failure = {'status': 'EVIDENCE_AUDIT_FAILED', 'error_type': type(exc).__name__, 'http_status': getattr(exc, 'code', None)}
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

