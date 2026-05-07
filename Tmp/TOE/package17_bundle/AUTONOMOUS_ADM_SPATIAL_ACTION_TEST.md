# AUTONOMOUS_ADM_SPATIAL_ACTION_TEST.md

# Autonomous ADM Spatial Action Test
## Combining local heat curvature and heat-trace zero mode

## Status
**Colab test script prepared. Not yet executed.**

This is the first autonomous-with-calibrated-zero-mode ADM spatial curvature action diagnostic.

It combines:

```text
local dx-normalized heat diagonal
+
global heat-trace zero mode
```

to reconstruct \(R^{(3)}\) without analytic mean insertion.

## Reconstruction

\[
\widehat R^{(3)}_{\mathrm{auto}}
=
s(\widehat R_{\mathrm{local}}-\langle\widehat R_{\mathrm{local}}\rangle)
+
\bar R_{\mathrm{trace}}.
\]

Then:

\[
\widehat I_R
=
\sum_i N_i\sqrt h_i\widehat R^{(3)}_{\mathrm{auto},i}dx^3.
\]

## Prepared script

Created:

```text
autonomous_adm_spatial_action_test.py
```

Run on T4 GPU and send back:

```text
AUTONOMOUS ADM SPATIAL ACTION SUMMARY
CSV_ROWS
GPU or CPU used
```

## Important caveat

The zero-mode map is still calibrated from reference amplitudes, so a pass would be:

```text
autonomous-with-calibrated-zero-mode ADM spatial action recovery
```

not theorem closure and not full GR.

**End of file.**
