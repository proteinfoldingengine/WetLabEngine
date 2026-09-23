"""Exact presentation-covariance checks for the compact v15.45 operator."""
from __future__ import annotations
from dataclasses import replace
from fractions import Fraction
import sys

from evidence import actual_carriers, reference_operator
from factorization import compact_operator

transport = sys.modules["transport"]
holonomy = sys.modules["holonomy"]
operational = sys.modules["operational_complex"]
exact = sys.modules["exact_algebra"]

FramePresentation = transport.FramePresentation


def _mat_at(operator, face, col):
    return tuple(tuple(operator.entries[4*face+2*i+j][col] for j in range(2))
                 for i in range(2))


def _transform(g, matrix):
    return exact.matmul(exact.matmul(g, matrix), exact.transpose(g))


def gauge_assignments(carrier):
    actions = tuple(sorted(carrier.complex.d4_actions))
    labels = carrier.complex.labels
    unit = exact.identity(2)
    for index, action in enumerate(actions):
        yield ("uniform", index), FramePresentation(
            tuple((label, action) for label in labels))
    for label in labels:
        for index, action in enumerate(actions):
            yield ("site", label, index), FramePresentation(
                tuple((x, action if x == label else unit) for x in labels))


def _verify_gauges(carrier, baseline):
    compared = 0
    for _key, presentation in gauge_assignments(carrier):
        presented = reference_operator(carrier, presentation)
        gauges = dict(presentation.gauges)
        for face, cycle in enumerate(baseline.cycles):
            g = gauges[cycle[0]]
            for col in range(len(baseline.labels)):
                if _mat_at(presented, face, col) != _transform(g, _mat_at(baseline, face, col)):
                    raise ValueError("gauge_alignment")
                compared += 1
    return compared


def _verify_orientations(carrier, baseline):
    n = len(baseline.labels)
    fields = tuple(tuple(Fraction(j == col) for j in range(n)) for col in range(n))
    transports = tuple(transport.construct_transport(
        carrier.complex, carrier.baseline, field) for field in fields)
    p = dict(carrier.baseline.transports)
    compared = 0
    for face, cycle in enumerate(baseline.cycles):
        path = exact.identity(2)
        for rotation in range(4):
            forward = cycle[rotation:] + cycle[:rotation]
            reversed_cycle = (forward[0],) + tuple(reversed(forward[1:]))
            for oriented, sign in ((forward, 1), (reversed_cycle, -1)):
                for col in range(n):
                    expected = _transform(path, _mat_at(baseline, face, col))
                    expected = tuple(tuple(Fraction(sign) * v for v in row) for row in expected)
                    actual = holonomy.linearized_holonomy(
                        carrier.baseline, transports[col], oriented)
                    if actual != expected:
                        raise ValueError("orientation_alignment")
                    compared += 1
            path = exact.matmul(
                p[(cycle[rotation], cycle[(rotation+1) % 4])], path)
    return compared


def _relabel_carrier(carrier, permutation):
    old = carrier.complex
    if len(permutation) != len(old.labels) or set(permutation) != set(old.labels):
        raise ValueError("invalid_label_permutation")
    names = dict(zip(old.labels, permutation, strict=True))
    labels = tuple(sorted(permutation))
    old_index = {label: j for j, label in enumerate(old.labels)}
    reverse = {new: old_label for old_label, new in names.items()}
    work = tuple(tuple(old.work[old_index[reverse[x]]][old_index[reverse[y]]]
                       for y in labels) for x in labels)
    neighbors = frozenset(frozenset(names[v] for v in pair) for pair in old.neighbors)
    audit = operational.construct_operational_complex(labels, work, neighbors)
    if audit.complex is None:
        raise ValueError("relabel_complex")
    baseline_audit = operational.enumerate_baseline_connection(audit.complex)
    if baseline_audit.connection is None:
        raise ValueError("relabel_baseline")
    return replace(carrier, complex=audit.complex, baseline=baseline_audit.connection), names


def _frame_alignment(original, changed, names):
    source, target = original.complex, changed.complex
    target_dirs = dict(zip(target.directed_edges, target.direction_classes, strict=True))
    source_dirs = dict(zip(source.directed_edges, source.direction_classes, strict=True))
    gauges = {}
    for label in source.labels:
        edges = tuple(edge for edge in source.directed_edges if edge[0] == label)
        matches = []
        for action in source.d4_actions:
            okay = True
            for edge in edges:
                vector = source_dirs[edge]
                mapped = tuple(sum(action[i][j] * vector[j] for j in range(2))
                               for i in range(2))
                if mapped != target_dirs.get((names[edge[0]], names[edge[1]])):
                    okay = False
                    break
            if okay:
                matches.append(action)
        if len(matches) != 1:
            raise ValueError("direction_frame_alignment")
        gauges[label] = matches[0]
    return gauges


def _verify_relabel(original, changed, before, after, names):
    gauges = _frame_alignment(original, changed, names)
    faces = {frozenset(cycle): j for j, cycle in enumerate(after.cycles)}
    p = dict(changed.baseline.transports)
    target_columns = {label: j for j, label in enumerate(after.labels)}
    compared = 0
    for face, cycle in enumerate(before.cycles):
        mapped = tuple(names[x] for x in cycle)
        other = faces[frozenset(mapped)]
        canonical = after.cycles[other]
        path = exact.identity(2)
        aligned = None
        for r in range(4):
            rotated = canonical[r:] + canonical[:r]
            if mapped == rotated:
                aligned = (path, 1); break
            if mapped == (rotated[0],) + tuple(reversed(rotated[1:])):
                aligned = (path, -1); break
            path = exact.matmul(p[(canonical[r], canonical[(r+1) % 4])], path)
        if aligned is None:
            raise ValueError("face_cycle_alignment")
        path, sign = aligned
        for col, label in enumerate(before.labels):
            dest = target_columns[names[label]]
            new_matrix = _mat_at(after, other, dest)
            lhs = _transform(path, new_matrix)
            lhs = tuple(tuple(Fraction(sign) * v for v in row) for row in lhs)
            rhs = _transform(gauges[cycle[0]], _mat_at(before, face, col))
            if lhs != rhs:
                raise ValueError("relabel_alignment")
            compared += 1
    return compared


def reject_raw_mismatch(carrier):
    baseline = compact_operator(carrier)
    reflected = next(p for key, p in gauge_assignments(carrier)
                     if key[0] == "uniform" and
                     p.gauges[0][1][0][0] * p.gauges[0][1][1][1]
                     - p.gauges[0][1][0][1] * p.gauges[0][1][1][0] == -1)
    presented = reference_operator(carrier, reflected)
    if presented.entries != baseline.entries:
        raise ValueError("presentation_alignment_required")
    raise ValueError("presentation_control_not_distinct")


def check_all_presentations(carrier):
    baseline = compact_operator(carrier)
    if baseline != reference_operator(carrier):
        raise ValueError("baseline_factorization")
    gauges = _verify_gauges(carrier, baseline)
    orientations = _verify_orientations(carrier, baseline)
    changed, names = _relabel_carrier(carrier, tuple(reversed(carrier.complex.labels)))
    changed_compact = compact_operator(changed)
    if changed_compact != reference_operator(changed):
        raise ValueError("relabeled_factorization")
    relabel = _verify_relabel(carrier, changed, baseline, changed_compact, names)
    return {"L": carrier.L, "scale": str(carrier.scale),
            "gauge_comparisons": gauges,
            "orientation_comparisons": orientations,
            "relabel_comparisons": relabel, "exact": True}
