# CAUSAL_ORDER_DERIVATION.md

# Causal Order Derivation
## Candidate route from microscopic update/pruning order to causal time orientation

## Status
**Live derivation target. First causal-order pass. Not yet physically closed.**

`LORENTZIAN_SIGNATURE_MAP.md` showed that if signed interval / time-orientation data are supplied, the local metric reconstruction can structurally produce Lorentzian signature:

\[
(-,+,+,+).
\]

This file attacks the missing upstream seam:

\[
\text{microscopic update / pruning order}
\longmapsto
\text{causal order / time orientation}.
\]

This file does **not** prove physical causality.

It defines a first candidate partial-order construction and a structural verifier.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Assumption**
- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**

Nothing here should be interpreted as a completed proof unless explicitly stated.

---

# 1. Goal of this file

The continuum chain currently requires a time-orientation variable:

\[
\tau_i
\]

or causal relation:

\[
e_i\prec e_j.
\]

Without this, `LORENTZIAN_SIGNATURE_MAP.md` remains conditional.

The goal of this file is to define when update/pruning order can supply a causal partial order.

---

# 2. Microscopic event set

## Definition 1
Let events be indexed by:

\[
e_i.
\]

Each event carries:

- update index or time:
  \[
  t_i;
  \]

- local state / block position:
  \[
  x_i;
  \]

- retained-memory activation flag:
  \[
  \rho_i\in\{0,1\};
  \]

- optional pruning threshold condition:
  \[
  |\xi_i|>\varepsilon^*.
  \]

## Assumption 1
The update index \(t_i\) is not merely bookkeeping. It represents the ordering of admissible state updates in the microscopic law.

This is still a strong assumption.

---

# 3. Candidate causal relation

## Definition 2
Define:

\[
e_i\prec e_j
\]

if:

1. \(t_j>t_i\);
2. event \(i\) retained transferable state:
   \[
   \rho_i=1;
   \]
3. the spatial/block separation is reachable:
   \[
   \|x_j-x_i\|\le c_{\mathrm{eff}}(t_j-t_i).
   \]

Thus:

\[
e_i\prec e_j
\quad\Longleftrightarrow\quad
t_j>t_i,\quad
\rho_i=1,\quad
\|x_j-x_i\|\le c_{\mathrm{eff}}\Delta t.
\]

Here \(c_{\mathrm{eff}}\) is the effective signal speed or update-propagation bound.

## Interpretation
This is a first causal-order candidate:

- update order supplies direction;
- retained memory supplies transmissible influence;
- finite propagation speed supplies locality.

---

# 4. Partial-order requirements

## Definition 3
A causal relation must satisfy:

1. irreflexivity:
   \[
   \neg(e_i\prec e_i);
   \]

2. antisymmetry:
   \[
   e_i\prec e_j\Rightarrow \neg(e_j\prec e_i);
   \]

3. acyclicity / transitive closure consistency;

4. nontrivial causal density:
   the relation is neither empty nor saturated.

## Lemma candidate 1
If:

\[
t_j>t_i
\]

is strictly enforced for every relation, then the generated relation is acyclic.

### Proof sketch
Every causal edge increases \(t\). A cycle would require:

\[
t_1<t_2<\dots<t_n<t_1,
\]

which is impossible.

---

# 5. Time function

## Definition 4
A time function is a map:

\[
\tau(e_i)
\]

such that:

\[
e_i\prec e_j
\Rightarrow
\tau(e_i)<\tau(e_j).
\]

The first candidate is:

\[
\tau(e_i)=t_i.
\]

## Failure condition 1
If update order cannot serve as a monotone time function, Lorentzian signature remains externally imposed.

---

# 6. Alexandrov interval proxy

## Definition 5
For comparable events:

\[
e_i\prec e_j,
\]

define the discrete interval:

\[
I(i,j)=\{e_k:e_i\prec e_k\prec e_j\}.
\]

The size:

\[
|I(i,j)|
\]

acts as a causal-volume proxy.

## Derivation target A
Show that interval counts can supply dimension and volume estimates compatible with the metric map.

This is not yet done.

---

# 7. Verifier implementation

## Status
**Implemented as `causal_order_derivation_verifier.py`. Execution log captured.**

The verifier tests:

\[
e_i\prec e_j
\quad\Longleftrightarrow\quad
t_j>t_i
\quad\text{and}\quad
\|x_j-x_i\|\le c_{\mathrm{eff}}(t_j-t_i),
\]

with retention gating.

It checks:

1. irreflexivity;
2. antisymmetry;
3. cycle freedom;
4. valid layering/time function;
5. nontrivial edge density;
6. finite Alexandrov interval proxy.

## Captured verifier output

```text
Causal order derivation verifier
==================================================
Candidate relation:
i -> j iff t_j > t_i and ||x_j-x_i|| <= c*(t_j-t_i), gated by retention
Checks: irreflexive, antisymmetric, cycle-free, layered, nontrivial density

Sweep results:
PASS: 84.0
SOFT_FAIL: 16.0
HARD_FAIL: 0.0
edge_density_median: 0.11913965918484795
active_fraction_median: 0.9325876350416227
interval_median_median: 2.0
edge_density_min: 0.0
edge_density_max: 0.48203723986856517
```

---

# 8. What this file establishes

### Established at current proof level

1. A first causal partial-order construction has been defined.
2. Update order can act as a monotone time function under the candidate relation.
3. Retained memory gates causal influence.
4. The verifier confirms structural partial-order viability in sampled regimes.
5. Failure modes are explicit:
   - empty relation,
   - saturated relation,
   - no retained events,
   - no finite propagation bound,
   - update order not physical.

### Not yet proved

1. Update order is not yet derived as physical time.
2. \(c_{\mathrm{eff}}\) is not derived.
3. Causal intervals are not yet linked to dimension or volume.
4. The relation is not yet shown to reproduce continuum light cones.
5. The construction may still be gauge/bookkeeping rather than physics.

---

# 9. Theorem candidate

## Theorem candidate 1
Suppose:

1. microscopic update order is physically meaningful;
2. retained-memory activation gates transmissible influence;
3. propagation is bounded by \(c_{\mathrm{eff}}\);
4. the induced relation is acyclic and nontrivial;
5. interval counts converge to causal volume estimates.

Then the microscopic update/pruning process induces a causal order suitable for Lorentzian metric reconstruction.

This theorem is **not yet proved**.

---

# 10. Updated proof-chain status

This file supports the prior Lorentzian signature chain:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
        ↓
CURVATURE_ESTIMATION.md
        ↓
EINSTEIN_HILBERT_LIMIT.md
        ↓
FIELD_EQUATION_VARIATION.md
        ↓
CONTINUUM_LIMIT.md
```

The next hard seam is now:

\[
\text{causal intervals}
\longmapsto
\text{dimension / volume / light-cone structure}.
\]

---

# 11. Next derivation target

The next file should be:

```text
CAUSAL_INTERVAL_GEOMETRY.md
```

Its job:

\[
I(i,j)
\longmapsto
\text{dimension, volume, interval scaling, light-cone structure}.
\]

That is the next step toward deriving the metric map from causal data rather than assuming coordinates.

---

# Honest status line

> `CAUSAL_ORDER_DERIVATION.md` supplies the first verifier-backed candidate map from microscopic update/pruning order to a causal partial order. It supports Lorentzian signature structurally, but it does not yet prove that update order is physical time or that causal intervals reproduce continuum spacetime geometry.

**End of file.**
