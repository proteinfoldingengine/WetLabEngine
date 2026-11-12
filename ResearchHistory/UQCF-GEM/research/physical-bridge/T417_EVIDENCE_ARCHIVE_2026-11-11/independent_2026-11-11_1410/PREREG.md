# Q151 PREREG (2026-11-11T14:10:48-07:00), written before q151.py is run
Gate log: Q148 (merge/pinch order on the survivor closure) DROPPED as implied by ledger §13.3 ("closure acts on the tree factor only, because Z(A_{S_{j-1}}) ⊆ A_{S_j}";
on the product frame J, prune and pinch act on different tensor factors and commute). Q149 (survivor closure is the least persistent reading) DROPPED as a duplicate of ledger Prop 9.2 / §9.4
and COMPATIBLE_FIBER_RETENTION §3. Q150 (grain/order-invariant content of the receiver record) DROPPED as a duplicate of T-413 §3 / T-414 ((x_t, R_min); order erased in the unlabelled partition).
Q151 question (Target D, chain-intrinsic receiver observables): the label-free core of the survivor closure is Core_j = ∩_{g∈G} g Ã_j^- (largest G-invariant subalgebra of the
R_inc^- algebra; G = chain automorphisms). Its partition is the join of {g𝒮_j}. Questions: (a) when C4 fails, is Core_j still strictly finer than R_min (π_j), i.e.
do some survivor observables beyond R_min survive without (E1)? (b) Is Core always a record closure for some G-invariant σ (Thm 13.3 family), i.e. is the sequence of Core partitions
obtainable as an invariant closure? Hunch: (a) yes sometimes (the Q146 n=6 witness suggests Core_2 = {0,2},{3},{1},{4,5}); (b) unknown.
Universe: all cases n≤6 as in Q146. Report counts. Falsifier for the hunch in (a): Core_j = π_j in every C4-failing case.
Exact closure test for (b): σ_j = blocks of Core_{j-1} that are blocks of Core_j, and Core_j == partition(B_j ∨ span σ_j). Also Core must be decreasing (coarsening).
Inherited: P1 chain, Thm 11.1, 13.3. NOT_DERIVED; local only.
