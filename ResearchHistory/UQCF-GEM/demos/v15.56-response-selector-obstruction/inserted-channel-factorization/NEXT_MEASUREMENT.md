# v16.04 numerical audit — proposed scope

Status: design only. No preregistration freeze, implementation, workflow run or measurement is claimed.

## Objective

Audit the commutator/Hessian factorization in DERIVATION.md against the already published v16.03 coefficient, and quantify the two source contributions without retuning the model.

## Frozen inputs to retain

Use publication a451398b307f89a380736186f387cf61f80718c1 and scientific implementation 850dc3538f04ce9efcb3e974fa04992bcb1cb150 as the parent references. Retain all 12 states, all 81 hidden probes, both preparation arms, native and transformed frames, 50/80-digit arithmetic, and the archived binary values 1, 1/3 and 1/6. Preserve all spectral-domain and rank thresholds. Complete erasure is outside the polar calculation.

## Proposed independent construction

Construct the 256-dimensional Pauli weight blocks of [D-A,M_a] directly using (a^u-a^v)(D-A)_vu. Compare against direct operator composition, before geometry. Apply the connected differential including one-body subtraction. Evaluate the two source contributions separately, sum with the declared sign, and compare with the parent cubic matrices.

Archive block norms, retained direction norms, each 3x81 source contribution, summed coefficient, parent discrepancy, covariance and precision discrepancies, ranks, domain margins, and all validity predicates. A cancellation ratio may be reported descriptively with an explicit undefined value when its denominator is zero.

## Controls and adjudication to freeze before execution

Include identity-middle null, exact affine-readout null, weight-preserving-block null, direct-composition versus block-construction agreement, connected-differential agreement, covariance, cross-precision agreement, finiteness, and parent-file hashes.

Retain the parent 1e-35 within-precision and 1e-30 cross-precision tolerances where the same absolute matrix norms are compared. Any new residual normalization must be defined explicitly before measurements. Test corrupted provenance, omitted connected subtraction and invalid domains using deterministic fixtures.

A verified factorization is an implementation audit result. Valid numerical null source contributions are allowed. Failed provenance, nonfinite arithmetic, mismatched domains or violated identity controls yield INVALID; never reinterpret them as discovery of a residual physical term.

## Execution and publication sequence

1. Finalize exact fields, tolerances and source hashes in PREREGISTRATION.md.
2. Commit preregistration and failing implementation tests before ensemble execution.
3. Implement the independent decomposition and satisfy the control tests.
4. Run the complete frozen ensemble and inspect actual outputs, not only CI success.
5. Publish the final report promptly with complete evidence links; archive all raw results and verify remote hashes.

No 16.04 numerical result should be announced before step 4. The analytic result is already stated independently in DERIVATION.md.
