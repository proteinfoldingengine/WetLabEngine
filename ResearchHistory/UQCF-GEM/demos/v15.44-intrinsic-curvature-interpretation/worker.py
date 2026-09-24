"""Fresh isolated process for each exact construction and verification stage."""
from __future__ import annotations
import argparse
import json
import sys
from dataclasses import fields, is_dataclass
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path

# Fresh -I workers explicitly admit only their own sibling implementation.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from operator_types import (Geometry, Operator, canonical_bytes, load_geometry,
                            validate_inventory, build_actual_carrier, _unique, _fraction, _int, _keys)
from exact_matrix import Reduction
from kernel import KernelResult, analyze_kernel, verify_kernel
from bootstrap import check_pure_modules, deny_archive_access, load_pinned_modules
from evidence import verify_evidence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INVENTORY = ((5,Q(1)), (5,Q(7,3)), (7,Q(1)), (7,Q(7,3)))


def wire(value):
    if is_dataclass(value): return {f.name: wire(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, Q): return str(value)
    if isinstance(value, tuple): return [wire(x) for x in value]
    if isinstance(value, list): return [wire(x) for x in value]
    if isinstance(value, dict):
        if any(type(k) is not str for k in value): raise ValueError('wire dictionary key')
        return {k: wire(v) for k,v in value.items()}
    if value is None or type(value) in (str,int,bool): return value
    raise ValueError('noncanonical wire type')


def comparison_wire(result):
    """Encode internal tuple-keyed coverage without weakening strict JSON wires."""
    if type(result) is not dict or set(result) != {'cases','pairs','scale_pairs','counts'}:
        raise ValueError('comparison result')
    counts = result['counts']
    if type(counts) is not dict or set(counts) != {
            'cases','pairs','scale_pairs','by_control','by_carrier'}:
        raise ValueError('comparison counts')
    by_carrier = counts['by_carrier']
    if type(by_carrier) is not dict:
        raise ValueError('comparison carrier counts')
    carriers = []
    for key, pairs in by_carrier.items():
        if (type(key) is not tuple or len(key) != 2 or type(key[0]) is not int or
                type(key[1]) is not Q or type(pairs) is not int):
            raise ValueError('comparison carrier count')
        carriers.append({'L': key[0], 'scale': str(key[1]), 'pairs': pairs})
    encoded = dict(result)
    encoded['counts'] = {**counts, 'by_carrier': carriers}
    return wire(encoded)


def parse(raw):
    try:
        obj = json.loads(raw.decode('ascii'), object_pairs_hook=_unique,
                         parse_float=lambda _: (_ for _ in ()).throw(ValueError('float')),
                         parse_constant=lambda _: (_ for _ in ()).throw(ValueError('constant')))
    except (UnicodeError, json.JSONDecodeError) as exc: raise ValueError('invalid_json') from exc
    if raw != canonical_bytes(obj): raise ValueError('noncanonical_json')
    return obj


def matrix(value, rows, columns):
    if type(value) is not list or len(value) != rows: raise ValueError('matrix rows')
    if any(type(row) is not list or len(row) != columns for row in value): raise ValueError('matrix columns')
    return tuple(tuple(_fraction(x) for x in row) for row in value)


def integer_tuple(value, length, *, max_value=None):
    if type(value) is not list or len(value) != length: raise ValueError('integer tuple length')
    result = tuple(_int(x) for x in value)
    if max_value is not None and any(not 0 <= x < max_value for x in result):
        raise ValueError('integer tuple range')
    return result


def operator_from_wire(obj):
    _keys(obj, {'labels','cycles','entries'})
    if type(obj['labels']) is not list: raise ValueError('labels')
    n = len(obj['labels']); labels = integer_tuple(obj['labels'], n)
    if labels != tuple(range(n)) or n not in (25,49): raise ValueError('labels order')
    if type(obj['cycles']) is not list or len(obj['cycles']) != n: raise ValueError('cycles')
    cycles = tuple(integer_tuple(c, 4, max_value=n) for c in obj['cycles'])
    if len(set(cycles)) != n or cycles != tuple(sorted(cycles)): raise ValueError('cycles order')
    return Operator(labels, cycles, matrix(obj['entries'], 4*n, n))


def certificate_from_wire(obj, operator):
    _keys(obj, {'rank','nullity','pivots','null_basis','image_basis','projector',
                'centered_basis','reduction'})
    n = len(operator.labels); m = len(operator.entries)
    rank = _int(obj['rank']); nullity = _int(obj['nullity'])
    if not 0 <= rank <= n or nullity != n-rank: raise ValueError('certificate dimensions')
    pivots = integer_tuple(obj['pivots'], rank, max_value=n)
    r = obj['reduction']; _keys(r, {'reduced','pivots','operations'})
    operations = []
    if type(r['operations']) is not list: raise ValueError('operations')
    for op in r['operations']:
        if type(op) is not list or not op or op[0] not in ('swap','scale','add'):
            raise ValueError('operation')
        name = op[0]
        if len(op) != (4 if name == 'add' else 3): raise ValueError('operation arity')
        operations.append(tuple([name] + [_fraction(v) if (name == 'scale' and j == 2 or
                            name == 'add' and j == 3) else _int(v)
                            for j,v in enumerate(op[1:], 1)]))
    reduced = Reduction(matrix(r['reduced'], m, n),
                        integer_tuple(r['pivots'],rank,max_value=n),tuple(operations))
    center = obj['centered_basis']
    if type(center) is not list or len(center) != n or type(center[0]) is not list:
        raise ValueError('centered basis')
    result = KernelResult(rank,nullity,pivots,matrix(obj['null_basis'],n,nullity),
                          matrix(obj['image_basis'],m,rank),matrix(obj['projector'],n,n),
                          matrix(center,n,len(center[0])),reduced)
    verify_kernel(operator,result)
    return result


def _geometry_from_payload(payload):
    return load_geometry(canonical_bytes({'L':payload.L,'scale':str(payload.scale),
        'labels':list(payload.labels),'work':[[str(x) for x in row] for row in payload.work],
        'neighbors':[list(e) for e in payload.neighbors]}))


def _projection():
    pins = verify_evidence(ROOT)
    parent = load_pinned_modules(ROOT)
    return parent['projection'].decode_projection(Path(pins['inputs']['path']).read_bytes())


def _prepared(data):
    _keys(data, {'geometries','operators','certificates','operator_hashes','certificate_hashes'})
    gs = tuple(load_geometry(canonical_bytes(g)) for g in data['geometries'])
    validate_inventory(gs)
    operators = tuple(operator_from_wire(x) for x in data['operators'])
    certificates = tuple(certificate_from_wire(x,o) for x,o in zip(data['certificates'],operators,strict=True))
    for i,(g,o,c) in enumerate(zip(gs,operators,certificates,strict=True)):
        if sha256(canonical_bytes(wire(o))).hexdigest() != data['operator_hashes'][i]:
            raise ValueError('operator seal')
        if sha256(canonical_bytes(wire(c))).hexdigest() != data['certificate_hashes'][i]:
            raise ValueError('certificate seal')
        if len(o.labels) != g.L*g.L: raise ValueError('carrier operator')
    return gs,operators,certificates


def run(stage, data, index, progress_path):
    if stage == 'evidence':
        _keys(data,set())
        pins=verify_evidence(ROOT)
        return {'pins': {k: (v if k not in ('spec','inputs','results','closure') else
                ({name: pin['blob'] for name,pin in v.items()} if k=='closure' else v['blob']))
                for k,v in pins.items()}}
    if stage == 'projection_carriers':
        _keys(data,{'pins'})
        projection=_projection()
        gs=validate_inventory(tuple(_geometry_from_payload(p) for p in projection.payloads))
        for g in gs: build_actual_carrier(g)
        return {'geometries':wire(gs)}
    if stage == 'operator_derivation_equality':
        _keys(data,{'geometries'})
        from derive import derive_operator, require_equal
        from oracle import reference_operator
        gs=validate_inventory(tuple(load_geometry(canonical_bytes(g)) for g in data['geometries']))
        check_pure_modules(HERE)
        carriers=tuple(build_actual_carrier(g) for g in gs)
        with deny_archive_access(): operators=tuple(derive_operator(c) for c in carriers)
        for carrier,operator in zip(carriers,operators,strict=True):
            require_equal(operator,reference_operator(carrier))
        return {'operators':wire(operators),'operator_hashes':[
            sha256(canonical_bytes(wire(o))).hexdigest() for o in operators]}
    if stage == 'kernel_image_certificates':
        _keys(data,{'geometries','operators','operator_hashes'})
        check_pure_modules(HERE)
        gs=validate_inventory(tuple(load_geometry(canonical_bytes(g)) for g in data['geometries']))
        operators=tuple(operator_from_wire(x) for x in data['operators'])
        for i,o in enumerate(operators):
            if sha256(canonical_bytes(wire(o))).hexdigest()!=data['operator_hashes'][i]:
                raise ValueError('operator seal')
        carriers=tuple(build_actual_carrier(g) for g in gs)
        if any(o.labels!=c.complex.labels or o.cycles!=c.complex.cycles for o,c in zip(operators,carriers)):
            raise ValueError('operator geometry')
        with deny_archive_access(): certificates=tuple(analyze_kernel(o) for o in operators)
        for o,c in zip(operators,certificates,strict=True): verify_kernel(o,c)
        return {'certificates':wire(certificates),'certificate_hashes':[
            sha256(canonical_bytes(wire(c))).hexdigest() for c in certificates]}
    if stage in ('controls','all_archived_field_comparisons'):
        gs,operators,certificates=_prepared(data)
        if stage == 'controls':
            if type(index) is not int or not 0<=index<4: raise ValueError('control index')
            from presentations import check_presentations
            carrier=build_actual_carrier(gs[index])
            receipt=check_presentations(carrier)
            if receipt['rank']!=certificates[index].rank or receipt['nullity']!=certificates[index].nullity:
                raise ValueError('control certificate')
            return {'control':wire(receipt),'index':index}
        from compare import complete_comparison
        projection=_projection()
        carriers={key:build_actual_carrier(g) for key,g in zip(INVENTORY,gs,strict=True)}
        ops=dict(zip(INVENTORY,operators,strict=True)); certs=dict(zip(INVENTORY,certificates,strict=True))
        pins=verify_evidence(ROOT)
        archived=parse(Path(pins['results']['path']).read_bytes())
        with progress_path.open('w',encoding='ascii') as progress:
            def accepted(kind):
                def callback(item):
                    progress.write(kind+'\n'); progress.flush()
                return callback
            result=complete_comparison(projection,carriers,ops,certs,archived,
                on_case=accepted('cases'),on_pair=accepted('pairs'),on_scale=accepted('scale_pairs'))
        return {'comparison':comparison_wire(result)}
    raise ValueError('unknown worker stage')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage',required=True)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--progress',required=True,type=Path)
    parser.add_argument('--index',type=int)
    args=parser.parse_args()
    data=parse(args.input.read_bytes())
    args.output.write_bytes(canonical_bytes({'stage':args.stage,
                                             'result':run(args.stage,data,args.index,args.progress)}))


if __name__=='__main__': main()
