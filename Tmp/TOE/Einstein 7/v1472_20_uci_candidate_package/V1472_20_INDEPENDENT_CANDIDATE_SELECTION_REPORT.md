# V1472.20 — Independent Empirical Candidate Selection

## Decision

```text
uci_incident_management_event_log_selected_as_first_external_candidate
```

## Reason

The UCI Incident Management Process Enriched Event Log is the best first candidate because it is:

```text
independent
public
sequential
incident-management focused
large enough for many traces
licensed for reuse with attribution
contains incident state and closure fields
contains update count and ordering fields
contains priority/impact/urgency proxies for disorder
contains reassignment/reopen counts as loss/complexity proxies
```

## Caveat

The dataset does not directly provide our entropy and damaged/repaired fields. Those must be preregistered as proxies before scoring.

## Proposed Proxy

Entropy/disorder proxy:

```text
priority + impact + urgency + active status + reassignment_count + reopen_count + SLA failure
```

Damage proxy:

```text
increase in disorder, reassignment_count, reopen_count, unresolved active state
```

Repair proxy:

```text
decrease in disorder, transition toward resolved/closed state, resolved_at/closed_at present
```

## Evidence Boundary

Running this dataset would be the first real empirical evidence attempt.

It would not prove physical geometry.

It would test whether an independent incident-management recovery trace produces geometry-like closure only when pruning order, provenance, prior dependency, and entropy arrow are preserved.
