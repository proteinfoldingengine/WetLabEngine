"""v15.95: fixed-support loop reduction and predicted edge-to-loop aggregation."""
import functools
import gzip
import hashlib
import importlib.util
import json
import pathlib
import sys
import numpy as np
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('composition94_holonomy',HERE.parent/'oriented-composition-compatibility'/'gate.py')
V94=importlib.util.module_from_spec(spec);spec.loader.exec_module(V94)
V93=V94.V93;V81=V93.V81;THRESHOLDS=[1e-9,1e-10,1e-11];RUNGS=[1e-3,1e-4,1e-5]
PINS={
'oriented-composition-compatibility':('a62df70edfef9f30563d4dd89681508d5c35e577a7d26bb1d59b798e74e634a1','627e9ac50b1ead13f76036965f020db19c85f5287f669e9a23f1a589118cc04a','7c9fc2bf42316e366d059e7b45d2aa8ebdeb11947a5b7593c4808de608a8e6b4'),
'oriented-rank-two-response':('e12b740453761330add8f8d9694befa242e6b5c24bc9c6b49870d648b5c8725c','4c3e4d893c69f1a72a5409f905a1eafa81d4a0295b10439a0643ed21ba1dcc09','540f46f32bf8f74ad2c4283870d14f36427b16d0155444546e7113cedd26cd2a')}


def loop_tangent(rs,ws):
    """ws has shape (edge, direction, 3, 3); no axis projection is performed."""
    a,b,c=rs;h=a@b@c
    dh=np.array([(a@ws[0,k])@b@c+a@(b@ws[1,k])@c+a@b@(c@ws[2,k]) for k in range(ws.shape[1])])
    omega=np.array([h.T@d for d in dh]);axial=np.column_stack([V93.coords(w) for w in omega])
    return h,dh,omega,axial


@functools.lru_cache(maxsize=1)
def symbolic_certificate():
    zero=lambda a:all(sp.simplify(x)==0 for x in a);checks={};P=sp.diag(1,1,0);F=sp.diag(1,-1,-1);n=sp.Matrix([0,0,1]);J=sp.Matrix([[0,-1,0],[1,0,0],[0,0,0]])
    def z(t):
        c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
        return sp.Matrix([[c,-s,0],[s,c,0],[0,0,1]])
    t,u=sp.symbols('t u',real=True);Z=z(t);ZF=Z*F
    checks['embedded_O2_proper']=all(zero(R.T*R-sp.eye(3)) and sp.simplify(R.det())==1 for R in [Z,ZF])
    checks['normal_sign_actions']=zero(Z*n-n) and zero(ZF*n+n)
    checks['plane_parallel']=all(zero(R*P*R.T-P) for R in [Z,ZF])
    checks['flip_conjugation']=zero(F*Z*F-Z.T)
    comm=(F*Z-Z*F).subs(t,sp.Rational(1,2));checks['flip_noncommutation']=sp.trace(comm.T*comm)==sp.Rational(128,25)
    x,y,w=sp.symbols('x y w',real=True);skew=sp.Matrix([[0,-w,y],[w,0,-x],[-y,x,0]])
    lin=sp.Matrix(list(skew*P-P*skew)).jacobian([x,y,w]);checks['fixed_plane_lie_kernel']=lin.rank()==2 and lin.nullspace()==[sp.Matrix([0,0,1])]
    checks['continuous_rotations_commute']=zero(Z*z(u)-z(u)*Z)
    ts=sp.symbols('t0:3',real=True);vel=sp.symbols('w0:3',real=True);rs=[z(q) for q in ts];a,b,c=rs;H=a*b*c
    dH=(a*vel[0]*J)*b*c+a*(b*vel[1]*J)*c+a*b*(c*vel[2]*J)
    checks['loop_derivative_sum']=zero(H.T*dH-sum(vel)*J)
    checks['fixed_plane_response_rank']=sp.Matrix([0,0,sum(vel)]).jacobian(vel).rank()==1
    checks['unrestricted_response_rank']=sp.Matrix([skew[2,1],skew[0,2],skew[1,0]]).jacobian([x,y,w]).rank()==3
    for i,g in enumerate(V93.exact_frames()):checks['frame_'+str(i)]=zero(g.T*g-sp.eye(3)) and g.det()==1
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def numerical_controls():
    J=np.array([[[0,0,0],[0,0,-1],[0,1,0]],[[0,0,1],[0,0,0],[-1,0,0]],[[0,-1,0],[1,0,0],[0,0,0]]],float)
    ws=np.zeros((3,3,3,3));ws[0]=J;h,dh,omega,k=loop_tangent(np.array([np.eye(3)]*3),ws)
    error=float(np.linalg.norm(k-np.eye(3)));rank=V81.describe(k,1.)['ranks']
    F=np.diag([1.,-1.,-1.]);Z=np.array([[.6,-.8,0],[.8,.6,0],[0,0,1.]])
    value=float(np.linalg.norm(F@Z-Z@F)**2);P=np.diag([1.,1.,0.]);pres=float(max(np.linalg.norm(R@P@R.T-P) for R in [F,Z]))
    return {'unrestricted_error':error,'unrestricted_ranks':rank,'flip_commutator_squared':value,'plane_preservation':pres,'valid':bool(error<=1e-9 and rank==[3]*3 and abs(value-128/25)<=1e-9 and pres<=1e-9)}


def adjudicate(valid,reduction,response):
    if not valid:return 'INVALID','INVALID'
    return ('FIXED_SUPPORT_HOLONOMY_REDUCTION_CONFIRMED' if reduction else 'FIXED_SUPPORT_HOLONOMY_REDUCTION_NOT_CONFIRMED',
            'PLANAR_LOOP_RESPONSE_CONFIRMED' if response else 'PLANAR_LOOP_RESPONSE_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    parents={};pins=True
    for name,expected in PINS.items():
        folder=HERE.parent/name;code=(folder/'gate.py').read_bytes();gz=(folder/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz)
        pins=pins and tuple(hashlib.sha256(b).hexdigest() for b in [code,gz,raw])==expected;parents[name]=json.loads(raw)
    p94=parents['oriented-composition-compatibility'];p93=parents['oriented-rank-two-response']
    pv=(p94['all_valid'] and p94['verdict']=='ORIENTED_COMPOSITION_OBSTRUCTED' and p94['matched_verdict']=='MATCHED_SUPPORT_COMPOSITION_CONFIRMED' and p93['all_valid'] and p93['verdict']=='ORIENTED_RANK_TWO_READOUT_CONFIRMED' and p93['response_verdict']=='PLANAR_ORIENTED_RESPONSE_CONFIRMED')
    expected=[13,16,22,25,27,29,37,39,46,50,66,77];indices=all([r['candidate_index'] for r in p93['rows'] if r['lambda']==lam]==expected for lam in [-1,0,1])
    saved={(r['candidate_index'],r['lambda']):r for r in p94['planar_rows']};frames=[np.array(g.tolist(),float) for g in V93.exact_frames()]
    controls={k:0. for k in ['archived_R','archived_W','archived_edge_map','support','normal_sector','parent_triple','product_rule','skew','confinement','sum_aggregation','covariance','finite_difference_final']}
    def mx(k,v):controls[k]=max(controls[k],float(v))
    rel=lambda a,b:float(np.linalg.norm(a-b)/max(1.,np.linalg.norm(b)))
    rows=[];domain_all=True;reduction=True;response=True;n=np.array([0.,0.,1.])
    for old in p93['rows']:
        cs=np.array([e['C'] for e in old['edges']]);ds=np.array([e['delta_C'] for e in old['edges']]);vs=np.array([e['V'] for e in old['edges']]);ps=np.array([v@v.T for v in vs]);ss=[np.linalg.svd(c,compute_uv=False) for c in cs]
        ranks=[[int(np.count_nonzero(s>t*e['rank_reference'])) for t in THRESHOLDS] for s,e in zip(ss,old['edges'])];domain=all(k==[2]*3 for k in ranks);domain_all=domain_all and domain
        row={'candidate_index':old['candidate_index'],'lambda':old['lambda'],'input_ranks':ranks,'domain':domain,'K':None}
        if not domain:rows.append(row);reduction=False;response=False;continue
        rs=[];ws=[];rcs=[];wcs=[];pcs=[];signs=[]
        for e,(c,delta) in enumerate(zip(cs,ds)):
            r,p,v=V93.oriented(c);w=np.array([V93.tangent(r,p,d)[1] for d in delta]);rs.append(r);ws.append(w)
            mx('archived_R',np.linalg.norm(r-np.array(old['edges'][e]['R'])));mx('archived_W',rel(w,np.array(old['edges'][e]['W'])))
            j=(e+1)%3;mx('support',max(np.linalg.norm(vs[e].T@vs[e]-ps[j]),np.linalg.norm(r@ps[j]@r.T-ps[e])))
            signs.append(float(n@r@n));mx('normal_sector',np.linalg.norm(r@n-n))
            gi,gj=frames[e],frames[j];rc,pc,vc=V93.oriented(gi@c@gj.T);wc=np.array([V93.tangent(rc,pc,gi@d@gj.T)[1] for d in delta]);rcs.append(rc);wcs.append(wc);pcs.append(vc@vc.T)
            mx('covariance',max(rel(rc,gi@r@gj.T),rel(wc,np.array([gj@x@gj.T for x in w])),np.linalg.norm(pcs[-1]-gi@ps[e]@gi.T)))
        rs=np.array(rs);ws=np.array(ws);emap=np.vstack([np.column_stack([V93.coords(w) for w in edge]) for edge in ws]);mx('archived_edge_map',rel(emap,np.array(old['E_map'])))
        H,dh,omega,k=loop_tangent(rs,ws);Hc,dhc,oc,kc=loop_tangent(np.array(rcs),np.array(wcs));p0=ps[0];g0=frames[0]
        mx('parent_triple',np.linalg.norm(H-np.array(saved[old['candidate_index'],old['lambda']]['triple']['completion'])))
        b,c=rs[1:];bc=b@c;ind=np.array([bc.T@ws[0,h]@bc+c.T@ws[1,h]@c+ws[2,h] for h in range(27)])
        mx('product_rule',rel(omega,ind));mx('skew',max(np.linalg.norm(w+w.T) for w in omega));mx('support',np.linalg.norm(H@p0@H.T-p0))
        mx('confinement',max(np.linalg.norm(p0@k),max(np.linalg.norm(w@p0-p0@w) for w in omega)))
        archived=np.array(old['E_map']);summed=archived[:3]+archived[3:6]+archived[6:9];mx('sum_aggregation',rel(k,summed))
        mx('covariance',max(rel(Hc,g0@H@g0.T),rel(oc,np.array([g0@w@g0.T for w in omega])),rel(kc,g0@k),np.linalg.norm(pcs[0]@kc)))
        errors=[];steps=[]
        for h in range(27):
            epsilons=[b*min(s[1] for s in ss)/max(1.,max(np.linalg.norm(ds[e,h]) for e in range(3))) for b in RUNGS];err=[]
            for eps in epsilons:
                plus=[V93.oriented(cs[e]+eps*ds[e,h])[0] for e in range(3)];minus=[V93.oriented(cs[e]-eps*ds[e,h])[0] for e in range(3)]
                hp=plus[0]@plus[1]@plus[2];hm=minus[0]@minus[1]@minus[2];err.append(rel((hp-hm)/(2*eps),dh[h]))
            mx('finite_difference_final',err[-1]);steps.append(epsilons);errors.append(err)
        kd=V81.describe(k,max(1.,old['E']['reference']));reduced=all(rank<=1 for rank in kd['ranks']);target=[0]*3 if old['lambda']==0 else [1]*3;passed=kd['ranks']==target
        if old['lambda']==0:passed=passed and kd['norm']<=1e-12
        reduction=reduction and reduced;response=response and passed
        row.update(H=H.tolist(),delta_H=dh.tolist(),Omega=omega.tolist(),K_map=k.tolist(),K=kd,edge_E=old['E'],support_projectors=ps.tolist(),edge_normal_signs=signs,normal_sign=float(np.trace((np.eye(3)-p0)@H)),holonomy_distance_from_identity=float(np.linalg.norm(H-np.eye(3))),finite_difference_steps=steps,finite_difference_errors=errors,reduction_pass=bool(reduced),response_pass=bool(passed));rows.append(row)
    symbolic=symbolic_certificate();numeric=numerical_controls()
    valid=bool(pins and pv and indices and len(rows)==36 and domain_all and symbolic['valid'] and numeric['valid'] and all(value<=(1e-6 if key=='finite_difference_final' else 1e-9) for key,value in controls.items()))
    controls.update(parent_hashes_valid=bool(pins),parent_verdicts_valid=bool(pv),candidate_indices_valid=bool(indices),input_domain_valid=bool(domain_all),symbolic_certificate=symbolic)
    verdict,rv=adjudicate(valid,reduction,response)
    report={'version':'15.95','all_valid':valid,'verdict':verdict,'response_verdict':rv,'reduction_predicate':bool(reduction),'response_predicate':bool(response),'controls':controls,'numerical_controls':numeric,'rows':rows,
            'scope':'Predicted fixed-support aggregation on one triangle, with embedded O(2) stabilizer and SO(2) identity component. No moving-support tangent bound, global gauge measurement or physical source selection.'}
    def finite(x):
        if isinstance(x,dict):return all(finite(v) for v in x.values())
        if isinstance(x,list):return all(finite(v) for v in x)
        if isinstance(x,(int,float)):return bool(np.isfinite(x))
        return True
    if not finite(report):report['all_valid']=False;report['verdict']=report['response_verdict']='INVALID'
    return report

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False));sys.exit(0 if result['all_valid'] else 2)
