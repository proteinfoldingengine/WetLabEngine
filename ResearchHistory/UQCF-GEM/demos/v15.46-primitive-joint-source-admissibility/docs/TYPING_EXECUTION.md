# Local typing-probe execution receipt

Scope: bounded v15.46 research screen, not full v15.46/CI certification.
Base: 20650af8d9583383925efc570026666b47d12788. Runtime: CPython 3.13.5.

## Local RED/GREEN

`python -m unittest -v test_typing_probe` first produced 8 assertion failures
and 0 errors: `typing_probe is absent`. Only tests existed at that step.
The implementation then passed all 8 tests with no skips (0.730 seconds in
that observed run). A fresh final run is also retained in the portable package.

The checks cover all 84 matrix units for 1/2/3-qubit twirling, exact torus
boundary and invariance ranks at L5/L6/L7/L8, boundary-of-boundary zero,
nonzero addressed covariance/sign controls, the translation-invariant harmonic
cycle outside the boundary target, invalid inputs, output determinism and limits.

These are 8 tests containing many exact assertions, not 8/84 independent discoveries.
No approximation of matrix logarithms is used by this new probe.

## Replays

The existing `exploratory/proof_checks.py` was restored from the earlier
conversation artifact and checked against its documented hash:
`8c024ca23bf0663ee819a72ff00f8607ad3952517162b861b62f73e4bcf9dd7b`.
Its 195-check output replayed exactly, SHA256:
`f686af1a062a92ff64c0de115ae522da17272bf4ec1c182c367e6ea8d3d9fe11`.
No earlier source was changed.

New source SHA256:
- `typing_probe.py`: `cd9af39bfdc17b076f7907c3ad94c627a6b334ff5b0f40a13e9b5a973a777c67`
- `test_typing_probe.py`: `8bded4c341efbb892d5c553b65ca537857fb777de4338e3a78d08cc4684b7fa3`
- `TYPING_PROBE_RESULTS.json`: `1204e72298c01bef99c4b8aff24939abbac189d2098b65189ba64a04939a196b`

The new JSON was generated twice and compared byte-for-byte. Compilation passed.

## Limits and rulings

1. Source-record review and mathematical probes are separate. The inventory is
   authored interpretation with exact source pins, not a computed absence proof.
2. No physical source law or subsystem-to-face dictionary is adopted.
3. The trace-only lemma assumes a linear map of D alone to a quantum-frame-trivial
   target. State-conditioned or observable-conditioned maps fall outside it.
4. The address lemma assumes independent cell translations acting trivially on
   the input and target im(B2). It does not exclude addressed inputs or the
   full cycle target. Both escapes are explicit controls.
5. The probe is a separate square-torus mathematical fixture, not another
   execution of v15.45's complete archived presentation suite.
6. Git clone was unavailable due to DNS resolution in this container. Repository
   files were inspected through the authorized GitHub connector. No local full
   repository checkout, complete regression, independent reviewer or CI result
   is claimed.
7. All changes are additive on PR #57. No workflow, new Actions job, predecessor
   branch edit, merge, or source-correspondence experiment is part of this step.
