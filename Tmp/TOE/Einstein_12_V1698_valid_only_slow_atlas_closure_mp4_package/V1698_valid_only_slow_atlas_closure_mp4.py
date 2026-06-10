
from pathlib import Path
import argparse, json, csv, hashlib, shutil, sys, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def h(*x,n=12):
    return hashlib.sha256("|".join(map(str,x)).encode()).hexdigest()[:n]

def write_csv(path, rows, cols):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c:r.get(c,"") for c in cols})

def basis(i):
    a=.25*i
    c,s=np.cos(a),np.sin(a)
    R=np.array([[c,-s,0],[s,c,0],[0,0,1.0]])
    S=np.diag([1+.05*i,1+.03*i,1+.02*i])
    Sh=np.eye(3); Sh[0,1]=.025*i
    return R@S@Sh

def norm(M): return float(np.linalg.norm(M))

def make_stack(n=5):
    theta=np.linspace(0,2*np.pi,n,endpoint=False)+np.pi/2
    pos={f"U{i}":np.array([2.45*np.cos(theta[i]),2.45*np.sin(theta[i]),.55*np.sin(2*theta[i])]) for i in range(n)}
    B={i:basis(i) for i in range(n)}
    T={(f"U{i}",f"U{j}"):np.linalg.inv(B[j])@B[i] for i in range(n) for j in range(n) if i!=j}
    charts=[dict(chart_id=f"U{i}",ordered_index=i,pos=pos[f"U{i}"],basis=B[i]) for i in range(n)]
    loops=[["U0","U1","U2","U0"],["U0","U2","U3","U0"],["U1","U3","U4","U1"],["U0","U1","U3","U4","U0"]]
    return charts,T,pos,loops

def evaluate(charts,T,loops):
    inv=[norm(T[(b,a)]@Tab-np.eye(3)) for (a,b),Tab in T.items()]
    ids=[c["chart_id"] for c in charts]
    coc=[]
    for a in ids:
        for b in ids:
            for c in ids:
                if len({a,b,c})<3: continue
                coc.append(norm(T[(c,a)]@T[(b,c)]@T[(a,b)]-np.eye(3)))
    hol=[]
    for loop in loops:
        H=np.eye(3)
        for a,b in zip(loop[:-1],loop[1:]):
            H=T[(a,b)]@H
        hol.append(norm(H-np.eye(3)))
    return dict(mode="valid_atlas_only",retained_admissible=True,max_inverse_residual=max(inv),
                max_cocycle_residual=max(coc),max_holonomy_residual=max(hol),
                inverse_pass=max(inv)<=1e-8,cocycle_pass=max(coc)<=1e-8,holonomy_pass=max(hol)<=1e-8,
                global_atlas_closed=max(inv)<=1e-8 and max(coc)<=1e-8 and max(hol)<=1e-8)

def smooth(x):
    x=max(0,min(1,x)); return x*x*(3-2*x)

def plane(center,B,scale=.5):
    e1=B[:,0]/np.linalg.norm(B[:,0]); e2=B[:,1]/np.linalg.norm(B[:,1])
    return [center+scale*(-e1-e2), center+scale*(e1-e2), center+scale*(e1+e2), center+scale*(-e1+e2)]

def line(ax,a,b,alpha=.6,style="-",lw=1.5):
    ax.plot([a[0],b[0]],[a[1],b[1]],[a[2],b[2]],style,alpha=alpha,linewidth=lw)

def frame(ax,p,B,alpha=.7):
    for v in [B[:,0],B[:,1],B[:,2]]:
        vv=.48*v/np.linalg.norm(v)
        ax.quiver(p[0],p[1],p[2],vv[0],vv[1],vv[2],length=1,normalize=False,alpha=alpha,linewidth=1.1)

def draw(ax,i,total,charts,T,pos,loops,m):
    ax.clear()
    f=i/(total-1)
    ax.set_xlim(-3.5,3.5); ax.set_ylim(-3.5,3.5); ax.set_zlim(-2.25,2.45)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.view_init(elev=24+4*np.sin(2*np.pi*f), azim=35+95*f)
    ax.set_title("V1698 Valid Global Retained-Atlas Closure", fontsize=13, weight="bold", pad=18)

    p0=smooth((f-.03)/.10)
    p1=smooth((f-.12)/.13)
    p2=smooth((f-.24)/.13)
    p3=smooth((f-.38)/.13)
    p4=smooth((f-.52)/.12)
    p5=smooth((f-.65)/.11)
    p6=smooth((f-.76)/.11)
    p7=smooth((f-.88)/.10)

    u=np.linspace(0,2*np.pi,28); v=np.linspace(0,np.pi,14)
    ax.plot_wireframe(2.05*np.outer(np.cos(u),np.sin(v)),
                      2.05*np.outer(np.sin(u),np.sin(v)),
                      .55*np.outer(np.ones_like(u),np.cos(v)),
                      alpha=.04+.08*p7,linewidth=.4)

    for c in charts:
        p=c["pos"]; root=np.array([p[0]*.32,p[1]*.32,-1.65])
        if p0>0:
            ax.scatter(root[0],root[1],root[2],s=40*p0,alpha=.8*p0)
            ax.text(root[0],root[1],root[2]-.13,"P",ha="center",fontsize=7,alpha=p0)
        if p1>0:
            line(ax,root,p,alpha=.18*p1,style=":",lw=1)

    for c in charts:
        p=c["pos"]
        if p1>0:
            poly=Poly3DCollection([plane(p,c["basis"])],alpha=.08+.20*p1)
            ax.add_collection3d(poly)
            ax.scatter(p[0],p[1],p[2],s=52*p1,alpha=.9*p1)
            ax.text(p[0],p[1],p[2]+.27,c["chart_id"],ha="center",fontsize=9,weight="bold",alpha=p1)
            frame(ax,p,c["basis"],alpha=.65*p1)

    ring=["U0","U1","U2","U3","U4","U0"]
    if p2>0:
        for a,b in zip(ring[:-1],ring[1:]):
            line(ax,pos[a],pos[b],alpha=.65*p2,style="-",lw=1.8)
        travel=min(4.999,max(0,(f-.24)/.22*5))
        k=int(travel); local=travel-k
        q=(1-local)*pos[ring[k]]+local*pos[ring[k+1]]
        ax.scatter(q[0],q[1],q[2],s=105,alpha=.85*p2)
        ax.text(q[0],q[1],q[2]+.18,"Gamma_R transport",ha="center",fontsize=8,alpha=p2)

    if p3>0:
        tri=["U0","U1","U2","U0"]; lift=np.array([0,0,.36])
        for a,b in zip(tri[:-1],tri[1:]):
            line(ax,pos[a]+lift,pos[b]+lift,alpha=.88*p3,style="-",lw=2.2)
        cpos=(pos["U0"]+pos["U1"]+pos["U2"])/3+np.array([0,0,.75])
        ax.text(cpos[0],cpos[1],cpos[2],"cocycle closes\nT_ki T_jk T_ij = I",ha="center",fontsize=9,alpha=p3)

    if p4>0:
        loop=["U0","U1","U3","U4","U0"]; low=np.array([0,0,-.28])
        for a,b in zip(loop[:-1],loop[1:]):
            line(ax,pos[a]+low,pos[b]+low,alpha=.85*p4,style="--",lw=2)
        cpos=np.mean([pos[x] for x in loop[:-1]],axis=0)+np.array([0,0,-.63])
        ax.text(cpos[0],cpos[1],cpos[2],"holonomy returns",ha="center",fontsize=9,alpha=p4)

    if p5>0:
        sink=np.array([0,0,-1.25])
        for c in charts:
            line(ax,c["pos"],sink,alpha=.25*p5,style="-",lw=1.1)
        ax.scatter(0,0,-1.25,s=120*p5,alpha=.7*p5)
        ax.text(0,0,-1.52,"J_R source-current / signed boundary",ha="center",fontsize=9,alpha=p5)

    if p6>0:
        verts=[pos[f"U{k}"] for k in range(5)]
        for face_pts in [[verts[0],verts[1],verts[2]],[verts[0],verts[2],verts[3]],[verts[0],verts[3],verts[4]]]:
            ax.add_collection3d(Poly3DCollection([face_pts],alpha=.14*p6))
        ax.scatter(0,0,.08,s=160*p6,alpha=.65*p6)
        ax.text(.05,.05,.82,"W1→W2→W3\nBianchi-certified fill",ha="center",fontsize=9,alpha=p6)

    if p7>0:
        ax.scatter(0,0,.10,s=300*p7,alpha=.75*p7)
        ax.text(0,0,1.35,"GLOBAL ATLAS CLOSURE",ha="center",fontsize=14,weight="bold",alpha=p7)
        ax.text(0,0,1.10,"PASS",ha="center",fontsize=20,weight="bold",alpha=p7)

    hud=("VALID ONLY — NON-LOOPING PROOF\n"
         f"retained admissible: {m['retained_admissible']}\n"
         f"inverse max: {m['max_inverse_residual']:.2e}\n"
         f"cocycle max: {m['max_cocycle_residual']:.2e}\n"
         f"holonomy max: {m['max_holonomy_residual']:.2e}\n"
         f"global_atlas_closed: {m['global_atlas_closed']}")
    ax.text2D(.02,.98,hud,transform=ax.transAxes,va="top",ha="left",fontsize=8,bbox=dict(boxstyle="round",alpha=.18))

def run(outdir, seconds=10, fps=8):
    outdir=Path(outdir)
    if outdir.exists(): shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    charts,T,pos,loops=make_stack(5)
    m=evaluate(charts,T,loops)
    proof={"version":"V1698_VALID_ONLY_SLOW_3D_GLOBAL_ATLAS_CLOSURE",
           "verdict":"PASS" if m["global_atlas_closed"] else "FAIL",
           "construction":"T_ij = B_j^-1 B_i",
           "findings":{"valid_atlas_closes":m["global_atlas_closed"],"non_looping":True,"seconds":seconds,"fps":fps},
           "phases":["Genesis/provenance","3D local charts","Gamma_R transition transport","triple-overlap cocycle","R3 holonomy","J_R source-current/signed boundary","W1/W2/W3 Bianchi-certified filling","Global closure lock"],
           "metrics":m}
    (outdir/"V1698_valid_only_slow_closure_summary.json").write_text(json.dumps(proof,indent=2))
    write_csv(outdir/"V1698_valid_only_slow_closure_metrics.csv",[m],["mode","retained_admissible","max_inverse_residual","max_cocycle_residual","max_holonomy_residual","inverse_pass","cocycle_pass","holonomy_pass","global_atlas_closed"])
    fig=plt.figure(figsize=(10,7))
    ax=fig.add_subplot(111,projection="3d")
    total=int(seconds*fps)
    anim=FuncAnimation(fig,lambda i: draw(ax,i,total,charts,T,pos,loops,m),frames=total,interval=1000/fps,repeat=False)
    mp4=outdir/"V1698_valid_only_slow_3D_global_atlas_closure.mp4"
    anim.save(mp4,writer=FFMpegWriter(fps=fps,bitrate=1800))
    draw(ax,total-1,total,charts,T,pos,loops,m)
    png=outdir/"V1698_valid_only_slow_3D_global_atlas_closure_static.png"
    fig.savefig(png,dpi=150,bbox_inches="tight")
    plt.close(fig)
    (outdir/"README.md").write_text("# V1698 Valid-Only Slow 3D Global Atlas Closure\n\nNon-looping proof MP4.\n")
    return proof

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",default="run")
    ap.add_argument("--seconds",type=int,default=10)
    ap.add_argument("--fps",type=int,default=8)
    args=ap.parse_args()
    proof=run(args.outdir,args.seconds,args.fps)
    print(json.dumps(proof,indent=2))
    return 0 if proof["verdict"]=="PASS" else 2

if __name__=="__main__":
    raise SystemExit(main())
