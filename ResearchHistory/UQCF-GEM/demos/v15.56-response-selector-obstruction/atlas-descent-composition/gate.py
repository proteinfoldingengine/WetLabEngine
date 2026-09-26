"""v15.70: strict marginal descent versus fixed-base source composition.

Source parameters label ordered repairs; no fundamental time is introduced.
Historical measurements are imported unchanged and never rewritten.
"""
import importlib.util
import itertools
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
SPEC = importlib.util.spec_from_file_location(
    'v64_atlas', PARENT / 'source-vector-field-null' / 'gate.py')
V64 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V64)
GL = V64.GL
EXPECTED = [13, 16, 22, 25, 27, 29, 37, 39, 46, 50, 66, 77]
EDGES = [(0, 1), (1, 2), (2, 0)]
ETA, S, U = 1e-4, 1e-3, -3e-4
LABELS = list(itertools.product(range(1, 4), repeat=3))
HIDDEN = [V64.ASYM.F.op(*ids)/np.sqrt(8) for ids in LABELS]


def restrict(matrix, keep):
    """Partial trace in explicitly ordered qubit coordinates, preserving complex data."""
    a = np.asarray(matrix)
    n = a.shape[0].bit_length()-1
    if a.shape != (2**n, 2**n) or len(set(keep)) != len(keep):
        raise ValueError('invalid matrix or duplicate retained index')
    if any(q < 0 or q >= n for q in keep):
        raise ValueError('invalid retained index')
    rest = tuple(q for q in range(n) if q not in keep)
    order = tuple(keep)+rest+tuple(q+n for q in keep)+tuple(q+n for q in rest)
    dk, dt = 2**len(keep), 2**len(rest)
    blocks = a.reshape((2,)*(2*n)).transpose(order).reshape(dk, dt, dk, dt)
    return np.einsum('aibi->ab', blocks)


def source_step(sigma, rho, h, y, strength):
    alpha = float(np.trace(h@(sigma-rho)).real / np.trace(h@h).real)
    return sigma+strength*alpha*y


def commutator_norm(a, b):
    return float(np.linalg.norm(a@b-b@a))


def adjudicate(valid, gaps):
    if not valid or not gaps or not np.isfinite(gaps).all():
        return 'INVALID'
    return ('ATLAS_NATURAL_NULL_OBSTRUCTED' if max(gaps) > 1e-10
            else 'ATLAS_NATURAL_NULL_CONFIRMED')


def coeffs(a):
    return np.array([np.trace(b@a).real for b in GL.BASIS])


def state_metrics(states):
    return {
        'min_eigenvalue': float(min(np.linalg.eigvalsh(z).min() for z in states)),
        'trace_error': float(max(abs(np.trace(z)-1) for z in states)),
        'hermiticity_error': float(max(np.linalg.norm(z-z.conj().T) for z in states)),
    }


def measure_state(row):
    rho = row['rho']
    y, lift_residual = V64.target_Y(rho)
    yc = coeffs(y)
    a1, ap = GL.derivative_maps(rho)
    o = GL.rotations(rho)
    reduced = [restrict(y, e) for e in EDGES]
    overlaps = []
    target_errors, skew_errors = [], []
    for k, e in enumerate(EDGES):
        d = (ap[9*k:9*(k+1)]@yc).reshape(3, 3)
        target_errors.append(float(np.linalg.norm(d-o[k]/np.sqrt(3))))
        skew_errors.append(float(np.linalg.norm(o[k].T@d-d.T@o[k])/np.linalg.norm(d)))
        for local, global_q in enumerate(e):
            nested = restrict(reduced[k], (local,))
            direct = restrict(y, (global_q,))
            overlaps.extend([float(np.linalg.norm(nested)), float(np.linalg.norm(nested-direct))])

    # Positive polar-skew control: one edge, same global lift machinery.
    k = np.zeros((3, 3)); k[0, 1] = 1/np.sqrt(2); k[1, 0] = -1/np.sqrt(2)
    b = np.concatenate([np.zeros(9), (o[0]@k).ravel(), np.zeros(18)])
    a = np.vstack([a1, ap])
    positive_coeffs = np.linalg.lstsq(a, b, rcond=None)[0]
    positive_reconstruction = float(np.linalg.norm(a@positive_coeffs-b))
    dpos = (ap[:9]@positive_coeffs).reshape(3, 3)
    skew_control = float(np.linalg.norm(o[0].T@dpos-dpos.T@o[0]))

    witnesses = []
    finite = [rho]
    for label, h in zip(LABELS, HIDDEN):
        plus, minus = rho+ETA*h, rho-ETA*h
        outplus = source_step(plus, rho, h, y, S)
        outminus = source_step(minus, rho, h, y, S)
        finite.extend([plus, minus, outplus, outminus])
        for ei, edge in enumerate(EDGES):
            inp = restrict(plus, edge)-restrict(minus, edge)
            actual = restrict(outplus, edge)-restrict(outminus, edge)
            prediction = 2*ETA*S*reduced[ei]
            witnesses.append({
                'hidden_label': list(label), 'edge': list(edge),
                'hidden_marginal_norm': float(np.linalg.norm(restrict(h, edge))),
                'input_gap': float(np.linalg.norm(inp)),
                'identity_control_gap': float(np.linalg.norm(inp)),
                'derivative_gap': float(np.linalg.norm(reduced[ei])),
                'output_gap': float(np.linalg.norm(actual)),
                'fiber_identity_relative_error': float(np.linalg.norm(actual-prediction)/max(np.linalg.norm(prediction), 1e-300)),
            })

    # Full tangent-space operator products. No restriction to probe span here.
    hc = [coeffs(h) for h in HIDDEN]
    operators = [np.outer(yc, c)/np.dot(c, c) for c in hc]
    max_product = max(float(np.linalg.norm(na@nb)) for na in operators for nb in operators)
    max_commutator = max(commutator_norm(na, nb) for na in operators for nb in operators)
    h1, h2 = HIDDEN[0], HIDDEN[LABELS.index((2, 2, 2))]
    n = operators[0]
    reverse = np.outer(hc[0], yc)/np.dot(yc, yc)
    commutator_control = commutator_norm(n, reverse)
    sig = rho+ETA*(h1+h2)
    first = source_step(sig, rho, h1, y, S)
    second = source_step(sig, rho, h2, y, U)
    seq = source_step(first, rho, h2, y, U)
    rev = source_step(second, rho, h1, y, S)
    combined = sig+(first-sig)+(second-sig)
    same_seq = source_step(first, rho, h1, y, U)
    same_combined = source_step(sig, rho, h1, y, S+U)
    finite.extend([sig, first, second, seq, rev, combined, same_seq, same_combined])
    finite_order = float(np.linalg.norm(seq-rev))
    finite_combined = float(np.linalg.norm(seq-combined))
    finite_additive = float(np.linalg.norm(same_seq-same_combined))
    # Direct finite polar checks without small-step divisions.
    rotation_change = 0.
    positive_min = float('inf')
    for z in [first, second, seq, rev, combined, same_seq, same_combined]:
        oz = GL.rotations(z)
        for ei, edge in enumerate(EDGES):
            rotation_change = max(rotation_change, float(np.linalg.norm(oz[ei]-o[ei])))
            c = V64.ASYM.F.corr(z, *edge)
            p = o[ei].T@c
            positive_min = min(positive_min, float(np.linalg.eigvalsh((p+p.T)/2).min()))

    sm = state_metrics(finite)
    diag = V64.ASYM.diagnostics(rho)
    checks = {
        'base_state': diag['min_eigenvalue'] >= .025-1e-12,
        'regular_polar': diag['min_edge_singular'] >= .020-1e-12 and diag['min_positive_polar_eigenvalue'] > 0,
        'lift': lift_residual <= 1e-10,
        'nonzero_target': np.linalg.norm(y) > 1e-6,
        'target_reconstruction': max(target_errors) <= 1e-10,
        'symmetric_null': max(skew_errors) <= 1e-10,
        'one_body': np.linalg.norm(a1@yc) <= 1e-12,
        'overlap': max(overlaps) <= 1e-12,
        'finite_positive': sm['min_eigenvalue'] >= -1e-12,
        'finite_normalized': sm['trace_error'] <= 1e-12,
        'finite_hermitian': sm['hermiticity_error'] <= 1e-12,
        'fiber_inputs': all(z['hidden_marginal_norm'] <= 1e-12 and z['input_gap'] <= 1e-12 for z in witnesses),
        'fiber_prediction': all(z['fiber_identity_relative_error'] <= 1e-8 for z in witnesses),
        'identity_control': all(z['identity_control_gap'] <= 1e-12 for z in witnesses),
        'skew_control': skew_control > 1 and positive_reconstruction <= 1e-10,
        'commutator_control': commutator_control > 1,
    }
    composition_confirmed = (max_product <= 1e-12 and max_commutator <= 1e-12
        and max(finite_order, finite_combined, finite_additive) <= 1e-12
        and rotation_change <= 1e-10 and positive_min > 0)
    result = {
        'candidate_index': row['candidate_index'],
        'Y_norm': float(np.linalg.norm(y)),
        'lift_relative_residual': lift_residual,
        'max_target_error': max(target_errors),
        'max_skew_relative_error': max(skew_errors),
        'max_overlap_error': max(overlaps),
        'one_body_norm': float(np.linalg.norm(a1@yc)),
        'hidden_lift_pairing_max': float(max(abs(np.dot(c, yc)) for c in hc)),
        'skew_control': skew_control,
        'skew_control_reconstruction': positive_reconstruction,
        'commutator_control': commutator_control,
        'base_diagnostics': diag, 'finite_states': sm,
        'descent_witnesses': witnesses,
        'composition': {
            'n_operator_pairs': len(operators)**2,
            'max_product_norm': max_product, 'max_commutator_norm': max_commutator,
            'finite_order_residual': finite_order, 'finite_combined_residual': finite_combined,
            'finite_additive_residual': finite_additive,
            'max_rotation_change': rotation_change, 'min_positive_polar_eigenvalue': positive_min,
            'confirmed': bool(composition_confirmed),
        },
    }
    def numeric_values(obj):
        if isinstance(obj, dict):
            for value in obj.values(): yield from numeric_values(value)
        elif isinstance(obj, list):
            for value in obj: yield from numeric_values(value)
        elif isinstance(obj, (int, float, np.number)): yield obj
    checks['all_finite'] = bool(np.isfinite(list(numeric_values(result))).all())
    result['checks'] = {key: bool(value) for key, value in checks.items()}
    result['valid'] = bool(all(checks.values()))
    return result


def run_measurement():
    rows = []
    try:
        states = V64.ASYM.select_states()
        indices = [z['candidate_index'] for z in states]
        if indices != EXPECTED:
            return {'verdict': 'INVALID', 'all_valid': False, 'candidate_indices': indices, 'rows': [], 'error': 'state identity mismatch'}
        rows = [measure_state(row) for row in states]
        gaps = [z['derivative_gap'] for row in rows for z in row['descent_witnesses']]
        valid = len(rows) == 12 and len(gaps) == 972 and all(row['valid'] for row in rows)
        composition = all(row['composition']['confirmed'] for row in rows)
        return {
            'verdict': adjudicate(valid, gaps), 'all_valid': bool(valid),
            'composition_verdict': ('INVALID' if not valid else
                'FIXED_BASE_NULL_COMPOSITION_CONFIRMED' if composition else
                'FIXED_BASE_NULL_COMPOSITION_NOT_CONFIRMED'),
            'candidate_indices': indices, 'n_descent_witnesses': len(gaps),
            'n_operator_pairs': sum(row['composition']['n_operator_pairs'] for row in rows),
            'seed': 20260928, 'eta': ETA, 'source_amplitudes': [S, U],
            'numpy_version': np.__version__, 'python_version': sys.version,
            'rows': rows,
        }
    except Exception as exc:
        return {'verdict': 'INVALID', 'all_valid': False, 'error': repr(exc), 'rows': rows}


def finalize_report(report):
    """Keep INVALID evidence serializable without representing NaN as a result."""
    nonfinite = []

    def clean(value, path):
        if isinstance(value, dict):
            return {key: clean(item, path+'.'+key) for key, item in value.items()}
        if isinstance(value, list):
            return [clean(item, path+'['+str(i)+']') for i, item in enumerate(value)]
        if isinstance(value, float) and not np.isfinite(value):
            nonfinite.append(path)
            return None
        return value

    result = clean(report, 'report')
    if nonfinite:
        result.update(verdict='INVALID', all_valid=False, composition_verdict='INVALID',
                      nonfinite_diagnostic_paths=nonfinite,
                      serialization_error='nonfinite diagnostics replaced by null')
    return result


if __name__ == '__main__':
    report = finalize_report(run_measurement())
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    raise SystemExit(2 if report['verdict'] == 'INVALID' else 0)
