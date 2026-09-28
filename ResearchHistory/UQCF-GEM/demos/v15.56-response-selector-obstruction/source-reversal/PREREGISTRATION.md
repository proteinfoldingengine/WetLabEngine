# 16.10 — Source-coherence reversal

Frozen before ensemble measurement. Parent: complete 16.09 publication `232da98ab29ac93d3c3b190e21f3cfa715984aec`, scientific head `b8bfa7cd3abf99884b6627ab2a42d0fa035154be`.

Question: is the common boundary polar limit intrinsic to the shared baseline, or can the sign of coherence in the already-defined two-component source change it?

Use U±=(ZI±XX)/sqrt(2) on sites (2,3), L±=Ad(U±)−I, and E±,s=I+sL±, 0≤s≤1. Each is a convex mixture of identity and a unitary channel. This reverses coherence, not source strength or the baseline. Explicitly verify the exact 16-column Pauli transfer maps against direct conjugation. Use all 12 archived inputs with the explicit physical normalization of 16.08, all three inherited binary a values, two preparation arms and both orders: 144 paired paths, no exclusions.

Reconstruct C,V±,W± from the channel paths. Check the plus path against every exact parent record. Compute N± with exact support projectors. Test the hypothesis N−=−N+ in each case, but a failure is a valid negative scientific result. Verify each path's eventual rank equals r+rank(N) using the 16.09 certificate before assigning B±=polar(C)+polar(N±). A missing certificate is LIMIT_NOT_CERTIFIED, never silently replaced by a chosen completion.

At 80 and 120 decimal digits in both inherited frames, record both limits and their gap; independently check partial-isometry identities, positivity/reconstruction, frame covariance and cross-precision residuals. Exact reversal with k>0 predicts squared Frobenius gap 4k. Use tolerance 1e-35 on controls, 1e-30 for cross-precision, as inherited. Preserve orientation; no SO correction. A non-reversal result is recorded without asserting source equality or inequality solely from that fact.

At 120 digits sample both source paths at s=2^-32,2^-128,2^-192, both frames. Use exact finite polynomial rank, no singular-value threshold. Record convergence errors descriptively, with no fit or convergence gate. Expected 144 exact records, 576 paired numerical rows, 1728 finite polar rows.

Verdicts: SOURCE_DEPENDENT_BOUNDARY_LIMIT_CERTIFIED only if all certificates hold and all nonzero normal blocks reverse exactly; LIMIT_NOT_CERTIFIED if any path lacks rank saturation; REVERSAL_NOT_UNIVERSAL otherwise. INVALID is reserved for provenance, physicality, completeness or numerical-control failure. Source dependence establishes nonexistence of a continuous baseline-only extension along these paths; it is not a universal source law or gravity claim. The mixture strength is not fundamental time.
