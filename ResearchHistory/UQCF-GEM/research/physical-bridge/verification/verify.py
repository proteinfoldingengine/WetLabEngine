"""Run the prospectively frozen A12 bounded corroboration, not a universal proof.

Python 3.11, standard library only. No scientific network access or engine imports.
All identities are enumerated; reference and certificate routes are separate.
Outputs contain counts and deterministic digests, not full raw per-state records.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from math import inf
from pathlib import Path
import re
import subprocess
import sys
import traceback

import certificate as cert
import reference as ref

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = '291425d273412a65e98facc79bc368616200d7a1'
EXPECTED = {2: 84, 3: 1884, 4: 33824}


def clean(value):
    if isinstance(value, float) and value == inf:
        return 'infinity'
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    return value


def encoded(value) -> bytes:
    return json.dumps(clean(value), sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


class Audit:
    def __init__(self):
        self.counts = Counter()
        self.context = None
        self.digest = sha256()

    def equal(self, name, actual, expected):
        self.counts[name] += 1
        if actual != expected:
            raise AssertionError(json.dumps(clean({'obligation': name, 'context': self.context,
                                                   'actual': actual, 'expected': expected}), sort_keys=True))

    def true(self, name, value):
        self.equal(name, bool(value), True)

    def record(self, name, value):
        self.digest.update(encoded([name, value]) + b'\n')


def moves(p, roots):
    return tuple(('del' if s & (1 << x) else 'add', i, x)
                 for i, s in enumerate(roots) for x in range(p))


def transforms(p, m):
    for x in range(p - 1):
        labels = list(range(p)); labels[x], labels[x + 1] = labels[x + 1], labels[x]
        yield ('label', x), tuple(labels), tuple(range(m))
    for i in range(m - 1):
        slots = list(range(m)); slots[i], slots[i + 1] = slots[i + 1], slots[i]
        yield ('root', i), tuple(range(p)), tuple(slots)


def map_mask(s, labels):
    return sum(1 << labels[x] for x in range(len(labels)) if s & (1 << x))


def mapped(roots, floors, labels, slots):
    new_roots, new_floors = [0] * len(roots), [0] * len(roots)
    for i, s in enumerate(roots):
        new_roots[slots[i]], new_floors[slots[i]] = map_mask(s, labels), floors[i]
    return tuple(new_roots), tuple(new_floors)


def map_move(move, labels, slots):
    kind, i, x = move
    return kind, slots[i], labels[x]


def response_matrix(a, p, roots, floors, candidates, before):
    matrix = {}
    for e in candidates:
        if not before[e]:
            continue
        post = ref.apply(p, roots, e)
        for g in candidates:
            if g[1:] == e[1:]:
                continue
            a.context = (p, roots, floors, e, g)
            a.true('common_candidate_syntax', cert.syntax(p, post, g))
            joint = ref.apply(p, post, g)
            a.equal('incidence_commutation', joint, ref.apply(p, ref.apply(p, roots, g), e))
            response = int(ref.legal(p, post, floors, g)) - int(before[g])
            a.true('response_sign_' + e[0] + '_' + g[0],
                   response <= 0 if e[0] == g[0] else response >= 0)
            after_cert = cert.legal(p, post, floors, g)
            a.equal('certificate_response', int(after_cert) - int(cert.legal(p, roots, floors, g)), response)
            if e[1] != g[1]:
                a.equal('cross_root_support_floor_unchanged',
                        (post[g[1]], floors[g[1]]), (roots[g[1]], floors[g[1]]))
            matrix[e, g] = response
    return matrix


def summary(matrix, e):
    values = [r for (first, _), r in matrix.items() if first == e]
    s, f = values.count(-1), values.count(1)
    return s, f, f - s, f + s


def check_state(a, p, roots, floors, *, covariance=True):
    a.context = (p, roots, floors)
    t, old = ref.tau(p, roots), cert.fields(p, roots)
    if p >= 2:
        a.equal('pair_equivalence', all(v >= 1 for v in old['W'].values()), t >= 3)
    a.equal('upper_equivalence', bool(any(old['C'].values())), t <= 4)
    protected = (len(floors) == len(roots) and all(f >= 1 and s.bit_count() >= f
                 for s, f in zip(roots, floors)) and 3 <= t <= 4)
    a.equal('protected_state_equivalence', cert.protected(p, roots, floors), protected)
    candidates = moves(p, roots)
    before = {}
    for e in candidates:
        a.context = (p, roots, floors, e)
        post = ref.apply(p, roots, e)
        a.equal('independent_toggle', cert.apply(p, roots, e), post)
        pred, actual = cert.predict(p, roots, e), cert.fields(p, post)
        for k, value in actual['W'].items():
            a.equal('W_update_coordinate', pred['W'][k], value)
            delta = value - old['W'][k]
            a.true('W_coordinate_monotone_lipschitz', -1 <= delta <= 0 if e[0] == 'add' else 0 <= delta <= 1)
        for h, value in actual['C'].items():
            a.equal('C_update_coordinate', pred['C'][h], value)
            a.true('C_coordinate_monotone', value >= old['C'][h] if e[0] == 'add' else value <= old['C'][h])
        changed = sum(actual['W'][k] != v for k, v in old['W'].items())
        expected_changed = p - roots[e[1]].bit_count() - int(e[0] == 'add')
        a.equal('W_changed_coordinate_count', changed, expected_changed)
        if old['W']:
            delta = min(actual['W'].values()) - min(old['W'].values())
            a.true('global_minimum_lipschitz', -1 <= delta <= 0 if e[0] == 'add' else 0 <= delta <= 1)
        delta_c = sum(actual['C'].values()) - sum(old['C'].values())
        a.true('N4_monotone', delta_c >= 0 if e[0] == 'add' else delta_c <= 0)
        post_t = ref.tau(p, post)
        a.true('transversal_monotone', post_t <= t if e[0] == 'add' else post_t >= t)
        if p >= 2:
            a.equal('endpoint_pair_equivalence', all(v >= 1 for v in actual['W'].values()), post_t >= 3)
        a.equal('endpoint_upper_equivalence', bool(any(actual['C'].values())), post_t <= 4)
        if protected:
            direct = ref.legal(p, roots, floors, e)
            a.equal('candidate_iff_' + e[0], cert.legal(p, roots, floors, e), direct)
            before[e] = direct
    matrix = response_matrix(a, p, roots, floors, candidates, before) if protected else {}
    if covariance:
        for tag, labels, slots in transforms(p, len(roots)):
            a.context = (p, roots, floors, tag)
            rr, ff = mapped(roots, floors, labels, slots)
            new = cert.fields(p, rr)
            a.equal('covariance_tau', ref.tau(p, rr), t)
            a.equal('covariance_W', new['W'], {map_mask(k, labels): v for k, v in old['W'].items()})
            a.equal('covariance_C', new['C'], {map_mask(h, labels): v for h, v in old['C'].items()})
            a.equal('covariance_protected', cert.protected(p, rr, ff), protected)
            if protected:
                for g in candidates:
                    gg = map_move(g, labels, slots)
                    a.equal('covariance_margin', cert.margin(p, rr, gg), cert.margin(p, roots, g))
                    a.equal('covariance_direct_legality', ref.legal(p, rr, ff, gg), before[g])
                    a.equal('covariance_certificate_legality', cert.legal(p, rr, ff, gg), before[g])
                transformed_matrix = {}
                for (e, g), r in matrix.items():
                    ee, gg = map_move(e, labels, slots), map_move(g, labels, slots)
                    value = int(ref.legal(p, ref.apply(p, rr, ee), ff, gg)) - int(ref.legal(p, rr, ff, gg))
                    a.equal('covariance_response', value, r)
                    transformed_matrix[ee, gg] = value
                for e in candidates:
                    if before[e]:
                        a.equal('covariance_SFQM', summary(transformed_matrix, map_move(e, labels, slots)), summary(matrix, e))
    a.record('state', [p, roots, floors, t, old, sorted(before.items()), sorted(matrix.items())])
    return protected


def roots_of(*supports):
    return tuple(sum(1 << (ord(x) - ord('a')) for x in s) for s in supports)


def component(roots, floors, origin):
    seen, frontier = {origin}, [origin]
    while frontier:
        i = frontier.pop()
        for j, s in enumerate(roots):
            if j not in seen and roots[i] & s:
                seen.add(j); frontier.append(j)
    return tuple((i, roots[i], floors[i]) for i in sorted(seen))


def overlap_originals():
    text = (ROOT / 'A12_5_OVERLAP_LOCALITY_NOGO.md').read_text()
    result = []
    for label in ('L', 'I'):
        block = text.split('State ' + label + ':', 1)[1]
        strings = re.findall(r'R[0-5]=\{([^}]+)\}', block)[:6]
        if len(strings) != 6:
            raise AssertionError('Incomplete original A12.5 fixture')
        result.append(roots_of(*(s.replace(',', '') for s in strings)))
    return tuple(result)


def controls(a):
    results = []
    def reject(name, bad, correct, witness):
        a.context = witness
        a.true('reject_' + name, bad != correct)
        results.append({'name': name, 'status': 'REJECTED', 'bad_claim': clean(bad),
                        'correct_value': clean(correct), 'witness': clean(witness)})
    ids = list(cert.universe(2, 1)); target = list(ref.universe(2, 1))
    a.true('control_valid_coverage', ref.coverage_ok(ids, target))
    reject('missing_identity', ref.coverage_ok(ids[:-1], target), True, ids[-1])
    reject('duplicate_identity', ref.coverage_ok(ids + ids[:1], target), True, ids[0])
    n = 2; family = (1, 2) + (4,) * (n + 1)
    reject('wrong_family_root_count', n + 2, len(family), {'n': n, 'roots': family})
    reject('unqualified_pair_equivalence', all(v >= 1 for v in cert.fields(1, (1,))['W'].values()),
           ref.tau(1, (1,)) >= 3, {'p': 1, 'roots': (1,)})
    roots = (1, 2, 4, 8); e = ('add', 2, 0)
    old = cert.fields(4, roots); post = cert.fields(4, ref.apply(4, roots, e))
    k = 3
    reject('wrong_W_update_sign', old['W'][k] + 1, post['W'][k], (roots, e, k))
    actual_count = sum(post['W'][k] != v for k, v in old['W'].items())
    reject('wrong_coordinate_count', 4 - roots[2].bit_count(), actual_count, (roots, e))
    roots_floor = (1, 2, 5, 8); floors = (1, 1, 2, 1); deletion = ('del', 2, 0)
    band_only = 3 <= ref.tau(4, ref.apply(4, roots_floor, deletion)) <= 4
    reject('floor_free_legality', band_only, ref.legal(4, roots_floor, floors, deletion),
           (roots_floor, floors, deletion))
    g = ('add', 3, 1)
    response = int(ref.legal(4, ref.apply(4, roots, e), (1,)*4, g)) - int(ref.legal(4, roots, (1,)*4, g))
    reject('reversed_strict_response_sign', 1, response, (roots, e, g))
    a.true('N4_control_first_move_legal', ref.legal(4, roots, (1,)*4, e))
    reject('false_N4_conservation', sum(old['C'].values()), sum(post['C'].values()), (roots, e))
    _, overlap_i = overlap_originals()
    reject('wrong_overlap_endpoint', 3, ref.tau(5, ref.apply(5, overlap_i, ('add', 0, 1))), overlap_i)
    source = (12, 4, 1, 2); first = ('add', 0, 1); candidate = ('add', 0, 0)
    reject('same_root_A_nonincrease', True,
           cert.margin(4, ref.apply(4, source, first), candidate) <= cert.margin(4, source, candidate),
           (source, first, candidate))
    a.equal('rejecting_control_count', len(results), 11)
    a.record('rejecting_controls', results)
    return results


def fixtures(a):
    records = []
    strict = [
        ('AA', 4, (1, 2, 4, 8), ('add', 2, 0), ('add', 3, 1), (4, 3, 3, 2), -1),
        ('DA', 4, (1, 2, 5, 8), ('del', 2, 0), ('add', 3, 1), (3, 4, 2, 3), 1),
        ('DD', 5, (1, 2, 4, 9, 18), ('del', 3, 0), ('del', 4, 1), (3, 4, 4, 5), -1),
        ('AD', 5, (1, 2, 4, 8, 18), ('add', 3, 0), ('del', 4, 1), (4, 3, 5, 4), 1),
    ]
    for name, p, roots, e, g, expected, sign in strict:
        floors = (1,) * len(roots)
        first, cand = ref.apply(p, roots, e), ref.apply(p, roots, g)
        joint = ref.apply(p, first, g)
        actual = tuple(ref.tau(p, s) for s in (roots, first, cand, joint))
        a.context = ('strict', name)
        a.equal('strict_tau_values', actual, expected)
        a.true('strict_first_legal', ref.legal(p, roots, floors, e))
        r = int(ref.legal(p, first, floors, g)) - int(ref.legal(p, roots, floors, g))
        a.equal('strict_response', r, sign)
        for s in (roots, first, cand, joint):
            check_state(a, p, s, floors)
            a.counts['fixture_states'] += 1
        records.append({'name': name, 'p': p, 'roots': roots, 'first': e, 'candidate': g,
                        'tau_source_first_candidate_joint': actual, 'response': r})
    pairs = [
        ('addition_fixed_candidate', 4, (1, 2, 5, 8), (1, 4, 3, 8), ('add', 3, 1), (False, True)),
        ('deletion_fixed_candidate', 5, (4, 3, 2, 16, 8), (4, 3, 1, 16, 8), ('del', 1, 0), (True, False)),
    ]
    for name, p, left, right, g, expected in pairs:
        floors = (1,) * len(left)
        lf, rf = cert.fields(p, left), cert.fields(p, right)
        scalars = lambda v: (min(v['W'].values()), sum(v['C'].values()))
        a.context = name
        a.equal('matched_global_scalar_pair', scalars(lf), scalars(rf))
        values = (ref.legal(p, left, floors, g), ref.legal(p, right, floors, g))
        a.equal('fixed_candidate_different_legality', values, expected)
        alternate = ('add', 3, 2) if p == 4 else ('del', 1, 1)
        a.equal('original_two_candidate_control', ref.legal(p, left, floors, alternate), expected[1])
        for s in (left, right):
            check_state(a, p, s, floors); a.counts['fixture_states'] += 1
        records.append({'name': name, 'left': left, 'right': right, 'candidate': g,
                        'global_scalars': scalars(lf), 'legalities': values})
    overlap_l, overlap_i = overlap_originals()
    a.context = 'A12.5 original-source fidelity'
    a.equal('original_L_fidelity', overlap_l, roots_of('d', 'ac', 'ce', 'a', 'ace', 'ab'))
    a.equal('original_I_fidelity', overlap_i, roots_of('d', 'abe', 'abe', 'ace', 'b', 'c'))
    floors, g = (1,) * 6, ('add', 0, 1)
    a.equal('overlap_component_identity', component(overlap_l, floors, 0), component(overlap_i, floors, 0))
    vals = (ref.tau(5, overlap_l), ref.tau(5, overlap_i),
            ref.tau(5, ref.apply(5, overlap_l, g)), ref.tau(5, ref.apply(5, overlap_i, g)))
    a.equal('overlap_exact_endpoints', vals, (3, 3, 3, 2))
    a.equal('overlap_critical_W', (cert.fields(5, overlap_l)['W'][6], cert.fields(5, overlap_i)['W'][6]), (2, 1))
    for s in (overlap_l, overlap_i, ref.apply(5, overlap_l, g), ref.apply(5, overlap_i, g)):
        check_state(a, 5, s, floors); a.counts['fixture_states'] += 1
    records.append({'name': 'overlap_originals', 'L': overlap_l, 'I': overlap_i, 'candidate': g,
                    'component': component(overlap_l, floors, 0), 'tau_L_I_gL_gI': vals})
    diagnostics = [
        ('empty_palette_family', 0, (), (), 0),
        ('empty_palette_support', 0, (0,), (1,), inf),
        ('one_label', 1, (1,), (1,), 1),
        ('empty_support', 1, (0,), (1,), inf),
        ('two_label', 2, (1, 2), (1, 1), 2),
        ('three_singleton', 3, (1, 2, 4), (1, 1, 1), 3),
        ('floor_boundary', 4, (1, 2, 5, 8), (1, 1, 2, 1), 3),
        ('finite_shadow', 4, (12, 4, 1, 2), (1,)*4, 3),
        ('empty_shadow', 4, (14, 4, 1, 2), (1,)*4, 3),
    ]
    for name, p, s, floors, expected in diagnostics:
        a.context = name; a.equal('diagnostic_tau', ref.tau(p, s), expected)
        check_state(a, p, s, floors); a.counts['fixture_states'] += 1
        records.append({'name': name, 'p': p, 'roots': s, 'floors': floors, 'tau': expected})
    a.equal('finite_to_empty_margin', (cert.margin(4, (12, 4, 1, 2), ('add', 0, 0)),
                                     cert.margin(4, (14, 4, 1, 2), ('add', 0, 0))), (2, inf))
    return records


def collective(a):
    records = []
    for n in range(2, 9):
        m, full, g = n + 3, (1 << n) - 1, ('add', 2, 0)
        floors = (1,) * m
        states = [(1, 2, 4) + tuple(5 if t & (1 << j) else 4 for j in range(n)) for t in range(1 << n)]
        chi, edges = [], 0
        for t, roots in enumerate(states):
            a.context = ('collective', n, t)
            a.equal('family_root_count', len(roots), m)
            a.equal('family_prefix_tau', ref.tau(3, roots), 3)
            value = ref.legal(3, roots, floors, g)
            a.equal('family_candidate_iff', cert.legal(3, roots, floors, g), value)
            a.equal('family_candidate_legality', value, t != full)
            a.equal('family_endpoint_tau', ref.tau(3, ref.apply(3, roots, g)), 2 if t == full else 3)
            a.equal('family_W_reservoir', cert.fields(3, roots)['W'][3], n + 1 - t.bit_count())
            chi.append(int(value))
            for j in range(n):
                if not (t & (1 << j)):
                    e = ('add', j + 3, 0)
                    a.true('family_edge_legal', ref.legal(3, roots, floors, e))
                    a.true('family_edge_certificate', cert.legal(3, roots, floors, e))
                    a.equal('family_edge_endpoint', ref.apply(3, roots, e), states[t | (1 << j)])
                    edges += 1
            for _, labels, slots in transforms(3, m):
                rr, ff = mapped(roots, floors, labels, slots); gg = map_move(g, labels, slots)
                a.equal('family_covariance', ref.legal(3, rr, ff, gg), value)
                a.equal('family_covariance_margin', cert.margin(3, rr, gg), cert.margin(3, roots, g))
        coefficients = chi.copy()
        for j in range(n):
            for u in range(1 << n):
                if u & (1 << j):
                    coefficients[u] -= coefficients[u ^ (1 << j)]
        for u in range(1 << n):
            v, direct = u, 0
            while True:
                direct += (-1) ** (u.bit_count() - v.bit_count()) * chi[v]
                if not v:
                    break
                v = (v - 1) & u
            expected = 1 if u == 0 else (-1 if u == full else 0)
            a.equal('mobius_independent_sum', coefficients[u], direct)
            a.equal('mobius_exact_coefficient', direct, expected)
        a.equal('family_complete_edge_count', edges, n * (1 << (n - 1)))
        records.append({'n': n, 'root_count': m, 'subsets': len(states), 'edges': edges,
                        'chi': chi, 'coefficients': coefficients})
    a.record('collective', records)
    return records


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encoded(data) + b'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--controls-only', action='store_true')
    args = parser.parse_args()
    a = Audit()
    source_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    result = {'schema': 'A12.bounded.v1', 'status': 'INCOMPLETE', 'protocol_commit': PROTOCOL,
              'implementation_commit': source_commit, 'completed_blocks': [],
              'interpretation': 'Finite corroboration only; universal claims rely on the written arguments.'}
    save(args.output, result)
    try:
        result['rejecting_controls'] = controls(a)
        if args.controls_only:
            result.update(status='CONTROLS_PASS', counts=dict(a.counts), check_digest=a.digest.hexdigest())
            save(args.output, result); print('CONTROLS_PASS:', len(result['rejecting_controls']))
            return 0
        for p in (2, 3, 4):
            count_p = 0
            for m in (1, 2, 3):
                ids, expected_ids = list(cert.universe(p, m)), list(ref.universe(p, m))
                a.context = ('universe', p, m)
                a.true('complete_identity_equality', ref.coverage_ok(ids, expected_ids))
                expected_count = (p * (2 ** (p - 1))) ** m
                a.equal('primary_state_count', len(ids), expected_count)
                a.true('full_block_omission_rejected', not ref.coverage_ok(ids[:-1], expected_ids))
                a.true('full_block_duplicate_rejected', not ref.coverage_ok(ids + ids[:1], expected_ids))
                protected_count = 0
                for roots, floors in ids:
                    protected_count += check_state(a, p, roots, floors)
                identity_digest = sha256(encoded(sorted(ids))).hexdigest()
                result['completed_blocks'].append({'p': p, 'm': m, 'states': len(ids),
                    'protected_states': protected_count, 'identity_sha256': identity_digest,
                    'coverage': 'EXACT_SET_EQUALITY_NO_DUPLICATES'})
                count_p += len(ids)
                result['counts'] = dict(a.counts); save(args.output, result)
                print(f'p={p} m={m}: {len(ids)} identities, {protected_count} protected; complete', flush=True)
            a.equal('palette_total_count', count_p, EXPECTED[p])
        total = sum(row['states'] for row in result['completed_blocks'])
        a.equal('primary_total_count', total, 35792)
        result['fixtures'] = fixtures(a)
        result['collective_families'] = collective(a)
        result.update(status='BOUNDED_PASS', primary_states=total, counts=dict(a.counts),
                      check_digest=a.digest.hexdigest(), overall_A12_gate='OPEN_PENDING_REPORTING_AUDIT')
        save(args.output, result)
        print(json.dumps({'status': result['status'], 'primary_states': total,
                          'rejecting_controls': len(result['rejecting_controls']),
                          'fixture_states': a.counts['fixture_states'],
                          'family_subsets': sum(x['subsets'] for x in result['collective_families']),
                          'check_digest': result['check_digest']}, sort_keys=True), flush=True)
        return 0
    except Exception as exc:
        result.update(status='FAIL', error=str(exc), first_failing_context=clean(a.context),
                      counts=dict(a.counts), traceback=traceback.format_exc())
        save(args.output, result)
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
