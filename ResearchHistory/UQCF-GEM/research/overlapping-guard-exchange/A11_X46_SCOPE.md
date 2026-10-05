# A11.X46 scope — deriving orbit compatibility from actual cycle gaps

Date 2026-10-05 UTC. Analytical parent 02add6acaa56284cd21308990dce23a84a469d75; X46 unused in the live tree.

## Authorized analytical objective

Continue beyond X45 by deriving its orbit-compatible four-cover input from actual root/cycle incidence structure. For a lower-selected simple ownership cycle, use only the declared masks to bound how many cyclic four-role windows fail to cover. Seek a reusable condition forcing two consecutive covering windows, hence the X45 intersection H4 intersect pi^{-1}(H4), without assuming global cover majority or supplying a precomputed cover family.

Native rules remain fixed: finite ordered palette, labelled original roots, SAME original positive floors and one-incidence primitives. No new labels/roots, weakened floors, simultaneous edits, compactness, geometry or fundamental time. X46 is an upper-interface derivation. Pair protection, floor legality, root scheduling, next-cycle existence and exact restoration must remain explicit lower-theorem obligations on the SAME physical path.

## Disclosed deduction before proof freeze

For a simple directed cycle C=(c_0,...,c_(ell-1)) with ell>=5, let W_a be four consecutive cycle roles starting at a. Let g_i(C) count starts a for which W_a is disjoint from actual mask Q_i. A window fails to cover exactly when at least one root misses it. Therefore the number of bad starts is at most sum_i g_i(C).

If

    sum_i g_i(C) < ceil(ell/2),

then more than floor(ell/2) cyclic starts are good. A cyclic binary word with that many good positions contains two consecutive good starts. Since W_(a+1)=pi(W_a), X45 compatibility follows. Equivalently, g_i is the total over cyclic gaps of Q_i intersect C of max(0,gap_length-3), with g_i=ell if the root avoids the cycle entirely. This is an actual mask bound, not an independent cover assumption.

A proposed all-parameter family uses q>=2 cyclic blocks, each of length 4h with h>=2. Include every co-triple mask G minus T and two sparse original masks D_0,D_2 consisting of residue classes 0 and 2 modulo four in every block. Each four-window meets both sparse roots, so every block cycle has zero gap budget. Co-triples force exact target four and pair redundancy at least m-2. The four-cover family is exactly the four-sets meeting D_0 and D_2, with count

    C(4H,4)-2C(3H,4)+C(2H,4),  H=qh,

which appears below half for H>=4. Singleton groups and the q block rotations appear to give q saturated long handovers with all four active representatives moving, unequal saturated floors H and m-3, and exact endpoint-event completion via X40L plus the derived X45 upper lift.

The family appears outside X38, X39, X40U, X41, X43 and X44 sufficient inputs. Four disjoint saturated supports cannot fit, and two selected labels whose footprints form a four-window appear to two-cover the whole endpoint union. These are disclosed analytical deductions, not accepted results or numerical preregistration.

## Required theorem obligations

Prove the good-window count, cyclic adjacency lemma, orientation W_(a+1)=pi(W_a), and rootwise gap formula. State precisely whether the gap condition is sufficient or exact; do not turn a union bound into necessity. Keep X45 compatibility and X40 lower protection as separate inherited components.

For the family prove exact transversal four, exact four-cover count, symbolic below-half inequality, zero gap budget for every active block cycle, actual pair redundancy and X40 strict margin, floor legality at both unequal saturated grades, q-cycle renewal, eligible progress, direct band, event minimum and FULL labelled/noncompact restoration.

Prove all claimed method separations in their exact accepted domains, including failure of X43 for every actual root and absence of a singleton-mask representation. Prove the disjoint-support and whole-union controls without promoting them to native disconnection or every-schedule impossibility.

## Scope and publication boundary

The cycle-gap condition is a structural sufficient derivation for prescribed lower-admissible cycles. It is not necessary for X45 compatibility, not an accessibility theorem for arbitrary endpoints, and not a lower repair theorem. A failed budget may still have adjacent covers or another repair mechanism.

Freeze the exact candidate before fresh independent whole-argument review. After acceptance reconcile STATUS.json, KNOWN_RESULTS.md, NEXT_OBLIGATION.md and A11_PROGRESS.md, obtain a distinct exact reporting review, append only that review, and perform immutable readbacks/full-tree/live-ref checks.

No numerical execution, enumeration, workflow, implementation, benchmark, integration merge or numbered certification. Certified v16.55/v16.54, frozen sources and all original evidence remain unchanged. The separately promised efficiency runner/fixtures/benchmarks remain unstarted and outside X46.
