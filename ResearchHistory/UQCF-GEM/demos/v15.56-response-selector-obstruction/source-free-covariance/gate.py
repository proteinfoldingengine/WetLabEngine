"""v15.78: fixed-law local covariance, distinct from source-family covariance."""
import importlib.util
import itertools
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('active77_covariance',HERE.parent/'active-baseline-null'/'gate.py')
V77=importlib.util.module_from_spec(spec);spec.loader.exec_module(V77)
V75=V77.V75;M=V77.M
LABELS=list(itertools.product(range(4),repeat=3))
BASIS=np.array([M.F.op(*p)/np.sqrt(8) for p in LABELS])
SUPPORTS=[tuple(i for i,a in enumerate(p) if a) for p in LABELS]
SECTORS=[np.array([i for i,s in enumerate(SUPPORTS) if s==support])
         for support in sorted(set(SUPPORTS),key=lambda s:(len(s),s))]
HIDX=np.array([i for i,p in enumerate(LABELS) if sum(a!=0 for a in p)==3])
RIDX=np.array([i for i,p in enumerate(LABELS) if sum(a!=0 for a in p) in (1,2)])
THRESHOLDS=[1e-9,1e-10,1e-11]


def support_project(l):
    out=np.zeros_like(l)
    for ids in SECTORS:out[ids,ids]=np.mean(np.diag(l)[ids])
    return out


def cliffords():
    out=[]
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((-1,1),repeat=3):
            r=np.zeros((3,3),int);r[perm,range(3)]=signs
            if round(np.linalg.det(r))==1:out.append(r)
    return out


def site_action(r,site):
    t=np.zeros((4,4));t[0,0]=1;t[1:,1:]=r
    factors=[t if q==site else np.eye(4) for q in range(3)]
    return np.kron(np.kron(factors[0],factors[1]),factors[2])


def finite_twirl(l,actions):
    out=l.copy()
    for site in actions:out=sum(a.T@out@a for a in site)/len(site)
    return out


def apply_ptm(l,z):
    coeff=np.einsum('aij,ji->a',BASIS,z)
    return np.einsum('a,aij->ij',l@coeff,BASIS)


def transfer(phi):
    outputs=np.array([phi(e) for e in BASIS])
    return np.einsum('aij,bji->ab',BASIS,outputs)


def characterize(a,reference=None):
    sv=np.linalg.svd(a,compute_uv=False)
    ref=float(sv[0]) if reference is None else float(reference)
    return {'norm':float(np.linalg.norm(a)),'singular_values':sv.tolist(),
            'reference':ref,'ranks':[int(np.count_nonzero(sv>t*ref)) for t in THRESHOLDS]}


def adjudicate(valid,primary,secondary):
    if not valid:return 'INVALID','INVALID'
    return ('SOURCE_FREE_COVARIANCE_FORCES_RETAINED_CLOSURE' if primary else 'SOURCE_FREE_COVARIANCE_CLOSURE_NOT_CONFIRMED',
            'COVARIANTIZATION_ERASES_POSITIVE_AND_NULL_LEAKAGE' if secondary else 'COVARIANTIZATION_ERASURE_NOT_CONFIRMED')


def run_measurement():
    c={};mx=lambda k,v:V77.maximize(c,k,v)
    selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
    domain=M.domain([r['rho'] for r in selected])
    mx('basis_orthogonality',np.linalg.norm(np.einsum('aij,bji->ab',BASIS,BASIS)-np.eye(64)))
    rotations=cliffords();actions=[[site_action(r,q) for r in rotations] for q in range(3)]
    group_ok=len(rotations)==24 and len({tuple(r.ravel()) for r in rotations})==24
    for r in rotations:
        group_ok=group_ok and round(np.linalg.det(r))==1
        mx('rotation_orthogonality',np.linalg.norm(r.T@r-np.eye(3)))
    for acts in actions:
        for a in acts:mx('adjoint_orthogonality',np.linalg.norm(a.T@a-np.eye(64)))
    # Six exact integer characters, independently checked on complex matrices.
    chars=[]
    for site in range(3):
        for axis in (1,3):
            p=[0,0,0];p[site]=axis;u=M.F.op(*p)
            char=np.array([1 if lab[site] in (0,axis) else -1 for lab in LABELS],int)
            chars.append(char)
            mx('character_matrix_error',np.linalg.norm(np.array([u@e@u.conj().T for e in BASIS])-char[:,None,None]*BASIS))
    chars=np.array(chars);gram=np.sum((chars[:,RIDX,None]-chars[:,None,HIDX])**2,axis=0)
    full_match=np.all(chars[:,:,None]==chars[:,None,:],axis=0)
    # Determine actual finite-group orbits, without using support labels.
    unseen=set(range(64));orbits=[]
    while unseen:
        orbit={min(unseen)};front=list(orbit)
        while front:
            k=front.pop()
            for acts in actions:
                for a in acts:
                    j=int(np.argmax(np.abs(a[:,k])))
                    if j not in orbit:orbit.add(j);front.append(j)
        unseen-=orbit;orbits.append(sorted(orbit))
    primary=(len(set(map(tuple,chars.T)))==64 and int(full_match.sum())==64
             and gram.shape==(36,27) and bool(np.all(gram>0))
             and sorted(map(len,orbits))==[1,3,3,3,9,9,9,27])
    generic=[]
    for site in range(3):
        for axis,angle in [(0,np.pi/7),(2,np.pi/5)]:
            n=np.eye(3)[axis]
            cross=np.array([[0,-n[2],n[1]],[n[2],0,-n[0]],[-n[1],n[0],0]])
            r=np.cos(angle)*np.eye(3)+(1-np.cos(angle))*np.outer(n,n)+np.sin(angle)*cross
            generic.append(site_action(r,site))
    dense=np.fromfunction(lambda i,j:(((i+1)*(j+3))%101-50)/101,(64,64))
    def projection_controls(l):
        p=support_project(l)
        mx('finite_twirl_projection_error',np.linalg.norm(finite_twirl(l,actions)-p))
        mx('projection_idempotence',np.linalg.norm(support_project(p)-p))
        for a in generic:mx('generic_rotation_commutator',np.linalg.norm(p@a-a@p))
        return p
    projection_controls(dense)
    units=[]
    for i in range(8):
        for j in range(8):
            z=np.zeros((8,8),complex);z[i,j]=1;units.append(z)
    hidden=np.array(M.HIDDEN);a=M.F.op(1,1,1)
    u=np.cos(np.pi/8)*np.eye(8)-1j*np.sin(np.pi/8)*M.F.op(1,1,0)
    rows=[];cp_rows=[];prepared=[];before_ok=True;cp_ok=True;erased=True
    for rec in selected:
        rho=rec['rho'];y=M.global_lift(rho);b=rho+.02*y
        pd=V75.density_diagnostics([b+.01*y,b-.01*y]);prepared.append({'candidate_index':rec['candidate_index'],**pd})
        cp_ok=cp_ok and pd['valid']
        channels={'active_symmetric':lambda z:np.trace(z)*b+.01*np.trace(a@z)*y,
                  'unitary_XXI':lambda z:u@z@u.conj().T,'identity':lambda z:z}
        for name,phi in channels.items():
            raw=transfer(phi);mx('PTM_imaginary',np.max(np.abs(raw.imag)));l=raw.real
            for z in units:mx('PTM_reconstruction',np.linalg.norm(apply_ptm(l,z)-phi(z)))
            projected=projection_controls(l);leading=None;original_leak=None
            for stage,mat in [('original',l),('projected',projected)]:
                cp=V75.cp_diagnostics(V75.choi(lambda z:apply_ptm(mat,z)))
                cp_rows.append({'candidate_index':rec['candidate_index'],'channel':name,'stage':stage,**cp});cp_ok=cp_ok and cp['valid']
                ys=np.array([apply_ptm(mat,h)-h for h in hidden])
                coeff=np.einsum('hij,kji->kh',ys,V75.G).real
                q,e,sy=V77.extract(rho,ys);mx('sylvester',sy)
                if stage=='original':
                    leading=[float(np.linalg.svd(v,compute_uv=False)[0]) for v in (coeff,q,e)]
                    if name=='active_symmetric':leading[1:]=[leading[0],leading[0]]
                    if name=='identity':leading=[1.,1.,1.]
                    original_leak=float(np.linalg.norm(coeff))
                metrics={key:characterize(v,ref) for key,v,ref in zip(('retained','Q','E'),(coeff,q,e),leading)}
                # Before positive ranks use each matrix's own leading value.
                if stage=='original' and name=='unitary_XXI':
                    before_ok=before_ok and original_leak>=1 and metrics['retained']['ranks']==[12]*3 and metrics['Q']['ranks']==[6]*3 and metrics['E']['ranks']==[6]*3
                if stage=='original' and name=='active_symmetric':
                    before_ok=before_ok and original_leak>=.01 and np.linalg.norm(q)<=1e-9*original_leak and np.linalg.norm(e)<=1e-8*original_leak
                if name=='identity':before_ok=before_ok and max(np.linalg.norm(v) for v in (coeff,q,e))<=1e-12
                if stage=='projected' and name!='identity':
                    erased=erased and np.linalg.norm(coeff)<=1e-12*original_leak and np.linalg.norm(q)<=1e-10*original_leak and np.linalg.norm(e)<=1e-9*original_leak and all(v['ranks']==[0]*3 for v in metrics.values())
                    if name=='active_symmetric':
                        dep=np.zeros((64,64));dep[0,0]=1
                        error=float(np.linalg.norm(mat-dep));mx('null_channel_depolarization_error',error);erased=erased and error<=1e-12
                rows.append({'candidate_index':rec['candidate_index'],'channel':name,'stage':stage,
                             'original_retained_norm':original_leak,**metrics,
                             'support_scalars':[float(np.mean(np.diag(mat)[ids])) for ids in SECTORS] if stage=='projected' else None})
    error_keys=['basis_orthogonality','rotation_orthogonality','adjoint_orthogonality','character_matrix_error',
                'finite_twirl_projection_error','projection_idempotence','generic_rotation_commutator','PTM_imaginary','PTM_reconstruction','sylvester']
    valid=(indices==M.EXPECTED and domain['valid'] and group_ok and cp_ok and before_ok
           and len(HIDX)==27 and len(RIDX)==36 and all(c[k]<=1e-12 for k in error_keys))
    c.update({'group_valid':bool(group_ok),'CP_valid':bool(cp_ok),'before_controls_valid':bool(before_ok)})
    verdict,erasure=adjudicate(valid,primary,erased)
    report={'version':'15.78','candidate_indices':indices,'hidden_probes_per_row':27,
            'all_valid':bool(valid),'verdict':verdict,'erasure_verdict':erasure,'controls':c,'domain':domain,
            'classification':{'distinct_characters':len(set(map(tuple,chars.T))),
                              'Pauli_commutant_dimension':int(full_match.sum()),'hidden_retained_Gram':gram.tolist(),
                              'hidden_retained_constraint_rank':int(np.count_nonzero(gram)),
                              'hidden_retained_nullity':int(np.count_nonzero(gram==0)),
                              'axis_orbits':orbits,'orbit_sizes':sorted(map(len,orbits))},
            'rows':rows,'Choi':cp_rows,'prepared_states':prepared}
    report=M.V70.finalize_report(report)
    if not report['all_valid']:report['erasure_verdict']='INVALID'
    return report

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False))
    sys.exit(0 if result['all_valid'] else 2)
