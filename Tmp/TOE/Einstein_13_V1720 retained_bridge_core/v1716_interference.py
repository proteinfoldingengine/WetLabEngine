# V1716 - Recombination History Interference Audit (the "V1714" in the user's numbering).
# Question: do multiple recombination-order histories between the SAME endpoints combine
# with cancellation/enhancement (interference) or as positive classical weights (no interference)?
# FROZEN pass condition: interference claim ONLY if the effect beats classical additive path
# sums AND vanishes in the associative/g=0 controls AND survives the phase-randomized null.
import numpy as np
rng=np.random.default_rng(11)
def roll(v): return np.roll(v,1)
def K_native(x,y): return roll(x)*y - x*roll(y)            # non-associative
def K_assoc(x,y):  return np.zeros_like(x)                  # TRUE associative control: op=x+y exactly
def op(x,y,K,g=0.17): return x+y+g*K(x,y)

# A "history" = a specific order/grouping of recombining n source states into one end state.
# Enumerate distinct bracketings/orders of recombining 4 sources -> many histories, SAME multiset
# of sources => same 'endpoints' (same inputs, same final combination target).
import itertools
def histories_of(sources,K,g=0.17):
    # all binary-tree bracketings over all permutations -> distinct recombination histories
    outs=[]
    n=len(sources)
    def combine(seq):
        # left-fold and right-fold and balanced give different bracketings; enumerate a few canonical ones
        # left fold:
        l=seq[0]
        for s in seq[1:]: l=op(l,s,K,g)
        # right fold:
        r=seq[-1]
        for s in reversed(seq[:-1]): r=op(s,r,K,g)
        # balanced (pairwise):
        if n==4:
            b=op(op(seq[0],seq[1],K,g),op(seq[2],seq[3],K,g),K,g)
            return [l,r,b]
        return [l,r]
    for perm in itertools.permutations(range(n)):
        seq=[sources[i] for i in perm]
        outs.extend(combine(seq))
    return outs

def interference_metric(K,g=0.17,phase_random=False):
    # For a family of histories with the same sources, compare:
    #   classical:    || sum_i |h_i| ||         (positive weights - no cancellation)
    #   coherent:     || sum_i h_i ||            (signed/vector sum - allows cancellation)
    # interference ratio = coherent / classical. <1 => destructive (cancellation), the quantum signal.
    ratios=[]
    for _ in range(150):
        sources=[rng.normal(size=8) for _ in range(4)]
        H=histories_of(sources,K,g)
        H=[h for h in H if np.linalg.norm(h)>1e-9]
        if len(H)<4: continue
        if phase_random:
            H=[h*np.sign(np.random.randn()) for h in H]   # randomize signs: destroys structured phase
        coherent=np.linalg.norm(np.sum(H,axis=0))
        classical=np.sum([np.linalg.norm(h) for h in H])
        ratios.append(coherent/(classical+1e-12))
    return np.mean(ratios)

print("V1716 - Recombination History Interference Audit\n")
print("interference ratio = ||sum h_i|| / sum||h_i||.  =1 no cancellation; <1 destructive interference.\n")
nat=interference_metric(K_native,0.17)
assoc=interference_metric(K_assoc,0.17)
g0=interference_metric(K_native,0.0)
phaserand=interference_metric(K_native,0.17,phase_random=True)
print(f"  native (g=0.17):            ratio = {nat:.4f}")
print(f"  associative control:        ratio = {assoc:.4f}")
print(f"  g=0 flat limit:             ratio = {g0:.4f}")
print(f"  phase-randomized null:      ratio = {phaserand:.4f}")
print("-"*56)
# The KEY comparison: does native show MORE cancellation than the associative/g0 controls?
# Interference = native ratio meaningfully BELOW the control ratios (extra cancellation from
# the non-associative structure, not from generic vector summation).
print(f"\nnative vs associative: {nat:.3f} vs {assoc:.3f}  (diff {nat-assoc:+.3f})")
print(f"native vs phase-random: {nat:.3f} vs {phaserand:.3f}  (diff {nat-phaserand:+.3f})")
print()
# FROZEN pass condition
if nat < assoc-0.05 and nat < g0-0.05 and nat < phaserand-0.05:
    print("INTERFERENCE: native histories cancel MORE than classical/associative/phase-random")
    print("  controls -> structure-specific destructive interference. Amplitude-like layer.")
elif abs(nat-assoc)<0.05 and abs(nat-phaserand)<0.05:
    print("NO INTERFERENCE: native cancellation = control cancellation. The histories combine")
    print("  like generic vectors (some cancellation, but NOT structure-specific). The model is")
    print("  non-classical ALGEBRAICALLY but shows no amplitude-like history interference.")
else:
    print(f"AMBIGUOUS: native={nat:.3f}, controls assoc={assoc:.3f} g0={g0:.3f} phase={phaserand:.3f}")
    print("  inspect which control it differs from.")

print("\n\n=== g-sweep: does the cancellation scale with non-associativity coupling? ===")
print(f"{'g':>6} | {'interference ratio':>18}{'cancellation %':>16}")
print("-"*42)
for g in [0.0,0.05,0.1,0.17,0.25,0.4,0.6]:
    r=interference_metric(K_native,g)
    print(f"{g:>6.2f} | {r:>18.4f}{100*(1-r):>15.2f}%")
print("-"*42)
print("If cancellation grows monotonically from 0 with g -> real interference, weak at g=0.17.")
print("If flat/noisy -> the 3.6% is not a structure-specific interference effect.")
