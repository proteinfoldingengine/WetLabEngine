# Q143 dropped as duplicate; Q144 RESULT (2026-11-11T12:05:46-07:00): the survivor closure R_inc^− is not a function of the restriction chain
Science, local, supporting math. Not posted. NOT_DERIVED; Not claimed; scientific_breakthrough false. notify_aaron: no.
Heads unchanged: research 8c4f6594; thread 8a86d82d. PR111: no comments after 6799790426. No lock.

## Q143: duplicate, dropped at the gate
Can a merge+pinch composite natively supply corner record compatibility? This is answered by ledger §13.1 Cor 13.2 (@8c4f6594): a straddling
merge removes the old unit p_t however much pinching the step does. Restoring it requires undoing the merge. No new work.

## Q144 (self-selected in the same block)
Question: Thm 13.3 makes every reading a record closure Ã under a retention selection σ, and says σ = survivors is "pinned by earned facts (E1),(E2),A".
Is any σ that yields R_inc^− determined by the restriction chain {A_j} ALONE, i.e. without the address labels?
Definition: σ is chain-intrinsic if it is invariant under every *-automorphism of A_0 that maps each A_j onto itself
(anything computed from the chain must be). Premises: Lemma 13.1, Thm 13.3 (ledger, inherited). Pass/fail: fail if a chain-intrinsic σ yields
R_inc^− on a loss-arrow witness. Counterexample strategy: exhaustive enumeration on the minimal loss-arrow witness.
Deviation disclosed: the enumeration (q144.py) was written in the same sitting as this question, not under a separate PREREG file. It is an
exhaustive finite enumeration, not a statistical run.

Witness: X_0={0,p,l1,l2}, with l1,l2 children of p, pruned simultaneously (the minimal loss-arrow case, Prop 9.4). B_0=C^4, B_1=span{e_0, e_p+e_l1+e_l2}.
Chain automorphisms: the permutations preserving the block {p,l1,l2}, S_3 (6 maps; stdout.txt). Invariant selections are unions of orbits,
{0} and {p,l1,l2}. Their closures are only B_1 (R_min) or C^4 (R_full = R_inc^+). The survivor closure span{e_0,e_p,e_l1+e_l2}
(R_inc^−) is not attainable (stdout: invariant-attainable False).

Prop 144.1. Suppose a straddling merge block contains a survivor sector and a pruned sector whose past fiber chains are isomorphic
(e.g. both atomic in A_0). Then on that block every chain-intrinsic σ gives either no record (R_min) or the full record (R_inc^+).
R_inc^−, the only reading with a loss arrow and survivor-only retention, requires the label datum that tells the survivor from the pruned atom.
That is exactly the (E1) stable-address / owner typing.
Proof: an automorphism of A_0 that swaps the two isomorphic sub-fibers and fixes everything else preserves every A_j, because later algebras
contain only the block's sum, and earlier algebras are preserved by the isomorphism. An invariant σ is a union of orbits. ∎
Consistent with: Q139 (x_p ≡ −x_u, so detection does not pick the owner), d28 (CN supplies receiver typing), and the ledger's own sentence (σ pinned by E1).
Novelty: near-implied (the ledger already says σ is label-fixed). New precision: without labels the reading lattice collapses on symmetric
merges to {R_min, R_full}, so the loss-with-retention reading is exactly label-dependent. Not postable on its own; a one-line scope candidate.
Hash inputs: q144.py, stdout.txt.

## NEXT
Q145: does the address label (E1) itself come from the chain once the chain is enriched with the native state ρ? That is, does a generic fixed state
break the S_3 symmetry so that "survivor" is defined by ρ? Dedup first vs §12.1 (fixed state frame), Q139/Q140 (balanced pair), and
T-235 Cor O.1. Hunch: no, because the pruned/survivor distinction must hold for every preparation, while ρ-dependent typing is
preparation-dependent; check against the d28 "relative-history reading of addresses".
