# Bianchi_CLOSURE_STATUS.md

# Bianchi Closure Status
## Audit of memory/matter exchange, ADM conservation proxies, and remaining covariant Bianchi gaps

## Status
**Closure audit. Not a proof.**

This file audits the Bianchi/conservation branch after:

```text
MEMORY_STRESS_PROJECTION.md
MEMORY_EXCHANGE_CURRENT_ADM.md
Bianchi_ADM_CONSERVATION_PROXY.md
MATTER_EXCHANGE_DERIVATION.md
Bianchi_INTERACTION_CHANNEL.md
```

It separates what is now verifier-backed, what is interaction-channel closed, what remains proxy-level, and what still blocks full covariant Bianchi closure.

This file does **not** claim:

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

has been proved.

---

# 1. Continuum target

The correct conservation target is total conservation:

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

Equivalently, matter and memory may exchange energy-momentum:

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

Separate conservation is not required.

---

# 2. Current Bianchi branch

```text
CONTINUUM_LIMIT.md
        ↓
MEMORY_STRESS_PROJECTION.md
        ↓
MEMORY_EXCHANGE_CURRENT_ADM.md
        ↓
MATTER_EXCHANGE_DERIVATION.md
        ↓
Bianchi_INTERACTION_CHANNEL.md
        ↓
Bianchi_ADM_CONSERVATION_PROXY.md
```

---

# 3. Seam-by-seam status

| Seam | File | Status | Evidence | Main limitation |
|---|---|---:|---|---|
| Scalar memory stress | `CONTINUUM_LIMIT.md` | Candidate | explicit \(T_{\mu\nu}^{\mathrm{mem}}\) form | coefficients not microscopically derived |
| ADM memory stress projection | `MEMORY_STRESS_PROJECTION.md` | Verifier-backed proxy | PASS 85.67% | not full spacetime projection |
| ADM memory exchange current | `MEMORY_EXCHANGE_CURRENT_ADM.md` | Verifier-backed proxy | PASS 94.0% | not covariant divergence |
| ADM total conservation residual | `Bianchi_ADM_CONSERVATION_PROXY.md` | Verifier-backed proxy | PASS 88.33% | matter exchange originally constructed |
| Matter exchange derivation | `MATTER_EXCHANGE_DERIVATION.md` | Verifier-backed interaction proxy | PASS 100.0% | \(\mathcal O_{\mathrm{mat}}\) schematic |
| Interaction-channel cancellation | `Bianchi_INTERACTION_CHANNEL.md` | Interaction-channel proxy closed | PASS 100.0% | not full Bianchi closure |
| Full covariant Bianchi identity | not yet | Open | N/A | graph-covariant divergence, boundary terms, full stress tensor |

---

# 4. What is now established

## 4.1 ADM projection of memory stress

`MEMORY_STRESS_PROJECTION.md` established:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
=
h_a^{\ \mu}h_b^{\ \nu}
T_{\mu\nu}^{\mathrm{mem}}.
\]

Verifier result:

```text
PASS: 85.67%
SOFT_FAIL: 14.33%
HARD_FAIL: 0.0%
```

Key diagnostics:

```text
source_norm_median: 0.0003135
scaling_ratio_median: 0.4984
kinetic_order_ratio_median: 0.2500
finite_fraction_median: 1.0
```

Meaning:

- projected memory source is finite;
- interaction-dominated source scales as \(O(\eta)\);
- kinetic source scales as \(O(\eta^2)\);
- source remains weak.

---

## 4.2 ADM memory exchange current

`MEMORY_EXCHANGE_CURRENT_ADM.md` established ADM exchange components:

\[
Q_\perp,
\qquad
Q_a.
\]

Verifier result:

```text
PASS: 94.0%
SOFT_FAIL: 6.0%
HARD_FAIL: 0.0%
```

Key diagnostics:

```text
q_perp_norm_median: 7.76e-06
q_spatial_norm_median: 1.54e-05
q_total_half_ratio: 0.4987
q_kinetic_half_ratio: 0.2500
finite_fraction_median: 1.0
```

Meaning:

- normal and spatial exchange proxies are finite;
- interaction exchange scales as \(O(\eta)\);
- kinetic exchange scales as \(O(\eta^2)\).

---

## 4.3 Matter exchange derived from interaction

`MATTER_EXCHANGE_DERIVATION.md` replaced constructed matter exchange with:

\[
Q_\nu^{\mathrm{mat}}
\sim
\lambda_{\mathrm{int}}
\mathcal O_{\mathrm{mat}}
\nabla_\nu R_{\mathrm{eff}}.
\]

Verifier result:

```text
PASS: 100.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 0.0%
```

Key diagnostics:

```text
q_mat_norm_median: 4.27e-05
q_mat_half_ratio: 0.5000
q_mem_int_norm_median: 4.27e-05
best_residual_ratio: 0.0
finite_fraction_median: 1.0
```

Meaning:

- matter exchange is finite;
- matter exchange scales as \(O(\eta)\);
- interaction memory exchange cancels under matched sign convention.

---

## 4.4 Interaction-channel cancellation

`Bianchi_INTERACTION_CHANNEL.md` established:

\[
Q_\nu^{\mathrm{mat,int}}
+
Q_\nu^{\mathrm{mem,int}}
=
0.
\]

Verifier result:

```text
PASS: 100.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 0.0%
```

Key diagnostics:

```text
q_channel_norm_median: 3.81e-05
q_half_ratio: 0.5000
cancellation_residual_median: 0.0
residual_to_channel_ratio: 0.0
finite_fraction_median: 1.0
```

Meaning:

The interaction-channel proxy is closed.

Important limitation:

This does not include:
- kinetic memory exchange;
- potential memory exchange;
- boundary flux;
- graph-covariant divergence;
- full spacetime stress tensor divergence.

---

## 4.5 ADM total-conservation residual

`Bianchi_ADM_CONSERVATION_PROXY.md` tested:

\[
Q_{\mathrm{mem}}^{(k)}
+
Q_{\mathrm{mat}}^{(k)}
=
\mathcal B^{(k)}
\approx0.
\]

Verifier result:

```text
PASS: 88.33%
SOFT_FAIL: 11.67%
HARD_FAIL: 0.0%
```

Key diagnostics:

```text
mem_exchange_norm_median: 2.41e-05
total_residual_norm_median: 5.26e-08
residual_to_mem_ratio: 0.00177
residual_tol_scaling_ratio: 0.49999
finite_fraction_median: 1.0
```

Meaning:

- total residual is finite;
- residual is strongly suppressed;
- residual scales with conservation tolerance.

---

# 5. What is now actually closed?

## Closed at proxy level

The following is now closed at **interaction-channel proxy level**:

\[
Q_\nu^{\mathrm{mat,int}}
+
Q_\nu^{\mathrm{mem,int}}
=
0.
\]

Both sides are derived from the same interaction:

\[
\mathcal L_{\mathrm{int}}
=
\lambda_{\mathrm{int}}
R_{\mathrm{eff}}
\mathcal O_{\mathrm{mat}}.
\]

## Not closed

The full covariant statement is not closed:

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

Why not:

1. the divergence is not computed covariantly;
2. graph-covariant spatial derivative is missing;
3. normal/lapse/shift terms are incomplete;
4. matter sector stress tensor is not fully specified;
5. boundary flux terms are absent;
6. non-interaction memory terms are not fully balanced;
7. coefficients \(Z_R,V,\lambda_{\mathrm{int}}\) remain parametric.

---

# 6. Updated Bianchi classification

| Object | Classification | Safe claim |
|---|---:|---|
| \(T_{\mu\nu}^{\mathrm{mem}}\) scalar candidate | Candidate | explicit but parametric |
| \(\mathcal S_{ab}^{\mathrm{mem}}\) | Verifier-backed proxy | ADM spatial projection scales correctly |
| \(Q_\perp^{\mathrm{mem}},Q_a^{\mathrm{mem}}\) | Verifier-backed proxy | finite and weak-memory suppressed |
| \(Q_\nu^{\mathrm{mat,int}}\) | Verifier-backed interaction proxy | derived from scalar interaction |
| \(Q_\nu^{\mathrm{mat,int}}+Q_\nu^{\mathrm{mem,int}}\) | Proxy closed | cancels exactly under sign convention |
| \(\mathcal B=Q_{\mathrm{mem}}+Q_{\mathrm{mat}}\) | Verifier-backed residual proxy | suppressed residual |
| Full \(\nabla^\mu T_{\mu\nu}^{\mathrm{tot}}=0\) | Open | not proved |

---

# 7. Required wording for `CONTINUUM_LIMIT.md`

Safe update:

```text
The interaction-channel matter-memory exchange is now derived from the scalar coupling and cancels exactly at ADM-proxy level. ADM memory exchange currents and total residuals are finite and weak-memory suppressed. This strengthens Bianchi consistency at proxy level.
```

Unsafe update:

```text
The Bianchi identity is proved.
```

Do not claim that.

More precise safe language:

```text
Bianchi-compatible total conservation is supported by ADM proxy tests, including an exactly cancelling derived interaction channel, but full covariant conservation remains open.
```

---

# 8. Remaining blockers to Bianchi closure

## 8.1 Graph-covariant divergence

Need:

\[
D^a\mathcal S_{ab}^{\mathrm{mem}}
\]

on the antichain graph, not a simple finite-difference proxy.

Next object:

```text
GRAPH_COVARIANT_DIVERGENCE.md
```

## 8.2 Full normal projection

Need lapse/normal contribution:

\[
n^\nu\nabla^\mu T_{\mu\nu}
\]

with measured \(N_k\), not just slice-to-slice energy difference.

## 8.3 Shift contribution

Need shift terms once \(N_a\) is no longer diagnostic-only.

## 8.4 Boundary flux

Need account for exchange through finite causal-slice boundaries.

## 8.5 Matter stress tensor

Need a real matter action / stress tensor, not only:

\[
\mathcal O_{\mathrm{mat}}
\]

as a scalar proxy.

## 8.6 Coefficients

Need microscopic derivation of:

\[
Z_R(\chi),\quad
V(R),\quad
\lambda_{\mathrm{int}}(\chi).
\]

---

# 9. Recommended next file

The next file should be:

```text
GRAPH_COVARIANT_DIVERGENCE.md
```

Purpose:

\[
\mathcal G_k,h_{ab}^{(k)},\mathcal S_{ab}^{\mathrm{mem},k}
\longmapsto
D^a\mathcal S_{ab}^{\mathrm{mem},k}.
\]

This replaces the simple finite-difference divergence proxy used in `MEMORY_EXCHANGE_CURRENT_ADM.md`.

---

# 10. Honest final status

> The Bianchi branch has advanced significantly. The interaction exchange channel is now proxy-closed because matter and memory exchange are derived from the same scalar interaction and cancel exactly. ADM memory stress projection, exchange currents, and total residual tests are verifier-backed. However, full covariant Bianchi conservation remains open.

**End of file.**
