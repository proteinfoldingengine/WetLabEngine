# CONTINUUM_LIMIT_REPO_UPDATE.md

# Continuum Limit Repo Update
## Repo-ready replacement sections for `CONTINUUM_LIMIT.md`

## Status
**Repo update draft. Not a proof.**

This file provides copy-ready replacement/addition sections for `CONTINUUM_LIMIT.md` after the causal ADM branch was expanded, tested, corrected, and reintegrated.

It incorporates:

- the failed naive order-distance embedding branch;
- the corrected causal-set / antichain branch;
- measured lapse;
- diagnostic-only shift;
- graph-native spatial curvature;
- ADM-like action proxy;
- finite-difference variation target;
- weak-memory field-equation proxy;
- updated honest status language.

This update does **not** close seam 3.

---

# 1. Recommended top-of-file status replacement

Replace the current status paragraph in `CONTINUUM_LIMIT.md` with:

```markdown
## Status
**Verifier-backed derivation program. Not yet closed.**

This file has been upgraded from a schematic continuum-limit blueprint into a decomposed, verifier-backed derivation program.

The original scalar-density memory-action route remains active. In addition, the emergent metric/action seam has been expanded into a corrected causal-slice ADM branch.

Important status:

- A naive order-distance embedding route was tested and failed.
- The corrected route uses causal order, longest-chain time, antichain spatial slices, causal-profile spatial adjacency, graph-derived spatial metric proxies, measured lapse, graph-native spatial curvature, and an ADM-like action proxy.
- The branch now includes a finite-difference variation target and a weak-memory field-equation proxy.
- These are structural/verifier-backed candidates, not a derivation of GR.

Seam 3 remains **not closed** because physical time, continuum spatial curvature, shift, ADM/EH convergence, covariance, and exact memory stress-energy remain open.
```

---

# 2. Add new section: corrected causal branch

Insert after the current coarse-graining / emergent metric discussion.

```markdown
# Corrected causal-slice branch for metric/action emergence

## Status
**Verifier-backed candidate branch. Not continuum-GR closed.**

The original continuum-limit target required:

\[
\text{discrete structure}
\rightarrow
g_{\mu\nu}
\rightarrow
R_{\mu\nu},R
\rightarrow
S_{\mathrm{EH}}.
\]

This has now been decomposed into a causal-slice branch:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_INTERVAL_GEOMETRY.md
        ↓
ORDER_DISTANCE_FAILURE_ANALYSIS.md
        ↓
CAUSAL_SET_RECONSTRUCTION.md
        ↓
ANTICHAIN_SPATIAL_GEOMETRY.md
        ↓
ANTICHAIN_GRAPH_METRIC.md
        ↓
CAUSAL_SLICE_LORENTZIAN_METRIC.md
        ↓
CAUSAL_SLICE_CURVATURE.md
        ↓
LAPSE_SHIFT_DERIVATION.md
        ↓
SLICE_ALIGNMENT_AND_SHIFT.md
        ↓
LAPSE_SHIFT_CLOSURE_STATUS.md
        ↓
ADM_ACTION_WITH_LAPSE.md
        ↓
SPATIAL_GRAPH_CURVATURE.md
        ↓
ADM_ACTION_WITH_GRAPH_CURVATURE.md
        ↓
CAUSAL_ADM_VARIATION_TARGET.md
        ↓
CAUSAL_ADM_FIELD_EQUATION_PROXY.md
```

This branch is stronger than the earlier schematic assumption “an emergent metric exists,” but it remains proxy-level.
```

---

# 3. Add new section: failed branch note

Insert immediately after the corrected branch.

```markdown
# Failed branch: naive order-distance embedding

## Status
**Falsified route. Retained for proof discipline.**

The tempting route:

\[
\text{causal interval cardinality}
\rightarrow
d_{\mathrm{ord}}
\rightarrow
\text{MDS embedding}
\rightarrow
g_{\mu\nu}
\]

was tested in:

```text
ORDER_DISTANCE_EMBEDDING.md
```

and failed:

```text
PASS: 0.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 100.0%
```

The diagnostic file:

```text
ORDER_DISTANCE_FAILURE_ANALYSIS.md
```

identified the reason:

- causal comparability is timelike and sparse;
- interval cardinality is volume-like, not a complete metric distance;
- spacelike distances are missing;
- Euclidean MDS is the wrong first reconstruction method.

Therefore the repo explicitly pivots to the causal-set / antichain route. This failed branch should remain documented and should not be removed.
```

---

# 4. Replace emergent metric assumption section

Replace any older statement equivalent to:

```text
Assume a Lorentzian metric g_mu_nu emerges.
```

with:

```markdown
# Emergent metric candidate

## Status
**Verifier-backed local candidate. Not fully derived.**

A local Lorentzian metric candidate is now built from:

1. causal rank / longest-chain depth as time;
2. antichain graph geometry as spatial metric;
3. measured lapse \(N_k\);
4. zero main-branch shift \(N_a=0\).

The local metric candidate is:

\[
g_{\mu\nu}^{(k)}
=
\begin{pmatrix}
-N_k^2 & 0 \\
0 & h_{ab}^{(k)}
\end{pmatrix}.
\]

Here:

\[
h_{ab}^{(k)}
\]

is obtained from antichain spatial graph embeddings, and:

\[
N_k
=
\frac{1}
{\sqrt{(V_{k-1}+V_k+V_{k+1})/(3\bar V)}}.
\]

Verifier status:

```text
CAUSAL_SLICE_LORENTZIAN_METRIC.md:
PASS: 78.75%
SOFT_FAIL: 13.75%
HARD_FAIL: 7.5%

LAPSE_SHIFT_DERIVATION.md:
PASS: 93.33%
SOFT_FAIL: 0.0%
HARD_FAIL: 6.67%
```

Important limitation:

\[
N_a
\]

is not closed. The aligned shift is diagnostic-only.
```

---

# 5. Replace spatial curvature placeholder section

Replace older spectral-only spatial curvature language with:

```markdown
# Spatial curvature candidate

## Status
**Graph-curvature proxy. Not continuum \(R^{(3)}\).**

The spatial curvature term is no longer only a spectral placeholder.

A graph-native spatial curvature proxy is defined in:

```text
SPATIAL_GRAPH_CURVATURE.md
```

using:

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

The scalar proxy is:

\[
R^{(3)}_{\mathrm{graph},k}
=
\langle O_{ij}\rangle
+
\frac{\langle F_{ij}\rangle}{|E_k|}.
\]

Verifier status:

```text
PASS: 90.0%
SOFT_FAIL: 1.67%
HARD_FAIL: 8.33%
```

This strengthens the spatial-curvature ingredient, but it is still not continuum \(R^{(3)}\).
```

---

# 6. Replace ADM/action section

Replace older schematic action language with:

```markdown
# Causal ADM-like action proxy

## Status
**Verifier-backed action proxy. Not Einstein-Hilbert action.**

The strongest current geometric action proxy is:

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

where:

\[
K_{ab}^{(k)}
=
\frac{1}{2N_k}\dot h_{ab}^{(k)}.
\]

The main branch uses:

\[
N_a=0.
\]

The aligned shift proxy is logged only as a diagnostic and is not used for closure claims.

Verifier status:

```text
ADM_ACTION_WITH_GRAPH_CURVATURE.md:
PASS: 86.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 14.0%
```

Key diagnostic:

```text
action_ratio_median: 0.6101
finite_fraction_median: 1.0
```

Interpretation:

The measured-lapse + graph-curvature ADM proxy is finite and controlled, but it is not yet the Einstein-Hilbert action.
```

---

# 7. Add variation section

Insert after the ADM/action section.

```markdown
# Finite-difference variation target

## Status
**Verifier-backed proxy variation. Not Einstein variation.**

A finite-difference Euler-response target is defined in:

```text
CAUSAL_ADM_VARIATION_TARGET.md
```

\[
\mathcal E_{ab}^{(k)}
\approx
\frac{\delta S_{\mathrm{proxy}}^{(N,R_3)}}{\delta h_{ab}^{(k)}}.
\]

Verifier status:

```text
PASS: 100.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 0.0%
```

Key diagnostics:

```text
grad_norm_median: 0.674
grad_norm_max_median: 1.548
finite_fraction_median: 1.0
positive_definite_fraction_median: 1.0
nontrivial_fraction_median: 1.0
```

This proves only that the proxy action has a stable finite-difference response. It does not derive ADM or Einstein equations.
```

---

# 8. Add field-equation proxy section

Insert after the variation section.

```markdown
# Discrete field-equation proxy with weak-memory source

## Status
**Verifier-backed source-coupling proxy. Not Einstein equation.**

The discrete proxy equation is:

\[
\mathcal E_{ab}^{(k)}
=
\mathcal S_{ab}^{\mathrm{mem},k}.
\]

The weak-memory source is:

\[
\mathcal S_{ab}^{\mathrm{mem},k}
=
O(\eta_{\mathrm{mem}}).
\]

Verifier status:

```text
CAUSAL_ADM_FIELD_EQUATION_PROXY.md:
PASS: 100.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 0.0%
```

Key diagnostics:

```text
euler_norm_median: 0.6801
source_norm_median: 0.00117
source_to_euler_ratio: 0.00161
weak_scaling_ratio: 0.5000
finite_fraction_median: 1.0
```

Interpretation:

The weak-memory source scales correctly and can be coupled to the proxy Euler response without singular behavior.

This is not:

\[
G_{\mu\nu}=8\pi T_{\mu\nu}.
\]
```

---

# 9. Updated closure table for CONTINUUM_LIMIT.md

Add or replace the status matrix with:

```markdown
# Updated seam status matrix

| Component | Current status | Evidence | Main limitation |
|---|---:|---|---|
| Causal order | Verifier-backed candidate | `CAUSAL_ORDER_DERIVATION.md` | Update order not proven physical time |
| Interval geometry | Verifier-backed / partly coordinate-assisted | `CAUSAL_INTERVAL_GEOMETRY.md` | Dimension not fully coordinate-free |
| Naive order embedding | Failed | `ORDER_DISTANCE_EMBEDDING.md` | Causal distance not full metric distance |
| Causal-set reconstruction | Verifier-backed candidate | `CAUSAL_SET_RECONSTRUCTION.md` | Manifoldlikeness not proven |
| Antichain spatial graph | Verifier-backed candidate | `ANTICHAIN_SPATIAL_GEOMETRY.md` | Spatial metric still graph-derived |
| Spatial metric proxy | Verifier-backed candidate | `ANTICHAIN_GRAPH_METRIC.md` | Graph embedding/gauge dependence |
| Lorentzian metric proxy | Verifier-backed candidate | `CAUSAL_SLICE_LORENTZIAN_METRIC.md` | Shift not closed |
| Lapse | Verifier-backed candidate | `LAPSE_SHIFT_CLOSURE_STATUS.md` | Normalization not unique |
| Shift | Diagnostic-only | `SLICE_ALIGNMENT_AND_SHIFT.md` | Not physical/covariant |
| Spatial curvature | Graph proxy | `SPATIAL_GRAPH_CURVATURE.md` | Not continuum \(R^{(3)}\) |
| ADM action | Verifier-backed proxy | `ADM_ACTION_WITH_GRAPH_CURVATURE.md` | Not EH action |
| Variation | Verifier-backed proxy | `CAUSAL_ADM_VARIATION_TARGET.md` | Not Einstein variation |
| Field-equation proxy | Verifier-backed proxy | `CAUSAL_ADM_FIELD_EQUATION_PROXY.md` | Not Einstein equation |
| Full continuum GR limit | Not closed | all above | EH/covariance/source closure open |
```

---

# 10. Updated honest status line

Replace the prior honest status line with:

```markdown
## Honest status line

> `CONTINUUM_LIMIT.md` has been upgraded into a verifier-backed continuum-limit derivation program. The causal branch now includes a corrected causal-set reconstruction route, a documented failed embedding route, antichain-derived spatial metric proxies, measured lapse, graph-native spatial curvature, an ADM-like action proxy, stable finite-difference variation, and a weak-memory field-equation proxy. These results significantly reduce ambiguity, but they remain proxy-level. The file does not derive GR, the Einstein-Hilbert action, or Einstein's field equations.
```

---

# 11. Updated bottom line

Replace the prior bottom line with:

```markdown
## Bottom line

Seam 3 is now far stronger than a blueprint.

It contains:
- explicit memory-action candidates;
- coefficient/verifier scaffolds;
- corrected causal-order reconstruction;
- documented failure of naive metric embedding;
- antichain spatial geometry;
- local Lorentzian metric proxy;
- measured lapse;
- graph-curvature spatial term;
- ADM-like action proxy;
- finite-difference variation target;
- weak-memory source coupling.

But seam 3 remains **not closed**.

The remaining hard blockers are:

1. physical derivation of causal time from microscopic update order;
2. coordinate-free dimension / manifoldlikeness;
3. covariant shift \(N_a\);
4. continuum spatial curvature \(R^{(3)}\);
5. ADM/EH convergence;
6. variational closure to ADM/Einstein equations;
7. exact \(T_{\mu\nu}^{\mathrm{mem}}\) coupling;
8. boundary terms and covariance.

The correct public claim is:

> The continuum-limit seam has been decomposed into a falsifiable, verifier-backed derivation program with several successful proxy constructions and one important falsified route. It is not yet a derivation of GR.
```

---

# 12. Recommended repo commit message

```text
Update CONTINUUM_LIMIT with corrected causal ADM branch and proxy-closure audit

- Document failed naive order-distance embedding route
- Add corrected causal-set / antichain reconstruction branch
- Add verifier-backed local Lorentzian metric proxy
- Add measured lapse and diagnostic-only shift status
- Replace spectral R3 placeholder with graph-curvature proxy
- Add ADM-like action proxy with measured lapse and graph curvature
- Add finite-difference variation target
- Add weak-memory field-equation proxy
- Update honest status: verifier-backed derivation program, not GR closure
```

---

# 13. Next file after repo update

After updating `CONTINUUM_LIMIT.md`, the next technical file should be:

```text
CONTINUUM_LIMIT_CLOSURE_STATUS_V2.md
```

Its job:

- supersede the older closure matrix;
- include the failed branch;
- include the corrected causal ADM branch;
- classify each seam as closed / verifier-backed / proxy / failed / open.

**End of file.**
