# UQCF-GEM v14.02 — Convex-Dual Boundary Normal / Canonical Admissibility Response Design

## Goal

Test whether the already-earned convex geometry of the global quantum-compatibility fiber supplies an **objective-independent local dual direction** at its positivity boundary.

The gate does **not** invent another state-weighting functional and does **not** reopen the stopped v13/v14.01 coupling branches by fiat.

The central question is:

\[
\text{Does the intrinsic normal cone of the admissible compatibility fiber collapse to one ray at a boundary point?}
\]

If yes, global compatibility itself supplies a canonical **local dual direction** there. If no, even the boundary dual geometry remains nonunique.

A canonical dual ray is not yet a source law, coupling magnitude, spacetime normal, stress-energy tensor, or Einstein equation.

---

## Why this gate is lawful after v14.01

v14.01 established:

1. source action inside a fixed admissibility architecture is not a law-level deformation;
2. incidence alone gives no cycle defect, \(P_{\rm cyc}B^T=0\);
3. relationally weighted source→defect maps exist but are nonunique;
4. relabeling covariance, source linearity, strict disjoint composition, and positivity do not select one of those maps.

Therefore v14.02 must not try another arbitrary \(f(\chi)\).

The frozen archive already contains a different kind of native object: the **convex positive compatibility fiber** and its dual/supporting-witness geometry. The existing UQCF Quantum Compatibility Lab constructs feasible global completions, a full hidden kernel, exact radial positivity boundaries, and a matching optimization dual effect. The lab also explicitly states that its trace-distance objective and source paths are stipulated, so an optimizer dual witness cannot automatically be promoted to an ontology-native law.

v14.02 separates these two notions:

- **intrinsic normal cone** of the compatibility set — objective-free geometry;
- **optimization dual witness** — potentially objective-dependent and therefore not automatically physical.

---

## Primary executable object

Use the archived compatibility construction:

`Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py`

with the frozen matched family already implemented there.

Primary configurations:

- `V_A`;
- `V_B`;
- `FIXED_T = 21/41`.

Use the actual coefficient-space representation returned by `build_completion`:

\[
T=L X L^\dagger,
\]

with faithful center \(X_0\), and use the **full Hermitian hidden kernel** returned by `hidden_basis(L)`.

Do **not** use the chosen 3D visualization section as scientific evidence. The normal-cone audit acts on the full hidden affine fiber.

---

## Compatibility fiber

Let \(Q_a\) be an orthonormal Hermitian basis for the full hidden kernel of the marginal/observation map. Write

\[
X(x)=X_0+\sum_a x_a Q_a.
\]

The fixed-visible-data compatibility fiber is

\[
\mathcal F=\left\{x:\;X(x)\succeq0\right\}.
\]

This is a spectrahedron in the full hidden-coordinate space.

The center \(X_0\succ0\) lies in the interior and therefore has zero relative normal cone.

---

## Frozen numerical conventions

These conventions are frozen before execution.

- deterministic RNG seed: `1402`;
- primary radial directions: exactly `64` for `V_A` and exactly `64` for `V_B`;
- hidden-coordinate directions are Gaussian, then normalized in the Euclidean coordinate norm induced by the Hilbert–Schmidt-orthonormal hidden basis;
- Hermiticity residual tolerance: `1e-11`;
- hidden-kernel/marginal residual tolerance: `1e-10`;
- boundary PSD residual tolerance: `1e-10 * max(1, ||X_*||_2)`;
- nullity threshold:
  \[
  \tau_{\rm null}=10^{-9}\max(1,\|X_*\|_2);
  \]
- a boundary is called **simple** only if exactly one eigenvalue has absolute value at or below \(\tau_{\rm null}\) and the second-smallest eigenvalue is at least `100 * tau_null`;
- a boundary failing that spectral-gap rule is classified as **degenerate/near-degenerate**, never silently rounded to simple;
- normal-rank SVD threshold: `1e-10` relative to the largest singular value;
- support-identity and basis-invariance certification tolerance: `2e-9` relative error.

The final report must include the minimum simple-boundary spectral gap and the number of points classified as near-degenerate.

---

## Boundary construction

For a nonzero hidden direction

\[
D(u)=\sum_a u_a Q_a,
\]

normalize \(u\) in the Hilbert–Schmidt coordinate metric induced by the orthonormal hidden basis.

Because a hidden perturbation leaves the full visible marginal data fixed, its trace is zero up to the frozen numerical tolerance. A nonzero Hermitian trace-zero direction therefore has both positive and negative spectrum, so the outward radial boundary is defined without post-hoc direction rejection.

The exact radial positivity boundary is

\[
r_{\max}(u)
=-\frac{1}{\lambda_{\min}\!\left(X_0^{-1/2}D(u)X_0^{-1/2}\right)}.
\]

Then

\[
X_*(u)=X_0+r_{\max}(u)D(u)
\]

is PSD and lies on the boundary of the same fixed compatibility fiber.

The deterministic random survey is a geometry audit, not a physical source selector.

---

## Intrinsic relative normal cone

The scientific object is the normal cone **relative to the hidden affine fiber**, not the ambient equality-constraint normals.

At a boundary point \(X_*\), let \(V_0\) span `ker(X_*)` with nullity \(r\).

Every PSD-cone supporting matrix supported on the kernel has the form

\[
Y=V_0 Z V_0^\dagger,
\qquad Z\succeq0.
\]

Its projection into hidden-coordinate dual space is

\[
g_a(Y)=\operatorname{Re}\operatorname{Tr}(Q_aY).
\]

The cone generated by all such \(g(Y)\) is the intrinsic relative supporting cone of the spectrahedral fiber at that boundary point. We orient the covectors inward by the convention

\[
g\cdot(x-x_*)\ge0
\]

for feasible \(x\). In the conventional outward-normal sign convention, the normal cone is the negative of this cone. The gate is about the **ray**, not the sign convention.

### Smooth simple boundary

If `nullity(X*) = 1`, with normalized null vector \(v\), then

\[
Y\propto vv^\dagger
\]

and the intrinsic supporting cone is at most one ray:

\[
g_a=\operatorname{Re}\langle v,Q_av\rangle.
\]

If \(g\neq0\), this gives an objective-independent canonical local ray.

### Degenerate boundary

If `nullity(X*) = r > 1`, define the real-linear map

\[
\mathcal G:\operatorname{Herm}(r)\to\mathbb R^{d_H},
\qquad
Z\mapsto g(V_0 ZV_0^\dagger),
\]

where \(d_H\) is the hidden-coordinate dimension.

Compute the rank of \(\mathcal G\) using a complete orthonormal Hermitian basis on the kernel.

- If `rank(G) > 1`, the projected normal cone has a multidimensional linear span and is `NONUNIQUE_NORMAL_CONE`.
- If `rank(G) = 1`, additionally evaluate projected normals of kernel rank-one PSD projectors and verify they all lie on the same **positive** ray. Only then may the point be called ray-valued.
- If `rank(G) = 0`, the PSD boundary normal is annihilated by restriction to the hidden affine fiber and supplies `NO_BOUNDARY_SELECTOR` at that point.

This prevents an indefinite kernel-basis span from being mistaken for the PSD normal cone itself.

---

## Exact supporting-hyperplane identity

For a simple boundary null vector \(v\), define

\[
g_a=\langle v,Q_av\rangle.
\]

For any feasible point \(x\in\mathcal F\),

\[
g\cdot(x-x_*)
=\langle v,X(x)v\rangle
\ge0,
\]

because \(X(x)\succeq0\) and \(X_*v=0\).

Thus the ray is a genuine global supporting covector to the fixed compatibility fiber. This is an analytic identity; numerical controls only verify implementation.

Verification must include the center `X0`, convex interior points between `X0` and `X*`, and independently sampled feasible interior points generated by shrinking other radial directions.

---

## Basis invariance

The hidden basis is not itself physical. Under an orthogonal hidden-basis change

\[
Q'_a=\sum_b R_{ab}Q_b,
\]

the coordinate normal must transform as

\[
g'=Rg.
\]

The Hilbert–Schmidt representative

\[
N_H=\sum_a g_aQ_a
\]

must remain invariant to numerical precision.

Test at least eight deterministic orthogonal hidden-basis rotations per primary configuration. This basis-invariance test is required before calling the ray intrinsic.

---

## Objective-independence and typed-dual audit

The archived compatibility lab constructs a matching trace-distance dual effect in the **visible pair-state optimization problem**. The intrinsic normal `g` in this gate lives in the **dual of the hidden completion fiber**. These are different typed dual spaces.

Therefore:

- **Do not compare them for collinearity.**
- **Do not use the archived trace-distance dual effect to define or certify the hidden-fiber normal ray.**
- Record the archived object only as `VISIBLE_OBJECTIVE_DUAL_WITNESS_DIFFERENT_DUAL_SPACE`.

The actual objective-independence audit occurs wholly inside the hidden-fiber dual space:

1. Compute the intrinsic supporting cone directly from the PSD boundary kernel, without choosing any optimization objective.
2. At a simple boundary, all kernel-supported PSD normals must project to the same ray because the kernel is one-dimensional.
3. At a degenerate boundary, explicitly generate multiple kernel-supported rank-one PSD witnesses and test whether their projected covectors are collinear or span more than one direction.
4. For a simple boundary, use `g` and positive scalar multiples of `g` as supporting linear objectives and verify the same point satisfies the exact support inequality.
5. Add a deterministic covector with a nonzero component orthogonal to `g`; demonstrate that it is not an intrinsic normal at the same smooth boundary by constructing a feasible first-order/interior displacement that violates its support sign.

This distinguishes objective-free cone geometry from a dual variable manufactured by an externally selected objective.

---

## Interior and degenerate positive controls

### Interior control

At faithful \(X_0\succ0\), certify:

- minimum eigenvalue > 0;
- intrinsic relative normal-cone rank = 0.

Expected classification:

`NO_BOUNDARY_SELECTOR`.

### Synthetic degenerate-boundary control

Add a small explicitly labeled synthetic spectrahedron with a boundary point of kernel dimension at least 2 and two linearly independent projected kernel-supported PSD normals.

Expected classification:

`NONUNIQUE_NORMAL_CONE`.

This control proves the checker does not mechanically label every PSD boundary as a ray.

It is a test fixture, not evidence about UQCF-GEM physics.

---

## Boundary survey controls

For both `V_A` and `V_B`, survey the frozen 64 deterministic full-hidden-space radial directions.

Record for every boundary point:

- boundary radius;
- minimum eigenvalue residual;
- second-smallest eigenvalue / spectral gap;
- nullity at the frozen tolerance;
- simple vs near-degenerate classification;
- projected normal-cone span rank;
- positivity-ray consistency for degenerate rank-1 spans;
- intrinsic normal norm;
- support-identity residual;
- basis-change covariance/invariance error.

Aggregate:

- number of simple boundaries;
- number of degenerate/near-degenerate boundaries;
- number of zero projected normals;
- maximum support-identity error;
- maximum basis-invariance error;
- minimum simple-boundary spectral gap;
- distribution of normal-cone span ranks.

Do not infer universality beyond the surveyed frozen family.

---

## Source-response diagnostic — conditional only

Only if an intrinsic canonical local ray is found may the gate compute a **diagnostic pairing** with an already-earned source tangent in the **same hidden-coordinate space**:

\[
\sigma_s = g\cdot \dot x_s.
\]

This pairing is not allowed to define \(\dot x_s\).

The current frozen program does not yet certify a canonical source→hidden-completion tangent. Therefore the expected default status is

`CANONICAL_DUAL_DIRECTION_BUT_SOURCE_LIFT_UNDERIVED`

if a ray is found.

A stipulated source path from the old lab may be used only as an explicitly labeled sensitivity control and may not upgrade the scientific claim.

---

## Gate outcomes

Exactly one primary outcome is permitted for the actual compatibility-boundary audit.

### `CANONICAL_DUAL_RAY`

Every one of the 128 predeclared actual-lab primary boundary samples is either:

- simple with a nonzero intrinsic supporting cone of rank 1; or
- degenerate/near-degenerate but nevertheless has projected PSD normal cone proven to lie on one positive ray.

Additionally, all basis-invariance and support-identity controls must pass.

Interpretation:

- global compatibility supplies a canonical **local boundary dual ray** at every audited boundary sample in the frozen family;
- it does **not** select which boundary point a physical source reaches;
- it does **not** fix magnitude;
- it does **not** derive gravity.

### `NONUNIQUE_NORMAL_CONE`

At least one primary boundary sample has a genuine projected intrinsic normal-cone span rank > 1, or admits two kernel-supported PSD normals that project to inequivalent positive rays at the same boundary point.

Interpretation: even local dual direction is not uniquely selected there.

### `NO_BOUNDARY_SELECTOR`

No primary sample yields a nonzero projected intrinsic boundary normal after restriction to the hidden affine fiber, or the construction fails to reach a certified boundary under the frozen radial procedure.

Interpretation: the compatibility boundary supplies no usable local selector in the tested setup.

### Mixed numerical pathologies

If the frozen tolerance/gap rules leave a mixture that cannot be rigorously placed into one of the three outcomes—for example, unresolved near-degeneracy whose normal rank changes under the frozen numerical sensitivity checks—**do not force an outcome**. Record `UNRESOLVED_NUMERICAL_BOUNDARY` and stop the gate for numerical hardening. This is a verification failure state, not a scientific fourth outcome.

---

## Claim boundaries

Even a successful `CANONICAL_DUAL_RAY` means only:

> At the audited boundary points of the frozen global compatibility spectrahedron, positivity and the fixed observation constraints determine an objective-independent local supporting ray in the dual of the hidden affine fiber.

It does **not** establish:

- a canonical source→higher-incidence law;
- a source-selected boundary point;
- an absolute source or gravitational coupling;
- a physical coframe or stress-energy tensor;
- time, spacetime, curvature, or Einstein equations.

A successful ray would be a new lawful object that can be tested in a later gate against source/provenance structure without inventing a weighting functional.

A negative result must be reported as a local/global-compatibility geometry obstruction only, not as a theorem that no deeper theory can produce a dual selector.

---

## Implementation / verification requirements

- Work on branch `research/v14.02-convex-dual-normal`.
- Use TDD: RED checker before audit implementation.
- Reuse the archived compatibility lab mathematics; do not silently replace it with a new toy model.
- The synthetic degenerate example is allowed only as a checker positive control and must be labeled as such.
- Pin Python 3.11, NumPy, and SciPy versions in CI because the archived compatibility lab uses SciPy linear algebra/root finding.
- Bind the final checker to `SUMMARY.json`.
- Run exact-SHA branch CI before merge.
- Require branch to be 0 commits behind `main` before integration.
- Fast-forward `main` only after exact-SHA CI succeeds.
- Require post-merge v14.02 CI and preserved v14.01/v13.28 regression checks where path filters trigger.
- Pillar 3 remains OPEN regardless of this gate outcome.
- `scientific_breakthrough` defaults to `false`; upgrade only if the executed result genuinely warrants it under the program governance rules.
