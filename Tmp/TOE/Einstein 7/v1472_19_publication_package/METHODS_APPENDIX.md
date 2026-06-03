# Methods Appendix

## A. Event Schema

Required canonical fields:

```text
event_id
pruning_order_index
event_type
provenance_id
prior_dependency
entropy_before
entropy_after
damaged_dependencies
repaired_dependencies
affected_node
repair_target
```

## B. Event Types

```text
source
disruption
loss
repair
recovery
closure
```

Optional advanced event types:

```text
provenance_transition
branch
merge
```

## C. Causal Governor

Pseudo-code:

```python
for event in sorted(trace, key=pruning_order_index):
    validate_unique_event_id(event)
    validate_unique_order_index(event)
    validate_source_origin(event)
    validate_prior_dependency_is_prior_event_id(event)
    validate_provenance_lineage(event)
    validate_entropy_arrow(event)

    if slice_is_admissible:
        compute_geometry_like_closure()
    else:
        do_not_compute_geometry()
        M_total = 0
```

## D. Nulls

```text
event_order_shuffle
provenance_shuffle
repair_before_disruption
source_removed
entropy_arrow_reverse
closure_only_static
```

## E. Certification

A trace certifies only if:

```text
real trace passes preregistered threshold
all nulls fail
geometry_computed_on_inadmissible_slice = false
```

## F. Peer Review Checks

```text
prior_dependency only matches event_id
provenance_id cannot satisfy dependency
geometry is not computed on inadmissible slices
threshold declared before score
all nulls run
claim boundary preserved
```
