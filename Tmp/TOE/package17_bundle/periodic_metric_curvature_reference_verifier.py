
from __future__ import annotations
import numpy as np

def sample_torus_metric(n, seed, amp=0.25, mode="mixed"):
    rng=np.random.default_rng(seed)
    x=rng.uniform(0,2*np.pi,n)
    y=rng.uniform(0,2*np.pi,n)
    if mode=="flat":
        phi=np.zeros(n)
        R=np.zeros(n)
    elif mode=="mixed":
        # phi = a cos x cos y, periodic.
        # R = -2 e^{-2phi} Δphi = 4a e^{-2phi} cos x cos y
        phi=amp*np.cos(x)*np.cos(y)
        R=4*amp*np.exp(-2*phi)*np.cos(x)*np.cos(y)
    elif mode=="mostly_negative":
        # phi = -a(cos x + cos y); R=-2e^-2phi * a(cos x+cos y) has mixed sign.
        # We'll sample weighted region where R tends negative by selecting around cos sums positive
        phi=-amp*(np.cos(x)+np.cos(y))
        R=-2*amp*np.exp(-2*phi)*(np.cos(x)+np.cos(y))
    else:
        raise ValueError(mode)
    return np.c_[x,y], phi, R

def periodic_base_dist(P):
    x=P[:,0]; y=P[:,1]
    dx=np.abs(x[:,None]-x[None,:]); dx=np.minimum(dx,2*np.pi-dx)
    dy=np.abs(y[:,None]-y[None,:]); dy=np.minimum(dy,2*np.pi-dy)
    return np.sqrt(dx*dx+dy*dy)

def operator(P, phi, k=10, alpha=1.0):
    # Approx local conformal distance: ds=e^phi sqrt(dx^2+dy^2); pair scale by average e^phi.
    D0=periodic_base_dist(P)
    scale=np.exp((phi[:,None]+phi[None,:])/2)
    D=D0*scale
    np.fill_diagonal(D,np.inf)
    n=len(P)
    nbr=np.argsort(D,axis=1)[:,:k]
    h=np.median([D[i,j] for i in range(n) for j in nbr[i]])
    eps=h*h
    K=np.zeros((n,n))
    for i in range(n):
        for j in nbr[i]:
            w=np.exp(-D[i,j]**2/(4*eps+1e-12))
            K[i,j]=max(K[i,j],w); K[j,i]=max(K[j,i],w)
    q=np.sum(K,axis=1)+1e-12
    Ka=K/(q[:,None]**alpha*q[None,:]**alpha)
    d=np.sum(Ka,axis=1)+1e-12
    inv=np.where(d>1e-12,1/np.sqrt(d),0)
    S=inv[:,None]*Ka*inv[None,:]
    L=(np.eye(n)-S)/(eps+1e-12)
    return L,h

def coeff(P,phi,scale):
    L,h=operator(P,phi)
    ev=np.maximum(np.linalg.eigvalsh(L)*scale,0)
    windows=[np.array([0.8,1.1,1.5,2.0]), np.array([1.1,1.5,2.0,2.7])]
    vals=[]
    for c in windows:
        t=c*h*h
        H=np.array([np.sum(np.exp(-tt*ev)) for tt in t])
        Y=H*((4*np.pi*t)**1)
        m,b=np.polyfit(t,Y,1)
        vals.append(6*m)
    vals=np.array(vals)
    return float(np.median(vals)), float(np.std(vals)/(abs(np.mean(vals))+1e-12)), h

def flat_scale(n,reps=4):
    lams=[]
    for r in range(reps):
        P,phi,R=sample_torus_metric(n,100000+r,mode="flat")
        L,h=operator(P,phi)
        ev=np.linalg.eigvalsh(L)
        lams.append(max(ev[1],0))
    return 1/(np.median(lams)+1e-12)

def run(n=130,reps=6):
    scale=flat_scale(n)
    rows=[]
    # Baseline from flat
    flat_coeff=[]
    for r in range(reps):
        P,phi,R=sample_torus_metric(n,101000+r,mode="flat")
        c,cv,h=coeff(P,phi,scale)
        flat_coeff.append(c)
    baseline=float(np.median(flat_coeff))
    for mode in ["flat","mixed","mostly_negative"]:
        cs=[]; cvs=[]; intRs=[]; meanRs=[]
        for r in range(reps):
            P,phi,R=sample_torus_metric(n,102000+r+len(mode)*37,mode=mode)
            c,cv,h=coeff(P,phi,scale)
            cs.append(c-baseline); cvs.append(cv)
            # approximate integral with volume weight e^{2phi} dxdy over torus = mean(R e^{2phi})*(2pi)^2
            intR=float(np.mean(R*np.exp(2*phi))*(2*np.pi)**2)
            intRs.append(intR); meanRs.append(float(np.mean(R)))
        rows.append((mode,float(np.median(cs)),float(np.std(cs)),float(np.median(cvs)),float(np.median(intRs)),float(np.median(meanRs))))
    return scale,baseline,rows

def main():
    print("Periodic metric curvature reference verifier")
    print("="*50)
    print("Route:")
    print("intrinsic periodic conformal metrics with computable scalar curvature")
    print("Diagnostic only; distance approximation is local conformal.")
    print()
    scale,baseline,rows=run()
    print(f"flat_lambda1_scale: {scale}")
    print(f"flat_baseline_coeff: {baseline}")
    print("mode,residual_coeff_median,residual_coeff_std,window_cv_median,analytic_intR_approx,analytic_meanR")
    for row in rows:
        print(",".join(str(x) for x in row))
    # Mixed conformal metric on torus should have total integral ~0 by Gauss-Bonnet, but local signs.
    # Mostly_negative mode also total integral should be ~0 for closed torus if exact, but sample may skew mean R.
    flat=[r for r in rows if r[0]=="flat"][0]
    mixed=[r for r in rows if r[0]=="mixed"][0]
    neg=[r for r in rows if r[0]=="mostly_negative"][0]
    local_response=abs(mixed[1]-flat[1])>5 or abs(neg[1]-flat[1])>5
    analytic_consistent=abs(mixed[4])<1e-10 and abs(neg[4])<1e-10
    print(f"local_metric_response_detected: {local_response}")
    print(f"gauss_bonnet_integral_near_zero: {analytic_consistent}")
    cls="PERIODIC_METRIC_DIAGNOSTIC_PROMISING" if local_response and analytic_consistent else "PERIODIC_METRIC_DIAGNOSTIC_WEAK"
    print(f"classification: {cls}")

if __name__=="__main__":
    main()
