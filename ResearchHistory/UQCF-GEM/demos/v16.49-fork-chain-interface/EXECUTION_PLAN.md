# Fork-of-chains interface implementation plan

> Use superpowers:executing-plans for inline implementation with independent review.

Goal: validate or falsify binary-parent interface composition through the full authorized closure chain.
Architecture: reuse frozen v16.48 chain normalizer, implement a binary-parent wrapper, independently reconstruct canonical branch identities and inspect raw paths. Reuse complete graph and provenance infrastructure.
Spec: PREREGISTRATION.md. Tech stack: pinned Python3.11/Sympy1.13.3/mpmath1.3.0, GitHub Actions only for science/tests.

Review focus: preserved overlap anchor; disjoint child palettes; primitive whole-subtree cloning; opposite-child pivot restoration; total L1 across both branches and parent; exhaustive versus directed identity coverage.

- [ ] Commit prospective protocol from exact verified parent.
- [ ] Record GitHub RED for missing fork interface and missing corpus case, preserving raw artifact.
- [ ] Implement producer.normalize(state,left,right,k,q), complete two-graph production and192 directed paths. Freeze chain_normalize.py from v16.48 without modifying inherited sources.
- [ ] Implement independent verifier structure, width/canonical recurrence, exact graph/corpus coverage and whole-path admission/L1 checks; add substantive mutation and interface controls.
- [ ] Independently review THEOREM.md and source. Execute all845 inherited checks plus new controls, fresh parent48 science and independent fresh reproduction; require33 exact scientific files.
- [ ] Audit execution and publication artifacts/Git bindings, ready/merge exact reviewed head, audit actual-merge full replay and durable receipt, obtain final independent approval and update PR status.
