
from __future__ import annotations
import numpy as np

def make_points(kind,n,seed):
    rng=np.random.default_rng(seed)
    if kind=="plane_patch":
        xy=rng.uniform(-1,1,(n,2)); X=np.c_[xy,np.zeros(n)]
    elif kind=="flat_torus":
        # intrinsic flat 2-torus embedded in 4D, then use ambient chord distances
        u=rng.uniform(0,2*np.pi,n); v=rng.uniform(0,2*np.pi,n)
        X=np.c_[np.cos(u),np.sin(u),np.cos(v),np.sin(v)]
    elif kind=="sphere":
        X=rng.normal(size=(n,3)); X/=np.linalg.norm(X,axis=1,keepdims=True)
    elif kind=="saddle_patch":
        xy=rng.uniform(-1,1,(n,2)); X=np.c_[xy,0.55*(xy[:,0]**2-xy[:,1]**2)]
    else: raise ValueError(kind)
    return X

def laplacian(X,k=12,normalized=False):
    n=len(X)
    D=np.linalg.norm(X[:,None,:]-X[None,:,:],axis=-1)
    np.fill_diagonal(D,np.inf)
    nbr=np.argsort(D,axis=1)[:,:k]
    h=np.median([D[i,j] for i in range(n) for j in nbr[i]])
    W=np.zeros((n,n))
    for i in range(n):
        for j in nbr[i]:
            w=np.exp(-D[i,j]**2/(2*h*h+1e-12))
            W[i,j]=max(W[i,j],w); W[j,i]=max(W[j,i],w)
    deg=np.sum(W,axis=1)
    if normalized:
        inv=np.where(deg>1e-12,1/np.sqrt(deg),0)
        L=np.eye(n)-inv[:,None]*W*inv[None,:]
        return L,h
    else:
        L=(np.diag(deg)-W)/(h*h+1e-12)
        return L,h

def coeff(X,k=12,normalized=False,window=(0.35,0.5,0.7,1.0,1.4,2.0),d=2):
    L,h=laplacian(X,k,normalized)
    evals=np.maximum(np.linalg.eigvalsh(L),0)
    cgrid=np.array(window)
    tgrid=cgrid if normalized else cgrid*h*h
    H=np.array([np.sum(np.exp(-t*evals)) for t in tgrid])
    Y=H*((4*np.pi*tgrid)**(d/2))
    slope,intercept=np.polyfit(tgrid,Y,1)
    return 6*slope, intercept, h

def run(n=180,reps=5):
    kinds=["plane_patch","flat_torus","sphere","saddle_patch"]
    configs=[("unnormalized_h2",(False,(0.35,0.5,0.7,1,1.4,2))),
             ("unnormalized_smaller_window",(False,(0.08,0.12,0.18,0.25,0.35))),
             ("normalized_dimensionless",(True,(0.25,0.5,1,2,4)))]
    rows=[]
    for cname,(norm,win) in configs:
        for kind in kinds:
            vals=[]; a0=[]; hs=[]
            for r in range(reps):
                X=make_points(kind,n,7100+r+len(kind)*101)
                v,b,h=coeff(X,normalized=norm,window=win)
                vals.append(v); a0.append(b); hs.append(h)
            rows.append((cname,kind,float(np.median(vals)),float(np.std(vals)),float(np.median(a0)),float(np.median(hs))))
    return rows

def main():
    print("Heat kernel failure analysis verifier")
    print("="*50)
    print("Route:")
    print("test sign/magnitude sensitivity to boundary, Laplacian normalization, and heat window")
    print()
    print("config,geometry,intR_coeff_median,intR_coeff_std,A0_median,h_median")
    rows=run()
    for row in rows:
        print(",".join(str(x) for x in row))
    print()
    print("diagnosis:")
    print("if flat_torus differs strongly from plane_patch, boundary/embedding/graph construction matters")
    print("if signs flip across windows/configs, coefficient sign is not stable")
    print("if normalized config suppresses separation, scale information is erased")

if __name__=="__main__":
    main()
