"""Manufactured and response identities on every supplied actual carrier."""
from fractions import Fraction as Q
from application import evaluate_field
from exact_algebra import add, scale
from presentation_checks import check_gauges, compare_aligned, require, local_linear_certificate
from projection import FAMILY_KEYS

ZERO = ((Q(0),Q(0)),(Q(0),Q(0)))


def check_carrier_controls(carrier):
    n = len(carrier.complex.labels)
    require(carrier.L in (5,7) and n==carrier.L**2,'control_carrier_size')
    certificate = local_linear_certificate(carrier)
    constant_keys, impulse_keys = [], []
    certified_count = 0
    basis_count = 0
    edge_checks = face_checks = 0
    for amplitude in (Q(0),Q(7,3)):
        values = (amplitude,)*n
        result = evaluate_field(carrier,values)
        require(result.nonzero_count==0 and all(m==ZERO for _,m in result.transport.source_endomorphisms), 'constant_null')
        keys, direct_count = check_gauges(carrier,values,result.transport,certify_core="mixed")
        basis_count += direct_count
        certified_count += len(keys)
        edge_checks += len(keys)*len(carrier.complex.directed_edges)
        face_checks += len(keys)*len(carrier.complex.cycles)
        constant_keys.append(amplitude)
    expected = ((Q(0),n-12),(Q(1,64),8),(Q(1,16),4))
    for root in carrier.complex.labels:
        values = tuple(Q(x==root) for x in carrier.complex.labels)
        result = evaluate_field(carrier,values)
        require(result.histogram==expected, 'every_root_impulse_histogram')
        keys, direct_count = check_gauges(carrier,values,result.transport,certify_core=True if root==carrier.complex.labels[0] else "mixed")
        basis_count += direct_count
        certified_count += len(keys)
        edge_checks += len(keys)*len(carrier.complex.directed_edges)
        face_checks += len(keys)*len(carrier.complex.cycles)
        impulse_keys.append(root)
    return {'L':carrier.L,'scale':carrier.scale,'constants':len(constant_keys),
            'constant_keys':tuple(constant_keys),'impulses':len(impulse_keys),
            'impulse_keys':tuple(impulse_keys),'impulse_histogram':expected,
            'basis_core_comparisons':basis_count,
            'identity_core_comparisons':len(constant_keys)+len(impulse_keys),
            'algebraically_certified_gauge_comparisons':certified_count,
            'local_linear_certificate':certificate,'edge_checks':edge_checks,
            'face_checks':face_checks,'all_exact':True}


def _linear(before, after, factor=Q(1), right=None, second=Q(0)):
    b = before.transport.source_endomorphisms
    a = after.transport.source_endomorphisms
    other_b = dict(right.transport.source_endomorphisms) if right else dict(b)
    require(a == tuple((edge,add(scale(factor,m),scale(second,other_b[edge]))) for edge,m in b), 'response_B_linearity')
    other_k = {c:k for c,k,_ in right.records} if right else {c:k for c,k,_ in before.records}
    require(tuple((c,k) for c,k,_ in after.records) == tuple((c,add(scale(factor,k),scale(second,other_k[c]))) for c,k,_ in before.records), 'response_K_linearity')


def check_response_controls(unit, scaled, unit_fields, scaled_fields):
    require(unit.L==scaled.L and unit.scale==1 and scaled.scale==Q(7,3), 'scale_carrier_pair')
    n = len(unit.complex.labels)
    expected = tuple((family,index) for family in FAMILY_KEYS for index in range(n))
    require(tuple((f.family,f.response_index) for f in unit_fields)==expected and tuple((f.family,f.response_index) for f in scaled_fields)==expected, 'response_control_coverage')
    factor = Q(7,3)
    require(all(b.values==tuple(factor*v for v in a.values) for a,b in zip(unit_fields,scaled_fields)), 'response_field_scale')
    require(scaled.complex.work == tuple(tuple(factor*v for v in row) for row in unit.complex.work), 'work_scale')
    names = dict(zip(unit.complex.labels,scaled.complex.labels))
    unit_results, scaled_results = [], []
    scale_keys, shift_keys, superposition_keys = [], [], []
    for left,right in zip(unit_fields,scaled_fields):
        before = evaluate_field(unit,left.values)
        after = evaluate_field(scaled,right.values)
        compare_aligned(unit,scaled,before,after,names,factor)
        unit_results.append(before)
        scaled_results.append(after)
        scale_keys.append((unit.L,left.family,left.response_index))
        for carrier,field,result in ((unit,left,before),(scaled,right,after)):
            shifted = evaluate_field(carrier,tuple(v+factor for v in field.values))
            _linear(result,shifted)
            require(tuple(i for _,_,i in result.records)==tuple(i for _,_,i in shifted.records), 'shift_invariant')
            shift_keys.append((carrier.L,field.family,carrier.scale,field.response_index))
    for carrier,fields,results in ((unit,unit_fields,unit_results),(scaled,scaled_fields,scaled_results)):
        for family_index,family in enumerate(FAMILY_KEYS):
            i = family_index*n
            left,right = fields[i:i+2]
            combined = tuple(Q(2,3)*x-Q(5,7)*y for x,y in zip(left.values,right.values))
            result = evaluate_field(carrier,combined)
            _linear(results[i],result,Q(2,3),results[i+1],Q(-5,7))
            superposition_keys.append((carrier.L,family,carrier.scale,0,1))
    return {'L':unit.L,'scale_pairs':len(scale_keys),'scale_keys':tuple(scale_keys),
            'shift_cases':len(shift_keys),'shift_keys':tuple(shift_keys),
            'superpositions':len(superposition_keys),'superposition_keys':tuple(superposition_keys),
            'transformation_names':('scale_7/3','shift_7/3','superposition_2/3_-5/7'),
            'all_exact':True}
