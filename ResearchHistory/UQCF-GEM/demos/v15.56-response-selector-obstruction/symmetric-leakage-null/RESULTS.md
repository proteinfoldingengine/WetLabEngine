# v15.62 Results — COMPLETE

Date: 2026-09-26.

Verdict: SYMMETRIC_LEAKAGE_NULL_CONFIRMED.

Across all 12 frozen asymmetric states and all three edges (36 state-edge cases), six nonzero Hilbert-Schmidt-normalized polar-symmetric leakage directions produced zero effective rotational rank at all frozen parent-scaled cuts 1e-9, 1e-10, 1e-11.

Every leakage column had Frobenius norm approximately 1. The O-frame skew projection was numerical roundoff only. In the same Sylvester solver, the three skew positive-control directions had rank 3 on every edge at all three cuts.

Therefore v15.61's observable-projection statement survived the direct falsification attempt:

    nonzero retained-observable leakage
        does not imply
    nonzero rotational response.

The missing condition is nonzero polar-skew observable leakage.

This test is at the retained-observable layer. It does not yet prove that a differentiable normalized global source vector field can realize the constructed symmetric-null sector simultaneously across compatible marginals. That global lifting/existence problem is next.

Reproducibility:
- branch: research/v15.62-symmetric-leakage-null
- preregistration: 6f96a083e3bb623b6b4825e4b6bb229b48d98042
- RED run: 36274126750
- tested implementation: e657e8b87059908497bfabd14326aa792be34a6d
- GREEN run: 36274162573
