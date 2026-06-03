# V1472 Peer Review Packet

## What reviewers should check

1. Does `prior_dependency` only match prior `event_id`?
2. Are provenance labels prevented from satisfying event dependency?
3. Is geometry-like closure skipped, not merely zeroed, on inadmissible slices?
4. Are thresholds declared before scoring?
5. Are all nulls run?
6. Is the trace genuinely independent?
7. Are entropy and damaged/repaired proxies externally defined?
8. Are claim boundaries preserved?

## Minimal falsifier

If any of these pass, the empirical claim fails:

```text
event_order_shuffle
provenance_shuffle
repair_before_disruption
source_removed
entropy_arrow_reverse
closure_only_static
```

## Most important audit line

```text
geometry_computed_on_inadmissible_slice must be false
```
