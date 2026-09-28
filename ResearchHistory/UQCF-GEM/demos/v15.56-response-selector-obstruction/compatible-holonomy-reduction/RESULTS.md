# v15.95 — fixed compatible supports restrict continuous loop response

Both frozen scientific verdicts passed:

- **FIXED_SUPPORT_HOLONOMY_REDUCTION_CONFIRMED**
- **PLANAR_LOOP_RESPONSE_CONFIRMED**

`all_valid=true`: four tests, 13 exact checks, 36 state/source cases and 972 loop-direction derivative checks. No scientific implementation repair or preregistration change was required after the first scientific run.

## Earned statement

A matched rank-two support atlas carries a parallel normal line. Its completed based-loop transport preserves the base support plane, so its allowed rotations lie in an embedded O(2) subgroup of SO(3). The identity component is SO(2). With supports held fixed under perturbation, the skew loop tangent therefore has only one independent rotational direction.

The full O(2) stabilizer is **not abelian**: a normal flip conjugates a planar rotation to its inverse. Our exact and numerical normal-flip control is noncommuting. The one-dimensional bound concerns continuous tangents at fixed support, not every discrete group operation and not families whose support planes move.

This is a conditional restriction of the specified readout. Together with v15.93–94: rank-two data can retain a rotational signal; matched supports restore completion under composition; the same parallel-plane structure restricts continuous holonomy. It does not yield general three-axis holonomy while those assumptions remain in force.

## Frozen triangle results

| Source arm | Cases | Archived edge response rank | Loop response rank |
|---|---:|---:|---:|
| Coherent lambda=-1 | 12 | 2 | 1 |
| Incoherent lambda=0 | 12 | 0 | 0 |
| Coherent lambda=+1 | 12 | 2 | 1 |

All ranks agree at thresholds 1e-9, 1e-10 and 1e-11 with the frozen reference floor. Coherent loop-map norms range from 1.2650251922767564 to 2.085070110946453. The maximum incoherent norm is 1.7061321160224521e-19.

The independently assembled loop derivative agrees with the sum of the three archived planar edge-response blocks to 1.2747484502619122e-15. This rank-one aggregation was an algebraic prediction from the two independent active planar edge rows, not an independently discovered rank collapse. No global gauge structure is inferred empirically from a single triangle or from commuting powers of one loop.

All measured loops preserve the normal with sign +1 to about 1e-15. As a recorded diagnostic, their Frobenius distances from identity range from 0.11262022673137513 to 2.202280057731124. A one-axis restriction is not a zero-holonomy claim. The negative normal-sign sector is covered by the algebraic control, not asserted to occur in these physical rows.

## Independent checks

The production full product-rule function returns rank three and exactly I3 for the unrestricted x/y/z-generator positive control. Unit tests exercise those derivatives on each of the three edges. No projection onto the normal is built into the derivative; confinement is checked afterward.

The normal-flip control has squared commutator norm 5.120000000000002, matching exact 128/25 while preserving the plane. This prevents conflating the full O(2) stabilizer with its abelian continuous component.

Worst residuals:

- Full product rule versus body-tangent conjugation formula: 1.223406398996942e-15.
- Fixed-support axial/skew confinement: 1.627173020939757e-15.
- Independent local-frame covariance: 1.5365508518495276e-14.
- v15.94 archived triple completion agreement: 1.828605908730779e-15.
- Final finite-difference error: 1.7861292880138705e-8, below frozen 1e-6.

Recomputed edge R, W and E_map match their archived values exactly. Finite-difference worst errors over the three rungs are 4.787912849084037e-10, 1.6705432971416546e-9 and 1.7861292880138705e-8. The frozen test requires derivative agreement, not a monotonic convergence rate. The increasing small-step numerical error is not turned into an asymptotic scaling claim. Probes vary correlation matrices, not quantum states.

## Boundaries and next question

Physicality and source-channel validity are inherited from immutable parents; no new density operators or physical source updates were introduced. Covariance is a coordinate check on the full data. Fixed-support confinement does not apply unchanged when source perturbations move the supports. Such a future test must distinguish frame motion from changes in loop conjugacy data; extra coordinate response directions alone would not establish additional intrinsic geometry.

The atlas reduction is a mathematical implication of matched parallel-plane assumptions. The numerical experiment is a predicted aggregation check on the inherited one-triangle ensemble. It does not establish a global empirical gauge group, select a source law, restore erased quantum information, derive gravity, or invalidate prior full-rank results. All earlier scientific NOs remain unchanged. Genesis Pin and ordered recoverability remain foundational; no fundamental time, external alignment, fitted support or dark-matter primitive is introduced. No novelty claim is made for stabilizer or Lie-algebra mathematics.

## Immutable provenance

- Branch: `research/v15.95-compatible-holonomy-reduction`
- Certified parent: `22f93cd9483eacca8d09e89e8a1b4aa8aa47a77b`
- Preregistration/tests: `3fa73e0238ad0fd19c3aa743c8e1446cb6ca6fdb`
- Tested implementation: `baa8860653d0b00eb20f9ec60c3fcefcd3619534`
- [Expected RED run 36368093376](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36368093376), job `108758435903`, artifact `10947937693`. Setup passed and the explicit absent-implementation assertion failed as expected.
- RED ZIP SHA-256: `cd1619e2c310885ee6570b64af28fef767fcc82570e0c624d9120819089f8896`.
- [GREEN run 36368371453](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36368371453), job `108759246129`, artifact `10948471545`.
- GREEN ZIP SHA-256: `09fda636ef0de677f3eaf56689663e6f67d1f2405f05431fa09f9743fb6d204d`.
- Full result SHA-256: `ee9b13d07c3856357b157fdcf58854957fe56767ee55eeba61266b34ee40e607` (926,458 bytes).
- Lossless gzip SHA-256: `f05a0ebc7d41128d8b2be4fd46161d7827f623d6107da8b3dd2c4585cb95561f` (83,596 bytes).
- Gzip Git blob: `e6a09f4f0fa66e3f44b635f7e0550e7195c6347c`.

Exact job logs and downloaded RED/GREEN archives were inspected. Archive digests, execution heads, frozen source bytes, implementation and all artifact SHA256SUMS entries were verified. The scientific JSON in the GREEN log has the artifact's exact SHA-256 after timestamp/optional log-chunk BOM removal. RESULT.json.gz is lossless; SUMMARY.json is a derived view. SHA256SUMS retains the artifact filename `result.json`.

Reproduce from a full checkout using the pinned dependencies and commands in `.github/workflows/uqcf-compatible-holonomy-reduction.yml`. The documentation commit containing this file has the tested implementation as its sole parent; its own SHA is given by Git history and the completion report. Nothing merged to main.
