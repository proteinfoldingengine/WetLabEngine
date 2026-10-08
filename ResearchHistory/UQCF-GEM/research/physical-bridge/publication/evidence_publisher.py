#!/usr/bin/env python3
"""Evidence-only Git Database publication; unchanged token permissions.

No force updates, workflow writes, scientific edits, or invented acceptance.
Preserves pinned failed-run archives and verifies every published blob byte.
"""
from __future__ import annotations
import base64
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

PREFIX = 'ResearchHistory/UQCF-GEM/research/physical-bridge/evidence/'
LIMIT = 2 * 1024 * 1024
ARCHIVE_BRANCH = 'research/c3-artifact-recovery-20261008'
ARCHIVE_ROOT = PREFIX + 'c3-artifact-recovery-20261008/'
COMMON = {'context.json', 'contracts.log', 'jobs_snapshot.json',
          'pipeline_control.json', 'pipeline_control.log'}
PINS = [
    {'run': 37832509819, 'attempt': 1, 'artifact': 11574560540, 'size': 11406,
     'source': '6a4ba75ca3a1ce332e6481e383bfecf6046f31b9',
     'sha256': 'c2b4645fa1c066b3c606c80f55a112e35d67cef5177edbff8644e8b978344312',
     'members': sorted(COMMON)},
    {'run': 37832751396, 'attempt': 1, 'artifact': 11574595760, 'size': 18798,
     'source': 'ad42d751f69c6fba7af585e6ba15b00941bc201f',
     'sha256': 'd04fda1889c362d3ed590cf953bf3e42bf9e0625a0bd4f8788589201ad244246',
     'members': sorted(COMMON | {'controls.json', 'controls.log', 'primary.json',
       'primary.log', 'reproduction.json', 'reproduction.log', 'reproduction_comparison.json'})},
]


class PublicationError(ValueError):
    pass


class APIError(PublicationError):
    def __init__(self, status, message):
        self.status = status
        super().__init__(f'HTTP {status}: {message}')


def require(ok, message):
    if not ok:
        raise PublicationError(message)


def sha256(body):
    return hashlib.sha256(body).hexdigest()


def git_blob(body):
    return hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()


def encoded(data):
    return (json.dumps(data, sort_keys=True, indent=2) + '\n').encode()


def validate(files):
    require(bool(files), 'Empty publication')
    require(sum(len(b) for b in files.values()) <= LIMIT, 'Evidence budget exceeded')
    for path, body in files.items():
        require(type(body) is bytes, 'Publication values must be bytes')
        parts = PurePosixPath(path).parts
        require(path.startswith(PREFIX) and '..' not in parts and
                str(PurePosixPath(path)) == path and '\\' not in path,
                'Non-evidence or noncanonical path: ' + path)


def file_manifest(files):
    validate(files)
    return {p: {'size': len(b), 'sha256': sha256(b), 'git_blob': git_blob(b)}
            for p, b in sorted(files.items())}


def unpack(blob, digest, expected_names):
    require(len(blob) <= LIMIT and sha256(blob) == digest, 'Wrong archive digest or size')
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        entries = z.infolist()
        names = [f.filename for f in entries]
        require(len(names) == len(set(names)) and set(names) == set(expected_names),
                'Duplicate, missing or extra archive member')
        require(sum(f.file_size for f in entries) <= LIMIT, 'Unpacked budget exceeded')
        for f in entries:
            path = PurePosixPath(f.filename)
            require(not f.is_dir() and not path.is_absolute() and '..' not in path.parts
                    and '\\' not in f.filename and str(path) == f.filename
                    and not stat.S_ISLNK(f.external_attr >> 16), 'Unsafe ZIP member')
        return {f.filename: z.read(f) for f in entries}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class API:
    def __init__(self):
        repo = os.environ['GITHUB_REPOSITORY']
        require(repo == 'proteinfoldingengine/WetLabEngine', 'Unexpected repository')
        self.root = 'https://api.github.com/repos/' + repo + '/'
        self.token = os.environ['GH_TOKEN']

    def request(self, method, path, data=None):
        require(not path.startswith('/') and '://' not in path, 'Invalid API path')
        request = urllib.request.Request(self.root + path,
            data=encoded(data) if data is not None else None, method=method,
            headers={'Authorization': 'Bearer ' + self.token,
                     'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
        return urllib.request.build_opener(NoRedirect).open(request, timeout=60)

    def json(self, method, path, data=None):
        try:
            with self.request(method, path, data) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='replace')
            raise APIError(exc.code, detail[:1000]) from None

    def archive(self, artifact):
        try:
            with self.request('GET', f'actions/artifacts/{artifact}/zip') as response:
                return response.read(LIMIT + 1)
        except urllib.error.HTTPError as exc:
            if exc.code != 302:
                raise APIError(exc.code, 'Artifact download rejected') from None
            url = exc.headers['Location']
        parsed = urllib.parse.urlsplit(url)
        require(parsed.scheme == 'https' and parsed.hostname and
                (parsed.hostname.endswith('.blob.core.windows.net') or
                 parsed.hostname.endswith('.githubusercontent.com')),
                'Unexpected artifact redirect host')
        # Deliberately do NOT forward the API Authorization header.
        with urllib.request.urlopen(url, timeout=60) as response:
            return response.read(LIMIT + 1)


def ref_sha(api, branch):
    try:
        return api.json('GET', 'git/ref/heads/' + branch)['object']['sha']
    except APIError as exc:
        if exc.status == 404:
            return None
        raise


def await_ref(api, branch, expected, previous, sleep=time.sleep):
    # Read-only bounded convergence: never accept an unrelated ref or rewrite it.
    observations = []
    for attempt in range(5):
        observed = ref_sha(api, branch)
        observations.append(observed)
        if observed == expected:
            return
        require(observed == previous, 'Unexpected concurrent reference: ' + str(observed))
        if attempt < 4:
            print('Reference readback has previous value; retrying GET:',
                  branch, observed, 'expected', expected, flush=True)
            sleep(0.5 * (2 ** attempt))
    raise PublicationError('Reference did not converge: ' + json.dumps(observations))


def blob_read(api, sha):
    result = api.json('GET', 'git/blobs/' + sha)
    require(result['encoding'] == 'base64', 'Unexpected blob encoding')
    body = base64.b64decode(result['content'])
    require(git_blob(body) == sha, 'Remote blob identity mismatch')
    return body


def verify_added(api, base, commit, files):
    diff = api.json('GET', f'compare/{base}...{commit}')
    rows = diff['files']
    expected = {(p, git_blob(b)) for p, b in files.items()}
    actual = {(r['filename'], r['sha']) for r in rows}
    require(diff['total_commits'] == 1 and len(rows) == len(files) and
            actual == expected and all(r['status'] == 'added' for r in rows),
            'Publication changed an unexpected path, existing file, or ancestor')
    for path, body in files.items():
        require(blob_read(api, git_blob(body)) == body, 'Immutable byte mismatch: ' + path)


def publish(api, base, branch, files):
    validate(files)
    require(re.fullmatch('[0-9a-f]{40}', base) is not None, 'Invalid base SHA')
    require(branch.startswith('research/') and '..' not in branch, 'Invalid evidence branch')
    existing = ref_sha(api, branch)
    require(existing is None or existing == base, 'Evidence reference collision')
    if existing is None:
        # Reference creation points ONLY at an already-published source commit.
        api.json('POST', 'git/refs', {'ref': 'refs/heads/' + branch, 'sha': base})
    await_ref(api, branch, base, None)
    tree = api.json('GET', 'git/commits/' + base)['tree']['sha']
    changes = []
    for path, body in sorted(files.items()):
        row = {'path': path, 'mode': '100644', 'type': 'blob'}
        try:
            row['content'] = body.decode('utf-8')
        except UnicodeDecodeError:
            result = api.json('POST', 'git/blobs',
                {'encoding': 'base64', 'content': base64.b64encode(body).decode()})
            require(result['sha'] == git_blob(body), 'Uploaded blob identity mismatch')
            row['sha'] = result['sha']
        changes.append(row)
    created_tree = api.json('POST', 'git/trees', {'base_tree': tree, 'tree': changes})['sha']
    result = api.json('POST', 'git/commits',
        {'message': 'evidence: immutable publication ' + branch.rsplit('/', 1)[-1],
         'tree': created_tree, 'parents': [base]})
    require([p['sha'] for p in result['parents']] == [base] and
            result['tree']['sha'] == created_tree, 'Unexpected evidence commit ancestry')
    commit = result['sha']
    verify_added(api, base, commit, files)
    updated = api.json('PATCH', 'git/refs/heads/' + branch, {'sha': commit, 'force': False})
    require(updated['object']['sha'] == commit, 'Reference update receipt differs')
    await_ref(api, branch, commit, base)
    verify_added(api, base, commit, files)
    return commit


def recover(api, base):
    existing = ref_sha(api, ARCHIVE_BRANCH)
    manifest_path = ARCHIVE_ROOT + 'MANIFEST.json'
    if existing:
        obj = api.json('GET', 'contents/' + manifest_path + '?ref=' + existing)
        raw = base64.b64decode(obj['content'])
        require(git_blob(raw) == obj['sha'], 'Archive manifest identity mismatch')
        data = json.loads(raw)
        require(data['archives'] == PINS, 'Archive provenance pins changed')
        files = {}
        for path, row in data['files'].items():
            files[path] = blob_read(api, row['git_blob'])
        require(file_manifest(files) == data['files'], 'Existing archival manifest mismatch')
        files[manifest_path] = raw
        verify_added(api, data['publication_parent'], existing, files)
        return existing
    files = {}
    for pin in PINS:
        meta = api.json('GET', f"actions/artifacts/{pin['artifact']}")
        require(meta['id'] == pin['artifact'] and meta['size_in_bytes'] == pin['size'] and
                meta['workflow_run']['id'] == pin['run'] and
                meta['workflow_run']['head_sha'] == pin['source'] and
                meta.get('digest') == 'sha256:' + pin['sha256'], 'Wrong original artifact metadata')
        blob = api.archive(pin['artifact'])
        require(len(blob) == pin['size'], 'Wrong original ZIP byte count')
        members = unpack(blob, pin['sha256'], set(pin['members']))
        context = json.loads(members['context.json'])
        require(context['implementation_commit'] == pin['source'] and
                int(context['run_id']) == pin['run'] and
                int(context['run_attempt']) == pin['attempt'], 'Wrong original execution provenance')
        root = ARCHIVE_ROOT + str(pin['run']) + '-1/'
        files[root + 'artifact.zip'] = blob
        files.update({root + 'members/' + name: body for name, body in members.items()})
    data = {'archives': PINS, 'publication_parent': base,
            'status': 'ARCHIVAL_RECOVERY_ONLY_ORIGINAL_RUN_FAILURES_UNCHANGED',
            'files': file_manifest(files)}
    files[manifest_path] = encoded(data)
    return publish(api, base, ARCHIVE_BRANCH, files)


def main():
    api = API()
    base = os.environ['GITHUB_SHA']
    root = Path(os.environ['RUNNER_TEMP']) / 'a12-output'
    root.mkdir(parents=True, exist_ok=True)
    archive_commit = recover(api, base)
    print('Verified historical archive commit:', archive_commit, flush=True)
    run, attempt = os.environ['GITHUB_RUN_ID'], os.environ['GITHUB_RUN_ATTEMPT']
    require(run.isdigit() and attempt.isdigit(), 'Invalid run/attempt')
    dest = PREFIX + run + '-' + attempt + '/'
    files = {}
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(), 'Symlink in execution output')
        if p.is_file():
            files[dest + p.relative_to(root).as_posix()] = p.read_bytes()
    data = {'publication_parent': base, 'run_id': run, 'run_attempt': attempt,
            'historical_archive_commit': archive_commit, 'files': file_manifest(files),
            'status': 'EXECUTION_EVIDENCE_NOT_MATHEMATICAL_ACCEPTANCE'}
    files[dest + 'MANIFEST.json'] = encoded(data)
    commit = publish(api, base, 'research/a12-evidence-' + run + '-' + attempt, files)
    receipt = {'status': 'PUBLISHED_AND_IMMUTABLE_BYTES_VERIFIED',
               'scientific_commit': base, 'evidence_commit': commit,
               'historical_archive_commit': archive_commit,
               'published_files': len(files), 'run_id': run, 'run_attempt': attempt}
    (root / 'publication_receipt.json').write_bytes(encoded(receipt))
    print(json.dumps(receipt, sort_keys=True), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
