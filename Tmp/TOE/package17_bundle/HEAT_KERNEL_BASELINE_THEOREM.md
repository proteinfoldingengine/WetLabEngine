# HEAT_KERNEL_BASELINE_THEOREM.md

# Heat Kernel Baseline Theorem
## Candidate theorem for separating graph discretization baseline from curvature signal

## Status
**Theorem-shaped baseline decomposition. Not yet proved.**

`HEAT_CURVATURE_STATUS_AND_NEXT_PROOF_OBLIGATIONS.md` identified the next decisive theorem:

\[
C_{\mathrm{raw}}
=
C_{\mathrm{flat\ baseline}}
+
C_{\mathrm{curvature}}
+
o(1).
\]

The current heat-kernel curvature route depends on subtracting a boundaryless flat-torus baseline.

This file makes that baseline correction explicit and states the proof obligations required before it can be treated as legitimate.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Assumption**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**
- **Closure status**

Nothing here should be interpreted as proving graph-to-continuum curvature convergence.

---

# 1. Continuum heat-kernel target

For a smooth compact boundaryless \(d\)-dimensional Riemannian manifold \((M,h)\), the heat trace satisfies:

\[
H(t)
=
\mathrm{Tr}(e^{-t\Delta_h})
\sim
(4\pi t)^{-d/2}
\left[
a_0+a_1t+a_2t^2+\cdots
\right],
\]

where:

\[
a_0=\int_M dV,
\]

and:

\[
a_1=\frac{1}{6}\int_M R\,dV.
\]

Thus:

\[
Y(t)
=
H(t)(4\pi t)^{d/2}
\sim
a_0+a_1t+a_2t^2+\cdots.
\]

The desired curvature coefficient is:

\[
C_{\mathrm{curv}}
=
6a_1
=
\int_M R\,dV.
\]

---

# 2. Graph heat coefficient

## Definition 1

For a graph \(\mathcal G_n\) approximating \(M\), let:

\[
L_n
\]

be the density-normalized graph Laplacian.

Define the graph heat trace:

\[
H_n(t)=\mathrm{Tr}(e^{-tL_n}).
\]

Define:

\[
Y_n(t)=H_n(t)(4\pi t)^{d/2}.
\]

Given a fixed admissible heat-window family \(\mathcal W_n\), define the raw graph coefficient:

\[
C_{\mathrm{raw},n}
=
6\widehat{A}_{1,n},
\]

where:

\[
Y_n(t)\approx \widehat{A}_{0,n}+\widehat{A}_{1,n}t
\]

over \(t\in\mathcal W_n\).

---

# 3. Observed problem

The raw graph coefficient contains a large graph discretization artifact.

Empirically:

```text
flat torus raw coefficient is large and negative
sphere raw coefficient is also large and negative
```

even though:

\[
\int_{T^2} R\,dV=0,
\]

and:

\[
\int_{S^2} R\,dV=8\pi>0.
\]

Therefore:

\[
C_{\mathrm{raw},n}
\]

cannot be interpreted directly as:

\[
\int R\,dV.
\]

---

# 4. Baseline decomposition ansatz

## Assumption 1

For a fixed graph construction rule, fixed density normalization, fixed spectral scale rule, and fixed heat-window rule, the raw graph coefficient admits the asymptotic decomposition:

\[
C_{\mathrm{raw},n}(M)
=
B_n(\mathcal R)
+
C_{\mathrm{curv}}(M)
+
E_n(M).
\]

Here:

- \(B_n(\mathcal R)\) is the universal graph-discretization baseline for the reference class \(\mathcal R\);
- \(C_{\mathrm{curv}}(M)=\int_M R\,dV\);
- \(E_n(M)\to0\) under refinement.

The reference class \(\mathcal R\) includes:

```text
dimension
sampling density rule
graph construction
kernel bandwidth rule
density normalization alpha
spectral scale rule
heat-window rule
```

---

# 5. Flat reference baseline

## Definition 2

Let \(F_d\) be a compact boundaryless flat reference geometry of the same dimension and comparable sampling/volume class.

For \(d=2\), use:

```text
flat torus
```

because:

\[
\int_{F_d} R\,dV=0.
\]

Define:

\[
C_{\mathrm{flat},n}
=
C_{\mathrm{raw},n}(F_d).
\]

Since:

\[
C_{\mathrm{curv}}(F_d)=0,
\]

the decomposition gives:

\[
C_{\mathrm{flat},n}
=
B_n(\mathcal R)+E_n(F_d).
\]

Thus, if:

\[
E_n(F_d)\to0,
\]

then:

\[
C_{\mathrm{flat},n}
\]

estimates the graph baseline.

---

# 6. Renormalized coefficient

## Definition 3

For a target geometry \(M\), define:

\[
C_{\mathrm{ren},n}(M)
=
C_{\mathrm{raw},n}(M)
-
C_{\mathrm{flat},n}.
\]

Then:

\[
C_{\mathrm{ren},n}(M)
=
C_{\mathrm{curv}}(M)
+
E_n(M)-E_n(F_d).
\]

If both error terms vanish:

\[
E_n(M)\to0,
\]

\[
E_n(F_d)\to0,
\]

then:

\[
C_{\mathrm{ren},n}(M)
\to
\int_M R\,dV.
\]

---

# 7. Baseline theorem candidate

## Theorem candidate 1

Let \(\mathcal G_n(M)\) be a sequence of graphs approximating a compact boundaryless \(d\)-manifold \(M\), and let \(L_n\) be the \(\alpha=1\) density-normalized graph Laplacian with universal spectral scale fixed by a flat reference \(F_d\).

Assume:

1. \(L_n\to\Delta_h\) spectrally on low modes;
2. the heat window \(\mathcal W_n\) satisfies:
   \[
   h_n^2\ll t\ll L_R^2;
   \]
3. the graph heat coefficient has a universal discretization baseline \(B_n(\mathcal R)\) depending only on graph rule and reference class, not curvature;
4. the flat reference is boundaryless and satisfies:
   \[
   \int_{F_d}R\,dV=0;
   \]
5. the coefficient-fit errors vanish:
   \[
   E_n(M)-E_n(F_d)\to0.
   \]

Then:

\[
C_{\mathrm{raw},n}(M)-C_{\mathrm{raw},n}(F_d)
\to
\int_M R\,dV.
\]

---

# 8. Proof sketch

Starting from the decomposition:

\[
C_{\mathrm{raw},n}(M)
=
B_n(\mathcal R)
+
\int_M R\,dV
+
E_n(M),
\]

and:

\[
C_{\mathrm{raw},n}(F_d)
=
B_n(\mathcal R)
+
0
+
E_n(F_d),
\]

subtract:

\[
C_{\mathrm{raw},n}(M)-C_{\mathrm{raw},n}(F_d)
=
\int_M R\,dV
+
E_n(M)-E_n(F_d).
\]

If:

\[
E_n(M)-E_n(F_d)\to0,
\]

then:

\[
C_{\mathrm{ren},n}(M)
\to
\int_M R\,dV.
\]

This proves the baseline theorem conditional on the decomposition and error-control assumptions.

---

# 9. What is not proved

The proof sketch is conditional.

The hard unproven pieces are:

1. \(L_n\to\Delta_h\);
2. the existence of a universal baseline \(B_n(\mathcal R)\);
3. curvature-independence of the baseline;
4. vanishing of \(E_n(M)-E_n(F_d)\);
5. correct heat-window scaling;
6. extension to \(d=3\);
7. robustness under irregular causal antichain graphs.

Therefore the theorem is not closed.

---

# 10. How current numerical results support the theorem candidate

The current best method:

```text
alpha=1 density normalization
flat-torus lambda1 spectral scaling
flat heat-coefficient baseline
sphere residual
small refinement ladder
```

produced:

```text
sphere residuals remained positive
separation improved across small refinement ladder
classification: NORMALIZED_REFINEMENT_PROMISING
```

This supports the possibility that:

\[
C_{\mathrm{raw}}
=
C_{\mathrm{flat\ baseline}}
+
C_{\mathrm{curvature}}
+
o(1).
\]

It does not prove it.

---

# 11. Failure modes

The baseline theorem fails if:

1. the baseline depends on curvature rather than graph construction alone;
2. the flat reference subtraction removes genuine curvature signal;
3. residuals do not converge under larger refinement;
4. negative curvature references give wrong sign;
5. 3D references fail;
6. spectral scaling must be tuned per geometry;
7. heat-window choices determine the outcome.

---

# 12. Immediate verifier target

The next verifier should test baseline universality.

File:

```text
HEAT_KERNEL_BASELINE_UNIVERSALITY_TEST.md
```

Goal:

Compare multiple flat boundaryless references or flat-like graph constructions:

```text
flat torus with different aspect ratios
different sample densities
different seeds
possibly product flat 3-torus
```

and ask whether:

\[
C_{\mathrm{flat},n}
\]

depends only on graph rule / dimension / sampling class, not geometry-specific artifacts.

---

# 13. Next proof target after universality

If baseline universality passes, next file:

```text
HEAT_CURVATURE_MAGNITUDE_TEST.md
```

Goal:

Check whether:

\[
C_{\mathrm{ren}}(S^2)
\]

approaches:

\[
8\pi.
\]

If baseline universality fails, next file:

```text
GRAPH_LAPLACIAN_BASELINE_FAILURE.md
```

---

# Honest status line

> `HEAT_KERNEL_BASELINE_THEOREM.md` states the conditional theorem needed to legitimize flat-reference heat-coefficient subtraction. It shows that the method would recover \(\int R\,dV\) if a universal graph baseline and vanishing residual error can be proved. Those conditions remain open.

**End of file.**
