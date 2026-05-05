# LORENTZIAN_SIGNATURE_MAP.md

# Lorentzian Signature Map
## Candidate upgrade from local metric reconstruction to Lorentzian spacetime signature

## Status
**Live derivation target. First Lorentzian-signature pass. Not yet causal-set or GR-closed.**

`EMERGENT_METRIC_MAP.md` showed a first verifier-backed route from positive geometry weights and adjacency to a nondegenerate local metric candidate in a Riemannian/local setting.

This file attacks the next seam:

\[
\text{adjacency + causal/time orientation}
\longmapsto
(-,+,+,+)\text{ metric signature}.
\]

This file does **not** prove:
- causal set emergence,
- full Lorentzian covariance,
- Einstein-Hilbert convergence,
- or GR recovery.

It only provides the first inspectable route by which causal/time-orientation data can force one negative and three positive metric directions in a local reconstruction.

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

The metric reconstruction chain currently has:

\[
(G_i,\text{ adjacency})
\longmapsto
g_{ab}^{(i)}
\]

in a positive-definite local test.

The missing ingredient is causal/time structure.

The goal of this file is to add:

\[
\tau_i
\]

or equivalent causal order data, so that local intervals become signed:

\[
ds^2
=
-c^2d\tau^2
+
d\ell^2.
\]

---

# 2. Discrete causal inputs

## Definition 1
Each block \(B_i\) carries:

- a local geometry weight:
  \[
  G_i>0;
  \]

- a time-orientation or causal label:
  \[
  \tau_i;
  \]

- adjacency:
  \[
  i\sim j;
  \]

- optionally a lapse-like local scale:
  \[
  C_i>0.
  \]

## Assumption 1
The causal/time label \(\tau_i\) is not arbitrary bookkeeping. It must descend from:
- causal order,
- update order,
- discrete light-cone structure,
- or another microscopic time-orientation rule.

This remains open.

---

# 3. Signed interval target

## Definition 2
For neighboring blocks \(i,j\), define:

\[
\Delta\tau_{ij}=\tau_j-\tau_i,
\]

\[
\Delta x_{ij}=x_j-x_i.
\]

The first signed interval ansatz is:

\[
ds_{ij}^2
=
-\frac{1}{2}(C_i+C_j)^2(\Delta\tau_{ij})^2
+
\frac{1}{2}(G_i+G_j)\|\Delta x_{ij}\|^2.
\]

This is the Lorentzian analogue of the positive local metric reconstruction used in `EMERGENT_METRIC_MAP.md`.

## Failure condition 1
If no signed interval or causal ordering can be defined, Lorentzian signature cannot be derived by this route.

---

# 4. Local Lorentzian metric fitting

## Definition 3
At each block \(i\), estimate a symmetric local metric tensor \(g^{(i)}_{\mu\nu}\) by solving:

\[
\Delta X_{ij}^{\mu}
g_{\mu\nu}^{(i)}
\Delta X_{ij}^{\nu}
\approx
ds_{ij}^2
\]

for neighboring blocks \(j\sim i\), where:

\[
\Delta X_{ij}=(\Delta\tau_{ij},\Delta x_{ij}).
\]

## Definition 4
The local metric has Lorentzian signature if its eigenvalue signs are:

\[
(-,+,+,+)
\]

or equivalently one negative and three positive eigenvalues.

## Lemma candidate 1
If the signed interval relation is stable and the local least-squares metric fit has one negative and three positive eigenvalues over most blocks, then the discrete geometry supports a local Lorentzian metric candidate.

This lemma is structural, not yet a proof of continuum Lorentzian covariance.

---

# 5. Conditions for signature stability

## Definition 5
Signature stability requires:

1. nondegenerate local metric fits;
2. one negative and three positive eigenvalues;
3. bounded condition number;
4. stable signature fraction under block resampling;
5. controlled variation of the metric over neighboring blocks.

## Failure condition 2
If signature flips randomly across blocks, the Lorentzian map is not stable.

## Failure condition 3
If the fitted metric is frequently degenerate or has Euclidean signature, causal orientation is insufficient.

---

# 6. Relationship to causal-set and Regge routes

## Derivation target A
Replace provisional coordinates \((\tau_i,x_i)\) with one of:

- causal-set order intervals;
- Lorentzian Regge simplex data;
- graph light-cone neighborhoods;
- update-order partial order plus spatial adjacency;
- signed interval counts.

This is required before the map can be considered physically derived.

## Failure condition 4
If Lorentzian signature only appears after imposing external coordinates by hand, then the signature map is not derived from the microscopic law.

---

# 7. Theorem candidate

## Theorem candidate 1
Suppose:

1. the block graph admits causal/time-orientation data \(\tau_i\);
2. local interval estimates are signed;
3. local metric fits are nondegenerate;
4. most local fits have one negative and three positive eigenvalues;
5. signature stability persists under block refinement;
6. the construction can be expressed without preferred-coordinate artifacts.

Then the block geometry admits a Lorentzian metric candidate:

\[
g_{\mu\nu}(x)
\]

with signature:

\[
(-,+,+,+).
\]

This theorem is **not yet proved**.

---

# 8. Verifier implementation

## Status
**Implemented as `lorentzian_signature_map_verifier.py`. Execution log captured.**

The verifier tests the structural signature map:

\[
(\tau_i,x_i,G_i,C_i,\text{ adjacency})
\longmapsto
g_{\mu\nu}^{(i)}.
\]

It checks:

1. signed interval construction;
2. local symmetric metric fit;
3. nondegeneracy;
4. one negative and three positive eigenvalues;
5. bounded condition number;
6. stable signature fraction across sampled blocks.

It does not prove causal-set emergence or coordinate independence.

## Captured verifier output

```text
Lorentzian signature map verifier
==================================================
Candidate tested:
time-oriented coordinates + positive lapse/geometry scales + adjacency
-> signed interval relation
-> local symmetric metric estimate
-> signature check: one negative, three positive

Sweep results:
PASS: 94.0
SOFT_FAIL: 0.0
HARD_FAIL: 6.0
valid_fraction_median: 1.0
signature_fraction_median: 1.0
cond_median: 1.5625773434744308
metric_variation_median: 0.5218283833020964
valid_fraction_min: 1.0
```

---

# 9. What this file establishes

### Established at current proof level

1. A first Lorentzian-signature reconstruction route is specified.
2. The signed interval requirement is explicit.
3. The need for causal/time-orientation data is isolated.
4. The verifier checks the one-negative / three-positive signature condition.
5. Failure conditions are explicit.

### Not yet proved

1. The time label \(\tau_i\) is not derived from the microscopic law.
2. Causal order is not derived.
3. Coordinate independence is not proved.
4. Curvature is not yet computed.
5. Einstein-Hilbert convergence is not shown.
6. The result is a local signature test, not a full spacetime derivation.

---

# 10. Updated proof-chain status

The continuum chain now becomes:

```text
COARSE_GRAINING_MAP.md
        ↓
EMERGENT_METRIC_MAP.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
        ↓
CONTINUUM_LIMIT.md
```

The remaining hard seams are now:

1. causal-order derivation;
2. curvature estimation;
3. Einstein-Hilbert convergence;
4. Bianchi/conservation compatibility.

---

# 11. Next derivation target

The next file should be:

```text
CURVATURE_ESTIMATION.md
```

Its job:

\[
g_{\mu\nu}^{(i)}
\longmapsto
\Gamma^\rho_{\mu\nu},
R_{\mu\nu},
R.
\]

This is the next mathematical bottleneck toward an Einstein-Hilbert limit.

---

# Honest status line

> `LORENTZIAN_SIGNATURE_MAP.md` adds the first verifier-backed route from causal/time-orientation data to a local Lorentzian metric signature. It confirms that signed interval data can structurally produce one negative and three positive directions, but it does not derive causal order, curvature, or GR covariance.

**End of file.**
