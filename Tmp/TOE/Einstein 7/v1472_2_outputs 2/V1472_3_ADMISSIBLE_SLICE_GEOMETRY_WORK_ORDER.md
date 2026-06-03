# V1472.3 Work Order — Geometry-Like Closure on Admissible Ordered Slices

## Goal
Add a real dynamic closure metric evaluated only on admissible pruning-order slices.

## Required

- maintain active dependency/recovery graph over ordered events
- compute closure only when P_sequence > 0 and E_arrow > 0
- compute C_closure from repaired/damaged dependency fraction plus slice coherence
- run nulls that preserve final closure but break pruning ledger

## Pass

- valid ordered trace produces high M_total
- closure-only static null fails
- order/provenance/entropy nulls collapse
- geometry-like closure is never computed on inadmissible slices
