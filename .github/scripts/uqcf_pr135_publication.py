"""Separate immutable readback audit; imports no integrity or reviewer helpers."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
BASE = 'ResearchHistory/UQCF-GEM/research/physical-bridge/groupoid_identity_ownership'
REL = BASE + '/independent_review_2026_11_12'
BASELINE = '2a72e2331e910e17c82abb537a1162280102ef78'
LOCK_HASH = 'f488edb90ded603ae345ed0d5c636a9094837e383ac816e38f8e9248b10adc1a'
REPOSITORY = 'proteinfoldingengine/WetLabEngine'
BRANCH = 'gpt/groupoid-identity-ownership'
WORKFLOW = '.github/workflows/uqcf-pr135-independent-review.yml'
MODEL = 'gemini-3.1-pro-preview'

def insist(ok, message):
    if not ok:
        raise ValueError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def identify(raw):
    return {'bytes': len(raw), 'sha256': digest(raw), 'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\x00' + raw).hexdigest()}

def decode(raw):
    def unique(pairs):
        out = {}
        for k, v in pairs:
            insist(k not in out, 'Duplicate JSON field')
            out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=unique)

def pathcheck(path):
    insist(isinstance(path, str) and path and '\\' not in path, 'Invalid path')
    p = PurePosixPath(path)
    insist(not p.is_absolute() and str(p) == path and all(x not in ('.', '..') for x in path.split('/')), 'Unsafe path')
    return path

def index(rows, key):
    insist(isinstance(rows, list), 'Expected list')
    out = {}
    for row in rows:
        name = pathcheck(row[key]); insist(name not in out, 'Duplicate identity'); out[name] = row
    return out

def api(path):
    request = urllib.request.Request('https://api.github.com/repos/' + REPOSITORY + path,
        headers={'Authorization': 'Bearer ' + os.environ['GH_READ_TOKEN'], 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return decode(response.read())

def tree_at(ref, path, get=api):
    insist(re.fullmatch('[a-f0-9]{40}', ref) is not None, 'Mutable readback ref')
    sha = ref
    for part in pathcheck(path).split('/'):
        tree = get('/git/trees/' + sha)
        insist(tree.get('truncated') is False, 'Truncated tree')
        entries = [x for x in tree['tree'] if x['path'] == part and x['type'] == 'tree']
        insist(len(entries) == 1, 'Missing source tree')
        sha = entries[0]['sha']
    tree = get('/git/trees/' + sha + '?recursive=1')
    insist(tree.get('truncated') is False, 'Truncated source tree')
    rows = [dict(x, path=path + '/' + x['path']) for x in tree['tree'] if x['type'] == 'blob']
    return index(rows, 'path')

def blob(sha, get=api):
    b = get('/git/blobs/' + sha)
    insist(b.get('sha') == sha and b.get('encoding') == 'base64', 'Invalid remote blob')
    raw = base64.b64decode(''.join(b['content'].split()), validate=True)
    insist(identify(raw)['git_blob'] == sha, 'Remote blob digest mismatch')
    return raw

def file_at(path, ref, get=api):
    insist(re.fullmatch('[a-f0-9]{40}', ref) is not None, 'Mutable file ref')
    item = get('/contents/' + urllib.parse.quote(pathcheck(path), safe='/') + '?ref=' + ref)
    insist(item.get('type') == 'file', 'Missing remote file')
    return blob(item['sha'], get)

def reconstruct_sources(lock, before, current, get=api):
    insist(set(lock) == {'baseline', 'files', 'archives'} and lock['baseline'] == BASELINE, 'Invalid baseline or lock')
    expected = index(lock['files'], 'path')
    insist(len(expected) == 115 and set(before) == set(expected), 'Lock does not cover full original packet')
    inherited = {p: r for p, r in current.items() if not p.startswith(REL + '/')}
    insist(set(inherited) == set(before), 'Inherited source set changed')
    sources = {}
    for path, row in expected.items():
        insist(set(row) == {'path', 'bytes', 'sha256', 'git_blob'} and type(row['bytes']) is int, 'Invalid source identity')
        insist(before[path]['sha'] == current[path]['sha'] == row['git_blob'], 'Source differs between baseline and reviewed head')
        raw = blob(row['git_blob'], get)
        insist(identify(raw) == {k: row[k] for k in ('bytes', 'sha256', 'git_blob')}, 'Locked source differs')
        sources[path] = raw
    archives = index(lock['archives'], 'path')
    insist(set(archives) == {p for p in expected if p.endswith('.zip')} and len(archives) == 11, 'Archive set incomplete')
    copies = set()
    for path, archive in archives.items():
        insist(set(archive) == {'path', 'members'}, 'Invalid archive schema')
        members = index(archive['members'], 'name')
        with zipfile.ZipFile(io.BytesIO(sources[path])) as z:
            names = z.namelist()
            insist(len(names) == len(set(names)) and set(names) == set(members) and z.testzip() is None, 'Archive inventory/CRC mismatch')
            for name, member in members.items():
                insist(set(member) == {'name', 'copy_path', 'bytes', 'sha256', 'git_blob'}, 'Invalid member schema')
                copy = pathcheck(member['copy_path'])
                insist(copy in sources and copy not in copies, 'Missing or duplicated extracted copy')
                copies.add(copy)
                raw = z.read(name)
                insist(raw == sources[copy] and identify(raw) == {k: member[k] for k in ('bytes', 'sha256', 'git_blob')}, 'Original/extracted bytes differ')
    insist(len(copies) == 74, 'Incomplete original-member coverage')
    return sources

def prompt_from(current, lock):
    paths = [REL + '/FREEZE.md', REL + '/source_lock.json'] + sorted(r['path'] for r in lock['files'] if not r['path'].endswith('.zip'))
    pieces = [current[REL + '/PROMPT.md']]
    for path in paths:
        raw = current[path]; raw.decode('utf-8')
        pieces.extend([('\nEXACT DOCUMENT ' + path + '\nUTF8-BYTES ' + str(len(raw)) + '\n').encode(), raw, b'\nEND EXACT DOCUMENT\n'])
    return b''.join(pieces)

def verify_review(review, integrity, context, inputs, lock, prompt):
    manifest = decode(review['manifest.json'])
    insist(all(manifest.get(k) == v for k, v in context.items()), 'Review run identity mismatch')
    insist(manifest.get('status') == 'ACCEPTED' and manifest.get('model_requested') == MODEL and manifest.get('generation_calls_maximum') == 1, 'Review incomplete or wrong requested model')
    insist(manifest.get('artifact_hashes') == {k: digest(v) for k, v in review.items() if k != 'manifest.json'}, 'Review artifact digest mismatch')
    insist(review['prompt.txt'] == prompt and decode(review['input_manifest.json']) == inputs, 'Exact reviewer input differs')
    insist(decode(review['request.json']) == {'contents': [{'role': 'user', 'parts': [{'text': prompt.decode('utf-8')}]}], 'generationConfig': {'temperature': 0, 'maxOutputTokens': 32768, 'responseMimeType': 'application/json'}}, 'Generation request differs')
    metadata = decode(review['model_metadata.json'])
    insist(metadata.get('name') == 'models/' + MODEL and 'generateContent' in metadata.get('supportedGenerationMethods', []), 'Availability not verified')
    response = decode(review['response.json'])
    insist(not response.get('promptFeedback', {}).get('blockReason'), 'Blocked prompt')
    candidates = response.get('candidates')
    insist(isinstance(candidates, list) and len(candidates) == 1 and candidates[0].get('finishReason') == 'STOP', 'Invalid or truncated candidate')
    parts = candidates[0].get('content', {}).get('parts', [])
    insist(isinstance(parts, list), 'Invalid response parts')
    answer = '\n'.join(p['text'] for p in parts if not p.get('thought', False) and isinstance(p.get('text'), str)).strip().encode()
    verdict = decode(answer)
    insist(answer == review['review.txt'] and verdict == decode(review['verdict.json']), 'Stored verdict differs from raw response')
    insist(isinstance(verdict, dict) and verdict.get('verdict') == 'ACCEPTED' and all(verdict.get(k) == [] for k in ('findings', 'missing_assumptions', 'counterexamples')), 'Substantive review not accepted')
    insist(all(isinstance(verdict.get(k), list) for k in ('limitations', 'constructive_analysis')) and isinstance(verdict.get('next_native_obligation'), str) and verdict.get('native_bridge_status') in ('NOT_DERIVED', 'DERIVED_FROM_SOURCES'), 'Invalid review scope')
    returned = response.get('modelVersion')
    insist(isinstance(returned, str) and (returned == MODEL or returned.startswith(MODEL + '-')) and returned == manifest.get('model_returned'), 'Unexpected returned model')
    insist(manifest.get('integrity_artifacts') == {k: digest(v) for k, v in integrity.items()}, 'Upstream integrity artifacts differ')
    evidence = decode(integrity['integrity.json'])
    insist(evidence.get('status') == 'PASS' and evidence.get('scientific_execution') is False and evidence.get('source_lock_sha256') == LOCK_HASH and all(evidence.get(k) == v for k, v in context.items()), 'Integrity context invalid')
    for label, expected in (('input_manifest', inputs), ('source_manifest', lock)):
        insist(decode(integrity[label + '.json']) == expected and digest(integrity[label + '.json']) == evidence.get(label + '_sha256'), 'Independent manifest reconstruction differs')
    insist(evidence.get('prompt_sha256') == digest(prompt), 'Integrity prompt hash differs')
    return verdict, returned

def save(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')

def main():
    out = Path('pr135_publication'); out.mkdir(exist_ok=True)
    try:
        head, workflow = os.environ['GITHUB_SHA'], os.environ['UQCF_WORKFLOW_SHA']
        insist(re.fullmatch('[a-f0-9]{40}', head) is not None and head == workflow, 'Source/workflow mismatch')
        insist(subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip() == head, 'Wrong checkout')
        context = {'source_sha': head, 'workflow_sha': workflow, 'run_id': os.environ['GITHUB_RUN_ID'], 'run_attempt': os.environ['GITHUB_RUN_ATTEMPT'], 'repository': REPOSITORY}
        insist(os.environ.get('GITHUB_REPOSITORY') == REPOSITORY and os.environ.get('GITHUB_REF_NAME') == BRANCH, 'Wrong repository/branch')
        run = api('/actions/runs/' + context['run_id'])
        insist(str(run.get('id')) == context['run_id'] and str(run.get('run_attempt')) == context['run_attempt'] and run.get('head_sha') == head and run.get('head_branch') == BRANCH and run.get('path') == WORKFLOW and run.get('event') == 'push', 'Remote workflow identity mismatch')
        jobs = api('/actions/runs/' + context['run_id'] + '/attempts/' + context['run_attempt'] + '/jobs?per_page=100')['jobs']
        prerequisites = []
        for name in ('integrity', 'argument-review'):
            chosen = [j for j in jobs if j['name'] == name]
            insist(len(chosen) == 1 and chosen[0]['status'] == 'completed' and chosen[0]['conclusion'] == 'success' and chosen[0]['head_sha'] == head, 'Prerequisite job did not pass exact head')
            prerequisites.append({k: chosen[0][k] for k in ('id', 'name', 'head_sha', 'status', 'conclusion')})
        before, current = tree_at(BASELINE, BASE), tree_at(head, BASE)
        lock_raw = blob(current[REL + '/source_lock.json']['sha'])
        insist(digest(lock_raw) == LOCK_HASH, 'Frozen lock differs')
        lock = decode(lock_raw)
        readback = reconstruct_sources(lock, before, current)
        extras = [REL + '/' + n for n in ('FREEZE.md', 'PROMPT.md', 'source_lock.json')] + ['.github/scripts/uqcf_pr135_' + x + '.py' for x in ('integrity', 'review', 'publication', 'tests')] + [WORKFLOW]
        for path in extras:
            readback[path] = file_at(path, head)
        insist(all((ROOT / path).read_bytes() == raw for path, raw in readback.items()), 'Local checkout differs from immutable source readback')
        inputs = {p: identify(raw) for p, raw in sorted(readback.items())}
        integrity = {p.name: p.read_bytes() for p in Path('pr135_integrity').iterdir() if p.is_file()}
        review = {p.name: p.read_bytes() for p in Path('pr135_review').iterdir() if p.is_file()}
        verdict, returned = verify_review(review, integrity, context, inputs, lock, prompt_from(readback, lock))
        save(out / 'readback_manifest.json', inputs)
        save(out / 'publication.json', {'status': 'PASS', **context, 'baseline': BASELINE, 'model_requested': MODEL, 'model_returned': returned,
            'verdict': verdict['verdict'], 'native_bridge_status': verdict['native_bridge_status'], 'scientific_execution': False,
            'source_lock_sha256': LOCK_HASH, 'original_files_verified': 115, 'original_archives_verified': 11, 'all_archive_members_verified': 74,
            'full_original_text_files_reviewed': 104, 'exact_input_files_read_back': len(inputs), 'prerequisite_jobs': prerequisites,
            'readback_manifest_sha256': digest((out / 'readback_manifest.json').read_bytes()),
            'review_artifacts': {k: digest(v) for k, v in review.items()}, 'integrity_artifacts': {k: digest(v) for k, v in integrity.items()},
            'scope': 'Independent analytical source-audit acceptance only; no native-delivery promotion, historical scientific replay, stage closure or merge.'})
        print('Independent publication and immutable GitHub full-packet readback PASS.')
    except Exception as exc:
        save(out / 'failure.json', {'status': 'FAIL', 'error_type': type(exc).__name__, 'http_status': getattr(exc, 'code', None)})
        raise SystemExit('Publication audit failed; sanitized evidence retained.')

if __name__ == '__main__':
    main()
