# v15.66 Result — ANALYTIC/NUMERIC DISAGREEMENT

Date: 2026-09-26.

Verdict: ANALYTIC_NUMERIC_DISAGREEMENT.

The preregistered numerical-cancellation confirmation failed.

Observed:
- analytic O-frame skew projections are ~1e-16;
- float64 four-corner raw numerators sit at a nearly t-independent ~few x 1e-15 floor, explaining the ~1/t float estimator;
- however, the 80-digit reconstruction reports O(1) mixed norms that are essentially independent of t, rather than <=1e-12.

Therefore NUMERICAL_CANCELLATION_CONFIRMED is not earned.

The O(1) high-precision result is inconsistent with both the analytic derivative and the float64 finite states by many orders of magnitude. Before treating it as a falsification of v15.61, the high-precision path must be audited for semantic equivalence: state representation, connected-correlation construction, polar branch/orientation, hidden-coordinate normalization, and four-corner source update.

No scientific theorem is changed in v15.66. The result is a method disagreement requiring audit.

Reproducibility:
- branch: research/v15.66-polar-derivative-numerics
- preregistration: 667d6b091b873520a1b166d73e638ecfccc00a4d
- RED run: 36275134785
- tested implementation: 80bae672c1c6c8e7e55202ea9081f2ced409aeca
- GREEN run: 36275180500
