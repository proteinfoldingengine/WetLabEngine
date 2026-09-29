"""Verify and durably publish the complete, pinned v16.15 Actions evidence.

No scientific source or result is altered. The original ZIP and JSON bytes are
hash-bound; a fresh reproduction may differ ONLY in its execution_head.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import io
import json
import lzma
import os
import subprocess
import zipfile

SOURCE_SHA = '9934cb1f05795694febf1f35b07580dc5c864e31'
ARCHIVE_SHA256 = '39256371aa5a0e1e17200e66b51cf1b1a18c7b0837d017776fcac7ee0297f74b'
RESULT_SHA256 = 'fd271a45a90bcb54bce30804d5321aa129914f62b6fc6563a1c3fd4d96e66ffc'
PREFIX = 'ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/network-interpretation/'
COUNTS = {'exact': 144, 'local_scalars': 1728, 'pairs': 72, 'independent_loop_checks': 504}
CANDIDATES = {13, 16, 22, 25, 27, 29, 37, 39, 46, 50, 66, 77}
AS = {1.0, 1/3, 1/6}
ARMS = {'plane', 'isotropic'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def key(row):
    return row['candidate'], row['a'], row['arm']

def summarize(result):
    require(result.get('version') == '16.15' and result.get('all_valid') is True,
            'invalid result version or validity')
    require(result.get('verdict') == 'NETWORK_NORMAL_COUPLING_CLASSIFIED', 'invalid verdict')
    for name, count in COUNTS.items():
        require(len(result[name]) == count, 'incomplete ' + name)
    expected = {(c, a, arm) for c in CANDIDATES for a in AS for arm in ARMS}
    require({key(x) for x in result['pairs']} == expected, 'pair identity coverage')
    require({key(x) + (x['order'],) for x in result['exact']} ==
            {k + (order,) for k in expected for order in ('after', 'before')}, 'path identity coverage')
    require({key(x) + (x['cycle'],) for x in result['independent_loop_checks']} ==
            {k + (cycle,) for k in expected for cycle in range(7)}, 'loop identity coverage')
    require({key(x) + (x['edge'], x['observable']) for x in result['local_scalars']} ==
            {k + (edge, obs) for k in expected for edge in range(6)
             for obs in ('gram1', 'gram2', 'gram3', 'determinant')}, 'local identity coverage')
    for row in result['exact']:
        require(0 <= row['normal_reference_rank'] <= row['normal_dimension'], 'rank bound')
        require(all(F(x) == 0 for x in row['normal_local_scalar_derivatives'][:3]), 'normal Gram blindness')
        b = row['projected_bounds']
        require(b['valid'] is True, 'invalid projected bounds')
        require(all(len(b[n]) == 7 for n in ('reference_norm_squared', 'bound_squared', 'response_squared')), 'bound coverage')
        for h, bound, response, value in zip(b['reference_norm_squared'], b['bound_squared'],
                                            b['response_squared'], row['normal_responses']):
            require(F(h) >= 0 and F(bound) == F(h)*F(row['normal_norm_squared']), 'bound value')
            require(F(response) == F(value)**2 and F(response) <= F(bound), 'exact bound inequality')
    for row in result['local_scalars']:
        contrast = [F(a)-F(b) for a, b in zip(row['after'], row['before'])]
        require(contrast == list(map(F, row['contrast'])), 'local contrast arithmetic')
        require(row['nonzero'] == any(contrast), 'local contrast flag')
    for row in result['pairs']:
        local = [x for x in result['local_scalars'] if key(x) == key(row)]
        loops = [x for x in result['independent_loop_checks'] if key(x) == key(row)]
        flags = {
            'local_scalar_distinguishes': any(x['nonzero'] for x in local),
            'local_odd_coefficient_nonzero': any(F(x['contrast'][1]) != 0 for x in local),
            'local_zero_coherence_nonzero': any(F(x['contrast'][0]) != 0 for x in local),
            'network_distinguishes': any(any(map(F, x['total'])) for x in loops),
            'network_normal_contribution': any(any(map(F, x['normal'])) for x in loops),
            'normal_amplitude_distinguishes': F(row['normal_energy_contrast']) != 0,
        }
        flags['first_order_network_beyond_chosen_local_scalars'] = flags['network_distinguishes'] and not flags['local_scalar_distinguishes']
        require(all(row[name] == value for name, value in flags.items()), 'pair classification consistency')
        if row['a'] == 1.0:
            require(not any(flags.values()), 'identity-middle null')
    return {
        'version': '16.15', 'verdict': result['verdict'], 'records': dict(COUNTS),
        'classifications': dict(Counter(x['classification'] for x in result['exact'])),
        'reference_ranks': dict(sorted(Counter(str(x['normal_reference_rank']) for x in result['exact']).items())),
        'normal_dimensions': dict(sorted(Counter(str(x['normal_dimension']) for x in result['exact']).items())),
        'normal_kernel_dimensions': dict(sorted(Counter(str(x['normal_dimension']-x['normal_reference_rank']) for x in result['exact']).items())),
        'pair_flags': {name: sum(x[name] for x in result['pairs']) for name in result['pairs'][0] if isinstance(result['pairs'][0][name], bool)},
        'pair_claims': dict(Counter(x['claim'] for x in result['pairs'])),
        'network_beyond_chosen_local_scalars': sum(x['first_order_network_beyond_chosen_local_scalars'] for x in result['pairs']),
        'local_nonzero_by_observable': {name: sum(x['nonzero'] for x in result['local_scalars'] if x['observable'] == name) for name in ('gram1', 'gram2', 'gram3', 'determinant')},
        'normal_determinant_nonzero_paths': sum(F(x['normal_local_scalar_derivatives'][3]) != 0 for x in result['exact']),
        'normal_nonzero_path_cycles': sum(F(v) != 0 for x in result['exact'] for v in x['normal_responses']),
        'total_nonzero_pair_cycles': sum(any(map(F, x['total'])) for x in result['independent_loop_checks']),
        'normal_nonzero_pair_cycles': sum(any(map(F, x['normal'])) for x in result['independent_loop_checks']),
        'zero_coherence_total_nonzero_pair_cycles': sum(F(x['total'][0]) != 0 for x in result['independent_loop_checks']),
        'projected_squared_inequalities_checked': 144*7,
    }

def verify_archive(raw):
    require(digest(raw) == ARCHIVE_SHA256, 'original artifact ZIP hash mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        require(archive.testzip() is None, 'ZIP CRC mismatch')
        members = {name: archive.read(name) for name in archive.namelist()}
    require(len(members) == 9, 'original artifact member count')
    require(members['execution_head.txt'].decode().strip() == SOURCE_SHA, 'execution head mismatch')
    data = members[PREFIX + 'result.json']
    require(digest(data) == RESULT_SHA256, 'result JSON hash mismatch')
    result = json.loads(data)
    require(result['execution_head'] == SOURCE_SHA, 'embedded execution head mismatch')
    return members, result, summarize(result)

def compare_reproduction(original, fresh):
    require({k: v for k, v in original.items() if k != 'execution_head'} ==
            {k: v for k, v in fresh.items() if k != 'execution_head'},
            'fresh scientific output differs from original')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', action='store_true')
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    members, result, summary = verify_archive((here/'evidence/original-actions-artifact.zip').read_bytes())
    if args.stage:
        fresh = json.loads((here/'result.json').read_text())
        compare_reproduction(result, fresh)
        source_hashes = {}
        for line in members[PREFIX+'SHA256SUMS'].decode().splitlines():
            expected, name = line.split()
            data = members[PREFIX+name] if name == 'result.json' else (here/name).read_bytes()
            require(digest(data) == expected, 'scientific source hash mismatch: '+name)
            source_hashes[name] = expected
        evidence = here/'evidence'
        evidence.mkdir(exist_ok=True)
        for name, data in members.items():
            target = evidence/Path(name).name
            if target.name != 'result.json':
                target.write_bytes(data)
        raw = members[PREFIX+'result.json']
        (here/'result.json.xz').write_bytes(lzma.compress(raw))
        require(lzma.decompress((here/'result.json.xz').read_bytes()) == raw, 'XZ round trip')
        (here/'SUMMARY.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
        receipt = {
            'version': '16.15', 'scientific_execution_head': SOURCE_SHA,
            'original_run_id': 36504243196, 'original_job_id': 109201934269,
            'original_artifact_id': 11006352186, 'original_artifact_sha256': ARCHIVE_SHA256,
            'original_artifact_bytes': 1058147, 'original_artifact_members': 9,
            'raw_result_sha256': RESULT_SHA256, 'raw_result_bytes': len(raw),
            'result_xz_sha256': digest((here/'result.json.xz').read_bytes()),
            'result_xz_bytes': (here/'result.json.xz').stat().st_size,
            'scientific_sha256sums': source_hashes,
            'reproduction_execution_head': fresh['execution_head'],
            'reproduction_run_id': os.environ.get('GITHUB_RUN_ID'),
            'reproduction_exact_scientific_equality': True,
            'parent_binding': json.loads((here/'PARENT_BINDING.json').read_text()),
            'checks': ['original ZIP SHA256 and all CRCs', 'embedded source SHA', 'all six scientific SHA256SUMS',
                       'complete record identity sets', '1008 exact projected bounds', '1728 local contrast arithmetic checks',
                       '72 pair classification reconciliations', 'all scientific JSON fields reproduced exactly; only execution_head excluded',
                       'lossless XZ round trip'],
            'publication_scope': 'research/v16.15-network-interpretation; not merged to main',
        }
        (here/'EVIDENCE.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
        names = ['result.json.xz', 'SUMMARY.json', 'EVIDENCE.json', 'RESULTS.md',
                 'publish_evidence.py', 'publication_tests.py',
                 'PREREGISTRATION.md', 'SOURCE_MANIFEST.json', 'PARENT_BINDING.json',
                 'DERIVATION.md', 'REVIEW.md', 'gate.py', 'test_gate.py']
        names += [str(p.relative_to(here)) for p in sorted(evidence.iterdir()) if p.is_file()]
        (here/'PUBLICATION_SHA256SUMS').write_text(''.join(digest((here/n).read_bytes())+'  '+n+'\n' for n in names))
    if args.verify:
        for line in (here/'PUBLICATION_SHA256SUMS').read_text().splitlines():
            expected, name = line.split()
            require(digest((here/name).read_bytes()) == expected, 'publication hash mismatch: '+name)
        require(lzma.decompress((here/'result.json.xz').read_bytes()) == members[PREFIX+'result.json'], 'published raw data mismatch')
        require(json.loads((here/'SUMMARY.json').read_text()) == summary, 'published summary mismatch')
    print(json.dumps({'all_valid': True, 'archive_sha256': ARCHIVE_SHA256, 'summary': summary}, sort_keys=True))

if __name__ == '__main__':
    main()
