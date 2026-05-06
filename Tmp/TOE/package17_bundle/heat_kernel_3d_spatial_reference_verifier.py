
from __future__ import annotations
import numpy as np

def conformal_grid_3d(N=24, amp=0.15):
    L=2*np.pi
    dx=L/N
    x=np.arange(N)*dx
    X,Y,Z=np.meshgrid(x,x,x,indexing="ij")
    # 3D conformal metric: g_ij = e^{2phi} delta_ij
    phi=amp*np.cos(X)*np.cos(Y)*np.cos(Z)
    # For n=3 and gbar flat:
    # R_g = e^{-2phi}[-4 Δphi - 2 |grad phi|^2]
    lap_phi=-3*amp*np.cos(X)*np.cos(Y)*np.cos(Z)
    phix=-amp*np.sin(X)*np.cos(Y)*np.cos(Z)
    phiy=-amp*np.cos(X)*np.sin(Y)*np.cos(Z)
    phiz=-amp*np.cos(X)*np.cos(Y)*np.sin(Z)
    grad2=phix*phix+phiy*phiy+phiz*phiz
    R=np.exp(-2*phi)*(-4*lap_phi-2*grad2)
    # volume element sqrt(g)=e^{3phi} dx^3
    dV=np.exp(3*phi)*dx**3
    rho=R*dV
    return phi,R,dV,rho,dx

def finite_difference_R_3d(phi,dx):
    lap=(np.roll(phi,1,0)+np.roll(phi,-1,0)+np.roll(phi,1,1)+np.roll(phi,-1,1)+np.roll(phi,1,2)+np.roll(phi,-1,2)-6*phi)/(dx*dx)
    phix=(np.roll(phi,-1,0)-np.roll(phi,1,0))/(2*dx)
    phiy=(np.roll(phi,-1,1)-np.roll(phi,1,1))/(2*dx)
    phiz=(np.roll(phi,-1,2)-np.roll(phi,1,2))/(2*dx)
    grad2=phix*phix+phiy*phiy+phiz*phiz
    return np.exp(-2*phi)*(-4*lap-2*grad2)

def stencil_stats(phi,dx):
    N=phi.shape[0]
    lengths=[]; weights=[]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for di,dj,dk in [(1,0,0),(0,1,0),(0,0,1)]:
                    ni=(i+di)%N; nj=(j+dj)%N; nk=(k+dk)%N
                    phimid=0.5*(phi[i,j,k]+phi[ni,nj,nk])
                    ell=np.exp(phimid)*dx
                    w=np.exp(-ell*ell/(4*dx*dx))
                    lengths.append(ell); weights.append(w)
    lengths=np.array(lengths); weights=np.array(weights)
    return {
        "nodes":N**3,
        "undirected_edges":len(lengths),
        "edge_length_min":float(lengths.min()),
        "edge_length_max":float(lengths.max()),
        "edge_length_mean":float(lengths.mean()),
        "weight_min":float(weights.min()),
        "weight_max":float(weights.max()),
        "weight_mean":float(weights.mean())
    }

def run(N=24, amp=0.15):
    phi,R,dV,rho,dx=conformal_grid_3d(N,amp)
    Rfd=finite_difference_R_3d(phi,dx)
    rel_err=float(np.sqrt(np.mean((Rfd-R)**2))/(np.sqrt(np.mean(R**2))+1e-12))
    stats=stencil_stats(phi,dx)
    out={
        "N":N,
        "amp":amp,
        "dx":float(dx),
        "int_R_dV":float(np.sum(rho)),
        "mean_R":float(np.mean(R)),
        "R_min":float(np.min(R)),
        "R_max":float(np.max(R)),
        "positive_R_fraction":float(np.mean(R>0)),
        "negative_R_fraction":float(np.mean(R<0)),
        "rho_positive_integral":float(np.sum(rho[rho>0])),
        "rho_negative_integral":float(np.sum(rho[rho<0])),
        "finite_difference_R_relative_error":rel_err,
    }
    out.update(stats)
    # In 3D no Gauss-Bonnet zero constraint for ∫R; just require exact and FD consistency + mixed signs.
    out["classification"]="CONFORMAL_3D_REFERENCE_READY" if rel_err<0.03 and out["positive_R_fraction"]>0.3 and out["negative_R_fraction"]>0.3 else "CONFORMAL_3D_REFERENCE_WEAK"
    return out

def main():
    print("3D conformal spatial reference verifier")
    print("="*50)
    print("Route:")
    print("periodic 3D conformal metric -> analytic R^(3), dV, finite-difference sanity, metric stencil")
    print()
    for k,v in run().items():
        print(f"{k}: {v}")

if __name__=="__main__":
    main()
