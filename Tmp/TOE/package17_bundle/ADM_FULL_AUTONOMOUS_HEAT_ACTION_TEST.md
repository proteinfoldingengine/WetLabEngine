# ADM_FULL_AUTONOMOUS_HEAT_ACTION_TEST.md

# ADM Full Autonomous Heat Action Test
## Replacing degree spatial curvature with autonomous heat curvature in the full ADM proxy

## Status
**Colab/CPU script prepared. Not yet executed.**

`ADM_FULL_GEOMETRIC_ACTION_PROXY.md` passed using a calibrated degree-based spatial curvature proxy plus a graph kinetic proxy.

This test upgrades the spatial branch.

It combines:

\[
\widehat R^{(3)}_{\mathrm{heat,auto}}
\]

from:

```text
local dx-normalized heat diagonal
+
global heat-trace zero mode
+
ADM-measure offset
```

with:

\[
\widehat{K_{ij}K^{ij}-K^2}_{\mathrm{graph}}
\]

from:

```text
two-slice graph degree-time derivative
```

The target is:

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

# 1. Prepared script

Created:

```text
adm_full_autonomous_heat_action_test.py
```

Initial grid ladder:

```text
N = 8, 10, 12, 14
```

Test amplitude:

```text
a = 0.15
```

Calibration amplitudes:

```text
0.05, 0.08, 0.10, 0.12, 0.18, 0.20, 0.25
```

---

# 2. What to send back

After running, send:

```text
ADM FULL AUTONOMOUS HEAT ACTION SUMMARY
CSV_ROWS
GPU or CPU used
```

---

# 3. Pass criteria

Promising if:

```text
ADM_action_rel_error_max < 0.10
ADM_density_corr_min > 0.95
ADM_local_corr_min > 0.95
```

---

# 4. Caveat

This is still calibrated because:

```text
heat-trace zero mode uses calibration amplitudes
kinetic proxy uses fitted phidot scale
```

But it removes the degree-based spatial curvature proxy from the full ADM action test.

**End of file.**
