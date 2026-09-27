"""v15.71: memory-enriched null source law on the positive-polar domain."""
import importlib.util
import itertools
import json
import pathlib
import sys
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('atlas70_memory', HERE.parent/'atlas-descent-composition'/'gate.py')
V70 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V70)
F, GL = V70.V64.ASYM.F, V70.GL
EDGES = V70.EDGES
HIDDEN, LABELS = V70.HIDDEN, V70.LABELS
EXPECTED = V70.EXPECTED
ETA, S, U = 1e-4, 1e-3, -3e-4
VISIBLE_OFFSET = 1e-4
EPSILONS = [1e-5, 5e-6]
PAULI = [np.array([[0,1],[1,0]],complex),
         np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]
LOCAL_PAIRS = np.array([np.kron(a,b) for a in PAULI for b in PAULI])
LOCAL_ONE = np.array([np.kron(a,np.eye(2)) for a in PAULI]+
                     [np.kron(np.eye(2),a) for a in PAULI])
ONE = []
PAIR = []
for q in range(3):
    for a in range(1,4):
        ids = [0,0,0]; ids[q] = a; ONE.append(F.op(*ids))
for i,j in EDGES:
    for a in range(1,4):
        for b in range(1,4):
            ids = [0,0,0]; ids[i] = a; ids[j] = b; PAIR.append(F.op(*ids))
ONE, PAIR = np.array(ONE), np.array(PAIR)
VISIBLE_LABELS = [ids for ids in itertools.product(range(4),repeat=3) if sum(q != 0 for q in ids)==2]
VISIBLE = [F.op(*ids)/np.sqrt(8) for ids in VISIBLE_LABELS]
V0 = F.op(1,1,0)/np.sqrt(8)


def moments(rho, observables):
    return np.einsum('ij,kji->k', rho, observables).real


def correlations(rho):
    one = moments(rho,ONE).reshape(3,3)
    pair = moments(rho,PAIR).reshape(3,3,3)
    return [pair[e]-np.outer(one[i],one[j]) for e,(i,j) in enumerate(EDGES)]


def polar(c):
    u,s,vh = np.linalg.svd(c)
    o = u@vh
    if min(s) <= 0 or np.linalg.det(o) <= 0:
        raise ValueError('outside positive-polar domain')
    return o, o.T@c, s


def polar_derivative(c, dc):
    o,p,_ = polar(c)
    vals,v = np.linalg.eigh((p+p.T)/2)
    if min(vals) <= 0:
        raise ValueError('nonpositive polar factor')
    q = o.T@dc-dc.T@o
    w = v@((v.T@q@v)/(vals[:,None]+vals[None,:]))@v.T
    return o@w


def global_lift(rho):
    os = np.array([polar(c)[0] for c in correlations(rho)])
    return np.einsum('k,kij->ij',os.ravel(),PAIR)/(8*np.sqrt(3))


def regional_lift(rho):
    one = moments(rho,LOCAL_ONE).reshape(2,3)
    c = moments(rho,LOCAL_PAIRS).reshape(3,3)-np.outer(one[0],one[1])
    o = polar(c)[0]
    return np.einsum('k,kij->ij',o.ravel(),LOCAL_PAIRS)/(4*np.sqrt(3))


def memory(rho,h):
    return float(np.trace(h@rho).real)


def field(rho,h):
    return memory(rho,h)*global_lift(rho)


def step(rho,h,strength):
    return rho+strength*field(rho,h)


def regional_step(rho,m,strength):
    return rho+strength*m*regional_lift(rho)


def lift_derivative(rho,v):
    one = moments(rho,ONE).reshape(3,3)
    done = moments(v,ONE).reshape(3,3)
    dpair = moments(v,PAIR).reshape(3,3,3)
    cs = correlations(rho)
    dos = []
    for e,(i,j) in enumerate(EDGES):
        dc = dpair[e]-np.outer(done[i],one[j])-np.outer(one[i],done[j])
        dos.append(polar_derivative(cs[e],dc))
    return np.einsum('k,kij->ij',np.array(dos).ravel(),PAIR)/(8*np.sqrt(3))


def adjudicate(valid,passed,curl_norms):
    if not valid or not curl_norms or not np.isfinite(curl_norms).all():
        return 'INVALID','INVALID'
    primary = 'MEMORY_ENRICHED_NULL_CONFIRMED' if passed else 'MEMORY_ENRICHED_NULL_NOT_CONFIRMED'
    secondary = ('FROZEN_FULL_JACOBIAN_OBSTRUCTED' if max(curl_norms)>1e-8
                 else 'FROZEN_FULL_JACOBIAN_NOT_OBSTRUCTED_ON_PROBES')
    return primary,secondary


def assignment_curl(lift_fn,rho,h,v,eps):
    """Numerically differentiate the full rank-one assignment in both orders."""
    def n(state,tangent):
        return lift_fn(state)*float(np.trace(h@tangent).real)
    dv_nh=(n(rho+eps*v,h)-n(rho-eps*v,h))/(2*eps)
    dh_nv=(n(rho+eps*h,v)-n(rho-eps*h,v))/(2*eps)
    return dv_nh-dh_nv


def domain(states):
    eigen = min(float(np.linalg.eigvalsh(z).min()) for z in states)
    trace = max(float(abs(np.trace(z)-1)) for z in states)
    herm = max(float(np.linalg.norm(z-z.conj().T)) for z in states)
    singular = float('inf'); positive = float('inf')
    for z in states:
        for c in correlations(z):
            _,p,s = polar(c)
            singular = min(singular,float(min(s)))
            positive = min(positive,float(np.linalg.eigvalsh((p+p.T)/2).min()))
    return {'min_density_eigenvalue':eigen,'trace_error':trace,'hermiticity_error':herm,
            'min_edge_singular':singular,'min_positive_polar':positive,
            'valid':bool(eigen>=-1e-12 and trace<=1e-12 and herm<=1e-12 and singular>=.015 and positive>0)}


def finite_numbers(obj):
    if isinstance(obj,dict):
        return all(finite_numbers(v) for v in obj.values())
    if isinstance(obj,(list,tuple)):
        return all(finite_numbers(v) for v in obj)
    if isinstance(obj,(float,int,np.number)):
        return bool(np.isfinite(obj))
    return True


def measure_derivatives(row):
    rho = row['rho']; h = HIDDEN[0]; sigma = rho+ETA*h
    columns = []; rows = []; probes = [rho,sigma]
    for label,v in zip(VISIBLE_LABELS,VISIBLE):
        dy = lift_derivative(rho,v)
        columns.append(V70.coeffs(dy))
        derivative_errors = []; completion_errors = []; curl_errors=[]
        for eps in EPSILONS:
            plus,minus = rho+eps*v,rho-eps*v
            fd = (global_lift(plus)-global_lift(minus))/(2*eps)
            derivative_errors.append(float(np.linalg.norm(fd-dy)/max(1.,np.linalg.norm(dy))))
            curl_fd=assignment_curl(global_lift,rho,h,v,eps)
            curl_errors.append(float(np.linalg.norm(curl_fd-dy)/max(1.,np.linalg.norm(dy))))
            cp,cm = sigma+eps*v,sigma-eps*v
            fdx = (field(cp,h)-field(cm,h))/(2*eps)
            expected = ETA*dy
            completion_errors.append(float(np.linalg.norm(fdx-expected)/max(ETA,np.linalg.norm(expected))))
            probes.extend([plus,minus,cp,cm])
        rows.append({'visible_label':list(label),'curl_column_norm':float(np.linalg.norm(dy)),
                     'DY_verification_errors':derivative_errors,
                     'frozen_jacobian_curl_errors':curl_errors,
                     'visible_completion_errors':completion_errors,
                     'visible_correction_norm':float(ETA*np.linalg.norm(dy))})
    singular = np.linalg.svd(np.column_stack(columns),compute_uv=False)
    ranks = [int(np.sum(singular>singular[0]*tol)) for tol in [1e-9,1e-10,1e-11]]
    # Independently lift a skew target with the historical least-squares constraints.
    a1,ap = GL.derivative_maps(rho);a=np.vstack([a1,ap]);o=GL.rotations(rho)[0]
    k=np.zeros((3,3));k[0,1]=1/np.sqrt(2);k[1,0]=-1/np.sqrt(2)
    b=np.concatenate([np.zeros(9),(o@k).ravel(),np.zeros(18)])
    yc=np.linalg.lstsq(a,b,rcond=None)[0];dc=(ap[:9]@yc).reshape(3,3)
    control=float(np.linalg.norm(o.T@dc-dc.T@o))
    # Feed a constant lift through the same two-order differentiation routine.
    constant=global_lift(rho)
    constant_curl=max(float(np.linalg.norm(assignment_curl(lambda _:constant,rho,h,v,EPSILONS[-1]))) for v in VISIBLE)
    dm=domain(probes)
    valid=dm['valid'] and control>1 and constant_curl==0. and max(max(z['DY_verification_errors']) for z in rows)<=1e-5
    return {'candidate_index':row['candidate_index'],'visible_columns':rows,
            'curl_singular_values':singular.tolist(),'curl_rank_sweep':ranks,
            'skew_control':control,'constant_lift_curl_control':constant_curl,
            'domain':dm,'valid':bool(valid),
            'completion_pass':bool(max(max(z['visible_completion_errors']) for z in rows)<=1e-5)}


def measure_case(base,h,k,index,offset,hidden_label):
    sigma=base+ETA*(h+k); y=global_lift(sigma); mh=memory(sigma,h);mk=memory(sigma,k)
    first=step(sigma,h,S); second=step(sigma,k,U)
    sequential=step(first,k,U); reversed_order=step(second,h,S)
    combined=sigma+S*field(sigma,h)+U*field(sigma,k)
    same=step(first,h,U); same_combined=step(sigma,h,S+U)
    eps=EPSILONS[-1]
    hp,hm=sigma+eps*h,sigma-eps*h
    hidden_error=float(np.linalg.norm((field(hp,h)-field(hm,h))/(2*eps)-y)/np.linalg.norm(y))
    updated=[first,second,sequential,reversed_order,combined,same,same_combined]
    y_change=max(float(np.linalg.norm(global_lift(z)-y)/np.linalg.norm(y)) for z in updated)
    memory_change=max(abs(memory(z,label)-memory(sigma,label)) for z in updated for label in [h,k])
    original_o=[polar(c)[0] for c in correlations(sigma)]
    rotation_change=max(float(np.linalg.norm(polar(c)[0]-original_o[e]))
                        for z in updated for e,c in enumerate(correlations(z)))
    edge_rows=[]
    for e,edge in enumerate(EDGES):
        local=V70.restrict(sigma,edge)
        ly=regional_lift(local)
        local_first=regional_step(local,mh,S)
        local_sequential=regional_step(local_first,mk,U)
        residual=max(float(np.linalg.norm(local_first-V70.restrict(first,edge))),
                     float(np.linalg.norm(local_sequential-V70.restrict(sequential,edge))))
        overlap=max(float(np.linalg.norm(V70.restrict(ly,(q,)))) for q in [0,1])
        omitted=float(np.linalg.norm(mh*ly))
        edge_rows.append({'edge':list(edge),'enriched_restriction_residual':residual,
                          'overlap_source_residual':overlap,'omitted_memory_discrepancy':omitted})
    dm=domain([sigma,hp,hm]+updated)
    source_ok=abs(mh-ETA)<=1e-12 and abs(mk-ETA)<=1e-12
    control_ok=all(e['omitted_memory_discrepancy']>1e-6 for e in edge_rows)
    order_error=float(np.linalg.norm(sequential-reversed_order))
    combined_error=float(np.linalg.norm(sequential-combined))
    additive_error=float(np.linalg.norm(same-same_combined))
    passed=(all(e['enriched_restriction_residual']<=1e-11 and e['overlap_source_residual']<=1e-12 for e in edge_rows)
            and memory_change<=1e-12 and max(order_error,combined_error,additive_error)<=1e-11
            and y_change<=1e-9 and rotation_change<=1e-10 and hidden_error<=1e-9)
    return {'candidate_index':index,'visible_offset':offset,'hidden_label':list(hidden_label),
            'memories':[mh,mk],'edges':edge_rows,'hidden_derivative_relative_error':hidden_error,
            'Y_recomputed_relative_change':y_change,'memory_change':float(memory_change),
            'rotation_change':rotation_change,'order_residual':order_error,
            'combined_residual':combined_error,'same_source_additive_residual':additive_error,
            'domain':dm,'valid':bool(dm['valid'] and source_ok and control_ok),'pass':bool(passed)}


def run_measurement():
    cases=[]; derivatives=[]; bases=[]
    try:
        states=V70.V64.ASYM.select_states()
        indices=[z['candidate_index'] for z in states]
        if indices!=EXPECTED:
            raise ValueError('state identity mismatch')
        hidden_free=max(abs(memory(z['rho'],h)) for z in states for h in HIDDEN)
        for row in states:
            derivatives.append(measure_derivatives(row))
            for offset in [0.,VISIBLE_OFFSET,-VISIBLE_OFFSET]:
                base=row['rho']+offset*V0
                y=global_lift(base); historical,lift_error=V70.V64.target_Y(base)
                agreement=float(np.linalg.norm(y-historical)/np.linalg.norm(historical))
                base_domain=domain([base])
                bases.append({'candidate_index':row['candidate_index'],'visible_offset':offset,
                              'historical_lift_relative_error':agreement,'historical_constraint_error':lift_error,
                              'domain':base_domain,'valid':bool(agreement<=1e-10 and lift_error<=1e-10 and base_domain['valid'])})
                for i,h in enumerate(HIDDEN):
                    cases.append(measure_case(base,h,HIDDEN[(i+1)%27],row['candidate_index'],offset,LABELS[i]))
        valid=(hidden_free<=1e-12 and len(cases)==972 and len(bases)==36
               and all(x['valid'] for x in cases+derivatives+bases)
               and finite_numbers(cases+derivatives+bases))
        passed=all(x['pass'] for x in cases) and all(x['completion_pass'] for x in derivatives)
        curl=[x['curl_column_norm'] for row in derivatives for x in row['visible_columns']]
        verdict,jacobian_verdict=adjudicate(valid,passed,curl)
        return {'verdict':verdict,'jacobian_verdict':jacobian_verdict,'all_valid':bool(valid),
                'candidate_indices':indices,'n_cases':len(cases),'n_edge_restrictions':3*len(cases),
                'hidden_free_memory_max':float(hidden_free),'eta':ETA,'source_amplitudes':[S,U],
                'derivative_epsilons':EPSILONS,'numpy_version':np.__version__,'python_version':sys.version,
                'base_rows':bases,'derivative_rows':derivatives,'rows':cases}
    except Exception as exc:
        return {'verdict':'INVALID','jacobian_verdict':'INVALID','all_valid':False,
                'error':repr(exc),'base_rows':bases,'derivative_rows':derivatives,'rows':cases}


if __name__=='__main__':
    result=V70.finalize_report(run_measurement())
    if result['verdict']=='INVALID':
        result['jacobian_verdict']='INVALID'
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(2 if result['verdict']=='INVALID' else 0)
