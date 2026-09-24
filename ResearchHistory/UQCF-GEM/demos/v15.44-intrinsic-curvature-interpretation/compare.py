"""Exact descriptive comparison of sealed intrinsic operators with frozen fields.

No construction reads archived results. The caller supplies validated projection,
actual carriers, sealed operators/certificates, and the archived JSON object.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from pathlib import Path
from bootstrap import load_pinned_modules
from exact_matrix import apply_matrix
from kernel import verify_kernel
from presentations import verify_scale

Q = Fraction


def _norm(values):
    return sum((v*v for v in values), Q(0))


def _ratio(num, den, reason):
    return (num / den, None) if den else (None, reason)


def analyze_field(operator, certificate, field, *, _verified=False):
    """Return exact full response, face data, and orthogonal kernel split."""
    if type(field) is not tuple or len(field) != len(operator.labels) or any(type(x) is not Q for x in field):
        raise ValueError('field_dimension_or_type')
    if not _verified: verify_kernel(operator, certificate)
    if len(operator.entries) != 4*len(operator.cycles): raise ValueError('face_shape')
    response = apply_matrix(operator.entries, field)
    matrices = tuple(((response[4*j], response[4*j+1]),
                      (response[4*j+2], response[4*j+3])) for j in range(len(operator.cycles)))
    invariants = []
    for matrix in matrices:
        a, b = matrix[0]; c, d = matrix[1]
        if a or d or b != -c: raise ValueError('non_skew_face')
        invariant = -(a*a + 2*b*c + d*d)/2
        if invariant < 0: raise ValueError('negative_invariant')
        invariants.append(invariant)
    invariants = tuple(invariants)
    z = apply_matrix(certificate.projector, field)
    v = tuple(x-y for x,y in zip(field,z,strict=True))
    S, z_norm, v_norm = _norm(field), _norm(z), _norm(v)
    if sum((x*y for x,y in zip(z,v,strict=True)), Q(0)) or S != z_norm+v_norm:
        raise ValueError('orthogonal_decomposition')
    if any(apply_matrix(operator.entries, z)) or apply_matrix(operator.entries, v) != response:
        raise ValueError('projection_response')
    E = sum(invariants, Q(0))
    e_s, e_s_reason = _ratio(E, S, 'UNDEFINED_ZERO_FIELD_NORM')
    e_v, e_v_reason = _ratio(E, v_norm, 'UNDEFINED_ZERO_VISIBLE_NORM')
    k_share, k_reason = _ratio(z_norm, S, 'UNDEFINED_ZERO_FIELD_NORM')
    v_share, v_reason = _ratio(v_norm, S, 'UNDEFINED_ZERO_FIELD_NORM')
    profile = tuple(value/E for value in invariants) if E else None
    return {'field': field, 'cycles': operator.cycles, 'response': response,
            'matrices': matrices, 'face_invariants': invariants, 'energy': E,
            'S': S, 'kernel_component': z, 'visible_component': v,
            'kernel_norm': z_norm, 'visible_norm': v_norm,
            'kernel_share': k_share, 'kernel_share_reason': k_reason,
            'visible_share': v_share, 'visible_share_reason': v_reason,
            'E_over_S': e_s, 'E_over_S_reason': e_s_reason,
            'E_over_visible_norm': e_v, 'E_over_visible_norm_reason': e_v_reason,
            'normalized_profile': profile,
            'normalized_profile_reason': None if E else 'UNDEFINED_ZERO_CURVATURE',
            'zero_count': sum(value == 0 for value in invariants),
            'nonzero_count': sum(value != 0 for value in invariants),
            'histogram': tuple(sorted(Counter(invariants).items()))}


def compare_pair(canonical, control):
    """Control-minus-canonical differences with exact sign-sensitive proportionality."""
    left, right = canonical['matrices'], control['matrices']
    if len(left) != len(right) or canonical['cycles'] != control['cycles']:
        raise ValueError('face_alignment')
    a = tuple(x for matrix in left for row in matrix for x in row)
    b = tuple(x for matrix in right for row in matrix for x in row)
    if len(a) != len(b): raise ValueError('face_length')
    if not any(a):
        category = 'BOTH_ZERO' if not any(b) else 'CANONICAL_ZERO_ONLY'
        factor = None
    elif not any(b):
        category, factor = 'CONTROL_ZERO_ONLY', None
    else:
        i = next(i for i,x in enumerate(a) if x)
        factor = b[i]/a[i]
        if factor and all(y == factor*x for x,y in zip(a,b,strict=True)):
            category = 'NONZERO_PROPORTIONAL'
        else:
            category, factor = 'NONZERO_NONPROPORTIONAL', None
    if canonical['energy'] and control['energy']:
        profile_equal, profile_reason = (canonical['normalized_profile'] == control['normalized_profile']), None
    else:
        profile_equal, profile_reason = None, 'UNDEFINED_ZERO_CURVATURE'
    result = {'proportionality': category, 'factor_control_over_canonical': factor,
              'matrix_equal': left == right, 'normalized_profile_equal': profile_equal,
              'normalized_profile_equal_reason': profile_reason,
              'energy_difference': control['energy']-canonical['energy'],
              'S_difference': control['S']-canonical['S'],
              'kernel_norm_difference': control['kernel_norm']-canonical['kernel_norm'],
              'visible_norm_difference': control['visible_norm']-canonical['visible_norm'],
              'face_invariant_differences': tuple(y-x for x,y in zip(canonical['face_invariants'],control['face_invariants'],strict=True))}
    for key in ('E_over_S','E_over_visible_norm','kernel_share','visible_share'):
        result[key+'_difference'], result[key+'_difference_reason'] = (
            (control[key]-canonical[key], None) if canonical[key] is not None and control[key] is not None
            else (None, ('CANONICAL_'+canonical[key+'_reason']) if canonical[key] is None
                  else ('CONTROL_'+control[key+'_reason'])))
    return result


def _fraction(value):
    if type(value) is not str: raise ValueError('archived_fraction')
    try: result = Q(value)
    except (ValueError, ZeroDivisionError) as error: raise ValueError('archived_fraction') from error
    if str(result) != value: raise ValueError('archived_fraction')
    return result


def validate_archived_cases(cases, projection=None):
    """Enforce all 740 case keys, exact face order, values, histograms, totals."""
    parent = load_pinned_modules(Path(__file__).resolve().parents[4])
    families = parent['projection'].FAMILY_KEYS
    expected = tuple((L, family, scale, index)
                     for L in (5,7) for scale in (Q(1), Q(7,3))
                     for family in families for index in range(L*L))
    if type(cases) is not list or len(cases) != len(expected): raise ValueError('archive_coverage')
    keys = []
    for case in cases:
        if type(case) is not dict or set(case) != {'L','family','scale','response_index','key',
               'carrier_family','face_count','zero_count','nonzero_count','histogram',
               'invariant_sum','faces','presentation_receipt'}: raise ValueError('archived_case_schema')
        key = (case['L'], case['family'], _fraction(case['scale']), case['response_index'])
        if case['key'] != [case['L'],case['family'],case['scale'],case['response_index']]:
            raise ValueError('archived_key')
        keys.append(key)
    if len(set(keys)) != len(expected) or set(keys) != set(expected): raise ValueError('archive_coverage')
    if tuple(keys) != expected: raise ValueError('archive_order')
    if projection is not None:
        projected = tuple((p.L,f.family,p.scale,f.response_index) for p in projection.payloads for f in p.fields)
        if projected != expected: raise ValueError('projection_order')
    for key,case in zip(expected,cases,strict=True):
        L = key[0]
        faces = case['faces']
        if type(faces) is not list or len(faces) != L*L or case['face_count'] != L*L:
            raise ValueError('archived_face_coverage')
        cycles = tuple(tuple(face['cycle']) for face in faces)
        # Frozen parent archive canonical order is the same order as the
        # periodic-square operator; check it again against actual A below.
        if len(set(cycles)) != L*L or cycles != tuple(sorted(cycles)):
            raise ValueError('archived_face_order')
        values = []
        for face in faces:
            if type(face) is not dict or set(face) != {'cycle','matrix','invariant','nonzero'}:
                raise ValueError('archived_face_schema')
            m = face['matrix']
            if type(m) is not list or len(m)!=2 or any(type(row) is not list or len(row)!=2 for row in m):
                raise ValueError('archived_matrix_shape')
            a,b,c,d = (_fraction(x) for row in m for x in row)
            invariant = _fraction(face['invariant'])
            if invariant != -(a*a+2*b*c+d*d)/2 or invariant < 0:
                raise ValueError('archived_invariant')
            if type(face['nonzero']) is not bool or face['nonzero'] != bool(a or b or c or d):
                raise ValueError('archived_nonzero')
            values.append(invariant)
        hist = [[str(x),n] for x,n in sorted(Counter(values).items())]
        if (case['histogram'] != hist or _fraction(case['invariant_sum']) != sum(values,Q(0)) or
                case['zero_count'] != sum(x==0 for x in values) or
                case['nonzero_count'] != sum(x!=0 for x in values)):
            raise ValueError('archived_summary')
    return tuple(keys)


def _check_archive(case, result, operator):
    if tuple(tuple(f['cycle']) for f in case['faces']) != operator.cycles:
        raise ValueError('archived_face_order')
    if case['carrier_family'] != 'GLOBAL_BALANCE_COMPLETION': raise ValueError('archived_carrier_family')
    for face,matrix,invariant in zip(case['faces'],result['matrices'],result['face_invariants'],strict=True):
        if tuple(tuple(_fraction(x) for x in row) for row in face['matrix']) != matrix:
            raise ValueError('archived_matrix_mismatch')
        if _fraction(face['invariant']) != invariant: raise ValueError('archived_invariant_mismatch')
    if (case['histogram'] != [[str(x),n] for x,n in result['histogram']] or
            _fraction(case['invariant_sum']) != result['energy']):
        raise ValueError('archived_summary_mismatch')


def validate_pair_coverage(pairs):
    """Reject missing, duplicate, or shuffled control comparisons."""
    families = load_pinned_modules(Path(__file__).resolve().parents[4])['projection'].FAMILY_KEYS
    expected = tuple(((L,families[0],scale,index),(L,family,scale,index))
                     for L in (5,7) for scale in (Q(1),Q(7,3))
                     for index in range(L*L) for family in families[1:])
    actual = tuple((p['canonical_key'],p['control_key']) for p in pairs)
    if len(actual) != len(expected) or len(set(actual)) != len(expected) or set(actual) != set(expected):
        raise ValueError('pair_coverage')
    if actual != expected: raise ValueError('pair_order')
    return len(actual)


def validate_archive_claims(claims):
    """Preserve the entire frozen v15.43 theorem/interpretation boundary."""
    expected = {'source_correspondence': 'NOT_EVALUATED',
                'physical_metric': False, 'physical_curvature': False,
                'stress_energy': False, 'einstein_equations': False,
                'continuum_limit': False, 'spacetime': False,
                'physical_gravity': False, 'scientific_breakthrough': False,
                'Pillar_3': 'OPEN', 'fundamental_time_introduced': False,
                'dark_matter_primitive_introduced': False,
                'inherited_axiom_dependence': True,
                'isotropic_scalar_lift_dependence': True}
    if (type(claims) is not dict or set(claims) != set(expected) or
            any(type(claims[name]) is not type(value) or claims[name] != value
                for name,value in expected.items())):
        raise ValueError('archive_claim_boundary')
    return True


def complete_comparison(projection, carriers, operators, certificates, archived, *, on_case=None, on_pair=None, on_scale=None):
    """Complete archive. Inputs indexed by (L, scale); callbacks receive accepted item.

    on_case(case), on_pair(pair), on_scale(pair) run after their own acceptance.
    A raised exception leaves caller-owned lists as actual completed progress.
    Return {'cases': tuple, 'pairs': tuple, 'scale_pairs': tuple, 'counts': dict}.
    No count is passed in or synthesized as a success receipt.
    """
    parent = load_pinned_modules(Path(__file__).resolve().parents[4])
    # Revalidate the frozen projection even when supplied as a mutable forged instance.
    parent['projection'].encode_projection(projection)
    if type(archived) is not dict: raise ValueError('archive_claim_boundary')
    validate_archive_claims(archived.get('claims'))
    keys = validate_archived_cases(archived['cases'], projection)
    carrier_keys = tuple((p.L,p.scale) for p in projection.payloads)
    if any(set(mapping) != set(carrier_keys) for mapping in (carriers,operators,certificates)):
        raise ValueError('carrier_coverage')
    for key in carrier_keys:
        if operators[key].labels != carriers[key].complex.labels or operators[key].cycles != carriers[key].complex.cycles:
            raise ValueError('operator_carrier_mismatch')
        verify_kernel(operators[key], certificates[key])
    cases = []
    by_key = {}
    cursor = 0
    for payload in projection.payloads:
        archive_group = archived['cases'][cursor:cursor+len(payload.fields)]
        cursor += len(payload.fields)
        key = payload.L,payload.scale
        for field, frozen in zip(payload.fields,archive_group,strict=True):
            result = analyze_field(operators[key],certificates[key],field.values,_verified=True)
            _check_archive(frozen,result,operators[key])
            case = {'key': (payload.L,field.family,payload.scale,field.response_index), **result}
            cases.append(case); by_key[case['key']] = case
            if on_case is not None: on_case(case)
    pairs = []
    for L in (5,7):
        for scale in (Q(1), Q(7,3)):
            for index in range(L*L):
                for family in parent['projection'].FAMILY_KEYS[1:]:
                    left=(L,parent['projection'].FAMILY_KEYS[0],scale,index)
                    right=(L,family,scale,index)
                    pair={'canonical_key':left,'control_key':right,**compare_pair(by_key[left],by_key[right])}
                    pairs.append(pair)
                    if on_pair is not None: on_pair(pair)
    if validate_pair_coverage(pairs) != 592 or len(cases) != 740 or len(keys)!=740:
        raise ValueError('comparison_coverage')
    scale_pairs=[]
    for L in (5,7):
        verify_scale(carriers[(L,Q(1))],carriers[(L,Q(7,3))],
                     operators[(L,Q(1))],operators[(L,Q(7,3))])
        for family in parent['projection'].FAMILY_KEYS:
            for index in range(L*L):
                left=(L,family,Q(1),index); right=(L,family,Q(7,3),index)
                a,b=by_key[left],by_key[right]
                factor=Q(7,3)
                if (b['field'] != tuple(factor*x for x in a['field']) or
                    b['matrices'] != tuple(tuple(tuple(factor*x for x in row) for row in m) for m in a['matrices']) or
                    b['face_invariants'] != tuple(factor*factor*x for x in a['face_invariants']) or
                    b['energy'] != factor*factor*a['energy']):
                    raise ValueError('scale_field_or_curvature')
                pair={'unit_key':left,'scaled_key':right,'field_factor':factor,'invariant_factor':factor*factor,
                      'aligned':True}
                scale_pairs.append(pair)
                if on_scale is not None: on_scale(pair)
    return {'cases':tuple(cases),'pairs':tuple(pairs),'scale_pairs':tuple(scale_pairs),
            'counts':{'cases':len(cases),'pairs':len(pairs),'scale_pairs':len(scale_pairs),
                      'by_control':{family:sum(p['control_key'][1]==family for p in pairs)
                                    for family in parent['projection'].FAMILY_KEYS[1:]},
                      'by_carrier':{(L,scale):sum(p['canonical_key'][0]==L and p['canonical_key'][2]==scale for p in pairs)
                                    for L in (5,7) for scale in (Q(1),Q(7,3))}}}
