# ADM_FULL_OPERATOR_KINETIC_ACTION_TEST.md

# ADM Full Operator-Kinetic Action Test
## Full ADM action with heat spatial curvature and operator-derived kinetic term

## Status
**Script prepared. Not yet executed.**

This test replaces the fitted kinetic proxy in the full ADM action test with:

\[
A\widehat{\dot\phi}=\dot d.
\]

The operator \(A\) is derived directly from the graph weight law:

\[
\dot d_i
=
-\frac14
\sum_{j\sim i}
w_{ij}e^{2\phi_{ij}}
(\dot\phi_i+\dot\phi_j).
\]

Then:

\[
\widehat{K_{ij}K^{ij}-K^2}
=
-6\widehat{\dot\phi}^{\,2}.
\]

The spatial term remains:

\[
\widehat R^{(3)}_{\mathrm{heat,auto}}.
\]

The full target is:

\[
\int_\Sigma N\sqrt h
\left[
R^{(3)}
+
K_{ij}K^{ij}
-
K^2
\right]d^3x.
\]

---

# Prepared file

```text
adm_full_operator_kinetic_action_test.py
```

Run it and send back:

```text
ADM FULL OPERATOR-KINETIC ACTION SUMMARY
CSV_ROWS
GPU or CPU used
```

---

# Expected significance

If this passes, the full ADM geometric action diagnostic no longer depends on a fitted kinetic scale in the controlled conformal setting.

Remaining calibrated seam would mainly be:

```text
heat-trace spatial zero-mode calibration
```

**End of file.**
