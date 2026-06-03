# V1472.4 Work Order — Multi-Provenance Transitions

## Goal
Allow valid provenance transitions without weakening lineage validation.

## Problem
V1472.3 uses simple single-root provenance continuity.

## Add
- explicit provenance_transition records
- allowed transition: P0 -> P1 only if transition event exists
- multi-source traces
- branch merge traces
- invalid provenance transition nulls

## Preserve
prior_dependency must still reference prior event_id, not provenance label.

## Pass
Valid transition traces pass.
Provenance-shuffled traces fail.
Unauthorized provenance transitions fail.
