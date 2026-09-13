# v15.06 — Recoverability Multiplicativity / Scalar-to-Operator Source Boundary

**Status:** CLOSED / measured on branch; full archive binding and final exact-SHA certification pending  
**Primary outcome:** `MULTIPLICATIVE_RECOVERABILITY_SCALAR_DOES_NOT_SELECT_LOCAL_SOURCE_LAW`  
**Secondary outcome:** `LEGACY_ACCESSIBILITY_MULTIPLICATIVITY_WAS_ASSUMED_OR_DEFINED_NOT_DERIVED`  
**Tertiary outcome:** `NEGATIVE_LOG_ROOT_FIDELITY_IS_ADDITIVE_ON_INDEPENDENT_RECOVERY_PAIRS`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Question

v15.05 isolated the precise extra structure that would select a logarithmic state-to-source shape: a genuinely state-derived multiplicative/additive composition law, not merely composition of an already-chosen source operator.

The next question is therefore upstream:

> Does the frozen recoverability ontology already supply a multiplicative quantity whose logarithmic additive generator can canonically become the local Hermitian source law?

The answer separates into two parts.

First, there **is** an exact multiplicative pre-time quantum recoverability scalar: root fidelity of independent supplied state/recovery pairs. Its negative logarithm is additive.

Second, that scalar does **not** select the local operator-valued source response. It is a scalar on a pair of states / recovery context, whereas v15.04 requires a Hermitian source direction and a spectral response function. The exact-recovery sector makes this obstruction decisive: the recoverability scalar can remain exactly constant while the local state spectrum, and therefore the admissible source response, varies over the full faithful qubit interval.

Thus

\[
\boxed{\texttt{MULTIPLICATIVE\_RECOVERABILITY\_SCALAR\_DOES\_NOT\_SELECT\_LOCAL\_SOURCE\_LAW}}.
\]

---

# I. LEGACY ACCESSIBILITY CLAIM AUDIT

The older V818/V824 accessibility branch contains a suggestive logarithmic story, but it does not provide the missing upstream derivation.

V818 states, conditionally:

> If accessible futures combine multiplicatively, then the natural potential is `log A`.

That is a mathematically valid implication, but the multiplicative premise is not derived there.

The V824 executable then explicitly declares

```text
A = exp(C - mu + eta * repair)
```

and tests curvature-like consequences of `Delta log(A)`. The executable therefore validates consequences of that chosen accessibility construction; it does not independently prove that ontology-native recoverability options must compose multiplicatively.

The correct archival classification is

\[
\boxed{\texttt{LEGACY\_ACCESSIBILITY\_MULTIPLICATIVITY\_NOT\_FROZEN\_DERIVATION}}.
\]

Nothing in v15.06 identifies the legacy accessibility field `A` with quantum root fidelity, CMI, or any other recoverability scalar.

---

# II. EXACT QUANTUM RECOVERY MULTIPLICATIVITY

For normalized positive states, root fidelity

\[
F_{\rm root}(\rho,\sigma)
=\operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\sqrt\rho}
\]

obeys the exact tensor-product law

\[
\boxed{
F_{\rm root}(\rho_1\otimes\rho_2,\sigma_1\otimes\sigma_2)
=
F_{\rm root}(\rho_1,\sigma_1)
F_{\rm root}(\rho_2,\sigma_2)
}.
\]

Therefore, where the fidelity is nonzero,

\[
\boxed{
-\log F_{\rm root}(12)
=
-\log F_{\rm root}(1)
-
\log F_{\rm root}(2)
}.
\]

This is exactly the multiplicative-to-additive structure sought in v15.05, but on a **scalar comparison object**.

Sixteen deterministic independent controls using faithful 2D and 3D states gave

```text
max root-fidelity product error = 3.219646771412954e-15
max -log additivity error       = 4.163336342344337e-15
```

The theorem itself is exact; these numerical controls validate the implementation.

No entropy, pruning, physical time, ADM, Einstein, gravity, cosmology, or empirical target enters this result.

The relationship to frozen v13.16 is direct but limited. v13.16 uses the recoverability bound

\[
F_{\rm root}(\rho_{ABC},\mathcal R(\rho_{AB}))
\ge e^{-I(A:C|B)/2}
\]

for some recovery channel. That supplies a principled scalar certification of recovery quality. It does not select a canonical generic recovery map and it does not itself return a Hermitian source operator.

---

# III. EXACT-RECOVERY NON-SELECTION THEOREM

The scalar/operator distinction can be made exact rather than rhetorical.

For every faithful qubit state

\[
\rho_A(r)=\frac12(I+\mathbf r\cdot\boldsymbol\sigma),
\qquad 0\le r<1,
\]

choose arbitrary faithful states \(\rho_B\) and \(\rho_C\), and form the product state

\[
\rho_{ABC}(r)
=\rho_A(r)\otimes\rho_B\otimes\rho_C.
\]

The channel that appends \(\rho_C\) to \(AB\) recovers this state exactly. Hence

\[
F_{\rm root}
\bigl(
\rho_{ABC}(r),
\mathcal R(\rho_{AB}(r))
\bigr)=1
\]

for **every** faithful local Bloch radius \(r\).

So the exact-recovery scalar is constant across the entire faithful local qubit spectrum.

The executed controls sampled

```text
r = 0.05, 0.20, 0.40, 0.60, 0.80, 0.95
```

and gave

```text
max exact-recovery infidelity = 8.881784197001252e-16
max product-state CMI         = 4.440892098500626e-16
```

CMI here is only an independent consistency diagnostic for the product/exact-recovery family; it is not being used as a source selector.

Across the same radius range, the logarithmic qubit response coefficient from v15.04 changes from

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

Therefore a scalar recovery value of exactly `1` is compatible with strongly different local spectral responses.

This proves

\[
\boxed{\texttt{EXACT\_RECOVERY\_SCALAR\_IS\_CONSTANT\_ACROSS\_ALL\_FAITHFUL\_LOCAL\_QUBIT\_SPECTRA}}.
\]

The statement is a non-selection theorem, not a claim that exact recovery is generic. v13.16 already establishes that exact Markovity is not selected by the ontology.

---

# IV. SAME RECOVERY SCALAR, DIFFERENT SOURCE RAYS

The obstruction survives at the actual projective-source level.

Use two local qubit states with radii `0.20` and `0.80`, both inside an exactly recoverable product construction. The recovery scalar is the same: `F_root = 1`.

Construct the labeled two-site source from three lawful local response functions:

```text
linear:      a(r) = 1
logarithmic: a(r) = 2 atanh(r) / r
polynomial:  a(r) = 1 + r^2
```

The projective-ray separations are

```text
linear vs log        = 0.06248625684944287
linear vs polynomial = 0.08772246091732869
log vs polynomial    = 0.025253513918714623
```

Thus one and the same exact recoverability scalar is compatible with at least three distinct lawful operator-valued source rays.

This is the decisive bridge failure for this candidate selector.

---

# V. SCALAR-TO-OPERATOR TYPE BOUNDARY

Once a scalar recovery context \(A\) is admitted, local unitary covariance does not remove the v15.04 freedom. For a qubit the most general traceless form becomes

\[
\boxed{
F_{\rm tr}(\rho,A)
=a(r,A)\left(\rho-\frac12 I\right).
}
\]

The recovery scalar can therefore parameterize the response, but it does not select the response function by itself.

The exact-recovery family sets

\[
A=1
\]

for every faithful \(r\). Consequently the entire function

\[
a(r,1)
\]

remains free.

So even after earning multiplicativity of the scalar, one still needs a new natural law

\[
(\rho,\text{recovery context})
\longrightarrow
P(\rho)
\]

that is typed directly in the Hermitian source space.

Hence

\[
\boxed{\texttt{MULTIPLICATIVE\_SCALAR\_NEEDS\_NEW\_MAP\_TO\_BECOME\_OPERATOR\_SOURCE}}.
\]

---

# VI. WHAT v15.06 CHANGES

v15.06 does not merely repeat v15.05's statement that composition is insufficient.

It identifies a genuine ontology-compatible multiplicative quantity and follows it as far as it can lawfully go:

```text
independent state/recovery pairs
    -> exact multiplicative root fidelity
    -> exact additive -log root fidelity
    -> scalar recovery/comparison generator
    -X-> unique local Hermitian source response
```

The obstruction is now localized **after multiplicativity**.

This is useful because it eliminates a tempting argument:

```text
recoverability is multiplicative
therefore log is natural
therefore the source must be log(rho)
```

The first implication can be made exact for root fidelity. The second produces an additive scalar. The third does not follow.

An additive scalar generator and an additive operator generator are different typed objects.

---

# VII. CLAIM BOUNDARY

### Derived / reproduced

- root fidelity is multiplicative on independent supplied state/recovery pairs;
- `-log F_root` is additive on those pairs;
- the legacy V818 accessibility multiplicativity statement is conditional;
- the V824 executable declares its accessibility field exponentially rather than deriving multiplicativity;
- an exact-recovery product family spans the full faithful local qubit spectrum while keeping the recovery scalar fixed at one;
- distinct lawful source rays coexist at that same recovery scalar;
- a scalar recoverability context does not remove the qubit freedom `a(r,A)`.

### Not derived

- an identification of legacy accessibility `A` with root fidelity or CMI;
- a canonical generic recovery map;
- a natural scalar-recoverability-to-Hermitian-source map;
- a unique `a(r)` or `a(r,A)`;
- `P = log rho` from recoverability alone;
- the retained-node-to-quantum-site carrier;
- the graph-site-to-`C^125/C^25` map;
- absolute source calibration;
- physical stress-energy;
- source-to-solder/coframe law;
- physical spacetime or Einstein equations;
- a physical time primitive;
- Pillar 3 closure.

The pre-pruning source-selector question remains atemporal. Entropy/CMI is not used as a selection objective in this gate.

---

# Stop rule / next lawful frontier

Do **not** identify the legacy accessibility field with root fidelity, CMI, or another recoverability scalar merely because each admits logarithmic notation.

Do **not** infer `log rho` from the existence of `-log F_root`.

Do **not** choose a scalar-to-operator map because it improves downstream gravitational behavior.

The lawful next question is:

> Does the frozen ontology contain a canonical **local quantum object** whose independent composition is multiplicative and whose logarithmic/additive generator is already typed in the local Hermitian source space?

If no such object exists without introducing a reference state, representation map, or source rule by hand, the logarithmic source branch should stop as irreducible relative to the current ontology.
