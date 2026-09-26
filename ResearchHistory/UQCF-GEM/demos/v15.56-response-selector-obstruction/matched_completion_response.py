"""Exact matched-input probe after the pruning-consistency correction.

Two distinct experiments; no map between their observables is assumed.
(1) Fixed prefix trees, balanced source, retained-vertex observable: compare
    lawful pruning orders with the same endpoints.
(2) Reproduce v13.13's commuting parity-state ETL/PGRL witness with the same
    supplied source and observable pair. This is also a classical probability
    example, not a new dynamics, quantum exclusivity, or a gravity claim.

Only standard-library rational arithmetic is used. The finite-tilt parameter
is source odds u=exp(2s), not physical time. Historical files are unmodified.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations, product
import json

import pruning_consistency_audit as baseline

SNAPSHOT = '72a3e4bec8c0ad906a6a01819543602529e106d4'
EPSILON = F(1, 5)


def rational(x: F | int) -> F:
    if type(x) is not int and not isinstance(x, F):
        raise TypeError('Use an integer or Fraction, not floating-point data')
    return F(x)


@lru_cache(maxsize=16)
def spin_states(n: int) -> tuple[tuple[int, ...], ...]:
    if type(n) is not int or not 1 <= n <= 12:
        raise ValueError('The executable supports 1..12 sites; this is not a theorem bound')
    return tuple(product((1, -1), repeat=n))


@dataclass(frozen=True)
class DiagonalState:
    n: int
    probabilities: tuple[F, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.probabilities, tuple):
            raise TypeError('Probabilities must be an immutable tuple')
        if len(self.probabilities) != len(spin_states(self.n)):
            raise ValueError('Probability array must have 2**n entries')
        p = tuple(rational(x) for x in self.probabilities)
        if any(x < 0 for x in p) or sum(p) != 1:
            raise ValueError('Probabilities must be nonnegative and sum exactly to one')
        object.__setattr__(self, 'probabilities', p)


def parity_state(n: int, epsilon: F | int = EPSILON, sign: int = 1) -> DiagonalState:
    """Diagonal rho=(I+sign*epsilon*Z_1...Z_n)/2**n, epsilon in [0,1)."""
    eps = rational(epsilon)
    if not 0 <= eps < 1 or type(sign) is not int or sign not in (-1, 1):
        raise ValueError('Require 0 <= epsilon < 1 and sign in {-1,+1}')
    values = z_observable(n, tuple(range(n)))
    return DiagonalState(n, tuple((1 + sign * eps * z) / (2**n) for z in values))


def sites(n: int, support) -> tuple[int, ...]:
    spin_states(n)
    support = tuple(support)
    if len(set(support)) != len(support) or any(type(i) is not int or not 0 <= i < n for i in support):
        raise ValueError('Sites must be distinct in-range integers')
    return support


def z_observable(n: int, support) -> tuple[F, ...]:
    support = sites(n, support)
    result = []
    for world in spin_states(n):
        value = 1
        for i in support:
            value *= world[i]
        result.append(F(value))
    return tuple(result)


def subsets(n: int):
    for size in range(n + 1):
        yield from combinations(range(n), size)


def expectation(state: DiagonalState, observable) -> F:
    observable = tuple(observable)
    if len(observable) != len(state.probabilities):
        raise ValueError('Observable dimension does not match state')
    return sum((p * rational(o) for p, o in zip(state.probabilities, observable)), F(0))


def susceptibility(state: DiagonalState, observable, source) -> F:
    """Exact ETL derivative for commuting data: E[OP]-E[O]E[P]."""
    observable, source = tuple(observable), tuple(source)
    if len(observable) != len(state.probabilities) or len(source) != len(observable):
        raise ValueError('Source and observable dimensions must match state')
    mean_o, mean_p = expectation(state, observable), expectation(state, source)
    joint = tuple(rational(o) * rational(p) for o, p in zip(observable, source))
    return expectation(state, joint) - mean_o * mean_p


def paired_response(state: DiagonalState, amplitude: F | int = 1,
                    identity_shift: F | int = 0) -> tuple[F, F]:
    if state.n < 2:
        raise ValueError('The fixed observable pair requires at least two sites')
    a, b = rational(amplitude), rational(identity_shift)
    ref = z_observable(state.n, (state.n - 1,))
    source = tuple(a * z + b for z in ref)
    observable = z_observable(state.n, range(state.n - 1))
    return (susceptibility(state, observable, source), susceptibility(state, ref, source))


def determinant(x, y) -> F:
    if len(x) != 2 or len(y) != 2:
        raise ValueError('Two response coordinates are required')
    return x[0] * y[1] - x[1] * y[0]


def _index(world) -> int:
    index = 0
    for value in world:
        index = 2 * index + (value == -1)
    return index


def marginal(state: DiagonalState, support) -> tuple[F, ...]:
    support = sites(state.n, support)
    out = [F(0)] * (2**len(support))
    for world, p in zip(spin_states(state.n), state.probabilities):
        out[_index(tuple(world[i] for i in support))] += p
    return tuple(out)


def tilt_odds(state: DiagonalState, source_site: int, odds: F | int) -> DiagonalState:
    """Exact positive reweighting for exp(s Z_site), odds=exp(2s)."""
    sites(state.n, (source_site,))
    u = rational(odds)
    if u <= 0:
        raise ValueError('Source odds must be strictly positive')
    p = tuple(p * (u if world[source_site] == 1 else 1)
              for p, world in zip(state.probabilities, spin_states(state.n)))
    total = sum(p)
    return DiagonalState(state.n, tuple(x / total for x in p))


def permute_sites(state: DiagonalState, permutation) -> DiagonalState:
    perm = sites(state.n, permutation)
    if len(perm) != state.n:
        raise ValueError('A complete site permutation is required')
    p = [F(0)] * len(state.probabilities)
    for world, value in zip(spin_states(state.n), state.probabilities):
        p[_index(tuple(world[i] for i in perm))] = value
    return DiagonalState(state.n, tuple(p))


def quantum_case(k: int) -> dict:
    n = k + 1
    plus, minus = parity_state(n, EPSILON, 1), parity_state(n, EPSILON, -1)
    supports = [s for s in subsets(n) if 0 < len(s) < n]
    errors = [max(abs(x-y) for x,y in zip(marginal(plus,s),marginal(minus,s))) for s in supports]
    vp, vm = paired_response(plus), paired_response(minus)
    finite = []
    for u in (F(1,4), F(1,2), F(1), F(2), F(4)):
        observations = []
        for state in (plus,minus):
            t = tilt_odds(state,n-1,u)
            observations.append([str(expectation(t,z_observable(n,range(n-1)))),
                                 str(expectation(t,z_observable(n,(n-1,))))])
        finite.append({'source_odds':str(u),'plus':observations[0],'minus':observations[1]})
    # The determinant, not a selected norm, establishes non-collinearity.
    return {
        'k': k, 'site_count': n, 'epsilon': str(EPSILON),
        'minimum_state_eigenvalue': str(min(plus.probabilities + minus.probabilities)),
        'proper_marginal_pairs_checked': len(supports),
        'max_proper_marginal_difference': str(max(errors)),
        'source': 'Z_last', 'observables': ['Z_first_1_through_k', 'Z_last'],
        'response_plus': [str(x) for x in vp], 'response_minus': [str(x) for x in vm],
        'absolute_determinant': str(abs(determinant(vp,vm))),
        'source_scale_free_ratio_plus': str(vp[0]/vp[1]),
        'source_scale_free_ratio_minus': str(vm[0]/vm[1]),
        'unavoidable_first_coordinate_error_from_common_low_data': str(abs(vp[0]-vm[0])/2),
        'exact_finite_tilts': finite,
    }


def pruning_path(fine, coarse, reverse: bool = False):
    baseline.operators(fine,coarse)  # Validate both carriers and subset relation.
    current, coarse = tuple(fine), tuple(coarse)
    path, removed = [current], []
    while set(current) != set(coarse):
        removable = [k for k in current if k not in coarse
                     and not any(c and c[:-1] == k for c in current)]
        if not removable:
            raise ValueError('No lawful leaf removal toward the requested carrier')
        k = sorted(removable, reverse=reverse)[0]
        removed.append(k)
        current = tuple(v for v in current if v != k)
        if set(current) == set(coarse):
            current = coarse
        path.append(current)
    if path[-1] != coarse:
        path.append(coarse)
    return tuple(path), tuple(removed)


def graph_history_case(fine, coarse) -> dict:
    d = baseline.operators(fine, coarse)
    n = len(fine)
    targets = baseline.mul(baseline.mul(d['Gc'],d['P']),d['Cf'])
    source_err = restriction_err = boundary_err = F(0)
    responses, orders = [], []
    for reverse in (False,True):
        path, order = pruning_path(fine,coarse,reverse)
        orders.append([list(k) for k in order])
        P, S = baseline.eye(n), baseline.eye(n)
        for a,b in zip(path,path[1:]):
            step = baseline.operators(a,b)
            P, S = baseline.mul(step['P'],P), baseline.mul(step['S'],S)
        source_err = max(source_err,baseline.maxabs(baseline.sub(P,d['P'])))
        restriction_err = max(restriction_err,baseline.maxabs(baseline.sub(S,d['S'])))
        response = baseline.mul(baseline.mul(d['Cc'],S),d['Gf'])
        boundary_err = max(boundary_err,baseline.maxabs(baseline.sub(response,targets)))
        responses.append(response)
    return {
        'fine_count': n, 'coarse_count': len(coarse), 'history_count': 2,
        'orders_distinct': orders[0] != orders[1], 'removed_address_orders': orders,
        'source_composition_residual': str(source_err),
        'restriction_composition_residual': str(restriction_err),
        'boundary_response_residual': str(boundary_err),
        'between_history_response_residual': str(baseline.maxabs(baseline.sub(*responses))),
        'source_and_observable': 'P C_f J and retained-vertex restriction; full source space',
    }


def control_receipts() -> dict:
    scale_error = null_error = permutation_error = F(0)
    for sign in (-1,1):
        state = parity_state(3,EPSILON,sign)
        v = paired_response(state)
        for a in (F(2,7),F(1),F(3)):
            for b in (F(-5,2),F(0),F(11,3)):
                scaled = paired_response(state,a,b)
                scale_error = max(scale_error,*(abs(x-a*y) for x,y in zip(scaled,v)))
        null_error = max(null_error,*(abs(x) for x in paired_response(state,0,7)))
        for perm in permutations(range(3)):
            state_p = permute_sites(state,perm)
            P = z_observable(3,(perm.index(2),))
            O = z_observable(3,(perm.index(0),perm.index(1)))
            permutation_error = max(permutation_error,abs(susceptibility(state_p,O,P)-v[0]))
    return {
        'max_source_scaling_and_identity_shift_error': str(scale_error),
        'max_identity_source_response': str(null_error),
        'max_site_permutation_error': str(permutation_error),
        'zero_hidden_correlation_response': [str(x) for x in paired_response(parity_state(3,0,1))],
    }


def run() -> dict:
    return {
        'schema': 'uqcf-matched-completion-response-v1', 'source_snapshot': SNAPSHOT,
        'arithmetic': 'EXACT_RATIONAL', 'parameters_fit': 0,
        'graph_histories': [graph_history_case(f,c) for f,c in baseline.CASES],
        'quantum_hierarchy': [quantum_case(k) for k in range(1,7)],
        'controls': control_receipts(),
        'claims': {
            'new_gravity_signal': False,
            'repair_history_generates_parity_states': False,
            'quantum_response_equals_lineage_curvature': False,
            'quantum_exclusive_or_novel_effect': False,
        },
        'interpretation': {
            'graph_arm': 'EXACT_ORDER_NULL_WITH_FIXED_BALANCED_SOURCE_AND_RETAINED_OBSERVABLE',
            'higher_incidence_arm': 'ARCHIVED_HIDDEN_COMPLETION_RESPONSE_REPRODUCED_WITH_NONCOLLINEAR_RESPONSE_PAIR',
            'unearned_bridge': 'NO_DERIVED_MAP_FROM_THE_QUANTUM_SUSCEPTIBILITY_TO_THE_LINEAGE_SCALAR_OPERATOR',
        },
    }

if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
