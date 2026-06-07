# V1688.38 — Prior ADM-Like Weak-Form Reconstruction Plan

**Project:** Retained Bridge / Recoverability Geometry  
**Branch:** reconnect Gamma_R/L3/L4 results to prior ADM-like same-slice weak-form work  
**Status:** reconstruction plan after V1688.37 synthetic target exhaustion  
**Claim level:** planning / reconstruction protocol only; no ADM / GR / physical spacetime claim

---

## 1. Executive Verdict

```text
PRIOR_ADM_LIKE_WEAK_FORM_RECONSTRUCTION_PLAN_DEFINED
```

V1688.35–V1688.36 showed that synthetic independent-flow targets were not useful because the source/divergence baseline saturated them.

Therefore the next valid target should not be invented synthetically.

The correct next move is:

```text
reconstruct the earlier ADM-like / same-slice weak-form harness
that already produced a nontrivial residual signal.
```

Then test whether Gamma_R / L3 / L4 features improve that reconstructed target.

---

## 2. Why This Plan Is Needed

The current state is:

```text
Gamma_R connection branch:
  supported as connection-like;
  L3/O3 dominates loop defect;
  L4/H4_perp adds independent loop-defect correction;
  compatibility / curvature-field closure failed.

Edge-faithfulness branch:
  strong for residuals containing edge strain;
  failed as predictor of independent synthetic targets;
  synthetic targets saturated by baseline.

Earlier ADM-like branch:
  had nontrivial same-slice / weak-form signals.
```

The earlier ADM-like branch is now the best target because it was not trivially saturated.

Known prior signals:

```text
momentum-like closure supported
flow-only predicted momentum-like branch
curvature-only failed
weak-form / ADM-like same-slice constraint signal
R_conf vs C_surplus corr ≈ 0.749
R² ≈ 0.561
continuum scaling residual p ≈ 2
```

These are exactly the kind of non-saturated targets needed.

---

## 3. Reconstruction Objective

The objective is to rebuild the earlier weak-form same-slice target as cleanly as possible.

Target object:

```text
R_weak_form
```

where:

```text
R_weak_form = residual of same-slice retained-flow / constraint balance
```

It must be reconstructed without using:

```text
edge-faithfulness by construction
O3 by construction
H4 by construction
post-hoc fitted counterterms
```

Then test whether Gamma_R-derived features add explanatory power.

---

## 4. Candidate Model Stack

Reconstructed target:

```text
Y = R_weak_form
```

Baseline model:

```text
M0 = original source-flow / same-slice weak-form predictors
```

Correction models:

```text
M1 = M0 + Gamma_R edge-faithfulness
M2 = M0 + O3 / L3 associator features
M3 = M0 + H4_perp / L4 features
M4 = M0 + edge + O3 + H4_perp
```

Pass logic:

```text
A correction is meaningful only if it improves held-out prediction
or residual explanation beyond M0 and survives nulls.
```

---

## 5. Required Inputs to Reconstruct

The reconstruction needs the original weak-form ingredients:

```text
source field
retained adjacency graph
accessibility / flow vector
same-slice divergence
C_surplus or closure surplus
R_conf or conformal curvature-like scalar proxy
momentum-like branch indicator
constraint residual definition
resolution ladder / grid size
null controls used in earlier branch
```

If exact original code is unavailable, rebuild only from definitions and label it:

```text
clean-room weak-form reconstruction
```

not:

```text
original harness replication
```

---

## 6. Required Guardrails

Do not use:

```text
time as primitive
physical spacetime assumptions
GR tensors
ADM equations as assumed truth
heuristic counterterms
threshold tuning
cosmetic residual subtraction
```

Use retained-order language:

```text
same-slice
ordered update
retained adjacency
source-flow
constraint residual
continuity closure
provenance/order flux
```

The target should be mathematical / informational, not physical spacetime.

---

## 7. Required Nulls

Minimum null set:

```text
edge-faithfulness shuffle
O3 shuffle
H4_perp shuffle
source-flow-preserving null
branch-label shuffle
transport-randomized null
linear recombination control
resolution/refinement ladder
operator-family variation
```

Important null:

```text
source-flow-preserving null
```

because the earlier ADM-like signal may be primarily source-flow driven.

Gamma_R features must add signal without merely re-encoding source flow.

---

## 8. Required Metrics

Report:

```text
R² / ΔR² over baseline
held-out prediction error
AUC if classification target exists
residual reduction
null margin
positive-gain rate across seeds / resolutions
scaling trend under refinement
leave-one-feature-family-out
```

For correction features:

```text
edge gain = M1 − M0
O3 gain = M2 − M0
H4 gain = M3 − M0
combined gain = M4 − M0
```

---

## 9. Success Criteria

### Strong Pass

```text
A Gamma_R-derived feature improves the reconstructed weak-form target beyond M0,
survives nulls,
and persists under refinement.
```

### Partial Pass

```text
A feature improves the target in some operator families / resolutions,
but not enough for closure.
```

### Fail

```text
No Gamma_R / O3 / H4 feature improves the reconstructed weak-form target beyond M0.
```

### Degenerate

```text
M0 saturates the reconstructed target with R² ≈ 1.0,
making corrections untestable.
```

If degenerate:

```text
the target is not suitable for correction testing.
```

---

## 10. Scientific Questions

The reconstruction should answer:

```text
1. Was the earlier ADM-like signal primarily source-flow conservation?
2. Does Gamma_R edge-faithfulness add anything beyond source-flow?
3. Does O3/L3 add anything beyond edge-faithfulness?
4. Does H4/L4 add anything beyond O3/L3?
5. Are Gamma_R features correction terms or separate diagnostics?
6. Does the result scale with refinement?
7. Does the result survive source-flow-preserving nulls?
```

---

## 11. Expected Outcomes

Possible outcome A:

```text
source-flow alone explains the weak-form target.
```

Meaning:

```text
ADM-like behavior belongs to source-flow branch, not Gamma_R.
```

Possible outcome B:

```text
edge / O3 improves weak-form target beyond source-flow.
```

Meaning:

```text
L3/Gamma_R has a legitimate correction role.
```

Possible outcome C:

```text
H4_perp improves beyond O3.
```

Meaning:

```text
L4 contributes to weak-form correction, not only loop-defect correction.
```

Possible outcome D:

```text
no correction survives nulls.
```

Meaning:

```text
Gamma_R and ADM-like flow remain separate branches.
```

---

## 12. Recommended Next Executable

```text
V1688.39 — Clean-Room Weak-Form Harness Rebuild
```

Deliverable:

```text
standalone Python harness that reconstructs a non-saturated weak-form same-slice target
from source-flow / closure / conformal-like residual ingredients.
```

Then V1688.40 should test:

```text
Gamma_R correction features against that target.
```

---

## 13. Final Status

```text
V1688.38 defines the correct reconstruction plan.

Do not continue synthetic target invention.

Return to the earlier ADM-like weak-form branch,
rebuild its target cleanly,
then test Gamma_R/L3/L4 corrections under nulls.
```
