# HEAT_NORMALIZATION_THEOREM_PROGRAM.md

# Heat Normalization Theorem Program
## Turning the spatial heat branch from calibrated diagnostic into theorem obligations

## Status
**Theorem program ready. Not yet proved.**

After `ADM_FULL_OPERATOR_KINETIC_ACTION_RESULT.md`, the fitted kinetic-scale seam is removed in the controlled conformal setting. The remaining dominant seam is now the spatial heat branch.

Current best result:

```text
classification: ADM_FULL_OPERATOR_KINETIC_ACTION_PROMISING
ADM_action_rel_error_max: 0.01905
K_action_rel_error_max: ~4.08e-10
R_action_rel_error_max: 0.01901
```

Interpretation:

```text
kinetic branch is now operator-derived
remaining full-action error is spatial heat normalization / zero-mode
```

---

# 1. Local heat diagonal theorem target

The local heat diagonal is:

\[
K_i(t)=[e^{-tL}]_{ii}.
\]

Define:

\[
H_i(t)=K_i(t)(4\pi t)^{3/2}.
\]

Fit:

\[
H_i(t)\approx A_i+B_i t.
\]

The current empirical estimator is:

\[
\widehat R_i=-\frac{6B_i}{dx}.
\]

The theorem target is:

\[
B_i \sim -\frac{dx}{6}R_i
\]

for the graph-normalized weighted Laplacian used in the ADM proxy.

This must explain:
- why the extra `dx` appears;
- why the sign is negative;
- why the estimator is stable across \(N\);
- what error order remains.

---

# 2. Global heat-trace zero-mode theorem target

The global heat trace is:

\[
H(t)=\mathrm{Tr}(e^{-tL})(4\pi t)^{3/2}.
\]

Fit:

\[
H(t)\approx A+Bt.
\]

The target is to derive:

\[
\int R\,dV=C_{\mathrm{trace}}(dx,L,W)B+o(1).
\]

The current diagnostic learns this map by calibration. The theorem must derive it.

Known evidence from the Colab/T4 campaign:

```text
heat-trace zero-mode R² > 0.999949
max relative error < 0.00445 after calibration
```

---

# 3. Heat-window theorem target

The current working window is:

```text
t = multiplier * dx^2
```

The theorem must justify:
- why \(t\sim dx^2\);
- which multiplier range suppresses higher-order heat terms;
- how the window changes with dimension, graph degree, and metric variation.

---

# 4. Sign convention theorem target

The estimator uses:

\[
-6B_i/dx.
\]

The theorem must derive the sign from:
- the graph Laplacian convention \(L=(D-W)/dx^2\);
- the edge-weight response under conformal expansion;
- the relationship between increased local scale and reduced weighted degree / heat return.

---

# 5. ADM-measure offset theorem target

The patched ADM spatial action demonstrated that the zero mode must be restored in the ADM measure:

\[
c=
\frac{
I_R^{trace}-
\sum_i\sqrt h_i\widehat R_{centered,i}dx^3
}{
\sum_i\sqrt h_i dx^3
}.
\]

This must be written as a lemma:

```text
zero-mode restoration must be performed in the same measure used by the action
```

not as an arithmetic node mean.

---

# 6. Lightweight verifier

Implemented as:

```text
heat_normalization_theorem_program_verifier.py
```

Run log:

```text
heat_normalization_theorem_program_verifier_run.log
```

Verifier output:

```text
Heat normalization theorem program lightweight verifier
============================================================
Purpose: freeze theorem obligations after kinetic scale removal.

OBLIGATIONS:
local_dx_normalization: derive why B_i scales as -dx*R_i/6 for the chosen graph Laplacian
global_trace_zero_mode: derive C_trace such that int R dV = C_trace * trace_slope + o(1)
heat_window_selection: derive t ~ dx^2 and admissible multiplier range
sign_convention: derive sign from L=(D-W)/dx^2 and conformal weight response
measure_offset: prove zero mode must be restored in ADM measure sqrt(h)d^3x

EVIDENCE_INPUTS:
direct_heat_local_R_corr: ~0.965 from prior dx-normalized 3D heat tests
heat_trace_zero_mode_R2: >0.999949 from Colab/T4 zero-mode campaign
patched_ADM_spatial_action_max_error: <0.01964
operator_kinetic_scale_removed: A phidot = dotd recovered phidot to ~1e-9 relative L2
full_ADM_operator_kinetic_max_error: 0.01905 dominated by spatial heat branch

NEXT_FILES:
LOCAL_HEAT_DX_NORMALIZATION_THEOREM.md
GLOBAL_HEAT_TRACE_ZERO_MODE_THEOREM.md
HEAT_WINDOW_SCALE_SELECTION.md
SIGN_CONVENTION_FOR_GRAPH_HEAT_CURVATURE.md

classification: HEAT_NORMALIZATION_THEOREM_PROGRAM_READY
```

---

# 7. Next files

Create these next:

```text
LOCAL_HEAT_DX_NORMALIZATION_THEOREM.md
GLOBAL_HEAT_TRACE_ZERO_MODE_THEOREM.md
HEAT_WINDOW_SCALE_SELECTION.md
SIGN_CONVENTION_FOR_GRAPH_HEAT_CURVATURE.md
```

The immediate next file should be:

```text
LOCAL_HEAT_DX_NORMALIZATION_THEOREM.md
```

---

# Honest status

> `HEAT_NORMALIZATION_THEOREM_PROGRAM.md` does not prove heat normalization. It freezes the remaining proof obligations after the kinetic operator seam was removed. The next step is to derive the local dx-normalization relation \(B_i\sim -dxR_i/6\).

**End of file.**
