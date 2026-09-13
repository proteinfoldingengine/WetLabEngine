# v15.06 — Recoverability Multiplicativity / Scalar-to-Operator Source Boundary

**Status:** CLOSED / measured and archive-bound on branch; merge/post-merge verification pending  
**Primary outcome:** `MULTIPLICATIVE_RECOVERABILITY_SCALAR_DOES_NOT_SELECT_LOCAL_SOURCE_LAW`  
**Secondary outcome:** `LEGACY_ACCESSIBILITY_MULTIPLICATIVITY_WAS_ASSUMED_OR_DEFINED_NOT_DERIVED`  
**Tertiary outcome:** `NEGATIVE_LOG_ROOT_FIDELITY_IS_ADDITIVE_ON_INDEPENDENT_RECOVERY_PAIRS`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Question

v15.05 showed that ordinary tensor composition of an already-chosen source law does not select the qubit spectral response

\[
F_{\rm tr}(\rho)=a(r)\left(\rho-\frac12I\right).
\]

It also showed that a stronger universal scalar-functional-calculus tensor law would select a logarithmic shape, but that stronger premise is not frozen ontology.

v15.06 therefore asks whether the existing recoverability stack already supplies the missing multiplicative structure in an ontology-native way.

The answer is two-sided:

1. **Yes:** root fidelity supplies an exact multiplicative quantum recoverability scalar, and its negative logarithm is additive on independent supplied recovery pairs.
2. **No:** this scalar is not a local Hermitian source law and cannot select `a(r)` by itself.

Hence

\[
\boxed{\texttt{MULTIPLICATIVE\_RECOVERABILITY\_SCALAR\_DOES\_NOT\_SELECT\_LOCAL\_SOURCE\_LAW}}.
\]

---

## 1. Legacy accessibility audit

The older V818 accessibility note says, conditionally:

> If accessible futures combine multiplicatively, then the natural potential is `log A`.

The V824 executable subsequently defines

```text
A = exp(C - mu + eta * repair)
```

and tests consequences of `Delta log(A)`.

Thus the legacy branch contains a valid conditional motivation for a logarithm, but it does **not** derive the multiplicative premise from the frozen pre-time ontology. The executable declares the exponential accessibility form rather than independently deriving it.

Therefore

```text
LEGACY_ACCESSIBILITY_MULTIPLICATIVITY_NOT_FROZEN_DERIVATION
```

remains the correct classification.

Nothing in this gate identifies legacy accessibility `A` with root fidelity, CMI, or another quantum recoverability scalar.

---

## 2. Exact multiplicative recoverability scalar

For normalized positive states define root fidelity

\[
F_{\rm root}(\rho,\sigma)
=\operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\sqrt\rho}.
\]

For independent pairs,

\[
\boxed{
F_{\rm root}(\rho_1\otimes\rho_2,\sigma_1\otimes\sigma_2)
=
F_{\rm root}(\rho_1,\sigma_1)
F_{\rm root}(\rho_2,\sigma_2)
}.
\]

Therefore, wherever fidelity is nonzero,

\[
\boxed{
-\log F_{\rm root}(12)
=
-\log F_{\rm root}(1)-\log F_{\rm root}(2).
}
\]

The theorem is exact. Sixteen deterministic numerical controls using faithful 2D and 3D states gave

```text
max root-fidelity product error = 3.219646771412954e-15
max -log additivity error       = 4.163336342344337e-15
```

This is a genuine pre-time multiplicative-to-additive law. No gravity target, entropy objective, pruning, or physical-time assumption is used to obtain it.

Frozen v13.16 already uses root fidelity as a recoverability quantity through

\[
F_{\rm root}(\rho_{ABC},\mathcal R(\rho_{AB}))
\ge e^{-I(A:C|B)/2}
\]

for some recovery channel. That relation supplies a scalar certification of recovery quality; it does not select a canonical generic recovery map and does not return a Hermitian source operator.

---

## 3. Exact-recovery non-selection theorem

For every faithful qubit state

\[
\rho_A(r)=\frac12(I+\mathbf r\cdot\boldsymbol\sigma),\qquad 0\le r<1,
\]

choose faithful \(\rho_B,\rho_C\) and form

\[
\rho_{ABC}(r)=\rho_A(r)\otimes\rho_B\otimes\rho_C.
\]

The channel that appends \(\rho_C\) to \(AB\) recovers this product state exactly, so

\[
F_{\rm root}\bigl(\rho_{ABC}(r),\mathcal R(\rho_{AB}(r))\bigr)=1
\]

for every faithful local radius \(r\).

Thus the exact-recovery scalar is constant across the full faithful local qubit spectrum.

Executed radii:

```text
0.05, 0.20, 0.40, 0.60, 0.80, 0.95
```

with

```text
max exact-recovery infidelity = 8.881784197001252e-16
max product-state CMI         = 4.440892098500626e-16
```

CMI is used only as a consistency diagnostic for this product/exact-recovery family, not as a source selector.

Across the same radius range, the v15.04 logarithmic qubit response coefficient changes from

```text
2.0016691711396506
```

to

```text
3.856380680136469
```

for a span of

```text
1.8547115089968185.
```

Therefore the same exact recovery scalar is compatible with substantially different local spectral responses.

```text
EXACT_RECOVERY_SCALAR_IS_CONSTANT_ACROSS_ALL_FAITHFUL_LOCAL_QUBIT_SPECTRA
```

This is a non-selection theorem, not a claim that exact recovery is generic.

---

## 4. Same recovery scalar, different source rays

At the same exact-recovery value `F_root=1`, take local qubit radii `0.20` and `0.80` and build two-site sources from three lawful local responses:

```text
linear:      a(r)=1
logarithmic: a(r)=2 atanh(r)/r
polynomial:  a(r)=1+r^2
```

Their projective separations are

```text
linear vs log        = 0.06248625684944287
linear vs polynomial = 0.08772246091732869
log vs polynomial    = 0.025253513918714623
```

So one and the same recovery scalar supports multiple distinct lawful source rays.

---

## 5. Scalar-to-operator type boundary

If a scalar recovery context `A` is admitted, local unitary covariance permits the qubit source family

\[
\boxed{
F_{\rm tr}(\rho,A)=a(r,A)\left(\rho-\frac12I\right).
}
\]

Multiplicativity of `A` does not by itself impose a functional equation on `a`.

The exact-recovery family makes this decisive: `A=1` for every faithful `r`, so the complete function

\[
a(r,1)
\]

remains free.

Therefore

```text
MULTIPLICATIVE_SCALAR_NEEDS_NEW_MAP_TO_BECOME_OPERATOR_SOURCE
```

and the missing object is now sharply typed: an ontology-native natural map from local quantum/recovery structure into the local Hermitian source space.

---

## 6. What changed

The source branch has advanced from

```text
maybe recoverability lacks the right multiplicative law
```

to

```text
independent state/recovery pairs
    -> exact multiplicative root fidelity
    -> exact additive -log root fidelity
    -> scalar recovery/comparison generator
    -X-> unique local Hermitian source response
```

The obstruction now lies **after multiplicativity**.

This rules out the tempting inference

```text
recoverability multiplies
therefore log is natural
therefore P must be log(rho).
```

The first step is exact for root fidelity. The second gives an additive scalar. The third does not follow because the scalar and operator generator are different typed objects.

---

## Claim boundary

### Derived / reproducibly executed

- root fidelity multiplicativity on independent supplied state/recovery pairs;
- additivity of `-log F_root`;
- conditional—not derived—status of legacy accessibility multiplicativity;
- exact-recovery scalar constancy across the faithful local qubit spectrum;
- coexistence of multiple source rays at the same recovery scalar;
- survival of the qubit response freedom as `a(r,A)` when a scalar recovery context is added.

### Not derived

- legacy accessibility `A = F_root` or `A = f(CMI)`;
- a canonical generic recovery map;
- a natural scalar-recovery-to-Hermitian-source map;
- a unique `a(r)` or `a(r,A)`;
- `P=log(rho)` from recoverability alone;
- the retained-node-to-quantum-site carrier or graph-site-to-`C^125/C^25` map;
- absolute source normalization or physical stress-energy;
- source-to-solder/coframe law;
- spacetime, Einstein equations, or Pillar 3 closure.

The primitive/pre-pruning ontology remains atemporal. No physical time is introduced as a source selector.

---

## Stop rule / next lawful frontier

Do **not** identify legacy accessibility with root fidelity, CMI, or another recoverability scalar merely because each admits logarithmic notation.

Do **not** infer `log(rho)` from the existence of `-log F_root`.

Do **not** choose a scalar-to-operator bridge from downstream gravity/ADM/Einstein performance.

The next lawful question is:

> Does the frozen ontology contain a canonical **local quantum object** whose independent composition is multiplicative and whose logarithmic/additive generator is already typed in the local Hermitian source space?

If every candidate requires an arbitrary reference state, representation map, normalization, or source rule, the logarithmic-source origin branch should stop as irreducible relative to the current frozen ontology.
