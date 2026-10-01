# Independent analytical review of v16.52 recursive interface

Verdict: **accept R1–R6 analytically**, with the harmless domain clarification below. The argument closes the identical interface under both binary and ternary joining and therefore covers arbitrary finite ordered mixed-arity trees, including repeated ternary vertices. I found no construction-breaking mathematical gap. This review does not accept an implementation, validate a numerical corpus, or certify the stage.

Reviewed sources: v16.52 `INTERFACE_LEMMA.md` and `PREREGISTRATION.md`; the supplied v16.50 and v16.51 `THEOREM.md` files as inherited analytical context. No numerical science or tests were executed. Repository lineage, PR status, and campaign artifacts were not independently audited by this proof review.

## R1: quantifiers and feasibility

The inductive variable is tree size, and the child hypothesis must quantify over every ordered palette and every exact state on it. The candidate does so. Arbitrary orders are essential because target-2 joining temporarily uses an anchor-first child order.

Minor editorial clarification: clauses defining K, its compact roles, and contraction should explicitly say “for |P| >= w(T,q).” For smaller palettes clause 1 says there is no exact state, so a literal unconditional reading of clause 2 would contradict clause 1. The construction and normalization proof consistently use the feasible-palette reading. Also write the excursion sum over internal vertices, or explicitly put h=q=0 on leaves. These are typing clarifications, not changes to the construction or recurrence.

Child feasibility gives the individual-width lower bounds. At maximum target the roots are pairwise disjoint, giving the sum bound. At ternary target 2 every label occurs in at most two child roots, giving the half-sum bound. The cyclic construction is sufficient: each block has length at most M, the concatenated positions have length S with M<S<=2M, and hence each residue appears at most twice and some appears twice. No block repeats a residue internally. Thus the child supports have their required sizes, no triple intersection, and a nonempty pair intersection. Their union is exactly the prefix of length M. No binary-only property enters.

## R2: exact-interior complete-role replacement

This proof is valid for every descendant arity, and even does not require the initial interior profile to be exact. Ancestor closure of occurrences follows from nesting. Preorder addition and reverse-preorder deletion preserve nesting; the installed replacement prevents emptied supports. The external parent must contain both labels throughout the operation, as stipulated.

At an interior vertex in the addition phase the new label's child-incidence set is dominated by the unchanged old label's set. Any new hitting set using the new label can substitute the old label without growing. Conversely adding incidences cannot increase the optimum. During deletion the completed new incidence set dominates the remaining old one, giving the analogous equality. This argument includes root-only roles and leaves. It correctly excludes the external parent's coordinate from the preservation claim.

## R3: binary joining with arbitrary children

For target 1, expansion changes no child interior coordinate and preserves the initial anchor. Once all roots are P, sequential normalization and prefix contraction preserve a shared first label. The only possible nonzero excursion lies inside the currently normalizing child, whose entire sum is bounded by 1.

For target 2, child roots stay disjoint through sequential normalization and contraction. Globally absent-label replacements preserve disjointness. Cross-child exchanges can produce only the single parent defect 2 to 1, while R2 preserves all interiors. The three-exchange pivot construction correctly realizes a same-child transposition and restores the pivot, even if it was an earlier fixed role. Distinct targets imply a later target cannot be carried by an earlier fixed role. Finite ordered assignment therefore reaches the full canonical role state, not merely its root supports.

## R4: ternary joining and nonstacking

Target 1 is the same shared-label argument. Target 3 uses pairwise disjoint roots; during an exchange the untouched third root contains neither exchanged label. A triple intersection therefore cannot arise, so the sole possible defect is 3 to 2. Each completed exchange restores exactness before another phase starts.

For target 2, the chosen shared label is absent from the third root because the starting triple intersection is empty. Fixed-root normalization cannot alter that root witness. Contraction of each selected nonfull child retains its anchor-first label, while contraction of a full-width child deletes nothing. Deletions cannot introduce a triple intersection. Thus every recursive call runs while the parent remains exact, and completed calls leave all interiors exact.

During the subsequent role-assignment phase there are no recursive normalization calls. A compact child with width below k has an actually subtree-absent label because all descendants lie in its root. A hole need not be absent from other children. If a target is occupied, its occupant cannot be an earlier fixed role; evacuating it into a hole and then installing the target is legal and fixes a new role in finitely many operations. All interiors stay exact throughout. The parent alone may be 1, 2, or 3, which is precisely the unit-deviation bound at target 2. The parent need not be exact between individual replacements in this phase.

There can be at most one child of width k: two such roots would equal P and intersect the nonempty third. If a full child exists, feasibility gives k<=M<=k, hence M=k. Its cyclic target block is all P, ordered by restriction of P, and its normalization used exactly that order. It already equals its required canonical state and needs no transport. This resolves the otherwise genuine missing-hole and ordering obstruction.

The global sum bound follows from these phase invariants, not from independently bounding each coordinate. A recursive defect at any depth occurs with all outside coordinates exact. Ancestor transport preserves every interior coordinate. Thus arbitrary depth does not stack defects.

## R5: closure, compactness, and equivariance

Every internal canonical state's immediate-child union is the claimed width prefix, and nesting puts all further descendants within it. Root labels outside the prefix consequently have no proper-descendant occurrences and may be deleted in an attached context without changing interior hitting numbers. Recomputing K on that prefix changes neither the child palettes nor their orders. The leaf separately contracts to one label. External-parent control remains a caller obligation, and each joining case supplies it.

Complete-role transport of a compact canonical state preserves its abstract ordered role pattern. Transporting all role positions to the target ordered palette therefore transports all descendants to the required K, including mixed ternary descendants.

Tree-order traversals and palette-order selections commute with simultaneous relabeling and order transport. Resetting numerical sort after relabeling is correctly excluded. To implement a uniquely deterministic sequence, choose deletion/traversal tie orders consistently as well; existence and the stated equivariance have no obstruction. All recursive calls concern strictly smaller trees and role assignment fixes finitely many positions, so structural induction is well founded and returns the identical interface.

## R6: barrier consequence

Reversal and concatenation of the two legal normalization paths connect any two exact states with the same fixed root and profile within total L1 excursion 1. Within an exact-profile component an exact path gives all inherited barriers zero. Between distinct exact components every path contains a nonzero integer defect, giving the inherited independent scalar lower bounds of 1; the constructed path attains their upper bounds. This uses the inherited B1, Binf, and Bs definitions and their stated integer lower-bound property, rather than introducing new scalar objectives. It neither proves that any particular profile is disconnected nor identifies dynamics or shortest paths.

## Frozen identity count, analytically checked

Each internal binary vertex contributes a factor 2 and each ternary vertex a factor 3 to the number of profiles:

| Shape | Binary vertices | Ternary vertices | Profiles |
|---|---:|---:|---:|
| A=(T,L,L) | 0 | 2 | 9 |
| F=(T,T,L) | 0 | 3 | 27 |
| G=(T,T,T) | 0 | 4 | 81 |
| H=(A,T,B) | 1 | 4 | 162 |
| J=((T,L),(L,T),T) | 2 | 4 | 324 |

The sum is 603. Two palette sizes, three permutation identities, and two start modes give 603*2*3*2=7236 directed identities. Coincident states do not permit identity deduplication. This verifies the specification arithmetic only; actual exact identity-set equality remains an independent-verifier obligation.

The frozen finite cases cannot establish generality, and this analytical acceptance cannot establish their execution or correctness. RED controls, implementation review, independent verification, reproduction, provenance, durable publication, merge replay, and closure receipts remain separate gates. No stage-certification claim follows from this review.
