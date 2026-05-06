# COEFFICIENT_CLOSURE_FROM_RECURSION.md

# Coefficient Closure From Recursion
## Production-specific closure test for \(Z_R\), \(V(R)\), and \(\lambda_{\mathrm{int}}\)

## Status
**Closure gate. Currently conditional until production recursion coefficients are supplied.**

`MICRO_RECURSION_EXTRACTION.md` defined the extraction machinery:

\[
R_{n+1}
=
a_RR_n+b_RA_n+c_R\mathcal O_n+d_R+\sigma_R\xi_n,
\]

\[
A_{n+1}
=
a_AA_n+b_AR_n+d_A+\sigma_A\zeta_n.
\]

This file is the actual closure gate.

It does not create another ansatz. It requires the production recursion coefficients.

If the exact recursion coefficients are supplied, this file computes:

\[
k_R,\quad D_R,\quad \lambda_{\mathrm{micro}},
\]

and therefore:

\[
Z_R,\quad V(R),\quad \lambda_{\mathrm{int}}.
\]

If they are not supplied, the coefficient seam remains conditional.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**
- **Closure gate**

Nothing here should be interpreted as closed unless the production recursion is supplied and passes the verifier.

---

# 1. Required production input

The verifier requires a file:

```text
production_recursion_coefficients.json
```

with:

```json
{
  "a_R": 0.72,
  "b_R": 0.03,
  "c_R": 0.08,
  "d_R": 0.0,
  "sigma_R": 0.12,
  "a_A": 0.68,
  "b_A": 0.04,
  "d_A": 0.0,
  "sigma_A": 0.10,
  "dt": 1.0,
  "chi": 0.2667,
  "eps_star": 0.05
}
```

The example above is illustrative only.

It is **not** the production recursion.

---

# 2. Fixed-point extraction

## Definition 1
Define:

\[
M
=
\begin{pmatrix}
a_R & b_R\\
b_A & a_A
\end{pmatrix},
\qquad
d=
\begin{pmatrix}
d_R\\
d_A
\end{pmatrix}.
\]

The fixed point satisfies:

\[
(I-M)
\begin{pmatrix}
R_*\\
A_*
\end{pmatrix}
=
d.
\]

Therefore:

\[
\begin{pmatrix}
R_*\\
A_*
\end{pmatrix}
=
(I-M)^{-1}d.
\]

This exists only if:

\[
\det(I-M)\ne0.
\]

---

# 3. Stability extraction

## Definition 2
The recursion is linearly stable only if:

\[
\rho(M)<1.
\]

If:

\[
\rho(M)\ge1,
\]

then the fixed point cannot support a stable local quadratic memory potential.

---

# 4. Coefficient extraction

## Definition 3
Given \(\Delta\tau=dt\), extract:

\[
k_R
=
\frac{1-a_R}{dt},
\]

\[
D_R
=
\frac{\sigma_R^2}{2dt},
\]

\[
\lambda_{\mathrm{micro}}
=
\frac{c_R}{dt}.
\]

Then:

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

---

# 5. Closure theorem candidate

## Theorem candidate 1
If the production recursion satisfies:

\[
\det(I-M)\ne0,
\]

\[
\rho(M)<1,
\]

\[
D_R>0,
\]

\[
k_R>0,
\]

and finite:

\[
\lambda_{\mathrm{micro}},
\]

then the scalar-density memory coefficients are production-specific and finite:

\[
Z_R=\frac{1}{2D_R},
\]

\[
V(R)=\frac12\frac{k_R}{D_R}(R-R_*)^2+\cdots,
\]

\[
\lambda_{\mathrm{int}}=\frac{\lambda_{\mathrm{micro}}}{D_R}.
\]

This closes the coefficient seam at quadratic order.

---

# 6. What counts as closure

## Closure gate
The coefficient seam may be marked:

```text
production-specific quadratic closure
```

only if the verifier reports:

```text
STATUS: PASS
```

using the actual production recursion.

If the verifier reports:

```text
STATUS: CONDITIONAL_NOT_CLOSED
```

then no production recursion was supplied.

If the verifier reports:

```text
STATUS: FAIL
```

then the supplied recursion does not produce a stable scalar-density memory action.

---

# 7. Verifier implementation

## Status
**Implemented as `coefficient_closure_from_recursion_verifier.py`.**

Current verifier output:

```text
Coefficient closure from recursion verifier
==================================================
STATUS: CONDITIONAL_NOT_CLOSED
Reason: production_recursion_coefficients.json was not supplied.

To close this seam, provide JSON with:
a_R,b_R,c_R,d_R,sigma_R,a_A,b_A,d_A,sigma_A,dt,chi,eps_star
```

Interpretation of current output:

- `CONDITIONAL_NOT_CLOSED` means the production recursion JSON was not supplied.
- This is honest and expected until the real recursion coefficients are available.
- The verifier is ready to promote the coefficient seam to production-specific closure once the real recursion is supplied.

---

# 8. Failure conditions

The closure attempt fails if any of the following occur:

1. missing production recursion;
2. \(\det(I-M)=0\);
3. \(\rho(M)\ge1\);
4. \(D_R\le0\);
5. \(k_R\le0\);
6. \(m_R^2\le0\);
7. \(\lambda_{\mathrm{int}}\) is singular;
8. \(\chi\) or \(\varepsilon^*\) is inconsistent with the fixed-point regime.

---

# 9. What remains after quadratic closure

Even if this file passes with production recursion, the following remain:

1. higher-order terms in \(V(R)\);
2. nonlinear dependence on \(A\);
3. exact matter operator \(\mathcal O_{\mathrm{mat}}\);
4. covariant conservation;
5. ADM/EH convergence.

So this file can close the **quadratic coefficient seam**, not all of GR.

---

# 10. Next action required

To proceed, create:

```text
production_recursion_coefficients.json
```

beside the verifier.

Use the exact production recursion coefficients, not illustrative values.

Then run:

```bash
python coefficient_closure_from_recursion_verifier.py
```

If it passes, update:

```text
COEFFICIENT_MICRO_DERIVATION.md
```

from:

```text
conditional theorem pass
```

to:

```text
production-specific quadratic coefficient closure
```

---

# Honest status line

> `COEFFICIENT_CLOSURE_FROM_RECURSION.md` is the closure gate for the memory-action coefficients. It is ready to close \(Z_R,V,\lambda_{\mathrm{int}}\) at quadratic order once the production recursion coefficients are supplied. Without those coefficients, the seam remains conditional.

**End of file.**
