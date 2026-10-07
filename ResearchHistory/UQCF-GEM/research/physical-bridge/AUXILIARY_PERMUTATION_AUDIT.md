# Reusable auxiliary permutation theorem — author-side audit and review gate

Date: 2026-10-07.
Status: PROOF CANDIDATE / AUTHOR-SIDE AUDIT PASSED / INDEPENDENT REVIEW PENDING.
This is NOT an independent verdict or scientific certification.

## Immutable sources

Scope commit 51bb75d3ca71f35c62b480eee21e6f9afcdd6fbb
Scope blob 8f05c9d376a3f45f267a8976890dfbb12ed9c4c9
Proof commit dcec4d02f79539c4b4ba0e5eb827917149040e77
Proof blob b9b2b37dbf548d3469eb11237434168cc339c41e

## Author-side whole-argument checks

1. A nontrivial permutation cycle (i1,...,il) is oriented so target of i_j is original label of i_(j+1); the reverse-order replacement fills the currently freed label at every step.
2. Each addition introduces a globally absent label, including the auxiliary w. Each deletion removes a label from a root that has just acquired a second label. Hence all supports stay nonempty and pairwise disjoint.
3. For n disjoint nonempty roots, tau=n exactly. For n=3,4 this stays in 3<=tau<=4.
4. After each cycle w is absent and all cycle targets are reached; w is reusable across all c nontrivial disjoint permutation cycles.
5. Per-cycle count is 2+2(l-1)+2=2(l+1); total 2m+2c.
6. For n=3, any first endpoint-only deletion empties a floor1 root; any first endpoint-only addition duplicates an occupied target label and reduces tau to2. No protected endpoint-only first event exists.
7. For n=3 with a single nontrivial cycle, each of 2l endpoint-differing incidences must be toggled, and at least one off-endpoint addition and corresponding deletion are needed. This gives lower bound 2l+2 attained by the construction.
8. For n=4, the displayed endpoint-only swap is an explicit rejecting control against a universal necessity claim for w.
9. The result does NOT imply one buffer suffices for arbitrary overlapping supports, general dependency graphs or n>4 within the target-four band.
10. No physical meaning is attributed to w.

## Separate external review initiated

Independent adversarial research-agent job:
    01a117ed-cd22-7520-b6d1-c6423766f657
Thread:
    01a117ed-cd5c-776b-967a-f349a433e468

The independent reviewer was instructed to read immutable scope/proof, seek counterexamples and return ACCEPTED/REVISE/REJECT. Its verdict has NOT yet been incorporated here.

## Next gate

Wait for the independent result, preserve exact provenance and reconcile any proof corrections. Only then publish a final accepted scoped closeout. Further auxiliary-cycle generalization should not inherit an unreviewed candidate as certified.
