# CAUSAL_CONTINUUM_REINTEGRATION.md

# Causal Continuum Reintegration
## Reintegrating the corrected causal ADM branch into `CONTINUUM_LIMIT.md`

## Status
**Reintegration audit. Not a proof.**

This file reintegrates the corrected causal-to-ADM branch back into the continuum-limit program.

It answers:

1. Which older schematic assumptions in `CONTINUUM_LIMIT.md` have now been replaced by verifier-backed candidate constructions?
2. Which pieces remain proxy-level?
3. Which failed branch must remain explicitly documented?
4. What can safely be claimed?
5. What still blocks a controlled GR continuum limit?

This file does **not** close seam 3.

---

# 1. Background

The original `CONTINUUM_LIMIT.md` required a chain of objects:

```text
discrete action
    -> coarse-grained fields
    -> emergent metric
    -> curvature
    -> Einstein-Hilbert-like action
    -> field equations
```

At first, several pieces were schematic:
- emergent Lorentzian metric,
- curvature construction,
- ADM action structure,
- lapse/shift,
- spatial curvature,
- variation,
- source coupling.

The recent causal-slice branch converted much of that schematic structure into verifier-backed candidate objects.

---

# 2. Corrected causal branch

The corrected branch is:

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

The failed branch remains:

```text
ORDER_DISTANCE_EMBEDDING.md  [FAILED]
```

That failed branch is not a weakness to hide. It is an important falsified path that improved the derivation.

---

# 3. Replacement map for CONTINUUM_LIMIT.md

## 3.1 Emergent causal order

Original schematic requirement:

```text
some discrete order / update structure becomes causal order
```

Replacement candidate:

```text
CAUSAL_ORDER_DERIVATION.md
```

Candidate relation:

```text
e_i ≺ e_j
iff
t_j > t_i,
rho_i = 1,
and ||x_j - x_i|| <= c_eff (t_j - t_i)
```

Status:

```text
Verifier-backed candidate
```

Limitation:

```text
update order is not yet proven physical time
```

---

## 3.2 Interval geometry

Original schematic requirement:

```text
causal order supports volume and dimension
```

Replacement candidate:

```text
CAUSAL_INTERVAL_GEOMETRY.md
ORDER_ONLY_METRIC_RECONSTRUCTION.md
```

Candidate scaling:

```text
|I(i,j)| ~ tau_ij^D
```

Status:

```text
Verifier-backed, partly coordinate-assisted
```

Limitation:

```text
dimension and proper time are not fully coordinate-free
```

---

## 3.3 Failed naive metric reconstruction

Original tempting but invalid route:

```text
interval cardinality -> distance -> MDS -> metric
```

Falsified by:

```text
ORDER_DISTANCE_EMBEDDING.md
ORDER_DISTANCE_FAILURE_ANALYSIS.md
```

Status:

```text
Failed and documented
```

Reason:

```text
causal comparability is timelike and sparse, not a complete spatial metric distance matrix
```

Required note for `CONTINUUM_LIMIT.md`:

> A naive order-distance embedding route was tested and failed; the continuum program therefore pivots to causal-set-style reconstruction using chains and antichains.

---

## 3.4 Causal-set reconstruction

Replacement candidate:

```text
CAUSAL_SET_RECONSTRUCTION.md
```

Route:

```text
causal order
    -> longest-chain depth
    -> antichain slices
    -> causal-profile spatial adjacency
```

Status:

```text
Verifier-backed candidate
```

Limitation:

```text
not yet manifoldlikeness proof
```

---

## 3.5 Spatial geometry on slices

Replacement candidates:

```text
ANTICHAIN_SPATIAL_GEOMETRY.md
ANTICHAIN_GRAPH_METRIC.md
```

Route:

```text
A_k
    -> causal-profile graph G_k
    -> graph Laplacian embedding
    -> h_ab^(k)
```

Status:

```text
Verifier-backed spatial metric proxy
```

Limitation:

```text
h_ab is proxy-level and graph-embedding dependent
```

---

## 3.6 Lorentzian metric assembly

Replacement candidate:

```text
CAUSAL_SLICE_LORENTZIAN_METRIC.md
```

Route:

```text
tau from longest-chain depth
h_ab from antichain graph metric
        ->
g_mu_nu = [[-N^2, 0], [0, h_ab]]
```

Status:

```text
Verifier-backed Lorentzian signature candidate
```

Limitation:

```text
shift not closed; lapse only recently upgraded
```

---

## 3.7 Lapse and shift

Replacement candidates:

```text
LAPSE_SHIFT_DERIVATION.md
SLICE_ALIGNMENT_AND_SHIFT.md
LAPSE_SHIFT_CLOSURE_STATUS.md
```

Audit result:

```text
N lapse: verifier-backed candidate
N_a shift: diagnostic-only proxy
```

Safe reintegration:

```text
Use measured N_k in main ADM proxy.
Keep N_a = 0 in main ADM proxy.
Log aligned N_a as diagnostic only.
```

---

## 3.8 Spatial curvature

Replacement candidate:

```text
SPATIAL_GRAPH_CURVATURE.md
```

Route:

```text
G_k, h_ab^(k)
    -> Forman-style curvature
    -> Ollivier-overlap curvature
    -> R3_graph,k
```

Status:

```text
Verifier-backed graph-curvature proxy
```

Limitation:

```text
not continuum R^(3)
```

---

## 3.9 ADM-like action

Replacement candidates:

```text
ADM_ACTION_WITH_LAPSE.md
ADM_ACTION_WITH_GRAPH_CURVATURE.md
```

Current strongest proxy:

```text
S_proxy^(N,R3)
=
sum_k N_k sqrt(det h_k)
[
R_graph,k^(3)
+
K_ab K^ab
-
K^2
] Δk
```

Status:

```text
Verifier-backed causal ADM action proxy
```

Limitation:

```text
not full ADM or Einstein-Hilbert action
```

---

## 3.10 Variation

Replacement candidate:

```text
CAUSAL_ADM_VARIATION_TARGET.md
```

Target:

```text
E_ab^(k)
≈
δS_proxy^(N,R3) / δh_ab^(k)
```

Status:

```text
Verifier-backed finite-difference proxy variation
```

Limitation:

```text
not Einstein variation
```

---

## 3.11 Field-equation proxy

Replacement candidate:

```text
CAUSAL_ADM_FIELD_EQUATION_PROXY.md
```

Target:

```text
E_ab^(k)
=
S_ab^(mem,k)
```

Status:

```text
Verifier-backed discrete field-equation proxy
```

Limitation:

```text
not G_mu_nu = 8πT_mu_nu
```

---

# 4. Updated continuum-limit chain

The updated causal continuum route is:

```text
microscopic update / pruning law
        ↓
causal order
        ↓
longest chains + antichains
        ↓
spatial antichain graph
        ↓
h_ab spatial metric proxy
        ↓
measured lapse N_k, diagnostic shift N_a
        ↓
local Lorentzian metric proxy
        ↓
graph R3 + extrinsic K terms
        ↓
ADM-like action proxy
        ↓
finite-difference Euler response
        ↓
weak-memory sourced field-equation proxy
```

This chain is much stronger than the original schematic continuum-limit section.

But it remains proxy-level.

---

# 5. What can safely update CONTINUUM_LIMIT.md

## Safe status update

`CONTINUUM_LIMIT.md` can now say:

> The emergent metric and geometric action seams have been expanded into a corrected causal-slice derivation branch. A naive order-distance embedding route failed and is documented. The corrected branch uses causal order, longest-chain time, antichain spatial slices, graph-derived spatial metric proxies, measured lapse, graph-curvature spatial curvature proxies, and an ADM-like action with finite-difference variation. These objects are verifier-backed as structural candidates, but they do not yet constitute a controlled GR continuum limit.

---

## Safe replacement statement

Replace older schematic wording:

```text
Assume emergent metric g_mu_nu exists.
```

with:

```text
A verifier-backed causal-slice metric candidate now exists:
longest-chain time plus antichain graph spatial metric produces a local Lorentzian block metric with measured lapse and zero main-branch shift.
```

---

## Safe action statement

Replace:

```text
Assume S_geom has EH limit.
```

with:

```text
A causal ADM-like proxy action has been constructed using measured lapse, graph-derived spatial curvature, and extrinsic-curvature terms. It is finite and variationally responsive, but not yet shown to converge to Einstein-Hilbert.
```

---

## Safe field-equation statement

Replace:

```text
Effective field equations follow by variation.
```

with:

```text
A finite-difference Euler-response proxy exists and can be coupled to a weak-memory source with correct O(eta_mem) scaling. This is a discrete field-equation proxy, not the Einstein equation.
```

---

# 6. What must not be claimed

Do **not** claim:

```text
The framework derives GR.
```

Do **not** claim:

```text
The Einstein-Hilbert action has been recovered.
```

Do **not** claim:

```text
The Ricci scalar has been derived.
```

Do **not** claim:

```text
Shift N_a is derived.
```

Do **not** claim:

```text
The field equation proxy is Einstein's equation.
```

Do **not** claim:

```text
Graph R3 is continuum R3.
```

---

# 7. Remaining blockers

## 7.1 Physical time
The causal order still depends on update order being physically meaningful.

Open target:

```text
microscopic update order -> physical causal time
```

---

## 7.2 Coordinate-free dimension
Interval geometry still needs stronger coordinate-free dimension and manifoldlikeness tests.

Open target:

```text
causal intervals -> stable dimension without hidden coordinates
```

---

## 7.3 Shift
Shift is still diagnostic-only.

Open target:

```text
slice matching -> covariant vector field N_a
```

---

## 7.4 Continuum spatial curvature
Graph \(R^{(3)}\) is not continuum \(R^{(3)}\).

Open target:

```text
graph curvature -> continuum spatial Ricci scalar
```

---

## 7.5 ADM / EH convergence
The ADM-like proxy is not yet the Einstein-Hilbert action.

Open target:

```text
S_proxy^(N,R3) -> S_ADM -> S_EH
```

---

## 7.6 Variational closure
The Euler response is finite but not known to converge to ADM constraints/evolution equations.

Open target:

```text
E_ab^(k) -> ADM field equations
```

---

## 7.7 Exact memory stress tensor
The source term is still a weak-memory proxy.

Open target:

```text
S_ab^mem -> exact projected T_mu_nu^mem
```

---

# 8. Recommended next file

The next file should be:

```text
CONTINUUM_LIMIT_REPO_UPDATE.md
```

Its job:

1. provide repo-ready replacement sections for `CONTINUUM_LIMIT.md`;
2. include the corrected causal branch;
3. include the failed branch note;
4. update the honest status line;
5. update the closure matrix.

---

# 9. Honest final status

> The causal branch now substantially upgrades `CONTINUUM_LIMIT.md`: metric, lapse, spatial curvature, ADM action, variation, and weak-memory source coupling all have verifier-backed proxy constructions. However, the result remains a proxy-level continuum program, not a derivation of GR. The strongest next move is a repo-ready update to `CONTINUUM_LIMIT.md` that accurately reflects this improved but still open status.

**End of file.**
