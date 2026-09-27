# v15.72 Operational mixture affinity — COMPLETE

Completed 2026-09-26 America/Los_Angeles (2026-09-27 UTC).
Branch: `research/v15.72-operational-mixture-affinity`.

## Scientific verdicts

**UNCONDITIONED_MIXTURE_AFFINITY_OBSTRUCTED**.

**PREPARATION_DEPENDENT_SKEW_CONFIRMED**.

The v15.71 null law fails mixture affinity in every one of the 972 frozen cases. Therefore it cannot coincide with a fixed unconditioned CPTP map on the tested states. The discrepancy between updating preparations separately and updating their pooled density matrix also spans all nine retained skew coordinates at every equal-mixture base, even though individual source paths preserve their rotations.

This skew is **preparation dependence**, not an earned physical source/gravity signal. The earlier smooth-field and memory-enriched null existence results remain valid in their stated mathematical scope.

## Frozen experiment

For a fixed h=XXX/sqrt(8), all 12 unchanged asymmetric states, all 27 unit weight-two Pauli v and weights p=.25,.5,.75:

    a = rho+eta h+delta v
    b = rho-eta h-delta v
    r = p a+(1-p)b
    J = p X_h(a)+(1-p)X_h(b)-X_h(r)

eta=delta=1e-4 and source strength s=1e-3 were frozen. J was computed from vector fields directly. The independent finite-state comparison verified

    p T_s(a)+(1-p)T_s(b)-T_s(r) = s J.

All source labels, state identities, amplitudes, weights and criteria remained unchanged after preregistration.

## Measurements

| Diagnostic | Observed |
|---|---:|
| Cases with affinity obstruction | 972 / 972 |
| Raw field-defect norm | 1.4182539036389474e-9–7.762772260809788e-8 |
| Analytically normalized field defect | 0.18910052048519296–7.764246557005518 |
| Frozen normalized affinity threshold | 1e-6 |
| Finite updated-state gap norm | 1.4182497551188711e-12–7.762772146085006e-11 |
| Maximum finite identity residual | 6.571538971869223e-17 |
| Maximum scalar-memory affinity error | 1.3552527156068805e-20 |
| Maximum unitary-control mixture defect | 8.503865706933559e-17 |
| Maximum hidden-only control defect | 1.1263132397950955e-20 |
| Maximum visible-only control defect | 0 |
| Maximum nonlinear-toy relative error | 4.679240163218305e-16 |
| Maximum individual-branch rotation change | 2.116169252845623e-15 |
| Maximum midpoint analytic tangent verification error | 7.240510960447075e-6 |
| Minimum density eigenvalue across probes | 0.03831477281773149 |
| Minimum edge singular value across probes | 0.02068144692891302 |

All validity checks and controls passed. The scalar memory itself is affine; the product of that memory with state-dependent Y is the obstruction. The finite-state discrepancy is resolved well above the independent identity-check residual and is not diagnosed as float64 cancellation noise.

## Retained skew result

At p=.5 the pooled input is the same rho for all 27 visible directions. All twelve resulting 9-by-27 skew-discrepancy matrices had **rank [9,9,9]** across the three frozen relative thresholds. The smallest ninth singular value across these matrices was **15.306497266555692**.

The unequal-weight matrices also had rank nine, but their pooled states vary with v. Those are descriptive finite-probe ranks; only the equal-weight matrices entered the preregistered secondary verdict.

The reported map is the **pre-Sylvester skew projection**. Its rank agrees with the polar rotational derivative rank on the regular stratum, but its norms are not rotational-derivative norms without the Sylvester conversion.

At equal weights,

    J = (eta/2)[Y(rho+delta v)-Y(rho-delta v)]
      = eta delta DY[v] + O(eta delta^3).

Thus the same visible dependence of Y that appeared in v15.71's Jacobian obstruction now produces a preparation-dependent retained skew discrepancy. A null response along each individual path does not guarantee invariance under forgetting preparation labels and pooling the resulting states.

## Earned conclusion

Covariance, local positivity, smooth state dependence, memory-enriched restriction and local composition were insufficient to make this engineered null law an ordinary unconditioned quantum operation. Mixture affinity exposes the missing operational specification.

A recorded selective operation can be nonlinear after normalization; preparation-dependent feedback also has additional inputs. This experiment does not exclude all such mechanisms. It requires that any proposed realization specify its records, success weights and update rule. It does not supply them, establish native source memory, or select a physical coupling.

The failure belongs to the unconditioned-channel interpretation of this particular candidate, not to every possible null source or the whole UQCF-GEM program. No earlier verdict is rewritten. No gravity, Einstein dynamics or source-induced deformation of admissible worlds is established.

The next useful task is to examine an explicitly specified quantum operation/source mechanism and keep its operational assumptions visible. A conditioned mechanism would need its record semantics; an unconditioned mechanism would need affinity and complete positivity. These are possible next tests, not gates silently added to the present result.

## Exact provenance and verification

| Stage | Commit | Actions run / job |
|---|---|---|
| Certified parent | `068abcc33ea69b9f1f3d8beaff55194b969ff710` | v15.71 |
| Preregistration / RED tests | `63d2e543712e8bb5025a5f799024ab48076c41e9` | [36294357684](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36294357684) / `108550329866` |
| Tested implementation / GREEN | `85f87d102c34348e5a62c9c76ae9110ffa37b679` | [36294454256](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36294454256) / `108550601484` |

RED was verified for the expected missing implementation. GREEN ran **four tests** and a separate full measurement. Exact job logs and scientific JSON were inspected. Independent read-only mathematical/code review found no material issue. No gate amendment or implementation correction was needed.

GREEN artifact: [10923382787](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36294454256/artifacts/10923382787).

Artifact SHA-256: `0591519a7bd93465e0f005c98482e8ec865fb91ca3d68a2b46b31e5c7338839c`.

Full JSON SHA-256: `5cde9efa51b1fa2f045f7be597c9b59a055357f66ea3d6b5a127fbc9ed431123`.

The ZIP was downloaded and its digest, execution SHA and all manifest hashes verified. `RESULT.json.gz` losslessly preserves the complete 1,480,380-byte result JSON; gzip SHA-256 `ce478f338f4c54f67a28867600e7669fb9d96b18c94cdf63a5795a4b13f226f1`. `SUMMARY.json`, `TEST_LOG.txt` and `EVIDENCE.json` preserve aggregate diagnostics, exact test output and full provenance. The subsequent documentation/evidence commit changes no scientific code or criterion.

## Reproduce

Check out the tested implementation above. With Python3.11 and numpy2.3.5:

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/operational-mixture-affinity
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > reproduced_result.json
```

Recover the archived original on the documentation head with `gzip -dc RESULT.json.gz > archived_result.json`. Read both verdict fields: successful CI here accompanies a scientific obstruction. Verification was scoped to the dedicated research gate, not unrelated repository projects. Nothing was merged to main.
