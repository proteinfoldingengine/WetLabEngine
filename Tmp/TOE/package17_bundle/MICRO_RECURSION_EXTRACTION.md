# MICRO_RECURSION_EXTRACTION.md

# Micro Recursion Extraction
## Extracting \(k_R\), \(D_R\), and \(\lambda_{\mathrm{micro}}\) from an explicit two-mode retained-memory recursion

## Status
**Extraction framework. Not production-recursion closure.**

`COEFFICIENT_MICRO_DERIVATION.md` reduced the memory-action coefficient problem to three microscopic quantities:

\[
k_R(\chi,\varepsilon^*),
\qquad
D_R(\chi,\varepsilon^*),
\qquad
\lambda_{\mathrm{micro}}(\chi,\varepsilon^*).
\]

This file defines how to extract those quantities from an explicit two-mode retained-memory recursion.

It does **not** claim the exact production recursion has already been supplied. It gives the extraction template and verifier.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Assumption**
- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**

Nothing here should be interpreted as final microscopic closure unless the actual recursion is substituted.

---

# 1. Required microscopic input

The exact recursion must supply update equations of the form:

\[
R_{n+1}=F_R(R_n,A_n,\mathcal O_n;\chi,\varepsilon^*)+\sigma_R\xi_n,
\]

\[
A_{n+1}=F_A(A_n,R_n;\chi,\varepsilon^*)+\sigma_A\zeta_n.
\]

Here:

- \(R_n\) is retained-memory/loading amplitude;
- \(A_n\) is the auxiliary adaptation/pruning mode;
- \(\mathcal O_n\) is the matter/operator input;
- \(\xi_n,\zeta_n\) are zero-mean fluctuations;
- \(\varepsilon^*\) is the pruning threshold;
- \(\chi\) is the fixed-point bridge/loading coefficient.

---

# 2. Local affine form near fixed point

## Definition 1
Linearize the recursion near the fixed point:

\[
R_n=R_*+\delta R_n,
\qquad
A_n=A_*+\delta A_n.
\]

The local affine form is:

\[
R_{n+1}
=
a_R R_n
+
b_R A_n
+
c_R\mathcal O_n
+
d_R
+
\sigma_R\xi_n,
\]

\[
A_{n+1}
=
a_A A_n
+
b_A R_n
+
d_A
+
\sigma_A\zeta_n.
\]

This is the minimal extraction form.

---

# 3. Fixed point

## Definition 2
With \(\mathcal O_n=0\), the fixed point satisfies:

\[
\begin{pmatrix}
R_*\\
A_*
\end{pmatrix}
=
\begin{pmatrix}
a_R & b_R\\
b_A & a_A
\end{pmatrix}
\begin{pmatrix}
R_*\\
A_*
\end{pmatrix}
+
\begin{pmatrix}
d_R\\
d_A
\end{pmatrix}.
\]

Thus:

\[
(I-M)
\begin{pmatrix}
R_*\\
A_*
\end{pmatrix}
=
d.
\]

The fixed point exists if:

\[
\det(I-M)\ne0.
\]

---

# 4. Stability condition

## Lemma candidate 1
The two-mode recursion is linearly stable if the spectral radius of:

\[
M=
\begin{pmatrix}
a_R & b_R\\
b_A & a_A
\end{pmatrix}
\]

satisfies:

\[
\rho(M)<1.
\]

If:

\[
\rho(M)\ge1,
\]

the retained-memory fixed point is unstable and cannot define a stable quadratic memory potential.

---

# 5. Extraction of microscopic coefficients

## Definition 3
Given time step \(\Delta\tau\), extract:

\[
k_R
=
\frac{1-a_R}{\Delta\tau}.
\]

Extract diffusion:

\[
D_R
=
\frac{\sigma_R^2}{2\Delta\tau}.
\]

Extract microscopic coupling:

\[
\lambda_{\mathrm{micro}}
=
\frac{c_R}{\Delta\tau}.
\]

These are the exact inputs required by `COEFFICIENT_MICRO_DERIVATION.md`.

---

# 6. Coefficient map after extraction

Once \(k_R,D_R,\lambda_{\mathrm{micro}}\) are extracted:

\[
Z_R
=
\frac{1}{2D_R},
\]

\[
m_R^2
=
\frac{k_R}{D_R},
\]

\[
V(R)
=
\frac12m_R^2(R-R_*)^2+\cdots,
\]

\[
\lambda_{\mathrm{int}}
=
\frac{\lambda_{\mathrm{micro}}}{D_R}.
\]

This connects the production recursion to the scalar-density memory action.

---

# 7. Failure conditions

The coefficient extraction fails if:

1. \(\det(I-M)=0\), so no fixed point is defined;
2. \(\rho(M)\ge1\), so the fixed point is unstable;
3. \(D_R\le0\), so \(Z_R\) is singular or nonphysical;
4. \(k_R\le0\), so \(m_R^2\le0\) and the memory well is unstable;
5. \(\lambda_{\mathrm{micro}}\) diverges;
6. the production recursion cannot be locally linearized.

---

# 8. Verifier implementation

## Status
**Implemented as `micro_recursion_extraction_verifier.py`. Execution log captured.**

The verifier samples affine two-mode recursions and extracts:

\[
k_R,\quad D_R,\quad \lambda_{\mathrm{micro}},
\]

then maps them to:

\[
Z_R,\quad m_R^2,\quad \lambda_{\mathrm{int}}.
\]

It checks:

1. fixed-point existence;
2. spectral stability;
3. positive diffusion;
4. positive restoring stiffness;
5. finite extracted coefficients;
6. failure detection for unstable/pathological recursions.

## Captured verifier output

```text
Micro recursion extraction verifier
==================================================
Route:
affine two-mode recursion -> k_R, D_R, lambda_micro -> Z_R, V, lambda_int
This validates extraction mechanics; production recursion still required.

PASS: 92.02
SOFT_FAIL: 6.15
HARD_FAIL: 1.83
k_R_median: 3.5978165282102834
D_R_median: 0.04893378248571067
lambda_micro_median: 0.22267537160464354
R_star_median: -0.003968720594299582
A_star_median: 0.004030400545775885
Z_R_median: 10.217889862611925
m_R2_median: 67.85511792230393
lambda_int_median: 1.039728801189361
stable_spectral_radius_median: 0.7249770898644605
finite_fraction_median: 1.0
```

---

# 9. What this file establishes

### Established

1. The extraction mechanics are explicit.
2. \(k_R,D_R,\lambda_{\mathrm{micro}}\) are identifiable from a local recursion.
3. The coefficient map is now operational.
4. Stability and failure conditions are explicit.
5. Pathological recursions are detected.

### Not yet established

1. The production recursion has not been substituted.
2. The actual \(\chi,\varepsilon^*\) dependence is not extracted yet.
3. Nonlinear corrections to \(V(R)\) are not fixed.
4. Coupling through the auxiliary mode \(A\) is only linearized.
5. This is still an extraction framework, not final coefficient closure.

---

# 10. What must be pasted next

To close this seam, paste the exact production recursion in any of these forms:

## Preferred

```python
R_next = ...
A_next = ...
```

including:
- noise term or stochastic update;
- pruning threshold \(\varepsilon^*\);
- \(\chi\)-dependent terms;
- matter/operator input \(\mathcal O\).

## Acceptable

Mathematical form:

\[
R_{n+1}=F_R(R_n,A_n,\mathcal O_n;\chi,\varepsilon^*),
\]

\[
A_{n+1}=F_A(A_n,R_n;\chi,\varepsilon^*).
\]

## Minimum required constants

\[
a_R,b_R,c_R,d_R,\sigma_R,a_A,b_A,d_A,\sigma_A,\Delta\tau.
\]

---

# 11. Next derivation target

After the real recursion is supplied, the next file should be:

```text
COEFFICIENT_CLOSURE_FROM_RECURSION.md
```

Its job:

- substitute the exact recursion;
- compute \(R_*,A_*\);
- extract \(k_R,D_R,\lambda_{\mathrm{micro}}\);
- compute \(Z_R,V,\lambda_{\mathrm{int}}\);
- update `COEFFICIENT_MICRO_DERIVATION.md` from conditional to production-specific.

---

# Honest status line

> `MICRO_RECURSION_EXTRACTION.md` defines the exact extraction machinery needed to turn a two-mode retained-memory recursion into \(Z_R,V,\lambda_{\mathrm{int}}\). It does not close the coefficient seam until the production recursion is supplied.

**End of file.**
