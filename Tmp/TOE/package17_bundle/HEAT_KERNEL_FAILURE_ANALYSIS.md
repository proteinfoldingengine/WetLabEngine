# HEAT_KERNEL_FAILURE_ANALYSIS.md

# Heat Kernel Failure Analysis
## Diagnosing why the heat-trace coefficient estimator separates geometries but has unstable sign/magnitude

## Status
**Failure analysis. First-principles route retained; current estimator not accepted.**

`HEAT_TRACE_COEFFICIENT_ESTIMATOR.md` produced a promising separation diagnostic, but with questionable signs and magnitudes:

```text
plane:             positive
sphere:            negative
saddle:            small positive
perturbed sphere:  negative
```

That is not acceptable as curvature closure.

A correct scalar-curvature estimator must not merely separate geometries; it must recover the correct sign, scaling, and integrated behavior under a principled heat-time window.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Observation**
- **Definition**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving graph curvature convergence.

---

# 1. Root issue

The heat-kernel principle is correct:

\[
\mathrm{Tr}(e^{-t\Delta})
\sim
(4\pi t)^{-d/2}
\left[
V+\frac{t}{6}\int R\,dV+O(t^2)
\right].
\]

But the graph implementation is not yet controlled.

The estimator:

\[
Y(t)=H_{\mathcal G}(t)(4\pi t)^{d/2}
\]

was fit as:

\[
Y(t)\approx A_0+A_1t.
\]

Then:

\[
\widehat{\int R\,dV}=6A_1.
\]

The diagnostic separated geometries, but sign and scale were not trustworthy.

---

# 2. Likely failure causes

## 2.1 Boundary contamination

Plane and saddle tests used finite patches. Heat trace on a manifold with boundary has additional half-power boundary terms:

\[
t^{1/2},\quad t^{3/2},\ldots
\]

These can dominate or corrupt the \(t\)-coefficient.

This can explain why the plane patch did not behave like \(R=0\).

## 2.2 Wrong heat-time window

The heat expansion is asymptotic as:

\[
t\to0.
\]

But if \(t\) is too small on a graph, discretization noise dominates. If \(t\) is too large, global spectrum/topology dominates.

The valid window must satisfy:

```text
graph spacing scale << diffusion scale << curvature radius scale
```

The current fixed \(c h^2\) window may not satisfy this.

## 2.3 Laplacian normalization

The normalized graph Laplacian erases metric scale. The unnormalized \(h^{-2}(D-W)\) Laplacian retains scale but may have density bias.

Neither is automatically the Laplace-Beltrami operator.

## 2.4 Density and volume normalization

The heat trace coefficient depends on volume measure. A raw point graph has implicit sampling density. Without a consistent volume weight, \(A_0\) and \(A_1\) may mix density artifacts into curvature.

## 2.5 Embedding distance vs intrinsic distance

Sphere, saddle, torus, and plane examples may use ambient chord distance rather than intrinsic geodesic distance. For small neighborhoods this can be acceptable, but it adds bias at finite \(h\).

---

# 3. Verifier implementation

## Status
**Implemented as `heat_kernel_failure_analysis_verifier.py`. Execution log captured.**

The verifier checks sensitivity to:
- boundary by comparing plane patch and flat torus;
- Laplacian choice;
- heat-time window;
- sign/magnitude stability.

## Captured verifier output

```text
Heat kernel failure analysis verifier
==================================================
Route:
test sign/magnitude sensitivity to boundary, Laplacian normalization, and heat window

config,geometry,intR_coeff_median,intR_coeff_std,A0_median,h_median
unnormalized_h2,plane_patch,11.479272489175688,13.547442416638715,3.8837980386268987,0.2159581502178231
unnormalized_h2,flat_torus,-59.11856826723677,14.76996322285992,32.62481089142009,0.6518172197934764
unnormalized_h2,sphere,-37.36064240114522,12.097962827834472,10.649902285661035,0.3692840017936622
unnormalized_h2,saddle_patch,14.436937344072813,16.795927130165964,5.20243584354693,0.24979279803870558
unnormalized_smaller_window,plane_patch,-209.63739987352358,49.80288907426748,5.207197772521502,0.2159581502178231
unnormalized_smaller_window,flat_torus,-396.2687846608115,44.204804570969465,47.892917281256636,0.6518172197934764
unnormalized_smaller_window,sphere,-341.9455771301492,76.30875031155318,15.222678626718869,0.3692840017936622
unnormalized_smaller_window,saddle_patch,-171.94270876307655,31.13376581359482,6.948629946900895,0.24979279803870558
normalized_dimensionless,plane_patch,-38.06610186324306,6.298288257957372,680.5471393381041,0.2159581502178231
normalized_dimensionless,flat_torus,-95.78868687797404,13.27727288671167,686.4553818136785,0.6518172197934764
normalized_dimensionless,sphere,-78.23597158021606,22.68001801211965,684.2562261863367,0.3692840017936622
normalized_dimensionless,saddle_patch,-42.7389355360906,19.086564058703857,681.1266767523218,0.24979279803870558

diagnosis:
if flat_torus differs strongly from plane_patch, boundary/embedding/graph construction matters
if signs flip across windows/configs, coefficient sign is not stable
if normalized config suppresses separation, scale information is erased
```

---

# 4. Interpretation of verifier

The key tests are:

```text
if flat_torus differs strongly from plane_patch, boundary/embedding/graph construction matters
```

```text
if signs flip across windows/configs, coefficient sign is not stable
```

```text
if normalized config suppresses separation, scale information is erased
```

A stable curvature estimator should not depend qualitatively on these choices.

---

# 5. First-principles correction

The next estimator must use:

## 5.1 Boundary-free references first

Use compact boundaryless geometries:

```text
flat torus
sphere
```

before plane patches or saddle patches.

## 5.2 Volume-weighted graph Laplacian

Use a graph Laplacian consistent with a sampled manifold measure, not merely \(D-W\).

## 5.3 Fixed asymptotic window rule

Choose \(t\)-window from graph spacing and curvature scale:

\[
h^2 \ll t \ll L_R^2.
\]

On finite graphs, approximate this by a window sweep and require coefficient plateaus.

## 5.4 Coefficient plateau, not one fit

Accept a heat coefficient only if the estimate is stable over a range of windows.

---

# 6. What this failure means

The heat-kernel route remains the right first-principles direction.

But the current estimator is still diagnostic, not admissible.

The failure is not:

```text
heat-kernel curvature is wrong
```

It is:

```text
the graph Laplacian, volume measure, boundary treatment, and heat-window rule are not controlled enough yet
```

---

# 7. Next derivation target

The next file should be:

```text
BOUNDARY_FREE_HEAT_KERNEL_TESTS.md
```

Purpose:

Test only boundaryless reference geometries first:

```text
flat torus
sphere
```

with:
- one volume-weighted graph Laplacian;
- heat-window plateau detection;
- no per-geometry calibration;
- expected sign/order:
  \[
  \int R_{\mathrm{sphere}}dV>0,
  \qquad
  \int R_{\mathrm{flat\ torus}}dV=0.
  \]

Only after that should finite patches or negative-curvature proxies be reintroduced.

---

# Honest status line

> `HEAT_KERNEL_FAILURE_ANALYSIS.md` diagnoses the current spectral estimator failure: it separates geometries but lacks sign and scale control due to boundary effects, graph Laplacian scaling, volume normalization, and heat-window instability. The first-principles route remains heat-kernel based, but the next tests must be boundary-free and plateau-based.

**End of file.**
