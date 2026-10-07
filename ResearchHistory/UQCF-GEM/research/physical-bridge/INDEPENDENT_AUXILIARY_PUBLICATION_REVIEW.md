# Independent publication consistency review — auxiliary permutation theorem

Date: 2026-10-07.
Status: ACCEPTED WITH REPORTING CLARIFICATIONS (already reconciled).
This is a separate publication/reference consistency review, not the original mathematical proof review.

## External review provenance

Model: spark-2
Job: 01a11806-6b95-729b-bac7-8ec3c8233402
Thread: 01a11806-6bc2-7568-b106-bb97a84b1bf5
Status: completed
Verification status: verified; both exact pinned GitHub documents retrieved.

## Immutable material reviewed

Frozen theorem: dcec4d02f79539c4b4ba0e5eb827917149040e77
Independent mathematical review: 361e5931368e44b2bfc6c82fad7483d92c05455a
Frozen scope: 51bb75d3ca71f35c62b480eee21e6f9afcdd6fbb

The earlier publication audit job 01a117ff-f16a-72fd-8f71-ab5b6dc722d1 was NOT a valid rejection of the research-branch publication: it checked the repository main tree rather than the pinned research commits. The corrected audit directly retrieved the immutable documents.

## Exact independent publication verdict

The external audit concluded: "Accept the theorem as publication-consistent within its frozen scope, with the three reporting-precision corrections above. No substantive mathematical correction is required."

The three required reporting clarifications:
1. One reusable label applies within n in {3,4} for the protected-band theorem; the same combinatorial construction beyond n=4 has tau=n>4.
2. The 2l+2 optimality statement is restricted to one nontrivial cycle at n=3 under sequential one-incidence toggles.
3. Explicitly define tau as the minimum cardinality of a label hitting set of the original root supports.

All three are recorded in AUXILIARY_PERMUTATION_PUBLICATION_STATUS.md at b6b738f54dd7cef3861da79415151a0b81192b20. The frozen proof is not altered.

## Claim boundaries

The theorem concerns n=3 or4 distinct singleton floor1 roots, a prescribed permutation target, and one globally fresh auxiliary w. Its 2m+2c count is a constructive schedule length. n=4 does not universally require w. It does not solve overlapping-support, arbitrary-floor or coupled-cycle repair. It has no physical interpretation.

## Gate disposition

Independent mathematical review: ACCEPTED.
Separate publication consistency review: ACCEPTED WITH REPORTING CLARIFICATIONS.
Reporting clarifications: published and immutable readback previously verified.
Remaining: publish final scoped closeout and read it back. No numerical campaign is claimed.
