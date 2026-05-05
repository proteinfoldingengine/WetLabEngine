# CONTINUUM_LIMIT_CL2_PATCH.md

# Patch CL-2
## Coefficient-function derivation target from the seam-2 loading fixed point

## Status
**Live derivation target. Verifier-backed candidate. Not yet microscopically closed.**

This patch adds the first coefficient-function derivation target to `CONTINUUM_LIMIT.md`.

The goal is to reduce the scalar-density coefficient functions

\[
Z_R(\chi),\qquad
V(R_{\mathrm{eff}};\chi,\varepsilon^*),\qquad
\lambda_{\mathrm{int}}(\chi)
\]

from arbitrary placeholders to explicit candidate functions tied to the seam-2 loading fixed point in `CHI_FIXED_POINT.md`.

This patch does **not** prove that the coefficient functions are derived from the microscopic pruning law. It establishes the first mathematically inspectable bridge:

\[
\text{two-mode loading map}
\quad\Rightarrow\quad
\text{scalar-density continuum coefficients}.
\]

---

# 26. Coefficient-function derivation target from retained-memory recursion

## Status
**Live derivation target. First coefficient ansatz tied to seam 2.**

Seam 2 reduced the bridge coefficient to a loading fixed point:

\[
\Lambda_{n+1}=a\Lambda_n+b,
\]

with stability condition

\[
0\le a<1,\qquad b>0.
\]

The fixed point is

\[
\Lambda_*=\frac{b}{1-a},
\]

and the bridge coefficient is

\[
\chi_*=\frac{1}{1+\Lambda_*}
=
\frac{1-a}{1-a+b}.
\]

The continuum scalar-density field is now identified at first pass as the coarse-grained loading amplitude:

\[
R_{\mathrm{eff}}\sim \Lambda.
\]

Thus the scalar memory action should possess a stable memory-loading equilibrium at

\[
R_*=\Lambda_*.
\]

---

## Definition 13
The first seam-2-tied scalar-memory potential is

\[
V(R_{\mathrm{eff}})
=
\frac{1}{2}m_R^2(\chi)
\left(R_{\mathrm{eff}}-R_*\right)^2
-
\frac{1}{2}m_R^2(\chi)R_*^2,
\]

where

\[
R_*=\Lambda_*=\frac{b}{1-a}.
\]

The subtraction is included so that

\[
V(0)=0.
\]

Therefore the weak-memory decoupling condition from the scalar-density verifier remains satisfied.

---

## Lemma candidate 3
The potential above satisfies:

\[
V(0)=0,
\]

\[
V'(R_*)=0,
\]

and

\[
V''(R_*)=m_R^2(\chi).
\]

Therefore, if

\[
m_R^2(\chi)>0,
\]

then \(R_*\) is a stable retained-memory loading equilibrium.

### Proof sketch
Direct differentiation gives:

\[
V'(R)=m_R^2(R-R_*),
\]

so

\[
V'(R_*)=0.
\]

Also,

\[
V''(R)=m_R^2.
\]

Thus the fixed point is stable if \(m_R^2>0\). The subtraction term makes \(V(0)=0\), preventing an \(O(1)\) cosmological-constant-like residue in the weak-memory limit.

---

# 27. Candidate stiffness from loading-map stability

## Definition 14
The first candidate memory stiffness is

\[
m_R^2(\chi)
=
\mu_R^2(1-a),
\]

where \(\mu_R\) is the coarse-grained memory scale.

## Interpretation
The loading-map perturbation satisfies

\[
\delta\Lambda_{n+1}=a\,\delta\Lambda_n.
\]

Thus:

- if \(a\to1\), the loading fixed point is marginal and the memory field should become soft;
- if \(a\ll1\), the loading fixed point is strongly attractive and the memory field should be stiff.

So

\[
m_R^2\propto 1-a
\]

is the minimal stability-compatible continuum identification.

## Failure condition 11
If the microscopic recursion implies a stiffness unrelated to \(1-a\), then this coefficient ansatz is only phenomenological and must be replaced.

---

# 28. Candidate kinetic coefficient

## Definition 15
The first candidate kinetic coefficient is

\[
Z_R(\chi)
=
Z_0\chi(1-\chi),
\]

where \(Z_0>0\).

## Interpretation
This coefficient:

- is finite at \(\chi\approx0.2667\);
- vanishes at pure-geometry and pure-memory endpoints;
- is largest in the mixed regime;
- uses only the bridge mixture structure and introduces no extra shape function.

This is an admissible first ansatz, not yet a microscopic derivation.

## Failure condition 12
If coarse-graining of the retained-memory recursion produces a different gradient penalty, then \(Z_R(\chi)=Z_0\chi(1-\chi)\) should be treated as a provisional regulator rather than a derived coefficient.

---

# 29. Candidate matter-memory coupling

## Definition 16
The first conservative matter-memory coupling is

\[
\lambda_{\mathrm{int}}(\chi)
=
\lambda_0\chi(1-\chi),
\]

where \(\lambda_0\ge0\).

## Interpretation
This coupling:

- shuts off at pure-geometry and pure-memory endpoints;
- is finite at \(\chi\approx0.2667\);
- suppresses uncontrolled coupling in the weak-memory limit;
- mirrors the same bridge-mixing envelope used by \(Z_R\).

A less conservative candidate would be

\[
\lambda_{\mathrm{int}}(\chi)=\lambda_0(1-\chi),
\]

but the symmetric envelope is safer for first-pass decoupling.

## Failure condition 13
If the microscopic matter-memory coupling scales only with retained-memory load and not with the geometry-memory overlap, then \(\lambda_0(1-\chi)\) may replace the symmetric candidate.

---

# 30. Updated scalar-density candidate after CL-2

Substituting the CL-2 coefficient candidates gives:

\[
S_{\mathrm{mem}}^{(A,\mathrm{CL2})}
=
\int d^4x\,\sqrt{-g}\,
\left[
-\frac{1}{2}Z_0\chi(1-\chi)
\nabla_\mu R_{\mathrm{eff}}\nabla^\mu R_{\mathrm{eff}}
-
\left(
\frac{1}{2}\mu_R^2(1-a)
(R_{\mathrm{eff}}-R_*)^2
-
\frac{1}{2}\mu_R^2(1-a)R_*^2
\right)
+
\lambda_0\chi(1-\chi)
R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
\right],
\]

with

\[
R_*=\frac{b}{1-a},
\qquad
\chi=\frac{1-a}{1-a+b}.
\]

This is the first explicit seam-2-to-seam-3 coefficient bridge.

---

# 31. Verifier v2 target

## Status
**Implemented as `continuum_limit_verifier_v2.py`. Execution log captured.**

Verifier v2 checks:

1. stable loading:
   \[
   0\le a<1,\qquad b>0;
   \]

2. bridge range:
   \[
   0<\chi<1;
   \]

3. finite positive kinetic coefficient:
   \[
   Z_R=Z_0\chi(1-\chi)>0;
   \]

4. finite matter coupling:
   \[
   \lambda_{\mathrm{int}}=\lambda_0\chi(1-\chi)\ge0;
   \]

5. positive stiffness:
   \[
   m_R^2=\mu_R^2(1-a)>0;
   \]

6. weak-memory decoupling:
   \[
   V(0)=0;
   \]

7. fixed-point stationarity:
   \[
   V'(R_*)=0;
   \]

8. stable potential curvature:
   \[
   V''(R_*)>0.
   \]

---

# 32. Verifier v2 captured output

```text
CL-2 symbolic coefficient derivation
==================================================
Lambda_star: -b/(a - 1)
chi: (1 - a)/(-a + b + 1)
Z_R: -Z0*b*(a - 1)/(-a + b + 1)**2
lambda_int: -b*lambda0*(a - 1)/(-a + b + 1)**2
m_R2: muR**2*(1 - a)
V0: 0
Vprime_at_Rstar: 0
Vsecond_at_Rstar: muR**2*(1 - a)
Tmem_expansion: eta*(-Tmat*b*lambda0*r*(a - 1)/(-a + b + 1)**2 - b**2*muR**2*(2*a*r/b - 2*r/b)/(2*(a - 1))) + eta**2*(-Z0*b*dr2*(a - 1)/(2*(-a + b + 1)**2) - b**2*muR**2*(a*r/b - r/b)**2/(2*(a - 1))) + O(eta**3)

CL-2 numerical sweep
==================================================
PASS: 99.191
SOFT_FAIL: 0.0
HARD_FAIL: 0.809
chi_min: 0.0005766938303031946
chi_median: 0.7935310738878313
chi_max: 0.9989839526125909
Lambda_min: 0.0010170807896883022
Lambda_median: 0.260190095771037
Lambda_max: 1733.0223658613684
Z_R_median: 0.05415588182140546
lambda_int_median: 0.005391396262720907
m_R2_median: 0.39301924878618466
```

---

# 33. Interpretation of CL-2

### Established at current proof level
- The scalar-density coefficients are no longer arbitrary placeholders.
- \(V\) is tied to the seam-2 loading fixed point.
- \(m_R^2\) is tied to loading-map stability.
- \(Z_R\) and \(\lambda_{\mathrm{int}}\) are tied to the geometry-memory overlap envelope.
- The verifier confirms that the CL-2 candidate satisfies the structural continuum checks for broad sampled parameter ranges.

### Not yet proved
- \(Z_0,\lambda_0,\mu_R\) are not derived from the microscopic pruning law.
- The \(\chi(1-\chi)\) envelope is symmetry-motivated, not uniquely forced.
- The scalar field \(R_{\mathrm{eff}}\sim\Lambda\) has not yet been produced by an explicit covariant coarse-graining map.
- The emergent metric and connection are still assumed.
- The matter-memory operator \(\mathcal O_{\mathrm{mat}}\) remains unspecified.

Therefore CL-2 does **not** close seam 3. It upgrades seam 3 from:

> admissible scalar-density candidate

to:

> scalar-density candidate with coefficients structurally tied to the seam-2 loading fixed point and verifier-backed for weak-memory decoupling.

---

# 34. Updated critical path

The next derivation target is now the microscopic coefficient link:

\[
(\alpha_s,\alpha_f,\beta_s,\beta_f,c_s,c_f,\mu_G,\overline I_*^{(s)},\overline I_*^{(f)})
\quad\Rightarrow\quad
(a,b)
\quad\Rightarrow\quad
(Z_R,V,\lambda_{\mathrm{int}}).
\]

The immediate next file should be:

```text
COEFFICIENT_DERIVATION.md
```

Its job:

1. derive \(a,b\) from the two-mode recursion,
2. derive \(R_*=\Lambda_*\),
3. derive or constrain \(Z_0,\lambda_0,\mu_R\),
4. determine whether the \(\chi(1-\chi)\) envelope is forced or merely admissible,
5. identify whether Class A survives microscopic closure or must yield to the nonlocal kernel Class C.

---

# Honest status line

> Patch CL-2 ties the first scalar-density continuum coefficients to the seam-2 loading fixed point and verifies their structural safety. This is not a derivation from the microscopic pruning law, but it is a real reduction in ambiguity: the continuum memory action is now connected to the fixed-point loading machinery rather than floating as an arbitrary effective field ansatz.

**End of patch.**
