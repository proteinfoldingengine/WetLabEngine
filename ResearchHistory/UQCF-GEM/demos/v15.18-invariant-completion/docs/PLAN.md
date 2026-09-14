# v15.18 — Minimal invariant observable-algebra completion

Base: a01f1ff5f1045bc701a97bfef44eab58cfc5b401. Preserve earlier files.

Continue the existing simulation without adding a physical rule. Determine the
smallest unital *-algebra containing each v15.16 retained algebra and invariant
under each v15.17 finite motion and its inverse; also test all six together.
The six-operation library is a supplied diagnostic family, not a sequence of
realized controller values. No clock or actual record is selected.

The original algebras contain the diagonal matrix units in the already-derived
input basis. Every larger algebra is therefore a partition coarsening. Generate
necessary matrix units from conjugated blocks and close their connectivity until
stable. Include inverse operations. Verify all-input closure independently with
central projector and superoperator tests. Reject ambiguous numerical supports:
zero <=1e-12, nonzero >=1e-9, anything between is unresolved, not tuned away.
This is exact algebraic reasoning with numerical support diagnostics, not a
formal symbolic proof of all floating-point zeros.

Tests first, then minimal implementation; compare with all small four-label
partitions as an independent minimality check. Distinguish a multiplicatively
closed algebra from a possibly smaller sufficient linear operator module. Do not
claim to close the earlier geometry-aware GOSM target. Enlargement specifies what
must have been retained BEFORE pruning; it does not recover an erased state.

Export all 112 cases and a small visual inspector. Produce a reproducible MP4,
rerun all 202 previous tests, verify baseline hashes, and publish an additive
stacked draft PR. No merge, release, live deployment, or new fundamental axiom.
