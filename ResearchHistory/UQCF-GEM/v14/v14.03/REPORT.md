# UQCF-GEM v14.03 — Projective Source-Ray / Hidden First-Contact Selection Gate

**Date:** 2026-09-12  
**Adjudication:** `PROJECTIVE_SOURCE_RAY_SELECTS_DUAL_RAY`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Executive result

For the two frozen archived compatibility families `V_A` and `V_B`, a **supplied positive projective support-space PGRL source ray** canonically determines:

1. the ray of its exact first-order hidden-completion tangent;
2. the corresponding **hidden-tangent radial first-contact point** on the fixed-visible-data PSD compatibility fiber; and
3. the objective-independent local dual ray already certified by v14.02 at that boundary point.

Across the frozen survey,

```text
64 V_A sources + 64 V_B sources = 128 sources
nonzero hidden source components = 128 / 128
simple/ray-valued first contacts  = 128 / 128
nonunique contacts                = 0
unresolved numerical contacts     = 0
```

The resulting conditional chain is

\[
\boxed{
[P]_+
\longrightarrow
[\Pi_{\rm hid}\dot X_P]
\longrightarrow
X_*(P)
\longrightarrow
[g(P)]
}
\]

for the audited construction and supplied source class.

This result does **not** establish that Genesis/provenance selects the support-space source ray `[P]`. The frozen provenance objects remain in a different typed space, with no certified natural map into the 25-dimensional Hermitian support-source space used here.

It also does **not** derive gravity, an absolute source normalization, `G`, stress-energy, spacetime, or Einstein equations.

---

## 1. Typed support-space source and exact PGRL tangent

The archived compatibility construction supplies an isometry

\[
L:\mathbb C^k\to\mathcal H,
\qquad
L^\dagger L=I,
\qquad
T=LX_0L^\dagger,
\]

with faithful coefficient-space state \(X_0\succ0\).

A Hermitian support-space source/log-density covector \(P\) therefore lifts as

\[
\widetilde P=LPL^\dagger.
\]

The normalized PGRL family is

\[
X_s(P)=
\frac{\exp(\log X_0+sP)}
{\operatorname{Tr}\exp(\log X_0+sP)}.
\]

Its exact first tangent is evaluated with the Fréchet derivative of the matrix exponential:

\[
\dot X_P
=
D\exp_{\log X_0}[P]
-X_0\,\operatorname{Tr}(X_0P).
\]

The implementation uses `scipy.linalg.expm_frechet`, which is analytically equivalent to the logarithmic-mean spectral formula and is numerically stable across repeated eigenvalues.

Fresh production controls give:

```text
max tangent Hermiticity residual = 0.0
max |Tr(dot X)|                  = 9.64939933512099e-18
max central-FD relative error    = 1.6582477388778675e-10
```

### Numerical-hardening note

The first implementation used explicit spectral divided differences for the logarithmic mean. A support-coordinate covariance audit exposed a `V_A` error at the `~10^-7` tangent level, amplified downstream in the dual representative. The failure was localized to repeated/near-repeated eigenvalue handling, not to the source→contact construction.

A direct hypothesis test replaced only that evaluation with the equivalent matrix-exponential Fréchet derivative. Covariance then returned to machine precision while the finite-difference derivative remained unchanged at the frozen accuracy. The production code was hardened accordingly; source sampling, scientific tolerances, boundary rules, and adjudication rules were not relaxed.

This debugging history is implementation evidence, not a separate scientific result.

---

## 2. Exact projective-source identity

For any \(a>0\) and scalar \(b\),

\[
X_s(aP+bI)=X_{as}(P).
\]

Hence, exactly,

\[
\dot X_{aP+bI}=a\dot X_P.
\]

Therefore source magnitude and identity shift are gauge-like parameterization freedoms for this step. The gate tests the transformed source **directly**, without re-centering or re-normalizing it.

The frozen survey gives:

```text
max tangent scaling error          = 4.789125308265857e-16
max hidden-direction drift         = 6.163108690215363e-14
max first-contact boundary drift   = 2.0131832593298626e-15
max oriented dual-ray drift        = 6.661338147750939e-16
```

Thus the map depends on the positive projective source ray rather than an absolute source magnitude in the audited construction.

This does not repair v13.26's observer-calibration obstruction. It shows only that absolute normalization is unnecessary for **this upstream direction-selection step**.

---

## 3. Canonical hidden tangent projection

Let \(Q_a\) be the full Hilbert–Schmidt-orthonormal hidden kernel of the visible marginal map, as certified by the archived compatibility lab and reused in v14.02.

The hidden tangent is the orthogonal projection

\[
V_P
=\Pi_{\rm hid}\dot X_P
=\sum_a
\operatorname{ReTr}(Q_a^\dagger\dot X_P)Q_a.
\]

This uses no fitted weighting function and no target physics.

All 128 frozen random sources had nonzero hidden component above the predeclared threshold:

```text
V_A: 64 / 64 nonzero
V_B: 64 / 64 nonzero
```

The maximum hidden-projector idempotence residual was

```text
1.547796903571955e-17
```

Two engineered controls behaved as required:

- an identity source produced zero PGRL tangent to `3.210776456982245e-17`;
- a constructed hidden-active tangent was recovered with hidden norm `0.9999999999999994` and target error `2.370471896426677e-15`;
- a constructed visible-only tangent had hidden norm `1.499385732841713e-19` and was classified `ZERO_HIDDEN_SOURCE_COMPONENT`.

The random survey therefore does not mechanically force every possible source tangent to be hidden-active.

---

## 4. Hidden-tangent radial first contact

For nonzero hidden tangent, define

\[
u_P=V_P/\|V_P\|_{\rm HS}.
\]

The gate does **not** evolve the physical PGRL family until it becomes singular. A faithful exponential family stays positive at finite parameter.

Instead it uses the linear hidden-affine continuation

\[
X(r)=X_0+r u_P
\]

and its first PSD boundary contact

\[
r_*(u_P)
=-\frac{1}
{\lambda_{\min}
\left(X_0^{-1/2}u_PX_0^{-1/2}\right)}.
\]

Then

\[
X_*(P)=X_0+r_*(u_P)u_P.
\]

In the original diagonal support coordinates, the coordinate-covariant implementation was explicitly checked against v14.02's certified radial formula:

```text
max relative formula mismatch = 4.5102810375396984e-17
max PSD residual              = 8.164027539109826e-17
```

All 128 first-contact points were simple and carried the v14.02 rank-1 intrinsic normal ray.

---

## 5. Support-coordinate gauge covariance

The coefficient basis on `ran(L)` is not physical. Under a support-coordinate unitary \(U\),

\[
L'=LU^\dagger,
\quad
X_0'=UX_0U^\dagger,
\quad
P'=UPU^\dagger,
\quad
Q_a'=UQ_aU^\dagger.
\]

The complete source→hidden-tangent→boundary→dual pipeline was recomputed under eight deterministic unitaries per configuration.

The maximum covariance error over the complete tested pipeline was

```text
3.8799143876726434e-13
```

well below the frozen `2e-9` gate.

This establishes that the positive result is not an artifact of the archived support-coordinate basis.

---

## 6. Relation to v14.02

v14.02 established:

\[
X_*\longrightarrow[g(X_*)]
\]

at the audited smooth compatibility boundaries.

v14.03 now establishes, for supplied projective PGRL source rays in the frozen support model,

\[
[P]_+
\longrightarrow
X_*(P)
\longrightarrow
[g(P)].
\]

So the right-hand side of the upstream selection problem is substantially tighter than after v14.01:

```text
supplied [P]
    -> exact full-state PGRL tangent
    -> canonical hidden projection
    -> hidden-tangent radial first contact X*
    -> canonical local dual ray [g]
```

The remaining origin problem is upstream of `[P]`.

---

## 7. Provenance audit

The current frozen Genesis/provenance/source-grading stack supplies:

- source-origin identity;
- retained source amount/grading;
- provenance consistency;
- source-flow/balance compatibility.

It does **not** currently return the same typed object required here: a Hermitian projective source/log-density covector on the 25-dimensional support coefficient space of the archived compatibility construction.

No certified natural map between those spaces is present in the frozen archive.

Therefore the provenance sub-audit is:

```text
PROVENANCE_SOURCE_TYPE_MISMATCH
```

This is stronger and cleaner than pretending the RNG source survey represents Genesis provenance. It does not.

The positive v14.03 result is explicitly conditional on supplying `[P]`.

---

## 8. What survives from earlier obstruction gates

Nothing in v14.03 retracts the recent no-go results.

### v14.01 remains valid

Arbitrary relationally weighted source→higher-incidence maps remain nonunique. v14.03 avoids that family by using the already-earned full-state PGRL tangent and the exact hidden orthogonal projection.

### v13.28 remains valid

The downstream absolute source→geometry coupling remains blocked. v14.03 selects an **upstream direction and local dual ray**, not an absolute gravitational coupling magnitude.

### v13.26 remains valid

Absolute observer source calibration is not derived. v14.03 instead shows that positive source rescaling drops out of the boundary-direction selection problem.

### v13.10 / v13.13 remain valid

The retained low-order ledger does not autonomously determine hidden source response, and exact response generically depends on full higher-order state information. v14.03 works directly with the full support state for precisely that reason.

---

## 9. Claim boundary

### Derived / reproducibly executed in the frozen model

- exact first-order PGRL tangent for a supplied support-space Hermitian source;
- canonical Hilbert–Schmidt projection of that tangent into the full hidden completion kernel;
- positive-projective invariance under `P -> aP+bI`, `a>0`;
- unique hidden-tangent radial first contact for every audited nonzero hidden source;
- v14.02 canonical local dual ray at every audited first contact;
- support-coordinate covariance of the composite map;
- `128/128` successful frozen source samples.

### Not derived

- Genesis/provenance → support-space source operator ray `[P]`;
- physical source magnitude or observer calibration;
- a physical statement that PGRL evolution hits a PSD boundary;
- source→solder/coframe law;
- absolute source→geometry coupling;
- stress-energy;
- physical spacetime or curvature;
- Einstein equations.

---

## Adjudication

\[
\boxed{\texttt{PROJECTIVE\_SOURCE\_RAY\_SELECTS\_DUAL\_RAY}}
\]

with the independent provenance status

\[
\boxed{\texttt{PROVENANCE\_SOURCE\_TYPE\_MISMATCH}}.
\]

The strongest defensible statement is:

> In the two frozen archived global-compatibility families, a supplied positive projective PGRL source ray canonically selects the ray of its hidden first-order response, the corresponding hidden-tangent radial first-contact point of the fixed-visible-data compatibility fiber, and the objective-independent local dual ray certified by v14.02. The frozen Genesis/provenance layer does not yet supply the required typed support-space source ray.

This is a **major positive structural result**, not a broad scientific breakthrough.

`scientific_breakthrough = false`.
