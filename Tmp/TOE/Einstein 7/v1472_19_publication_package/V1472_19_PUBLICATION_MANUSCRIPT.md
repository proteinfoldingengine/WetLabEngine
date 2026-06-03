# Pruning-Order Recoverability Traces as the Empirical Object for Geometry-Like Closure

## Abstract

Static network topology is an insufficient empirical object for testing recoverability-based geometry-like closure because it preserves architecture while discarding the ordered history of information loss and repair. Prior tests on static software import and function-call graphs failed against directed-degree, configuration, and community-preserving nulls. We reinterpret that failure as an ontological mismatch rather than a simple implementation failure. The valid empirical object is a pruning-order recoverability trace: an ordered ledger of source-origin, disruption/loss, repair/recovery, and closure events, with explicit event dependencies, provenance lineage, and entropy-arrow consistency. We present a causal governor that computes geometry-like closure only on admissible ordered slices. The governor rejects traces with broken prior-event dependencies, provenance drift, reversed entropy arrows, repair-before-disruption order, missing source-origin, or closure-only static structure. A key methodological correction is enforced: geometry-like closure is never computed on inadmissible slices. Controlled traces, multi-provenance traces, and sample incident-log imports validate the harness and null suite, but no independent external trace has yet been scored. Therefore, this paper presents a falsifiable methodology and reproducibility framework, not proof of physical geometry.

## 1. Introduction

The project began with a direct question:

```text
Can geometry-like closure be recovered from empirical structure?
```

Initial attempts used static software graphs. Those attempts failed. Directed-degree and community-preserving nulls could match or exceed the original. This showed that static topology was the wrong empirical object.

The corrected question is:

```text
Can geometry-like closure emerge only from valid pruning-order recoverability traces?
```

This changes the empirical target from architecture to ordered loss-repair history.

## 2. Static Topology Failure

Static graphs encode:

```text
nodes
edges
reachability
degree
community
locality
```

They do not encode:

```text
source appeared first
disruption followed source
repair followed disruption
closure followed recovery
entropy moved in the admissible direction
provenance remained valid across the sequence
```

Because of this, spatial nulls can preserve or improve topology while destroying the recoverability history the theory actually requires.

## 3. Empirical Object: Pruning-Order Recoverability Trace

A valid trace has the form:

```text
source-origin
→ disruption / loss
→ repair / recovery
→ closure
```

Each event must include:

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

The central rule is:

```text
No pruning-order trace, no empirical geometry claim.
```

## 4. Causal Governor

The causal governor processes the trace in pruning order and validates each slice before geometry-like closure is allowed.

At each ordered slice it checks:

```text
unique event_id
unique pruning_order_index
source-origin has appeared
prior_dependency references a prior event_id
provenance lineage is authorized
entropy-arrow direction is valid
```

The prior-dependency rule is strict:

```text
prior_dependency must reference prior event_id only.
provenance_id cannot satisfy prior_dependency.
```

## 5. Admissible-Slice Geometry Gate

The strongest correction learned during peer review was:

```text
Geometry-like closure is never computed on inadmissible slices.
```

This is not equivalent to computing geometry and then multiplying it by zero. The system must refuse to compute the geometry-like quantity at all until the slice is admissible.

A slice is inadmissible if it violates:

```text
source-origin
prior event dependency
provenance lineage
entropy-arrow direction
ordered recovery sequence
```

## 6. Margin

The governing margin is:

```text
M_total = C_closure × P_sequence × E_arrow
```

where:

```text
C_closure = repair/recovery closure × geometry-like slice coherence
P_sequence = pruning-order / prior-event / provenance validity
E_arrow = entropy-arrow consistency
```

If a slice is inadmissible:

```text
geometry_like_closure = not computed
M_total = 0
```

## 7. Required Null Suite

Every candidate trace must be tested against:

```text
event_order_shuffle
provenance_shuffle
repair_before_disruption
source_removed
entropy_arrow_reverse
closure_only_static
```

The empirical claim fails if any of these nulls certify.

## 8. Threshold Preregistration

Positive certification requires a threshold, but thresholds can create claim-risk if selected after seeing the result.

Therefore:

```text
threshold must be declared before scoring
continuous M_total must be reported
threshold sweep must be reported
all nulls must be reported
```

Recommended policy:

```text
small pilot trace: 0.40 if declared before scoring
larger/non-pilot trace: 0.70 recommended
```

## 9. Current Validation Status

Validated:

```text
causal governor on controlled traces
event dependency validation
provenance lineage validation
entropy-arrow validation
admissible-slice geometry gate
multi-provenance transitions
external-style log adapter
threshold-preregistered runner
manifest-gated runner
independent trace intake kit
```

Not validated:

```text
real empirical geometry evidence
independent external trace pass
physical geometry
GR / ADM / physical curvature
```

## 10. Reproducibility Protocol

To test an independent trace:

```bash
python v1472_12_manifest_runner.py your_manifest.json
```

The manifest must declare before scoring:

```text
trace source
threshold
pilot/non-pilot status
event mapping
entropy definition
damaged/repaired proxy
prior dependency definition
provenance definition
claim boundary
```

## 11. Claim Boundaries

This framework may support statements such as:

```text
The V1472 framework tests geometry-like closure on pruning-order recoverability traces.
The testing pipeline is ready for independent traces.
A passing independent trace would be an empirical evidence candidate.
```

It does not support:

```text
proof of physical geometry
proof of spacetime
proof of GR
proof of physical curvature
proof of Einstein equations
proof of ADM closure
static topology as sufficient evidence
controlled sample as independent evidence
```

## 12. Conclusion

The work has moved from a failed static-topology approach to a falsifiable pruning-order recoverability framework. The methodology, null suite, admissible-slice gate, threshold preregistration, and manifest-gated runner are ready. The next required step is a genuinely independent external trace scored under preregistered conditions.

Until that happens:

```text
the framework is ready;
the empirical claim is not closed.
```
