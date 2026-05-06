# MEMORY_EXCHANGE_CURRENT_ADM.md

# Memory Exchange Current in ADM Form
## Projecting memory-sector nonconservation into normal and spatial exchange currents

## Status
**Live derivation target. First ADM exchange-current pass. Not covariant conservation closure.**

`MEMORY_STRESS_PROJECTION.md` projected the scalar-density memory stress tensor onto ADM spatial slices:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
=
h_a^{\ \mu}h_b^{\ \nu}
T_{\mu\nu}^{\mathrm{mem}}.
\]

This file attacks the next seam:

\[
\nabla^\mu T_{\mu\nu}^{\mathrm{mem}}
=
-Q_\nu
\]

projected into ADM form.

The goal is to separate:

- normal energy exchange;
- spatial momentum exchange;
- weak-memory suppression.

This file does **not** prove covariant conservation. It defines and verifies finite ADM exchange-current proxies.

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

# 1. Continuum exchange target

The total stress-energy must satisfy:

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

If matter and memory exchange energy-momentum, then:

\[
\nabla^\mu T_{\mu\nu}^{\mathrm{mat}}
=
Q_\nu,
\]

\[
\nabla^\mu T_{\mu\nu}^{\mathrm{mem}}
=
-Q_\nu.
\]

Earlier `CONTINUUM_LIMIT.md` correctly updated the Bianchi condition to controlled total conservation rather than separate conservation.

---

# 2. ADM projection of exchange current

## Definition 1
Let \(n^\nu\) be the unit normal to a causal slice and \(h^\nu_{\ a}\) the spatial projector.

Define normal exchange:

\[
Q_\perp
=
n^\nu Q_\nu.
\]

Define spatial exchange:

\[
Q_a
=
h^\nu_{\ a}Q_\nu.
\]

The target is:

\[
Q_\nu
=
Q_\perp n_\nu
+
Q_a h^a_{\ \nu}.
\]

---

# 3. First finite proxy

## Definition 2
The normal exchange proxy is the slice-to-slice change in memory energy density:

\[
Q_\perp^{(k)}
\sim
\frac{
\rho_{\mathrm{mem}}^{(k+1)}
-
\rho_{\mathrm{mem}}^{(k-1)}
}{
2\Delta\tau
}.
\]

The spatial exchange proxy is the spatial divergence of projected memory stress:

\[
Q_a^{(k)}
\sim
D^b\mathcal S_{ab}^{\mathrm{mem},k}.
\]

In the verifier, \(D^b\) is approximated by a discrete finite-difference divergence over sampled slice points.

---

# 4. Weak-memory scaling

## Lemma candidate 1
If:

\[
R_{\mathrm{eff}}=\eta_{\mathrm{mem}}r,
\]

then interaction-dominated exchange should scale as:

\[
Q = O(\eta_{\mathrm{mem}}),
\]

while kinetic-only exchange should scale as:

\[
Q_{\mathrm{kin}}=O(\eta_{\mathrm{mem}}^2).
\]

Thus:

\[
\frac{\|Q(\eta/2)\|}{\|Q(\eta)\|}
\approx
\frac12
\]

for interaction-dominated exchange, and:

\[
\frac{\|Q_{\mathrm{kin}}(\eta/2)\|}{\|Q_{\mathrm{kin}}(\eta)\|}
\approx
\frac14
\]

for kinetic exchange.

---

# 5. Verifier implementation

## Status
**Implemented as `memory_exchange_current_adm_verifier.py`. Execution log captured.**

The verifier constructs:
- ADM slice metrics;
- weak memory fields;
- memory energy-density proxy;
- projected memory stress;
- normal exchange \(Q_\perp\);
- spatial exchange \(Q_a\).

It checks:

1. finite exchange current;
2. weak-memory suppression;
3. interaction-dominated \(O(\eta)\) scaling;
4. kinetic \(O(\eta^2)\) scaling;
5. no hard singular failures.

## Captured verifier output

```text
Memory exchange current ADM verifier
==================================================
Route:
project ∇^μ T^mem_{μν} = -Q_ν into ADM normal/spatial exchange proxies
Checks finite exchange and weak-memory scaling.

PASS: 94.0
SOFT_FAIL: 6.0
HARD_FAIL: 0.0
q_perp_norm_median_median: 7.75566319733455e-06
q_spatial_norm_median_median: 1.5353386148452698e-05
q_total_half_ratio_median: 0.49871047698313964
q_kinetic_half_ratio_median: 0.24999941209250437
finite_fraction_median: 1.0
weak_suppression_fraction_median: 1.0
```

---

# 6. What this file establishes

### Established at current proof level

1. ADM exchange-current components are defined.
2. Normal and spatial exchange proxies are explicit.
3. Weak-memory scaling is verified.
4. The exchange current remains finite and suppressed in sampled regimes.

### Not yet proved

1. This is not covariant divergence \(\nabla^\mu T_{\mu\nu}\).
2. The spatial derivative is a finite proxy, not graph-covariant \(D_a\).
3. Lapse/shift effects are not fully included.
4. Matter-side \(Q_\nu\) is not independently computed.
5. Bianchi-compatible total conservation is not fully proved.
6. Coefficients \(Z_R,V,\lambda_{\mathrm{int}}\) are still not microscopically derived.

---

# 7. Integration into continuum limit

This file strengthens the Bianchi / exchange section of `CONTINUUM_LIMIT.md`.

The safe update is:

```text
The memory sector now has ADM-projected exchange-current proxies Q_perp and Q_a with verified weak-memory suppression. This supports controlled total-conservation structure at proxy level, but not full covariant conservation.
```

---

# 8. Next derivation target

The next file should be:

```text
Bianchi_ADM_CONSERVATION_PROXY.md
```

Its job:

\[
Q_\nu^{\mathrm{mat}}
+
Q_\nu^{\mathrm{mem}}
=
0
\]

at ADM proxy level.

That requires constructing a matching matter-side exchange proxy.

---

# Honest status line

> `MEMORY_EXCHANGE_CURRENT_ADM.md` defines ADM normal/spatial memory exchange-current proxies and verifies weak-memory suppression. It strengthens the conservation story but does not yet prove covariant Bianchi-compatible conservation.

**End of file.**
