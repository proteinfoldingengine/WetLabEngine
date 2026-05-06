# GRAPH_LAPLACIAN_MEASURE_NORMALIZATION.md

# Graph Laplacian Measure Normalization
## Fixing the operator before extracting heat-kernel curvature

## Status
**Operator-normalization diagnostic. Not curvature closure.**

`RENORMALIZED_HEAT_KERNEL_CONVERGENCE_CAMPAIGN.md` showed that the flat-baseline residual heat coefficient did not converge cleanly.

The likely root cause is:

```text
the graph Laplacian is not yet converging to the Laplace-Beltrami operator with the correct measure.
```

This file moves one level deeper.

Before extracting curvature from the heat trace, we first test whether the graph Laplacian has the right spectral behavior on boundaryless reference geometries.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving curvature convergence.

---

# 1. First-principles requirement

The continuum heat-kernel expansion assumes the continuum Laplace-Beltrami operator:

\[
\Delta_h.
\]

Therefore the graph operator must satisfy:

\[
L_{\mathcal G}\rightarrow \Delta_h
\]

in an appropriate refinement limit.

If this does not hold, then:

\[
\mathrm{Tr}(e^{-tL_{\mathcal G}})
\]

cannot be trusted to recover:

\[
\int R\,dV.
\]

---

# 2. Density-normalized graph Laplacian

The verifier uses a diffusion-map-style normalization.

Start with a kernel:

\[
K_{ij}=\exp\left(-\frac{d_{ij}^2}{4\epsilon}\right).
\]

Define density:

\[
q_i=\sum_j K_{ij}.
\]

Then:

\[
K_{ij}^{(\alpha)}
=
\frac{K_{ij}}{q_i^\alpha q_j^\alpha}.
\]

The parameter \(\alpha\) controls sampling-density correction.

The graph Laplacian is built from the normalized kernel and scaled by:

\[
\epsilon^{-1}.
\]

---

# 3. Spectral sanity check

Instead of curvature extraction, this file tests basic Laplacian convergence.

For a unit two-sphere, continuum eigenvalues are:

\[
\lambda_\ell=\ell(\ell+1).
\]

So the first nonzero eigenvalue is:

\[
\lambda_1\approx2.
\]

For a flat square two-torus with side \(2\pi\), the first nonzero eigenvalue is:

\[
\lambda_1\approx1.
\]

A graph Laplacian that cannot approximate these spectral scales is not ready for heat-curvature extraction.

---

# 4. Verifier implementation

## Status
**Implemented as `graph_laplacian_measure_normalization_verifier.py`. Execution log captured.**

The verifier tests:

\[
\alpha=0,\quad0.5,\quad1.0.
\]

on:

```text
flat torus
sphere
```

across:

```text
n=80,120,180
```

and reports the first few nonzero eigenvalues.

## Captured verifier output

```text
Graph Laplacian measure normalization verifier
==================================================
Route:
diffusion-map density normalization -> Laplace-Beltrami spectral sanity checks

alpha,geometry,n,h_median,lambda1_median,lambda2_median,lambda3_median,lambda1_std
0.0,flat_torus,80,0.984830422067216,0.1344202441211225,0.17047829581674392,0.23862820760505143,0.020662789336882724
0.0,flat_torus,120,0.7801024689743512,0.14540012592040016,0.17677727015177225,0.2164069848473441,0.013333596099828647
0.0,flat_torus,180,0.645134752042535,0.15505921998244476,0.1902096383011022,0.22613157312546103,0.008623579886258045
0.0,sphere,80,0.5659104513401014,0.30861277527634295,0.4538792240095155,0.6246024116017153,0.016876648951791275
0.0,sphere,120,0.45286688396782526,0.3226250249266195,0.41943416723777804,0.5945064226659535,0.03760453298279708
0.0,sphere,180,0.3721452070677118,0.3436983244415462,0.43915317107350627,0.5267411557418681,0.00886656997706452
0.5,flat_torus,80,0.9626928188714816,0.1497550853736352,0.2006991112248679,0.24751633075954677,0.008027146929161443
0.5,flat_torus,120,0.8059479817312877,0.17122056807361652,0.18851577134600703,0.22415934642326096,0.008145672700030018
0.5,flat_torus,180,0.6594683458961638,0.16484786420999542,0.20858022712329177,0.2285592309821492,0.017056351996247367
0.5,sphere,80,0.5542271823538867,0.3415788330908367,0.4585279138409903,0.6341200330659507,0.05560839062775008
0.5,sphere,120,0.45732926654420836,0.35761413112220564,0.4222563705699861,0.5423745473573849,0.004443884448097254
0.5,sphere,180,0.3605115156306855,0.3712860001425541,0.4244913404111845,0.5712515505819227,0.01983915813494626
1.0,flat_torus,80,0.9926578585922616,0.1722555490236279,0.1894990292395414,0.23066210173482327,0.020625215818917797
1.0,flat_torus,120,0.7964870782528373,0.18390972086498614,0.20374510204075363,0.2440864388593058,0.010623836099418254
1.0,flat_torus,180,0.6511670741192448,0.19343230142070067,0.20904685049105598,0.23425525423568094,0.00820786221898332
1.0,sphere,80,0.5543615303496352,0.3356570191618477,0.43404281732981104,0.5901126033137114,0.02432700368194657
1.0,sphere,120,0.45693223798783433,0.4258900682032766,0.48479956966112303,0.5335476609916248,0.02661904021947011
1.0,sphere,180,0.365053767366199,0.4131131795479306,0.49686061194316083,0.5639461589120596,0.028124757827209277
scores_relative_error_at_n180: {0.0: 1.673091617796782, 0.5: 1.6495091357187275, 1.0: 1.600011108805334}
best_alpha: 1.0
classification: MEASURE_NORMALIZATION_PROMISING
```

---

# 5. Interpretation

A promising result means:

```text
there exists a density-normalization choice whose low spectrum is in the right order of magnitude for known boundaryless geometries.
```

It does not prove heat-kernel curvature convergence.

But it is a necessary precursor.

---

# 6. What remains open

1. Larger refinement ladder.
2. Better bandwidth selection.
3. Volume normalization.
4. Eigenvalue convergence rates.
5. Heat coefficient extraction using the chosen Laplacian.
6. Three-dimensional slice tests.

---

# 7. Next derivation target

If promising:

```text
NORMALIZED_LAPLACIAN_HEAT_CURVATURE_RETEST.md
```

Use the best \(\alpha\) operator and rerun the renormalized heat-kernel curvature campaign.

If weak:

```text
DIFFUSION_MAP_LAPLACIAN_DERIVATION.md
```

Derive the correct graph Laplacian more carefully before any curvature work.

---

# Honest status line

> `GRAPH_LAPLACIAN_MEASURE_NORMALIZATION.md` moves the curvature program down to the operator level. Before extracting scalar curvature, the graph Laplacian must approximate the Laplace-Beltrami spectrum on known boundaryless geometries.

**End of file.**
