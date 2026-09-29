# 16.19 — Full-response information-kernel gate

## Motivation

16.16 proved that, on the frozen two-coefficient order-contrast domain, the chosen local invariant differential map and the closed-network readout have the same rank and the network adds no quotient direction. That result does not classify information discarded when the *full matrix-valued first derivative* is compressed to those local scalars.

## Frozen question

Using only the already-published 16.15/16.12 path data, compare the exact full six-edge matrix first-order derivative with the differential of the frozen local scalar family. Determine the kernel of the local-scalar differential restricted to the actually realized response span.

No metric, area, connection, curvature, embedding, alignment, fitted weights, or geometric target is allowed.

For each frozen baseline class, collect the exact realized first-order response vectors from the archived physical paths. Vectorize all six 3x3 edge derivatives into one exact response vector. Let X be their exact rational span. Let J be the exact differential map of the 24 local scalars (six edges × Gram1, Gram2, Gram3, determinant) evaluated on X.

Report:
- dim X;
- rank J|X;
- dim ker(J|X);
- whether nonzero realized response information is invisible to the frozen local scalar differential;
- decomposition by preparation and inherited middle parameter where the data support it.

This is an information-compression classification only. A nonzero kernel is not geometry.

## Outcomes

- LOCAL_SCALARS_COMPLETE_ON_REALIZED_RESPONSE
- NONTRIVIAL_RESPONSE_INFORMATION_KERNEL
- MIXED_RESPONSE_INFORMATION_KERNEL
- INVALID

## Controls

Bind parent publications by committed SHA256. Reconstruct local scalar derivatives independently from baseline C and derivative V using exact formulas:
d tr((C^T C)^k)[V], k=1,2,3, and d det(C)[V]=cof(C):V.
Do not infer J from the archived local-scalar output itself for the primary calculation. Compare the independently reconstructed values to the archive as a control.

Identity/source-null controls and frame covariance inherited from the parent remain required. Exact rational rank decides the classification; no singular-value threshold.

## Firewall

The output is information only. Do not call a kernel direction metric, connection, area, curvature, gravity, or a physical source law.

Time remains pruning / ordered recoverability update.
