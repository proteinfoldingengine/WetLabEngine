# v15.31 Source-Extension Minimality — Implementation Plan

**Date:** 2026-09-18  
**Base:** `2d9eb636d9d216ef0c7f9029e32832b7c435f0d8`  
**Design:** `docs/superpowers/specs/2026-09-18-v1531-source-extension-minimality-design.md`

## Execution order

1. Freeze the exact v15.28 representation sources and inventory by Git blob SHA.
2. Write RED tests for inherited dimensions, exact character-space dimension, semisimplicity boundary, early-stop adjudication, deterministic ledger, and gravity firewall.
3. Confirm RED by missing `source_extension_gate`, without modifying inherited theory code.
4. Implement only the exact representation audit:
   - reuse the frozen 7×7 torus automorphism action;
   - recover `C1`, `Q`, and `Z=ker(B1)`;
   - verify the v15.28 target remains the same certified cycle-space target;
   - compute the exact cycle character;
   - compute `dim Hom_G(Z,Y_cyc)` by character inner product;
   - stop immediately if the dimension is greater than one.
5. Record the characteristic-zero finite-group semisimplicity boundary. Do not claim integral splitting.
6. Freeze `docs/RESULTS.json` and require byte-identical regeneration.
7. Run targeted inherited v15.28 and v15.30 regressions plus all v15.31 tests on exact head.
8. Keep the PR draft/unmerged. No new source semantics and no gravity calculation are authorized.

## RED receipt

GitHub Actions run `35394986093` on head
`cb1e328dd4f10fc692f77d962554faa584413b2c`
failed exactly at the intended boundary:

`ModuleNotFoundError: No module named 'source_extension_gate'`.

The environment and checkout completed before the expected missing-implementation failure.

## Computational strategy

Do not solve a 2500-variable exact intertwiner system unless the character dimension is one.

The character inner product gives the exact dimension first:

```text
dim Hom_G(Z,Y) = |G|^-1 sum_g chi_Z(g) chi_Y(g).
```

Because v15.28 defines `Y_cyc` as the cycle-space representation on the same chain complex, `chi_Y = chi_Z`.

If the exact dimension is greater than one, nonuniqueness is already proved and deeper decomposition cannot change the primary gate.

## Scope

This plan is representation mathematics only. It does not propose or test a physical source axiom, coupling strength, gravity law, metric selector, entropy law, pruning law, or physical time.
