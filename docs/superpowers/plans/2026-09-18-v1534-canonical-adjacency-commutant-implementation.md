# v15.34 Canonical Adjacency / Commutant Generator — Implementation Plan

**Date:** 2026-09-18
**Base:** `04ad5d3cf24b7f051d714d61d2fe6d8da4fd8eec`

## Execution

1. Pin v15.28 exact representation code plus v15.32/v15.33 result ledgers.
2. RED tests require canonical adjacency preservation/covariance, the preregistered degree-10 polynomial, power-span rank 10, and the full-commutant verdict.
3. Confirm RED by absent `canonical_adjacency_gate`.
4. Build `A` from the exact four primitive translations on the 50-D cycle basis.
5. Verify D4 invariance of the translation set and cycle preservation.
6. Verify the exact polynomial annihilator, cubic irreducibility, pairwise coprimality, and proper-factor omission controls.
7. Verify exact rank 10 of `I,A,...,A^9`.
8. Compare with independently certified v15.32 commutant dimension 10.
9. Freeze deterministic result only after GREEN.
10. Keep all source/gravity selectors firewalled.

## RED receipt

Run `35407686609`, job `105800731899`, head
`66b702545ffb00d3741083026988122255873fd7`
failed exactly with:

`ModuleNotFoundError: No module named 'canonical_adjacency_gate'`.
