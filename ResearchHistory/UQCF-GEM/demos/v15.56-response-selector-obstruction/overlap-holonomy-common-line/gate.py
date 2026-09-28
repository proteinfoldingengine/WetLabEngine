"""v15.96: two retained triangles, separable preparation and common invariant lines."""
import functools
import gzip
import hashlib
import importlib.util
import itertools
import json
import pathlib
import sys
import numpy as np
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('holonomy95_overlap',HERE.parent/'compatible-holonomy-reduction'/'gate.py')
V95=importlib.util.module_from_spec(spec);spec.loader.exec_module(V95)
V93=V95.V93;V92=V93.V92;V81=V93.V81;V75=V93.V75;M=V93.M
THRESHOLDS=[1e-9,1e-10,1e-11];LAMBDAS=[-1.,0.,1.];U_SOURCE=.1
EXPECTED=[13,16,22,25,27,29,37,39,46,50,66,77]
EDGES=[(0,1),(1,2),(2,0),(1,3),(3,0),(2,3)]
QUATS=[(1,2,3,4),(2,-1,3,1),(3,2,-1,2),(1,-2,1,3)]
CODE_HASH='c38eba50e1d99e01026cb956fd308f750b48b9932422ca100966c16a70a5251a'
GZIP_HASH='f05a0ebc7d41128d8b2be4fd46161d7827f623d6107da8b3dd2c4585cb95561f'
JSON_HASH='ee9b13d07c3856357b157fdcf58854957fe56767ee55eeba61266b34ee40e607'
LOCAL_HASH='7d65d2525353ec83426694e5375881740031c33d2bb02ea38aec4737ac052ec9'


def tensor(items):return functools.reduce(np.kron,items)


def swap_matrix():
    s=np.zeros((16,16))
    for k in range(16):
        bits=[(k>>p)&1 for p in [3,2,1,0]];bits[2],bits[3]=bits[3],bits[2]
        target=sum(b*2**(3-i) for i,b in enumerate(bits));s[target,k]=1
    return s


def exact_basis():
    out=[sp.diag(1,-1,0)/sp.sqrt(2),sp.diag(1,1,-2)/sp.sqrt(6)]
    for i,j in [(0,1),(0,2),(1,2)]:
        a=sp.zeros(3);a[i,j]=a[j,i]=1;out.append(a/sp.sqrt(2))
    return out

S_BASIS=np.array([np.array(s.tolist(),float) for s in exact_basis()])
PAULI=[np.eye(2),*M.PAULI];LABELS=list(itertools.product(range(4),repeat=4))
BASIS=np.array([tensor([PAULI[k] for k in label])/4 for label in LABELS])

def op(site,a,other=None,b=None):
    labs=[0]*4;labs[site]=a
    if other is not None:labs[other]=b
    return tensor([PAULI[k] for k in labs])
ONE=np.array([[op(i,a) for a in [1,2,3]] for i in range(4)])
PAIR=np.array([[[op(i,a,j,b) for b in [1,2,3]] for a in [1,2,3]] for i,j in EDGES])


def correlations(rho):
    one=np.einsum('ij,naji->na',rho,ONE).real;pair=np.einsum('ij,eabji->eab',rho,PAIR).real
    return np.array([pair[e]-np.outer(one[i],one[j]) for e,(i,j) in enumerate(EDGES)])


def partial_trace(rho,keep):
    n=int(round(np.log2(rho.shape[0])));a=rho.reshape([2]*(2*n))
    for q in reversed(range(n)):
        if q not in keep:a=np.trace(a,axis1=q,axis2=q+n);n-=1
    d=2**len(keep);return a.reshape(d,d)


def exact_frames():
    X=sp.Matrix([[0,1],[1,0]]);Y=sp.Matrix([[0,-sp.I],[sp.I,0]]);Z=sp.diag(1,-1);ps=[X,Y,Z];out=[]
    for w,x,y,z in QUATS:
        n=w*w+x*x+y*y+z*z
        g=sp.Matrix([[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]])/n
        u=(w*sp.eye(2)-sp.I*(x*X+y*Y+z*Z))/sp.sqrt(n);out.append((g,u))
    return ps,out


def representation(h):
    transformed=np.array([h@s@h.T for s in S_BASIS])
    return np.einsum('aij,bji->ab',S_BASIS,transformed)


def loop_diagnostic(h1,h2):
    d1,d2=representation(h1),representation(h2);B=np.vstack([d1-np.eye(5),d2-np.eye(5)]);sv=np.linalg.svd(B,compute_uv=False)
    cn=float(np.linalg.norm(h1@h2-h2@h1));gn=float(np.linalg.norm(h1@h2@h1.T@h2.T-np.eye(3)))
    residual=max(np.linalg.norm(h1.T@h1-np.eye(3)),np.linalg.norm(h2.T@h2-np.eye(3)),abs(np.linalg.det(h1)-1),abs(np.linalg.det(h2)-1),np.linalg.norm(d1.T@d1-np.eye(5)),np.linalg.norm(d2.T@d2-np.eye(5)),abs(cn-gn))
    ranks=[int(np.count_nonzero(sv>t)) for t in THRESHOLDS]
    return {'H1':h1.tolist(),'H2':h2.tolist(),'B':B.tolist(),'B_singular_values':sv.tolist(),'B_ranks':ranks,'kernel_dimensions':[5-r for r in ranks],'commutator_norm':cn,'group_commutator_distance':gn,'identity_residual':float(residual)}


@functools.lru_cache(maxsize=1)
def symbolic_certificate():
    checks={};zero=lambda a:all(sp.simplify(v)==0 for v in a);sb=exact_basis()
    rep=lambda h:sp.Matrix(5,5,lambda a,b:sp.trace(sb[a]*h*sb[b]*h.T))
    X=sp.Matrix([[1,0,0],[0,0,-1],[0,1,0]]);Z90=sp.Matrix([[0,-1,0],[1,0,0],[0,0,1]])
    Z=sp.Matrix([[sp.Rational(3,5),-sp.Rational(4,5),0],[sp.Rational(4,5),sp.Rational(3,5),0],[0,0,1]]);F=sp.diag(1,-1,-1);N=sp.diag(0,0,1)-sp.eye(3)/3
    checks['basis_orthonormal']=sp.Matrix(5,5,lambda a,b:sp.trace(sb[a]*sb[b]))==sp.eye(5)
    checks['representation_product']=zero(rep(X*Z90)-rep(X)*rep(Z90))
    checks['planar_fixed_tensor']=zero(Z*N*Z.T-N) and zero(F*N*F.T-N)
    checks['shared_line_rank']=sp.Matrix.vstack(rep(F)-sp.eye(5),rep(Z)-sp.eye(5)).rank()==4
    comm=F*Z-Z*F;checks['flip_commutator']=sp.trace(comm.T*comm)==sp.Rational(128,25)
    checks['no_common_line_rank']=sp.Matrix.vstack(rep(X)-sp.eye(5),rep(Z90)-sp.eye(5)).rank()==5
    ps,frames=exact_frames();g=frames[0][0];dg=rep(g)
    checks['representation_covariance']=all(zero(rep(g*h*g.T)-dg*rep(h)*dg.T) for h in [X,Z90])
    swap=sp.Matrix(swap_matrix().astype(int));checks['swap_unitary_involution']=swap.T*swap==sp.eye(16) and swap*swap==sp.eye(16)
    x=sp.Matrix(sp.symbols('x0:3',real=True));y=sp.Matrix(sp.symbols('y0:3',real=True))
    r=(sp.eye(2)+sum((x[i]*ps[i] for i in range(3)),sp.zeros(2)))/2;s=(sp.eye(2)+sum((y[i]*ps[i] for i in range(3)),sp.zeros(2)))/2
    pair=(sp.kronecker_product(r,sp.eye(2)/2)+sp.kronecker_product(sp.eye(2)/2,s))/2
    corr=sp.Matrix(3,3,lambda i,j:sp.expand(sp.trace(pair*sp.kronecker_product(ps[i],ps[j]))-sp.trace(pair*sp.kronecker_product(ps[i],sp.eye(2)))*sp.trace(pair*sp.kronecker_product(sp.eye(2),ps[j]))))
    checks['spectator_connected_identity']=zero(corr+x*y.T/4)
    for k,(g,u) in enumerate(frames):
        checks['frame_'+str(k)]=zero(g.T*g-sp.eye(3)) and g.det()==1 and zero(u.H*u-sp.eye(2)) and sp.simplify(u.det())==1 and all(zero(u*ps[j]*u.H-sum((g[i,j]*ps[i] for i in range(3)),sp.zeros(2))) for j in range(3))
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def post(zs,scale):
    coeff=np.einsum('hij,kji->hk',zs,BASIS,optimize=True)
    return np.einsum('hk,kij->hij',coeff*scale,BASIS,optimize=True)


def arms():
    _,local=V92.exact_arms();out={}
    for name in ['plane','isotropic']:
        T,_,effects,prepared=local[name];T=np.array(T.tolist(),float);es=[np.array(x.tolist(),complex) for x in effects];ps=[np.array(x.tolist(),complex) for x in prepared]
        choices=list(itertools.product(range(len(es)),repeat=4));E=np.array([tensor([es[k] for k in c]) for c in choices]);P=np.array([tensor([ps[k] for k in c]) for c in choices])
        factors=np.r_[1.,np.diag(T)];scale=np.array([np.prod(factors[list(label)]) for label in LABELS])
        out[name]={'T':T,'effects':E,'prepared':P,'scale':scale}
    return out


def choi_from_units(zs):return zs.reshape(16,16,16,16).transpose(0,2,1,3).reshape(256,256)


def cp16(zs):
    j=choi_from_units(zs);ev=np.linalg.eigvalsh((j+j.conj().T)/2);herm=float(np.linalg.norm(j-j.conj().T));tp=float(np.linalg.norm(np.trace(j.reshape(16,16,16,16),axis1=1,axis2=3)-np.eye(16)))
    return {'min_eigenvalue':float(ev.min()),'hermiticity_error':herm,'TP_error':tp,'valid':bool(ev.min()>=-1e-12 and herm<=1e-12 and tp<=1e-12)}


def geometry(cs,source_cs,name):
    edges=[];rs=[];domain=True;residual=0.
    for c,source in zip(cs[:5],source_cs[:5]):
        u,s,vh=np.linalg.svd(c);ref=float(np.linalg.svd(source,compute_uv=False)[0]);ranks=[int(np.count_nonzero(s>t*ref)) for t in THRESHOLDS];det=float(np.linalg.det(u@vh));inside=ranks==([2]*3 if name=='plane' else [3]*3) and (name=='plane' or det>0)
        edge={'C':c.tolist(),'source_C':source.tolist(),'singular_values':s.tolist(),'reference':ref,'ranks':ranks,'full_polar_determinant':det,'domain':bool(inside),'R':None};domain=domain and inside
        if inside:
            r=V93.oriented(c)[0] if name=='plane' else u@vh;p=r.T@c;residual=max(residual,np.linalg.norm(r.T@r-np.eye(3)),abs(np.linalg.det(r)-1),np.linalg.norm(r@p-c),np.linalg.norm(p-p.T),max(0.,-np.linalg.eigvalsh((p+p.T)/2).min()));rs.append(r);edge['R']=r.tolist()
        edges.append(edge)
    geom=None
    if domain:
        h1=rs[0]@rs[1]@rs[2];h2=rs[0]@rs[3]@rs[4];geom=loop_diagnostic(h1,h2);residual=max(residual,geom['identity_residual'])
    return {'domain':bool(domain),'edges':edges,'geometry':geom,'residual':float(residual)}


def adjudicate(valid,full,plane):
    if not valid:return 'INVALID','INVALID'
    return ('OVERLAP_COMMON_LINE_OBSTRUCTION_CONFIRMED' if full else 'OVERLAP_COMMON_LINE_OBSTRUCTION_NOT_CONFIRMED',
            'PLANAR_COMMON_LINE_PRESERVED' if plane else 'PLANAR_COMMON_LINE_PRESERVATION_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    folder=HERE.parent/'compatible-holonomy-reduction';code=(folder/'gate.py').read_bytes();gz=(folder/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz);parent=json.loads(raw)
    localcode=(HERE.parent/'preparation-span-obstruction'/'gate.py').read_bytes()
    parents=(hashlib.sha256(code).hexdigest()==CODE_HASH and hashlib.sha256(gz).hexdigest()==GZIP_HASH and hashlib.sha256(raw).hexdigest()==JSON_HASH and hashlib.sha256(localcode).hexdigest()==LOCAL_HASH and parent['all_valid'] and parent['verdict']=='FIXED_SUPPORT_HOLONOMY_REDUCTION_CONFIRMED' and parent['response_verdict']=='PLANAR_LOOP_RESPONSE_CONFIRMED')
    selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected];swap=swap_matrix();armdata=arms();units=np.eye(256,dtype=complex).reshape(256,16,16)
    keys=['effect_completeness','effect_hermiticity','unit_reconstruction','center_reconstruction','probability_imaginary','probability_sum','overlap','regional_correlation','spectator_marginal','spectator_formula','connected_affine','geometry','covariance','planar_normal']
    controls={k:0. for k in keys}
    def mx(k,v):controls[k]=max(controls[k],float(v))
    def marginals(z):
        a=partial_trace(z,[0,1,2]);b=partial_trace(z,[0,1,3]);common=partial_trace(z,[0,1]);direct=correlations(z)
        mx('overlap',max(np.linalg.norm(partial_trace(a,[0,1])-common),np.linalg.norm(partial_trace(b,[0,1])-common)))
        mx('regional_correlation',max(np.max(np.abs(np.array(M.correlations(a))-direct[[0,1,2]])),np.max(np.abs(np.array(M.correlations(b))-direct[[0,3,4]]))))
    prep_diags=[];effect_min=1.;prob_min=1.;prepared_valid=True
    for name,a in armdata.items():
        es=a['effects'];ps=a['prepared'];pd=V75.density_diagnostics(ps);prepared_valid=prepared_valid and pd['valid'];prep_diags.append({'arm':name,'outcomes':len(ps),**pd})
        mx('effect_completeness',np.linalg.norm(es.sum(axis=0)-np.eye(16)));mx('effect_hermiticity',np.max(np.linalg.norm(es-es.conj().transpose(0,2,1),axis=(1,2))))
        effect_min=min(effect_min,float(np.linalg.eigvalsh(es).min()))
        w=np.einsum('hij,kji->hk',units,es,optimize=True);rebuilt=np.einsum('hk,kij->hij',w,ps,optimize=True)
        mx('unit_reconstruction',np.max(np.abs(rebuilt-post(units,a['scale']))))
    unitaries=np.array([np.kron(u,np.eye(2)) for u in V81.UNITARIES])
    def source(zs,lam):return sum(w*(u@zs@u.conj().T) for w,u in zip(V81.weights(lam,U_SOURCE),unitaries))
    channels=[]
    for lam in LAMBDAS:
        sourceunits=source(units,lam);channels.append({'lambda':lam,'arm':'source',**cp16(sourceunits)})
        for name,a in armdata.items():channels.append({'lambda':lam,'arm':name,**cp16(post(sourceunits,a['scale']))})
    _,fr=exact_frames();gs=[np.array(g.tolist(),float) for g,u in fr];us=[np.array(u.tolist(),complex) for g,u in fr];bigU=tensor(us)
    inputs=[];centers=[];outputs=[];input_records=[];rows=[];full=True;plane=True
    N=np.diag([0.,0.,1.])-np.eye(3)/3
    for k,rec in enumerate(selected):
        following=selected[(k+1)%12];a=np.kron(rec['rho'],np.eye(2)/2);b=np.kron(following['rho'],np.eye(2)/2);rho=(a+swap@b@swap.T)/2;inputs.append(rho);marginals(rho)
        input_records.append({'candidate_index':rec['candidate_index'],'successor_index':following['candidate_index'],'state_hex':[[[float(v.real).hex(),float(v.imag).hex()] for v in row] for row in rho]})
        rlast=M.moments(rec['rho'],M.ONE).reshape(3,3)[2];slast=M.moments(following['rho'],M.ONE).reshape(3,3)[2];spectator=-np.outer(rlast,slast)/4
        for lam in LAMBDAS:
            center=source(rho[None],lam)[0];centers.append(center);marginals(center);sc=correlations(center)
            mx('spectator_marginal',np.linalg.norm(partial_trace(center,[2,3])-partial_trace(rho,[2,3])));mx('spectator_formula',np.linalg.norm(sc[5]-spectator))
            for name,a in armdata.items():
                out=post(center[None],a['scale'])[0];outputs.append(out);marginals(out);cs=correlations(out);T=a['T'];formula=np.array([T@c@T.T for c in sc]);mx('connected_affine',np.max(np.abs(cs-formula)))
                probs=np.einsum('ij,kji->k',center,a['effects'],optimize=True);rebuilt=np.einsum('k,kij->ij',probs,a['prepared'],optimize=True)
                mx('center_reconstruction',np.max(np.abs(out-rebuilt)));mx('probability_imaginary',np.max(np.abs(probs.imag)));mx('probability_sum',abs(probs.sum()-1));prob_min=min(prob_min,float(probs.real.min()))
                geom=geometry(cs,sc,name);mx('geometry',geom['residual'])
                rotated=bigU@out@bigU.conj().T;cc=correlations(rotated);expected_cc=np.array([gs[i]@c@gs[j].T for c,(i,j) in zip(cs,EDGES)]);mx('covariance',np.max(np.abs(cc-expected_cc)))
                rotated_source=np.array([gs[i]@c@gs[j].T for c,(i,j) in zip(sc,EDGES)]);gc=geometry(cc,rotated_source,name);mx('geometry',gc['residual'])
                row={'candidate_index':rec['candidate_index'],'successor_index':following['candidate_index'],'lambda':lam,'arm':name,'domain':geom['domain'],'transformed_domain':gc['domain'],'edges':geom['edges'],'geometry':geom['geometry'],'transformed_geometry':gc['geometry'],'probabilities':probs.real.tolist(),
                     'spectator_edge':{'edge':[2,3],'source_C':sc[5].tolist(),'C':cs[5].tolist(),'singular_values':np.linalg.svd(cs[5],compute_uv=False).tolist(),'ranks':[int(np.count_nonzero(np.linalg.svd(cs[5],compute_uv=False)>t)) for t in THRESHOLDS],'reference':1.}}
                if geom['domain'] and gc['domain']:
                    base=geom['geometry'];rot=gc['geometry'];g0=gs[0]
                    for key in ['H1','H2']:mx('covariance',np.linalg.norm(np.array(rot[key])-g0@np.array(base[key])@g0.T))
                    for e,(i,j) in enumerate(EDGES[:5]):mx('covariance',np.linalg.norm(np.array(gc['edges'][e]['R'])-gs[i]@np.array(geom['edges'][e]['R'])@gs[j].T))
                    mx('covariance',max(np.linalg.norm(np.array(rot['B_singular_values'])-base['B_singular_values']),abs(rot['commutator_norm']-base['commutator_norm']),abs(rot['group_commutator_distance']-base['group_commutator_distance'])))
                if name=='isotropic':
                    ok=geom['domain'] and gc['domain'] and geom['geometry']['B_ranks']==[5]*3 and gc['geometry']['B_ranks']==[5]*3;full=full and ok
                else:
                    for candidate,normaltensor in [(geom,N),(gc,gs[0]@N@gs[0].T)]:
                        if candidate['domain']:
                            for key in ['H1','H2']:
                                h=np.array(candidate['geometry'][key]);mx('planar_normal',np.linalg.norm(h@normaltensor@h.T-normaltensor))
                    ok=geom['domain'] and gc['domain'] and all(r<=4 for r in geom['geometry']['B_ranks']+gc['geometry']['B_ranks']);plane=plane and ok
                row['scientific_pass']=bool(ok);rows.append(row)
    X=np.array([[1.,0,0],[0,0,-1],[0,1,0]]);Z90=np.array([[0.,-1,0],[1,0,0],[0,0,1.]]);Z=np.array([[.6,-.8,0],[.8,.6,0],[0,0,1.]]);F=np.diag([1.,-1.,-1.])
    nc={'shared_line_noncommuting':loop_diagnostic(F,Z),'no_common_line':loop_diagnostic(X,Z90)};numeric_valid=nc['shared_line_noncommuting']['B_ranks']==[4]*3 and nc['no_common_line']['B_ranks']==[5]*3 and abs(nc['shared_line_noncommuting']['commutator_norm']**2-128/25)<=1e-9 and all(x['identity_residual']<=1e-9 for x in nc.values())
    symbolic=symbolic_certificate();inherited=V92.symbolic_certificate();ip=V75.density_diagnostics(inputs);cp=V75.density_diagnostics(centers);opd=V75.density_diagnostics(outputs)
    valid=bool(parents and indices==EXPECTED and len(rows)==72 and len(channels)==9 and symbolic['valid'] and inherited['valid'] and numeric_valid and prepared_valid and ip['valid'] and cp['valid'] and opd['valid'] and effect_min>=-1e-12 and prob_min>=-1e-12 and all(c['valid'] for c in channels) and all(v<=(1e-9 if key in ['geometry','covariance','planar_normal'] else 1e-12) for key,v in controls.items()))
    controls.update(parents_valid=bool(parents),symbolic_certificate=symbolic,inherited_certificate=inherited,preparations=prep_diags,minimum_effect_eigenvalue=effect_min,minimum_probability=prob_min,input_physicality=ip,source_physicality=cp,output_physicality=opd,numerical_controls_valid=bool(numeric_valid))
    verdict,pv=adjudicate(valid,full,plane)
    report={'version':'15.96','all_valid':valid,'verdict':verdict,'planar_verdict':pv,'fullspan_predicate':bool(full),'planar_predicate':bool(plane),'candidate_indices':indices,'controls':controls,'numerical_controls':nc,'channels':channels,'input_states':input_records,'rows':rows,
            'scope':'No common invariant line for two loops is not continuous SO(3) holonomy. Five-edge overlapping-region atlas, deterministic constructed ensemble, fully separable preparation outputs, baseline geometry not causal source derivative.'}
    def finite(x):
        if isinstance(x,dict):return all(finite(v) for v in x.values())
        if isinstance(x,list):return all(finite(v) for v in x)
        if isinstance(x,(int,float)):return bool(np.isfinite(x))
        return True
    if not finite(report):report['all_valid']=False;report['verdict']=report['planar_verdict']='INVALID'
    return report

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False));sys.exit(0 if result['all_valid'] else 2)
