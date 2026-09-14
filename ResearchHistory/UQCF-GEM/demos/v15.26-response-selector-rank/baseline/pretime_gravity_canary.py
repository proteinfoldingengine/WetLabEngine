from __future__ import annotations
from dataclasses import dataclass
import numpy as np

X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.array([[1,0],[0,-1]],complex)
I2=np.eye(2,dtype=complex)

@dataclass(frozen=True)
class ComplexData:
    L:int; B1:np.ndarray; B2:np.ndarray; vertices:tuple; edges:tuple; faces:tuple
    vertex_index:dict; edge_index:dict; face_index:dict; face_loops:dict; edge_axes:tuple

@dataclass(frozen=True)
class Response:
    current:np.ndarray; potential:np.ndarray; residual:float

def torus_complex(L:int=7)->ComplexData:
    if type(L) is not int or L<3: raise ValueError('L>=3 integer required')
    verts=tuple((x,y) for y in range(L) for x in range(L)); vi={v:i for i,v in enumerate(verts)}
    edges=[]; axes=[]
    for y in range(L):
        for x in range(L):
            edges.append(((x,y),((x+1)%L,y),'h')); axes.append('X')
            edges.append(((x,y),(x,(y+1)%L),'v')); axes.append('Y')
    ei={(u,v,t):i for i,(u,v,t) in enumerate(edges)}
    B1=np.zeros((len(verts),len(edges)),float)
    for e,(u,v,t) in enumerate(edges): B1[vi[u],e]=-1; B1[vi[v],e]=1
    faces=tuple((x,y) for y in range(L) for x in range(L)); fi={f:i for i,f in enumerate(faces)}
    B2=np.zeros((len(edges),len(faces)),float); loops={}
    for f,(x,y) in enumerate(faces):
        bottom=ei[((x,y),((x+1)%L,y),'h')]; right=ei[(((x+1)%L,y),((x+1)%L,(y+1)%L),'v')]
        top=ei[((x,(y+1)%L),((x+1)%L,(y+1)%L),'h')]; left=ei[((x,y),(x,(y+1)%L),'v')]
        seq=((bottom,1),(right,1),(top,-1),(left,-1)); loops[(x,y)]=seq
        for e,s in seq: B2[e,f]=s
    return ComplexData(L,B1,B2,verts,tuple(edges),faces,vi,ei,fi,loops,tuple(axes))

def incidence_defect(c,face=(0,0),edge_slot='bottom',amplitude=1.0):
    if face not in c.face_loops or not np.isfinite(amplitude): raise ValueError('invalid source')
    slots={'bottom':0,'right':1,'top':2,'left':3}
    if edge_slot not in slots: raise ValueError('unknown edge slot')
    e,_=c.face_loops[face][slots[edge_slot]]; delta=np.zeros(c.B1.shape[1]); delta[e]=float(amplitude)
    return c.B1@delta,delta

def closed_face_control(c,face=(0,0),amplitude=1.0):
    if face not in c.face_index or not np.isfinite(amplitude): raise ValueError('invalid control')
    return c.B1@(float(amplitude)*c.B2[:,c.face_index[face]])

def compatibility_response(B1,q):
    B1=np.asarray(B1,float); q=np.asarray(q,float)
    if B1.ndim!=2 or q.shape!=(B1.shape[0],) or not np.isfinite(B1).all() or not np.isfinite(q).all(): raise ValueError('finite incidence/source required')
    if abs(float(q.sum()))>1e-10: raise ValueError('source must be neutral')
    phi=np.linalg.pinv(B1@B1.T,rcond=1e-13)@q; j=-B1.T@phi
    return Response(j,phi,float(np.linalg.norm(B1@j+q)))

def weighted_response(B1,q,weights):
    B1=np.asarray(B1,float); q=np.asarray(q,float); weights=np.asarray(weights,float)
    if B1.ndim!=2 or q.shape!=(B1.shape[0],) or weights.shape!=(B1.shape[1],): raise ValueError('dimension mismatch')
    if not np.isfinite(B1).all() or not np.isfinite(q).all() or not np.isfinite(weights).all() or np.any(weights<=0): raise ValueError('finite positive edge inner product required')
    if abs(float(q.sum()))>1e-10: raise ValueError('neutral source required')
    winv=1.0/weights; phi=np.linalg.pinv((B1*winv[None,:])@B1.T,rcond=1e-13)@q
    j=-(winv[:,None]*B1.T)@phi
    return Response(j,phi,float(np.linalg.norm(B1@j+q)))

def torus_face_distance(c,a,b):
    L=c.L; dx=abs(a[0]-b[0]); dy=abs(a[1]-b[1]); return min(dx,L-dx)+min(dy,L-dy)
def farthest_face(c,source=(0,0)): return max(c.faces,key=lambda f:(torus_face_distance(c,source,f),f[1],f[0]))
def face_circulation(c,j,face): return float(sum(s*j[e] for e,s in c.face_loops[face]))
def _rot(axis,angle):
    s={'X':X,'Y':Y,'Z':Z}[axis]; return np.cos(angle)*I2+1j*np.sin(angle)*s

def face_holonomy(c,j,face,epsilon=.2,commuting=False):
    if face not in c.face_loops or not np.isfinite(epsilon): raise ValueError('invalid holonomy input')
    H=I2.copy()
    for e,s in c.face_loops[face]: H=H@_rot('Z' if commuting else c.edge_axes[e],float(epsilon*s*j[e]))
    return H

def response_commutator_holonomy(c,j,face,epsilon=.2,commuting=False):
    if face not in c.face_loops or not np.isfinite(epsilon): raise ValueError('invalid commutator input')
    loop=c.face_loops[face]; ex=next(e for e,_ in loop if c.edge_axes[e]=='X'); ey=next(e for e,_ in loop if c.edge_axes[e]=='Y')
    a=float(epsilon*j[ex]); b=float(epsilon*j[ey]); ax='Z' if commuting else 'X'; ay='Z' if commuting else 'Y'
    return _rot(ax,a)@_rot(ay,b)@_rot(ax,-a)@_rot(ay,-b)
def holonomy_defect(H): return float(np.linalg.norm(np.asarray(H)-I2))

def remote_shell_summary(c,j,source_face=(0,0),epsilon=.2,min_distance=None):
    if source_face not in c.face_index: raise ValueError('unknown source face')
    if min_distance is None: min_distance=max(1,c.L//3)
    faces=[f for f in c.faces if torus_face_distance(c,source_face,f)>=min_distance]
    if not faces: raise ValueError('empty remote shell')
    hn=np.array([holonomy_defect(face_holonomy(c,j,f,epsilon,False)) for f in faces]); hc=np.array([holonomy_defect(face_holonomy(c,j,f,epsilon,True)) for f in faces]); cm=np.array([holonomy_defect(response_commutator_holonomy(c,j,f,epsilon,False)) for f in faces])
    return {'face_count':len(faces),'min_distance':min_distance,'noncommuting_rms':float(np.sqrt(np.mean(hn*hn))),'noncommuting_max':float(np.max(hn)),'commuting_rms':float(np.sqrt(np.mean(hc*hc))),'commutator_rms':float(np.sqrt(np.mean(cm*cm)))}

def block_incidence(A,B):
    A=np.asarray(A,float); B=np.asarray(B,float); return np.block([[A,np.zeros((A.shape[0],B.shape[1]))],[np.zeros((B.shape[0],A.shape[1])),B]])

def audit():
    c=torus_complex(7); q,d=incidence_defect(c,(0,0),'bottom',1.0); r=compatibility_response(c.B1,q); far=farthest_face(c,(0,0))
    hn=holonomy_defect(face_holonomy(c,r.current,far,.2,False)); hc=holonomy_defect(face_holonomy(c,r.current,far,.2,True))
    rng=np.random.default_rng(140926); pv=rng.permutation(c.B1.shape[0]); pe=rng.permutation(c.B1.shape[1]); rp=compatibility_response(c.B1[pv][:,pe],q[pv]); cov=float(np.linalg.norm(rp.current-r.current[pe]))
    closed=float(np.linalg.norm(compatibility_response(c.B1,closed_face_control(c,(0,0),3.0)).current)); frac=float(np.mean(np.abs(r.current)>1e-10))
    cycle=c.B2[:,c.face_index[far]]; shifted=r.current+0.25*cycle; shift_closure=float(np.linalg.norm(c.B1@shifted+q)); cycle_change=abs(holonomy_defect(face_holonomy(c,shifted,far,.2,False))-hn)
    alt=weighted_response(c.B1,q,np.linspace(.75,1.25,c.B1.shape[1])); weight_diff=float(np.linalg.norm(alt.current-r.current)); nonunique=int(c.B1.shape[1]-np.linalg.matrix_rank(c.B1,tol=1e-11))
    orientation=[]
    for slot in ('bottom','right','top','left'):
        qs,_=incidence_defect(c,(0,0),slot,1.0); rs=compatibility_response(c.B1,qs); shell=remote_shell_summary(c,rs.current,(0,0),epsilon=.2); orientation.append({'slot':slot,'response_fraction':float(np.mean(np.abs(rs.current)>1e-10)),'response_norm':float(np.linalg.norm(rs.current)),**shell})
    translations=[]
    for face in ((0,0),(1,2),(3,4)):
        qt,_=incidence_defect(c,face,'bottom',1.0); rt=compatibility_response(c.B1,qt); translations.append({'face':list(face),'response_norm':float(np.linalg.norm(rt.current)),'remote_noncommuting_rms':remote_shell_summary(c,rt.current,face)['noncommuting_rms']})
    trans_error=max(abs(x['response_norm']-translations[0]['response_norm'])+abs(x['remote_noncommuting_rms']-translations[0]['remote_noncommuting_rms']) for x in translations)
    q2,_=incidence_defect(c,(3,3),'right',-.4); q1,_=incidence_defect(c,(0,0),'bottom',.7); super_err=float(np.linalg.norm(compatibility_response(c.B1,q1+q2).current-(compatibility_response(c.B1,q1).current+compatibility_response(c.B1,q2).current)))
    a1=remote_shell_summary(c,compatibility_response(c.B1,incidence_defect(c,(0,0),'bottom',.5)[0]).current,(0,0),epsilon=.05)['commutator_rms']; a2=remote_shell_summary(c,r.current,(0,0),epsilon=.05)['commutator_rms']
    eps1=holonomy_defect(face_holonomy(c,r.current,far,.01,False)); eps2=holonomy_defect(face_holonomy(c,r.current,far,.02,False)); cm1=holonomy_defect(response_commutator_holonomy(c,r.current,far,.01,False)); cm2=holonomy_defect(response_commutator_holonomy(c,r.current,far,.02,False))
    structural=(np.linalg.norm(c.B1@c.B2)<1e-12 and r.residual<1e-10 and min(x['response_fraction'] for x in orientation)>.4 and min(x['noncommuting_rms'] for x in orientation)>1e-4 and max(x['commuting_rms'] for x in orientation)<1e-10 and closed<1e-12 and cov<1e-10 and trans_error<1e-10 and super_err<1e-10)
    local=-d; local_residual=float(np.linalg.norm(c.B1@local+q)); local_support=int(np.count_nonzero(np.abs(local)>1e-12)); local_remote_holonomy=holonomy_defect(face_holonomy(c,local,far,.2,False))
    return {'version':'v15.25','status':'PRETIME_GRAVITY_CANARY_KILLED_LOCAL_COMPLETION_AND_RESPONSE_NONUNIQUENESS','candidate_law_status':'SUPPLIED_PRETIME_HIGHER_INCIDENCE_CANARY','admissibility_equation':'B1 j + q = 0','baseline_chain_error':float(np.linalg.norm(c.B1@c.B2)),'closure_residual':r.residual,'global_response_fraction':frac,'response_norm':float(np.linalg.norm(r.current)),'remote_face':list(far),'remote_face_distance':torus_face_distance(c,(0,0),far),'remote_noncommuting_holonomy':hn,'remote_commuting_holonomy':hc,'remote_shell':remote_shell_summary(c,r.current,(0,0),epsilon=.2),'orientation_sweep':orientation,'translation_sweep':translations,'translation_covariance_error':float(trans_error),'superposition_error':super_err,'source_commutator_quadratic_ratio':float(a2/a1),'face_epsilon_scaling_ratio':float(eps2/eps1),'commutator_epsilon_scaling_ratio':float(cm2/cm1),'closed_face_control_response':closed,'covariance_error':cov,'response_nonuniqueness_dimension':nonunique,'cycle_shift_closure_residual':shift_closure,'cycle_shift_holonomy_change':float(cycle_change),'weighted_response_difference':weight_diff,'diagnostic_global_representative':bool(structural),'local_cancellation_exists':bool(local_residual<1e-12 and local_support==1),'local_cancellation_closure_residual':local_residual,'local_cancellation_support':local_support,'local_cancellation_remote_holonomy':local_remote_holonomy,'global_compatibility_signal':False,'signal_of_life':False,'gravity_canary_certified':False,'canary_verdict':'KILLED_BARE_COMPATIBILITY_DOES_NOT_FORCE_GLOBAL_RESPONSE','selector_status':'UNRESOLVED_CYCLE_COMPONENT_AND_EDGE_INNER_PRODUCT','response_selector_supplied':True,'state_operation_used':False,'uses_pruning':False,'uses_entropy':False,'uses_physical_time':False,'fits_newton_or_gr':False,'physical_gravity_derived':False,'canary_positive':False,'interpretation':'A supplied Hodge representative is global and develops remote noncommuting holonomy, but bare compatibility also admits exact one-edge local cancellation and arbitrary cycle additions. Therefore global response is not forced by this source law; the canary is killed until a response selector or stronger source-to-admissibility law is derived pre-time.'}

def main():
    import argparse,json
    from pathlib import Path
    p=argparse.ArgumentParser(); p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'outputs'); a=p.parse_args(); a.out.mkdir(parents=True,exist_ok=True); r=audit(); (a.out/'verification.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n'); print(json.dumps(r,indent=2,allow_nan=False))

if __name__=='__main__': main()
