# V1701.19 - Target-Sensitive H-H Diagnostic Reconstruction
# c-INDEPENDENT score, defined BEFORE any c is chosen:
#   S = span of the momentum-constraint family { M(e_k) : e_k unit fields }
#   in_fraction(Comm) = ||P_S Comm|| / ||Comm||   (how much of the scalar-scalar
#       commutator lives in the momentum-constraint subspace at all)
# THEN, separately, a selection score: among targets c, which one best matches the
#   commutator WITHIN S?  best_c = argmin || P_S Comm - M(c) || over c.
# The true c should win ONLY if the commutator genuinely points at it. Decoys of
# equal norm that point elsewhere should lose. S never uses the true c.
import numpy as np

SIZES=[33,65]; FAMS=["gaussian3","dipole","chirp","mixed"]

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
def Ablk(N): return 2*np.diag(N)
def Bblk(N,D,rho,ginv): return np.diag(1/rho)@D.T@np.diag(ginv)@D@np.diag(rho*N)
def omegaW(A,B,W):
    WA=W[:,None]*A; WB=W[:,None]*B
    return 0.5*(WA+WA.T)/W[:,None], 0.5*(WB+WB.T)/W[:,None]
def mom_blocks(c,D,W):
    Ag=np.diag(c)@D+np.diag(D@c); Ak=-(Ag.T*W[None,:])/W[:,None]; return Ag,Ak

def mom_vector(c,D,W):
    # full momentum-constraint operator as a flat vector (both diagonal target blocks stacked)
    Ag,Ak=mom_blocks(c,D,W)
    return np.concatenate([Ag.ravel(),Ak.ravel()])

def scalar_commutator_vector(N,M,D,rho,ginv,W):
    AN,BN=omegaW(Ablk(N),Bblk(N,D,rho,ginv),W); AM,BM=omegaW(Ablk(M),Bblk(M,D,rho,ginv),W)
    C11=-AN@BM+AM@BN   # top-left block of [X_H(N),X_H(M)]
    C22=-BN@AM+BM@AN   # bottom-right block
    return np.concatenate([C11.ravel(),C22.ravel()])

def build_S_basis(n,D,W):
    # momentum-constraint subspace: span of M(e_k) for unit coordinate fields e_k.
    # Defined WITHOUT reference to the true c.
    cols=[]
    for k in range(n):
        e=np.zeros(n); e[k]=1.0; e-=e.mean()
        cols.append(mom_vector(e,D,W))
    Bmat=np.column_stack(cols)
    Q,_=np.linalg.qr(Bmat)   # orthonormal basis for S
    return Q

def true_c(n,fam):
    D=Dmat(n); rho=rho_(n,fam); ginv=ginv_(n,fam); N,M=lapses(n)
    return (ginv/rho)*(N*(D@M)-M*(D@N))

def smooth_random_field(n,target_norm,rng):
    k=np.fft.rfftfreq(n,d=1/n); amp=np.exp(-(k/4.0)**2)
    ph=rng.uniform(0,2*np.pi,size=len(k)); f=np.fft.irfft(amp*np.exp(1j*ph),n=n)
    f-=f.mean(); return f/(np.linalg.norm(f)+1e-12)*target_norm

rng=np.random.default_rng(1719)
in_fracs=[]
sel_rows=[]
labels=["TRUE_c","random_smooth","sign_flip","scrambled_c","wrong_deriv"]

for fam in FAMS:
    for n in SIZES:
        D=Dmat(n); rho=rho_(n,fam); ginv=ginv_(n,fam); W=rho/ginv; N,M=lapses(n)
        Q=build_S_basis(n,D,W)                       # S built with NO true c
        Comm=scalar_commutator_vector(N,M,D,rho,ginv,W)
        cnorm=np.linalg.norm(Comm)+1e-24
        proj=Q@(Q.T@Comm)
        in_frac=np.linalg.norm(proj)/cnorm           # c-INDEPENDENT score
        in_fracs.append(in_frac)

        # selection: which target c minimizes || P_S Comm - M(c) || ? compare true vs decoys
        c=true_c(n,fam); cn=np.linalg.norm(c)
        Df=np.zeros((n,n))
        for i in range(n): Df[i,(i+1)%n]=1.0; Df[i,i]=-1.0
        c_wd=(ginv/rho)*(N*(Df@M)-M*(Df@N)); c_wd=c_wd/np.linalg.norm(c_wd)*cn
        c_scr=c.copy(); rng.shuffle(c_scr)
        targets={"TRUE_c":c,"random_smooth":smooth_random_field(n,cn,rng),
                 "sign_flip":-c,"scrambled_c":c_scr,"wrong_deriv":c_wd}
        row={}
        for lab,cc in targets.items():
            mv=mom_vector(cc,D,W)
            # match against the in-subspace part of the commutator; score = residual / ||proj||
            row[lab]=float(np.linalg.norm(proj-mv)/(np.linalg.norm(proj)+1e-24))
        sel_rows.append(row)

in_fracs=np.array(in_fracs)
print("=== c-INDEPENDENT score: fraction of scalar commutator lying in momentum-constraint subspace S ===")
print(f"  in_fraction  mean={in_fracs.mean():.4f}  min={in_fracs.min():.4f}  max={in_fracs.max():.4f}")
print("  (1.0 => commutator fully inside the momentum-constraint family; ~0 => essentially outside it)")

print("\n=== SELECTION score (lower = better match): does TRUE_c win over decoys? ===")
print(f"{'target':>14} | {'mean':>8} {'min':>8} {'max':>8}")
print("-"*44)
agg={lab:np.array([r[lab] for r in sel_rows]) for lab in labels}
for lab in labels:
    a=agg[lab]; print(f"{lab:>14} | {a.mean():>8.4f} {a.min():>8.4f} {a.max():>8.4f}")

true_mean=agg["TRUE_c"].mean()
decoy_best=min(lab for lab in labels if lab!="TRUE_c")  # placeholder
decoy_best=min((lab for lab in labels if lab!="TRUE_c"), key=lambda l: agg[l].mean())
decoy_best_val=agg[decoy_best].mean()

# How often does TRUE_c strictly beat ALL decoys per-case?
wins=0; total=len(sel_rows)
for r in sel_rows:
    if all(r["TRUE_c"]<r[l] for l in labels if l!="TRUE_c"): wins+=1

print(f"\nTRUE_c selection score mean = {true_mean:.4f}")
print(f"best decoy = '{decoy_best}' mean = {decoy_best_val:.4f}")
print(f"TRUE_c strictly beats all decoys in {wins}/{total} cases")

print("\n--- VERDICT ---")
if in_fracs.mean() < 0.2:
    print(f"FAIL (subspace): commutator lies essentially OUTSIDE the momentum-constraint subspace")
    print(f"      (in_fraction={in_fracs.mean():.3f}). The bracket does not close on M(c) for ANY c.")
    print("      => retained construction does not encode the ADM target. Negative result.")
elif true_mean < 0.5*decoy_best_val and wins==total:
    print(f"PASS: commutator lands in S (in_frac={in_fracs.mean():.3f}) AND TRUE_c sharply selected over all decoys.")
    print("      A target-sensitive H-H diagnostic exists and the construction recovers the ADM target.")
elif true_mean < decoy_best_val and wins > total*0.7:
    print(f"WEAK PASS: TRUE_c preferred in most cases but not sharply/universally.")
else:
    print(f"FAIL (selection): even though some commutator mass is in S, TRUE_c is NOT preferentially")
    print(f"      selected over decoys. No target-sensitive diagnostic recovered.")
