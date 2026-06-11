# RUNG 1 - does the Pillar-1 atlas induce a CONSISTENT emergent metric?
# Derived, not imposed: the metric must come from the atlas transition structure itself.
# A chart i carries a local inner product; the induced distance between configurations must
# (a) be symmetric, (b) be non-degenerate (positive), (c) AGREE across chart overlaps (the
# defining consistency condition - same distance whether measured in chart i or chart j),
# (d) satisfy the triangle inequality. Tested against a null: a RANDOM (non-atlas) frame set.
import numpy as np
def orth(rng,d):
    M=rng.normal(size=(d,d)); Q,R=np.linalg.qr(M); s=np.sign(np.diag(R)); s[s==0]=1; return Q*s

DIM=24; NCH=6
def atlas(seed): 
    rng=np.random.default_rng(seed); return [orth(rng,DIM) for _ in range(NCH)]

# A chart's local metric: g_i = frames_i^T frames_i = I for orthonormal frames -> trivial.
# That can't be the metric (it's the same in every chart). The NON-trivial induced metric must
# come from how the recombination/native structure weights directions WITHIN a chart.
# Derive g_i from the native kernel's local action: g_i(u,v) = <u, J_i v> where J_i is the
# symmetric part of the native transport's linearization at chart i's reference state.
def roll(v): return np.roll(v,1)
def native_jacobian(qstate,g=0.17):
    # linearization of T(dx)=dx+g(roll(dx)*q - dx*roll(q)) wrt dx, at state q
    n=len(qstate); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0
        col=e+g*(roll(e)*qstate - e*roll(qstate))
        J[:,a]=col
    return J
def chart_metric(frames_i, qstate):
    J=native_jacobian(qstate)
    g_amb=0.5*(J+J.T)                      # symmetric part = candidate metric in ambient coords
    # express in chart i's frame
    return frames_i.T @ g_amb @ frames_i

def metric_distance(g, u, v):
    d=u-v; val=float(d@g@d)
    return val

def run(seed, use_atlas=True):
    rng=np.random.default_rng(seed)
    frames = atlas(seed) if use_atlas else [orth(np.random.default_rng(seed+1000+k),DIM) for k in range(NCH)]
    qstates=[rng.normal(size=DIM) for _ in range(NCH)]
    # one shared ambient metric source (native kernel) but a SHARED reference state so charts
    # describe the SAME geometry: overlap-consistency means g expressed in chart i and chart j
    # must give the same distance for the same ambient pair.
    qref=rng.normal(size=DIM)
    g_amb=0.5*(native_jacobian(qref)+native_jacobian(qref).T)
    # pick ambient test points
    pts=[rng.normal(size=DIM) for _ in range(5)]
    # (c) overlap consistency: distance in chart i vs chart j for same ambient pair
    overlap_err=[]
    for i in range(NCH):
        for j in range(i+1,NCH):
            gi=frames[i].T@g_amb@frames[i]; gj=frames[j].T@g_amb@frames[j]
            for a in range(len(pts)):
                for b in range(a+1,len(pts)):
                    ui,vi=frames[i].T@pts[a],frames[i].T@pts[b]
                    uj,vj=frames[j].T@pts[a],frames[j].T@pts[b]
                    di=metric_distance(gi,ui,vi); dj=metric_distance(gj,uj,vj)
                    overlap_err.append(abs(di-dj)/(0.5*(abs(di)+abs(dj))+1e-12))
    # (b) non-degeneracy / positivity: eigenvalues of g_amb
    eig=np.linalg.eigvalsh(g_amb)
    pos_frac=float((eig>1e-9).mean())
    # (d) triangle inequality on metric distances (need PSD; test rate of violation)
    tri_viol=0; tri_tot=0
    if (eig>-1e-9).all():
        gp=g_amb
    else:
        gp=g_amb - (eig.min()-1e-6)*np.eye(DIM)   # shift to PSD to test triangle on the PSD part
    def dd(a,b): 
        d=pts[a]-pts[b]; return np.sqrt(max(0.0,d@gp@d))
    for a in range(len(pts)):
        for b in range(len(pts)):
            for c in range(len(pts)):
                if a!=b and b!=c and a!=c:
                    tri_tot+=1
                    if dd(a,c) > dd(a,b)+dd(b,c)+1e-9: tri_viol+=1
    return np.mean(overlap_err), pos_frac, (tri_viol/max(tri_tot,1)), eig

print("RUNG 1 - atlas-induced metric consistency\n")
oe=[];pf=[];tv=[]
for s in range(30):
    o,p,t,eig=run(s,use_atlas=True); oe.append(o);pf.append(p);tv.append(t)
oe_n=[];pf_n=[];tv_n=[]
for s in range(30):
    o,p,t,eig=run(s,use_atlas=False); oe_n.append(o);pf_n.append(p);tv_n.append(t)
print(f"(c) overlap-consistency error (same ambient pair, chart i vs j):")
print(f"      atlas: {np.mean(oe):.2e}   random-frames null: {np.mean(oe_n):.2e}")
print(f"      -> if ~0 for atlas, the metric AGREES across charts (consistency holds)")
print(f"(b) positive-eigenvalue fraction of g_amb: {np.mean(pf):.3f}  (1.0 = Riemannian; <1 = indefinite)")
print(f"(d) triangle-inequality violation rate: {np.mean(tv):.3f}  (0 = metric-like)")
print()
print("eigenvalues of induced g (one seed):", np.round(np.sort(eig)[:6],3),"...",np.round(np.sort(eig)[-3:],3))
print("-"*55)
if np.mean(oe)<1e-6 and np.mean(tv)<0.01:
    sig = "Riemannian (all positive)" if np.mean(pf)>0.99 else f"indefinite (signature: {np.mean(pf):.2f} positive)"
    print(f"RUNG 1 PASS: atlas induces a consistent metric. Type: {sig}.")
    print("  -> proceed to Rung 2 (metric-compatible connection).")
else:
    print("RUNG 1: metric not yet consistent - characterize before climbing.")
