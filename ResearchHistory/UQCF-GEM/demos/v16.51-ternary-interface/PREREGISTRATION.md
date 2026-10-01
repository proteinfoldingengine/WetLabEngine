# v16.51 prospective ternary-interface campaign

Status: PREREGISTERED DESIGN; no v16.51 scientific execution, proof acceptance, or stage certification is claimed.

## Parent, scope, and prior knowledge

Exact verified integrated parent: `4a2866132b53c8400e10c425e1461143d9f3bdd9` (v16.50, PR #98); tree `9e80e59c31afef814d8de450d049e7fdbd561cd3`. The independent assistant closeout is published at commit `6ec0f63851b3456bc7493edd7e36e02b95f44fe9`, path `ResearchHistory/UQCF-GEM/audits/v16.50/4a2866132b53c8400e10c425e1461143d9f3bdd9/INDEPENDENT_CLOSEOUT.json`. There is no additional external-auditor dependency.

The primary question is whether a single genuine ternary parent with target hitting number two preserves the inherited fixed-root child repair interface, for three arbitrary finite full binary child trees. Targets one and three are boundary controls. The ternary vertex remains a ternary vertex: no artificial binary refinement is allowed. Repeated ternary composition and higher arity are outside this stage's theorem claim.

Before this preregistration, v16.50 established binary normalization and complete-role transport. The user supplied the triangle overlap example A={a,b}, B={b,c}, C={a,c}; it has hitting number two and is not a nonunit witness. Preliminary analytical reasoning in this conversation also identified the candidate route below: preserve one shared pair-label during child contraction; perform role transport only when all child interiors are exact; distinguish children occupying the whole root palette. These ideas, the candidate width formula, and the cyclic support assignment below are disclosed exploratory hypotheses, not prospectively discovered results. No v16.51 numerical science has been executed. This document freezes their subsequent falsification/validation and independent review.

## Frozen objects and child guarantees

Use exactly the parent's admitted states: each vertex carries a nonempty finite label support, each child support is contained in its parent's support, and the global root support is the fixed ordered palette P. A primitive move changes one nonroot label incidence while preserving admission. An internal hitting coordinate is the minimum cardinality of a label set intersecting every immediate child support. Leaves have coordinate zero. The primary path bound is the sum of absolute deviations from the target over ALL internal vertices, including the ternary root, at EVERY primitive state.

Primary B1, Binf, and Bs retain the parent's three independent scalar minimizations. LEX_BARRIER remains a separate diagnostic. A common unit-total-excursion construction supplies an upper bound; equality one is claimed only between distinct exact-profile components with the inherited integer lower-bound argument. No existence, uniqueness, or path-length claim about a selected physical evolution is made.

Extract and cite the following exact guarantees from v16.50 THEOREM.md:

1. Binary child width w(L)=1; w=max(a,b) for target one and w=a+b for target two, with necessity and sufficiency at a fixed root palette.
2. Canonical descendants on an ordered fixed root palette, distinct from the attached compact endpoint obtained by root contraction.
3. Fixed-root normalization from ANY admitted exact child state to that endpoint, total child excursion at most one, ending with every child coordinate exact.
4. Complete-role replacement by a label absent from the subtree: parent-before-child additions and child-before-parent deletions preserve every inner hitting coordinate. Its external parent must contain both labels.
5. Compact root contraction removes only unused labels and preserves the interior; leaves require the parent's attached-root convention.
6. Equivariance relabels the ordered palette together with labels; consecutive deviation phases must meet at whole-profile exact states.

## Proof obligations and frozen proposed route

T1. Establish the three-child classification: hitting one iff triple intersection is nonempty; hitting three iff all pairs are disjoint; hitting two otherwise. In particular, at target two a root-only deviation is at most one, but this does not permit a simultaneous child deviation.

T2. Prove or refute the proposed minimum root-palette width for child widths a,b,c:

- target one: M=max(a,b,c);
- target two: M=max(a,b,c,ceil((a+b+c)/2));
- target three: M=a+b+c.

For target two, test necessity using absence of triple incidence and sufficiency by the canonical assignment below. A false width or unavailable canonical state is a scientific failure of this proposed interface; it must not be silently replaced after observing outcomes.

T3. For target two, select a pair of initial child-root supports with shared label x. The third support excludes x. Normalize each child at its fixed initial root and then contract, retaining x in the selected pair. Specify and prove the palette-order choice that ensures x survives contraction. Root hitting must remain exactly two during every child deviation. The construction must cover arbitrary admitted exact initial states, not merely the directed corpus.

T4. Map the resulting compact child roles to the prescribed canonical endpoint while all child interiors remain exact. If child width is less than |P|, prove that the available absent label permits every required role assignment and permutation, including spare-free final support assignments. If child width equals |P|, prove and explicitly use the constraints on the other two roots, and show how to achieve the prescribed internal canonical order without stacking. Do not assume an absent label exists in this case. Treat pairwise overlap distributed over three different labels explicitly.

T5. Establish termination, fixed global root, legal individual additions/deletions, exact phase endpoints, common canonical endpoint, attached compact contraction, and ordered-palette equivariance. Review the GLOBAL excursion sum, not separate coordinate or subtree bounds. If T1--T5 hold, concatenate two normalizations to obtain the scoped barrier consequence. Do not extrapolate to recursive ternary trees in this stage.

T6. Check target-one and target-three boundary constructions: respectively a common anchor and disjoint child palettes. A role swap for target three must not merge all three branches at once. Boundary controls do not replace T3--T4.

## Frozen directed validation universe

Let L be a leaf, C=(L,L), D=(C,L), and F=(C,C), with the indicated child order. Use exactly the ternary-root shapes T=(C,C,C) and U=(C,D,F). T has three binary internal vertices plus its ternary root; U has six binary internal vertices plus its ternary root. Vertex indices are preorder, child order as written. No larger shape family is substituted.

For every binary target profile in {1,2}^3 for T and {1,2}^6 for U, in lexicographic preorder, combine all root targets r in {1,2,3}, palette sizes k=M and M+1, global relabelings identity/reversal/cyclic j->(j+1) mod k, and the two start modes below. Specification identities include shape, full target, k, relabeling, and mode. Retain distinct specification identities even if raw states coincide.

Canonical state before relabeling: P=(0,...,k-1). For r=1 assign each child the first w_i labels. For r=3 assign consecutive disjoint blocks of lengths w_i. For r=2 place consecutive blocks of lengths a,b,c at positions 0 through a+b+c-1 modulo M in the first M labels of P, assigning each block to its corresponding child. Child supports are sets, ordered by their inherited order in P for recursive v16.50 canonical descendants. Keep the global root equal to all P. This construction is a hypothesis subject to T2 and independent validity checks.

Start modes:

- `compact`: the above canonical state followed by the designated global relabeling.
- `interface_and_binary_inflated`: begin with `compact`; visit the three root children in order, and labels 0 through k-1 in order, adding a missing label to that child's root if and only if the ternary hitting number remains r. Then visit every binary internal vertex in preorder; at target-one vertices expand both immediate child roots to that vertex's current support. Retain all other incidences. This deterministic single sweep, with no repeated search for a fixed point, defines the start.

There are exactly (8+64)*3*2*3*2=2592 directed specification cases, of which 864 have root target two. These cases are not an exhaustive state-space universe. Normalization targets the unpermuted canonical state on ordered P; equivariance is checked separately with the order transported too.

The producer must retain exact identities, shapes, targets, candidate widths, initial states, every primitive intermediate state, endpoint, and success or explicit construction failure. It must not discard an invalid start or failed case. Any infeasibility of a frozen case triggers a recorded failure and blocks a validated outcome.

The independent verifier reconstructs the complete 2592-identity set and all starts/endpoints from this document, independently of producer code. It uses support sets and explicit hitting-set minimization at the ternary node, independently checks the candidate widths on these fixed cases by finite root-support feasibility, and recomputes every inner coordinate and total excursion at every primitive. For each distinct (a,b,c,r), the width check must establish feasibility at M and infeasibility at M-1, including the empty-palette boundary. Enumerate nonnegative counts in the seven nonempty three-child incidence regions, with their sum at most the tested palette size, each child cardinality at least its inherited width, and hitting number computed independently from the occupied incidence regions. Unused labels are allowed. This avoids enumerating interior states or repeatedly enumerating all labeled support triples; cache only by the complete (a,b,c,r,palette-size) identity. Exact case identity equality is mandatory; supplied-record checking and counts alone are insufficient. Width feasibility checks are confined to this interface and do not replace the composition argument.

## Substantive controls

Require direct controls for: triangle overlap at T with binary targets (2,2,2), k=3; asymmetric U; minimum and one-spare palettes; anchor excluding label zero; every choice of shared pair; a child of width k with the other children nonempty and disjoint; a width k-1 child requiring an internal role permutation; relabeling with palette order transported; exact end-of-phase profiles; and both root-plus-child and two-child simultaneous unit defects whose total is two and must be rejected. Give controls explicit states and exercised production branches before science; assertions must detect removal of the intended mechanism.

Reject omitted, duplicated, substituted or extra case identities; wrong target/width/start/endpoint; empty or unnested supports; nonprimitive or root-changing moves; understated total excursion; false profile values; false coverage/provenance; producer-dependent verification; altered preregistration; and scope claims beyond one ternary root with binary descendants. Preserve genuine GitHub RED for the missing ternary mechanism and for an otherwise-valid corpus with one identity removed before adding the implementation. The omission RED must reach and fail the exact-universe assertion through the verifier; an import, missing-interface, or fixture-setup failure does not establish that control.

## Competing outcomes and stopping rules

`TERNARY_Q2_INTERFACE_VALIDATED`: independent analytical review accepts every scoped proof obligation and all frozen cases, controls, reproduction, and closure gates pass. The theorem's generality comes from the proof, not finite paths.

`INTERFACE_NOT_PRESERVED`: identify an exact failed guarantee, proof gap, illegal step, width/canonical failure, or overcost proposed path. Preserve the input, raw attempt, and failed obligation. Failure of this construction is NOT evidence that every legal path has nonunit barrier.

`INCOMPLETE`: coverage, resource, provenance, review, publication, reproduction, or closure is incomplete. Report which gates remain unmet. Failure may close a fully audited diagnostic campaign, but cannot be relabeled a validated theorem.

No `NONUNIT_WITNESS` outcome is available from directed normalization failures. Such a claim requires a separate prospectively amended experiment with an independently verified complete unit-threshold cut on a precisely declared admitted finite graph AND an admitted unrestricted connecting path for the relevant independent scalar objective.

Freeze the entire corpus before implementation. No result-dependent expansion, case dropping, early-success stopping, or post hoc conversion of exploratory reasoning into preregistered discoveries. Amendments preserve the original protocol and failed evidence, disclose their timing, and precede affected execution.

## Execution and full closure contract

Commit this protocol and its execution plan as a direct child of the exact integrated parent before new scientific execution. All numerical science and tests run on GitHub Actions ONLY: ubuntu-24.04, Python 3.11, Sympy 1.13.3, mpmath 1.3.0. Local source inspection and byte/hash/Git auditing are allowed. Run all 994 inherited checks and freshly reproduce the complete v16.50 scientific stack, requiring byte identity for its 36 scientific files, plus the new substantive controls. Before EACH GitHub execution, commit a versioned manifest of its exact expected test identities, counts, assertions and intended outcomes, including development RED/GREEN runs. Freeze the complete new suite before the definitive scientific campaign, preserving all earlier development runs; additions and changes require prospective disclosure in a new manifest before affected execution and renewed verification.

Independent proof/source review precedes the definitive campaign. Science and fresh reproduction use separate Actions runners. Preflight timeout 5 minutes; science, fresh reproduction, publication, and actual-merge replay each 45 minutes; receipt 10 minutes. Exhaustion yields INCOMPLETE; no adaptive weakening of the frozen cases. Record workflow SHA, checked-out science SHA, exact attempt, workflow, dependency versions, logs, full source/input manifests and complete raw paths in uploaded artifacts. Audit downloaded artifact bytes, SHA-256 digests, exact manifest membership and Git blob bindings. Publish all scientific evidence durably, review and merge the exact verified head, replay the actual merge, independently audit the receipt and publish the independent decision before CLOSED/CERTIFIED. An independent assistant reviewer is sufficient under the documented contract; no external-auditor dependency is invented.

No physical energy, action, metric, gravity, or fundamental-time claim follows from this combinatorial campaign.
