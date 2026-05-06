# GEOMETRIC_GR_OBLIGATIONS_REFOCUS.md

# Geometric GR Obligations Refocus
## Returning from the \(\chi\)-fixed-point seam to the actual GR continuum-limit spine

## Status
**Refocus document. Not a proof.**

`CHI_FIXED_POINT_STATUS_FINAL.md` froze the current \(\chi\)-fixed-point branch as:

```text
reachable and selection-plausible, but not derived
```

Therefore the GR derivation program should stop spending cycles trying to derive \(\chi\approx0.2667\) from the same micro-to-block/block-action map.

The memory/coefficient branch is useful, but bounded.

We now return to the geometric GR obligations:

\[
S_{\mathrm{proxy}}
\rightarrow
S_{\mathrm{ADM}}
\rightarrow
S_{\mathrm{EH}}
\rightarrow
G_{\mu\nu}=8\pi GT_{\mu\nu}.
\]

---

# 1. Current memory branch status

The memory branch has produced:

\[
m_R^2=1-a,
\]

\[
Z_R=
\chi(1-\chi)
\sigma_{\nabla\Lambda}^2
\left(\frac{dx}{dt}\right)^2,
\]

\[
\lambda_{\mathrm{int}}
=
\chi(1-\chi)\rho_{\mathrm{mat}}.
\]

But because:

\[
\chi\approx0.2667
\]

is not derived, the correct status is:

```text
micro-to-block constrained with selected χ regime
```

not:

```text
fully first-principles coefficient closure
```

This is enough to proceed with weak-memory corrections, but not enough to claim full derivation.

---

# 2. GR target spine

The standard GR variational target is:

\[
S_{\mathrm{EH}}
=
\frac{1}{16\pi G}
\int d^4x\sqrt{-g}\,R.
\]

With matter:

\[
S=
S_{\mathrm{EH}}+S_{\mathrm{mat}}.
\]

Variation gives:

\[
G_{\mu\nu}=8\pi G T_{\mu\nu}.
\]

The framework must show that the discrete/proxy action converges to this spine.

---

# 3. Current geometric branch

The current geometric branch includes:

```text
CAUSAL_ORDER_DERIVATION.md
CAUSAL_INTERVAL_GEOMETRY.md
CAUSAL_SET_RECONSTRUCTION.md
ANTICHAIN_SPATIAL_GEOMETRY.md
ANTICHAIN_GRAPH_METRIC.md
CAUSAL_SLICE_LORENTZIAN_METRIC.md
LAPSE_SHIFT_DERIVATION.md
LAPSE_SHIFT_CLOSURE_STATUS.md
SPATIAL_GRAPH_CURVATURE.md
ADM_ACTION_WITH_GRAPH_CURVATURE.md
ADM_ACTION_WITH_LAPSE.md
CAUSAL_ADM_VARIATION_TARGET.md
CAUSAL_ADM_FIELD_EQUATION_PROXY.md
```

This branch has produced a verifier-backed ADM-like proxy, but not GR.

---

# 4. Remaining hard GR obligations

## Obligation 1: geometric action convergence

Current object:

\[
S_{\mathrm{proxy}}^{(N,R_3)}
=
\sum_k
N_k\sqrt{\det h_k}
\left[
R_{\mathrm{graph},k}^{(3)}
+
K_{ab}K^{ab}
-
K^2
\right]\Delta k.
\]

Needed:

\[
S_{\mathrm{proxy}}^{(N,R_3)}
\rightarrow
S_{\mathrm{ADM}}.
\]

Then:

\[
S_{\mathrm{ADM}}
\rightarrow
S_{\mathrm{EH}}
\]

up to boundary terms.

Status:

```text
open
```

---

## Obligation 2: curvature convergence

Current object:

\[
R_{\mathrm{graph}}^{(3)}.
\]

Needed:

\[
R_{\mathrm{graph}}^{(3)}
\rightarrow
R^{(3)}.
\]

Then ADM identity:

\[
R^{(4)}
=
R^{(3)}
+
K_{ab}K^{ab}
-
K^2
+
\text{boundary terms}.
\]

Status:

```text
open
```

---

## Obligation 3: physical causal time

Current object:

```text
causal/update order
```

Needed:

```text
microscopic update order -> physical causal time
```

or at least:

```text
causal slicing parameter -> ADM time up to lapse normalization
```

Status:

```text
open
```

---

## Obligation 4: shift vector

Current status:

```text
N_a diagnostic-only / not closed
```

Needed:

\[
ds^2
=
-N^2dt^2
+
h_{ab}(dx^a+N^adt)(dx^b+N^bdt).
\]

Status:

```text
open
```

---

## Obligation 5: covariant Bianchi conservation

Current branch:

```text
ADM graph-level conservation proxies
interaction-channel cancellation
graph divergence
boundary flux
```

Needed:

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

Status:

```text
open
```

---

# 5. Ranked next geometric targets

## Rank 1: graph-to-continuum curvature convergence

Next file:

```text
GRAPH_TO_CONTINUUM_CURVATURE_LIMIT.md
```

Why first:

The ADM action cannot converge to GR unless:

\[
R_{\mathrm{graph}}^{(3)}
\rightarrow
R^{(3)}.
\]

This is the most direct geometric blocker.

---

## Rank 2: ADM/EH action convergence

Next file after curvature:

```text
ADM_TO_EH_ACTION_LIMIT.md
```

Purpose:

\[
\sum_k
N_k\sqrt{h}
\left[
R^{(3)}
+
K_{ab}K^{ab}
-
K^2
\right]
\rightarrow
\int d^4x\sqrt{-g}R^{(4)}.
\]

---

## Rank 3: physical causal time

Next file:

```text
PHYSICAL_CAUSAL_TIME.md
```

Purpose:

Show why causal/update order can play ADM time.

---

## Rank 4: shift vector closure

Next file:

```text
SHIFT_VECTOR_FIELD.md
```

Purpose:

Derive or constrain \(N_a\).

---

## Rank 5: covariant Bianchi closure

Next file:

```text
COVARIANT_BIANCHI_CLOSURE.md
```

Purpose:

Upgrade ADM graph conservation proxies to covariant conservation.

---

# 6. Recommended immediate next file

The highest-value next file is:

```text
GRAPH_TO_CONTINUUM_CURVATURE_LIMIT.md
```

It should answer:

\[
R_{\mathrm{graph}}^{(3)}
\longrightarrow
R^{(3)}
?
\]

This is the correct next hard GR seam.

---

# 7. What not to do next

Do not keep chasing:

```text
χ≈0.2667
```

inside the same block-action map.

That branch has been honestly bounded.

Do not create more selection-principle variants unless a genuinely new microscopic term is introduced.

Do not claim:

```text
GR is derived
```

until geometric action convergence is shown.

---

# 8. Safe current claim

Use:

```text
The memory/coefficient branch is now bounded: χ≈0.2667 is reachable and selection-plausible but not derived. We are now returning to the geometric GR obligations, starting with graph-curvature convergence.
```

---

# 9. Report-out language

```text
Milestone: χ seam frozen honestly.

The target fixed point is reachable and selection-plausible, but the current block-action route does not derive it.

So we stop looping there.

Next hard GR seam: graph curvature must converge to continuum spatial curvature.

Back to the spine:
S_proxy -> S_ADM -> S_EH.
```

---

# Honest final status

> `GEOMETRIC_GR_OBLIGATIONS_REFOCUS.md` freezes the \(\chi\)-selection branch as bounded and redirects the GR derivation program to the geometric action-convergence spine. The next decisive file is `GRAPH_TO_CONTINUUM_CURVATURE_LIMIT.md`.

**End of file.**
