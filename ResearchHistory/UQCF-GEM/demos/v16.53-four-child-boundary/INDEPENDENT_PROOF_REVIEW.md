# Independent analytical review: four-child joining

**Verdict: ACCEPT as an analytical joining theorem.** No Critical or Important mathematical defect was found in the reviewed argument. One Minor specification clarification was addressed and rechecked; no findings remain outstanding. This verdict is independent analytical review, not implementation validation, execution replay, or full-stage certification.

## Review scope and evidence

I read the native-admissibility specification, scope, complete candidate four-child proof, and accepted v16.52 six-clause interface. I checked their mathematical obligations directly, including individual primitive admission and the global excursion bound. I did not run numerical scientific computations, tests, searches over cases, or implementation code. File reads and SHA-256 hashing were the only execution used to inspect evidence; writing this report does not change scientific source.

The supplied provenance identifies parent `b6bf95798ec5892963c29f4020f8b75069fd2e3b`, native/scope commit `8fcc46597ab7c2b83fe9dd2fd0611a07e66169cd`, and initial candidate proof commit `088f6e4cd3c4c19df13aac5ab6d31be30559ea75`. The final reviewed local proof additionally contains the two canonical-specification clarifications described below and a status-header update pointing to this review. I reread that complete revised proof. This review did not independently query GitHub commit ancestry. Its precise accepted content boundary is the following local byte hashes:

| Document | SHA-256 |
|---|---|
| NATIVE_ADMISSIBILITY.md | `a08edf466b041d00932e197dac01d6845bfd202ac317e6debf4695db770e9e23` |
| SCOPE.md | `c13dd50e6b32a03c04670ab4efbdebbd8cec0f8cd958ebd92e425b233f0854a1` |
| FOUR_CHILD_INTERFACE.md | `a42d22c25568475f8e9373c6288646b1b68abdc90ecc657a517a0375990f8872` |
| v16.52 INTERFACE_LEMMA.md | `2ed71f0e20e60060bff002e4741119434ee8c97cc031738686ebeec25935b133` |

## Findings by severity

**Critical: none.**

**Important: none.**

**Minor — canonical encoding and the q=4 wording.** Section 2 should explicitly specify the concatenation order of the four positional membership strings and the alphabet order used for lexicographic comparison. Section 7 should refer to the disjoint canonical tuple selected in Section 2, or explicitly establish its chosen consecutive-block convention. Ordinary `0<1` with child-major strings places earlier children on later blocks, whereas `1<0` gives earlier blocks to earlier children. Both choices support the proof, but an implementation must not silently substitute one endpoint for the other. The role-assignment argument works for either disjoint tuple, so this is a deterministic-specification clarification rather than a joining obstruction.

**Resolution: addressed.** The revised Section 2 specifies children 1 through 4, increasing palette positions, and bit 1 before bit 0. Revised Section 7 explicitly targets that same tuple A_i* without a separate block convention. I inspected both changes and reread the revised proof; the issue is closed.

## Adversarial obligation checks

### 1. Exact feasibility and the finite width definition

The width minimum exists. Identifying one selected label in each of `5-q` initially disjoint child palettes leaves `q-1` isolated palettes. The resulting transversal number is exactly q, including q=1 and q=4. Each root keeps precisely its required number of distinct labels. The 15-region formulation is equivalent: multiplicities determine cardinalities, and covering all four indices with occupied region types gives exactly the minimum transversal number. Repeated labels in one type cannot improve a minimum cover.

Native feasibility implies compact feasibility without assuming the desired four-child theorem. Each child root in an exact native state has size at least its inherited width. A minimum parent transversal H supplies an anchor in every child. Child normalization with that anchor ordered first is legitimate because the inherited interface is quantified over every ordered palette. Its root is fixed, so it leaves the parent exact. Subsequent root contraction retains that child's anchor. Shrinking supports cannot lower the parent transversal number, and the surviving H bounds it above by q. Sequential compression therefore produces the required compact tuple on the existing palette.

Conversely, a minimum-width tuple plus the inherited canonical children constructs a native exact state on every larger palette by retaining extra labels only at the new parent root. A minimum tuple cannot have an unused label: dropping such a label would contradict minimality. This also proves the canonical proper-descendant union is precisely the width prefix. No failure filtering or unproved extrapolated middle-target width formula is used.

### 2. Clearance below a fixed child root

After the initial exact-parent normalization, a nonleaf child's proper-descendant union has exactly its width a. If a proposed root deletion leaves at least a labels, the current root has more than a labels. Consequently, when the deleted label x occurs below the root, a label y exists in that same root outside the proper-descendant union. This local slack is enough; global absence is not required.

During preorder additions of y, its child-incidence pattern at every internal vertex is contained in x's unchanged pattern. Every transversal using y can substitute x, while adding incidences cannot increase the minimum. During reverse-preorder deletions of x, y has the complete original pattern and the residual x pattern is contained in it. These two inequalities prove exact coordinate preservation, including the child-root coordinate. Nonemptiness follows from installing y before removing x. Nesting follows from preorder addition and reverse-preorder deletion, with both labels available at the unchanged boundary root.

The completed operation exchanges x and y in the proper-descendant union, keeping its cardinality a. Root additions do not alter that union. Thus the invariant required by the next clearance survives every lifted step. If x is unused below the root, direct deletion is valid. A leaf has no interior clearance obligation and its root remains nonempty since its width is one.

The phrase “full-width children require no deletions” is correct when full width means a=k; deletion would violate the size constraint. A root initially equal to P with a<k can undergo clearance and deletion normally. No special exception invalidates that case.

### 3. Global excursion and the q=1,2 paths

Initial and final recursive normalizations occur only when the outer parent is exact and every inactive child subtree is exact. Their inherited total excursion bound therefore remains a total bound in the joined tree. Clearance does not spend any interior excursion. During root transport the only changing coordinate that can be inexact is the new parent.

For q=1 or q=2, expanding roots to P monotonically decreases the transversal number. Contracting toward the target keeps each root a superset of its target, whose transversal still hits every intermediate root. Nonempty roots rule out zero. Thus the parent remains in {1} or {1,2}, respectively. All root sizes remain at least their child widths. The lifting argument applies throughout, including minimum palettes and arbitrary tree depths.

### 4. Cover reconfiguration and q=3

At a completed one-owner partition the occupancy is exactly k. The strict capacity surplus therefore supplies a free slot whenever needed. If the desired bin j is full, it must contain a label y not destined for j; otherwise its already correct occupants together with x would exceed the target partition's allowed capacity. In particular, b_j=0 cannot occur for a label whose target is j.

The spare bin differs from full bin j. Moving y there uses an existing free slot and creates space in j; moving x to j then fixes x. Each transfer is add-before-delete, preserving coverage, and the temporary duplicate respects the receiving bin's capacity. The spare bin is permitted to be x's current bin if it has room. No fixed label is moved. The number of correctly assigned labels strictly increases at every iteration, although the displaced y may also become correct. This proves termination without requiring a bound on the number of possible covers. Once the target owner partition is reached, extra target occurrences can be added because intermediate bins remain subsets of the target bins.

In an exact four-root q=3 tuple, a label in three roots would hit those three and need at most one additional label for the fourth, contradicting q=3. Hence total root size is at most 2k, and the sum S of child widths is at most 2k. Exactness also implies k>=3. Thus complementary capacities satisfy `sum b_i=4k-S>=2k>=k+1`.

Complementary coverage is exactly the absence of a common label in all four roots. Together with `|A_i|>=a_i>=1`, this puts the parent in {2,3,4}. Every cover move has a legal root counterpart; zero capacities cause no exception. The required surplus is derived from exact native admissibility, not added as an independent hypothesis. The final canonical tuple is exact, so final child normalizations are authorized by the global budget.

### 5. q=4 role transport

Four nonempty roots have transversal number four exactly when they are pairwise disjoint. If any two intersect, their shared label and one label from each of the remaining roots give a transversal of size at most three. Initial child normalization and contraction preserve this disjointness.

For an exchange between two compact child roles, the first complete-role replacement introduces only the other child's role label as a possible cross-child overlap. Its own subtree lacks the incoming label, as required by the inherited role interface. After it finishes, the old label is absent from the second child, permitting the reverse replacement there. Throughout, two untouched children remain disjoint from both active children and each other. The parent therefore has value three or four; every child interior remains exact. A replacement into a globally unused label preserves disjointness outright.

Same-child swaps can be decomposed into three cross-child swaps with another nonempty child's role as pivot. Each completed swap restores disjointness, and the three-swap sequence restores the pivot. Previously fixed roles may serve as temporary pivots but are restored at the end of the operation. Processing ordered target roles terminates and realizes the chosen canonical role assignment. There is always another nonempty child to supply the pivot. This reasoning does not require an extra palette label.

### 6. Identical interface and noncircular induction

The returned canonical endpoint is compact; its root-only surplus labels can be deleted in an attached context without changing any interior coordinate. Restricting to the width prefix leaves the positional canonical construction unchanged. Complete-role replacement remains the same arity-independent domination argument, with external-parent control explicitly left to its caller.

Every construction uses finite operations and positional choices. With the addressed encoding clarification, transported palette order determines the same transported endpoint and primitive sequence. The induction is structural: the new join invokes the six clauses only for strictly smaller children; its feasibility argument does not invoke its own normalization theorem. Inspection of the accepted binary/ternary proof confirms those joins also consume the interface rather than a descendant-arity restriction. Therefore the leaf case and these three joins establish the same interface for all finite ordered trees of arities 2,3,4.

## Result and limits

The argument delivers the reusable interface, rather than a collection of additional binary/ternary examples. The two unsafe middle-target transport sequences demonstrate failure of an unrestricted transport shortcut only. They do not prove unavoidable nonunit separation; the guarded normalization paths instead give a unit upper bound between any two admitted exact endpoints on the same fixed root and profile.

The scalar-barrier corollary retains the inherited scalar definitions and their integer lower-bound interpretation. This review establishes the stronger explicit total-coordinate path bound used for the upper bound; it does not independently re-audit scientific source implementing those scalar objectives. No assertion of multiple exact components, minimal path length, arity beyond four, physical interpretation, implemented protocol, passing numerical campaign, or stage certification is licensed by this acceptance.

No mathematical proof obligation remains OPEN within this analytical scope. The Minor canonical specification is resolved. Future implementation, validation protocols, execution evidence, and certification remain separate gates.
