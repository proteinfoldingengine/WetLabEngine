# A12.5 — exact no-go for naive incidence-overlap locality

Date: 2026-10-06 UTC.
Status: analytical physics-bridge candidate for fresh independent whole-argument review.
Scope freeze: fe6cf6207f5d9a007e52a75c088d0595d8c78a9d.
Native exact construction; no pending A12 theorem is required.

No claim of physical nonlocality, geometry, force, energy, continuum, numerical execution or implementation.

## 1. Candidate-locality question

For state E define the root-overlap graph G_E: distinct original roots i,j are adjacent iff E_i intersect E_j is nonempty.

A candidate-root overlap observer sees the complete labelled incidence structure and original floors in the connected component of the candidate root. This is stronger than any finite-radius view inside that graph.

Question: can that component, even supplemented by palette size, total root count and current transversal tau, determine exact legality of a candidate move?

A12.5 gives a counterexample.

## 2. Two states with identical candidate component

Use palette P={a,b,c,d,e}, six ORIGINAL roots, all original floors1, and candidate

    f=Add(R0,b)

on

    R0={d}.

State L:
    R0={d}
    R1={a,c}
    R2={c,e}
    R3={a}
    R4={a,c,e}
    R5={a,b}.

State I:
    R0={d}
    R1={a,b,e}
    R2={a,b,e}
    R3={a,c,e}
    R4={b}
    R5={c}.

In both states d occurs only in R0. Hence R0 has no overlap edge and its ENTIRE connected component is the singleton labelled root {d} with floor1.

Therefore every finite-radius candidate overlap neighborhood is identical in L and I. The states also have the same palette size5, root count6, candidate syntax, candidate floor and current tau as proved next.

## 3. Both source states have tau=3

### State L

Any hitting set must contain d to hit R0 and a to hit singleton R3. It must additionally contain c or e to hit R2={c,e}. Therefore every hitting set has size at least3.

Set {a,c,d} hits all six roots. Hence

    tau(L)=3.

### State I

Any hitting set must contain d to hit R0, b to hit singleton R4, and c to hit singleton R5. Therefore every hitting set has size at least3.

Set {b,c,d} hits R0 through d, R1/R2 through b, R3 through c, R4 through b and R5 through c. Hence

    tau(I)=3.

Both states are in the protected band.

## 4. Same candidate, different response

### State L after f

R0 becomes {b,d}. Singleton R3={a} still forces a in any hitting set. Root R2={c,e} forces c or e.

No pair covers:
- {a,b} misses R2;
- {a,c} and {a,e} miss R0={b,d};
- any pair omitting a misses R3;
- pairs containing neither a nor b/c/e as required miss an evident singleton/forced root.

More directly, any two-set must hit R3 with a. Its second label must hit R0 with b or d. If it uses b, R2 is missed; if d, R2 is missed. Thus no pair hits all roots.

Set {a,b,c} hits every root. Hence tau(fL)=3 and f is legal.

### State I after f

R0 becomes {b,d}. Pair {b,c} hits:
- R0 through b;
- R1,R2 through b;
- R3={a,c,e} through c;
- R4 through b;
- R5 through c.

Therefore tau(fI)<=2. The addition is illegal in the protected band.

So the SAME typed candidate on the SAME local component is legal in L and illegal in I.

## 5. Exact witness explanation

The difference is global pair-witness structure.

For critical pair K={b,c}:

In I before f, the only root missing K is R0={d}. Thus

    W_I({b,c})=1.

Candidate f adds b to that last witness, making W=0 and producing the pair cover.

In L, roots R0={d} and R2={c,e}? R2 contains c and is not a witness. But R1={a,c} contains c, R3={a} misses {b,c}, and possibly other roots are checked directly. At least R0 and R3 miss {b,c}, so

    W_L({b,c})>=2.

After f removes R0 as a witness, R3 remains. More generally the candidate shadow has no witness count1, consistent with its legality.

Thus the remote roots determine whether the candidate consumes the last global witness.

## 6. No-go statement

No function whose state input is restricted to:
- the candidate root's complete connected component in G_E;
- its full labelled incidence data and floors;
- palette size;
- total root count;
- current tau;
- candidate move identity/type

can determine exact candidate legality for all protected states.

Proof: all those inputs are identical for L and I, but the correct outputs differ.

Since the entire connected component is identical, the result is stronger than failure at any fixed finite overlap radius.

This does NOT prove physical nonlocality. It proves only:

    raw root-incidence overlap is not, by itself, an exact locality notion for admissibility response.

The global hitting constraint couples roots that need not overlap in labels.

## 7. Physics-facing consequence

If a physical notion of locality is to emerge from this program, it cannot simply be declared to be adjacency in the raw root-overlap graph.

A more defensible candidate is RESPONSE locality: two relational regions are near in the operational sense when interventions in one materially change candidate-centered admissibility margins in the other.

That proposal must itself be derived and tested. In particular:
- response adjacency may be state-dependent;
- collective A12.2-type effects mean pairwise response edges may miss higher-order dependence;
- a coarse response geometry would need composition/scaling laws before it could be interpreted spatially.

The next analytical target is therefore to define a relabeling-invariant dependency hypergraph from exact candidate shadows and surviving-cover dependencies, then test whether its coarse structure has stable distance/composition properties.

No fundamental time is introduced; only ordered relational updates are used.

v16.54/v16.55 and accepted A11 remain unchanged. Pending X62-X64 and A12.1-A12.4 are not promoted. Separate efficiency work remains unstarted.
