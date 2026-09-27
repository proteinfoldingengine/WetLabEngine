"""v15.85: exact qubit affine-shift obstruction and nonunital recovery audit."""
import functools
import hashlib
import importlib.util
import json
import pathlib
import sys
import mpmath as mp
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('channel84_affine',HERE.parent/'loop-channel-recoverability'/'gate.py')
V84=importlib.util.module_from_spec(spec);spec.loader.exec_module(V84)
HASH84='2b51d58a3d5b93c494904a179942feb3e574b8bcec53dbe80c6a6cf5b5ced9f4'
HASH83='bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166'
TAUS=['-1','-.5','0','.5','1']
num=V84.number;matrix=V84.matrix;maximum=V84.maximum
I=V84.I;PAULI=V84.PAULI;tr=V84.tr


def kron(a,b):
    return mp.matrix([[a[i//b.rows,j//b.cols]*b[i%b.rows,j%b.cols] for j in range(a.cols*b.cols)] for i in range(a.rows*b.rows)])


def symbolic_identity():
    eye=sp.eye(2);p=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
    s=sp.kronecker_product(p[1],p[1]);coefficients=[('constant',sp.kronecker_product(eye,eye)/2,1)]
    for i in range(3):
        for j in range(3):coefficients.append(('T'+str(i)+str(j),sp.kronecker_product(p[j].T,p[i])/2,1))
    for k in range(3):coefficients.append(('shift'+str(k),sp.kronecker_product(eye,p[k])/2,-1))
    rows=[{'name':name,'expected_sign':sign,'exact':bool(s*a.T*s.H==sign*a)} for name,a,sign in coefficients]
    unitary=bool(s.H*s==sp.eye(4))
    return {'coefficient_count':len(rows),'unitary_exact':unitary,'rows':rows,'valid':unitary and all(x['exact'] for x in rows)}


def affine(t,shift,z):return V84.phi(t,z)+tr(z)*V84.bloch(shift)/2


def choi_from(action):
    j=mp.zeros(4)
    for a in range(2):
        for b in range(2):
            out=action(V84.UNITS[2*a+b])
            for i in range(2):
                for k in range(2):j[2*a+i,2*b+k]=out[i,k]
    return j


def choi(t,shift):return choi_from(lambda z:affine(t,shift,z))


def marginals(j):
    left=mp.zeros(2);right=mp.zeros(2)
    for a in range(2):
        for b in range(2):
            left[a,b]=sum(j[2*a+i,2*b+i] for i in range(2))
            right[a,b]=sum(j[2*i+a,2*i+b] for i in range(2))
    return left,right


def affine_checks(t,shift):
    j=choi(t,shift);j0=V84.choi(t);opposite=choi(t,-shift)
    s=kron(PAULI[1],PAULI[1]);left,right=marginals(j)
    expected=I+V84.bloch(shift)
    residuals={'hermiticity':maximum(j-j.H),'TP':maximum(left-I),
               'output_offset':maximum(right-expected),'identity_action':maximum(affine(t,shift,I)-expected),
               'shift_reconstruction':maximum(j-j0-kron(I,V84.bloch(shift))/2),
               'spin_flip':maximum(opposite-s*j.T*s.H),'opposite_average':maximum((j+opposite)/2-j0)}
    return j,residuals


def synthetic_controls():
    with mp.workdps(80):
        gamma=mp.mpf('.5');t=mp.diag([mp.sqrt(1-gamma),mp.sqrt(1-gamma),1-gamma]);shift=mp.matrix([0,0,gamma])
        k0=mp.diag([1,mp.sqrt(1-gamma)]);k1=mp.matrix([[0,mp.sqrt(gamma)],[0,0]])
        direct=choi_from(lambda z:k0*z*k0.H+k1*z*k1.H)
        j,res=affine_checks(t,shift);e=mp.eighe(j,eigvals_only=True)
        expected=[0,0,gamma,2-gamma];error=max(abs(a-b) for a,b in zip(e,expected))
        opposite=mp.eighe(choi(t,-shift),eigvals_only=True)
        errors=[maximum(j-direct),error,*res.values()];replacements=[]
        for tau,target in [('0.5',['.25','.25','.75','.75']),('1.5',['-.25','-.25','1.25','1.25'])]:
            jj,rr=affine_checks(mp.zeros(3),mp.matrix([0,mp.mpf(tau),0]));ev=mp.eighe(jj,eigvals_only=True)
            er=max(abs(a-mp.mpf(b)) for a,b in zip(ev,target));errors.extend([er,*rr.values()])
            replacements.append({'Y_shift':tau,'eigenvalues':[num(x) for x in ev],'classification':V84.cp_class(ev[0])})
        valid=max(errors)<=mp.mpf('1e-45') and min(opposite)>=-mp.mpf('1e-40')
        return {'valid':bool(valid),'amplitude_damping_spectrum':[num(x) for x in e],
                'opposite_damping_minimum':num(min(opposite)),'kraus_error':num(maximum(j-direct)),
                'replacement_controls':replacements,'max_error':num(max(errors))}


def witness(j,n):
    eigen,vectors=mp.eighe(j);w=mp.matrix([vectors[i,0] for i in range(4)]);projector=w*w.H
    left,right=marginals(projector);expect=(w.H*j*w)[0]
    coefficients=[(w.H*(kron(I,p)/2)*w)[0] for p in PAULI]
    checks={'normalization':abs(tr(projector)-1),'eigenvector':maximum(j*w-eigen[0]*w),
            'input_marginal':maximum(left-I/2),'output_marginal':maximum(right-I/2),
            'imaginary_expectation':abs(mp.im(expect))}
    return {'n':n,'negative_expectation':num(mp.re(expect)),
            'witness_real':matrix(projector.apply(mp.re)),'witness_imag':matrix(projector.apply(mp.im)),
            'input_marginal_real':matrix(left.apply(mp.re)),'input_marginal_imag':matrix(left.apply(mp.im)),
            'output_marginal_real':matrix(right.apply(mp.re)),'output_marginal_imag':matrix(right.apply(mp.im)),
            'shift_coefficients':[{'real':num(mp.re(x)),'imag':num(mp.im(x)),'absolute':num(abs(x))} for x in coefficients],
            'controls':{k:num(v) for k,v in checks.items()},'valid':bool(max(checks.values())<=mp.mpf('1e-45'))}


def recovery(t,shift,u,s,vh):
    rows=[];errors=[];densities=[]
    for a in range(3):
        left=mp.matrix([u[i,a] for i in range(3)]);right=mp.matrix([vh[a,i] for i in range(3)])
        inputs=[(I+sign*V84.bloch(right))/2 for sign in [1,-1]]
        outputs=[affine(t,shift,z) for z in inputs]
        restored=[V84.measurement_preparation(z,left,right) for z in outputs]
        densities.extend(V84.density(z) for z in inputs+outputs+restored)
        din=V84.distance(*inputs);dout=V84.distance(*outputs)
        fidelity=sum(mp.re(tr(a*b)) for a,b in zip(inputs,restored))/2
        errors.extend([abs(din-1),abs(dout-s[a]),abs(fidelity-(1+dout)/2)])
        rows.append({'axis':a,'role':'active' if a<2 else 'kernel','input_distance':num(din),
                     'output_distance':num(dout),'attained_mean_overlap_fidelity':num(fidelity),
                     'optimal_mean_overlap_fidelity':num((1+dout)/2)})
    valid=max(errors)<=mp.mpf('1e-45') and all(V84.density_valid(d) for d in densities)
    return {'valid':bool(valid),'axes':rows,'max_identity_error':num(max(errors)),
            'minimum_state_eigenvalue':num(min(d['minimum_eigenvalue'] for d in densities)),
            'max_state_trace_error':num(max(d['trace'] for d in densities)),
            'max_state_hermiticity_error':num(max(d['hermiticity'] for d in densities))}


def adjudicate(valid,obstruction,extension):
    if not valid:return 'INVALID','INVALID'
    return ('AFFINE_SHIFT_RESCUE_OBSTRUCTED' if obstruction else 'AFFINE_SHIFT_RESCUE_OBSTRUCTION_NOT_CONFIRMED',
            'NONUNITAL_RECOVERY_OBSTRUCTION_CONFIRMED' if extension else 'NONUNITAL_RECOVERY_OBSTRUCTION_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    with mp.workdps(80):return _run()


def _run():
    b84=(HERE.parent/'loop-channel-recoverability'/'RESULT.json').read_bytes()
    b83=(HERE.parent/'support-loop-composition'/'RESULT.json').read_bytes();p84=json.loads(b84);p83=json.loads(b83)
    inherited=(hashlib.sha256(b84).hexdigest()==HASH84 and hashlib.sha256(b83).hexdigest()==HASH83 and p84['all_valid'] and p83['all_valid'] and
               p84['verdict']=='LATE_CPTP_LOOP_POWER_CONFIRMED' and p84['recovery_verdict']=='CPTP_LOOP_RECOVERY_OBSTRUCTED' and
               p83['crossing_verdict']=='SUPPORT_RESTRICTED_CROSSING_CONFIRMED' and p83['composition_verdict']=='SUPPORT_LOOP_COMPOSITION_OBSTRUCTED' and p83['core_verdict']=='LOSSLESS_LOOP_CORE_TRIVIAL')
    exact=symbolic_identity();synthetic=synthetic_controls();loop=V84.real_matrix(p83['loop']);t=mp.eye(3)
    rows=[];witnesses=[];residuals=[];parent_errors=[]
    for n in range(1,5):
        t=t*loop;j0,rr=affine_checks(t,mp.zeros(3,1));residuals.extend(rr.values())
        eigen=mp.eighe(j0,eigvals_only=True)
        me=maximum(t-V84.real_matrix(p83['powers'][n-1]['matrix']))
        ee=max(abs(a-mp.mpf(b)) for a,b in zip(eigen,p84['rows'][n-1]['choi_eigenvalues']))
        parent_errors.extend([me,ee]);derivatives=[]
        for k in range(3):
            shift=mp.zeros(3,1);shift[k]=1;jj,checks=affine_checks(t,shift);residuals.extend(checks.values())
            de=maximum(jj-j0-kron(I,PAULI[k])/2);residuals.append(de);derivatives.append(num(de))
        rows.append({'n':n,'unital_minimum_eigenvalue':num(eigen[0]),'parent_matrix_error':num(me),
                     'parent_spectrum_error':num(ee),'shift_derivative_errors':derivatives})
        if n<4:witnesses.append(witness(j0,n))
    u,s,vh=mp.svd_r(t);null_axis=mp.matrix([u[i,2] for i in range(3)])
    radicand=1-(s[0]+s[1])**2;radicand_valid=radicand>=-mp.mpf('1e-45')
    bound=mp.sqrt(max(mp.mpf(0),radicand)) if radicand_valid else None
    shifted=[];formula_errors=[];recovery_ok=True
    for text in TAUS:
        tau=mp.mpf(text);shift=tau*null_axis;j,checks=affine_checks(t,shift);residuals.extend(checks.values())
        eigen=mp.eighe(j,eigvals_only=True)
        roots=[mp.sqrt(tau*tau+(s[0]+sign*s[1])**2) for sign in [1,-1]]
        expected=sorted([(1+sign*r)/2 for r in roots for sign in [1,-1]])
        error=max(abs(a-b) for a,b in zip(eigen,expected));formula_errors.append(error)
        classification=V84.cp_class(eigen[0]);rec=None
        if text in ['-.5','0','.5'] and classification=='CPTP':
            rec=recovery(t,shift,u,s,vh);recovery_ok=recovery_ok and rec['valid']
        shifted.append({'tau':text,'shift':[num(x) for x in shift],'classification':classification,
                        'choi_eigenvalues':[num(x) for x in eigen],'spectrum_formula_error':num(error),
                        'controls':{k:num(v) for k,v in checks.items()},'recovery':rec})
    valid=(inherited and exact['valid'] and synthetic['valid'] and max(parent_errors)<=mp.mpf('1e-60') and
           max(residuals)<=mp.mpf('1e-45') and all(w['valid'] for w in witnesses) and
           s[1]>=mp.mpf('1e-4') and s[2]<=mp.mpf('1e-60') and radicand_valid and
           max(formula_errors)<=mp.mpf('1e-45') and recovery_ok)
    obstruction=(exact['valid'] and all(mp.mpf(w['negative_expectation'])<=-mp.mpf('1e-8') and
                 all(mp.mpf(c['absolute'])<=mp.mpf('1e-45') for c in w['shift_coefficients']) for w in witnesses))
    extension=True
    for row in shifted:
        if row['tau'] in ['-1','1']:extension=extension and row['classification']=='NON_CP'
        else:
            rec=row['recovery'];extension=extension and row['classification']=='CPTP' and rec is not None
            if rec is not None:
                extension=extension and rec['valid'] and all(mp.mpf('1e-4')<=mp.mpf(a['output_distance'])<=1-mp.mpf('1e-4') for a in rec['axes'][:2]) and mp.mpf(rec['axes'][2]['output_distance'])<=mp.mpf('1e-40')
    verdict,rv=adjudicate(valid,obstruction,extension)
    report={'version':'15.85','candidate_index':46,'precision_digits':80,'parent_hashes':{'v15.84':HASH84,'v15.83':HASH83},
            'all_valid':bool(valid),'verdict':verdict,'recovery_verdict':rv,
            'controls':{'inherited_valid':bool(inherited),'symbolic_identity':exact,'synthetic':synthetic,
                        'max_parent_error':num(max(parent_errors)),'max_affine_identity_error':num(max(residuals)),
                        'max_null_axis_formula_error':num(max(formula_errors)),'recovery_valid':bool(recovery_ok)},
            'unital_rows':rows,'witnesses':witnesses,'fourth_singular_values':[num(v) for v in s],
            'null_left_axis':[num(v) for v in null_axis],'tau_bound_radicand':num(radicand),
            'null_axis_admissible_abs_tau':None if bound is None else num(bound),'shift_rows':shifted,
            'scope':'All-shifts theorem is exact qubit spin-flip positivity argument. Native Bloch interpretation remains conditional.'}
    def finite(a):
        if isinstance(a,dict):return all(finite(v) for v in a.values())
        if isinstance(a,list):return all(finite(v) for v in a)
        if isinstance(a,str):return a.lower() not in ['nan','inf','+inf','-inf']
        return True
    if not finite(report):report['all_valid']=False;report['verdict']='INVALID';report['recovery_verdict']='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
