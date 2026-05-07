
from __future__ import annotations
import numpy as np

def grid(N=18, amp=0.25):
    L=2*np.pi; dx=L/N
    x=np.arange(N)*dx; y=np.arange(N)*dx
    X,Y=np.meshgrid(x,y,indexing="ij")
    phi=amp*np.cos(X)*np.cos(Y)
    R=4*amp*np.exp(-2*phi)*np.cos(X)*np.cos(Y)
    dV=np.exp(2*phi)*dx*dx
    rho=R*dV
    return phi,R,dV,rho,dx

def graph_laplacian(phi,dx):
    N=phi.shape[0]; n=N*N
    W=np.zeros((n,n))
    def idx(i,j): return (i%N)*N+(j%N)
    for i in range(N):
        for j in range(N):
            a=idx(i,j)
            for di,dj in [(1,0),(-1,0),(0,1),(0,-1)]:
                ni=(i+di)%N; nj=(j+dj)%N
                phimid=0.5*(phi[i,j]+phi[ni,nj])
                ell=np.exp(phimid)*dx
                w=np.exp(-ell*ell/(4*dx*dx))
                b=idx(ni,nj)
                W[a,b]=w
    W=0.5*(W+W.T)
    deg=W.sum(axis=1)
    return (np.diag(deg)-W)/(dx*dx)

def corr(a,b):
    a=np.asarray(a).ravel(); b=np.asarray(b).ravel()
    a=a-np.mean(a); b=b-np.mean(b)
    return float(np.sum(a*b)/(np.sqrt(np.sum(a*a)*np.sum(b*b))+1e-12))

def local_slope(L,dx):
    ev,V=np.linalg.eigh(L)
    ev=np.maximum(ev,0)
    V2=V*V
    times=np.array([0.7,1.0,1.4,2.0])*dx*dx
    diags=np.array([V2 @ np.exp(-t*ev) for t in times])
    Y=diags*((4*np.pi*times)[:,None])
    slopes=np.empty(L.shape[0])
    for i in range(L.shape[0]):
        m,b=np.polyfit(times,Y[:,i],1)
        slopes[i]=6*m
    return slopes

def analyze(name, field, R, rho):
    coeff=field.reshape(R.shape)
    c0=coeff-np.mean(coeff)
    R0=R-np.mean(R)
    rho0=rho-np.mean(rho)
    pos_mean=float(np.mean(c0[R>0]))
    neg_mean=float(np.mean(c0[R<0]))
    return {
        name+"_corr_R": corr(c0,R0),
        name+"_corr_RdV": corr(c0,rho0),
        name+"_sign_match": float(np.mean(np.sign(c0)==np.sign(R0))),
        name+"_pos_gt_neg": bool(pos_mean>neg_mean),
        name+"_mean_pos_R": pos_mean,
        name+"_mean_neg_R": neg_mean,
    }

def run():
    phi,R,dV,rho,dx=grid()
    L=graph_laplacian(phi,dx)
    slope=local_slope(L,dx)
    out={}
    out.update(analyze("original",slope,R,rho))
    out.update(analyze("sign_flipped",-slope,R,rho))
    out["classification"]="SIGN_CONVENTION_FLIP_PROMISING" if out["sign_flipped_corr_R"]>0.85 and out["sign_flipped_sign_match"]>0.75 and out["sign_flipped_pos_gt_neg"] else "SIGN_CONVENTION_UNRESOLVED"
    return out

def main():
    print("Local heat sign convention analysis verifier")
    print("="*50)
    print("Route:")
    print("original local heat slope vs explicit sign-flipped coefficient")
    print()
    for k,v in run().items():
        print(f"{k}: {v}")

if __name__=="__main__":
    main()
