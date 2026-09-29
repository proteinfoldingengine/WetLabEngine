# UQCF-GEM v16.29 — Local profile versus maximum aggregation

Sequential foundational continuation of completed v16.28.

## Main result

The mixed difference of the existing scalar h=max(1,max_v tau_v) is not, in general, a faithful indicator of mixed dependence in the local tau profile.

- Nonzero scalar D_h can occur while EVERY local D_v is zero: explicit admissible examples realize both signs.
- A nonzero local D_v can be hidden while all scalar h values are equal.
- For events with different parents, every local D_v vanishes and D_h=-(delta_e h)(delta_f h).
- For a common parent, the exact law is the thresholded four-state difference with background B fixed by the unchanged profile. PROOFS.md L1–L7 establish the complete cases.

This does not invalidate .28's theorem for its specified scalar F. It identifies the boundary of extending that theorem to richer local data. No response model or geometry is introduced.

## Verified coverage

All 45,488 original .28 diamond occurrences and their transported copies were reconstructed. All its nonzero values are locally transmitted, consistently with its <=4-vertex boundary.

The extension through five vertices checks **54,842** actual two-event squares: **5,755** locally transmitted, **32** maximum-only, **19** local-but-hidden, **49,036** zero in both. Its full relabeled/storage-reversed copy is also verified. A separate six-vertex control realizes positive maximum-only dependence.

**228 tests passed**, including 198 inherited tests. Complete raw certificates: 97,275,232 bytes compressed losslessly to 1,731,596 bytes. Scientific GREEN **36637296991**, SHA `5d09e6c28827f70412c5f8b05fd98af75d3b7e5f`. Exact publication provenance is recorded separately in the linked receipt.

[Combined findings](demos/v16.29-local-profile-closure/RESULTS.md) · [Typed proofs](demos/v16.29-local-profile-closure/PROOFS.md) · [Publication evidence](demos/v16.29-local-profile-closure/PUBLICATION_EVIDENCE.json) · [Reproduction](demos/v16.29-local-profile-closure/REPRODUCE.md)

Self-review with an algorithmically independent verifier; no separately authored review. h remains a consistency-testing order, not a physical interaction or temporal quantity.

**Time is pruning / ordered recoverability update.**
