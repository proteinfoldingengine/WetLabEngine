# CAUSAL_ADM_FIELD_EQUATION_PROXY.md

# Causal ADM Field Equation Proxy
## Discrete Euler-response equation for causal-slice ADM action proxy with weak-memory source

## Status
**Live derivation target. First field-equation proxy pass. Not Einstein equations.**

`CAUSAL_ADM_VARIATION_TARGET.md` defined a stable finite-difference variational response:

\[
\mathcal E_{ab}^{(k)}
\approx
\frac{\delta S_{\mathrm{proxy}}^{(N,R_3)}}{\delta h_{ab}^{(k)}}.
\]

This file attacks the next seam:

\[
\mathcal E_{ab}^{(k)}
=
\mathcal S_{ab}^{\mathrm{mem},k}.
\]

This is a **discrete field-equation proxy**, not the Einstein field equations.

Its purpose is to test whether the causal ADM proxy can accept a controlled weak-memory source without singular behavior.

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

# 1. Geometric Euler response

## Definition 1
For each causal slice \(k\), define:

\[
\mathcal E_{ab}^{(k)}
=
\frac{\delta S_{\mathrm{proxy}}^{(N,R_3)}}{\delta h_{ab}^{(k)}}.
\]

In the current implementation, this is estimated by symmetric finite differences:

\[
\mathcal E_{ab}^{(k)}
\approx
\frac{
S[h+\epsilon E_{ab}]
-
S[h-\epsilon E_{ab}]
}{
2\epsilon
}.
\]

This is the discrete geometric response of the proxy action.

---

# 2. Weak-memory source

## Definition 2
The first weak-memory source proxy is:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
=
\eta_{\mathrm{mem}}
\left(
\frac{h_{ab}^{(k)}}{\mathrm{Tr}(h^{(k)})}
+
\delta s_{ab}^{(k)}
\right),
\]

where:

- \(\eta_{\mathrm{mem}}\ll1\);
- \(\delta s_{ab}^{(k)}\) is a bounded symmetric perturbation;
- the source scales linearly with memory loading.

This mirrors the weak-memory condition from `CONTINUUM_LIMIT.md`:

\[
T_{\mu\nu}^{\mathrm{mem}}
=
O(\eta_{\mathrm{mem}}).
\]

---

# 3. Field-equation proxy

## Definition 3
The discrete field-equation proxy is:

\[
\mathcal E_{ab}^{(k)}
-
\mathcal S_{ab}^{\mathrm{mem},k}
=
0.
\]

Equivalently:

\[
\mathcal E_{ab}^{(k)}
=
\mathcal S_{ab}^{\mathrm{mem},k}.
\]

This is not yet:

\[
G_{\mu\nu}=8\pi T_{\mu\nu}.
\]

It is a proxy-level consistency equation for the causal ADM action.

---

# 4. Weak-memory scaling check

## Lemma candidate 1
If:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
=
O(\eta_{\mathrm{mem}}),
\]

then halving \(\eta_{\mathrm{mem}}\) should halve the source norm:

\[
\|\mathcal S(\eta/2)\|
/
\|\mathcal S(\eta)\|
\approx
1/2.
\]

The verifier checks this scaling.

---

# 5. Verifier implementation

## Status
**Implemented as `causal_adm_field_equation_proxy_verifier.py`. Execution log captured.**

The verifier tests:

1. finite Euler-response norm;
2. finite weak-memory source norm;
3. finite residual norm;
4. source small relative to Euler response in weak-memory regime;
5. source norm scales linearly with \(\eta_{\mathrm{mem}}\).

## Captured verifier output

```text
Causal ADM field equation proxy verifier
==================================================
Route:
finite Euler response E_ab^(k) = weak-memory source S_ab^(mem,k)
This is a discrete proxy, not Einstein's equation.

PASS: 100.0
SOFT_FAIL: 0.0
HARD_FAIL: 0.0
euler_norm_median_median: 0.6800877978990056
source_norm_median_median: 0.0011714507094753575
residual_norm_median_median: 0.6791999554202897
source_to_euler_ratio_median: 0.001612824295743367
weak_scaling_ratio_median: 0.499999999573022
finite_fraction_median: 1.0
```

---

# 6. What this file establishes

### Established at current proof level

1. A discrete field-equation proxy is explicitly defined.
2. Weak-memory source scaling is explicit.
3. The verifier confirms finite residuals and linear source scaling.
4. This links the causal ADM proxy branch back to the memory-sector logic.

### Not yet proved

1. The source is not yet the exact \(T_{\mu\nu}^{\mathrm{mem}}\).
2. The equation is not covariant.
3. The equation is not derived from original graph variables.
4. Lapse and shift constraints are not varied.
5. No continuum Einstein equation is derived.
6. Matter source coupling remains schematic.

---

# 7. Next derivation target

The next file should be:

```text
CAUSAL_CONTINUUM_REINTEGRATION.md
```

Its job is to reintegrate the corrected causal ADM branch back into `CONTINUUM_LIMIT.md` and classify which parts replace older schematic metric/action assumptions.

---

# Honest status line

> `CAUSAL_ADM_FIELD_EQUATION_PROXY.md` defines a finite discrete field-equation proxy for the causal ADM action and a weak-memory source. It reconnects geometry and memory at proxy level, but it is not a derivation of Einstein's equations.

**End of file.**
