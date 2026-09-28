# Pre-measurement review

Independent reviewer review1607 found no blockers and independently passed all five tests without executing the ensemble. The review checked symbolic continuum identities, coefficientwise rank bounds for every fixed nonzero coherence, the separate exact polynomial-rank proof at zero, endpoint provenance, common order baselines/scaling, identity-middle control, class gaps, covariance/precision gates, expected 144/1728/2592 counts and negative-result handling.

The reviewer emphasized the fixed-λ then s↓0 scope: no uniformity or joint-limit claim follows. Local and preregistered GitHub RED both produced the five expected absent-implementation failures. No ensemble was run locally before the scientific workflow.

## Determinant recording correction after first INVALID execution

The initial scientific run reached the numerical limit recording step and raised a TypeError inside mpmath 1.3.0's pivoted LU determinant for a rank-one matrix. `DETERMINANT_REGRESSION.json` stores the exact internal mpmath binary numbers of the reproducer (the already-audited candidate22/a1/isotropic/after/native baseline polar at 80 digits), not rounded decimal approximations. The old determinant raises the same TypeError on this fixture. A new test was observed RED before implementation.

The correction uses the ordinary division-free 3×3 determinant formula for the descriptive determinant field. This avoids pivot selection on singular matrices, without changing a path, rank certificate, threshold, input, limit or validity criterion. All six tests now pass, including the exact reproducer and positive/negative determinant controls. The original failed result, implementation, tests, source checksums and logs remain under `failed-*`, with `FAILED_ATTEMPT.json` and a filename map. They retain INVALID status.

Independent re-review approved this minimal fix, reproduced the original TypeError, and independently passed all six tests without an ensemble run. The regression intentionally pins the mpmath 1.3.0 behavior; a future dependency upgrade may require updating the assertion about the old routine.
