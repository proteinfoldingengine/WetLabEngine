# v15.45 Task 4 — conditioning and evidence-dependency audit

## Scope

Task 4 asks two deliberately separate questions about the frozen operator established in Tasks 1–3:

1. On the odd archived carriers, does exact centered injectivity also have a finite reconstruction scale, and how does that scale change from L=5 to L=7?
2. Which v15.44 canonical-control separation statements are logically forced once centered injectivity and input nonproportionality are already known?

No operator coefficient, admissibility rule, threshold, regulator, source law, or physical interpretation is changed by this task. Source correspondence remains NOT_EVALUATED and Pillar 3 remains OPEN.

## Dependency theorem used

Let A be linear and injective on the centered subspace. For centered u and v and scalar a,

    Au = a Av  =>  A(u-a v)=0  =>  u=a v.

Therefore, on a centered-injective carrier,

    u and v nonproportional  =>  Au and Av nonproportional.

This implication is not available when the centered kernel is nontrivial. Task 3 therefore supplies the exact scope boundary: the implication is valid on the archived odd L=5/L=7 carriers, but it cannot be promoted across the even-period formula extensions.

## Archived pair audit

The audit replays the frozen projected fields and the Task-1 compact operator for every archived canonical-control pair.

- total pairs: 592
- centered pairs: 592
- output-nonproportional pairs: 592
- output-nonproportional pairs classified as dependent on centered injectivity plus input nonproportionality: 592
- pairs for which that implication was unavailable: 0 on the archived odd carriers

Consequently, the v15.44 statement that every canonical-control pair has a nonproportional full matrix response is correct but is **not independent evidence** once centered injectivity and the corresponding input nonproportionality have been established. Matrix inequality follows as well.

This does **not** demote every v15.44 comparison statistic. In particular, equality or inequality of normalized quadratic face-invariant profiles is not determined merely by linear injectivity, so those profile comparisons are not reclassified by this theorem. Task 4 records all 592 such profile claims as not forced by injectivity.

## Conditioning diagnostic

For the periodic-square factorization

    A = (I+X)(I+Y) Delta / 8,

the visible Fourier response magnitude is evaluated only after the exact zero-mode set is selected symbolically. No floating threshold decides whether a mode is zero.

Descriptive values:

| L | centered injective | minimum nonzero response scale | maximum response scale | condition number | inverse minimum scale |
|---|---|---:|---:|---:|---:|
| 5 | yes | 0.34549150281252616 | 0.9045084971874740 | 2.6180339887498967 | 2.894427190999917 |
| 7 | yes | 0.18825509907063312 | 0.9504844339512097 | 5.048917339522309 | 5.3119411104227305 |

These are descriptive finite Fourier diagnostics, not scientific gate thresholds. The exact injectivity result remains exact; the numerical values indicate that the smallest visible response scale decreases between the two archived odd periods. Two sizes do not establish an asymptotic refinement law or continuum instability.

The even-period formula extensions remain noninjective on the centered domain by the exact Task-3 theorem, so a finite condition number on the full centered space is not asserted for them.

## Verification

Task-4 TDD RED was GitHub Actions run `35927196049`, which failed because `dependency_audit.py` did not yet exist.

Focused GREEN is run `35927335968` on exact head `23012d74c1976a9b0b9e1806bbc85c42df4a08ce`: 6/6 tests passed in 34.356 seconds under CPython 3.13.5.

The tests enforce that a nonconstant kernel blocks the dependency classification, contradictions are rejected on an injective centered domain, all 592 archived pairs are covered, and conditioning output has no threshold/tuning surface and cannot mutate the spectral certificate.

The separate long presentation regression is tracked independently and is not replaced by this focused run.

## Scientific consequence

Task 4 sharpens the evidence ledger rather than increasing the apparent evidence count:

- exact centered recoverability on the archived odd carriers remains an earned mathematical result;
- full-response pair nonproportionality is a dependent consequence for all 592 archived pairs, not a second independent selector;
- normalized-profile comparisons remain separate descriptive evidence;
- exact injectivity is distinct from stable reconstruction;
- the observed L=5 to L=7 conditioning change is insufficient to claim a continuum/refinement trend.

No source-correspondence verdict is emitted here. The next preregistered stage is Task 5, which must identify source-curvature relations already guaranteed by construction before any later physical source test.
