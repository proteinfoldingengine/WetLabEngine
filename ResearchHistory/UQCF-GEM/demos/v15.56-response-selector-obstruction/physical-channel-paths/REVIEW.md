# Independent review

The independent reviewer checked the physical-path construction, exact normalization/positivity/CPTP argument, one-sided rank obstruction, implementation, protocol and tests before measurement. No blocking issues were found. The reviewer ran all five unit tests successfully without running the ensemble or editing files.

The review emphasized that normalization changes connected correlations nonlinearly, so normalized moments/ranks must be rebuilt rather than rescaled. It also clarified that the inherited zero-normal-block label concerns uncertified constant-rank stability, not physical-path existence. Both points are explicit in the implementation and derivation.

## Exact complex LDL implementation correction

The first implemented audit, run 36489262513 at bcbe869c385940a0dcbf029cb58a1c94f9123548, was INVALID before candidate path measurement. SymPy's built-in Hermitian LDL routine rejected candidate 13's positive-definite leading 4x4 block. The saved regression fixture has a strictly positive exact Gershgorin lower bound, independently establishing positivity. The built-in routine leaves complex intermediate products unsimplified before its sign predicate.

A regression test reproduced the rejection. The replacement uses the standard exact Hermitian LDL recurrence, expands every stored intermediate, requires each pivot to be a strictly positive rational, and verifies exact reconstruction. All six tests pass. No state, tolerance or preregistered positivity requirement changed. The original failed result, checksums and logs remain published as failed-* and FAILED_ATTEMPT.json.
