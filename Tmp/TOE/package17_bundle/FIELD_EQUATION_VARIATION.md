# FIELD_EQUATION_VARIATION.md

# Field Equation Variation
## Candidate variational route from effective action to Einstein-like field equations

## Status
**Live derivation target. First variation-consistency pass. Not yet full GR-closed.**

`EINSTEIN_HILBERT_LIMIT.md` established a first verifier-backed action-convergence target for the geometric curvature-density sector.

This file attacks the next seam:

\[
\delta S_{\mathrm{eff}}=0
\quad\Rightarrow\quad
G_{\mu\nu}
=
8\pi
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right).
\]

This file does **not** prove the full Einstein equations from the microscopic law.

It organizes the variational target, the memory stress-energy contribution, the weak-memory decoupling statement, and the Bianchi-compatible conservation requirement.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Assumption**
- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**

Nothing here should be interpreted as a completed proof unless explicitly stated.

---

# 1. Goal of this file

The effective continuum action has the target form:

\[
S_{\mathrm{eff}}
=
S_{\mathrm{EH}}
+
S_{\mathrm{mat}}
+
S_{\mathrm{mem}}.
\]

The target field equation is:

\[
G_{\mu\nu}
=
8\pi
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right).
\]

This file asks:

> what exact variational conditions are needed for the scalar-density memory sector to enter the field equations without violating weak-memory GR recovery or Bianchi consistency?

---

# 2. Effective action

## Definition 1
The effective action is:

\[
S_{\mathrm{eff}}[g,\phi,R_{\mathrm{eff}}]
=
\frac{1}{16\pi G_N}
\int d^4x\sqrt{-g}R
+
S_{\mathrm{mat}}[g,\phi]
+
S_{\mathrm{mem}}[g,R_{\mathrm{eff}},\phi].
\]

For the scalar-density memory class:

\[
S_{\mathrm{mem}}
=
\int d^4x\sqrt{-g}
\left[
-\frac12 Z_R(\chi)
\nabla_\mu R_{\mathrm{eff}}\nabla^\mu R_{\mathrm{eff}}
-
V(R_{\mathrm{eff}})
+
\lambda_{\mathrm{int}}(\chi)R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
\right].
\]

## Assumption 1
The effective action is diffeomorphism invariant and all fields are varied consistently, including any metric dependence inside \(\mathcal O_{\mathrm{mat}}\).

---

# 3. Stress-energy definitions

## Definition 2
Matter stress-energy is:

\[
T_{\mu\nu}^{\mathrm{mat}}
=
-\frac{2}{\sqrt{-g}}
\frac{\delta S_{\mathrm{mat}}}{\delta g^{\mu\nu}}.
\]

Memory stress-energy is:

\[
T_{\mu\nu}^{\mathrm{mem}}
=
-\frac{2}{\sqrt{-g}}
\frac{\delta S_{\mathrm{mem}}}{\delta g^{\mu\nu}}.
\]

The scalar local contribution is:

\[
T_{\mu\nu}^{\mathrm{mem,local}}
=
Z_R
\left(
\nabla_\mu R_{\mathrm{eff}}\nabla_\nu R_{\mathrm{eff}}
-
\frac12 g_{\mu\nu}
\nabla^\rho R_{\mathrm{eff}}\nabla_\rho R_{\mathrm{eff}}
\right)
-
g_{\mu\nu}V(R_{\mathrm{eff}}).
\]

The interaction contribution depends on:

\[
\frac{\delta(\sqrt{-g}\mathcal O_{\mathrm{mat}})}
{\delta g^{\mu\nu}}.
\]

## Derivation target A
Specify \(\mathcal O_{\mathrm{mat}}\) and compute the exact interaction stress-energy tensor.

Until \(\mathcal O_{\mathrm{mat}}\) is fixed, the interaction term remains schematic.

---

# 4. Metric variation target

## Lemma candidate 1
If:

\[
\delta S_{\mathrm{EH}}
=
\frac{1}{16\pi G_N}
\int d^4x\sqrt{-g}
G_{\mu\nu}\delta g^{\mu\nu}
\]

up to sign convention and boundary terms, and:

\[
\delta S_{\mathrm{mat}}+\delta S_{\mathrm{mem}}
=
-\frac12
\int d^4x\sqrt{-g}
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right)
\delta g^{\mu\nu},
\]

then stationary variation gives:

\[
G_{\mu\nu}
=
8\pi G_N
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right).
\]

In units \(G_N=1\):

\[
G_{\mu\nu}
=
8\pi
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right).
\]

This is standard variational GR structure, conditional on the geometric sector having already reached the Einstein-Hilbert limit.

---

# 5. Weak-memory decoupling

## Definition 3
Let:

\[
R_{\mathrm{eff}}=\eta r(x),
\qquad
\eta\to0.
\]

The memory stress-energy decouples if:

\[
T_{\mu\nu}^{\mathrm{mem}}
=
O(\eta)
\quad\text{or smaller}.
\]

## Lemma candidate 2
If:

\[
V(0)=0,
\]

\[
Z_R(\chi)<\infty,
\]

\[
\lambda_{\mathrm{int}}(\chi)<\infty,
\]

and the matter operator remains finite, then:

\[
T_{\mu\nu}^{\mathrm{mem}}
=
O(\eta)
\quad\text{or}\quad
O(\eta^2).
\]

Therefore:

\[
G_{\mu\nu}
=
8\pi G_N T_{\mu\nu}^{\mathrm{mat}}
+
O(\eta).
\]

This is the weak-memory GR recovery statement.

## Failure condition 1
If \(V(0)\neq0\), the memory sector leaves an \(O(1)\) vacuum term and GR does not decouple without additional cancellation.

---

# 6. Bianchi compatibility and exchange current

## Definition 4
The contracted Bianchi identity requires:

\[
\nabla^\mu G_{\mu\nu}=0.
\]

Therefore the total source must satisfy:

\[
\nabla^\mu
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right)
=
0.
\]

If the memory interaction is nonzero, separate conservation is not required. Instead:

\[
\nabla^\mu T_{\mu\nu}^{\mathrm{mat}}=Q_\nu,
\]

\[
\nabla^\mu T_{\mu\nu}^{\mathrm{mem}}=-Q_\nu.
\]

## Lemma candidate 3
If \(S_{\mathrm{eff}}\) is diffeomorphism invariant and all fields satisfy their equations of motion, then the total stress-energy is covariantly conserved on shell.

This is a standard Noether identity, but the exact exchange current \(Q_\nu\) must still be derived once \(\mathcal O_{\mathrm{mat}}\) is fixed.

## Failure condition 2
If \(Q_\nu\) is singular, noncovariant, or not suppressed/controlled in the weak-memory regime, the continuum-limit field equation fails.

---

# 7. Verifier implementation

## Status
**Implemented as `field_equation_variation_verifier.py`. Execution log captured.**

The verifier tests a symbolic/proxy version of the scalar-density variation.

It checks:

1. memory stress-energy scaling under:
   \[
   R_{\mathrm{eff}}=\eta r;
   \]

2. absence of \(O(1)\) memory residue when:
   \[
   V(0)=0;
   \]

3. interaction exchange current scaling:
   \[
   Q_\nu=O(\eta);
   \]

4. hard failure when:
   \[
   V(0)\neq0
   \]
   or coefficients are singular.

## Captured verifier output

```text
Field equation variation verifier
==================================================
Symbolic proxy:
Tmem_general: eta**2*(ZR*dr2/2 + r**2*v2/2) + eta*(Tmat*lam*r + r*v1) + v0
Tmem_with_V0_zero: eta**2*(ZR*dr2/2 + r**2*v2/2) + eta*(Tmat*lam*r + r*v1)
Q_exchange_proxy: eta*(Tmat*lam + divT*lam*r)

Sweep results:
PASS: 95.1
SOFT_FAIL: 0.0
HARD_FAIL: 4.9
leading_order_median: 1.0
fraction_Oeta: 100.0
fraction_Oeta2: 0.0
fraction_Q_Oeta: 100.0
```

---

# 8. What this file establishes

### Established at current proof level

1. The target field equation is explicitly tied to the effective action variation.
2. The memory stress-energy definition is explicit.
3. Weak-memory decoupling conditions are restated in variational form.
4. Bianchi compatibility is phrased as total conservation, not separate conservation.
5. A verifier checks the stress-energy scaling and exchange-current order.

### Not yet proved

1. Full Einstein-Hilbert variation from the discrete geometric sector remains conditional.
2. Boundary terms are not handled.
3. \(\mathcal O_{\mathrm{mat}}\) is not specified.
4. The exact \(Q_\nu\) is not derived.
5. The memory equation of motion is not fully analyzed.
6. Covariant conservation is not derived from the microscopic action.

---

# 9. Theorem candidate

## Theorem candidate 1
Suppose:

1. \(S_{\mathrm{geom}}^{\mathrm{disc}}\to S_{\mathrm{EH}}\);
2. the memory action is a diffeomorphism-invariant scalar density;
3. \(T_{\mu\nu}^{\mathrm{mem}}\) exists as a metric variation;
4. \(T_{\mu\nu}^{\mathrm{mem}}=O(\eta)\) in the weak-memory regime;
5. the total stress-energy is covariantly conserved on shell.

Then:

\[
G_{\mu\nu}
=
8\pi G_N
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right)
\]

and:

\[
G_{\mu\nu}
=
8\pi G_NT_{\mu\nu}^{\mathrm{mat}}
+
O(\eta)
\]

in the weak-memory regime.

This theorem is **not yet proved**, because its first and fifth assumptions remain open at microscopic/discrete level.

---

# 10. Updated proof-chain status

The continuum chain now becomes:

```text
EINSTEIN_HILBERT_LIMIT.md
        ↓
FIELD_EQUATION_VARIATION.md
        ↓
CONTINUUM_LIMIT.md
```

The next remaining hard seam is the fully integrated final check:

```text
CONTINUUM_LIMIT_CLOSURE_STATUS.md
```

Its job is to audit every seam and state what is closed, verifier-backed, conditional, or still open.

---

# Honest status line

> `FIELD_EQUATION_VARIATION.md` gives the first verifier-backed variational consistency pass from effective action to Einstein-like field equations with a controlled memory stress-energy sector. It does not prove the full field equations from the microscopic law, because Einstein-Hilbert convergence, matter coupling, exact exchange current, and microscopic conservation remain open.

**End of file.**
