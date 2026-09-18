# v15.32 Commutant / Canonical Sector Decomposition — Implementation Plan

**Date:** 2026-09-18  
**Base:** `d2b767c88a4bdb3d750d7bb696b29b4fbd34dca1`

## Goal

Resolve the internal structure of the v15.31 ten-dimensional commutant without adding source semantics or consulting gravity.

## Execution

1. Pin the exact v15.28 representation machinery and v15.31 result.
2. RED tests require:
   - rational macro-sector dimensions 2/12/12/24;
   - exact Hom matrix diagonal 1/3/3/3 with zero cross terms;
   - nine nonzero D4 momentum orbits;
   - three axis, three diagonal, three generic orbit families;
   - one F7* Galois group per rational boundary macro-sector;
   - multiplicity-free splitting-field decomposition with ten sectors.
3. Confirm RED on absent `sector_decomposition_gate`.
4. Implement exact rational face projectors and all-G commutation checks.
5. Verify boundary injectivity and translation-fixed homology.
6. Compute exact sector characters and Hom dimensions.
7. Independently enumerate D4/F7* character-lattice orbits.
8. Adjudicate mixing versus scalar-weight freedom.
9. Freeze a deterministic result ledger only after GREEN telemetry is confirmed.
10. Run exact-head regression/certification with gravity firewall intact.

## RED receipt

Run `35395895077`, job `105764517915`, head
`c02aee671b37be27ed068ad62b9b3965bca797c9` failed exactly at:

`ModuleNotFoundError: No module named 'sector_decomposition_gate'`.

## Scientific firewall

No physical sector is selected. No new source axiom, coupling solve, holonomy/Newton/GR criterion, metric/Hodge selector, entropy, pruning, or physical time is used.
