from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UniquenessResult:
    status: str
    signatures: tuple[tuple[int, ...], ...]
    witness_pair: tuple[tuple[int, ...], tuple[int, ...]] | None

    def __post_init__(self) -> None:
        if self.status not in {'NONE', 'UNIQUE', 'MULTIPLE'}:
            raise ValueError(f'unknown uniqueness status: {self.status}')
        if self.status == 'NONE' and (self.signatures or self.witness_pair is not None):
            raise ValueError('NONE status cannot carry signatures')
        if self.status == 'UNIQUE' and (len(self.signatures) != 1 or self.witness_pair is not None):
            raise ValueError('UNIQUE status requires exactly one signature')
        if self.status == 'MULTIPLE':
            if len(self.signatures) < 2 or self.witness_pair is None:
                raise ValueError('MULTIPLE status requires at least two signatures and a witness pair')
            if self.witness_pair[0] == self.witness_pair[1]:
                raise ValueError('nonuniqueness witness pair must be inequivalent')


def canonical_partition_signature(labels) -> tuple[int, ...]:
    ids = {}
    next_id = 0
    out = []
    for label in tuple(labels):
        if label not in ids:
            ids[label] = next_id
            next_id += 1
        out.append(ids[label])
    return tuple(out)


def relations_inequivalent(a, b) -> bool:
    return canonical_partition_signature(a) != canonical_partition_signature(b)


def classify_relation_family(labelings) -> UniquenessResult:
    signatures = []
    seen = set()
    for labels in tuple(labelings):
        signature = canonical_partition_signature(labels)
        if signature not in seen:
            seen.add(signature)
            signatures.append(signature)

    frozen = tuple(signatures)
    if not frozen:
        return UniquenessResult('NONE', (), None)
    if len(frozen) == 1:
        return UniquenessResult('UNIQUE', frozen, None)
    return UniquenessResult('MULTIPLE', frozen, (frozen[0], frozen[1]))
