# Protein P8B — Core contract certification

**Status:** GREEN certified before prospective protein measurement.

## TDD evidence

- RED head: `3346b4c798dabbad542bdee8fccd69b00c8f58a5`
- RED workflow run: `35358043104`
- RED job: `105642143315`
- RED shape: environment/install succeeded; contract failed only because `p8b_core` did not yet exist.

- GREEN implementation head: `aeafd110e0080e6f219d3142ed0fd7b8ac180899`
- GREEN workflow run: `35358555343`
- GREEN job: `105643830369`
- Result: 8/8 contract tests passed.

## Certified boundaries

The GREEN implementation establishes only the premeasurement mechanics:

- exact vendored P6 canonical peptide core, Git blob `e517164834636ffc5e52ea118f9d43624edebdad`;
- frozen Patch-622/623 coefficients;
- recovered pseudo-dihedral and Betti-proxy semantics;
- append-before-DAG history ordering;
- Compaction through step 98 and first idealized LockIn transition at step 99 under continuously qualifying Betti history;
- correct three timing-control semantics;
- exact canonical covalent reconstruction;
- native-information objective/gradient firewall.

No P8B native structural outcome had been computed when this certification was recorded.
