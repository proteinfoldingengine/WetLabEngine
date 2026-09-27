"""v15.71: minimal hidden-fiber extension memory and rebased null integrability.

Ordered source strength is an ordering parameter, not fundamental time.
"""
import importlib.util
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
PARENT=HERE.parent

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

V70=load(PARENT/'atlas-descent-composition'/'gate.py','v70_mem')
V64=V70.V64
GL=V64.GL
EDGES=V70.EDGES
HIDDEN=V70.HIDDEN
LABELS=V70.LABELS
EXPECTED=V70.EXPECTED

ETA=1e-4
STRENGTH=1e-3
FLOW_LEVELS=[-1e-2,-3e-3,-1e-3,1e-3,3e-3,1e-2]
REBASE_A=4e-3
REBASE_B=-1.5e-3

I2=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)
Y=np.array([[0,-1j],[1j,0]],dtype=complex)
Z=np.array([[1,0],[0,-1]],dtype=complex)
P=[X,Y,Z]

def memory_gram():
    return np.array([[np.trace(a@b).real for b in HIDDEN] for a in HIDDEN])

def memory(z):
    return np.array([np.trace(h@z).real for h in HIDDEN])

def proper_polar(c):
    u,s,vh=np.linalg.svd(c)
    o=u@vh
    if np.linalg.det(o)<0:
        u[:,-1]*=-1
        o=u@vh
    return o

def local_corr(q):
    out=np.zeros((3,3),float)
    mi=np.array([np.trace(q@np.kron(a,I2)).real for a in P])
    mj=np.array([np.trace(q@np.kron(I2,b)).real for b in P])
    for a in range(3):
        for b in range(3):
            raw=np.trace(q@np.kron(P[a],P[b])).real
            out[a,b]=raw-mi[a]*mj[b]
    return out

def local_retained_lift(q):
    o=proper_polar(local_corr(q))
    d=o/np.sqrt(3)
    y=np.zeros((4,4),dtype=complex)
    for a in range(3):
        for b in range(3):
            y += (d[a,b]/4)*np.kron(P[a],P[b])
    return y

def global_source_step(sigma,rho,y,source_index):
    m=memory(sigma-rho)
    return sigma+STRENGTH*m[source_index]*y

def regional_source_step(q,m,source_index,y_local):
    return q+STRENGTH*m[source_index]*y_local

def adjudicate(valid,confirmed):
    if not valid:
        return 'INVALID'
    return ('MINIMAL_EXTENSION_MEMORY_DESCENT_CONFIRMED' if confirmed
            else 'MINIMAL_EXTENSION_MEMORY_DESCENT_NOT_CONFIRMED')

def adjudicate_rebase(valid,confirmed):
    if not valid:
        return 'INVALID'
    return ('REBASED_NULL_INTEGRABILITY_CONFIRMED' if confirmed
            else 'REBASED_NULL_INTEGRABILITY_NOT_CONFIRMED')

def compression_control():
    row=V64.ASYM.select_states()[0]
    rho=row['rho']
    y,_=V64.target_Y(rho)
    k=26
    plus=rho+ETA*HIDDEN[k]
    minus=rho-ETA*HIDDEN[k]
    mp=memory(plus-rho)
    mm=memory(minus-rho)
    compressed_gap=float(np.linalg.norm(mp[:26]-mm[:26]))
    op=global_source_step(plus,rho,y,k)
    om=global_source_step(minus,rho,y,k)
    retained_gap=float(np.linalg.norm(V70.restrict(op,EDGES[0])-V70.restrict(om,EDGES[0])))
    return {'compressed_memory_gap':compressed_gap,'retained_output_gap':retained_gap}

def state_diag(z):
    return {
        'min_eigenvalue':float(np.linalg.eigvalsh(z).min()),
        'trace_error':float(abs(np.trace(z)-1)),
        'hermiticity_error':float(np.linalg.norm(z-z.conj().T)),
    }

def positive_polar_min(z):
    out=float('inf')
    oz=GL.rotations(z)
    for ei,e in enumerate(EDGES):
        c=V64.ASYM.F.corr(z,*e)
        p=oz[ei].T@c
        out=min(out,float(np.linalg.eigvalsh((p+p.T)/2).min()))
    return out

def measure_descent_state(row):
    rho=row['rho']
    y,lift=V64.target_Y(rho)
    yr=[V70.restrict(y,e) for e in EDGES]
    q0=[V70.restrict(rho,e) for e in EDGES]
    yl=[local_retained_lift(q) for q in q0]
    lift_local_rel=[float(np.linalg.norm(a-b)/np.linalg.norm(b)) for a,b in zip(yl,yr)]
    max_mem_err=0.
    max_abs=0.
    max_rel=0.
    witness_count=0
    finite=[rho]
    worst=None
    for ai,h in enumerate(HIDDEN):
        for sign in (-1,1):
            sigma=rho+sign*ETA*h
            finite.append(sigma)
            m=memory(sigma-rho)
            expect=np.zeros(27);expect[ai]=sign*ETA
            max_mem_err=max(max_mem_err,float(np.max(np.abs(m-expect))))
            for bi in range(27):
                gout=global_source_step(sigma,rho,y,bi)
                # All nonmatching source-label outputs equal sigma analytically; checking
                # positivity on the matching output plus sigma covers the distinct states.
                if bi==ai:
                    finite.append(gout)
                for ei,e in enumerate(EDGES):
                    q=V70.restrict(sigma,e)
                    rout=regional_source_step(q,m,bi,yl[ei])
                    actual=V70.restrict(gout,e)
                    absres=float(np.linalg.norm(actual-rout))
                    upd=STRENGTH*m[bi]*yl[ei]
                    un=float(np.linalg.norm(upd))
                    rel=0. if un<=1e-14 else absres/un
                    max_abs=max(max_abs,absres)
                    max_rel=max(max_rel,rel)
                    witness_count+=1
                    if worst is None or absres>worst['absolute_residual']:
                        worst={'hidden_index':ai,'hidden_label':list(LABELS[ai]),
                               'source_index':bi,'source_label':list(LABELS[bi]),
                               'sign':sign,'edge':list(e),
                               'absolute_residual':absres,'relative_residual':rel,
                               'memory_pairing':float(m[bi])}
    sd={
        'min_eigenvalue':float(min(np.linalg.eigvalsh(z).min() for z in finite)),
        'trace_error':float(max(abs(np.trace(z)-1) for z in finite)),
        'hermiticity_error':float(max(np.linalg.norm(z-z.conj().T) for z in finite)),
    }
    valid=(lift<=1e-10 and max(lift_local_rel)<=1e-10 and max_mem_err<=1e-12
           and sd['min_eigenvalue']>=-1e-12 and sd['trace_error']<=1e-12
           and sd['hermiticity_error']<=1e-12)
    confirmed=(max_abs<=1e-12 and max_rel<=1e-9)
    return {
        'candidate_index':row['candidate_index'],
        'lift_relative_residual':float(lift),
        'local_lift_relative_residual_max':max(lift_local_rel),
        'memory_coordinate_error_max':max_mem_err,
        'enriched_output_absolute_residual_max':max_abs,
        'enriched_output_relative_residual_max':max_rel,
        'n_witnesses':witness_count,
        'finite_state_diagnostics':sd,
        'worst_witness':worst,
        'valid':bool(valid),
        'confirmed':bool(confirmed),
    }

def measure_rebase_state(row):
    rho=row['rho']
    y0,lift0=V64.target_Y(rho)
    o0=GL.rotations(rho)
    c0=[V64.ASYM.F.corr(rho,*e) for e in EDGES]
    max_y=0.;max_mem=0.;max_rot=0.;max_local=0.;max_null=0.;max_corr=0.
    min_density=float('inf');min_polar=float('inf');max_trace=0.;max_herm=0.
    levels=[]
    for c in FLOW_LEVELS:
        z=rho+c*y0
        yc,lift=V64.target_Y(z)
        oc=GL.rotations(z)
        yrel=float(np.linalg.norm(yc-y0)/np.linalg.norm(y0))
        memdrift=float(np.max(np.abs(memory(z-rho))))
        rot=max(float(np.linalg.norm(oc[i]-o0[i])) for i in range(3))
        local=0.;null=0.;corrres=0.
        coeff=V70.coeffs(yc)
        a1,ap=GL.derivative_maps(z)
        for ei,e in enumerate(EDGES):
            q=V70.restrict(z,e)
            yl=local_retained_lift(q)
            yr=V70.restrict(yc,e)
            local=max(local,float(np.linalg.norm(yl-yr)/np.linalg.norm(yr)))
            d=(ap[9*ei:9*(ei+1)]@coeff).reshape(3,3)
            null=max(null,float(np.linalg.norm(oc[ei].T@d-d.T@oc[ei])/np.linalg.norm(d)))
            pred=c0[ei]+c*o0[ei]/np.sqrt(3)
            corrres=max(corrres,float(np.linalg.norm(V64.ASYM.F.corr(z,*e)-pred)))
        sd=state_diag(z)
        pp=positive_polar_min(z)
        max_y=max(max_y,yrel);max_mem=max(max_mem,memdrift);max_rot=max(max_rot,rot)
        max_local=max(max_local,local);max_null=max(max_null,null);max_corr=max(max_corr,corrres)
        min_density=min(min_density,sd['min_eigenvalue']);min_polar=min(min_polar,pp)
        max_trace=max(max_trace,sd['trace_error']);max_herm=max(max_herm,sd['hermiticity_error'])
        levels.append({'strength':c,'lift_relative_change':yrel,'memory_drift':memdrift,
                       'rotation_change':rot,'local_lift_relative_residual':local,
                       'null_relative_residual':null,'correlation_path_residual':corrres,
                       'min_density_eigenvalue':sd['min_eigenvalue'],
                       'min_positive_polar_eigenvalue':pp,'lift_solve_residual':float(lift)})
    za=rho+REBASE_A*y0
    ya,resa=V64.target_Y(za)
    seq_ab=za+REBASE_B*ya
    zb=rho+REBASE_B*y0
    yb,resb=V64.target_Y(zb)
    seq_ba=zb+REBASE_A*yb
    direct=rho+(REBASE_A+REBASE_B)*y0
    order=float(np.linalg.norm(seq_ab-seq_ba))
    combined=max(float(np.linalg.norm(seq_ab-direct)),float(np.linalg.norm(seq_ba-direct)))
    edge_combined=max(float(np.linalg.norm(V70.restrict(seq_ab,e)-V70.restrict(direct,e)))
                      for e in EDGES)
    edge_order=max(float(np.linalg.norm(V70.restrict(seq_ab,e)-V70.restrict(seq_ba,e)))
                   for e in EDGES)
    for z in [za,zb,seq_ab,seq_ba,direct]:
        sd=state_diag(z)
        min_density=min(min_density,sd['min_eigenvalue'])
        min_polar=min(min_polar,positive_polar_min(z))
        max_trace=max(max_trace,sd['trace_error'])
        max_herm=max(max_herm,sd['hermiticity_error'])
    valid=(lift0<=1e-10 and resa<=1e-10 and resb<=1e-10
           and min_density>=-1e-12 and min_polar>0
           and max_trace<=1e-12 and max_herm<=1e-12)
    confirmed=(max_y<=1e-10 and max_mem<=1e-12 and max_rot<=1e-10
               and max_local<=1e-10 and max_null<=1e-10
               and order<=1e-11 and combined<=1e-11
               and edge_combined<=1e-11 and edge_order<=1e-11)
    return {
        'candidate_index':row['candidate_index'],
        'levels':levels,
        'max_lift_relative_change':max_y,
        'max_memory_drift':max_mem,
        'max_rotation_change':max_rot,
        'max_local_lift_relative_residual':max_local,
        'max_null_relative_residual':max_null,
        'max_correlation_path_residual':max_corr,
        'sequential_order_residual':order,
        'sequential_combined_residual':combined,
        'edge_sequential_order_residual':edge_order,
        'edge_sequential_combined_residual':edge_combined,
        'min_density_eigenvalue':min_density,
        'min_positive_polar_eigenvalue':min_polar,
        'max_trace_error':max_trace,
        'max_hermiticity_error':max_herm,
        'valid':bool(valid),
        'confirmed':bool(confirmed),
    }

def run_measurement():
    rows=[]
    rebase=[]
    try:
        states=V64.ASYM.select_states()
        indices=[x['candidate_index'] for x in states]
        if indices!=EXPECTED:
            return {'verdict':'INVALID','rebasing_verdict':'INVALID','n_states':len(states),
                    'n_descent_witnesses':0,'error':'state identity mismatch','rows':[]}
        gram=memory_gram()
        sv=np.linalg.svd(gram,compute_uv=False)
        gram_rank=int(np.linalg.matrix_rank(gram))
        gram_err=float(np.max(np.abs(gram-np.eye(27))))
        comp=compression_control()
        rows=[measure_descent_state(x) for x in states]
        rebase=[measure_rebase_state(x) for x in states]
        n=sum(x['n_witnesses'] for x in rows)
        valid=(gram_rank==27 and gram_err<=1e-12 and len(rows)==12 and n==52488
               and all(x['valid'] for x in rows)
               and comp['compressed_memory_gap']<=1e-12
               and comp['retained_output_gap']>1e-8)
        confirmed=all(x['confirmed'] for x in rows)
        rvalid=len(rebase)==12 and all(x['valid'] for x in rebase)
        rconfirmed=all(x['confirmed'] for x in rebase)
        return {
            'verdict':adjudicate(valid,confirmed),
            'rebasing_verdict':adjudicate_rebase(rvalid,rconfirmed),
            'n_states':len(states),
            'candidate_indices':indices,
            'n_descent_witnesses':n,
            'memory_dimension':27,
            'memory_gram_rank':gram_rank,
            'memory_gram_max_identity_error':gram_err,
            'memory_gram_singular_values':[float(x) for x in sv],
            'compression_control':comp,
            'eta':ETA,'source_strength':STRENGTH,
            'flow_levels':FLOW_LEVELS,
            'rebase_increments':[REBASE_A,REBASE_B],
            'python_version':sys.version,'numpy_version':np.__version__,
            'rows':rows,
            'rebasing_rows':rebase,
        }
    except Exception as exc:
        return {'verdict':'INVALID','rebasing_verdict':'INVALID','n_states':0,
                'n_descent_witnesses':0,'error':repr(exc),'rows':rows,'rebasing_rows':rebase}

def finalize_report(report):
    nonfinite=[]
    def clean(v,path):
        if isinstance(v,dict):
            return {k:clean(x,path+'.'+k) for k,x in v.items()}
        if isinstance(v,list):
            return [clean(x,path+'['+str(i)+']') for i,x in enumerate(v)]
        if isinstance(v,(float,np.floating)) and not np.isfinite(v):
            nonfinite.append(path);return None
        return v
    out=clean(report,'report')
    if nonfinite:
        out['verdict']='INVALID';out['rebasing_verdict']='INVALID'
        out['nonfinite_diagnostic_paths']=nonfinite
    return out

if __name__=='__main__':
    r=finalize_report(run_measurement())
    print(json.dumps(r,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(2 if r['verdict']=='INVALID' or r['rebasing_verdict']=='INVALID' else 0)
