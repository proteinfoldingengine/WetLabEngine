# V1701.17 - Full-Block Scalar Generator Necessity Audit
# Question: can admissible retained-local diagonal-ish P_N,Q_N blocks remove the
# post-frame H-H obstruction WITHOUT creating off-diagonal bracket leakage?
import numpy as np
from scipy.optimize import least_squares

SIZES=[17,33]; FAMS=["gaussian3","dipole","chirp","mixed"]

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

# Retained-local linear-in-lapse generator block builder.
# P_N(theta) = th0*diag(N) + th1*(D@diag(N)) + th2*(diag(N)@D) + th3*diag(D@N)
# Same family for Q_N with separate coeffs. All linear in N => P_M is same with M.
def Pblk(N,D,th):
    return th[0]*np.diag(N)+th[1]*(D@np.diag(N))+th[2]*(np.diag(N)@D)+th[3]*np.diag(D@N)
def Qblk(N,D,th):
    return th[0]*np.diag(N)+th[1]*(D@np.diag(N))+th[2]*(np.diag(N)@D)+th[3]*np.diag(D@N)

def blocks_for(N,M,D,rho,ginv,W,thP,thQ):
    AN,BN=omegaW(Ablk(N),Bblk(N,D,rho,ginv),W)
    AM,BM=omegaW(Ablk(M),Bblk(M,D,rho,ginv),W)
    PN=Pblk(N,D,thP); PM=Pblk(M,D,thP)
    QN=Qblk(N,D,thQ); QM=Qblk(M,D,thQ)
    return AN,BN,AM,BM,PN,PM,QN,QM

def commutator_blocks(AN,BN,AM,BM,PN,PM,QN,QM,Ag,Ak):
    C11=PN@PM-PM@PN - AN@BM + AM@BN
    C12=PN@AM - PM@AN + AN@QM - AM@QN
    C21=-BN@PM + BM@PN - QN@BM + QM@BN
    C22=QN@QM-QM@QN - BN@AM + BM@AN
    # target: C11->Ag? No. Target X_M(c): diag blocks Ag (top-left), Ak (bottom-right), off-diag 0.
    # In V1701.15 the realized identification was C11~Ag, C22~Ak. Keep that.
    Og=C11-Ag; OK=C22-Ak; Ooff1=C12; Ooff2=C21
    return Og,OK,Ooff1,Ooff2

def case(n,fam,thP,thQ):
    D=Dmat(n); rho=rho_(n,fam); ginv=ginv_(n,fam); W=rho/ginv; N,M=lapses(n)
    c=(ginv/rho)*(N*(D@M)-M*(D@N)); Ag,Ak=mom(c,D,W)
    AN,BN,AM,BM,PN,PM,QN,QM=blocks_for(N,M,D,rho,ginv,W,thP,thQ)
    Og,OK,O1,O2=commutator_blocks(AN,BN,AM,BM,PN,PM,QN,QM,Ag,Ak)
    den=np.sqrt(np.linalg.norm(Ag,"fro")**2+np.linalg.norm(Ak,"fro")**2)+1e-24
    hh=np.sqrt(np.linalg.norm(Og,"fro")**2+np.linalg.norm(OK,"fro")**2)/den
    leak=np.sqrt(np.linalg.norm(O1,"fro")**2+np.linalg.norm(O2,"fro")**2)/den
    return hh,leak

def total_residual(params, with_leak_penalty=True):
    thP=params[:4]; thQ=params[4:]
    res=[]
    for fam in FAMS:
        for n in SIZES:
            hh,leak=case(n,fam,thP,thQ)
            res.append(hh)
            if with_leak_penalty: res.append(leak)  # leakage must also be driven down
    return np.array(res)

# baseline: P=Q=0 (original off-diagonal-only generator)
base=total_residual(np.zeros(8),with_leak_penalty=False)
print(f"Baseline (P=Q=0): mean HH = {base.mean():.4f}")

# Optimize admissible P_N/Q_N to minimize HH AND leakage jointly.
best=None
for seed in range(4):
    x0=np.random.default_rng(seed).normal(scale=0.3,size=8)
    sol=least_squares(total_residual,x0,method="lm",max_nfev=800)
    if best is None or sol.cost<best.cost: best=sol

thP,thQ=best.x[:4],best.x[4:]
# Report HH and leakage separately at the optimum
hh_list=[];leak_list=[]
for fam in FAMS:
    for n in SIZES:
        hh,leak=case(n,fam,thP,thQ); hh_list.append(hh);leak_list.append(leak)
print(f"Optimized full-block: mean HH = {np.mean(hh_list):.4f}   mean leakage = {np.mean(leak_list):.4f}")
print(f"  best coeffs P_N = {np.round(thP,4)}")
print(f"  best coeffs Q_N = {np.round(thQ,4)}")

# Also: can we kill HH if we IGNORE leakage? (the 'fake solution' check)
best2=None
for seed in range(4):
    x0=np.random.default_rng(100+seed).normal(scale=0.3,size=8)
    sol=least_squares(lambda p: total_residual(p,with_leak_penalty=False),x0,method="lm",max_nfev=800)
    if best2 is None or sol.cost<best2.cost: best2=sol
thP2,thQ2=best2.x[:4],best2.x[4:]
hh2=[];lk2=[]
for fam in FAMS:
    for n in SIZES:
        hh,leak=case(n,fam,thP2,thQ2); hh2.append(hh);lk2.append(leak)
print(f"\nIgnoring leakage (fake-solution check): mean HH = {np.mean(hh2):.4f}   resulting leakage = {np.mean(lk2):.4f}")

# Stencil robustness of the honest optimum (does the P/Q solution survive 5-point D?)
def Dmat5(n):
    D=np.zeros((n,n))
    for i in range(n):
        for k,co in {1:2/3,2:-1/12}.items():
            D[i,(i+k)%n]+=co; D[i,(i-k)%n]-=co
    return D
def case5(n,fam,thP,thQ):
    D=Dmat5(n); rho=rho_(n,fam); ginv=ginv_(n,fam); W=rho/ginv; N,M=lapses(n)
    c=(ginv/rho)*(N*(D@M)-M*(D@N)); Ag,Ak=mom(c,D,W)
    AN,BN,AM,BM,PN,PM,QN,QM=blocks_for(N,M,D,rho,ginv,W,thP,thQ)
    Og,OK,O1,O2=commutator_blocks(AN,BN,AM,BM,PN,PM,QN,QM,Ag,Ak)
    den=np.sqrt(np.linalg.norm(Ag,"fro")**2+np.linalg.norm(Ak,"fro")**2)+1e-24
    return np.sqrt(np.linalg.norm(Og,"fro")**2+np.linalg.norm(OK,"fro")**2)/den
hh5=[case5(n,fam,thP,thQ) for fam in FAMS for n in SIZES]
print(f"\nHonest optimum re-tested on 5-point stencil: mean HH = {np.mean(hh5):.4f}")

# Verdict
mean_hh=np.mean(hh_list); mean_leak=np.mean(leak_list)
if mean_hh<0.1 and mean_leak<0.1:
    print("\nVERDICT: PASS - admissible full-block P_N/Q_N CLOSES H-H. Obstruction was an incomplete generator.")
elif mean_hh<0.1 and mean_leak>=0.1:
    print("\nVERDICT: PARTIAL - P_N/Q_N reduces H-H only by creating off-diagonal leakage. Not an honest close.")
elif mean_hh < 0.9*base.mean():
    print("\nVERDICT: PARTIAL - meaningful but incomplete reduction without leakage.")
else:
    print("\nVERDICT: FAIL - no admissible retained-local P_N/Q_N significantly reduces H-H without leakage.")
    print("         => candidate 1 (missing P_N/Q_N) does NOT explain the obstruction within this family.")
