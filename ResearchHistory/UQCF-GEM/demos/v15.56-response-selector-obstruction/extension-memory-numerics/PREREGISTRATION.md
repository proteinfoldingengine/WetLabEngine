# v15.72 Extension-memory descent numerical adjudication — preregistration

Date: 2026-09-26. Parent: b59ed3bd8a96d0578beb8686a05bc29847290dc8.
Branch: research/v15.72-extension-memory-numerics.

## Purpose

Adjudicate the narrow numerical failure of the v15.71 primary gate without changing its verdict.

v15.71 remains:

    MINIMAL_EXTENSION_MEMORY_DESCENT_NOT_CONFIRMED

because its full-state float64 comparison reached a maximum relative residual 1.756e-9 against a frozen 1e-9 threshold, even though the absolute discrepancy was only 8.78e-17.

The hypothesis tested here is that the failure is caused by adding a ~5e-8 retained source increment to an O(1) density matrix and then subtracting two independently rounded full states.

## Frozen data

Reuse unchanged from v15.71:

- 12 asymmetric states [13,16,22,25,27,29,37,39,46,50,66,77];
- 27 HS-normalized exact-weight-three hidden directions;
- 27 source basis labels;
- both hidden signs;
- three ordered retained edges;
- eta=1e-4;
- source strength=1e-3;
- the same independently reconstructed local retained lift.

No source law, state, strength, memory coordinate, or geometry is changed.

## Method A — reproduce full-state float64 gate

Repeat all 52,488 v15.71 witnesses exactly:

    global = R_e[sigma + strength (s·m) Y]
    regional = R_e sigma + strength (s·m) Y_e.

Record absolute and relative residuals for nonzero source pairings.

The v15.71 failure must reproduce: maximum relative residual >1e-9.

## Method B — increment-space float64 identity

Before adding the small source increment to the state, compare

    Delta_global = R_e[strength (s·m) Y]

with

    Delta_regional = strength (s·m) Y_e.

Run the same 52,488 witness loop.

For the 1,944 nonzero matching-source cases, require maximum relative increment residual <=1e-12.

This is not a new source law. It is the same v15.71 equality evaluated before O(1)+O(1e-8) state addition.

## Method C — 80-digit full-state arithmetic

Use mpmath 1.3.0 at 80 decimal digits with full complex transport.

For every nonzero matching-source case (12 states x 27 hidden directions x 2 signs x 3 edges = 1,944), convert the frozen float64 sigma, Y and local Y_e to 80-digit complex matrices.

Compute

    R_e^mp[sigma + Delta_global]

and

    R_e^mp[sigma] + Delta_regional

using an independent ordered high-precision partial trace.

Require maximum relative residual <=1e-12.

The high-precision path is an arithmetic adjudication only; it does not recompute the polar geometry or alter the frozen local lift.

## Frozen verdicts

EXTENSION_MEMORY_CANCELLATION_CONFIRMED if all validity checks pass and:

1. float64 full-state maximum relative residual >1e-9;
2. float64 direct-increment maximum relative residual <=1e-12;
3. 80-digit full-state maximum relative residual <=1e-12.

EXTENSION_MEMORY_NUMERIC_DISAGREEMENT if valid but any of the three conditions fail.

INVALID for malformed state identity, nonfinite diagnostics, memory/local-lift validity failure, or high-precision arithmetic failure.

The historical v15.71 verdict is never rewritten.

## Interpretation

Confirmation would establish that the v15.71 primary NO was a numerical property of its frozen full-state float64 estimator, while leaving that historical NO intact. It would certify the mathematical sufficiency of the 27-coordinate enriched descent implementation on the frozen ensemble.

It would not select this memory physically or make it fundamental. The next scientific question would be the origin/selection law for the extension memory itself.
