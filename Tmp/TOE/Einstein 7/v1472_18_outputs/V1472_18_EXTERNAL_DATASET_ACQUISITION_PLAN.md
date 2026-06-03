# V1472.18 — External Dataset Acquisition Plan

## Goal

Acquire one genuinely independent pruning-order recoverability trace.

## Best First Dataset Classes

### 1. Incident recovery log

Best because it naturally contains:

```text
incident opened
failure detected
loss/degradation
mitigation
recovery verification
incident closure
```

### 2. Database transaction rollback/retry log

Best because it naturally contains:

```text
transaction source
failure
rollback
retry
commit
closure
```

### 3. CI/CD deployment failure rollback log

Best because it naturally contains:

```text
deployment source
failure
rollback/fix
verification
closure
```

### 4. Packet-routing failure/recovery trace

Useful if it has ordered routing disruption/recovery events.

### 5. Protein folding trajectory event ledger

Scientifically interesting, but harder because event semantics and entropy proxies must be defined carefully.

## Minimum Viable Independent Trace

```text
6–20 ordered events
one source-origin event
one disruption/loss event
one repair/recovery event
one closure event
prior dependencies as event_id
one provenance lineage
entropy_before and entropy_after
damaged/repaired counts or defensible proxies
affected component/node
```

## Required Manifest Decisions Before Scoring

```text
threshold
pilot/non-pilot status
event mapping
entropy definition
damaged/repaired proxy
prior dependency definition
provenance definition
exclusion rules
claim boundary
```

## Data Request Template

Please provide a CSV/JSON/JSONL trace with columns similar to:

```text
log_id,seq,kind,component,ticket,depends_on,entropy_before,entropy_after,damaged,repaired
```

Where:

```text
log_id = unique event id
seq = pruning order index
kind = raw event type
component = affected node/component
ticket = provenance lineage id
depends_on = prior log_id
entropy_before/after = externally defined disorder/risk
damaged/repaired = external damage/recovery counts or proxies
```

## Do Not Use

```text
static graphs
generated samples
manually invented traces
traces with no prior dependencies
traces with no entropy measure
traces with no recovery/closure
```
