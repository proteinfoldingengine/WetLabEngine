
from __future__ import annotations
import numpy as np

def grid3(N=32, amp=0.15):
    L=2*np.pi; dx=L/N
    x=np.arange(N)*dx
    X,Y,Z=np.meshgrid(x,x,x,indexing="ij")
    phi=amp*np.cos(X)*np.cos(Y)*np.cos(Z)
    lap_phi=-3*amp*np.cos(X)*np.cos(Y)*np.cos(Z)
    phix=-amp*np.sin(X)*np.cos(Y)*np.cos(Z)
    phiy=-amp*np.cos(X)*np.sin(Y)*np.cos(Z)
    phiz=-amp*np.cos(X)*np.cos(Y)*np.sin(Z)
    grad2=phix*phix+phiy*phiy+phiz*phiz
    R=np.exp(-2*phi)*(-4*lap_phi-2*grad2)
    sqrt_h=np.exp(3*phi)
    dV=sqrt_h*dx**3
    rho=R*dV
    return phi,R,sqrt_h,dV,rho,dx

def degree_proxy(phi, dx):
    N=phi.shape[0]
    deg=np.zeros_like(phi)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                s=0.0
                for di,dj,dk in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    ni=(i+di)%N; nj=(j+dj)%N; nk=(k+dk)%N
                    phimid=0.5*(phi[i,j,k]+phi[ni,nj,nk])
                    ell=np.exp(phimid)*dx
                    s += np.exp(-ell*ell/(4*dx*dx))
                deg[i,j,k]=s
    return deg

def corr(a,b):
    a=np.asarray(a).ravel(); b=np.asarray(b).ravel()
    a=a-np.mean(a); b=b-np.mean(b)
    return float(np.sum(a*b)/(np.sqrt(np.sum(a*a)*np.sum(b*b))+1e-12))

def metrics_for(N, amp):
    phi,R,sqrt_h,dV,rho,dx=grid3(N, amp)
    deg=degree_proxy(phi,dx)
    deg0=deg-np.mean(deg)
    # candidate global zero-mode predictors
    mean_R=float(np.mean(R))
    vol=float(np.sum(dV))
    int_RdV=float(np.sum(rho))
    mean_R_vol=float(int_RdV/vol)
    candidates={
        "amp": amp,
        "N": N,
        "dx": float(dx),
        "mean_R_arithmetic": mean_R,
        "mean_R_volume": mean_R_vol,
        "int_RdV": int_RdV,
        "volume": vol,
        "mean_phi": float(np.mean(phi)),
        "var_phi": float(np.var(phi)),
        "mean_degree": float(np.mean(deg)),
        "var_degree": float(np.var(deg)),
        "mean_neg_degree_deficit": float(np.mean(6.0-deg)),
        "int_degree_deficit_dV": float(np.sum((6.0-deg)*dV)),
        "int_centered_degree_sq_dV": float(np.sum((deg0**2)*dV)),
        "corr_minus_degree_R": corr(-(deg-np.mean(deg)), R),
        "corr_minus_degree_RdV": corr(-(deg-np.mean(deg)), rho),
    }
    return candidates

def fit_linear(x,y):
    x=np.asarray(x,dtype=float); y=np.asarray(y,dtype=float)
    A=np.vstack([np.ones_like(x), x]).T
    coef=np.linalg.lstsq(A,y,rcond=None)[0]
    pred=A@coef
    rel=float(np.linalg.norm(pred-y)/(np.linalg.norm(y)+1e-12))
    r2=float(1-np.sum((y-pred)**2)/(np.sum((y-np.mean(y))**2)+1e-12))
    return coef,pred,rel,r2

def run():
    # Vary amplitude so zero mode changes; test whether graph globals predict int R dV / volume mean.
    amps=[0.05,0.08,0.10,0.12,0.15,0.18,0.20,0.25]
    N=32
    rows=[metrics_for(N,a) for a in amps]
    y=np.array([r["mean_R_volume"] for r in rows])
    predictors=["var_phi","mean_degree","var_degree","mean_neg_degree_deficit","int_degree_deficit_dV","int_centered_degree_sq_dV"]
    fits=[]
    for p in predictors:
        x=np.array([r[p] for r in rows])
        coef,pred,rel,r2=fit_linear(x,y)
        fits.append((p,float(coef[0]),float(coef[1]),rel,r2))
    return rows,fits

def main():
    print("ADM spatial zero-mode recovery verifier")
    print("="*50)
    print("Route:")
    print("vary conformal amplitude, test graph/global observables as predictors of volume-mean R^(3)")
    print()
    rows,fits=run()
    print("AMPLITUDE_ROWS:")
    print("amp,N,dx,mean_R_volume,int_RdV,volume,var_phi,mean_degree,var_degree,mean_neg_degree_deficit,int_degree_deficit_dV,int_centered_degree_sq_dV,corr_minus_degree_R,corr_minus_degree_RdV")
    for r in rows:
        print(",".join(str(r[k]) for k in ["amp","N","dx","mean_R_volume","int_RdV","volume","var_phi","mean_degree","var_degree","mean_neg_degree_deficit","int_degree_deficit_dV","int_centered_degree_sq_dV","corr_minus_degree_R","corr_minus_degree_RdV"]))
    print("FITS:")
    print("predictor,intercept,slope,relative_error,R2")
    for f in fits:
        print(",".join(str(x) for x in f))
    best=max(fits,key=lambda z:z[4])
    print(f"best_predictor: {best[0]}")
    print(f"best_R2: {best[4]}")
    print(f"best_relative_error: {best[3]}")
    cls="ZERO_MODE_GRAPH_GLOBAL_PROMISING" if best[4]>0.99 and best[3]<0.08 else "ZERO_MODE_GRAPH_GLOBAL_WEAK"
    print(f"classification: {cls}")

if __name__=="__main__":
    main()
