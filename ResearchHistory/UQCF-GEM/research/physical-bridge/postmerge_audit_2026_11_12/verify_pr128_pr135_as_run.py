"""Offline checks for the two integrated archival review packets."""
import ast
import functools
import hashlib
import io
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
GIT = ROOT / 'pr106_conflict'
BASE = 'ResearchHistory/UQCF-GEM/research/physical-bridge/'
HEAD = '2ab565c3f5bf10305a96ddeef30901de49959ba5'
MODEL = 'gemini-3.1-pro-preview'
REPO = 'proteinfoldingengine/WetLabEngine'
ORIGINS = {128: ROOT / 'pr128_review/repo', 135: ROOT / 'pr135_review/repo'}


def git(*args):
    return subprocess.check_output(
        ['git', '-C', str(GIT), *args],
        env={**os.environ, 'GIT_NO_LAZY_FETCH': '1', 'GIT_TERMINAL_PROMPT': '0'},
        stderr=subprocess.DEVNULL,
    )


@functools.cache
def tree(ref):
    rows = {}
    for entry in git('ls-tree', '-rz', ref).split(b'\0'):
        if entry:
            info, path = entry.split(b'\t', 1)
            mode, kind, digest = info.decode().split()
            if kind == 'blob':
                rows[path.decode()] = (mode, digest)
    return rows


def read(pr, path, *refs):
    raw = git('cat-file', 'blob', tree(HEAD)[path][1])
    local = ORIGINS[pr] / path
    if local.is_file():
        assert raw == local.read_bytes(), path
    assert all(tree(ref)[path] == ('100644', identity(raw)['git_blob'])
               for ref in (HEAD, *refs)), path
    return raw


def unique_dict(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, f'duplicate JSON key {key}'
        result[key] = value
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique_dict)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(raw):
    return {'bytes': len(raw), 'sha256': sha(raw),
            'git_blob': hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()}


def directory(ref, prefix):
    return {p: data for p, data in tree(ref).items() if p.startswith(prefix + '/')}


def parents(ref):
    return git('show', '-s', '--format=%P', ref).decode().split()


def ancestor(early, late):
    git('merge-base', '--is-ancestor', early, late)


def check_chain(review, evidence, pr_head, merge):
    ancestor(review, evidence)
    assert parents(pr_head) == [evidence]
    assert parents(merge)[1:] == [pr_head]
    ancestor(merge, HEAD)


def zip_members(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names))
        assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts
                   for n in names)
        assert archive.testzip() is None
        return {name: archive.read(name) for name in names}


def check_run(run, jobs, run_id, review):
    assert (run['id'], run['run_attempt'], run['head_sha']) == (run_id, 1, review)
    assert run['status'] == 'completed' and run['conclusion'] == 'success'
    assert run['repository']['full_name'] == REPO
    assert len(jobs) == 3
    assert {job['name'] for job in jobs} == {'integrity', 'argument-review', 'publication-audit'}
    for job in jobs:
        assert (job['status'], job['conclusion'], job['run_id']) == ('completed', 'success', run_id)
        assert job.get('head_sha', review) == review and job.get('run_attempt', 1) == 1


def verify_zip(raw, prior, meta, upload_log, run, review, branch):
    assert raw == prior
    assert (meta['workflow_run']['id'], meta['workflow_run']['head_sha'],
            meta['workflow_run']['head_branch']) == (run, review, branch)
    assert len(raw) == meta['size_in_bytes'] and meta['digest'] == 'sha256:' + sha(raw)
    assert re.search(rb'SHA256 digest of uploaded artifact zip is ' + sha(raw).encode() + rb'\b',
                     upload_log)
    members = zip_members(raw)
    return members, {'artifact_id': meta['id'], **identity(raw),
                     'members': {n: identity(data) for n, data in sorted(members.items())}}


def framed(label, raw):
    raw.decode('utf-8')
    return f'\nEXACT DOCUMENT {label}\nUTF8-BYTES {len(raw)}\n'.encode() + raw + b'\nEND EXACT DOCUMENT\n'


def verify_answer(members, prompt):
    assert members['prompt.txt'] == prompt
    request = parse(members['request.json'])
    assert request == {
        'contents': [{'role': 'user', 'parts': [{'text': prompt.decode()}]}],
        'generationConfig': {'temperature': 0, 'maxOutputTokens': 32768,
                             'responseMimeType': 'application/json'},
    }
    metadata = parse(members['model_metadata.json'])
    assert metadata['name'] == 'models/' + MODEL and 'generateContent' in metadata['supportedGenerationMethods']
    response = parse(members['response.json'])
    assert not response.get('promptFeedback', {}).get('blockReason')
    assert response['modelVersion'] == MODEL
    candidates = response['candidates']
    assert len(candidates) == 1 and candidates[0]['finishReason'] == 'STOP'
    visible = '\n'.join(
        part['text'] for part in candidates[0]['content']['parts']
        if not part.get('thought', False) and isinstance(part.get('text'), str)
    ).strip().encode()
    assert visible == members['review.txt']
    verdict = parse(visible)
    assert verdict == parse(members['verdict.json'])
    assert verdict['verdict'] == 'ACCEPTED' and verdict['native_bridge_status'] == 'NOT_DERIVED'
    assert all(verdict[name] == [] for name in ('findings', 'missing_assumptions', 'counterexamples'))
    return verdict


def audit128():
    pr = 128
    review = '2a2b0de6e5109dadf72b826268ed77f2c6faed41'
    evidence = '5ccb8cbdc7580bebfb0c6fc5436d2b5bdaa4a36c'
    pr_head = '9b7a37f565c661fdef1c608ba3b33c156547ab59'
    merge = '7f59608e6b33548415c65a7f378c760825d29172'
    science = '844c237d27dc5206acbcfaf5579485cc5274c04f'
    run = 43239959416
    rel = BASE + 'retained_grade_transport/independent_review_2026_11_12'
    public = rel + '/public_evidence'
    check_chain(review, evidence, pr_head, merge)
    paths = directory(HEAD, rel)
    assert paths == directory(merge, rel) == directory(pr_head, rel)
    integrated = {path: read(pr, path) for path in paths}
    receipt = parse(integrated[rel + '/READBACK.json'])
    assert receipt['readback_commit'] == evidence and receipt['status'] == 'PASS'
    assert receipt['all_changes_additive'] and receipt['all_original_files_unchanged']
    assert (receipt['workflow_sha'], receipt['scientific_sha'], receipt['run_id'], receipt['run_attempt']) == (
        review, science, str(run), 1)
    new_files = {item['path']: item for item in receipt['new_files']}
    assert len(new_files) == receipt['new_file_count'] == 32
    assert set(new_files) == set(tree(evidence)) - set(tree(science))
    for p, row in new_files.items():
        assert row == {'path': p, **identity(read(pr, p, evidence, pr_head, merge))}, p
    assert set(tree(pr_head)) - set(tree(evidence)) == {rel + '/READBACK.json'}
    manifest = parse(integrated[public + '/MANIFEST.json'])['files']
    assert {p for p in paths if p.startswith(public + '/')} == {
        public + '/' + p for p in set(manifest) | {'MANIFEST.json'}}
    assert manifest == {p: identity(integrated[public + '/' + p]) for p in manifest}
    archived_api = parse(integrated[public + '/artifacts.json'])['artifacts']
    jobs = parse(integrated[public + '/jobs.json'])['jobs']
    check_run(parse(integrated[public + '/run.json']), jobs, run, review)
    download = parse(integrated[public + '/DOWNLOAD_AUDIT.json'])
    zip_sets, archives = {}, {}
    for meta in archived_api:
        artifact = meta['name']
        label = artifact.removeprefix('retained-grade-').removesuffix('-1')
        log_name = {'integrity': 'integrity', 'review': 'argument-review',
                    'publication': 'publication-audit'}[label]
        zip_path = public + '/' + artifact + '.zip'
        members, record = verify_zip(
            integrated[zip_path], (ROOT / 'pr128_review' / (artifact + '.zip')).read_bytes(),
            meta, integrated[public + '/logs/' + log_name + '.log'], run, review,
            'gpt/retained-grade-transport',
        )
        assert parse(members['artifact_manifest.json']) == {
            n: identity(data) for n, data in members.items() if n != 'artifact_manifest.json'}
        assert next(a for a in download['archives'] if a['name'] == artifact) == {
            'name': artifact, **{k: v for k, v in record.items() if k != 'members'},
            'members': [{'name': n, **ident} for n, ident in record['members'].items()],
        }
        assert next(a for a in receipt['original_archives'] if a['path'] == zip_path) == {
            'path': zip_path, **{k: v for k, v in record.items() if k != 'members'},
        }
        for name, data in members.items():
            if not name.startswith('source_originals/'):
                assert integrated[f'{public}/{label}/{name}'] == data
        zip_sets[label] = members
        archives[artifact] = record
    assert set(zip_sets) == {'integrity', 'review', 'publication'}
    packet_raw = integrated[rel + '/SOURCE_PACKET.json']
    assert packet_raw == zip_sets['integrity']['SOURCE_PACKET.json'] == zip_sets['review']['SOURCE_PACKET.json']
    packet = parse(packet_raw)
    assert len(packet['documents']) == 6 and len(packet['helpers']) == 2 and len(packet['sources']) == 9
    assert receipt['source_packet_sha256'] == sha(packet_raw) == download['source_packet_sha256']
    original_readback = {item['path']: item for item in receipt['originals']}
    assert len(original_readback) == receipt['original_file_count'] == 6
    docs = {doc['id']: doc for doc in packet['documents']}
    for entry in packet['documents'] + packet['helpers']:
        p = entry['path']
        raw = read(pr, p, science, review, pr_head, merge)
        assert entry['ref'] == science and all(entry[k] == v for k, v in identity(raw).items())
        if 'content' in entry:
            assert raw == entry['content'].encode()
            assert all(original_readback[p][k] == v for k, v in identity(raw).items())
    historical_commit_bindings = []
    for i, entry in enumerate(packet['sources']):
        raw = zip_sets['integrity'][f'source_originals/{i}.txt']
        assert all(entry[k] == v for k, v in identity(raw).items())
        source = parse(docs[entry['packet_id']]['content'])
        table = 'sources' if entry['packet_id'] == 'original_sources' else 'additional_sources'
        entry_source = source[table][entry['index']]
        assert (entry_source['commit'], entry_source['git_blob']) == (entry['ref'], entry['git_blob'])
        assert (entry_source.get('path') or entry_source['url'].split('/blob/' + entry['ref'] + '/')[1]) == entry['path']
        assert 0 <= entry['byte_start'] <= entry['byte_end'] <= len(raw)
        assert raw[entry['byte_start']:entry['byte_end']] == entry_source['content'].encode()
        try:
            source_tree = tree(entry['ref'])
        except subprocess.CalledProcessError:
            historical_commit_bindings.append(False)
        else:
            assert source_tree[entry['path']][1] == entry['git_blob']
            historical_commit_bindings.append(True)
    script_path = '.github/scripts/uqcf_retained_grade_review.py'
    script = read(pr, script_path, review, pr_head, merge)
    for p in ['.github/scripts/uqcf_retained_grade_tests.py',
              '.github/workflows/uqcf-retained-grade-transport-review.yml']:
        read(pr, p, review, pr_head, merge)
    header = next(ast.literal_eval(node.value) for node in ast.parse(script).body
                  if isinstance(node, ast.Assign)
                  and any(isinstance(target, ast.Name) and target.id == 'HEADER'
                          for target in node.targets))
    prompt = header.encode() + b''.join(framed(d['id'], d['content'].encode()) for d in packet['documents'])
    verdict = verify_answer(zip_sets['review'], prompt)
    assert len(verdict['proof_checks']) == 14
    integrity = parse(zip_sets['integrity']['integrity.json'])
    review_manifest = parse(zip_sets['review']['manifest.json'])
    publication = parse(zip_sets['publication']['receipt.json'])
    for body in (integrity, review_manifest, publication):
        assert (body['run_id'], body['run_attempt'], body['checkout_sha'], body['workflow_sha'],
                body['scientific_sha'], body['source_packet_sha256']) == (
            str(run), '1', review, review, science, sha(packet_raw))
    assert (integrity['status'], review_manifest['status'], publication['status']) == ('PASS', 'ACCEPTED', 'PASS')
    assert review_manifest['model_requested'] == review_manifest['model_returned'] == MODEL
    assert publication['reviewer_verdict'] == 'ACCEPTED' and publication['native_bridge'] == 'NOT_DERIVED'
    assert review_manifest['integrity_manifest_sha256'] == publication['integrity_manifest_sha256'] == sha(
        zip_sets['integrity']['artifact_manifest.json'])
    assert publication['review_manifest_sha256'] == sha(zip_sets['review']['artifact_manifest.json'])
    assert integrity['scientific_execution'] is publication['scientific_execution'] is publication['inherited_stack_recertified'] is False
    assert publication['remote_source_count'] == 17 and integrity['source_binding_count'] == 9
    assert 'Ran 10 tests' in zip_sets['integrity']['plumbing.log'].decode()
    record = integrated[rel + '/ACCEPTANCE.md'].decode()
    for key in ('response.json', 'review.txt'):
        assert sha(zip_sets['review'][key]) in record
    assert 'without relying on controller memory' in verdict['next_native_obligation']
    assert 'not adopted' in record and 'COMPLETE augmented input' in record and 'T237' in record
    return {
        'reviewed_checkout': review, 'evidence_commit': evidence, 'verified_pr_head': pr_head,
        'actual_merge': merge, 'run_id': run, 'run_attempt': 1, 'model': MODEL,
        'scoped_review': verdict['verdict'], 'native_status': verdict['native_bridge_status'],
        'publication_files_verified': len(paths), 'readback_files_verified': len(new_files),
        'readable_evidence_manifest_entries': len(manifest),
        'original_documents': len(packet['documents']), 'source_bindings': len(packet['sources']),
        'archived_source_bindings_also_matched_to_locally_available_historical_git_trees': sum(historical_commit_bindings),
        'helper_bindings': len(packet['helpers']), 'plumbing_tests_preserved': 10,
        'source_packet_sha256': sha(packet_raw), 'prompt': identity(prompt),
        'raw_response': identity(zip_sets['review']['response.json']),
        'archives': archives,
        'scope_reconciliation': 'The supplied grade lift and coincident complete augmented input bound the result. '
                                'The memory-free suggestion was not adopted. The T237 generalization remains outside review.',
        'premerge_status_wording': 'ACCEPTANCE.md is the historical premerge record. Actual merged state is established by Git ancestry.',
    }


def audit135():
    pr = 135
    review = 'd94eb535fe41aba2b57d96a5f657ae6058737e47'
    evidence = 'a33bb0a80bc786f97ebb1bb580cc81552360c5a8'
    pr_head = 'e4ec38ef414c1c7d6a37c0b3c8d10c433357ecfc'
    merge = 'b7289a144a68c4f7f9d0c59c53cfd8edb48da224'
    baseline = '2a72e2331e910e17c82abb537a1162280102ef78'
    run = 43239476179
    original = BASE + 'groupoid_identity_ownership'
    rel = original + '/independent_review_2026_11_12'
    public = rel + '/evidence/run_43239476179_attempt_1'
    check_chain(review, evidence, pr_head, merge)
    paths = directory(HEAD, rel)
    assert paths == directory(merge, rel) == directory(pr_head, rel)
    integrated = {path: read(pr, path) for path in paths}
    receipt = parse(integrated[rel + '/IMMUTABLE_READBACK.json'])
    assert (receipt['evidence_commit'], receipt['reviewed_commit'], receipt['source_packet_baseline']) == (
        evidence, review, baseline)
    assert (receipt['status'], receipt['run_id'], receipt['run_attempt'], receipt['run_conclusion']) == (
        'PASS', run, 1, 'success')
    assert receipt['requested_and_returned_model'] == MODEL
    assert receipt['raw_verdict'] == 'ACCEPTED' and receipt['native_bridge_status'] == 'NOT_DERIVED'
    assert all(row['status'] == 'EXACT_REMOTE_BYTE_MATCH' for row in receipt['files'])
    readback = {row['path']: {k: row[k] for k in ('bytes', 'sha256', 'git_blob')}
                for row in receipt['files']}
    assert set(readback) == set(tree(evidence)) - set(tree(review))
    assert set(tree(pr_head)) - set(tree(evidence)) == {rel + '/IMMUTABLE_READBACK.json'}
    assert len(readback) == receipt['files_verified'] == 23
    assert readback == {p: identity(read(pr, p, evidence, pr_head, merge)) for p in readback}
    assert receipt['total_bytes_verified'] == sum(a['bytes'] for a in readback.values())
    manifest = parse(integrated[rel + '/PUBLICATION_MANIFEST.json'])
    assert manifest['files'] == {p: v for p, v in readback.items() if p != rel + '/PUBLICATION_MANIFEST.json'}
    assert (manifest['reviewed_sha'], manifest['source_baseline'], manifest['run_id'], manifest['run_attempt']) == (
        review, baseline, run, 1)
    assert manifest['model_requested'] == manifest['model_returned'] == MODEL
    assert manifest['verdict'] == 'ACCEPTED' and manifest['native_bridge_status'] == 'NOT_DERIVED'
    assert manifest['scientific_execution'] is False
    run_meta = parse(integrated[public + '/run_metadata.json'])
    check_run(run_meta['run'], run_meta['jobs'], run, review)
    zip_sets, archives = {}, {}
    for meta in run_meta['artifacts']:
        artifact = meta['name']
        label = artifact.removeprefix('pr135-').removesuffix('-1')
        members, record = verify_zip(
            integrated[public + '/original_artifacts/' + artifact + '.zip'],
            (ROOT / 'pr135_review/artifacts' / (artifact + '.zip')).read_bytes(),
            meta, integrated[public + '/job_logs/' + label + '.log'], run, review,
            'gpt/groupoid-identity-ownership',
        )
        member_prefix = f'{public}/pr135_{label}/'
        assert {p.removeprefix(member_prefix) for p in paths if p.startswith(member_prefix)} == set(members)
        assert all(integrated[member_prefix + n] == data for n, data in members.items())
        zip_sets[label] = members
        archives[artifact] = record
    assert set(zip_sets) == {'integrity', 'review', 'publication'}
    lock_raw = integrated[rel + '/source_lock.json']
    lock = parse(lock_raw)
    integrity = zip_sets['integrity']
    reviewer = zip_sets['review']
    publication = zip_sets['publication']
    assert lock_raw == integrity['source_manifest.json']
    source_paths = {item['path'] for item in lock['files']}
    assert len(source_paths) == len(lock['files']) == 115
    assert set(directory(baseline, original)) == source_paths
    assert {p for p in directory(review, original) if not p.startswith(rel + '/')} == source_paths
    assert {p for p in directory(HEAD, original) if not p.startswith(rel + '/')} == source_paths
    inputs = parse(integrity['input_manifest.json'])
    assert integrity['input_manifest.json'] == reviewer['input_manifest.json'] == publication['readback_manifest.json']
    assert len(inputs) == 123
    input_bytes = {p: read(pr, p, review, pr_head, merge) for p in inputs}
    assert inputs == {p: identity(raw) for p, raw in input_bytes.items()}
    for item in lock['files']:
        p = item['path']
        assert item == {'path': p, **inputs[p]}
        assert tree(baseline)[p] == tree(HEAD)[p]
    source_archives = {archive['path']: archive['members'] for archive in lock['archives']}
    assert len(source_archives) == len(lock['archives']) == 11
    assert set(source_archives) == {p for p in source_paths if p.endswith('.zip')}
    copies = set()
    for path, records in source_archives.items():
        members = zip_members(input_bytes[path])
        assert set(members) == {r['name'] for r in records} and len(members) == len(records)
        for record in records:
            n, copy = record['name'], record['copy_path']
            assert copy not in copies and copy in source_paths
            copies.add(copy)
            assert members[n] == input_bytes[copy]
            assert record == {'name': n, 'copy_path': copy, **identity(members[n])}
    assert len(copies) == 74
    extra_paths = [rel + '/' + name for name in ('FREEZE.md', 'PROMPT.md', 'source_lock.json')]
    extra_paths += ['.github/scripts/uqcf_pr135_' + name + '.py'
                    for name in ('integrity', 'review', 'publication', 'tests')]
    extra_paths += ['.github/workflows/uqcf-pr135-independent-review.yml']
    assert set(inputs) == source_paths | set(extra_paths)
    prompt_paths = [rel + '/FREEZE.md', rel + '/source_lock.json'] + sorted(source_paths - set(source_archives))
    prompt = input_bytes[rel + '/PROMPT.md'] + b''.join(framed(p, input_bytes[p]) for p in prompt_paths)
    verdict = verify_answer(reviewer, prompt)
    integrity_summary = parse(integrity['integrity.json'])
    review_manifest = parse(reviewer['manifest.json'])
    publication_summary = parse(publication['publication.json'])
    for body in (integrity_summary, review_manifest, publication_summary):
        assert (body['run_id'], body['run_attempt'], body['source_sha'], body['workflow_sha'], body['repository']) == (
            str(run), '1', review, review, REPO)
    assert (integrity_summary['status'], review_manifest['status'], publication_summary['status']) == (
        'PASS', 'ACCEPTED', 'PASS')
    assert review_manifest['generation_calls_maximum'] == 1
    assert review_manifest['model_requested'] == review_manifest['model_returned'] == MODEL
    assert publication_summary['model_requested'] == publication_summary['model_returned'] == MODEL
    assert publication_summary['verdict'] == 'ACCEPTED' and publication_summary['native_bridge_status'] == 'NOT_DERIVED'
    assert publication_summary['source_lock_sha256'] == integrity_summary['source_lock_sha256'] == sha(lock_raw)
    assert integrity_summary['source_manifest_sha256'] == sha(lock_raw)
    assert integrity_summary['prompt_sha256'] == sha(prompt)
    assert integrity_summary['input_manifest_sha256'] == publication_summary['readback_manifest_sha256'] == sha(
        integrity['input_manifest.json'])
    integrity_hashes = {n: sha(raw) for n, raw in integrity.items()}
    review_hashes = {n: sha(raw) for n, raw in reviewer.items()}
    assert review_manifest['artifact_hashes'] == {n: v for n, v in review_hashes.items() if n != 'manifest.json'}
    assert review_manifest['integrity_artifacts'] == publication_summary['integrity_artifacts'] == integrity_hashes
    assert publication_summary['review_artifacts'] == review_hashes
    assert integrity_summary['scientific_execution'] is publication_summary['scientific_execution'] is False
    assert 'Ran 31 tests' in integrity['tests.log'].decode()
    record = integrated[rel + '/REVIEW_RECORD.md'].decode()
    assert all(sha(raw) in record for raw in (reviewer['response.json'], prompt, lock_raw))
    limitations = ' '.join(verdict['limitations'])
    assert 'v9.50' in limitations and 'V1689' in limitations and 'W_R/W_E' in limitations
    assert 'requires a new axiom' in ' '.join(verdict['constructive_analysis'])
    assert 'typed mapping into the W_R/W_E' in verdict['next_native_obligation']
    assert 'not adopted as a universal necessity theorem' in record
    assert 'not imposed as a Hilbert-space prerequisite' in record and 'discrepancy remains open' in record
    return {
        'reviewed_checkout': review, 'evidence_commit': evidence, 'verified_pr_head': pr_head,
        'actual_merge': merge, 'run_id': run, 'run_attempt': 1, 'model': MODEL,
        'scoped_review': verdict['verdict'], 'native_status': verdict['native_bridge_status'],
        'publication_files_verified': len(paths), 'readback_files_verified': len(readback),
        'publication_manifest_entries': len(manifest['files']), 'original_packet_files': len(source_paths),
        'workflow_inputs': len(inputs), 'original_packet_archives': len(source_archives),
        'original_packet_archive_members': len(copies), 'plumbing_tests_preserved': 31,
        'source_lock_sha256': sha(lock_raw), 'prompt': identity(prompt),
        'raw_response': identity(reviewer['response.json']), 'archives': archives,
        'scope_reconciliation': 'The copy-new-axiom and Hilbert-space suggestions are not universal '
                                'requirements. The v9.50 byte discrepancy, absent V1689 generating-code '
                                'provenance and missing typed W_R/W_E correspondence remain unresolved.',
        'premerge_status_wording': 'REVIEW_RECORD.md is the historical premerge record. Actual merged state is established by Git ancestry.',
    }


report = {
    'status': 'PASS',
    'integrated_research_head': HEAD,
    'method': 'Offline Git path/mode/blob checks and independent verification of integrated Git blob bytes '
              'against prior downloads and archival copies.',
    'pr128': audit128(),
    'pr135': audit135(),
    'limits': 'Revalidated publication evidence and exact review reconstruction. The original CI job '
              'entry points require their historic checkout/run environment and, for live API readback, '
              'GitHub access. Review generation and historical scientific calculations were not run.',
}
print(json.dumps(report, indent=2, sort_keys=True))
