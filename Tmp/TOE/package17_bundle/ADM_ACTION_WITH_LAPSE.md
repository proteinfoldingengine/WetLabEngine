# ADM_ACTION_WITH_LAPSE.md

# ADM Action With Measured Lapse
## Upgrade of causal-slice ADM proxy from fixed lapse to measured lapse

## Status
**Live derivation target. First measured-lapse ADM action pass. Shift remains excluded from closure.**

`LAPSE_SHIFT_CLOSURE_STATUS.md` concluded:

```text
Use measured N_k in the main ADM proxy.
Keep N_a = 0 in the main ADM proxy.
Log aligned N_a as diagnostic only.
```

This file upgrades:

\[
N=1
\]

to:

\[
N=N_k
\]

inside the ADM-like action proxy.

This file does **not** derive full ADM or Einstein-Hilbert convergence. It tests whether measured lapse destabilizes or improves the finite action proxy.

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

# 1. Prior ADM proxy

`ADM_CAUSAL_SLICE_ACTION.md` used:

\[
S_{\mathrm{proxy}}
=
\sum_k
\sqrt{\det h_k}
\left(
R^{(3)}_{\mathrm{proxy},k}
+
K_{ab}^{(k)}K^{ab}_{(k)}
-
K_k^2
\right).
\]

with first-pass assumptions:

\[
N=1,
\qquad
N_a=0.
\]

---

# 2. Measured lapse

## Definition 1
Let:

\[
V_k=|A_k|
\]

be antichain slice volume proxy and:

\[
\bar V=\mathrm{median}_k(V_k).
\]

Define centered measured lapse:

\[
N_k
=
\frac{1}
{\sqrt{
(V_{k-1}+V_k+V_{k+1})/(3\bar V)
}}.
\]

This normalizes causal-rank spacing by local slice density.

## Observation
For uniform slices:

\[
V_k\approx\bar V
\quad\Rightarrow\quad
N_k\approx1.
\]

For denser slices:

\[
N_k<1.
\]

For sparser slices:

\[
N_k>1.
\]

---

# 3. ADM action with measured lapse

## Definition 2
The measured-lapse action proxy is:

\[
S_{\mathrm{proxy}}^{(N)}
=
\sum_k
N_k\sqrt{\det h_k}
\left(
R^{(3)}_{\mathrm{proxy},k}
+
K_{ab}^{(k)}K^{ab}_{(k)}
-
K_k^2
\right)
\Delta k.
\]

The extrinsic curvature proxy now includes lapse:

\[
K_{ab}^{(k)}
=
\frac{1}{2N_k}
\dot h_{ab}^{(k)}.
\]

The main branch still uses:

\[
N_a=0.
\]

---

# 4. Shift policy

## Observation
`SLICE_ALIGNMENT_AND_SHIFT.md` improved shift structure but did not close it.

Therefore:

```text
Aligned N_a is diagnostic-only.
```

It should not enter the main ADM action used for closure claims.

## Failure condition 1
If the action only stabilizes when diagnostic shift is included, then the main ADM proxy is not closed.

---

# 5. Verifier implementation

## Status
**Implemented as `adm_action_with_lapse_verifier.py`. Execution log captured.**

The verifier compares:

\[
S_{\mathrm{fixed}}
\]

using \(N=1\), against:

\[
S_N
\]

using measured \(N_k\).

It checks:

1. finite measured lapse;
2. low lapse variation;
3. finite action with measured lapse;
4. controlled ratio:
   \[
   \frac{|S_N|}{|S_{\mathrm{fixed}}|};
   \]
5. no action blow-up from lapse normalization.

## Captured verifier output

```text
ADM action with measured lapse verifier
==================================================
Route:
replace fixed N=1 with measured N_k from causal rank/slice density
main branch keeps N_a=0; aligned shift remains diagnostic-only

PASS: 94.0
SOFT_FAIL: 0.0
HARD_FAIL: 6.0
n_slices_median: 8.0
lapse_median_median: 1.003458747156299
lapse_cv_median: 0.03932362339741718
fixed_action_abs_median: 1761.3451410870189
lapse_action_abs_median: 1784.7064889599249
action_ratio_median: 1.0038791499625725
finite_fraction_median: 1.0
```

---

# 6. What this file establishes

### Established at current proof level

1. The ADM proxy now uses measured lapse.
2. The measured lapse is tied to causal slice density.
3. \(K_{ab}\) is updated to include \(1/N_k\).
4. The verifier checks whether the measured-lapse action remains finite and controlled.

### Not yet proved

1. Lapse normalization is not uniquely derived.
2. Shift remains excluded from the main action.
3. \(R^{(3)}\) is still a spectral proxy.
4. Boundary terms are not included.
5. The action is not yet variationally derived.
6. Einstein-Hilbert convergence is not shown.

---

# 7. Updated proof-chain status

The ADM causal-slice action chain is now:

```text
CAUSAL_SLICE_CURVATURE.md
        ↓
LAPSE_SHIFT_CLOSURE_STATUS.md
        ↓
ADM_ACTION_WITH_LAPSE.md
        ↓
EINSTEIN_HILBERT_LIMIT.md
```

---

# 8. Next derivation target

The next file should be:

```text
SPATIAL_GRAPH_CURVATURE.md
```

Its job:

\[
\mathcal G_k,h_{ab}^{(k)}
\longmapsto
R^{(3)}_k
\]

replacing the spectral placeholder with a true spatial graph curvature estimator.

---

# Honest status line

> `ADM_ACTION_WITH_LAPSE.md` safely upgrades the main ADM-like causal-slice action from fixed \(N=1\) to measured \(N_k\), while keeping shift diagnostic-only. This strengthens the action proxy but does not yet derive full ADM or Einstein-Hilbert convergence.

**End of file.**
