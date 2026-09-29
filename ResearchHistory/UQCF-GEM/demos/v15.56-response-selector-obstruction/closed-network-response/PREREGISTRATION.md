# 16.14 — Closed-network signed response (frozen before measurement)

Parent publication: 18d49baad706b44abd57b1e2e1289c92b9bb2614. Frozen 12 candidates, three archived middle-channel coefficients, two preparation arms, two orders: 144 paths, 72 order pairs. Inputs are the exactly normalized physical states and CPTP source family of 16.11–16.13. No new states, alignment, spectral truncation or readout selection.

## Observable and decomposition
Use all six oriented baseline connected matrices Cij, with Cji=Cij transpose. Fix cycles (012),(013),(023),(123),(0123),(0132),(0213): all four triangles and three unoriented quadrilaterals. For each cycle measure trace of its edge product and its first derivative in the source strength s. The channel path is polynomial C+s(V0+lambda V1)+s²W(lambda). Derivatives are affine in lambda on [-1,1]; store both exact coefficients, so zero, reversal and the entire interval are adjudicated without sampling inference.

For each path and cycle separate the sixth-edge (23) normal contribution tr(product with lambda N replacing C23), remaining sixth-edge tangent contribution, and all other edges. Store every contribution and the total, and after-minus-before order contrasts. A nonzero total cannot certify a normal signal by itself. A zero total does not prove all network invariants blind.

Counts: 144 six-edge path records, 1008 path-cycle records, 504 pair-cycle contrasts. Numerical checks: 144 paths × 7 cycles × 3 coherence values (-1,0,1) × 2 precisions (80,120 digits) × 2 independent-frame choices = 12096 rows. Numeric values are exact derivative evaluations, not finite differences.

## Gates and controls
Exact source/state parent binding; reconstructed sixth-edge coefficients and N agree with 16.12; identity middle has equal complete derivatives; normal is exactly lambda N and zero at lambda=0; exact derivative decomposition and cycle reversal; SO(3) endpoint invariance including moving-frame connection terms; all data and scalar values finite. Numerical residual <=1e-35, cross-precision <=1e-30; exact rational zero decides response, never a tolerance. Synthetic cancellation and nonzero normal-reference examples validate both outcomes.

Archive a projected intrinsic reference for every cycle: the gradient G23 of the trace with respect to C23, and H=(I-P)G23(I-Q). Normal response is Frobenius inner product H:N. Bound |H:N|<=||H||F||N||F. No normalization by a small spectral quantity. The 16.13 rank-two determinant witness remains separately qualified; this test uses matrix products only, with no inverse or polar factor.

Verdicts: INVALID on failed gates; CLOSED_NETWORK_NORMAL_RESPONSE if any nonidentity pair has nonzero normal coefficient; NETWORK_RESPONSE_WITHOUT_NORMAL if totals respond but all normal contrasts vanish; CLOSED_NETWORK_FIRST_ORDER_NULL if every chosen total contrast vanishes. Report counts, zeros, cancellations and actual magnitudes for all arms/cycles. This is a bounded first-order probe, not gravity, curvature, transport, source emergence, or a statement about every invariant.

Time is pruning / ordered recoverability update; s is a channel strength, not fundamental time.
