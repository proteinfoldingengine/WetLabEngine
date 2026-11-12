"""Exact source-packet integrity only. Never execute historical scientific code."""
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile

BASE = 'ResearchHistory/UQCF-GEM/research/physical-bridge/groupoid_identity_ownership'
REL = BASE + '/independent_review_2026_11_12'
BASELINE = '2a72e2331e910e17c82abb537a1162280102ef78'
LOCK_SHA256 = 'f488edb90ded603ae345ed0d5c636a9094837e383ac816e38f8e9248b10adc1a'
REPOSITORY = 'proteinfoldingengine/WetLabEngine'
BRANCH = 'gpt/groupoid-identity-ownership'
WORKFLOW = '.github/workflows/uqcf-pr135-independent-review.yml'
SCRIPTS = tuple('.github/scripts/uqcf_pr135_' + x + '.py' for x in ('integrity', 'review', 'publication', 'tests'))
ROOT = Path(__file__).resolve().parents[2]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def identity(raw):
    return {'bytes': len(raw), 'sha256': sha256(raw),
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}

def parse_json(raw):
    def unique(pairs):
        out = {}
        for k, v in pairs:
            require(k not in out, 'Duplicate JSON key')
            out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=unique)

def safe(path):
    require(isinstance(path, str) and path and '\\' not in path, 'Invalid path')
    p = PurePosixPath(path)
    require(not p.is_absolute() and str(p) == path and all(x not in ('.', '..') for x in path.split('/')), 'Unsafe path')
    return path

def indexed(rows, key):
    require(isinstance(rows, list), 'Expected list')
    out = {}
    for r in rows:
        name = safe(r[key])
        require(name not in out, 'Duplicate identity')
        out[name] = r
    return out

def verify_record(record, raw):
    actual = identity(raw)
    require(type(record.get('bytes')) is int, 'Invalid byte length')
    require(all(record.get(k) == v for k, v in actual.items()), 'Source byte identity mismatch')
    return actual

def validate_sources(root, lock):
    require(set(lock) == {'baseline', 'files', 'archives'} and lock['baseline'] == BASELINE, 'Wrong source-lock schema or baseline')
    files = indexed(lock['files'], 'path')
    require(len(files) == 115, 'Wrong original source count')
    actual = {p.relative_to(root).as_posix() for p in (root / BASE).rglob('*') if p.is_file() and not p.is_relative_to(root / REL)}
    require(actual == set(files), 'Missing, additional or substituted source file')
    raw = {}
    for path, record in sorted(files.items()):
        require(set(record) == {'path', 'bytes', 'sha256', 'git_blob'}, 'Unexpected source record')
        require(path.startswith(BASE + '/') and not path.startswith(REL + '/'), 'Source outside frozen packet')
        raw[path] = (root / path).read_bytes()
        verify_record(record, raw[path])
        if not path.endswith('.zip'):
            raw[path].decode('utf-8')
    archives = indexed(lock['archives'], 'path')
    require(set(archives) == {p for p in files if p.endswith('.zip')} and len(archives) == 11, 'Incomplete archive coverage')
    copied = set()
    for path, archive in sorted(archives.items()):
        require(set(archive) == {'path', 'members'}, 'Unexpected archive record')
        members = indexed(archive['members'], 'name')
        with zipfile.ZipFile(io.BytesIO(raw[path])) as z:
            infos = z.infolist()
            names = [i.filename for i in infos]
            require(len(names) == len(set(names)) and set(names) == set(members), 'Missing or duplicated ZIP member')
            require(z.testzip() is None, 'ZIP CRC failed')
            for info in infos:
                require(not info.is_dir(), 'Unexpected ZIP directory entry')
                member = members[safe(info.filename)]
                require(set(member) == {'name', 'copy_path', 'bytes', 'sha256', 'git_blob'}, 'Unexpected member record')
                copy = safe(member['copy_path'])
                require(copy in files and copy not in copied, 'Missing or duplicated extracted copy')
                copied.add(copy)
                data = z.read(info)
                verify_record(member, data)
                require(data == raw[copy], 'Extracted member differs from original ZIP')
    require(len(copied) == 74, 'Wrong full archive-member count')
    return raw

def load_sources(root):
    lock_raw = (root / REL / 'source_lock.json').read_bytes()
    require(sha256(lock_raw) == LOCK_SHA256, 'Frozen source lock changed')
    lock = parse_json(lock_raw)
    return lock, validate_sources(root, lock)

def document_paths(lock):
    return [REL + '/FREEZE.md', REL + '/source_lock.json'] + sorted(r['path'] for r in lock['files'] if not r['path'].endswith('.zip'))

def build_prompt(root, lock):
    pieces = [(root / REL / 'PROMPT.md').read_bytes()]
    for path in document_paths(lock):
        raw = (root / path).read_bytes()
        raw.decode('utf-8')
        pieces += [('\nEXACT DOCUMENT ' + path + '\nUTF8-BYTES ' + str(len(raw)) + '\n').encode(), raw, b'\nEND EXACT DOCUMENT\n']
    return b''.join(pieces)

def input_manifest(root, lock):
    paths = [r['path'] for r in lock['files']] + [REL + '/' + n for n in ('FREEZE.md', 'PROMPT.md', 'source_lock.json')] + list(SCRIPTS) + [WORKFLOW]
    require(len(paths) == len(set(paths)), 'Duplicate reviewer input')
    return {p: identity((root / safe(p)).read_bytes()) for p in sorted(paths)}

def run_identity(root):
    head = os.environ['GITHUB_SHA']
    workflow = os.environ['UQCF_WORKFLOW_SHA']
    require(re.fullmatch('[a-f0-9]{40}', head) is not None and head == workflow, 'Invalid source/workflow identity')
    require(subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip() == head, 'Wrong checkout')
    require(os.environ.get('GITHUB_REPOSITORY') == REPOSITORY and os.environ.get('GITHUB_REF_NAME') == BRANCH, 'Wrong repository or branch')
    run, attempt = os.environ['GITHUB_RUN_ID'], os.environ['GITHUB_RUN_ATTEMPT']
    require(run.isdigit() and attempt.isdigit() and int(attempt) > 0, 'Invalid run identity')
    return {'source_sha': head, 'workflow_sha': workflow, 'run_id': run, 'run_attempt': attempt, 'repository': REPOSITORY}

def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')

def main():
    out = Path('pr135_integrity'); out.mkdir(exist_ok=True)
    try:
        run = run_identity(ROOT)
        lock, _ = load_sources(ROOT)
        inputs = input_manifest(ROOT, lock)
        write_json(out / 'input_manifest.json', inputs)
        write_json(out / 'source_manifest.json', lock)
        write_json(out / 'integrity.json', {'status': 'PASS', **run, 'scientific_execution': False,
            'source_lock_sha256': LOCK_SHA256, 'input_manifest_sha256': sha256((out / 'input_manifest.json').read_bytes()),
            'source_manifest_sha256': sha256((out / 'source_manifest.json').read_bytes()), 'prompt_sha256': sha256(build_prompt(ROOT, lock)),
            'original_files': 115, 'original_archives': 11, 'all_archive_members': 74, 'full_text_files': 104})
        print('Full packet byte integrity PASS: 115 files, 11 ZIPs, all 74 members; no scientific execution.')
    except Exception as exc:
        write_json(out / 'failure.json', {'status': 'FAIL', 'error_type': type(exc).__name__})
        raise SystemExit('Integrity failed; sanitized evidence retained.')

if __name__ == '__main__':
    main()
