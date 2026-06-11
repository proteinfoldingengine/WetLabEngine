# V1702.1 - Commutator Home / Operator-Subspace Characterization
# What subspace do scalar-scalar commutators actually occupy? Non-circular: we do
# NOT fit a target. We characterize span{C(N_i,M_i)} and project it onto candidate
# operator families. Rank measured against MANY pairs so low-rank is meaningful.
import numpy as np

N_PAIRS=40   # oversample: ceiling for rank; low-rank only meaningful << this
FAMS=["gaussian3","dipole","chirp","mixed"]
n=49         # single resolution for the span study (band families defined here)

def src(n,fam):
    x=np.arange(n)/n
    if fam=="gaussian3": s=np.exp(-((x-0.15)/0.055)**2)-0.7*np.exp(-((x-0.52)/0.075)**2)-0.3*np.exp(-((x-0.78)/0.06)**2)
    elif fam=="dipole": s=np.sin(2*np.pi*x)+0.35*np.sin(4*np.pi*x+0.4)
    elif fam=="chirp": s=np.sin(2*np.pi*(x+2.2*x*x))+0.25*np.cos(10*np.pi*x)
    elif fam=="mixed": s=0.65*np.sin(2*np.pi*x+0.3)+0.45*np.exp(-((x-0.33)/0.07)**2)-0.55*np.exp(-((x-0.72)/0.09)**2)
    s-=s.mean(); return s/(np.max(np.abs(s))+1e-12)
def Dmat(n):
    D=np.zeros((n,n))
    for i in range(n): D[i,(i+1)%n]=0.5; D[i,(i-1)%n]=-0.5
    return D
def rho_(n,fam):
    x=np.arange(n)/n; return np.maximum(1+0.18*np.cos(2*np.pi*x)+0.05*src(n,fam),0.25)
def ginv_(n,fam):
    x=np.arange(n)/n; return 1/(1+0.08*np.sin(2*np.pi*x)+0.04*src(n,fam))**2

D=Dmat(n)
# fixed background for the span study (use 'mixed')
rho=rho_(n,"mixed"); ginv=ginv_(n,"mixed"); W=rho/ginv

def Ablk2(N): return 2*np.diag(N)
def Bblk2(N): return np.diag(1/rho)@D.T@np.diag(ginv)@D@np.diag(rho*N)
def omegaW(A,B):
    WA=W[:,None]*A; WB=W[:,None]*B
    return 0.5*(WA+WA.T)/W[:,None],0.5*(WB+WB.T)/W[:,None]
def gen2_commutator(N,M):
    AN,BN=omegaW(Ablk2(N),Bblk2(N)); AM,BM=omegaW(Ablk2(M),Bblk2(M))
    return np.concatenate([(-AN@BM+AM@BN).ravel(),(-BN@AM+BM@AN).ravel()])
def transport(N,alpha=1.0):
    A=np.diag(N)@D+alpha*np.diag(D@N); B=-(A.T*W[None,:])/W[:,None]; return A,B
def gen1_commutator(N,M):
    AN,BN=transport(N); AM,BM=transport(M)
    return np.concatenate([(-AN@BM+AM@BN).ravel(),(-BN@AM+BM@AN).ravel()])

rng=np.random.default_rng(17021)
def rand_lapse():
    x=np.arange(n)/n; k=rng.integers(1,6); ph=rng.uniform(0,2*np.pi)
    f=np.sin(2*np.pi*k*x+ph)+0.3*rng.normal(size=n); f-=f.mean(); return f

def analyze(commfun,label):
    cols=[]
    for _ in range(N_PAIRS):
        N=rand_lapse(); M=rand_lapse(); cols.append(commfun(N,M))
    Cmat=np.column_stack(cols)
    # normalize columns
    Cmat=Cmat/(np.linalg.norm(Cmat,axis=0,keepdims=True)+1e-24)
    U,s,Vt=np.linalg.svd(Cmat,full_matrices=False)
    s=s/s[0]
    rank=int((s>1e-6).sum())
    eff_rank=float((s.sum())**2/ (s**2).sum())  # participation ratio
    # candidate family projections: build basis vectors of dimension 2*n*n (two blocks)
    dim_block=n*n
    def vec_from_blocks(B1,B2): return np.concatenate([B1.ravel(),B2.ravel()])
    # family bases (each a set of operator vectors)
    fam={}
    # M(c) momentum family
    mom=[]
    for k in range(n):
        e=np.zeros(n); e[k]=1; e-=e.mean()
        Ag=np.diag(e)@D+np.diag(D@e); Ak=-(Ag.T*W[None,:])/W[:,None]; mom.append(vec_from_blocks(Ag,Ak))
    fam["M(c)"]=np.column_stack(mom)
    # first-order transport family (diag(f)D, D diag(f), diag(Df)) in each block
    t1=[]
    for k in range(n):
        e=np.zeros(n); e[k]=1; e-=e.mean()
        t1.append(vec_from_blocks(np.diag(e)@D, np.zeros((n,n))))
        t1.append(vec_from_blocks(np.zeros((n,n)), np.diag(e)@D))
        t1.append(vec_from_blocks(D@np.diag(e), np.zeros((n,n))))
    fam["transport_1st"]=np.column_stack(t1)
    # second-order Laplacian-like family diag(f) D^T diag D
    t2=[]
    for k in range(n):
        e=np.zeros(n); e[k]=1; e-=e.mean()
        L=np.diag(1/rho)@D.T@np.diag(ginv)@D@np.diag(rho*e)
        t2.append(vec_from_blocks(L,np.zeros((n,n))))
        t2.append(vec_from_blocks(np.zeros((n,n)),L))
    fam["second_order"]=np.column_stack(t2)
    # diagonal/density family
    dg=[]
    for k in range(n):
        e=np.zeros(n); e[k]=1
        dg.append(vec_from_blocks(np.diag(e),np.zeros((n,n))))
        dg.append(vec_from_blocks(np.zeros((n,n)),np.diag(e)))
    fam["diagonal"]=np.column_stack(dg)
    # symmetry classes computed directly on the dominant commutator block
    # take leading left singular vector, reshape, measure sym/antisym split per block
    lead=U[:,0]
    B1=lead[:dim_block].reshape(n,n); B2=lead[dim_block:].reshape(n,n)
    def symfrac(B):
        s_=0.5*(B+B.T); a_=0.5*(B-B.T); tot=np.linalg.norm(B)+1e-24
        return np.linalg.norm(s_)/tot, np.linalg.norm(a_)/tot
    s1,a1=symfrac(B1); s2,a2=symfrac(B2)
    # bandwidth of dominant block
    def bandfrac(B,b):
        I,J=np.meshgrid(np.arange(n),np.arange(n),indexing="ij"); dist=np.minimum((I-J)%n,(J-I)%n)
        return np.linalg.norm(B*(dist<=b))/(np.linalg.norm(B)+1e-24)

    print(f"\n=== {label} ===")
    print(f"  pairs={N_PAIRS}  hard_rank(>1e-6)={rank}  participation_rank={eff_rank:.1f}")
    print(f"  singular spectrum (top8): {np.round(s[:8],3)}")
    print(f"  dominant block1 sym/antisym = {s1:.2f}/{a1:.2f}   block2 = {s2:.2f}/{a2:.2f}")
    print(f"  dominant block1 bandfrac(b1,b2,b3) = {bandfrac(B1,1):.2f}/{bandfrac(B1,2):.2f}/{bandfrac(B1,3):.2f}")
    # projection of commutator span onto each family (mean captured energy of C's top components)
    Qc,_=np.linalg.qr(Cmat)   # basis for commutator span
    rk=rank
    Qc=Qc[:,:rk]
    print("  projection of commutator-span onto candidate families (captured fraction):")
    for fname,Fb in fam.items():
        Qf,_=np.linalg.qr(Fb)
        # how much of commutator span lies in family span: ||Qf Qf^T Qc||_F^2 / rk
        P=Qf@(Qf.T@Qc)
        cap=np.linalg.norm(P,"fro")**2/rk
        print(f"     {fname:>14}: {cap:.4f}")

analyze(gen2_commutator,"V1701 second-order Omega_W-repaired generator")
analyze(gen1_commutator,"V1702 first-order transport generator")

print("\n--- INTERPRETATION GUIDE ---")
print(" Case A (structured low-rank, high projection into SOME family): Hypothesis 1 viable.")
print(" Case B (structured but only via diagonal/density or Omega-tied family): Hypothesis 3 viable.")
print(" Case C (high participation rank, no family captures it): Pillar 3 negative across constructions.")
