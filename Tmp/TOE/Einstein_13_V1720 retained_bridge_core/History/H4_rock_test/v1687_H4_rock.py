# Is H4 a true geometric rock? Three antibodies aimed at REFERENCE, not consistency.
import numpy as np

def roll_down(v): return np.r_[v[-1], v[:-1]]
def roll_up(v):   return np.r_[v[1:], v[0]]

# operator families
def recombine_native(x,y,g):   return x+y+g*(roll_down(x)*y - x*roll_up(y))      # non-associative kernel
def recombine_assoc(x,y,g):    return x+y                                          # associative/linear control
def recombine_symover(x,y,g):  return x+y+g*(roll_down(x)*y + x*roll_up(y))        # symmetric overlap (no antisym order)
def recombine_nonlin_sym(x,y,g):return x+y+g*(x*y)                                 # nonlinear but symmetric

def assoc3(A,B,C,gAB,gBC,gL,gR,op):
    return op(op(A,B,gAB),C,gL) - op(A,op(B,C,gBC),gR)

def H4_canonical(J,g,op):
    J1,J2,J3,J4=J
    left  = op(op(op(J1,J2,g["g12"]),J3,g["g123"]),J4,g["g1234"])
    right = op(J1,op(J2,op(J3,J4,g["g34"]),g["g234"]),g["g1234r"])
    return left-right

def matrank(cols,tol=1e-8):
    return int(np.linalg.matrix_rank(np.stack(cols,axis=1),tol=tol))

def gates(rng):
    names=["g12","g23","g13","g14","g24","g34","g123_L","g123_R","g124_L","g124_R",
           "g134_L","g134_R","g234_L","g234_R","g123","g1234","g234","g1234r"]
    return {n: float(rng.uniform(0.3,1.5)) for n in names}

def lift_for(dim,n_branch,op,rng,randomize_branches=False):
    # branches
    if randomize_branches:
        J=[rng.normal(size=dim) for _ in range(n_branch)]
    else:
        raw=rng.normal(size=(dim,n_branch)); Q,_=np.linalg.qr(raw); J=[Q[:,i] for i in range(n_branch)]
    g=gates(rng)
    # O3 over all triples
    O3=[]
    idx=[(i,j,k) for i in range(n_branch) for j in range(i+1,n_branch) for k in range(j+1,n_branch)]
    for (i,jj,k) in idx:
        O3.append(assoc3(J[i],J[jj],J[k],g["g12"],g["g23"],g["g123_L"],g["g123_R"],op))
    # H4 canonical on first 4 branches (need >=4)
    H4=H4_canonical(J[:4],g,op)
    base=matrank(J+O3); full=matrank(J+O3+[H4])
    return full-base

# ---------- Antibody 1: robustness sweep (dim, n_branch, gamma via reseeding) ----------
print("=== ANTIBODY 1: does H4 rank-lift survive dim/n_branch sweep? (native operator) ===")
print(f"{'dim':>4}{'nbr':>5} | {'mean_lift':>10}{'min':>5}{'max':>5}")
for dim in [8,12,16,24,32]:
    for nb in [4,5,6]:
        lifts=[lift_for(dim,nb,recombine_native,np.random.default_rng(700+dim*10+nb+t)) for t in range(8)]
        print(f"{dim:>4}{nb:>5} | {np.mean(lifts):>10.2f}{min(lifts):>5}{max(lifts):>5}")

# ---------- Antibody 2: reference/non-tautology (orthonormal vs random branches) ----------
print("\n=== ANTIBODY 2: does the lift care about branch STRUCTURE, or do random vectors lift equally? ===")
dim,nb=16,4
orth=[lift_for(dim,nb,recombine_native,np.random.default_rng(900+t),randomize_branches=False) for t in range(20)]
rand=[lift_for(dim,nb,recombine_native,np.random.default_rng(900+t),randomize_branches=True) for t in range(20)]
print(f"orthonormal branches: mean lift = {np.mean(orth):.2f}")
print(f"random      branches: mean lift = {np.mean(rand):.2f}")
print(f"-> if equal, H4 lift is generic 4th-order headroom, not structure-specific")

# ---------- Antibody 3: operator-dependence (must vanish for associative/symmetric controls) ----------
print("\n=== ANTIBODY 3: does the lift vanish for controls where there should be NO obstruction? ===")
dim,nb=16,4
for name,op in [("native_nonassoc",recombine_native),("associative_linear",recombine_assoc),
                ("symmetric_overlap",recombine_symover),("nonlinear_symmetric",recombine_nonlin_sym)]:
    lifts=[lift_for(dim,nb,op,np.random.default_rng(1100+t)) for t in range(12)]
    print(f"{name:>20}: mean lift = {np.mean(lifts):.2f}  (max {max(lifts)})")

print("\n--- VERDICT GUIDE ---")
print(" ROCK  : lift survives sweep (Antibody1), structure-dependent (orth != random, Antibody2),")
print("         and vanishes for associative/symmetric controls (Antibody3).")
print(" NOT-ROCK: lift is headroom-only (collapses when space saturates), or random==orth,")
print("           or lift persists even for associative control (then it's not measuring non-assoc).")
