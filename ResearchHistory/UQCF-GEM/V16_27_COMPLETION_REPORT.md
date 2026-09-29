# v16.27 — Completed independent verification and durable evidence

The scientific finding remains: **actual per-event delta-h attribution is generally path-dependent, while the endpoint sum h(final)-h(initial) is invariant.** This finishes v16.27; it does not start v16.28.

[Combined completed findings](demos/v16.27-increment-attribution-closure/completion/RESULTS.md) · [Types and complete arguments C1–C7](demos/v16.27-increment-attribution-closure/completion/PROOFS.md) · [Reproduction](demos/v16.27-increment-attribution-closure/completion/REPRODUCE.md)

The original verifier called the producer for coverage and missed several malformed witness fields. A substantive contract RED exposed seven failures; the identical checks pass against a replacement that imports no producer. The replacement independently checks the COMPLETE path set and every intermediate invariant, rather than only counts or a selected example.

Corrected scientific GREEN: **36625099103**, execution **a89f4cabc484612ed2924247245a0a8a2adab6d2**, job **109599923952**, attempt **1**. **170 tests passed.**

The independently reconstructed original universe agrees with the earlier counts: eight rooted shapes through four vertices; 3,486 endpoint refinements; 3,446 multipath; 1,091 path-dependent; 56,498 complete legal paths. Every case/path is also checked under the actual relabeling and storage reversal. Raw complete path certificate: 22,500,736 bytes, compressed to 203,300 bytes. All raw paths, local profiles, h values, deltas and triggers are included—not merely stream digests.

[Full raw certificates](demos/v16.27-increment-attribution-closure/completion/evidence/FULL_CERTIFICATES.json.xz) · [Explicit admissible witness](demos/v16.27-increment-attribution-closure/completion/evidence/WITNESS.json) · [Independent verification](demos/v16.27-increment-attribution-closure/completion/evidence/VERIFICATION.json) · [Publication/run evidence](demos/v16.27-increment-attribution-closure/completion/PUBLICATION_EVIDENCE.json)

The old reports/code are preserved. Historical GREEN is not retroactively credited with the new checks. The publication record separately identifies original executions, the new scientific execution and the fresh publication reproduction.

**Scope:** h is a consistency-testing order, not information amount or physical time. This result establishes neither a physical-time no-go nor geometry. Review is self-review with an algorithmically independent verifier, not an independently authored review.

**Time is pruning / ordered recoverability update.**
