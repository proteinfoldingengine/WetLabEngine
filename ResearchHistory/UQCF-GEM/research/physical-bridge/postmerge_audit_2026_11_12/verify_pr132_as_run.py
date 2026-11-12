import hashlib
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile


LOCAL = Path(__file__).resolve().parent
REPO = LOCAL.parent / 'pr106_conflict'
ROOT = Path('ResearchHistory/UQCF-GEM/research/physical-bridge/constructive_candidates/t273_rank_refinement')
BASE = '750554de424a1e12e2d14c6665920bda31163dfc'
REVIEWED = '8921a58e3ec687b3c712b07a75746e5a392ef54b'
CONTROLLER = '05dccd97511c201fc56822012335f3333b947143'
HEAD = '7718b659c49ffe44fb72d4adaad24da09b8982fc'
MERGE = '0d79b6bfbc9f1ee48dcf6be4b090e17796885d91'
INTEGRATED = '2ab565c3f5bf10305a96ddeef30901de49959ba5'
SNAPSHOTS = (HEAD, MERGE, INTEGRATED)
URL = 'https://github.com/proteinfoldingengine/WetLabEngine'


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])


def blob(ref, path):
    return git('cat-file', 'blob', f'{ref}:{path}')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_archive(artifact_id, zip_sha, path):
    archive = LOCAL / f't273-{artifact_id}.zip'
    assert sha(archive.read_bytes()) == zip_sha
    with ZipFile(archive) as opened:
        entries = opened.namelist()
        assert len(entries) == len(set(entries))
        data = {name: opened.read(name) for name in entries}
    manifest = json.loads(data['artifact_manifest.json'])
    assert set(data) == set(manifest) | {'artifact_manifest.json'}
    for name, record in manifest.items():
        assert record == {'bytes': len(data[name]), 'sha256': sha(data[name])}
    for name, raw in data.items():
        for ref in SNAPSHOTS:
            assert raw == blob(ref, path / name), (ref, str(path / name))
    return data


def main():
    parent_line = git('show', '-s', '--format=%P', MERGE).decode().strip().split()
    assert parent_line == ['5df9bde7c40553568c276177bee725683e43ad1d', HEAD]
    assert git('show', '-s', '--format=%an%n%aI', MERGE).decode().splitlines() == [
        'proteinfolding-grokbot', '2026-11-12T09:55:54-07:00'
    ]
    for parent, child in ((BASE, REVIEWED), (REVIEWED, CONTROLLER), (CONTROLLER, HEAD), (MERGE, INTEGRATED)):
        git('merge-base', '--is-ancestor', parent, child)

    audit_receipt = json.loads(blob(INTEGRATED, ROOT / 'AUDIT_ARTIFACT_RECEIPT.json'))
    review_receipt = json.loads(blob(INTEGRATED, ROOT / 'REVIEW_ARTIFACT_RECEIPT.json'))
    assert audit_receipt['reviewed_sha'] == review_receipt['reviewed_sha'] == REVIEWED
    assert audit_receipt['review_run_id'] == review_receipt['review_run_id'] == 41524434282
    assert audit_receipt['controller_sha'] == CONTROLLER
    assert audit_receipt['audit_run_id'] == 41525059170
    assert audit_receipt['audit_attempt'] == review_receipt['review_attempt'] == 1
    assert audit_receipt['status'] == 'PASS' and audit_receipt['publication_replay'] is True
    assert audit_receipt['native_bridge_status'] == review_receipt['native_bridge_status'] == 'NOT_DERIVED'
    live_archives = {
        'review': (13179825871, '660efc5a5a54ca4c627fdaad0aaa8c2c0dc44f87c578260454e94b1888d1d5e4'),
        'verification': (13180435111, 'd1f268a76264651d49b46e138e1c1c8a58448089405c953ef0f4a03d50b6cf14'),
        'publication': (13179272577, '5810d8afa68ac3711e142b3cf797765ed29fcbd6235846e680b5ae67d5851e81'),
    }
    assert live_archives['review'] == (review_receipt['artifact_id'], review_receipt['artifact_zip_sha256'])
    evidence_paths = {'review': ROOT / 'review/actions-41524434282'}
    for kind in ('verification', 'publication'):
        artifact = audit_receipt[f'{kind}_artifact']
        assert live_archives[kind] == (artifact['id'], artifact['zip_sha256'])
        evidence_paths[kind] = ROOT / 'audit/actions-41525059170' / kind
    evidence = {kind: verify_archive(*artifact, evidence_paths[kind]) for kind, artifact in live_archives.items()}

    review = evidence['review']
    docs = json.loads(review['documents.json'])
    assert len(docs) == 6
    prompt = review['prompt.txt']
    assert sha(prompt) == review_receipt['prompt_sha256']
    assert json.loads(review['request.json'])['contents'] == [{'role': 'user', 'parts': [{'text': prompt.decode()}]}]
    raw_response = review['response.json']
    response = json.loads(raw_response)
    assert not response.get('promptFeedback', {}).get('blockReason')
    assert sha(raw_response) == review_receipt['response_sha256']
    candidate, = response['candidates']
    assert candidate['finishReason'] == 'STOP'
    answer, = [part['text'] for part in candidate['content']['parts'] if not part.get('thought') and 'text' in part]
    assert answer.encode() == review['review.txt']
    verdict = json.loads(answer)
    assert verdict == json.loads(review['verdict.json'])
    assert verdict['verdict'] == review_receipt['verdict'] == 'ACCEPTED'
    assert verdict['native_bridge_status'] == 'NOT_DERIVED'
    assert all(verdict[key] == [] for key in ('findings', 'missing_assumptions', 'counterexamples', 'limitations'))
    assert len(verdict['constructive_analysis']) == 6
    identity = json.loads(review['review_identity.json'])
    assert identity['workflow_sha'] == identity['science_sha'] == REVIEWED
    assert (identity['run_id'], identity['run_attempt']) == ('41524434282', '1')
    assert identity['prompt_sha256'] == sha(prompt) and identity['response_sha256'] == sha(raw_response)
    assert identity['model_requested'] == identity['model_returned'] == response['modelVersion'] == 'gemini-3.1-pro-preview'
    metadata = json.loads(review['model_metadata.json'])
    assert metadata['name'] == f"models/{response['modelVersion']}"

    verification = evidence['verification']
    publication = evidence['publication']
    assert verification['review-gate.json'] == publication['review-gate.json']
    assert verification['source-readback.json'] == publication['source-readback.json']
    verified = json.loads(verification['receipt.json'])
    published = json.loads(publication['receipt.json'])
    assert verified | {'publication_replay': True} == published
    assert published['publication_replay'] is True and verified['publication_replay'] is False
    assert published['status'] == 'PASS' and published['scientific_breakthrough'] is False
    assert published['controller_sha'] == CONTROLLER and published['reviewed_sha'] == REVIEWED
    assert published['review_run_id'] == 41524434282 and published['native_bridge_status'] == 'NOT_DERIVED'
    assert json.loads(publication['review-gate.json'])['verdict'] == verdict
    source_readback = json.loads(publication['source-readback.json'])
    assert set(source_readback) == set(docs)
    for label, record in docs.items():
        path = record['path']
        raw = blob(REVIEWED, path)
        assert record == {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}
        assert b'\nEXACT DOCUMENT ' + label.encode() + f'\nUTF8-BYTES {len(raw)}\n'.encode() + raw + b'\nEND EXACT DOCUMENT\n' in prompt
        for ref in (CONTROLLER, *SNAPSHOTS):
            assert raw == blob(ref, path), (ref, path)
        assert source_readback[label] == record | {'current_sha256': sha(raw), 'reviewed_blob_equal': True}

    result = {
        'pr': {'number': 132, 'url': f'{URL}/pull/132', 'base_branch': 'research/uqcf-overlapping-guard-exchange',
               'base_sha': BASE, 'head_sha': HEAD, 'merge_sha': MERGE, 'merge_parents': parent_line,
               'merged_by': 'proteinfolding-grokbot', 'merged_at_utc': '2026-11-12T16:55:54Z',
               'integrated_research_sha': INTEGRATED},
        'scope': {
            'status': 'ACCEPTED_CONDITIONAL_ANALYTICAL_RESULT',
            'theorem': 'Under the supplied finite-dimensional channel benchmark, if a realizing unitary leaves R pure on rho_*, then 2 rank(tau_E) <= d_E. New full-rank TB forces R mixed on rho_* for every realizing unitary.',
            'scope_control': 'With the benchmark equal-dimensional E and R, a receiver-writing realization followed by SWAP moves the source record to E and gives R the source-independent bath state tau_E. R mixedness alone establishes no delivery, location, ownership, access, event/state/record correspondence, or probability law.',
            'entropy_companion': 'In bits, S(R) >= 1 + S(tau_E) - log2(d_E); the bound can be nonpositive. The strict mixedness conclusion uses rank.',
            'native_bridge_status': 'NOT_DERIVED',
            'numbered_stage_certification': False,
            'required_correction': None,
            'related_prs': {'130': 'open and unmerged', '131': 'open and unmerged'},
        },
        'review': identity | {
            'job_id': 125548408532, 'actions_url': f'{URL}/actions/runs/41524434282',
            'response_id': response['responseId'], 'finish_reason': candidate['finishReason'],
            'model_metadata_version': metadata['version'],
            'verdict': verdict['verdict'], 'native_bridge_status': verdict['native_bridge_status'],
            'findings': verdict['findings'], 'missing_assumptions': verdict['missing_assumptions'],
            'counterexamples': verdict['counterexamples'], 'limitations': verdict['limitations'],
            'verdict_path': str(evidence_paths['review'] / 'verdict.json'),
            'raw_response_path': str(evidence_paths['review'] / 'response.json'),
        },
        'publication': published | {
            'run_id': 41525059170, 'run_attempt': 1, 'workflow_sha': CONTROLLER,
            'verification_job_id': 125550559083, 'publication_job_id': 125551617013,
            'actions_url': f'{URL}/actions/runs/41525059170',
            'verified_deterministic_replay_files': ['review-gate.json', 'source-readback.json'],
        },
        'evidence': {
            'argument_path': str(ROOT / 'ARGUMENT.md'), 'adjudication_path': str(ROOT / 'ADJUDICATION.md'),
            'review_receipt_path': str(ROOT / 'REVIEW_ARTIFACT_RECEIPT.json'),
            'audit_receipt_path': str(ROOT / 'AUDIT_ARTIFACT_RECEIPT.json'),
            'archives': {kind: {'artifact_id': artifact[0], 'zip_sha256': artifact[1],
                                'git_path': str(evidence_paths[kind]), 'entry_count': len(evidence[kind]),
                                'verified_against': list(SNAPSHOTS)}
                         for kind, artifact in live_archives.items()},
            'source_documents': docs,
            'source_documents_verified_against': [REVIEWED, CONTROLLER, *SNAPSHOTS],
            'actions_log_checks': {'gemini_review': 'ACCEPTED / NOT_DERIVED at reviewed SHA',
                                   'verification': 'readback executed at controller SHA',
                                   'publication': 'verification ZIP digest matched on download; fresh replay executed at controller SHA'},
        },
        'evidence_limits': [
            'This is a scoped analytical review and publication replay. Neither T-273 workflow ran a numbered-stage preregistration, independent exhaustive enumeration with rejecting controls, or the inherited foundational stack.',
            'The current post-merge audit independently checked saved archive bytes, review inputs/outputs, manifests, and deterministic replay equality. It made no new model calls and ran no new numerical campaign.',
            'Review obligations for the numbered retained-stage pipeline, and separate remediation of PRs 130 and 131, cannot be satisfied by these receipts.',
        ],
    }
    (LOCAL / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n')
    print(f'Verified {sum(map(len, evidence.values()))} archive entries, {len(docs)} bound review documents, raw verdict, and 2 deterministic replay files.')


if __name__ == '__main__':
    main()
