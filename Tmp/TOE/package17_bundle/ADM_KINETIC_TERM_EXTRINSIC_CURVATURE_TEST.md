# ADM_KINETIC_TERM_EXTRINSIC_CURVATURE_TEST.md

# ADM Kinetic Term / Extrinsic Curvature Test
## Analytic reference for the full ADM geometric integrand

## Status
**Analytic ADM kinetic reference created and verified. Not graph recovery yet. Not full ADM closure.**

`PATCHED_AUTONOMOUS_ADM_SPATIAL_ACTION_RESULT.md` established a successful diagnostic recovery of the spatial curvature action term:

\[
\int_\Sigma N\sqrt h\,R^{(3)}d^3x.
\]

The next ADM seam is the kinetic/extrinsic-curvature term:

\[
\int_\Sigma N\sqrt h\left(K_{ij}K^{ij}-K^2\right)d^3x.
\]

This file creates the analytic target for that term.

---

# 1. Controlled time-dependent metric

Use a time-dependent conformal spatial metric:

\[
h_{ij}(t,x)=e^{2\phi(t,x)}\delta_{ij},
\]

with:

\[
\phi(t,x,y,z)=a\cos(\omega t)\cos x\cos y\cos z.
\]

With zero shift and unit lapse:

\[
K_{ij}=\frac{1}{2}\partial_t h_{ij}.
\]

Since:

\[
\partial_t h_{ij}=2\dot\phi h_{ij},
\]

we get:

\[
K_{ij}=\dot\phi h_{ij}.
\]

Therefore:

\[
K^i{}_j=\dot\phi\delta^i{}_j,
\]

\[
K=3\dot\phi,
\]

\[
K_{ij}K^{ij}=3\dot\phi^2,
\]

and:

\[
K_{ij}K^{ij}-K^2=-6\dot\phi^2.
\]

This gives an exact analytic ADM kinetic target.

---

# 2. Full ADM geometric slice target

The single-slice geometric integrand is:

\[
N\sqrt h
\left[
R^{(3)}
+
K_{ij}K^{ij}
-
K^2
\right].
\]

The verifier computes:

\[
I_R=\int N\sqrt h R^{(3)}d^3x,
\]

\[
I_K=\int N\sqrt h(K_{ij}K^{ij}-K^2)d^3x,
\]

\[
I_{\mathrm{ADM}}=I_R+I_K.
\]

---

# 3. Verifier implementation

Implemented as:

```text
adm_kinetic_term_extrinsic_curvature_verifier.py
```

Execution log:

```text
adm_kinetic_term_extrinsic_curvature_verifier_run.log
```

## Captured output

```text
ADM kinetic/extrinsic curvature verifier
==================================================
Route:
time-dependent conformal metric -> analytic K_ij -> ADM kinetic integrand

N,nodes,lapse_kind,dx,I_R,I_K,I_ADM,I_K_ref,kinetic_identity_rel_error,mean_phidot,std_phidot,mean_lapse,min_lapse,max_lapse
16,4096,unit,0.39269908169872414,4.010012021067027,-0.017046005030704758,3.992966016036323,-0.017046005030704758,0.0,-4.446922973085076e-21,0.003316576697699525,1.0,1.0,1.0
16,4096,smooth_positive,0.39269908169872414,4.010012021067026,-0.017046005030704758,3.992966016036324,-0.01704600503070476,2.0353431466790064e-16,-4.446922973085076e-21,0.003316576697699525,1.0,0.85,1.1500000000000001
16,4096,curvature_coupled,0.39269908169872414,9.485065512397073,-0.01735568315691212,9.467709829240164,-0.017355683156912122,1.999026440150217e-16,-4.446922973085076e-21,0.003316576697699525,1.0,0.9,1.1
16,4096,mixed_wave,0.39269908169872414,4.010012021067026,-0.017046005030704758,3.992966016036323,-0.017046005030704758,0.0,-4.446922973085076e-21,0.003316576697699525,1.0,0.8999999999999999,1.1
24,13824,unit,0.2617993877991494,4.010012021067024,-0.017046005030704754,3.992966016036319,-0.017046005030704754,0.0,3.6082308880247284e-21,0.0033165766976995244,1.0,1.0,1.0
24,13824,smooth_positive,0.2617993877991494,4.010012021067024,-0.017046005030704754,3.992966016036319,-0.017046005030704754,0.0,3.6082308880247284e-21,0.0033165766976995244,1.0,0.85,1.1500000000000001
24,13824,curvature_coupled,0.2617993877991494,9.485065512397066,-0.017355683156912112,9.467709829240153,-0.017355683156912112,0.0,3.6082308880247284e-21,0.0033165766976995244,1.0,0.9,1.1
24,13824,mixed_wave,0.2617993877991494,4.010012021067024,-0.01704600503070475,3.9929660160363185,-0.01704600503070475,0.0,3.6082308880247284e-21,0.0033165766976995244,1.0,0.8999999999999999,1.1
32,32768,unit,0.19634954084936207,4.010012021067027,-0.017046005030704758,3.992966016036322,-0.017046005030704758,0.0,-8.528232115421721e-22,0.0033165766976995244,1.0,1.0,1.0
32,32768,smooth_positive,0.19634954084936207,4.010012021067026,-0.017046005030704758,3.992966016036323,-0.017046005030704758,0.0,-8.528232115421721e-22,0.0033165766976995244,1.0,0.85,1.1500000000000001
32,32768,curvature_coupled,0.19634954084936207,9.485065512397071,-0.017355683156912115,9.46770982924016,-0.017355683156912115,0.0,-8.528232115421721e-22,0.0033165766976995244,1.0,0.9,1.1
32,32768,mixed_wave,0.19634954084936207,4.010012021067026,-0.017046005030704758,3.992966016036321,-0.017046005030704758,0.0,-8.528232115421721e-22,0.0033165766976995244,1.0,0.8999999999999999,1.1
40,64000,unit,0.15707963267948966,4.010012021067025,-0.017046005030704754,3.992966016036321,-0.017046005030704758,2.035343146679007e-16,9.551049684495452e-22,0.0033165766976995244,1.0,1.0,1.0
40,64000,smooth_positive,0.15707963267948966,4.010012021067026,-0.017046005030704754,3.992966016036321,-0.017046005030704754,0.0,9.551049684495452e-22,0.0033165766976995244,1.0,0.85,1.1500000000000001
40,64000,curvature_coupled,0.15707963267948966,9.48506551239707,-0.017355683156912115,9.467709829240157,-0.017355683156912115,0.0,9.551049684495452e-22,0.0033165766976995244,1.0,0.9,1.1
40,64000,mixed_wave,0.15707963267948966,4.010012021067025,-0.017046005030704754,3.992966016036321,-0.017046005030704754,0.0,9.551049684495452e-22,0.0033165766976995244,1.0,0.8999999999999999,1.1
kinetic_identity_ok: True
finite_action_terms_ok: True
unit_IK_grid_cv: 1.4392049410582919e-16
unit_IK_grid_cv_lt_1e_minus_10: True
classification: ADM_KINETIC_ANALYTIC_REFERENCE_READY
```

---

# 4. Interpretation

This file only verifies the analytic ADM kinetic reference.

It does not yet recover \(K_{ij}\) from graph slices.

It prepares the target for the next file:

```text
GRAPH_EXTRINSIC_CURVATURE_PROXY.md
```

---

# 5. What is now ready

Ready:

```text
analytic R^(3)
analytic K_ij
analytic K
analytic K_ijK^ij - K^2
analytic full ADM geometric integrand
```

Not ready:

```text
graph recovery of K_ij
graph recovery of inter-slice distance
causal lapse/shift
variation of action
Einstein equations
```

---

# 6. Next target

```text
GRAPH_EXTRINSIC_CURVATURE_PROXY.md
```

Purpose:

Recover:

\[
K^i{}_j
\]

or at least its scalar contraction:

\[
K_{ij}K^{ij}-K^2
\]

from two nearby graph slices:

\[
h_{ij}(t),\quad h_{ij}(t+\Delta t).
\]

For the conformal test case, the target is especially simple:

\[
K_{ij}K^{ij}-K^2=-6\dot\phi^2.
\]

---

# Honest status line

> `ADM_KINETIC_TERM_EXTRINSIC_CURVATURE_TEST.md` creates and verifies the analytic ADM kinetic/extrinsic-curvature reference for a time-dependent conformal metric. It prepares the kinetic seam but does not yet recover \(K_{ij}\) from graphs.

**End of file.**
