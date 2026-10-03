# Independent A11.X13 whole-argument review

Decision: ACCEPT — no mathematical revisions requested.
Reviewer: independent agent /root/x13_whole_argument_review, requested under the user's fresh whole-argument review requirement.
Candidate: 81cc1d59fb7ae79328cdcb0129f216a57c9a31bf.
Source: A11_X13_NARROW_PALETTE_PROTECTION.md.
Git blob: 899a9eab99c3cb25b0ecd4ddc6abcf38e039f2af.
SHA256: bbb17c815f8bbce1cb27982452cceb87052f553739ca36f0af2433cbad6bbf84.
Scope: 4bd9d85475b4070731b985c8d1099941872d7379.

## Attributable independent report

The following is the reviewer's actual mathematical report, preserved with its decision. Formatting of identifiers is normalized for this receipt.

I read the actual candidate, accepted X12 proof at 1216c1007b0a91cf5e6c0a1c14d813a81dcc23b9, actual GUARD_HANDOVER.md, and the relevant frozen baseline sources for maximum-layer removal, full endpoint permutation, and palette-room connectivity at 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.

The new completion bound is correct. A colourful selection hits the actual disjoint guard blocks. For each additional support, its fraction of missed selections is the product of the blockwise omission fractions; palette exhaustion and the original floor bound their sum, so AM-GM supplies the stated upper bound. The union bound proves an existing full-family transversal whenever b*(1-1/t)^t<1. Consequently the necessary integer lower bound is exactly ceil((t/(t-1))^t). This argument tracks the same support across all blocks and assumes no independent capacities. For three disjoint triples exhausting nine labels, three additional roots cannot raise transversal to four.

The exact endpoint protection and degree deductions are correct. Exact compaction retains a supplied four-cover and cannot decrease transversal, so it preserves exact four at every primitive. Every avoiding-label family is an actual three-guard. A three-root three-guard must have pairwise disjoint supports. Therefore k<3h forces at least four avoiding roots and yields the stated compact incidence constraint. These endpoint deductions are appropriately withheld from arbitrary inexact prefixes.

The six-vertex cubic multigraph argument is complete. If the induced four-vertex graph contains a matching of size two, the chosen initial edge completes it. Otherwise its distinct edges form a star or lie in a triangle. The star's leaf-degree requirement contradicts the combined centre/external degree budget. In the triangle case, the isolated fourth vertex requires three external edges; parity forces exactly one external triangle edge. The resulting degree equations provide the three matching edges claimed. Parallel edges are handled consistently and no loop can arise from the incidence construction.

The six-root feasibility theorem follows. Below nine labels the compact eighteen-incidence count contradicts the degree-at-most-two requirement. At nine labels, degree three would expose the prohibited exhausted-palette three-block completion; degree above three already contradicts exact four. Thus every label has degree exactly two, giving the loopless cubic six-vertex multigraph and its actual three-label hitting set. This excludes noncompact endpoints too, because their legal exact compaction would produce the same contradiction. The ten-label hub supplies the converse.

The complete repair conclusion uses inherited results within their domains:

- For 10<=k<18, eighteen compact incidences force degree at least two. The corresponding actual avoiding family leaves enough slots to place the hub's three-root guard with at most one overlap.
- Full endpoint token permutations are justified by uniform original floors. They are implemented by finite safe swaps of exact-four tuples, rather than treated as primitive moves or applied to an unprotected level-three guard.
- The O1 bridge supplies a missed actual root for every forbidden pair. Initial preparation retains the old guard; shared-slot transfer uses the union comparison certificate; remaining edits retain the installed destination guard.
- Every scheduled addition or deletion has a supplied eligible incidence and retains an original floor-safe endpoint support. The finite symmetric-difference schedule terminates.
- The preliminary path maintains the lower guard. Maximum-layer removal is explicitly distinguished from that schedule and supplies the final {3,4} band.
- At k>=18, palette-room AE applies using the original floor sum eighteen and existing palette labels.
- Each leg returns to the same original full labelled exact-four hub. Reversing the second leg restores every original destination support, including excess incidences. Exact joins permit repeated reuse.

The scope is accurately limited. X13 establishes a coupled completion obstruction and the full six-root feasibility/repair consequence; it does not claim a new necessary multiple-overlap handover, native disconnection, universal mixed-floor or nested closure, physical interpretation, numerical certification, or efficiency improvement. The residual possible domains k=8,r=7..8 and k=9,r=7..9 are consistent with accepted X12 coverage and the new six-root exclusions, without asserting feasibility of every tuple.

This is independent analytical acceptance of the immutable candidate and its supplied whole argument. It is not numerical execution, source re-certification, or v16.55 implementation certification. No enumeration, tests, workflows, or branch mutations were performed during this review.
