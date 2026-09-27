# v15.71 Memory-enriched null / Jacobian integrability — COMPLETE

Completed 2026-09-26 America/Los_Angeles (2026-09-27 UTC).
Branch: `research/v15.71-memory-enriched-null`.

## Scientific verdicts

**MEMORY_ENRICHED_NULL_CONFIRMED**.

**FROZEN_FULL_JACOBIAN_OBSTRUCTED**.

The symmetric null can be realized by a single smooth state-dependent field on the regular positive-polar domain, with explicitly supplied source memory. It survives the frozen enriched restriction and recomputed-update composition checks. However, the entire historical reference-centered Jacobian cannot be preserved across base points: it has a nonzero integrability curl. A visible derivative term is necessary in the exhibited completion.

## The source law that was actually tested

For a fixed HS-unit full-support source label h,

    m_h(rho) = Tr(h rho),
    X_h(rho) = m_h(rho) Y(rho).

Y is the unchanged historical symmetric-null target lift, expressed in closed form and independently checked against the v15.64 least-squares implementation at all 36 visible bases.

The candidate contains no moving reference state. Each sequential update recomputes the field at its new state. It obeys

    DX_h[z] = Tr(hz)Y + m_h DY[z],
    DX_h[h] = Y.

The regional object is explicitly `(rho_e,m_h)`; for two sources it carries both memories. Regional Y is computed using the edge marginal's own connected correlations and polar factor. The source memory is extra global information, not inferred from the marginal. The law therefore does not reverse v15.70's marginal-only obstruction.

## Frozen coverage and measurements

- All 12 unchanged asymmetric states.
- Three visible bases per state: original and +/-1e-4 times XXI/sqrt(8).
- All 27 hidden source labels, with a second distinct cyclic label in each case.
- **972 source/state cases and 2,916 edge restriction comparisons**.
- All 27 visible weight-two directions per original state for the Jacobian-curl test.
- No amplitude, tolerance, selector or criterion changed after measurement.

| Diagnostic | Observed |
|---|---:|
| Maximum enriched restriction residual | 1.6900879266351857e-16 |
| Maximum endpoint overlap source residual | 0 |
| Maximum hidden derivative relative error | 1.6967986475455047e-12 |
| Maximum recomputed Y relative change | 9.404082902416718e-16 |
| Maximum source-memory change | 2.0816681711721685e-17 |
| Maximum finite rotation change | 2.1094237467877974e-15 |
| Maximum reversed-order residual | 9.583083854271089e-21 |
| Maximum sequential-versus-combined residual | 9.583083854271089e-21 |
| Maximum same-source additivity residual | 5.675133333246605e-17 |
| Closed-form/historical lift maximum relative error | 5.896782287845015e-16 |
| Maximum analytic DY/finite-difference verification error | 7.240808700250343e-8 |
| Maximum visible-completion derivative verification error | 7.240777257246537e-8 |
| Minimum density eigenvalue across probes | 0.03829829620495415 |
| Minimum edge singular value across probes | 0.020843099194109576 |

All validity and positive/null controls passed. Deleting the supplied memory leaves a regional vector-field discrepancy of approximately **5e-5** in every case. Thus the enriched comparison is not passing because the source is inactive on the tested hidden-shifted states.

## What the Jacobian obstruction means

The old full rank-one assignment is

    N_rho[z] = Y(rho) Tr(hz).

For weight-two v and fixed full-support h, its derivative curl is

    D_v N[h] - D_h N[v] = DY[v].

The measured curl map has **rank nine on all 12 states at all three frozen rank tolerances**. Its smallest ninth singular value across states is **2.7058329755734807**; the largest tenth singular value is **1.7202430965742502e-15**. This is a resolved obstruction, not a near-threshold rank decision. Curl column norms range from **0.18919275401138633** to **7.762799156799393**.

The new field supplies the missing visible derivative `m_h DY[v]`. The numerical probes verified this nonzero correction, whose norms range from **1.8919275401138634e-5** to **7.762799156799394e-4** at the frozen hidden amplitude.

The two verdicts are therefore consistent: the hidden-sector response is integrable into the displayed field; the complete old Jacobian, with all visible derivatives forced to zero, is not integrable unchanged. Rank nine here is the rank of the derivative-curl map. The 27 candidate source fields are pointwise collinear with Y and do not describe 27 independent flow directions.

## Earned conclusion and boundary

**Supplying explicit source memory and requiring one smooth state-dependent null field with locally composable updates still does not force rotational response.** The minimum-norm symmetric-null freedom survives those particular requirements.

This is a constructed mathematical counterexample, not a physically selected source law. It deliberately reuses the observable-dependent Y to test sufficiency. The memory's native/recoverability origin is not derived; frame covariance requires transforming h with the state. Density positivity and polar regularity are established only on the stated local domain and tested paths, not at arbitrary source strength. No tensor-product naturality, unique source law, gravity derivation or Einstein dynamics is claimed.

At hidden-free bases, the new field matches the historical construction along pure-hidden variations. At arbitrary bases with nonzero hidden memory it has additional drift; that difference is explicit, not a redefinition of the historical results. No earlier verdict was modified.

The next source-law question is operational admissibility and origin: can the required memory and coupling arise from specified retained/source data without engineering Y from the desired observable? Mixture consistency or an explicitly recorded conditioning mechanism may be useful discriminators, but neither has been imposed as a physical axiom or preregistered here.

## Exact provenance

| Stage | Commit | Actions run / job |
|---|---|---|
| Certified parent | `0d90d48da6c121ae2e808930a9c5d10198abe437` | v15.70 |
| Preregistration, derivation and RED tests | `385363f909e52501fec40cbc4c4940b0b7bd72e0` | [36293602246](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36293602246) / `108548213693` |
| Tested scientific implementation | `c519cec3156413f23b68a4012bb35b851590dcd7` | [36293792299](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36293792299) / `108548743483` |

RED was verified for the expected absent implementation after setup succeeded. GREEN completed **five tests** plus a separate full measurement; the scientific verdicts were read from the JSON/log, not inferred from job color. Independent read-only mathematical/code review found no material issue. No implementation correction or gate amendment was needed.

GREEN artifact: [10923755020](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36293792299/artifacts/10923755020).

Artifact SHA-256: `6ace0e6d951df1937340e4fd61891c8055ca609e52e82beb520f44d7ec6238c8`.

Original full result JSON SHA-256: `fdf5540984077a979cea2a4fde02332527583d66a218b0cf50f17e40baf9b12a`.

The artifact was downloaded; execution SHA, ZIP digest and every manifest hash were verified. `RESULT.json.gz` preserves that complete 1,849,250-byte JSON losslessly in GitHub. Its gzip SHA-256 is `07f9121cbe7c34c312d6848062c428e9d78f47163bbe6f0e052631167fa28e7a`. `SUMMARY.json` provides readable aggregate diagnostics; `TEST_LOG.txt` preserves the complete gate-test output; `EVIDENCE.json` records all file hashes and identifiers. The following documentation/evidence commit does not change executable code or criteria.

## Reproduce

Check out the tested implementation above. Use Python 3.11 and numpy 2.3.5:

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/memory-enriched-null
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > reproduced_result.json
```

On the documentation head, recover the archived original with `gzip -dc RESULT.json.gz > archived_result.json`. Read both verdict fields. These were dedicated research-gate tests, not a claim that unrelated repository test suites were run. Nothing was merged to main.
