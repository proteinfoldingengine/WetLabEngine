"""Fail-closed, dependency-free checks for original publication evidence."""
import hashlib
import io
import json
import pathlib
import re
import zipfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def check_review(raw, manifest, event):
    require(manifest['research_commit'] == manifest['workflow_commit'] == event,
            'Review event-commit mismatch')
    require(sha256(raw) == manifest['response_sha256'], 'Review response digest mismatch')
    require(manifest['model'] == 'gemini-3.1-pro-preview', 'Unexpected reviewed model')
    require(manifest['attempts'] == [{'attempt': 1, 'status': 'RESPONSE_RECEIVED'}],
            'Unexpected review attempt history for pinned run')
    text = raw.decode('utf-8').strip()
    if text.startswith('```'):
        require(text.endswith('```'), 'Unclosed review code fence')
        text = re.sub(r'^```(?:json)?\s*', '', text)[:-3].strip()
    obj = json.loads(text)
    for key in ('findings', 'missing_assumptions', 'counterexamples', 'limitations'):
        require(type(obj.get(key)) is list, 'Missing review array: ' + key)
    require(obj['verdict'] == 'ACCEPTED', 'Nonaccepting review must be reconciled')
    require(not obj['missing_assumptions'] and not obj['counterexamples'],
            'Adverse review findings require reconciliation')
    return obj


def check_tests(text, expected):
    counts = re.findall(r'^Ran (\d+) tests? in ', text, re.M)
    require(counts == [str(expected)], 'Per-suite test count mismatch')
    require(len(re.findall(r'^test_[^\n]*\.\.\. ok$', text, re.M)) == expected,
            'Missing individual passing test identities')
    require(text.rstrip().endswith('OK'), 'Missing successful suite terminator')
    require(not re.search(r'^FAILED|^ERROR:|^FAIL:', text, re.M), 'Failed tests in evidence')
    return expected


def check_inputs(wanted, actual):
    require(set(wanted) == set(actual), 'Review input identity set mismatch')
    for name, digest in wanted.items():
        require(sha256(actual[name]) == digest, 'Input digest mismatch: ' + name)
    return len(actual)


def check_log(text, event, digest):
    for marker in ('Current runner version', event, digest, 'Cleaning up orphan processes'):
        require(marker in text, 'Incomplete or misbound job log: ' + marker)


def check_zip(raw, expected):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'Duplicate ZIP member')
        require(set(names) == set(expected), 'ZIP member identity mismatch')
        require(archive.testzip() is None, 'ZIP CRC failure')
        for name in names:
            p = pathlib.PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts, 'Unsafe ZIP member path')
        return {name: archive.read(name) for name in names}
