# v16.24 — Exact consistency order of retained views

Sequential first-principles continuation of v16.23, parent `3dda0f9f0aa6882a9acacc39fd709f779460cfb2`.

**Result:** for a fixed family of actual retained prefix views, the least positive worst-case testing order is the maximum, over union vertices, of the minimum number of views needed to cover that vertex's immediate children, bounded below by one. Sufficiency and sharpness are proved for arbitrary finite covers in the declared formal nonnegative rational cone.

Consequently, pairwise nonnegative feasibility suffices on binary prefix trees. It does not suffice at arbitrary branching: an m-leaf star can require all m views, even when every proper subfamily is feasible. This classifies the existing global consistency obstruction; no source/response model or geometric target is added.

- [Combined findings and boundaries](demos/v16.24-consistency-order/RESULTS.md)
- [Types, provenance and proofs H0–H6](demos/v16.24-consistency-order/TYPE_AND_PROOF.md)
- [Preregistration and complete test universe](demos/v16.24-consistency-order/PREREGISTRATION.md)
- [Full scientific certificates](demos/v16.24-consistency-order/evidence/certificates.json.xz)
- [Independent verification](demos/v16.24-consistency-order/evidence/VERIFICATION.json)
- [Durable publication/run provenance](demos/v16.24-consistency-order/PUBLICATION_EVIDENCE.json)
- [Reproduction](demos/v16.24-consistency-order/REPRODUCE.md)

Corrected scientific GREEN: [36585110111](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36585110111), execution `19c7069bad79ff361d612f742ad5e79dbfef1dc6`. Thirty new/validation tests plus 82 inherited tests passed. The publication workflow independently reruns and binds its own execution/commit; read its receipt before asserting publication completion.

Original-coordinate coverage: 17 rooted shapes, 3,522 complete covers, 94,185 compatible integer local-source families of total at most two, and 1,841 separate sharpness witnesses. Cover orders: 1,681 of order one, 1,720 of order two, 120 of order three and one of order four. The full enumeration is repeated under actual relabeling and storage reversal. The order-four witness uses total three and is not falsely counted in the total-at-most-two sample grid.

Review is self-review with an algorithmically independent verifier, not a separate reviewer. No merge to main, historical rewrite, physical source attainability, quantum contextuality, geometry or gravity is claimed.

**Time is pruning / ordered recoverability update.**
