# v15.07 — Canonical Neutral Reference / Relative-Density Generator Gate

**Status:** CLOSED / measured and archive-bound on branch; final exact-head certification and integration pending  
**Primary outcome:** `CANONICAL_NEUTRAL_RELATIVE_GENERATOR_EXISTS_SOURCE_IDENTIFICATION_UNDERIVED`  
**Secondary:** `UNIQUE_FRAME_INVARIANT_REFERENCE_IS_MAXIMALLY_MIXED`  
**Tertiary:** `NEUTRAL_TO_STATE_PGRL_ENDPOINT_SELECTS_LOG_PROJECTIVE_RAY_CONDITIONALLY`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Question

v15.06 established that a genuine multiplicative recoverability scalar exists, but its logarithm remains a scalar comparison generator rather than a local Hermitian source generator.

The next question was therefore deliberately typed:

> Does the frozen local quantum structure contain a canonical multiplicative **operator-valued** object whose logarithmic additive generator already lives in the local Hermitian source space?

The answer is **yes** at the mathematical/operator level.

But a second question remains separate:

> Does the frozen provenance/source ontology identify that canonical generator as *the source*?

The answer to that second question is **no, not yet**.

The gate therefore closes with

\[
\boxed{
\texttt{CANONICAL\_NEUTRAL\_RELATIVE\_GENERATOR\_EXISTS\_SOURCE\_IDENTIFICATION\_UNDERIVED}
}
\]

This is a stronger positive result than v15.06, but it does not retroactively derive a physical source law.

---

# I. CANONICAL FRAME-NEUTRAL REFERENCE

Let \(\tau_d\) be a normalized density operator on a local \(d\)-dimensional Hilbert space and require no preferred local frame:

\[
U\tau_dU^\dagger=\tau_d
\qquad\text{for every }U\in U(d).
\]

The full-unitary commutant consists only of scalar operators. Therefore

\[
\tau_d=cI_d.
\]

Normalization fixes

\[
\boxed{\tau_d=I_d/d}.
\]

This reference also composes exactly:

\[
\tau_{d_1d_2}
=\frac{I_{d_1d_2}}{d_1d_2}
=\tau_{d_1}\otimes\tau_{d_2}.
\]

Thus

```text
UNIQUE_FRAME_INVARIANT_REFERENCE_IS_MAXIMALLY_MIXED
```

The executed commutant controls used dimensions

```text
2, 3, 4, 5
```

and found commutant nullity `1` in every case.

```text
max commutant residual       = 0.0
max unitary-invariance error = 1.9272741954495747e-16
max reference tensor error   = 0.0
```

The theorem is exact; the numerics validate the implementation.

### Meaning of “neutral”

`tau_d=I_d/d` is neutral only in the precise sense used here:

> it is the unique normalized state with no preferred local quantum frame.

v15.07 does **not** identify it with:

- the Genesis Pin;
- a physical vacuum;
- a source-free physical state;
- thermal equilibrium;
- a cosmological background;
- a pruning state;
- or a physical time origin.

Those would require independent derivations.

No entropy, pruning, or time primitive is used to select this reference.

---

# II. CANONICAL MULTIPLICATIVE LOCAL OPERATOR

Relative to the frame-neutral reference, define

\[
Q_d(\rho)
=\tau_d^{-1/2}\rho\tau_d^{-1/2}.
\]

Since \(\tau_d=I_d/d\),

\[
\boxed{Q_d(\rho)=d\rho}.
\]

For independent product states,

\[
\begin{aligned}
Q_{d_1d_2}(\rho\otimes\sigma)
&=(d_1d_2)(\rho\otimes\sigma)\\
&=(d_1\rho)\otimes(d_2\sigma)\\
&=Q_{d_1}(\rho)\otimes Q_{d_2}(\sigma).
\end{aligned}
\]

Therefore

\[
\boxed{
Q_{12}(\rho\otimes\sigma)=Q_1(\rho)\otimes Q_2(\sigma)
}
\]

is an exact multiplicative **operator** law.

This directly answers the lawful question left by v15.06:

```text
CANONICAL_RELATIVE_DENSITY_OPERATOR_IS_MULTIPLICATIVE
```

Executed controls gave

```text
max relative-operator tensor error = 6.675060769998483e-16
```

No arbitrary reference state was chosen: the reference was fixed by local-frame neutrality.

---

# III. THE ADDITIVE HERMITIAN GENERATOR IS CENTERED LOG RHO

Because \(Q_d(\rho)>0\) for faithful \(\rho\), define

\[
K_d(\rho)=\log Q_d(\rho).
\]

Then

\[
\boxed{
K_d(\rho)=\log\rho+\log d\,I_d
}.
\]

The multiplicative tensor law becomes additive:

\[
\boxed{
K_{12}(\rho\otimes\sigma)
=K_1(\rho)\otimes I
+I\otimes K_2(\sigma).
}
\]

After removing the central/projectively irrelevant component,

\[
\boxed{
K_d^0(\rho)
=\log\rho-rac{\operatorname{Tr}\log\rho}{d}I_d.
}
\]

This is exactly the centered logarithmic operator shape isolated conditionally in v15.04-v15.05.

Executed controls:

```text
max log tensor-additivity error   = 2.896658855432451e-14
max centered-log identity error   = 2.8379538820721116e-15
max local-frame covariance error  = 1.1729620862932955e-14
```

Therefore v15.07 materially strengthens the previous result:

```text
v15.05: log shape is unique IF a stronger functional-calculus tensor law is assumed.
v15.07: state + full local-frame neutrality canonically construct a multiplicative operator whose centered additive generator IS log rho.
```

That is an earned mathematical object, not a downstream fit.

---

# IV. CONDITIONAL NEUTRAL-TO-STATE PGRL THEOREM

The frozen PGRL family has the form

\[
\rho_s
=\frac{\exp(\log\rho_0+sP)}{Z_s}.
\]

Now set the baseline to the frame-neutral reference

\[
\rho_0=\tau_d=I_d/d
\]

and demand that a faithful target state \(\rho\) be the endpoint at some \(s>0\):

\[
\rho
=\frac{\exp(\log\tau_d+sP)}{Z}.
\]

Taking logarithms modulo the central normalization gives

\[
sP^0
=
\log\rho-rac{\operatorname{Tr}\log\rho}{d}I.
\]

Hence the **positive projective source-generator ray** is fixed:

\[
\boxed{
[P]_+
=
\left[
\log\rho-rac{\operatorname{Tr}\log\rho}{d}I
\right]_+.
}
\]

The overall magnitude remains unfixed because

\[
P\to aP,
\qquad
s\to s/a
\]

leaves the endpoint unchanged. This is consistent with the earlier RSCL/projective-source results.

Executed endpoint controls in dimensions `2,3,4,5` gave

```text
max endpoint reconstruction error = 6.123282208614186e-16
max generator identity error       = 3.5046408488399772e-15
product endpoint error             = 8.309111647037891e-16
```

Thus

```text
NEUTRAL_TO_STATE_PGRL_ENDPOINT_SELECTS_LOG_PROJECTIVE_RAY_CONDITIONALLY
```

is exact as a theorem about a declared neutral-to-state preparation problem.

The word **conditionally** is load-bearing.

---

# V. WHY THIS STILL DOES NOT PROVE “THE SOURCE IS LOG RHO”

The frozen PGRL source semantics do not say that every supplied state must be regarded as an endpoint prepared from \(I/d\) by its own physical source.

The archived source stack instead says:

- v13.04: PGRL/ETL is local in a source/deformation coordinate **at a supplied faithful state**; it does not prescribe the baseline-state origin.
- v13.11: \(P\) is an independently supplied Hermitian source generator in the exponential family.
- v13.25: the retained side supplies Genesis/source anchoring and source-current compatibility but not a state-preparation definition of sourcehood.
- v13.26: Genesis anchoring is source-origin identity/compatibility structure and does not turn the origin itself into an absolute source-strength law.
- v15.04: state covariance alone leaves \(a(r)\) free.
- v15.05: generic composition of already-chosen source laws does not select \(a(r)\).
- v15.06: multiplicative scalar recoverability does not bridge scalar comparison data into an operator source.

The v15.07 checker binds the exact archive blobs for these source-origin statements, including:

```text
v13.04 REPORT  e857d81f58a540833a7672fe769b2a301bad4459
v13.25 REPORT  65847800d6c079803e7c18537ef57cdc7f87da25
v13.26 REPORT  9917085b211ca0e1f4737082227f55097cc72b66
```

No audited frozen rule says

\[
\boxed{
\text{physical sourcehood}
\equiv
\text{neutral-reference-to-state preparation generator}.
}
\]

That identification cannot be inferred merely because the preparation generator is mathematically canonical.

---

# VI. SAME STATE, MULTIPLE VALID PGRL GENERATORS

This boundary is executable rather than semantic-only.

At one fixed faithful two-qubit product state, v15.07 applies finite PGRL deformations using three previously lawful generator families:

```text
linear
a logarithmic law
1+r^2 polynomial response
```

All produce positive normalized nearby states under the PGRL exponential map.

The minimum output eigenvalue was

```text
0.027251058487541124
```

and the maximum trace error was

```text
0.0
```

while their projective generator rays remain distinct:

```text
linear vs log        = 0.06248625684944288
linear vs polynomial = 0.08772246091732862
log vs polynomial    = 0.025253513918714537
```

Meanwhile the canonical neutral-relative generator agrees with the v15.04 logarithmic ray to

```text
5.77851202639302e-16.
```

So two statements are simultaneously true:

1. the neutral-relative construction canonically produces the logarithmic ray;
2. the frozen PGRL kinematics still permit other supplied generator rays at the same state.

Therefore

```text
CANONICAL_OPERATOR_GENERATOR_DOES_NOT_BY_ITSELF_DEFINE_THE_SOURCE
```

is the correct claim boundary.

---

# VII. WHAT v15.07 CHANGES

The upstream chain is now sharper:

```text
full local-frame symmetry
    -> unique normalized neutral reference tau_d = I/d
    -> canonical relative-density operator Q_d(rho)=d rho
    -> exact tensor multiplicativity
    -> canonical additive Hermitian generator log Q_d(rho)
    -> centered generator = centered log rho
    -> neutral-to-state PGRL endpoint fixes [centered log rho]_+ conditionally
    -X-> frozen proof that this preparation generator IS the physical source
```

The missing step is no longer:

- a logarithm;
- a multiplicative object;
- an operator-valued object;
- a frame-neutral reference;
- or a projective log-generator theorem.

All of those now exist.

The missing step is specifically the **ontology of sourcehood**.

---

# VIII. CLAIM BOUNDARY

## Derived / certified on this branch

- the unique fully local-frame-invariant normalized reference is \(I_d/d\);
- that reference composes exactly under independent tensor products;
- the relative-density operator \(Q_d(\rho)=d\rho\) is canonical and multiplicative;
- its logarithm is an additive Hermitian generator;
- after centering, the generator is exactly centered \(\log\rho\);
- the construction is local-frame covariant;
- a declared neutral-to-state PGRL endpoint fixes the positive projective centered-log generator ray;
- the absolute source-generator scale remains unfixed;
- multiple other supplied PGRL generator rays remain kinematically lawful at the same state;
- the audited frozen source-origin stack contains no rule identifying physical sourcehood with the neutral preparation generator.

## Not derived

- that \(I/d\) is the Genesis Pin or a physical vacuum;
- that every physical state is prepared from \(I/d\);
- that the neutral-to-state preparation generator is the physical gravitational/source operator;
- an absolute source scale;
- the retained-node-to-quantum-site carrier;
- the graph-site-to-`C^125/C^25` compatibility map;
- physical stress-energy;
- a source-to-solder/coframe law;
- physical spacetime or Einstein equations;
- a physical time primitive;
- Pillar 3 closure.

No ADM, Einstein, gravity, cosmology, or empirical residual was consulted to choose the logarithmic generator.

No entropy, pruning, or physical time was used as a pre-pruning selector.

---

# IX. SCIENTIFIC ASSESSMENT

v15.07 is a **major structural result**, because a search that began with an arbitrary qubit response function

\[
a(r)
\]

has now identified a canonical operator construction whose projective generator is the logarithmic law previously only known as a conditional candidate.

But it is not yet a broad scientific breakthrough, because the physical/ontological statement that would turn that generator into *the source* remains absent.

```text
major_structural_result = true
scientific_breakthrough = false
Pillar_3 = OPEN
```

---

# Stop rule / next lawful frontier

Do not declare

```text
P = centered log(rho)
```

as the physical source merely because v15.07 canonically constructs that generator.

Do not identify `I/d` with Genesis/vacuum/source-free physics without an independent law.

Do not use downstream gravitational performance to justify the missing semantic identification.

The next lawful question is now extremely narrow:

> **Does the frozen Genesis/provenance ontology independently imply that a source is the generator which prepares the observed local quantum state from the unique frame-neutral reference?**

If yes, then the positive projective logarithmic source ray is canonically selected without downstream fitting.

If no, the source-law-selection branch stops here and

```text
SOURCEHOOD_IS_NEUTRAL_PREPARATION_GENERATOR
```

must be introduced explicitly as a **NEW ASSUMPTION** before any downstream test.
