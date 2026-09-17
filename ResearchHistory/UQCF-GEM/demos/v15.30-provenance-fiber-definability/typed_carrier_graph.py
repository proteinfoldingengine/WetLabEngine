from __future__ import annotations

from dataclasses import asdict, dataclass
from collections import deque

import frozen_inputs as fi

_CERTIFYING_CLASSES = {
    'CERTIFIED_PROVENANCE_RELATION',
    'CERTIFIED_GAUGE_OR_EQUIVALENCE',
    'CERTIFIED_PROJECTION_TO_Q',
    'CERTIFIED_ACTION',
}


@dataclass(frozen=True)
class TypedEdge:
    source: str
    target: str
    relation_class: str
    evidence_key: str
    synthetic: bool = False


@dataclass(frozen=True)
class CarrierConnection:
    candidate_domain: str
    torus_domain: str
    direct_path: tuple[TypedEdge, ...]
    common_node: str | None
    common_node_kind: str | None
    real_certified: bool
    reason: str


class CarrierGraph:
    def __init__(self) -> None:
        self._edges: list[TypedEdge] = []
        self._nodes: set[str] = set()
        self._untyped_notes: list[str] = []

    def add_node(self, node: str) -> None:
        self._nodes.add(node)

    def add_edge(self, edge: TypedEdge) -> None:
        self._nodes.add(edge.source)
        self._nodes.add(edge.target)
        self._edges.append(edge)

    def add_untyped_note(self, text: str) -> None:
        self._untyped_notes.append(str(text))

    def nodes(self) -> tuple[str, ...]:
        return tuple(sorted(self._nodes))

    def edges(self) -> tuple[TypedEdge, ...]:
        return tuple(self._edges)

    def _neighbors(self, node: str, real_only: bool) -> tuple[TypedEdge, ...]:
        return tuple(
            edge for edge in self._edges
            if edge.source == node
            and relation_class_is_certifying(edge.relation_class)
            and (not real_only or not edge.synthetic)
        )

    def certified_path(
        self, source: str, target: str, real_only: bool = True
    ) -> tuple[TypedEdge, ...]:
        if source == target:
            return ()
        queue = deque([(source, ())])
        seen = {source}
        while queue:
            node, path = queue.popleft()
            for edge in self._neighbors(node, real_only):
                new_path = path + (edge,)
                if edge.target == target:
                    return new_path
                if edge.target not in seen:
                    seen.add(edge.target)
                    queue.append((edge.target, new_path))
        return ()

    def has_certified_path(
        self, source: str, target: str, real_only: bool = True
    ) -> bool:
        return bool(self.certified_path(source, target, real_only=real_only))


def relation_class_is_certifying(name: str) -> bool:
    return name in _CERTIFYING_CLASSES


def _connection(
    candidate_domain: str,
    torus_domain: str,
    direct_path: tuple[TypedEdge, ...] = (),
    common_node: str | None = None,
    common_node_kind: str | None = None,
    reason: str = 'NO_CERTIFIED_TYPED_CONNECTION',
) -> CarrierConnection:
    edges = direct_path
    real_certified = bool(edges) and not any(edge.synthetic for edge in edges)
    return CarrierConnection(
        candidate_domain=candidate_domain,
        torus_domain=torus_domain,
        direct_path=direct_path,
        common_node=common_node,
        common_node_kind=common_node_kind,
        real_certified=real_certified,
        reason=reason,
    )


def _all_paths_real(paths: tuple[tuple[TypedEdge, ...], ...]) -> bool:
    return all(path and not any(edge.synthetic for edge in path) for path in paths)


def find_typed_connection(
    graph: CarrierGraph,
    candidate_domain: str,
    torus_domain: str,
    real_only: bool = True,
) -> CarrierConnection:
    direct = graph.certified_path(candidate_domain, torus_domain, real_only=real_only)
    if direct:
        return _connection(
            candidate_domain, torus_domain, direct_path=direct,
            reason='CERTIFIED_DIRECT_PATH_CANDIDATE_TO_TORUS',
        )

    reverse = graph.certified_path(torus_domain, candidate_domain, real_only=real_only)
    if reverse:
        real = not any(edge.synthetic for edge in reverse)
        return CarrierConnection(
            candidate_domain=candidate_domain,
            torus_domain=torus_domain,
            direct_path=reverse,
            common_node=None,
            common_node_kind=None,
            real_certified=real,
            reason='CERTIFIED_DIRECT_PATH_TORUS_TO_CANDIDATE',
        )

    for node in graph.nodes():
        if node in {candidate_domain, torus_domain}:
            continue
        to_candidate = graph.certified_path(node, candidate_domain, real_only=real_only)
        to_torus = graph.certified_path(node, torus_domain, real_only=real_only)
        if to_candidate and to_torus:
            paths = (to_candidate, to_torus)
            return CarrierConnection(
                candidate_domain=candidate_domain,
                torus_domain=torus_domain,
                direct_path=to_candidate + to_torus,
                common_node=node,
                common_node_kind='PARENT',
                real_certified=_all_paths_real(paths),
                reason='CERTIFIED_COMMON_PARENT',
            )

        from_candidate = graph.certified_path(candidate_domain, node, real_only=real_only)
        from_torus = graph.certified_path(torus_domain, node, real_only=real_only)
        if from_candidate and from_torus:
            paths = (from_candidate, from_torus)
            return CarrierConnection(
                candidate_domain=candidate_domain,
                torus_domain=torus_domain,
                direct_path=from_candidate + from_torus,
                common_node=node,
                common_node_kind='QUOTIENT',
                real_certified=_all_paths_real(paths),
                reason='CERTIFIED_COMMON_QUOTIENT',
            )

    return _connection(candidate_domain, torus_domain)


def build_real_graph() -> tuple[CarrierGraph, tuple[fi.CandidateEvidence, ...]]:
    modules = fi.load_v1529()
    candidates = fi.candidate_inventory(fi.REPO_ROOT)
    graph = CarrierGraph()

    graph.add_node('TORUS_EDGE_REPRESENTATIVE')
    graph.add_node('Q_SOURCE_QUOTIENT')
    graph.add_edge(TypedEdge(
        source='TORUS_EDGE_REPRESENTATIVE',
        target='Q_SOURCE_QUOTIENT',
        relation_class='CERTIFIED_PROJECTION_TO_Q',
        evidence_key='v15.29-fiber-model:B1',
        synthetic=False,
    ))

    for candidate in candidates:
        graph.add_node(candidate.domain)

    for record in modules.provenance_inventory.frozen_inventory(
        modules.provenance_inventory.REPO_ROOT
    ):
        if not relation_class_is_certifying(record.relation_class):
            graph.add_untyped_note(
                f'{record.key}:{record.relation_class}:{record.domain}->{record.codomains}'
            )
            continue
        if record.relation_class == 'CERTIFIED_ACTION' and not record.certifies_action:
            graph.add_untyped_note(f'{record.key}:action-metadata-without-action-certificate')
            continue
        for codomain in record.codomains:
            graph.add_edge(TypedEdge(
                source=record.domain,
                target=codomain,
                relation_class=record.relation_class,
                evidence_key=record.key,
                synthetic=False,
            ))
            if record.relation_class == 'CERTIFIED_GAUGE_OR_EQUIVALENCE':
                graph.add_edge(TypedEdge(
                    source=codomain,
                    target=record.domain,
                    relation_class=record.relation_class,
                    evidence_key=record.key,
                    synthetic=False,
                ))

    return graph, candidates


def audit_candidate_common_carrier(
    candidate: fi.CandidateEvidence, graph: CarrierGraph
) -> dict:
    connection = find_typed_connection(
        graph, candidate.domain, 'TORUS_EDGE_REPRESENTATIVE', real_only=True
    )
    return {
        'candidate': candidate.key,
        'typed_common_carrier': connection.real_certified,
        'connection': asdict(connection),
    }


def synthetic_supplied_embedding_graph() -> CarrierGraph:
    graph = CarrierGraph()
    graph.add_edge(TypedEdge(
        source='SYNTHETIC_PROVENANCE',
        target='TORUS_EDGE_REPRESENTATIVE',
        relation_class='CERTIFIED_PROVENANCE_RELATION',
        evidence_key='synthetic-supplied-embedding',
        synthetic=True,
    ))
    return graph


def synthetic_common_parent_graph() -> CarrierGraph:
    graph = CarrierGraph()
    graph.add_edge(TypedEdge(
        source='SYNTHETIC_PARENT',
        target='SYNTHETIC_PROVENANCE',
        relation_class='CERTIFIED_PROVENANCE_RELATION',
        evidence_key='synthetic-parent-to-provenance',
        synthetic=True,
    ))
    graph.add_edge(TypedEdge(
        source='SYNTHETIC_PARENT',
        target='TORUS_EDGE_REPRESENTATIVE',
        relation_class='CERTIFIED_PROVENANCE_RELATION',
        evidence_key='synthetic-parent-to-torus',
        synthetic=True,
    ))
    return graph
