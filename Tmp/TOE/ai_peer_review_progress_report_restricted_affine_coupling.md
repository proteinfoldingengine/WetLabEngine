# AI Peer Review Progress Report
## Restricted Affine Coupling Program — Current Status

## Purpose
This report is intended for AI peer review.

It summarizes the current state of the restricted affine coupling program after empirical cleanup, theorem-shape reduction, operational separation, and derivation work.

The goal is not to claim universal closure. The goal is to present the strongest current restricted result, the theorem shape now reached, the current operational structure, and the remaining proof gap in a form suitable for scrutiny.

---

## 1. Executive Summary

The project has progressed meaningfully.

The most important development is that the work now has a coherent restricted theorem shape:

\[
\Delta \mathrm{Cov} = a_0 \,\Delta \mathrm{Var} + b_0 + \epsilon
\]

with:
- \(a_0\) and \(b_0\) arising from baseline residual geometry
- \(\epsilon\) reduced to explicit control terms

The strongest current claim is still **restricted**, not universal. But it is now substantially cleaner, narrower, and more honest than earlier stages.

The most important remaining gap is no longer “what is the theorem shape?” It is now:

> validating the size of the controlling constants on the screened validity region.

That is a much narrower and more credible remaining problem.

---

## 2. Strongest Current Restricted Result

The strongest current object is a **restricted covariance–variance coupling draft**.

### Restricted theorem draft
\[
\Delta \mathrm{Cov} = a \,\Delta \mathrm{Var} + \epsilon
\]

with a robust empirical slope band and bounded residual structure on the screened family.

### Current robust empirical slope band
The safest carry-forward band is:

\[
a \in [0.250,\ 0.307]
\]

A narrower descriptive sub-band exists, but it is not treated as the main robust bound.

### Interpretation
This remains the strongest restricted bridge object discovered so far.

It is stronger than:
- downstream certification rules
- screening heuristics
- pipeline defaults
- explanatory slope-origin stories

---

## 3. Exact Backbone

The exact restricted identity remains:

\[
-\Delta B = 2\Delta \mathrm{Cov} - \Delta \mathrm{Var} - \Delta \mathrm{Bias}^2
\]

This is exact and serves as the explicit algebraic backbone of the restricted program.

This identity was not the main unresolved issue.
The unresolved issue was why \(\Delta \mathrm{Cov}\) should become approximately affine in \(\Delta \mathrm{Var}\) in the restricted regime.

---

## 4. Minimal Derivation Program

The key reduction uses:

\[
r := q - p_b,\qquad \delta := p_c - p_b
\]

and the decomposition

\[
\delta = \lambda r + \xi
\]

where:
- \(\lambda r\) is the residual-directed correction component
- \(\xi\) is residual-orthogonal innovation

From this, the exact reduced system becomes

\[
\Delta \mathrm{Cov} = \lambda(C+V)+A
\]
\[
\Delta \mathrm{Var} = \lambda(2C+\lambda V)+B
\]

with:
- \(C = \mathrm{Cov}(p_b,r)\)
- \(V = \mathrm{Var}(r)\)
- \(A = \mathrm{Cov}(q,\xi)\)
- \(B = 2\mathrm{Cov}(p_b,\xi)+2\lambda\mathrm{Cov}(r,\xi)+\mathrm{Var}(\xi)\)

This was the first major reduction.

---

## 5. Fixed-Baseline Simplification

A major simplification then emerged:

in the restricted family under study, the **baseline generator is fixed**.

That means \(p_b\), \(q\), and therefore \(r\) are fixed across the family. So the baseline residual moments

\[
C_0 = \mathrm{Cov}(p_b,r),\qquad V_0=\mathrm{Var}(r)
\]

are fixed across the family, up to seed/sample noise.

This removes drift in \(C\) and \(V\) from the main theorem burden.

With fixed \(C_0,V_0\), the affine remainder reduces to:

\[
\Delta \mathrm{Cov}-a_0\Delta \mathrm{Var}-b_0
=
-a_0V_0(\lambda-\lambda_0)^2 + (A-a_0B)
\]

This was a major narrowing of the gap.

---

## 6. Theorem Shape Now Reached

The current restricted theorem shape is:

\[
\Delta \mathrm{Cov}
=
a_0\,\Delta \mathrm{Var}
+
b_0
+
\epsilon
\]

with
\[
a_0=\frac{C_0+V_0}{2C_0+2\lambda_0V_0}
\]
and
\[
b_0=\frac{\lambda_0^2V_0(C_0+V_0)}{2(C_0+\lambda_0V_0)}.
\]

These are not arbitrary fit parameters.
They arise from the baseline residual geometry.

This is the strongest current theorem shape.

---

## 7. Innovation Control

The innovation term was then reduced explicitly.

If the innovation is residual-orthogonal, the innovation contribution becomes controllable by:
- covariance leakage to \(p_b\)
- innovation variance

Under the fixed-baseline reduction, the affine error can be bounded by:

\[
|\epsilon|
\le
|a_0|V_0|\lambda-\lambda_0|^2
+
|1-2a_0|\,\sigma_p\,\eta_\xi
+
|a_0|\,\eta_\xi^2
\]

where:
- \(\sigma_p=\sqrt{\mathrm{Var}(p_b)}\)
- \(\eta_\xi=\sqrt{\mathrm{Var}(\xi)}\)

So the theorem is now controlled by:
1. gain drift
2. innovation size

This was another major narrowing.

---

## 8. Smooth-Response Closure Candidate

The next step was to assume the deterministic corrected family acts through a smooth response map to the baseline residual:

\[
\delta = h_\theta(r) + \nu_\theta
\]

with
\[
h_\theta(0)=0,\qquad \lambda_\theta=h_\theta'(0).
\]

Taylor expansion gives

\[
h_\theta(r)=\lambda_\theta r + \rho_\theta(r)
\]

with curvature-controlled remainder.

This yields the explicit innovation-size bound:

\[
\eta_{\xi,\theta}
\le
\frac12 M_\theta \sqrt{\mathbb E[r^4]} + \eta_{\nu,\theta}
\]

where:
- \(M_\theta\) is a curvature bound for the response map
- \(\eta_{\nu,\theta}\) is the residual-orthogonal innovation scale

Substituting this into the affine remainder yields:

\[
|\epsilon(\theta)|
\le
|a_0|V_0|\lambda_\theta-\lambda_0|^2
+
|1-2a_0|\,\sigma_p
\left(
\frac12 M_\theta\sqrt{\mathbb E[r^4]} + \eta_{\nu,\theta}
\right)
+
|a_0|
\left(
\frac12 M_\theta\sqrt{\mathbb E[r^4]} + \eta_{\nu,\theta}
\right)^2
\]

This is the most explicit theorem-level remainder bound reached so far.

---

## 9. Parameter-Controlled Theorem Shape

The family parameters were then made explicit as

\[
\theta=(\alpha,\beta,\nu)
\]

corresponding to:
- sharpen
- power
- noise scale

For the deterministic corrected family
\[
T_{\alpha,\beta}(x)=\sigma(\alpha x)^\beta
\]
the derivative structure is explicit:

\[
T'_{\alpha,\beta}(x)=\beta\alpha\,u^\beta(1-u),
\qquad u=\sigma(\alpha x)
\]

and

\[
T''_{\alpha,\beta}(x)=\beta\alpha^2u^\beta(1-u)\big[\beta-(\beta+1)u\big]
\]

This yields a mechanistic split:

- sharpen/power primarily control gain and curvature
- noise scale primarily feeds innovation

This gave the current restricted theorem its parameter-level interpretation.

---

## 10. Conditional Restricted Closure

The restricted theorem is now closed in the following conditional sense:

if the screened parameter region keeps
- \(|\lambda_\theta-\lambda_0|\) small
- \(M_\theta\) small enough
- \(\eta_{\nu,\theta}\) small enough

then
\[
\Delta \mathrm{Cov}=a_0\Delta \mathrm{Var}+b_0+\epsilon
\]
with explicit remainder control.

So the theorem shape itself is no longer the unresolved issue.

The unresolved issue is now the **size of the controlling constants** on the screened family.

That is a calibration problem, not a form-discovery problem.

---

## 11. Domain Layer Separation

The domain side of the packet is now intentionally separated into three distinct objects:

### A. Theorem-validity region
Defined by the theorem-quality criteria themselves.

### B. Operational domain screens
Used to improve downstream certification behavior.

### C. Auxiliary family-validity heuristic
A weak family-screening clue, deliberately kept below theorem level.

This separation was important because earlier versions blurred these roles together.

---

## 12. Downstream Corollary Layer

The downstream Brier-sign layer is now treated as an official affine corollary family rather than a single tuned rule.

This was important because coverage and precision trade off continuously.

The family now has an operational reading:
- high-coverage = permissive
- balanced = softer structure-preserving alternative
- high-confidence = stricter alternative

The project no longer treats a single fitted downstream rule as “the answer.”

---

## 13. Operational Layer

The operational layer is now much cleaner than before.

### Preferred pipeline mode
Aggressive mode is the family-wide default pipeline mode.

### Hard operational default
The strongest current hard default is:

- aggressive mode
- high-coverage operating point

This default remained stronger on raw downstream utility across multiple randomized family banks.

### Softer interpretive alternative
A softer alternative remains:

- aggressive mode
- balanced operating point

This remains useful as a more selective / structure-preserving option, but it is no longer carried as the hard default.

---

## 14. Theorem–Utility Alignment

An important intermediate result was that theorem-valid families tend to produce better downstream certification behavior than theorem-invalid families.

This means theorem validity is not only structurally stronger, but operationally meaningful.

However, this alignment is not strong enough yet to fix a uniquely stable theorem-aligned operating point inside the affine family.

So the alignment result is kept, but weaker operational claims were demoted when they proved unstable.

---

## 15. What Was Demoted

Several things were intentionally weakened or demoted during this process:

- family-validity screening from raw parameters
- operating-point claims that were not stable enough
- over-strong interpretations of theorem-alignment defaults
- overly narrow slope-band readings

This is an important part of the progress.
The packet got stronger by losing weak claims.

---

## 16. Current Honest Status

### Closed enough to report
- exact backbone
- restricted affine theorem shape
- explicit remainder structure
- explicit role of gain drift, curvature, and innovation
- stable operational default
- clear layer separation

### Not yet universally closed
- full analytical proof beyond the restricted family
- analytical characterization of the empirical validity region
- stable theorem-alignment operating-point metric
- universal transfer beyond the current screened family

---

## 17. Strongest Current Claim

The strongest current claim is:

> In the restricted sigmoid-power corrected family with fixed baseline geometry, the covariance–variance relation admits an affine theorem shape
> \[
> \Delta \mathrm{Cov}=a_0\Delta \mathrm{Var}+b_0+\epsilon
> \]
> where \(a_0\) and \(b_0\) arise from baseline residual geometry, and \(\epsilon\) is explicitly controlled by gain drift, response curvature, and innovation scale.

That is the current best reportable theorem-level statement.

---

## 18. Remaining Proof Gap

The remaining proof gap is now narrow:

> show that the screened validity region actually keeps the controlling constants
> \[
> |\lambda_\theta-\lambda_0|,\quad M_\theta,\quad \eta_{\nu,\theta}
> \]
> small enough.

That is where the project still needs work.

But this is no longer the same as “discover the theorem.”
It is now “calibrate and verify the constants.”

---

## 19. Final Assessment

The progress is meaningful.

Not because universal closure has been reached.
It has not.

But because the work has advanced from:
- exploratory empirical pattern finding

to:
- a clean restricted theorem shape
- a mechanistic remainder bound
- a stable operational default
- and a much narrower proof gap

That is a legitimate improvement in scientific quality and peer-reviewability.

---

## 20. Request for AI Peer Review

The most useful review questions now are:

1. Is the affine theorem shape stated above mathematically coherent?
2. Is the reduction from the exact backbone to the residual-response form valid?
3. Is the fixed-baseline simplification legitimate for the restricted family?
4. Are the gain-drift / curvature / innovation controls the correct remaining variables?
5. Does the parameter-controlled theorem shape capture the real remaining gap?
6. Are there cleaner sufficient conditions that collapse the current remainder bound further?

These are the questions most likely to improve the program from here.
