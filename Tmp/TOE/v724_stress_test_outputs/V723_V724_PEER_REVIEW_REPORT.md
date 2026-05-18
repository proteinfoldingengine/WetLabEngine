# V723 → V724 Peer-Review Report  
## Passive-Equivalent Recoverability and Stress-Tested Restoration Deficit in a Controlled Synthetic Retained-Atlas Assay

**Prepared for peer review**  
**Scope:** Controlled synthetic retained-atlas experiments  
**Posture:** Observation-only reporting. No universal physics, biological, engineering, or real-world generalization claim is made here.  
**Core question:** Does active post-perturbation restoration behavior reveal recoverability information that passive burden observables do not contain?

---

## 1. Executive Summary

This report summarizes two sequential retained-atlas assay runs:

- **V723 — Passive-Equivalent Recoverability Audit**
- **V724 — Stress-Test Recoverability Audit**

The purpose of V723 was to close the specificity objection exposed by V722.

V722 showed that changing restoration capacity `k` strongly changed the whole system. However, all measured observables separated, including passive burden metrics. That meant V722 confirmed causal `k`-separation, but did **not** isolate a restoration-specific observable.

V723 corrected this by enforcing passive-equivalent counterfactual pairs:

- same pre-probe state,
- same perturbation,
- same perturbation amplitude,
- same relaxation noise,
- same target field,
- passive burden held equivalent,
- only restorative capacity `k` changed.

V723 result:

```text
adm_z AUC:            1.000
passive_mean AUC:     0.500
passive_peak AUC:     0.500
probe_start AUC:      0.500
curvature-like AUC:   0.500
defect-weighted AUC:  0.500
paired Δadm_z:        ~124.53
paired passive delta: 0.0
```

V724 then stress-tested the V723 result by adding harder, more realistic conditions:

- overlapping `k` distributions,
- nonlinear restoration saturation,
- reserve fatigue,
- stochastic stalls,
- perturbation-family variation,
- shortened / aliased observation windows.

V724 result:

```text
adm_z AUC:            ~0.845
passive_mean AUC:     ~0.500
passive_peak AUC:     ~0.500
probe_start AUC:      ~0.500
curvature-like AUC:   ~0.500
defect-weighted AUC:  ~0.500
paired Δadm_z:        ~1.209
95% CI:               [~0.943, ~1.462]
paired passive delta: 0.0
```

### Observation

In these controlled synthetic assays, active post-perturbation restoration deficit retained discriminatory signal while passive burden observables remained at chance.

### Narrow claim supported by V723 → V724

> In this controlled synthetic retained-atlas assay, active post-perturbation restoration deficit reveals hidden restorative capacity under passive-equivalent conditions, and the signal persists under harder stress conditions.

### Claims not made

This report does **not** claim:

- a universal law of nature,
- proof of physical field behavior,
- proof of real-world generalization,
- a biological or engineering theorem,
- that `adm_z` is sufficient in all systems.

The observations speak only for the controlled synthetic assays described here.

---

## 2. Background and Scientific Motivation

The retained-atlas work developed iteratively. Earlier runs observed that passive state quality alone was insufficient to describe whether a system could recover from disturbance.

The recurring observation was:

> Two systems can appear similarly burdened yet differ in their capacity to convert perturbation into restoration.

This led to the operational measurement question:

> Can recoverability be measured as an active response property rather than a passive state property?

The current assay stack investigates that question using a synthetic retained-atlas field model.

---

## 3. Core Model

The model evolves a synthetic field:

```text
Omega(x, y, t)
```

around a target field:

```text
Omega_target(x, y)
```

The target field represents the admissible or restored configuration in the synthetic assay.

The system contains internally generated spatial structures:

- retained load / stress field,
- margin-like field,
- lineage-like field,
- repair-like field,
- capacity floor,
- defect-weighted leakage,
- curvature-like second-variation diagnostic.

These quantities are not asserted to be physical spacetime quantities. They are operational synthetic field variables used to test recoverability under controlled perturbation-response dynamics.

---

## 4. Restoration Capacity Parameter `k`

The variable `k` controls restoration capacity.

Higher `k` means stronger restorative flow toward the target field after perturbation.

Lower `k` means weaker restorative flow.

The central experimental design requirement is:

> `k` should affect restorative capacity without allowing passive burden differences to explain the classification result.

This requirement was not fully satisfied in V722 because passive metrics also separated. V723 was designed to correct that.

---

## 5. Frozen Observable: `adm_z`

The primary restoration-deficit observable is:

```text
adm_z = (restoration_measure - admissible_mean) / admissible_std
```

where:

```text
restoration_measure = mean post-perturbation distance to target
admissible_mean     = mean restoration_measure from admissible calibration runs
admissible_std      = standard deviation from admissible calibration runs
```

Interpretation:

- `adm_z ≈ 0`: post-perturbation restoration resembles admissible baseline.
- larger positive `adm_z`: post-perturbation restoration remains farther from admissible baseline.

The observable is calibrated using admissible-only runs.

---

## 6. Passive Burden Observables

To test specificity, the following passive or quasi-passive metrics are compared against `adm_z`:

```text
passive_mean_distance
passive_peak_distance
probe_start_mean
curvature_like_z
defect_weighted_z
```

The specificity requirement is:

> If passive burden explains the result, passive metrics should classify as well as `adm_z`.

The desired V723/V724 result is:

```text
adm_z AUC meaningfully above chance
passive metric AUC near chance
```

---

## 7. V722 Problem That Motivated V723

V722 produced strong separation, but all observables separated:

```text
adm_z AUC = 1.0
passive metrics AUC = 1.0
```

This meant the system was too easy. Changing `k` changed the entire trajectory geometry.

V722 supported:

> changing restoration capacity changes the system.

V722 did not support:

> `adm_z` isolates restoration-specific recoverability beyond passive burden.

This motivated V723.

---

## 8. V723 Design: Passive-Equivalent Counterfactual Audit

V723 was designed to hold passive burden equivalent while varying restoration capacity.

### Design principle

For each paired counterfactual:

```text
same initial state
same passive field evolution before probe
same perturbation
same perturbation amplitude
same relaxation noise
same target field
different restoration capacity k
```

The goal was to make passive burden unable to classify the conditions.

### Pass condition

```text
passive AUC ≈ 0.50–0.65
adm_z AUC meaningfully higher
paired Δadm_z > 0
k-gap collapses toward null when k_high ≈ k_low
```

---

## 9. V723 Results

### Summary metrics

```text
n_calibration_pairs: 24
n_test_pairs:        36
test samples:        72
high_k:              1.0
low_k:               0.35
k_gap:               0.65
```

### Classification metrics

```text
adm_z AUC:            1.000
adm_z_l2 AUC:         1.000
passive_mean AUC:     0.500
passive_peak AUC:     0.500
probe_start AUC:      0.500
curvature-like AUC:   0.500
defect-weighted AUC:  0.500
```

### Passive-equivalence metrics

```text
delta_passive_mean_distance_mean_abs:        0.0
delta_passive_mean_distance_max_abs:         0.0
delta_passive_peak_distance_mean_abs:        0.0
delta_probe_start_mean_mean_abs:             0.0
delta_curvature_like_energy_mean_abs:        0.0
delta_defect_weighted_error_mean_abs:        0.0
```

### Paired restoration effect

```text
paired_delta_adm_z_mean:       ~124.53
95% CI low:                    ~123.99
95% CI high:                   ~125.12
paired_delta_passive_mean:     0.0
```

### V723 observation

The passive observables were neutralized while active restoration still separated.

V723 therefore closed the synthetic specificity objection that remained after V722.

---

## 10. V723 Visual Diagnostics

### `adm_z_distribution.png`

The admissible/high-k distribution clustered near:

```text
adm_z ≈ 0
```

The low-k distribution clustered near:

```text
adm_z ≈ 120–130
```

with essentially no overlap.

### `roc_specificity_comparison.png`

The ROC comparison showed:

```text
adm_z AUC ≈ 1.0
passive AUC ≈ 0.5
```

This is the clearest visual evidence that passive observables were neutralized while active restoration remained discriminative.

### `paired_delta_adm_z_vs_passive.png`

The paired counterfactual delta plot showed:

```text
Δpassive_mean ≈ 0
Δadm_z >> 0
```

for every pair.

This directly visualizes the specificity result.

### `k_gap_ablation.png`

The k-gap ablation showed collapse toward null when `k_gap` approaches zero and increasing separability as the gap increases.

This supports the interpretation that the signal depends on restoration capacity difference rather than label leakage.

---

## 11. Why V724 Was Needed

V723 was intentionally clean.

However, V723 was also idealized. Perfect separation can indicate:

1. a genuine strong effect,
2. an overly easy synthetic setup,
3. remaining shortcut structure,
4. insufficient realism.

V724 was created to test whether the V723 observation survives when the synthetic assay is made harder.

---

## 12. V724 Design: Stress-Test Recoverability Audit

V724 retained the observation-only posture and added the following stressors:

```text
overlapping_k
nonlinear_saturation
reserve_fatigue
stochastic_stalls
perturbation_families
short_window_sweep
```

### Overlapping capacity

Instead of widely separated fixed values, V724 sampled overlapping high/low nominal capacity distributions.

Reported test ranges:

```text
mean_high_k_nominal_test: 0.8410
mean_low_k_nominal_test:  0.6718
min_high_k_nominal_test:  0.6471
max_low_k_nominal_test:   0.8564
```

This means some low-k samples had nominal capacity greater than some high-k samples.

### Nonlinear saturation

Restoration was not treated as a perfectly linear unlimited correction process.

### Reserve fatigue

Repeated restoration demand could reduce effective recovery.

### Stochastic stalls

Some recovery trajectories experienced partial stalls.

### Perturbation families

The assay was made less dependent on one probe geometry.

### Shortened / aliased observation windows

The observation process was made less ideal.

---

## 13. V724 Results

### Summary metrics

```text
test_n:          96
test_positive:   48
test_negative:   48
```

### Classification metrics

```text
test_auc_adm_z:             0.845052
test_auc_adm_z_l2:          0.846788
test_auc_passive_mean_z:    0.500000
test_auc_passive_peak_z:    0.500000
test_auc_probe_start_z:     0.500000
test_auc_curvature_like_z:  0.500000
test_auc_defect_weighted_z: 0.500000
```

### Bootstrap confidence intervals

```text
auc_adm_z_ci95_low:          0.767741
auc_adm_z_ci95_high:         0.906548
auc_passive_mean_z_ci95_low: 0.389916
auc_passive_mean_z_ci95_high:0.609375
```

### Paired restoration effect

```text
paired_delta_adm_z_mean:      1.208891
95% CI low:                   0.943060
95% CI high:                  1.461997
paired passive delta mean:    0.0
paired passive delta max abs: 0.0
```

### Specificity gap

```text
specificity_gap_auc_adm_minus_passive_mean: 0.345052
```

### V724 observation

Under stress, `adm_z` degraded from perfect to partial-but-strong discrimination, while passive burden observables remained at chance.

This is the expected direction if V723 captured a real synthetic response signal rather than an artifact of passive burden.

---

## 14. V723 → V724 Interpretation

### V723 established specificity under ideal passive-equivalent controls

V723 showed that passive burden can be held equivalent while restoration behavior remains separable.

### V724 tested robustness under harder conditions

V724 showed that the restoration signal persists when the assay becomes messier:

- capacity distributions overlap,
- recovery is nonlinear,
- fatigue is introduced,
- stalls occur,
- perturbation families vary,
- observation windows become less ideal.

### Combined observation

```text
V723: ideal passive-equivalent specificity
V724: stressed passive-equivalent robustness
```

Together:

> The active restoration-deficit observable retained information not present in passive burden observables across both clean and stressed controlled synthetic assays.

---

## 15. What V723 Supports

V723 supports the observation that:

```text
post-perturbation restoration deficit can separate hidden restoration capacity
even when passive burden observables are held equivalent.
```

This is an internal synthetic assay result.

---

## 16. What V724 Adds

V724 adds the observation that:

```text
the V723 separation weakens under harder conditions but does not disappear,
while passive burden observables remain at chance.
```

This strengthens the V723 result by showing the signal is not only a perfect-clean-assay phenomenon.

---

## 17. What Is Not Established

The runs do not establish:

```text
real-world generality
universal recoverability law
biological recoverability theorem
engineering resilience theorem
physical field theory
GR or quantum analogy
domain-independent validity
```

The current evidence is restricted to the controlled synthetic retained-atlas assay.

---

## 18. Main Peer-Review Concerns and Responses

### Concern 1: Was V723 too clean?

Yes, V723 was intentionally clean.

V724 was introduced specifically to stress-test that concern.

The V724 result degraded realistically:

```text
V723 adm_z AUC: 1.000
V724 adm_z AUC: ~0.845
```

This is a healthier result than perfect persistence.

---

### Concern 2: Could passive burden still explain the result?

In V723 and V724, passive burden observables remained at chance:

```text
passive_mean AUC ≈ 0.500
passive_peak AUC ≈ 0.500
probe_start AUC ≈ 0.500
```

Thus, within these assay designs, passive burden did not explain the classification result.

---

### Concern 3: Is there leakage from `k`?

V723 and V724 should be read as controlled synthetic assays where restoration capacity is intentionally manipulated.

The meaningful question is not whether `k` affects the result, but whether the result is visible through active restoration while passive observables are neutralized.

That condition was met.

---

### Concern 4: Does perfect V723 AUC undermine the result?

Not by itself.

Perfect separation in a clean assay can be valid, but it requires stress testing.

V724 addressed this by making the assay harder and producing a non-perfect but still positive result.

---

### Concern 5: Is this real-world validated?

No.

Real-world validation remains open.

The current result justifies external testing; it does not replace it.

---

## 19. Recommended Next Tests

### 19.1 Real-data mapping

Apply the V713/V723/V724 measurement protocol to external data where:

```text
target_value
observed_value
perturbation magnitude
admissible calibration set
passive burden covariates
```

can be defined.

Candidate domains:

- battery relaxation/recovery data,
- thermal recovery systems,
- cyber remediation telemetry,
- infrastructure recovery after load shocks,
- biological recovery signals where perturbation and recovery windows are measurable.

### 19.2 Harder synthetic stressors

Future runs can further stress the observation using:

```text
stronger stochastic stalls
partial observability
noisy target estimation
delayed response
adaptive adversarial perturbations
mixed topology families
capacity drift over time
calibration-set shift
```

### 19.3 Blind held-out assay

Freeze all code and thresholds, generate hidden labels, then score on held-out synthetic families.

### 19.4 Real-data passive equivalence

The most important real-data test is:

```text
match or stratify by passive burden,
then test whether active restoration deficit adds information.
```

---

## 20. Suggested Peer-Review Claim Boundary

The strongest supported language is:

> In controlled synthetic retained-atlas assays, active post-perturbation restoration deficit separated restoration-capacity conditions even when passive burden observables were held equivalent. Under V724 stress conditions, the separation weakened but persisted, while passive burden metrics remained near chance.

Avoid saying:

```text
we proved a universal law
we discovered a physical law
we proved recoverability geometry
this generalizes to real systems
```

Use:

```text
observed
measured
under controlled synthetic assay
passive-equivalent
stress-tested
specific to this model
requires external validation
```

---

## 21. Conclusion

V723 and V724 together form the strongest retained-atlas result in the current sequence.

V723 closed the specificity objection by showing that `adm_z` separated restoration-capacity conditions while passive burden observables were neutralized.

V724 strengthened the V723 observation by showing the signal persisted under overlapping capacity, nonlinear saturation, fatigue, stochastic stalls, perturbation-family variation, and shortened observation windows.

The result is not a universal claim.

It is a controlled synthetic observation:

> active restoration behavior contained information not present in passive burden metrics.

That observation now appears strong enough to justify real-data testing and independent replication.

---

## Appendix A — Key Metric Definitions

### Restoration measure

```text
mean post-perturbation distance to target
```

### adm_z

```text
adm_z = (restoration_measure - admissible_mean) / admissible_std
```

### Passive mean distance

```text
mean field distance to target during passive evolution
```

### Passive peak distance

```text
maximum field distance to target during passive evolution
```

### Probe start mean

```text
distance to target immediately after perturbation and before relaxation
```

### Curvature-like energy

```text
mean absolute second-variation / Laplacian-like diagnostic
```

### Defect-weighted error

```text
distance-to-target weighted by localized defect field
```

---

## Appendix B — Compact Result Table

| Run | Purpose | adm_z AUC | Passive AUC | Paired Δadm_z | Paired Passive Δ | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| V723 | Passive-equivalent specificity | 1.000 | ~0.500 | ~124.53 | 0.0 | Clean specificity result |
| V724 | Stressed robustness | ~0.845 | ~0.500 | ~1.209 | 0.0 | Signal persists under stress |

---

## Appendix C — Observation-Only Summary

The observations from V723 and V724 are:

1. Passive burden observables were held equivalent or remained non-discriminative.
2. Active post-perturbation restoration deficit remained discriminative.
3. The clean-assay result in V723 weakened under V724 stress, as expected.
4. The signal did not collapse under stress.
5. Real-world validation remains open.

No additional claim is required.
