"""v15.88: established exact-erasure qubit EB theorem and soft boundary audit."""
import functools
import hashlib
import importlib.util
import json
import pathlib
import sys
import mpmath as mp
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent

def load_helper(name,folder):
    spec=importlib.util.spec_from_file_location(name,HERE.parent/folder/'gate.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

V85=load_helper('affine85_eb','affine-shift-obstruction')
V86=load_helper('completion86_eb','cptp-support-completion')
V84=V85.V84
HASH83='bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166'
HASH87='4167a743c5e2da6fa0de9a00e3a2cf56778286eb58dbee4e2cb31a807dbb5c66'
num=V84.number;mat=V84.matrix;maximum=V84.maximum


def partial_input(z):
    out=z.copy()
    for a in range(2):
        for b in range(2):
            for i in range(2):
                for k in range(2):out[2*a+i,2*b+k]=z[2*b+i,2*a+k]
    return out


def symbolic_certificate():
    I=sp.eye(2);X=sp.Matrix([[0,1],[1,0]]);Y=sp.Matrix([[0,-sp.I],[sp.I,0]]);Z=sp.diag(1,-1)
    pauli=[X,Y,Z];S=sp.kronecker_product(X,I)
    coefficients=[('constant',sp.eye(4)/2)]
    for j in range(2):
        for i in range(3):coefficients.append(('T'+str(i)+str(j),sp.kronecker_product(pauli[j].T,pauli[i])/2))
    for i in range(3):coefficients.append(('shift'+str(i),sp.kronecker_product(I,pauli[i])/2))
    zero=lambda m:all(sp.simplify(x)==0 for x in m)
    checks={name:zero(partial_input(c)-S*c*S.H) for name,c in coefficients}
    e=sp.symbols('epsilon',real=True)
    J=(sp.eye(4)+sp.kronecker_product(X.T,X)/2+sp.kronecker_product(Y.T,Y)/2+e*sp.kronecker_product(Z.T,Z))/2
    G=partial_input(J)
    vectors=[sp.Matrix(v)/sp.sqrt(2) for v in [[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]]]
    ev=[1+e/2,e/2,(1-e)/2,(1-e)/2]
    gv=[(1+e)/2,(1+e)/2,1-e/2,-e/2]
    soft={}
    for label,operator,eigen in [('choi',J,ev),('partial_input',G,gv)]:
        for k,(v,x) in enumerate(zip(vectors,eigen)):soft[label+'_'+str(k)]=zero(operator*v-x*v)
    return {'coefficient_count':len(checks),'coefficient_checks':{k:bool(v) for k,v in checks.items()},
            'soft_equation_count':len(soft),'soft_checks':{k:bool(v) for k,v in soft.items()},
            'valid':bool(all(checks.values()) and all(soft.values()))}


def ppt_class(x):
    if x>=-mp.mpf('1e-40'):return 'PPT'
    if x<=-mp.mpf('1e-8'):return 'NOT_PPT'
    return 'UNRESOLVED'


def channel_row(T,t):
    J,checks=V85.affine_checks(T,t);G=partial_input(J);F=mp.diag([1,-1,1])
    checks['partial_transpose_reconstruction']=maximum(G-V85.choi(T*F,t))
    checks['partial_hermiticity']=maximum(G-G.H)
    checks['choi_trace']=abs(V84.tr(J)-2)
    checks['action_reconstruction']=max(maximum(V84.choi_action(J,z)-V85.affine(T,t,z)) for z in V84.UNITS)
    e=list(mp.eighe(J,eigvals_only=True));g=list(mp.eighe(G,eigvals_only=True))
    neg=sum(max(mp.mpf(0),-v) for v in g)/2
    row={'matrix':mat(T),'shift':[num(v) for v in t],'shift_norm':num(V86.frobenius(t)),
         'singular_values':[num(v) for v in mp.svd_r(T,compute_uv=False)],
         'cp_class':V84.cp_class(e[0]),'ppt_class':ppt_class(g[0]),
         'choi_eigenvalues':[num(v) for v in e],'partial_transpose_eigenvalues':[num(v) for v in g],
         'normalized_choi_negativity':num(neg),'controls':{k:num(v) for k,v in checks.items()}}
    return row,e,g,list(checks.values())


def spectrum_error(e,target):return max(abs(a-b) for a,b in zip(e,sorted(target)))


def kernel_pair(T,t,n):
    inputs=[(V84.I+sign*V84.bloch(n))/2 for sign in [1,-1]]
    outputs=[V85.affine(T,t,z) for z in inputs]
    return V84.distance(*outputs),[V84.density(z) for z in inputs+outputs]


def synthetic_controls():
    zero=mp.zeros(3,1);half=mp.mpf('.5');q=1/mp.sqrt(2)
    cases=[('identity',mp.eye(3),zero,[0,0,0,2],[-1,1,1,1]),
           ('depolarizing',mp.eye(3)/4,zero,[mp.mpf(3)/8]*3+[mp.mpf(7)/8],[mp.mpf(1)/8]+[mp.mpf(5)/8]*3),
           ('amplitude_damping',mp.diag([q,q,half]),mp.matrix([0,0,half]),[0,0,half,mp.mpf('1.5')],[-half,half,1,1])]
    rows=[];errors=[]
    for name,T,t,expected,ptexpected in cases:
        row,e,g,checks=channel_row(T,t);errors.extend(checks)
        er=max(spectrum_error(e,expected),spectrum_error(g,ptexpected));errors.append(er)
        row.update({'name':name,'formula_error':num(er)});rows.append(row)
    k0=mp.diag([1,q]);k1=mp.matrix([[0,q],[0,0]])
    direct=V85.choi_from(lambda z:k0*z*k0.H+k1*z*k1.H)
    kraus_error=maximum(direct-V85.choi(cases[2][1],cases[2][2]));errors.append(kraus_error)
    dep_error=abs(mp.svd_r(cases[1][1],compute_uv=False)[2]-mp.mpf('.25'));errors.append(dep_error)
    valid=(max(errors)<=mp.mpf('1e-45') and [r['cp_class'] for r in rows]==['CPTP']*3 and
           [r['ppt_class'] for r in rows]==['NOT_PPT','PPT','NOT_PPT'])
    return {'valid':bool(valid),'rows':rows,'kraus_error':num(kraus_error),'depolarizing_minimum_singular_value_error':num(dep_error),'max_error':num(max(errors))}


def adjudicate(valid,exact,soft):
    if not valid:return 'INVALID','INVALID'
    return ('EXACT_ERASURE_ENTANGLEMENT_BREAKING_CONFIRMED' if exact else 'EXACT_ERASURE_ENTANGLEMENT_BREAKING_NOT_CONFIRMED',
            'SOFT_ERASURE_ENTANGLEMENT_SURVIVES' if soft else 'SOFT_ERASURE_ENTANGLEMENT_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    with mp.workdps(80):return _run()


def _run():
    b83=(HERE.parent/'support-loop-composition'/'RESULT.json').read_bytes()
    b87=(HERE.parent/'cptp-erasure-cost'/'RESULT.json').read_bytes()
    p83=json.loads(b83);p87=json.loads(b87)
    parents=(hashlib.sha256(b83).hexdigest()==HASH83 and hashlib.sha256(b87).hexdigest()==HASH87 and
             p83['all_valid'] and p87['all_valid'] and
             p83['crossing_verdict']=='SUPPORT_RESTRICTED_CROSSING_CONFIRMED' and
             p83['composition_verdict']=='SUPPORT_LOOP_COMPOSITION_OBSTRUCTED' and
             p83['core_verdict']=='LOSSLESS_LOOP_CORE_TRIVIAL' and
             p87['verdict']=='ERASURE_COST_BOUND_ATTAINED' and
             p87['translation_verdict']=='OPTIMAL_ERASURE_TRANSLATION_RIGID' and
             p87['distinguishability_verdict']=='OPTIMAL_ERASURE_DISTINGUISHABILITY_CONFIRMED')
    L=V84.real_matrix(p83['loop']);P=L.T*L;N=V86.cofactor(L);U,s,Vh=mp.svd_r(L)
    parent_error=max(maximum(P-V84.real_matrix(p83['initial_projector'])),maximum(L/2-V84.real_matrix(p87['optimal']['matrix'])),max(abs(s[i]-[1,1,0][i]) for i in range(3)))
    v1=mp.matrix([Vh[0,i] for i in range(3)]);v2=mp.matrix([Vh[1,i] for i in range(3)])
    n=V86.cross(v1,v2);u1=L*v1;u2=L*v2;u3=N*n
    F=mp.diag([1,-1,1]);H=mp.eye(3)-2*n*n.T;A=H*F
    geometry_errors=[maximum(A.T*A-mp.eye(3)),abs(mp.det(A)-1),maximum(H*H-mp.eye(3)),abs(mp.det(H)+1)]
    zero=mp.zeros(3,1);native=[];errors=[];densities=[]
    cases=[('plane_minus',L/4,-u3/2),('plane_unital',L/4,zero),('plane_plus',L/4,u3/2),
           ('optimal',L/2,zero),('line_nonunital',u1*v1.T/2,u2/4),('point_Y',mp.zeros(3),mp.matrix([0,mp.mpf('.5'),0]))]
    for name,T,t in cases:
        row,e,g,checks=channel_row(T,t);errors.extend(checks)
        identity_errors=[maximum(T*A-T*F),maximum(T*H-T),maximum(V85.choi(T*A,t)-V85.choi(T*F,t))]
        geometry_errors.extend(identity_errors)
        distance,ds=kernel_pair(T,t,n);densities.extend(ds)
        row.update({'name':name,'kernel_norm':num(V86.frobenius(T*n)),'kernel_pair_distance':num(distance),
                    'isospectral_error':num(max(abs(x-y) for x,y in zip(e,g))),
                    'proper_rotation_identity_error':num(max(identity_errors))});native.append(row)
    soft=[]
    for text in ['0','0.01','0.0001','0.000001']:
        epsilon=mp.mpf(text);T=L/2+epsilon*N;row,e,g,checks=channel_row(T,zero);errors.extend(checks)
        distance,ds=kernel_pair(T,zero,n);densities.extend(ds)
        kn=V86.frobenius(T*n);smallest=mp.svd_r(T,compute_uv=False)[2]
        jerr=spectrum_error(e,[epsilon/2,(1-epsilon)/2,(1-epsilon)/2,1+epsilon/2])
        gerr=spectrum_error(g,[-epsilon/2,(1+epsilon)/2,(1+epsilon)/2,1-epsilon/2])
        neg=mp.mpf(row['normalized_choi_negativity'])
        row.update({'epsilon':text,'kernel_norm':num(kn),'kernel_pair_distance':num(distance),
                    'minimum_singular_value':num(smallest),'choi_formula_error':num(jerr),'partial_formula_error':num(gerr),
                    'erasure_formula_error':num(max(abs(kn-epsilon),abs(distance-epsilon),abs(smallest-epsilon))),
                    'negativity_formula_error':num(abs(neg-epsilon/4))});soft.append(row)
    symbolic=symbolic_certificate();synthetic=synthetic_controls()
    valid=(parents and symbolic['valid'] and synthetic['valid'] and parent_error<=mp.mpf('1e-60') and
           max(errors+geometry_errors)<=mp.mpf('1e-45') and all(V84.density_valid(d) for d in densities))
    exact=all(r['cp_class']=='CPTP' and r['ppt_class']=='PPT' and mp.mpf(r['isospectral_error'])<=mp.mpf('1e-45') and
              max(mp.mpf(r[k]) for k in ['kernel_norm','kernel_pair_distance','normalized_choi_negativity'])<=mp.mpf('1e-40') for r in native)
    soft_yes=([r['cp_class'] for r in soft]==['CPTP']*4 and [r['ppt_class'] for r in soft]==['PPT','NOT_PPT','NOT_PPT','NOT_PPT'] and
              max(mp.mpf(r[k]) for r in soft for k in ['choi_formula_error','partial_formula_error','erasure_formula_error','negativity_formula_error'])<=mp.mpf('1e-45'))
    verdict,sv=adjudicate(valid,exact,soft_yes)
    report={'version':'15.88','candidate_index':46,'precision_digits':80,'parent_hashes':{'v15.83':HASH83,'v15.87':HASH87},
            'all_valid':bool(valid),'exact_erasure_predicate':bool(exact),'soft_predicate':bool(soft_yes),'verdict':verdict,'soft_verdict':sv,
            'controls':{'parents_valid':bool(parents),'symbolic_certificate':symbolic,'synthetic':synthetic,
                        'parent_error':num(parent_error),'max_affine_partial_error':num(max(errors)),
                        'max_reflection_rotation_error':num(max(geometry_errors)),
                        'minimum_state_eigenvalue':num(min(d['minimum_eigenvalue'] for d in densities)),
                        'max_state_trace_error':num(max(d['trace'] for d in densities)),
                        'max_state_hermiticity_error':num(max(d['hermiticity'] for d in densities))},
            'kernel_axis':[num(x) for x in n],'input_rotation':mat(A),'native_rows':native,'soft_rows':soft,
            'scope':'Reproducible application of established exact-erasure qubit EB theorem; no approximate-erasure implication or source-law selection.',
            'sources':['https://arxiv.org/abs/quant-ph/0302031','https://arxiv.org/abs/quant-ph/9605038']}
    def finite(a):
        if isinstance(a,dict):return all(finite(v) for v in a.values())
        if isinstance(a,list):return all(finite(v) for v in a)
        if isinstance(a,str):return a.lower() not in ['nan','inf','+inf','-inf']
        return True
    if not finite(report):report['all_valid']=False;report['verdict']='INVALID';report['soft_verdict']='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
