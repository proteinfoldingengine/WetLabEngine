from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from itertools import combinations, permutations, product
from math import isqrt

from exact_algebra import identity, matmul, nullspace, rank, transpose

Vector2 = tuple[Fraction, Fraction]
Matrix2 = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]


class ConnectionStatus(str, Enum):
    IDENTIFIABLE = "IDENTIFIABLE"
    NOT_IDENTIFIABLE = "NOT_IDENTIFIABLE"


@dataclass(frozen=True)
class OperationalComplex:
    labels: tuple[int, ...]
    work: tuple[tuple[Fraction, ...], ...]
    neighbors: frozenset[frozenset[int]]
    adjacency: tuple[tuple[int, ...], ...]
    cycles: tuple[tuple[int, int, int, int], ...]
    directed_edges: tuple[tuple[int, int], ...]
    direction_classes: tuple[Vector2, ...]
    tangent_rank: int
    local_vectors: tuple[tuple[tuple[int, Vector2], ...], ...]
    d4_actions: tuple[Matrix2, ...]
    metric_automorphisms: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class OperationalComplexAudit:
    status: ConnectionStatus
    reason: str | None
    complex: OperationalComplex | None


@dataclass(frozen=True)
class BaselineConnection:
    labels: tuple[int, ...]
    directed_edges: tuple[tuple[int, int], ...]
    transports: tuple[tuple[tuple[int, int], Matrix2], ...]
    transport_candidate_counts: tuple[int, ...]
    gauge_orbit_count: int
    holonomy_classes: tuple[tuple[Matrix2, ...], ...]
    identity: Matrix2
    identity_class: tuple[Matrix2, ...]
    flat: bool
    d4_actions: tuple[Matrix2, ...]


@dataclass(frozen=True)
class BaselineConnectionAudit:
    status: ConnectionStatus
    reason: str | None
    connection: BaselineConnection | None


def _exact_work(work, count):
    rows = tuple(tuple(row) for row in work)
    if len(rows) != count or any(len(row) != count for row in rows):
        raise ValueError("work matrix dimension mismatch")
    if any(
        isinstance(value, bool) or not isinstance(value, (int, Fraction))
        for row in rows
        for value in row
    ):
        raise TypeError("work requires exact integer or Fraction entries")
    return tuple(tuple(Fraction(value) for value in row) for row in rows)


def _canonical_cycle(vertices):
    vertices = tuple(vertices)
    rotations = tuple(vertices[i:] + vertices[:i] for i in range(4))
    reversed_vertices = tuple(reversed(vertices))
    reverse_rotations = tuple(
        reversed_vertices[i:] + reversed_vertices[:i] for i in range(4)
    )
    return min(rotations + reverse_rotations)


def _cycles(labels, adjacency):
    found = set()
    for first in labels:
        for second in adjacency[first]:
            for third in adjacency[second]:
                if third in (first, second) or third in adjacency[first]:
                    continue
                for fourth in adjacency[third]:
                    if fourth in (first, second, third):
                        continue
                    if first not in adjacency[fourth] or fourth in adjacency[second]:
                        continue
                    found.add(_canonical_cycle((first, second, third, fourth)))
    return tuple(sorted(found))


def _d4_actions():
    actions = set()
    for swap in (False, True):
        for signs in product((-1, 1), repeat=2):
            if swap:
                matrix = (
                    (Fraction(0), Fraction(signs[0])),
                    (Fraction(signs[1]), Fraction(0)),
                )
            else:
                matrix = (
                    (Fraction(signs[0]), Fraction(0)),
                    (Fraction(0), Fraction(signs[1])),
                )
            actions.add(matrix)
    return tuple(sorted(actions))


def _matvec2(matrix, vector):
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def _det(left, right):
    return left[0] * right[1] - left[1] * right[0]


def _basis_coordinates(first, second, vector):
    determinant = _det(first, second)
    if determinant == 0:
        raise ValueError("dependent tangent basis")
    return (
        (vector[0] * second[1] - first[1] * vector[1]) / determinant,
        (first[0] * vector[1] - vector[0] * second[0]) / determinant,
    )


def _tangent_data(labels, adjacency, cycles, opposite_pairs):
    directed_edges = tuple(
        (label, neighbor) for label in labels for neighbor in adjacency[label]
    )
    edge_index = {edge: index for index, edge in enumerate(directed_edges)}
    relations = []
    for first, second in sorted(
        tuple(sorted(edge)) for edge in {
            frozenset((x, y)) for x, y in directed_edges
        }
    ):
        row = [Fraction(0)] * len(directed_edges)
        row[edge_index[(first, second)]] = Fraction(1)
        row[edge_index[(second, first)]] = Fraction(1)
        relations.append(tuple(row))
    for first, second, third, fourth in cycles:
        for positive, negative in (
            ((first, second), (fourth, third)),
            ((second, third), (first, fourth)),
        ):
            row = [Fraction(0)] * len(directed_edges)
            row[edge_index[positive]] = Fraction(1)
            row[edge_index[negative]] = Fraction(-1)
            relations.append(tuple(row))
    for center in labels:
        for pair in opposite_pairs[center]:
            first, second = sorted(pair)
            for incoming, outgoing in ((first, second), (second, first)):
                row = [Fraction(0)] * len(directed_edges)
                row[edge_index[(incoming, center)]] = Fraction(1)
                row[edge_index[(center, outgoing)]] = Fraction(-1)
                relations.append(tuple(row))
    tangent_rank = len(directed_edges) - rank(tuple(relations))
    if tangent_rank != 2:
        return directed_edges, (), tangent_rank, ()
    dual_basis = nullspace(tuple(relations))
    raw = tuple(
        (dual_basis[0][index], dual_basis[1][index])
        for index in range(len(directed_edges))
    )
    root = labels[0]
    root_vectors = [raw[edge_index[(root, neighbor)]] for neighbor in adjacency[root]]
    basis_pair = next(
        ((left, right) for left, right in combinations(root_vectors, 2) if _det(left, right)),
        None,
    )
    if basis_pair is None:
        return directed_edges, (), tangent_rank, ()
    normalized = tuple(
        _basis_coordinates(basis_pair[0], basis_pair[1], vector) for vector in raw
    )
    local_vectors = tuple(
        tuple((neighbor, normalized[edge_index[(label, neighbor)]]) for neighbor in adjacency[label])
        for label in labels
    )
    standard = {
        (Fraction(1), Fraction(0)),
        (Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(-1)),
    }
    if any({vector for _neighbor, vector in row} != standard for row in local_vectors):
        return directed_edges, normalized, tangent_rank, ()
    return directed_edges, normalized, tangent_rank, local_vectors


def _metric_automorphisms(labels, work, neighbors, adjacency, local_vectors, d4):
    position = {label: index for index, label in enumerate(labels)}
    vectors = {
        (label, neighbor): vector
        for label, row in zip(labels, local_vectors)
        for neighbor, vector in row
    }
    root = labels[0]
    accepted = set()
    for target in labels:
        for action in d4:
            mapping = {root: target}
            queue = deque([root])
            valid = True
            while queue and valid:
                current = queue.popleft()
                image = mapping[current]
                image_by_vector = {
                    vectors[(image, neighbor)]: neighbor for neighbor in adjacency[image]
                }
                for neighbor in adjacency[current]:
                    desired = _matvec2(action, vectors[(current, neighbor)])
                    changed = image_by_vector.get(desired)
                    if changed is None:
                        valid = False
                        break
                    if neighbor in mapping and mapping[neighbor] != changed:
                        valid = False
                        break
                    if neighbor not in mapping:
                        mapping[neighbor] = changed
                        queue.append(neighbor)
            if not valid or len(mapping) != len(labels) or len(set(mapping.values())) != len(labels):
                continue
            image = tuple(mapping[label] for label in labels)
            if any(
                work[i][j] != work[position[image[i]]][position[image[j]]]
                for i in range(len(labels))
                for j in range(len(labels))
            ):
                continue
            if frozenset(
                frozenset((mapping[first], mapping[second]))
                for first, second in (tuple(edge) for edge in neighbors)
            ) != neighbors:
                continue
            accepted.add(image)
    return tuple(sorted(accepted))


def _stop(reason):
    return OperationalComplexAudit(ConnectionStatus.NOT_IDENTIFIABLE, reason, None)


def construct_operational_complex(labels, work, neighbors) -> OperationalComplexAudit:
    labels = tuple(labels)
    if len(labels) < 2:
        raise ValueError("at least two labels required")
    if any(isinstance(label, bool) or not isinstance(label, int) for label in labels):
        raise TypeError("integer labels required")
    if len(set(labels)) != len(labels):
        raise ValueError("duplicate labels")
    work = _exact_work(work, len(labels))
    position = {label: index for index, label in enumerate(labels)}
    parsed_edges = set()
    for edge in neighbors:
        edge = frozenset(edge)
        if len(edge) != 2:
            raise ValueError("simple two-label edges required")
        if any(label not in position for label in edge):
            raise ValueError("edge label outside carrier")
        parsed_edges.add(edge)
    neighbors = frozenset(parsed_edges)
    adjacency_map = {label: set() for label in labels}
    for edge in neighbors:
        first, second = tuple(edge)
        adjacency_map[first].add(second)
        adjacency_map[second].add(first)
    if any(len(adjacency_map[label]) != 4 for label in labels):
        return _stop("degree_not_four")
    seen = {labels[0]}
    queue = deque([labels[0]])
    while queue:
        for neighbor in adjacency_map[queue.popleft()]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    if len(seen) != len(labels):
        return _stop("disconnected")
    cycles = _cycles(labels, adjacency_map)
    counts = {edge: 0 for edge in neighbors}
    for cycle in cycles:
        for index in range(4):
            counts[frozenset((cycle[index], cycle[(index + 1) % 4]))] += 1
    if any(count != 2 for count in counts.values()):
        return _stop("edge_cycle_count")
    side = isqrt(len(labels))
    if side * side == len(labels) and side % 2 == 1 and len(cycles) != len(labels):
        return _stop("cycle_count")
    adjacency = tuple(tuple(sorted(adjacency_map[label])) for label in labels)
    all_off_diagonal = [
        work[i][j] for i in range(len(labels)) for j in range(i + 1, len(labels))
    ]
    minimum = min(all_off_diagonal)
    opposite_pairs = {}
    for label in labels:
        row = adjacency_map[label]
        pairs = tuple(combinations(sorted(row), 2))
        values = {
            pair: work[position[pair[0]]][position[pair[1]]] for pair in pairs
        }
        maximum = max(values.values())
        maxima = tuple(pair for pair in pairs if values[pair] == maximum)
        if len(maxima) != 2 or set(maxima[0]) | set(maxima[1]) != set(row) or set(maxima[0]) & set(maxima[1]):
            return _stop("opposites_ambiguous")
        if any(work[position[label]][position[neighbor]] != minimum for neighbor in row):
            return _stop("radial_work_not_minimum")
        opposite_pairs[label] = frozenset(frozenset(pair) for pair in maxima)
    directed_edges, directions, tangent_rank, local_vectors = _tangent_data(
        labels, adjacency_map, cycles, opposite_pairs
    )
    if tangent_rank != 2 or not local_vectors:
        return _stop("tangent_rank_not_two")
    direction_lookup = {
        edge: direction for edge, direction in zip(directed_edges, directions)
    }
    for label, pairs in opposite_pairs.items():
        derived = frozenset(
            frozenset((first, second))
            for first, second in combinations(adjacency_map[label], 2)
            if direction_lookup[(label, first)]
            == tuple(-value for value in direction_lookup[(label, second)])
        )
        if derived != pairs:
            return _stop("opposites_quotient_mismatch")
    d4 = _d4_actions()
    automorphisms = _metric_automorphisms(
        labels, work, neighbors, adjacency_map, local_vectors, d4
    )
    if not automorphisms:
        return _stop("metric_automorphism_failure")
    complex_ = OperationalComplex(
        labels,
        work,
        neighbors,
        adjacency,
        cycles,
        directed_edges,
        directions,
        tangent_rank,
        local_vectors,
        d4,
        automorphisms,
    )
    return OperationalComplexAudit(ConnectionStatus.IDENTIFIABLE, None, complex_)


def _conjugacy_class(matrix, actions):
    values = {
        matmul(matmul(action, matrix), transpose(action)) for action in actions
    }
    return tuple(sorted(values))


def cycle_holonomy(connection: BaselineConnection, cycle, orientation=1):
    cycle = tuple(cycle)
    if len(cycle) != 4 or len(set(cycle)) != 4:
        raise ValueError("four distinct cycle labels required")
    if orientation not in (-1, 1):
        raise ValueError("orientation must be +1 or -1")
    if orientation == -1:
        cycle = (cycle[0], cycle[3], cycle[2], cycle[1])
    transports = dict(connection.transports)
    result = connection.identity
    for index in range(4):
        edge = (cycle[index], cycle[(index + 1) % 4])
        if edge not in transports:
            raise ValueError("cycle edge missing from connection")
        result = matmul(transports[edge], result)
    return result


def enumerate_baseline_connection(complex_: OperationalComplex):
    if not isinstance(complex_, OperationalComplex):
        raise TypeError("OperationalComplex required")
    unit = identity(2)
    direction = dict(zip(complex_.directed_edges, complex_.direction_classes))
    candidate_counts = []
    for edge in complex_.directed_edges:
        candidates = set()
        for source_frame in complex_.d4_actions:
            for target_frame in complex_.d4_actions:
                transport = matmul(target_frame, transpose(source_frame))
                source_vector = _matvec2(source_frame, direction[edge])
                target_vector = _matvec2(target_frame, direction[edge])
                if _matvec2(transport, source_vector) != target_vector:
                    return BaselineConnectionAudit(
                        ConnectionStatus.NOT_IDENTIFIABLE,
                        "forward_transport_failure",
                        None,
                    )
                if matmul(transpose(transport), transport) != unit:
                    return BaselineConnectionAudit(
                        ConnectionStatus.NOT_IDENTIFIABLE,
                        "metric_transport_failure",
                        None,
                    )
                candidates.add(transport)
        if candidates != set(complex_.d4_actions):
            return BaselineConnectionAudit(
                ConnectionStatus.NOT_IDENTIFIABLE,
                "transport_orbit_failure",
                None,
            )
        candidate_counts.append(len(candidates))
    transports = tuple((edge, unit) for edge in complex_.directed_edges)
    candidate_counts = tuple(candidate_counts)
    provisional = BaselineConnection(
        complex_.labels,
        complex_.directed_edges,
        transports,
        candidate_counts,
        1,
        (),
        unit,
        _conjugacy_class(unit, complex_.d4_actions),
        False,
        complex_.d4_actions,
    )
    classes = tuple(
        _conjugacy_class(
            cycle_holonomy(provisional, cycle, 1), complex_.d4_actions
        )
        for cycle in complex_.cycles
    )
    for cycle in complex_.cycles:
        forward = cycle_holonomy(provisional, cycle, 1)
        reverse = cycle_holonomy(provisional, cycle, -1)
        if reverse != transpose(forward):
            return BaselineConnectionAudit(
                ConnectionStatus.NOT_IDENTIFIABLE,
                "orientation_inverse_failure",
                None,
            )
    flat = all(conjugacy_class == provisional.identity_class for conjugacy_class in classes)
    connection = BaselineConnection(
        provisional.labels,
        provisional.directed_edges,
        provisional.transports,
        provisional.transport_candidate_counts,
        provisional.gauge_orbit_count,
        classes,
        provisional.identity,
        provisional.identity_class,
        flat,
        provisional.d4_actions,
    )
    return BaselineConnectionAudit(ConnectionStatus.IDENTIFIABLE, None, connection)
