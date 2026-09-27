# v15.73 — Two-body unitary hidden-information transfer

Parent: 846cc623b6c4f26f8e85e0cbd64d2eb0ba9ed040.
Branch: research/v15.73-two-body-unitary-source.
Implementation is absent at preregistration. No measurements of this gate precede RED.

## Frozen experiment
Use the historical 12 states, candidate indices [13,16,22,25,27,29,37,39,46,50,66,77], without reselection. Use all 27 lexicographic weight-two raw Pauli sources P and all nine weight-one controls. H=P/2, U_s=cos(s/2)I-i sin(s/2)P, X=-i[H,rho]. Source labels are ordered update parameters, not fundamental time. All 27 unit-HS exact-weight-three h are probes; h is not an additional source memory. Y=DX[h]=-i[H,h]. Freeze s=1e-3, eta=1e-4, mixture weight p=.37. No new randomness.

For each state compute retained pair leakage L (raw pair moments), connected-correlation derivative including both one-body terms, pre-Sylvester skew Q, and polar rotational W. Stack three orthonormal skew coordinates per edge for Q/E. Publish aggregate Q/E matrices and singular spectra, per-source spectra, validity extrema and exact coverage.

Scientific prediction: each weight-two source has exactly 12 nonzero unit-HS Y, leakage rank 12, Q/E rank six, zero source-support-edge leakage and rank three on each other edge. Aggregate weight-two leakage rank 27 and Q/E rank nine. Aggregate weight-one retained leakage/Q/E rank zero. Rank thresholds are 1e-9,1e-10,1e-11 times the largest singular value of the corresponding aggregate weight-two map at that state (same reference for all submaps and local controls). All thresholds must agree. Nonzero Y cutoff 1e-10, norm-one tolerance 1e-12. Local aggregate norm relative to corresponding positive aggregate <=1e-10. Source-edge marginal norm <=1e-12. These structural predictions are scientific criteria, not validity conditions.

Validity controls: all 36 baseline source norms >1e-8 at all states; unitary residual <=1e-12; channel mixture affinity residual <=1e-12; centered source derivative equals sinc(s)Y with absolute error <=1e-10, and differs from Y by <=1e-6 max(1,||Y||); Sylvester residual <=1e-10. For every state, source, hidden direction, inspect rho +/- eta h and both +/-s updates of these states: density eigenvalue >=-1e-12, trace/Hermitian error <=1e-12, all connected edges positive-polar with minimum singular value >=.015. Mixture uses the two signed input probes. Disjoint singleton channel invariance <=1e-12 for weight-two sources. Nonfinite values, selection mismatch, missing coverage or failed numerical controls mean INVALID.

Verdicts: TWO_BODY_UNITARY_HIDDEN_ROTATION_CONFIRMED if valid and all scientific predictions hold; TWO_BODY_UNITARY_HIDDEN_ROTATION_NOT_CONFIRMED if valid but any prediction fails; INVALID otherwise. Tests accept either valid scientific outcome. No threshold changes after observation.

## Interpretation boundary
This is a specified two-body quantum interaction, not an interaction derived from recoverability. Unitarity establishes a fixed unconditioned CPTP source and mixture affinity; the generator contains no extracted polar geometry. The experiment tests operator-support transfer of hidden correlations. Responding regions overlap source support; disjoint exterior closure remains intact. It selects no unique physical source, changes no admissible-world law, and derives no gravity. Genesis Pin and ordered recoverability framing are unchanged. Historical verdicts remain unchanged.
