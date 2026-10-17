"""Comparator: declared universe of RECONSTRUCTION_CONTRACT.md, producer vs independent checker,
analytic controls K3-K7/ORTH and rejecting controls W1-W4. Writes relref_reconstruction/."""
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import uqcf_relref_formula as producer  # noqa: E402
import uqcf_relref_checker as checker  # noqa: E402

TOL = 1e-8
STRUCTURES = [(2,), (3,), (1, 2), (2, 2), (1, 3), (2, 3), (1, 1, 2)]
COUNTS = {'B-in': 8, 'B-out': 4, 'COR': 4, 'A-a-mixed': 4, 'A-a-central': 2, 'A-b': 4, 'A-c': 4}
OUT = Path('relref_reconstruction')


def slices(dims):
    out, s = [], 0
    for n in dims:
        out.append(slice(s, s + n)); s += n
    return out


def ginibre(rng, n):
    g = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    m = g @ g.conj().T
    return m / np.trace(m).real


def random_in_A(rng, dims):
    n = sum(dims)
    w = rng.dirichlet(np.ones(len(dims)))
    rho = np.zeros((n, n), dtype=complex)
    for wi, s in zip(w, slices(dims)):
        rho[s, s] = wi * ginibre(rng, s.stop - s.start)
    return rho


def central_blind_partner(rng, dims, rho0):
    n = sum(dims)
    rho1 = np.zeros((n, n), dtype=complex)
    for s in slices(dims):
        rho1[s, s] = np.trace(rho0[s, s]).real * ginibre(rng, s.stop - s.start)
    return rho1


def haar_in_A(rng, dims):
    n = sum(dims)
    u = np.zeros((n, n), dtype=complex)
    for s in slices(dims):
        b = s.stop - s.start
        z = (rng.normal(size=(b, b)) + 1j * rng.normal(size=(b, b))) / np.sqrt(2)
        q, r = np.linalg.qr(z)
        u[s, s] = q * (np.diag(r) / np.abs(np.diag(r)))
    return u


def central_state(rng, dims):
    n = sum(dims)
    c = rng.dirichlet(np.ones(len(dims)))
    w = np.zeros((n, n), dtype=complex)
    for ci, s in zip(c, slices(dims)):
        w[s, s] = ci * np.eye(s.stop - s.start) / (s.stop - s.start)
    return w


def r(x):
    return float(round(x, 10))


def build():
    records, comm_cache = [], {}

    def comm(dims, labels):
        key = (dims, labels)
        if key not in comm_cache:
            comm_cache[key] = checker.commutant(list(dims), list(labels))
        return comm_cache[key]

    diag = []
    for k, dims in enumerate(STRUCTURES):
        rng = np.random.default_rng(20261016 + k)
        n = sum(dims)
        basis_id, gens_id, info_id = comm(dims, (0, 0))
        diag.append({'structure': list(dims), 'checker_dimension': info_id['dimension'],
                     'producer_prediction': producer.predicted_commutant_dim(list(dims)),
                     'smallest_nonzero_singular_value': info_id['smallest_nonzero_singular_value'],
                     'largest_null_singular_value': info_id['largest_null_singular_value']})
        for fam in ('B-in', 'B-out'):
            for j in range(COUNTS[fam]):
                rho0 = random_in_A(rng, dims); rho1 = central_blind_partner(rng, dims, rho0)
                sigma = random_in_A(rng, dims) if fam == 'B-in' else ginibre(rng, n)
                d = np.kron(rho1 - rho0, sigma)
                tc = checker.optimum(basis_id, d)
                tf = producer.t_formula(list(dims), rho0, rho1, sigma)
                e = producer.reader(list(dims), rho0, rho1, sigma)
                ef = producer.reader(list(dims), rho0, rho1, sigma, flip=True)
                records.append({'key': f'{dims}/{fam}/{j}', 'family': fam, 'T_check': r(tc), 'T_formula': r(tf),
                                'reader_invariant': checker.commutes(e, gens_id), 'reader_value': r(checker.value(e, d)),
                                'W1_wrong_formula': r(producer.t_wrong_no_block_abs(list(dims), rho0, rho1, sigma)),
                                'W2_flipped_value': r(checker.value(ef, d))})
        for j in range(COUNTS['COR']):
            rho0 = random_in_A(rng, dims); u = haar_in_A(rng, dims); rho1 = u @ rho0 @ u.conj().T
            d = np.kron(rho1 - rho0, rho0)
            records.append({'key': f'{dims}/COR/{j}', 'family': 'COR', 'T_check': r(checker.optimum(basis_id, d)),
                            'T_formula': r(producer.corollary_value(rho0, rho1))})
        for fam in ('A-a-mixed', 'A-a-central'):
            for j in range(COUNTS[fam]):
                rho0 = random_in_A(rng, dims); rho1 = central_blind_partner(rng, dims, rho0)
                omega = np.eye(n) / n if fam == 'A-a-mixed' else central_state(rng, dims)
                records.append({'key': f'{dims}/{fam}/{j}', 'family': fam,
                                'T_check': r(checker.optimum(basis_id, np.kron(rho1 - rho0, omega))), 'T_formula': 0.0})
        basis_un, _, _ = comm(dims, (0, 1))
        for j in range(COUNTS['A-b']):
            rho0 = random_in_A(rng, dims); rho1 = central_blind_partner(rng, dims, rho0); omega = ginibre(rng, n)
            records.append({'key': f'{dims}/A-b/{j}', 'family': 'A-b',
                            'T_check': r(checker.optimum(basis_un, np.kron(rho1 - rho0, omega))), 'T_formula': 0.0})
        for j in range(COUNTS['A-c']):
            rho0 = random_in_A(rng, dims); u = haar_in_A(rng, dims); rho1 = u @ rho0 @ u.conj().T
            d = np.kron(rho1, rho1) - np.kron(rho0, rho0)
            records.append({'key': f'{dims}/A-c/{j}', 'family': 'A-c', 'T_check': r(checker.optimum(basis_id, d)), 'T_formula': 0.0})
    # analytic controls on a qubit
    q0 = np.diag([0, 1]).astype(complex); q1 = np.diag([1, 0]).astype(complex)
    plus = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)
    had = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    b2, g2, _ = comm((2,), (0, 0))
    def ctl(key, d, expected, label='CONTROL'):
        records.append({'key': key, 'family': label, 'T_check': r(checker.optimum(b2, d)), 'T_formula': expected})
    ctl('K3', np.kron(q1 - q0, plus), 0.0)
    ctl('K4', np.kron(q1, q1) - np.kron(np.eye(2) / 2, np.eye(2) / 2), 0.25)
    ctl('K5-aligned', np.kron(q1 - q0, q1), 0.5)
    ctl('K5-twisted', np.kron(q1 - q0, had @ q1 @ had.conj().T), 0.0)
    ctl('K6-answer-bearing', np.kron(q1 - q0, q1), 0.5, 'NOT_A_CONSEQUENCE')
    ctl('ORTH', np.kron(q0 - q1, q1), 0.5)
    # K7: reweight the one-dimensional block of sigma on structure (1,2)
    rng = np.random.default_rng(20261016 + 99)
    dims = (1, 2); bk, _, _ = comm(dims, (0, 0))
    rho0 = random_in_A(rng, dims); rho1 = central_blind_partner(rng, dims, rho0); sigma = random_in_A(rng, dims)
    w = sigma[0, 0].real; s2 = sigma.copy(); s2[0, 0] = 0.9; s2[1:, 1:] *= (0.1 / (1 - w))
    t1 = checker.optimum(bk, np.kron(rho1 - rho0, sigma)); t2 = checker.optimum(bk, np.kron(rho1 - rho0, s2))
    records.append({'key': 'K7', 'family': 'CONTROL', 'T_check': r(t2), 'T_formula': r(t1 * 0.1 / (1 - w))})
    w3 = np.kron(q1, q1)
    return records, diag, {'W3_noninvariant_rejected': not checker.commutes(w3, g2)}


def declared_keys():
    keys = []
    for dims in STRUCTURES:
        for fam in ('B-in', 'B-out', 'COR', 'A-a-mixed', 'A-a-central', 'A-b', 'A-c'):
            keys += [f'{dims}/{fam}/{j}' for j in range(COUNTS[fam])]
    return keys + ['K3', 'K4', 'K5-aligned', 'K5-twisted', 'K6-answer-bearing', 'ORTH', 'K7']


def validate(records):
    """Return list of failures; empty iff the certificate satisfies the preregistered requirements."""
    fails = []
    keys = [x['key'] for x in records]
    if len(keys) != len(set(keys)):
        fails.append('duplicate record')
    if set(keys) != set(declared_keys()):
        fails.append('universe membership mismatch')
    for x in records:
        if abs(x['T_check'] - x['T_formula']) > TOL:
            fails.append('value mismatch ' + x['key'])
        if x['family'] in ('B-in', 'B-out'):
            if not x['reader_invariant'] or abs(x['reader_value'] - x['T_formula']) > TOL:
                fails.append('reader fails ' + x['key'])
        if x['family'] == 'COR' and x['T_check'] <= TOL:
            fails.append('corollary not positive ' + x['key'])
    return fails


def main():
    OUT.mkdir(exist_ok=True)
    records, diag, extra = build()
    fails = validate(records)
    bin_ = [x for x in records if x['family'] == 'B-in']
    w1 = any(abs(x['W1_wrong_formula'] - x['T_check']) > TOL for x in bin_)
    w2 = all(abs(x['W2_flipped_value'] - x['T_check']) > TOL for x in bin_ if x['T_check'] > 1e-6)
    tamper = {}
    t = json.loads(json.dumps(records)); t[0]['T_check'] += 1e-3; tamper['perturbed_value'] = bool(validate(t))
    t = json.loads(json.dumps(records)); del t[5]; tamper['deleted_record'] = bool(validate(t))
    t = json.loads(json.dumps(records)); t.append(dict(t[3])); tamper['duplicated_record'] = bool(validate(t))
    t = json.loads(json.dumps(records)); t[7]['key'] = 'substituted'; tamper['substituted_key'] = bool(validate(t))
    rejecting = {'W1_wrong_formula_detected': w1, 'W2_flipped_reader_detected': w2,
                 'W3_noninvariant_rejected': extra['W3_noninvariant_rejected'], 'W4_tamper_detected': tamper}
    green = not fails and w1 and w2 and extra['W3_noninvariant_rejected'] and all(tamper.values())
    cert = {'status': 'GREEN' if green else 'RED', 'tolerance': TOL, 'record_count': len(records),
            'declared_count': len(declared_keys()), 'failures': fails, 'rejecting_controls': rejecting,
            'commutant_dimension_diagnostic': diag, 'records': records, 'numpy': np.__version__,
            'scope': 'bounded finite-dimensional reconstruction of ADMISSION.md section 2 and controls; not a proof, not a native mechanism'}
    data = (json.dumps(cert, sort_keys=True, indent=1) + '\n').encode()
    (OUT / 'certificate.json').write_bytes(data)
    (OUT / 'provenance.json').write_text(json.dumps({k: os.environ.get(v) for k, v in {
        'scientific_sha': 'GITHUB_SHA', 'workflow_sha': 'UQCF_WORKFLOW_SHA', 'run_id': 'GITHUB_RUN_ID',
        'run_attempt': 'GITHUB_RUN_ATTEMPT'}.items()}, sort_keys=True, indent=2) + '\n')
    lines = ['status %s records %d failures %d certificate_sha256 %s' % (cert['status'], len(records), len(fails), hashlib.sha256(data).hexdigest()),
             json.dumps(rejecting, sort_keys=True), json.dumps(diag, sort_keys=True)] + fails
    (OUT / 'reconstruction.log').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    manifest = {q.name: {'bytes': q.stat().st_size, 'sha256': hashlib.sha256(q.read_bytes()).hexdigest()}
                for q in sorted(OUT.iterdir()) if q.is_file() and q.name != 'file_manifest.json'}
    (OUT / 'file_manifest.json').write_text(json.dumps(manifest, sort_keys=True, indent=2) + '\n')
    if not green:
        raise SystemExit('RED: reconstruction or rejecting controls failed; certificate retained.')


if __name__ == '__main__':
    main()
