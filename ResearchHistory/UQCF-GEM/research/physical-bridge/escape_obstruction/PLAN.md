# Perfect-matching escape obstruction verification plan

This directory implements the prospectively frozen scope in
`COUPLED_C3_ESCAPE_OBSTRUCTION_SCOPE.md` without enlarging its claim.

The bounded universe is exactly:

- `H = K6 - {45}`;
- every perfect matching of `H` (12);
- every positive multiplicity profile in `{1,2}^6` (64);
- 768 source instances;
- every cover of size at most four and every `B(v)`;
- every ordered `V` and `X` candidate, including rejected candidates;
- every independent set and its matching-neighborhood cardinality;
- every admitted `X` route for every source-label choice, every route slice,
  every floor, hitting, domination, and protected one-hidden-mask check.

The producer and checker must be independent implementations and must agree on
the byte-level SHA-256 digest of the complete canonical JSONL stream.  Negative
controls must reject a forbidden `45` edge, incomplete matching, false `X`,
missing third vertex, minimum-degree substitution, false deficiency, saturated
bridge substitution, stream truncation, extra rows, and canonical corruption.

## Tests-first record

The first commit `7aaccd8b83f9a001e2d8f138fa2dbb4397ffc28d` deliberately contains this plan, the tests, and the workflow
but no producer/checker modules.  Its verification job must fail specifically
because `producer` is absent.  That run is the required RED observation; the
implementation is added only after the actual Actions log confirms that cause.

Observed RED: Actions run `38167334252`, job `114552511434`, failed in the exact
bounded test step with `ModuleNotFoundError: No module named 'independent'`;
all producer, checker, inherited-test, and review steps were skipped.  This
failure is preserved and was inspected before either implementation was added.

No result in this campaign is CLOSED until the bounded run, rejecting controls,
adversarial mathematical review, separate publication audit, evidence
publication, and immutable readback all succeed.
