# v16.22 review record

Review status: **self-reviewed**, not a separate person/agent review. The producer/verifier have different enumeration and solution algorithms; algorithmic independence is not independent authorship or formal theorem verification.

## Mathematical challenges

- Is an inherited object removed to force a no-go? No: T^G and its defining l T=id remain fixed. C is explicitly a logical subset of C+INV. The conclusion is nonuniqueness of the subset, while C+INV retains uniqueness. Neither is labeled universal closure of the physical foundation.
- Are actual retained maps omitted? No: both source P/I and potential R/H are used. The necessity proof needs BOTH comparison equations. All root/parent-preserving retained embeddings and automorphisms are included.
- Is the result a diagonal ansatz? No: primary unknowns are arbitrary (n-1)^2 root-coordinate entries per tree. The proof derives diagonality; the independent solver starts with all edge-coordinate entries before identifying zero/equality classes.
- Is a coordinate isomorphism inferred from dimension? No: subtree summation explicitly inverts b and ancestral path integration explicitly inverts d. Source and response types remain distinct.
- Are different depths related by an existing arrow? Actual retained prefix inclusions and rooted isomorphisms preserve a retained edge's depth. No re-rooting or ancestor suppression is silently admitted or excluded from the declared parent inventory.
- Does nonuniqueness mean no canonical construction? No. The unchanged unweighted inverse remains a canonical specified construction; C simply does not uniquely characterize it. Two mathematical witnesses are not selected physical laws.

## Executed review finding and corrective RED

Initial implementation `db10a265da716d4b16e10e8db42df0c5947f4207`, run 36519534901, passed its 18 tests and the exact finite audit. A subsequent self-review found that Python Boolean/floating values equal to integers could pass the parent-array equality check. Local reproduction confirmed that malformed parent scalars were accepted. The mathematical certificate from the producer contains actual integers and is unaffected, but the verifier's rejection contract was incomplete.

Commit `0111d84990e93c86936f31c8d72dfce25388b6e8`, run 36519735366, added two new controls. The original 18 tests passed and BOTH new tests failed with `VerificationError not raised`. This is a substantive RED against an implemented verifier, not missing-module wiring.

The correction validates parent-array scalar types BEFORE equality comparisons or cache lookups and adds both corruptions to the machine-readable rejection campaign. Local execution passed 20 tests and independently reverified the original complete certificate. The corrected GitHub GREEN must be recorded separately; no old run is described as testing the new parser.

Only type validation/rejection controls changed. No mathematical premises, candidate family, exact constraint, underlying producer, test universe or acceptance threshold changed. Both original RED and initial GREEN must remain archived alongside regression RED and final GREEN.
