# DISCRETE_MEMORY_ACTION.md

# Discrete Memory Action
## Candidate block-level action for deriving continuum memory coefficient scales

## Status
**Live derivation target. First discrete-action scale pass. Not yet covariantly closed.**

This file sits downstream of:

```text
COEFFICIENT_DERIVATION.md
```

and upstream of:

```text
CONTINUUM_LIMIT.md
```

Its purpose is to attack the next open seam:

> can the remaining continuum scale constants \(\mu_R\), \(Z_0\), and \(\lambda_0\) be derived or constrained from a block-level discrete memory action?

`COEFFICIENT_DERIVATION.md` tied the **shape** of the continuum memory coefficients to the seam-2 loading fixed point:

\[
R_*=\Lambda_*=\frac{b}{1-a},
\]

\[
\chi_*=\frac{1-a}{1-a+b},
\]

\[
m_R^2=\mu_R^2(1-a),
\]

\[
Z_R(\chi)=Z_0\chi(1-\chi),
\]

\[
\lambda_{\mathrm{int}}(\chi)=\lambda_0\chi(1-\chi).
\]

But it did not derive the remaining scale constants:

\[
\mu_R,\qquad Z_0,\qquad \lambda_0.
\]

This file provides the first discrete-action route for deriving or constraining them.

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

The goal is to propose a block-level discrete retained-memory action:

\[
S_{\mathrm{mem}}^{\mathrm{disc}}
\]

whose continuum scaling produces the coefficient scales used by the scalar-density memory action:

\[
S_{\mathrm{mem}}^{(A)}
=
\int d^4x\sqrt{-g}
\left[
-\frac12 Z_R(\chi)\nabla_\mu R_{\mathrm{eff}}\nabla^\mu R_{\mathrm{eff}}
-
V(R_{\mathrm{eff}})
+
\lambda_{\mathrm{int}}(\chi)R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
\right].
\]

This file does not yet prove a covariant continuum limit. It only supplies the first block-action mechanism for the remaining scalar-density coefficients.

---

# 2. Block variables

## Definition 1
Let \(B_n\) denote a coarse-grained memory block. Define the block retained-memory loading variable:

\[
\Lambda_n
=
\frac{\mathcal M_n}{\mathcal G_n}.
\]

For spatially resolved blocks, write:

\[
\Lambda_i^n
\]

where \(i\) labels a spatial/causal block and \(n\) labels the coarse-grained update step.

The continuum memory field is identified at first pass as:

\[
R_{\mathrm{eff}}(x_n,x_i)\sim \Lambda_i^n.
\]

## Assumption 1
\(\Lambda_i^n\) is the discrete precursor of the scalar field \(R_{\mathrm{eff}}\).

If this assumption fails, the scalar-density Class A route becomes suspect.

---

# 3. Prototype discrete memory action

## Definition 2
The first block-level discrete memory action is:

\[
S_{\mathrm{mem}}^{\mathrm{disc}}
=
\sum_n
\left[
\frac12 K_t(\Lambda_{n+1}-\Lambda_n)^2
+
U(\Lambda_n)
\right]
+
\sum_{n,\langle ij\rangle}
\frac12 K_x(\Lambda_i^n-\Lambda_j^n)^2
+
\sum_n
K_{\mathrm{int}}\Lambda_n\mathcal O_{\mathrm{mat},n}.
\]

Here:

- \(K_t\) is the time/update-direction memory inertia;
- \(K_x\) is the block-to-block gradient stiffness;
- \(K_U\) is the local potential stiffness hidden inside \(U\);
- \(K_{\mathrm{int}}\) is the discrete matter-memory coupling strength;
- \(\langle ij\rangle\) denotes adjacent coarse-grained blocks.

## Assumption 2
This is not yet the microscopic pruning law. It is an effective block action whose Euler-Lagrange / coarse-grained behavior should reproduce the stationary loading structure from seam 2.

---

# 4. Local potential around the retained-memory fixed point

## Definition 3
Let the loading fixed point be:

\[
\Lambda_*=\frac{b}{1-a}.
\]

Define the local block potential:

\[
U(\Lambda)
=
\frac12 K_U(\Lambda-\Lambda_*)^2
-
\frac12 K_U\Lambda_*^2.
\]

The subtraction enforces:

\[
U(0)=0.
\]

## Lemma candidate 1
The block potential satisfies:

\[
U'( \Lambda_*)=0,
\]

\[
U''(\Lambda_*)=K_U.
\]

Thus, if:

\[
K_U>0,
\]

\(\Lambda_*\) is a stable block-memory loading equilibrium.

---

# 5. Discrete-to-continuum coefficient map

## Definition 4
Let \(dt\) be the coarse-grained update scale and \(dx\) the block spacing scale.

At first pass, define the structural coefficient map:

\[
\mu_R^2=\frac{K_U}{K_t},
\]

\[
Z_0=\frac{K_x}{K_t}\left(\frac{dx}{dt}\right)^2,
\]

\[
\lambda_0=\frac{K_{\mathrm{int}}}{K_t}.
\]

Then:

\[
m_R^2=\mu_R^2(1-a).
\]

## Interpretation

- \(K_t\) normalizes memory inertia.
- \(K_U\) supplies the local restoring scale.
- \(K_x\) supplies the gradient/neighbor coherence penalty.
- \(K_{\mathrm{int}}\) supplies the matter-memory coupling scale.
- \(dt,dx\) carry the leading block-scale conversion between update and spatial variation.

This is a first structural map, not a full covariant derivation.

---

# 6. Positivity and stability conditions

## Lemma candidate 2
If:

\[
K_t>0,
\]

\[
K_U>0,
\]

\[
K_x\ge0,
\]

\[
K_{\mathrm{int}}\ge0,
\]

\[
dt>0,\qquad dx>0,
\]

and the seam-2 loading map satisfies:

\[
0\le a<1,\qquad b>0,
\]

then:

\[
\mu_R^2>0,
\]

\[
Z_0\ge0,
\]

\[
\lambda_0\ge0,
\]

\[
m_R^2>0,
\]

and:

\[
0<\chi_*<1.
\]

Thus the scalar-density coefficient map is structurally stable.

---

# 7. Relation to continuum action

Substituting the discrete-derived scale map into the CL-2 continuum coefficients gives:

\[
Z_R(\chi)
=
\frac{K_x}{K_t}\left(\frac{dx}{dt}\right)^2
\chi(1-\chi),
\]

\[
\lambda_{\mathrm{int}}(\chi)
=
\frac{K_{\mathrm{int}}}{K_t}
\chi(1-\chi),
\]

\[
m_R^2
=
\frac{K_U}{K_t}(1-a),
\]

and:

\[
V(R)
=
\frac12
\frac{K_U}{K_t}
(1-a)
(R-R_*)^2
-
\frac12
\frac{K_U}{K_t}
(1-a)
R_*^2.
\]

with:

\[
R_*=\frac{b}{1-a}.
\]

This is the first full block-action-to-continuum coefficient map.

---

# 8. Verifier implementation

## Status
**Implemented as `discrete_memory_action_verifier.py`. Execution log captured.**

The verifier checks:

1. seam-2 stability:
   \[
   0\le a<1,\qquad b>0;
   \]

2. action positivity:
   \[
   K_t>0,\qquad K_U>0,\qquad K_x\ge0,\qquad K_{\mathrm{int}}\ge0;
   \]

3. block-scale validity:
   \[
   dt>0,\qquad dx>0;
   \]

4. continuum scale finiteness:
   \[
   \mu_R^2,\quad Z_0,\quad \lambda_0,\quad m_R^2<\infty;
   \]

5. bridge admissibility:
   \[
   0<\chi_*<1.
   \]

## Captured verifier output

```text
Discrete memory action verifier
==================================================
Continuum scale map:
mu_R^2 = K_U / K_t
Z0     = (K_x / K_t) * (dx / dt)^2
lambda0= K_int / K_t
m_R^2  = mu_R^2 * (1-a)

Sweep results:
PASS: 98.988
SOFT_FAIL: 0.193
HARD_FAIL: 0.819
chi_median: 0.7908626513090353
mu_R2_median: 0.31698772999262315
Z0_median: 0.2995201010519064
lambda0_median: 0.0314293688446046
m_R2_median: 0.12218476761960194
chi_min: 0.0007198712317079496
chi_max: 0.9990001095950791
```

---

# 9. What this file establishes

### Established at current proof level

1. A concrete block-level memory action has been written.
2. The remaining continuum scales \(\mu_R^2,Z_0,\lambda_0\) are no longer floating symbols; they are mapped to discrete block constants.
3. The stability of \(m_R^2\) follows from both:
   \[
   K_U/K_t>0
   \]
   and:
   \[
   0\le a<1.
   \]
4. The gradient coefficient \(Z_R\) is tied to neighbor-block loading mismatch.
5. The matter coupling is tied to a discrete matter-memory loading term.
6. A verifier confirms structural stability for broad sampled parameter ranges.

### Not yet proved

1. \(K_t,K_U,K_x,K_{\mathrm{int}}\) are not yet derived from the microscopic pruning law.
2. The block action is not yet shown to be the unique effective action.
3. The continuum scaling is structural, not fully covariant.
4. \(dx,dt\) are not yet derived from a causal lattice geometry.
5. The matter operator \(\mathcal O_{\mathrm{mat}}\) remains unspecified.
6. Nonlocal memory effects may still require Class C.

---

# 10. Failure modes

This route fails if:

1. no block variable \(\Lambda_i^n\) can be derived from the microscopic law;
2. the block action does not reproduce the seam-2 loading recursion;
3. \(K_t,K_U,K_x,K_{\mathrm{int}}\) remain arbitrary knobs;
4. the continuum map for \(Z_0\) depends on noncovariant choices that cannot be removed;
5. \(K_x=0\) universally, eliminating local spatial/causal gradient structure;
6. the memory interaction cannot be represented by a local \(K_{\mathrm{int}}\Lambda\mathcal O_{\mathrm{mat}}\) term;
7. the true memory sector is fundamentally nonlocal.

---

# 11. Next derivation target

The next file should be:

```text
MICRO_TO_BLOCK_ACTION.md
```

Its job:

\[
\text{microscopic pruning / retained-memory recursion}
\quad\Rightarrow\quad
K_t,K_U,K_x,K_{\mathrm{int}}.
\]

That is the next real closure seam.

The required derivation targets are:

1. derive \(K_t\) from update-to-update retained-memory inertia;
2. derive \(K_U\) from fixed-point restoring curvature;
3. derive \(K_x\) from neighbor-block memory mismatch;
4. derive \(K_{\mathrm{int}}\) from matter-source loading;
5. prove or falsify locality of the block action.

---

# Honest status line

> `DISCRETE_MEMORY_ACTION.md` gives the first block-level action that maps the remaining continuum coefficient scales \(\mu_R,Z_0,\lambda_0\) to discrete memory-action constants. This is a real reduction in ambiguity, but not yet microscopic closure: the constants \(K_t,K_U,K_x,K_{\mathrm{int}}\), the block geometry, and the matter operator still need to be derived from the microscopic pruning law.

**End of file.**
