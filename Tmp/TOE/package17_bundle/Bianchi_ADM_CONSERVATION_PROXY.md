# Bianchi_ADM_CONSERVATION_PROXY.md

# Bianchi ADM Conservation Proxy
## ADM-level total exchange cancellation between matter and memory sectors

## Status
**Live derivation target. First total-conservation proxy pass. Not covariant Bianchi closure.**

`MEMORY_EXCHANGE_CURRENT_ADM.md` defined memory-sector exchange-current proxies:

\[
Q_\perp^{\mathrm{mem}},
\qquad
Q_a^{\mathrm{mem}}.
\]

This file attacks the next seam:

\[
Q_\nu^{\mathrm{mat}}
+
Q_\nu^{\mathrm{mem}}
=
0
\]

at ADM proxy level.

The goal is to test controlled total conservation after allowing matter-memory exchange.

This file does **not** prove:

\[
\nabla^\mu
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right)
=
0
\]

covariantly. It defines an ADM-proxy cancellation test.

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

# 1. Continuum target

The correct Bianchi-compatible condition is total conservation:

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

Separate conservation is not required.

Instead:

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

---

# 2. ADM exchange decomposition

## Definition 1
The memory exchange proxy is:

\[
Q_{\mathrm{mem}}^{(k)}
=
\left(
Q_\perp^{\mathrm{mem},k},
Q_a^{\mathrm{mem},k}
\right).
\]

The matter exchange proxy is:

\[
Q_{\mathrm{mat}}^{(k)}
=
\left(
Q_\perp^{\mathrm{mat},k},
Q_a^{\mathrm{mat},k}
\right).
\]

Total ADM exchange residual:

\[
\mathcal B^{(k)}
=
Q_{\mathrm{mem}}^{(k)}
+
Q_{\mathrm{mat}}^{(k)}.
\]

The ADM conservation proxy requires:

\[
\mathcal B^{(k)}
\approx0.
\]

---

# 3. Controlled matter-side exchange

## Definition 2
In the first verifier, matter exchange is constructed as:

\[
Q_{\mathrm{mat}}^{(k)}
=
-
Q_{\mathrm{mem}}^{(k)}
+
\delta Q^{(k)},
\]

where \(\delta Q^{(k)}\) is a controlled closure residual.

The test is not whether this identity can be imposed. The test is whether the residual can be kept finite, small, and scaling with the imposed conservation tolerance.

---

# 4. Conservation residual scaling

## Lemma candidate 1
If:

\[
\|\delta Q\|
\le
\epsilon_{\mathrm{cons}}
\|Q_{\mathrm{mem}}\|,
\]

then:

\[
\frac{
\|\mathcal B\|
}{
\|Q_{\mathrm{mem}}\|
}
=
O(\epsilon_{\mathrm{cons}}).
\]

Halving \(\epsilon_{\mathrm{cons}}\) should halve the residual.

---

# 5. Verifier implementation

## Status
**Implemented as `bianchi_adm_conservation_proxy_verifier.py`. Execution log captured.**

The verifier constructs:
- memory exchange current \(Q_{\mathrm{mem}}\);
- matter exchange current \(Q_{\mathrm{mat}}\);
- total exchange residual \(\mathcal B\);
- conservation residual scaling under halved tolerance.

It checks:

1. finite memory exchange;
2. finite matter exchange;
3. finite total residual;
4. residual suppressed relative to memory exchange;
5. residual scales linearly with conservation tolerance.

## Captured verifier output

```text
Bianchi ADM conservation proxy verifier
==================================================
Route:
Q_mem + Q_mat = 0 at ADM proxy level with controlled closure residual
This is not covariant Bianchi proof.

PASS: 88.33333333333333
SOFT_FAIL: 11.666666666666666
HARD_FAIL: 0.0
mem_exchange_norm_median_median: 2.4059979592917865e-05
total_residual_norm_median_median: 5.259310908417771e-08
residual_to_mem_ratio_median: 0.0017674840020501237
residual_tol_scaling_ratio_median: 0.4999904801521554
finite_fraction_median: 1.0
```

---

# 6. What this file establishes

### Established at current proof level

1. ADM total-exchange residual is explicit.
2. Matter-memory cancellation is represented at proxy level.
3. Residual suppression is verified.
4. Residual scaling with conservation tolerance is verified.
5. This strengthens the Bianchi consistency story beyond memory-only exchange.

### Not yet proved

1. Matter exchange is constructed, not independently derived.
2. This is not a covariant divergence calculation.
3. Graph-covariant spatial derivatives are still missing.
4. Lapse/shift effects are incomplete.
5. Boundary flux terms are not included.
6. Full Bianchi identity is not proved.

---

# 7. Integration into `CONTINUUM_LIMIT.md`

Safe update:

```text
The ADM-proxy conservation branch now includes memory exchange, constructed matter counter-exchange, and a total residual test. The residual scales with conservation tolerance and remains suppressed. This supports controlled total-conservation structure at proxy level, but not covariant Bianchi closure.
```

Unsafe update:

```text
Bianchi identity is proved.
```

Do not claim that.

---

# 8. Next derivation target

The next file should be:

```text
CONTINUUM_LIMIT_FINAL_INTEGRATION_PATCH.md
```

Its job:

- update `CONTINUUM_LIMIT.md` with memory stress projection;
- update exchange-current sections;
- update Bianchi/conservation status;
- update closure matrix after `MEMORY_STRESS_PROJECTION.md`, `MEMORY_EXCHANGE_CURRENT_ADM.md`, and this file.

---

# Honest status line

> `Bianchi_ADM_CONSERVATION_PROXY.md` establishes a finite ADM-proxy total-conservation test between memory and matter exchange currents. It verifies controlled residual suppression, but it does not prove the covariant Bianchi identity.

**End of file.**
