# COEFFICIENT_DERIVATION.md

# Coefficient Derivation
## Candidate derivation program for continuum memory coefficients from the retained-memory loading law

## Status
**Live derivation target. First coefficient-closure pass. Not yet microscopically closed.**

This file sits between:

```text
CHI_FIXED_POINT.md
```

and

```text
CONTINUUM_LIMIT.md
```

Its purpose is to attack the next seam:

> can the continuum scalar-density coefficient functions \(Z_R(\chi)\), \(V(R_{\mathrm{eff}};\chi,\varepsilon^*)\), and \(\lambda_{\mathrm{int}}(\chi)\) be derived or tightly constrained from the two-mode retained-memory recursion and the seam-2 loading fixed point?

This file does **not** claim that the coefficients are fully derived from the microscopic pruning law.

It establishes the first structured reduction:

\[
(\alpha_s,\alpha_f,\beta_s,\beta_f,c_s,c_f,\mu_G,\overline I_*^{(s)},\overline I_*^{(f)})
\quad\Rightarrow\quad
(a,b)
\quad\Rightarrow\quad
(\Lambda_*,\chi_*,R_*,m_R^2,Z_R,\lambda_{\mathrm{int}},V).
\]

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

`CHI_FIXED_POINT.md` reduced the bridge coefficient \(\chi\) to a stable loading fixed point:

\[
\Lambda_{n+1}=a\Lambda_n+b,
\]

\[
\Lambda_*=\frac{b}{1-a},
\]

\[
\chi_*=\frac{1}{1+\Lambda_*}
=
\frac{1-a}{1-a+b}.
\]

`CONTINUUM_LIMIT.md` introduced the minimal scalar-density memory action:

\[
S_{\mathrm{mem}}^{(A)}
=
\int d^4x\,\sqrt{-g}
\left[
-\frac{1}{2}Z_R(\chi)
\nabla_\mu R_{\mathrm{eff}}\nabla^\mu R_{\mathrm{eff}}
-
V(R_{\mathrm{eff}};\chi,\varepsilon^*)
+
\lambda_{\mathrm{int}}(\chi)R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
\right].
\]

The remaining question is:

> are \(Z_R\), \(V\), and \(\lambda_{\mathrm{int}}\) arbitrary effective-field placeholders, or can they be forced by the same loading law that fixed \(\chi\)?

This file attacks that question.

---

# 2. Inputs from the two-mode retained-memory recursion

## Definition 1
The two-mode retained-memory magnitude at fine time \(t\) is:

\[
M_t
=
w_s R_t^{(s)}
+
w_f R_t^{(f)}.
\]

The two-mode recursion has the coarse-grained form:

\[
\overline M_{n+1}
\approx
a_M\overline M_n
+
b_{\mathrm{raw},n},
\]

where

\[
a_M
=
w_s\alpha_s c_s+w_f\alpha_f c_f,
\]

and

\[
b_{\mathrm{raw},n}
=
w_s\beta_s\overline I_n^{(s)}
+
w_f\beta_f\overline I_n^{(f)}.
\]

Here:

\[
\overline I_n^{(s)}
=
\frac{1}{|B_n|}\sum_{t\in B_n}|\xi_t|,
\]

\[
\overline I_n^{(f)}
=
\frac{1}{|B_n|}\sum_{t\in B_n}
|\xi_t|\Theta(|\xi_t|-\varepsilon^*).
\]

The geometry channel evolves as:

\[
\mathcal G_{n+1}=\mu_G\mathcal G_n.
\]

Thus the loading ratio

\[
\Lambda_n=\frac{\mathcal M_n}{\mathcal G_n}
\]

obeys:

\[
\Lambda_{n+1}
\approx
a\Lambda_n+b_n,
\]

with

\[
a
=
\frac{w_s\alpha_s c_s+w_f\alpha_f c_f}{\mu_G},
\]

and

\[
b_n
=
\frac{
w_s\beta_s\overline I_n^{(s)}
+
w_f\beta_f\overline I_n^{(f)}
}
{\mu_G\mathcal G_n}.
\]

In the stationary regime:

\[
b_n\to b.
\]

---

# 3. First closure map to continuum memory field

## Definition 2
At first pass, identify the continuum memory field with the coarse-grained loading ratio:

\[
R_{\mathrm{eff}}(x)
\sim
\Lambda(x).
\]

The stationary value is:

\[
R_*
=
\Lambda_*
=
\frac{b}{1-a}.
\]

## Assumption 1
The scalar-density memory field is the continuum representation of local retained-memory loading, not a new independent microscopic degree of freedom.

This assumption is central. If it fails, the scalar-density class is probably not the correct continuum memory sector.

## Failure condition 1
If no covariant coarse-graining map produces a scalar \(R_{\mathrm{eff}}\sim\Lambda\), then this coefficient derivation route fails and `CONTINUUM_LIMIT.md` must pivot toward a nonlocal kernel or stress-like memory sector.

---

# 4. Potential coefficient from fixed-point loading

## Definition 3
The first candidate scalar-memory potential is:

\[
V(R)
=
\frac{1}{2}m_R^2(R-R_*)^2
-
\frac{1}{2}m_R^2R_*^2.
\]

This enforces:

\[
V(0)=0.
\]

It also enforces:

\[
V'(R_*)=0.
\]

## Lemma candidate 1
If

\[
m_R^2>0,
\]

then \(R_*\) is a stable stationary point of the memory potential.

### Proof sketch
Differentiate:

\[
V'(R)=m_R^2(R-R_*).
\]

Therefore:

\[
V'(R_*)=0.
\]

Second derivative:

\[
V''(R)=m_R^2.
\]

So \(R_*\) is stable if \(m_R^2>0\).

---

# 5. Stiffness from loading-map stability

## Definition 4
The candidate stiffness is:

\[
m_R^2
=
\mu_R^2(1-a),
\]

where \(\mu_R\) is the coarse-grained memory scale.

## Rationale
The loading perturbation satisfies:

\[
\delta\Lambda_{n+1}=a\,\delta\Lambda_n.
\]

Thus:

- \(a\to1\): marginal fixed point, soft memory mode;
- \(a\ll1\): strongly attractive fixed point, stiff memory mode.

So the minimal stability-compatible continuum identification is:

\[
m_R^2\propto 1-a.
\]

## Derivation target A
Derive \(\mu_R\) from microscopic time/block scale data, rather than treating it as an external scale.

Possible route:

\[
\mu_R\sim \frac{1}{\ell_{\mathrm{cg}}},
\]

where \(\ell_{\mathrm{cg}}\) is the coarse-graining length/time scale of the retained-memory block.

## Failure condition 2
If the microscopic recursion implies a stiffness that does not scale with \(1-a\), then this potential remains only a stability-matched ansatz.

---

# 6. Kinetic coefficient from bridge overlap

## Definition 5
The first candidate kinetic coefficient is:

\[
Z_R(\chi)
=
Z_0\chi(1-\chi).
\]

## Rationale
The gradient cost for \(R_{\mathrm{eff}}\) should be largest when geometry and retained memory are genuinely mixed and should vanish at pure endpoints:

\[
\chi=0
\quad\text{or}\quad
\chi=1.
\]

The simplest endpoint-safe overlap envelope is:

\[
\chi(1-\chi).
\]

## Derivation target B
Derive \(Z_0\) and the \(\chi(1-\chi)\) envelope from the covariance or block-rescaling behavior of the loading field:

\[
\Lambda_n(x)
\to
\Lambda_{n+1}(x).
\]

Possible microscopic interpretation:

\[
Z_0
\sim
\ell_{\mathrm{cg}}^2
\mathrm{Var}(\nabla\Lambda),
\]

or the continuum limit of nearest-block loading mismatch:

\[
\sum_{\langle ij\rangle}
\kappa_R
(\Lambda_i-\Lambda_j)^2
\to
\int d^4x\sqrt{-g}
Z_R(\chi)\nabla_\mu R\nabla^\mu R.
\]

## Failure condition 3
If retained-memory gradients do not coarse-grain to a local quadratic gradient penalty, the scalar-density kinetic term is not microscopically justified and Class C should be revisited.

---

# 7. Matter-memory coupling from overlap envelope

## Definition 6
The first conservative matter-memory coupling is:

\[
\lambda_{\mathrm{int}}(\chi)
=
\lambda_0\chi(1-\chi).
\]

## Rationale
The memory field should not couple uncontrollably at pure endpoints. A symmetric overlap coupling:

\[
\chi(1-\chi)
\]

makes the interaction strongest only in the mixed bridge regime.

## Alternative candidate
If the microscopic law shows that matter couples to retained-memory load but not to geometry-memory overlap, then the candidate becomes:

\[
\lambda_{\mathrm{int}}(\chi)
=
\lambda_0(1-\chi).
\]

## Derivation target C
Determine whether the matter-memory coupling is overlap-controlled:

\[
\chi(1-\chi),
\]

or load-controlled:

\[
1-\chi.
\]

This requires specifying \(\mathcal O_{\mathrm{mat}}\) and deriving how matter variables enter the retained-memory recursion.

## Failure condition 4
If no microscopic matter-memory coupling exists, then \(\lambda_{\mathrm{int}}\) should be set to zero in the first continuum limit.

---

# 8. Full CL-2 coefficient map

## Definition 7
The CL-2 coefficient map is:

\[
a
=
\frac{w_s\alpha_s c_s+w_f\alpha_f c_f}{\mu_G},
\]

\[
b
=
\frac{
w_s\beta_s\overline I_*^{(s)}
+
w_f\beta_f\overline I_*^{(f)}
}
{\mu_G\mathcal G_*},
\]

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
\lambda_{\mathrm{int}}(\chi)=\lambda_0\chi(1-\chi),
\]

and

\[
V(R)
=
\frac{1}{2}\mu_R^2(1-a)(R-R_*)^2
-
\frac{1}{2}\mu_R^2(1-a)R_*^2.
\]

This is the first full coefficient bridge from the retained-memory recursion to the scalar-density continuum action.

---

# 9. What this file currently proves

### Established at current proof level

1. \(a,b\) are inherited from the seam-2 loading reduction.
2. \(R_*\) is identified with the stable retained-memory loading fixed point.
3. The potential \(V\) is forced to have a stationary point at \(R_*\).
4. The subtraction term enforces \(V(0)=0\), preserving weak-memory decoupling.
5. The stiffness \(m_R^2\propto1-a\) matches loading-map stability.
6. \(Z_R\) and \(\lambda_{\mathrm{int}}\) are given endpoint-safe bridge-overlap forms.
7. The coefficient map is verifier-backed by `continuum_limit_verifier_v2.py`.

### Not yet proved

1. \(\mu_R,Z_0,\lambda_0\) are not derived from the microscopic law.
2. The \(\chi(1-\chi)\) envelope is symmetry-motivated, not uniquely forced.
3. \(R_{\mathrm{eff}}\sim\Lambda\) still needs an explicit covariant coarse-graining map.
4. \(\mathcal O_{\mathrm{mat}}\) remains unspecified.
5. The scalar-density class may still fail if memory is fundamentally nonlocal.

---

# 10. Verifier status

The coefficient map is implemented in:

```text
continuum_limit_verifier_v2.py
```

with execution log:

```text
continuum_limit_verifier_v2_run.log
```

The verifier checks:

- \(0\le a<1\),
- \(b>0\),
- \(0<\chi<1\),
- \(V(0)=0\),
- \(V'(R_*)=0\),
- \(V''(R_*)>0\),
- finite \(Z_R\),
- finite \(\lambda_{\mathrm{int}}\),
- finite \(m_R^2\).

---

# 11. Failure modes

This coefficient route fails if:

1. \(a,b\) cannot be derived from the microscopic recursion without hidden phenomenological calibration;
2. \(R_{\mathrm{eff}}\sim\Lambda\) cannot be produced by a covariant coarse-graining map;
3. \(\mu_R,Z_0,\lambda_0\) remain permanently free knobs;
4. the \(\chi(1-\chi)\) envelope is contradicted by microscopic scaling;
5. \(V(0)=0\) requires an artificial subtraction not justified by vacuum normalization;
6. \(\mathcal O_{\mathrm{mat}}\) cannot be specified without overfitting;
7. the memory sector must be nonlocal, invalidating the scalar-density Class A.

---

# 12. Next derivation target

The next step is to attack the remaining scale constants:

\[
\mu_R,\qquad Z_0,\qquad \lambda_0.
\]

The most direct route is to define a block-scale discrete quadratic memory action:

\[
S_{\mathrm{mem}}^{\mathrm{disc}}
=
\sum_n
\left[
\frac{1}{2}K_R(\Lambda_{n+1}-\Lambda_n)^2
+
\frac{1}{2}K_\nabla\sum_{\langle ij\rangle}(\Lambda_i-\Lambda_j)^2
+
U(\Lambda_n)
\right],
\]

then take the continuum limit to identify:

\[
\mu_R^2,\qquad Z_0,\qquad V(R).
\]

This should become the next file:

```text
DISCRETE_MEMORY_ACTION.md
```

---

# Honest status line

> `COEFFICIENT_DERIVATION.md` gives the first structured coefficient-closure map from the seam-2 retained-memory loading law into the scalar-density continuum action. It ties \(V\), \(m_R^2\), \(Z_R\), and \(\lambda_{\mathrm{int}}\) to \(a,b,\chi\), but does not yet derive the remaining scale constants or the covariant coarse-graining map from the microscopic law.

**End of file.**
