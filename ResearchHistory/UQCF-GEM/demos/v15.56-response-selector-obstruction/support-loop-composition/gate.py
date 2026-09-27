"""v15.83: native surviving support and raw spatial-loop composition."""
import functools
import hashlib
import importlib.util
import json
import pathlib
import sys
import numpy as np
import sympy as sp
import mpmath as mp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('boundary82_support',HERE.parent/'polar-boundary-obstruction'/'gate.py')
V82=importlib.util.module_from_spec(spec);spec.loader.exec_module(V82)
M=V82.M;V81=V82.V81
PARENT_HASH='a60feb6ab4506e8049d72c6a4e85627ae6f9137e3509aa9da44e14f6f151df56'
DELTAS=['1e-3','1e-5','1e-7'];THRESHOLDS=['1e-9','1e-10','1e-11']
num=V82.number;mat=V82.serial_matrix;maxabs=V82.maxabs


def composition_verdict(defects):
    values=[mp.mpf(str(x)) for x in defects]
    if any(x>=mp.mpf('1e-8') for x in values):return 'SUPPORT_LOOP_COMPOSITION_OBSTRUCTED'
    if all(x<=mp.mpf('1e-40') for x in values):return 'SUPPORT_LOOP_COMPOSITION_CLOSED'
    return 'SUPPORT_LOOP_COMPOSITION_UNRESOLVED'


def core_verdict(dimensions):
    if dimensions==[0,0,0]:return 'LOSSLESS_LOOP_CORE_TRIVIAL'
    if len(set(dimensions))==1 and dimensions[0]>0:return 'LOSSLESS_LOOP_CORE_NONTRIVIAL'
    return 'LOSSLESS_LOOP_CORE_UNRESOLVED'


def power_diagnostics(loop):
    eye=mp.eye(3);p=loop.T*loop;deficit=eye-p
    powers=[eye]
    for n in range(4):powers.append(powers[-1]*loop)
    rows=[]
    for n in range(1,5):
        a=powers[n].T*powers[n];g=eye-a;tel=mp.zeros(3);stack=mp.zeros(3*n,3)
        for k in range(n):
            term=deficit*powers[k];tel+=powers[k].T*term
            for i in range(3):
                for j in range(3):stack[3*k+i,j]=term[i,j]
        eigen=mp.eigsy(g,eigvals_only=True)
        stacked_sv=mp.svd_r(stack,compute_uv=False)
        dims=[sum(v<=mp.mpf(t) for v in eigen) for t in THRESHOLDS]
        stack_dims=[sum(v*v<=mp.mpf(t) for v in stacked_sv) for t in THRESHOLDS]
        sv=mp.svd_r(powers[n],compute_uv=False)
        rows.append({'n':n,'matrix':mat(powers[n]),'singular_values':[num(v) for v in sv],
                     'partial_isometry_defect':num(mp.norm(a*a-a)),
                     'loss_gramian':mat(g),'loss_eigenvalues':[num(v) for v in eigen],
                     'lossless_dimensions':dims,'stacked_constraint_singular_values':[num(v) for v in stacked_sv],
                     'stacked_lossless_dimensions':stack_dims,
                     'telescoping_residual':num(maxabs(g-tel)),
                     'valid':bool(maxabs(g-tel)<=mp.mpf('1e-50') and min(eigen)>=-mp.mpf('1e-50') and
                                  max(eigen)<=1+mp.mpf('1e-50') and dims==stack_dims)})
    return rows


def synthetic_controls():
    with mp.workdps(80):
        p=mp.diag([1,1,0]);r=mp.matrix([[mp.mpf(3)/5,0,mp.mpf(4)/5],[0,1,0],[-mp.mpf(4)/5,0,mp.mpf(3)/5]])
        cycle=mp.matrix([[0,1,0],[0,0,1],[1,0,0]])
        closed=power_diagnostics(p);attenuated=power_diagnostics(p*r);nilpotent=power_diagnostics(p*cycle)
        closed_dims=[row['lossless_dimensions'][0] for row in closed]
        cycle_dims=[row['lossless_dimensions'][0] for row in nilpotent]
        cs=max(mp.mpf(row['partial_isometry_defect']) for row in closed)
        sa=attenuated[1]['singular_values'];se=max(abs(mp.mpf(sa[i])-[mp.mpf(1),mp.mpf(3)/5,mp.mpf(0)][i]) for i in range(3))
        de=abs(mp.mpf(attenuated[1]['partial_isometry_defect'])-mp.mpf(144)/625)
        nz=max(abs(mp.mpf(v)) for row in nilpotent[2]['matrix'] for v in row)
        valid=(all(row['valid'] for table in [closed,attenuated,nilpotent] for row in table) and
               all(row['lossless_dimensions']==[2]*3 for row in closed) and
               all(row['lossless_dimensions']==[d]*3 for row,d in zip(nilpotent,[2,1,0,0])) and
               max(cs,se,de,nz)<=mp.mpf('1e-45'))
        return {'valid':bool(valid),'projector_dimensions':closed_dims,'cycle_dimensions':cycle_dims,
                'projector_max_defect':num(cs),'attenuated_square_singular_values':sa,
                'attenuated_square_defect':attenuated[1]['partial_isometry_defect'],
                'attenuated_spectrum_error':num(se),'attenuated_defect_error':num(de),'cycle_cubed_norm':num(nz)}


@functools.lru_cache(maxsize=1)
def run_measurement():
    with mp.workdps(80):return _run()


def _run():
    payload=(HERE.parent/'polar-boundary-obstruction'/'RESULT.json').read_bytes()
    prior=json.loads(payload);hash_ok=hashlib.sha256(payload).hexdigest()==PARENT_HASH
    parent_ok=prior['all_valid'] and prior['verdict']=='POLAR_CONTINUATION_OBSTRUCTION_CONFIRMED'
    rho=np.array([[complex(float.fromhex(x),float.fromhex(y)) for x,y in row] for row in prior['input_hex']])
    selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
    reference=next(r['rho'] for r in selected if r['candidate_index']==46)
    r0=V82.exact_matrix(rho);b=V82.exact_matrix(V81.PP-V81.QQ);r1=sp.expand(b*r0*b/2)
    root_interval=prior['root_intervals'][0]
    xr=(sp.Rational(root_interval['left'])+sp.Rational(root_interval['right']))/2
    x=V82.mp_scalar(xr);u0=-mp.log(x)/2
    r0m=V82.mp_matrix(r0);r1m=V82.mp_matrix(r1)
    state=lambda t:((1+t)*r0m+(1-t)*r1m)/2
    q=V82.q
    def op(site,a):
        labels=[0,0,0];labels[site]=a;return V82.exact_matrix(M.F.op(*labels))
    def moment(o):return sp.expand(((1+q)*sp.trace(r0*o)+(1-q)*sp.trace(r1*o))/2)
    polynomials=[]
    for i,j in M.EDGES:
        left=[op(i,a) for a in [1,2,3]];right=[op(j,a) for a in [1,2,3]]
        ml=[moment(o) for o in left];mr=[moment(o) for o in right]
        polynomials.append(sp.Matrix(3,3,lambda a,d:sp.expand(moment(left[a]*right[d])-ml[a]*mr[d])))
    root_c=[V82.matrix_at(c,x) for c in polynomials]
    uu,ss,vv=mp.svd_r(root_c[0]);v=uu*mp.diag([1,1,0])*vv
    previous=mp.matrix([[mp.mpf(t) for t in row] for row in prior['root']['correlation']])
    identity=maxabs(root_c[0]-previous)
    polar_checks=[];root_edges=[];root_factors=[v];regular=True
    for k,c in enumerate(root_c):
        if k==0:
            root_edges.append({'edge':list(M.EDGES[k]),'singular_values':[num(t) for t in ss],
                               'factor':mat(v),'factor_kind':'rank_two_partial_isometry_approximation'})
        else:
            o,s,pc=V82.polar(c);root_factors.append(o);polar_checks.append(pc)
            det=mp.det(o);regular=regular and min(s)>=mp.mpf('1e-4') and abs(det-1)<=mp.mpf('1e-40')
            root_edges.append({'edge':list(M.EDGES[k]),'singular_values':[num(t) for t in s],
                               'factor':mat(o),'factor_kind':'orthogonal_polar','determinant':num(det)})
    loop=root_factors[0]*root_factors[1]*root_factors[2]
    p=loop.T*loop;qout=loop*loop.T;eye=mp.eye(3)
    trace=lambda a:sum(a[i,i] for i in range(a.rows))
    projector_checks={'P_symmetry':maxabs(p-p.T),'Q_symmetry':maxabs(qout-qout.T),
                      'P_idempotence':maxabs(p*p-p),'Q_idempotence':maxabs(qout*qout-qout),
                      'partial_isometry':maxabs(loop*loop.T*loop-loop),
                      'P_trace':abs(trace(p)-2),'Q_trace':abs(trace(qout)-2)}
    densities=[{'label':'original','value':V82.density(r0m)},{'label':'root','value':V82.density(state(x))}]
    crossing=[]
    for delta in DELTAS:
        row={'delta':delta};factors=[]
        for label,us in [('before',u0-mp.mpf(delta)),('after',u0+mp.mpf(delta))]:
            xs=mp.exp(-2*us);os=[]
            for c in polynomials:
                o,s,pc=V82.polar(V82.matrix_at(c,xs));os.append(o);polar_checks.append(pc)
            ls=os[0]*os[1]*os[2];factors.append(ls)
            row[label]={'strength':num(us),'loop':mat(ls),'determinant':num(mp.det(ls)),
                        'restricted_error':num(mp.norm(ls*p-loop))}
            densities.append({'label':delta+'_'+label,'value':V82.density(state(xs))})
        diff=factors[0]-factors[1]
        row['restricted_difference']=num(mp.norm(diff*p));row['full_difference']=num(mp.norm(diff));crossing.append(row)
    powers=power_diagnostics(loop)
    c2=trace((eye-p)*(eye-qout));c2valid=-mp.mpf('1e-50')<=c2<=1+mp.mpf('1e-50')
    cvalue=mp.sqrt(min(mp.mpf(1),max(mp.mpf(0),c2)))
    expected=[mp.mpf(1),cvalue,mp.mpf(0)]
    spectrum_error=max(abs(mp.mpf(powers[1]['singular_values'][i])-expected[i]) for i in range(3))
    defect=mp.mpf(powers[1]['partial_isometry_defect']);comm=mp.norm(p*qout-qout*p)
    scalar_error=abs(defect-c2*(1-c2));comm_error=abs(defect-comm**2/2)
    synthetic=synthetic_controls()
    controls={'parent_hash_valid':hash_ok,'parent_verdict_valid':bool(parent_ok),
              'selector_valid':indices==M.EXPECTED,
              'input_selector_error':float(np.max(np.abs(rho-reference))),
              'complex_roundtrip_error':float(np.max(np.abs(V82.to_numpy(r0)-rho))),
              'source_unitary_exact':bool(b*b/2==sp.eye(8)),
              'root_source_edge_identity_error':num(identity),
              'root_rank_two_guard':bool(ss[2]<=mp.mpf('1e-45') and ss[1]>=mp.mpf('1e-4')),
              'other_root_edges_regular':bool(regular),
              'projector_checks':{k:num(t) for k,t in projector_checks.items()},
              'max_polar_residual':num(max(t for pc in polar_checks for t in pc.values())),
              'density_valid':all(V82.density_valid(row['value']) for row in densities),
              'powers_valid':all(row['valid'] for row in powers),'c_squared_range_valid':bool(c2valid),
              'square_spectrum_error':num(spectrum_error),'square_defect_formula_error':num(scalar_error),
              'commutator_formula_error':num(comm_error),'synthetic':synthetic}
    valid=(hash_ok and parent_ok and controls['selector_valid'] and
           controls['input_selector_error']<=1e-16 and controls['complex_roundtrip_error']<=1e-16 and
           controls['source_unitary_exact'] and identity<=mp.mpf('1e-60') and controls['root_rank_two_guard'] and regular and
           max(projector_checks.values())<=mp.mpf('1e-50') and mp.mpf(controls['max_polar_residual'])<=mp.mpf('1e-50') and
           controls['density_valid'] and controls['powers_valid'] and c2valid and
           max(spectrum_error,scalar_error,comm_error)<=mp.mpf('1e-45') and synthetic['valid'])
    last=crossing[-1]
    passed=(max(mp.mpf(last[k]['restricted_error']) for k in ['before','after'])<=mp.mpf('1e-5') and
            mp.mpf(last['restricted_difference'])<=mp.mpf('1e-5') and mp.mpf(last['full_difference'])>=mp.mpf('1.9'))
    cv='SUPPORT_RESTRICTED_CROSSING_CONFIRMED' if passed else 'SUPPORT_RESTRICTED_CROSSING_NOT_CONFIRMED'
    report={'version':'15.83','candidate_index':46,'candidate_indices':indices,'lambda':-1,'precision_digits':80,
            'parent_result_sha256':PARENT_HASH,'root_q_midpoint':num(x),'root_strength':num(u0),
            'all_valid':bool(valid),'crossing_verdict':cv,
            'composition_verdict':composition_verdict([row['partial_isometry_defect'] for row in powers[1:]]),
            'core_verdict':core_verdict(powers[2]['lossless_dimensions']),
            'controls':controls,'root_edges':root_edges,'loop':mat(loop),'initial_projector':mat(p),'final_projector':mat(qout),
            'c_squared':num(c2),'projector_commutator_norm':num(comm),'crossing_rows':crossing,'powers':powers,
            'three_traversal_operator_norm':powers[2]['singular_values'][0],
            'densities':densities,'root_Q':None,'root_E':None,
            'scope':'Raw spatial loop composition at one frozen slice. Common frames for cross-slice comparisons; no repolarization.'}
    def finite(a):
        if isinstance(a,dict):return all(finite(v) for v in a.values())
        if isinstance(a,list):return all(finite(v) for v in a)
        if isinstance(a,float):return bool(np.isfinite(a))
        if isinstance(a,str):return a.lower() not in ['nan','inf','+inf','-inf']
        return True
    if not finite(report):report['all_valid']=False
    if not report['all_valid']:
        for key in ['crossing_verdict','composition_verdict','core_verdict']:report[key]='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
