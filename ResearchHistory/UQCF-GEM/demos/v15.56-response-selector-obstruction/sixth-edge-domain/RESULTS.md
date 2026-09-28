# v16.06 final report: sixth-edge domain audit

Completed 2026-09-28. **SIXTH_EDGE_OUTSIDE_FROZEN_DOMAIN. All validity controls passed.**

The omitted edge (2,3) cannot be inserted into the inherited full-link polar readout at these frozen baselines. All 288 frame configurations are rejected by its existing spectral domain. This is a valid domain-obstruction result, not a null geometric response: no out-of-domain loop response was computed.

## Evidence

[GitHub run 36485049321](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36485049321) completed successfully at scientific head `dd7a023ac95de9a984b791a0de736f7f30174824`. Four new tests and twelve parent tests passed. The earlier [RED run 36484851333](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36484851333) failed for precisely the four absent-implementation checks. Preregistration was committed at `e9ad01c913d78abbf2abcaa4286105796f97d104` before the audit.

All twelve frozen candidates were evaluated at archived binary a=1,1/3,1/6, both preparations, native and transformed frames, and 50/80 digits. There are 72 distinct baseline configurations, or 288 frame/precision cases. The full output is permanently published as [result.json.gz](result.json.gz), with [EVIDENCE.json](EVIDENCE.json), checksums, exact job logs, tests, pinned source manifest and [analytic derivation](DERIVATION.md).

## Findings

| Quantity | Result |
|---|---:|
| Plane domain admissions | 0 / 144 |
| Isotropic domain admissions | 0 / 144 |
| Exact plane baseline rank | 1 in all 36 state/attenuation cases |
| Exact isotropic baseline rank | 2 in 27 cases; 1 in 9 cases |
| Largest plane second singular value / source reference | 2.91613482324e-51 |
| Largest isotropic second singular value / source reference | 1.66041762949e-15 |
| Required second singular value / reference | greater than 1e-9 |
| Maximum native exact-to-archive discrepancy | 5.274e-54 |
| Maximum transformed exact-to-archive discrepancy | 7.003e-54 |
| Maximum cross-precision discrepancy | 6.864e-54 |

Domain decisions agree across frames and precisions. No exact rank-three isotropic baseline was found. Every plane case has zero exact 2x2 minors; isotropic rank-two cases retain their nonzero exact minors rather than rounding them away. All exact determinants vanish.

| Candidate | Preparation | Symbolic generic rank | Ranks at 1, binary 1/3, binary 1/6 |
|---|---|---:|---|
| 13 | plane | 1 | 1, 1, 1 |
| 13 | isotropic | 2 | 2, 2, 2 |
| 16 | plane | 1 | 1, 1, 1 |
| 16 | isotropic | 2 | 2, 2, 2 |
| 22 | plane | 1 | 1, 1, 1 |
| 22 | isotropic | 2 | 2, 2, 2 |
| 25 | plane | 1 | 1, 1, 1 |
| 25 | isotropic | 1 | 1, 1, 1 |
| 27 | plane | 1 | 1, 1, 1 |
| 27 | isotropic | 2 | 2, 2, 2 |
| 29 | plane | 1 | 1, 1, 1 |
| 29 | isotropic | 2 | 2, 2, 2 |
| 37 | plane | 1 | 1, 1, 1 |
| 37 | isotropic | 2 | 2, 2, 2 |
| 39 | plane | 1 | 1, 1, 1 |
| 39 | isotropic | 1 | 1, 1, 1 |
| 46 | plane | 1 | 1, 1, 1 |
| 46 | isotropic | 2 | 2, 2, 2 |
| 50 | plane | 1 | 1, 1, 1 |
| 50 | isotropic | 1 | 1, 1, 1 |
| 66 | plane | 1 | 1, 1, 1 |
| 66 | isotropic | 2 | 2, 2, 2 |
| 77 | plane | 1 | 1, 1, 1 |
| 77 | isotropic | 2 | 2, 2, 2 |

## Interpretation from first principles

The historical ideal state has no raw two-body moment on pair (2,3). Its connected matrix is the negative outer product of the two one-body Bloch vectors, so it has rank at most one. Product attenuation and the frozen local preparations preserve that bound. Archived binary residues can raise the exact isotropic rank to two, but their second singular values remain far below the frozen domain gate. They cannot supply a robust missing transport direction.

A rank-one polar partial isometry is unique on its one-dimensional support. A full proper orthogonal link still has an undetermined rotation on the orthogonal two-plane. Selecting such a completion would add alignment information that the retained matrix does not determine. The plane readout requires rank two, and the isotropic readout requires proper full rank; neither requirement is met.

Together with v16.05, this distinguishes three statements: D changes connected information on edge (2,3); the existing five-edge geometry does not receive that direction; and the omitted edge does not currently satisfy the conditions needed to join that geometry. The first statement does not imply the third is admissible.

This closes the direct sixth-edge insertion route for the frozen state/preparation/readout family. It does not rule out all observables based on support partial transports or prove a universal impossibility of emergent geometry. No state, source, threshold or loop was changed, and no external alignment, regularization or dark-matter primitive was introduced. Time remains pruning / ordered recoverability update. No gravity or universal source-law claim follows.

## Verification and reproduction

The downloaded artifact ZIP digest and all five execution SHA256 checks were verified. A separate publication audit recomputed exact ranks and determinants from the archived polynomial matrices, verified all 288 case identities, and recomputed numerical singular values, references and domain decisions at 100 digits. All checks passed. Its results are in EVIDENCE.json.

At the scientific execution head, install the workflow's pinned dependencies and run `python -m unittest -v`, then `python gate.py` in this directory. To inspect the permanent raw file, run `gzip -dk result.json.gz`; `sha256sum -c SHA256SUMS` then verifies the uncompressed result and four execution files. The compressed bytes have their own SHA256SUMS-gzip. DERIVATION.md and this report are publication documents added after the scientific run; they do not change its execution identity.

## Next question

Can canonical support partial transports provide a covariant, stable observable here, or does the D direction change rank and make that transport discontinuous? Audit the rank stratum and continuity before proposing any replacement readout. The present result supplies no license to choose a null-space rotation or introduce a new state solely to produce a signal.
