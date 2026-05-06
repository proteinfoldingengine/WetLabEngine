
from __future__ import annotations
import numpy as np

def flat_torus_points(n, seed, aspect=1.0):
    rng=np.random.default_rng(seed)
    # rectangular flat torus: side lengths 2pi and 2pi*aspect
    u=rng.uniform(0,2*np.pi,n)
    v=rng.uniform(0,2*np.pi*aspect,n)
    return np.c_[u,v], aspect

def flat_torus_dist(P, aspect):
    L1=2*np.pi; L2=2*np.pi*aspect
    u=P[:,0]; v=P[:,1]
    du=np.abs(u[:,None]-u[None,:]); du=np.minimum(du,L1-du)
    dv=np.abs(v[:,None]-v[None,:]); dv=np.minimum(dv,L2-dv)
    return np.sqrt(du*du+dv*dv)

def operator(P, aspect, k=10, alpha=1.0):
    D=flat_torus_dist(P,aspect); np.fill_diagonal(D,np.inf); n=len(P)
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

def coeff(n, seed, aspect):
    P,asp=flat_torus_points(n,seed,aspect)
    L,h=operator(P,asp)
    ev=np.maximum(np.linalg.eigvalsh(L),0)
    # spectral scale: for rectangular torus, first eigenvalue target = min((2pi/L1)^2, (2pi/L2)^2)=min(1,1/aspect^2)
    target=min(1.0,1.0/(aspect*aspect))
    scale=target/(ev[1]+1e-12)
    evs=ev*scale
    windows=[np.array([0.8,1.1,1.5,2.0]),np.array([1.1,1.5,2.0,2.7])]
    vals=[]
    for c in windows:
        t=c*h*h
        H=np.array([np.sum(np.exp(-tt*evs)) for tt in t])
        Y=H*((4*np.pi*t)**1)
        m,b=np.polyfit(t,Y,1)
        vals.append(6*m)
    vals=np.array(vals)
    return float(np.median(vals)), float(np.std(vals)/(abs(np.mean(vals))+1e-12)), h, scale

def run(ns=(90,130), aspects=(0.75,1.0,1.5,2.0), reps=5):
    rows=[]
    for n in ns:
        for aspect in aspects:
            vals=[]; cvs=[]; hs=[]; scales=[]
            for r in range(reps):
                v,cv,h,s=coeff(n,70000+n*5+r+int(aspect*1000),aspect)
                vals.append(v); cvs.append(cv); hs.append(h); scales.append(s)
            rows.append((n,aspect,float(np.median(vals)),float(np.std(vals)),float(np.median(cvs)),float(np.median(hs)),float(np.median(scales))))
    return rows

def main():
    print("Heat kernel baseline universality verifier")
    print("="*50)
    print("Route:")
    print("flat rectangular tori with different aspect ratios -> baseline coefficient stability")
    print("No curvature target; all references have R=0.")
    print()
    rows=run()
    print("n,aspect,flat_baseline_coeff_median,flat_baseline_coeff_std,window_cv_median,h_median,spectral_scale_median")
    for row in rows:
        print(",".join(str(x) for x in row))
    # Universality: within each n, aspect variation should be small relative to seed variation
    for n in sorted(set(r[0] for r in rows)):
        subset=[r for r in rows if r[0]==n]
        meds=np.array([r[2] for r in subset])
        stds=np.array([r[3] for r in subset])
        aspect_spread=float(np.std(meds))
        seed_noise=float(np.median(stds))
        ratio=aspect_spread/(seed_noise+1e-12)
        print(f"n_{n}_aspect_spread: {aspect_spread}")
        print(f"n_{n}_seed_noise_median: {seed_noise}")
        print(f"n_{n}_aspect_spread_over_seed_noise: {ratio}")
    # classify using larger n
    subset=[r for r in rows if r[0]==max(set(rr[0] for rr in rows))]
    meds=np.array([r[2] for r in subset]); stds=np.array([r[3] for r in subset])
    ratio=float(np.std(meds)/(np.median(stds)+1e-12))
    cls="BASELINE_UNIVERSALITY_PROMISING" if ratio<1.5 else "BASELINE_UNIVERSALITY_WEAK"
    print(f"classification: {cls}")

if __name__=="__main__":
    main()
