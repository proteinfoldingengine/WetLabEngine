# v16.23 review and evidence corrections

Review status: self-reviewed. An algorithmically independent verifier is not an independent person/agent review. Written arguments O1-O7 are not proof-assistant formalizations.

## Substantive verification defect and correction

The initial GREEN at 939293191fd5bdd13a086b1d86ac15af595a1b6d (run 36569139253) checked the equations, coverage and reported variants, but the verifier only compared rooted shape and aggregate counts between variants. A copied original certificate labeled relabeled could pass without carrying out the declared coordinate change.

New tests at 54a3a1c57be3d749e86c88969b1556452235d513 (run 36569553274) exposed this: the original 22 tests passed, two new guards failed because ValueError was not raised, and the true metamorphic positive control passed. This is a real test-strengthening RED, not a missing-module failure.

The correction reconstructs the canonical original parent array from the rooted shape code (or the pinned historical fixture), computes the exact declared nonroot-identity reversal, and checks both the actual parent array and actual retained-array storage order. Direct checker fixtures with separate tags remain separate from campaign coverage. No producer, mathematical input, proof, source law, or scientific acceptance criterion was changed. The original GREEN is not retroactively described as testing these guards.

## Mathematical challenges considered

- Union/intersection occur inside an actual common carrier, not a claimed common refinement across unrelated Genesis identities.
- Signed inclusion-exclusion is not silently used as an operation internal to arbitrary positive source monoids. The cone feasibility condition is tested independently against global positive enumeration.
- Response constants are gauge; source constants are not. The negative source witness cannot be repaired by adding a background and calling it the same source.
- Gluing is unique only on the union, and only on compatible data. Fine information outside the union can remain lost. The verifier accepts arbitrary off-domain linear extensions that agree on the equalizer.
- All four certified parent comparison basis vectors, not selected depth examples, must satisfy new overlap diagrams. The general naturality argument keeps comparison freedom and the fixed inverse definition distinct.
- Finite enumeration is implementation evidence, not the proof of universal gluing. Proofs provide the finite-cover and rational-cone statements; bounded integer examples do not establish physical source attainability.

The campaign has no separate reviewer and makes no quantum contextuality, geometric, gravitational, or new physical memory claim.
