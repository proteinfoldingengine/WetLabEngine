
from __future__ import annotations
import numpy as np

def pts(kind,n,seed):
    rng=np.random.default_rng(seed)
    if kind=="flat_torus":
        u=rng.uniform(0,2*np.pi,n); v=rng.uniform(0,2*np.pi,n)
        return np.c_[u,v]
    if kind=="sphere":
        X=rng.normal(size=(n,3)); X/=np.linalg.norm(X,axis=1,keepdims=True); return X
    raise ValueError(kind)

def dist(kind,P):
    if kind=="flat_torus":
        u=P[:,0]; v=P[:,1]
        du=np.abs(u[:,None]-u[None,:]); du=np.minimum(du,2*np.pi-du)
        dv=np.abs(v[:,None]-v[None,:]); dv=np.minimum(dv,2*np.pi-dv)
        return np.sqrt(du*du+dv*dv)
    return np.arccos(np.clip(P@P.T,-1,1))

def build_lap(kind,P,k=12,alpha=1.0):
    # Diffusion maps style density normalization:
    # K_ij = exp(-d^2/(4 eps)), q_i=sum_j K_ij,
    # K^alpha_ij = K_ij/(q_i^alpha q_j^alpha), then normalized Markov/Laplacian.
    D=dist(kind,P); np.fill_diagonal(D,np.inf); n=len(P)
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
    # symmetric normalized diffusion generator scaled by eps^-1
    inv=np.where(d>1e-12,1/np.sqrt(d),0)
    S=inv[:,None]*Ka*inv[None,:]
    L=(np.eye(n)-S)/(eps+1e-12)
    return L,h

def spectral_check(kind,n,seed,alpha):
    P=pts(kind,n,seed); L,h=build_lap(kind,P,alpha=alpha)
    ev=np.maximum(np.linalg.eigvalsh(L),0)
    # Use first nonzero eigenvalues as Laplace-Beltrami sanity check.
    # Unit sphere LB eigenvalues: l(l+1): first nonzero ≈2, multiplicity 3.
    # flat square torus with side 2pi has first nonzero ≈1.
    first=float(ev[1])
    second=float(ev[2])
    third=float(ev[3])
    return first,second,third,h

def run(ns=(80,120,180),reps=4):
    rows=[]
    for alpha in [0.0,0.5,1.0]:
        for kind in ["flat_torus","sphere"]:
            for n in ns:
                vals=[]; hs=[]
                for r in range(reps):
                    f,s,t,h=spectral_check(kind,n,30000+r+n*7+int(alpha*10),alpha)
                    vals.append((f,s,t)); hs.append(h)
                arr=np.array(vals)
                rows.append((alpha,kind,n,float(np.median(hs)),float(np.median(arr[:,0])),float(np.median(arr[:,1])),float(np.median(arr[:,2])),float(np.std(arr[:,0]))))
    return rows

def score(rows):
    # Choose alpha by whether sphere first eigenvalue is closer to 2 and torus first closer to 1 at largest n.
    scores={}
    for alpha in [0.0,0.5,1.0]:
        subset=[r for r in rows if r[0]==alpha and r[2]==180]
        err=0
        for _,kind,n,h,e1,e2,e3,std in subset:
            target=1.0 if kind=="flat_torus" else 2.0
            err += abs(e1-target)/target
        scores[alpha]=err
    best=min(scores,key=scores.get)
    return scores,best

def main():
    print("Graph Laplacian measure normalization verifier")
    print("="*50)
    print("Route:")
    print("diffusion-map density normalization -> Laplace-Beltrami spectral sanity checks")
    print()
    rows=run()
    print("alpha,geometry,n,h_median,lambda1_median,lambda2_median,lambda3_median,lambda1_std")
    for row in rows:
        print(",".join(str(x) for x in row))
    scores,best=score(rows)
    print(f"scores_relative_error_at_n180: {scores}")
    print(f"best_alpha: {best}")
    cls="MEASURE_NORMALIZATION_PROMISING" if scores[best] < 2.0 else "MEASURE_NORMALIZATION_WEAK"
    print(f"classification: {cls}")

if __name__=="__main__":
    main()
