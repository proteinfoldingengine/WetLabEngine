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

The first commit deliberately contains this plan, the tests, and the workflow
but no producer/checker modules.  Its verification job must fail specifically
because `producer` is absent.  That run is the required RED observation; the
implementation is added only after the actual Actions log confirms that cause.

No result in this campaign is CLOSED until the bounded run, rejecting controls,
adversarial mathematical review, separate publication audit, evidence
publication, and immutable readback all succeed.
