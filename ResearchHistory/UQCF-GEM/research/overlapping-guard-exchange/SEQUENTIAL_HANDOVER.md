# Sequential handover and renewal through precedence constraints

Status: candidate analytical result for independent review. Parent analytical checkpoint: eb33a68af3fcd98dc2abdea82fcf8d1fc85ef30b. Certified integrated baseline remains 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f. No code, tests, numerical enumeration or workflow execution. Native admissibility is unchanged from SCOPE.md.

## 1. Fixed preparation and the restricted schedule class

Let A,C be exact-q endpoints, q>=3, t=q-1, with actual t-guards on old indices I and destination indices J. Put K=I intersect J. Prepare J minus I by the floor-safe union replacements of GUARD_HANDOVER.md while I remains fixed.

During the shared-slot stage, hold every slot outside K fixed: its support is C_i if i is in J minus I and A_i otherwise. Call this entire fixed family F. It includes all outside roots, not merely the exclusive guard roots. Thus the criterion below tests the full root tuple for this prepared stage.

The restricted schedules studied here process each index of K once. An index i changes from A_i to A_i union C_i to C_i, by single-incidence additions followed by deletions. Complete that root before starting the next. No other root changes during this stage. This is a chosen method, not a restriction added to native admissibility.

For every label set H with |H|<=t-1 that hits F, define

    L(H)={i in K: H misses A_i},
    R(H)={i in K: H misses C_i}.

Both are nonempty: a hitting set of F meeting all old shared roots would hit the old guard, and one meeting all new shared roots would hit the destination guard. If K is empty, there are no such H and preparation already establishes the destination guard.

## 2. Exact local safety condition

Suppose S subset K has completed its replacements, and i is an unprocessed index. The remaining shared roots are still old. At the largest support in the replacement of i, all shared roots equal their completed new or unprocessed old support, except i which equals A_i union C_i.

For any H hitting F with |H|<=t-1, that tuple has a root missed by H exactly when

    R(H) intersect S is nonempty,
    or L(H) minus (S union {i}) is nonempty,
    or i belongs to L(H) intersect R(H).

**Lemma S1.** Replacement of i preserves tau>=t throughout if and only if the displayed disjunction holds for every such H.

Proof. The three alternatives exhaust the completed new slots, untouched old slots, and active union slot respectively. A small set not hitting F cannot be a transversal at any point of the stage. Every intermediate tuple is componentwise contained in the active-union tuple, so the active union has the minimum transversal along this individual replacement. It is itself visited. Its lower bound is therefore both necessary and sufficient. Floors hold because additions start from A_i and deletions end at C_i, which meet the same labelled slot's floor.

This condition is valid even when the current tuple is only at level t. It does not reuse exact-q redundancy at an inexact state.

## 3. Exact ordering criterion

If L(H) intersect R(H) is nonempty, any common index protects against H before its edit, during its union, and afterward. Such H imposes no ordering condition.

For the remaining H, L(H) and R(H) are nonempty and disjoint. Let pos(i) be the position of shared slot i in a proposed permutation of K.

**Theorem S2.** The restricted shared-slot schedule preserves the lower guard if and only if every such disjoint pair satisfies

    min_{j in R(H)} pos(j) < max_{i in L(H)} pos(i).

In words, at least one new missed root must be completed before the last old missed root is edited.

Necessity: if all R indices follow all L indices, consider the replacement of the last L index. Every other old missed root has been replaced, no new missed root has been installed, and the active index is not in R. H hits the active-union tuple. Thus the full lower bound fails.

Sufficiency: before the first R replacement is completed, the last L index is still untouched, including during that first R replacement, because it occurs later in the order. It is missed by H. After the first R replacement is completed, that fixed destination support is missed by H for the rest of the stage. Consequently there is no gap in protection. Together with common-index protection, this covers every small H. S1 supplies all primitive moves.

This is a finite quantified mathematical criterion, not a claim of efficient evaluation or an instruction to enumerate its hitting sets.

## 4. Acyclic certificates give eligible moves and termination

For each H with disjoint L(H),R(H), select a witness pair j(H) in R(H), i(H) in L(H), and place the directed edge j(H)->i(H) on the fixed shared-slot set K. Repeated edges cause no problem.

**Corollary S3.** A safe restricted schedule exists if and only if these witness pairs can be selected so that the resulting directed graph is acyclic.

If the graph is acyclic, any topological order places j(H) before i(H), so satisfies S2 for every H. Conversely, a safe order supplies a pair with j before i for each H by S2; all selected edges increase position and hence have no directed cycle.

An acyclic certificate gives more than a potential: every nonempty remaining directed acyclic graph has a zero-indegree vertex, since otherwise following predecessors in the finite graph yields a cycle. Process such a vertex, using the finite union replacement, and remove it from the remaining graph. S2 guarantees the chosen topological order is safe at every prefix. The number of unprocessed shared slots strictly decreases, while each root replacement uses finitely many eligible toggles. This proves existence of the next eligible operation and finite completion under the certificate hypothesis.

Once every shared slot is complete, J is an unchanged destination t-guard. Restore all other roots to C through their own union paths while holding J fixed. This reaches the exact labelled endpoint. Preparation, sequential handover and restoration form a finite path with tau>=q-1. The accepted upper-excursion-removal theorem converts it to a path with tau in {q-1,q}. Conditional native lifting has exactly the child-interface requirements recorded in GUARD_HANDOVER.md Section 6.

The renewed protection here is an explicit transfer of missed-root witnesses. It does not require exact-q intermediate states. Exact endpoint redundancy returns at C, permitting concatenation along any finite exact-endpoint chain whose adjacent pairs have the required certificates.

## 5. What this settles and what it does not

The all-unions bridge is sufficient whenever every small H has a common missed index. S2 additionally permits disjoint old/new miss sets, provided their protections can be handed over in a compatible order. It therefore resolves some multiple-overlap handovers unavailable to the prior bridge; SEQUENTIAL_EXAMPLES.md gives an exact-endpoint witness.

The condition characterizes this fixed-preparation, one-root-at-a-time, one-pass union method only. It does not show that a compatible acyclic selection exists for arbitrary exact endpoints or for every guard choice. A failed particular witness selection is not proof that every selection fails. Only impossibility of all selections rules out every schedule in this restricted class.

Even that method obstruction leaves other guard choices, different preparation, interleaved partial root edits, temporary admissible supports, and native paths outside the width-floor carrier available. No universal higher-floor theorem, genuine native barrier, implementation certification, sharpness, originality or physical conservation claim is made.
