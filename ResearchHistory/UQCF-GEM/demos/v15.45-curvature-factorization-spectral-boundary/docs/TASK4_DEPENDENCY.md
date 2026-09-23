# v15.45 Task 4 — Conditioning and Evidence-Dependency Audit

## Scope

Task 4 asks two questions only:

1. Does exact centered injectivity on the archived odd carriers also have a useful stability margin?
2. Which v15.44 canonical-control separation statements are independent observations, and which follow automatically once centered injectivity and input nonproportionality are known?

The frozen operator is unchanged. No threshold, regulator, carrier selector, source correspondence, or downstream gravity fit is introduced. The even-size kernel obstruction from Task 3 remains intact.

## TDD receipts

Initial RED:
- Run `35927196049`
- Head `b3599d242ed992713ab7020932736e861a3026bd`
- Expected failure: `ModuleNotFoundError: No module named 'dependency_audit'`.

First GREEN established 592-pair coverage.

Dependency-classification RED:
- Run `35927551772`
- Head `755a03a6c3a576fe933901f05ae18e8f5d97504a`
- Expected failure: missing `claim_dependency` record.

Final focused GREEN before this documentation-only commit:
- Run `35927729021`
- Verified code head `ae4c2f70974ae6693cf70b2adf11f2072992ea10`
- CPython 3.13.5
- 8/8 Task-4 tests passed in 42.507 s.
- Task-3 exact spectral regression also passed on the same code head in run `35927729078`.

## Evidence-dependency result

All **592/592** archived canonical-control pairs are centered, and all **592/592** input pairs are nonproportional. On the archived L5/L7 carriers, Task 3 established that the centered kernel is zero. Therefore linearity plus centered injectivity gives

```text
A u = a A v   iff   u = a v
```

for centered fields on those carriers.

Consequently, once input nonproportionality is known:

- response nonproportionality is **DEPENDENT_ON_CENTERED_INJECTIVITY**;
- matrix inequality is **DEPENDENT_ON_CENTERED_INJECTIVITY**.

Those two v15.44 separation observations remain correct, but they are not independent physical selectors.

The following are **NOT_FORCED_BY_INJECTIVITY** and remain separate descriptive evidence:

- normalized face-invariant profile inequality;
- energy differences;
- individual face-invariant differences;
- field/visible/kernel norm differences and normalized ratio differences.

Injectivity alone does not determine any of those quadratic or distributional comparisons.

## Conditioning result

For the scalar compact operator

```text
A = (I+X)(I+Y) Delta / 8
```

the visible Fourier-mode magnitude is evaluated only after the exact zero-mode set is fixed symbolically. No floating threshold decides whether a mode is zero.

| L | Centered injective | Smallest nonzero response scale | Largest response scale | Condition number |
|---|---|---:|---:|---:|
| 5 | yes | 0.34549150281252616 | 0.9045084971874740 | 2.6180339887498967 |
| 7 | yes | 0.18825509907063312 | 0.9504844339512097 | 5.048917339522309 |

Thus the archived finite operators are exactly injective after centering, but the smaller visible scale decreases from L5 to L7 and the descriptive condition number increases. This is evidence that exact injectivity must not be conflated with uniform stable reconstruction or a refinement theorem.

These numbers are descriptive only. They cannot alter operator coefficients, admissibility, scientific thresholds, or any gate outcome.

## Claim boundary

Task 4 does not evaluate source correspondence and does not establish physical curvature, gravity, stress-energy, Einstein equations, spacetime, a continuum limit, or foundational uniqueness. The even-period Task-3 obstruction is unchanged. Pillar 3 remains OPEN.

Next planned task: **Task 5 — source-correspondence firewall**, which will identify source-curvature relations already implied by the frozen construction before any later physical source test.
