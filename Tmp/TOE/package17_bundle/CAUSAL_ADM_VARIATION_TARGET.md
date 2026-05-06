# CAUSAL_ADM_VARIATION_TARGET.md

# Causal ADM Variation Target
## Finite-difference variational target for the causal-slice ADM action proxy

## Status
**Live derivation target. First proxy-variation pass. Not Einstein variation.**

`ADM_ACTION_WITH_GRAPH_CURVATURE.md` produced the strongest causal-slice geometric action proxy so far:

\[
S_{\mathrm{proxy}}^{(N,R_3)}
=
\sum_k
N_k\sqrt{\det h_k}
\left(
R^{(3)}_{\mathrm{graph},k}
+
K_{ab}K^{ab}
-
K^2
\right)\Delta k.
\]

This file attacks the next seam:

\[
\delta S_{\mathrm{proxy}}^{(N,R_3)}
\longmapsto
\text{discrete field-equation target}.
\]

This file does **not** claim to derive the Einstein equations.

It defines a finite-difference variational target and checks whether the proxy action has a stable discrete gradient with respect to spatial metric perturbations.

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

# 1. Action being varied

The proxy action is:

\[
S_{\mathrm{proxy}}^{(N,R_3)}
=
\sum_k
N_k\sqrt{\det h_k}
\left[
R^{(3)}_{\mathrm{graph},k}
+
\mathrm{Tr}(K^2)
-
(\mathrm{Tr}K)^2
\right]\Delta k.
\]

Current assumptions:

\[
N=N_k,
\qquad
N_a=0.
\]

The variation target is:

\[
\frac{\delta S_{\mathrm{proxy}}^{(N,R_3)}}{\delta h_{ab}^{(k)}}.
\]

---

# 2. Finite-difference variation

## Definition 1
For each slice \(k\), perturb:

\[
h_{ab}^{(k)}
\rightarrow
h_{ab}^{(k)}
+
\epsilon E_{ab},
\]

where \(E_{ab}\) is symmetric.

The finite-difference gradient is:

\[
\frac{
S[h+\epsilon E]-S[h-\epsilon E]
}{
2\epsilon
}.
\]

This defines a discrete Euler-response vector:

\[
\mathcal E_{ab}^{(k)}
\approx
\frac{\delta S_{\mathrm{proxy}}}{\delta h_{ab}^{(k)}}.
\]

---

# 3. What would count as closure?

## Derivation target A
A real closure step would require showing:

\[
\mathcal E_{ab}^{(k)}
=
0
\]

corresponds, under continuum limit, to ADM / Einstein equations.

This file does not do that.

It only verifies that \(\mathcal E_{ab}^{(k)}\) is:
- finite;
- nontrivial;
- stable under small perturbations;
- defined on positive-definite \(h_{ab}\).

---

# 4. Verifier implementation

## Status
**Implemented as `causal_adm_variation_target_verifier.py`. Execution log captured.**

The verifier uses synthetic positive-definite metric slices and computes finite-difference gradients.

It checks:

1. finite base action;
2. perturbed metrics remain positive definite;
3. finite gradient norm;
4. nontrivial variation response;
5. bounded gradient maximum.

## Captured verifier output

```text
Causal ADM variation target verifier
==================================================
Route:
finite-difference variation of S_proxy^(N,R3) with respect to h_ab slices
This is proxy variation, not Einstein variation.

PASS: 100.0
SOFT_FAIL: 0.0
HARD_FAIL: 0.0
action0_median: 28.155098086688078
grad_norm_median_median: 0.67397372229357
grad_norm_max_median: 1.5477056417511443
finite_fraction_median: 1.0
positive_definite_fraction_median: 1.0
nontrivial_fraction_median: 1.0
```

---

# 5. What this file establishes

### Established at current proof level

1. A proxy variation target is defined.
2. A finite-difference Euler-response vector is explicit.
3. The verifier shows the action proxy can be varied stably in sampled regimes.

### Not yet proved

1. The variation is not derived from the original causal graph variables.
2. \(R^{(3)}_{\mathrm{graph}}\) variation is held proxy-level.
3. Lapse variation is not included.
4. Shift variation is not included.
5. Boundary terms are absent.
6. No Einstein equation is derived.

---

# 6. Next derivation target

The next file should be:

```text
CAUSAL_ADM_FIELD_EQUATION_PROXY.md
```

Its job:

\[
\mathcal E_{ab}^{(k)}
=
0
\]

as a discrete field-equation proxy, including source terms from:

\[
T_{\mu\nu}^{\mathrm{mem}}.
\]

---

# Honest status line

> `CAUSAL_ADM_VARIATION_TARGET.md` defines and verifies a finite-difference variational target for the strongest causal-slice ADM action proxy. It is a stable proxy variation, not a derivation of Einstein's equations.

**End of file.**
