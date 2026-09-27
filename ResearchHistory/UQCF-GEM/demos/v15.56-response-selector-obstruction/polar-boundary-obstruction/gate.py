"""v15.82: exact source-edge determinant and canonical polar boundary diagnostic."""
import functools
import importlib.util
import json
import pathlib
import sys
import numpy as np
import sympy as sp
import mpmath as mp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('interference81_boundary',HERE.parent/'source-component-interference'/'gate.py')
V81=importlib.util.module_from_spec(spec);spec.loader.exec_module(V81)
M=V81.M
q=sp.Symbol('q',real=True)
LO=sp.Rational(1,5);HI=sp.Rational(9,20);EPS=sp.Rational(1,10**60)
DELTAS=['1e-3','1e-5','1e-7'];IDENTITY_U=['0','.1','.2','.4','.8']


def rational(x):return sp.Rational(*float(x).as_integer_ratio())

def exact_matrix(a):
    a=np.asarray(a)
    return sp.Matrix(a.shape[0],a.shape[1],lambda i,j:rational(a[i,j].real)+sp.I*rational(a[i,j].imag))

def to_numpy(a):return np.array(a.tolist(),dtype=complex)

def mp_scalar(x):
    x=sp.expand(x);r=sp.re(x);i=sp.im(x)
    rr=mp.mpf(int(r.p))/int(r.q);ii=mp.mpf(int(i.p))/int(i.q)
    return rr if ii==0 else mp.mpc(rr,ii)

def mp_matrix(a):return mp.matrix([[mp_scalar(a[i,j]) for j in range(a.cols)] for i in range(a.rows)])

def number(x):return mp.nstr(x,80)

def serial_matrix(a):return [[number(a[i,j]) for j in range(a.cols)] for i in range(a.rows)]

def maxabs(a):return max(abs(x) for x in a)

def poly_at(expr,x):
    return mp.polyval([mp_scalar(c) for c in sp.Poly(expr,q).all_coeffs()],x)

def matrix_at(a,x):return mp.matrix([[poly_at(a[i,j],x) for j in range(a.cols)] for i in range(a.rows)])

def isolate(poly):return poly.intervals(eps=EPS,inf=LO,sup=HI)

def polar(c):
    u,s,v=mp.svd_r(c);o=u*v;p=v.T*mp.diag(s)*v
    check={'orthogonality':maxabs(o.T*o-mp.eye(3)),
           'reconstruction':maxabs(c-o*p)}
    return o,s,check

def density(r):
    eigen=mp.eighe(r,eigvals_only=True)
    tr=sum(r[i,i] for i in range(r.rows))
    return {'minimum_eigenvalue':number(min(eigen)),
            'trace_error':number(abs(tr-1)),
            'hermiticity_error':number(maxabs(r-r.H))}

def density_valid(row):
    return (mp.mpf(row['minimum_eigenvalue'])>=-mp.mpf('1e-12') and
            mp.mpf(row['trace_error'])<=mp.mpf('1e-12') and
            mp.mpf(row['hermiticity_error'])<=mp.mpf('1e-12'))

def adjudicate(valid,passed):
    if not valid:return 'INVALID'
    return 'POLAR_CONTINUATION_OBSTRUCTION_CONFIRMED' if passed else 'POLAR_CONTINUATION_OBSTRUCTION_NOT_CONFIRMED'


def synthetic_controls():
    with mp.workdps(80):
        cross=sp.diag(sp.Rational(1,5),sp.Rational(1,10),q-sp.Rational(1,3))
        smooth=sp.diag(sp.Rational(1,5),sp.Rational(1,10),sp.Rational(1,20)+q)
        roots=isolate(sp.Poly(cross.det(),q));none=isolate(sp.Poly(smooth.det(),q))
        a,_,ca=polar(matrix_at(cross,mp.mpf(1)/3-mp.mpf('1e-7')))
        b,_,cb=polar(matrix_at(cross,mp.mpf(1)/3+mp.mpf('1e-7')))
        sv=mp.svd_r(a-b,compute_uv=False)
        error=max(abs(sv[i]-([2,0,0][i])) for i in range(3))
        exact=(len(roots)==1 and roots[0][1]==1 and roots[0][0][0]<=sp.Rational(1,3)<=roots[0][0][1])
        valid=exact and not none and error<=mp.mpf('1e-40') and max(*ca.values(),*cb.values())<=mp.mpf('1e-50')
        return {'valid':bool(valid),'crossing_root_count':len(roots),'smooth_root_count':len(none),
                'jump_singular_values':[number(x) for x in sv],'jump_error':number(error)}


@functools.lru_cache(maxsize=1)
def run_measurement():
    with mp.workdps(80):return _run()


def _run():
    selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
    domain=M.domain([r['rho'] for r in selected])
    rho=next(r['rho'] for r in selected if r['candidate_index']==46)
    r0=exact_matrix(rho);b=exact_matrix(V81.PP-V81.QQ);r1=sp.expand(b*r0*b/2)
    # No sqrt(2) rounding: A z A is exactly B z B / 2, B=P-Q.
    source_unitary=(b*b/2==sp.eye(8))
    one0=[exact_matrix(M.F.op(a,0,0)) for a in [1,2,3]]
    one1=[exact_matrix(M.F.op(0,a,0)) for a in [1,2,3]]
    pair=[x*y for x in one0 for y in one1]
    trace=lambda a:sp.expand(sp.trace(a))
    def moment(o):return sp.expand(((1+q)*trace(r0*o)+(1-q)*trace(r1*o))/2)
    m0=[moment(o) for o in one0];m1=[moment(o) for o in one1]
    c=sp.Matrix(3,3,lambda i,j:sp.expand(moment(pair[3*i+j])-m0[i]*m1[j]))
    polynomial=sp.Poly(sp.expand(c.det()),q,domain=sp.QQ)
    intervals=isolate(polynomial)
    unique=len(intervals)==1 and intervals[0][1]==1
    controls={'source_unitary_exact':bool(source_unitary),'selector_valid':indices==M.EXPECTED,
              'original_domain_valid':bool(domain['valid']),
              'complex_roundtrip_error':float(np.max(np.abs(to_numpy(r0)-rho))),
              'polynomial_degree':int(polynomial.degree()),'synthetic':synthetic_controls()}
    r0m=mp_matrix(r0);r1m=mp_matrix(r1)
    state=lambda x:((1+x)*r0m+(1-x)*r1m)/2
    checks=[];density_rows=[density(r0m)];polar_checks=[]
    for strength in IDENTITY_U:
        x=mp.exp(-2*mp.mpf(strength));cm=matrix_at(c,x);rm=state(x)
        original=V81.channel(-1,float(strength),rho)
        expected=M.correlations(original)[0]
        ce=float(np.max(np.abs(np.array(cm.tolist(),dtype=float)-expected)))
        re=float(np.max(np.abs(np.array(rm.tolist(),dtype=complex)-original)))
        dr=density(rm);density_rows.append(dr)
        checks.append({'strength':strength,'q':number(x),'correlation_error':ce,'state_error':re,
                       'determinant':number(mp.det(cm)),'density':dr})
    # Exact source-edge marginal closure, for the full hidden basis. Normalization
    # by sqrt(8) is irrelevant to zero; all 15 moments are tested, not only pairs.
    hidden_checks=[]
    for label in M.LABELS:
        h=exact_matrix(M.F.op(*label));ah=b*h*b/2
        coeffs=[trace(h*o)==0 and trace(ah*o)==0 for o in one0+one1+pair]
        hidden_checks.append({'label':list(label),'all_15_exact_zero':bool(all(coeffs))})
    root=None;sides=[];gate_checks={'unique_simple_root':bool(unique)}
    if unique:
        (left,right),multiplicity=intervals[0]
        root_rational=(left+right)/2;x=mp_scalar(root_rational);u0=-mp.log(x)/2
        cr=matrix_at(c,x);uu,sv,vv=mp.svd_r(cr)
        v0=uu*mp.diag([1,1,0])*vv
        reconstructed=uu*mp.diag([sv[0],sv[1],0])*vv
        reconstruction=maxabs(cr-reconstructed)
        derivative=poly_at(polynomial.diff().as_expr(),x)
        dr=density(state(x));density_rows.append(dr)
        rank_guard=sv[2]<=mp.mpf('1e-45') and sv[1]>=mp.mpf('1e-4')
        root={'q_midpoint':number(x),'strength':number(u0),'interval_width':str(right-left),
              'determinant_residual':number(mp.det(cr)), 'determinant_derivative_q':number(derivative),
              'singular_values':[number(t) for t in sv],'correlation':serial_matrix(cr),
              'partial_isometry_approximation':serial_matrix(v0),'partial_reconstruction_error':number(reconstruction),
              'density':dr,'Q':None,'E':None}
        orientations=True;last_jump_error=None;last_distance_error=None
        for delta in DELTAS:
            dd=mp.mpf(delta);side_factors=[];row={'delta':delta}
            for name,us in [('before',u0-dd),('after',u0+dd)]:
                xs=mp.exp(-2*us);cs=matrix_at(c,xs);o,s,pc=polar(cs)
                polar_checks.append(pc);ds=density(state(xs));density_rows.append(ds)
                side_factors.append(o);det=mp.det(o)
                orientations=orientations and abs(det-(1 if name=='before' else -1))<=mp.mpf('1e-40')
                row[name]={'strength':number(us),'q':number(xs),'determinant_C':number(mp.det(cs)),
                           'determinant_O':number(det),'singular_values':[number(t) for t in s],
                           'polar_factor':serial_matrix(o),'density':ds,
                           'polar_checks':{k:number(v) for k,v in pc.items()},
                           'distance_to_partial_isometry':number(mp.norm(o-v0))}
            a,d=side_factors;jump=mp.svd_r(a-d,compute_uv=False)
            last_jump_error=max(abs(jump[i]-[2,0,0][i]) for i in range(3))
            last_distance_error=max(abs(mp.norm(t-v0)-1) for t in side_factors)
            row['jump_singular_values']=[number(t) for t in jump]
            row['jump_error']=number(last_jump_error);row['partial_distance_error']=number(last_distance_error)
            sides.append(row)
        gate_checks.update(root_in_original_strength_bracket=bool(mp.mpf('.4')<u0<mp.mpf('.8')),
                           transverse=bool(abs(derivative)>=mp.mpf('1e-8')),
                           rank_two_guard=bool(rank_guard),orientations=bool(orientations),
                           rank_one_jump=bool(last_jump_error<=mp.mpf('1e-4')),
                           partial_distances=bool(last_distance_error<=mp.mpf('1e-4')))
        controls['root_partial_reconstruction_valid']=bool(not rank_guard or reconstruction<=mp.mpf('1e-45'))
    else:controls['root_partial_reconstruction_valid']=True
    gate_checks['positive_density_margin']=all(mp.mpf(r['minimum_eigenvalue'])>=mp.mpf('.01') for r in density_rows)
    gate_checks['hidden_source_edge_closed']=len(hidden_checks)==27 and all(r['all_15_exact_zero'] for r in hidden_checks)
    controls['density_valid']=all(density_valid(r) for r in density_rows)
    controls['identity_valid']=all(r['correlation_error']<=1e-12 and r['state_error']<=1e-12 for r in checks)
    controls['root_isolation_width_valid']=all(r-l<=EPS for (l,r),m in intervals)
    controls['polar_valid']=all(max(pc.values())<=mp.mpf('1e-50') for pc in polar_checks)
    valid=(controls['selector_valid'] and controls['original_domain_valid'] and source_unitary and
           controls['complex_roundtrip_error']<=1e-16 and polynomial.degree()<=6 and controls['synthetic']['valid'] and
           all(controls[k] for k in ['density_valid','identity_valid','root_isolation_width_valid','polar_valid','root_partial_reconstruction_valid']))
    report={'version':'15.82','candidate_index':46,'candidate_indices':indices,'lambda':-1,'edge':[0,1],
            'precision_digits':80,'q_interval':[str(LO),str(HI)],'all_valid':bool(valid),
            'verdict':adjudicate(valid,all(gate_checks.values())),'controls':controls,'gate_checks':gate_checks,
            'input_hex':[[[float(z.real).hex(),float(z.imag).hex()] for z in row] for row in rho],
            'original_domain':domain,'original_density':density_rows[0],
            'correlation_polynomials':[[str(c[i,j]) for j in range(3)] for i in range(3)],
            'determinant_coefficients_descending':[str(t) for t in polynomial.all_coeffs()],
            'root_intervals':[{'left':str(l),'right':str(r),'multiplicity':int(m)} for (l,r),m in intervals],
            'unique_simple_root':bool(unique),'root':root,'identity_checks':checks,'sides':sides,
            'hidden_source_edge_checks':hidden_checks,
            'interpretation':'Diagnostic of stored complex input; v15.81 finite-window NO unchanged. Q/E undefined at singularity.'}
    # Catch nonfinite values even though arbitrary-precision scalars are strings.
    def finite(a):
        if isinstance(a,dict):return all(finite(v) for v in a.values())
        if isinstance(a,list):return all(finite(v) for v in a)
        if isinstance(a,float):return bool(np.isfinite(a))
        if isinstance(a,str):return a.lower() not in ['nan','inf','+inf','-inf']
        return True
    if not finite(report):report['all_valid']=False;report['verdict']='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False))
    sys.exit(0 if r['all_valid'] else 2)
