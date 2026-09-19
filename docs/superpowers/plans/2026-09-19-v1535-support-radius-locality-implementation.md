# v15.35 Canonical Support-Radius / Locality Filtration — Implementation Plan

**Date:** 2026-09-19
**Base:** `e24b94fb1a0ca4c8eda33379f5a4ab3f4c360487`

## Execution

1. Pin v15.28 representation machinery, v15.34 result, and the v13.15/v13.18 locality evidence.
2. RED tests require the exact ten-orbit basis, exact polynomial reconstruction, support-radius filtration, locality-vs-degree separation, zero frozen hard-radius selection, and claim firewall.
3. Confirm RED by missing `support_radius_locality_gate`.
4. Enumerate D4 displacement orbits on `Z_7^2` and build one exact convolution operator per orbit.
5. Restrict all orbit operators to the 50-D cycle basis and verify rank 10.
6. Reconstruct each orbit kernel exactly in `I,A,...,A^9`.
7. Compute exact support-radius filtration ranks.
8. Audit frozen locality theorems by type; do not turn conditional or approximate locality into a hard radius.
9. Run inherited v15.33/v15.34 regressions and exact-head certification.
10. Freeze deterministic ledger only after GREEN.

## RED receipt

Run `35408173039`, job `105802159476`, head
`9ca8e508b117be880bfda1c0b961f02472f7ca50`
failed exactly with:

`ModuleNotFoundError: No module named 'support_radius_locality_gate'`.
