# 16.09 — Common order boundary limits

**Result: COMMON_ORDER_BOUNDARY_LIMIT_CERTIFIED.** All 144 normalized physical paths have certified one-sided canonical polar limits. All 72 before/after comparisons agree exactly. This establishes an order-independent boundary limit for the fixed source, not a source-independent extension of the baseline readout.

For C(s)=C+sV+s²W, let N=(I-CC⁺)V(I-C⁺C). Exact rank saturation certifies

`lim(s↓0) polar(C(s)) = polar(C) + polar(N)`.

The polar is the canonical partial isometry, zero on the kernel; no determinant correction is applied. In every pair the baseline is identical and N_before=a N_after with a>0, so their polar limits coincide. Identity-middle controls (a=1) also agree.

| Arm | Baseline rank r | New rank k | Paths |
|---|---:|---:|---:|
| Plane | 1 | 1 | 72 |
| Isotropic | 2 | 1 | 54 |
| Isotropic | 1 | 2 | 18 |

There are 144 exact records, 72 order comparisons, 576 limit evaluations (80/120 digits, two frames), and 1,440 finite-path evaluations. The 288 isotropic limit evaluations split into determinant +1 (168) and −1 (120); the 288 plane limits have determinant zero. Thus this is not an automatic proper-rotation readout.

The largest numerical order difference was 1.579e-80. Maximum cross-precision discrepancy was 1.529e-67, support residual 5.582e-68, and finite-frame covariance residual 5.207e-64. All frozen controls passed. Independent publication checks reconstructed every normal using column-basis projectors, without the audit pseudoinverse routine, and checked all 72 exact order identities.

Finite s matters: maximum error to the limit at s=2^-8, 2^-32, 2^-64, 2^-128, 2^-192 was respectively 2.2268, 2.0000, 0.0022620, 1.2271e-22, 6.6520e-42. The tiny inherited nonzero singular values produce a very small asymptotic neighborhood. No fit or finite-step convergence threshold was used.

## Provenance and complete evidence

- Scientific commit: `b8bfa7cd3abf99884b6627ab2a42d0fa035154be`.
- [Successful targeted run 36492791730](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36492791730), job 109165094308; 5 new and 6 parent tests passed.
- Preregistered RED commit: `ef3b558b678a0f5a8da0c6ca8adc8a5f54e587f2`; expected missing-implementation failures are preserved in `red-job.log`.
- `result.json.xz` is the **complete losslessly compressed raw result**, not a summary. Decode with `python -c "import lzma,pathlib; p=pathlib.Path('result.json.xz'); p.with_suffix('').write_bytes(lzma.decompress(p.read_bytes()))"`.
- `SHA256SUMS` verifies the decoded raw result and scientific inputs; `SHA256SUMS-xz` verifies the compressed archive. `EVIDENCE.json` records artifact digest, execution head, counts and metrics.
- `job.log`, `test.log`, `parent-test.log`, `audit.log`, `PUBLICATION_CHECK.json`, preregistration, derivation, review, source manifest, code and tests are included.

The question for 16.10 is whether the common limit survives reversal of coherence within the existing source family. Both paths will have the same baseline; a source-dependent limit would obstruct selecting a boundary value from that baseline alone. These are specified source models, not a derivation of a universal source law. The mixture strength is not fundamental time; no gravity or dark-matter claim follows.
