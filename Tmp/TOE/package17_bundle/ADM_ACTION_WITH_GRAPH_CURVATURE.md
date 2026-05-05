# ADM_ACTION_WITH_GRAPH_CURVATURE.md

# ADM Action With Graph Curvature
## Integration of measured lapse and explicit spatial graph curvature into causal-slice ADM proxy

## Status
**Live derivation target. First measured-lapse + graph-curvature ADM action pass. Not Einstein-Hilbert closed.**

`ADM_ACTION_WITH_LAPSE.md` safely upgraded the action proxy from fixed lapse:

\[
N=1
\]

to measured lapse:

\[
N=N_k.
\]

`SPATIAL_GRAPH_CURVATURE.md` replaced the spectral \(R^{(3)}\) placeholder with explicit graph-curvature proxies.

This file integrates both:

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
\right)
\Delta k.
\]

The shift remains:

\[
N_a=0
\]

in the main branch. Aligned shift remains diagnostic-only.

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

# 1. Ingredients

The action now uses:

1. antichain spatial metric proxy:
   \[
   h_{ab}^{(k)};
   \]

2. measured lapse:
   \[
   N_k;
   \]

3. zero shift:
   \[
   N_a=0;
   \]

4. finite-difference extrinsic curvature:
   \[
   K_{ab}^{(k)}
   =
   \frac{1}{2N_k}\dot h_{ab}^{(k)};
   \]

5. explicit spatial graph curvature:
   \[
   R^{(3)}_{\mathrm{graph},k}.
   \]

---

# 2. Graph-curvature scalar

## Definition 1
From `SPATIAL_GRAPH_CURVATURE.md`:

\[
R^{(3)}_{\mathrm{graph},k}
=
\langle O_{ij}\rangle
+
\frac{\langle F_{ij}\rangle}{|E_k|},
\]

where:

\[
F_{ij}
=
(4-\deg(i)-\deg(j))W_{ij},
\]

and:

\[
O_{ij}
=
\frac{|N(i)\cap N(j)|}{|N(i)\cup N(j)|}.
\]

This is graph-native but not continuum \(R^{(3)}\).

---

# 3. ADM-like action with measured lapse and graph curvature

## Definition 2
The upgraded ADM-like proxy is:

\[
S_{\mathrm{proxy}}^{(N,R_3)}
=
\sum_k
N_k
\sqrt{\det h_k}
\left[
R^{(3)}_{\mathrm{graph},k}
+
\mathrm{Tr}(K^2)
-
(\mathrm{Tr}K)^2
\right]
\Delta k.
\]

This is the strongest causal-slice geometric action proxy so far.

## Failure condition 1
If graph curvature destabilizes the action, the graph \(R^{(3)}\) proxy cannot replace the spectral placeholder.

---

# 4. Verifier implementation

## Status
**Implemented as `adm_action_with_graph_curvature_verifier.py`. Execution log captured.**

The verifier compares:

\[
S_{\mathrm{proxy}}^{(N,R_3)}
\]

against the prior measured-lapse spectral action.

It checks:

1. enough valid metric slices;
2. finite measured lapse;
3. finite graph \(R^{(3)}\);
4. finite action;
5. controlled ratio to spectral-placeholder action;
6. no action blow-up.

## Captured verifier output

```text
ADM action with graph curvature verifier
==================================================
Route:
measured lapse + explicit R3_graph -> ADM-like action proxy
main branch keeps N_a=0; not full ADM/EH convergence

PASS: 86.0
SOFT_FAIL: 0.0
HARD_FAIL: 14.0
n_slices_median: 9.0
lapse_median_median: 0.9999999999995073
lapse_cv_median: 0.0367625773546524
R3_graph_median_median: 0.2643796148801645
action_graph_abs_median: 879.9853498689251
action_spectral_abs_median: 1758.4425220873677
action_ratio_median: 0.61009408526721
finite_fraction_median: 1.0
```

---

# 5. What this file establishes

### Established at current proof level

1. The causal-slice ADM proxy now includes measured lapse.
2. The spatial curvature term is graph-native rather than purely spectral.
3. The action remains finite and testable.
4. The verifier compares graph-curvature and spectral-placeholder actions.

### Not yet proved

1. \(R^{(3)}_{\mathrm{graph}}\) is not continuum spatial curvature.
2. \(N_a\) is still excluded from the main branch.
3. Boundary terms are absent.
4. The action is not yet varied.
5. Einstein-Hilbert convergence is not shown.
6. Matter/memory coupling is not included.

---

# 6. Updated proof-chain status

The causal-slice geometric action branch is now:

```text
ANTICHAIN_GRAPH_METRIC.md
        ↓
LAPSE_SHIFT_CLOSURE_STATUS.md
        ↓
SPATIAL_GRAPH_CURVATURE.md
        ↓
ADM_ACTION_WITH_GRAPH_CURVATURE.md
        ↓
EINSTEIN_HILBERT_LIMIT.md
```

---

# 7. Next derivation target

The next file should be:

```text
CAUSAL_ADM_VARIATION_TARGET.md
```

Its job:

\[
\delta S_{\mathrm{proxy}}^{(N,R_3)}
\longmapsto
\text{discrete field-equation target}
\]

while honestly distinguishing proxy variation from true Einstein variation.

---

# Honest status line

> `ADM_ACTION_WITH_GRAPH_CURVATURE.md` is the strongest causal-slice geometric action proxy so far: it combines measured lapse, antichain spatial metric, graph-native spatial curvature, and extrinsic-curvature terms. It remains proxy-level and does not yet prove ADM or Einstein-Hilbert convergence.

**End of file.**
