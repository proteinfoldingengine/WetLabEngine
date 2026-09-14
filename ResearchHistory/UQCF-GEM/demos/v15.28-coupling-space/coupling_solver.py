from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd, lcm
import hashlib
import json
import exact_linear as ql

@dataclass(frozen=True)
class RepresentationPair:
    source_rep: dict
    target_rep: dict

@dataclass(frozen=True)
class CouplingSpace:
    dimension: int
    basis: tuple[ql.MatrixQ, ...]
    constraint_rank: int
    orbit_count: int | None = None
    metadata: dict = field(default_factory=dict)


def _dims(rep: dict) -> int:
    if not rep:
        raise ValueError('empty representation')
    dims = set()
    for a in rep.values():
        a = ql.matrix(a); r, c = ql.shape(a)
        if r != c:
            raise ValueError('representation matrix not square')
        dims.add(r)
    if len(dims) != 1:
        raise ValueError('inconsistent representation dimensions')
    return next(iter(dims))


def _check_pair(pair: RepresentationPair):
    if set(pair.source_rep) != set(pair.target_rep):
        raise ValueError('group keys differ')
    return _dims(pair.source_rep), _dims(pair.target_rep)


def solve_exact_intertwiners(pair: RepresentationPair) -> CouplingSpace:
    sdim, tdim = _check_pair(pair); nvars = sdim * tdim; rows = []
    for key in pair.source_rep:
        S = ql.matrix(pair.source_rep[key]); T = ql.matrix(pair.target_rep[key])
        for i in range(tdim):
            for j in range(sdim):
                row = [Fraction(0) for _ in range(nvars)]
                for k in range(sdim):
                    row[i*sdim+k] += S[k][j]
                for ell in range(tdim):
                    row[ell*sdim+j] -= T[i][ell]
                if any(row):
                    rows.append(tuple(row))
    if rows:
        _rr, piv = ql.rref(tuple(rows)); ns = ql.nullspace(tuple(rows)); cr = len(piv)
    else:
        cr = 0
        ns = tuple(tuple(Fraction(1 if k == i else 0) for k in range(nvars))
                   for i in range(nvars))
    basis = []
    for v in ns:
        basis.append(tuple(tuple(v[i*sdim+j] for j in range(sdim)) for i in range(tdim)))
    return CouplingSpace(len(basis), tuple(basis), cr, None,
                         {'source_dim': sdim, 'target_dim': tdim, 'equation_count': len(rows)})


def synthetic_c2_sign_mismatch() -> RepresentationPair:
    return RepresentationPair({'e': ql.identity(1), 'g': ql.identity(1)},
                              {'e': ql.identity(1), 'g': ql.matrix(((-1,),))})


def synthetic_c2_identical_sign() -> RepresentationPair:
    s = {'e': ql.identity(1), 'g': ql.matrix(((-1,),))}
    return RepresentationPair(s, dict(s))


def synthetic_trivial_multiplicity(source_dim: int, target_dim: int) -> RepresentationPair:
    if type(source_dim) is not int or type(target_dim) is not int or min(source_dim, target_dim) < 1:
        raise ValueError('positive dimensions required')
    return RepresentationPair({'e': ql.identity(source_dim), 'g': ql.identity(source_dim)},
                              {'e': ql.identity(target_dim), 'g': ql.identity(target_dim)})


def change_pair_basis(pair: RepresentationPair, source_change, target_change) -> RepresentationPair:
    sdim, tdim = _check_pair(pair); source_change = ql.matrix(source_change); target_change = ql.matrix(target_change)
    if ql.shape(source_change) != (sdim, sdim) or ql.shape(target_change) != (tdim, tdim):
        raise ValueError('change of basis dimension mismatch')
    return RepresentationPair({k: ql.conjugate(v, source_change) for k, v in pair.source_rep.items()},
                              {k: ql.conjugate(v, target_change) for k, v in pair.target_rep.items()})


def hom_dimension_from_characters(source_rep: dict, target_rep: dict) -> int:
    if set(source_rep) != set(target_rep) or not source_rep:
        raise ValueError('group keys differ or empty')
    total = sum((ql.trace(ql.matrix(target_rep[k])) * ql.trace(ql.matrix(source_rep[k]))
                 for k in source_rep), Fraction(0))
    value = total / Fraction(len(source_rep))
    if value.denominator != 1:
        raise ArithmeticError('nonintegral character inner product')
    return value.numerator


def hom_dimension_from_character_values(source_chars: dict, target_chars: dict) -> int:
    if set(source_chars) != set(target_chars) or not source_chars:
        raise ValueError('character keys differ or empty')
    total = sum((Fraction(source_chars[k]) * Fraction(target_chars[k]) for k in source_chars), Fraction(0))
    value = total / Fraction(len(source_chars))
    if value.denominator != 1:
        raise ArithmeticError('nonintegral character inner product')
    return value.numerator


def canonical_projective_matrix(a):
    a = ql.matrix(a); flat = [x for row in a for x in row]; nz = [x for x in flat if x]
    if not nz:
        raise ValueError('zero matrix has no projective form')
    den = 1
    for x in nz:
        den = lcm(den, x.denominator)
    ints = [int(x * den) for x in flat]; g = 0
    for x in ints:
        g = gcd(g, abs(x))
    if g == 0:
        raise ValueError('zero matrix')
    ints = [x // g for x in ints]
    first = next(x for x in ints if x)
    if first < 0:
        ints = [-x for x in ints]
    r, c = ql.shape(a)
    return tuple(tuple(ints[i*c+j] for j in range(c)) for i in range(r))


def projective_hash(a) -> str:
    canon = canonical_projective_matrix(a)
    raw = json.dumps(canon, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


def solve_signed_ambient(source_actions: dict, target_actions: dict,
                         source_null_vectors=(), target_constraint_rows=()) -> CouplingSpace:
    if set(source_actions) != set(target_actions) or not source_actions:
        raise ValueError('group action keys differ or empty')
    keys = tuple(source_actions); s0 = source_actions[keys[0]]; t0 = target_actions[keys[0]]
    s0.validate(); t0.validate(); sdim = len(s0.image); tdim = len(t0.image)
    for k in keys:
        source_actions[k].validate(); target_actions[k].validate()
        if len(source_actions[k].image) != sdim or len(target_actions[k].image) != tdim:
            raise ValueError('action dimension mismatch')
    n = sdim * tdim; assigned = [None] * n; components = []; zero_flags = []
    for seed in range(n):
        if assigned[seed] is not None:
            continue
        assigned[seed] = 1; queue = [seed]; members = []; zero = False
        while queue:
            p = queue.pop(); members.append(p); i, j = divmod(p, sdim); sp = assigned[p]
            for k in keys:
                ta = target_actions[k]; sa = source_actions[k]
                qidx = ta.image[i] * sdim + sa.image[j]
                want = sp * ta.sign[i] * sa.sign[j]
                if assigned[qidx] is None:
                    assigned[qidx] = want; queue.append(qidx)
                elif assigned[qidx] != want:
                    zero = True
        components.append(tuple(members)); zero_flags.append(zero)
    orbit_map = {}; orbit_sign = {}; orbit_count = 0; zero_components = 0
    for cid, members in enumerate(components):
        if zero_flags[cid]:
            zero_components += 1; continue
        oid = orbit_count; orbit_count += 1
        for p in members:
            orbit_map[p] = oid; orbit_sign[p] = assigned[p]
    rows = []
    for vec in source_null_vectors:
        vec = tuple(Fraction(x) for x in vec)
        if len(vec) != sdim:
            raise ValueError('source null vector dimension mismatch')
        for i in range(tdim):
            row = [Fraction(0) for _ in range(orbit_count)]
            for j, x in enumerate(vec):
                p = i*sdim+j
                if p in orbit_map and x:
                    row[orbit_map[p]] += Fraction(orbit_sign[p]) * x
            if any(row):
                rows.append(tuple(row))
    for crow in target_constraint_rows:
        crow = tuple(Fraction(x) for x in crow)
        if len(crow) != tdim:
            raise ValueError('target constraint dimension mismatch')
        for j in range(sdim):
            row = [Fraction(0) for _ in range(orbit_count)]
            for i, x in enumerate(crow):
                p = i*sdim+j
                if p in orbit_map and x:
                    row[orbit_map[p]] += x * Fraction(orbit_sign[p])
            if any(row):
                rows.append(tuple(row))
    if orbit_count == 0:
        ns = (); cr = 0
    elif rows:
        cr = ql.rank(tuple(rows)); ns = ql.nullspace(tuple(rows))
    else:
        cr = 0
        ns = tuple(tuple(Fraction(1 if i == j else 0) for i in range(orbit_count))
                   for j in range(orbit_count))
    basis = []
    for coeff in ns:
        dense = [[Fraction(0) for _ in range(sdim)] for _ in range(tdim)]
        for p, oid in orbit_map.items():
            i, j = divmod(p, sdim); dense[i][j] = Fraction(orbit_sign[p]) * coeff[oid]
        basis.append(tuple(tuple(row) for row in dense))
    return CouplingSpace(len(basis), tuple(basis), cr, orbit_count,
                         {'pair_count': n, 'component_count': len(components),
                          'zero_components': zero_components, 'structural_equations': len(rows)})
