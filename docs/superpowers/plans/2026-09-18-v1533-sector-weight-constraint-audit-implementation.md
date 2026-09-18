# v15.33 Sector-Weight Constraint Audit — Implementation Plan

**Date:** 2026-09-18
**Base:** `ff4707b3a09bc7cd091e89986c8cc3dcaf758798`

## Execution

1. Pin v15.32 plus the frozen composition/refinement/recoverability/source-scale evidence.
2. Write RED tests for sector count, frozen constraint rank, surviving projective dimension, controls, adjudication and firewall.
3. Confirm RED by missing `sector_weight_constraint_gate`.
4. Implement the ten-coordinate multiplicity-free weight algebra exactly over `Fraction`.
5. Separate automatic family-closure laws from type-blocked laws and projective gauge.
6. Run stronger-selector controls without promoting them to ontology.
7. Run v15.31/v15.32 inherited regressions and v15.33 tests.
8. Freeze a result ledger only after GREEN.

## RED receipt

Run `35405750220`, job `105795052412`, head `4f6ad94b0c05b32f7be54e3053c0ce2d7dd092ba` failed exactly with

`ModuleNotFoundError: No module named 'sector_weight_constraint_gate'`.

## Boundary

No new source semantics, no sector selector, no coupling solve and no gravity observable are introduced.
