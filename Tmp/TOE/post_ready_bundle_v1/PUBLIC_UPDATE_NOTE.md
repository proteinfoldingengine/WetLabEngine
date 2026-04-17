# Public-Facing Update Note
## Restricted Affine Coupling Program — Current Status

This is a publish-safe update.

## What can be claimed now

The program now has a **restricted affine theorem shape**:

Delta Cov = a0 * Delta Var + b0 + epsilon

where:
- a0 and b0 come from baseline residual geometry
- epsilon is controlled by gain drift, curvature, and innovation

A full calibration pass was run on a user-supplied dataset, and the screened family stayed within the theorem-controlled bound on that run.

## What should NOT be claimed yet

This is not:
- universal closure
- a final proof
- a provenance-clean real-data result

## Strongest honest statement

A successful calibrated restricted-theorem pass has been demonstrated on the supplied dataset, and the next step is to reproduce the same result from a direct source-export run.
