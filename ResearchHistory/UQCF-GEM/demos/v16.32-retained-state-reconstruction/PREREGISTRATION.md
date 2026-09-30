# v16.32 — Retained-state reconstruction / information-loss closure

Parent: v16.31 published head `73cd2cdfe8f9d5207d5434c10661a703d7901c95`.

## Scientific question
v16.31 proves that the complete local consistency profile factors canonically over actual legal histories. Does the information now retained by that closure determine the underlying retained cover state, or do distinct legal retained states remain observationally indistinguishable to the entire closed profile?

We do not add a discriminator. We measure exactly what the existing retained invariants determine and what they forget.

For a fixed lineage tree and fixed indexed initial/final endpoint interval, let S be a reachable deletion ideal and Y(S) its indexed retained cover. Define the frozen signature

I(S) = (S-order data available intrinsically from the interval, tau(S), h(S), component coordinates g_C(S∩C)).

Run two deliberately separated tests:

A. PROFILE INJECTIVITY: does tau(S) alone distinguish legal retained states?
B. CLOSED-DATA INJECTIVITY: after adding only already-earned intrinsic order/component information, does the resulting closed data distinguish Y(S)?

Do not include S itself or a full incidence bitmap in a signature whose injectivity is being tested; that would make reconstruction tautological. Event labels may index component coordinates but the signature may contain only their earned component values and inherited predecessor relations, not a declaration of which events occurred.

## Outcomes
1. RECONSTRUCTIVE: prove an inverse construction from the closed data to every retained cover state.
2. NONINJECTIVE: provide the smallest admissible pair of distinct legal retained states with identical frozen closed-data signatures.
3. CONDITIONAL: identify the exact additional already-earned datum that separates collisions, prove sufficiency, and state that datum explicitly.
4. UNRESOLVED.

No outcome is preferred.

## Required collision witness
A noninjectivity claim requires two states in the same admitted endpoint interval, distinct indexed covers, exact equality of every field in the declared signature, legal histories reaching both, and an independent verifier reconstructing all fields from raw lineage/cover data.

## Bounded audit
Reuse v16.31's frozen endpoint universe where practical. Enumerate every reachable state and group by profile signature and closed-data signature. Publish collision multiplicities, smallest witnesses, and transformations under lineage relabeling and view-storage permutations.

## Adversarial controls
Reject:
- comparing states from different endpoint intervals;
- treating view storage order as physical;
- signatures that secretly include the deletion mask/state identity;
- fabricated collision pairs;
- equality of h without equality of tau;
- equality of tau without equality of all declared closed-data fields;
- invalid histories or changed union.

Include a checker-only fixture where two distinct objects deliberately share a coarse signature, and one where a richer legitimate signature separates them.

## Interpretation guardrail
A collision means the declared retained invariant is noninjective on retained states. It does NOT by itself mean information is physically destroyed, quantum information is lost, or geometry is absent. A positive inverse theorem is likewise mathematical reconstruction only.

Time is pruning / ordered recoverability update.
