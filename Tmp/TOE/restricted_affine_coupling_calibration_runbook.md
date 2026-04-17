# Restricted Affine Coupling Calibration Runbook
## Phase: Numerical Anchoring and Constant Calibration

## Purpose
This runbook defines the next execution step after theorem-shape stabilization.

The goal is to move from a restricted theorem draft to a calibrated restricted theorem result by anchoring:

\[
C_0,\quad V_0,\quad \lambda_0,\quad a_0,\quad b_0
\]

and then checking the empirical remainder against the theorem-controlled bound across the screened family.

---

## 1. Freeze one baseline example

Choose one concrete baseline instance and hold it fixed.

Required baseline objects:
- latent target probability vector \(q\)
- baseline score vector \(p_b\)

Then compute the fixed residual:
\[
r = q - p_b
\]

and the baseline geometry:
\[
C_0 = \mathrm{Cov}(p_b, r)
\]
\[
V_0 = \mathrm{Var}(r)
\]

These are the first two anchor constants.

---

## 2. Choose one reference corrected setting

Pick one reference screened parameter point:
\[
\theta_0 = (\alpha_0,\beta_0,\nu_0)
\]

Let the corrected score at that point be \(p_{c,0}\).

Define:
\[
\delta_0 = p_{c,0} - p_b
\]

Project the update onto the residual direction:
\[
\lambda_0 = \frac{\mathrm{Cov}(\delta_0, r)}{\mathrm{Var}(r)}
\]

Then define the residual-orthogonal innovation by construction:
\[
\xi_0 = \delta_0 - \lambda_0 r
\]

This makes
\[
\mathrm{Cov}(\xi_0, r)=0
\]
by design.

This is the preferred definition and should be used consistently.

---

## 3. Compute anchored theorem coefficients

After anchoring \(C_0,V_0,\lambda_0\), compute:

\[
a_0 = \frac{C_0 + V_0}{2C_0 + 2\lambda_0 V_0}
\]

\[
b_0 = \frac{\lambda_0^2 V_0 (C_0 + V_0)}{2(C_0 + \lambda_0 V_0)}
\]

These define the theoretical affine line:

\[
\Delta \mathrm{Cov} = a_0 \Delta \mathrm{Var} + b_0
\]

---

## 4. Build the empirical cloud on the screened family

For each screened parameter point \(\theta\), compute:
- corrected score \(p_{c,\theta}\)
- update:
\[
\delta_\theta = p_{c,\theta} - p_b
\]

- covariance change:
\[
\Delta \mathrm{Cov}_\theta = \mathrm{Cov}(q,p_{c,\theta}) - \mathrm{Cov}(q,p_b)
\]

- variance change:
\[
\Delta \mathrm{Var}_\theta = \mathrm{Var}(p_{c,\theta}) - \mathrm{Var}(p_b)
\]

This creates the empirical cloud.

---

## 5. Calibrate the gain term

At each screened point, compute:

\[
\lambda_\theta = \frac{\mathrm{Cov}(\delta_\theta, r)}{\mathrm{Var}(r)}
\]

Then measure gain drift:
\[
|\lambda_\theta - \lambda_0|
\]

This is the first control term in the theorem remainder.

---

## 6. Calibrate the innovation term

At each screened point, define the projected innovation:

\[
\xi_\theta = \delta_\theta - \lambda_\theta r
\]

Then measure innovation scale:
\[
\eta_{\nu,\theta} \approx \sqrt{\mathrm{Var}(\xi_\theta)}
\]

This is the second control term in the theorem remainder.

Note:
- using the projected definition makes \(\xi_\theta \perp r\) exact
- this removes ambiguity about orthogonality in the restricted theorem packet

---

## 7. Calibrate the curvature term

If the corrected family is explicitly parameterized by
\[
T_{\alpha,\beta}(x)=\sigma(\alpha x)^\beta
\]
then curvature may be estimated either:

### A. Analytically
via the second derivative
\[
T''_{\alpha,\beta}(x)=\beta\alpha^2u^\beta(1-u)\big[\beta-(\beta+1)u\big]
\]
with \(u=\sigma(\alpha x)\),

or

### B. Empirically
via local Taylor residuals of the residual-response map.

For the first calibration pass, either is acceptable, but the method should be stated explicitly.

Denote the resulting curvature proxy by:
\[
M_\theta
\]

This is the third control term in the theorem remainder.

---

## 8. Compute the observed remainder

For each screened point, compute the observed affine remainder:

\[
\epsilon_\theta = \Delta \mathrm{Cov}_\theta - a_0 \Delta \mathrm{Var}_\theta - b_0
\]

This is the quantity to compare against the predicted theorem bound.

---

## 9. Compare with the controlled theorem bound

The working restricted theorem bound is:

\[
|\epsilon_\theta|
\le
|a_0|V_0|\lambda_\theta-\lambda_0|^2
+
|1-2a_0|\sigma_p
\left(
\frac12 M_\theta \sqrt{\mathbb E[r^4]} + \eta_{\nu,\theta}
\right)
+
|a_0|
\left(
\frac12 M_\theta \sqrt{\mathbb E[r^4]} + \eta_{\nu,\theta}
\right)^2
\]

where
\[
\sigma_p = \sqrt{\mathrm{Var}(p_b)}.
\]

The calibration task is to test whether the observed \(|\epsilon_\theta|\) stays within the scale predicted by the right-hand side.

---

## 10. Required outputs

The calibration package should include:

### A. Baseline anchor table
- \(C_0\)
- \(V_0\)
- \(\lambda_0\)
- \(a_0\)
- \(b_0\)

### B. Affine overlay plot
- empirical cloud \((\Delta \mathrm{Var},\Delta \mathrm{Cov})\)
- theoretical line \(a_0\Delta \mathrm{Var}+b_0\)

### C. Control-term diagnostics
- \( |\lambda_\theta-\lambda_0| \)
- \( M_\theta \)
- \( \eta_{\nu,\theta} \)

### D. Remainder calibration plot
- observed \(|\epsilon_\theta|\)
- predicted theorem-bound magnitude

---

## 11. What counts as success

A successful first calibration pass would show:

1. the affine line overlays the empirical cloud reasonably well
2. the observed remainder is small relative to the raw cloud scale
3. the measured control terms explain where the remainder grows
4. the screened family is demonstrably a bounded-gain, bounded-curvature, bounded-innovation regime

That would convert the current theorem packet from:
- a strong restricted theorem draft

into:
- a calibrated restricted theorem result

---

## 12. Recommended execution order

1. Freeze baseline
2. Compute \(C_0,V_0\)
3. Choose reference point and compute \(\lambda_0\)
4. Compute \(a_0,b_0\)
5. Build empirical cloud
6. Measure \(\lambda_\theta,\eta_{\nu,\theta},M_\theta\)
7. Compute \(\epsilon_\theta\)
8. Compare observed remainder to predicted bound

This is now the shortest path forward.
