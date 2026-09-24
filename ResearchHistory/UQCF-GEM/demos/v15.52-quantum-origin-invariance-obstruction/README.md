# v15.52 — quantum-origin invariance obstruction investigation

**Current status: general recovery theorem proved; submitted quantum witness rejected. Quantum-origin certification is NOT established.**

The archived Task-3 producer reports `WITNESS_FOUND`, and its 17 original tests pass, but it constructs differently named records rather than independently validated quantum realizations. Do not treat that legacy status as a theorem certificate.

The additive Task-4 audit identifies the missing semantic premises and executable integrity failures without altering the original source, tests, frozen equivalence or predecessor outcomes.

## Evidence

- [Theorem, proof, audit findings and claim boundaries](docs/TASK4_THEOREM_AUDIT.md)
- [Exact-head execution receipt: 231 passed tests](docs/TASK4_CI_RECEIPT.md)
- [Canonical independent audit output](docs/VERIFICATION.json)

The general theorem is: a target can be recovered exactly from observations if and only if it is constant on each observation fiber. A valid pair with equal observations and distinct target classes would obstruct uniformly correct recovery. Arbitrarily choosing a label is still possible and is not a derivation.

The quantum-specific implication remains uninstantiated: no lawful realization family, quantum-to-source reduction and semantic non-equivalence certificate were registered. The independent verifier deliberately cannot promote unvalidated candidate records to a positive certificate.

## Reproduce from a complete repository checkout

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.52-quantum-origin-invariance-obstruction
python -m unittest discover -v
python verify_obstruction.py --output /tmp/v1552-audit.json
cmp docs/VERIFICATION.json /tmp/v1552-audit.json
```

The branch-scoped GitHub workflow also runs the discovered v15.46--v15.51 suites, repeats the audit, verifies exact checkout and original source bytes, and checks tracked-tree immutability. Passing tests means the audit executed as specified; it does not establish the rejected quantum premise.

## Next scientific dependency

Before another quantum-origin certification attempt, explicitly define the admissible realization family, its lawful reduction to the retained source, and the earned semantic equivalence. Then construct and independently validate an actual inequivalent pair, or establish why such a pair is absent in that specified family. Any new diagnostic assumptions must be distinguished from first-principles derivation. Do not repair the claim with invented labels, a post-result gauge, or downstream geometry.

Task 5 remains pending those prerequisites. `source_correspondence=NOT_EVALUATED`; **Pillar 3 remains OPEN**. No gravity, Einstein-equation or continuum result is claimed.
