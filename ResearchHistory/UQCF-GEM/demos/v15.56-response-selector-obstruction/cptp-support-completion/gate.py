"""v15.86: unique CPTP completion of an isometrically retained Bloch plane."""
import functools
import hashlib
import importlib.util
import json
import pathlib
import sys
import mpmath as mp
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v1584_helpers',HERE.parent/'loop-channel-recoverability'/'gate.py')
V84=importlib.util.module_from_spec(spec);spec.loader.exec_module(V84)
HASH83='bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166'
HASH85='a61ca58f52ca49e9a9f4186ded63a29b9cf84195f688ba00e77d05d15329370a'
num=V84.number
mat=V84.matrix
maximum=V84.maximum


def symbolic_certificate():
    a,b,c=sp.symbols('a b c',real=True)
    x,y,z=sp.symbols('t1 t2 t3',real=True)
    ps=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
    T=sp.Matrix([[1,0,a],[0,1,b],[0,0,c]])
    def action(w):
        out=sp.trace(w)*sp.eye(2)
        for j in range(3):
            for i in range(3):out+=T[i,j]*sp.trace(ps[j]*w)*ps[i]
        return out/2
    J=sp.zeros(4)
    for p in range(2):
        for q in range(2):
            e=sp.zeros(2);e[p,q]=1;o=action(e)
            for i in range(2):
                for k in range(2):J[2*p+i,2*q+k]=o[i,k]
    target=sp.Matrix([[(1+c)/2,(a-sp.I*b)/2,0,1],[(a+sp.I*b)/2,(1-c)/2,0,0],
                      [0,0,(1-c)/2,-(a-sp.I*b)/2],[1,0,-(a+sp.I*b)/2,(1+c)/2]])
    zero=lambda m: all(sp.simplify(e)==0 for e in m)
    w=sp.Matrix([1,0,0,-1])/sp.sqrt(2)
    normsum=(x+1)**2+y*y+z*z+(x-1)**2+y*y+z*z
    bell=sp.Matrix([1,0,0,1]);jidentity=bell*bell.T
    algebra=sp.Matrix.hstack(*[m.reshape(4,1) for m in [sp.eye(2),ps[0],ps[1],ps[0]*ps[1]]])
    checks={'general_choi':zero(J-target),
            'translation_norm_sum':sp.simplify(normsum-2-2*(x*x+y*y+z*z))==0,
            'diagonal_bound':sp.simplify(J[1,1]-(1-c)/2)==0,
            'bell_bound':sp.simplify((w.H*J*w)[0]-(c-1)/2)==0,
            'zero_diagonal_minor':sp.simplify(J.subs(c,1).extract([0,1],[0,1]).det()+(a*a+b*b)/4)==0,
            'identity_completion':zero(J.subs({a:0,b:0,c:1})-jidentity),
            'pauli_commutator':zero(ps[0]*ps[1]-ps[1]*ps[0]-2*sp.I*ps[2]),
            'generated_algebra_dimension':algebra.rank()==4}
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def cofactor(a):
    c=mp.zeros(3)
    for i in range(3):
        for j in range(3):
            rows=[r for r in range(3) if r!=i];cols=[k for k in range(3) if k!=j]
            c[i,j]=(-1)**(i+j)*(a[rows[0],cols[0]]*a[rows[1],cols[1]]-a[rows[0],cols[1]]*a[rows[1],cols[0]])
    return c


def cross(a,b):return mp.matrix([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])
def frobenius(a):return mp.sqrt(sum(abs(x)**2 for x in a))
def spectrum_error(e,expected):return max(abs(x-y) for x,y in zip(e,sorted(expected)))


def synthetic_controls():
    errors=[];rows=[]
    for ctext in ['-1','0','0.5','1','1.5']:
        c=mp.mpf(ctext);T=mp.diag([1,1,c]);J,e,checks=V84.channel_diagnostics(T)
        error=spectrum_error(e,[(c-1)/2,(1-c)/2,(1-c)/2,(3+c)/2])
        errors.extend([error,*checks.values()]);rows.append({'c':ctext,'classification':V84.cp_class(e[0]),'choi_eigenvalues':[num(v) for v in e],'formula_error':num(error)})
    identity=mp.eye(3);dephase=mp.diag([0,0,1]);distances=[];density_checks=[]
    for a in [0,1]:
        state=(V84.I+V84.PAULI[a])/2
        out1=V84.phi(identity,state);out2=V84.phi(dephase,state)
        d=V84.distance(out1,out2);distances.append(num(d));errors.append(abs(d-mp.mpf('.5')))
        density_checks.extend(V84.density(z) for z in [state,out1,out2])
    axis_error=maximum(V84.phi(identity,V84.PAULI[2])-V84.phi(dephase,V84.PAULI[2]));errors.append(axis_error)
    classes=[]
    for T in [identity,dephase]:
        J,e,checks=V84.channel_diagnostics(T);errors.extend(checks.values());classes.append(V84.cp_class(e[0]))
    contractive=mp.svd_r(mp.diag([1,1,0]),compute_uv=False)[0]<=1+mp.mpf('1e-40')
    valid=(max(errors)<=mp.mpf('1e-45') and classes==['CPTP','CPTP'] and
           [r['classification'] for r in rows]==['NON_CP','NON_CP','NON_CP','CPTP','NON_CP'] and
           contractive and all(V84.density_valid(d) for d in density_checks))
    return {'valid':bool(valid),'ladder':rows,'single_axis_channel_classes':classes,
            'single_axis_agreement_error':num(axis_error),'X_Y_output_difference_distances':distances,
            'zero_extension_positive_contractive':bool(contractive),'max_error':num(max(errors))}


def adjudicate(valid,completion,restoration):
    if not valid:return 'INVALID','INVALID'
    return ('UNIQUE_CPTP_SUPPORT_COMPLETION_CONFIRMED' if completion else 'UNIQUE_CPTP_SUPPORT_COMPLETION_NOT_CONFIRMED',
            'DISCARDED_DIRECTION_RESTORATION_CONFIRMED' if completion and restoration else 'DISCARDED_DIRECTION_RESTORATION_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    with mp.workdps(80):return _run()


def _run():
    b83=(HERE.parent/'support-loop-composition'/'RESULT.json').read_bytes()
    b85=(HERE.parent/'affine-shift-obstruction'/'RESULT.json').read_bytes()
    p83=json.loads(b83);p85=json.loads(b85)
    parents=(hashlib.sha256(b83).hexdigest()==HASH83 and hashlib.sha256(b85).hexdigest()==HASH85 and
             p83['all_valid'] and p85['all_valid'] and
             p83['crossing_verdict']=='SUPPORT_RESTRICTED_CROSSING_CONFIRMED' and
             p83['composition_verdict']=='SUPPORT_LOOP_COMPOSITION_OBSTRUCTED' and
             p83['core_verdict']=='LOSSLESS_LOOP_CORE_TRIVIAL' and
             p85['verdict']=='AFFINE_SHIFT_RESCUE_OBSTRUCTED' and
             p85['recovery_verdict']=='NONUNITAL_RECOVERY_OBSTRUCTION_CONFIRMED')
    L=V84.real_matrix(p83['loop']);N=cofactor(L);R=L+N;minus=L-N
    P=L.T*L;Q=L*L.T;I3=mp.eye(3);U,s,Vh=mp.svd_r(L)
    parent_error=max(maximum(P-V84.real_matrix(p83['initial_projector'])),maximum(Q-V84.real_matrix(p83['final_projector'])),max(abs(s[i]-[1,1,0][i]) for i in range(3)))
    native={'orthogonality_error':maximum(R.T*R-I3),'determinant_error':abs(mp.det(R)-1),
            'support_agreement_error':maximum(R*P-L),'normal_on_support_error':maximum(N*P),
            'normal_input_projector_error':maximum(N.T*N-(I3-P)),
            'normal_output_projector_error':maximum(N*N.T-(I3-Q))}
    rows=[];channel_errors=[]
    for name,T,target in [('zero_extension',L,[-mp.mpf('.5'),mp.mpf('.5'),mp.mpf('.5'),mp.mpf('1.5')]),
                          ('proper_completion',R,[0,0,0,2]),('improper_completion',minus,[-1,1,1,1])]:
        J,e,checks=V84.channel_diagnostics(T);channel_errors.extend(checks.values())
        rows.append({'name':name,'classification':V84.cp_class(e[0]),'choi_eigenvalues':[num(v) for v in e],
                     'expected_spectrum_error':num(spectrum_error(e,target)),
                     'controls':{k:num(v) for k,v in checks.items()}})
    v1=mp.matrix([Vh[0,i] for i in range(3)]);v2=mp.matrix([Vh[1,i] for i in range(3)])
    basis_rows=[];basis_errors=[]
    for label,angle in [('0',mp.mpf(0)),('pi/7',mp.pi/7),('pi/3',mp.pi/3)]:
        w1=mp.cos(angle)*v1+mp.sin(angle)*v2;w2=-mp.sin(angle)*v1+mp.cos(angle)*v2
        u1=L*w1;u2=L*w2;w3=cross(w1,w2);u3=cross(u1,u2)
        rec=u1*w1.T+u2*w2.T+u3*w3.T;error=maximum(rec-R);basis_errors.append(error)
        basis_rows.append({'angle':label,'completion_error':num(error)})
    missing=cross(v1,v2);output=N*missing
    inputs=[(V84.I+sign*V84.bloch(missing))/2 for sign in [1,-1]]
    completed=[V84.phi(R,z) for z in inputs];pruned=[V84.phi(L,z) for z in inputs]
    densities=[V84.density(z) for z in inputs+completed+pruned]
    din=V84.distance(*inputs);dcomplete=V84.distance(*completed);dzero=V84.distance(*pruned)
    inverse_error=max(maximum(V84.phi(R.T,V84.phi(R,z))-z) for z in V84.UNITS)
    change=frobenius(R-L)
    restoration_errors={'input_distance_error':abs(din-1),'completed_distance_error':abs(dcomplete-1),
                        'change_norm_error':abs(change-1),'inverse_matrix_units_error':inverse_error}
    cert=symbolic_certificate();synthetic=synthetic_controls()
    valid=(parents and cert['valid'] and synthetic['valid'] and parent_error<=mp.mpf('1e-60') and
           max(channel_errors+ basis_errors)<=mp.mpf('1e-45') and all(V84.density_valid(d) for d in densities))
    completion=(cert['valid'] and max(native.values())<=mp.mpf('1e-45') and
                [r['classification'] for r in rows]==['NON_CP','CPTP','NON_CP'] and
                max(mp.mpf(r['expected_spectrum_error']) for r in rows)<=mp.mpf('1e-45'))
    restoration=(max(restoration_errors.values())<=mp.mpf('1e-45') and dzero<=mp.mpf('1e-40'))
    verdict,rv=adjudicate(valid,completion,restoration)
    report={'version':'15.86','candidate_index':46,'precision_digits':80,'parent_hashes':{'v15.83':HASH83,'v15.85':HASH85},
            'all_valid':bool(valid),'completion_predicate':bool(completion),'restoration_predicate':bool(restoration),
            'verdict':verdict,'restoration_verdict':rv,
            'controls':{'parents_valid':bool(parents),'symbolic_certificate':cert,'synthetic':synthetic,
                        'parent_error':num(parent_error),'max_channel_error':num(max(channel_errors)),
                        'max_basis_error':num(max(basis_errors)),
                        'minimum_state_eigenvalue':num(min(d['minimum_eigenvalue'] for d in densities)),
                        'max_state_trace_error':num(max(d['trace'] for d in densities)),
                        'max_state_hermiticity_error':num(max(d['hermiticity'] for d in densities))},
            'loop':mat(L),'cofactor':mat(N),'completion':mat(R),'improper_completion':mat(minus),
            'completion_determinant':num(mp.det(R)),'native_residuals':{k:num(v) for k,v in native.items()},
            'channel_rows':rows,'basis_rows':basis_rows,
            'restoration':{'input_axis':[num(x) for x in missing],'output_axis':[num(x) for x in output],
                           'input_distance':num(din),'zero_extension_distance':num(dzero),'completion_distance':num(dcomplete),
                           'change_frobenius_norm':num(change),'residuals':{k:num(v) for k,v in restoration_errors.items()}},
            'scope':'Conditional qubit completion restores the missing direction; it does not rescue the fixed zero extension or select a source law.'}
    def finite(a):
        if isinstance(a,dict):return all(finite(v) for v in a.values())
        if isinstance(a,list):return all(finite(v) for v in a)
        if isinstance(a,str):return a.lower() not in ['nan','inf','+inf','-inf']
        return True
    if not finite(report):report['all_valid']=False;report['verdict']='INVALID';report['restoration_verdict']='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
