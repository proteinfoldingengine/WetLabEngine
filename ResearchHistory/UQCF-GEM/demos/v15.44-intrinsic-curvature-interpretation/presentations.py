"""Exact frame, face, label, and scale checks for intrinsic response matrices."""
from __future__ import annotations
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from contextlib import contextmanager
from functools import lru_cache
from bootstrap import load_pinned_modules, check_pure_modules, deny_archive_access
from operator_types import Operator
from derive import derive_operator, require_equal
from oracle import reference_operator
from exact_matrix import identity, matmul, transpose, apply_matrix
from kernel import analyze_kernel, verify_kernel


def _parent():
    return load_pinned_modules(Path(__file__).resolve().parents[4])


@contextmanager
def memoized_core(parent):
    """Reuse immutable exact arithmetic values while still calling the frozen core.

    Parent modules retain their original files and callables are restored even
    on failure. This cache stores matrices/vectors, never a test verdict,
    transport object, operator column, or holonomy result.
    """
    saved = []
    try:
        for module_name in ('exact_algebra', 'transport', 'holonomy'):
            module = parent[module_name]
            for name in ('matmul', 'matvec', 'add', 'scale', 'transpose'):
                if name in vars(module):
                    original = vars(module)[name]
                    saved.append((module, name, original))
                    setattr(module, name, lru_cache(maxsize=65536)(original))
        yield
    finally:
        for module, name, original in reversed(saved):
            setattr(module, name, original)


def _transform(g, matrix):
    return matmul(matmul(g, matrix), transpose(g))


def gauge_assignments(carrier):
    modules = _parent()
    frame = modules['transport'].FramePresentation
    actions = tuple(sorted(carrier.complex.d4_actions))
    labels = carrier.complex.labels
    unit = identity(2)
    for index, action in enumerate(actions):
        yield ('uniform', index), frame(tuple((label, action) for label in labels))
    for label in labels:
        for index, action in enumerate(actions):
            yield ('site', label, index), frame(tuple((x, action if x == label else unit) for x in labels))


def _face_columns(operator, face):
    return operator.entries[4*face:4*face+4]


def _matrix_at(operator, face, col):
    return tuple(tuple(operator.entries[4*face+2*i+j][col] for j in range(2)) for i in range(2))


def _require_shape(a):
    if len(a.entries) != 4*len(a.cycles) or any(len(row) != len(a.labels) for row in a.entries):
        raise ValueError('operator_shape')


def verify_gauge(carrier, before, presentation, actual=None, frozen=None):
    """Check every presented face and basis column against two independent references."""
    _require_shape(before)
    actual = derive_operator(carrier, presentation) if actual is None else actual
    frozen = reference_operator(carrier, presentation) if frozen is None else frozen
    require_equal(actual, frozen)
    gauges = dict(presentation.gauges)
    if actual.cycles != before.cycles or actual.labels != before.labels:
        raise ValueError('gauge_operator_shape')
    for face, cycle in enumerate(before.cycles):
        gauge = gauges[cycle[0]]
        for col in range(len(before.labels)):
            if _matrix_at(actual, face, col) != _transform(gauge, _matrix_at(before, face, col)):
                raise ValueError('gauge_face_conjugation')
    return len(before.labels), len(before.cycles)


def verify_orientations(carrier, before):
    _require_shape(before)
    if before.labels != carrier.complex.labels or before.cycles != carrier.complex.cycles:
        raise ValueError('orientation_operator')
    p = dict(carrier.baseline.transports)
    unit = identity(2)
    modules = _parent()
    construct = modules['transport'].construct_transport
    holonomy = modules['holonomy'].linearized_holonomy
    transports = tuple(construct(carrier.complex, carrier.baseline,
                                  tuple(Fraction(j == col) for j in range(len(before.labels))))
                       for col in range(len(before.labels)))
    compared = 0
    for face, cycle in enumerate(before.cycles):
        path = unit
        for rotation in range(4):
            forward = cycle[rotation:]+cycle[:rotation]
            for oriented, sign in ((forward, 1), ((forward[0],)+tuple(reversed(forward[1:])), -1)):
                for col in range(len(before.labels)):
                    want = _transform(path, _matrix_at(before, face, col))
                    expected = tuple(tuple(sign*entry for entry in row) for row in want)
                    if holonomy(carrier.baseline, transports[col], oriented) != expected:
                        raise ValueError('orientation_basepoint_or_reverse')
                    compared += 1
            path = matmul(p[(cycle[rotation],cycle[(rotation+1)%4])], path)
    return compared


def relabel_geometry(carrier, permutation):
    old = carrier.complex
    if len(permutation) != len(old.labels) or set(permutation) != set(old.labels):
        raise ValueError('invalid_label_permutation')
    names = dict(zip(old.labels, permutation, strict=True))
    labels = tuple(sorted(permutation))
    old_index = {label: j for j, label in enumerate(old.labels)}
    reverse = {new: old for old, new in names.items()}
    work = tuple(tuple(old.work[old_index[reverse[x]]][old_index[reverse[y]]]
                       for y in labels) for x in labels)
    neighbors = frozenset(frozenset(names[v] for v in pair) for pair in old.neighbors)
    modules = _parent()
    operational = modules['operational_complex']
    audit = operational.construct_operational_complex(labels, work, neighbors)
    if audit.complex is None: raise ValueError('relabel_complex_identification')
    baseline_audit = operational.enumerate_baseline_connection(audit.complex)
    if baseline_audit.connection is None: raise ValueError('relabel_baseline_identification')
    return replace(carrier, complex=audit.complex, baseline=baseline_audit.connection), names


def _alignment(original, changed, names):
    source, target = original.complex, changed.complex
    directions = dict(zip(target.directed_edges, target.direction_classes, strict=True))
    old_dirs = dict(zip(source.directed_edges, source.direction_classes, strict=True))
    gauges = {}
    for label in source.labels:
        matches = []
        edges = tuple(edge for edge in source.directed_edges if edge[0] == label)
        for action in source.d4_actions:
            if all(tuple(sum(action[i][j]*old_dirs[edge][j] for j in range(2)) for i in range(2))
                   == directions.get((names[edge[0]], names[edge[1]])) for edge in edges):
                matches.append(action)
        if len(matches) != 1: raise ValueError('direction_frame_alignment')
        gauges[label] = matches[0]
    before, after = dict(original.baseline.transports), dict(changed.baseline.transports)
    for (x,y), p in before.items():
        mapped = (names[x], names[y])
        if mapped not in after or after[mapped] != matmul(matmul(gauges[y], p), transpose(gauges[x])):
            raise ValueError('aligned_baseline')
    return gauges


def verify_alignment(original, changed, before, after, names, *, permute_columns=True):
    """Geometry fixes frames; face sets and oriented cycles fix rows; names fix columns."""
    _require_shape(before)
    _require_shape(after)
    gauges = _alignment(original, changed, names)
    faces = {}
    for j, cycle in enumerate(after.cycles):
        key = frozenset(cycle)
        if key in faces: raise ValueError('nonunique_face_match')
        faces[key] = j
    if len(faces) != len(before.cycles): raise ValueError('nonunique_face_match')
    p = dict(changed.baseline.transports)
    target_columns = {label: j for j, label in enumerate(after.labels)}
    comparisons = 0
    for face, cycle in enumerate(before.cycles):
        mapped = tuple(names[x] for x in cycle)
        other = faces.get(frozenset(mapped))
        if other is None: raise ValueError('nonunique_face_match')
        canonical = after.cycles[other]
        path = identity(2)
        aligned = None
        for r in range(4):
            rotated = canonical[r:]+canonical[:r]
            if mapped == rotated: aligned = (path, 1); break
            if mapped == (rotated[0],)+tuple(reversed(rotated[1:])):
                aligned = (path, -1); break
            path = matmul(p[(canonical[r], canonical[(r+1)%4])], path)
        if aligned is None: raise ValueError('face_cycle_alignment')
        path, sign = aligned
        for col, label in enumerate(before.labels):
            dest = target_columns[names[label]] if permute_columns else col
            new_matrix = _matrix_at(after, other, dest)
            canonical_aligned = tuple(tuple(sign*v for v in row) for row in _transform(path, new_matrix))
            expected = _transform(gauges[cycle[0]], _matrix_at(before, face, col))
            if canonical_aligned != expected: raise ValueError('aligned_operator')
            comparisons += 1
    return comparisons


def verify_scale(unit, scaled, before=None, after=None):
    if unit.L != scaled.L or scaled.scale/unit.scale != Fraction(7,3):
        raise ValueError('scale_carrier')
    if unit.complex.labels != scaled.complex.labels:
        raise ValueError('scale_labels')
    before = derive_operator(unit) if before is None else before
    after = derive_operator(scaled) if after is None else after
    names = {label: label for label in unit.complex.labels}
    # Compare on the same abstract field. Archived fields, rather than A, carry
    # the factor 7/3; their response and quadratic invariant are checked later.
    return verify_alignment(unit, scaled, before, after, names)


def verify_core_fields(carrier, operator, certificate=None):
    """Replay constants, an exact kernel basis, and the fixed mixed field in core."""
    certificate = analyze_kernel(operator) if certificate is None else certificate
    verify_kernel(operator, certificate)
    modules = _parent()
    construct = modules['transport'].construct_transport
    holonomy = modules['holonomy'].linearized_holonomy
    n = len(operator.labels)
    fields = ((Fraction(1),)*n,) + tuple(
        tuple(row[j] for row in certificate.null_basis)
        for j in range(certificate.nullity)) + (tuple(Fraction(j+1) for j in range(n)),)
    for values in fields:
        response = apply_matrix(operator.entries, values)
        transport = construct(carrier.complex, carrier.baseline, values)
        for face, cycle in enumerate(operator.cycles):
            matrix = holonomy(carrier.baseline, transport, cycle)
            if tuple(value for row in matrix for value in row) != response[4*face:4*face+4]:
                raise ValueError('core_field_response')
    return len(fields)


def check_presentations(carrier):
    """Complete immutable geometry receipts; timeout is controlled by the caller."""
    check_pure_modules(Path(__file__).resolve().parent)
    _parent()
    with deny_archive_access():
        baseline = derive_operator(carrier)
        certificate = analyze_kernel(baseline)
        verify_kernel(baseline, certificate)
    require_equal(baseline, reference_operator(carrier))
    core_fields = verify_core_fields(carrier, baseline, certificate)
    orientations = verify_orientations(carrier, baseline)
    relabeled, names = relabel_geometry(carrier, tuple(reversed(carrier.complex.labels)))
    aligned = verify_alignment(carrier, relabeled, baseline, derive_operator(relabeled), names)
    count = columns = faces = 0
    matrices = {}
    with memoized_core(_parent()):
        for key, presentation in gauge_assignments(carrier):
            if presentation.gauges not in matrices:
                matrices[presentation.gauges] = (derive_operator(carrier, presentation),
                                                 reference_operator(carrier, presentation))
            actual, frozen = matrices[presentation.gauges]
            col, face = verify_gauge(carrier, baseline, presentation, actual, frozen)
            count += 1; columns += col; faces += face
    return {'L': carrier.L, 'scale': carrier.scale, 'gauge_assignments': count,
            'gauge_columns': columns, 'gauge_faces': faces,
            'oriented_basis_faces': orientations, 'aligned_basis_faces': aligned,
            'core_fields': core_fields, 'rank': certificate.rank,
            'nullity': certificate.nullity, 'exact': True}
