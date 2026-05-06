
from __future__ import annotations
import numpy as np

def pts(kind,n,seed):
    rng=np.random.default_rng(seed)
    if kind=="flat_torus":
        u=rng.uniform(0,2*np.pi,n); v=rng.uniform(0,2*np.pi,n)
        return np.c_[u,v]
    if kind=="sphere":
        X=rng.normal(size=(n,3)); X/=np.linalg.norm(X,axis=1,keepdims=True); return X
    if kind=="saddle_patch":
        # Diagnostic negative-curvature proxy; has boundary and is not compact.
        xy=rng.uniform(-1,1,(n,2))
        z=0.6*(xy[:,0]**2-xy[:,1]**2)
        return np.c_[xy,z]
    raise ValueError(kind)

def dist(kind,P):
    if kind=="flat_torus":
        u=P[:,0]; v=P[:,1]
        du=np.abs(u[:,None]-u[None,:]); du=np.minimum(du,2*np.pi-du)
        dv=np.abs(v[:,None]-v[None,:]); dv=np.minimum(dv,2*np.pi-dv)
        return np.sqrt(du*du+dv*dv)
    if kind=="sphere":
        return np.arccos(np.clip(P@P.T,-1,1))
    return np.linalg.norm(P[:,None,:]-P[None,:,:],axis=-1)

def operator(kind,P,k=10,alpha=1.0):
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
    inv=np.where(d>1e-12,1/np.sqrt(d),0)
    S=inv[:,None]*Ka*inv[None,:]
    L=(np.eye(n)-S)/(eps+1e-12)
    return L,h

def coeff_from_evals(ev,h,scale):
    ev=np.maximum(ev*scale,0)
    windows=[np.array([0.8,1.1,1.5,2.0]), np.array([1.1,1.5,2.0,2.7])]
    vals=[]
    for c in windows:
        t=c*h*h
        H=np.array([np.sum(np.exp(-tt*ev)) for tt in t])
        Y=H*((4*np.pi*t)**1)
        m,b=np.polyfit(t,Y,1)
        vals.append(6*m)
    vals=np.array(vals)
    return float(np.median(vals)), float(np.std(vals)/(abs(np.mean(vals))+1e-12))

def raw(kind,n,seed):
    P=pts(kind,n,seed); L,h=operator(kind,P)
    ev=np.linalg.eigvalsh(L)
    return ev,h,float(max(ev[1],0))

def run(n=130,reps=5):
    # flat torus scale and baseline
    lam=[]
    for r in range(reps):
        ev,h,l1=raw("flat_torus",n,90000+r)
        lam.append(l1)
    scale=1/(np.median(lam)+1e-12)
    vals={}
    cvs={}
    for kind in ["flat_torus","sphere","saddle_patch"]:
        coeffs=[]; ccvs=[]
        for r in range(reps):
            ev,h,l1=raw(kind,n,91000+r+len(kind)*101)
            c,cv=coeff_from_evals(ev,h,scale)
            coeffs.append(c); ccvs.append(cv)
        vals[kind]=np.array(coeffs)
        cvs[kind]=np.array(ccvs)
    baseline=float(np.median(vals["flat_torus"]))
    out={}
    for kind in ["flat_torus","sphere","saddle_patch"]:
        res=vals[kind]-baseline
        out[kind+"_residual_median"]=float(np.median(res))
        out[kind+"_residual_std"]=float(np.std(res))
        out[kind+"_window_cv_median"]=float(np.median(cvs[kind]))
    out["ordering_positive_flat_negative"]=bool(out["sphere_residual_median"]>out["flat_torus_residual_median"]>out["saddle_patch_residual_median"])
    out["sphere_positive"]=bool(out["sphere_residual_median"]>0)
    out["saddle_negative"]=bool(out["saddle_patch_residual_median"]<0)
    out["classification"]="SIGN_TEST_PROMISING" if out["ordering_positive_flat_negative"] and out["sphere_positive"] and out["saddle_negative"] else "SIGN_TEST_WEAK"
    out["note"]="saddle_patch is boundary/embedding proxy, not compact negative-curvature proof"
    return out

def main():
    print("Heat curvature sign tests verifier")
    print("="*50)
    print("Route:")
    print("flat baseline residuals for sphere, flat torus, and saddle proxy")
    print("Saddle is diagnostic only, not compact negative-curvature proof.")
    print()
    for k,v in run().items():
        print(f"{k}: {v}")

if __name__=="__main__":
    main()
