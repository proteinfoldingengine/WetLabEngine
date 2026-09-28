# v16.07 final report: support-stratum stability

Completed 2026-09-28. **SUPPORT_POLAR_DISCONTINUITY_FORCED. All validity controls passed.**

All 48 nonidentity D directions point outside the sixth-edge baseline's constant-rank manifold. Consequently, any differentiable matrix path with that derivative must gain rank near its baseline, and its canonical support polar partial isometry cannot approach the baseline transport continuously. This is an exact local obstruction, not a finite-step numerical inference.

**Scope:** D here is the prepared commutator contrast between ordered-channel derivatives. This audit does not establish that the contrast is itself an admissible physical path, or that either individual ordered-channel path has that derivative. The conclusion is conditional on a path whose own derivative equals D.

## Execution and publication

[Successful GitHub run 36486973238](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36486973238) executed scientific head `fc08e122cd6b1949ba71b2582500c0724bb3ff1c`. Five new tests and four parent tests passed. The new tests include a counterexample that prevents an affine-pencil rank increase from being mistaken for a forced rank increase along every path. The independent reviewer checked the proof and implementation and ran the new tests before the ensemble measurement.

Preregistration: `025343f057d56dd6f048e1ade9443548827a05d1`. [Expected RED run 36486688604](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36486688604) failed only the five absent-implementation checks. Full RED/GREEN logs are committed here.

The frozen ensemble contains 12 states, both preparations, and binary attenuation values 1,1/3,1/6: 72 exact cases. Numerical reconstruction and covariance were checked at 50/80 digits in both frames: 288 frame configurations. No new state, source, readout, alignment or threshold was introduced.

## What was established

For baseline C and D direction V, exact rational arithmetic constructs the support projectors P=C C+ and Q=C+ C, then the normal block

    N = (I-P) V (I-Q).

The exact Moore-Penrose inverse retains all binary residues. No numerical rank threshold is used to choose support. Let r=rank(C) and k=rank(N). For k>0, every differentiable matrix path with derivative V has rank at least r+k sufficiently near, but away from, the baseline. The canonical polar partial isometry, defined as zero on the kernel, then stays at Frobenius distance at least √k from its baseline value. See [DERIVATION.md](DERIVATION.md) for the Schur-complement and trace-inequality proof.

| Group | Cases | Baseline rank r | Normal rank k | Forced nearby rank | Minimum polar gap |
|---|---:|---:|---:|---:|---:|
| Plane, nonidentity | 24 | 1 | 1 | 2 | 1 |
| Isotropic, nonidentity | 18 | 2 | 1 | 3 | 1 |
| Isotropic, nonidentity | 6 | 1 | 2 | 3 | √2 |
| Identity-middle control | 24 | 1 or 2 | 0 | no forced increase | no forced gap |

Both nonidentity attenuation values give the following ranks in every candidate/preparation pair:

| Candidate | Preparation | r | k | Rank at least | Gap at least |
|---|---|---:|---:|---:|---:|
| 13 | plane | 1 | 1 | 2 | 1 |
| 13 | isotropic | 2 | 1 | 3 | 1 |
| 16 | plane | 1 | 1 | 2 | 1 |
| 16 | isotropic | 2 | 1 | 3 | 1 |
| 22 | plane | 1 | 1 | 2 | 1 |
| 22 | isotropic | 2 | 1 | 3 | 1 |
| 25 | plane | 1 | 1 | 2 | 1 |
| 25 | isotropic | 1 | 2 | 3 | √2 |
| 27 | plane | 1 | 1 | 2 | 1 |
| 27 | isotropic | 2 | 1 | 3 | 1 |
| 29 | plane | 1 | 1 | 2 | 1 |
| 29 | isotropic | 2 | 1 | 3 | 1 |
| 37 | plane | 1 | 1 | 2 | 1 |
| 37 | isotropic | 2 | 1 | 3 | 1 |
| 39 | plane | 1 | 1 | 2 | 1 |
| 39 | isotropic | 1 | 2 | 3 | √2 |
| 46 | plane | 1 | 1 | 2 | 1 |
| 46 | isotropic | 2 | 1 | 3 | 1 |
| 50 | plane | 1 | 1 | 2 | 1 |
| 50 | isotropic | 1 | 2 | 3 | √2 |
| 66 | plane | 1 | 1 | 2 | 1 |
| 66 | isotropic | 2 | 1 | 3 | 1 |
| 77 | plane | 1 | 1 | 2 | 1 |
| 77 | isotropic | 2 | 1 | 3 | 1 |

The normal-block Frobenius norms range from 1.2067e-5 to 8.3962e-4 in the plane preparation and 1.3299e-5 to 4.8347e-4 in the isotropic preparation. The obstruction is therefore not merely the assertion that an unreported tiny entry is nonzero. However, the asymptotic neighborhood can depend on the baseline's smallest supported singular value, including binary residues; no finite-scale robustness bound was measured.

## How this changes the interpretation

v16.05 localized D outside the five edges entering the existing readout. v16.06 showed that its omitted edge fails that readout's polar domain. v16.07 rules out a simple repair by substituting the canonical support partial transport and differentiating it along the same contrast direction: the transport is discontinuous under any differentiable matrix realization of that direction.

This closes that particular smooth support-polar derivative route. It does not invalidate the earlier five-edge results, rule out all scalar observables, or establish a general impossibility of retained geometry. A scalar observable may behave differently from the underlying partial transport and requires its own analysis.

The physical-path distinction matters: the difference of two source derivatives is not automatically either physical derivative. The next principled question is to audit the two inherited ordered-channel paths separately, using their own derivatives and physically defined channels, before assigning this discontinuity to an actual preparation sequence. No replacement source law is selected here.

Time remains pruning / ordered recoverability update. This result makes no gravity or universal source-law claim and introduces no dark-matter primitive.

## Controls and reproducibility

All exact pseudoinverse/projector identities and tangent-normal decompositions passed. Exact baseline matrices and ranks agree with v16.06. Reconstructed baseline and D matrices agree with v16.05 in both frames and precisions. Identity-middle V and N are exactly zero.

| Numerical control | Maximum absolute residual |
|---|---:|
| archive_C | 7.0032453774907874201746253333736806832337665254307e-54 |
| archive_V | 3.0687738631333935469894252439950490766777128410967e-52 |
| normal_covariance | 2.879710095191511713362518686068003253035536396906e-54 |
| projector_identity | 3.2434814681170888481785589888795383299749426388261e-51 |
| normal_identity | 2.1826608502925378704122849423925730908444664531525e-54 |
| precision | 2.5722311665924979165047488320605605306408631618041e-54 |

Within-precision gates are 1e-35; the cross-precision gate is 1e-30. All were satisfied. A separate publication audit rebuilt both support projectors from independent column-space bases, recomputed all 72 exact normal blocks/ranks/norms, and verified all 288 numerical case identities and normal-block identities at 100 digits. Artifact ZIP and execution-file hashes matched.

[Full raw result](result.json.gz) contains every exact C,V,C+,P,Q,N, tangent component, squared norm, rank, classification and all numerical matrices/controls. [EVIDENCE.json](EVIDENCE.json) records run identity, artifact and raw digests, counts and residuals. SHA256SUMS binds the uncompressed result to the exact four execution files; SHA256SUMS-gzip covers the permanent compressed bytes.

To inspect: `gzip -dk result.json.gz`, then `sha256sum -c SHA256SUMS`. To reproduce the scientific run, use the pinned workflow dependencies and execute `python -m unittest -v` and `python gate.py` at the scientific head in this directory. The report and publication logs were added afterward without changing the scientific execution files.
