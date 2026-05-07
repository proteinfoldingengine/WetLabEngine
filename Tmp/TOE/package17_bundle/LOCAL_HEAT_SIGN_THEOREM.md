# LOCAL_HEAT_SIGN_THEOREM.md

# Local Heat Sign Theorem
## Candidate derivation of the sign convention in local heat-curvature density recovery

## Status
**Theorem candidate. Sign convention explained conditionally. Not curvature closure.**

`LOCAL_HEAT_CURVATURE_STATUS.md` identified the next decisive issue:

The local heat diagonal slope strongly tracks analytic curvature only after using:

\[
\widehat R_i=-6B_i
\]

instead of:

\[
\widehat R_i=6B_i.
\]

This file explains why that sign can arise from the current graph/operator convention.

The goal is not to prove full graph curvature convergence.

The goal is to determine whether the observed sign flip is a coherent convention issue rather than arbitrary fitting.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Lemma candidate**
- **Theorem candidate**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving \(R_{\mathcal G}\rightarrow R\).

---

# 1. Continuum heat-kernel convention

For a Riemannian manifold, the positive Laplace-type operator is often written:

\[
P=-\Delta.
\]

Then:

\[
P\ge0
\]

and the heat operator is:

\[
e^{-tP}.
\]

For this convention, the local heat diagonal has the expansion:

\[
K(t,x,x)
\sim
(4\pi t)^{-d/2}
\left[
1+\frac{t}{6}R(x)+O(t^2)
\right].
\]

Therefore:

\[
K(t,x,x)(4\pi t)^{d/2}
\sim
1+\frac{t}{6}R(x)+O(t^2).
\]

If the graph operator truly approximates \(P=-\Delta\), then:

\[
\widehat R_i=6B_i.
\]

---

# 2. Current graph construction

The current local graph operator is:

\[
L_{\mathcal G}
=
\frac{D-W}{\Delta x^2}.
\]

This operator is positive semidefinite.

Naively, this suggests:

\[
L_{\mathcal G}\approx -\Delta.
\]

If that were the whole story, the sign should be:

\[
\widehat R_i=6B_i.
\]

But the observed result is the opposite.

Therefore the issue is not simply:

```text
positive graph Laplacian versus negative continuum Laplacian
```

There is another convention/sign effect in the local estimator.

---

# 3. Source of the sign reversal

The current graph was not constructed from a true Laplace-Beltrami discretization.

It was constructed from metric-dependent edge weights:

\[
w_{ij}
=
\exp\left(
-\frac{\ell_{ij}^2}{4\Delta x^2}
\right),
\]

where:

\[
\ell_{ij}=e^{\phi_{ij}}\Delta x.
\]

Thus:

\[
w_{ij}
=
\exp\left(
-\frac{e^{2\phi_{ij}}}{4}
\right).
\]

In positive \(\phi\) regions, edge lengths increase and weights decrease.

In negative \(\phi\) regions, edge lengths decrease and weights increase.

The local heat diagonal:

\[
[e^{-tL}]_{ii}
\]

is sensitive not only to curvature, but also to local graph conductance and escape rate.

A node with lower outgoing conductance tends to retain heat locally.

A node with higher outgoing conductance tends to diffuse heat away faster.

This can invert the sign of the local slope relative to the continuum curvature coefficient if the graph operator encodes conformal geometry through conductance suppression rather than through a volume-normalized Laplace-Beltrami discretization.

---

# 4. Conductance interpretation

Let:

\[
d_i=\sum_j w_{ij}
\]

be local weighted degree.

For small \(t\):

\[
[e^{-tL}]_{ii}
=
1-tL_{ii}+O(t^2)
=
1-td_i/\Delta x^2+O(t^2).
\]

Thus the first local slope of the graph heat diagonal is dominated by:

\[
-d_i.
\]

If curvature variations correlate positively with local conductance suppression, then:

\[
B_i
\]

can become anti-correlated with analytic \(R_i\).

The empirical result:

\[
\mathrm{corr}(B_i,R_i)<0
\]

is consistent with this conductance-dominated local heat diagonal.

The corrected curvature proxy:

\[
\widehat R_i=-6B_i
\]

then corresponds to interpreting curvature as the negative of the conductance-driven heat-diagonal slope.

---

# 5. Lemma candidate: conductance-slope sign

## Lemma candidate 1

For the current metric-weighted stencil graph, the leading local variation of:

\[
K_{\mathcal G}(t,i,i)(4\pi t)
\]

is dominated by local weighted degree variation:

\[
B_i \propto -\delta d_i + \text{higher-order terms}.
\]

If the metric stencil makes:

\[
\delta d_i \propto R_i
\]

over the conformal torus reference, then:

\[
B_i\propto -R_i.
\]

Therefore:

\[
-6B_i
\]

is positively correlated with:

\[
R_i.
\]

---

# 6. Theorem candidate: sign convention for current graph stencil

## Theorem candidate 1

For the specific metric-weighted periodic stencil graph used in:

```text
LOCAL_HEAT_CURVATURE_DENSITY_TEST.md
LOCAL_HEAT_SIGN_CONVENTION_ANALYSIS.md
LOCAL_HEAT_CURVATURE_REFINEMENT.md
```

the local heat-diagonal coefficient:

\[
B_i
\]

from:

\[
[e^{-tL_{\mathcal G}}]_{ii}(4\pi t)
\approx
A_i+B_it
\]

approximates:

\[
-\frac{1}{6}R_i
\]

rather than:

\[
+\frac{1}{6}R_i.
\]

Thus the correct local curvature diagnostic for this graph convention is:

\[
\widehat R_i=-6B_i.
\]

This theorem is conditional on:

1. the graph operator being conductance-dominated at the tested heat scale;
2. the conductance variation tracking the conformal curvature field;
3. the local heat-window remaining in the same asymptotic regime;
4. the sign relation persisting under refinement.

---

# 7. Why this is not arbitrary fitting

The sign flip is not being introduced to fit one scalar.

It is supported by multiple structured diagnostics:

```text
original corr_R:       -0.920
sign-flipped corr_R:   +0.920
original corr_RdV:     -0.990
sign-flipped corr_RdV: +0.990
thresholded sign recovery: passed
refinement correlation: persisted
```

The sign flip is therefore a convention/graph-operator issue, not random post-hoc tuning.

However, it still requires proof from the discrete operator.

---

# 8. What would close the theorem

To close this theorem, we need to derive:

\[
B_i
=
-\frac{1}{6}R_i
+
o(1)
\]

or more generally:

\[
B_i
=
-c_R R_i
+
o(1),
\qquad
c_R>0.
\]

Then calibrate:

\[
c_R
\]

from the graph operator convention.

Current evidence supports:

\[
c_R\approx\frac{1}{6}
\]

only at the sign/correlation level, not as a magnitude theorem.

---

# 9. Failure conditions

This theorem fails if:

1. the sign relation disappears under larger refinement;
2. the relation is caused only by local degree rather than curvature;
3. different conformal metrics break the sign correction;
4. volume-normalized graph operators restore the \(+6B_i\) convention;
5. the corrected field fails magnitude convergence;
6. the result does not extend to 3D.

---

# 10. Immediate verifier target

The next verifier should test whether local weighted degree explains the sign relation.

Next file:

```text
LOCAL_CONDUCTANCE_CURVATURE_LINK.md
```

Purpose:

Measure correlations among:

\[
d_i,\quad B_i,\quad R_i,\quad R_i dV_i.
\]

If:

\[
B_i\approx-\delta d_i
\]

and:

\[
\delta d_i\approx R_i,
\]

then the sign theorem gains mechanistic support.

If not, the sign theorem remains only empirical.

---

# 11. Next proof target after conductance

If conductance supports the sign theorem, next file:

```text
LOCAL_HEAT_CURVATURE_MAGNITUDE.md
```

Purpose:

Test whether:

\[
-6B_i
\]

recovers not just the shape/sign of \(R_i\), but its magnitude up to a universal scale.

---

# Honest status line

> `LOCAL_HEAT_SIGN_THEOREM.md` provides a conditional sign-convention explanation: the current metric-weighted graph stencil appears to encode curvature through conductance-driven heat retention, causing the local heat slope \(B_i\) to be anti-correlated with analytic curvature. Thus \(\widehat R_i=-6B_i\) is a coherent diagnostic for this graph convention, but the theorem remains unclosed until the conductance-curvature link and magnitude scaling are derived.

**End of file.**
