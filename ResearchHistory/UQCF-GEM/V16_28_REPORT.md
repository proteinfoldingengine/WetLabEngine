# UQCF-GEM v16.28 — Exact event-attribution criterion

Continues the completed v16.27 publication `134b3d6c3358d91df2e34a9bb57ac82a2f0406ce` on an additive research branch.

## Main result

For a fixed same-union retained refinement, the actual event increments are path-independent **if and only if** every reachable commuting-deletion diamond has zero mixed difference:

    D(S;e,f)=F(Sef)-F(Se)-F(Sf)+F(S)=0,

where F(S) is the existing consistency-testing order h after deleting the ideal S. This is equivalent to a unique additive representation F(S)=F(empty)+sum w_e, with actual w_e in {0,1}, and to the modular identity on reachable event ideals.

If D is nonzero, the certificate constructs two full legal paths with identical endpoints and common prefix/suffix whose event attributions differ. The two path totals still agree. D is NOT curvature, holonomy, physical time or failure of pruning-map composition.

## Verified scope

All 3,486 endpoints of .27's frozen universe are independently classified: **2,395** are attribution-independent, including **1,302** with a nonzero fixed coefficient; **1,091** are dependent. The original-coordinate audit reconstructs **34,562 states**, **45,488 diamonds** and **56,498 full paths**, plus a complete relabeled/storage-reversed copy. Positive and negative mixed differences both occur.

**198 tests passed.** Scientific GREEN: [36629091598](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36629091598), execution SHA `02954512b3e84e62a978dfe56f6007c501ef3b7f`.

[Combined findings](demos/v16.28-diamond-attribution-closure/RESULTS.md) · [Types and proofs D1–D7](demos/v16.28-diamond-attribution-closure/PROOFS.md) · [Publication provenance](demos/v16.28-diamond-attribution-closure/PUBLICATION_EVIDENCE.json) · [Reproduction](demos/v16.28-diamond-attribution-closure/REPRODUCE.md).

Scope: formal finite common-Genesis retained-view h. Physical source attainability, response-law selection and the operational quantum bridge remain open. Review is self-review with an algorithmically independent verifier.

**Time is pruning / ordered recoverability update.**
