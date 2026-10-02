# Independent analytical review — v16.54 parent-support connectivity

**Verdict: ACCEPT the scoped analytical claims in the reviewed candidate.** No Critical, Important, or Minor mathematical defect was found. This is acceptance of the stated theorems and conditional native lifting, not merge approval, implementation validation, or v16.54 certification. Universal higher-target connectivity remains OPEN.

## Scope, identity, and method

The requested comparison is against verified v16.53 integrated parent `f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8`, with v16.54 admissibility/scope freeze `3932248af7bb5c64bdd3d467fcd6d78ddf7adde5` and candidate head `26bdda935564ba828e89bb7879400285789f2d72` on `research/v16.54-parent-support-connectivity` (draft PR 102). These repository identities were supplied to this reviewer; I did not independently query commit ancestry or fetch the immutable GitHub file.

I read the complete local `v1654/GENERAL_PARENT_CONNECTIVITY.md`, `NATIVE_ADMISSIBILITY.md`, `RESEARCH_SCOPE.md`, `PROGRESS.md`, and README, together with `v1653/FOUR_CHILD_INTERFACE.md` and its independent proof review. The exact accepted candidate proof byte boundary is SHA-256 `de144b98ee80c99510dc1eabb7318be11d67603f5f7337004019dc8372bc2751`, independently matched by local file hashing. Acceptance attaches to those proof bytes and the stated mathematical assumptions, rather than an unverified assertion about remote state.

This review adapts the requesting-code-review template to mathematical obligations. It used manual reasoning, source reads, and byte hashing only. No numerical search, scientific computation, tests, imports, implementation changes, or subagents were used. This report is the only file written by this reviewer.

## Strengths and alignment with the frozen scope

The argument supplies an arity-independent structural reduction: remove upper excursions while preserving the lower guard, then identify that guard with capacity-constrained subset coverage. Five-child targets 3 and 4 serve as diagnostics of this reduction. Target 3 is proved for arbitrary arity; target 4 requires a separate pair-cover-preserving mechanism. The candidate distinguishes sufficient root transport from necessary native transport, and explicitly leaves the general higher-target cover question open.

The proof uses actual single-incidence paths. Its auxiliary role merges are not incorrectly charged as compulsory prefixes from forbidden maximum-level vertices. Original-role packet membership is also kept separate from sequentially recomputed role membership; this distinction is essential to the lower bound.

## Findings by severity

- **Critical:** none found.
- **Important:** none found.
- **Minor:** none found.

No revision is required for analytical acceptance at this exact content boundary.

## Adversarial checks

### Sections 2–3: original-role packets and maximum-layer surgery

A single added incidence can lower the transversal by at most one because a hitting set using the new incidence can be repaired with one label from the old nonempty root. Floors guarantee the required nonemptiness. For a completed merge of the y role into x, adding y to any new hitting set repairs every newly covered root simultaneously. Choosing x and y in a minimum hitting set supplies the opposite inequality and gives transversal exactly t-1.

For two packets derived from original source roles in Z, adding both source labels repairs any hitting set. This proves the t-2 lower bound even when packet pairs share labels, when target and source roles overlap across packets, or when the packets add duplicate incidences. The proof never requires the packets to be disjoint or sequentially recomputed.

If a level-t vertex A neighbors a lower vertex C, monotonicity and the one-step bound force C to be A with one incidence added and to have value t-1. The union C union S(A) therefore lowers S(A)'s value by at most one. Each half of the replacement path contains one endpoint of value t-1 and is a subset of that union. These inclusions give both guards, and retain width floors during every deletion.

For two adjacent level-t vertices, their union Z is the larger original vertex and still has value t. Each merge packet selected at either original vertex is contained in the corresponding packet defined from original membership in Z. Thus S(A) union S(C) is a subset of Z augmented by those two full packets, giving the claimed lower bound in the correct monotonicity direction. Its addition/deletion paths preserve floors and stay below level t.

Every replaced maximum vertex has the same S(A) at both adjacent path segments, so the segments concatenate. Consecutive equal states can be omitted. Endpoints below t remain unchanged, each replacement is finite, and the maximum strictly falls. With L=q-1 and final maximum q, the last removed layer is q+1 and its lower bound is precisely q-1. This proves Theorem A, including its stronger downward-only excursion conclusion. The reverse direction is immediate from graph inclusion.

### Sections 4–5: complement criterion and arbitrary-arity target 3

For a root tuple, H fails to hit some root exactly when H is contained in a complementary block. Hence tau>=q-1 means every (q-2)-subset is covered. Exact-q endpoint feasibility guarantees k>=q; smaller hitting sets can be extended to size q-2 when needed. The q=2 empty-subset case is harmless because the block family is nonempty. Complement incidence moves reverse root incidence moves, and block capacities encode the positive root floors exactly.

Lemma C first reduces both covers to owner partitions. A full desired bin must contain a misplaced occupant, since otherwise its correct occupants plus the incoming label would violate the target capacity. Total capacity greater than k guarantees a spare bin. The two transfers remain legal if that spare bin is the incoming label's current bin: the displaced label is distinct and absent there, and the incoming label can subsequently leave. No correct label is displaced; each outer iteration fixes at least one new label. Final duplicate restoration stays inside target blocks. Zero-capacity bins do not create an exception.

At an exact-q tuple, a label in d roots gives a hitting set of size at most 1+r-d. Thus d<=r-q+1 follows without assuming that all labels are used. For q=3 this derives the required total complementary capacity at least 2k, rather than imposing new admissibility. Lemma C supplies a lower-guard path, and Theorem A removes its upper excursions. Theorem D is therefore valid for every stated arity and every feasible positive width vector.

### Section 6: compact endpoints and degree-two reconfiguration

Retaining one anchor from a minimum hitting set in each root permits compaction to its positive floor. Shrinking cannot lower tau and the surviving hitting set cannot raise it, so compaction stays exact. At five-child target 4, the incidence-degree bound is two and S<=2k follows.

In Lemma E, at completed transfers the remaining directed surplus/deficit edges describe current-minus-target occupancy at each column. If no pending edge ends at a free column, every column with an incoming edge is full; its outgoing count is at least its incoming count because target occupancy is at most two. Following directed edges therefore yields a cycle, from which a simple cycle can be chosen.

A row's surplus and deficit sets are disjoint, so adjacent cycle edges cannot have the same row color. There are at least two cycle colors. Since S<2k at completed-transfer states, some column z has at most one occupant; in the blocked situation it has no incoming edge and cannot lie on the cycle. One of the cycle colors is absent from z, making its buffer transfer legal. This also handles the case that z has a pending outgoing edge of another color: the buffer returns z to its old state and does not resolve or invalidate that edge.

Transferring backward around the simple cycle opens the next destination each time. Repeated nonadjacent row colors cause no duplicate incidence: original surplus and deficit sets of that row are disjoint, cycle columns are distinct, and other transfers of that row cannot prepopulate another pending cycle destination. The final buffered transfer restores z and resolves the entire cycle. Add-before-delete steps preserve each row floor, and every addition uses a column slot already freed or initially spare. Remaining differences strictly decrease at each greedy transfer or completed cycle. This proves the stated arbitrary-row Lemma E without an unproved swap-connectivity assumption.

For five rows, degree at most two excludes a two-label cover throughout, including the temporary extra incidence in a row. Nonemptiness gives tau<=5. Applying Theorem A to the resulting lower-guard path removes level 5 and yields tau in {3,4}.

### Section 6: saturated case

When S=2k, every compact endpoint column has degree exactly two. Any two disjoint edges in the corresponding child graph would give a three-label hitting set, contradicting tau=4. A pairwise-intersecting family of ordinary two-vertex edges is a star or is contained in a triangle; parallel labels do not change this classification. Nonempty roots on all five children rule out the triangle case and the degenerate single-edge cases. The hub is therefore present in every label and its width is k. The four other positive widths sum to k, so none can be another width-k hub. The same width vector forces the same hub at both endpoints.

The nonhub roots are a partition of P of fixed positive bin sizes. The stated four-step swap shares labels only between the two participating bins. The other two bins retain disjoint nonempty label sets, so three labels remain necessary; four remain sufficient. Floors hold at each step. Choosing a misplaced occupant from a misplaced label's full destination bin fixes at least one label without moving a fixed one, proving termination. Thus the saturated case closes the exact case not handled by Lemma E, and Theorem F follows for all feasible widths and palettes.

### Section 7: native lifting and interface consequences

The fixed-root clearance is the v16.53 mechanism with no dependence on sibling count. The child proper-descendant union has exactly a_i labels after normalization. A legal root deletion starts from a root larger than a_i, so a replacement label outside that union exists whenever clearance is needed. Preorder additions and reverse-preorder deletions preserve nesting and nonemptiness. Domination of the partial new role by the complete old role, then of the remaining old role by the complete new role, preserves every internal coordinate. The completed exchange retains the union size a_i. Leaves require only their direct nonempty deletion.

Consequently repeated root deletions do not require recursive normalization while the parent is inexact. Initial and final child normalizations occur at an exact parent; during lifted root transport every child interior remains exact. This establishes the global sum-of-deviations bound, not merely a bound at each coordinate considered separately.

The native conclusion is sufficient and conditional on inherited child interfaces and the required root connection. The text correctly does not infer a native obstruction from width-floor disconnection: a native unit path could leave the exact-child-width carrier by spending its deviation inside a child.

The finite nonempty-region enumeration, private-palette feasibility construction, minimum-width absence of unused labels, and positional canonical selection extend to arbitrary r. Abstract compaction plus inherited child feasibility is enough for the feasibility reduction; lifted transport supplies normalization where root connectivity has been proved. Attached role replacement and root-only contraction remain inherited arity-independent clauses. These statements do not prove every arbitrary-target join, and the candidate explicitly refrains from that inference.

## Recommendations

Preserve the stated separation when reporting this result: the general theorem is a reduction and upper-excursion-removal principle; the unconditional connectivity conclusions proved here are target 3 at arbitrary arity and target 4 with five children (alongside the elementary targets 1 and 2). The general pair/higher-subset cover problem is still the remaining obligation. Future implementation or numerical investigation requires its own prospective protocol and review.

## Declined to judge

- Universal connectivity for arbitrary feasible r,a,k,q>=4: explicitly OPEN in the frozen scope and candidate; no proof is asserted or supplied.
- Necessity of the width-floor root criterion for native unit repair, or any native nonunit barrier: the carrier is only a sufficient native model, as expressly stated.
- New implementation correctness, deterministic serialized move output, runtime, and path-length bounds: no implementation or such bound is part of this analytical candidate.
- Numerical coverage, campaign results, source-test agreement, actual-merge replay, and full-stage certification: no campaign is authorized or offered for review.
- Independent verification of remote commit ancestry, draft-PR state, or candidate-file placement on GitHub: supplied provenance was not independently fetched; the local proof's exact bytes were verified instead.
- Re-certification of the inherited v16.53 scientific implementation or all ancestral child-interface proofs: this review checks the supplied accepted interface mechanism as the declared hypothesis, not its full implementation lineage.
- Physical interpretation or optimization beyond the native finite incidence category: outside the stated problem.

## Assessment

**ACCEPT:** Theorem A, Corollary B, Lemma C, Theorem D, Lemma E, Theorem F, and the conditional arity-independent native lifting/interface consequences as precisely stated in the reviewed bytes.

**BLOCK if presented as established:** universal arbitrary-target connectivity, necessity of width-floor connectivity for native repair, a new native obstruction, implemented validation, or v16.54 certification. None of these stronger claims is made by the reviewed candidate.

The proofs meet the frozen analytical objective without a new numerical campaign. Acceptance ends at the explicit higher-subset-cover frontier.
