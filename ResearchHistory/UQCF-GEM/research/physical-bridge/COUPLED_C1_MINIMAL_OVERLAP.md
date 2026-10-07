# C1 — minimum overlapping carrier lemma

Date: 2026-10-07.
Status: ANALYTICAL LEMMA CANDIDATE / AUTHOR-SIDE PROOF, NOT INDEPENDENTLY ACCEPTED.
Prospective scope: COUPLED_AUXILIARY_SCOPE.md at f95cdfef30b452e1688172b978ee2e25fb1924d8.

## Definitions

Let E=(S_1,...,S_n) be n labelled nonempty finite supports in a finite label palette P. A transversal H subseteq P meets every S_i. The hitting number tau(E) is the minimum size of a transversal.

Supports overlap if there are distinct i,j with S_i intersect S_j nonempty.

## Theorem C1.1

For n>=1 nonempty supports,
    tau(E)=n if and only if S_i intersect S_j is empty for all i!=j.

Proof:

Always tau<=n: select one label from each nonempty support and take their union.

If supports are pairwise disjoint, a label can hit at most one root, so every transversal contains at least one distinct label per root. Thus tau>=n and equality follows.

Conversely, suppose S_i and S_j overlap at label x. Choose x once, and choose one label from each of the remaining n-2 nonempty supports. These n-1 labels hit every root, so tau<=n-1. Thus tau=n implies pairwise disjointness. QED.

## Corollary C1.2 — minimum overlapping target-four carrier

With exactly three nonempty roots, tau>=3 forces tau=3 and hence pairwise disjoint supports. No genuinely overlapping three-root state is in the protected band 3<=tau<=4.

With exactly four nonempty roots, if supports overlap and 3<=tau<=4, then tau<=3 by C1.1, hence tau=3.

Thus a four-root state is the smallest possible protected carrier with genuine overlap. Every such protected overlapping four-root state sits on the lower edge tau=3, not the tau=4 layer.

This is a minimum in number of original roots, not a statement about palette cardinality or support sizes.

## Explicit positive control

Take P={a,b,c,d,e} and four roots

    S1={a,b}
    S2={a,c}
    S3={d}
    S4={e}.

S1 and S2 overlap at a. The singleton roots force d,e. Since neither d nor e hits S1 or S2, any transversal also needs a label hitting both, or separate labels; hence tau>=3. The set {a,d,e} hits all four roots, so tau=3.

This demonstrates the lower-edge carrier exists.

## Rejecting control

Replace S3 by {a,d} while leaving S1,S2 and S4={e}. Now {a,e} hits every root, so tau<=2. An overlap alone does not guarantee protected tau=3.

Therefore a future C2 carrier must explicitly prove the absence of all two-label covers, not infer lower protection from root count.

## Scientific consequence and limitations

The earlier n=3 singleton-swap buffer construction cannot be generalized to overlapping supports while retaining n=3 and tau>=3: such an overlapping source is mathematically excluded.

A genuinely overlapping coupled-cycle test must begin at n>=4, and the first minimal n=4 target-four carrier necessarily lives at tau=3 at any overlapping endpoint.

This lemma does not establish a coupled dependency cycle, an auxiliary host-selection rule, renewable protection, or exact repair. It is a structural filter for C2.

No numerical experiment, independent review, physical interpretation, force, geometry, energy, or fundamental time is claimed.
