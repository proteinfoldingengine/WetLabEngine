"""Typed finite retained carriers and fiber operations; no matrix conventions here."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True)
class Carrier:
    genesis: str
    keys: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        if not isinstance(self.genesis, str) or not self.genesis:
            raise ValueError('nonempty Genesis identifier required')
        if not isinstance(self.keys, tuple) or not self.keys:
            raise ValueError('nonempty tuple of addresses required')
        for key in self.keys:
            if not isinstance(key, tuple) or any(type(t) is not int or t < 0 for t in key):
                raise ValueError('malformed lineage address')
        if () not in self.keys or len(set(self.keys)) != len(self.keys):
            raise ValueError('missing root or duplicate address')
        if any(k and k[:-1] not in self.keys for k in self.keys):
            raise ValueError('missing ancestor')

    @property
    def identity(self):
        return self.genesis, frozenset(self.keys)

@dataclass(frozen=True)
class Pruning:
    fine: Carrier
    coarse: Carrier

    def __post_init__(self):
        if self.fine.genesis != self.coarse.genesis:
            raise ValueError('different Genesis domains')
        if not set(self.coarse.keys) <= set(self.fine.keys):
            raise ValueError('illegal pruning target')

    def ancestor(self, key):
        if key not in self.fine.keys:
            raise ValueError('key outside source carrier')
        return max((p for p in self.coarse.keys if key[:len(p)] == p), key=len)

    def aggregate(self, values):
        if len(values) != len(self.fine.keys):
            raise ValueError('source length mismatch')
        if any(type(v) is not int and not isinstance(v, Fraction) for v in values):
            raise ValueError('exact integer/rational sources required')
        out = {k: Fraction(0) for k in self.coarse.keys}
        for k, x in zip(self.fine.keys, values):
            out[self.ancestor(k)] += x
        return tuple(out[k] for k in self.coarse.keys)

    def then(self, following: Pruning):
        if self.coarse.identity != following.fine.identity:
            raise ValueError('incompatible composition endpoints')
        return Pruning(self.fine, following.coarse)
