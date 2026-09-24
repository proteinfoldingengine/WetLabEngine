#!/usr/bin/env python3
"""Scientifically scoped visualizations of the exact UQCF-GEM v15.45 scalar operator.

The published operator is the exact rational periodic-square operator
    A = (I+X)(I+Y) Delta / 8.
This script reconstructs it numerically for plotting, while independently
checking the exact rational matrix, exact kernel basis, and certified finite
spectral data before producing any figure or animation.

The torus is ONLY a visualization embedding of the periodic square. Surface
normal displacement is ONLY a visualization of scalar amplitude.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, cm

HERE=Path(__file__).resolve().parent
OUT=HERE/"artifacts"
CERTIFIED={5:(24,1,0),6:(24,12,11),7:(48,1,0),8:(48,16,15)}

def scalar_operator_exact(L):
    if type(L) is not int or L<3: raise ValueError("L")
    n=L*L
    def idx(x,y): return (x%L)*L+y%L
    rows=[]
    for x in range(L):
        for y in range(L):
            row=[Q(0)]*n
            for dx,dy in ((0,0),(1,0),(1,1),(0,1)):
                a,b=x+dx,y+dy
                row[idx(a,b)]+=Q(1,2)
                for ex,ey in ((1,0),(-1,0),(0,1),(0,-1)):
                    row[idx(a+ex,b+ey)]-=Q(1,8)
            rows.append(tuple(row))
    return tuple(rows)

def scalar_operator(L):
    return np.array(scalar_operator_exact(L),dtype=float)

def rational_rank(M):
    a=[list(r) for r in M]; pivot=0
    for col in range(len(a[0])):
        sel=next((i for i in range(pivot,len(a)) if a[i][col]),None)
        if sel is None: continue
        a[pivot],a[sel]=a[sel],a[pivot]
        u=a[pivot][col]; a[pivot]=[v/u for v in a[pivot]]
        for i in range(len(a)):
            if i==pivot: continue
            c=a[i][col]
            if c: a[i]=[x-c*y for x,y in zip(a[i],a[pivot])]
        pivot+=1
        if pivot==len(a): break
    return pivot

def kernel_basis_exact(L):
    b=[[1]*(L*L)]
    if L%2==0:
        b += [[(-1)**x*int(y==j) for x in range(L) for y in range(L)] for j in range(L)]
        b += [[(-1)**y*int(x==i) for x in range(L) for y in range(L)] for i in range(L-1)]
    return b

def verify_exact(L):
    A=scalar_operator_exact(L); rank=rational_rank(A); null=L*L-rank
    basis=kernel_basis_exact(L)
    if L in CERTIFIED and (rank,null,null-1)!=CERTIFIED[L]:
        raise AssertionError(("certified spectral mismatch",L,rank,null))
    if len(basis)!=null or rational_rank(tuple(tuple(Q(x) for x in v) for v in basis))!=null:
        raise AssertionError("kernel basis completeness")
    for v in basis:
        if any(sum(row[j]*v[j] for j in range(L*L)) for row in A):
            raise AssertionError("kernel vector not annihilated")
    return rank,null,null-1

def torus(L,R=2.15,r=.82):
    u=np.linspace(0,2*np.pi,L,endpoint=False); v=np.linspace(0,2*np.pi,L,endpoint=False)
    uu,vv=np.meshgrid(u,v,indexing="ij")
    return ((R+r*np.cos(vv))*np.cos(uu),(R+r*np.cos(vv))*np.sin(uu),r*np.sin(vv),
            np.cos(vv)*np.cos(uu),np.cos(vv)*np.sin(uu),np.sin(vv))

def wrap(a):
    return np.pad(a,((0,1),(0,1)),mode="wrap")

def draw_mode(ax,L,field,title):
    field=np.asarray(field,float).reshape(L,L)
    m=np.max(np.abs(field)); field=field/(m if m else 1)
    x,y,z,nx,ny,nz=torus(L); lift=.30*field
    ax.clear(); ax.set_axis_off(); ax.set_box_aspect((1,1,.52)); ax.view_init(22,40)
    ax.plot_surface(wrap(x+lift*nx),wrap(y+lift*ny),wrap(z+lift*nz),
                    facecolors=cm.coolwarm((wrap(field)+1)/2),rstride=1,cstride=1,
                    linewidth=.35,edgecolor="#1b2430",antialiased=True)
    ax.set_title(title,color="white",fontsize=10)

def centered_finite_condition(L):
    A=scalar_operator(L); w=np.linalg.eigvalsh(A); nz=np.abs(w)>1e-10
    vals=np.abs(w[nz])
    return float(vals.max()/vals.min())

def plot_spectrum():
    fig,axes=plt.subplots(2,2,figsize=(9,6.8),facecolor="#0b0d10")
    for ax,L in zip(axes.ravel(),(5,6,7,8)):
        rank,null,centered=verify_exact(L); w=np.sort(np.linalg.eigvalsh(scalar_operator(L)))
        ax.set_facecolor("#12151a"); ax.axhline(0,color="#555",lw=.6); ax.plot(w,"o",ms=4)
        ax.set_title(f"L={L}  exact nullity={null}  centered={centered}",color="w",fontsize=10)
        ax.tick_params(colors="#ccc",labelsize=7)
        for s in ax.spines.values(): s.set_color("#444")
    fig.suptitle("v15.45 exact periodic-square operator A=(I+X)(I+Y)Δ/8\nodd L: kernel = constants; even L: additional Nyquist-line kernel",color="white")
    fig.text(.5,.01,"Eigenvalues plotted numerically; nullities/kernel dimensions verified by exact rational arithmetic. L=6,8 are formula-extension controls.",ha="center",color="#9aa",fontsize=8)
    fig.tight_layout(rect=(0,.04,1,.88)); p=OUT/"spectrum_exact_L5678.png"; fig.savefig(p,dpi=180,bbox_inches="tight",facecolor=fig.get_facecolor()); plt.close(fig); return p

def plot_matrix(L=5):
    verify_exact(L); A=scalar_operator(L)
    fig=plt.figure(figsize=(6.6,5.8),facecolor="#0b0d10"); ax=fig.add_subplot(111)
    im=ax.imshow(A,cmap="magma",interpolation="nearest"); ax.set_title(f"v15.45 exact operator A, L={L} ({L*L}×{L*L})",color="w"); ax.tick_params(colors="#ccc")
    cb=fig.colorbar(im,ax=ax,fraction=.046); cb.ax.tick_params(colors="white")
    fig.text(.5,.01,"Numerical rendering of the exact rational matrix on the periodic-square formula domain.",ha="center",color="#9aa",fontsize=8)
    p=OUT/f"matrix_exact_L{L}.png"; fig.savefig(p,dpi=180,bbox_inches="tight",facecolor=fig.get_facecolor()); plt.close(fig); return p

def animate_modes(L=5,frames=120):
    verify_exact(L); A=scalar_operator(L); w,V=np.linalg.eigh(A); order=np.argsort(np.abs(w))[::-1]; v=V[:,order[0]]
    fig=plt.figure(figsize=(8,6.3),facecolor="#0b0d10"); ax=fig.add_subplot(111,projection="3d",facecolor="#0b0d10")
    def update(i):
        phase=np.sin(2*np.pi*i/frames)
        draw_mode(ax,L,phase*v,f"v15.45 periodic-square field visualized on torus • L={L}\nlargest-|λ| eigenmode • amplitude phase {phase:+.2f}")
        return ()
    ani=animation.FuncAnimation(fig,update,frames=frames,interval=50,blit=False)
    fig.text(.5,.012,"Torus embedding and normal displacement are visualization only; scalar operator/eigenmode are the mathematical objects.",ha="center",color="#9aa",fontsize=7.5)
    mp4=OUT/f"v1545_L{L}_largest_eigenmode.mp4"
    try: ani.save(mp4,writer=animation.FFMpegWriter(fps=20,bitrate=2200))
    except Exception:
        mp4=OUT/f"v1545_L{L}_largest_eigenmode.gif"; ani.save(mp4,writer=animation.PillowWriter(fps=20))
    plt.close(fig); return mp4

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--frames",type=int,default=120); args=ap.parse_args(); OUT.mkdir(parents=True,exist_ok=True)
    ledger={}
    for L in (5,6,7,8):
        rank,null,centered=verify_exact(L); ledger[str(L)]={"rank":rank,"nullity":null,"centered_nullity":centered}
        if L%2: ledger[str(L)]["centered_finite_condition"]=centered_finite_condition(L)
    outputs=[plot_spectrum(),plot_matrix(5),animate_modes(5,args.frames),animate_modes(7,args.frames)]
    (OUT/"verification.json").write_text(json.dumps(ledger,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"verification":ledger,"outputs":[str(p) for p in outputs]},indent=2))
if __name__=="__main__": main()
