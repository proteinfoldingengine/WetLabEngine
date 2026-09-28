> Completion update: this preimplementation design was superseded by PREREGISTRATION.md and executed. See RESULTS.md for the completed 16.03 results.

# v16.03 next measurement design — finite-source order response

Status: concrete design for the next implementation. No finite-source measurement has been run. This is not yet an executable preregistration or a claim of a nonzero cubic coefficient.

## Objective

Test the cubic coefficient derived in DERIVATION.md for disjoint source channels separated by the inherited intermediate channel. Separately verify local finite continuation of the overlapping-source invariant response.

Use the 12 archived states, all 81 weight-four probe columns, both planar/isotropic preparations, both source pairs and both orders. Preserve a=1 and the exact archived binary values of 1/3 and 1/6. Include a=0 only as an erasure/undefined-domain control.

## Method to freeze before execution

1. Reuse the independent global 256-component Pauli construction at 50 and 80 digits. Construct actual finite centers using E_X(lambda)=I+lambda L_X; do not substitute the source-origin center.
2. Compute connected correlations including finite-center one-body subtraction. Evaluate J_o^phys and its normalization by the known lambda squared factor; never normalize a measured response to make it agree with its parent.
3. Evaluate T_a=D^2F(C_0)[V_f-V_r,B_a] through a differentiated polar/Sylvester calculation independent of finite lambda differencing. Include the connected-centering derivatives in V. Record the full 3x81 tensor, singular spectrum and invariant frame comparison.
4. Use fixed mixture parameters lambda=2^-4,2^-5,2^-6,2^-7,2^-8 for direct finite-center evaluation. These are convex-mixture parameters, not the previous u strength. Do not shrink a failed step until it passes. Record domain exits as scientific outcomes.
5. Check Delta J/lambda^3 against T_a for disjoint protocols and Delta J/lambda^2 against the parent contrast for overlapping protocols. Record residuals at every step, including exact-null cases. Do not fit an exponent and call the fit a derivation.
6. Preserve the a=1 disjoint full-protocol null, lambda=0/one-source-null checks, invalid/nonfinite override, coordinate covariance, 50/80-digit convergence, density physicality, and explicit unsupported-domain rejection.
7. Freeze numerical coefficient/nonzero and convergence adjudication rules, dependency hashes, failure-injection tests and a targeted workflow before any measurement. Retain the existing 1e-35 arithmetic covariance and 1e-30 cross-precision bounds; keep the existing three rank thresholds. Derive finite-step remainder checks from the derivative order and numerical conditioning, not observed outcome adjustment.

## Decision boundary

Possible scientific outcomes include a valid nonzero cubic coefficient, a valid cubic null (including an exact structural null), or a finite-domain obstruction. A failed arithmetic/covariance/physicality control gives INVALID rather than a scientific NO.

A nonzero coefficient would establish finite order sensitivity caused by the inserted channel under the specified source/preparation law. It would not establish universal source coupling or gravity. Origin rank equality at all finite steps is not required: finite centers can activate new directions.

## Implementation scope

A new finite-source-continuation gate and tests should consume the immutable 16.02 dependency path. Earlier code and historical verdicts stay byte-identical. Keep native and transformed computations independent, archive raw JSON/checksums/job logs, inspect the exact run, and publish both positive and negative results on the research branch. Do not merge to main.

This design leaves the quantitative finite-step remainder rule to be derived and frozen before implementation; it must not be selected after observing measurements. No expensive new CI run is justified until that rule and the independent Hessian implementation are reviewable.
