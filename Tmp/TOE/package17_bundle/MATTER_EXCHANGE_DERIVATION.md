# MATTER_EXCHANGE_DERIVATION.md

# Matter Exchange Derivation
## Deriving the matter-side exchange proxy from the memory-matter interaction term

## Status
**Live derivation target. First derived matter-exchange pass. Not full covariant conservation.**

`Bianchi_ADM_CONSERVATION_PROXY.md` constructed matter exchange as:

\[
Q_{\mathrm{mat}}^{(k)}
=
-
Q_{\mathrm{mem}}^{(k)}
+
\delta Q^{(k)}.
\]

That was useful for testing controlled total residuals, but it was not a derivation.

This file attacks the next seam:

\[
\lambda_{\mathrm{int}}R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
\longmapsto
Q_\nu^{\mathrm{mat}}.
\]

The goal is to derive a matter-side exchange proxy from the interaction term itself.

This file does **not** prove covariant conservation. It defines and verifies the first ADM-level matter exchange from the scalar interaction.

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

# 1. Interaction term

The scalar-density memory action includes:

\[
S_{\mathrm{int}}
=
\int d^4x\,\sqrt{-g}\,
\lambda_{\mathrm{int}}R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}.
\]

This term permits controlled matter-memory energy-momentum exchange.

---

# 2. Matter exchange proxy

## Definition 1
For scalar coupling, the first exchange-current proxy is:

\[
Q_\nu^{\mathrm{mat}}
\sim
\lambda_{\mathrm{int}}\mathcal O_{\mathrm{mat}}
\nabla_\nu R_{\mathrm{eff}}.
\]

The sign depends on the stress-energy convention and whether \(Q_\nu\) is defined as matter gain or memory loss.

The interaction part of the memory exchange should be equal and opposite:

\[
Q_\nu^{\mathrm{mem,int}}
\sim
-
\lambda_{\mathrm{int}}\mathcal O_{\mathrm{mat}}
\nabla_\nu R_{\mathrm{eff}}.
\]

---

# 3. ADM projection

## Definition 2
Normal exchange:

\[
Q_\perp^{\mathrm{mat}}
\sim
\lambda_{\mathrm{int}}
\mathcal O_{\mathrm{mat}}
\partial_\tau R_{\mathrm{eff}}.
\]

Spatial exchange:

\[
Q_a^{\mathrm{mat}}
\sim
\lambda_{\mathrm{int}}
\mathcal O_{\mathrm{mat}}
\partial_a R_{\mathrm{eff}}.
\]

Thus:

\[
Q_{\mathrm{mat}}^{(k)}
=
\left(
Q_\perp^{\mathrm{mat},k},
Q_a^{\mathrm{mat},k}
\right).
\]

---

# 4. Weak-memory scaling

## Lemma candidate 1
If:

\[
R_{\mathrm{eff}}
=
\eta_{\mathrm{mem}}r,
\]

then:

\[
\nabla_\nu R_{\mathrm{eff}}
=
O(\eta_{\mathrm{mem}}),
\]

and therefore:

\[
Q_\nu^{\mathrm{mat}}
=
O(\eta_{\mathrm{mem}}),
\]

provided \(\lambda_{\mathrm{int}}\) and \(\mathcal O_{\mathrm{mat}}\) remain bounded.

Thus:

\[
\frac{\|Q_{\mathrm{mat}}(\eta/2)\|}
{\|Q_{\mathrm{mat}}(\eta)\|}
\approx
\frac12.
\]

---

# 5. Verifier implementation

## Status
**Implemented as `matter_exchange_derivation_verifier.py`. Execution log captured.**

The verifier constructs:
- weak memory field \(R_{\mathrm{eff}}=\eta r\);
- normal derivative \(\partial_\tau R_{\mathrm{eff}}\);
- spatial gradient \(\partial_aR_{\mathrm{eff}}\);
- bounded matter operator proxy \(\mathcal O_{\mathrm{mat}}\);
- matter exchange \(Q_{\mathrm{mat}}\);
- interaction memory exchange \(Q_{\mathrm{mem,int}}\).

It checks:

1. finite derived matter exchange;
2. \(O(\eta)\) scaling;
3. cancellation with interaction memory exchange under consistent sign convention;
4. no singular failures.

## Captured verifier output

```text
Matter exchange derivation verifier
==================================================
Route:
L_int = lambda R_eff O_mat -> Q_mat ADM proxy
Checks O(eta) scaling and cancellation with interaction memory exchange.

PASS: 100.0
SOFT_FAIL: 0.0
HARD_FAIL: 0.0
q_mat_norm_median_median: 4.2702961654984524e-05
q_mat_half_ratio_median: 0.4999999882889808
q_mem_int_norm_median_median: 4.2702961654984524e-05
best_residual_ratio_median: 0.0
finite_fraction_median: 1.0
```

---

# 6. What this file establishes

### Established at current proof level

1. Matter exchange is no longer merely imposed as \(-Q_{\mathrm{mem}}\).
2. A first exchange proxy is derived from \(\lambda R\mathcal O_{\mathrm{mat}}\).
3. ADM normal and spatial components are explicit.
4. Weak-memory scaling is verified.
5. The interaction component cancels the memory interaction exchange under consistent sign convention.

### Not yet proved

1. This is not full covariant \(\nabla^\mu T_{\mu\nu}^{\mathrm{mat}}\).
2. \(\mathcal O_{\mathrm{mat}}\) is not specified microscopically.
3. The sign convention must be fixed in the final action convention.
4. Graph-covariant derivatives are not implemented.
5. Boundary flux terms are not included.
6. Full Bianchi conservation remains open.

---

# 7. Integration into Bianchi proxy

The prior constructed exchange:

\[
Q_{\mathrm{mat}}
=
-
Q_{\mathrm{mem}}
+
\delta Q
\]

can now be replaced, for the interaction channel, by:

\[
Q_\nu^{\mathrm{mat,int}}
=
\lambda_{\mathrm{int}}\mathcal O_{\mathrm{mat}}
\nabla_\nu R_{\mathrm{eff}}.
\]

This strengthens `Bianchi_ADM_CONSERVATION_PROXY.md`.

---

# 8. Next derivation target

The next file should be:

```text
Bianchi_INTERACTION_CHANNEL.md
```

Its job:

\[
Q_\nu^{\mathrm{mat,int}}
+
Q_\nu^{\mathrm{mem,int}}
=
0
\]

using both sides derived from the same interaction term.

---

# Honest status line

> `MATTER_EXCHANGE_DERIVATION.md` derives the first ADM matter-exchange proxy from the scalar memory-matter interaction term and verifies \(O(\eta)\) scaling. It improves the Bianchi proxy but does not yet prove covariant conservation.

**End of file.**
