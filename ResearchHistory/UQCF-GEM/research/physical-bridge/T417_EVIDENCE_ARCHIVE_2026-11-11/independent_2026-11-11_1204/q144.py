# Q144 check: on X0={0,p,l1,l2} (p child of 0; l1,l2 children of p), one step prunes l1,l2 simultaneously into p.
# B0=C^4, B1=span{e0, ep+el1+el2}. Enumerate permutation automorphisms of C^4 preserving B1 (as a set) and
# the selections sigma (subsets of minimal projections of B0) invariant under all of them. Report the closure algebra dims.
import itertools
atoms=['0','p','l1','l2']; B1=[{'0'},{'p','l1','l2'}]
def preserves(perm):
    m=dict(zip(atoms,perm)); return all({m[a] for a in blk} in B1 for blk in B1)
auts=[dict(zip(atoms,pm)) for pm in itertools.permutations(atoms) if preserves(pm)]
print("auts",len(auts))
def closure(sig):
    # generated algebra by B1 blocks and selected atoms: partition refinement
    parts=[set(b) for b in B1]; out=[]
    for b in parts:
        sel=[a for a in b if a in sig]; rest=b-set(sel)
        out+= [{a} for a in sel]+([rest] if rest else [])
    return sorted(map(lambda s:tuple(sorted(s)),out))
inv=[]
for r in range(5):
    for sig in itertools.combinations(atoms,r):
        S=set(sig)
        if all({m[a] for a in S}==S for m in auts): inv.append((sig,closure(S)))
for s,c in inv: print(sig:=s, c)
surv=closure({'0','p'}); print("R_inc^- (survivor closure):",surv, "invariant-attainable:", surv in [c for _,c in inv])
