# CONSERVATION_WITH_BOUNDARY_FLUX.md

# Conservation With Boundary Flux
## ADM graph-proxy residual with interaction cancellation, graph divergence, and boundary flux

## Status
**Live derivation target. First combined conservation-with-boundary pass. Not covariant conservation closure.**

`BOUNDARY_FLUX_TERMS.md` added graph-boundary flux accounting for projected memory stress.

This file attacks:

\[
Q_{\mathrm{mem}}
+
Q_{\mathrm{mat}}
+
\Phi_{\partial A}
\approx0
\]

at ADM graph-proxy level.

The goal is to combine:
- exactly canceling interaction-channel exchange;
- graph-compatible interior divergence;
- boundary flux terms.

This file does **not** prove the covariant Bianchi identity.

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

# 1. Conservation structure

On a finite graph region, conservation requires interior exchange plus boundary flux accounting.

The proxy residual is:

\[
\mathcal C^{(k)}
=
Q_{\mathrm{mem}}^{(k)}
+
Q_{\mathrm{mat}}^{(k)}
+
\Phi_{\partial A}^{(k)}.
\]

The target is:

\[
\mathcal C^{(k)}
\approx0.
\]

At this proof level, \(\mathcal C^{(k)}\) is a diagnostic residual, not a covariant conservation theorem.

---

# 2. Interaction channel

The interaction channel is already proxy-closed:

\[
Q_{\mathrm{mat,int}}
+
Q_{\mathrm{mem,int}}
=
0.
\]

This file keeps that cancellation explicit and separates it from interior non-interaction stress divergence and boundary flux.

---

# 3. Interior graph divergence

The spatial memory exchange now uses graph-compatible divergence:

\[
Q_a^{\mathrm{mem}}(i)
\sim
(D^b_{\mathcal G}S_{ab})(i).
\]

This replaces arbitrary index finite differences.

---

# 4. Boundary flux

Boundary contribution is:

\[
\Phi_{\partial A}
=
\sum_{i\in\partial A}
w_i n_i^a S_{ab}(i)n_i^b.
\]

In the verifier, a vector boundary flux proxy is used:

\[
\Phi_b
\sim
\langle n^a S_{ab}\rangle_{\partial A}.
\]

---

# 5. Weak-memory scaling

## Lemma candidate 1
If:

\[
S_{ab}^{\mathrm{mem}}=O(\eta_{\mathrm{mem}}),
\]

then both graph divergence and boundary flux scale as:

\[
O(\eta_{\mathrm{mem}}).
\]

For kinetic-only stress:

\[
O(\eta_{\mathrm{mem}}^2).
\]

---

# 6. Verifier implementation

## Status
**Implemented as `conservation_with_boundary_flux_verifier.py`. Execution log captured.**

The verifier constructs:
- a graph-compatible interior divergence;
- derived interaction cancellation;
- graph-boundary flux;
- total ADM graph residual.

It checks:

1. exact interaction-channel cancellation;
2. finite boundary flux;
3. finite total residual;
4. \(O(\eta)\) scaling for interaction-dominated terms;
5. \(O(\eta^2)\) scaling for kinetic-only terms.

## Captured verifier output

```text
Conservation with boundary flux verifier
==================================================
Route:
interaction cancellation + graph divergence + boundary flux -> ADM graph residual
Checks finite residual and weak-memory scaling.

PASS: 89.2
SOFT_FAIL: 10.8
HARD_FAIL: 0.0
interaction_residual_ratio_median: 0.0
boundary_flux_norm_median: 1.0363461993860918e-05
total_residual_norm_median: 9.211580268481072e-05
total_half_ratio_median: 0.49891436334642714
kinetic_half_ratio_median: 0.2499999614841444
finite_fraction_median: 1.0
```

---

# 7. What this file establishes

### Established at current proof level

1. Interaction cancellation is integrated into the combined conservation residual.
2. Interior divergence uses graph geometry.
3. Boundary flux is included.
4. Weak-memory scaling remains correct.
5. The combined residual is finite.

### Not yet proved

1. \(\mathcal C^{(k)}=0\) is not enforced or derived.
2. Boundary flux is still heuristic.
3. Normal/lapse terms are incomplete.
4. Shift terms remain absent.
5. No graph Stokes theorem is proved.
6. No continuum Bianchi identity is proved.

---

# 8. Next derivation target

The next file should be:

```text
CONSERVATION_CLOSURE_STATUS_V2.md
```

Its job:
- audit interaction cancellation;
- graph divergence;
- boundary flux;
- combined residual;
- update the Bianchi closure status after boundary terms.

---

# Honest status line

> `CONSERVATION_WITH_BOUNDARY_FLUX.md` combines interaction-channel cancellation, graph-compatible interior divergence, and graph-boundary flux into one ADM graph-level conservation residual. It verifies finite weak-memory scaling, but it does not prove covariant conservation.

**End of file.**
