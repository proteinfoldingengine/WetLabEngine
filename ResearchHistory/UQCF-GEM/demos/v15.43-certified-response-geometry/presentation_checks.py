"""Exact presentation identities on the supplied operational carrier only."""
from dataclasses import replace
from fractions import Fraction as Q
from functools import lru_cache
from application import evaluate_field
from carriers import Carrier
from exact_algebra import add, identity, matmul, matvec, scale, transpose
from holonomy import linearized_holonomy, cotangent_holonomy, reverse_cycle, rotate_cycle
from operational_complex import construct_operational_complex, enumerate_baseline_connection
from transport import FramePresentation, construct_transport, centered_derivatives

ZERO = ((Q(0), Q(0)), (Q(0), Q(0)))
UNIT = identity(2)


def require(condition, name):
    if not condition:
        raise ValueError(name)


@lru_cache(maxsize=32768)
def _mul(a, b):
    return matmul(a, b)


@lru_cache(maxsize=32768)
def _conjugate(left, value, right):
    return _mul(left, _mul(value, transpose(right)))


def expanded(baseline, deltas, cycle):
    """Four separate ordered products; no production recurrence."""
    edges = tuple(zip(cycle, cycle[1:] + cycle[:1]))
    return _expanded_terms(tuple(baseline[e] for e in edges), tuple(deltas[e] for e in edges))


@lru_cache(maxsize=32768)
def _expanded_terms(baseline, deltas):
    result = ZERO
    for slot in range(4):
        term = UNIT
        for index in range(4):
            term = _mul(deltas[index] if index == slot else baseline[index], term)
        result = add(result, term)
    return result


def _faces(carrier, transport):
    p, delta = dict(transport.baseline), dict(transport.tangent_deltas)
    dual = dict(transport.cotangent_pullback_deltas)
    presented = replace(carrier.baseline, transports=transport.baseline)
    require(all(dual[e] == transpose(m) for e,m in delta.items()), 'edge_duality')
    for cycle in carrier.complex.cycles:
        value = linearized_holonomy(presented, transport, cycle)
        edges = tuple(zip(cycle, cycle[1:]+cycle[:1]))
        edges += tuple((y,x) for x,y in edges)
        face_p = tuple((e,p[e]) for e in edges)
        base = replace(presented, transports=face_p, directed_edges=edges)
        local = replace(transport, baseline=face_p,
                        tangent_deltas=tuple((e,delta[e]) for e in edges),
                        cotangent_pullback_deltas=tuple((e,dual[e]) for e in edges))
        path = UNIT
        for step in range(4):
            rotated = rotate_cycle(cycle,step)
            expected = _conjugate(path,value,path)
            for oriented, sign in ((rotated,1),(reverse_cycle(rotated),-1)):
                actual = linearized_holonomy(base,local,oriented)
                require(actual == scale(sign,expected), 'basepoint_orientation')
                require(actual == expanded(p,delta,oriented), 'independent_product')
                require(cotangent_holonomy(base,local,oriented) == transpose(actual), 'face_duality')
            path = _mul(p[(cycle[step],cycle[(step+1)%4])],path)


def gauge_presentations(complex_):
    actions = tuple(sorted(complex_.d4_actions))
    for label in complex_.labels:
        for index, action in enumerate(actions):
            yield ('site',label,index), FramePresentation(tuple((x,action if x==label else UNIT) for x in complex_.labels))
    yield ('mixed',), FramePresentation(tuple((x,actions[i%8]) for i,x in enumerate(sorted(complex_.labels))))


@lru_cache(maxsize=32768)
def _endpoint(value_difference, qx, qy, p_reverse, direction):
    endpoint = matvec(p_reverse,qy)
    mean = tuple((a+b)/2 for a,b in zip(qx,endpoint))
    return tuple(tuple(value_difference/2 * int(i==j) +
                       (mean[i]*direction[j]-direction[i]*mean[j])/2
                       for j in range(2)) for i in range(2))


@lru_cache(maxsize=256)
def _gradients(complex_, baseline, values):
    return centered_derivatives(complex_,baseline,values,FramePresentation.identity(complex_))


def _gauge_context(carrier, values, original):
    complex_ = carrier.complex
    q = dict(_gradients(complex_,carrier.baseline,values))
    field = dict(zip(complex_.labels,values))
    directions = dict(zip(complex_.directed_edges,complex_.direction_classes))
    p = dict(original.baseline)
    b = dict(original.source_endomorphisms)
    delta = dict(original.tangent_deltas)
    dual = dict(original.cotangent_pullback_deltas)
    actions = tuple(sorted(complex_.d4_actions))
    gradients = {}
    axes = ((Q(1),Q(0)),(Q(0),Q(1)))
    for x in complex_.labels:
        local = tuple((y,d) for (a,y),d in directions.items() if a==x)
        for index,g in enumerate(actions):
            neighbors = {matvec(g,d):y for y,d in local}
            actual = tuple((field[neighbors[d]]-field[neighbors[tuple(-v for v in d)]])/2 for d in axes)
            gradients[x,index] = (actual,matvec(g,q[x]))
    # This is an invocation-local cache of immutable mathematical matrices,
    # never evidence or verdicts. Every lookup is compared anew below.
    edge_values = {}
    def edge_math(edge,ix,iy):
        key = (edge,ix,iy)
        if key not in edge_values:
            x,y = edge
            gx,gy = actions[ix],actions[iy]
            forward = _conjugate(gy,p[edge],gx)
            reverse = _conjugate(gx,p[(y,x)],gy)
            actual_b = _endpoint(field[x]-field[y],gradients[x,ix][0],gradients[y,iy][0],reverse,matvec(gx,directions[edge]))
            actual_delta = _mul(forward,actual_b)
            actual_dual = transpose(actual_delta)
            edge_values[key] = (forward,actual_b,actual_delta,actual_dual,
                                _conjugate(gx,b[edge],gx),
                                _conjugate(gy,delta[edge],gx),
                                _conjugate(gx,dual[edge],gy))
        return edge_values[key]
    return actions, gradients, edge_math


def incremental_transport(carrier, values, original, presentation, context=None):
    """Independent endpoint evaluation; reuse only unaffected exact matrices."""
    complex_ = carrier.complex
    presentation.validate(complex_)
    actions, gradients, edge_math = _gauge_context(carrier,values,original) if context is None else context
    gauges = {x:actions.index(g) for x,g in presentation.gauges}
    for x,index in gauges.items():
        actual,expected = gradients[x,index]
        require(actual==expected,'gradient_covariance')
    p,source,delta,dual = [],[],[],[]
    for edge in complex_.directed_edges:
        x,y = edge
        forward,b,d,c,expected_b,expected_d,expected_c = edge_math(edge,gauges[x],gauges[y])
        require(b==expected_b,'source_endpoint_covariance')
        require(d==expected_d,'tangent_endpoint_covariance')
        require(c==expected_c,'cotangent_endpoint_covariance')
        p.append((edge,forward)); source.append((edge,b)); delta.append((edge,d)); dual.append((edge,c))
    return replace(original,baseline=tuple(p),source_endomorphisms=tuple(source),
                   tangent_deltas=tuple(delta),cotangent_pullback_deltas=tuple(dual))


def check_gauges(carrier, values, original, certify_core=False):
    p, delta = dict(original.baseline),dict(original.tangent_deltas)
    curves = tuple(expanded(p,delta,c) for c in carrier.complex.cycles)
    keys = []
    core_count = 0
    context = _gauge_context(carrier,values,original)
    for key,presentation in gauge_presentations(carrier.complex):
        changed = incremental_transport(carrier,values,original,presentation,context)
        if certify_core is True or (certify_core == "mixed" and key == ("mixed",)):
            direct = construct_transport(carrier.complex,carrier.baseline,values,presentation=presentation)
            require(changed == direct, 'incremental_core_basis')
            core_count += 1
        if key == ('mixed',):
            _faces(carrier,changed)
        gauges = dict(presentation.gauges)
        cp,cd = dict(changed.baseline),dict(changed.tangent_deltas)
        for cycle,value in zip(carrier.complex.cycles,curves):
            require(expanded(cp,cd,cycle) == _conjugate(gauges[cycle[0]],value,gauges[cycle[0]]), 'gauge_face_conjugation')
        keys.append(key)
    return tuple(keys), core_count


def _relabel_values(labels, values, names):
    mapped = dict(zip((names[x] for x in labels),values))
    return tuple(mapped[x] for x in sorted(mapped))


@lru_cache(maxsize=8)
def _relabeled_geometry(old, permutation):
    names = dict(zip(old.labels,permutation))
    labels = tuple(sorted(permutation))
    indices = {names[x]:i for i,x in enumerate(old.labels)}
    work = tuple(tuple(old.work[indices[x]][indices[y]] for y in labels) for x in labels)
    neighbors = frozenset(frozenset(names[x] for x in edge) for edge in old.neighbors)
    audit = construct_operational_complex(labels,work,neighbors)
    require(audit.complex is not None, 'relabel_complex_identification')
    baseline = enumerate_baseline_connection(audit.complex)
    require(baseline.connection is not None, 'relabel_baseline_identification')
    return audit.complex,baseline.connection


def relabeled_carrier(carrier, permutation):
    complex_,baseline = _relabeled_geometry(carrier.complex,permutation)
    return Carrier(complex_,baseline,carrier.L,carrier.scale,carrier.receipt)


def frame_alignment(original, changed, names):
    old = original.complex
    new_d = dict(zip(changed.complex.directed_edges,changed.complex.direction_classes))
    gauges = {}
    for x in old.labels:
        local = tuple((y,d) for (a,y),d in zip(old.directed_edges,old.direction_classes) if a==x)
        matches = tuple(g for g in old.d4_actions if all(matvec(g,d)==new_d[(names[x],names[y])] for y,d in local))
        require(len(matches)==1, 'direction_frame_alignment')
        gauges[x] = matches[0]
    old_p,new_p = dict(original.baseline.transports),dict(changed.baseline.transports)
    require(all(new_p[(names[x],names[y])] == _conjugate(gauges[y],p,gauges[x]) for (x,y),p in old_p.items()), 'aligned_baseline')
    return gauges


def compare_aligned(original, changed, before, after, names, factor=Q(1)):
    gauges = frame_alignment(original,changed,names)
    for old_entries,new_entries,mode in ((before.transport.source_endomorphisms,after.transport.source_endomorphisms,'source'),(before.transport.tangent_deltas,after.transport.tangent_deltas,'tangent'),(before.transport.cotangent_pullback_deltas,after.transport.cotangent_pullback_deltas,'dual')):
        new = dict(new_entries)
        for (x,y),value in old_entries:
            left,right = (gauges[x],gauges[x]) if mode=='source' else ((gauges[y],gauges[x]) if mode=='tangent' else (gauges[x],gauges[y]))
            require(new[(names[x],names[y])] == scale(factor,_conjugate(left,value,right)), 'aligned_'+mode)
    records = {frozenset(c):(c,k,i) for c,k,i in after.records}
    p = dict(after.transport.baseline)
    rotations = reversals = 0
    for cycle,value,invariant in before.records:
        mapped = tuple(names[x] for x in cycle)
        canonical,k,new_invariant = records[frozenset(mapped)]
        path = UNIT
        for step in range(4):
            rotated = rotate_cycle(canonical,step)
            if mapped == rotated or mapped == reverse_cycle(rotated):
                sign = 1 if mapped==rotated else -1
                rotations += int(step != 0)
                reversals += int(sign == -1)
                actual = scale(sign,_conjugate(path,k,path))
                require(actual == scale(factor,_conjugate(gauges[cycle[0]],value,gauges[cycle[0]])), 'aligned_face')
                require(new_invariant == factor*factor*invariant, 'aligned_invariant')
                break
            path = _mul(p[(canonical[step],canonical[(step+1)%4])],path)
        else: raise ValueError('relabel_cycle_correspondence')
    return {'rotations':rotations,'reversals':reversals}


def check_presentations(carrier, values):
    result = evaluate_field(carrier,values)
    _faces(carrier,result.transport)
    keys, _ = check_gauges(carrier,values,result.transport)
    labels = carrier.complex.labels
    n = len(labels)
    permutations = (tuple((2*i+1)%n for i in range(n)),tuple(n-1-i for i in range(n)))
    relabel_counts = []
    for permutation in permutations:
        names = dict(zip(labels,permutation))
        changed = relabeled_carrier(carrier,permutation)
        after = evaluate_field(changed,_relabel_values(labels,values,names))
        relabel_counts.append(compare_aligned(carrier,changed,result,after,names))
    return {'L':carrier.L,'scale':carrier.scale,'faces':len(result.records),
            'oriented_faces':8*len(result.records),'gauge_presentations':len(keys),
            'gauge_keys':keys,'gradient_checks':len(keys)*n,
            'edge_checks':len(keys)*len(carrier.complex.directed_edges),
            'gauge_face_checks':len(keys)*len(result.records),'relabelings':2,
            'relabel_cycle_rotations':sum(r['rotations'] for r in relabel_counts),
            'relabel_cycle_reversals':sum(r['reversals'] for r in relabel_counts),
            'transformation_names':('four_basepoints','both_orientations','duality','independent_four_terms','single_site_D4','fixed_mixed_D4','label_component_permutation'),
            'all_exact':True}


def local_linear_certificate(carrier):
    """Complete local linear basis, against the literal frozen wedge algebra.

    For fixed geometry, the constructor edge rule is linear in the scalar
    difference and four endpoint gradient components. Exhausting these five
    basis vectors proves the independent evaluator for arbitrary field values.
    """
    actions = tuple(sorted(carrier.complex.d4_actions))
    p = dict(carrier.baseline.transports)
    edge_types = tuple(sorted(set((p[e],d) for e,d in zip(carrier.complex.directed_edges,carrier.complex.direction_classes))))
    comparisons = 0
    def outer(a,b):
        return tuple(tuple(x*y for y in b) for x in a)
    for forward,direction in edge_types:
        reverse = transpose(forward)
        for gx in actions:
            for gy in actions:
                transformed_reverse = _conjugate(gx,reverse,gy)
                for slot in range(5):
                    basis = tuple(Q(i==slot) for i in range(5))
                    du,qx,qy = basis[0],basis[1:3],basis[3:5]
                    endpoint = matvec(reverse,qy)
                    mean = tuple((a+b)/2 for a,b in zip(qx,endpoint))
                    frozen = add(scale(du/2,UNIT),scale(Q(1,2),add(outer(mean,direction),scale(-1,outer(direction,mean)))))
                    plain = _endpoint(du,qx,qy,reverse,direction)
                    changed = _endpoint(du,matvec(gx,qx),matvec(gy,qy),transformed_reverse,matvec(gx,direction))
                    require(plain == frozen, 'local_basis_frozen_formula')
                    require(changed == _conjugate(gx,frozen,gx), 'local_basis_source')
                    require(_mul(_conjugate(gy,forward,gx),changed)==_conjugate(gy,_mul(forward,frozen),gx), 'local_basis_tangent')
                    comparisons += 1
    directions = ((Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),(Q(0),Q(-1)))
    gradient_comparisons = 0
    for action in actions:
        for slot in range(4):
            values = {d:Q(i==slot) for i,d in enumerate(directions)}
            original = ((values[directions[0]]-values[directions[1]])/2,(values[directions[2]]-values[directions[3]])/2)
            changed = {matvec(action,d):v for d,v in values.items()}
            actual = ((changed[directions[0]]-changed[directions[1]])/2,(changed[directions[2]]-changed[directions[3]])/2)
            require(actual==matvec(action,original),'local_gradient_basis')
            gradient_comparisons += 1
    return {'edge_types':edge_types,'endpoint_frame_pairs':64,
            'linear_basis_dimension':5,'local_basis_comparisons':comparisons,
            'gradient_basis_comparisons':gradient_comparisons,'all_exact':True}
