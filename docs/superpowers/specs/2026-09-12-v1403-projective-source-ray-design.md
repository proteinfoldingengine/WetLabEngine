# UQCF-GEM v14.03 — Projective Source-Ray / Hidden First-Contact Selection Design

## Goal

Test whether an already-supplied **projective PGRL source ray** on the full support state canonically determines

\[
[P]_+ \longrightarrow [\Pi_{\rm hid}\dot X_P]
\longrightarrow X_*(P)
\longrightarrow [g(P)].
\]

Here \([P]_+\) quotients positive rescaling and identity shifts only.

The gate does **not** claim that a finite PGRL trajectory reaches the PSD boundary. For faithful finite-dimensional states, the normalized exponential family remains positive for every finite source parameter. The boundary object in v14.03 is instead the first PSD contact of the **hidden component of the first-order PGRL tangent** under linear radial continuation inside the fixed-visible-data hidden affine fiber.

A positive result would therefore be a theorem about a supplied projective source direction and the frozen compatibility geometry—not a source-origin law, dynamics law, coupling law, or gravity derivation.

---

## Prior results that constrain this gate

v14.03 must preserve the following results.

- **v13.10:** the frozen retained ledger does not determine hidden completion response; W1/W2/W3, F2/F3, atlas closure and related certificates cannot be promoted into a hidden selector without a new rule.
- **v13.13:** exact source response generically depends on the full higher-order quantum completion, not on a fixed low-body-order geometric summary.
- **v13.26:** absolute source normalization is not derived; however \(P\to aP\), \(s\to s/a\) with \(a>0\) leaves the PGRL state family unchanged.
- **v14.01:** arbitrary weighted source→higher-incidence maps remain nonunique.
- **v14.02:** at every one of the 128 audited smooth full-hidden-space boundary points of the frozen `V_A`/`V_B` compatibility families, the intrinsic relative normal cone is a nonzero rank-1 ray.

Thus v14.03 may use the full support state and a supplied PGRL source ray, but it may not ask the retained ledger to reconstruct hidden response and may not invent another arbitrary source-weighting functional.

---

## Primary archived construction

Reuse without replacement:

`Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py`

with:

- `V_A`;
- `V_B`;
- `FIXED_T = 21/41`;
- `build_completion`;
- `hidden_basis`.

For either configuration, the archived construction supplies

\[
T=LX_0L^\dagger,
\qquad
L^\dagger L=I_k,
\qquad
X_0\succ0,
\qquad
\operatorname{Tr}X_0=1.
\]

The full hidden Hermitian kernel of the visible marginal map is spanned by Hilbert–Schmidt-orthonormal matrices \(Q_a\) returned by `hidden_basis(L)`.

The 3D visualization section is excluded from scientific adjudication.

---

## Typed support-space source

Let \(P=P^\dagger\) be a Hermitian log-density/source covector on the coefficient support \(\mathbb C^k\). Its physical support lift is

\[
\widetilde P=LPL^\dagger.
\]

Because \(L\) is an isometry, the coefficient-space PGRL family

\[
X_s(P)=
\frac{\exp(\log X_0+sP)}
{\operatorname{Tr}\exp(\log X_0+sP)}
\]

is the support-coordinate representation of the corresponding exponential family on `ran(L)`.

This gate therefore does not introduce a second unrelated source type. But \([P]_+\) is still **supplied**: the current Genesis/provenance stack has not been shown to select this same-space operator ray.

---

## Exact PGRL tangent

Define

\[
\dot X_P=
\left.\frac{dX_s(P)}{ds}\right|_{s=0}.
\]

If

\[
X_0=U\operatorname{diag}(p_i)U^\dagger,
\qquad
\widehat P=U^\dagger P U,
\]

then use the logarithmic mean

\[
\mathcal L(p_i,p_j)=
\begin{cases}
\dfrac{p_i-p_j}{\log p_i-\log p_j}, &p_i\ne p_j,\\[5pt]
p_i,&p_i=p_j,
\end{cases}
\]

and

\[
\widehat{\dot X}_{ij}
=
\mathcal L(p_i,p_j)\widehat P_{ij}
-
\delta_{ij}p_i\operatorname{Tr}(X_0P).
\]

Transform back with \(U\).

Required controls:

- tangent Hermiticity;
- \(\operatorname{Tr}\dot X_P=0\);
- agreement with symmetric finite differences of the normalized exponential family;
- equivalence with a matrix-exponential Fréchet derivative if that is used computationally.

---

## Exact projective-source identity

For all \(a>0\) and real \(b\),

\[
X_s(aP+bI)=X_{as}(P),
\]

so

\[
\dot X_{aP+bI}=a\dot X_P.
\]

This identity is analytic and must not be manufactured by preprocessing.

### Critical testing rule

For the projective invariance controls, begin with each frozen stored base source `P` and form

\[
P' = aP+bI
\]

directly.

**Do not re-center or re-normalize `P'` before evaluating its tangent.**

Otherwise positive-scale/identity invariance would be partly enforced by the test harness rather than tested as a consequence of the normalized exponential family.

The downstream target is

\[
[\Pi_{\rm hid}\dot X_{P'}]
=
[\Pi_{\rm hid}\dot X_P],
\]

\[
X_*(P')=X_*(P),
\]

\[
[g(P')]=[g(P)].
\]

Negative source scaling is not quotiented. `-P` may select the opposite hidden radial direction and a different boundary point.

---

## Canonical hidden tangent component

The full hidden tangent space is

\[
\mathcal H_{\rm hid}=\operatorname{span}_{\mathbb R}\{Q_a\}
\]

with the inherited trace inner product

\[
\langle A,B\rangle_{HS}
=
\operatorname{ReTr}(A^\dagger B).
\]

Because the archived hidden basis is Hilbert–Schmidt orthonormal,

\[
V_P
=
\Pi_{\rm hid}\dot X_P
=
\sum_a
\operatorname{ReTr}(Q_a^\dagger\dot X_P)Q_a.
\]

This is the orthogonal projection of the full source tangent onto the exact kernel of the visible marginal map.

If

\[
\|V_P\|_{HS}>	au_{\rm hidden},
\]

define

\[
u_P=V_P/\|V_P\|_{HS}.
\]

Otherwise record `ZERO_HIDDEN_SOURCE_COMPONENT` and do not normalize numerical noise.

Important boundary: the actual source tangent may also contain visible components. v14.03 does not claim that the PGRL physical trajectory remains inside the fixed-visible-data fiber.

---

## Hidden-tangent radial first contact

For nonzero \(u_P\), reuse the v14.02 radial construction:

\[
r_*(u_P)
=-\frac{1}
{\lambda_{\min}(X_0^{-1/2}u_PX_0^{-1/2})},
\]

and

\[
X_*(P)=X_0+r_*(u_P)u_P.
\]

Because a nonzero hidden perturbation is Hermitian and trace-zero, it must have both positive and negative spectrum; the outward radial PSD contact is therefore well defined for the audited faithful centers.

The report must call this object a **hidden-tangent radial first contact**. It must not be called a PGRL boundary crossing or a finite source endpoint.

At `X_*(P)`, reuse the v14.02 intrinsic relative normal construction to obtain the inward Hilbert–Schmidt dual ray

\[
[g_P].
\]

---

## Source survey

For each of `V_A` and `V_B`:

- RNG seed: `1403`;
- exactly 64 primary Hermitian source covectors;
- generate complex Gaussian `A` and set `P=(A+A†)/2`;
- for the **base frozen source only**, remove `Tr(X0 P) I` and normalize its Hilbert–Schmidt norm;
- store that base `P` unchanged for all downstream projective tests;
- record SHA-256 of the source-array bytes.

The source distribution is a deterministic generic survey, not a physical provenance model.

Required separately labeled controls:

1. `IDENTITY_SOURCE_CONTROL`: `P=I`, which must give zero normalized PGRL tangent;
2. `HIDDEN_ACTIVE_CONTROL`: at least one predeclared source with nonzero hidden projection;
3. `VISIBLE_ONLY_TANGENT_CONTROL`: construct only if an exact, non-tuned source can be obtained from the frozen linear algebra. Otherwise record `NOT_CONSTRUCTED` rather than optimizing a post-hoc example.

Primary zero-hidden sources must remain in the sample and must not be resampled.

---

## Frozen numerical conventions

- Python `3.11`;
- NumPy `2.4.6`;
- SciPy `1.17.1`;
- seed `1403`;
- 64 sources for `V_A` and 64 for `V_B`;
- symmetric finite-difference epsilon `1e-6`;
- source Hermiticity tolerance `1e-12`;
- tangent Hermiticity tolerance `2e-11`;
- tangent trace tolerance `2e-11`;
- finite-difference relative error tolerance `2e-7`;
- hidden threshold
  \[
  \tau_{\rm hidden}=10^{-10}\max(1,\|\dot X_P\|_{HS});
  \]
- boundary PSD residual tolerance `2e-9`;
- nullity threshold
  \[
  \tau_{\rm null}=10^{-9}\max(1,\|X_*\|_2);
  \]
- projective hidden-direction drift tolerance `2e-9`;
- boundary-point relative drift tolerance `2e-9`;
- inward dual-ray drift tolerance `2e-9` using
  \[
  1-\widehat N_1\!:\!\widehat N_2,
  \]
  **without an absolute value after the inward orientation has been fixed**;
- support-coordinate covariance tolerance `2e-9`.

Positive scales:

`[0.2, 0.5, 2.0, 5.0, 11.0]`.

Identity shifts:

`[-3.0, -0.7, 0.4, 2.5]`.

Do not revise thresholds after inspecting execution results.

---

## Support-coordinate gauge covariance

The coefficient basis on `ran(L)` is not physical. For a unitary support-coordinate change \(U\), use

\[
L'=LU^\dagger,
\quad
X_0'=UX_0U^\dagger,
\quad
P'=UPU^\dagger,
\quad
Q_a'=UQ_aU^\dagger.
\]

Then

\[
L'X_0'L'^\dagger=LX_0L^\dagger,
\qquad
L'P'L'^\dagger=LPL^\dagger.
\]

Required checks:

\[
\dot X'=U\dot XU^\dagger,
\]

\[
V_P'=UV_PU^\dagger,
\]

\[
X_*'=UX_*U^\dagger,
\]

and the normalized inward Hilbert–Schmidt dual representative transforms by the same conjugation.

Use eight deterministic unitary coordinate changes for each configuration.

Additionally, for at least one coordinate change per configuration, recompute `hidden_basis(L')` and verify that its hidden-space orthogonal projector agrees with the conjugated original hidden-space projector. This ensures covariance is a property of the hidden subspace, not only of a manually rotated basis.

---

## Dual-ray orientation and comparison

At a simple radial boundary, let `v` be the unique null vector and define

\[
g_a=\operatorname{Re}\langle v,Q_av\rangle.
\]

Construct the Hilbert–Schmidt representative

\[
N_H=\sum_a g_aQ_a.
\]

Orient it inward by requiring positive pairing with the center displacement `X0-X*`, then normalize by Frobenius norm.

All projective-source and support-coordinate comparisons use this normalized, inward-oriented Hilbert–Schmidt representative. Once this orientation is fixed, opposite sign is a failure, not an equivalent ray for the numerical invariance test.

---

## Outcome logic

### `PROJECTIVE_SOURCE_RAY_SELECTS_DUAL_RAY`

For every primary source with nonzero hidden component:

- analytic and finite-difference PGRL tangents agree;
- raw transformed sources `aP+bI` produce the exact expected tangent scaling without harness re-normalization;
- normalized hidden tangent direction is invariant under positive source scaling and identity shifts;
- the hidden-tangent radial first-contact point is unique and stable;
- the first contact is simple/ray-valued under the frozen v14.02 rules;
- the inward dual representative is invariant under projective source transformations;
- the entire construction is support-coordinate covariant;
- no same-projective-source ambiguity survives.

Interpretation: a **supplied projective PGRL source ray** selects a canonical hidden radial contact and its v14.02 local dual ray in the frozen compatibility model.

### `SOURCE_TO_BOUNDARY_NONUNIQUE`

At least one nonzero-hidden primary source produces inequivalent hidden directions, boundary contacts, or inward dual rays under transformations that represent the same projective source or the same support-coordinate gauge orbit.

### `NO_HIDDEN_SOURCE_CONTACT`

All 128 primary supplied sources have hidden tangent norm below the frozen threshold.

### `UNRESOLVED_NUMERICAL_SOURCE_LIFT`

Numerical sensitivity prevents stable adjudication under the frozen tolerances. This is a verification-stop state, not a scientific result.

A mixed zero/nonzero-hidden survey is allowed. Record zero-hidden and nonzero-hidden counts; do not discard null cases.

---

## Required telemetry

For each configuration record:

- support dimension;
- hidden dimension;
- source-array SHA-256;
- zero-hidden count;
- nonzero-hidden count;
- hidden-fraction distribution
  \[
  \|V_P\|_{HS}/\|\dot X_P\|_{HS};
  \]
- minimum nonzero hidden fraction;
- maximum analytic-vs-finite-difference tangent error;
- maximum tangent Hermiticity and trace residuals;
- maximum raw projective tangent-scaling error;
- maximum hidden-direction drift under all `a,b` controls;
- maximum first-contact boundary drift;
- maximum inward dual-ray drift;
- maximum support-coordinate covariance error;
- number of simple, degenerate and unresolved first-contact boundaries.

Global output must include the same aggregates across all 128 primary sources.

---

## Provenance/source-ray sub-audit

This is logically separate from the supplied-source gate.

Audit the frozen archive for whether Genesis/provenance/source grading already returns the required support-space projective operator \([P]_+\).

Allowed statuses:

- `PROVENANCE_TO_SOURCE_RAY_DERIVED` — only if an already-certified natural construction actually returns the required same-space projective operator;
- `PROVENANCE_TO_SOURCE_RAY_UNDERIVED` — provenance identifies source origin/amount/compatibility but not the operator ray;
- `PROVENANCE_SOURCE_TYPE_MISMATCH` — existing provenance data live in a different typed space with no certified natural map to the required operator ray.

The random source survey cannot upgrade this status.

---

## Claim boundary

Even a successful primary outcome means only:

> In the frozen archived compatibility families, a supplied support-space PGRL source direction, modulo positive scale and identity, has a canonical Hilbert–Schmidt hidden tangent component; when that component is nonzero, its radial first contact with the fixed-visible-data PSD fiber selects the local canonical dual ray established by v14.02.

It does **not** establish:

- that the physical PGRL trajectory reaches that boundary;
- that nature follows linear radial continuation of the hidden tangent;
- that Genesis/provenance selects the source operator ray;
- an absolute source magnitude;
- stress-energy, source→coframe dynamics, or absolute coupling;
- gravity, physical curvature, spacetime, or Einstein equations.

If provenance remains underived, the architecture after a positive primary result is

\[
\text{provenance}
\quad ? \quad
\longrightarrow [P]_+
\longrightarrow u_P
\longrightarrow X_*(P)
\longrightarrow[g_P].
\]

The linear radial continuation is a geometric construction on the hidden tangent ray, not a dynamical law.

---

## Implementation and verification requirements

- Work on `research/v14.03-projective-source-ray`.
- Use TDD: checker/CI RED before implementation.
- Reuse the archived compatibility lab and v14.02 normal-cone mathematics rather than replacing either with a toy primary model.
- Pin Python/NumPy/SciPy versions in CI.
- Bind the final checker to `SUMMARY.json`.
- Exact-SHA branch certification is required before integration.
- Branch must be 0 commits behind `main` before fast-forward integration.
- Post-merge v14.03 certification is required, with v14.02/v14.01/v13.28 regression checks where path filters trigger.
- Pillar 3 remains OPEN regardless of v14.03 outcome.
- `scientific_breakthrough` defaults to `false`; upgrade only if the executed evidence genuinely warrants it under project governance.
