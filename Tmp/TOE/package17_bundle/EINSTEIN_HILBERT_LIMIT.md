# EINSTEIN_HILBERT_LIMIT.md

# Einstein-Hilbert Limit
## Candidate convergence program from discrete geometric action to continuum curvature action

## Status
**Live derivation target. First action-convergence pass. Not yet GR-closed.**

`CURVATURE_ESTIMATION.md` established a first verifier-backed route for estimating scalar curvature from a controlled metric field.

This file attacks the next seam:

\[
S_{\mathrm{geom}}^{\mathrm{disc}}
\longrightarrow
S_{\mathrm{EH}}
=
\frac{1}{16\pi G}
\int d^4x\sqrt{-g}R.
\]

This file does **not** derive general relativity.

It provides the first controlled action-convergence target and verifier:
- start with a metric where curvature is known,
- compute a discrete curvature-density sum,
- compare to the continuum integral,
- track convergence under refinement.

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

The geometric sector in `CONTINUUM_LIMIT.md` requires:

\[
S_{\mathrm{geom}}
\to
S_{\mathrm{EH}}
=
\frac{1}{16\pi G}
\int d^4x\sqrt{-g}R.
\]

Earlier files built pieces of the chain:

```text
EMERGENT_METRIC_MAP.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
        ↓
CURVATURE_ESTIMATION.md
```

This file asks:

> can a discrete curvature sum converge to a continuum curvature action?

---

# 2. Discrete geometric action target

## Definition 1
The generic discrete geometric action is:

\[
S_{\mathrm{geom}}^{\mathrm{disc}}
=
\sum_i
w_i R_i,
\]

where:
- \(R_i\) is a discrete scalar curvature estimate at block/cell \(i\),
- \(w_i\) is the discrete volume element, corresponding to \(\sqrt{|g|}\Delta V\).

The continuum target is:

\[
S_{\mathrm{geom}}^{\mathrm{cont}}
=
\int d^dx\sqrt{|g|}R.
\]

In four Lorentzian dimensions, this becomes the Einstein-Hilbert action up to the prefactor:

\[
\frac{1}{16\pi G}.
\]

## Assumption 1
The discrete weights \(w_i\) converge to:

\[
\sqrt{|g|}d^dx.
\]

## Failure condition 1
If no discrete volume element converges to \(\sqrt{|g|}d^dx\), the Einstein-Hilbert limit fails.

---

# 3. Controlled 2D conformal test

## Definition 2
For the first controlled verifier, use:

\[
g_{ij}=e^{2\phi(x,y)}\delta_{ij}.
\]

Then:

\[
\sqrt{g}=e^{2\phi},
\]

and in two dimensions:

\[
R=-2e^{-2\phi}\Delta\phi.
\]

Thus:

\[
\sqrt{g}R=-2\Delta\phi.
\]

On a periodic domain:

\[
\int \sqrt{g}R\,d^2x
=
-2\int \Delta\phi\,d^2x
=
0.
\]

This is topological / boundary-sensitive, so the raw Einstein-Hilbert-like action is not a strong numerical convergence test in this setting.

Therefore the verifier also tracks non-topological diagnostics:

\[
A_{|R|}
=
\int \sqrt{g}|R|\,d^2x,
\]

and:

\[
A_{R^2}
=
\int \sqrt{g}R^2\,d^2x.
\]

These are not the Einstein-Hilbert action, but they are useful tests of curvature-density convergence.

---

# 4. Discrete curvature-density sum

## Definition 3
The first discrete action proxy is:

\[
S_{\mathrm{disc}}
=
\sum_i
\sqrt{g_i}R_i\Delta A.
\]

The diagnostic action proxies are:

\[
A_{|R|}^{\mathrm{disc}}
=
\sum_i
\sqrt{g_i}|R_i|\Delta A,
\]

\[
A_{R^2}^{\mathrm{disc}}
=
\sum_i
\sqrt{g_i}R_i^2\Delta A.
\]

## Lemma candidate 1
If \(R_i\to R(x_i)\) and \(\sqrt{g_i}\Delta A\to\sqrt{g}d^2x\), then:

\[
S_{\mathrm{disc}}
\to
\int\sqrt{g}R\,d^2x,
\]

and similarly for the diagnostic curvature-density integrals.

This is a standard quadrature convergence statement, not yet a Regge or Lorentzian proof.

---

# 5. Verifier implementation

## Status
**Implemented as `einstein_hilbert_limit_verifier.py`. Execution log captured.**

The verifier uses:

\[
\phi(x,y)=A\sin(2\pi k_xx)\sin(2\pi k_yy),
\]

\[
g_{ij}=e^{2\phi}\delta_{ij}.
\]

It computes:

\[
R_{\mathrm{num}}
=
-2e^{-2\phi}\widehat{\Delta\phi},
\]

then sums:

\[
\sum_i\sqrt{g_i}R_i\Delta A,
\]

\[
\sum_i\sqrt{g_i}|R_i|\Delta A,
\]

and:

\[
\sum_i\sqrt{g_i}R_i^2\Delta A.
\]

It checks refinement and noise sensitivity.

## Captured verifier output

```text
Einstein-Hilbert limit verifier
==================================================
Controlled 2D conformal metric:
g_ij = exp(2 phi) delta_ij
EH-like density sqrt(g) R = -2 Laplacian(phi)
Also testing absolute curvature and R^2 convergence diagnostics.

Refinement test:
abs_rel_err_n24: 0.04182948800486294
R2_rel_err_n24: 0.0819092699429803
abs_rel_err_n32: 0.02372177815344278
R2_rel_err_n32: 0.046880833548126485
abs_rel_err_n48: 0.010604669080448383
R2_rel_err_n48: 0.021096879154595353
abs_rel_err_n64: 0.005977318990046603
R2_rel_err_n64: 0.011918909637783467
abs_rel_err_n96: 0.0026604645387316187
R2_rel_err_n96: 0.00531385100591137
abs_rel_err_n128: 0.0014972756952113002
R2_rel_err_n128: 0.0029923095559142594
abs_rel_err_n192: 0.000665698648422814
R2_rel_err_n192: 0.0013309541421699757

Sweep results:
PASS: 32.0
SOFT_FAIL: 68.0
HARD_FAIL: 0.0
abs_rel_error_median: 0.16094912435528386
R2_rel_error_median: 0.31714743261194456
abs_rel_error_max: 136.1921922995654
R2_rel_error_max: 19415.407858336555
```

---

# 6. What this file establishes

### Established at current proof level

1. A discrete curvature-density action target is explicitly stated.
2. A controlled convergence verifier is implemented.
3. The raw 2D EH-like integral is correctly identified as weak/topological on periodic domains.
4. Diagnostic curvature-density integrals are added to test convergence.
5. Refinement behavior is explicitly tracked.

### Not yet proved

1. Four-dimensional Lorentzian Einstein-Hilbert convergence is not shown.
2. Regge action convergence is not derived.
3. Causal-set action convergence is not derived.
4. Boundary/Gibbons-Hawking-York terms are not addressed.
5. Gauge/diffeomorphism independence is not established.
6. Newton's constant \(G\) is not derived or normalized.
7. The memory sector is not yet included in the action convergence test.

---

# 7. Theorem candidate

## Theorem candidate 1
Suppose:

1. the emergent metric map produces stable metric estimates;
2. the curvature estimator converges;
3. the discrete volume element converges to \(\sqrt{|g|}d^dx\);
4. the geometric action is a consistent curvature-density quadrature;
5. boundary terms are controlled;
6. the Lorentzian continuation is stable.

Then:

\[
S_{\mathrm{geom}}^{\mathrm{disc}}
\to
\int d^dx\sqrt{|g|}R.
\]

This theorem is **not yet proved**.

---

# 8. Failure modes

This route fails if:

1. curvature estimates do not converge under refinement;
2. the volume element does not converge to \(\sqrt{|g|}d^dx\);
3. the discrete action is dominated by noise;
4. boundary terms cannot be controlled;
5. Lorentzian signature breaks the convergence;
6. the Regge/causal-set action cannot be connected to the metric estimator;
7. Newton's constant must be inserted by phenomenological calibration only.

---

# 9. Updated proof-chain status

The geometric continuum chain is now:

```text
EMERGENT_METRIC_MAP.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
        ↓
CURVATURE_ESTIMATION.md
        ↓
EINSTEIN_HILBERT_LIMIT.md
        ↓
CONTINUUM_LIMIT.md
```

The remaining hard seam is:

\[
G_{\mu\nu}
=
8\pi
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right)
\]

with Bianchi-compatible variation.

That requires the next file:

```text
FIELD_EQUATION_VARIATION.md
```

---

# Honest status line

> `EINSTEIN_HILBERT_LIMIT.md` gives the first verifier-backed action-convergence test for a controlled curvature-density sum. It supports the plausibility of discrete curvature-density convergence in a simplified 2D conformal setting, but it does not derive the full 4D Lorentzian Einstein-Hilbert action or GR field equations.

**End of file.**
