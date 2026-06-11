# V1703.0 - L3 as REAL algebra, not a curve.
# Build the actual third-order object the v1638 narrative only plotted:
#   - real retained branches (orthonormal, as V1698 does)
#   - real non-associative product (the V1698 roll-kernel op_global)
#   - real associator3 = O3 (this is genuine algebra from V1698)
#   - L3 "excess" = the third-order associator field
#   - CLOSURE question, made computational and falsifiable:
#       Does the third-order associator lie in the span of the lower-order
#       (branch + pairwise) structure?  If yes -> L3 closes (it's reducible).
#       If no  -> L3 is a genuine irreducible third-order excess (does NOT close).
#   Pre-registered gate + random control. No tuned constants. Can fail either way.
import numpy as np

def roll_kernel(x,y): return np.roll(x,1)*y - x*np.roll(y,1)
def op_global(x,y,g=0.17): return x+y+g*roll_kernel(x,y)
def associator3(a,b,c,g):
    return op_global(op_global(a,b,g),c,g)-op_global(a,op_global(b,c,g),g)

def residual_to_span(v, basis):
    B=np.column_stack(basis); coef,*_=np.linalg.lstsq(B,v,rcond=None); return v-B@coef

def captured_fraction(v, basis):
    # fraction of v's norm explained by span(basis)
    r=residual_to_span(v,basis); return 1.0 - np.linalg.norm(r)/(np.linalg.norm(v)+1e-24)

def pairwise_products(branches,g):
    # lower-order structure available below third order: the branches themselves
    # plus all pairwise products op_global(b_i,b_j) (the "L2" pairwise layer)
    P=[]
    for i in range(len(branches)):
        for j in range(len(branches)):
            P.append(op_global(branches[i],branches[j],g)-branches[i]-branches[j])  # pure interaction part
    return P

def trial(dim, n_branch, g, rng):
    raw=rng.normal(size=(dim,n_branch)); Q,_=np.linalg.qr(raw)
    branches=[Q[:,i] for i in range(n_branch)]
    # third-order associators over all ordered triples
    O3=[]
    for i in range(n_branch):
        for j in range(n_branch):
            for k in range(n_branch):
                if len({i,j,k})==3:
                    O3.append(associator3(branches[i],branches[j],branches[k],g))
    # lower-order span: branches + pairwise interaction terms
    lower = branches + pairwise_products(branches,g)
    # closure test: how much of each third-order associator is captured by lower-order span?
    caps=[captured_fraction(o,lower) for o in O3 if np.linalg.norm(o)>1e-10]
    return np.array(caps)

dim=12; n_branch=4; g=0.17
rng=np.random.default_rng(1703)

caps_all=[]
for t in range(40):
    caps_all.append(trial(dim,n_branch,g,rng))
caps_all=np.concatenate(caps_all)

# RANDOM CONTROL: random vectors of same dim, captured by a random lower-span of same size
def control_trial(dim,n_branch,rng):
    branches=[rng.normal(size=dim) for _ in range(n_branch)]
    lower=branches+[rng.normal(size=dim) for _ in range(n_branch*n_branch)]
    targets=[rng.normal(size=dim) for _ in range(n_branch*(n_branch-1)*(n_branch-2))]
    return np.array([captured_fraction(v,lower) for v in targets])
ctrl=np.concatenate([control_trial(dim,n_branch,rng) for _ in range(40)])

print("=== L3 REAL CLOSURE TEST ===")
print(f"third-order associator captured by lower-order (branch+pairwise) span:")
print(f"  mean={caps_all.mean():.4f}  min={caps_all.min():.4f}  max={caps_all.max():.4f}")
print(f"random control (random target into random same-size span):")
print(f"  mean={ctrl.mean():.4f}  min={ctrl.min():.4f}  max={ctrl.max():.4f}")

# Also: rank-lift check (the V1698 move) - does adding O3 raise the rank beyond branches+pairwise?
def rank_lift(dim,n_branch,g,rng):
    raw=rng.normal(size=(dim,n_branch)); Q,_=np.linalg.qr(raw); branches=[Q[:,i] for i in range(n_branch)]
    lower=branches+pairwise_products(branches,g)
    O3=[associator3(branches[i],branches[j],branches[k],g)
        for i in range(n_branch) for j in range(n_branch) for k in range(n_branch) if len({i,j,k})==3]
    r_low=np.linalg.matrix_rank(np.column_stack(lower),tol=1e-9)
    r_full=np.linalg.matrix_rank(np.column_stack(lower+O3),tol=1e-9)
    return r_low,r_full
rl=[rank_lift(dim,n_branch,g,rng) for _ in range(20)]
r_low_mean=np.mean([a for a,b in rl]); r_full_mean=np.mean([b for a,b in rl])
print(f"\nrank(lower)={r_low_mean:.1f}   rank(lower+O3)={r_full_mean:.1f}   lift={r_full_mean-r_low_mean:.1f}")

print("\n--- PRE-REGISTERED VERDICT ---")
print("  L3 CLOSES (reducible)      if mean capture > 0.90 AND rank lift ~ 0")
print("  L3 OPEN (irreducible 3rd)  if mean capture < 0.50 OR rank lift > 0")
mc=caps_all.mean()
if mc>0.90 and (r_full_mean-r_low_mean)<0.5:
    print(f"\nRESULT: L3 CLOSES. Third-order associator is reducible to lower order (capture={mc:.3f}, no rank lift).")
    print("  The stack's 'third-order excess' is not irreducible -- it collapses into branch+pairwise structure.")
elif mc<0.50 or (r_full_mean-r_low_mean)>=0.5:
    print(f"\nRESULT: L3 OPEN / IRREDUCIBLE. Third-order associator carries genuine structure")
    print(f"  not captured by lower order (capture={mc:.3f}, rank lift={r_full_mean-r_low_mean:.1f}).")
    print("  This is a REAL third-order excess -- the narrative claim, now computed, holds.")
else:
    print(f"\nRESULT: PARTIAL. capture={mc:.3f}, rank lift={r_full_mean-r_low_mean:.1f}. Neither cleanly closes nor cleanly opens.")
