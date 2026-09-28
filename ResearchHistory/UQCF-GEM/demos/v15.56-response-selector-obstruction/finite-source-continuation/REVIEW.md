Implementation review before measurement

Preregistration head: 150d9fe908d9480d54e0ec820ed2e1c9aa036473. Expected RED run 36449687457, job 109020926196, was inspected: five absent-implementation assertion failures, measurement skipped.

An independent reviewer checked the differentiated polar equations and connected finite-center construction. A generic analytical check found Hessian finite-difference error 2.97e-23 and mixed symmetry error 1.67e-52 at 50 digits. Review identified classification agreement, domain-error handling and precision-domain mismatch defects before any ensemble measurement. These were corrected, with two regression tests added. All seven tests passed locally and in the reviewer's independent execution. The source/preparation residuals and explicitly checked mixture weights are archived in the output.

The test suite permits scientific numerical-null, unresolved and finite-domain-negative outcomes. Review is not measurement evidence. Local runtime used Python 3.12; the scientific workflow pins Python 3.11. Historical files are unchanged. The parent 80-digit J extraction is lossless and hash-pinned; the full source JSON hash and original artifact are documented in PREREGISTRATION.md.
