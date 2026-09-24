# UQCF-GEM v15.45 — Curvature Factorization / Spectral-Boundary Preregistration

**Status:** approved next scientific step; preregistration only. No v15.45 scientific outcome is claimed by this document.

## Parent and purpose

Parent: v15.44 certified head `9085e4fa0bec3dbd700f759a8a9629b230d226ff`.
Certification: GitHub Actions run `35814970929` completed successfully.

v15.44 exactly characterized the frozen finite response-curvature map on the four inherited L=5/L=7 carriers. The next task is to explain that operator structurally and determine its spectral/domain boundary before any new source-correspondence or gravity interpretation is attempted.

This gate preserves the program rules: no fundamental time, no dark-matter primitive, no downstream gravity fit, no transport retuning, and no post-result choice of admissible carriers.

## Hypothesis to test

In a canonical consistently oriented square-torus presentation, define

```text
Delta = 4 I - X - X^{-1} - Y - Y^{-1}
M     = (1/4) (I + X)(I + Y)
```

and let `J=[[0,-1],[1,0]]` in the chosen oriented orthonormal frame.

The review-level candidate factorization is

```text
chi = (1/2) M Delta phi
K_f = chi_f J
```

up to the already-certified frame/orientation/basepoint transformation rules.

This identity is **not yet an archived-carrier theorem**. v15.45 must derive it from the frozen v15.44 coefficient formula and verify it against the actual archived operators without using archived outcomes to alter the formula.

## Required tests

1. **Actual-carrier factorization.** On all four inherited v15.44 carriers (L=5 and L=7, scales 1 and 7/3), compare every exact operator coefficient with the independently constructed compact factorization after applying the declared presentation alignment.
2. **Presentation controls.** Repeat the equality through the frozen frame, orientation, basepoint, relabeling and scale controls. No comparison may rely on raw matrix entries across mismatched frames.
3. **Kernel explanation.** Prove from the factorization why the odd-size certified carriers have only the constant kernel, and independently reproduce the v15.44 exact rank/nullity certificates.
4. **Spectral/parity falsifier.** Before looking at results, test even periodic sizes L=6 and L=8 under the same frozen formula. Do not redefine the carrier class, modify the averaging map, remove modes, or add a regulator after exposure.
5. **General finite spectral statement.** If supported, state the exact Fourier/spectral condition for kernel membership and distinguish theorem from finite checks. In particular test whether modes at X=-1 or Y=-1 are annihilated by M.
6. **Conditioning/refinement diagnostic.** Distinguish exact injectivity from stable reconstruction. Report the smallest nonzero singular/eigen response scale or an exact equivalent where lawfully derivable; do not use it to tune the operator.
7. **Pair-separation dependency audit.** Determine which v15.44 canonical-control separation statements follow automatically from centered injectivity plus input nonproportionality, and mark those as dependent consequences rather than independent physical evidence.
8. **Source-correspondence firewall.** No new physical source correspondence is evaluated in this gate. Before a later source test, algebraically compose the frozen response-generation law with the curvature factorization and identify every correspondence that is already guaranteed by construction.

## Predeclared adjudication

A valid null, parity obstruction, or conditioning failure is a successful scientific characterization.

Possible outcomes include:

- `FACTORIZATION_CERTIFIED_WITH_EXPLICIT_SPECTRAL_BOUNDARY`
- `FACTORIZATION_CERTIFIED_BUT_ARCHIVED_PRESENTATION_REQUIRES_REFINEMENT`
- `CANDIDATE_FACTORIZATION_FALSIFIED_ON_ARCHIVED_CARRIER`

The outcome must be selected mechanically from preregistered exact checks; wording may not be changed to rescue the hypothesis.

## Claim boundary

Even a successful factorization establishes a discrete finite operator identity, not physical curvature, gravity, spacetime, stress-energy, Einstein equations, a continuum limit, or foundational uniqueness. The global-balance source/response semantics introduced upstream remain conditional. Pillar 3 remains OPEN.

The purpose of this gate is to identify exactly what v15.44 measures, expose any spectral edge/parity limitation, and prevent a future source-correspondence test from rediscovering an identity already implied by the chosen response law.
