# v16.28 test-fixture correction

Run 36628829369 at 1cee24db0d120e685f8849e4ed5823281e63e6d5 failed before full production: 27 of 28 tests passed; the purported positive relabeling fixture raised ValueError('changed union'). The validator was correct. The original fixture on (-1,2,0) removed node 1 from the only view containing it, so its final union was {0,2}, not {0,1,2}.

The positive control now retains a second full view before and after deleting node 1 from the first. This changes only the invalid positive fixture. The same-union requirement, malformed-input rejection tests, proofs, candidate theorem, primary universe, producer and verifier are unchanged.

This is a documented invalid test input, not a scientific counterexample and not an implementation bug disguised as expected RED. The original failed run and its artifact 11062290464 are preserved in the publication record.
