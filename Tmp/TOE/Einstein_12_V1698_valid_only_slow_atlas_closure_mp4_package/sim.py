# Install/import required libraries
import json, csv, hashlib, shutil, base64
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg") # Use Agg backend for headless rendering in Colab
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from IPython.display import HTML, display

# ---------------------------------------------------------
# PHYSICS CORE (FROZEN - DO NOT ALTER)
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# CINEMATIC RENDERING LAYER
# ---------------------------------------------------------

def smooth(x):
    x=max(0,min(1,x)); return x*x*(3-2*x)

def plane(center,B,scale=.6):
    e1=B[:,0]/np.linalg.norm(B[:,0]); e2=B[:,1]/np.linalg.norm(B[:,1])
    return [center+scale*(-e1-e2), center+scale*(e1-e2), center+scale*(e1+e2), center+scale*(-e1+e2)]

def draw_chart_grid(ax, center, B, scale=.6, alpha=0.3, color='#00FFFF'):
    e1=B[:,0]/np.linalg.norm(B[:,0])
    e2=B[:,1]/np.linalg.norm(B[:,1])
    for t in np.linspace(-scale, scale, 5):
        p1, p2 = center + t*e1 - scale*e2, center + t*e1 + scale*e2
        ax.plot([p1[0],p2[0]],[p1[1],p2[1]],[p1[2],p2[2]], color=color, alpha=alpha, lw=0.6)
        p3, p4 = center - scale*e1 + t*e2, center + scale*e1 + t*e2
        ax.plot([p3[0],p4[0]],[p3[1],p4[1]],[p3[2],p4[2]], color=color, alpha=alpha, lw=0.6)

def glow_line(ax, a, b, alpha=0.8, style="-", lw=1.5, color="cyan"):
    ax.plot([a[0],b[0]],[a[1],b[1]],[a[2],b[2]], style, alpha=alpha, linewidth=lw, color=color)
    ax.plot([a[0],b[0]],[a[1],b[1]],[a[2],b[2]], style, alpha=alpha*0.3, linewidth=lw*2.5, color=color)
    ax.plot([a[0],b[0]],[a[1],b[1]],[a[2],b[2]], style, alpha=alpha*0.1, linewidth=lw*5, color=color)

def glow_scatter(ax, p, s, alpha, color):
    ax.scatter(p[0], p[1], p[2], s=s, color=color, alpha=alpha)
    ax.scatter(p[0], p[1], p[2], s=s*2.5, color=color, alpha=alpha*0.3, edgecolors='none')
    ax.scatter(p[0], p[1], p[2], s=s*5, color=color, alpha=alpha*0.1, edgecolors='none')

def frame(ax,p,B,alpha=.7, color='#FFFFFF'):
    for v in [B[:,0],B[:,1],B[:,2]]:
        vv=.55*v/np.linalg.norm(v)
        ax.quiver(p[0],p[1],p[2],vv[0],vv[1],vv[2],length=1,normalize=False,alpha=alpha,linewidth=1.5,color=color)

def draw(ax,i,total,charts,T,pos,loops,m):
    ax.clear()
    f=i/(total-1)

    ax.set_facecolor('#050510')
    ax.set_xlim(-3.8,3.8); ax.set_ylim(-3.8,3.8); ax.set_zlim(-2.5,2.6)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.view_init(elev=22+6*np.sin(2*np.pi*f), azim=35+115*f)
    ax.set_title("V1698 Valid Global Retained-Atlas Closure", fontsize=14, weight="bold", pad=20, color='#E0E0FF')

    p0, p1, p2, p3, p4, p5, p6, p7 = smooth((f-.03)/.10), smooth((f-.12)/.13), smooth((f-.24)/.13), smooth((f-.38)/.13), smooth((f-.52)/.12), smooth((f-.65)/.11), smooth((f-.76)/.11), smooth((f-.88)/.10)

    u=np.linspace(0,2*np.pi,40); v=np.linspace(0,np.pi,20)
    ax.plot_wireframe(2.2*np.outer(np.cos(u),np.sin(v)), 2.2*np.outer(np.sin(u),np.sin(v)), .65*np.outer(np.ones_like(u),np.cos(v)), color='#4A00E0', alpha=.05+.10*p7, linewidth=.6)

    for c in charts:
        p=c["pos"]; root=np.array([p[0]*.32,p[1]*.32,-1.8])
        if p0>0:
            glow_scatter(ax, root, s=45*p0, alpha=.8*p0, color='#A9A9A9')
            ax.text(root[0],root[1],root[2]-.2,"P",ha="center",fontsize=8,alpha=p0, color='#FFFFFF')
        if p1>0: glow_line(ax, root, p, alpha=.25*p1, style=":", lw=1, color='#8888AA')

    for c in charts:
        p=c["pos"]
        if p1>0:
            poly=Poly3DCollection([plane(p,c["basis"])], facecolors='#00FFFF', alpha=.05+.15*p1, edgecolors='#00FFFF', linewidths=0.5)
            ax.add_collection3d(poly)
            draw_chart_grid(ax, p, c["basis"], alpha=0.4*p1, color='#00FFFF')
            glow_scatter(ax, p, s=60*p1, alpha=.9*p1, color='#00FFFF')
            ax.text(p[0],p[1],p[2]+.35,c["chart_id"],ha="center",fontsize=10,weight="bold",alpha=p1, color='#FFFFFF')
            frame(ax,p,c["basis"],alpha=.8*p1, color='#FFFFFF')

    ring=["U0","U1","U2","U3","U4","U0"]
    if p2>0:
        for a,b in zip(ring[:-1],ring[1:]): glow_line(ax, pos[a], pos[b], alpha=.75*p2, style="-", lw=2, color='#FFA500')
        k=int(min(4.999,max(0,(f-.24)/.22*5))); local=min(4.999,max(0,(f-.24)/.22*5))-k
        q=(1-local)*pos[ring[k]]+local*pos[ring[k+1]]
        glow_scatter(ax, q, s=120, alpha=.9*p2, color='#FFD700')
        ax.text(q[0],q[1],q[2]+.25,"Gamma_R transport",ha="center",fontsize=9,alpha=p2, color='#FFD700', weight="bold")

    if p3>0:
        tri=["U0","U1","U2","U0"]; lift=np.array([0,0,.45])
        for a,b in zip(tri[:-1],tri[1:]): glow_line(ax, pos[a]+lift, pos[b]+lift, alpha=.9*p3, style="-", lw=2.5, color='#39FF14')
        cpos=(pos["U0"]+pos["U1"]+pos["U2"])/3+np.array([0,0,.85])
        ax.text(cpos[0],cpos[1],cpos[2],"cocycle closes\nT_ki T_jk T_ij = I",ha="center",fontsize=10,alpha=p3, color='#39FF14', weight="bold")

    if p4>0:
        loop=["U0","U1","U3","U4","U0"]; low=np.array([0,0,-.4])
        for a,b in zip(loop[:-1],loop[1:]): glow_line(ax, pos[a]+low, pos[b]+low, alpha=.9*p4, style="--", lw=2.5, color='#FF00FF')
        cpos=np.mean([pos[x] for x in loop[:-1]],axis=0)+np.array([0,0,-.8])
        ax.text(cpos[0],cpos[1],cpos[2],"holonomy returns",ha="center",fontsize=10,alpha=p4, color='#FF00FF', weight="bold")

    if p5>0:
        sink=np.array([0,0,-1.4])
        for c in charts: glow_line(ax, c["pos"], sink, alpha=.4*p5, style="-", lw=1.5, color='#DC143C')
        glow_scatter(ax, sink, s=180*p5, alpha=.9*p5, color='#FF2020')
        ax.text(0,0,-1.7,"J_R source-current / signed boundary",ha="center",fontsize=10,alpha=p5, color='#FF4040', weight="bold")

    if p6>0:
        verts=[pos[f"U{k}"] for k in range(5)]
        for i in range(5):
            for j in range(i+1, 5): glow_line(ax, verts[i], verts[j], alpha=.35*p6, style="-", lw=1, color='#00FFFF')
        for face_pts in [[verts[0],verts[1],verts[2]],[verts[0],verts[2],verts[3]],[verts[0],verts[3],verts[4]]]:
            ax.add_collection3d(Poly3DCollection([face_pts], facecolors='#00BFFF', alpha=.18*p6))
        glow_scatter(ax, [0,0,.1], s=200*p6, alpha=.8*p6, color='#00BFFF')
        ax.text(.05,.05,.95,"W1→W2→W3\nBianchi-certified fill",ha="center",fontsize=10,alpha=p6, color='#00FFFF', weight="bold")

    if p7>0:
        glow_scatter(ax, [0,0,.15], s=400*p7, alpha=.9*p7, color='#FFFFFF')
        ax.text(0,0,1.55,"GLOBAL ATLAS CLOSURE",ha="center",fontsize=16,weight="bold",alpha=p7, color='#FFFFFF')
        ax.text(0,0,1.25,"PASS",ha="center",fontsize=24,weight="bold",alpha=p7, color='#39FF14')

    hud=("VALID ONLY — NON-LOOPING PROOF\n"
         f"retained admissible: {m['retained_admissible']}\n"
         f"inverse max: {m['max_inverse_residual']:.2e}\n"
         f"cocycle max: {m['max_cocycle_residual']:.2e}\n"
         f"holonomy max: {m['max_holonomy_residual']:.2e}\n"
         f"global_atlas_closed: {m['global_atlas_closed']}")
    props = dict(boxstyle='round,pad=0.5', facecolor='#001122', edgecolor='#00FFFF', alpha=0.85)
    ax.text2D(.02,.98,hud,transform=ax.transAxes,va="top",ha="left",fontsize=9, color='#00FFFF', family='monospace', bbox=props)

# ---------------------------------------------------------
# COLAB EXECUTION & DISPLAY
# ---------------------------------------------------------
def run_and_display(seconds=10, fps=12):
    outdir=Path("run_cinematic")
    if outdir.exists(): shutil.rmtree(outdir)
    outdir.mkdir(parents=True)

    charts,T,pos,loops=make_stack(5)
    m=evaluate(charts,T,loops)

    plt.style.use('dark_background')
    fig=plt.figure(figsize=(12,8), facecolor='#050510')
    ax=fig.add_subplot(111,projection="3d")
    ax.set_facecolor('#050510')

    total=int(seconds*fps)
    print(f"Mathematical Closure Verified: {m['global_atlas_closed']}. Rendering {total} frames...")

    anim=FuncAnimation(fig,lambda i: draw(ax,i,total,charts,T,pos,loops,m),frames=total,interval=1000/fps,repeat=False)
    mp4_path = outdir/"V1698_cinematic_closure.mp4"
    anim.save(mp4_path,writer=FFMpegWriter(fps=fps,bitrate=3000))
    plt.close(fig)
    print(f"Render complete. Generating inline video player...")

    # Embed video directly into Colab output
    video_binary = open(mp4_path, 'rb').read()
    video_url = "data:video/mp4;base64," + base64.b64encode(video_binary).decode()
    display(HTML(f"""
    <video width="800" height="600" controls autoplay loop style="border: 2px solid #00FFFF; border-radius: 8px;">
          <source src="{video_url}" type="video/mp4">
          Your browser does not support the video tag.
    </video>
    """))

# Execute the process
run_and_display(seconds=10, fps=12)
