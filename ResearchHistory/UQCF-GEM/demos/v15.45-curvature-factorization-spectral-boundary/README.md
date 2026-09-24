# UQCF-GEM v15.45 — Curvature Factorization / Spectral Boundary

## Task-6 scientific adjudication

`FACTORIZATION_CERTIFIED_WITH_EXPLICIT_SPECTRAL_BOUNDARY`

This is the deterministic Tasks 1–5 scientific ledger result. Final exact-head whole-branch certification is Task 7 and remains outstanding.

The frozen differentiated-holonomy response on the four archived carriers admits the compact periodic-square form

    A = (I+X)(I+Y) Delta / 8,
    K_f = (A phi)_f J.

Tasks 1–2 verified the factorization coefficient-by-coefficient on L=5/L=7 at scales 1 and 7/3 and through the frozen frame/orientation/basepoint/relabeling presentations.

## Spectral boundary

The exact finite theorem gives:

| L | rank | nullity | centered nullity |
|---|---:|---:|---:|
| 5 | 24 | 1 | 0 |
| 6 | 24 | 12 | 11 |
| 7 | 48 | 1 | 0 |
| 8 | 48 | 16 | 15 |

For odd periodic L the only null direction is the constant field. For even L, the face-averaging factors annihilate the two Nyquist lines, giving centered nullity 2L-1. L6/L8 are mathematical formula-extension controls, not newly admitted physical carriers. No null modes were removed and no regulator or post-result carrier rule was introduced.

## Evidence dependency

All 592 archived canonical-control pairs are centered and have nonproportional full responses. On the archived odd carriers, all 592 of those response-nonproportionality statements follow from centered injectivity plus input nonproportionality. They are therefore correct but dependent evidence, not an additional independent selector.

Normalized quadratic face-profile comparisons are not forced by linear injectivity and remain separate descriptive comparisons.

Finite conditioning is descriptive only: the condition number is about 2.618 at L5 and 5.049 at L7. Two sizes do not establish a refinement or continuum trend, and no numerical threshold is used in a scientific gate.

## Source-correspondence firewall

For the canonical global-balance construction, upstream defines

    D_ax phi = s

on the augmentation subspace. Since the frozen curvature factorization gives

    A phi = (1/2) M D_ax phi,

the relation

    A phi = (1/2) M s

is `DEPENDENT_BY_CONSTRUCTION`. It cannot later be counted as independent evidence that a physical source produces curvature. The four controls likewise have explicit construction-dependent composition identities.

Source correspondence is therefore still `NOT_EVALUATED`.

## Claim boundary

This stage establishes a finite discrete operator identity, its exact finite spectral boundary, and an evidence-dependency/source-construction audit. It does not establish a physical metric, physical curvature, gravity, stress-energy, spacetime, Einstein equations, a continuum limit, foundational uniqueness, or a scientific breakthrough.

No fundamental time or dark-matter primitive is introduced. **Pillar 3 remains OPEN.**

## Deterministic ledger

`gate.py` produces canonical ASCII JSON and fails closed on a forged spectral boundary, dependency count, source firewall, or claim boundary. The canonical ledger is stored in `docs/RESULTS.json` and replayed with:

    python gate.py --check docs/RESULTS.json

Task 6 focused TDD: RED run `35928393176`; GREEN run `35928465247` on `5593d4c755683b44cb2096915c8ca73073ee3046`, 6/6 tests passed.

Final Task 7 must perform fresh whole-branch review and exact-head certification before v15.45 is closed.
