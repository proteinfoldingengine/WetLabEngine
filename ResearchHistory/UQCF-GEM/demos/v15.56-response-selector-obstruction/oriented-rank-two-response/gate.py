"""v15.93: oriented rank-two readout, independent planar derivative controls."""
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
spec=importlib.util.spec_from_file_location('span92_oriented',HERE.parent/'preparation-span-obstruction'/'gate.py')
V92=importlib.util.module_from_spec(spec);spec.loader.exec_module(V92)
V81=V92.V81;V75=V92.V75;M=V92.M
THRESHOLDS=[1e-9,1e-10,1e-11];LAMBDAS=[-1.,0.,1.];U=.1;ETA=1e-4;FD_RUNGS=[1e-3,1e-4,1e-5]
QUATERNIONS=[(1,2,3,4),(2,-1,3,1),(3,2,-1,2)]
CODE_HASH='7d65d2525353ec83426694e5375881740031c33d2bb02ea38aec4737ac052ec9'
GZIP_HASH='ea33a8cd3dbbea12bffd13e5af1a5eecd61e235ee7617d056058b95cf4f72a7f'
JSON_HASH='bd2749b7f7b1afd836074890bf66f49ba96faa20353615b741fb2bd6cac1b30a'


def cofactor(a):
    return np.column_stack([np.cross(a[:,1],a[:,2]),np.cross(a[:,2],a[:,0]),np.cross(a[:,0],a[:,1])])


def oriented(c):
    """Caller establishes rank-two domain; fixed-rank support used for matrix probes."""
    u,s,vh=np.linalg.svd(c);v=u[:,:2]@vh[:2,:];r=v+cofactor(v)
    return r,r.T@c,v


def tangent(r,p,dc):
    q=r.T@dc-dc.T@r
    vals,v=np.linalg.eigh((p+p.T)/2);qq=v.T@q@v;ww=np.zeros((3,3))
    for i in range(3):
        for j in range(i+1,3):
            denom=vals[i]+vals[j]
            if denom<=0:raise ValueError('rank-two skew Sylvester denominator is nonpositive')
            ww[i,j]=qq[i,j]/denom;ww[j,i]=-ww[i,j]
    return q,v@ww@v.T


def coords(w):return np.array([w[2,1],w[0,2],w[1,0]])


def planar(c,dc):
    a,b=c[0,:2];cc,d=c[1,:2];da,db=dc[0,:2];dcc,dd=dc[1,:2]
    k=1. if a*d-b*cc>0 else -1.;x=a+k*d;y=cc-k*b;dx=da+k*dd;dy=dcc-k*db;n=np.hypot(x,y)
    r=np.zeros((3,3));r[:2,:2]=np.array([[x,-k*y],[y,k*x]])/n;r[2,2]=k
    angle=(x*dy-y*dx)/(x*x+y*y);w=np.zeros((3,3));w[1,0]=k*angle;w[0,1]=-k*angle
    return r,w,k


def exact_frames():
    out=[]
    for w,x,y,z in QUATERNIONS:
        n=w*w+x*x+y*y+z*z
        out.append(sp.Matrix([[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],
                              [2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],
                              [2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]])/n)
    return out


@functools.lru_cache(maxsize=1)
def symbolic_certificate():
    zero=lambda a:all(sp.simplify(v)==0 for v in a);checks={};v=sp.diag(1,1,0);r=v+v.cofactor_matrix()
    checks['rank_two_completion']=zero(r.T*r-sp.eye(3)) and r.det()==1 and zero(r*v-v)
    p1,p2=sp.symbols('p1 p2',positive=True);a,b,c=sp.symbols('a b c',real=True)
    skew=lambda x,y,z:sp.Matrix([[0,-z,y],[z,0,-x],[-y,x,0]])
    p=sp.diag(p1,p2,0);q=skew(a,b,c);w=skew(a/p2,b/p1,c/(p1+p2))
    checks['rank_two_sylvester']=zero(p*w+w*p-q)
    generic=skew(a,b,c);image=p*generic+generic*p
    operator=sp.Matrix([image[2,1],image[0,2],image[1,0]]).jacobian([a,b,c])
    checks['skew_operator_determinant']=sp.expand(operator.det()-p1*p2*(p1+p2))==0
    p0=sp.diag(1,0,0);alt=sp.Matrix([[1,0,0],[0,0,-1],[0,1,0]])
    checks['rank_one_identity_completion']=zero(sp.eye(3)*p0-p0)
    checks['rank_one_alternative_completion']=zero(alt.T*alt-sp.eye(3)) and alt.det()==1 and zero(alt*p0-p0) and not zero(alt-sp.eye(3))
    kernel=skew(1,0,0);checks['rank_one_skew_kernel']=zero(p0*kernel+kernel*p0) and not zero(kernel)
    frames=exact_frames()
    for i,A in enumerate(frames):checks['frame_'+str(i)]=zero(A.T*A-sp.eye(3)) and A.det()==1
    for e,(i,j) in enumerate(M.EDGES):
        A,B=frames[i],frames[j];checks['cofactor_covariance_'+str(e)]=zero((A*v*B.T).cofactor_matrix()-A*v.cofactor_matrix()*B.T)
    x,y,dx,dy=sp.symbols('x y dx dy',real=True);n=sp.sqrt(x*x+y*y)
    for k in [-1,1]:
        o=sp.Matrix([[x,-k*y],[y,k*x]])/n;do=o.diff(x)*dx+o.diff(y)*dy
        target=k*(x*dy-y*dx)/(x*x+y*y)*sp.Matrix([[0,-1],[1,0]])
        checks['planar_angle_'+str(k)]=zero(o.T*do-target)
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def connected_derivatives(rho,ys):
    one=M.moments(rho,M.ONE).reshape(3,3)
    done=np.einsum('hij,kji->hk',ys,np.array(M.ONE)).real.reshape(len(ys),3,3)
    pair=np.einsum('hij,kji->hk',ys,np.array(M.PAIR)).real.reshape(len(ys),3,3,3)
    return np.array([[pair[h,e]-np.outer(done[h,i],one[j])-np.outer(one[i],done[h,j]) for e,(i,j) in enumerate(M.EDGES)] for h in range(len(ys))])


def adjudicate(valid,domain,response):
    if not valid:return 'INVALID','INVALID'
    return ('ORIENTED_RANK_TWO_READOUT_CONFIRMED' if domain else 'ORIENTED_RANK_TWO_READOUT_NOT_CONFIRMED',
            'PLANAR_ORIENTED_RESPONSE_CONFIRMED' if domain and response else 'PLANAR_ORIENTED_RESPONSE_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    folder=HERE.parent/'preparation-span-obstruction';rawcode=(folder/'gate.py').read_bytes();gz=(folder/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz);parent=json.loads(raw)
    parents=(hashlib.sha256(rawcode).hexdigest()==CODE_HASH and hashlib.sha256(gz).hexdigest()==GZIP_HASH and hashlib.sha256(raw).hexdigest()==JSON_HASH and parent['all_valid'] and parent['verdict']=='PREPARATION_SPAN_GEOMETRY_OBSTRUCTION_CONFIRMED' and parent['noncommuting_verdict']=='NONCOMMUTING_PREPARATIONS_INSUFFICIENT_CONFIRMED')
    saved={(r['candidate_index'],r['lambda'],r['arm']):r for r in parent['rows']};selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
    hidden=np.array(M.HIDDEN);arm=V92.numeric_arms()['plane'];T=arm['T'];frames=[np.array(x.tolist(),float) for x in exact_frames()]
    limits={k:1e-12 for k in ['archive_center','derivative_identity','xy_support']}
    limits.update({k:1e-9 for k in ['completion','sylvester','skew','planar_comparison','covariance','inactive_response']});limits['finite_difference_final']=1e-6
    controls={k:0. for k in limits};mx=lambda k,v:controls.__setitem__(k,max(controls[k],float(v)))
    rel=lambda a,b:float(np.linalg.norm(a-b)/max(1.,np.linalg.norm(b)))
    channels=[];cache={};inputs=[];outputs=[];rows=[];domain_all=True;response_all=True
    for lam in LAMBDAS:
        ys=np.array([V81.channel(lam,U,h) for h in hidden]);outys=V92.apply_many(ys,arm['R']);cache[lam]=(ys,outys)
        channels.append({'lambda':lam,'arm':'source',**V75.cp_diagnostics(V75.choi(lambda z:V81.channel(lam,U,z)))})
        channels.append({'lambda':lam,'arm':'plane',**V75.cp_diagnostics(V75.choi(lambda z:V92.apply_many(V81.channel(lam,U,z)[None],arm['R'])[0]))})
    for rec in selected:
        rho=rec['rho'];candidate=rec['candidate_index'];inputs.extend([rho]+[rho+sign*ETA*h for h in hidden for sign in [-1,1]])
        for lam in LAMBDAS:
            center=V81.channel(lam,U,rho);ys,outys=cache[lam];out=V92.apply_many(center[None],arm['R'])[0]
            for state,tangents in [(center,ys),(out,outys)]:outputs.extend([state]+[state+sign*ETA*h for h in tangents for sign in [-1,1]])
            C=np.array(M.correlations(out));DC=connected_derivatives(out,outys);sourceDC=connected_derivatives(center,ys)
            old=saved[candidate,lam,'plane'];iso=saved[candidate,lam,'isotropic'];expected=np.array([e['correlation'] for e in old['edges']])
            mx('archive_center',np.max(np.abs(C-expected)));formula=np.array([[T@d@T.T for d in ds] for ds in sourceDC]);mx('derivative_identity',np.max(np.abs(DC-formula)))
            mask=np.ones((3,3));mask[:2,:2]=0;mx('xy_support',max(np.max(np.abs(C*mask)),np.max(np.abs(DC*mask))))
            edge_rows=[];qmap=np.zeros((9,27));emap=np.zeros((9,27));domain=True
            qref=max(1.,iso['Q']['reference']);eref=max(1.,iso['E']['reference'])
            for e,(i,j) in enumerate(M.EDGES):
                c=C[e];sv=np.linalg.svd(c,compute_uv=False);ref=old['edges'][e]['reference'];ranks=[int(np.count_nonzero(sv>t*ref)) for t in THRESHOLDS];inside=ranks==[2]*3
                edge={'edge':[i,j],'C':c.tolist(),'delta_C':DC[:,e].tolist(),'singular_values':sv.tolist(),'rank_reference':ref,'ranks':ranks,'domain':inside,'R':None,'P':None,'V':None,'W':None}
                domain=domain and inside
                if not inside:edge_rows.append(edge);continue
                r,p,v=oriented(c);pv=np.linalg.eigvalsh((p+p.T)/2)
                comp=max(np.linalg.norm(r.T@r-np.eye(3)),abs(np.linalg.det(r)-1),np.linalg.norm(r@p-c),np.linalg.norm(p-p.T),max(0.,-pv.min()),np.linalg.norm(r@(v.T@v)-v))
                mx('completion',comp);rp,_,sign=planar(c,np.zeros((3,3)));mx('planar_comparison',rel(r,rp))
                A,B=frames[i],frames[j];rc,pc,vc=oriented(A@c@B.T);mx('covariance',rel(rc,A@r@B.T))
                wlist=[];qlist=[];fd_errors=[];fd_steps=[];denoms=[float(pv[a]+pv[b]) for a in range(3) for b in range(a+1,3)]
                for h,dc in enumerate(DC[:,e]):
                    q,w=tangent(r,p,dc);dr=r@w;qlist.append(q);wlist.append(w);qmap[3*e:3*e+3,h]=coords(q);emap[3*e:3*e+3,h]=coords(w)
                    mx('sylvester',rel(p@w+w@p,q));mx('skew',np.linalg.norm(w+w.T));_,wp,_=planar(c,dc);mx('planar_comparison',rel(w,wp))
                    qc,wc=tangent(rc,pc,A@dc@B.T);mx('covariance',max(rel(wc,B@w@B.T),rel(rc@wc,A@dr@B.T)))
                    mx('inactive_response',np.linalg.norm(w*mask))
                    if e==0:mx('inactive_response',max(np.linalg.norm(w),np.linalg.norm(q)))
                    steps=[b*sv[1]/max(1.,np.linalg.norm(dc)) for b in FD_RUNGS];errs=[]
                    for eps in steps:
                        plus=oriented(c+eps*dc)[0];minus=oriented(c-eps*dc)[0];errs.append(rel((plus-minus)/(2*eps),dr))
                    mx('finite_difference_final',errs[-1]);fd_errors.append(errs);fd_steps.append(steps)
                edge.update(R=r.tolist(),P=p.tolist(),V=v.tolist(),P_eigenvalues=pv.tolist(),skew_sylvester_eigenvalues=denoms,planar_determinant_sign=sign,completion_residual=float(comp),Q=np.array(qlist).tolist(),W=np.array(wlist).tolist(),finite_difference_steps=fd_steps,finite_difference_errors=fd_errors,
                            Q_rank=V81.describe(qmap[3*e:3*e+3],qref),E_rank=V81.describe(emap[3*e:3*e+3],eref))
                edge_rows.append(edge)
            row={'candidate_index':candidate,'lambda':lam,'domain':bool(domain),'edges':edge_rows,'Q':None,'E':None,'Q_map':None,'E_map':None,'response_pass':False}
            domain_all=domain_all and domain
            if domain:
                qm=V81.describe(qmap,qref);em=V81.describe(emap,eref);target=[0]*3 if lam==0 else [2]*3
                passed=qm['ranks']==target and em['ranks']==target
                if lam==0:passed=passed and qm['norm']<=1e-12 and em['norm']<=1e-12
                row.update(Q=qm,E=em,Q_map=qmap.tolist(),E_map=emap.tolist(),response_pass=bool(passed))
            response_all=response_all and row['response_pass'];rows.append(row)
    sym=symbolic_certificate();ip=V75.density_diagnostics(inputs);op=V75.density_diagnostics(outputs)
    valid=bool(parents and indices==V92.V91.EXPECTED and len(rows)==36 and len(channels)==6 and sym['valid'] and all(x['valid'] for x in channels) and ip['valid'] and op['valid'] and all(controls[k]<=v for k,v in limits.items()))
    controls.update(parents_valid=bool(parents),symbolic_certificate=sym,input_physicality=ip,source_output_physicality=op)
    verdict,response_verdict=adjudicate(valid,domain_all,response_all)
    report={'version':'15.93','all_valid':valid,'verdict':verdict,'response_verdict':response_verdict,'domain_predicate':bool(domain_all),'response_predicate':bool(response_all),'candidate_indices':indices,'controls':controls,'channels':channels,'frames':[a.tolist() for a in frames],'rows':rows,
            'scope':'Oriented rank-two extension, conditional on Bloch SO(3) orientation; no physical source selection, composition theorem or gravity derivation. Prior singular-domain verdicts unchanged.'}
    def finite(x):
        if isinstance(x,dict):return all(finite(v) for v in x.values())
        if isinstance(x,list):return all(finite(v) for v in x)
        if isinstance(x,(int,float)):return bool(np.isfinite(x))
        return True
    if not finite(report):report['all_valid']=False;report['verdict']=report['response_verdict']='INVALID'
    return report

if __name__=='__main__':
    report=run_measurement();print(json.dumps(report,indent=2,allow_nan=False));sys.exit(0 if report['all_valid'] else 2)
