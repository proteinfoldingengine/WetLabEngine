# V1702.0 - Transport-Compatible Scalar Generator Entry Gate (Hypothesis 2)
# Scalar generator blocks are now FIRST-ORDER transport operators, same family as
# the momentum target. Gate: does [X_H(N),X_H(M)] project substantially into
# S = span{M(e_k)} -- AND substantially MORE than a generic same-family operator?
import numpy as np

SIZES=[33,65]; FAMS=["gaussian3","dipole","chirp","mixed"]
ALPHAS=[0.0,0.5,1.0]

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
def lapses(n):
    x=np.arange(n)/n
    N=np.sin(4*np.pi*x+0.4)+0.1*np.cos(2*np.pi*x); M=np.cos(4*np.pi*x-0.1)+0.12*np.sin(8*np.pi*x)
    return N-N.mean(),M-M.mean()

# Momentum-family block (the target family), unchanged from V1701.
def mom_blocks(c,D,W):
    Ag=np.diag(c)@D+np.diag(D@c); Ak=-(Ag.T*W[None,:])/W[:,None]; return Ag,Ak
def mom_vector(c,D,W):
    Ag,Ak=mom_blocks(c,D,W); return np.concatenate([Ag.ravel(),Ak.ravel()])

# NEW first-order transport scalar generator blocks.
# A_N = diag(N)D + alpha*diag(D N)   (transport / product-rule family)
# B_N chosen as the W-adjoint-compatible partner so X_H is Omega_W-consistent:
#   require W-weighted antisymmetry pairing like the momentum block does.
def transport_blocks(N,D,W,alpha):
    A = np.diag(N)@D + alpha*np.diag(D@N)
    # W-adjoint partner: B = -(A^T * W)/W  (same construction that makes Ak the partner of Ag)
    B = -(A.T*W[None,:])/W[:,None]
    return A,B

def omegaW_sym(A,W):
    # symmetrize in the W-metric (frame check); returns frame residual too
    WA=W[:,None]*A
    sym=0.5*(WA+WA.T)/W[:,None]
    res=np.linalg.norm(WA-WA.T,"fro")/(np.linalg.norm(WA,"fro")+1e-24)
    return sym,res

def commutator_vec(N,M,D,W,alpha):
    AN,BN=transport_blocks(N,D,W,alpha); AM,BM=transport_blocks(M,D,W,alpha)
    # X_H = [[0,A],[-B,0]]; [X_H(N),X_H(M)] block structure:
    C11=-AN@BM+AM@BN
    C22=-BN@AM+BM@AN
    return np.concatenate([C11.ravel(),C22.ravel()]), (AN,BN,AM,BM)

def build_S(n,D,W):
    cols=[]
    for k in range(n):
        e=np.zeros(n); e[k]=1.0; e-=e.mean(); cols.append(mom_vector(e,D,W))
    Q,_=np.linalg.qr(np.column_stack(cols)); return Q

def random_firstorder_vec(n,D,W,rng):
    # generic same-family first-order operator, for the triviality control
    f=rng.normal(size=n); f-=f.mean()
    g=rng.normal(size=n); g-=g.mean()
    A=np.diag(f)@D + rng.normal()*np.diag(D@f)
    B=-(A.T*W[None,:])/W[:,None]
    C11=-A@(np.diag(g)@D)+ (np.diag(g)@D)@A   # arbitrary same-family commutator
    return np.concatenate([C11.ravel(),C11.ravel()])

def true_c(n,fam,D):
    rho=rho_(n,fam); ginv=ginv_(n,fam); N,M=lapses(n)
    return (ginv/rho)*(N*(D@M)-M*(D@N))

rng=np.random.default_rng(17020)
print(f"{'alpha':>6} | {'overlap_C':>10} {'overlap_rand':>13} {'ratio':>7} | {'frame_res':>10}")
print("-"*60)
results={}
for alpha in ALPHAS:
    ov=[]; ovr=[]; fr=[]
    for fam in FAMS:
        for n in SIZES:
            D=Dmat(n); rho=rho_(n,fam); ginv=ginv_(n,fam); W=rho/ginv; N,M=lapses(n)
            Q=build_S(n,D,W)
            C,(AN,BN,AM,BM)=commutator_vec(N,M,D,W,alpha)
            cn=np.linalg.norm(C)+1e-24
            overlap=np.linalg.norm(Q@(Q.T@C))/cn
            # frame residual of the transport block under W
            _,r1=omegaW_sym(AN,W)
            ov.append(overlap); fr.append(r1)
            # triviality control: generic same-family operator
            R=random_firstorder_vec(n,D,W,rng); rn=np.linalg.norm(R)+1e-24
            ovr.append(np.linalg.norm(Q@(Q.T@R))/rn)
    ov=np.array(ov); ovr=np.array(ovr); fr=np.array(fr)
    ratio=ov.mean()/(ovr.mean()+1e-12)
    results[alpha]=(ov.mean(),ovr.mean(),ratio)
    print(f"{alpha:>6.2f} | {ov.mean():>10.4f} {ovr.mean():>13.4f} {ratio:>7.2f} | {fr.mean():>10.3e}")

print("\n(overlap_C = real commutator into S; overlap_rand = generic same-family op into S;")
print(" ratio>1 means the real commutator is preferentially in S, not trivially.)")

# Gate evaluation on best alpha
best_alpha=max(results,key=lambda a: results[a][0])
ovC,ovR,ratio=results[best_alpha]
print(f"\nBest alpha={best_alpha}: overlap_C={ovC:.4f}, control={ovR:.4f}, ratio={ratio:.2f}")
print("\n--- V1702.0 GATE ---")
if ovC>0.8 and ratio>1.5:
    print("STRONG PASS: commutator lands strongly and non-trivially in momentum family. Proceed to selection test.")
elif ovC>0.5 and ratio>1.2:
    print("PASS: substantial non-trivial overlap. Proceed to selection test.")
elif ovC>0.5 and ratio<=1.2:
    print(f"TRIVIAL PASS (REJECT): overlap high ({ovC:.2f}) but generic ops also overlap ({ovR:.2f}).")
    print("  The whole first-order sector sits in S; high overlap is tautological, not structural.")
else:
    print(f"FAIL AT ENTRY: overlap={ovC:.3f}. Transport generator does not close on momentum family either.")
    print("  Hypothesis 2 does not rescue Pillar 3. Stop. No decomposition, no GR language.")
