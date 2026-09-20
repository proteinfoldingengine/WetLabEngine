"""Exact manufactured fields and sequential certification controls.

Local D4 covariance is checked on vector basis elements and every single-site
D4 action, plus simultaneous mixed frames. This is a structural generator
check, not enumeration of the exponentially many frame assignments.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from fractions import Fraction
from functools import lru_cache
from typing import Callable

from exact_algebra import add, identity, matmul, matvec, scale, transpose
from fixtures import periodic_square_input, relabel_input
from holonomy import (ZERO, cotangent_holonomy, curvature_invariant,
                      linearized_holonomy, reverse_cycle, rotate_cycle)
from operational_complex import (Matrix2, construct_operational_complex,
                                 enumerate_baseline_connection)
from transport import FramePresentation, construct_transport, validate_exact_field


@dataclass(frozen=True)
class ControlResult:
    L: int
    root: int | None
    amplitude: Fraction
    curvatures: tuple[Matrix2, ...]
    invariant_counts: tuple[tuple[Fraction, int], ...]
    all_covariances_exact: bool


@dataclass(frozen=True)
class ControlStage:
    passed: bool
    results: tuple[ControlResult, ...] = ()


@dataclass(frozen=True)
class ControlExecutors:
    covariance: Callable[[], ControlStage]
    constant_null: Callable[[], ControlStage]
    l5_nonflat: Callable[[], ControlStage]
    every_root_equivalent: Callable[[], ControlStage]
    l7_holdout_nonflat: Callable[[], ControlStage]
    scale_exact: Callable[[], ControlStage]
    superposition_exact: Callable[[], ControlStage]

    @classmethod
    def default(cls):
        return cls(covariance_control, constant_null_control, l5_nonflat_control,
                   every_root_equivalence_control, l7_holdout_control,
                   scale_control, superposition_stage)


@dataclass(frozen=True)
class ControlFamily:
    covariance_exact: bool | None
    constant_null: bool | None
    l5_nonflat: bool | None
    l7_holdout_nonflat: bool | None
    every_root_equivalent: bool | None
    scale_exact: bool | None
    superposition_exact: bool | None
    results: tuple[ControlResult, ...]
    failed_stage: str | None

    @property
    def all_required_pass(self):
        return all(value is True for value in (
            self.covariance_exact, self.constant_null, self.l5_nonflat,
            self.l7_holdout_nonflat, self.every_root_equivalent,
            self.scale_exact, self.superposition_exact))


def _exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError('exact integer or Fraction required')
    return Fraction(value)


def _size(L):
    if type(L) is not int or L not in (5, 7):
        raise ValueError('manufactured carriers are L=5 and L=7')


@lru_cache(maxsize=2)
def _carrier(L):
    _size(L)
    complex_ = construct_operational_complex(*periodic_square_input(L)).complex
    if complex_ is None:
        raise ArithmeticError('manufactured carrier is not identifiable')
    baseline = enumerate_baseline_connection(complex_).connection
    if baseline is None or not baseline.flat:
        raise ArithmeticError('manufactured baseline is not flat')
    return complex_, baseline


def impulse_field(L: int, marked_vertex: int, amplitude=Fraction(1)):
    _size(L)
    amplitude = _exact(amplitude)
    if type(marked_vertex) is not int or marked_vertex not in range(L * L):
        raise ValueError('marked vertex must belong to the carrier')
    return tuple(amplitude if label == marked_vertex else Fraction(0)
                 for label in range(L * L))


def _expanded(p, delta, cycle):
    """Independent Leibniz expansion: four full products, one insertion each."""
    edges = tuple(zip(cycle, cycle[1:] + cycle[:1]))
    result = ZERO
    for insertion in range(4):
        term = identity(2)
        for i, edge in enumerate(edges):
            term = matmul(delta[edge] if i == insertion else p[edge], term)
        result = add(result, term)
    return result


def _pairing_exact(transport):
    # Testing every vector/covector basis pairing proves the bilinear identity.
    dual = dict(transport.cotangent_pullback_deltas)
    basis = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    return all(sum(a*b for a,b in zip(alpha,matvec(delta,v))) ==
               sum(a*b for a,b in zip(matvec(dual[edge],alpha),v))
               for edge,delta in transport.tangent_deltas for alpha in basis for v in basis)


def _curvatures_and_checks(complex_, baseline, transport):
    presented = replace(baseline, transports=transport.baseline)
    p, delta = dict(transport.baseline), dict(transport.tangent_deltas)
    dual = dict(transport.cotangent_pullback_deltas)
    passed = transport.metric_compatibility_exact and transport.reversal_exact and _pairing_exact(transport)
    curvatures = []
    for cycle in complex_.cycles:
        value = linearized_holonomy(presented, transport, cycle)
        curvatures.append(value)
        # Restrict validation to the eight directed edges used by this face.
        # The initial full-carrier call above still validates the entire record.
        edges = tuple(zip(cycle,cycle[1:]+cycle[:1]))
        edges += tuple((y,x) for x,y in edges)
        face_p = tuple((edge,p[edge]) for edge in edges)
        face_baseline = replace(presented,transports=face_p,directed_edges=edges)
        face_transport = replace(transport,baseline=face_p,
                                 tangent_deltas=tuple((edge,delta[edge]) for edge in edges),
                                 cotangent_pullback_deltas=tuple((edge,dual[edge]) for edge in edges))
        path = identity(2)
        for step in range(4):
            rotated = rotate_cycle(cycle, step)
            expected = matmul(path, matmul(value, transpose(path)))
            for oriented, sign in ((rotated,1),(reverse_cycle(rotated),-1)):
                actual = linearized_holonomy(face_baseline, face_transport, oriented)
                passed = (actual == scale(sign,expected) and
                          actual == _expanded(p,delta,oriented) and
                          cotangent_holonomy(face_baseline,face_transport,oriented) == transpose(actual) and passed)
            path = matmul(p[(cycle[step],cycle[(step+1)%4])],path)
    return tuple(curvatures), passed


@lru_cache(maxsize=256)
def _evaluated(L, field, presentation):
    complex_, baseline = _carrier(L)
    transport = construct_transport(complex_,baseline,field,presentation=presentation)
    curvatures, passed = _curvatures_and_checks(complex_,baseline,transport)
    return transport, curvatures, passed


def _result(L, control_root, amplitude, field, presentation=None):
    transport, curvatures, passed = _evaluated(L,field,presentation)
    counts = tuple(sorted(Counter(curvature_invariant(value) for value in curvatures).items()))
    return ControlResult(L,control_root,amplitude,curvatures,counts,passed)


def constant_control(L: int, value: Fraction) -> ControlResult:
    _size(L)
    value = _exact(value)
    return _result(L,None,value,(value,)*(L*L))


def impulse_control(L: int, root: int, amplitude: Fraction,
                    presentation: FramePresentation | None = None) -> ControlResult:
    field = impulse_field(L,root,amplitude)
    if presentation is not None:
        presentation.validate(_carrier(L)[0])
    return _result(L,root,_exact(amplitude),field,presentation)


def _gauge_matches(original, changed, gauges):
    def forward(values):
        return tuple(((x,y),matmul(gauges[y],matmul(m,transpose(gauges[x]))))
                     for (x,y),m in values)
    return (changed.baseline == forward(original.baseline) and
            changed.tangent_deltas == forward(original.tangent_deltas) and
            changed.source_endomorphisms == tuple(
                ((x,y),matmul(gauges[x],matmul(m,transpose(gauges[x]))))
                for (x,y),m in original.source_endomorphisms) and
            changed.cotangent_pullback_deltas == tuple(
                ((x,y),matmul(gauges[x],matmul(m,transpose(gauges[y]))))
                for (x,y),m in original.cotangent_pullback_deltas))


def _local_structure_exact(complex_):
    """Check the D4 inner-product and opposite-direction identities on bases."""
    basis = ((Fraction(1),Fraction(0)),(Fraction(0),Fraction(1)))
    for g in complex_.d4_actions:
        if matmul(transpose(g),g) != identity(2):
            return False
        for u in basis:
            if matvec(g,tuple(-v for v in u)) != tuple(-v for v in matvec(g,u)):
                return False
            for v in basis:
                if sum(a*b for a,b in zip(matvec(g,u),matvec(g,v))) != sum(a*b for a,b in zip(u,v)):
                    return False
    # The edge rule is linear in its two endpoint gradients and scalar
    # difference. Check its complete vector basis for every pair of local
    # frames, including reflections; bilinearity extends this to all data.
    zero = (Fraction(0),Fraction(0))
    directions = basis + tuple(tuple(-x for x in v) for v in basis)
    def skew(q,d):
        return tuple(tuple((q[i]*d[j]-d[i]*q[j])/2 for j in range(2)) for i in range(2))
    for gx in complex_.d4_actions:
        for gy in complex_.d4_actions:
            p = matmul(gy,transpose(gx))
            for qx,qy in tuple((v,zero) for v in basis)+tuple((zero,v) for v in basis):
                mean = tuple((x+y)/2 for x,y in zip(qx,qy))
                changed_mean = tuple((x+y)/2 for x,y in zip(matvec(gx,qx),matvec(transpose(p),matvec(gy,qy))))
                if changed_mean != matvec(gx,mean):
                    return False
                for d in directions:
                    before = skew(mean,d)
                    after = skew(changed_mean,matvec(gx,d))
                    if after != matmul(gx,matmul(before,transpose(gx))):
                        return False
                    if matmul(p,after) != matmul(gy,matmul(before,transpose(gx))):
                        return False
            if matmul(p,identity(2)) != matmul(gy,transpose(gx)):
                return False
    return True


def _relabel_exact(complex_, baseline, field, original, permutation, marked_vertex):
    names = dict(zip(complex_.labels,permutation))
    new = construct_operational_complex(*relabel_input(
        (complex_.labels,complex_.work,complex_.neighbors),permutation)).complex
    if new is None:
        return False
    new_baseline = enumerate_baseline_connection(new).connection
    values = dict(zip(permutation,field))
    changed = construct_transport(new,new_baseline,tuple(values[x] for x in new.labels))
    if values[names[marked_vertex]] != field[complex_.labels.index(marked_vertex)]:
        return False
    old_d = dict(zip(complex_.directed_edges,complex_.direction_classes))
    new_d = dict(zip(new.directed_edges,new.direction_classes))
    gauges = {}
    for x in complex_.labels:
        matching = [g for g in complex_.d4_actions if all(
            matvec(g,d) == new_d[(names[x],names[y])]
            for (a,y),d in old_d.items() if a == x)]
        if len(matching) != 1:
            return False
        gauges[x] = matching[0]
    # Pull the newly constructed record back to the original label order.
    inverse = {v:k for k,v in names.items()}
    fields = {}
    for name in ('baseline','source_endomorphisms','tangent_deltas','cotangent_pullback_deltas'):
        mapping = {(inverse[x],inverse[y]):m for (x,y),m in getattr(changed,name)}
        fields[name] = tuple((edge,mapping[edge]) for edge in complex_.directed_edges)
    pulled = replace(changed,**fields)
    if not _gauge_matches(original,pulled,gauges):
        return False
    old_p = replace(baseline,transports=original.baseline)
    new_p = replace(new_baseline,transports=changed.baseline)
    return all(linearized_holonomy(new_p,changed,tuple(names[x] for x in cycle)) ==
               matmul(gauges[cycle[0]],matmul(linearized_holonomy(old_p,original,cycle),transpose(gauges[cycle[0]])))
               for cycle in complex_.cycles)


def covariance_control() -> ControlStage:
    for L in (5,7):
        complex_, baseline = _carrier(L)
        if not _local_structure_exact(complex_):
            return ControlStage(False)
        # A dense exact field exercises every local stencil under every action.
        field = tuple(Fraction((i*i+3*i)%17,7) for i in range(L*L))
        original = construct_transport(complex_,baseline,field)
        unit = identity(2)
        for label in complex_.labels:
            for action in complex_.d4_actions:
                presentation = FramePresentation(tuple((x,action if x == label else unit) for x in complex_.labels))
                changed = construct_transport(complex_,baseline,field,presentation=presentation)
                if not _gauge_matches(original,changed,dict(presentation.gauges)) or not _pairing_exact(changed):
                    return ControlStage(False)
        mixed = FramePresentation(tuple((x,complex_.d4_actions[(3*i+1)%8]) for i,x in enumerate(complex_.labels)))
        changed = construct_transport(complex_,baseline,field,presentation=mixed)
        if not _gauge_matches(original,changed,dict(mixed.gauges)):
            return ControlStage(False)
        values,passed = _curvatures_and_checks(complex_,baseline,changed)
        plain,pplain = _curvatures_and_checks(complex_,baseline,original)
        gauges = dict(mixed.gauges)
        if not passed or not pplain or values != tuple(matmul(gauges[c[0]],matmul(k,transpose(gauges[c[0]]))) for c,k in zip(complex_.cycles,plain)):
            return ControlStage(False)
        field = impulse_field(L,0)
        original = construct_transport(complex_,baseline,field)
        for permutation in (tuple((2*i+3)%(L*L) for i in range(L*L)),tuple(1000-13*i for i in range(L*L))):
            if not _relabel_exact(complex_,baseline,field,original,permutation,0):
                return ControlStage(False)
    return ControlStage(True)


def _nonflat(result):
    return (result.all_covariances_exact and len(result.curvatures) == result.L**2 and
            sum(value != ZERO for value in result.curvatures) == 12 and
            dict(result.invariant_counts) == {Fraction(1,16):4,Fraction(1,64):8,Fraction(0):result.L**2-12})


def constant_null_control():
    retained = []
    for L in (5,7):
        for value in (Fraction(0),Fraction(7,3)):
            result = constant_control(L,value)
            transport = _evaluated(L,(value,)*(L*L),None)[0]
            if not (result.all_covariances_exact and result.invariant_counts == ((Fraction(0),L*L),) and
                    all(k == ZERO for k in result.curvatures) and
                    all(k == ZERO for _,k in transport.source_endomorphisms) and
                    all(k == ZERO for _,k in transport.tangent_deltas)):
                return ControlStage(False,tuple(retained))
            if value:
                retained.append(result)
    return ControlStage(True,tuple(retained))


def l5_nonflat_control():
    result = impulse_control(5,0,Fraction(1))
    return ControlStage(_nonflat(result),(result,))


def every_root_equivalence_control():
    results = tuple(impulse_control(5,r,Fraction(1)) for r in range(1,25))
    return ControlStage(all(_nonflat(r) for r in results),results)


def l7_holdout_control():
    results = tuple(impulse_control(7,r,Fraction(1)) for r in range(49))
    return ControlStage(all(_nonflat(r) for r in results),(results[0],))


def scale_control():
    retained = []
    for L in (5,7):
        unit = impulse_control(L,0,Fraction(1))
        unit_transport = _evaluated(L,impulse_field(L,0),None)[0]
        for amplitude in (Fraction(1),Fraction(7,3)):
            result = impulse_control(L,0,amplitude)
            changed = _evaluated(L,impulse_field(L,0,amplitude),None)[0]
            if not (unit.all_covariances_exact and result.all_covariances_exact and
                    result.curvatures == tuple(scale(amplitude,k) for k in unit.curvatures) and
                    dict(result.invariant_counts) == {amplitude**2*k:n for k,n in unit.invariant_counts} and
                    all(getattr(changed,name) == tuple((edge,scale(amplitude,k)) for edge,k in getattr(unit_transport,name))
                        for name in ('source_endomorphisms','tangent_deltas','cotangent_pullback_deltas'))):
                return ControlStage(False,tuple(retained))
            if L == 5 and amplitude == Fraction(7,3):
                retained.append(result)
    return ControlStage(True,tuple(retained))


def superposition_control(L: int, left: tuple[Fraction,...], right: tuple[Fraction,...],
                          a: Fraction, b: Fraction) -> bool:
    _size(L)
    a,b = _exact(a),_exact(b)
    complex_,baseline = _carrier(L)
    validate_exact_field(complex_,left)
    validate_exact_field(complex_,right)
    combined = tuple(a*x+b*y for x,y in zip(left,right))
    evaluated = tuple(_evaluated(L,field,None) for field in (left,right,combined))
    (lt,lk,lp),(rt,rk,rp),(ct,ck,cp) = evaluated
    return (lp and rp and cp and ck == tuple(add(scale(a,x),scale(b,y)) for x,y in zip(lk,rk)) and
            all(getattr(ct,name) == tuple((edge,add(scale(a,x),scale(b,y)))
                for (edge,x),(_,y) in zip(getattr(lt,name),getattr(rt,name)))
                for name in ('source_endomorphisms','tangent_deltas','cotangent_pullback_deltas')))


def superposition_stage():
    return ControlStage(all(superposition_control(L,impulse_field(L,0),impulse_field(L,7),
                                                  Fraction(2,3),Fraction(-5,7)) for L in (5,7)))


class ControlExecutionError(Exception):
    """Preserve the first failed executor and its original exception cause."""
    def __init__(self, stage, error):
        self.stage = stage
        super().__init__(f"{stage}: {type(error).__name__}: {error}")


def run_control_family(executors: ControlExecutors | None = None) -> ControlFamily:
    executors = ControlExecutors.default() if executors is None else executors
    stages = ('covariance','constant_null','l5_nonflat','every_root_equivalent',
              'l7_holdout_nonflat','scale_exact','superposition_exact')
    values = dict.fromkeys(('covariance_exact',)+stages[1:])
    results = []
    failed = None
    for name in stages:
        try:
            stage = getattr(executors,name)()
            if not isinstance(stage,ControlStage) or type(stage.passed) is not bool:
                raise TypeError('executors must return ControlStage with a boolean verdict')
        except Exception as error:
            raise ControlExecutionError(name, error) from error
        values['covariance_exact' if name == 'covariance' else name] = stage.passed
        results.extend(stage.results)
        if not stage.passed:
            failed = name
            break
    return ControlFamily(**values,results=tuple(results),failed_stage=failed)
