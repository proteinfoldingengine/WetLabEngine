# v16.08 final report: physical ordered-channel paths

Completed 2026-09-28. **PHYSICAL_PATH_SUPPORT_DISCONTINUITY_FORCED. All validity controls passed.**

Both specified physical channel paths have discontinuous canonical support-polar transport at their common baseline. The rank-stratum obstruction is nonzero in all **96 normalized nonidentity path cases**, and also in all **48 normalized identity-middle cases**. Thus the physical-path qualification left open by v16.07 is resolved for these explicitly defined paths.

The identity-middle result is essential: when the two orders are identical, both still have the obstruction. This is a singularity of the support-polar extraction under source activation, not a distinctive ordering signal or a gravity result.

## Exact physical paths

The frozen source is L_D=Ad_U−I, with Hermitian unitary U=(Z⊗I+X⊗X)/√2 on pair (2,3). For mixture strength 0≤s≤1, E_s=(1−s)I+s Ad_U is CPTP. The paths are

    rho_after(s)  = Q E_s M_a rho_hat,
    rho_before(s) = Q M_a E_s rho_hat.

Their common baseline is Q M_a rho_hat. Their individual derivatives were measured separately. Their difference reproduces the inherited commutator contrast on the RAW benchmark. The parameter s is a channel mixture strength, not fundamental time.

Exact positivity of every input and exact nonnegative normalized channel weights prove the NORMALIZED paths are physical throughout [0,1]. No finite-step extrapolation was used to establish physicality. Their connected matrices are quadratic in s because of the one-body product subtraction; those full exact polynomials are archived and their linear terms agree with the independently computed connected derivatives.

## Explicit input convention

The archived binary matrices have small exact trace defects. They were preserved unchanged as RAW algebraic controls. Physical paths use the separately identified rho_hat=rho/Tr(rho), a unique parameter-free normalization. All normalized moments, connected matrices, projectors and ranks were recomputed from scratch. No state was spectrally clipped, fitted, replaced or selected based on its result.

| Candidate | Exact RAW trace minus one | Exact LDL pivots |
|---|---|---|
| 13 | -15/144115188075855872 | positive |
| 16 | -5/144115188075855872 | positive |
| 22 | -3/144115188075855872 | positive |
| 25 | 3/36028797018963968 | positive |
| 27 | 3/144115188075855872 | positive |
| 29 | -9/144115188075855872 | positive |
| 37 | -11/144115188075855872 | positive |
| 39 | 3/72057594037927936 | positive |
| 46 | 7/72057594037927936 | positive |
| 50 | 1/72057594037927936 | positive |
| 66 | -9/144115188075855872 | positive |
| 77 | -9/144115188075855872 | positive |

All normalized traces are exactly one, and all inputs are exactly positive definite. Independent publication verification additionally proved positivity through their real 32×32 matrix representations. RAW paths retain their nonunit traces and are not labeled density-state paths. Their rank/normal-rank outcomes match the normalized counterparts in every paired case, but this agreement was checked rather than assumed. Historical outputs remain unchanged.

## Results

The exact normal block is N=(I−P)V(I−Q_r), where P and Q_r project onto C's column and row support. With r=rank(C), k=rank(N)>0, the actual physical path has rank at least r+k for all sufficiently small positive s. The canonical polar partial isometry remains at Frobenius distance at least √k from its baseline value; see [DERIVATION.md](DERIVATION.md).

| Normalized cases, both orders combined | Cases | Baseline rank r | Normal rank k | Nearby rank at least | Polar gap at least |
|---|---:|---:|---:|---:|---:|
| Nonidentity, plane | 48 | 1 | 1 | 2 | 1 |
| Nonidentity, isotropic | 36 | 2 | 1 | 3 | 1 |
| Nonidentity, isotropic | 12 | 1 | 2 | 3 | √2 |
| Identity middle, plane | 24 | 1 | 1 | 2 | 1 |
| Identity middle, isotropic | 18 | 2 | 1 | 3 | 1 |
| Identity middle, isotropic | 6 | 1 | 2 | 3 | √2 |

Each order has half the cases in every row. At a=1 the complete path polynomials agree exactly between orders, while their individual derivatives need not vanish. Only the order contrast vanishes. The same table of outcomes holds for the separately retained RAW controls.

For normalized nonidentity cases, normal-block Frobenius norms span:

| Preparation | Source after middle | Source before middle |
|---|---:|---:|
| Plane | 1.4481e-5 to 1.2594e-3 | 2.4135e-6 to 4.1981e-4 |
| Isotropic | 1.5959e-5 to 7.2521e-4 | 2.6599e-6 to 2.4174e-4 |

These are exact nonzero obstructions with high-precision magnitudes, not threshold-selected ranks. No finite-scale lower bound on the asymptotic neighborhood is claimed, and the tiny stored residues supporting some rank-two isotropic baselines remain explicit.

## Execution, implementation failure and correction

Preregistration was committed at `575cb5d0b9a4fed16b2cc10c737a267f3f571ee7`. [RED run 36488890335](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36488890335) failed the five expected absent-implementation tests.

The first implementation, `bcbe869c385940a0dcbf029cb58a1c94f9123548`, produced **INVALID** in [run 36489262513](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36489262513), before any candidate path measurements. SymPy's built-in complex LDL routine rejected a positive-definite leading 4×4 input block. The saved regression fixture has exact Gershgorin lower bound 404653638933731403/9223372036854775808 > 0; its positivity does not depend on numerical eigenvalues. The routine leaves compound complex products unsimplified before its sign predicate.

The correction implements the standard Hermitian LDL recurrence with exact expansion of every intermediate and requires strictly positive rational pivots plus exact reconstruction. It changes no input, tolerance or physical criterion. The regression failed before the correction and passed afterward. The independent reviewer reproduced the old rejection and approved the fix. The initial INVALID result, original checksums and complete logs are preserved as `failed-*` with [FAILED_ATTEMPT.json](FAILED_ATTEMPT.json); it is not relabeled successful.

[Successful run 36489802902](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36489802902) executed head `8739e9db7ce1cb2c4ae0a91600e20fb4a2e953f5`. All six new tests and five parent tests passed. All 12 candidates completed. The exact audit includes 144 baselines and 288 individual path records; 50/80 digits and both frames give 1,152 numerical path records.

## Verification and complete evidence

All exact density/channel certificates, parent contrast identities, path polynomial identities and rank-stratum identities passed. Independent global transfer calculations agree with the exact C/V/normal matrices in native and transformed frames.

| Numerical control | Maximum absolute residual |
|---|---:|
| global_C | 3.7499457751717092007817754235564051456235876202839e-54 |
| global_V | 3.5767895598832886287446173868723758438660627515901e-52 |
| normal | 2.9778782204651585439880945607676126985940895477602e-52 |
| covariance | 2.9739316151189421982736436640690104578285842269769e-52 |
| projector | 3.2434814681170888481785589888795383299749426388261e-51 |
| precision | 3.5976314589972369854566199277331875705858914610599e-52 |

Within-precision limits are 1e-35; cross-precision limit is 1e-30. Separate publication verification reconstructed support projectors through independent column-space bases, checked all 288 exact records and 1,152 numerical records, rechecked each path polynomial from its input, and independently proved state positivity using real-matrix LDL. Both the failed and successful artifact digests and execution-file hashes were verified.

[Full raw result](result.json.xz) contains every exact density pivot, channel certificate, path polynomial, C,V,C+,support projector, normal block, rank and all numerical matrices/controls. [EVIDENCE.json](EVIDENCE.json) records run/artifact identities, hashes and complete count summaries. Compression is lossless; the uncompressed result is 6,020,044 bytes.

For inspection, run `xz -dk result.json.xz`, then `sha256sum -c SHA256SUMS`. SHA256SUMS-xz covers the compressed bytes. Reproduce the measurement at its scientific head using the workflow's pinned dependencies, then `python -m unittest -v` and `python gate.py` in this directory. The new physical-path tests and inherited tests are targeted research controls, with no unrelated workflows.

## Interpretation and next question

The stored quantum states are positive, and the normalized paths remain valid density states. The discontinuity occurs in the extracted support-polar transport, not in the physical state itself. It prevents differentiating that baseline canonical partial transport along either of these paths. It does not prohibit every smooth scalar observable or prove that every notion of geometry fails.

A sharper next question is whether the two physical paths select the same covariant one-sided polar limit as s approaches zero, or incompatible limits. Such a limit would differ from the baseline zero-on-kernel partial isometry; its existence and agreement must be proved before treating it as intrinsic boundary geometry. No such extension is introduced in this run.

The source law remains the frozen specified model, not a law derived from retained consistency. Time is pruning / ordered recoverability update. No external alignment, dark-matter primitive or gravity claim is introduced.
