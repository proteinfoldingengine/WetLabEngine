"""v15.89: sharp normalized Choi-negativity bound for qubit CPTP maps."""
import functools
import hashlib
import importlib.util
import json
import pathlib
import sys
import mpmath as mp
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('erasure88_bound',HERE.parent/'exact-erasure-entanglement'/'gate.py')
V88=importlib.util.module_from_spec(spec);spec.loader.exec_module(V88)
V84=V88.V84;V85=V88.V85;V86=V88.V86
num=V84.number;mat=V84.matrix;maximum=V84.maximum;norm=V86.frobenius
HASH83='bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166'
HASH88='06295e1705c9c38567ee8dc1bee10a737b0d9a8b260200867a68d01fc10130ab'


def symbolic_certificate():
    I=sp.eye(2);X=sp.Matrix([[0,1],[1,0]]);Y=sp.Matrix([[0,-sp.I],[sp.I,0]]);Z=sp.diag(1,-1)
    pauli=[X,Y,Z];S=sp.kronecker_product(X,I);zero=lambda m:all(sp.simplify(x)==0 for x in m)
    coefficients=[('constant',sp.eye(4)/2,sp.zeros(4))]
    for j in range(3):
        for i in range(3):
            coefficients.append(('T'+str(i)+str(j),sp.kronecker_product(pauli[j].T,pauli[i])/2,
                                 sp.kronecker_product(Z,pauli[i]) if j==2 else sp.zeros(4)))
    for i in range(3):coefficients.append(('shift'+str(i),sp.kronecker_product(I,pauli[i])/2,sp.zeros(4)))
    checks={name:zero(V88.partial_input(c)-S*c*S.H-rhs) for name,c,rhs in coefficients}
    w=sp.symbols('w1 w2 w3',real=True);W=sum((a*b for a,b in zip(w,pauli)),sp.zeros(2));D=sp.kronecker_product(Z,W)
    checks['norm_square']=zero(D*D-sum(x*x for x in w)*sp.eye(4))
    e=sp.symbols('epsilon',real=True);a=(1+e)/2
    J=(sp.eye(4)+a*sp.kronecker_product(X.T,X)+a*sp.kronecker_product(Y.T,Y)+e*sp.kronecker_product(Z.T,Z))/2
    G=V88.partial_input(J)
    vectors=[sp.Matrix(v)/sp.sqrt(2) for v in [[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]]]
    for name,operator,eigen in [('choi',J,[1+e,0,(1-e)/2,(1-e)/2]),('partial',G,[(1+e)/2,(1+e)/2,1,-e])]:
        for k,(v,x) in enumerate(zip(vectors,eigen)):checks[name+'_'+str(k)]=zero(operator*v-x*v)
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def adjudicate(valid,bound,sharpness):
    if not valid:return 'INVALID','INVALID'
    return ('WEAKEST_DIRECTION_NEGATIVITY_BOUND_CONFIRMED' if bound else 'WEAKEST_DIRECTION_NEGATIVITY_BOUND_NOT_CONFIRMED',
            'NEGATIVITY_BOUND_SHARPNESS_CONFIRMED' if bound and sharpness else 'NEGATIVITY_BOUND_SHARPNESS_NOT_CONFIRMED')


def evaluate(T,t,family,label):
    row,e,g,errors=V88.channel_row(T,t);J=V85.choi(T,t);G=V88.partial_input(J)
    U,s,Vh=mp.svd_r(T);delta=s[2];n=mp.matrix([Vh[2,i] for i in range(3)]);w=T*n
    F=mp.diag([1,-1,1]);H=mp.eye(3)-2*n*n.T;A=H*F
    B,bc=V85.affine_checks(T*A,t);eb=list(mp.eighe(B,eigvals_only=True));D=G-B
    formula=V85.kron(V84.bloch(F*n).T,V84.bloch(w));d_norm=max(abs(x) for x in mp.eighe(D,eigvals_only=True))
    controls={'proper_orthogonality':maximum(A.T*A-mp.eye(3)),'proper_determinant':abs(mp.det(A)-1),
              'axis_unit':abs(norm(n)-1),'weakest_norm':abs(norm(w)-delta),
              'difference_formula':maximum(D-formula),'difference_hermiticity':maximum(D-D.H),
              'difference_norm':abs(d_norm-delta),'comparison_isospectral':max(abs(x-y) for x,y in zip(e,eb))}
    errors.extend(bc.values());errors.extend(controls.values())
    inputs=[(V84.I+sign*V84.bloch(n))/2 for sign in [1,-1]];outputs=[V85.affine(T,t,z) for z in inputs]
    densities=[V84.density(z) for z in inputs+outputs]
    di=V84.distance(*inputs);do=V84.distance(*outputs);de=max(abs(di-1),abs(do-delta))
    neg=sum(max(mp.mpf(0),-x) for x in g)/2;slack=delta/2-neg;lower=g[0]+delta;count=sum(x<-mp.mpf('1e-40') for x in g)
    row.update({'family':family,'label':label,'weakest_axis':[num(x) for x in n],'input_rotation':mat(A),
                'comparison_eigenvalues':[num(x) for x in eb],'comparison_cp_class':V84.cp_class(eb[0]),
                'minimum_singular_value':num(delta),'negativity_bound':num(delta/2),'bound_slack':num(slack),
                'partial_minimum_plus_delta':num(lower),'negative_partial_eigenvalue_count':count,
                'difference_operator_norm':num(d_norm),'input_pair_distance':num(di),'output_pair_distance':num(do),
                'distance_prediction_error':num(de),'attainment_error':num(abs(neg-delta/2)),
                'comparison_controls':{k:num(v) for k,v in controls.items()},
                'comparison_affine_controls':{k:num(v) for k,v in bc.items()},
                'state_controls':[{k:num(v) for k,v in d.items()} for d in densities]})
    valid=(row['cp_class']=='CPTP' and row['comparison_cp_class']=='CPTP' and max(errors)<=mp.mpf('1e-45') and all(V84.density_valid(d) for d in densities))
    bound=count<=1 and slack>=-mp.mpf('1e-40') and lower>=-mp.mpf('1e-40') and de<=mp.mpf('1e-45')
    return row,bool(valid),bool(bound),max(errors),densities,e,g


@functools.lru_cache(maxsize=1)
def run_measurement():
    with mp.workdps(80):return _run()


def _run():
    b83=(HERE.parent/'support-loop-composition'/'RESULT.json').read_bytes();b88=(HERE.parent/'exact-erasure-entanglement'/'RESULT.json').read_bytes()
    p83=json.loads(b83);p88=json.loads(b88)
    parents=(hashlib.sha256(b83).hexdigest()==HASH83 and hashlib.sha256(b88).hexdigest()==HASH88 and p83['all_valid'] and p88['all_valid'] and
             p83['crossing_verdict']=='SUPPORT_RESTRICTED_CROSSING_CONFIRMED' and p83['composition_verdict']=='SUPPORT_LOOP_COMPOSITION_OBSTRUCTED' and
             p83['core_verdict']=='LOSSLESS_LOOP_CORE_TRIVIAL' and p88['verdict']=='EXACT_ERASURE_ENTANGLEMENT_BREAKING_CONFIRMED' and p88['soft_verdict']=='SOFT_ERASURE_ENTANGLEMENT_SURVIVES')
    L=V84.real_matrix(p83['loop']);P=L.T*L;N=V86.cofactor(L);U,s,Vh=mp.svd_r(L)
    parent_error=max(maximum(P-V84.real_matrix(p83['initial_projector'])),maximum(P*P-P),max(abs(s[i]-[1,1,0][i]) for i in range(3)))
    v1=mp.matrix([Vh[0,i] for i in range(3)]);v2=mp.matrix([Vh[1,i] for i in range(3)]);n=V86.cross(v1,v2)
    u1=L*v1;u2=L*v2;u3=N*n
    input_frame=mp.matrix([[v1[i],v2[i],n[i]] for i in range(3)]);output_frame=mp.matrix([[u1[i],u2[i],u3[i]] for i in range(3)])
    frame_error=max(maximum(A.T*A-mp.eye(3)) for A in [input_frame,output_frame])
    frame_error=max(frame_error,abs(mp.det(input_frame)-1),abs(mp.det(output_frame)-1))
    zero=mp.zeros(3,1);cases=[]
    for family,key in [('inherited_native','native_rows'),('inherited_soft','soft_rows')]:
        for k,r in enumerate(p88[key]):cases.append((family,r.get('name',r.get('epsilon',str(k))),V84.real_matrix(r['matrix']),mp.matrix([mp.mpf(v) for v in r['shift']]),r,None))
    for text in ['0','0.000001','0.0001','0.01','0.25','0.5','1']:
        e=mp.mpf(text);cases.append(('saturation',text,((1+e)/2)*L+e*N,zero,None,([0,(1-e)/2,(1-e)/2,1+e],[-e,(1+e)/2,(1+e)/2,1],e)))
    for text in ['0','0.25','0.5','0.75','1']:
        gamma=mp.mpf(text);q=1-gamma;cases.append(('amplitude_damping',text,mp.sqrt(q)*L+q*N,gamma*u3,None,([0,0,gamma,2-gamma],[-q,q,1,1],q)))
    for text in ['0.25','0.5','1']:
        a=mp.mpf(text);cases.append(('depolarizing',text,a*(L+N),zero,None,([(1-a)/2]*3+[(1+3*a)/2],[(1-3*a)/2]+[(1+a)/2]*3,a)))
    rows=[];valids=[];bounds=[];errors=[];densities=[];archive_errors=[];formula_errors=[]
    for family,label,T,t,archive,expected in cases:
        row,valid,bound,error,ds,e,g=evaluate(T,t,family,label);valids.append(valid);bounds.append(bound);errors.append(error);densities.extend(ds)
        if archive is not None:
            er=max(V88.spectrum_error(e,[mp.mpf(x) for x in archive['choi_eigenvalues']]),V88.spectrum_error(g,[mp.mpf(x) for x in archive['partial_transpose_eigenvalues']]),abs(mp.mpf(row['normalized_choi_negativity'])-mp.mpf(archive['normalized_choi_negativity'])))
            archive_errors.append(er);row['archive_error']=num(er)
        if expected is not None:
            je,ge,delta=expected;er=max(V88.spectrum_error(e,je),V88.spectrum_error(g,ge),abs(mp.mpf(row['minimum_singular_value'])-delta))
            formula_errors.append(er);row['spectrum_delta_formula_error']=num(er)
        if family=='depolarizing':row['negativity_formula_error']=num(abs(mp.mpf(row['normalized_choi_negativity'])-max(0,(3*mp.mpf(label)-1)/4)))
        rows.append(row)
    symbolic=symbolic_certificate()
    valid=(parents and symbolic['valid'] and len(rows)==25 and all(valids) and parent_error<=mp.mpf('1e-60') and
           max(archive_errors)<=mp.mpf('1e-60') and max(formula_errors+[frame_error])<=mp.mpf('1e-45'))
    bound=all(bounds)
    equality=[r for r in rows if r['family'] in ['saturation','amplitude_damping']];dep=[r for r in rows if r['family']=='depolarizing']
    sharp=(len(equality)==12 and max(mp.mpf(r['attainment_error']) for r in equality)<=mp.mpf('1e-45') and
           max(mp.mpf(r['negativity_formula_error']) for r in dep)<=mp.mpf('1e-45') and
           all(mp.mpf(r['bound_slack'])>=mp.mpf('1e-4') for r in dep if r['label'] in ['0.25','0.5']))
    verdict,sv=adjudicate(valid,bound,sharp)
    report={'version':'15.89','precision_digits':80,'candidate_index':46,'parent_hashes':{'v15.83':HASH83,'v15.88':HASH88},
            'all_valid':bool(valid),'bound_predicate':bool(bound),'sharpness_predicate':bool(sharp),'verdict':verdict,'sharpness_verdict':sv,
            'controls':{'parents_valid':bool(parents),'symbolic_certificate':symbolic,'parent_error':num(parent_error),'frame_error':num(frame_error),
                        'max_archive_error':num(max(archive_errors)),'max_spectrum_delta_formula_error':num(max(formula_errors)),
                        'max_affine_comparison_error':num(max(errors)),'minimum_state_eigenvalue':num(min(d['minimum_eigenvalue'] for d in densities)),
                        'max_state_trace_error':num(max(d['trace'] for d in densities)),'max_state_hermiticity_error':num(max(d['hermiticity'] for d in densities))},
            'rows':rows,'scope':'Sharp normalized Choi-negativity bound for qubit CPTP maps; not quantum capacity or physical source-law selection.',
            'sources':['https://arxiv.org/abs/1304.6775']}
    def finite(a):
        if isinstance(a,dict):return all(finite(v) for v in a.values())
        if isinstance(a,list):return all(finite(v) for v in a)
        if isinstance(a,str):return a.lower() not in ['nan','inf','+inf','-inf']
        return True
    if not finite(report):report['all_valid']=False;report['verdict']='INVALID';report['sharpness_verdict']='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
