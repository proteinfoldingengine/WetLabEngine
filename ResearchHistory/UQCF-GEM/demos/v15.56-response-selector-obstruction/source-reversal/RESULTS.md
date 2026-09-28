# 16.10 — Source reversal selects different boundary limits

**SOURCE_DEPENDENT_BOUNDARY_LIMIT_CERTIFIED.** All 144 paired physical paths share their baseline and have certified unequal boundary limits under reversal of the source coherence. This supplies a concrete obstruction to a continuous baseline-only extension of the canonical polar readout.

The two sources are U±=(ZI±XX)/sqrt(2), acting on sites (2,3). Their channels E±,s=(1−s)I+s Ad(U±) are CPTP for 0≤s≤1. Exact unitary and direct 32-column Pauli conjugation checks passed. Every input uses the explicit positive, trace-one normalization introduced in 16.08. The source strength, middle channel, preparation, input and baseline are held fixed while the coherence sign is reversed.

For every case, N−=−N+≠0 exactly. Both physical path ranks saturate at r+k, so the 16.09 theorem gives B±=polar(C)±polar(N+). Thus the squared Frobenius distance is exactly 4k.

| Arm | Baseline rank | New normal rank k | Paired paths | Limit gap |
|---|---:|---:|---:|---:|
| Plane | 1 | 1 | 72 | 2 |
| Isotropic | 2 | 1 | 54 | 2 |
| Isotropic | 1 | 2 | 18 | 2√2 |

These counts include both orders and all three middle-channel parameters, including the identity. The obstruction therefore survives when there is no ordering contrast. It is source-choice dependence of this boundary readout, not an ordering-specific gravity signal.

All 144 exact paired records, 576 paired limit evaluations (80/120 digits and two frames), and 1,728 finite-polar evaluations are archived. Maximum squared-gap residual was 8.434e-80, cross-precision discrepancy 1.529e-67, limit partial-isometry residual 2.443e-67, and finite-frame covariance residual 5.207e-64. All frozen controls passed. Independent publication verification reconstructed the 288 normal blocks with column-basis projectors and checked all 144 exact nonzero reversals and gap predictions.

The finite-grid maximum errors at s=2^-32, 2^-128 and 2^-192 were 2.0000, 1.9494e-22 and 1.0568e-41. The early grid point is not treated as asymptotic evidence; exact rank saturation is the proof. Tiny inherited singular values remain explicit. No fitting, threshold rank, determinant correction or arbitrary null-space choice was introduced.

## Complete publication and provenance

- Scientific commit: `1e9a5e8029e53b09998f99b122a9df3324178b1b`.
- [Successful targeted run 36493793738](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36493793738), job 109168486420: 4 new tests and 5 parent tests passed.
- Preregistered RED commit `7d4c116694571fc1d501d4609d60b4bb06f594ae`, [run 36493546753](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36493546753): four expected absent-implementation failures, preserved in `red-job.log`.
- `result.json.xz` contains the **entire losslessly compressed raw result**, including exact C/V/W/N matrices for both sources, ranks and certificates, all numerical limits and all finite polar matrices. Decode with `xz -dk result.json.xz` and check `sha256sum -c SHA256SUMS`.
- `SHA256SUMS-xz`, `EVIDENCE.json`, `PUBLICATION_CHECK.json`, complete job/test/audit logs, source manifest, preregistration, derivation, review, code and tests accompany the report.

16.09 showed equal limits for two orderings of one specified source. 16.10 shows that this agreement does not remove source-choice dependence. A source label could distinguish approaches, but selecting that source intrinsically is a separate unresolved problem. No universal source law, physical clock, dark-matter primitive or gravity correspondence is claimed. Time remains pruning / ordered recoverability update.

Next: 16.11 will test the full already-defined coherence interval and separately certify the zero-coherence path, rather than inferring its behavior from a vanishing first derivative.
