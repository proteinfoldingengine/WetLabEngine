"""Immutable geometry-only interface for the intrinsic operator."""
from __future__ import annotations
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

Matrix = tuple[tuple[Fraction, ...], ...]

@dataclass(frozen=True)
class Geometry:
    L: int
    scale: Fraction
    labels: tuple[int, ...]
    work: Matrix
    neighbors: tuple[tuple[int, int], ...]

@dataclass(frozen=True)
class Operator:
    labels: tuple[int, ...]
    cycles: tuple[tuple[int, int, int, int], ...]
    entries: Matrix

def canonical_bytes(value: object) -> bytes:
    def default(item):
        if isinstance(item, Fraction): return str(item)
        if isinstance(item, tuple): return list(item)
        raise TypeError('noncanonical value')
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True,
                       separators=(',', ': '), allow_nan=False, default=default) + '\n').encode('ascii')

def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError('duplicate_key')
        result[key] = value
    return result

def _keys(value, expected):
    if type(value) is not dict: raise ValueError('invalid_type')
    if set(value) != expected:
        raise ValueError('unknown_field' if set(value) - expected else 'missing_field')

def _int(value):
    if type(value) is not int: raise ValueError('invalid_integer')
    return value

def _fraction(value):
    if type(value) is not str: raise ValueError('invalid_fraction_type')
    try: result = Fraction(value)
    except (ValueError, ZeroDivisionError): raise ValueError('malformed_fraction') from None
    if str(result) != value: raise ValueError('noncanonical_fraction')
    return result

def load_geometry(raw: bytes) -> Geometry:
    if type(raw) is not bytes: raise TypeError('bytes required')
    try: wire = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError('invalid_number')))
    except (UnicodeDecodeError, json.JSONDecodeError) as error: raise ValueError('invalid_json') from error
    _keys(wire, {'L', 'scale', 'labels', 'work', 'neighbors'})
    L, scale = _int(wire['L']), _fraction(wire['scale'])
    if L not in (5, 7): raise ValueError('invalid_L')
    if scale not in (Fraction(1), Fraction(7, 3)): raise ValueError('invalid_scale')
    N = L * L
    if type(wire['labels']) is not list: raise ValueError('invalid_labels')
    labels = tuple(_int(x) for x in wire['labels'])
    if labels != tuple(range(N)): raise ValueError('invalid_label_order')
    if type(wire['work']) is not list or any(type(row) is not list for row in wire['work']):
        raise ValueError('invalid_work')
    work = tuple(tuple(_fraction(x) for x in row) for row in wire['work'])
    if len(work) != N or any(len(row) != N for row in work): raise ValueError('work_dimension')
    if any(work[i][i] for i in range(N)): raise ValueError('work_diagonal')
    if any(work[i][j] != work[j][i] for i in range(N) for j in range(N)):
        raise ValueError('work_asymmetry')
    if type(wire['neighbors']) is not list: raise ValueError('invalid_neighbors')
    neighbors = []
    for edge in wire['neighbors']:
        if type(edge) is not list or len(edge) != 2: raise ValueError('invalid_neighbor')
        a, b = (_int(x) for x in edge)
        if not 0 <= a < b < N: raise ValueError('invalid_neighbor')
        neighbors.append((a, b))
    neighbors = tuple(neighbors)
    if neighbors != tuple(sorted(set(neighbors))): raise ValueError('neighbor_order')
    if len(neighbors) != 2*N: raise ValueError('edge_inventory')
    if raw != canonical_bytes(wire): raise ValueError('noncanonical_json')
    return Geometry(L, scale, labels, work, neighbors)

def validate_inventory(geometries: tuple[Geometry, ...]) -> tuple[Geometry, ...]:
    expected = ((5, Fraction(1)), (5, Fraction(7, 3)),
                (7, Fraction(1)), (7, Fraction(7, 3)))
    if type(geometries) is not tuple or tuple((g.L, g.scale) for g in geometries) != expected:
        raise ValueError('carrier_inventory')
    for g in geometries:
        if type(g) is not Geometry or len(g.labels) != g.L*g.L or len(g.neighbors) != 2*g.L*g.L:
            raise ValueError('carrier_inventory')
    return geometries

def build_actual_carrier(geometry: Geometry):
    if type(geometry) is not Geometry: raise ValueError('invalid_geometry')
    # Re-validate even when a caller directly constructs the immutable type.
    wire = {'L': geometry.L, 'scale': str(geometry.scale), 'labels': list(geometry.labels),
            'work': [[str(x) for x in row] for row in geometry.work],
            'neighbors': [list(e) for e in geometry.neighbors]}
    if load_geometry(canonical_bytes(wire)) != geometry: raise ValueError('invalid_geometry')
    from bootstrap import load_pinned_modules
    modules = load_pinned_modules(Path(__file__).resolve().parents[4])
    payload = modules['projection'].Payload(geometry.L, geometry.scale, geometry.labels,
                                            geometry.work, geometry.neighbors, ())
    carrier = modules['carriers'].build_carrier(payload)
    N = geometry.L * geometry.L
    if len(carrier.complex.labels) != N or len(carrier.complex.neighbors) != 2*N or len(carrier.complex.cycles) != N:
        raise ValueError('carrier_inventory')
    return carrier
