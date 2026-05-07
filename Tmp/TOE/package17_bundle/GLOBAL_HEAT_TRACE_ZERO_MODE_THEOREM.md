# GLOBAL_HEAT_TRACE_ZERO_MODE_THEOREM.md

# Global Heat-Trace Zero-Mode Theorem
## Candidate derivation target from full held-out campaign

## Status
**Theorem candidate. Numerically supported. Not yet proved.**

This file records the theorem target implied by:

```text
TRACE_DX_SCALING_FULL_HELDOUT_RESULT.md
```

The empirical result is:

\[
C_\Delta(dx)=
\frac{\int_\Sigma R(a)\,dV}{B(a)-B(0)}
\approx
-14.5\,dx^2.
\]

Equivalently:

\[
\int_\Sigma R(a)\,dV
\approx
-14.5\,dx^2
\left[B(a)-B(0)\right].
\]

---

# 1. Setup

Let \(G_N(a)\) be the weighted periodic 3D conformal lattice with:

\[
h_{ij}=e^{2\phi}\delta_{ij},
\]

and graph Laplacian:

\[
L_a=\frac{D_a-W_a}{dx^2}.
\]

Define the heat trace:

\[
T_a(t)=\mathrm{Tr}(e^{-tL_a}).
\]

Define the normalized trace:

\[
H_a(t)=T_a(t)(4\pi t)^{3/2}.
\]

Over the admissible short-time discrete window:

\[
t=\lambda dx^2,
\]

fit:

\[
H_a(t)\approx A(a)+B(a)t.
\]

Let:

\[
\Delta B(a)=B(a)-B(0).
\]

---

# 2. Candidate theorem

For the tested conformal torus family and graph weighting law, as \(dx\to 0\):

\[
\boxed{
\int_\Sigma R(a)\,dV
=
-C_0 dx^2 \Delta B(a)
+
O(dx^\alpha)
+
O(a^3)
}
\]

with empirical:

\[
C_0\approx 14.5.
\]

---

# 3. Why flat subtraction is necessary

The raw slope \(B(a)\) contains a dominant graph spectral background term:

\[
B_{\mathrm{flat}}=B(0).
\]

Therefore:

\[
B(a)
=
B(0)
+
B_R(a)
+
\text{higher order terms}.
\]

Only:

\[
\Delta B(a)=B(a)-B(0)
\]

isolates the curvature-coupled heat-trace response.

---

# 4. Empirical support

Full held-out campaign:

```text
N = 8, 10, 12, 14, 16, 18
amp = 0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25
n_rows = 54
```

All-data fit:

```text
C_delta ≈ -14.5025 dx^1.9849
mean error ≈ 0.92%
max error ≈ 2.59%
```

Held-out \(N=16,18\):

```text
mean error ≈ 2.41%
max error ≈ 3.89%
```

Held-out amplitudes \(a=0.05,0.25\):

```text
mean error ≈ 1.18%
max error ≈ 2.65%
```

---

# 5. Required derivation steps

## Step 1: Discrete heat expansion

Show that:

\[
H_a(t)-H_0(t)
\]

has leading curvature response proportional to:

\[
dx^{-2}\int R\,dV
\]

under \(t=\lambda dx^2\).

## Step 2: Graph spectral background cancellation

Prove that subtracting \(B(0)\) cancels the lattice background slope.

## Step 3: dx² normalization

Derive:

\[
C_\Delta(dx)\sim -C_0dx^2.
\]

## Step 4: Coefficient derivation

Identify:

\[
C_0\approx 14.5
\]

from:
- stencil geometry;
- six-neighbor periodic lattice degree;
- chosen Gaussian edge weight;
- heat-window multipliers;
- \((4\pi t)^{3/2}\) normalization.

## Step 5: Error order

Bound:

\[
O(dx^\alpha)
\]

and finite-amplitude corrections.

---

# 6. Open issues

This theorem is not yet closed because:

```text
C0 is empirical
alpha is not derived
window dependence is not bounded
only one conformal family has been tested
non-conformal perturbations have not been tested
```

---

# 7. Next numerical falsifier

Run:

```text
COLAB_MULTI_GEOMETRY_TRACE_DX_SCALING.py
```

Required geometries:

```text
cos x cos y cos z
cos 2x cos y cos z
cos x + 0.5 cos 2y
mixed Fourier conformal field
anisotropic conformal packet
```

Test whether the same:

\[
C_\Delta(dx)\sim -C_0 dx^2
\]

survives.

---

# 8. Status line

> The global heat-trace zero-mode theorem is now a concrete derivation problem: explain why the background-subtracted heat-trace slope obeys \(\int R\,dV\approx -14.5dx^2[B(a)-B(0)]\).

**End of file.**
