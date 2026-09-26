# v15.70 Strict marginal descent / fixed-base composition — COMPLETE

Date: 2026-09-26. Branch: `research/v15.70-atlas-descent-composition`.

## Scientific verdicts

**ATLAS_NATURAL_NULL_OBSTRUCTED** — the historical symmetric-null field does not descend to marginal state/source data alone.

**FIXED_BASE_NULL_COMPOSITION_CONFIRMED** — at one fixed base point, the affine null source updates commute and combine additively without producing rotational response on the frozen paths.

These are separate conclusions. The first is specifically strict marginal descent, not a no-go for every possible enriched atlas. The second is fixed-base composition, not a globally integrable physical source law.

## What was measured

All 12 unchanged asymmetric states; all 27 exact-weight-three hidden Pauli directions; three retained edges. This gives **972 marginal-descent witnesses** and **8,748 full-tangent-space operator-pair checks**.

For each fixed labeled source, the two global inputs rho +/- eta h have identical retained inputs but different retained outputs. No single-valued regional update depending only on those marginal inputs can reproduce both outputs.

| Diagnostic | Observed |
|---|---:|
| Retained derivative gap, every edge | 0.49999999999999983–0.5000000000000002 |
| Finite retained output gap | 9.999999997401252e-8–1.0000000004309342e-7 |
| Maximum retained input gap | 6.938893903907228e-18 |
| Maximum finite fiber-identity relative error | 1.0547693776843267e-9 |
| Maximum overlap restriction error | 8.610940881164415e-17 |
| Maximum polar-skew relative residual | 2.760038037983836e-16 |
| Maximum pairwise source-operator product norm | 2.5495124165822226e-17 |
| Maximum source commutator norm | 2.687422053093287e-17 |
| Finite reversed-order residual | 0 |
| Finite sequential-versus-combined residual | 0 |
| Maximum same-source additivity residual | 4.430350769486221e-17 |
| Maximum finite rotation change | 1.7406530350733312e-15 |
| Minimum finite density eigenvalue | 0.03831618449748307 |
| Minimum composed positive-polar eigenvalue | 0.020861026221258898 |

All frozen validity checks and positive/null controls passed. Full per-state and per-hidden/edge evidence is preserved in `RESULT.json`, copied byte-for-byte from the final Actions artifact. Its SHA-256 is `2e5d4a6d6030648fd7ca3d68e772313e3c54d2280d2742628fd01d4f7d0fef4b`.

## What was learned

Strict marginal naturality implies

    R DX[h] = D x[R h] = 0    when R h = 0.

It therefore excludes **all hidden-to-retained leakage**, including any rotationally visible leakage. This is not an axiom that selectively removes the symmetric null and forces a rotational signal. Its theoretical strength was derived before measurement in `DERIVATION.md`.

Overlap compatibility alone survives: the nonzero edge derivatives have zero common endpoint derivatives. Consistent output marginals and a source assignment computable from local input marginals are different requirements.

The composition result follows from the structure of the actual minimum-norm lift. Y occupies weight-two Pauli coefficients; all hidden h_a occupy weight three. Consequently

    N_a = |Y><h_a|,
    N_a N_b = 0,
    (I+s N_a)(I+u N_b) = I+s N_a+u N_b.

On the tested hidden-input paths the retained correlations stay O_e(P_e+c I/sqrt(3)); the positive factor remains positive. Thus fixed-base composition does not force an observable skew sector.

**Earned statement:** marginal-only naturality is too restrictive to discriminate a rotational source mechanism, while fixed-base additive composition still leaves the symmetric-null freedom intact.

## RED, GREEN, review and implementation-only correction

1. Preregistration, derivation, tests and workflow were published with `gate.py` absent. The exact RED log shows the expected missing-implementation assertion, with setup/dependency steps successful.
2. Initial implementation completed all five original tests and the scientific measurement. Both scientific verdicts above were obtained.
3. Independent code/mathematical review found one error-reporting issue: nonfinite diagnostics would fail strict JSON serialization instead of producing INVALID evidence. No issue was found in the finite-data scientific calculation or derivation.
4. A separate RED regression was published. The original five tests passed; the new test failed for the missing finalizer. A JSON-safe finalizer was then implemented. No states, amplitudes, tolerances, scientific logic or preregistration changed.
5. Final GREEN ran six tests successfully and repeated the complete measurement. **Initial and final result JSON files are byte-identical.** Both artifact ZIP hashes and all final manifest file hashes were checked after downloading the evidence. The reviewer verified the correction.

Historical v15.64–v15.69 verdicts remain untouched. These are dedicated gate tests, not a claim that every unrelated test in this multi-project repository was executed.

## Exact provenance

| Stage | Commit | Run / job |
|---|---|---|
| Certified parent | `5d079ca4bef6d51a38111f2312af87aa03e753c7` | v15.69 evidence independently checked |
| Frozen preregistration / RED | `d093f5008f701fc4d0cf76cbc735fa6252981194` | [36277749232](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36277749232) / `108503640126` |
| Initial scientific GREEN | `e27a3e330de54f7b6cf41b894d6fe1615bc54766` | [36277822967](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36277822967) / `108503848595` |
| INVALID-output regression RED | `58b57d1def405b680c6113ff29a9c325e8dad0f4` | [36277880145](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36277880145) / `108504006777` |
| Final tested implementation | `834f49aa8fee20c3e3eff7b28af80e73703e29cb` | [36277918302](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36277918302) / `108504116448` |

Final artifact: [10916664976](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36277918302/artifacts/10916664976).

Final artifact SHA-256: `e91c45af909d859d022c8198c9d303bdcbecf22113863a9c0581322503314687`.

Initial scientific artifact: `10917955682`; SHA-256 `2249d05509909dcac3f1c486326925f8fbb3e3ad2b104147af35e7c498c1c34a`.

Initial RED artifact: `10917741885`; SHA-256 `52d6ecdf8d7cd20177d252153bc12192e8fb8370d90fcba8341c40c5e7d84fb1`.

The documentation/evidence commit following the final tested implementation changes no scientific executable or criterion. `EVIDENCE.json` records the complete file-hash manifest and run identifiers; `TEST_LOG.txt` preserves the final test output.

## Reproduce

Check out the final tested implementation SHA above. With Python 3.11 and numpy 2.3.5:

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/atlas-descent-composition
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > reproduced_result.json
```

Read both verdict fields. A successful process can report an obstructed scientific gate.

## Boundaries and next question

This deliberately constructed null remains an existence counterexample using the retained observable; it is not a foundational explanation inserting that geometry into a physical source law. No gravity derivation, unique source selector, arbitrary-strength positivity, tensor-product composition, or base-point rebasing/integrability has been established.

The next useful question is whether an explicitly specified regional source-memory/extension object can retain the hidden source information needed for restriction consistency, and whether the corresponding differential assignment is integrable across base points. Merely demanding marginal-only descent would eliminate the desired signal as well. This is a next research direction, not a new preregistered gate or an earned physical axiom.
