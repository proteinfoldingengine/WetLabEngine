# POST-MORTEM AUDIT of V1702.2
# Goal: find bugs that would FAKE a negative. A false negative here comes from:
#  (a) the projection/overlap metric being wrong (under-reporting overlap),
#  (b) the momentum-slice bases being degenerate/rank-deficient,
#  (c) a positive-control target that SHOULD score ~1.0 failing -> metric is broken,
#  (d) block-structure mismatch (comparing C's [C11,C22] against M's [Ag,Ak] in wrong order).
import numpy as np
n=49
def src(n,fam):
    x=np.arange(n)/n
    if fam=="mixed": s=0.65*np.sin(2*np.pi*x+0.3)+0.45*np.exp(-((x-0.33)/0.07)**2)-0.55*np.exp(-((x-0.72)/0.09)**2)
    s-=s.mean(); return s/(np.max(np.abs(s))+1e-12)
def Dmat(n):
    D=np.zeros((n,n))
    for i in range(n): D[i,(i+1)%n]=0.5; D[i,(i-1)%n]=-0.5
    return D
D=Dmat(n)
rho=np.maximum(1+0.18*np.cos(2*np.pi*np.arange(n)/n)+0.05*src(n,"mixed"),0.25)
ginv=1/(1+0.08*np.sin(2*np.pi*np.arange(n)/n)+0.04*src(n,"mixed"))**2
W=rho/ginv
def Wadj(A): return -(A.T*W[None,:])/W[:,None]
def M0(c): return np.diag(c)@D+np.diag(D@c)
def momvec(Agfun,c): Ag=Agfun(c); return np.concatenate([Ag.ravel(),Wadj(Ag).ravel()])
def build_S(Agfun):
    cols=[]
    for k in range(n):
        e=np.zeros(n); e[k]=1; e-=e.mean(); cols.append(momvec(Agfun,e))
    B=np.column_stack(cols); Q,Rr=np.linalg.qr(B)
    return Q,B,Rr

print("=== CHECK (b): is the momentum-slice basis rank-deficient? ===")
Q,B,Rr=build_S(M0)
ranks=np.linalg.matrix_rank(B,tol=1e-9)
print(f"M0 basis: {B.shape[1]} columns, numerical rank = {ranks}")
print(f"  (e is mean-subtracted so we EXPECT rank n-1={n-1}, not n. If much lower -> degenerate.)")
diagR=np.abs(np.diag(Rr)); print(f"  smallest |R_ii| = {diagR.min():.2e}, largest = {diagR.max():.2e}")

print("\n=== CHECK (c): POSITIVE CONTROL. A target that IS in the slice must score ~1.0 ===")
def overlap_into(Q_S,Q_span): 
    P=Q_S@(Q_S.T@Q_span); return np.linalg.norm(P,"fro")**2/Q_span.shape[1]
# Build a 'commutator span' that is LITERALLY made of M0 operators. Overlap must be ~1.
rng=np.random.default_rng(1)
cols=[]
for _ in range(40):
    c=rng.normal(size=n); c-=c.mean()
    cols.append(momvec(M0,c))
Cpos=np.column_stack(cols); Cpos/=(np.linalg.norm(Cpos,axis=0,keepdims=True)+1e-24)
Qpos,_=np.linalg.qr(Cpos); rkpos=int((np.linalg.svd(Cpos,compute_uv=False)>1e-6).sum()); Qpos=Qpos[:,:rkpos]
print(f"  positive-control overlap into M0 slice = {overlap_into(Q,Qpos):.4f}  (MUST be ~1.0)")

print("\n=== CHECK (a)+(d): does the metric see a PARTIAL plant? ===")
# Build commutator span = 50% real-transport-like + 50% M0. Overlap should be ~0.5.
def transport(N,alpha=1.0):
    A=np.diag(N)@D+alpha*np.diag(D@N); return A,Wadj(A)
def rand_lapse():
    x=np.arange(n)/n; k=rng.integers(1,6); ph=rng.uniform(0,2*np.pi)
    f=np.sin(2*np.pi*k*x+ph)+0.3*rng.normal(size=n); f-=f.mean(); return f
def gen1_comm(N,M):
    AN,BN=transport(N); AM,BM=transport(M)
    return np.concatenate([(-AN@BM+AM@BN).ravel(),(-BN@AM+BM@AN).ravel()])
real=gen1_comm(rand_lapse(),rand_lapse()); real/=np.linalg.norm(real)
plant=momvec(M0,rng.normal(size=n)); plant/=np.linalg.norm(plant)
mix=0.5*real+0.5*plant
Qmix,_=np.linalg.qr(mix.reshape(-1,1))
print(f"  overlap of (0.5 M0-plant + 0.5 real) into M0 = {overlap_into(Q,Qmix):.4f}  (expect noticeably >0 if metric honest)")

print("\n=== CHECK: recompute the REAL V1702.2 numbers with an INDEPENDENT overlap formula ===")
# independent method: for each commutator column, solve least-squares onto M0 basis, measure captured norm
cols=[gen1_comm(rand_lapse(),rand_lapse()) for _ in range(40)]
Cmat=np.column_stack(cols); Cmat/=(np.linalg.norm(Cmat,axis=0,keepdims=True)+1e-24)
# method 1: subspace projection (as used)
Qc,_=np.linalg.qr(Cmat); rk=int((np.linalg.svd(Cmat,compute_uv=False)>1e-6).sum()); Qc=Qc[:,:rk]
m1=overlap_into(Q,Qc)
# method 2: per-column least squares captured energy
caps=[]
for j in range(Cmat.shape[1]):
    v=Cmat[:,j]; coef,_,_,_=np.linalg.lstsq(B,v,rcond=None); cap=np.linalg.norm(B@coef)/np.linalg.norm(v); caps.append(cap**2)
m2=np.mean(caps)
print(f"  M0 overlap  method1(subspace)={m1:.4f}   method2(per-col lstsq captured energy)={m2:.4f}")
print(f"  (the two independent methods should AGREE; if they disagree the metric is suspect)")

print("\n=== CHECK: are C11 and C22 actually antisymmetric, and is M's Ak the right partner? ===")
AN,BN=transport(rand_lapse()); AM,BM=transport(rand_lapse())
C11=-AN@BM+AM@BN
print(f"  ||C11+C11^T||/||C11|| = {np.linalg.norm(C11+C11.T)/np.linalg.norm(C11):.3f}  (near 0 => antisymmetric)")
Ag=M0(rng.normal(size=n)); Ak=Wadj(Ag)
print(f"  check Wadj: ||W Ak + (W Ag)^T||/scale = {np.linalg.norm(W[:,None]*Ak+(W[:,None]*Ag).T)/(np.linalg.norm(W[:,None]*Ak)+1e-12):.2e} (near 0 => partner rule consistent)")
