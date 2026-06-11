# V1701.18 - Target Identification Null Test
# Question: does the post-frame H-H obstruction metric actually distinguish the
# TRUE structure-function target c from norm/smoothness-matched DECOY targets?
# If true-c is not meaningfully lower than decoys, the metric is blind and the
# whole persistence story collapses into "HH is ~constant regardless of target".
import numpy as np

SIZES=[33,65]; FAMS=["gaussian3","dipole","chirp","mixed"]
rng_global=np.random.default_rng(1718)

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
def mom(c,D,W):
    Ag=np.diag(c)@D+np.diag(D@c); Ak=-(Ag.T*W[None,:])/W[:,None]; return Ag,Ak
def obstruction(AN,BN,AM,BM,Ag,Ak):
    return (-AN@BM+AM@BN)-Ag, (-BN@AM+BM@AN)-Ak
def total_hh(Og,OK,Ag,Ak):
    num=np.linalg.norm(Og,"fro")**2+np.linalg.norm(OK,"fro")**2
    den=np.linalg.norm(Ag,"fro")**2+np.linalg.norm(Ak,"fro")**2
    return float(np.sqrt(num/(den+1e-24)))

def smooth_random_field(n, target_norm, rng):
    # low-frequency random field, matched to target norm, zero mean
    k=np.fft.rfftfreq(n,d=1/n)
    amp=np.exp(-(k/4.0)**2)  # smooth: suppress high freq
    ph=rng.uniform(0,2*np.pi,size=len(k))
    spec=amp*np.exp(1j*ph)
    f=np.fft.irfft(spec,n=n); f-=f.mean()
    f=f/(np.linalg.norm(f)+1e-12)*target_norm
    return f

def hh_for_target(n,fam,c):
    D=Dmat(n); rho=rho_(n,fam); ginv=ginv_(n,fam); W=rho/ginv; N,M=lapses(n)
    Ag,Ak=mom(c,D,W)
    AN,BN=omegaW(Ablk(N),Bblk(N,D,rho,ginv),W); AM,BM=omegaW(Ablk(M),Bblk(M,D,rho,ginv),W)
    Og,OK=obstruction(AN,BN,AM,BM,Ag,Ak)
    return total_hh(Og,OK,Ag,Ak)

def true_c(n,fam):
    D=Dmat(n); rho=rho_(n,fam); ginv=ginv_(n,fam); N,M=lapses(n)
    return (ginv/rho)*(N*(D@M)-M*(D@N))

# Collect HH for true c and a battery of decoys, all norm-matched to true c.
labels=["TRUE_c","random_smooth","sign_flip","no_weight","wrong_deriv","scrambled_c","zero_target"]
agg={k:[] for k in labels}

for fam in FAMS:
    for n in SIZES:
        D=Dmat(n); rho=rho_(n,fam); ginv=ginv_(n,fam); N,M=lapses(n)
        c=true_c(n,fam); cn=np.linalg.norm(c)
        # decoys
        c_rand=smooth_random_field(n,cn,rng_global)
        c_flip=-c
        c_nw=(N*(D@M)-M*(D@N)); c_nw=c_nw/np.linalg.norm(c_nw)*cn          # strip ginv/rho weight, renorm
        # wrong derivative: forward difference instead of central
        Df=np.zeros((n,n))
        for i in range(n): Df[i,(i+1)%n]=1.0; Df[i,i]=-1.0
        c_wd=(ginv/rho)*(N*(Df@M)-M*(Df@N)); c_wd=c_wd/np.linalg.norm(c_wd)*cn
        c_scr=c.copy(); rng_global.shuffle(c_scr)                          # spatial scramble, same values
        c_zero=np.zeros(n)
        agg["TRUE_c"].append(hh_for_target(n,fam,c))
        agg["random_smooth"].append(hh_for_target(n,fam,c_rand))
        agg["sign_flip"].append(hh_for_target(n,fam,c_flip))
        agg["no_weight"].append(hh_for_target(n,fam,c_nw))
        agg["wrong_deriv"].append(hh_for_target(n,fam,c_wd))
        agg["scrambled_c"].append(hh_for_target(n,fam,c_scr))
        agg["zero_target"].append(hh_for_target(n,fam,c_zero))

print(f"{'target':>16} | {'mean_HH':>8} {'min_HH':>8} {'max_HH':>8}")
print("-"*48)
for k in labels:
    a=np.array(agg[k]); print(f"{k:>16} | {a.mean():>8.4f} {a.min():>8.4f} {a.max():>8.4f}")

true_mean=np.mean(agg["TRUE_c"])
decoy_means={k:np.mean(agg[k]) for k in labels if k not in ("TRUE_c","zero_target")}
best_decoy=min(decoy_means,key=decoy_means.get)
best_decoy_val=decoy_means[best_decoy]

# Also: averaged over random smooth decoys, build a distribution for a fair z-like comparison
rand_samples=[]
for fam in FAMS:
    for n in SIZES:
        c=true_c(n,fam); cn=np.linalg.norm(c)
        for s in range(20):
            cr=smooth_random_field(n,cn,np.random.default_rng(5000+s))
            rand_samples.append(hh_for_target(n,fam,cr))
rand_samples=np.array(rand_samples)
print(f"\nrandom-smooth decoy distribution: mean={rand_samples.mean():.4f}  std={rand_samples.std():.4f}  min={rand_samples.min():.4f}")
print(f"TRUE_c mean HH = {true_mean:.4f}")
sep=(rand_samples.mean()-true_mean)/(rand_samples.std()+1e-12)
print(f"separation of TRUE_c below random decoys: {sep:.2f} sigma")

print("\n--- VERDICT ---")
if true_mean < 0.5*best_decoy_val:
    print(f"PASS: TRUE_c ({true_mean:.3f}) is sharply lower than best decoy '{best_decoy}' ({best_decoy_val:.3f}).")
    print("      The metric distinguishes the true ADM target. Identification is doing real work.")
elif true_mean < best_decoy_val and sep>2:
    print(f"WEAK PASS: TRUE_c lower than decoys and {sep:.1f} sigma below random, but not dramatically.")
    print("      Identification carries some signal; not a sharp selection.")
else:
    print(f"FAIL: TRUE_c ({true_mean:.3f}) is NOT meaningfully lower than decoys (best decoy '{best_decoy}'={best_decoy_val:.3f}, random {rand_samples.mean():.3f}).")
    print("      The obstruction metric is ~blind to the target. 'HH~1.3' is generic, not physics.")
