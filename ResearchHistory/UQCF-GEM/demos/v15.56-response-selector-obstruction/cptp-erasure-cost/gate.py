"""v15.87: exact-erasure CPTP distortion floor and its unique affine optimum."""
import functools
import hashlib
import importlib.util
import json
import pathlib
import sys
import mpmath as mp
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v1585_erasure_helpers',HERE.parent/'affine-shift-obstruction'/'gate.py')
V85=importlib.util.module_from_spec(spec);spec.loader.exec_module(V85)
V84=V85.V84
HASH83='bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166'
HASH86='7e0df41086ed226c90a22e09270f305e3de68abfe5d1d6a9e5811598c324090d'
num=V84.number;mat=V84.matrix;maximum=V84.maximum


def symbolic_certificate():
    s1,s2=sp.symbols('s1 s2',real=True)
    t1,t2,t3=sp.symbols('t1 t2 t3',real=True)
    X=sp.Matrix([[0,1],[1,0]]);Y=sp.Matrix([[0,-sp.I],[sp.I,0]]);Z=sp.diag(1,-1)
    J=(sp.eye(4)+s1*sp.kronecker_product(X.T,X)+s2*sp.kronecker_product(Y.T,Y))/2
    vectors=[sp.Matrix(v)/sp.sqrt(2) for v in [[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]]]
    eigen=[(1+s1+s2)/2,(1-s1-s2)/2,(1+s1-s2)/2,(1-s1+s2)/2]
    zero=lambda m:all(sp.simplify(v)==0 for v in m)
    checks={name:zero(J*v-e*v) for name,v,e in zip(['Phi_plus','Phi_minus','Psi_plus','Psi_minus'],vectors,eigen)}
    Jt=J.subs({s1:sp.Rational(1,2),s2:sp.Rational(1,2)})+sp.kronecker_product(sp.eye(2),t1*X+t2*Y+t3*Z)/2
    w=vectors[1];jw=Jt*w
    checks['translation_kernel_expectation']=sp.simplify((w.H*Jt*w)[0])==0
    checks['translation_kernel_image_norm']=sp.simplify((jw.H*jw)[0]-(t1*t1+t2*t2+t3*t3)/4)==0
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def cross(a,b):return mp.matrix([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])
def frobenius(a):return mp.sqrt(sum(abs(x)**2 for x in a))
def operator(a):return mp.svd_r(a,compute_uv=False)[0]
def spectrum_error(e,target):return max(abs(a-b) for a,b in zip(e,sorted(target)))


def channel_row(T,shift):
    J,checks=V85.affine_checks(T,shift)
    checks['action_reconstruction']=max(maximum(V85.affine(T,shift,z)-V84.choi_action(J,z)) for z in V84.UNITS)
    eigen=list(mp.eighe(J,eigvals_only=True))
    return {'classification':V84.cp_class(eigen[0]),'choi_eigenvalues':[num(v) for v in eigen],
            'controls':{k:num(v) for k,v in checks.items()}},eigen,list(checks.values())


def adjudicate(valid,bound,translation,distinguishability):
    if not valid:return ('INVALID',)*3
    return ('ERASURE_COST_BOUND_ATTAINED' if bound else 'ERASURE_COST_BOUND_NOT_ATTAINED',
            'OPTIMAL_ERASURE_TRANSLATION_RIGID' if bound and translation else 'OPTIMAL_ERASURE_TRANSLATION_RIGIDITY_NOT_CONFIRMED',
            'OPTIMAL_ERASURE_DISTINGUISHABILITY_CONFIRMED' if bound and distinguishability else 'OPTIMAL_ERASURE_DISTINGUISHABILITY_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    with mp.workdps(80):return _run()


def _run():
    b83=(HERE.parent/'support-loop-composition'/'RESULT.json').read_bytes()
    b86=(HERE.parent/'cptp-support-completion'/'RESULT.json').read_bytes()
    p83=json.loads(b83);p86=json.loads(b86)
    parents=(hashlib.sha256(b83).hexdigest()==HASH83 and hashlib.sha256(b86).hexdigest()==HASH86 and
             p83['all_valid'] and p86['all_valid'] and
             p83['crossing_verdict']=='SUPPORT_RESTRICTED_CROSSING_CONFIRMED' and
             p83['composition_verdict']=='SUPPORT_LOOP_COMPOSITION_OBSTRUCTED' and
             p83['core_verdict']=='LOSSLESS_LOOP_CORE_TRIVIAL' and
             p86['verdict']=='UNIQUE_CPTP_SUPPORT_COMPLETION_CONFIRMED' and
             p86['restoration_verdict']=='DISCARDED_DIRECTION_RESTORATION_CONFIRMED')
    L=V84.real_matrix(p83['loop']);P=L.T*L;K=mp.eye(3)-P;T=L/2;zero=mp.zeros(3,1)
    U,s,Vh=mp.svd_r(L)
    parent_error=max(maximum(L-V84.real_matrix(p86['loop'])),maximum(P-V84.real_matrix(p83['initial_projector'])),max(abs(s[i]-[1,1,0][i]) for i in range(3)))
    v1=mp.matrix([Vh[0,i] for i in range(3)]);v2=mp.matrix([Vh[1,i] for i in range(3)])
    u1=L*v1;u2=L*v2;v3=cross(v1,v2)
    optimal,eigen,errors=channel_row(T,zero)
    nuc=sum(mp.svd_r(T,compute_uv=False));op=operator(T-L);frob=frobenius(T-L)
    construction_error=max(maximum((V84.measurement_preparation(z,v1,u1)+V84.measurement_preparation(z,v2,u2))/2-V84.phi(T,z)) for z in V84.UNITS)
    native={'kernel_erasure_error':maximum(T*K),'nuclear_norm_error':abs(nuc-1),
            'operator_cost_error':abs(op-mp.mpf('.5')),'frobenius_cost_error':abs(frob-1/mp.sqrt(2)),
            'measure_prepare_reconstruction_error':construction_error,
            'choi_spectrum_error':spectrum_error(eigen,[0,mp.mpf('.5'),mp.mpf('.5'),1])}
    optimal.update({'matrix':mat(T),'nuclear_norm':num(nuc),'operator_error':num(op),'frobenius_error':num(frob),
                    'residuals':{k:num(v) for k,v in native.items()}})
    iso=[];formula_errors=[]
    for text in ['0','0.25','0.5','0.75','1']:
        a=mp.mpf(text);row,e,check=channel_row(a*L,zero);errors.extend(check)
        err=spectrum_error(e,[(1-2*a)/2,mp.mpf('.5'),mp.mpf('.5'),(1+2*a)/2]);formula_errors.append(err)
        row.update({'alpha':text,'formula_error':num(err)});iso.append(row)
    aniso=[];aniso_errors=[]
    for at,bt,ot,ft in [('0.75','0.25',mp.mpf('.75'),mp.sqrt(10)/4),('1','0',mp.mpf(1),mp.mpf(1)),('0.25','0.25',mp.mpf('.75'),3*mp.sqrt(2)/4)]:
        a=mp.mpf(at);b=mp.mpf(bt);A=a*u1*v1.T+b*u2*v2.T;row,e,check=channel_row(A,zero);errors.extend(check)
        oa=operator(A-L);fa=frobenius(A-L)
        err=max(abs(oa-ot),abs(fa-ft),spectrum_error(e,[(1-a-b)/2,(1-a+b)/2,(1+a-b)/2,(1+a+b)/2]))
        aniso_errors.append(err);row.update({'a':at,'b':bt,'operator_error':num(oa),'frobenius_error':num(fa),'formula_error':num(err)});aniso.append(row)
    shifts=[('zero',zero)]
    for j in range(3):
        for sign in [1,-1]:
            t=mp.zeros(3,1);t[j]=sign*mp.mpf('.1');shifts.append(('axis_'+str(j)+'_'+str(sign),t))
    translation_rows=[]
    for label,t in shifts:
        row,e,check=channel_row(T,t);errors.extend(check);row.update({'label':label,'shift':[num(x) for x in t]});translation_rows.append(row)
    distance_rows=[];distance_errors=[];kernel_distance=None;densities=[]
    for label,v,expected in [('v1',v1,mp.mpf('.5')),('v2',v2,mp.mpf('.5')),('plane_diagonal',(v1+v2)/mp.sqrt(2),mp.mpf('.5')),('kernel',v3,mp.mpf(0))]:
        inputs=[(V84.I+sign*V84.bloch(v))/2 for sign in [1,-1]]
        outputs=[V84.phi(T,z) for z in inputs]
        densities.extend(V84.density(z) for z in inputs+outputs)
        din=V84.distance(*inputs);dout=V84.distance(*outputs);distance_errors.append(abs(din-1))
        target_distance=None
        if label=='kernel':kernel_distance=dout
        else:
            distance_errors.append(abs(dout-expected));target=V84.phi(L,inputs[0]);densities.append(V84.density(target))
            target_distance=V84.distance(outputs[0],target);distance_errors.append(abs(target_distance-mp.mpf('.25')))
        distance_rows.append({'axis':label,'input_axis':[num(x) for x in v], 'input_distance':num(din),'output_distance':num(dout),
                              'formal_target_output_distance':None if target_distance is None else num(target_distance)})
    exact=symbolic_certificate();spin=V85.symbolic_identity();synthetic=V85.synthetic_controls()
    valid=(parents and exact['valid'] and spin['valid'] and synthetic['valid'] and parent_error<=mp.mpf('1e-60') and
           max(errors+formula_errors+aniso_errors)<=mp.mpf('1e-45') and
           [x['classification'] for x in iso]==['CPTP','CPTP','CPTP','NON_CP','NON_CP'] and
           [x['classification'] for x in aniso]==['CPTP']*3 and all(V84.density_valid(d) for d in densities))
    bound=optimal['classification']=='CPTP' and max(native.values())<=mp.mpf('1e-45')
    translation=[x['classification'] for x in translation_rows]==['CPTP']+['NON_CP']*6
    distinguishability=max(distance_errors)<=mp.mpf('1e-45') and kernel_distance<=mp.mpf('1e-40')
    verdict,tv,dv=adjudicate(valid,bound,translation,distinguishability)
    report={'version':'15.87','candidate_index':46,'precision_digits':80,'parent_hashes':{'v15.83':HASH83,'v15.86':HASH86},
            'all_valid':bool(valid),'bound_predicate':bool(bound),'translation_predicate':bool(translation),'distinguishability_predicate':bool(distinguishability),
            'verdict':verdict,'translation_verdict':tv,'distinguishability_verdict':dv,
            'controls':{'parents_valid':bool(parents),'symbolic_certificate':exact,'spin_flip_certificate':spin,'synthetic_affine':synthetic,
                        'parent_error':num(parent_error),'max_affine_error':num(max(errors)),
                        'max_isotropic_formula_error':num(max(formula_errors)),'max_anisotropic_formula_error':num(max(aniso_errors)),
                        'minimum_state_eigenvalue':num(min(d['minimum_eigenvalue'] for d in densities)),
                        'max_state_trace_error':num(max(d['trace'] for d in densities)),
                        'max_state_hermiticity_error':num(max(d['hermiticity'] for d in densities))},
            'optimal':optimal,'isotropic_rows':iso,'anisotropic_rows':aniso,'translation_rows':translation_rows,
            'distinguishability_rows':distance_rows,'max_distance_error':num(max(distance_errors)),
            'scope':'Exact-erasure qubit channel optimum for fixed norm objectives; not physical source-law selection.'}
    def finite(a):
        if isinstance(a,dict):return all(finite(v) for v in a.values())
        if isinstance(a,list):return all(finite(v) for v in a)
        if isinstance(a,str):return a.lower() not in ['nan','inf','+inf','-inf']
        return True
    if not finite(report):
        report['all_valid']=False
        for k in ['verdict','translation_verdict','distinguishability_verdict']:report[k]='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
