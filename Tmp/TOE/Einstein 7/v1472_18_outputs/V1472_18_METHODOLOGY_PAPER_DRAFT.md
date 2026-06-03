# V1472.18 — Methodology Paper Draft

## Title

From Static Topology to Pruning-Order Recoverability Traces: A Causal Governor for Testing Geometry-Like Closure Under Entropy-Arrow Constraints

## Abstract

Prior empirical attempts to extract geometry-like closure from static software graphs failed under degree-, direction-, and community-preserving nulls. This failure revealed an ontological mismatch: static graphs preserve architecture, not recoverability history. We therefore reset the empirical object from static topology to a pruning-order recoverability trace: an ordered ledger of source-origin, disruption/loss, repair/recovery, and closure events with explicit provenance, prior event dependency, and entropy-arrow information. We introduce a causal governor that computes geometry-like closure only on admissible ordered slices. The governor enforces that prior dependencies reference prior event IDs only, provenance labels cannot satisfy dependencies, entropy-arrow direction must be preserved, and geometry-like closure is never computed on inadmissible slices. Controlled traces, multi-provenance traces, and sample incident-log imports validate the harness architecture and falsification nulls. However, no genuinely independent external trace has yet been scored. Therefore, the present result is a methodology and testing framework, not empirical proof of real geometry.

## 1. Motivation

The original empirical question was:

```text
Can geometry-like closure be extracted from structure?
```

The corrected question is:

```text
Can geometry-like closure emerge only from valid pruning-order recoverability traces?
```

The first question failed because static topology can look geometric while lacking the ordered loss-repair history required by the framework.

## 2. Failed Static-Topology Route

Tested empirical objects included:

```text
Python import/dependency graph
function-call graph
static topology-derived paths
```

Failure mode:

```text
directed degree/configuration/community nulls matched or exceeded original scores
```

Interpretation:

```text
Static topology preserves architecture, not pruning/recovery history.
```

## 3. Correct Empirical Object

The valid empirical object is:

```text
pruning-order recoverability trace
```

Minimum event sequence:

```text
source-origin
→ disruption / loss
→ repair / recovery
→ closure
```

Required event fields:

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

## 4. Core Axiom

```text
No pruning-order trace, no empirical geometry claim.
```

## 5. Causal Governor

The governor processes events in pruning order.

At every ordered slice it validates:

```text
source has appeared
prior_dependency references prior event_id
provenance lineage is authorized
entropy-arrow direction is valid
event IDs and order indices are non-duplicated
```

Critically:

```text
provenance_id cannot satisfy prior_dependency
```

## 6. Margin

```text
M_total = C_closure × P_sequence × E_arrow
```

Where:

```text
C_closure = repair/recovery closure × geometry-like slice coherence
P_sequence = pruning-order / prior-event / provenance validity
E_arrow = entropy-arrow consistency
```

## 7. Hard Peer-Review Correction

The strongest methodological correction was:

```text
Geometry-like closure is never computed on inadmissible slices.
```

This is not the same as computing geometry and setting it to zero afterward.

If the slice is inadmissible:

```text
geometry_like_closure = not computed
M_total = 0
```

## 8. Required Nulls

Every candidate trace must be tested against:

```text
event_order_shuffle
provenance_shuffle
repair_before_disruption
source_removed
entropy_arrow_reverse
closure_only_static
```

A candidate fails if any null certifies.

## 9. Threshold Preregistration

Thresholds must be declared before scoring.

Policy:

```text
small-trace pilot threshold: 0.40 allowed if declared
larger/non-pilot threshold: 0.70 recommended
continuous M_total must always be reported
threshold sweep must always be reported
threshold cannot be altered after seeing the score
```

## 10. Current Results

Validated on controlled/sample traces:

```text
causal governor
event dependency validation
provenance lineage validation
entropy-arrow validation
admissible-slice geometry gate
multi-provenance transitions
external-style log adapter
threshold-preregistered runner
manifest-gated runner
independent trace intake
```

Not yet validated:

```text
independent external trace pass
real empirical geometry evidence
physical geometry
GR / ADM / physical curvature
```

## 11. Evidence Lock

Evidence scoring is locked until both are provided:

```text
1. independent CSV/JSON/JSONL trace
2. completed preregistration manifest
```

## 12. Claim Boundaries

Allowed:

```text
The V1472 framework tests geometry-like closure on pruning-order recoverability traces.
The testing pipeline is ready for independent traces.
A passing independent trace would be an empirical evidence candidate.
```

Not allowed:

```text
This proves real physical geometry.
This proves spacetime.
This proves GR.
This proves physical curvature.
This proves Einstein equations.
This proves ADM closure.
Static topology is sufficient.
The controlled sample is independent evidence.
```

## 13. Next Work

The next scientific step is:

```text
Run a genuinely independent external pruning-order recoverability trace with a preregistered manifest.
```
