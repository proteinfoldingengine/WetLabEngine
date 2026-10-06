# A12.3 scope — dual certificate response fields

Date: 2026-10-06 UTC.
Status: prospective analytical physics-bridge scope. Native proof only; A12.1/A12.2 are comparisons, not accepted dependencies.

## Objective

Rewrite target-four band admissibility as exact update laws for two relabeling-covariant certificate fields.

Domain: E is a finite nonempty-root state on a finite palette P with |P|>=2. In the intended protected target-four band, tau(E)>=3 implies |P|>=3. This domain is explicit because extending a zero- or one-label cover to a physical pair requires |P|>=2.

For state E define lower witness multiplicity for every physical pair K:
    W_E(K)=#{i:E_i intersect K=empty}.

Define upper cover indicator for every physical H with |H|<=4:
    C_E(H)=1 iff H intersects every root E_i.

Then:
    tau(E)>=3 iff W_E(K)>=1 for every pair K;
    tau(E)<=4 iff C_E(H)=1 for at least one H with |H|<=4.

Prove exact sparse primitive updates.

For Add(i,x):
- W(K) decreases by1 exactly when x in K and E_i misses K before the addition; otherwise unchanged.
- C(H) can change0->1 exactly when x in H, root i is the unique root missed by H before the addition, and all other roots are hit. It never changes1->0.

For Del(i,x):
- W(K) increases by1 exactly when x in K and E_i intersect K={x} before deletion; otherwise unchanged.
- C(H) changes1->0 exactly when x in H, E_i intersect H={x}, and H covered all roots before deletion; it never changes0->1.

Include floor legality separately.

## Required consequences

1. Derive A12.1 sign quadrants from these field updates rather than from case-by-case intuition.
2. Show cross-root response is mediated by depletion/restoration of W or creation/destruction of C.
3. Express irreducible A12.2 collective suppression as exhaustion of one W(K) reservoir across several roots.
4. Prove covariance under root/label relabeling and invariance of the multisets {W(K)} and cover counts by size.
5. Define protection margins
       mu_-(E)=min_K W_E(K)
   and
       N_4(E)=sum_{|H|<=4} C_E(H)
   carefully: mu_- is lower-witness redundancy; N_4 counts available small upper certificates. Neither is energy.
6. Determine exact one-update Lipschitz bounds: each W(K) coordinate changes by at most1; characterize how many K coordinates one incidence can affect. Upper cover indicators may change for many H but only through the edited root.
7. Do NOT claim W and C are conserved or canonically combine into one scalar unless proved.

## Physics boundary

This would establish an exact native response law for the certificate structure that keeps the relational state in the one-unit band. It is not geometry or force. The next bridge would ask whether an internal observer can access coarse summaries of W/C and whether their ordered response admits stable scaling/composition.

No numerical execution, implementation, efficiency, GR/ADM, dark matter, or fundamental time.
