# V725 Atrium Metric Extraction

## Purpose

V725 begins **Step 3: Extract the Atrium Metric** from the retained-atlas recoverability stack.

V723 closed the specificity objection by showing that active restoration can separate hidden restorative capacity while passive burden observables are held equivalent.

V725 asks the next question:

> What operational geometry is this restoration signal living in?

The goal is not yet to derive a GR metric tensor.  
The goal is to extract a first response-geometry scalar that can later be generalized into a metric-field candidate.

---

## Scientific posture

This work does **not** claim:

- Einstein field equations,
- GR recovery,
- spacetime curvature,
- quantum collapse mechanics,
- or a universal physical law.

It claims only this:

> In a controlled synthetic retained-atlas assay, a scalar built from post-perturbation restoration behavior tracks hidden restorative capacity while passive burden remains fixed.

---

## Background

The project’s current bridge is:

```text
Step 1: Discover/freeze recoverability observable
Step 2: Close perturbation-response / Lyapunov-style restoration behavior
Step 3: Extract Atrium Metric
Step 4: Compare to GR-like structure
Step 5: Testable predictions
```

V723/V724 established that:

```text
passive burden ≈ chance
active restoration ≈ signal
```

V725 converts that signal into a first candidate metric scalar.

---

## Passive-equivalent assay design

For each paired counterfactual:

```text
same passive baseline
same pre-probe state
same perturbation mask
same perturbation amplitude
same relaxation noise
same target field
same observation window
only k changes
```

This means passive burden is held equivalent by construction.

The system then asks:

> After identical perturbation, does the system restore differently because k differs?

---

## Frozen restoration observable

The base observable remains:

```text
adm_z = (restoration_measure - admissible_mean) / admissible_std
```

Where:

```text
restoration_measure = mean post-relaxation distance to target field
```

Positive `adm_z` means worse restoration than the admissible high-k baseline.

---

## Candidate Atrium scalar

V725 defines:

```text
A = adm_z
  + 2(1 - contraction)
  + (1 - curvature_relief)
  + 0.15 log(1 + metric_strain)
```

Where:

| Component | Meaning |
|---|---|
| `adm_z` | admissible-normalized restoration deficit |
| `contraction` | fractional return toward target after perturbation |
| `curvature_relief` | reduction in curvature-like second variation during relaxation |
| `metric_strain` | path length per unit restoration, a response inefficiency term |

Interpretation:

```text
High A = poor response geometry / high restoration deformation.
Low A = admissible-like response geometry.
```

---

## V725 result

The compact run produced:

```text
adm_z AUC:             1.000
Atrium metric AUC:     1.000
passive mean AUC:      0.500
passive curvature AUC: 0.500
```

The paired deltas showed:

```text
paired_delta_atrium_mean ≈ 22.58
paired_delta_adm_z_mean  ≈ 21.79
paired_delta_passive_abs_max = 0.0
```

So the extracted Atrium scalar is response-specific while passive burden is held fixed.

---

## K-gap behavior

The k-gap ablation produced:

| k_gap | Atrium AUC |
|---:|---:|
| 0.80 | 1.000 |
| 0.65 | 1.000 |
| 0.50 | 1.000 |
| 0.30 | 1.000 |
| 0.15 | 1.000 |
| 0.00 | ~0.524 |

This matters because the metric collapses toward null when the hidden restorative-capacity gap disappears.

---

## Scientific interpretation

V725 is the first extraction of an **operational Atrium scalar**.

It suggests that recoverability geometry can be represented as a composite response quantity involving:

```text
restoration deficit
+ contraction failure
+ curvature-like non-relief
+ inefficient trajectory strain
```

This is not yet a tensor.

It is a scalar prototype.

---

## What V725 supports

V725 supports the statement:

> A response-geometry scalar can be extracted from passive-equivalent perturbation-response assays and can track hidden restorative capacity better than passive burden observables.

---

## What V725 does not yet establish

V725 does not establish:

- coordinate invariance,
- tensor structure,
- GR compatibility,
- Einstein equations,
- real-world validity,
- universality.

---

## Next step

The correct next step is:

```text
V726 — Local Atrium Tensor Candidate
```

V726 should move from a run-level scalar to a local field:

```text
g_atrium(x,y)
```

It should test:

1. locality,
2. coordinate perturbation robustness,
3. perturbation-family invariance,
4. monotonic dependence on k,
5. collapse to null at k_gap = 0,
6. relation to Lyapunov/energy descent.

Only after that should the project return to GR matching.
