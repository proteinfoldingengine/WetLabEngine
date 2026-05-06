# MEMORY_STRESS_PROJECTION.md

# Memory Stress Projection
## Projecting scalar-density memory stress-energy onto causal ADM slices

## Status
**Live derivation target. First projected memory-source pass. Not exact \(T_{\mu\nu}^{\mathrm{mem}}\) closure.**

`CAUSAL_ADM_FIELD_EQUATION_PROXY.md` used a generic weak-memory source:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
=
O(\eta_{\mathrm{mem}}).
\]

This file attacks the next seam:

\[
T_{\mu\nu}^{\mathrm{mem}}
\longmapsto
\mathcal S_{ab}^{\mathrm{mem},k}.
\]

The goal is to replace the generic weak-memory source with a projected source from the scalar-density memory action introduced in `CONTINUUM_LIMIT.md`.

This file does **not** derive the exact memory stress tensor from the microscopic pruning law. It performs the first ADM-slice projection of the candidate scalar-density memory stress tensor.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Lemma candidate**
- **Derivation target**
- **Failure condition**

Nothing here should be interpreted as a completed proof unless explicitly stated.

---

# 1. Starting memory action

The scalar-density candidate from `CONTINUUM_LIMIT.md` is:

\[
S_{\mathrm{mem}}^{(A)}
=
\int d^4x\,\sqrt{-g}
\left[
-\frac12 Z_R(\chi)\nabla_\mu R_{\mathrm{eff}}\nabla^\mu R_{\mathrm{eff}}
-
V(R_{\mathrm{eff}};\chi,\varepsilon^*)
+
\lambda_{\mathrm{int}}(\chi)R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
\right].
\]

The weak-memory regime is:

\[
R_{\mathrm{eff}}
=
\eta_{\mathrm{mem}}r,
\qquad
\eta_{\mathrm{mem}}\ll1.
\]

---

# 2. Spatial ADM projection

## Definition 1
Let \(h_{ab}^{(k)}\) be the spatial metric proxy on causal slice \(k\).

The spatial memory source is the projection:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
=
h_a^{\ \mu}
h_b^{\ \nu}
T_{\mu\nu}^{\mathrm{mem}}.
\]

In the first slice-level approximation:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
\approx
Z_R
\partial_aR_{\mathrm{eff}}\partial_bR_{\mathrm{eff}}
-
\frac12h_{ab}Z_R
|\nabla R_{\mathrm{eff}}|_h^2
+
h_{ab}V(R_{\mathrm{eff}})
-
\lambda_{\mathrm{int}}R_{\mathrm{eff}}T_{ab}^{\mathrm{mat}}.
\]

---

# 3. Weak-memory scaling

## Lemma candidate 1
If:

\[
R_{\mathrm{eff}}=\eta_{\mathrm{mem}}r,
\]

and:

\[
\nabla_a R_{\mathrm{eff}}
=
O(\eta_{\mathrm{mem}}),
\]

then:

- kinetic terms scale as:
  \[
  O(\eta_{\mathrm{mem}}^2);
  \]

- if \(V(0)=V'(0)=0\), potential terms scale as:
  \[
  O(\eta_{\mathrm{mem}}^2);
  \]

- interaction terms scale as:
  \[
  O(\eta_{\mathrm{mem}}).
  \]

Thus:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
=
O(\eta_{\mathrm{mem}})
\]

when interaction dominates, and:

\[
O(\eta_{\mathrm{mem}}^2)
\]

when interaction is absent or suppressed.

---

# 4. Projection verifier

## Status
**Implemented as `memory_stress_projection_verifier.py`. Execution log captured.**

The verifier constructs:
- positive-definite slice metrics \(h_{ab}^{(k)}\);
- weak memory fields \(R_{\mathrm{eff}}=\eta r\);
- weak spatial gradients \(\nabla_aR_{\mathrm{eff}}\);
- bounded matter stress proxy \(T_{ab}^{\mathrm{mat}}\);
- projected source \(\mathcal S_{ab}^{\mathrm{mem},k}\).

It checks:

1. finite projected source;
2. source norm remains small in weak-memory regime;
3. total source scales as \(O(\eta)\) when interaction dominates;
4. kinetic component scales as \(O(\eta^2)\);
5. halving \(\eta\) produces the expected scaling.

## Captured verifier output

```text
Memory stress projection verifier
==================================================
Route:
scalar-density T_mu_nu^mem -> ADM spatial projection S_ab^mem,k
Checks weak-memory scaling and finite projected source.

PASS: 85.66666666666667
SOFT_FAIL: 14.333333333333334
HARD_FAIL: 0.0
source_norm_median_median: 0.0003134972927777605
source_half_norm_median_median: 0.00013925493045850685
scaling_ratio_median: 0.49841653538789676
kinetic_order_ratio_median: 0.24999998279915903
finite_fraction_median: 1.0
small_source_fraction_median: 1.0
```

---

# 5. What this file establishes

### Established at current proof level

1. The generic weak-memory source is replaced by a projected scalar-density source.
2. The ADM spatial projection is explicit.
3. Weak-memory scaling is tested.
4. The source remains finite and small in sampled regimes.
5. Interaction and kinetic scaling separate correctly.

### Not yet proved

1. \(Z_R,V,\lambda_{\mathrm{int}}\) are still not microscopically derived.
2. The exact matter operator \(\mathcal O_{\mathrm{mat}}\) remains open.
3. Full spacetime projection is not implemented.
4. Lapse/normal projection terms are not included.
5. Conservation / \(Q_\nu\) exchange is not recomputed in ADM form.
6. This is still not exact \(T_{\mu\nu}^{\mathrm{mem}}\) closure.

---

# 6. Integration into field-equation proxy

The prior proxy equation:

\[
\mathcal E_{ab}^{(k)}
=
\mathcal S_{ab}^{\mathrm{mem},k}
\]

can now use the projected source:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
=
h_a^{\ \mu}h_b^{\ \nu}
T_{\mu\nu}^{\mathrm{mem}}.
\]

This strengthens `CAUSAL_ADM_FIELD_EQUATION_PROXY.md`.

---

# 7. Next derivation target

The next file should be:

```text
MEMORY_EXCHANGE_CURRENT_ADM.md
```

Its job:

\[
\nabla^\mu T_{\mu\nu}^{\mathrm{mem}}
=
-Q_\nu
\]

projected into ADM form, separating:
- normal energy exchange;
- spatial momentum exchange;
- weak-memory suppression.

---

# Honest status line

> `MEMORY_STRESS_PROJECTION.md` replaces the generic weak-memory source proxy with an explicit ADM spatial projection of the scalar-density memory stress tensor. It verifies the expected weak-memory scaling, but it does not yet derive the coefficients or prove full covariant conservation.

**End of file.**
