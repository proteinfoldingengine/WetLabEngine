# V1702.2 - Pre-Registered Momentum-Slice Audit
# 8 PRE-REGISTERED momentum families M0..M7. Score commutator overlap into each,
# with per-slice random-control ratio. Selection test only for slices passing overlap>0.5.
import numpy as np

N_PAIRS=40; n=49
FAMS=["gaussian3","dipole","chirp","mixed"]
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
D=Dmat(n)
rho=np.maximum(1+0.18*np.cos(2*np.pi*np.arange(n)/n)+0.05*src(n,"mixed"),0.25)
ginv=1/(1+0.08*np.sin(2*np.pi*np.arange(n)/n)+0.04*src(n,"mixed"))**2
W=rho/ginv

def Wadj(A):  # A_K = -W^-1 A^T W
    return -(A.T*W[None,:])/W[:,None]

# PRE-REGISTERED Ag(c) builders
def M0(c): return np.diag(c)@D+np.diag(D@c)
def M1(c): return np.diag(c)@D
def M2(c): return D@np.diag(c)
def M3(c): return 0.5*(np.diag(c)@D+D@np.diag(c))
def M4(c): return np.diag(c)@D-D@np.diag(c)
def M5(c): return np.diag(1/rho)@D@np.diag(rho*c)
def M6(c): return np.diag(1/W)@D.T@np.diag(W*c)
# M7 handled as 2-channel span below
SLICES={"M0":M0,"M1":M1,"M2":M2,"M3":M3,"M4":M4,"M5":M5,"M6":M6}

def momvec(Agfun,c): Ag=Agfun(c); return np.concatenate([Ag.ravel(),Wadj(Ag).ravel()])

def build_S(Agfun):
    cols=[]
    for k in range(n):
        e=np.zeros(n); e[k]=1; e-=e.mean(); cols.append(momvec(Agfun,e))
    Q,_=np.linalg.qr(np.column_stack(cols)); return Q

def build_S_M7():  # span{diag(c)D, D diag(c)} two channels
    cols=[]
    for k in range(n):
        e=np.zeros(n); e[k]=1; e-=e.mean()
        cols.append(np.concatenate([(np.diag(e)@D).ravel(),Wadj(np.diag(e)@D).ravel()]))
        cols.append(np.concatenate([(D@np.diag(e)).ravel(),Wadj(D@np.diag(e)).ravel()]))
    Q,_=np.linalg.qr(np.column_stack(cols)); return Q

# transport generator commutator family (the one with structure)
def transport(N,alpha=1.0):
    A=np.diag(N)@D+alpha*np.diag(D@N); return A,Wadj(A)
rng=np.random.default_rng(17022)
def rand_lapse():
    x=np.arange(n)/n; k=rng.integers(1,6); ph=rng.uniform(0,2*np.pi)
    f=np.sin(2*np.pi*k*x+ph)+0.3*rng.normal(size=n); f-=f.mean(); return f
def gen1_comm(N,M):
    AN,BN=transport(N); AM,BM=transport(M)
    return np.concatenate([(-AN@BM+AM@BN).ravel(),(-BN@AM+BM@AN).ravel()])

# commutator span
cols=[gen1_comm(rand_lapse(),rand_lapse()) for _ in range(N_PAIRS)]
Cmat=np.column_stack(cols); Cmat/= (np.linalg.norm(Cmat,axis=0,keepdims=True)+1e-24)
Qc,_=np.linalg.qr(Cmat); rk=int((np.linalg.svd(Cmat,compute_uv=False)>1e-6).sum()); Qc=Qc[:,:rk]

def rand_firstorder_span():
    cols=[]
    for _ in range(N_PAIRS):
        f=rand_lapse(); g=rand_lapse()
        A=np.diag(f)@D; B=Wadj(A)
        Cc=np.concatenate([(-A@(np.diag(g)@D)+(np.diag(g)@D)@A).ravel()]*2)
        cols.append(Cc)
    R=np.column_stack(cols); R/=(np.linalg.norm(R,axis=0,keepdims=True)+1e-24)
    Qr,_=np.linalg.qr(R); return Qr[:,:rk]
Qrand=rand_firstorder_span()

def overlap_into(Q_S, Q_span):
    P=Q_S@(Q_S.T@Q_span); return np.linalg.norm(P,"fro")**2/Q_span.shape[1]

print(f"commutator span rank={rk}")
print(f"{'slice':>5} | {'overlap_C':>10} {'overlap_rand':>13} {'ratio':>7}")
print("-"*42)
allS={**{k:build_S(v) for k,v in SLICES.items()},"M7":build_S_M7()}
order=["M0","M1","M2","M3","M4","M5","M6","M7"]
passers=[]
for name in order:
    Q_S=allS[name]
    oc=overlap_into(Q_S,Qc); orr=overlap_into(Q_S,Qrand)
    ratio=oc/(orr+1e-12)
    tag=""
    if oc>0.5 and ratio>1.2: tag=" <-- PASS overlap"; passers.append(name)
    print(f"{name:>5} | {oc:>10.4f} {orr:>13.4f} {ratio:>7.2f}{tag}")

print("\n--- VERDICT ---")
if not passers:
    print("FAIL: no pre-registered slice clears overlap>0.5 with ratio>1.2.")
    print("Across tested generators and 8 pre-registered admissible momentum slices,")
    print("the retained scalar-scalar commutator does NOT recover an ADM-like H-H target.")
    print("=> Pillar 3 NEGATIVE for the current retained construction class.")
else:
    print(f"Slices passing overlap gate: {passers}  -> run selection test next.")
