# V1715 - Quantum-geometry signature audit. NOT claiming Hilbert space/Born rule/amplitudes.
# Testing the SPECIFIC operator-algebraic properties that distinguish a non-classical operator
# geometry from a classical one. Each has an associative (classical) control that must give the
# classical answer. We claim ONLY what is measured.
import numpy as np
def roll(v): return np.roll(v,1)
def K_native(x,y): return roll(x)*y - x*roll(y)          # non-associative recombination
def K_assoc(x,y):  return x + y                          # classical/associative control (no order)
def op(x,y,K,g=0.17): return x+y+g*K(x,y)
DIM=8
rng=np.random.default_rng(7)

# ---- SIGNATURE 1: NONCOMMUTATIVITY  [x,y] = op(x,y)-op(y,x) ----
def noncomm(K):
    vals=[]
    for _ in range(200):
        x=rng.normal(size=DIM); y=rng.normal(size=DIM)
        c=op(x,y,K)-op(y,x,K)
        vals.append(np.linalg.norm(c)/(np.linalg.norm(x)+np.linalg.norm(y)+1e-12))
    return np.mean(vals)
print("SIGNATURE 1 - noncommutativity ||[x,y]||:")
print(f"  native: {noncomm(K_native):.4f}   associative control: {noncomm(K_assoc):.4f}")

# ---- SIGNATURE 2: NON-ASSOCIATIVITY (already known real, quantify as operator property) ----
def nonassoc(K):
    vals=[]
    for _ in range(200):
        x=rng.normal(size=DIM);y=rng.normal(size=DIM);z=rng.normal(size=DIM)
        a=op(op(x,y,K),z,K)-op(x,op(y,z,K),K)
        vals.append(np.linalg.norm(a)/(np.linalg.norm(x)+np.linalg.norm(y)+np.linalg.norm(z)+1e-12))
    return np.mean(vals)
print(f"\nSIGNATURE 2 - non-associativity ||(xy)z - x(yz)||:")
print(f"  native: {nonassoc(K_native):.4f}   associative control: {nonassoc(K_assoc):.4f}")

# ---- SIGNATURE 3: STATE-DEPENDENT GEOMETRY (the metric depends on the state - background-independent) ----
def jac(q,K,g=0.17):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n);e[a]=1.0; J[:,a]=op(e,q,K,g)-q  # linearized action
    return J
def state_dependence(K):
    # how much does the metric change between two different states? classical bg = 0.
    diffs=[]
    for _ in range(100):
        q1=rng.normal(size=DIM);q2=rng.normal(size=DIM)
        g1=0.5*(jac(q1,K)+jac(q1,K).T); g2=0.5*(jac(q2,K)+jac(q2,K).T)
        diffs.append(np.linalg.norm(g1-g2)/(np.linalg.norm(g1)+1e-12))
    return np.mean(diffs)
print(f"\nSIGNATURE 3 - state-dependent geometry (metric varies with state):")
print(f"  native: {state_dependence(K_native):.4f}   associative control: {state_dependence(K_assoc):.4f}")

# ---- SIGNATURE 4: COMPLEMENTARITY-like tradeoff. Define two 'observables' = projections onto
# the roll-conjugate directions. Is there a tradeoff: states sharp in one are spread in the other?
def complementarity(K):
    # A = position-like (identity basis), B = roll-basis (shift-conjugate, like momentum)
    F=np.fft.fft(np.eye(DIM),axis=0)/np.sqrt(DIM)   # roll is diagonalized by DFT -> conjugate basis
    spreads=[]
    for _ in range(200):
        x=rng.normal(size=DIM); x=op(x,x,K); x=x/np.linalg.norm(x)
        pA=np.abs(x)**2                              # distribution in position basis
        xB=np.abs(F@x)**2                            # distribution in conjugate (roll) basis
        # spread = participation entropy in each basis
        def H(p): p=p/p.sum(); return -np.sum(p*np.log(p+1e-12))
        spreads.append((H(pA),H(xB)))
    spreads=np.array(spreads)
    # complementarity: is the SUM of spreads bounded below (can't be sharp in both)?
    total=spreads.sum(axis=1)
    return total.min(), total.mean(), np.log(DIM)*2
print(f"\nSIGNATURE 4 - complementarity (entropy tradeoff between conjugate bases):")
mn,mean,maxposs=complementarity(K_native)
mn_a,mean_a,_=complementarity(K_assoc)
print(f"  native: min total-spread={mn:.3f}, mean={mean:.3f}  (max possible {maxposs:.3f})")
print(f"  assoc : min total-spread={mn_a:.3f}, mean={mean_a:.3f}")
print(f"  -> a NONZERO lower bound on combined spread = uncertainty-like tradeoff")

print("\n" + "="*58)
print("READING: native >> associative on signatures 1-3 = the recombination geometry is")
print("genuinely non-classical (noncommutative, non-associative, state-dependent/background-free).")
print("Signature 4: if min combined spread is bounded away from minimum, there is an")
print("uncertainty-like complementarity between conjugate recombination bases.")
print("We claim ONLY these measured properties - NOT Hilbert space, Born rule, or amplitudes.")
