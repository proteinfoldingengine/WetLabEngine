"""UQCF-GEM: an executable, matrix-derived quantum compatibility laboratory.

The implemented example is the matched four-weight family in v9.167--v9.171.
It is NOT the different product-reference family from v9.156.

Physical objects: density matrices, partial traces, Hermitian observables and
purifications. The equal-partner requirement and target family are hypotheses.
No motion in this animation is asserted to be physical dynamics or gravity.

Required: numpy, scipy, matplotlib. MP4 rendering additionally needs ffmpeg.
The optional reference certificate rerun needs sympy. Run:
    python uqcf_quantum_lab.py --out output
    python uqcf_quantum_lab.py --out output --render
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any
import numpy as np
from scipy.linalg import svd
from scipy.optimize import brentq

N = 5
V_A = np.array([[0,1,2,3,4],[4,0,1,2,3],[3,4,0,1,2],[2,3,4,0,1],[1,2,3,4,0]], dtype=int)
V_B = np.array([[0,1,2,3,4],[1,0,3,4,2],[2,4,0,1,3],[3,2,4,0,1],[4,3,1,2,0]], dtype=int)
WEIGHTS = np.array([.1,.2,.3,.4])
FIXED_T = 21 / 41
PHASE = (9 / 19, 6 / 11)
CHECK_TOL = 2e-10


def dagger(a: np.ndarray) -> np.ndarray:
    return a.conj().T


def herm(a: np.ndarray) -> np.ndarray:
    return (a + dagger(a)) / 2


def trace_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Half the trace norm, evaluated from the Hermitian eigenvalues."""
    return float(np.abs(np.linalg.eigvalsh(herm(a-b))).sum()/2)


def pair_marginals(T: np.ndarray, n: int = N) -> tuple[np.ndarray, np.ndarray]:
    """Tensor order A,B1,B2; return AB1 and AB2 without physical discarding."""
    x = np.asarray(T).reshape(n,n,n,n,n,n)
    return (np.einsum('abcdec->abde',x).reshape(n*n,n*n),
            np.einsum('abcdbf->acdf',x).reshape(n*n,n*n))


def embed_pair(W: np.ndarray, partner: int, n: int = N) -> np.ndarray:
    if partner not in (1,2):
        raise ValueError('partner must be 1 or 2')
    O = np.kron(W,np.eye(n)).reshape(n,n,n,n,n,n)
    if partner == 2:
        O = O.transpose(0,2,1,3,5,4)
    return O.reshape(n**3,n**3)


def bell(n: int = N) -> np.ndarray:
    v = np.eye(n).reshape(-1)/np.sqrt(n)
    return np.outer(v,v)


def scalar_from_z(z: float) -> dict[str, Any]:
    r = np.clip(np.sqrt(z*WEIGHTS),1.,2.)
    D = 2 + np.dot(r,r)
    C = 2 + r.sum()
    H = 2*D/z + np.maximum(WEIGHTS-4/z,0).sum()
    t = 1-1/H
    return dict(z=z,r=r,D=D,C=C,H=H,t=t,
                predicted_distance=t-(1-t)*C*C/(N*z))


def scalar_at(t: float) -> dict[str, Any]:
    if not 0 <= t <= 1:
        raise ValueError('t must be in [0,1]')
    if t == 0:
        return dict(z=np.inf,r=np.full(4,2.),D=18.,C=10.,t=t,c=0.,predicted_distance=0.)
    if t == 1:
        return dict(z=0.,r=np.ones(4),D=6.,C=6.,t=t,c=1/60,predicted_distance=.4)
    # Monotone scalar normalization equation, not data fitting or a force law.
    target = 1/(1-t)
    logz = brentq(lambda x: scalar_from_z(np.exp(x))['H']-target,-40,40,xtol=1e-13)
    out = scalar_from_z(float(np.exp(logz)))
    out.update(t=t,c=(1-t)/(N*out['z']))
    out['predicted_distance']=t-out['c']*out['C']**2
    return out


def build_completion(V: np.ndarray, t: float) -> dict[str, Any]:
    """Construct a feasible optimal state and its matching dual effect.

    Uses a strictly positive product table on all saturated exterior coordinates.
    This is a selected mathematical representative, not a physical selection rule.
    In the open two-saturation phase it is faithful on the entire top support.
    """
    V = np.asarray(V)
    if V.shape != (N,N) or np.any(np.diag(V)):
        raise ValueError('Require a loop-free 5 by 5 array')
    if any(sorted(row)!=list(range(N)) for row in V) or any(sorted(col)!=list(range(N)) for col in V.T):
        raise ValueError('Every row and column must contain 0,1,2,3,4')
    p = scalar_at(float(t))
    Phi = bell()
    B = np.diag(V.reshape(-1)/50)
    rho = t*Phi+(1-t)*B
    F = p['r'][np.maximum(V-1,0)].copy()
    np.fill_diagonal(F,2.)
    stars = np.zeros((N**3,N))
    for k in range(N):
        for i in range(N):
            a = 1. if i==k else F[i,k]
            stars[(i*N+i)*N+k,k] += a
            stars[(i*N+k)*N+i,k] += a
    # c * |star><star|; the normalized column form is better conditioned.
    L = [stars[:,k]/np.sqrt(2*p['D']) for k in range(N)]
    populations = [p['c']*2*p['D']]*N
    exterior=[]
    if t < 1:
        invz = 0. if t==0 else 1/p['z']
        for i in range(N):
            delta=(1-t)/N*np.maximum(V[i]/10-4*invz,0.)
            sat=np.flatnonzero(delta>1e-14)
            if len(sat):
                denom=float(delta[sat].sum())
                for j in sat:
                    for k in sat:
                        q=np.zeros(N**3);q[(i*N+j)*N+k]=1.
                        L.append(q);populations.append(float(delta[j]*delta[k]/denom))
                        exterior.append((int(i),int(j),int(k)))
    L=np.column_stack(L)
    X0=np.diag(populations)
    T=(L*np.asarray(populations))@L.T
    sigma,sigma2=pair_marginals(T)
    q=(p['C']/N)*(1-1/F)
    np.fill_diagonal(q,0.)
    W=Phi+np.diag(q.reshape(-1))
    O=embed_pair(W,1)+embed_pair(W,2)
    max_support=float(np.linalg.eigvalsh(O)[-1])
    primal=trace_distance(rho,sigma)
    dual=float(np.trace(W@rho).real-max_support/2)
    we=np.linalg.eigvalsh(W)
    errors=dict(
        target_trace=abs(float(np.trace(rho).real)-1),
        target_psd=max(0.,-float(np.linalg.eigvalsh(rho)[0])),
        effect_psd=max(0.,-float(we[0])),
        effect_upper_bound=max(0.,float(we[-1])-1),
        trace=abs(float(np.trace(T).real)-1),
        hermiticity=float(np.linalg.norm(T-dagger(T))),
        psd=max(0.,-float(np.linalg.eigvalsh(T)[0])),
        equal_marginals=float(np.linalg.norm(sigma-sigma2)),
        local_marginals=float(np.linalg.norm(np.einsum('abcb->ac',sigma.reshape(N,N,N,N))-np.eye(N)/N)),
        primal_dual_gap=abs(primal-dual),
        formula_gap=abs(primal-p['predicted_distance']),
        support_gap=abs(max_support-p['C']/N),
        frame_orthonormality=float(np.linalg.norm(L.T@L-np.eye(L.shape[1])))
    )
    if max(errors.values())>CHECK_TOL:
        raise ArithmeticError(f'Matrix certificate failed at t={t}: {errors}')
    return dict(**p,V=V,F=F,B=B,rho=rho,T=T,sigma=sigma,W=W,L=L,X0=X0,
                exterior=exterior,primal=primal,dual=dual,errors=errors)


def coefficient_marginal_map(L: np.ndarray) -> np.ndarray:
    """Linear map vec(X) -> both marginals of L X L*, in orthonormal support."""
    k=L.shape[1]
    x=L.reshape(N,N,N,k)
    first=np.einsum('abcu,decv->abdeuv',x,x.conj(),optimize=True).reshape(N**4,k*k)
    second=np.einsum('abcu,dbfv->acdfuv',x,x.conj(),optimize=True).reshape(N**4,k*k)
    return np.vstack([first,second])


def real_hermitian_basis(k: int) -> tuple[np.ndarray,np.ndarray]:
    """Real symmetric and real skew coordinates; i*skew is Hermitian.

    Columns are orthonormal for Re Tr(X*Y), so no imaginary directions are lost.
    """
    sym=[];skew=[]
    for i in range(k):
        a=np.zeros((k,k));a[i,i]=1.;sym.append(a.reshape(-1))
    for i in range(k):
        for j in range(i+1,k):
            a=np.zeros((k,k));a[i,j]=a[j,i]=1/np.sqrt(2);sym.append(a.reshape(-1))
            a=np.zeros((k,k));a[i,j]=1/np.sqrt(2);a[j,i]=-1/np.sqrt(2);skew.append(a.reshape(-1))
    return np.column_stack(sym),np.column_stack(skew)


def hidden_basis(L: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    """Numerical complete Hermitian kernel, independently checked against exact ranks."""
    M=coefficient_marginal_map(L).real
    k=L.shape[1];Bsym,Bskew=real_hermitian_basis(k)
    modes=[];ranks=[];spectra=[]
    for B,phase in [(Bsym,1.),(Bskew,1j)]:
        _,s,vh=svd(M@B,full_matrices=False,check_finite=False)
        threshold=1e-10*s[0]
        rank=int(np.sum(s>threshold));ranks.append(rank);spectra.append(s)
        modes.extend((phase*(B@vh[rank:].T)).T.reshape(-1,k,k))
    modes=np.asarray(modes)
    residual=float(np.max(np.abs(M@modes.reshape(len(modes),-1).T)))
    flat=modes.reshape(len(modes),-1)
    gram=np.real(flat.conj()@flat.T)
    nonzero=[s[r-1] for s,r in zip(spectra,ranks) if r]
    zeros=[s[r] for s,r in zip(spectra,ranks) if r<len(s)]
    report=dict(support_dimension=k,numeric_map_rank=sum(ranks),real_hidden_dimension=len(modes),
                smallest_kept_singular=float(min(nonzero)),largest_discarded_singular=float(max(zeros)),
                maximum_marginal_null_residual=residual,
                basis_orthonormality=float(np.max(np.abs(gram-np.eye(len(modes))))))
    if residual>1e-10 or report['basis_orthonormality']>1e-10:
        raise ArithmeticError(f'Hidden kernel failed: {report}')
    return modes,report


def choose_section(modes: np.ndarray, seed: int) -> np.ndarray:
    """Three seeded directions FOR VISUALIZATION ONLY, not selected by physics."""
    rng=np.random.default_rng(seed)
    q,_=np.linalg.qr(rng.standard_normal((len(modes),3)))
    return np.einsum('ma,mij->aij',q,modes,optimize=True)


def radial_boundary(X0: np.ndarray, Q: np.ndarray, directions: np.ndarray) -> np.ndarray:
    """Exact radial PSD formula, evaluated numerically.

    r_max(u)=-1/lambda_min(X0^(-1/2)*(sum u_i Q_i)*X0^(-1/2)).
    Valid for the faithful X0 in this selected phase. No optimization fit.
    """
    if np.min(np.diag(X0))<=0:
        raise ValueError('The section center must be strictly positive on its support')
    inv=1/np.sqrt(np.diag(X0))
    Z=Q*inv[None,:,None]*inv[None,None,:]
    Y=np.einsum('...a,aij->...ij',directions,Z,optimize=True)
    lam=np.linalg.eigvalsh(Y)[...,0]
    if np.any(lam>=-1e-12):
        raise ArithmeticError('A nonzero trace-zero radial direction must have a negative eigenvalue')
    return -1/lam


def section_data(state: dict, modes: np.ndarray, seed: int,
                 nu: int=57, nv: int=29, frames: int=144) -> dict:
    Q=choose_section(modes,seed)
    u,v=np.meshgrid(np.linspace(0,2*np.pi,nu),np.linspace(0,np.pi,nv))
    direction=np.stack([np.sin(v)*np.cos(u),np.sin(v)*np.sin(u),np.cos(v)],axis=-1)
    radii=radial_boundary(state['X0'],Q,direction)
    surface=direction*radii[...,None]
    theta=np.linspace(0,2*np.pi,frames)
    path_dir=np.column_stack([np.cos(theta),np.sin(theta),.55*np.sin(2*theta)])
    path_dir/=np.linalg.norm(path_dir,axis=1)[:,None]
    path=.70*radial_boundary(state['X0'],Q,path_dir)[:,None]*path_dir
    purity=[];min_eig=[];global_dist=[];marginal_drift=[];distance_error=[];purification_error=[]
    quantum_coordinates_error=[]
    L=state['L'];X0=state['X0'];M=coefficient_marginal_map(L)
    for x in path:
        DX=np.einsum('a,aij->ij',x,Q)
        X=herm(X0+DX)
        ev,U=np.linalg.eigh(X)
        if ev[0]<-CHECK_TOL:
            raise ArithmeticError('Sampling left the positive quantum state set')
        purity.append(float(np.dot(ev,ev)))
        min_eig.append(float(ev[0]))
        global_dist.append(trace_distance(X,X0))
        drift=(M@DX.reshape(-1)).reshape(2,N*N,N*N)
        marginal_drift.append(float(np.max(np.abs(drift))))
        distance_error.append(abs(trace_distance(state['rho'],state['sigma']+drift[0])-state['primal']))
        # W is an actual normalized purification amplitude on H_AB1B2 x C^25.
        W=(L@U)*np.sqrt(np.maximum(ev,0))[None,:]
        recovered=W@dagger(W)
        T=L@X@dagger(L)
        # Independently check the full 125x125 matrix, not only the cached map.
        m1,m2=pair_marginals(T)
        marginal_drift[-1]=max(marginal_drift[-1],float(np.max(np.abs(m1-state['sigma']))),float(np.max(np.abs(m2-state['sigma']))))
        purification_error.append(max(float(np.linalg.norm(recovered-T)),abs(float(np.vdot(W,W).real)-1)))
        coordinates=np.einsum('aij,ji->a',Q,DX).real
        quantum_coordinates_error.append(float(np.max(np.abs(coordinates-x))))
    boundary_X=state['X0'][None,None,:,:]+np.einsum('...a,aij->...ij',surface,Q)
    boundary_min=np.linalg.eigvalsh(boundary_X)[...,0]
    report=dict(frame_count=frames,seed=seed,slice_directions=3,
                max_pair_marginal_change=max(marginal_drift),max_distance_change=max(distance_error),
                minimum_supported_eigenvalue=min(min_eig),purity_range=[min(purity),max(purity)],
                global_trace_distance_from_center_range=[min(global_dist),max(global_dist)],
                max_purification_error=max(purification_error),
                max_observable_coordinate_error=max(quantum_coordinates_error),
                max_boundary_zero_eigenvalue_error=float(np.max(np.abs(boundary_min))))
    if max(report['max_pair_marginal_change'],report['max_distance_change'],report['max_purification_error'])>CHECK_TOL:
        raise ArithmeticError(f'Hidden path verification failed: {report}')
    return dict(surface=surface,path=path,Q=Q,purity=np.array(purity),min_eig=np.array(min_eig),
                global_dist=np.array(global_dist),marginal_drift=np.array(marginal_drift),report=report)




def operational_test(state: dict, section: dict) -> dict:
    """A collective two-outcome measurement distinguishes two hidden completions.

    This computes Born probabilities; it is not a simulated force, source action,
    or empirical experiment. The two pair marginals remain identical.
    """
    i,j=0,len(section['path'])//2
    Q=section['Q'];X0=state['X0'];L=state['L']
    X1=herm(X0+np.einsum('a,aij->ij',section['path'][i],Q))
    X2=herm(X0+np.einsum('a,aij->ij',section['path'][j],Q))
    ev,U=np.linalg.eigh(X1-X2)
    plus=U[:,ev>1e-12]
    effect=plus@dagger(plus)
    p1=float(np.trace(effect@X1).real);p2=float(np.trace(effect@X2).real)
    D=trace_distance(X1,X2)
    T1=L@X1@dagger(L);T2=L@X2@dagger(L)
    a1,b1=pair_marginals(T1);a2,b2=pair_marginals(T2)
    result=dict(frames=[i,j],collective_measurement_probabilities=[p1,p2],
                probability_difference=abs(p1-p2),global_trace_distance=D,
                helstrom_identity_error=abs(abs(p1-p2)-D),
                AB1_trace_distance=trace_distance(a1,a2),AB2_trace_distance=trace_distance(b1,b2),
                statement='One collective yes/no measurement distinguishes these global states; no AB1-only or AB2-only measurement can distinguish them exactly.')
    if result['helstrom_identity_error']>CHECK_TOL:
        raise ArithmeticError('Operational measurement check failed')
    return result


def exact_dimensions() -> dict:
    """Rerun the v9.170 two-array nullity certificate over Q(sqrt(2),sqrt(5)).

    Adapted from the supplied exact reference script. Complex rank equals real
    Hermitian rank for this adjoint-preserving map; do not double the nullity.
    """
    import sympy as s
    from sympy.polys.matrices import DomainMatrix
    field=s.QQ.algebraic_field(s.sqrt(2),s.sqrt(5))
    answer={}
    for name,V in [('A',V_A),('B',V_B)]:
        vectors=[]
        for k in range(N):
            vec={}
            for i in range(N):
                amp=s.Integer(1) if i==k else s.sqrt(min(s.Integer(4),s.Rational(8,5)*int(V[i,k])))
                for ijk in ((i,i,k),(i,k,i)):vec[ijk]=vec.get(ijk,0)+amp
            vectors.append(vec)
        for i in range(N):
            neighbors=[j for j in range(N) if V[i,j]>=3]
            for j in neighbors:
                for k in neighbors:vectors.append({(i,j,k):s.Integer(1)})
        q=len(vectors);maps=[{},{}]
        for u,U in enumerate(vectors):
            for v,VV in enumerate(vectors):
                col=u*q+v
                for (a,b,c),x in U.items():
                    for (e,f,g),y in VV.items():
                        if c==g:
                            row=maps[0].setdefault((N*a+b,N*e+f),{})
                            row[col]=row.get(col,0)+x*y
                        if b==f:
                            row=maps[1].setdefault((N*a+c,N*e+g),{})
                            row[col]=row.get(col,0)+x*y
        rows=list(maps[0].values())+list(maps[1].values());cache={};data={}
        for i,row in enumerate(rows):
            dr={}
            for j,value in row.items():
                value=s.expand(value)
                if value==0:continue
                if value not in cache:cache[value]=field.from_sympy(value)
                dr[j]=cache[value]
            if dr:data[i]=dr
        M=DomainMatrix(data,(len(rows),q*q),field)
        reduced,pivots=M.rref();kernel=reduced.nullspace()
        if not (M*kernel.transpose()).is_zero_matrix:
            raise ArithmeticError('Exact kernel multiplication failed')
        answer[name]={'exact_map_rank':len(pivots),'real_affine_dimension':q*q-len(pivots)}
        expected=315 if name=='A' else 311
        if answer[name]['real_affine_dimension']!=expected:
            raise ArithmeticError('Exact dimension mismatch')
    return answer


def load_lab(out: Path | str) -> dict:
    """Load the validated scientific arrays, without rerunning the sweep."""
    out=Path(out);summary=json.loads((out/'validation.json').read_text())
    curves={};states={};sections={}
    for name,V in [('A',V_A),('B',V_B)]:
        with np.load(out/f'arrangement_{name}.npz') as f:
            curves[name]=f['curve'].copy()
            states[name]=build_completion(V,FIXED_T)
            sections[name]=dict(surface=f['surface'].copy(),path=f['path'].copy(),Q=f['section_directions'].copy(),
                purity=f['path_purity'].copy(),min_eig=f['path_min_eigenvalue'].copy(),
                global_dist=f['path_global_distance'].copy(),marginal_drift=f['path_pair_drift'].copy(),
                report=summary['hidden_sampling'][name])
    return dict(summary=summary,curves=curves,states=states,sections=sections,out=out)


def run_lab(out: Path | str, samples: int=201) -> dict:
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    boundaries=sorted(set(float(scalar_from_z(z)['t']) for z in (40,20,40/3,10,5,10/3,2.5)))
    ts=np.unique(np.r_[np.linspace(0,1,samples),boundaries,FIXED_T,31/51,19/34])
    curves={};states={};sections={};dimension_reports={};all_errors={}
    for name,V,seed in [('A',V_A,917001),('B',V_B,917002)]:
        rows=[];maxerr={}
        for t in ts:
            s=build_completion(V,float(t))
            rows.append([t,s['primal'],s['dual'],s['predicted_distance'],np.trace(s['sigma']@s['sigma']).real])
            for k,x in s['errors'].items():maxerr[k]=max(maxerr.get(k,0),x)
        curves[name]=np.asarray(rows)
        states[name]=build_completion(V,FIXED_T)
        modes,dimension_reports[name]=hidden_basis(states[name]['L'])
        expected=315 if name=='A' else 311
        if len(modes)!=expected:raise ArithmeticError(f'{name}: wrong hidden dimension {len(modes)} != {expected}')
        sections[name]=section_data(states[name],modes,seed)
        all_errors[name]=maxerr
        np.savez_compressed(out/f'arrangement_{name}.npz',V=V,curve=curves[name],
            target=states[name]['rho'],optimal_marginal=states[name]['sigma'],
            reference_global_completion=states[name]['T'],support=states[name]['L'],
            coefficient_center=states[name]['X0'],hidden_basis=modes,
            section_directions=sections[name]['Q'],surface=sections[name]['surface'],
            path=sections[name]['path'],path_purity=sections[name]['purity'],
            path_min_eigenvalue=sections[name]['min_eig'],path_global_distance=sections[name]['global_dist'],
            path_pair_drift=sections[name]['marginal_drift'])
    samecurve=float(np.max(np.abs(curves['A'][:,1]-curves['B'][:,1])))
    if samecurve>CHECK_TOL:raise ArithmeticError('Matched scalar distance curves disagree')
    # Independent symmetry check: conjugate an ACTUAL hidden completion by
    # U_A tensor U_B tensor U_B, transforming all readouts consistently.
    rng=np.random.default_rng(917099)
    def unitary():
        Q,R=np.linalg.qr(rng.normal(size=(N,N))+1j*rng.normal(size=(N,N)))
        phase=np.diag(R);phase=phase/np.abs(phase)
        return Q*phase[None,:]
    UA,UB=unitary(),unitary();pairU=np.kron(UA,UB);globalU=np.kron(pairU,UB)
    s=states['A'];T=globalU@s['T']@dagger(globalU)
    marg,marg2=pair_marginals(T)
    covariance_error=max(float(np.linalg.norm(marg-pairU@s['sigma']@dagger(pairU))),
                         float(np.linalg.norm(marg-marg2)),
                         abs(trace_distance(pairU@s['rho']@dagger(pairU),marg)-s['primal']))
    summary=dict(model='v9.167 matched four-weight family; v9.170 fixed slice; NOT v9.156',
        physical_system='Three five-level systems A,B1,B2; state matrices 125x125; pair matrices 25x25',
        static_parameter='t labels density matrices; animation is not physical time',
        fixed_t=FIXED_T,fixed_t_rational='21/41',phase=list(PHASE),
        phase_boundaries=boundaries,sampled_target_parameters=len(ts),
        computed_primal_dual_pairs=2*len(ts),maximum_curve_difference=samecurve,
        fixed_distance=states['A']['primal'],fixed_optimal_pair_purity={k:float(np.trace(v['sigma']@v['sigma']).real) for k,v in states.items()},
        matrix_checks=all_errors,dimensions=dimension_reports,
        hidden_sampling={k:s['report'] for k,s in sections.items()},
        operational_measurement={k:operational_test(states[k],sections[k]) for k in states},
        local_unitary_covariance_error=covariance_error,
        scientific_status='Numerical reproduction of supplied finite-model theorems; not a new theorem, empirical test, dynamics or gravity derivation',
        section_warning='A chosen 3D affine SECTION of each convex fiber, not a full 315D/311D rendering, not a topology or spatial-curvature claim; the two section bases differ',
        selection_warning='Trace-distance objective, equal-partner obligations and source paths are stipulated; no physical minimization or source rule is derived')
    try:
        summary['exact_dimension_check']=exact_dimensions()
    except ImportError:
        summary['exact_dimension_check']='NOT RERUN: install sympy for the exact-arithmetic stage'
    (out/'validation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (out/'curve_data.json').write_text(json.dumps(dict(columns=['t','primal_trace_distance','dual_lower_bound','theorem_value','optimal_pair_purity'],A=curves['A'].tolist(),B=curves['B'].tolist())),encoding='utf-8')
    return dict(summary=summary,curves=curves,states=states,sections=sections,out=out)


def render_lab(lab: dict, videos: bool=True, video_targets: tuple[str,...]=('curve','A','B')) -> dict[str,Path]:
    """Separate figures; every plotted vertex comes from computed quantum matrices."""
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation,FFMpegWriter
    out=lab['out'];summary=lab['summary'];paths={}
    fig=plt.figure(figsize=(10,6),layout='constrained');ax=fig.add_subplot(111)
    A,B=lab['curves']['A'],lab['curves']['B']
    ax.plot(A[:,0],A[:,1],linewidth=3,label='Arrangement A: matrix trace distance')
    ax.plot(B[:,0],B[:,1],linestyle='--',linewidth=1.6,label='Arrangement B: coincident curve')
    ax.axvspan(*PHASE,alpha=.12,label='Certified 315 vs 311 phase')
    for boundary in summary['phase_boundaries']:
        ax.axvline(boundary,linestyle=':',linewidth=.65,alpha=.4)
    ax.set(xlabel='Target parameter t (not physical time)',ylabel='Distance to equal-partner compatibility',
           title='SAME SCALAR RESPONSE, DIFFERENT GLOBAL COMPLETIONS',xlim=(0,1),ylim=(-.012,.425))
    ax.legend(loc='upper left',framealpha=.94,fontsize=10);ax.grid(alpha=.17)
    dot,=ax.plot([],[],'o',markersize=9)
    text=ax.text(.02,.56,'',transform=ax.transAxes,fontsize=11,va='top')
    def curve_frame(i):
        row=A[i];dot.set_data([row[0]],[row[1]])
        text.set_text(f't = {row[0]:.4f}\nDistance = {row[1]:.8f}\nPrimal/dual mismatch = {abs(row[1]-row[2]):.1e}\n\n125 x 125 global density matrices\n25 x 25 pair marginals\nNo fitted response curve')
        return dot,text
    fixed_i=int(np.argmin(abs(A[:,0]-FIXED_T)));curve_frame(fixed_i)
    paths['curve_png']=out/'compatibility_curve.png';fig.savefig(paths['curve_png'],dpi=170)
    if videos and 'curve' in video_targets:
        anim=FuncAnimation(fig,curve_frame,frames=range(0,len(A),2),interval=100,blit=False)
        paths['curve_video']=out/'compatibility_curve.mp4'
        anim.save(paths['curve_video'],writer=FFMpegWriter(fps=16,bitrate=2100,extra_args=['-pix_fmt','yuv420p']),dpi=110)
    plt.close(fig)

    # Global state purity changes along hidden paths, while their pair states do not.
    fig=plt.figure(figsize=(10,5.5),layout='constrained');ax=fig.add_subplot(111)
    for name in ['A','B']:
        section=lab['sections'][name]
        ax.plot(np.arange(len(section['purity'])),section['purity'],label=f'{name}: global purity',linewidth=2)
    ax.set(title='THE GLOBAL QUANTUM STATE CHANGES; BOTH PAIR MARGINALS STAY FIXED',
           xlabel='Illustration frame (not physical time)',ylabel='Global purity Tr(T²)')
    ax.grid(alpha=.2);ax.legend()
    paths['purity_png']=out/'hidden_global_purity.png';fig.savefig(paths['purity_png'],dpi=170);plt.close(fig)

    if 'operational_measurement' in summary:
        info=summary['operational_measurement']['A']
        fig=plt.figure(figsize=(9,5),layout='constrained');ax=fig.add_subplot(111)
        probs=info['collective_measurement_probabilities']
        bars=ax.bar(['Hidden completion 1','Hidden completion 2'],probs)
        ax.bar_label(bars,labels=[f'{v:.6f}' for v in probs],padding=5)
        ax.set(ylim=(0,1),ylabel='Born probability of the same collective outcome',
               title='SAME PAIR DATA; A COLLECTIVE MEASUREMENT CAN TELL THEM APART')
        ax.text(.5,.9,f'Global trace distance = {info["global_trace_distance"]:.6f}\n'
                f'AB1 distance = {info["AB1_trace_distance"]:.1e}; AB2 distance = {info["AB2_trace_distance"]:.1e}',
                transform=ax.transAxes,ha='center',va='top')
        paths['measurement_png']=out/'collective_measurement.png'
        fig.savefig(paths['measurement_png'],dpi=170);plt.close(fig)

    # Use the SAME symmetric axis scale for the two chosen sections, but do not
    # infer comparative geometry from this arbitrary three-direction selection.
    common_lim=1.08*max(float(np.max(np.abs(s['surface']))) for s in lab['sections'].values())
    for name in ['A','B']:
        data=lab['sections'][name];surface=data['surface'];path=data['path']
        fig=plt.figure(figsize=(10,7));ax=fig.add_subplot(111,projection='3d')
        fig.subplots_adjust(left=.015,right=.985,bottom=.20,top=.87)
        ax.plot_surface(surface[...,0],surface[...,1],surface[...,2],alpha=.28,
                        linewidth=.20,rstride=2,cstride=2,antialiased=True)
        ax.plot(*path.T,linestyle=':',linewidth=1.,alpha=.7)
        trail,=ax.plot([],[],[],linewidth=2.5)
        point,=ax.plot([],[],[],'o',markersize=8)
        ax.set(xlim=(-common_lim,common_lim),ylim=(-common_lim,common_lim),zlim=(-common_lim,common_lim),
               xlabel=r'$\Delta\langle Q_1\rangle$',ylabel=r'$\Delta\langle Q_2\rangle$',zlabel=r'$\Delta\langle Q_3\rangle$')
        ax.set_box_aspect((1,1,1));ax.ticklabel_format(style='sci',axis='both',scilimits=(-2,2))
        dim=summary['dimensions'][name]['real_hidden_dimension']
        fig.suptitle(f'ARRANGEMENT {name}: REAL HIDDEN QUANTUM COMPLETIONS\n'
                     f'A chosen 3D section of a {dim}-dimensional convex solution family',fontsize=14,y=.98)
        live=fig.text(.06,.13,'',fontsize=10.5,va='top')
        fig.text(.06,.025,'Surface: exact PSD boundary in this section. Axes: chosen global-observable expectations.\n'
                 'Both AB marginals and target distance remain fixed. Animation is not physical evolution.',fontsize=9.5,va='bottom')
        def draw(i,ax=ax,path=path,point=point,trail=trail,data=data,live=live):
            point.set_data([path[i,0]],[path[i,1]]);point.set_3d_properties([path[i,2]])
            trail.set_data(path[:i+1,0],path[:i+1,1]);trail.set_3d_properties(path[:i+1,2])
            ax.view_init(elev=24,azim=35+240*i/(len(path)-1))
            live.set_text(f'Global purity = {data["purity"][i]:.8f}    '
                          f'Global change D(T,T₀) = {data["global_dist"][i]:.5f}\n'
                          f'Max pair-entry drift = {data["marginal_drift"][i]:.1e}    '
                          f'Min supported eigenvalue = {data["min_eig"][i]:.2e}')
            return point,trail,live
        draw(len(path)//3)
        paths[f'hidden_{name}_png']=out/f'hidden_completion_{name}.png';fig.savefig(paths[f'hidden_{name}_png'],dpi=155)
        if videos and name in video_targets:
            anim=FuncAnimation(fig,draw,frames=len(path),interval=70,blit=False)
            paths[f'hidden_{name}_video']=out/f'hidden_completion_{name}.mp4'
            anim.save(paths[f'hidden_{name}_video'],writer=FFMpegWriter(fps=16,bitrate=2300,extra_args=['-pix_fmt','yuv420p']),dpi=110)
        plt.close(fig)
    return paths


def write_interactive_lab(lab: dict) -> Path:
    """Standalone offline HTML with independent Plotly figures (no subplots).

    Plotly only displays NumPy-computed vertices and states; it does not compute
    the physics. No external server, CDN, fitted mesh, or image generator is used.
    """
    import html
    import plotly.graph_objects as go
    import plotly.io as pio
    summary=lab['summary'];parts=[]
    A,B=lab['curves']['A'],lab['curves']['B']
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=A[:,0],y=A[:,1],mode='lines',name='A: matrix trace distance'))
    fig.add_trace(go.Scatter(x=B[:,0],y=B[:,1],mode='lines',name='B: coincident curve',line=dict(dash='dash')))
    fig.update_layout(title='One scalar distance curve for two different arrangements',height=430,
                      xaxis_title='Target parameter t — not physical time',
                      yaxis_title='Half trace-norm distance to equal-partner compatibility',
                      legend=dict(orientation='h',y=-.20))
    parts.append('<section><h2>1. The full, matrix-verified distance curve</h2><p>'
                 'Hover to inspect computed values. This is the four-weight matched-arrangement family '
                 'of v9.167, not the different linear-phase example from v9.156.</p>'+
                 pio.to_html(fig,full_html=False,include_plotlyjs=True,config={'responsive':True})+'</section>')
    lim=1.08*max(float(np.max(np.abs(s['surface']))) for s in lab['sections'].values())
    for name in ['A','B']:
        data=lab['sections'][name];S=data['surface'];P=data['path'];dim=summary['dimensions'][name]['real_hidden_dimension']
        def annotation(i):
            return dict(text=f'Frame {i+1}/{len(P)} · purity {data["purity"][i]:.8f} · '
                        f'global D(T,T₀) {data["global_dist"][i]:.6f}<br>'
                        f'pair-entry drift {data["marginal_drift"][i]:.2e} · '
                        f'min supported eigenvalue {data["min_eig"][i]:.2e}',
                        x=.5,y=1.06,xref='paper',yref='paper',showarrow=False)
        fig=go.Figure(data=[
            go.Surface(x=S[...,0],y=S[...,1],z=S[...,2],opacity=.35,showscale=False,name='PSD boundary'),
            go.Scatter3d(x=P[:,0],y=P[:,1],z=P[:,2],mode='lines',name='Chosen admissible path',line=dict(width=3,dash='dot')),
            go.Scatter3d(x=[P[0,0]],y=[P[0,1]],z=[P[0,2]],mode='markers',name='Current global state',marker=dict(size=6))
        ])
        fig.frames=[go.Frame(name=str(i),data=[go.Scatter3d(x=[P[i,0]],y=[P[i,1]],z=[P[i,2]],mode='markers',marker=dict(size=6))],
                            traces=[2],layout=go.Layout(annotations=[annotation(i)])) for i in range(len(P))]
        fig.update_layout(height=640,margin=dict(l=0,r=0,t=65,b=110),uirevision=f'preserve_camera_{name}',
            scene=dict(xaxis=dict(title='Δ〈Q₁〉',range=[-lim,lim]),
                       yaxis=dict(title='Δ〈Q₂〉',range=[-lim,lim]),
                       zaxis=dict(title='Δ〈Q₃〉',range=[-lim,lim]),aspectmode='cube'),
            annotations=[annotation(0)],legend=dict(orientation='h',y=-.1),
            updatemenus=[dict(type='buttons',showactive=False,x=0,y=-.16,direction='left',buttons=[
                dict(label='Play state samples',method='animate',args=[None,dict(frame=dict(duration=75,redraw=True),transition=dict(duration=0),fromcurrent=True)]),
                dict(label='Pause',method='animate',args=[[None],dict(mode='immediate',frame=dict(duration=0,redraw=False))])])],
            sliders=[dict(active=0,x=.32,len=.65,y=-.13,currentvalue=dict(prefix='Frame '),steps=[
                dict(label=str(i),method='animate',args=[[str(i)],dict(mode='immediate',frame=dict(duration=0,redraw=True),transition=dict(duration=0))])
                for i in range(0,len(P),6)])])
        parts.append(f'<section><h2>2{name}. Arrangement {name}: {dim} hidden dimensions, three displayed</h2>'
            '<p>Drag to rotate; pinch or scroll to zoom. Play or slide through verified positive global states. '
            'All sampled states in this panel have the same two prescribed pair marginals and the same '
            'optimal distance. A point is one whole quantum state—not a particle.</p>'+
            pio.to_html(fig,full_html=False,include_plotlyjs=False,config={'responsive':True})+
            '<p class="note">This is a chosen three-dimensional affine <strong>section</strong> of a convex completion set, '
            'not a visualization of every hidden dimension. The A and B section directions were chosen separately; '
            'their displayed shapes are not a new invariant comparison. Surface facets approximate a boundary '
            'computed by eigenvalues. Camera rotation and sample playback are not physical dynamics.</p></section>')
    q=summary['operational_measurement']['A']
    p1,p2=q['collective_measurement_probabilities']
    measurement=go.Figure(go.Bar(x=['Hidden completion 1','Hidden completion 2'],y=[p1,p2],text=[f'{p1:.6f}',f'{p2:.6f}'],textposition='outside'))
    measurement.update_layout(height=400,yaxis=dict(range=[0,1],title='Born probability'),
                              title='Within A: one collective outcome distinguishes two hidden completions')
    parts.append('<section><h2>3. What a measurement could distinguish</h2>'
        '<p>The two states above are two completions within arrangement A, not the A/B source pair. '
        'Their AB₁ and AB₂ states agree, but a collective measurement on AB₁B₂ gives different '
        'Born probabilities. These are predictions from the matrices, not laboratory observations.</p>'+
        pio.to_html(measurement,full_html=False,include_plotlyjs=False,config={'responsive':True})+'</section>')
    rows=[('Computed target parameters',summary['sampled_target_parameters']),
          ('Primal/dual matrix checks',summary['computed_primal_dual_pairs']),
          ('A/B curve difference',f'{summary["maximum_curve_difference"]:.3e}'),
          ('Hidden-state pair drift',f'{max(s["max_pair_marginal_change"] for s in summary["hidden_sampling"].values()):.3e}'),
          ('Exact affine dimensions','A: 315; B: 311'),('Fixed section parameter','t = 21/41'),
          ('Pure-extension recovery error',f'{max(s["max_purification_error"] for s in summary["hidden_sampling"].values()):.3e}')]
    table=''.join(f'<tr><th>{html.escape(str(k))}</th><td>{html.escape(str(v))}</td></tr>' for k,v in rows)
    parts.append('<section><h2>4. Validation and mathematical meaning</h2><table>'+table+'</table>'
        '<p>Core equation: ρ(t)=tΦ₅+(1−t)B. The program constructs a positive trace-one T with '
        'Tr<sub>B₂</sub>T=Tr<sub>B₁</sub>T=σ, and matches D(ρ,σ) to a dual lower bound. '
        'For the hidden view it uses T(x)=L[X₀+ΣxᵢQᵢ]L† with both marginal derivatives exactly zero.</p>'
        '<p>On the chosen support, the radial surface is '
        'r<sub>max</sub>(u)=−1/λ<sub>min</sub>(X₀<sup>−1/2</sup>[ΣuᵢQᵢ]X₀<sup>−1/2</sup>). '
        'This is the actual positivity boundary of the selected section.</p>'
        '<p>The three-system density T can be mixed. The program also constructs a normalized pure '
        'extension on AB₁B₂ plus a 25-dimensional ancilla and checks that its reduction recovers T. '
        'It does not claim purity on the original three factors alone.</p></section>')
    doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>UQCF-GEM — Computed Quantum Compatibility Lab</title>
<style>body{font-family:system-ui,-apple-system,sans-serif;max-width:1100px;margin:0 auto;padding:24px;line-height:1.55}h1{font-size:2.1rem;line-height:1.18}h2{font-size:1.3rem}section{margin:28px 0 42px;padding-top:12px;border-top:1px solid #ddd}.note,footer{font-size:.91rem}table{border-collapse:collapse;width:100%}th,td{text-align:left;padding:8px;border-bottom:1px solid #ddd}header p{max-width:900px}</style></head><body>
<header><p>UQCF–GEM · NUMERICAL REPRODUCTION OF v9.167–v9.171</p>
<h1>Same pair data. Different global quantum states.</h1>
<p>Every surface vertex and sample comes from an actual density-matrix calculation. The model uses three five-level quantum systems. This page opens offline; all chart code and data are embedded.</p>
<p><strong>Scope:</strong> a static quantum compatibility model, not a gravity or spacetime simulation. Equal-partner constraints, the target family, and the trace-distance objective are stipulated. A parameter sweep is not physical time.</p></header>'''+''.join(parts)+'''
<footer><strong>Sources:</strong> supplied UQCF–GEM v9.167 Full-Curve Weighted-Layer Theorem, v9.170 Higher-Saturated-Incidence Census, and v9.171 Phase-Persistence Gate. Exact dimension code adapted from the supplied v9170 certificate. Independent numerical checks and all data accompany this lab. No result from v9.172 is asserted.</footer></body></html>'''
    path=lab['out']/'UQCF_Quantum_Lab.html';path.write_text(doc,encoding='utf-8')
    return path


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('uqcf_quantum_lab_output'))
    parser.add_argument('--samples',type=int,default=201)
    parser.add_argument('--render',action='store_true')
    args=parser.parse_args()
    lab=run_lab(args.out,args.samples)
    if args.render:render_lab(lab)
    try:
        write_interactive_lab(lab)
    except ImportError:
        print('Interactive HTML skipped: install plotly to enable it.')
    print(json.dumps(lab['summary'],indent=2))

if __name__=='__main__':main()
